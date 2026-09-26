"""
Phase 6 (Study 2) driver: paper_draft/phase6_method_study_protocol.md.

Subcommands
  tune       Stage L2 P11 tuning on TRAINING pools (§5.4) and the runtime
             projection of §14 on a training pool.     Guard: protocol L1 signed.
  main       single-wave study on TEST pools (§3 to §8): all arms, GSV, anchors,
             execution robustness, set-versus-sequence. Guard: L1 and L2 signed.
  warmstart  five-wave chains (§9); needs the G4-decided screening key from
             v0_6_phase6_gates.json.                    Guard: L1 and L2 signed.
  runtime    wall-clock study (§10).                    Guard: L1 and L2 signed.
  case       calibrated case (§11), needs --case-data.  Guard: L1 and L2 signed.

Candidates are evaluated per sequence signature (the ordered source,
destination, ready list that every evaluator sees); shortlists count distinct
signatures (§5.5). --des-subset switches on the §14 runtime contingency.

--selftest runs a toy version of any subcommand (toy configurations, toy seeds
far from every registered seed, tiny candidate sets) and writes only to the
scratch directory. It never touches a registered pool.

Run from prototype/:  python -m src.experiments_phase6 main --selftest
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import random
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from src import phase6_config as cfg
from src.demand_patterns import generate_pool
from src.des_evaluator import des_makespan
from src.features import compute_all_features
from src.phase6_policies import (apply_perm, concat_chain, first_k_distinct,
                                 local_search_budgeted, p10_permutation,
                                 p10g_permutation, p11_construct, p8_score,
                                 p9_predictions, ranked, signature, tie_ranks,
                                 tuples_of, wave_of)
from src.registration_guard import (REGISTRATIONS, STUDY2_L1, TOY_SEED_BASE,
                                    code_tree_sha256, front_matter_field,
                                    require_bundle, require_l2, scratch_dir,
                                    sha256_file)
from src.simulator import Order, simulate_wave
from src.wave_policies import (build_candidates, corner_positions,
                               favorable_label, fit_phi_beta)

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
EVALS = ("M1", "M2", "DES-M1", "DES-M2")
# §14 subset mode: fixed stream-97 offsets per distribution arm (re-ordered
# arms reuse their base arm's subsample and are therefore paired)
SUBSET_ARM_OFFSET = {"P0": 0, "P2": 1, "P5": 2, "P8-200": 3, "P9-200": 4,
                     "P0+P10": 0, "P5+P10": 2, "P8+P10": 3}


# --------------------------------------------------------------------------
# Provenance
# --------------------------------------------------------------------------

CODE_CHANGE_REF: Optional[str] = None        # set by --allow-code-change


def _versions() -> dict:
    import platform
    out = {"python": platform.python_version(), "numpy": np.__version__}
    for mod in ("scipy", "pandas"):
        try:
            out[mod] = __import__(mod).__version__
        except ImportError:
            out[mod] = "missing"
    return out


def provenance() -> dict:
    tree = code_tree_sha256()
    l2 = REGISTRATIONS["phase6_L2"]
    l2_code = front_matter_field(l2, "code_tree_sha256") if l2.exists() else ""
    return {"generated_utc": datetime.now(timezone.utc).isoformat(),
            "code_tree_sha256": tree,
            "protocol_L1_sha256": sha256_file(REGISTRATIONS["phase6"]),
            "L2_addendum_sha256": sha256_file(l2) if l2.exists() else None,
            "code_matches_L2": (tree == l2_code) if l2_code else None,
            "code_change_after_L2": CODE_CHANGE_REF,
            "versions": _versions()}


# --------------------------------------------------------------------------
# Evaluators (closed form and DES), with timing parameters
# --------------------------------------------------------------------------

class Evaluator:
    """Closed-form M1/M2, DES-M1/DES-M2, and the §7.3 robustness variants."""

    def __init__(self, config: dict, timing: Optional[dict] = None,
                 capacity: int = cfg.CAPACITY):
        timing = timing or {}
        self.A, self.E, self.c = config["n_amrs"], config["n_elevators"], capacity
        self.sim_kw = {k: timing[k] for k in
                       ("speed_per_floor", "load_time", "unload_time")
                       if timing.get(k) is not None}
        self.service = timing.get("service_time") or 5.0
        self.des_kw = {"speed_per_floor": self.sim_kw.get("speed_per_floor", 5.0),
                       "load_time": self.sim_kw.get("load_time", 2.0),
                       "unload_time": self.sim_kw.get("unload_time", 2.0),
                       "service_time": self.service}
        self.calls = {e: 0 for e in EVALS + ("robust",)}

    def __call__(self, orders, model: str) -> float:
        self.calls[model] += 1
        if model in ("M1", "M2"):
            return simulate_wave(wave_of(orders), n_amrs=self.A,
                                 n_elevators=self.E, capacity=self.c,
                                 batched=(model == "M2"),
                                 service_time=self.service, **self.sim_kw)
        return des_makespan(orders, self.A, self.E, self.c, model[-2:],
                            **self.des_kw)

    def robust(self, orders, sigma: float = 0.0, seed: Optional[int] = None,
               b5: bool = False) -> float:
        self.calls["robust"] += 1
        return des_makespan(orders, self.A, self.E, self.c, "M2", **self.des_kw,
                            b5_compat=b5, noise_sigma=sigma, noise_seed=seed)


# --------------------------------------------------------------------------
# Candidate sets (§3.4)
# --------------------------------------------------------------------------

def order_pool(config: dict, base: int, size_pool: int = cfg.ORDER_POOL_SIZE):
    seed = cfg.seed6(base, config["config_id"], cfg.STREAM["order_pool"], 0)
    return generate_pool(config["demand"], config["F"], size_pool, seed=seed,
                         **cfg.DEMAND_PARAMS[config["demand"]])


def p11_candidates(pool, n: int, k: int, weights, seed: int,
                   capacity: int = cfg.CAPACITY) -> List[Tuple[int, ...]]:
    src = np.array([o.source_floor for o in pool])
    dst = np.array([o.dest_floor for o in pool])
    out = []
    for j in range(k):
        rng = random.Random(seed + 7919 * (j + 1))
        seq = p11_construct(src, dst, n, capacity, *weights, rng)
        out.append(apply_perm(seq, p10_permutation(tuples_of(pool, seq),
                                                    capacity)))
    return out


def build_G(pool, config: dict, base: int, n: int, K: int, K11: int, weights):
    cid = config["config_id"]
    cand = build_candidates(pool, n, K, random.Random(
        cfg.seed6(base, cid, cfg.STREAM["random_candidates"], n)))
    R = [tuple(x) for x in cand["idxs"]]
    P10 = [apply_perm(ix, p10_permutation(tuples_of(pool, ix))) for ix in R]
    P11 = p11_candidates(pool, n, K11, weights,
                         cfg.seed6(base, cid, cfg.STREAM["p11"], n))
    G = R + P10 + P11
    source = np.array(["R"] * len(R) + ["P10"] * len(P10) + ["P11"] * len(P11))
    parent = np.array(list(range(len(R))) + list(range(len(R))) + [-1] * len(P11))
    return cand, G, source, parent


class SigTable:
    """Distinct sequence signatures and their evaluator values (lazy)."""

    def __init__(self, pool, ev: Evaluator):
        self.pool, self.ev = pool, ev
        self.index: Dict[tuple, int] = {}
        self.orders: List[list] = []
        self.val: Dict[str, Dict[int, float]] = {e: {} for e in EVALS}

    def sid(self, ix) -> int:
        s = signature(self.pool, ix)
        if s not in self.index:
            self.index[s] = len(self.orders)
            self.orders.append(list(s))
        return self.index[s]

    def get(self, sid: int, model: str) -> float:
        if sid not in self.val[model]:
            self.val[model][sid] = self.ev(self.orders[sid], model)
        return self.val[model][sid]


# --------------------------------------------------------------------------
# One decision (§4 to §7.3)
# --------------------------------------------------------------------------

def _median(v) -> float:
    return float(np.median(np.asarray(v, dtype=float)))


def _best(values: np.ndarray, positions: Sequence[int], ties: np.ndarray) -> int:
    pos = np.asarray(positions, dtype=int)
    return int(pos[np.lexsort((ties[pos], values[pos]))[0]])


def _n_tied(values, target: float) -> int:
    return int(np.sum(np.abs(np.asarray(values, dtype=float) - target) <= 1e-9))


def _first_k_distinct_scanned(order, sig_ids, k: int) -> Tuple[List[int], int]:
    """first_k_distinct plus the number of positions of `order` walked to
    reach k distinct signatures (the candidates scanned of protocol §5.5);
    the whole order counts when it holds fewer than k distinct signatures."""
    short = first_k_distinct(order, sig_ids, k)
    if len(short) < k:
        return short, int(len(order))
    return short, int(np.flatnonzero(np.asarray(order) == short[-1])[0]) + 1


def run_decision(config: dict, base: int, n: int, *, K: int, K11: int,
                 weights, timing=None, gsv_k=cfg.GSV_K,
                 p7_budget=cfg.P7_MATCHED_BUDGET, p7_verify=cfg.P7_MATCHED_VERIFY,
                 seqvar=(cfg.SEQVAR_CANDIDATES, cfg.SEQVAR_PERMUTATIONS),
                 robust=(cfg.ROBUST_SIGMAS, cfg.ROBUST_REPS, cfg.ROBUST_SUBSAMPLE),
                 des_subset=None, pool=None) -> Tuple[dict, list]:
    """des_subset: None (full DES enumeration) or (top, random, per-arm) sizes
    for the §14 contingency."""
    t0 = time.perf_counter()
    cid = config["config_id"]
    pool = pool if pool is not None else order_pool(config, base)
    ev = Evaluator(config, timing)
    st = SigTable(pool, ev)
    cand, G, source, parent = build_G(pool, config, base, n, K, K11, weights)
    nG = len(G)
    sig = np.array([st.sid(ix) for ix in G])
    isR, isP10, isP11 = source == "R", source == "P10", source == "P11"
    Rpos = np.flatnonzero(isR)
    t_gen = time.perf_counter()

    # ---- phase 1: closed form for every distinct signature of G ------------
    M1 = np.array([st.get(s, "M1") for s in sig])
    M2 = np.array([st.get(s, "M2") for s in sig])
    ties = tie_ranks(nG, random.Random(cfg.seed6(base, cid, cfg.STREAM["ties"], n)))
    to_p10 = {int(parent[g]): int(g) for g in np.flatnonzero(isP10)}

    # ---- phase 2: position sets of every arm ------------------------------
    cf = cand["cross_floor"].to_numpy()
    pos_P2 = Rpos[cf <= np.quantile(cf, 0.25)]
    rng94 = random.Random(cfg.seed6(base, cid, cfg.STREAM["training_sample"], n))
    tr = [rng94.randrange(len(Rpos)) for _ in range(min(cfg.TRAIN_SAMPLE, len(Rpos)))]
    fav = favorable_label(fit_phi_beta(cand.iloc[tr], M2[Rpos][tr]))
    try:
        corner = corner_positions(cand, fav)
    except ValueError:                        # empty favourable corner: recorded
        corner = None
    p8 = np.array([p8_score(tuples_of(pool, G[g])) for g in Rpos])
    p8_rank = Rpos[np.lexsort((ties[Rpos], p8))]
    pred9 = p9_predictions(cand[["C", "I", "T"]].to_numpy(float), tr,
                           M2[Rpos][tr], cfg.P9_HYPER)
    p9_rank = Rpos[np.lexsort((ties[Rpos], pred9))]
    p8v_short = first_k_distinct([to_p10[int(g)] for g in p8_rank], sig,
                                 cfg.P8_VERIFY_K)
    p11pos = np.flatnonzero(isP11)
    k_grid = sorted(set(gsv_k))
    masks = {"G": np.ones(nG, dtype=bool), "R": isR, "R+P10": isR | isP10,
             "R+P11": isR | isP11}
    key_max = np.where(isR, M2, np.maximum(M1, M2))
    orders_by_key = {"M2": ranked(M2, ties), "max": ranked(key_max, ties)}
    shortlists: Dict[Tuple[str, str], Dict[int, List[int]]] = {}
    scanned: Dict[Tuple[str, str], Dict[int, int]] = {}    # candidates scanned
    for key, order in orders_by_key.items():
        for name, mask in masks.items():
            if key == "max" and name == "R":          # R has no P10/P11 part
                continue
            o = order[mask[order]]
            sl = {k: _first_k_distinct_scanned(o, sig, k) for k in k_grid}
            shortlists[(key, name)] = {k: short for k, (short, _) in sl.items()}
            scanned[(key, name)] = {k: c for k, (_, c) in sl.items()}
    perm_R = list(Rpos)
    random.Random(cfg.seed6(base, cid, cfg.STREAM["r_verify"], n)).shuffle(perm_R)
    rv = {k: _first_k_distinct_scanned(perm_R, sig, k) for k in k_grid}
    rverify_short = {k: short for k, (short, _) in rv.items()}
    rverify_scanned = {k: c for k, (_, c) in rv.items()}

    # ---- phase 3: DES-M1 and DES-M2 (full, or the §14 subset) --------------
    dist_sub = None
    if des_subset is None:
        des_sids = np.unique(sig)
    else:
        top_n, rand_n, arm_n = des_subset
        rng97 = random.Random(cfg.seed6(base, cid, cfg.STREAM["des_subset"], n))
        need = set(sig[first_k_distinct(orders_by_key["M2"], sig, top_n)].tolist())
        need |= set(sig[first_k_distinct(orders_by_key["max"], sig, top_n)].tolist())
        # DL_M1 needs the M1 optimum inside the evaluated subset
        need |= set(sig[first_k_distinct(ranked(M1, ties), sig, top_n)].tolist())
        need |= set(sig[np.flatnonzero(M1 <= M1.min() + 1e-9)].tolist())
        uniq = sorted(set(sig.tolist()))
        need |= set(rng97.sample(uniq, min(rand_n, len(uniq))))
        small_k = [k for k in k_grid if k <= 100]
        for sl in list(shortlists.values()) + [rverify_short]:
            for k in small_k:
                need |= set(sig[sl[k]].tolist())
        need |= set(sig[p8v_short].tolist())

        def dist_sub(pos, j):
            # fixed per-arm offset j (SUBSET_ARM_OFFSET), independent of the
            # order in which arms are computed
            pos = [int(p) for p in pos]
            r = random.Random(cfg.seed6(base, cid, cfg.STREAM["des_subset"], n)
                              + 101 * (j + 1))
            return pos if len(pos) <= arm_n else r.sample(pos, arm_n)
        des_sids = np.array(sorted(need))
    for s in des_sids:
        st.get(int(s), "DES-M2")
        st.get(int(s), "DES-M1")

    def des_arrays():
        d2 = np.array([st.val["DES-M2"].get(int(s), np.nan) for s in sig])
        d1 = np.array([st.val["DES-M1"].get(int(s), np.nan) for s in sig])
        return d2, d1

    D2, D1 = des_arrays()
    have = ~np.isnan(D2)
    t_eval = time.perf_counter()

    # ---- phase 4: arm values ----------------------------------------------
    def fill(positions):
        for g in positions:                              # evaluate if missing
            if np.isnan(D2[g]):
                D2[g] = st.get(int(sig[g]), "DES-M2")
                D1[g] = st.get(int(sig[g]), "DES-M1")

    def dist(name, positions, paired_from=None):
        """Distribution arm. In the §14 subset mode a fixed 200-candidate
        subsample (offset SUBSET_ARM_OFFSET[name]) is used; a re-ordered arm
        (paired_from = (base positions, mapping)) uses the images of its base
        arm's subsample, so the two stay paired."""
        positions = np.asarray(positions, dtype=int)
        if dist_sub is not None:
            if paired_from is None:
                positions = np.asarray(dist_sub(positions, SUBSET_ARM_OFFSET[name]),
                                       dtype=int)
            else:
                base_pos, mapping = paired_from
                sub = dist_sub(base_pos, SUBSET_ARM_OFFSET[name])
                positions = np.asarray([mapping(g) for g in sub], dtype=int)
            fill(positions)
        return {"DES-M2": _median(D2[positions]), "M2": _median(M2[positions]),
                "n": int(len(positions))}

    def single(g):
        g = int(g)
        if np.isnan(D2[g]):
            D2[g] = st.get(int(sig[g]), "DES-M2")
            D1[g] = st.get(int(sig[g]), "DES-M1")
        return {"DES-M2": float(D2[g]), "M2": float(M2[g]), "pos": g,
                "source": str(source[g])}

    arms: Dict[str, dict] = {"P0": dist("P0", Rpos), "P2": dist("P2", pos_P2)}
    if corner is not None:
        arms["P5"] = {**dist("P5", Rpos[corner]), "favorable_corner": fav}
        arms["P5+P10"] = dist("P5+P10", [to_p10[int(i)] for i in corner],
                              paired_from=(Rpos[corner], lambda g: to_p10[int(g)]))
    else:
        arms["P5"] = {"error": "empty favourable corner", "favorable_corner": fav}
    arms["P8-200"] = dist("P8-200", p8_rank[:cfg.P8_K])
    arms["P8-1"] = single(p8_rank[0])
    g8v = _best(D2, p8v_short, ties)
    arms["P8-verify"] = {**single(g8v), "k_distinct": len(p8v_short),
                         "ties_at_release": _n_tied(D2[p8v_short], D2[g8v])}
    arms["P9-200"] = dist("P9-200", p9_rank[:cfg.P9_HYPER["k_deploy"]])
    arms["P9-1"] = single(p9_rank[0])
    arms["P0+P10"] = dist("P0+P10", [to_p10[i] for i in range(len(Rpos))],
                          paired_from=(Rpos, lambda g: to_p10[int(g)]))
    arms["P8+P10"] = dist("P8+P10", [to_p10[int(g)] for g in p8_rank[:cfg.P8_K]],
                          paired_from=(p8_rank[:cfg.P8_K], lambda g: to_p10[int(g)]))
    # P0+P10g (outside G): evaluated by signature, sharing runs with G; in the
    # subset mode it uses the P0 subsample (paired)
    g10_pos = (list(Rpos) if dist_sub is None
               else dist_sub(Rpos, SUBSET_ARM_OFFSET["P0"]))
    g10_eval = [st.sid(apply_perm(G[g], p10g_permutation(tuples_of(pool, G[g]))))
                for g in g10_pos]
    arms["P0+P10g"] = {"DES-M2": _median([st.get(s, "DES-M2") for s in g10_eval]),
                       "M2": _median([st.get(s, "M2") for s in g10_eval]),
                       "n": len(g10_eval)}
    arms["P11-1"] = single(_best(M2, p11pos, ties))
    arms["P11-1"]["n_distinct_P11"] = int(len(set(sig[p11pos].tolist())))

    # local search: P7-matched (the M2 budget includes the P10 end-point hook)
    def m2_of(ix):
        return st.get(st.sid(ix), "M2")

    def hook(ix):
        ix2 = apply_perm(ix, p10_permutation(tuples_of(pool, ix)))
        return m2_of(ix2), ix2

    ends, spent, extras = local_search_budgeted(
        len(pool), n, m2_of, random.Random(cfg.seed6(base, cid, cfg.STREAM["p7"], n)),
        budget=p7_budget, n_iter=cfg.P7_ITER, end_hook=hook)
    run8 = [ix for _, ix in ends[:cfg.P7_RUNS]]
    arms["P7-run"] = {"DES-M2": _median([st.get(st.sid(ix), "DES-M2") for ix in run8]),
                      "M2": _median([v for v, _ in ends[:cfg.P7_RUNS]]),
                      "n": len(run8)}
    found = []                                         # discovery order
    for i, (v, ix) in enumerate(ends):
        found.append((v, ix, False))
        if i < len(extras):
            found.append((extras[i][0], extras[i][1], True))
    seen, short7 = set(), []
    for rank, (v, ix, is10) in sorted(enumerate(found), key=lambda t: (t[1][0], t[0])):
        s = st.sid(ix)
        if s not in seen:
            seen.add(s)
            short7.append((rank, s, is10))
        if len(short7) == p7_verify:
            break
    ver7 = sorted((st.get(s, "DES-M2"), rank, s, is10) for rank, s, is10 in short7)
    best7 = ver7[0]
    arms["P7-matched"] = {"DES-M2": float(best7[0]), "M2": float(st.get(best7[2], "M2")),
                          "m2_evaluations": int(spent), "des_evaluations": len(ver7),
                          "n_runs": len(ends), "released_is_P10": bool(best7[3]),
                          "ties_at_release": sum(abs(v[0] - best7[0]) <= 1e-9
                                                 for v in ver7)}

    # GSV, R-verify, ablations, anchors (values rebuilt by signature, so a
    # signature evaluated through any position counts everywhere)
    D2n, D1n = des_arrays()
    D2 = np.where(np.isnan(D2), D2n, D2)
    D1 = np.where(np.isnan(D1), D1n, D1)
    opt_G = float(np.nanmin(D2))
    opt_R = float(np.nanmin(D2[Rpos]))
    tol_G = max(cfg.REGRET_TOL_REL, cfg.REGRET_TOL_ABS / opt_G)
    tol_R = max(cfg.REGRET_TOL_REL, cfg.REGRET_TOL_ABS / opt_R)

    def released(short, order_values, n_scanned):
        for g in short:
            single(g)                                    # DES for every entry
        g = _best(D2, short, ties)
        bound = order_values[short[-1]]
        return {"DES-M2": float(D2[g]), "M2": float(M2[g]), "pos": int(g),
                "source": str(source[g]), "k_actual": len(short),
                "n_scanned": int(n_scanned),
                "regret": float((D2[g] - opt_G) / opt_G),
                "regret_R": float((D2[g] - opt_R) / opt_R),
                "ties_screen_boundary": _n_tied(order_values, bound),
                "ties_at_release": _n_tied(D2[short], D2[g])}

    def within_subset(short):
        # §14 subset mode: shortlists longer than 100 are restricted to the
        # evaluated subset (G3, G8, and the anchors are defined on it)
        if dist_sub is None or len(short) <= 100:
            return short
        return [g for g in short if not np.isnan(D2[g])]

    gsv_res: Dict[str, Dict[str, dict]] = {}
    for (key, name), sl in shortlists.items():
        vals = M2 if key == "M2" else key_max
        label = name if key == "M2" else f"{name}_maxkey"
        gsv_res[label] = {str(k): released(within_subset(s), vals,
                                           scanned[(key, name)][k])
                          for k, s in sl.items()}
    rverify = {str(k): released(within_subset(s), M2, rverify_scanned[k])
               for k, s in rverify_short.items()}

    def first_k(label, rel="regret", tol=tol_G):
        return next((k for k in k_grid if gsv_res[label][str(k)][rel] <= tol), None)

    kstar = {"M2": first_k("G"), "max": first_k("G_maxkey"),
             "M2_vs_R_opt": first_k("G", "regret_R", tol_R),
             "max_vs_R_opt": first_k("G_maxkey", "regret_R", tol_R)}
    have = ~np.isnan(D2)

    def dl(values):
        v = np.where(have, values, np.nan)
        m = np.nanmin(v)
        tied = np.flatnonzero(np.abs(v - m) <= 1e-9)
        return {"DL": float((np.nanmean(D2[tied]) - opt_G) / opt_G),
                "n_tied": int(len(tied))}

    anchors = {"M2_opt_G": gsv_res["G"]["1"], "DES-M2_opt_G": opt_G,
               "DES-M2_opt_R": opt_R, "tolerance_G": tol_G,
               "des_subset": des_subset is not None,
               "n_des_evaluated_signatures": int(len(st.val["DES-M2"]))}
    ladder = {"M1": dl(M1), "M2": dl(M2), "DES-M1": dl(D1)}
    ordering = {}
    for src in ("R", "P10", "P11"):
        m = source == src
        hm = m & have & ~np.isnan(D1)
        first = {}
        for g in np.flatnonzero(m):
            first.setdefault(int(sig[g]), g)
        dpos = np.array(sorted(first.values()), dtype=int)
        ordering[src] = {"M1<=M2": int(np.sum(M1[m] <= M2[m] + 1e-9)),
                         "n": int(m.sum()),
                         "M1<=M2_distinct": int(np.sum(M1[dpos] <= M2[dpos] + 1e-9))
                         if len(dpos) else 0,
                         "DES-M1<=DES-M2": int(np.sum(D1[hm] <= D2[hm] + 1e-9)),
                         "n_des": int(hm.sum()),
                         "n_distinct": int(len(set(sig[m].tolist())))}
    t_arms = time.perf_counter()

    # ---- §7.3 execution robustness of released waves -----------------------
    sigmas, reps, n_sub = robust
    nseed = cfg.seed6(base, cid, cfg.STREAM["noise"], n)
    head = str(cfg.GSV_HEADLINE_K) if str(cfg.GSV_HEADLINE_K) in gsv_res["G"] \
        else str(max(k_grid))
    rel_sids = {"GSV20": sig[gsv_res["G"][head]["pos"]],
                "GSV20_maxkey": sig[gsv_res["G_maxkey"][head]["pos"]],
                "GSV1": sig[gsv_res["G"]["1"]["pos"]], "P8-verify": sig[g8v],
                "P8-1": sig[int(p8_rank[0])], "P9-1": sig[int(p9_rank[0])],
                "P11-1": sig[arms["P11-1"]["pos"]], "P7-matched": best7[2]}

    def robust_of(s):
        o = st.orders[int(s)]
        out = {"sigma0": ev.robust(o)}                  # deterministic DES-M2
        out.update({f"sigma{x}": float(np.mean([ev.robust(o, x, nseed + r)
                                                for r in range(reps)]))
                    for x in sigmas})
        out["b5"] = ev.robust(o, b5=True)
        return out

    rob = {name: robust_of(s) for name, s in rel_sids.items()}
    sub_rng = random.Random(cfg.seed6(base, cid, cfg.STREAM["robust_subsample"], n))
    sub0 = sub_rng.sample(list(Rpos), min(n_sub, len(Rpos)))
    r0 = [robust_of(sig[g]) for g in sub0]
    r10 = [robust_of(sig[to_p10[int(g)]]) for g in sub0]
    rob["P0_sub_median"] = {k: _median([x[k] for x in r0]) for k in r0[0]}
    rob["P0+P10_sub_median"] = {k: _median([x[k] for x in r10]) for k in r10[0]}
    t_rob = time.perf_counter()

    sv = set_vs_sequence(pool, G, Rpos, ev, base, cid, n, *seqvar)
    t_sv = time.perf_counter()
    summary = {
        "config_id": cid, "base": base, "size": n, "nG": nG,
        "n_distinct_signatures_G": int(len(set(sig.tolist()))),
        "arms": arms, "gsv": gsv_res, "r_verify": rverify, "k_star": kstar,
        "anchors": anchors, "ladder": ladder, "ordering": ordering,
        "robust": rob, "seqvar": sv,
        "ties": {"M2_min": _n_tied(M2, M2.min()),
                 "P8_rank1": _n_tied(p8, p8.min()),
                 "P8_boundary_200": _n_tied(p8, np.sort(p8)[min(cfg.P8_K, len(p8)) - 1]),
                 "P9_rank1": _n_tied(pred9, pred9.min())},
        "evaluator_calls": dict(ev.calls),
        "seconds": {"generate": t_gen - t0, "enumerate": t_eval - t_gen,
                    "arms": t_arms - t_eval, "robust": t_rob - t_arms,
                    "seqvar": t_sv - t_rob},
    }
    feats = _features_for(G, pool, cand, source, parent)
    rows = [(cid, base, n, g, str(source[g]), int(parent[g]), int(sig[g]),
             M1[g], M2[g], D1[g], D2[g], *feats[g]) for g in range(nG)]
    return summary, rows


def _features_for(G, pool, cand, source, parent):
    cols = ("C", "I", "T", "cross_floor")
    base = cand[list(cols)].to_numpy(float)
    out = []
    for g, ix in enumerate(G):
        if source[g] in ("R", "P10"):
            out.append(tuple(base[parent[g]]))
        else:
            f = compute_all_features(wave_of(tuples_of(pool, ix)))
            out.append(tuple(float(f[c]) for c in cols))
    return out


def set_vs_sequence(pool, G, Rpos, ev: Evaluator, base, cid, n, n_cand, n_perm):
    rng91 = random.Random(cfg.seed6(base, cid, cfg.STREAM["seqvar_draw"], n))
    rng92 = random.Random(cfg.seed6(base, cid, cfg.STREAM["permutations"], n))
    picks = rng91.sample(list(Rpos), min(n_cand, len(Rpos)))
    groups = {"M2": [], "DES-M2": []}
    for g in picks:
        seqs = [list(G[g])]
        for _ in range(n_perm):
            s = list(G[g])
            rng92.shuffle(s)
            seqs.append(s)
        for model in ("M2", "DES-M2"):
            groups[model].append([ev(tuples_of(pool, s), model) for s in seqs])
    out = {}
    for model, rows in groups.items():
        y = np.asarray(rows, dtype=float)              # candidates x sequences
        m = y.shape[1]
        msw = float(((y - y.mean(axis=1, keepdims=True)) ** 2).sum()
                    / (y.shape[0] * (m - 1)))
        msb = float(m * ((y.mean(axis=1) - y.mean()) ** 2).sum() / (y.shape[0] - 1))
        s2b = max(0.0, (msb - msw) / m)
        out[model] = {"sigma2_within": msw, "sigma2_between": s2b,
                      "share_sequence": msw / (msw + s2b) if msw + s2b > 0 else None,
                      "n_candidates": int(y.shape[0]), "n_sequences": int(m)}
    return out


# --------------------------------------------------------------------------
# Stage L2 tuning (§5.4) and runtime projection (§14)
# --------------------------------------------------------------------------

def tune_instance(config, base, n, K, K11, grid):
    pool = order_pool(config, base)
    ev = Evaluator(config)
    cid = config["config_id"]
    cand = build_candidates(pool, n, K, random.Random(
        cfg.seed6(base, cid, cfg.STREAM["random_candidates"], n)))
    med_R = _median([ev(tuples_of(pool, tuple(ix)), "M2") for ix in cand["idxs"]])
    seed = cfg.seed6(base, cid, cfg.STREAM["p11"], n)
    out = {}
    for w in grid:
        vals = [ev(tuples_of(pool, ix), "M2")
                for ix in p11_candidates(pool, n, K11, w, seed)]
        out[w] = float(np.quantile(vals, cfg.P11_TUNE_QUANTILE)) / med_R
    return out


def runtime_projection(config, base, sizes, kw) -> dict:
    """Time full decisions on a TRAINING pool; project the main study (§14).
    Only wall-clock times are kept; no value from this run is stored."""
    secs = {}
    for n in sizes:
        t0 = time.perf_counter()
        run_decision(config, base, n, **kw)
        secs[n] = time.perf_counter() - t0
    per_pool = sum(secs.values())
    hours = per_pool * len(cfg.CONFIGS) * len(cfg.TEST_POOL_BASES) / 3600.0
    return {"config_id": config["config_id"], "base": base, "seconds_by_size": secs,
            "projected_hours_main": hours,
            "subset_mode_triggered": bool(hours > cfg.RUNTIME_LIMIT_HOURS)}


# --------------------------------------------------------------------------
# Warm start (§9)
# --------------------------------------------------------------------------

def run_chain(config, base, arm, j, variant, *, K, K11, weights, key="M2",
              pool=None, timing=None, steps=cfg.WARM_STEPS, n=cfg.WARM_SIZE,
              g5a=cfg.WARM_G5A_SAMPLE, fav=None):
    cid = config["config_id"]
    pool = pool if pool is not None else order_pool(config, base)
    ev = Evaluator(config, timing)
    released: List[Tuple[int, ...]] = []
    epochs: List[float] = []
    remaining = list(range(len(pool)))
    log = []
    g5 = {"R": [0, 0], "P11": [0, 0]}
    epoch, prev_c, stopped = 0.0, 0.0, None
    for s in range(1, steps + 1):
        screen = None                     # GSV arm: k verified, candidates scanned
        seed = (cfg.seed6(base, cid, cfg.STREAM["warm_start"] + s, n)
                + 1000 * cfg.WARM_ARM_INDEX[arm] + 100 * j)
        rng = random.Random(seed)
        sub = [pool[i] for i in remaining]
        cand = build_candidates(sub, n, K, rng)
        R = [tuple(remaining[i] for i in ix) for ix in cand["idxs"]]
        if arm == "P0":
            pick = R[rng.randrange(len(R))]
        elif arm == "P5":
            try:
                pos = corner_positions(cand, fav)
            except ValueError:
                stopped = f"empty favourable corner at step {s}"
                break
            pick = R[int(pos[rng.randrange(len(pos))])]
        else:                                           # GSV(20), headline key
            P10 = [apply_perm(ix, p10_permutation(tuples_of(pool, ix))) for ix in R]
            P11 = [tuple(remaining[i] for i in ix) for ix in
                   p11_candidates(sub, n, K11, weights, seed + 1)]
            Gs = R + P10 + P11
            prefix = concat_chain(pool, released, epochs)
            memo: Dict[Tuple[tuple, str], float] = {}

            def after(ix, model):
                sg = signature(pool, ix)
                if (sg, model) not in memo:
                    memo[(sg, model)] = ev(prefix + [(a, b, epoch + r)
                                                     for a, b, r in sg], model)
                return memo[(sg, model)]

            src = np.array(["R"] * len(R) + ["P10"] * len(P10) + ["P11"] * len(P11))
            m2 = np.array([after(ix, "M2") for ix in Gs])
            if key == "max":
                m1 = np.array([after(ix, "M1") if src[g] != "R" else m2[g]
                               for g, ix in enumerate(Gs)])
                keyv = np.where(src == "R", m2, np.maximum(m1, m2))
            else:
                keyv = m2
            ties = tie_ranks(len(Gs), random.Random(seed + 2))
            sig_id: Dict[tuple, int] = {}
            sids = [sig_id.setdefault(signature(pool, ix), len(sig_id)) for ix in Gs]
            short, n_scanned = _first_k_distinct_scanned(ranked(keyv, ties), sids,
                                                         cfg.GSV_HEADLINE_K)
            screen = {"k_actual": len(short), "n_scanned": n_scanned}
            d2 = {g: after(Gs[g], "DES-M2") for g in short}
            pick = Gs[min(d2, key=lambda g: (d2[g], ties[g]))]
            if s >= 2:
                samp = random.Random(seed + 3).sample(range(len(R)), min(g5a, len(R)))
                for g in samp:                           # G5(a): random part R_s
                    g5["R"][0] += after(Gs[g], "M1") <= m2[g] + 1e-9
                g5["R"][1] += len(samp)
                for g in np.flatnonzero(src == "P11"):   # descriptive
                    g5["P11"][0] += after(Gs[g], "M1") <= m2[g] + 1e-9
                    g5["P11"][1] += 1
        released.append(pick)
        epochs.append(epoch)
        orders = concat_chain(pool, released, epochs)
        c_des = ev(orders, "DES-M2")
        c_m2 = ev(orders, "M2")
        log.append({"step": s, "epoch": epoch, "C_DES-M2": c_des, "C_M2": c_m2,
                    "increment_DES-M2": c_des - prev_c, "screen": screen})
        prev_c = c_des
        rel = set(pick)
        remaining = [i for i in remaining if i not in rel]
        epoch = (c_des if variant == "A"
                 else epoch + cfg.WARM_VARIANT_B_FRACTION * (c_des - epoch))
    return {"config_id": cid, "base": base, "arm": arm, "replicate": j,
            "variant": variant, "key": key, "steps": log, "stopped": stopped,
            "C5_DES-M2": log[-1]["C_DES-M2"] if log and not stopped else None,
            "g5a_hits": int(g5["R"][0]), "g5a_n": int(g5["R"][1]),
            "g5a_P11_hits": int(g5["P11"][0]), "g5a_P11_n": int(g5["P11"][1])}


# --------------------------------------------------------------------------
# Calibrated case (§11): order mapping, tested on synthetic data
# --------------------------------------------------------------------------

def case_pool_from_lines(lines, F: int, n_orders: int, rng: random.Random,
                         outbound_share: float = cfg.CASE_OUTBOUND_SHARE,
                         ready_horizon: Optional[float] = None) -> List[Order]:
    """Map cleaned invoice lines [(stock_code, sortable invoice time)] of one
    day to loads (§11.2). Storage floor = 2 + (SHA-256(stock code) mod (F - 1))."""
    picks = rng.sample(range(len(lines)), n_orders)
    chosen = [lines[i] for i in picks]
    if ready_horizon is not None:
        order = sorted(range(n_orders), key=lambda k: (chosen[k][1], picks[k]))
        rank = {k: r for r, k in enumerate(order)}
    pool = []
    for k, (code, _t) in enumerate(chosen):
        h = int(hashlib.sha256(str(code).encode("utf-8")).hexdigest(), 16)
        storage = 2 + h % (F - 1)
        outbound = rng.random() < outbound_share
        s, d = (storage, 1) if outbound else (1, storage)
        r = (ready_horizon * rank[k] / max(1, n_orders - 1)
             if ready_horizon is not None else 0.0)
        pool.append(Order(id=k, source_floor=s, dest_floor=d, release_time=r))
    return pool


# --------------------------------------------------------------------------
# Commands
# --------------------------------------------------------------------------

TOY_CONFIGS = [
    {"config_id": 901, "F": 5, "n_amrs": 5, "n_elevators": 2, "demand": "uniform"},
    {"config_id": 902, "F": 3, "n_amrs": 15, "n_elevators": 1, "demand": "diurnal"},
]
TOY = {"bases": [TOY_SEED_BASE + 1, TOY_SEED_BASE + 2], "sizes": [8, 16],
       "K": 120, "K11": 20, "weights": (2.0, 1.0, 0.5), "gsv_k": [1, 5, 10, 20, 260],
       "p7_budget": 260, "p7_verify": 20, "seqvar": (10, 5),
       "robust": ([0.1, 0.2], 3, 10), "subset": (30, 30, 20)}


def toy_kw() -> dict:
    return dict(K=TOY["K"], K11=TOY["K11"], weights=TOY["weights"],
                gsv_k=TOY["gsv_k"], p7_budget=TOY["p7_budget"],
                p7_verify=TOY["p7_verify"], seqvar=TOY["seqvar"],
                robust=TOY["robust"])


def _real_weights():
    w = cfg.p11_weights()
    if w is None:
        raise SystemExit("p11_weights is empty in the L2 addendum: complete "
                         "Stage L2 first.")
    return w


def _write_json(obj, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=1, default=float), encoding="utf-8")


def _write_rows(rows, path: Path, header) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(path, "wt", encoding="utf-8") as f:
        f.write(",".join(header) + "\n")
        for r in rows:
            f.write(",".join(str(x) for x in r) + "\n")


ROW_HEADER = ["config_id", "base", "size", "cand", "source", "parent", "sig",
              "M1", "M2", "DES_M1", "DES_M2", "C", "I", "T", "cross_floor"]


def _guard_l2(args) -> None:
    """Stage L2 guard; records a logged code-change reference if one is given."""
    global CODE_CHANGE_REF
    CODE_CHANGE_REF = require_l2(args.selftest,
                                 allow_code_change=args.allow_code_change)


def _part_paths(out_dir: Path, tag: str, cid: int):
    return (out_dir / f"{tag}v0_6_phase6_main_part_c{cid:03d}.json",
            out_dir / "raw" / f"{tag}mvs_v0_6_phase6_candidates_part_c{cid:03d}.csv.gz")


def cmd_main(args) -> None:
    """Runs configuration by configuration, writing one checkpoint part per
    configuration (existing parts are kept unless --redo), then merges when
    every configuration of the design is present."""
    _guard_l2(args)
    subset = None
    if args.selftest:
        configs, bases, sizes, kw = TOY_CONFIGS, TOY["bases"], TOY["sizes"], toy_kw()
        subset = TOY["subset"] if args.des_subset else None
        out_dir = scratch_dir()
        design = [c["config_id"] for c in TOY_CONFIGS]
    else:
        if args.des_subset:
            raise SystemExit("The §14 subset mode is set in the L2 addendum "
                             "(des_subset_mode), not on the command line.")
        configs = [c for c in cfg.CONFIGS
                   if not args.configs or c["config_id"] in args.configs]
        bases, sizes = cfg.TEST_POOL_BASES, cfg.SIZES
        kw = dict(K=cfg.K_RANDOM, K11=cfg.K_P11, weights=_real_weights())
        if cfg.des_subset_mode():
            subset = (cfg.DES_SUBSET_TOP, cfg.DES_SUBSET_RANDOM, cfg.TRAIN_SAMPLE)
        out_dir = RESULTS
        design = [c["config_id"] for c in cfg.CONFIGS]
    tag = "selftest_" if args.selftest else ""
    for config in configs:
        jpath, cpath = _part_paths(out_dir, tag, config["config_id"])
        if jpath.exists() and not args.redo:
            print(f"  cfg {config['config_id']}: part exists, kept")
            continue
        summaries, rows = [], []
        for base in bases:
            pool = order_pool(config, base)
            for n in sizes:
                s, r = run_decision(config, base, n, pool=pool, des_subset=subset, **kw)
                summaries.append(s)
                rows += r
        _write_json({"meta": {**provenance(), "selftest": args.selftest,
                              "des_subset": subset, "config_id": config["config_id"]},
                     "decisions": summaries}, jpath)
        _write_rows(rows, cpath, ROW_HEADER)
        print(f"  cfg {config['config_id']}: {len(summaries)} decisions written")
    if all(_part_paths(out_dir, tag, cid)[0].exists() for cid in design):
        merge_parts(out_dir, tag, design, len(bases) * len(sizes))


def merge_parts(out_dir: Path, tag: str, design: List[int], per_config: int) -> None:
    """Combine the per-configuration parts; stop unless every decision of the
    design is present exactly once."""
    decisions, metas = [], []
    for cid in design:
        d = json.loads(_part_paths(out_dir, tag, cid)[0].read_text("utf-8"))
        decisions += d["decisions"]
        metas.append(d["meta"])
    keys = [(d["config_id"], d["base"], d["size"]) for d in decisions]
    if len(keys) != len(set(keys)) or len(keys) != len(design) * per_config:
        raise SystemExit(f"merge stopped: {len(keys)} decisions, "
                         f"{len(set(keys))} distinct, expected "
                         f"{len(design) * per_config}")
    trees = {m["code_tree_sha256"] for m in metas}
    _write_json({"meta": {**provenance(), "selftest": tag == "selftest_",
                          "parts_code_tree_sha256": sorted(trees),
                          "n_decisions": len(decisions)}, "decisions": decisions},
                out_dir / f"{tag}v0_6_phase6_main.json")
    raw = out_dir / "raw" / f"{tag}mvs_v0_6_phase6_candidates.csv.gz"
    with gzip.open(raw, "wt", encoding="utf-8") as fo:
        fo.write(",".join(ROW_HEADER) + "\n")
        for cid in design:
            with gzip.open(_part_paths(out_dir, tag, cid)[1], "rt",
                           encoding="utf-8") as fi:
                next(fi)
                for line in fi:
                    fo.write(line)
    print(f"merged {len(decisions)} decisions ({len(trees)} code version(s)) "
          f"into {out_dir}")


def cmd_merge(args) -> None:
    _guard_l2(args)
    if args.selftest:
        merge_parts(scratch_dir(), "selftest_", [c["config_id"] for c in TOY_CONFIGS],
                    len(TOY["bases"]) * len(TOY["sizes"]))
    else:
        merge_parts(RESULTS, "", [c["config_id"] for c in cfg.CONFIGS],
                    len(cfg.TEST_POOL_BASES) * len(cfg.SIZES))


def cmd_tune(args) -> None:
    require_bundle(STUDY2_L1, args.selftest)
    grid = [(a, b, g) for a in cfg.P11_GRID["alpha"] for b in cfg.P11_GRID["beta"]
            for g in cfg.P11_GRID["gamma"]]
    if args.selftest:
        configs, bases, sizes = TOY_CONFIGS, [TOY_SEED_BASE + 51], [8]
        K, K11, grid = TOY["K"], TOY["K11"], grid[:4]
        proj_cfg, proj_sizes, proj_kw = TOY_CONFIGS[0], [8], toy_kw()
        out_dir = scratch_dir()
    else:
        configs, bases, sizes = cfg.CONFIGS, cfg.TRAIN_POOL_BASES, cfg.SIZES
        K, K11 = cfg.K_RANDOM, cfg.K_P11
        proj_cfg = next(c for c in cfg.CONFIGS
                        if c["config_id"] == cfg.PROJECTION_CONFIG)
        proj_sizes = cfg.SIZES
        proj_kw = dict(K=cfg.K_RANDOM, K11=cfg.K_P11, weights=(2.0, 1.0, 0.5))
        out_dir = RESULTS
    scores = {w: [] for w in grid}
    for config in configs:
        for base in bases:
            for n in sizes:
                for w, v in tune_instance(config, base, n, K, K11, grid).items():
                    scores[w].append(v)
    table = {str(w): float(np.mean(v)) for w, v in scores.items()}
    best = min(grid, key=lambda w: (table[str(w)], w))
    proj = runtime_projection(proj_cfg, bases[0], proj_sizes, proj_kw)
    _write_json({"meta": {**provenance(), "selftest": args.selftest},
                 "n_instances": len(next(iter(scores.values()))),
                 "scores": table, "selected": best, "runtime_projection": proj},
                out_dir / f"{'selftest_' if args.selftest else ''}v0_6_phase6_L2_tuning.json")
    print(f"selected (alpha, beta, gamma) = {best}; projected main-study hours "
          f"{proj['projected_hours_main']:.2f}"
          f"{' (toy timing)' if args.selftest else ''}")


def _headline_key(args) -> str:
    if args.screen_key:
        if not args.selftest:
            raise SystemExit("--screen-key is for self-tests; the registered key "
                             "comes from G4 (v0_6_phase6_gates.json).")
        return args.screen_key
    if args.selftest:
        return "M2"
    gates = RESULTS / "v0_6_phase6_gates.json"
    main_json = RESULTS / "v0_6_phase6_main.json"
    if not gates.exists() or not main_json.exists():
        raise SystemExit("Run analysis_phase6 on the complete main study first: "
                         "G4 decides the warm-start screening key (§9).")
    g = json.loads(gates.read_text("utf-8"))
    if g["meta"].get("main_sha256") != sha256_file(main_json):
        raise SystemExit("The gates file was not computed from the current "
                         "main results; rerun analysis_phase6.")
    k = g["gates"]["headline_screening_key"]
    return "M2" if k == "M2" else "max"


def cmd_warmstart(args) -> None:
    _guard_l2(args)
    key = _headline_key(args)
    if args.selftest:
        configs, bases = TOY_CONFIGS[:1], TOY["bases"][:1]
        K, K11, weights = TOY["K"], TOY["K11"], TOY["weights"]
        reps, steps, g5a = {"P0": 3, "P5": 1, "GSV": 1}, 3, 20
        out_dir = scratch_dir()
    else:
        configs, bases = cfg.CONFIGS, cfg.TEST_POOL_BASES
        K, K11, weights = cfg.K_RANDOM, cfg.K_P11, _real_weights()
        reps, steps, g5a = cfg.WARM_REPLICATES, cfg.WARM_STEPS, cfg.WARM_G5A_SAMPLE
        out_dir = RESULTS
    chains = []
    for config in configs:
        for base in bases:
            pool = order_pool(config, base)
            # P5 corner: the single-wave P5 protocol at size 16 (no refit later)
            ev = Evaluator(config)
            cid, n = config["config_id"], cfg.WARM_SIZE
            cand = build_candidates(pool, n, K, random.Random(
                cfg.seed6(base, cid, cfg.STREAM["random_candidates"], n)))
            rng94 = random.Random(cfg.seed6(base, cid, cfg.STREAM["training_sample"], n))
            tr = [rng94.randrange(len(cand)) for _ in range(min(cfg.TRAIN_SAMPLE, len(cand)))]
            m2 = [ev(tuples_of(pool, tuple(cand["idxs"].iloc[i])), "M2") for i in tr]
            fav = favorable_label(fit_phi_beta(cand.iloc[tr], m2))
            for variant in ("A", "B"):
                for arm, r in reps.items():
                    for j in range(r):
                        chains.append(run_chain(config, base, arm, j, variant, K=K,
                                                K11=K11, weights=weights, key=key,
                                                pool=pool, steps=steps, g5a=g5a,
                                                fav=fav))
    _write_json({"meta": {**provenance(), "selftest": args.selftest, "key": key},
                 "chains": chains},
                out_dir / f"{'selftest_' if args.selftest else ''}v0_6_phase6_warmstart.json")
    print(f"wrote {len(chains)} chains (screening key {key})")


def cmd_runtime(args) -> None:
    _guard_l2(args)
    if args.selftest:
        configs, Ks, sizes, weights = TOY_CONFIGS[:1], [60, 120], [8, 16], TOY["weights"]
        base, K11, out_dir = TOY_SEED_BASE + 1, TOY["K11"], scratch_dir()
    else:
        configs = [c for c in cfg.CONFIGS if c["config_id"] in cfg.RUNTIME_CONFIGS]
        Ks, sizes, weights = cfg.RUNTIME_K, cfg.RUNTIME_SIZES, _real_weights()
        base, K11, out_dir = cfg.TEST_POOL_BASES[0], cfg.K_P11, RESULTS
    rows = []
    for config in configs:
        pool = order_pool(config, base)
        for K in Ks:
            for n in sizes:
                ev = Evaluator(config)
                t0 = time.perf_counter()
                cand, G, source, _ = build_G(pool, config, base, n, K, K11, weights)
                t1 = time.perf_counter()
                m2 = np.array([ev(tuples_of(pool, ix), "M2") for ix in G])
                t2 = time.perf_counter()
                ties = tie_ranks(len(G), random.Random(0))
                sids: Dict[tuple, int] = {}
                sid = [sids.setdefault(signature(pool, ix), len(sids)) for ix in G]
                short = first_k_distinct(ranked(m2, ties), sid, cfg.GSV_HEADLINE_K)
                _ = [ev(tuples_of(pool, G[g]), "DES-M2") for g in short]
                t3 = time.perf_counter()
                rows.append({"config_id": config["config_id"], "K": K, "size": n,
                             "nG": len(G), "generate_s": t1 - t0, "screen_s": t2 - t1,
                             "verify_s": t3 - t2,
                             "per_candidate_ms": 1000 * (t2 - t1) / len(G)})
    _write_json({"meta": {**provenance(), "selftest": args.selftest}, "rows": rows},
                out_dir / f"{'selftest_' if args.selftest else ''}v0_6_phase6_runtime.json")
    print(f"wrote {len(rows)} runtime rows")


def run_case(df, days, configs, bases, sizes, kw, timing, ranges,
             ready_horizon, sens_size) -> Tuple[list, list, list]:
    """§11.4: primary runs on every case pool and size, then the one-at-a-time
    sensitivity runs at n = sens_size (parameter range ends; ready offsets)."""
    from src.case_online_retail import draw_case_pool
    main_rows, sens_rows, raw = [], [], []
    for config in configs:
        cid = config["config_id"]
        for base in bases:
            seed = cfg.seed6(base, cid, cfg.STREAM["order_pool"], 0)
            pool, info = draw_case_pool(df, config["F"], seed, days=days)
            for n in sizes:
                s, r = run_decision(config, base, n, pool=pool, timing=timing, **kw)
                s["case_pool"] = info
                main_rows.append(s)
                raw += r
            settings = [("ready_offsets", "rank-scaled", None)]
            settings += [(k, end_, v) for k, lohi in ranges.items() if lohi
                         for end_, v in zip(("low", "high"), lohi)]
            for name, end_, value in settings:
                if name == "ready_offsets":
                    p_s, _ = draw_case_pool(df, config["F"], seed,
                                            ready_horizon=ready_horizon, days=days)
                    t_s = timing
                else:
                    p_s, t_s = pool, {**timing, name: value}
                s, _ = run_decision(config, base, sens_size, pool=p_s, timing=t_s, **kw)
                s["sensitivity"] = {"parameter": name, "end": end_, "value": value}
                sens_rows.append(s)
    return main_rows, sens_rows, raw


def cmd_case(args) -> None:
    _guard_l2(args)
    from src.case_online_retail import (_synthetic, clean, eligible_days,
                                        load_raw, standardize)
    if args.selftest:
        raw_df = _synthetic()
        raw_df["src_pos"] = range(len(raw_df))
        df, report = clean(standardize(raw_df))
        configs = [{**c, "n_amrs": 5} for c in cfg.CASE_CONFIGS[:1]]
        timing = {"speed_per_floor": 4.0, "load_time": 3.0, "unload_time": 3.0,
                  "service_time": 6.0}
        ranges = {"speed_per_floor": (3.0, 5.0), "load_time": None,
                  "unload_time": None, "service_time": None}
        bases, sizes, sens = [TOY_SEED_BASE + 9], [8], 8
        kw, out_dir, tag = toy_kw(), scratch_dir(), "selftest_"
    else:
        if not cfg.case_included():
            raise SystemExit("case_included is not 'yes' in the L2 addendum "
                             "(decision D-K); the case is not run.")
        if args.case_data is None:
            raise SystemExit("--case-data <path to the Online Retail II file> is required")
        timing, ranges = cfg.case_timing(), cfg.case_timing_ranges()
        if any(v is None for v in timing.values()) or any(v is None for v in ranges.values()):
            raise SystemExit("Case midpoints or ranges are empty in the L2 addendum.")
        df, report = clean(load_raw(args.case_data))
        configs, bases, sizes, sens = (cfg.CASE_CONFIGS, cfg.TEST_POOL_BASES,
                                       cfg.SIZES, cfg.WARM_SIZE)
        kw = dict(K=cfg.K_RANDOM, K11=cfg.K_P11, weights=_real_weights())
        out_dir, tag = RESULTS, ""
    days = eligible_days(df)
    main_rows, sens_rows, raw = run_case(df, days, configs, bases, sizes, kw, timing,
                                         ranges, cfg.CASE_READY_HORIZON, sens)
    meta = {**provenance(), "selftest": args.selftest, "cleaning": report,
            "n_eligible_days": len(days), "timing": timing, "ranges": ranges,
            "data_file_sha256": (None if args.selftest
                                 else sha256_file(args.case_data))}
    _write_json({"meta": meta, "decisions": main_rows},
                out_dir / f"{tag}v0_6_case_main.json")
    _write_json({"meta": meta, "decisions": sens_rows},
                out_dir / f"{tag}v0_6_case_sensitivity.json")
    _write_rows(raw, out_dir / "raw" / f"{tag}mvs_v0_6_case_candidates.csv.gz", ROW_HEADER)
    print(f"case: {len(main_rows)} decisions, {len(sens_rows)} sensitivity runs")


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["tune", "main", "merge", "warmstart",
                                        "runtime", "case"])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--configs", type=int, nargs="*")
    ap.add_argument("--case-data", type=Path)
    ap.add_argument("--des-subset", action="store_true",
                    help="self-test only; in real runs the L2 addendum decides")
    ap.add_argument("--redo", action="store_true",
                    help="recompute configurations whose part file exists")
    ap.add_argument("--allow-code-change", metavar="LOG_REFERENCE",
                    help="run although the code differs from the L2 hash; the "
                         "reference to the dated deviation-log entry is recorded")
    ap.add_argument("--screen-key", choices=["M2", "max"])
    args = ap.parse_args(argv)
    {"tune": cmd_tune, "main": cmd_main, "merge": cmd_merge,
     "warmstart": cmd_warmstart,
     "runtime": cmd_runtime, "case": cmd_case}[args.command](args)


if __name__ == "__main__":
    main()
