"""
S1-6 / S1-7 / TH-2 -- Registered re-analysis displays on stored Phase 5 data [RA].

Registration: revision_2026-09-26_ijpr/amendments/AMEND-2026-09-26-S1A_reanalyses.md
  S1-6  "Minimax-regret row and stability of the Hedge corner"
  S1-7  "Supp-1 coupling display" [RA, prior-exposed]
  TH-2  "Abstraction-bias display"
Guard key: "S1A" (author_signoff PENDING as of 2026-09-26).

None of these three changes a locked verdict (S1A "General rules" #1); each
is reported beside the locked result. Real mode reads the stored raw CSVs
the registration names and never executes tonight: `require_signed("S1A")`
stops the script first. Self-test mode never touches prototype/results; it
fabricates small synthetic CSVs with the same column schema and writes to
registration_guard.scratch_dir().

Run:
  python -m src.analysis_S1_displays s1-6             # stops at the guard
  python -m src.analysis_S1_displays s1-6 --selftest  # toy run to scratch
  python -m src.analysis_S1_displays s1-7 --selftest
  python -m src.analysis_S1_displays th-2 --selftest
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import warnings
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

from src.analysis_phase5_blockA import CORNERS
from src.analysis_S1_cluster_bootstrap import _check_join
from src.experiments_S1_blockC_ext import (_class_stat_dict,
                                           clustered_stability,
                                           hedge_and_minimax)
from src.registration_guard import require_signed, scratch_dir

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RAW_DIR = RESULTS_DIR / "raw"
FIG_DIR = RESULTS_DIR / "figures"
REG_PATH = (Path(__file__).resolve().parents[2] / "revision_2026-09-26_ijpr"
            / "amendments" / "AMEND-2026-09-26-S1A_reanalyses.md")

BLOCK_C_CONFIGS = [1, 3, 5, 7, 9, 11]
STAB_B_DEFAULT = 2000
STAB_SEED = 20260928
# S1-6 "Wording rule (locked)": the locked D2-d collapse count, reported
# UNCHANGED beside this [RA] display -- a fixed reference value from the
# General rules of AMEND-2026-09-26-S1A_reanalyses.md, not recomputed here.
LOCKED_D2D_COLLAPSE = "6/6"


def _sha256_file(path: Path) -> str:
    """Line-ending-normalized SHA-256 (the guard's definition), so
    recorded hashes match MANIFEST_SIGNED.json."""
    from src.registration_guard import sha256_file
    return sha256_file(path)


# ==========================================================================
# S1-6: minimax-regret row and Hedge-corner stability
# ==========================================================================

def run_s1_6(B: int, selftest: bool) -> dict:
    if selftest:
        primary, secondary = _fabricate_blockC_pair()
    else:
        blockC = pd.read_csv(RAW_DIR / "mvs_v0_5_phase5_blockC.csv")
        blockC_ids = pd.read_csv(RAW_DIR / "mvs_v0_5_phase5_blockC_candidate_ids.csv")
        primary = _check_join(blockC, blockC_ids, ["config_id", "size", "arm"],
                              "Block C (S1-6 primary)")
        secondary = pd.read_csv(RAW_DIR / "mvs_v0_5_phase5_blockC_tiebreakfix.csv")

    rows = []
    for label, df in (("primary_stored", primary),
                      ("secondary_tiebreakfix", secondary)):
        for cid in sorted(df["config_id"].unique()):
            gc = df[df["config_id"] == cid]
            for basis, agg in (("mean", np.mean), ("median", np.median)):
                hm = hedge_and_minimax(_class_stat_dict(gc, agg))
                stab = clustered_stability(gc, agg, B, STAB_SEED)
                margin = hm["second_place_margin"]
                rows.append({
                    "source": label, "config_id": int(cid), "basis": basis,
                    "hedge_corner": hm["hedge_corner"],
                    "minimax_regret_corner": hm["minimax_regret_corner"],
                    "agree_hedge_vs_minimax": bool(
                        hm["hedge_corner"] == hm["minimax_regret_corner"]),
                    "second_place_margin": margin,
                    "hedge_stability": stab["hedge_stability"],
                    "minimax_regret_stability": stab["minimax_regret_stability"],
                    "near_tie": bool(margin < 0.01),
                    "not_stable_under_resampling": bool(
                        stab["hedge_stability"] < 0.80),
                })
    # mean vs median agreement, per source/config (S1-6 "Display")
    agree_rows = []
    by_key = {(r["source"], r["config_id"], r["basis"]): r for r in rows}
    for label in ("primary_stored", "secondary_tiebreakfix"):
        cids = sorted({r["config_id"] for r in rows if r["source"] == label})
        for cid in cids:
            rm = by_key[(label, cid, "mean")]
            rd = by_key[(label, cid, "median")]
            agree_rows.append({
                "source": label, "config_id": cid,
                "mean_hedge": rm["hedge_corner"], "median_hedge": rd["hedge_corner"],
                "mean_median_agree": bool(rm["hedge_corner"] == rd["hedge_corner"])})
    return {"B": B, "seed": STAB_SEED, "locked_D2d_collapse": LOCKED_D2D_COLLAPSE,
           "per_config_basis": rows, "mean_vs_median_agreement": agree_rows}


# ==========================================================================
# S1-7: Supp-1 coupling display
# ==========================================================================

EXPECTED_OPS = {"fifo", "cluster"}
EXPECTED_ARMS = {"random", "phi_corner"}


def run_s1_7(selftest: bool) -> dict:
    if selftest:
        df = _fabricate_supp1()
        supp_json_hash = "n/a (selftest: fabricated in-memory)"
    else:
        df = pd.read_csv(RAW_DIR / "mvs_v0_5_supp1_h1scale.csv")
        supp_json_path = RESULTS_DIR / "v0_5_phase5_supp.json"
        # REGISTRATION NOTE (analysis_S1_displays.py, run_s1_7): S1-7 lists
        # `v0_5_phase5_supp.json` among its Inputs (for the "already stored
        # as MV" dispatch-gain figure). Absolute Rule 1 tonight forbids
        # loading values out of ANY stored result file, and this script's
        # real-mode path is written to run correctly after sign-off, not
        # tonight -- but to avoid depending on an internal JSON schema this
        # session never inspected, every S1-7 quantity below (including the
        # dispatch gain) is recomputed directly from the raw CSV instead of
        # parsed out of that JSON. The JSON is only hashed, for the audit
        # trail the output format requires.
        supp_json_hash = (_sha256_file(supp_json_path)
                          if supp_json_path.exists() else None)

    ops_vals = set(df["ops_policy"].astype(str).str.lower().unique())
    arm_vals = set(df["arm"].astype(str).str.lower().unique())
    if not EXPECTED_OPS.issubset(ops_vals):
        raise SystemExit(f"S1-7: unexpected ops_policy values {ops_vals}, "
                         f"expected a superset of {EXPECTED_OPS}")
    if not EXPECTED_ARMS.issubset(arm_vals):
        raise SystemExit(f"S1-7: unexpected arm values {arm_vals}, "
                         f"expected a superset of {EXPECTED_ARMS}")
    df = df.copy()
    df["ops_policy"] = df["ops_policy"].astype(str).str.lower()
    df["arm"] = df["arm"].astype(str).str.lower()

    cell_rows = []
    for (cid, size), g in df.groupby(["config_id", "size"]):
        for r in ("fifo", "cluster"):
            gr = g[g["ops_policy"] == r]
            med_rand = gr[gr["arm"] == "random"]["makespan"].median()
            med_phi = gr[gr["arm"] == "phi_corner"]["makespan"].median()
            A_r = (float(med_rand) - float(med_phi)) / float(med_rand)
            cell_rows.append({"config_id": int(cid), "size": int(size),
                            "dispatch": r, "median_random": float(med_rand),
                            "median_phi_corner": float(med_phi), "A": A_r})
    cell_df = pd.DataFrame(cell_rows)

    aggregates = {}
    for r in ("fifo", "cluster"):
        sub = cell_df[cell_df["dispatch"] == r]
        mean_of_ratios = float(sub["A"].mean())
        ratio_of_grand_means = float(
            (sub["median_random"].mean() - sub["median_phi_corner"].mean())
            / sub["median_random"].mean())
        n_pos = int((sub["A"] > 0).sum())
        aggregates[r] = {"n_cells": len(sub), "mean_of_cell_ratios": mean_of_ratios,
                        "ratio_of_grand_means": ratio_of_grand_means,
                        "n_cells_positive": n_pos}

    # REGISTRATION NOTE (analysis_S1_displays.py, run_s1_7): the wording rule
    # reads "A_cluster > 0 in at least 9 of 12 cells under both aggregates",
    # but "cells with A_cluster > 0" is a single per-cell sign count,
    # independent of which of the two aggregation formulas (mean-of-ratios
    # vs ratio-of-grand-means) is used to SUMMARISE the 12 ratios -- the
    # aggregates do not each induce their own "positive cell" count. Read
    # literally as: the persistence flag uses the (aggregation-invariant)
    # count of A_cluster > 0 cells against the 9/12 threshold, and BOTH
    # aggregate values are reported alongside it as the registration
    # separately requires ("the mean of per-cell A_r, and the ratio of grand
    # means").
    # Clarified in the registration (2026-09-26): at least 9 of 12 cells with
    # A_cluster > 0 AND both aggregates of A_cluster positive.
    n_pos_cluster = aggregates["cluster"]["n_cells_positive"]
    n_cells_cluster = aggregates["cluster"]["n_cells"]
    persists = (n_pos_cluster >= 9 and n_cells_cluster == 12
                and aggregates["cluster"]["mean_of_cell_ratios"] > 0
                and aggregates["cluster"]["ratio_of_grand_means"] > 0)
    wording = ("persisting under clustered dispatch" if persists
              else "not robust to the dispatch rule")

    # Dispatch gain per arm: (median FIFO - median cluster) / median FIFO.
    gain_rows = []
    for (cid, size, arm), g in df.groupby(["config_id", "size", "arm"]):
        med_fifo = g[g["ops_policy"] == "fifo"]["makespan"].median()
        med_cluster = g[g["ops_policy"] == "cluster"]["makespan"].median()
        if pd.isna(med_fifo) or pd.isna(med_cluster) or med_fifo == 0:
            continue
        gain_rows.append({"config_id": int(cid), "size": int(size), "arm": arm,
                        "median_fifo": float(med_fifo),
                        "median_cluster": float(med_cluster),
                        "dispatch_gain": (float(med_fifo) - float(med_cluster))
                                        / float(med_fifo)})

    return {"supp_json_sha256": supp_json_hash, "per_cell": cell_rows,
           "aggregates": aggregates, "wording_rule_outcome": wording,
           "n_cells_A_cluster_positive": f"{n_pos_cluster}/{n_cells_cluster}",
           "dispatch_gain_per_arm": gain_rows}


# ==========================================================================
# TH-2: abstraction-bias display
# ==========================================================================

def _add_bias(df: pd.DataFrame, m1_col: str, m2_col: str) -> pd.DataFrame:
    df = df.copy()
    df["B"] = (df[m2_col] - df[m1_col]) / df[m1_col]
    return df


def _dedup(df: pd.DataFrame) -> pd.DataFrame:
    if "candidate_id" in df.columns:
        return df.drop_duplicates(
            subset=[c for c in ("config_id", "size", "arm", "candidate_id")
                   if c in df.columns], keep="first")
    return df           # no identifiers: dedup == as-drawn (Supp-2 rows)


def _facet_stats(df: pd.DataFrame, by: str) -> dict:
    out = {}
    for lvl, g in df.groupby(by):
        out[str(lvl)] = {"n": int(len(g)), "median_B": float(g["B"].median()),
                        "iqr_B": [float(g["B"].quantile(0.25)),
                                 float(g["B"].quantile(0.75))],
                        "reversal_share": float((g["B"] < 0).mean())}
    return out


def run_th2(selftest: bool, s1_3_csv: Optional[Path]) -> tuple:
    if selftest:
        primary, secondary = _fabricate_blockC_pair()
        primary, secondary = _add_bias(primary, "makespan_M1", "makespan_M2"), \
                             _add_bias(secondary, "makespan_M1", "makespan_M2")
        supp2 = _add_bias(_fabricate_supp2(), "makespan_M1", "makespan_M2")
        s1_3 = None
    else:
        # TH-2 Inputs: PRIMARY is the tie-break-fixed CSV here (opposite of
        # S1-1's primary/secondary convention -- TH-2's own text: "primary:
        # tie-break-fixed CSV, which reflects the current simulator;
        # secondary: stored CSV").
        primary = _add_bias(
            pd.read_csv(RAW_DIR / "mvs_v0_5_phase5_blockC_tiebreakfix.csv"),
            "makespan_M1", "makespan_M2")
        blockC = pd.read_csv(RAW_DIR / "mvs_v0_5_phase5_blockC.csv")
        blockC_ids = pd.read_csv(RAW_DIR / "mvs_v0_5_phase5_blockC_candidate_ids.csv")
        secondary = _add_bias(
            _check_join(blockC, blockC_ids, ["config_id", "size", "arm"],
                       "Block C (TH-2 secondary)"),
            "makespan_M1", "makespan_M2")
        supp2 = _add_bias(pd.read_csv(RAW_DIR / "mvs_v0_5_supp2_capacity.csv"),
                          "makespan_M1", "makespan_M2")
        s1_3 = None
        path = s1_3_csv or (RAW_DIR / "mvs_v0_5_phase5_S1-3_blockC_ext.csv")
        if path.exists():
            s1_3 = pd.read_csv(path)
            if "abstraction_bias" in s1_3.columns:
                s1_3 = s1_3.rename(columns={"abstraction_bias": "B"})
            else:
                s1_3 = _add_bias(s1_3, "makespan_M1", "makespan_M2")

    headline_primary = primary[(primary["size"] == 16)
                              & (primary["config_id"].isin(BLOCK_C_CONFIGS))]
    headline_median = float(headline_primary["B"].median())
    headline_iqr = [float(headline_primary["B"].quantile(0.25)),
                    float(headline_primary["B"].quantile(0.75))]
    wording = (f"In this benchmark the throughput abstraction is optimistic "
              f"by a median of {100*headline_median:.1f}% (interquartile "
              f"range {100*headline_iqr[0]:.1f}% to {100*headline_iqr[1]:.1f}%)")

    result = {
        "headline": {"source": "primary_tiebreakfix_size16_block_c_configs",
                    "median_B": headline_median, "iqr_B": headline_iqr,
                    "wording": wording,
                    "reversal_share": float((headline_primary["B"] < 0).mean())},
        "primary_as_drawn": {"n": int(len(primary)),
                            "median_B": float(primary["B"].median()),
                            "reversal_share": float((primary["B"] < 0).mean())},
        "primary_dedup": {"n": int(len(_dedup(primary))),
                         "median_B": float(_dedup(primary)["B"].median())},
        "secondary_as_drawn": {"n": int(len(secondary)),
                              "median_B": float(secondary["B"].median())},
        "facet_E": _facet_stats(primary, "n_elevators"),
        "facet_F": _facet_stats(primary, "F"),
        "facet_n_size16_only": _facet_stats(primary, "size"),
        "facet_c_supp2": _facet_stats(supp2, "capacity"),
        "s1_3_extension_available": s1_3 is not None,
    }
    if s1_3 is not None:
        combined_n = pd.concat([primary[["size", "B"]], s1_3[["size", "B"]]],
                              ignore_index=True)
        result["facet_n_with_S1-3_extension"] = _facet_stats(combined_n, "size")
    return result, primary, secondary, supp2


def _th2_figure(result: dict, out_path: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")   # silent fallback if the font is absent
        import matplotlib.pyplot as plt
        plt.rcParams["font.family"] = "Times New Roman"
        facets = [("facet_E", "elevators E"), ("facet_F", "floors F"),
                 ("facet_c_supp2", "capacity c")]
        fig, axes = plt.subplots(1, len(facets), figsize=(4 * len(facets), 3.2))
        if len(facets) == 1:
            axes = [axes]
        for ax, (key, title) in zip(axes, facets):
            facet = result.get(key, {})
            levels = sorted(facet.keys(), key=lambda s: float(s))
            meds = [100 * facet[l]["median_B"] for l in levels]
            lo = [100 * facet[l]["median_B"] - 100 * facet[l]["iqr_B"][0]
                 for l in levels]
            hi = [100 * facet[l]["iqr_B"][1] - 100 * facet[l]["median_B"]
                 for l in levels]
            ax.errorbar(range(len(levels)), meds, yerr=[lo, hi], fmt="o",
                       capsize=4, color="#2b6cb0")
            ax.axhline(0.0, color="gray", linewidth=0.8, linestyle="--")
            ax.set_xticks(range(len(levels)))
            ax.set_xticklabels(levels)
            ax.set_title(f"B by {title}")
            ax.set_ylabel("abstraction bias B (%)")
        fig.suptitle("TH-2: throughput-abstraction bias, median +/- IQR")
        fig.tight_layout()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_path, dpi=150)
        plt.close(fig)


# ==========================================================================
# Self-test fixtures
# ==========================================================================

def _fabricate_blockC_pair():
    rng = random.Random(9002)
    rows_p, rows_s = [], []
    for cid in (0, 1):
        for arm in CORNERS:
            for wid in range(20):
                cpick = rng.randrange(6)
                m1 = 100.0 + cpick + rng.uniform(-0.5, 0.5)
                # Mostly M2 >= M1 (abstraction optimistic, B > 0), with an
                # occasional reversal -- a more representative smoke fixture
                # for TH-2's median/IQR/reversal-share than a one-sided draw.
                m2 = m1 + rng.uniform(-3.0, 10.0)
                rows_p.append({"config_id": cid, "F": 5, "n_amrs": 10,
                             "n_elevators": 2, "demand": "uniform", "size": 16,
                             "arm": arm, "wave_id": wid, "candidate_id": cpick,
                             "makespan_M1": m1, "makespan_M2": m2,
                             "makespan_M3_s20": m2})
                rows_s.append({"config_id": cid, "F": 5, "n_amrs": 10,
                             "n_elevators": 2, "demand": "uniform", "size": 16,
                             "arm": arm, "wave_id": wid, "candidate_id": cpick,
                             "makespan_M1": m1 + 0.1, "makespan_M2": m2 + 0.1,
                             "makespan_M3_s20": m2 + 0.1})
    return pd.DataFrame(rows_p), pd.DataFrame(rows_s)


def _fabricate_supp1() -> pd.DataFrame:
    rng = random.Random(9003)
    rows = []
    for cid in (0, 1):
        for size in (8, 30):
            for arm, base in (("random", 110.0), ("phi_corner", 100.0)):
                for ops in ("fifo", "cluster"):
                    penalty = 0.0 if ops == "fifo" else -4.0
                    for wid in range(15):
                        rows.append({"config_id": cid, "F": 5, "n_amrs": 10,
                                   "n_elevators": 2, "demand": "uniform",
                                   "size": size, "arm": arm, "ops_policy": ops,
                                   "wave_id": wid,
                                   "makespan": base + penalty
                                              + rng.uniform(-3, 3)})
    return pd.DataFrame(rows)


def _fabricate_supp2() -> pd.DataFrame:
    rng = random.Random(9004)
    rows = []
    for cid in (0,):
        for cap in (2, 3, 4, 5):
            for arm in CORNERS:
                for wid in range(10):
                    m1 = 120.0 - 2 * cap + rng.uniform(-1, 1)
                    m2 = m1 - rng.uniform(0.0, 5.0)
                    rows.append({"config_id": cid, "F": 5, "n_amrs": 10,
                               "n_elevators": 2, "demand": "uniform",
                               "capacity": cap, "arm": arm, "wave_id": wid,
                               "makespan_M1": m1, "makespan_M2": m2})
    return pd.DataFrame(rows)


# ==========================================================================
# CLI
# ==========================================================================

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("cmd", choices=["s1-6", "s1-7", "th-2"])
    p.add_argument("--selftest", action="store_true")
    p.add_argument("--B", type=int, default=None)
    p.add_argument("--s1-3-csv", type=str, default=None)
    args = p.parse_args()

    require_signed("S1A", selftest=args.selftest)

    inputs = {"s1-6": ["mvs_v0_5_phase5_blockC.csv",
                       "mvs_v0_5_phase5_blockC_candidate_ids.csv",
                       "mvs_v0_5_phase5_blockC_tiebreakfix.csv"],
              "s1-7": ["mvs_v0_5_supp1_h1scale.csv"],
              "th-2": ["mvs_v0_5_phase5_blockC_tiebreakfix.csv",
                       "mvs_v0_5_phase5_blockC.csv",
                       "mvs_v0_5_phase5_blockC_candidate_ids.csv",
                       "mvs_v0_5_supp2_capacity.csv",
                       "mvs_v0_5_phase5_S1-3_blockC_ext.csv"]}[args.cmd]
    input_paths = [RAW_DIR / f for f in inputs]
    if args.cmd == "s1-7":
        input_paths.append(RESULTS_DIR / "v0_5_phase5_supp.json")
    meta = {"registration_sha256": _sha256_file(REG_PATH),
           "code_sha256": _sha256_file(Path(__file__)),
           "input_sha256": ({} if args.selftest else
                            {q.name: _sha256_file(q) for q in input_paths
                             if q.exists()}),
           "selftest": args.selftest}
    out_dir = scratch_dir() if args.selftest else RESULTS_DIR

    if args.cmd == "s1-6":
        B = args.B or (100 if args.selftest else STAB_B_DEFAULT)
        res = run_s1_6(B, args.selftest)
        out = {**meta, **res}
        path = out_dir / "v0_5_phase5_S1-6_minimax_stability.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2, default=str)
        print(f"S1-6 {'[selftest] ' if args.selftest else ''}wrote {path}")

    elif args.cmd == "s1-7":
        res = run_s1_7(args.selftest)
        out = {**meta, **res}
        path = out_dir / "v0_5_phase5_S1-7_supp1_coupling.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2, default=str)
        print(f"S1-7 {'[selftest] ' if args.selftest else ''}wrote {path}")

    else:  # th-2
        s1_3_path = Path(args.s1_3_csv) if args.s1_3_csv else None
        res, *_frames = run_th2(args.selftest, s1_3_path)
        out = {**meta, **res}
        json_path = out_dir / "v0_5_phase5_TH-2_abstraction_bias.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2, default=str)
        fig_dir = out_dir if args.selftest else FIG_DIR
        fig_path = fig_dir / "TH-2_abstraction_bias.png"
        _th2_figure(res, fig_path)
        print(f"TH-2 {'[selftest] ' if args.selftest else ''}wrote {json_path} "
             f"and {fig_path}")


if __name__ == "__main__":
    main()
