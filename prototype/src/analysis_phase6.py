"""
Phase 6 (Study 2) analysis: gates G1 to G8, the §7.3 execution-robustness
companions, and the statistics of paper_draft/phase6_method_study_protocol.md
§7 and §8.

Reads results/v0_6_phase6_main.json and, if present,
results/v0_6_phase6_warmstart.json (or the self-test files in the scratch
directory with --selftest) and writes v0_6_phase6_gates.json. Cell =
(configuration, size); cell value = mean over the test pools of the
per-pool quantity; configuration-level values average the sizes.

Run from prototype/:  python -m src.analysis_phase6 [--selftest]
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from typing import Callable, Dict, List, Optional

import numpy as np

from src import experiments_phase6 as _ep
from src import phase6_config as cfg
from src.experiments_phase6 import RESULTS, _write_json, provenance
from src.registration_guard import require_l2, scratch_dir, sha256_file

G = cfg.GATES
DEMAND = {c["config_id"]: c["demand"] for c in cfg.CONFIGS}
ROBUST_KEYS = [f"sigma{s}" for s in cfg.ROBUST_SIGMAS] + ["b5"]
N_DECISIONS = len(cfg.CONFIGS) * len(cfg.TEST_POOL_BASES) * len(cfg.SIZES)


def _tier(value, upper, middle):
    if value is None:
        return None
    if value >= upper:
        return "upper"
    if value >= middle:
        return "middle"
    return "lower"


def cells_of(decisions, fn: Callable) -> Dict[tuple, float]:
    """Cell mean over pools of a per-decision quantity (None values skipped)."""
    acc = defaultdict(list)
    for d in decisions:
        v = fn(d)
        if v is not None:
            acc[(d["config_id"], d["size"])].append(v)
    return {k: float(np.mean(v)) for k, v in acc.items() if v}


def config_level(cells: Dict[tuple, float], size: Optional[int] = None) -> Dict[int, float]:
    acc = defaultdict(list)
    for (cid, n), v in cells.items():
        if size is None or n == size:
            acc[cid].append(v)
    return {cid: float(np.mean(v)) for cid, v in acc.items()}


def bootstrap_ci(values: List[float], seed: int, B: int = 2000):
    v = np.asarray(values, dtype=float)
    if len(v) < 2:
        return None
    rng = np.random.default_rng(seed)
    means = v[rng.integers(0, len(v), size=(B, len(v)))].mean(axis=1)
    return [float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))]


def holm(pvals: Dict[str, float], alpha: float = 0.05) -> Dict[str, dict]:
    """Holm step-down: monotone adjusted p-values, rejection at alpha."""
    order = sorted(pvals, key=pvals.get)
    m, out, running = len(order), {}, 0.0
    for i, name in enumerate(order):
        running = max(running, min(1.0, (m - i) * pvals[name]))
        out[name] = {"p": pvals[name], "p_holm": running,
                     "reject": bool(running <= alpha)}
    return out


def wilcoxon_p(x: np.ndarray, y: np.ndarray) -> float:
    """Two-sided signed-rank test, zero differences discarded; 1.0 when every
    difference is zero (the comparison stays in the family)."""
    from scipy.stats import wilcoxon
    d = np.asarray(x, dtype=float) - np.asarray(y, dtype=float)
    if np.all(np.abs(d) <= 1e-12):
        return 1.0
    return float(wilcoxon(x, y, zero_method="wilcox",
                          alternative="two-sided").pvalue)


# --------------------------------------------------------------------------
# Per-decision quantities
# --------------------------------------------------------------------------

def head(d) -> str:
    k = str(cfg.GSV_HEADLINE_K)
    return k if k in d["gsv"]["G"] else str(max(int(x) for x in d["gsv"]["G"]))


def gsv20(d, key_label: str = "G"):
    return d["gsv"][key_label][head(d)]["DES-M2"]


def red(a, b):
    """Relative reduction of b against a."""
    return (a - b) / a


def analyse(main: dict, warm: Optional[dict]) -> dict:
    D = main["decisions"]
    out: Dict[str, dict] = {}
    # G4 first: it decides the headline screening key (D-F pre-commitment)
    hits = sum(d["ordering"]["P11"]["M1<=M2"] for d in D)
    n = sum(d["ordering"]["P11"]["n"] for d in D)
    g4 = hits / n if n else None
    out["G4"] = {"value": g4, "hits": hits, "n": n,
                 "tier": _tier(g4, G["G4"]["upper"], G["G4"]["middle"]),
                 "companions": {
                     src: {"M1<=M2": sum(d["ordering"][src]["M1<=M2"] for d in D)
                           / max(1, sum(d["ordering"][src]["n"] for d in D)),
                           "DES-M1<=DES-M2": sum(d["ordering"][src]["DES-M1<=DES-M2"]
                                                 for d in D)
                           / max(1, sum(d["ordering"][src]["n_des"] for d in D)),
                           "n_distinct": sum(d["ordering"][src]["n_distinct"] for d in D),
                           "M1<=M2_distinct_share": sum(
                               d["ordering"][src].get("M1<=M2_distinct", 0) for d in D)
                           / max(1, sum(d["ordering"][src]["n_distinct"] for d in D))}
                     for src in ("R", "P10", "P11")}}
    upper4 = out["G4"]["tier"] == "upper"
    key_label = "G" if upper4 else "G_maxkey"
    rob_label = "GSV20" if upper4 else "GSV20_maxkey"
    out["headline_screening_key"] = ("M2" if upper4 else
                                     "max{M1, M2} for P10 and P11 candidates")

    # G1 (cell value = mean over pools of the per-pool relative reduction)
    c1 = cells_of(D, lambda d: red(d["arms"]["P0"]["DES-M2"],
                                   d["arms"]["P0+P10"]["DES-M2"]))
    mean1 = float(np.mean(list(c1.values())))
    sign1 = float(np.mean([v > 0 for v in c1.values()]))
    if mean1 >= G["G1"]["upper"] and sign1 >= G["G1"]["sign"]:
        t1 = "upper"
    elif mean1 >= G["G1"]["middle"]:
        t1 = "middle"
    else:
        t1 = "lower"

    def mean_cells(fn):
        c = cells_of(D, fn)
        return float(np.mean(list(c.values()))) if c else None

    comp1 = {
        "M2_closed_form_prior_exposed": mean_cells(
            lambda d: red(d["arms"]["P0"]["M2"], d["arms"]["P0+P10"]["M2"])),
        "P5+P10_vs_P5": mean_cells(
            lambda d: red(d["arms"]["P5"]["DES-M2"], d["arms"]["P5+P10"]["DES-M2"])
            if "P5+P10" in d["arms"] else None),
        "P8+P10_vs_P8-200": mean_cells(
            lambda d: red(d["arms"]["P8-200"]["DES-M2"], d["arms"]["P8+P10"]["DES-M2"])),
        "chaining_increment_P10_vs_P10g": mean_cells(
            lambda d: red(d["arms"]["P0+P10g"]["DES-M2"], d["arms"]["P0+P10"]["DES-M2"])),
        "by_demand": {dem: float(np.mean([v for (cid, _), v in c1.items()
                                          if DEMAND.get(cid) == dem] or [np.nan]))
                      for dem in ("uniform", "clustered", "diurnal")},
    }

    def g1_tier(m, sg):
        if m >= G["G1"]["upper"] and sg >= G["G1"]["sign"]:
            return "upper"
        return "middle" if m >= G["G1"]["middle"] else "lower"

    # §7.3 for G1: the paired 50-candidate subsample under deterministic DES-M2
    # (sigma0, the baseline) and under each execution-robustness evaluator
    g1_rob = {}
    for k in ["sigma0"] + ROBUST_KEYS:
        c = cells_of(D, lambda d, k=k: red(d["robust"]["P0_sub_median"][k],
                                           d["robust"]["P0+P10_sub_median"][k]))
        m = float(np.mean(list(c.values())))
        sg = float(np.mean([v > 0 for v in c.values()]))
        g1_rob[k] = {"mean": m, "sign_share": sg, "tier": g1_tier(m, sg)}
    rank = {"lower": 0, "middle": 1, "upper": 2}
    out["G1"] = {"mean": mean1, "sign_share": sign1, "tier": t1,
                 "n_cells": len(c1), "companions": comp1,
                 "execution_robustness_subsample": g1_rob,
                 "lower_under_robustness": any(
                     rank[g1_rob[k]["tier"]] < rank[g1_rob["sigma0"]["tier"]]
                     for k in ROBUST_KEYS)}

    # G2 (versus P8-verify(20)) and G2' (versus P7-matched), with robustness
    def share_lower(fa, fb, ties_count=False):
        """Share of cells where arm a is below arm b (G2: strictly; G2':
        at or below, since its wording is 'matches or beats')."""
        ca, cb = cells_of(D, fa), cells_of(D, fb)
        common = [k for k in ca if k in cb]
        if not common:
            return None
        if ties_count:
            return float(np.mean([ca[k] <= cb[k] + 1e-9 for k in common]))
        return float(np.mean([ca[k] < cb[k] for k in common]))

    def gates_under_key(key_label, rob_label, sfx, kk, key_name):
        """G2, G2', the §7.3 execution-robustness companions, the C3 wording
        inputs and G3 under one screening key (GSV label, robustness label,
        ablation label suffix, k_star key). Called for the headline key and,
        when that key is max{M1, M2}, again for the M2 key (§5.5: the M2-key
        results are reported beside it)."""
        res: Dict[str, dict] = {}
        s2 = share_lower(lambda d: gsv20(d, key_label),
                         lambda d: d["arms"]["P8-verify"]["DES-M2"])
        s2p = share_lower(lambda d: gsv20(d, key_label),
                          lambda d: d["arms"]["P7-matched"]["DES-M2"], ties_count=True)
        rob = {}
        for k in ROBUST_KEYS:
            r2 = share_lower(lambda d, k=k: d["robust"][rob_label][k],
                             lambda d, k=k: d["robust"]["P8-verify"][k])
            r2p = share_lower(lambda d, k=k: d["robust"][rob_label][k],
                              lambda d, k=k: d["robust"]["P7-matched"][k], ties_count=True)
            rob[k] = {"G2_share": r2, "G2_tier": _tier(r2, G["G2"]["upper"], G["G2"]["middle"]),
                      "G2p_share": r2p,
                      "G2p_tier": _tier(r2p, G["G2p"]["upper"], G["G2p"]["middle"])}
        t2 = _tier(s2, G["G2"]["upper"], G["G2"]["middle"])
        t2p = _tier(s2p, G["G2p"]["upper"], G["G2p"]["middle"])
        res["G2"] = {"share": s2, "tier": t2, "descriptive_vs_P8_best": share_lower(
            lambda d: gsv20(d, key_label),
            lambda d: min(d["arms"]["P8-200"]["DES-M2"], d["arms"]["P8-1"]["DES-M2"]))}
        res["G2p"] = {"share": s2p, "tier": t2p}
        res["execution_robustness"] = {
            "by_evaluator": rob,
            "G2_lower_elsewhere": any(rank[v["G2_tier"]] < rank[t2] for v in rob.values()
                                      if v["G2_tier"] and t2),
            "G2p_lower_elsewhere": any(rank[v["G2p_tier"]] < rank[t2p] for v in rob.values()
                                       if v["G2p_tier"] and t2p)}

        # inputs to the C3 wording rule (STORY_CONTRACT §8): generator ablations
        def abl(d, label):
            lab = label if label == "R" else label + sfx
            return d["gsv"][lab][head(d)]["DES-M2"] if lab in d["gsv"] else None

        res["C3_wording_inputs"] = {
            "share_GSV20_released_from_P11": float(np.mean(
                [d["gsv"][key_label][head(d)]["source"] == "P11" for d in D])),
            "share_GSV20_released_from_P10": float(np.mean(
                [d["gsv"][key_label][head(d)]["source"] == "P10" for d in D])),
            "gain_adding_P11_to_R": mean_cells(
                lambda d: red(abl(d, "R"), abl(d, "R+P11"))),
            "gain_adding_P10_to_R": mean_cells(
                lambda d: red(abl(d, "R"), abl(d, "R+P10"))),
            "note": "relative DES-M2 reduction of GSV(20) when P11 (or P10) "
                    "candidates are added to R, mean over cells; screening key "
                    + key_name}

        # G3 (k* under the given key; tolerance max{2 %, 1 s / optimum}, protocol
        # §7.1; values computed in experiments_phase6.py from
        # phase6_config.REGRET_TOL_*)
        ck, ckr = defaultdict(list), defaultdict(list)
        for d in D:
            ck[(d["config_id"], d["size"])].append(d["k_star"][kk])
            ckr[(d["config_id"], d["size"])].append(d["k_star"][f"{kk}_vs_R_opt"])
        med_k = {c: float(np.median([x if x is not None else np.inf for x in v]))
                 for c, v in ck.items()}
        sh20 = float(np.mean([v <= G["G3"]["upper_k"] for v in med_k.values()]))
        sh50 = float(np.mean([v <= G["G3"]["middle_k"] for v in med_k.values()]))
        t3 = ("upper" if sh20 >= G["G3"]["share"] else
              "middle" if sh50 >= G["G3"]["share"] else "lower")
        res["G3"] = {"share_k20": sh20, "share_k50": sh50, "tier": t3,
                     "median_k_star_by_cell": {f"{c[0]}_{c[1]}": v for c, v in med_k.items()},
                     "companion_k_star_vs_R_opt": {
                         f"{c[0]}_{c[1]}": float(np.median([x if x is not None else np.inf
                                                            for x in v]))
                         for c, v in ckr.items()}}
        return res

    out.update(gates_under_key(key_label, rob_label, "" if upper4 else "_maxkey",
                               "M2" if upper4 else "max",
                               out["headline_screening_key"]))
    # §5.5 (pre-commitment D-F): when the headline key is max{M1, M2}, the same
    # single-wave quantities under the M2 key are reported beside it
    out["companion_M2_key"] = (None if upper4 else
                               {"key": "M2", **gates_under_key("G", "GSV20", "",
                                                               "M2", "M2")})

    # G5 (warm start)
    if warm is not None:
        ch = warm["chains"]
        gs = [c for c in ch if c["arm"] == "GSV"]
        a_hits, a_n = sum(c["g5a_hits"] for c in gs), sum(c["g5a_n"] for c in gs)
        g5a = a_hits / a_n if a_n else None
        p0 = defaultdict(list)
        for c in ch:
            if c["arm"] == "P0" and not c["stopped"]:
                p0[(c["config_id"], c["base"], c["variant"])].append(
                    [s["increment_DES-M2"] for s in c["steps"]])
        ret, excluded = [], 0
        for c in gs:
            u = (c["config_id"], c["base"], c["variant"])
            if not p0.get(u):
                continue
            inc0 = np.mean(np.asarray(p0[u], dtype=float), axis=0)
            incg = np.asarray([s["increment_DES-M2"] for s in c["steps"]], dtype=float)
            gain1 = inc0[0] - incg[0]
            if gain1 <= 0:
                excluded += 1
                continue
            ret.append(float(np.mean(inc0[1:] - incg[1:]) / gain1))
        g5b = float(np.median(ret)) if ret else None
        met = [(g5a or 0) >= G["G5"]["ordering"], (g5b or -np.inf) >= G["G5"]["retention"]]
        p11h = sum(c["g5a_P11_hits"] for c in gs)
        p11n = sum(c["g5a_P11_n"] for c in gs)
        out["G5"] = {"ordering_share_R": g5a, "retention_median": g5b,
                     "n_units": len(ret), "n_excluded_no_step1_gain": excluded,
                     "tier": "upper" if all(met) else "middle" if any(met) else "lower",
                     "screening_key": warm.get("meta", {}).get("key"),
                     "descriptive_P11_ordering_share": p11h / p11n if p11n else None}

    # G6
    c6 = cells_of(D, lambda d: d["seqvar"]["DES-M2"]["share_sequence"])
    s6 = float(np.mean(list(c6.values())))
    t6 = ("upper" if s6 > G["G6"]["upper"] else
          "middle" if s6 >= G["G6"]["middle"] else "lower")
    out["G6"] = {"mean_share": s6, "tier": t6,
                 "M2_descriptive": mean_cells(lambda d: d["seqvar"]["M2"]["share_sequence"])}

    # G8 (DL at k = 1)
    cm1 = cells_of(D, lambda d: d["ladder"]["M1"]["DL"])
    cm2 = cells_of(D, lambda d: d["ladder"]["M2"]["DL"])
    s8 = float(np.mean([cm1[k] > cm2[k] for k in cm1]))
    out["G8"] = {"share": s8, "tier": _tier(s8, G["G8"]["upper"], G["G8"]["middle"]),
                 "mean_DL": {m: mean_cells(lambda d, m=m: d["ladder"][m]["DL"])
                             for m in ("M1", "M2", "DES-M1")}}

    # §8 statistics
    arm_fn = {
        "GSV20": lambda d: gsv20(d, key_label),
        "P8-verify": lambda d: d["arms"]["P8-verify"]["DES-M2"],
        "P7-matched": lambda d: d["arms"]["P7-matched"]["DES-M2"],
        "P5": lambda d: d["arms"]["P5"].get("DES-M2"),
        "R-verify20": lambda d: d["r_verify"][head(d)]["DES-M2"],
        "P0": lambda d: d["arms"]["P0"]["DES-M2"],
        "P0+P10": lambda d: d["arms"]["P0+P10"]["DES-M2"],
        "P5+P10": lambda d: d["arms"].get("P5+P10", {}).get("DES-M2"),
    }
    cells = {a: cells_of(D, f) for a, f in arm_fn.items()}
    pairs = {"GSV20 vs P8-verify": ("GSV20", "P8-verify"),
             "GSV20 vs P7-matched": ("GSV20", "P7-matched"),
             "GSV20 vs P5": ("GSV20", "P5"),
             "GSV20 vs R-verify20": ("GSV20", "R-verify20"),
             "P0+P10 vs P0": ("P0+P10", "P0"), "P5+P10 vs P5": ("P5+P10", "P5")}

    def family(size=None):
        pv = {}
        for name, (a, b) in pairs.items():
            ca, cb = config_level(cells[a], size), config_level(cells[b], size)
            common = sorted(set(ca) & set(cb))
            if len(common) >= 2:
                pv[name] = wilcoxon_p(np.array([ca[c] for c in common]),
                                      np.array([cb[c] for c in common]))
        return holm(pv)

    out["tests"] = family()
    out["tests_by_size"] = {str(n): family(n) for n in sorted({d["size"] for d in D})}
    per_cell = defaultdict(lambda: defaultdict(list))
    for d in D:
        c = (d["config_id"], d["size"])
        for a in ("GSV20", "P0", "P8-verify", "P7-matched"):
            v = arm_fn[a](d)
            if v is not None:
                per_cell[c][a].append(v)
        per_cell[c]["G1_reduction"].append(
            red(d["arms"]["P0"]["DES-M2"], d["arms"]["P0+P10"]["DES-M2"]))
    out["bootstrap_by_cell"] = {
        f"{c[0]}_{c[1]}": {a: bootstrap_ci(v, cfg.BOOTSTRAP_SEED + i)
                           for a, v in per_cell[c].items()}
        for i, c in enumerate(sorted(per_cell))}
    out["budgets_per_decision"] = {
        "P0/P2/P8-1/P8-200": {"M2": 0, "DES": 0},
        "P8-verify(20)": {"M2": 0, "DES": cfg.P8_VERIFY_K},
        "P5/P9": {"M2": cfg.TRAIN_SAMPLE, "DES": 0},
        "P7-matched": {"M2": cfg.P7_MATCHED_BUDGET, "DES": cfg.P7_MATCHED_VERIFY},
        "GSV(20)": {"M2": 2 * cfg.K_RANDOM + cfg.K_P11, "DES": cfg.GSV_HEADLINE_K},
        "R-verify(20)": {"M2": 0, "DES": cfg.GSV_HEADLINE_K}}
    return out


def main(argv=None) -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--allow-code-change", metavar="LOG_REFERENCE")
    args = ap.parse_args(argv)
    # the deviation-log reference given with --allow-code-change is stored in
    # the gates output too (protocol §12 item 7: recorded in every output)
    _ep.CODE_CHANGE_REF = require_l2(args.selftest,
                                     allow_code_change=args.allow_code_change)
    base = scratch_dir() if args.selftest else RESULTS
    tag = "selftest_" if args.selftest else ""
    main_path = base / f"{tag}v0_6_phase6_main.json"
    main_res = json.loads(main_path.read_text("utf-8"))
    keys = {(d["config_id"], d["base"], d["size"]) for d in main_res["decisions"]}
    if not args.selftest and (len(keys) != N_DECISIONS
                              or len(main_res["decisions"]) != N_DECISIONS):
        raise SystemExit(f"analysis stopped: {len(main_res['decisions'])} decisions "
                         f"({len(keys)} distinct), expected {N_DECISIONS}")
    wpath = base / f"{tag}v0_6_phase6_warmstart.json"
    warm = json.loads(wpath.read_text("utf-8")) if wpath.exists() else None
    res = analyse(main_res, warm)
    _write_json({"meta": {**provenance(), "selftest": args.selftest,
                          "main_sha256": sha256_file(main_path),
                          "warmstart_sha256": sha256_file(wpath) if warm else None},
                 "gates": res}, base / f"{tag}v0_6_phase6_gates.json")
    print("gates computed:", ", ".join(k for k in res if k.startswith("G")))


if __name__ == "__main__":
    main()
