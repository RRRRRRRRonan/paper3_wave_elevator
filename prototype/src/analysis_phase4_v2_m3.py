"""
MVS v0.2 Phase 4 v2 Reinforcement Experiment R3 — M3 sensitivity analysis.

Reads results/raw/mvs_v0_2_phase4_v2_m3_samples.csv (3000 rows; 5 arms x
200 waves x 3 regimes, each with M1/M2/M3a/M3b makespans on the SAME wave).

Two questions:
  Q1: Does M2 dominate worst-case? Specifically, is M3 between M1 and M2?
      Per (regime, arm, wave): check ordering med_M2 >= med_M3 >= med_M1.
      Pass: in >= 80% of (regime, arm) cells, M3 sits inside [M1, M2] span.

  Q2: Does M5 collapse-to-batched rule survive M2 -> M3 substitution?
      For each regime: compute robust corner under {M1, M2} (= Phase 4 v2)
      and under {M1, M3a}, {M1, M3b}.
      Pass: robust corner identical across model substitutions in
            sign-divergent regimes (E2_c2, E3_c2).

Output: results/v0_2_phase4_v2_m3_sensitivity.json + figure.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RAW_DIR = RESULTS_DIR / "raw"
FIG_DIR = RESULTS_DIR / "figures"

CSV = RAW_DIR / "mvs_v0_2_phase4_v2_m3_samples.csv"
REGIMES = ["E1_c2", "E2_c2", "E3_c2"]
ARMS = ["random", "HC_HI", "HC_LI", "LC_HI", "LC_LI"]
CORNERS = ["HC_HI", "HC_LI", "LC_HI", "LC_LI"]


def main() -> None:
    df = pd.read_csv(CSV)
    print(f"Loaded {len(df)} rows")

    # Q1: per-wave ordering
    print()
    print("=" * 88)
    print("Q1: Per-wave ordering — is M3 inside the [M1, M2] span?")
    print("=" * 88)

    print()
    print(f"{'regime':8s} {'arm':6s}  "
          f"{'M2>=M1 %':>10s}  "
          f"{'M3a in [M1,M2] %':>17s}  "
          f"{'M3b in [M1,M2] %':>17s}  "
          f"{'med_M1':>7s}  {'med_M2':>7s}  {'med_M3a':>8s}  {'med_M3b':>8s}")

    q1_rows = []
    for regime in REGIMES:
        for arm in ARMS:
            sub = df[(df["regime"] == regime) & (df["arm"] == arm)]
            m1 = sub["makespan_M1"].to_numpy()
            m2 = sub["makespan_M2"].to_numpy()
            m3a = sub["makespan_M3_s10"].to_numpy()
            m3b = sub["makespan_M3_s20"].to_numpy()

            frac_m2_ge_m1 = float(np.mean(m2 >= m1))
            # Note: M3 is stochastic so per-wave ordering is noisy; use [min(M1,M2), max(M1,M2)]
            lo = np.minimum(m1, m2); hi = np.maximum(m1, m2)
            frac_m3a_in = float(np.mean((m3a >= lo) & (m3a <= hi)))
            frac_m3b_in = float(np.mean((m3b >= lo) & (m3b <= hi)))

            print(f"{regime:8s} {arm:6s}  "
                  f"{frac_m2_ge_m1:>9.2%}  {frac_m3a_in:>16.2%}  "
                  f"{frac_m3b_in:>16.2%}  "
                  f"{np.median(m1):>7.1f}  {np.median(m2):>7.1f}  "
                  f"{np.median(m3a):>8.1f}  {np.median(m3b):>8.1f}")

            q1_rows.append({
                "regime": regime, "arm": arm,
                "frac_m2_ge_m1": frac_m2_ge_m1,
                "frac_m3a_in_span": frac_m3a_in,
                "frac_m3b_in_span": frac_m3b_in,
                "med_M1": float(np.median(m1)),
                "med_M2": float(np.median(m2)),
                "med_M3a": float(np.median(m3a)),
                "med_M3b": float(np.median(m3b)),
            })

    # Q1 gates
    n_cells = len(q1_rows)
    n_dominate = sum(1 for r in q1_rows if r["frac_m2_ge_m1"] >= 0.80)
    n_m3a_in = sum(1 for r in q1_rows if r["frac_m3a_in_span"] >= 0.80)
    n_m3b_in = sum(1 for r in q1_rows if r["frac_m3b_in_span"] >= 0.80)

    print()
    print(f"  M2>=M1 in >=80% of waves: {n_dominate}/{n_cells} cells")
    print(f"  M3a in span in >=80% of waves: {n_m3a_in}/{n_cells}")
    print(f"  M3b in span in >=80% of waves: {n_m3b_in}/{n_cells}")

    q1_pass = (n_dominate >= int(0.8 * n_cells)
               and n_m3a_in >= int(0.8 * n_cells))
    q1_verdict = "PASS" if q1_pass else "FAIL"
    print(f"  Q1 verdict: {q1_verdict}")

    # Q2: M5 robust corner stability
    print()
    print("=" * 88)
    print("Q2: M5 robust corner under model substitutions")
    print("=" * 88)

    def robust_corner(med_a: dict, med_b: dict) -> str:
        """Min over corners of max(med_a, med_b)."""
        wc = {c: max(med_a[c], med_b[c]) for c in CORNERS}
        return min(wc, key=wc.get)

    print()
    print(f"{'regime':8s}  {'robust_{M1,M2}':>16s}  "
          f"{'robust_{M1,M3a}':>16s}  {'robust_{M1,M3b}':>16s}  "
          f"{'stable?':>9s}")

    q2_rows = []
    for regime in REGIMES:
        med_M1 = {c: float(np.median(df[(df["regime"] == regime) & (df["arm"] == c)]["makespan_M1"])) for c in CORNERS}
        med_M2 = {c: float(np.median(df[(df["regime"] == regime) & (df["arm"] == c)]["makespan_M2"])) for c in CORNERS}
        med_M3a = {c: float(np.median(df[(df["regime"] == regime) & (df["arm"] == c)]["makespan_M3_s10"])) for c in CORNERS}
        med_M3b = {c: float(np.median(df[(df["regime"] == regime) & (df["arm"] == c)]["makespan_M3_s20"])) for c in CORNERS}

        rc12 = robust_corner(med_M1, med_M2)
        rc1a = robust_corner(med_M1, med_M3a)
        rc1b = robust_corner(med_M1, med_M3b)
        stable = (rc12 == rc1a == rc1b)

        print(f"{regime:8s}  {rc12:>16s}  {rc1a:>16s}  {rc1b:>16s}  "
              f"{'YES' if stable else 'no':>9s}")

        q2_rows.append({
            "regime": regime,
            "robust_M1_M2": rc12,
            "robust_M1_M3a": rc1a,
            "robust_M1_M3b": rc1b,
            "stable": stable,
            "is_sign_divergent": regime in ("E2_c2", "E3_c2"),
        })

    n_stable = sum(1 for r in q2_rows if r["stable"])
    n_div_stable = sum(1 for r in q2_rows if r["stable"] and r["is_sign_divergent"])
    n_div = sum(1 for r in q2_rows if r["is_sign_divergent"])

    print()
    print(f"  Robust corner stable across all 3 model pairs: {n_stable}/3 regimes")
    print(f"  In sign-divergent regimes (E2, E3): {n_div_stable}/{n_div}")

    q2_pass = (n_div_stable == n_div)
    q2_verdict = "PASS" if q2_pass else "FAIL"
    print(f"  Q2 verdict: {q2_verdict}")

    # Overall
    overall = "PASS" if (q1_pass and q2_pass) else (
        "PASS-with-caveats" if (q1_pass or q2_pass) else "FAIL")
    print()
    print(f"  R3 overall: {overall}")

    # Figure: median makespan per (regime, arm) under each model
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.5), sharey=False)
    for k, regime in enumerate(REGIMES):
        ax = axes[k]
        rows = [r for r in q1_rows if r["regime"] == regime]
        x = np.arange(len(rows))
        w = 0.2
        ax.bar(x - 1.5*w, [r["med_M1"] for r in rows], w, label="M1", color="#3a8")
        ax.bar(x - 0.5*w, [r["med_M2"] for r in rows], w, label="M2", color="#83a")
        ax.bar(x + 0.5*w, [r["med_M3a"] for r in rows], w, label="M3 σ=0.1", color="#a83")
        ax.bar(x + 1.5*w, [r["med_M3b"] for r in rows], w, label="M3 σ=0.2", color="#a38")
        ax.set_xticks(x)
        ax.set_xticklabels([r["arm"] for r in rows], fontsize=8, rotation=30, ha="right")
        ax.set_title(f"{regime} (size={6})", fontsize=10)
        if k == 0:
            ax.set_ylabel("Median makespan (s)")
            ax.legend(fontsize=8)
    fig.suptitle(f"R3: median makespan per (regime, arm) under M1/M2/M3 ({overall})", fontsize=11)
    fig.tight_layout()
    fig_path = FIG_DIR / "phase4_v2_m3_medians.png"
    fig.savefig(fig_path, dpi=110, bbox_inches="tight")
    plt.close(fig)
    print(f"\n  Saved {fig_path}")

    out = {
        "generated": "2026-04-22",
        "purpose": "R3 M3 stochastic-batching sensitivity for M5 dominance-collapse rule.",
        "Q1_per_cell_ordering": q1_rows,
        "Q2_robust_corner_per_regime": q2_rows,
        "summary": {
            "n_cells": n_cells,
            "n_M2_dominates": n_dominate,
            "n_M3a_in_span": n_m3a_in,
            "n_M3b_in_span": n_m3b_in,
            "Q1_verdict": q1_verdict,
            "n_regimes_robust_stable": n_stable,
            "n_sign_divergent_stable": n_div_stable,
            "Q2_verdict": q2_verdict,
            "overall_R3_verdict": overall,
        },
    }
    out_path = RESULTS_DIR / "v0_2_phase4_v2_m3_sensitivity.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"  Saved {out_path}")


if __name__ == "__main__":
    main()
