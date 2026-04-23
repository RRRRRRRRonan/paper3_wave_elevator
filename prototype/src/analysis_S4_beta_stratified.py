"""
MVS v0.2 Tier-1.5 S4 — β(C) per-corner stratified fit.

Tests whether within-corner β(C) is more bootstrap-stable than pooled β(C).
Motivation (outline §8 L5): pooled β(C) bootstrap sign-stability is 76-85%
within regime; reviewers ask whether this instability means Φ is unreliable.

Hypothesis: pooled instability is driven by inter-corner heterogeneity
(different corners have structurally different β(C) contributions). Fitting
β(C) *within each corner* should reduce residual variance and stabilise
the sign, because the corner-restricted pool is more homogeneous.

Design:
  - Use Phase 4 v2 samples (results/raw/mvs_v0_2_phase4_v2_samples.csv):
    18 000 simulations, 6 cells x 3 sizes x 5 arms x 200 waves with C, I
    features attached (via Phase 4 v2 candidate pool).
  - Actually the samples CSV only has makespan + cell metadata; refit by
    re-attaching C, I from the candidate pool.
  - For each cell (regime, model): fit pooled OLS (makespan ~ C + I + size)
    and per-corner OLS on the 4 non-random arms.
  - Bootstrap 1 000 resamples within each fit; report sign stability of
    β(C) and β(I) at the pooled level and per-corner level.

Output: results/v0_2_S4_beta_stratified.json
"""
from __future__ import annotations

import json
import random
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd

from src.experiments_v0_2 import N_AMRS, build_order_pool
from src.experiments_phase4_v2 import (
    POOL_SIZE_PER_BAND,
    build_candidate_waves,
    select_corner,
)
from src.features import compute_all_features
from src.simulator import Wave, simulate_wave

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RAW_DIR = RESULTS_DIR / "raw"
OUT_JSON = RESULTS_DIR / "v0_2_S4_beta_stratified.json"

REGIMES = [(1, 2), (2, 2), (3, 2)]
MODELS = ["abstraction", "batched"]
SIZE = 6
N_PER_ARM = 200
N_BOOT = 1000
CORNERS = ["HC_HI", "HC_LI", "LC_HI", "LC_LI"]
RNG = np.random.default_rng(20260423)


def fit_bootstrap(df: pd.DataFrame, features: List[str], n_boot: int = N_BOOT):
    X = df[features].to_numpy(dtype=float)
    y = df["makespan"].to_numpy(dtype=float)
    Xb = np.column_stack([np.ones(len(X)), X])
    coef, *_ = np.linalg.lstsq(Xb, y, rcond=None)
    pred = Xb @ coef
    ss_res = np.sum((y - pred) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")

    n = len(df)
    boot_coefs = np.zeros((n_boot, Xb.shape[1]))
    for i in range(n_boot):
        idx = RNG.integers(0, n, size=n)
        c, *_ = np.linalg.lstsq(Xb[idx], y[idx], rcond=None)
        boot_coefs[i] = c
    names = ["intercept"] + features
    result = {}
    for j, name in enumerate(names):
        sign_stab = float((np.sign(boot_coefs[:, j]) == np.sign(coef[j])).mean())
        lo, hi = np.percentile(boot_coefs[:, j], [2.5, 97.5])
        result[name] = {
            "estimate": float(coef[j]),
            "ci_lo": float(lo),
            "ci_hi": float(hi),
            "sign_stability": sign_stab,
        }
    return result, r2


def main() -> None:
    pool = build_order_pool(seed=43)
    cand = build_candidate_waves(SIZE, POOL_SIZE_PER_BAND, pool, seed=2026 + SIZE)
    corners_df = {
        "HC_HI": select_corner(cand, True, True),
        "HC_LI": select_corner(cand, True, False),
        "LC_HI": select_corner(cand, False, True),
        "LC_LI": select_corner(cand, False, False),
    }

    print("=" * 120)
    print("S4 — β(C) per-corner stratified fit vs pooled fit")
    print("=" * 120)
    print("Design: per-cell pooled regression (all corners) vs per-corner regression;")
    print("        expect within-corner fits to show higher β(C) sign stability.")

    rows = []
    cell_summary = []

    for E, cap in REGIMES:
        regime_str = f"E{E}_c{cap}"
        for model in MODELS:
            cell_label = f"{regime_str}|{model}"
            print(f"\nCell {cell_label}")
            batched = (model == "batched")

            # Simulate all 4 corners (200 waves each) + attach C, I features
            rng_sim = random.Random(hash((regime_str, model, "S4")) & 0x7fff)
            corner_frames = []
            for corner_label, df_corner in corners_df.items():
                idxs = rng_sim.choices(range(len(df_corner)), k=N_PER_ARM)
                for i in idxs:
                    row_cand = df_corner.iloc[i]
                    orders = [pool[j] for j in row_cand["idxs"]]
                    wave = Wave(orders=orders, release_time=0.0)
                    feats = compute_all_features(wave)
                    mk = simulate_wave(
                        wave, n_amrs=N_AMRS, n_elevators=E, capacity=cap,
                        batched=batched,
                    )
                    corner_frames.append({
                        "corner": corner_label, "size": SIZE,
                        "C": feats["C"], "I": feats["I"],
                        "T": feats["T"], "floor_distance": feats["floor_distance"],
                        "cross_floor": feats["cross_floor"],
                        "makespan": mk,
                    })
            df_cell = pd.DataFrame(corner_frames)

            # Pooled fit (all 800 waves, 4 corners combined)
            pooled, r2_pooled = fit_bootstrap(
                df_cell, features=["C", "I", "cross_floor"])
            beta_C_pooled = pooled["C"]
            beta_I_pooled = pooled["I"]
            print(f"  Pooled (N={len(df_cell)}, R^2={r2_pooled:.3f}):")
            print(f"    β(C) = {beta_C_pooled['estimate']:+.3f}  "
                  f"CI=[{beta_C_pooled['ci_lo']:+.3f}, {beta_C_pooled['ci_hi']:+.3f}]  "
                  f"sign_stab={beta_C_pooled['sign_stability']:.1%}")
            print(f"    β(I) = {beta_I_pooled['estimate']:+.3f}  "
                  f"CI=[{beta_I_pooled['ci_lo']:+.3f}, {beta_I_pooled['ci_hi']:+.3f}]  "
                  f"sign_stab={beta_I_pooled['sign_stability']:.1%}")

            # Per-corner fits (each N=200)
            per_corner = {}
            bCs = []
            bIs = []
            for corner in CORNERS:
                sub = df_cell[df_cell["corner"] == corner]
                if len(sub) < 20:
                    continue
                # Within corner, C and I have low variance (by construction).
                # Regress on C, I, cross_floor using residual C, I variance.
                res, r2 = fit_bootstrap(
                    sub, features=["C", "I", "cross_floor"])
                bC = res["C"]
                bI = res["I"]
                per_corner[corner] = {
                    "N": int(len(sub)), "R2": r2,
                    "beta_C": bC, "beta_I": bI,
                }
                bCs.append(bC["sign_stability"])
                bIs.append(bI["sign_stability"])
                print(f"  {corner} (N={len(sub)}, R^2={r2:.3f}): "
                      f"β(C)={bC['estimate']:+.3f} (stab={bC['sign_stability']:.0%})  "
                      f"β(I)={bI['estimate']:+.3f} (stab={bI['sign_stability']:.0%})")

            mean_bC_stab = float(np.mean(bCs)) if bCs else float("nan")
            mean_bI_stab = float(np.mean(bIs)) if bIs else float("nan")
            delta_bC = mean_bC_stab - beta_C_pooled["sign_stability"]
            delta_bI = mean_bI_stab - beta_I_pooled["sign_stability"]
            print(f"  Mean per-corner β(C) stab: {mean_bC_stab:.1%}  "
                  f"(Δ vs pooled {delta_bC:+.1%})")
            print(f"  Mean per-corner β(I) stab: {mean_bI_stab:.1%}  "
                  f"(Δ vs pooled {delta_bI:+.1%})")

            cell_summary.append({
                "cell": cell_label,
                "regime": regime_str, "model": model,
                "pooled_beta_C": beta_C_pooled, "pooled_beta_I": beta_I_pooled,
                "pooled_R2": r2_pooled,
                "per_corner": per_corner,
                "mean_per_corner_beta_C_sign_stability": mean_bC_stab,
                "mean_per_corner_beta_I_sign_stability": mean_bI_stab,
                "delta_beta_C_stability": delta_bC,
                "delta_beta_I_stability": delta_bI,
            })

    # Final summary
    print()
    print("=" * 120)
    print("Stratified fit summary — does per-corner β(C) stability exceed pooled?")
    print("=" * 120)
    print(f"{'cell':25s}  {'pooled_bC':>10s}  {'per_corner_bC':>13s}  "
          f"{'Δ':>6s}  {'pooled_bI':>10s}  {'per_corner_bI':>13s}  {'Δ':>6s}")
    n_improved_C = 0
    n_improved_I = 0
    for c in cell_summary:
        pC = c["pooled_beta_C"]["sign_stability"]
        ppC = c["mean_per_corner_beta_C_sign_stability"]
        pI = c["pooled_beta_I"]["sign_stability"]
        ppI = c["mean_per_corner_beta_I_sign_stability"]
        dC = ppC - pC
        dI = ppI - pI
        if dC > 0:
            n_improved_C += 1
        if dI > 0:
            n_improved_I += 1
        print(f"{c['cell']:25s}  {pC:>9.1%}  {ppC:>12.1%}  {dC:>+5.1%}  "
              f"{pI:>9.1%}  {ppI:>12.1%}  {dI:>+5.1%}")

    print()
    print(f"β(C) stability improved by stratification: {n_improved_C}/6 cells")
    print(f"β(I) stability improved by stratification: {n_improved_I}/6 cells")

    if n_improved_C >= 4:
        verdict_C = ("β(C) STABILISES UNDER STRATIFICATION — pooled instability was "
                     "driven by inter-corner heterogeneity; within-corner sign is more "
                     "coherent, supporting Φ as a structured decomposition")
    elif n_improved_C >= 3:
        verdict_C = ("β(C) PARTIALLY STABILISED — majority of cells improve under "
                     "stratification, but not all")
    else:
        verdict_C = ("β(C) POOLED AND STRATIFIED ARE COMPARABLE — stratification does "
                     "not rescue the 76-85% pooled stability claim")
    print(f"Verdict (β(C)): {verdict_C}")

    out = {
        "generated": "2026-04-22",
        "purpose": "S4: β(C) per-corner stratified fit vs pooled",
        "n_per_arm": N_PER_ARM, "n_boot": N_BOOT, "size": SIZE,
        "per_cell": cell_summary,
        "summary": {
            "n_cells_beta_C_improved": n_improved_C,
            "n_cells_beta_I_improved": n_improved_I,
            "verdict_beta_C": verdict_C,
        },
    }
    OUT_JSON.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nSaved {OUT_JSON}")


if __name__ == "__main__":
    main()
