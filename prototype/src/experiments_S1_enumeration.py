"""
S1-2 / S1-8 / S1-11 -- Full-pool enumeration and its derived displays [NS].

Registration: revision_2026-09-26_ijpr/amendments/AMEND-2026-09-26-S1B_new_simulations.md
  S1-2  "Full-pool enumeration"
  S1-8  "Where the best waves are" [depends on S1-2]
  S1-11 "Complementary fractions, closed-form descriptive layer"
         [NS; only if D-D1 is signed -- see the note in cmd_s1_11 below]
Guard key: "S1B" (signed 2026-09-26; the guard also requires the S1D note).

None of these three items carries a gate; all are descriptive and reported
beside the locked verdicts (S1-2/S1-8 "Reporting rule", S1-11 "Reporting
rule"). Real mode enumerates every candidate of the named pools under BOTH
M1 (abstraction) and M2 (batched) with the CURRENT production simulator, and
additionally reads the stored Phase 5 raw CSVs for (a) the regeneration
check and (b) the "stored favourable corner" / "stored policy medians" used
in the side-by-side displays -- this is legitimate for the registered
procedure (S1-2's own Inputs name these CSVs). Real mode runs only after
`require_signed("S1B")` passes; the registered run took place on
2026-09-26 (revision_2026-09-26_ijpr/study1_run_2026-09-26/). Self-test mode never reads any file under
prototype/results; it patches `phase5_config.SEED_BASE` to
`registration_guard.TOY_SEED_BASE` and enumerates tiny toy pools.

Run:
  python -m src.experiments_S1_enumeration s1-2             # real run: writes into prototype/results/; only at the author's request
  python -m src.experiments_S1_enumeration s1-2 --selftest  # toy run
  python -m src.experiments_S1_enumeration s1-8 --selftest
  python -m src.experiments_S1_enumeration s1-11 --selftest
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from src import phase5_config as cfg
from src.analysis_phase5_blockA import CORNERS, decompose
from src.demand_patterns import generate_pool
from src.experiments_phase5 import MODEL_IDX, MODEL_TAG, _seed, sim_makespan
from src.registration_guard import code_provenance  # S1D: code-tree hash in every output
from src.registration_guard import require_checkbox
from src.registration_guard import TOY_SEED_BASE, require_signed, scratch_dir
from src.simulator import Wave
from src.wave_policies import (build_candidates, corner_positions,
                               favorable_label, fit_phi_beta)

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RAW_DIR = RESULTS_DIR / "raw"
REG_PATH = (Path(__file__).resolve().parents[2] / "revision_2026-09-26_ijpr"
            / "amendments" / "AMEND-2026-09-26-S1B_new_simulations.md")

BLOCK_B_CONFIGS = [1, 3, 5, 7, 9, 11]
_DUMMY_RNG = random.Random(0)
EPS = 0.05          # U_c(EPS), matching analysis_phase5_blockC.py's EPS


# --------------------------------------------------------------------------
# Small utilities
# --------------------------------------------------------------------------

def _sha256_file(path: Path) -> str:
    """Line-ending-normalized SHA-256 (the guard's definition), so
    recorded hashes match MANIFEST_SIGNED.json."""
    from src.registration_guard import sha256_file
    return sha256_file(path)


def _quantile_bin(values: np.ndarray, n_bins: int) -> np.ndarray:
    """Assign each value to a quantile bin 0..n_bins-1 (covering partition)."""
    qs = [np.quantile(values, k / n_bins) for k in range(1, n_bins)]
    return np.digitize(values, qs)


# --------------------------------------------------------------------------
# Pool enumeration (the S1-2 core: exact makespans for a whole candidate pool)
# --------------------------------------------------------------------------

def enumerate_pool(config: dict, size: int, cand_n: int,
                   seed_model: Optional[str], block: str) -> dict:
    """Build one candidate pool and evaluate EVERY candidate under M1 and M2.

    `seed_model` selects the seed stream: Blocks A/B use the per-model seed
    `_seed(cid, MODEL_IDX[m], size)`; Block C uses the model-independent
    `_seed(cid, 99, size)` (pass seed_model=None, block="C").
    """
    pool = generate_pool(config["demand"], config["F"], cfg.ORDER_POOL_SIZE,
                         seed=cfg.SEED_BASE + config["config_id"],
                         **cfg.DEMAND_PARAMS[config["demand"]])
    if block == "C":
        seed = _seed(config["config_id"], 99, size)
    else:
        seed = _seed(config["config_id"], MODEL_IDX[seed_model], size)
    cand = build_candidates(pool, size, cand_n, random.Random(seed))
    waves = [Wave(orders=[pool[i] for i in idxs], release_time=0.0)
            for idxs in cand["idxs"]]
    makespans = {}
    for m in ("abstraction", "batched"):
        makespans[MODEL_TAG[m]] = np.array(
            [sim_makespan(w, config, m, _DUMMY_RNG) for w in waves],
            dtype=float)
    return {"config_id": config["config_id"], "block": block,
           "seed_model": seed_model, "size": size, "cand_n": cand_n,
           "pool_seed": cfg.SEED_BASE + config["config_id"], "cand_seed": seed,
           "cand": cand, "makespans": makespans}


# --------------------------------------------------------------------------
# S1-2 per-pool quantities
# --------------------------------------------------------------------------

def corner_family_quantities(cand: pd.DataFrame, mk: np.ndarray,
                             favorable_by_label: Dict[str, Optional[str]]
                             ) -> dict:
    """Exact class medians/sizes/overlaps + GAP decomposition(s) for the
    4-corner family (S1-2 quantity 1-3)."""
    m0 = float(np.median(mk))
    corner_pos = {c: corner_positions(cand, c) for c in CORNERS}
    m_q = {c: float(np.median(mk[pos])) for c, pos in corner_pos.items()}
    sizes = {c: int(len(pos)) for c, pos in corner_pos.items()}
    overlaps = {}
    for i, c1 in enumerate(CORNERS):
        for c2 in CORNERS[i + 1:]:
            inter = len(set(corner_pos[c1].tolist())
                       & set(corner_pos[c2].tolist()))
            overlaps[f"{c1}&{c2}"] = inter
    decomps = {}
    for label, fav in favorable_by_label.items():
        if fav is None:
            decomps[label] = None
            continue
        H_up, M_phi, UB, LB, qmax, qmin = decompose(m_q, m0, fav)
        decomps[label] = {"favorable": fav, "H_up": H_up, "M_Phi": M_phi,
                         "GAP": H_up + M_phi, "UB": UB, "LB": LB,
                         "q_max": qmax, "q_min": qmin}
    return {"m0": m0, "class_medians": m_q, "class_sizes": sizes,
           "class_overlaps": overlaps, "decompositions": decomps}


def pool_optimum(mk: np.ndarray) -> dict:
    m = float(np.min(mk))
    ties = int(np.sum(np.isclose(mk, m, rtol=0.0, atol=1e-9)))
    return {"optimum": m, "tie_count": ties}


def covering_partition(cand: pd.DataFrame, mk: np.ndarray, n_bins: int,
                       beta: dict) -> dict:
    """Exact class medians on an n_bins x n_bins covering partition of (C,I),
    with the partition-relative H_up / M_Phi generalising Section 4.1 /
    SECTION_4_METHODOLOGY.md Section 4.2.3 (Corollary 1: H_up(P) and
    UB(P) = H_up(P) + S_or(P) are defined for any covering partition on the
    max/min cell median; "the selection term M_Phi additionally depends on
    the rule's choice at each resolution"). The rule's choice is generalised
    here as the SAME beta-sign direction the 4-corner favorable_label rule
    uses, projected onto the extreme bin combination of the finer grid.
    # REGISTRATION NOTE (experiments_S1_enumeration.py, covering_partition):
    # S1-2 cites "the partition-relative H_up and M_Phi defined as in
    # Section 4.1" without restating the formula. SECTION_4_METHODOLOGY.md
    # Section 4.2.3 gives H_up(P) and the oracle gain S_or(P) generically for
    # any covering partition, but says M_Phi(P) "depends on the rule's choice
    # at each resolution" without fixing that choice for an n x n grid. The
    # extreme-bin generalisation of the beta-sign rule implemented here is
    # this script's own literal extension, not a restatement of a formula
    # found verbatim in the source text.
    """
    C, I = cand["C"].to_numpy(), cand["I"].to_numpy()
    c_bins, i_bins = _quantile_bin(C, n_bins), _quantile_bin(I, n_bins)
    m0 = float(np.median(mk))
    med: Dict[tuple, float] = {}
    sizes: Dict[tuple, int] = {}
    for cb in range(n_bins):
        for ib in range(n_bins):
            mask = (c_bins == cb) & (i_bins == ib)
            if mask.sum() > 0:
                med[(cb, ib)] = float(np.median(mk[mask]))
                sizes[(cb, ib)] = int(mask.sum())
    qmax_key = max(med, key=med.get)
    qmin_key = min(med, key=med.get)
    H_up = (med[qmax_key] - m0) / m0
    fav_c = (n_bins - 1) if beta["beta_C"] < 0 else 0
    fav_i = (n_bins - 1) if beta["beta_I"] < 0 else 0
    fav_key = (fav_c, fav_i)
    if fav_key not in med:                    # empty extreme cell (rare tie case)
        fav_key = qmin_key
    M_phi = (med[fav_key] - med[qmin_key]) / m0
    S_or = (m0 - med[qmin_key]) / m0          # Corollary 1 / A-R1 quantities
    UB = H_up + S_or
    return {"n_bins": n_bins, "m0": m0, "S_or": S_or, "UB": UB,
           "share_H_up_over_UB": (H_up / UB) if UB > 0 else None,
           "M_Phi_note": "M_Phi(P) uses the extreme bin in the direction of the "
                         "fitted signs (a labelled generalization of the corner rule)",
           "cell_medians": {f"{k[0]}_{k[1]}": v for k, v in med.items()},
           "cell_sizes": {f"{k[0]}_{k[1]}": v for k, v in sizes.items()},
           "q_max_cell": f"{qmax_key[0]}_{qmax_key[1]}",
           "q_min_cell": f"{qmin_key[0]}_{qmin_key[1]}",
           "favorable_cell": f"{fav_key[0]}_{fav_key[1]}",
           "H_up": H_up, "M_Phi": M_phi, "GAP": H_up + M_phi}


def theorem2_full_classes(cand: pd.DataFrame, m1: np.ndarray,
                          m2: np.ndarray) -> dict:
    """Per-candidate M1<=M2 rate, minimax (Hedge) corner, and U_c(0.05),
    each computed on the FULL corner class (not a 200-wave sample)."""
    per_corner = {}
    for c in CORNERS:
        pos = corner_positions(cand, c)
        t1, t2 = m1[pos], m2[pos]
        per_corner[c] = {
            "ordering_rate_M1_le_M2": float(np.mean(t1 <= t2)),
            "median_M1": float(np.median(t1)), "median_M2": float(np.median(t2)),
            f"U_c_{EPS}": float(np.quantile(t2, 0.5 + EPS) - np.quantile(t2, 0.5)),
        }
    for c in CORNERS:
        pos = corner_positions(cand, c)
        per_corner[c]["mean_M1"] = float(np.mean(m1[pos]))
        per_corner[c]["mean_M2"] = float(np.mean(m2[pos]))
    minimax_corner = min(
        per_corner, key=lambda c: max(per_corner[c]["median_M1"],
                                      per_corner[c]["median_M2"]))
    minimax_mean = min(
        per_corner, key=lambda c: max(per_corner[c]["mean_M1"],
                                      per_corner[c]["mean_M2"]))
    return {"per_corner": per_corner, "minimax_corner": minimax_corner,
            "minimax_corner_mean_basis": minimax_mean}


# --------------------------------------------------------------------------
# Regeneration check (real mode only -- reads the stored raw CSVs it names)
# --------------------------------------------------------------------------

def regeneration_check_blockA(pool_result: dict, blockA_ids: pd.DataFrame,
                              blockA: pd.DataFrame) -> dict:
    """Compare freshly enumerated makespans to the STORED Block A rows that
    drew the same candidate_id in this (config, model, size) cell."""
    cid, model, size = (pool_result["config_id"], pool_result["seed_model"],
                        pool_result["size"])
    ids_sub = blockA_ids[(blockA_ids["config_id"] == cid)
                        & (blockA_ids["model"] == model)
                        & (blockA_ids["size"] == size)]
    tag = MODEL_TAG[model]
    n_checked, n_exact, n_diff = 0, 0, 0
    max_abs_diff = 0.0
    for _, idrow in ids_sub.iterrows():
        row = blockA.iloc[int(idrow["row_index"])]      # join by row_index
        if (int(row["config_id"]) != cid or row["model"] != model
                or int(row["size"]) != size or row["arm"] != idrow["arm"]):
            raise SystemExit(f"S1-2 STOP: Block A join mismatch at row_index "
                             f"{int(idrow['row_index'])}")
        stored_mk = row["makespan"]
        fresh_mk = pool_result["makespans"][tag][int(idrow["candidate_id"])]
        n_checked += 1
        diff = abs(float(stored_mk) - float(fresh_mk))
        if diff < 1e-9:
            n_exact += 1
        else:
            n_diff += 1
            max_abs_diff = max(max_abs_diff, diff)
    return {"n_checked": n_checked, "n_exact": n_exact, "n_diff": n_diff,
           "max_abs_diff": max_abs_diff}


def regeneration_check_blockC(pool_result: dict, blockC_fix: pd.DataFrame) -> dict:
    """Compare enumerated M1/M2 with the tie-break-fixed Block C CSV (same
    simulator semantics as the current code, so every value must agree)."""
    cid = pool_result["config_id"]
    sub = blockC_fix[blockC_fix["config_id"] == cid]
    n_checked = n_diff = 0
    for _, r in sub.iterrows():
        k = int(r["candidate_id"])
        for col, tag in (("makespan_M1", "M1"), ("makespan_M2", "M2")):
            n_checked += 1
            n_diff += abs(float(r[col]) - float(pool_result["makespans"][tag][k])) > 1e-9
    if n_diff:
        raise SystemExit(f"S1-2 STOP: Block C config {cid}: {int(n_diff)} of "
                         f"{n_checked} values differ from the tie-break-fixed "
                         "CSV (same simulator); the pools are not reproduced")
    return {"n_checked": n_checked, "n_diff": int(n_diff),
            "reference": "mvs_v0_5_phase5_blockC_tiebreakfix.csv"}


# --------------------------------------------------------------------------
# S1-2 driver
# --------------------------------------------------------------------------

def _e2_subset_first6(configs: List[dict]) -> List[dict]:
    e2 = cfg.e2_subset(configs)
    return e2[:6]


def run_s1_2(configs: List[dict], sizes: List[int], cand_n: int,
            selftest: bool) -> dict:
    # Real mode: the registered 6 Block C / Block B configs (1,3,5,7,9,11).
    # Selftest: those ids do not exist in the tiny toy config list, so fall
    # back to whichever config ids selftest actually built (still exercises
    # the identical Block C code path on toy data).
    block_c_ids = (BLOCK_B_CONFIGS if not selftest
                  else [c["config_id"] for c in configs])
    blockA_raw = blockB_raw = blockA_ids = blockC_raw = blockC_ids = None
    ablP7 = None
    if not selftest:
        blockA_raw = pd.read_csv(RAW_DIR / "mvs_v0_5_phase5_blockA.csv")
        blockA_ids = pd.read_csv(RAW_DIR / "mvs_v0_5_phase5_blockA_candidate_ids.csv")
        blockB_raw = pd.read_csv(RAW_DIR / "mvs_v0_5_phase5_blockB.csv")
        ablP7 = pd.read_csv(RAW_DIR / "mvs_v0_5_phase5_ablation_P7.csv")
        blockC_fix = pd.read_csv(RAW_DIR / "mvs_v0_5_phase5_blockC_tiebreakfix.csv")
        tier2 = (Path(__file__).resolve().parents[2] / "revision_2026-07-08"
                 / "tier2_analysis" / "outputs")
        p8_cells = {(c["config_id"], c["size"]): c["m_P8"] for c in json.loads(
            (tier2 / "b2_b3_benchmarks.json").read_text("utf-8"))["B3"]["per_cell"]}
        p9_cells = {(c["config_id"], c["size"]): c["m_P9"] for c in json.loads(
            (tier2 / "amendC1_p9_spoplus.json").read_text("utf-8"))["per_cell"]}

    blockA_pools: Dict[tuple, dict] = {}
    pool_rows = []
    for config in configs:
        for seed_model in ("abstraction", "batched"):
            for size in sizes:
                pr = enumerate_pool(config, size, cand_n, seed_model, "A")
                blockA_pools[(config["config_id"], seed_model, size)] = pr
                fav_stored = None
                if not selftest:
                    sub = blockA_raw[(blockA_raw.config_id == config["config_id"])
                                    & (blockA_raw.model == seed_model)
                                    & (blockA_raw["size"] == size)]
                    if len(sub):
                        fav_stored = sub["favorable_corner"].iloc[0]
                tag = MODEL_TAG[seed_model]
                mk = pr["makespans"][tag]
                beta_refit = fit_phi_beta(pr["cand"], mk)
                # REGISTRATION NOTE (experiments_S1_enumeration.py, run_s1_2,
                # Block A loop): "the stored favourable corner" (S1-2
                # quantity 2(i)) exists only for the model the row was
                # ORIGINALLY generated under (matching MODEL_TAG[seed_model]);
                # reported under that one model tag. This is the literal
                # reading -- the stored CSV records one favorable_corner per
                # (config, model, size), fit from THAT model's makespans.
                fav_refit = favorable_label(beta_refit)
                cq = corner_family_quantities(
                    pr["cand"], mk, {"stored": fav_stored, "full_pool_fit": fav_refit})
                cov = {n: covering_partition(pr["cand"], mk, n, beta_refit)
                      for n in (2, 3, 4)}
                th2 = None    # filled once both M1 and M2 arrays are known below
                regen = None
                if not selftest:
                    regen = regeneration_check_blockA(pr, blockA_ids, blockA_raw)
                pool_rows.append({
                    "block": "A", "config_id": config["config_id"],
                    "seed_model": seed_model, "size": size,
                    "pool_seed": pr["pool_seed"], "cand_seed": pr["cand_seed"],
                    "optimum_M1": pool_optimum(pr["makespans"]["M1"]),
                    "optimum_M2": pool_optimum(pr["makespans"]["M2"]),
                    "corner_quantities_this_model": cq,
                    "covering_partitions_this_model": cov,
                    "theorem2_full_classes": theorem2_full_classes(
                        pr["cand"], pr["makespans"]["M1"], pr["makespans"]["M2"]),
                    "regeneration_check": regen,
                })

    blockC_pools: Dict[int, dict] = {}
    for cid in block_c_ids:
        config = next(c for c in configs if c["config_id"] == cid)
        pr = enumerate_pool(config, 16, cand_n, None, "C")
        blockC_pools[cid] = pr
        beta_refit = fit_phi_beta(pr["cand"], pr["makespans"]["M2"])
        # REGISTRATION NOTE (experiments_S1_enumeration.py, run_s1_2, Block C
        # loop): Block C's stored CSV has no `favorable_corner` column (the
        # harness's run_chain_block never fits beta -- see
        # src/experiments_phase5.py) and Block A does not cover size 16, so
        # there is no "stored favourable corner" for a Block C pool. Only the
        # full-pool fit_phi_beta corner (S1-2 quantity 2(ii)) is reported for
        # Block C; the "stored" side of the decomposition is emitted as null.
        cq = corner_family_quantities(
            pr["cand"], pr["makespans"]["M2"],
            {"stored": None, "full_pool_fit": favorable_label(beta_refit)})
        cov = {n: covering_partition(pr["cand"], pr["makespans"]["M2"], n, beta_refit)
              for n in (2, 3, 4)}
        pool_rows.append({
            "block": "C", "config_id": cid, "seed_model": None, "size": 16,
            "pool_seed": pr["pool_seed"], "cand_seed": pr["cand_seed"],
            "optimum_M1": pool_optimum(pr["makespans"]["M1"]),
            "optimum_M2": pool_optimum(pr["makespans"]["M2"]),
            "corner_quantities_this_model": cq,
            "covering_partitions_this_model": cov,
            "theorem2_full_classes": theorem2_full_classes(
                pr["cand"], pr["makespans"]["M1"], pr["makespans"]["M2"]),
            "regeneration_check": (None if selftest else
                                   regeneration_check_blockC(pr, blockC_fix)),
        })

    block_b_gap = []
    if not selftest:
        for cid in block_c_ids:
            for size in (8, 30):
                pr = blockA_pools.get((cid, "batched", size))
                if pr is None:
                    continue
                opt = pool_optimum(pr["makespans"]["M2"])["optimum"]
                row = {"config_id": cid, "size": size, "pool_optimum_M2": opt}
                gB = blockB_raw[(blockB_raw.config_id == cid)
                               & (blockB_raw["size"] == size)]
                for pname, col in (("P5", "P5_phi"), ("P6", "P6_spo_tree")):
                    sub = gB[gB.policy == col]
                    if len(sub):
                        med = float(np.median(sub["makespan"]))
                        row[f"{pname}_median"] = med
                        row[f"{pname}_gap_to_optimum"] = (med - opt) / opt
                g7 = ablP7[(ablP7.config_id == cid) & (ablP7["size"] == size)]
                if len(g7):
                    med7 = float(np.median(g7["makespan"]))
                    row["P7_median"] = med7
                    row["P7_gap_to_optimum"] = (med7 - opt) / opt
                # P8 and P9: stored cell medians of AMEND-B B-3 and AMEND-C C-1
                for pname, cells in (("P8", p8_cells), ("P9", p9_cells)):
                    med = cells.get((cid, size))
                    row[f"{pname}_median"] = med
                    row[f"{pname}_gap_to_optimum"] = (None if med is None
                                                      else (med - opt) / opt)
                row["simulator_note"] = (
                    "policy medians are the stored values (generated before the "
                    "2026-09-11 tie-break fix; S1-9 regenerates P5 to P7); the "
                    "pool optimum is enumerated with the current simulator")
                block_b_gap.append(row)

    return {"pools": pool_rows, "block_b_gap_to_optimum": block_b_gap,
           "_blockA_pools_cache": blockA_pools,      # reused by cmd_s1_8
           "_blockC_pools_cache": blockC_pools}


# --------------------------------------------------------------------------
# S1-8 driver (depends on S1-2's enumerated pools)
# --------------------------------------------------------------------------

def top1pct_facet(cand: pd.DataFrame, mk: np.ndarray,
                  fav: Optional[str]) -> dict:
    n = len(mk)
    k = max(1, round(0.01 * n))
    order = np.argsort(mk)
    cutoff_val = float(mk[order[k - 1]])
    top_idx = np.where(mk <= cutoff_val + 1e-9)[0]     # ties at cut included
    n_top = int(len(top_idx))
    corner_pos = {c: set(corner_positions(cand, c).tolist()) for c in CORNERS}
    top_set = set(top_idx.tolist())
    any_corner = set().union(*corner_pos.values())
    share_fav = (len(top_set & corner_pos[fav]) / n_top
                if (fav in corner_pos and n_top) else None)
    share_any = (len(top_set & any_corner) / n_top) if n_top else None

    C, I = cand["C"].to_numpy(), cand["I"].to_numpy()
    cb, ib = _quantile_bin(C, 4), _quantile_bin(I, 4)
    grid_share, enrichment = {}, {}
    for a in range(4):
        for b in range(4):
            cell_mask = (cb == a) & (ib == b)
            pool_share = float(cell_mask.sum()) / n
            top_share = (float(cell_mask[top_idx].sum()) / n_top
                        if n_top else 0.0)
            grid_share[f"{a}_{b}"] = top_share
            enrichment[f"{a}_{b}"] = (top_share / pool_share
                                      if pool_share > 0 else float("nan"))
    return {"n_top": n_top, "cutoff_value": cutoff_val,
           "share_in_favorable": share_fav, "share_in_any_corner": share_any,
           "grid_4x4_share": grid_share, "grid_4x4_enrichment": enrichment}


def run_s1_8(s1_2_result: dict) -> dict:
    rows = []
    for pr_row in s1_2_result["pools"]:
        cid, block, size = pr_row["config_id"], pr_row["block"], pr_row["size"]
        if block == "A":
            pr = s1_2_result["_blockA_pools_cache"][(cid, pr_row["seed_model"], size)]
            tag = MODEL_TAG[pr_row["seed_model"]]
            mk = pr["makespans"][tag]
            fav = (pr_row["corner_quantities_this_model"]["decompositions"]
                          ["full_pool_fit"]["favorable"])
        else:
            pr = s1_2_result["_blockC_pools_cache"][cid]
            mk = pr["makespans"]["M2"]
            fav = (pr_row["corner_quantities_this_model"]["decompositions"]
                          ["full_pool_fit"]["favorable"])
        facet = top1pct_facet(pr["cand"], mk, fav)
        stored = (pr_row["corner_quantities_this_model"]["decompositions"]
                  .get("stored"))
        facet["share_in_stored_favorable"] = (
            top1pct_facet(pr["cand"], mk, stored["favorable"])["share_in_favorable"]
            if stored else None)
        rows.append({"block": block, "config_id": cid,
                   "seed_model": pr_row["seed_model"], "size": size,
                   **facet})
    shares = [r["share_in_favorable"] for r in rows
             if r["share_in_favorable"] is not None]
    median_share = float(np.median(shares)) if shares else float("nan")
    wording = ("concentrate in the favourable corner" if median_share > 0.5
              else "spread across classes")
    return {"per_pool": rows, "median_share_in_favorable": median_share,
           "wording_rule_outcome": wording}


# --------------------------------------------------------------------------
# S1-11 driver
# --------------------------------------------------------------------------

def make_s1_11_configs() -> List[dict]:
    """The 36 complementary-fraction configs, ids 18-53 (S1-11 "Design")."""
    configs = []
    for j in (1, 2):
        pos = 0
        for fi, F in enumerate(cfg.FACTOR_F):
            for ai, A in enumerate(cfg.FACTOR_A):
                demand = cfg.FACTOR_DEMAND[(fi + ai + j) % 3]
                for E in cfg.FACTOR_E:
                    configs.append({"config_id": 18 * j + pos, "F": F,
                                   "n_amrs": A, "n_elevators": E,
                                   "demand": demand})
                    pos += 1
    # cid variable unused after loop rewrite; keep ids as computed above.
    return configs


def _s1_11_config_summary_row(config: dict, size: int, cand_n: int,
                              seed_model: str) -> tuple:
    """One (config, seed model, size) pool, as in Block A: the pool seeded
    for model m, every candidate under M1 and M2, the summary under m."""
    pr = enumerate_pool(config, size, cand_n, seed_model, "A")
    tag = MODEL_TAG[seed_model]
    mk = pr["makespans"][tag]
    beta = fit_phi_beta(pr["cand"], mk)
    fav = favorable_label(beta)
    cq = corner_family_quantities(pr["cand"], mk, {"full_pool_fit": fav})
    pool_row = {"config_id": config["config_id"], "F": config["F"],
               "n_amrs": config["n_amrs"], "n_elevators": config["n_elevators"],
               "demand": config["demand"], "size": size, "seed_model": seed_model,
               "optimum_M1": pool_optimum(pr["makespans"]["M1"]),
               "optimum_M2": pool_optimum(pr["makespans"]["M2"]),
               "corner_quantities_this_model": cq}
    summary_row = {"config_id": config["config_id"], "F": config["F"],
                  "n_amrs": config["n_amrs"], "n_elevators": config["n_elevators"],
                  "demand": config["demand"], "model": tag,
                  "log_median_makespan": float(np.log(cq["m0"])),
                  "GAP": cq["decompositions"]["full_pool_fit"]["GAP"]}
    return pool_row, summary_row


def run_s1_11(sizes: List[int], cand_n: int, existing_configs: List[dict]
             ) -> dict:
    new_configs = make_s1_11_configs()
    pool_rows = []
    per_config_summary = {(m, n): [] for m in ("M1", "M2") for n in sizes}
    for config in new_configs:
        for size in sizes:
            for sm in ("abstraction", "batched"):
                pool_row, summary_row = _s1_11_config_summary_row(
                    config, size, cand_n, sm)
                pool_rows.append(pool_row)
                per_config_summary[(MODEL_TAG[sm], size)].append(summary_row)

    # "Together with S1-2, this gives exact values on the full 54-config
    # factorial" (S1-11 Design) -- merge in the 18 existing Phase 5 configs
    # (re-enumerated here under the same batched/M2 full-pool fit as the new
    # 36, so the main-effects table below is a genuine 54-config factorial,
    # not just the 36 new ones). Re-enumeration is deterministic and cheap
    # relative to this item's own ~864,000-run budget; it is NOT read from
    # any stored artefact.
    for config in existing_configs:
        for size in sizes:
            for sm in ("abstraction", "batched"):
                pool_row, summary_row = _s1_11_config_summary_row(
                    config, size, cand_n, sm)
                pool_row["source"] = "existing_phase5_config_reenumerated"
                pool_rows.append(pool_row)
                per_config_summary[(MODEL_TAG[sm], size)].append(summary_row)

    # REGISTRATION NOTE (experiments_S1_enumeration.py, run_s1_11): "Across
    # the 54 configurations: main effects of F, |A|, E, and demand on the
    # log median makespan and on GAP" does not say which (model, size) slice
    # feeds this table (both S1-2's 18 existing configs and S1-11's 36 new
    # ones supply pools under both seed models at BOTH sizes {8,30}).
    # Implemented literally by reporting the main effects and the F x demand
    # interaction table SEPARATELY for each (model, size) slice, M1 and M2
    # crossed with n in {8, 30}, rather than picking one slice or pooling
    # slices together, neither of which the registration states.
    main_effects_by_size = {}
    for key in per_config_summary:
        rows = list(per_config_summary[key])
        df = pd.DataFrame(rows)
        size = f"{key[0]}_n{key[1]}"
        if df.empty:
            main_effects_by_size[size] = None
            continue
        factors = ["F", "n_amrs", "n_elevators", "demand"]
        effects = {}
        for resp in ("log_median_makespan", "GAP"):
            grand = float(df[resp].mean())
            eff = {}
            for f in factors:
                eff[f] = {str(lvl): float(g[resp].mean()) - grand
                          for lvl, g in df.groupby(f)}
            effects[resp] = {"grand_mean": grand, "effects": eff}
        inter = {}
        for resp in ("log_median_makespan", "GAP"):
            cell = df.groupby(["F", "demand"])[resp].mean()
            inter[resp] = {f"{k[0]}|{k[1]}": float(v) for k, v in cell.items()}
        main_effects_by_size[size] = {"n_configs": len(df), "effects": effects,
                                      "F_x_demand_interaction": inter}
    return {"new_configs": [c["config_id"] for c in new_configs],
           "pools": pool_rows,
           "per_config_summary": {f"{k[0]}_n{k[1]}": v
                                  for k, v in per_config_summary.items()},
           "main_effects_by_size": main_effects_by_size,
           "d_d1_signoff_note": (
               "S1-11 is registered '[NS; only if D-D1 is signed]'. In real "
               "mode it runs only if the 'S1-11 included (D-D1 signed)' line "
               "in AMEND-2026-09-26-S1B_new_simulations.md is ticked '[x] yes'; "
               "this is enforced mechanically by "
               "registration_guard.require_checkbox('S1B', 'S1-11 included', "
               "'yes') in main(), in addition to require_signed('S1B'). "
               "Self-test runs skip both guards and write only to the "
               "scratch directory.")}


# --------------------------------------------------------------------------
# Self-test fixtures
# --------------------------------------------------------------------------

def _toy_configs(n: int = 2) -> List[dict]:
    all_cfg = cfg.make_config_array()
    return all_cfg[:n]


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def _write_out(out: dict, selftest: bool, name: str) -> Path:
    out_path = (scratch_dir() if selftest else RESULTS_DIR) / name
    out.pop("_blockA_pools_cache", None)
    out.pop("_blockC_pools_cache", None)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, default=str)
    return out_path


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("cmd", choices=["s1-2", "s1-8", "s1-11"])
    p.add_argument("--selftest", action="store_true")
    p.add_argument("--cand-n", type=int, default=None)
    args = p.parse_args()

    require_signed("S1B", selftest=args.selftest)
    if args.cmd == "s1-11":            # only if D-D1 is signed (S1B sign-off box)
        require_checkbox("S1B", "S1-11 included", "yes", selftest=args.selftest)

    if args.selftest:
        cfg.SEED_BASE = TOY_SEED_BASE          # patch BEFORE any pool/seed call
        cand_n = args.cand_n or 80
        sizes = [8]
        configs = _toy_configs(2)
    else:
        cand_n = args.cand_n or cfg.CANDIDATE_POOL
        sizes = [8, 30]
        configs = cfg.make_config_array()

    tier2 = (Path(__file__).resolve().parents[2] / "revision_2026-07-08"
             / "tier2_analysis" / "outputs")
    input_paths = ([] if args.cmd == "s1-11" else
                   [RAW_DIR / f for f in ("mvs_v0_5_phase5_blockA.csv",
                                          "mvs_v0_5_phase5_blockA_candidate_ids.csv",
                                          "mvs_v0_5_phase5_blockB.csv",
                                          "mvs_v0_5_phase5_ablation_P7.csv",
                                          "mvs_v0_5_phase5_blockC_tiebreakfix.csv")]
                   + [tier2 / "b2_b3_benchmarks.json",
                      tier2 / "amendC1_p9_spoplus.json"])
    meta = {"registration_sha256": _sha256_file(REG_PATH),
           "code_sha256": _sha256_file(Path(__file__)), **code_provenance(),
           "input_sha256": ({} if args.selftest else
                            {q.name: _sha256_file(q) for q in input_paths
                             if q.exists()}),
           "selftest": args.selftest, "cand_n": cand_n, "sizes": sizes}

    if args.cmd == "s1-2":
        res = run_s1_2(configs, sizes, cand_n, args.selftest)
        out = {**meta, **{k: v for k, v in res.items()
                          if not k.startswith("_")}}
        path = _write_out(out, args.selftest,
                         "v0_5_phase5_S1-2_enumeration.json")
    elif args.cmd == "s1-8":
        s1_2_res = run_s1_2(configs, sizes, cand_n, args.selftest)
        res = run_s1_8(s1_2_res)
        out = {**meta, **res}
        path = _write_out(out, args.selftest, "v0_5_phase5_S1-8_top1pct.json")
    else:  # s1-11
        # Only 2 of the 36 new configs in selftest, for speed.
        if args.selftest:
            orig = make_s1_11_configs
            globals()["make_s1_11_configs"] = lambda: orig()[:2]
        res = run_s1_11(sizes, cand_n, configs if not args.selftest else [])
        out = {**meta, **res}
        path = _write_out(out, args.selftest,
                         "v0_5_phase5_S1-11_factorial.json")

    print(f"S1 enumeration [{args.cmd}] "
         f"{'[selftest] ' if args.selftest else ''}wrote {path}")


if __name__ == "__main__":
    main()
