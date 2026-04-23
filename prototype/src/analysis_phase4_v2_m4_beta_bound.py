"""
MVS v0.2 Phase 4 v2 — Calibration of Corollary M4.3 (beta-based lower bound on H_up).

For each (regime, model, size) cell:
  1) Fit OLS  m = m_0 + beta_C * C + beta_I * I   on per-wave (C, I, makespan)
  2) Estimate centroid offsets C_0 := |C - mean(C)|.mean(), I_0 likewise
  3) Compute beta-based bound:  H_up_pred := (|beta_C| C_0 + |beta_I| I_0 - sigma*sqrt(K)) / m_0
       sigma := residual std,  K := number of corners (4 for 2x2)
  4) Compare with empirically observed H_up from v0_2_phase4_v2_m4_decomposition.json.

Pre-reg gate (Task C item):
  beta-based bound is within 30% of observed H_up in >= 4/6 cells (size-aggregated)
   -> M4.3 reported as empirically calibrated; otherwise downgrade to "loose but informative".

Output:
  results/v0_2_phase4_v2_m4_beta_bound.json
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RAW_DIR = RESULTS_DIR / "raw"
PARTITION_CSV = RAW_DIR / "mvs_v0_2_phase4_v2_partition_samples.csv"
DECOMP_JSON = RESULTS_DIR / "v0_2_phase4_v2_m4_decomposition.json"

REGIMES = ["E1_c2", "E2_c2", "E3_c2"]
MODELS = ["abstraction", "batched"]
SIZES = [4, 6, 8]
K = 4  # number of corners in 2x2 partition


def fit_ols(C, I, m):
    """Fit m = a + bC*C + bI*I via least squares; return (a, bC, bI, sigma_resid)."""
    X = np.column_stack([np.ones_like(C), C, I])
    coef, *_ = np.linalg.lstsq(X, m, rcond=None)
    a, bC, bI = coef
    pred = X @ coef
    resid = m - pred
    sigma = float(np.std(resid, ddof=3))
    return float(a), float(bC), float(bI), sigma


def main() -> None:
    df = pd.read_csv(PARTITION_CSV)
    decomp = json.load(open(DECOMP_JSON))
    obs_lookup = {(r["regime"], r["model"], r["size"]): r for r in decomp["per_cell_size"]}

    print("=" * 110)
    print("M4.3 calibration — beta-based lower bound on H_up")
    print("=" * 110)
    print(f"{'regime':8s} {'model':12s} {'sz':>3s}  "
          f"{'m_0':>7s}  {'beta_C':>8s} {'beta_I':>8s} {'sigma':>6s}  "
          f"{'C_0':>5s} {'I_0':>5s}  "
          f"{'H_up_pred':>10s} {'H_up_obs':>9s}  {'rel_err':>8s} {'within30?':>9s}")

    rows = []
    for regime in REGIMES:
        for model in MODELS:
            for size in SIZES:
                sub = df[(df["regime"] == regime) & (df["model"] == model)
                         & (df["size"] == size)]
                if len(sub) < 10:
                    continue
                C = sub["C"].to_numpy(dtype=float)
                I = sub["I"].to_numpy(dtype=float)
                m = sub["makespan"].to_numpy(dtype=float)
                a, bC, bI, sigma = fit_ols(C, I, m)
                m0 = float(np.median(m))  # use median for consistency with H_up definition
                C0 = float(np.mean(np.abs(C - np.mean(C))))
                I0 = float(np.mean(np.abs(I - np.mean(I))))
                deterministic = abs(bC) * C0 + abs(bI) * I0
                noise_pen = sigma * np.sqrt(K)
                H_up_pred = (deterministic - noise_pen) / m0

                obs = obs_lookup.get((regime, model, size), {})
                H_up_obs = obs.get("H_up", float("nan"))

                if np.isnan(H_up_obs) or H_up_obs <= 0:
                    rel = float("nan")
                    within = False
                else:
                    rel = (H_up_pred - H_up_obs) / H_up_obs
                    within = abs(rel) <= 0.30

                print(f"{regime:8s} {model:12s} {size:>3d}  "
                      f"{m0:>7.2f}  {bC:>8.3f} {bI:>8.3f} {sigma:>6.2f}  "
                      f"{C0:>5.3f} {I0:>5.3f}  "
                      f"{H_up_pred:>10.4f} {H_up_obs:>9.4f}  "
                      f"{rel:>+8.2%} {'YES' if within else 'no':>9s}")

                rows.append({
                    "regime": regime,
                    "model": model,
                    "size": size,
                    "m_0": m0,
                    "beta_C": bC,
                    "beta_I": bI,
                    "sigma_resid": sigma,
                    "C_0": C0,
                    "I_0": I0,
                    "H_up_pred": H_up_pred,
                    "H_up_obs": H_up_obs,
                    "relative_error": rel if not np.isnan(rel) else None,
                    "within_30pct": bool(within),
                })

    # Cell-level aggregation (size-mean predictor vs observed)
    print()
    print("=" * 110)
    print("Cell-level (size-averaged) calibration")
    print("=" * 110)
    print(f"{'cell':25s}  {'mean H_up_pred':>14s}  {'mean H_up_obs':>13s}  "
          f"{'rel_err':>8s}  {'within30?':>9s}")

    cell_rows = []
    n_cells_within = 0
    for regime in REGIMES:
        for model in MODELS:
            cell = f"{regime}|{model}"
            sub = [r for r in rows if r["regime"] == regime and r["model"] == model]
            if not sub:
                continue
            mean_pred = float(np.mean([r["H_up_pred"] for r in sub]))
            mean_obs = float(np.mean([r["H_up_obs"] for r in sub]))
            if mean_obs > 0:
                rel = (mean_pred - mean_obs) / mean_obs
                within = abs(rel) <= 0.30
            else:
                rel = float("nan"); within = False
            if within:
                n_cells_within += 1
            print(f"{cell:25s}  {mean_pred:>14.4f}  {mean_obs:>13.4f}  "
                  f"{rel:>+8.2%}  {'YES' if within else 'no':>9s}")
            cell_rows.append({
                "cell": cell,
                "regime": regime,
                "model": model,
                "mean_H_up_pred": mean_pred,
                "mean_H_up_obs": mean_obs,
                "relative_error": rel if not np.isnan(rel) else None,
                "within_30pct": within,
            })

    n_cells = len(cell_rows)
    print()
    print("Pre-reg gate (Task C, M4.3):")
    print(f"  Cells with |rel_err| <= 30%: {n_cells_within}/{n_cells}")
    if n_cells_within >= 4:
        verdict = "CALIBRATED — M4.3 reported as empirically tight"
    elif n_cells_within >= 2:
        verdict = "PARTIAL — M4.3 reported as informative but loose"
    else:
        verdict = "LOOSE — M4.3 reported with caveat about residual noise"
    print(f"  Verdict: {verdict}")

    out = {
        "generated": "2026-04-22",
        "purpose": "Calibration of Corollary M4.3 beta-based lower bound on H_up.",
        "per_cell_size": rows,
        "per_cell_aggregate": cell_rows,
        "summary": {
            "n_cells": n_cells,
            "n_within_30pct": n_cells_within,
            "verdict": verdict,
        },
    }
    out_path = RESULTS_DIR / "v0_2_phase4_v2_m4_beta_bound.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved {out_path}")


if __name__ == "__main__":
    main()
