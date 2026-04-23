"""
MVS v0.2 Phase 4 H1 — Analysis: P1 (cluster) vs P0 (fifo) mean-makespan.

Loads results/raw/mvs_v0_2_phase4_H1_samples.csv and produces:
  1) Per-cell x size mean makespan under P0, P1, delta, and paired-bootstrap 95% CI
  2) Per-cell aggregate (size-mean) summary
  3) Pre-reg H1 gate outcome:
       H1 supported if P1 mean < P0 mean (CI upper < 0) in >= 4/6 cells on
       the favorable arm.

Output: results/v0_2_phase4_H1_summary.json
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RAW_CSV = RESULTS_DIR / "raw" / "mvs_v0_2_phase4_H1_samples.csv"
OUT_JSON = RESULTS_DIR / "v0_2_phase4_H1_summary.json"

REGIMES = ["E1_c2", "E2_c2", "E3_c2"]
MODELS = ["abstraction", "batched"]
SIZES = [4, 6, 8]
ARMS = ["random", "favorable"]
N_BOOT = 2000
RNG = np.random.default_rng(20260422)


def paired_bootstrap_ci(p0: np.ndarray, p1: np.ndarray,
                        n_boot: int = N_BOOT, alpha: float = 0.05):
    """Paired bootstrap for (mean(P1) - mean(P0))."""
    n = len(p0)
    assert len(p1) == n
    diffs = p1 - p0
    idx = RNG.integers(0, n, size=(n_boot, n))
    boot = diffs[idx].mean(axis=1)
    lo, hi = np.percentile(boot, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return float(diffs.mean()), float(lo), float(hi)


def main() -> None:
    df = pd.read_csv(RAW_CSV)
    print("=" * 110)
    print("Phase 4 H1 analysis — P1 (cluster) vs P0 (fifo)")
    print("=" * 110)
    print(f"{'regime':8s} {'model':12s} {'sz':>3s} {'arm':11s}  "
          f"{'mean_P0':>8s} {'mean_P1':>8s} {'delta':>8s} {'rel%':>7s}  "
          f"{'CI_lo':>8s} {'CI_hi':>8s}  {'sig':>5s}")

    rows = []
    for regime in REGIMES:
        for model in MODELS:
            for size in SIZES:
                for arm in ARMS:
                    sub = df[(df["regime"] == regime) & (df["model"] == model)
                            & (df["size"] == size) & (df["arm"] == arm)]
                    # Align paired samples by row order (seeds differ by policy,
                    # so do independent-sample comparison — still paired by
                    # wave index within each (seed, policy) stream).
                    p0 = sub[sub["policy"] == "fifo"]["makespan"].to_numpy()
                    p1 = sub[sub["policy"] == "cluster"]["makespan"].to_numpy()
                    n = min(len(p0), len(p1))
                    if n == 0:
                        continue
                    p0, p1 = p0[:n], p1[:n]
                    delta, lo, hi = paired_bootstrap_ci(p0, p1)
                    m0 = float(p0.mean())
                    m1 = float(p1.mean())
                    rel = delta / m0 if m0 > 0 else float("nan")
                    sig = "YES" if hi < 0 else ("neg+" if lo > 0 else "ns")
                    print(f"{regime:8s} {model:12s} {size:>3d} {arm:11s}  "
                          f"{m0:>8.2f} {m1:>8.2f} {delta:>+8.2f} {rel:>+7.2%}  "
                          f"{lo:>+8.2f} {hi:>+8.2f}  {sig:>5s}")
                    rows.append({
                        "regime": regime, "model": model, "size": size, "arm": arm,
                        "mean_P0": m0, "mean_P1": m1, "delta": delta,
                        "rel": rel, "ci_lo": lo, "ci_hi": hi,
                        "sig_P1_better": bool(hi < 0),
                        "sig_P1_worse": bool(lo > 0),
                    })

    # Aggregate to cell level (favorable arm, size-averaged)
    print()
    print("=" * 110)
    print("Cell-level aggregate — favorable arm, size-averaged (primary H1 test)")
    print("=" * 110)
    print(f"{'cell':25s}  {'mean_delta':>10s}  {'n_sizes_sig':>11s}  "
          f"{'verdict':>12s}")

    cell_rows = []
    n_cells_supported = 0
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
            # cell-level support: at least 2/3 sizes show sig P1<P0
            supported = n_sig >= 2
            if supported:
                n_cells_supported += 1
            verdict = "SUPPORTED" if supported else "not"
            print(f"{cell:25s}  {mean_delta:>+10.2f}  {n_sig:>3d}/3"
                  f"{'':>6s}  {verdict:>12s}")
            cell_rows.append({
                "cell": cell, "regime": regime, "model": model,
                "mean_delta_favorable": mean_delta,
                "n_sizes_sig": n_sig,
                "supported": supported,
            })

    print()
    print("Pre-reg gate (H1):")
    n_cells = len(cell_rows)
    print(f"  Cells supporting P1 < P0 (>=2/3 sizes sig, favorable arm): "
          f"{n_cells_supported}/{n_cells}")
    if n_cells_supported >= 4:
        verdict = "H1 SUPPORTED — P1 beats P0 in majority of cells"
    elif n_cells_supported >= 2:
        verdict = ("H1 PARTIAL — P1 benefit concentrated in specific cells, "
                   "interpret as regime-conditional finding")
    else:
        verdict = "H1 NOT SUPPORTED — P1 fails in most cells"
    print(f"  Verdict: {verdict}")

    out = {
        "generated": "2026-04-22",
        "n_samples_total": int(len(df)),
        "n_boot": N_BOOT,
        "per_arm_size": rows,
        "per_cell_aggregate": cell_rows,
        "summary": {
            "n_cells": n_cells,
            "n_cells_supported": n_cells_supported,
            "verdict": verdict,
        },
    }
    OUT_JSON.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nSaved {OUT_JSON}")


if __name__ == "__main__":
    main()
