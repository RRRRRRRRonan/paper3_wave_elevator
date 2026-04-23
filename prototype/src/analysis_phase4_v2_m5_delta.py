"""
MVS v0.2 Phase 4 v2 — Numerical verification of Corollary M5.2 (one-sided bound).

For each (regime, corner) cell, compute:
  1) eps_c   := P[T_M2 < T_M1 | W ~ W_c]                     (a.s. dominance violation freq.)
  2) U_c(eps) := q_{0.5+eps}(T_M2|c) - q_{0.5}(T_M2|c)       (one-sided wiggle room)
  3) m_1^c, m_2^c                                            (paired medians)
  4) Median bound gate: m_1^c - m_2^c <= U_c(eps)            (M5.2 prediction)

Per-regime collapse verification:
  5) c*_{M2} := argmin_c m_2^c
  6) c*_actual := argmin_c max(m_1^c, m_2^c)                 (true minimax corner)
  7) Stable-argmin sufficient condition:
        min_{c != c*_M2} (m_2^c - m_2^{c*_M2}) > max_c U_c(eps)

M3 stochastic extension (sigma = 0.20): expected knife-edge regime.

Output:
  results/v0_2_phase4_v2_m5_delta.json
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RAW_DIR = RESULTS_DIR / "raw"
CSV = RAW_DIR / "mvs_v0_2_phase4_v2_m3_samples.csv"

REGIMES = ["E1_c2", "E2_c2", "E3_c2"]
CORNERS = ["HC_HI", "HC_LI", "LC_HI", "LC_LI"]


def quantile_safe(arr, q):
    arr = np.asarray(arr, dtype=float)
    if len(arr) == 0:
        return float("nan")
    q = float(np.clip(q, 0.0, 1.0))
    return float(np.quantile(arr, q))


def main() -> None:
    df = pd.read_csv(CSV)

    print("=" * 105)
    print("M5.2 numerical verification — one-sided bound U_c(eps) on M1 vs M2")
    print("=" * 105)
    print(f"{'regime':8s} {'corner':8s}  {'n':>4s}  "
          f"{'eps':>6s}  {'m1':>7s} {'m2':>7s} {'m1-m2':>7s}  "
          f"{'U_c':>7s}  {'gate?':>6s}")

    rows = []
    cell_max_U = {}
    m1_per = {regime: {} for regime in REGIMES}
    m2_per = {regime: {} for regime in REGIMES}

    for regime in REGIMES:
        max_U = 0.0
        for corner in CORNERS:
            sub = df[(df["regime"] == regime) & (df["arm"] == corner)]
            n = len(sub)
            if n == 0:
                continue
            T1 = sub["makespan_M1"].to_numpy()
            T2 = sub["makespan_M2"].to_numpy()

            eps = float(np.mean(T2 < T1))
            m1 = float(np.median(T1))
            m2 = float(np.median(T2))
            signed_gap = m1 - m2

            U_c = quantile_safe(T2, 0.5 + eps) - quantile_safe(T2, 0.5)

            # M5.2 median bound: m_1^c - m_2^c <= U_c(eps)
            gate = signed_gap <= U_c + 1e-9

            print(f"{regime:8s} {corner:8s}  {n:>4d}  "
                  f"{eps:>6.4f}  {m1:>7.2f} {m2:>7.2f} {signed_gap:>7.2f}  "
                  f"{U_c:>7.2f}  {'YES' if gate else 'NO':>6s}")

            m1_per[regime][corner] = m1
            m2_per[regime][corner] = m2
            max_U = max(max_U, U_c)

            rows.append({
                "regime": regime,
                "corner": corner,
                "n": n,
                "epsilon": eps,
                "m1": m1,
                "m2": m2,
                "signed_gap_m1_minus_m2": signed_gap,
                "U_c_oneSided": U_c,
                "median_bound_holds": gate,
            })
        cell_max_U[regime] = max_U

    # Per-regime collapse verification
    print()
    print("=" * 105)
    print("Per-regime collapse: c* = c*_M2 ?")
    print("=" * 105)
    print(f"{'regime':8s}  {'c*_M2':>8s}  {'c*_actual':>10s}  "
          f"{'collapse?':>10s}  {'min_gap_M2':>11s}  {'max_U_c':>8s}  "
          f"{'sufficient?':>12s}")

    regime_summaries = []
    for regime in REGIMES:
        m1d = m1_per[regime]
        m2d = m2_per[regime]
        if len(m2d) < 2:
            continue
        c_star_M2 = min(m2d, key=m2d.get)
        # Actual minimax: max over models, then argmin over corners
        max_per_corner = {c: max(m1d[c], m2d[c]) for c in m2d}
        c_star_actual = min(max_per_corner, key=max_per_corner.get)
        collapse_holds = (c_star_actual == c_star_M2)

        m2_star = m2d[c_star_M2]
        others = [v for c, v in m2d.items() if c != c_star_M2]
        min_gap = min(v - m2_star for v in others)
        max_U = cell_max_U[regime]
        sufficient = min_gap > max_U

        print(f"{regime:8s}  {c_star_M2:>8s}  {c_star_actual:>10s}  "
              f"{'YES' if collapse_holds else 'NO':>10s}  {min_gap:>11.2f}  {max_U:>8.2f}  "
              f"{'YES' if sufficient else 'NO':>12s}")

        regime_summaries.append({
            "regime": regime,
            "c_star_M2": c_star_M2,
            "c_star_actual": c_star_actual,
            "collapse_holds": collapse_holds,
            "min_inter_corner_gap_M2": min_gap,
            "max_U_c": max_U,
            "sufficient_condition_holds": sufficient,
        })

    # M3 stochastic extension: M2 vs M3_s20
    print()
    print("=" * 105)
    print("M3 stochastic extension (sigma=0.20) — M2 vs M3_s20")
    print("=" * 105)
    print(f"{'regime':8s} {'corner':8s}  {'eps_M3':>7s}  {'m_M3':>7s}  "
          f"{'U_c_M3':>7s}")

    m3_rows = []
    m3_per = {regime: {} for regime in REGIMES}
    cell_max_U_M3 = {}
    for regime in REGIMES:
        max_U_m3 = 0.0
        for corner in CORNERS:
            sub = df[(df["regime"] == regime) & (df["arm"] == corner)]
            if len(sub) == 0:
                continue
            T2 = sub["makespan_M2"].to_numpy()
            T3 = sub["makespan_M3_s20"].to_numpy()
            eps3 = float(np.mean(T3 < T2))
            m3 = float(np.median(T3))
            U3 = quantile_safe(T3, 0.5 + eps3) - quantile_safe(T3, 0.5)
            print(f"{regime:8s} {corner:8s}  {eps3:>7.4f}  {m3:>7.2f}  {U3:>7.2f}")
            m3_per[regime][corner] = m3
            max_U_m3 = max(max_U_m3, U3)
            m3_rows.append({
                "regime": regime,
                "corner": corner,
                "epsilon_M3_s20": eps3,
                "m_M3_s20": m3,
                "U_c_M3_s20": U3,
            })
        cell_max_U_M3[regime] = max_U_m3

    # Per-regime collapse for M2 vs M3 (knife-edge expected)
    print()
    print("M2-vs-M3 collapse: c*_{M3} = c*_{M2} ?  (knife-edge expected)")
    print(f"{'regime':8s}  {'c*_M2':>8s}  {'c*_M3':>8s}  {'collapse?':>10s}  "
          f"{'min_gap_M3':>11s}  {'max_U_M3':>9s}")

    m3_summaries = []
    for regime in REGIMES:
        m2d = m2_per[regime]
        m3d = m3_per[regime]
        if len(m3d) < 2:
            continue
        c_star_M2 = min(m2d, key=m2d.get)
        c_star_M3 = min(m3d, key=m3d.get)
        collapse_m3 = (c_star_M3 == c_star_M2)
        m3_star = m3d[c_star_M3]
        others = [v for c, v in m3d.items() if c != c_star_M3]
        min_gap_m3 = min(v - m3_star for v in others)
        max_U_m3 = cell_max_U_M3[regime]
        print(f"{regime:8s}  {c_star_M2:>8s}  {c_star_M3:>8s}  "
              f"{'YES' if collapse_m3 else 'no':>10s}  "
              f"{min_gap_m3:>11.2f}  {max_U_m3:>9.2f}")
        m3_summaries.append({
            "regime": regime,
            "c_star_M2": c_star_M2,
            "c_star_M3_s20": c_star_M3,
            "M3_collapse_holds": collapse_m3,
            "min_inter_corner_gap_M3": min_gap_m3,
            "max_U_c_M3": max_U_m3,
        })

    # Summary gates
    n_total = len(rows)
    n_gate = sum(1 for r in rows if r["median_bound_holds"])
    n_collapse = sum(1 for r in regime_summaries if r["collapse_holds"])
    n_sufficient = sum(1 for r in regime_summaries if r["sufficient_condition_holds"])
    n_regimes = len(regime_summaries)

    print()
    print("Corollary M5.2 verification gates:")
    print(f"  m_1^c - m_2^c <= U_c (per cell):       {n_gate}/{n_total}")
    print(f"  c* = c*_M2 (empirical, per regime):    {n_collapse}/{n_regimes}")
    print(f"  Sufficient condition (per regime):     {n_sufficient}/{n_regimes}")

    verdict = "PASS" if (n_gate == n_total and n_collapse == n_regimes) else "PARTIAL"
    print(f"  Overall verdict:                       {verdict}")

    out = {
        "generated": "2026-04-22",
        "purpose": "Numerical verification of Corollary M5.2 one-sided bound U_c(eps).",
        "M1_vs_M2": {
            "per_corner": rows,
            "per_regime_collapse": regime_summaries,
        },
        "M3_stochastic_sigma_0_20": {
            "per_corner": m3_rows,
            "per_regime_collapse": m3_summaries,
        },
        "summary": {
            "n_corner_cells": n_total,
            "n_median_bound_holds": n_gate,
            "n_regimes_collapse": n_collapse,
            "n_regimes_sufficient": n_sufficient,
            "n_regimes": n_regimes,
            "verdict": verdict,
        },
    }
    out_path = RESULTS_DIR / "v0_2_phase4_v2_m5_delta.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved {out_path}")


if __name__ == "__main__":
    main()
