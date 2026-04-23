"""
MVS v0.2 Phase 4 H1 with stagger — analysis (Gap 2 cross-check).

Loads results/raw/mvs_v0_2_phase4_H1_stagger_samples.csv and produces the
same cell-aggregate supported/not summary as analysis_phase4_H1.py,
comparing against the T=0 baseline to test survival of the
tactical-operational substitutability map.

Output: results/v0_2_phase4_H1_stagger_summary.json
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RAW_CSV = RESULTS_DIR / "raw" / "mvs_v0_2_phase4_H1_stagger_samples.csv"
BASELINE_JSON = RESULTS_DIR / "v0_2_phase4_H1_summary.json"
OUT_JSON = RESULTS_DIR / "v0_2_phase4_H1_stagger_summary.json"

REGIMES = ["E1_c2", "E2_c2", "E3_c2"]
MODELS = ["abstraction", "batched"]
SIZES = [4, 6, 8]
ARMS = ["random", "favorable"]
N_BOOT = 2000
RNG = np.random.default_rng(20260423)


def paired_bootstrap_ci(p0: np.ndarray, p1: np.ndarray,
                        n_boot: int = N_BOOT, alpha: float = 0.05):
    n = len(p0)
    assert len(p1) == n
    diffs = p1 - p0
    idx = RNG.integers(0, n, size=(n_boot, n))
    boot = diffs[idx].mean(axis=1)
    lo, hi = np.percentile(boot, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return float(diffs.mean()), float(lo), float(hi)


def main() -> None:
    df = pd.read_csv(RAW_CSV)

    print("=" * 120)
    print("Phase 4 H1 STAGGER analysis — P1 vs P0 under T-stagger CV = 0.5")
    print("=" * 120)

    rows = []
    for regime in REGIMES:
        for model in MODELS:
            for size in SIZES:
                for arm in ARMS:
                    sub = df[(df["regime"] == regime) & (df["model"] == model)
                             & (df["size"] == size) & (df["arm"] == arm)]
                    p0 = sub[sub["policy"] == "fifo"]["makespan"].to_numpy()
                    p1 = sub[sub["policy"] == "cluster"]["makespan"].to_numpy()
                    n = min(len(p0), len(p1))
                    if n == 0:
                        continue
                    p0, p1 = p0[:n], p1[:n]
                    delta, lo, hi = paired_bootstrap_ci(p0, p1)
                    rows.append({
                        "regime": regime, "model": model, "size": size, "arm": arm,
                        "mean_P0": float(p0.mean()), "mean_P1": float(p1.mean()),
                        "delta": delta, "ci_lo": lo, "ci_hi": hi,
                        "sig_P1_better": bool(hi < 0),
                        "sig_P1_worse": bool(lo > 0),
                    })

    # Cell aggregate on favorable arm
    print(f"{'cell':25s}  {'mean_delta':>10s}  {'n_sizes_sig':>11s}  {'supported':>10s}")
    cell_rows = []
    n_supported = 0
    for regime in REGIMES:
        for model in MODELS:
            cell = f"{regime}|{model}"
            sub = [r for r in rows
                   if r["regime"] == regime and r["model"] == model
                   and r["arm"] == "favorable"]
            if not sub:
                continue
            mean_delta = float(np.mean([r["delta"] for r in sub]))
            n_sig = sum(1 for r in sub if r["sig_P1_better"])
            supported = n_sig >= 2
            if supported:
                n_supported += 1
            verdict = "SUPPORTED" if supported else "not"
            print(f"{cell:25s}  {mean_delta:>+10.2f}  {n_sig:>3d}/3"
                  f"{'':>6s}  {verdict:>10s}")
            cell_rows.append({
                "cell": cell, "regime": regime, "model": model,
                "mean_delta_favorable": mean_delta,
                "n_sizes_sig": n_sig, "supported": supported,
            })

    # Compare to T=0 baseline
    print()
    print("=" * 120)
    print("Comparison to T=0 baseline")
    print("=" * 120)
    baseline_cells = {}
    if BASELINE_JSON.exists():
        baseline = json.loads(BASELINE_JSON.read_text(encoding="utf-8"))
        for c in baseline.get("per_cell_aggregate", []):
            baseline_cells[c["cell"]] = c

    print(f"{'cell':25s}  {'T=0 supported':>14s}  {'T=0.5 supported':>16s}  "
          f"{'status':>16s}")
    n_both = n_lost = n_gained = n_neither = 0
    for c in cell_rows:
        base = baseline_cells.get(c["cell"])
        base_sup = base["supported"] if base else None
        stag_sup = c["supported"]
        if base_sup and stag_sup:
            status = "BOTH"; n_both += 1
        elif base_sup and not stag_sup:
            status = "LOST UNDER T"; n_lost += 1
        elif not base_sup and stag_sup:
            status = "GAINED UNDER T"; n_gained += 1
        else:
            status = "neither"; n_neither += 1
        print(f"{c['cell']:25s}  {str(base_sup):>14s}  {str(stag_sup):>16s}  "
              f"{status:>16s}")

    print()
    print(f"BOTH (T=0 and T=0.5 both supported): {n_both}/6")
    print(f"LOST UNDER T (T=0 supported but T=0.5 not): {n_lost}/6")
    print(f"GAINED UNDER T: {n_gained}/6")
    print(f"neither: {n_neither}/6")

    if n_lost == 0 and n_both >= 2:
        verdict = ("SUBSTITUTABILITY MAP PRESERVED — the non-substitutable cells from "
                   "T=0 remain non-substitutable at T=0.5; tactical-operational "
                   "boundary is stable under realistic order-arrival stagger")
    elif n_lost <= 1:
        verdict = ("MOSTLY PRESERVED — 1 cell changes status; report cell-level "
                   "stagger sensitivity in §8")
    else:
        verdict = "SHIFTED — stagger materially changes substitutability map"
    print(f"Verdict: {verdict}")

    out = {
        "generated": "2026-04-22",
        "purpose": "Phase 4 H1 re-run with T-stagger CV=0.5 (Gap 2 cross-check)",
        "stagger_cv": 0.5, "n_boot": N_BOOT,
        "per_arm_size": rows,
        "per_cell_aggregate": cell_rows,
        "comparison_to_baseline": {
            "n_both": n_both, "n_lost": n_lost,
            "n_gained": n_gained, "n_neither": n_neither,
            "verdict": verdict,
        },
    }
    OUT_JSON.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nSaved {OUT_JSON}")


if __name__ == "__main__":
    main()
