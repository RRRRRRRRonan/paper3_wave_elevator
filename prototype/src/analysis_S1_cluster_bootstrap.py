"""
S1-1 -- Candidate-clustered bootstrap for the Phase 5 intervals [RA].

Registration: revision_2026-09-26_ijpr/amendments/AMEND-2026-09-26-S1A_reanalyses.md
(section "S1-1. Candidate-clustered bootstrap for the Phase 5 intervals [RA]").
Guard key: "S1A" (author_signoff PENDING as of 2026-09-26 -- real mode refuses
to run until signed; --selftest exercises the code on fabricated data only).

Corner arms of Blocks A and C draw N_PER_ARM waves WITH REPLACEMENT from a
finite corner class, so the same candidate_id repeats within an arm. The
stored bootstraps (analysis_phase5_blockA.py, analysis_phase5_blockC.py)
resample ROWS as if independent, which understates interval width. This
script resamples CLUSTERS (= distinct candidate_id) instead, keeping each
drawn cluster's full row multiplicity, and reports the result BESIDE the
locked row-level verdict -- never in place of it (S1-1 "Reporting rule").

Real mode reads only the CSVs the registration names, under
prototype/results/raw/, and writes exactly one new file:
  results/v0_5_phase5_S1-1_cluster_bootstrap.json
Self-test mode (--selftest) never touches prototype/results; it fabricates
small synthetic CSVs with the same column schema, runs the identical code
path, and writes to registration_guard.scratch_dir().

Run:
  python -m src.analysis_S1_cluster_bootstrap            # stops at the guard
  python -m src.analysis_S1_cluster_bootstrap --selftest # toy run to scratch
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

from src.analysis_phase5_blockA import CORNERS, decompose
from src.registration_guard import require_signed, scratch_dir

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RAW_DIR = RESULTS_DIR / "raw"
OUT_NAME = "v0_5_phase5_S1-1_cluster_bootstrap.json"
REG_PATH = (Path(__file__).resolve().parents[2] / "revision_2026-09-26_ijpr"
            / "amendments" / "AMEND-2026-09-26-S1A_reanalyses.md")

ARMS_WITH_RANDOM = ["random"] + CORNERS

# Registered constants (S1-1 "Procedure").
B_MAIN = 2000
SEED_MAIN = 20260927
# Seed sensitivity: seeds 20260927 + i, i = 0, ..., 9 (i = 0 is the primary
# seed), as the registration states since its 2026-09-26 clarification.
SENSITIVITY_SEEDS = [SEED_MAIN + i for i in range(10)]
B_REF = 1000
SEED_REF = 20260519           # == phase5_config.SEED_BASE, but used here only
                               # as analysis_phase5_blockA.SEED (a bootstrap
                               # RNG seed for resampling STORED rows), never
                               # to seed a simulation -- see module docstring.
STORED_D1D = 57
STORED_D1D_N = 72


# --------------------------------------------------------------------------
# Small utilities
# --------------------------------------------------------------------------

def _sha256_file(path: Path) -> str:
    """Line-ending-normalized SHA-256 (the guard's definition), so
    recorded hashes match MANIFEST_SIGNED.json."""
    from src.registration_guard import sha256_file
    return sha256_file(path)


def cluster_resample_indices(cluster_ids: np.ndarray,
                             rng: np.random.Generator) -> np.ndarray:
    """Row positions for ONE clustered-bootstrap draw.

    Draws as many clusters (= distinct values of `cluster_ids`) as there are
    distinct clusters, uniformly with replacement; each drawn cluster
    contributes every one of its rows (multiplicity of repeated candidate
    draws is kept), per S1-1 "Procedure".
    """
    uniq, inverse = np.unique(cluster_ids, return_inverse=True)
    buckets = [np.where(inverse == k)[0] for k in range(len(uniq))]
    draw = rng.integers(0, len(uniq), size=len(uniq))
    return np.concatenate([buckets[k] for k in draw])


def _percentile_ci(x: np.ndarray) -> Tuple[float, float]:
    lo, hi = np.percentile(x, [2.5, 97.5])
    return float(lo), float(hi)


def _check_join(main_df: pd.DataFrame, ids_df: pd.DataFrame,
                key_cols: List[str], label: str) -> pd.DataFrame:
    """Join `ids_df` onto `main_df` by row_index == row position; verify
    `key_cols` agree row by row (S1-1 Inputs: "The join is checked row by
    row ... any mismatch stops the analysis")."""
    if len(main_df) != len(ids_df):
        raise SystemExit(
            f"S1-1 join check FAILED for {label}: row counts differ "
            f"({len(main_df)} vs {len(ids_df)})")
    ids_sorted = ids_df.sort_values("row_index").reset_index(drop=True)
    main_r = main_df.reset_index(drop=True)
    for col in key_cols:
        a = main_r[col].astype(str).to_numpy()
        b = ids_sorted[col].astype(str).to_numpy()
        mism = np.where(a != b)[0]
        if len(mism):
            i = int(mism[0])
            raise SystemExit(
                f"S1-1 join check FAILED for {label} at row {i}: column "
                f"{col!r} mismatch ({a[i]!r} vs {b[i]!r})")
    out = main_r.copy()
    out["candidate_id"] = ids_sorted["candidate_id"].to_numpy()
    out["cand_seed"] = ids_sorted["cand_seed"].to_numpy()
    return out


# --------------------------------------------------------------------------
# Block A: clustered GAP bootstrap
# --------------------------------------------------------------------------

def _blockA_subcell_arrays(g: pd.DataFrame) -> Tuple[Dict[str, np.ndarray],
                                                      Dict[str, np.ndarray]]:
    vals, clus = {}, {}
    for arm in ARMS_WITH_RANDOM:
        a = g[g["arm"] == arm].reset_index(drop=True)
        vals[arm] = a["makespan"].to_numpy(float)
        clus[arm] = a["candidate_id"].to_numpy()
    return vals, clus


def _blockA_gap_boot(vals, clus, fav: str, B: int,
                     rng: np.random.Generator) -> np.ndarray:
    boot = np.empty(B)
    for b in range(B):
        m_q = {}
        for c in CORNERS:
            idx = cluster_resample_indices(clus[c], rng)
            m_q[c] = float(np.median(vals[c][idx]))
        idx0 = cluster_resample_indices(clus["random"], rng)
        m0 = float(np.median(vals["random"][idx0]))
        h, mp, *_ = decompose(m_q, m0, fav)
        boot[b] = h + mp
    return boot


def _blockA_point_gap(vals, fav: str) -> float:
    m_q = {c: float(np.median(vals[c])) for c in CORNERS}
    m0 = float(np.median(vals["random"]))
    h, mp, *_ = decompose(m_q, m0, fav)
    return h + mp


def reference_row_level_blockA(df: pd.DataFrame, B: int = B_REF,
                               seed: int = SEED_REF) -> int:
    """Re-run the STORED row-level bootstrap unchanged (identical code path
    to analysis_phase5_blockA.decompose / analysis_phase5_blockA.main), and
    return the D1-d count. One shared RNG stream across sub-cells, matching
    analysis_phase5_blockA.py's own loop structure exactly."""
    rng = np.random.default_rng(seed)
    g_d = 0
    for (_cid, _model, _size), g in df.groupby(["config_id", "model", "size"]):
        fav = g["favorable_corner"].iloc[0]
        arms = {c: g[g["arm"] == c]["makespan"].to_numpy(float) for c in CORNERS}
        rnd = g[g["arm"] == "random"]["makespan"].to_numpy(float)
        boot = np.empty(B)
        for b in range(B):
            mb = {c: float(np.median(rng.choice(arms[c], size=len(arms[c]),
                                                 replace=True)))
                  for c in CORNERS}
            m0b = float(np.median(rng.choice(rnd, size=len(rnd), replace=True)))
            hb, mpb, *_ = decompose(mb, m0b, fav)
            boot[b] = hb + mpb
        lo, _hi = _percentile_ci(boot)
        g_d += int(lo > 0.0)
    return g_d


def blockA_clustered(df: pd.DataFrame, B: int, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    rows = []
    for (cid, model, size), g in df.groupby(["config_id", "model", "size"]):
        fav = g["favorable_corner"].iloc[0]
        vals, clus = _blockA_subcell_arrays(g)
        boot = _blockA_gap_boot(vals, clus, fav, B, rng)
        lo, hi = _percentile_ci(boot)
        rows.append({"config_id": int(cid), "model": str(model),
                     "size": int(size), "favorable_corner": fav,
                     "gap_ci_lo": lo, "gap_ci_hi": hi,
                     "d1d": bool(lo > 0.0)})
    d1d_count = sum(r["d1d"] for r in rows)
    return {"per_subcell": rows, "n_subcells": len(rows), "d1d_count": d1d_count}


def blockA_dedup_companion(df: pd.DataFrame, B: int, seed: int) -> dict:
    """Deduplicated companion: each distinct candidate_id counted once per
    arm; point GAP estimate plus a plain ROW bootstrap of the deduplicated
    rows (S1-1 Procedure, "Companion (deduplicated) analysis")."""
    rng = np.random.default_rng(seed)
    rows = []
    for (cid, model, size), g in df.groupby(["config_id", "model", "size"]):
        fav = g["favorable_corner"].iloc[0]
        vals = {}
        for arm in ARMS_WITH_RANDOM:
            a = g[g["arm"] == arm].drop_duplicates(subset=["candidate_id"],
                                                    keep="first")
            vals[arm] = a["makespan"].to_numpy(float)
        point_gap = _blockA_point_gap(vals, fav)
        boot = np.empty(B)
        for b in range(B):
            m_q = {c: float(np.median(rng.choice(vals[c], size=len(vals[c]),
                                                  replace=True)))
                  for c in CORNERS}
            m0 = float(np.median(rng.choice(vals["random"],
                                            size=len(vals["random"]),
                                            replace=True)))
            h, mp, *_ = decompose(m_q, m0, fav)
            boot[b] = h + mp
        lo, hi = _percentile_ci(boot)
        rows.append({"config_id": int(cid), "model": str(model),
                     "size": int(size), "point_gap": point_gap,
                     "gap_ci_lo": lo, "gap_ci_hi": hi, "d1d": bool(lo > 0.0)})
    return {"per_subcell": rows, "n_subcells": len(rows),
           "d1d_count": sum(r["d1d"] for r in rows)}


def run_blockA(df: pd.DataFrame) -> dict:
    ref_count = reference_row_level_blockA(df)
    if ref_count != STORED_D1D:
        raise SystemExit(
            f"S1-1 reference-row check FAILED: row-level bootstrap "
            f"reproduced {ref_count}/{STORED_D1D_N}, expected "
            f"{STORED_D1D}/{STORED_D1D_N} (stored). Stopping before any "
            "clustered analysis is reported, per the registration's "
            "Procedure ('If it does not, the analysis stops...').")
    # row-level seed sensitivity (registration S1-1): the locked count is
    # seed-dependent; report the stored procedure over seeds 20260519 + i
    row_level_range = [reference_row_level_blockA(df, B_REF, SEED_REF + i)
                       for i in range(10)]
    main = blockA_clustered(df, B_MAIN, SEED_MAIN)
    sens_counts = []
    for s in SENSITIVITY_SEEDS:
        r = blockA_clustered(df, B_MAIN, s) if s != SEED_MAIN else main
        sens_counts.append(r["d1d_count"])
    dedup = blockA_dedup_companion(df, B_MAIN, SEED_MAIN)
    return {
        "reference_row_level": {"B": B_REF, "seed": SEED_REF,
                                "d1d_count": ref_count,
                                "matches_stored": True,
                                "stored_d1d": f"{STORED_D1D}/{STORED_D1D_N}",
                                "seed_sensitivity_counts": row_level_range,
                                "seed_sensitivity_range": [min(row_level_range),
                                                           max(row_level_range)]},
        "clustered": {"B": B_MAIN, "seed": SEED_MAIN, **main},
        "clustered_seed_sensitivity": {"seeds": SENSITIVITY_SEEDS,
                                       "d1d_counts": sens_counts,
                                       "range": [min(sens_counts),
                                                max(sens_counts)]},
        "deduplicated_companion": dedup,
    }


# --------------------------------------------------------------------------
# Block B: clustered policy-median intervals + paired differences
# --------------------------------------------------------------------------

POLICIES_B = ["P0_random", "P1_dest_cluster", "P2_cardinality",
             "P3_dir_balanced", "P4_temporal", "P5_phi", "P6_spo_tree"]
PAIRED_AGAINST = ["P0_random", "P1_dest_cluster", "P6_spo_tree"]


def blockB_clustered(df: pd.DataFrame, dfP7: pd.DataFrame, B: int,
                     seed: int) -> dict:
    rng = np.random.default_rng(seed)
    policy_rows = []
    paired_rows = []
    for (cid, size), g in df.groupby(["config_id", "size"]):
        cell_vals, cell_clus = {}, {}
        for p in POLICIES_B:
            a = g[g["policy"] == p].reset_index(drop=True)
            cell_vals[p] = a["makespan"].to_numpy(float)
            cell_clus[p] = a["candidate_id"].to_numpy()
            boot = np.empty(B)
            for b in range(B):
                idx = cluster_resample_indices(cell_clus[p], rng)
                boot[b] = np.median(cell_vals[p][idx])
            lo, hi = _percentile_ci(boot)
            policy_rows.append({"config_id": int(cid), "size": int(size),
                               "policy": p,
                               "median": float(np.median(cell_vals[p])),
                               "ci_lo": lo, "ci_hi": hi})
        # P7: independent runs, row-level bootstrap (no candidate_id).
        g7 = dfP7[(dfP7["config_id"] == cid) & (dfP7["size"] == size)]
        v7 = g7["makespan"].to_numpy(float)
        boot7 = np.array([np.median(rng.choice(v7, size=len(v7), replace=True))
                          for _ in range(B)])
        lo7, hi7 = _percentile_ci(boot7)
        policy_rows.append({"config_id": int(cid), "size": int(size),
                           "policy": "P7_localsearch",
                           "median": float(np.median(v7)),
                           "ci_lo": lo7, "ci_hi": hi7,
                           "note": "row-level bootstrap (independent runs, "
                                   "no candidate_id)"})
        # Paired differences P5 - {P0, P1, P6} (S1-1 "Statistics reported").
        # REGISTRATION NOTE (analysis_S1_cluster_bootstrap.py, ~line 240):
        # the registration names the three paired differences but does not
        # specify (a) whether the CI is per (config,size) cell or pooled
        # across cells, or (b) how the two policies' resamples are coupled.
        # Most literal reading implemented: per-cell CI, with each policy's
        # clusters resampled independently within the cell (mirroring the
        # "within each arm independently" rule from the general Procedure),
        # differenced per replicate. The cross-cell aggregate reported is
        # the plain mean of the per-cell POINT differences; no pooled CI is
        # constructed, since a pooling rule across heterogeneous cells is
        # not specified.
        for other in PAIRED_AGAINST:
            boot_p5 = np.array([
                np.median(cell_vals["P5_phi"][
                    cluster_resample_indices(cell_clus["P5_phi"], rng)])
                for _ in range(B)])
            boot_o = np.array([
                np.median(cell_vals[other][
                    cluster_resample_indices(cell_clus[other], rng)])
                for _ in range(B)])
            diff_boot = boot_p5 - boot_o
            lo_d, hi_d = _percentile_ci(diff_boot)
            point_diff = (float(np.median(cell_vals["P5_phi"]))
                         - float(np.median(cell_vals[other])))
            paired_rows.append({"config_id": int(cid), "size": int(size),
                               "pair": f"P5_phi - {other}",
                               "point_diff": point_diff,
                               "ci_lo": lo_d, "ci_hi": hi_d})
    mean_point_diff = {}
    for other in PAIRED_AGAINST:
        pair = f"P5_phi - {other}"
        vals = [r["point_diff"] for r in paired_rows if r["pair"] == pair]
        mean_point_diff[pair] = float(np.mean(vals))
    return {"per_policy_cell": policy_rows, "paired_differences": paired_rows,
           "mean_point_diff_across_cells": mean_point_diff}


# --------------------------------------------------------------------------
# Block C: clustered per-wave ordering-rate intervals
# --------------------------------------------------------------------------

def blockC_clustered(df: pd.DataFrame, B: int, seed: int) -> dict:
    # REGISTRATION NOTE (analysis_S1_cluster_bootstrap.py, ~line 300): S1-1
    # defines clusters as "one distinct candidate_id within (config, model,
    # size, arm) ... for Blocks A and C". Block C's matched-wave CSV is
    # wide-format (one row carries makespan_M1 AND makespan_M2 together, so
    # there is no per-row "model" split) and size is fixed at 16 in both the
    # primary and secondary (tie-break-fixed) Block C inputs used here. The
    # literal cluster key therefore collapses to (config, arm) for Block C;
    # implemented as such below.
    rng = np.random.default_rng(seed)
    cell_vals: Dict[tuple, Dict[str, np.ndarray]] = {}
    cell_clus: Dict[tuple, np.ndarray] = {}
    for (cid, arm), g in df.groupby(["config_id", "arm"]):
        if arm not in CORNERS:
            continue
        a = g.reset_index(drop=True)
        cell_vals[(cid, arm)] = {"M1": a["makespan_M1"].to_numpy(float),
                                 "M2": a["makespan_M2"].to_numpy(float)}
        cell_clus[(cid, arm)] = a["candidate_id"].to_numpy()

    keys = list(cell_vals)
    per_cell_boot = {k: np.empty(B) for k in keys}
    for b in range(B):
        for k in keys:
            idx = cluster_resample_indices(cell_clus[k], rng)
            m1, m2 = cell_vals[k]["M1"][idx], cell_vals[k]["M2"][idx]
            per_cell_boot[k][b] = float(np.mean(m2 >= m1))
    avg_boot = np.mean(np.vstack([per_cell_boot[k] for k in keys]), axis=0)
    worst_boot = np.min(np.vstack([per_cell_boot[k] for k in keys]), axis=0)

    per_cell_rows = []
    for k in keys:
        cid, arm = k
        point = float(np.mean(cell_vals[k]["M2"] >= cell_vals[k]["M1"]))
        lo, hi = _percentile_ci(per_cell_boot[k])
        per_cell_rows.append({"config_id": int(cid), "arm": arm,
                             "point_ordering_rate": point,
                             "ci_lo": lo, "ci_hi": hi})
    avg_lo, avg_hi = _percentile_ci(avg_boot)
    worst_lo, worst_hi = _percentile_ci(worst_boot)
    return {"n_cells": len(keys), "per_cell": per_cell_rows,
           "average_ci": {"lo": avg_lo, "hi": avg_hi},
           "worst_cell_ci": {"lo": worst_lo, "hi": worst_hi}}


# --------------------------------------------------------------------------
# Real-data loaders (never invoked before the guard passes)
# --------------------------------------------------------------------------

def _load_real_inputs() -> dict:
    paths = {
        "blockA": RAW_DIR / "mvs_v0_5_phase5_blockA.csv",
        "blockA_ids": RAW_DIR / "mvs_v0_5_phase5_blockA_candidate_ids.csv",
        "blockB": RAW_DIR / "mvs_v0_5_phase5_blockB.csv",
        "blockB_ids": RAW_DIR / "mvs_v0_5_phase5_blockB_candidate_ids.csv",
        "blockB_P7": RAW_DIR / "mvs_v0_5_phase5_ablation_P7.csv",
        "blockC": RAW_DIR / "mvs_v0_5_phase5_blockC.csv",
        "blockC_ids": RAW_DIR / "mvs_v0_5_phase5_blockC_candidate_ids.csv",
        "blockC_tiebreakfix": RAW_DIR / "mvs_v0_5_phase5_blockC_tiebreakfix.csv",
    }
    dfs = {k: pd.read_csv(p) for k, p in paths.items()}
    hashes = {k: _sha256_file(p) for k, p in paths.items()}
    return dfs, hashes, paths


def run_real() -> dict:
    dfs, hashes, paths = _load_real_inputs()

    a = _check_join(dfs["blockA"], dfs["blockA_ids"],
                    ["config_id", "model", "size", "arm"], "Block A")
    b = _check_join(dfs["blockB"], dfs["blockB_ids"],
                    ["config_id", "model", "size", "policy"], "Block B")
    c_primary = _check_join(dfs["blockC"], dfs["blockC_ids"],
                            ["config_id", "size", "arm"], "Block C (primary)")
    c_secondary = dfs["blockC_tiebreakfix"]   # candidate_id already embedded

    out = {
        "registration_sha256": _sha256_file(REG_PATH),
        "code_sha256": _sha256_file(Path(__file__)),
        "input_sha256": hashes,
        "selftest": False,
        "blockA": run_blockA(a),
        "blockB": blockB_clustered(b, dfs["blockB_P7"], B_MAIN, SEED_MAIN),
        "blockC_primary": blockC_clustered(c_primary, B_MAIN, SEED_MAIN),
        "blockC_secondary_tiebreakfix": blockC_clustered(
            c_secondary, B_MAIN, SEED_MAIN),
    }
    return out


# --------------------------------------------------------------------------
# Self-test: synthetic fixtures with the same column schema
# --------------------------------------------------------------------------

def _fabricate_blockA(rng: random.Random) -> Tuple[pd.DataFrame, pd.DataFrame]:
    rows, id_rows = [], []
    ri = 0
    for cid in (0, 1):
        for model in ("abstraction", "batched"):
            fav = "HC_HI"
            for arm in ARMS_WITH_RANDOM:
                n_cand = 6          # distinct candidates in this arm's class
                base = 100.0 + 5 * cid + (3 if arm == fav else 8)
                cand_vals = [base + rng.uniform(-2, 2) for _ in range(n_cand)]
                for _ in range(20):                     # 20 draws w/ repeats
                    cid_pick = rng.randrange(n_cand)
                    mk = cand_vals[cid_pick] + rng.uniform(-0.5, 0.5)
                    rows.append({"config_id": cid, "F": 5, "n_amrs": 10,
                               "n_elevators": 2, "demand": "uniform",
                               "model": model, "size": 8, "arm": arm,
                               "favorable_corner": fav, "makespan": mk})
                    id_rows.append({"row_index": ri, "config_id": cid,
                                   "model": model, "size": 8, "arm": arm,
                                   "candidate_id": cid_pick,
                                   "cand_seed": 1, "pool_seed": 1})
                    ri += 1
    return pd.DataFrame(rows), pd.DataFrame(id_rows)


def _fabricate_blockB(rng: random.Random) -> Tuple[pd.DataFrame, pd.DataFrame,
                                                    pd.DataFrame]:
    rows, id_rows, p7_rows = [], [], []
    ri = 0
    for cid in (0,):
        for size in (8,):
            for p in POLICIES_B:
                n_cand = 6
                base = 100.0 + (5 if p == "P5_phi" else 12)
                cand_vals = [base + rng.uniform(-2, 2) for _ in range(n_cand)]
                for _ in range(20):
                    cpick = rng.randrange(n_cand)
                    mk = cand_vals[cpick] + rng.uniform(-0.5, 0.5)
                    rows.append({"config_id": cid, "F": 5, "n_amrs": 10,
                               "n_elevators": 2, "demand": "uniform",
                               "model": "batched", "size": size,
                               "policy": p, "makespan": mk})
                    id_rows.append({"row_index": ri, "config_id": cid,
                                   "model": "batched", "size": size,
                                   "policy": p, "candidate_id": cpick,
                                   "cand_seed": 1, "pool_seed": 1,
                                   "favorable_corner_stored": "HC_HI",
                                   "favorable_corner_refit": "HC_HI"})
                    ri += 1
            for wid in range(10):
                p7_rows.append({"config_id": cid, "F": 5, "n_amrs": 10,
                               "n_elevators": 2, "demand": "uniform",
                               "size": size, "policy": "P7_localsearch",
                               "wave_id": wid,
                               "makespan": 95.0 + rng.uniform(-3, 3)})
    return pd.DataFrame(rows), pd.DataFrame(id_rows), pd.DataFrame(p7_rows)


def _fabricate_blockC(rng: random.Random) -> Tuple[pd.DataFrame, pd.DataFrame,
                                                    pd.DataFrame]:
    rows, id_rows, tb_rows = [], [], []
    ri = 0
    for cid in (0,):
        for arm in CORNERS:
            n_cand = 6
            base1 = 100.0
            for _ in range(20):
                cpick = rng.randrange(n_cand)
                m1 = base1 + cpick + rng.uniform(-0.5, 0.5)
                m2 = m1 - rng.uniform(0.0, 6.0)         # M2 <= M1 usually
                wid = _
                rows.append({"config_id": cid, "F": 5, "n_amrs": 10,
                           "n_elevators": 2, "demand": "uniform", "size": 16,
                           "arm": arm, "wave_id": wid,
                           "makespan_M1": m1, "makespan_M2": m2,
                           "makespan_M3_s20": m2})
                id_rows.append({"row_index": ri, "config_id": cid, "size": 16,
                               "arm": arm, "wave_id": wid,
                               "candidate_id": cpick, "cand_seed": 1,
                               "pool_seed": 1})
                tb_rows.append({"config_id": cid, "F": 5, "n_amrs": 10,
                               "n_elevators": 2, "demand": "uniform",
                               "size": 16, "arm": arm, "wave_id": wid,
                               "candidate_id": cpick, "cand_seed": 1,
                               "makespan_M1": m1 + 0.1, "makespan_M2": m2 + 0.1,
                               "makespan_M3_s20": m2 + 0.1})
                ri += 1
    return pd.DataFrame(rows), pd.DataFrame(id_rows), pd.DataFrame(tb_rows)


def run_selftest(B: int) -> dict:
    rng = random.Random(9001)   # local fixture seed, unrelated to any
                                # registered simulation seed (Rule 2)
    a, a_ids = _fabricate_blockA(rng)
    b, b_ids, p7 = _fabricate_blockB(rng)
    c, c_ids, c_tb = _fabricate_blockC(rng)

    a_joined = _check_join(a, a_ids, ["config_id", "model", "size", "arm"],
                           "Block A [selftest]")
    b_joined = _check_join(b, b_ids, ["config_id", "model", "size", "policy"],
                           "Block B [selftest]")
    c_joined = _check_join(c, c_ids, ["config_id", "size", "arm"],
                           "Block C [selftest]")

    # Reference-row-level reproducibility check, selftest form: run the
    # UNCHANGED row-level function twice on the same synthetic data and
    # require an identical count (we cannot check against the real stored
    # 57/72, since that would require reading stored data -- forbidden
    # tonight under Absolute Rule 1).
    ref1 = reference_row_level_blockA(a_joined, B=200, seed=SEED_REF)
    ref2 = reference_row_level_blockA(a_joined, B=200, seed=SEED_REF)
    if ref1 != ref2:
        raise SystemExit(
            "S1-1 selftest FAILED: the row-level bootstrap function is not "
            f"reproducible on identical synthetic data + seed ({ref1} != "
            f"{ref2}); this would also break the real-mode hard stop.")

    blockA_main = blockA_clustered(a_joined, B, SEED_MAIN)
    sens = [blockA_clustered(a_joined, B, s)["d1d_count"]
           for s in SENSITIVITY_SEEDS[:3]]     # 3 seeds is enough to smoke it
    dedup = blockA_dedup_companion(a_joined, B, SEED_MAIN)
    blockB_out = blockB_clustered(b_joined, p7, B, SEED_MAIN)
    blockC_out = blockC_clustered(c_joined, B, SEED_MAIN)
    blockC_tb_out = blockC_clustered(c_tb, B, SEED_MAIN)

    return {
        "registration_sha256": _sha256_file(REG_PATH),
        "code_sha256": _sha256_file(Path(__file__)),
        "input_sha256": "n/a (selftest: fabricated in-memory, not read from disk)",
        "selftest": True,
        "reference_row_level_reproducibility_check": {"ref1": ref1, "ref2": ref2,
                                                       "match": ref1 == ref2},
        "blockA": {"clustered": {"B": B, "seed": SEED_MAIN, **blockA_main},
                  "seed_sensitivity_3of10_smoke": sens,
                  "deduplicated_companion": dedup},
        "blockB": blockB_out,
        "blockC_primary": blockC_out,
        "blockC_secondary_tiebreakfix": blockC_tb_out,
    }


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--selftest", action="store_true",
                  help="toy run on fabricated data, writes to scratch_dir()")
    p.add_argument("--B", type=int, default=None,
                  help="bootstrap replicate count (default 2000 real, "
                       "200 selftest)")
    args = p.parse_args()

    require_signed("S1A", selftest=args.selftest)

    if args.selftest:
        B = args.B if args.B is not None else 200
        out = run_selftest(B)
        out_path = scratch_dir() / OUT_NAME
    else:
        out = run_real()
        out_path = RESULTS_DIR / OUT_NAME

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"S1-1 {'[selftest] ' if args.selftest else ''}wrote {out_path}")


if __name__ == "__main__":
    main()
