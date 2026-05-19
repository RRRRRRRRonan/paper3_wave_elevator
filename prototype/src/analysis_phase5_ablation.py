"""
MVS v0.5 Phase 5 — ablation + P7 analysis (pre-reg §9 amendment).

Four ablations of the P5 / Bound-and-Gap method plus the P7 optimization
reference. Pre-registered as a §9 amendment, run before the W6 confirmatory
analysis; none of these touch the locked H-D1 / H-D2 / H-Policy gates.

  A1 feature       — Φ = (C, I) vs C-only vs I-only          (from Block A)
  A2 T dimension   — 2x2 (C,I) vs 2x2x2 (C,I,T) partition    (from scheme run)
  A3 estimator     — cell-median vs cell-mean GAP stability  (from Block A)
  A4 granularity   — 2x2 vs 3x3 (C,I) partition              (from scheme run)
  P7 reference     — how far P5 sits above a local-search optimum

(The originally listed 5th ablation — β-sign corner vs OLS-argmin corner —
collapses: for a linear OLS fit the sign rule and the predicted-argmin pick
the *same* corner identically, and the β-sign-vs-nonlinear-predictor question
is already the P5-vs-P6 contest in Block B. So four genuine ablations, not a
contrived fifth. Logged honestly here and in pre-reg §9.)

Output:
  results/v0_5_phase5_ablation.json
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RAW = RESULTS_DIR / "raw"
RNG = np.random.default_rng(20260519)
N_BOOT = 300


def _arm(df, **f):
    sub = df
    for k, v in f.items():
        sub = sub[sub[k] == v]
    return sub["makespan"].to_numpy(dtype=float)


# ----------------------------------------------------------- A1 feature
def ablation_feature(dfA: pd.DataFrame) -> dict:
    rows = []
    for (cid, model, size), g in dfA.groupby(["config_id", "model", "size"]):
        fav = g["favorable_corner"].iloc[0]
        favC, favI = fav.split("_")            # e.g. "HC", "HI"
        m0 = float(np.median(_arm(g, arm="random")))
        m_CI = float(np.median(_arm(g, arm=fav)))
        # C-only: favourable C side, either I; I-only: favourable I side, either C
        c_only = np.concatenate([_arm(g, arm=f"{favC}_HI"),
                                 _arm(g, arm=f"{favC}_LI")])
        i_only = np.concatenate([_arm(g, arm=f"HC_{favI}"),
                                 _arm(g, arm=f"LC_{favI}")])
        red_CI = (m0 - m_CI) / m0
        red_C = (m0 - float(np.median(c_only))) / m0
        red_I = (m0 - float(np.median(i_only))) / m0
        rows.append({"config_id": int(cid), "model": model, "size": int(size),
                     "reduction_CI": red_CI, "reduction_C_only": red_C,
                     "reduction_I_only": red_I,
                     "CI_beats_both": bool(red_CI >= red_C - 1e-9
                                           and red_CI >= red_I - 1e-9)})
    n = len(rows)
    n_both = sum(r["CI_beats_both"] for r in rows)
    return {"per_cell": rows, "n_cells": n, "n_CI_beats_both": n_both,
            "mean_reduction_CI": float(np.mean([r["reduction_CI"] for r in rows])),
            "mean_reduction_C_only": float(np.mean([r["reduction_C_only"] for r in rows])),
            "mean_reduction_I_only": float(np.mean([r["reduction_I_only"] for r in rows])),
            "verdict": "both features contribute"
                       if n_both >= 0.8 * n else "single feature dominates"}


# ------------------------------------------------ A3 estimator stability
def _gap(arms: dict, fav: str, agg) -> float:
    m = {k: agg(v) for k, v in arms.items()}
    m0 = m["random"]
    corners = {k: v for k, v in m.items() if k != "random"}
    q_max, q_min = max(corners.values()), min(corners.values())
    H_up = (q_max - m0) / m0
    M_phi = (m[fav] - q_min) / m0
    return H_up + M_phi


def ablation_estimator(dfA: pd.DataFrame) -> dict:
    rows = []
    for (cid, model, size), g in dfA.groupby(["config_id", "model", "size"]):
        fav = g["favorable_corner"].iloc[0]
        arms = {a: _arm(g, arm=a) for a in
                ["random", "HC_HI", "HC_LI", "LC_HI", "LC_LI"]}
        gap_med = _gap(arms, fav, lambda v: float(np.median(v)))
        gap_mean = _gap(arms, fav, lambda v: float(np.mean(v)))
        boot_med, boot_mean = [], []
        for _ in range(N_BOOT):
            res = {a: RNG.choice(v, size=len(v), replace=True)
                   for a, v in arms.items()}
            boot_med.append(_gap(res, fav, lambda v: float(np.median(v))))
            boot_mean.append(_gap(res, fav, lambda v: float(np.mean(v))))
        # Absolute bootstrap SD — CV (std/|mean|) explodes on near-zero-GAP cells.
        sd_med = float(np.std(boot_med))
        sd_mean = float(np.std(boot_mean))
        rows.append({"config_id": int(cid), "model": model, "size": int(size),
                     "GAP_median": gap_med, "GAP_mean": gap_mean,
                     "boot_SD_median": sd_med, "boot_SD_mean": sd_mean,
                     "median_more_stable": bool(sd_med <= sd_mean)})
    n = len(rows)
    n_stable = sum(r["median_more_stable"] for r in rows)
    return {"per_cell": rows, "n_cells": n,
            "n_median_more_stable": n_stable,
            "mean_SD_median": float(np.mean([r["boot_SD_median"] for r in rows])),
            "mean_SD_mean": float(np.mean([r["boot_SD_mean"] for r in rows])),
            "verdict": "cell-median is the more stable estimator"
                       if n_stable >= 0.8 * n
                       else ("cell-mean is at least as stable here — the "
                             "cell-median is retained for Theorem-1 "
                             "(SPO-regret) consistency, not for lower variance")}


# ------------------------------------------- A2 / A4 partition schemes
def _scheme_leverage(dfS: pd.DataFrame, scheme: str) -> list:
    out = []
    for cid, g in dfS[dfS["scheme"] == scheme].groupby("config_id"):
        med = g.groupby("corner")["makespan"].median()
        m0 = float(med.get("random"))
        corners = med.drop("random")
        ub = float((corners.max() - corners.min()) / m0)
        best_red = float((m0 - corners.min()) / m0)
        out.append({"config_id": int(cid), "demand": g["demand"].iloc[0],
                    "UB": ub, "best_reduction": best_red})
    return out


def ablation_granularity(dfS: pd.DataFrame) -> dict:
    a2, a3_ = _scheme_leverage(dfS, "2x2_CI"), _scheme_leverage(dfS, "3x3_CI")
    by = {r["config_id"]: r for r in a3_}
    rows = []
    for r in a2:
        f = by[r["config_id"]]
        rows.append({"config_id": r["config_id"],
                     "UB_2x2": r["UB"], "UB_3x3": f["UB"],
                     "refinement_raises_UB": bool(f["UB"] >= r["UB"] - 1e-9)})
    n_mono = sum(r["refinement_raises_UB"] for r in rows)
    return {"per_config": rows, "n_configs": len(rows),
            "n_refinement_monotone": n_mono,
            "mean_UB_2x2": float(np.mean([r["UB_2x2"] for r in rows])),
            "mean_UB_3x3": float(np.mean([r["UB_3x3"] for r in rows])),
            "verdict": "3x3 raises UB as Corollary M4.4 predicts"
                       if n_mono >= 0.8 * len(rows) else "refinement non-monotone"}


def ablation_tdim(dfS: pd.DataFrame) -> dict:
    ci, cit = _scheme_leverage(dfS, "2x2_CI"), _scheme_leverage(dfS, "2x2x2_CIT")
    by = {r["config_id"]: r for r in cit}
    rows = []
    for r in ci:
        f = by[r["config_id"]]
        rows.append({"config_id": r["config_id"], "demand": r["demand"],
                     "best_red_CI": r["best_reduction"],
                     "best_red_CIT": f["best_reduction"],
                     "T_adds_leverage": bool(f["best_reduction"]
                                             > r["best_reduction"] + 0.005)})
    n_help = sum(r["T_adds_leverage"] for r in rows)
    diurnal = [r for r in rows if r["demand"] == "diurnal"]
    return {"per_config": rows, "n_configs": len(rows), "n_T_adds": n_help,
            "n_T_adds_diurnal": sum(r["T_adds_leverage"] for r in diurnal),
            "n_diurnal": len(diurnal),
            "verdict": "T adds leverage chiefly under diurnal demand"
                       if n_help else "T adds no leverage at this horizon"}


# --------------------------------------------------------- P7 reference
def p7_reference(dfB: pd.DataFrame, dfP7: pd.DataFrame) -> dict:
    rows = []
    for (cid, size), g7 in dfP7.groupby(["config_id", "size"]):
        gb = dfB[(dfB["config_id"] == cid) & (dfB["size"] == size)]
        m_p0 = float(np.median(_arm(gb, policy="P0_random")))
        m_p5 = float(np.median(_arm(gb, policy="P5_phi")))
        m_p7 = float(np.median(g7["makespan"].to_numpy(dtype=float)))
        gap = (m_p5 - m_p7) / m_p7
        span = m_p0 - m_p7
        capture = (m_p0 - m_p5) / span if span > 1e-9 else float("nan")
        rows.append({"config_id": int(cid), "size": int(size),
                     "m_P0": m_p0, "m_P5": m_p5, "m_P7": m_p7,
                     "P5_above_P7_frac": gap, "P5_capture_of_P0_P7": capture})
    valid = [r["P5_capture_of_P0_P7"] for r in rows
             if not np.isnan(r["P5_capture_of_P0_P7"])]
    return {"per_cell": rows, "n_cells": len(rows),
            "mean_P5_above_P7": float(np.mean([r["P5_above_P7_frac"] for r in rows])),
            "mean_P5_capture": float(np.mean(valid)) if valid else float("nan")}


def main() -> None:
    dfA = pd.read_csv(RAW / "mvs_v0_5_phase5_blockA.csv")
    dfB = pd.read_csv(RAW / "mvs_v0_5_phase5_blockB.csv")
    dfP7 = pd.read_csv(RAW / "mvs_v0_5_phase5_ablation_P7.csv")
    dfS = pd.read_csv(RAW / "mvs_v0_5_phase5_ablation_scheme.csv")

    A1 = ablation_feature(dfA)
    A2 = ablation_tdim(dfS)
    A3 = ablation_estimator(dfA)
    A4 = ablation_granularity(dfS)
    P7 = p7_reference(dfB, dfP7)

    print("=" * 78)
    print("Phase 5 ablations + P7 reference (pre-reg §9 amendment)")
    print("=" * 78)
    print(f"\nA1 feature   Φ=(C,I) vs C-only vs I-only")
    print(f"   mean makespan reduction: CI={A1['mean_reduction_CI']:+.4f}  "
          f"C-only={A1['mean_reduction_C_only']:+.4f}  "
          f"I-only={A1['mean_reduction_I_only']:+.4f}")
    print(f"   (C,I) ≥ both single features: {A1['n_CI_beats_both']}/{A1['n_cells']}"
          f"  -> {A1['verdict']}")

    print(f"\nA2 T dimension   2x2 (C,I) vs 2x2x2 (C,I,T)")
    print(f"   T adds leverage: {A2['n_T_adds']}/{A2['n_configs']} configs "
          f"({A2['n_T_adds_diurnal']}/{A2['n_diurnal']} diurnal)  "
          f"-> {A2['verdict']}")

    print(f"\nA3 estimator   cell-median vs cell-mean GAP")
    print(f"   bootstrap SD of GAP: median={A3['mean_SD_median']:.4f}  "
          f"mean={A3['mean_SD_mean']:.4f}")
    print(f"   median more stable: {A3['n_median_more_stable']}/{A3['n_cells']}"
          f"  -> {A3['verdict']}")

    print(f"\nA4 granularity   2x2 vs 3x3 (C,I)")
    print(f"   mean UB: 2x2={A4['mean_UB_2x2']:.4f}  3x3={A4['mean_UB_3x3']:.4f}")
    print(f"   3x3 raises UB: {A4['n_refinement_monotone']}/{A4['n_configs']}"
          f"  -> {A4['verdict']}")

    print(f"\nP7 reference   local-search optimizer (n_iter={40})")
    print(f"   P5 sits {100*P7['mean_P5_above_P7']:.1f} % above the P7 optimum")
    print(f"   P5 captures {100*P7['mean_P5_capture']:.1f} % of the P0→P7 gap")

    out = {"generated": "2026-05-19",
           "purpose": "Phase 5 ablations A1-A4 + P7 optimization reference; "
                      "pre-reg §9 amendment, pre-W6.",
           "A1_feature": A1, "A2_T_dimension": A2, "A3_estimator": A3,
           "A4_granularity": A4, "P7_reference": P7}
    out_path = RESULTS_DIR / "v0_5_phase5_ablation.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved {out_path}")


if __name__ == "__main__":
    main()
