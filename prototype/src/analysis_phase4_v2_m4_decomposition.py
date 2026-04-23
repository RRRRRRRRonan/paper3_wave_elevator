"""
MVS v0.2 Phase 4 v2 — Numerical verification of Proposition M4.1.

Decomposes GAP = H_up + M_Phi per (regime, model, size) cell and verifies:
  1) GAP equals H_up + M_Phi exactly (sanity of the algebra).
  2) Both H_up and M_Phi are individually non-negative.
  3) Reports the per-cell diagnostic reading:
       - Large H_up / small M_Phi  -> Phi near-optimal, partition intrinsic
       - Small H_up / large M_Phi  -> Phi miscalibrated, corners flat
       - Large both                -> Phi feature expansion is high priority
       - Small both                -> wave planning lever is small

Output:
  results/v0_2_phase4_v2_m4_decomposition.json
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RAW_DIR = RESULTS_DIR / "raw"
CSV = RAW_DIR / "mvs_v0_2_phase4_v2_samples.csv"

REGIMES = ["E1_c2", "E2_c2", "E3_c2"]
MODELS = ["abstraction", "batched"]
SIZES = [4, 6, 8]
CORNERS = ["HC_HI", "HC_LI", "LC_HI", "LC_LI"]


def med(df, regime, model, size, arm):
    sub = df[(df["regime"] == regime) & (df["model"] == model)
             & (df["size"] == size) & (df["arm"] == arm)]
    if len(sub) == 0:
        return float("nan")
    return float(np.median(sub["makespan"]))


def main() -> None:
    df = pd.read_csv(CSV)

    print("=" * 88)
    print("M4.1 numerical verification — GAP = H_up + M_Phi")
    print("=" * 88)
    print(f"{'regime':8s} {'model':12s} {'sz':>3s}  "
          f"{'q_max':>6s} {'q_Phi':>6s} {'q_min':>6s}  "
          f"{'H_up':>7s} {'M_Phi':>7s} {'GAP':>7s}  "
          f"{'UB-LB':>7s} {'match?':>7s}")

    rows = []
    for regime in REGIMES:
        for model in MODELS:
            for size in SIZES:
                # Corner medians
                m_q = {q: med(df, regime, model, size, q) for q in CORNERS}
                m_random = med(df, regime, model, size, "random")
                # Identify corners
                q_max = max(m_q, key=m_q.get)
                q_min = min(m_q, key=m_q.get)
                # favorable_corner is the same across rows for a cell; grab one
                fav_rows = df[(df["regime"] == regime) & (df["model"] == model)
                              & (df["size"] == size)]
                q_phi = fav_rows["favorable_corner"].iloc[0]
                m_phi = m_q[q_phi]
                # Components
                H_up = (m_q[q_max] - m_random) / m_random
                M_phi = (m_phi - m_q[q_min]) / m_random
                gap_decomposed = H_up + M_phi
                # Original UB, LB (from bg_robust definition)
                UB = (m_q[q_max] - m_q[q_min]) / m_random
                LB = (m_random - m_phi) / m_random
                gap_ublb = UB - LB
                # Sanity: must match within float tolerance
                match = abs(gap_decomposed - gap_ublb) < 1e-9

                print(f"{regime:8s} {model:12s} {size:>3d}  "
                      f"{q_max:>6s} {q_phi:>6s} {q_min:>6s}  "
                      f"{H_up:>7.4f} {M_phi:>7.4f} {gap_decomposed:>7.4f}  "
                      f"{gap_ublb:>7.4f} {'YES' if match else 'NO':>7s}")

                rows.append({
                    "regime": regime,
                    "model": model,
                    "size": size,
                    "q_max": q_max,
                    "q_Phi": q_phi,
                    "q_min": q_min,
                    "m_random": m_random,
                    "m_q_max": m_q[q_max],
                    "m_q_Phi": m_phi,
                    "m_q_min": m_q[q_min],
                    "H_up": H_up,
                    "M_Phi": M_phi,
                    "GAP_decomposed": gap_decomposed,
                    "GAP_ublb": gap_ublb,
                    "decomposition_matches": match,
                    "H_up_nonneg": H_up >= -1e-12,
                    "M_Phi_nonneg": M_phi >= -1e-12,
                })

    # Cell-level aggregation (average across sizes per (regime, model) cell)
    print()
    print("=" * 88)
    print("Cell-level (size-averaged) diagnostic reading")
    print("=" * 88)
    print(f"{'cell':25s}  {'mean H_up':>10s}  {'mean M_Phi':>10s}  "
          f"{'mean GAP':>10s}  {'dominant component':>20s}  {'diagnosis':>30s}")

    cell_rows = []
    for regime in REGIMES:
        for model in MODELS:
            cell = f"{regime}|{model}"
            sub = [r for r in rows if r["regime"] == regime and r["model"] == model]
            mean_H = np.mean([r["H_up"] for r in sub])
            mean_M = np.mean([r["M_Phi"] for r in sub])
            mean_G = mean_H + mean_M
            # Diagnostic
            if mean_H > 0.04 and mean_M < 0.02:
                diagnosis = "Phi near-optimal, invest E+"
            elif mean_H < 0.02 and mean_M > 0.04:
                diagnosis = "Phi miscalibrated, fix features"
            elif mean_H > 0.04 and mean_M > 0.04:
                diagnosis = "High priority: Phi expansion"
            elif mean_H < 0.02 and mean_M < 0.02:
                diagnosis = "Wave lever small here"
            else:
                diagnosis = "mixed / moderate"
            dominant = "H_up" if mean_H > mean_M else ("M_Phi" if mean_M > mean_H else "tied")

            print(f"{cell:25s}  {mean_H:>10.4f}  {mean_M:>10.4f}  "
                  f"{mean_G:>10.4f}  {dominant:>20s}  {diagnosis:>30s}")

            cell_rows.append({
                "cell": cell,
                "regime": regime,
                "model": model,
                "mean_H_up": float(mean_H),
                "mean_M_Phi": float(mean_M),
                "mean_GAP": float(mean_G),
                "dominant_component": dominant,
                "diagnosis": diagnosis,
            })

    # Overall gates
    n_cells = len(rows)
    n_match = sum(1 for r in rows if r["decomposition_matches"])
    n_H_nonneg = sum(1 for r in rows if r["H_up_nonneg"])
    n_M_nonneg = sum(1 for r in rows if r["M_Phi_nonneg"])

    print()
    print("Corollary M4.2 verification gates:")
    print(f"  GAP = H_up + M_Phi exactly:  {n_match}/{n_cells}")
    print(f"  H_up >= 0:                   {n_H_nonneg}/{n_cells}")
    print(f"  M_Phi >= 0:                  {n_M_nonneg}/{n_cells}")

    verdict = "PASS" if (n_match == n_cells and n_H_nonneg == n_cells
                         and n_M_nonneg == n_cells) else "PARTIAL"
    print(f"  Overall:                     {verdict}")

    out = {
        "generated": "2026-04-22",
        "purpose": "Numerical verification of Proposition M4.1 (GAP decomposition) "
                   "and Corollary M4.2 (non-negativity).",
        "per_cell_size": rows,
        "per_cell_aggregate": cell_rows,
        "summary": {
            "n_cells_size": n_cells,
            "n_decomposition_matches": n_match,
            "n_H_up_nonneg": n_H_nonneg,
            "n_M_Phi_nonneg": n_M_nonneg,
            "verdict": verdict,
        },
    }
    out_path = RESULTS_DIR / "v0_2_phase4_v2_m4_decomposition.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved {out_path}")


if __name__ == "__main__":
    main()
