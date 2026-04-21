"""
MVS v0.2 Phase 1 — regime-sweep analysis.

For each (E, capacity) regime, fit the model ladder:
  M1  = [size]
  M2  = [size, floor_distance]                 (decollinearised baseline)
  M2c = [size, cross_floor]                    (v0.1-style baseline, for comparison)
  M3  = [size, floor_distance, C, I]
  M3+ = M3 + 6 interaction terms (C*I, C^2, I^2, C*fd, I*fd, size*I)

Compute 5-fold CV R2 for each, plus the increments:
  delta_M3_minus_M2  (the headline number for H_v2.1)
  delta_M3plus_minus_M3
  delta_M3_minus_M2c (also report so we can compare to v0.1's framing)

Decision gate per plan:
  delta_M3_minus_M2 >= 0.05 in any regime -> H_v2.1 supported.

Outputs:
  prototype/results/v0_2_phase1_regime_sweep.json
  prototype/results/figures/phase1_heatmap.png
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold, cross_val_score

DATA = Path(__file__).resolve().parents[1] / "results" / "raw" / "mvs_v0_2_phase1_samples.csv"
OUT_DIR = Path(__file__).resolve().parents[1] / "results"
FIG_DIR = OUT_DIR / "figures"
RANDOM_STATE = 42
N_SPLITS = 5


def add_inter(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["C_x_I"] = df["C"] * df["I"]
    out["C_sq"] = df["C"] ** 2
    out["I_sq"] = df["I"] ** 2
    out["C_x_fd"] = df["C"] * df["floor_distance"]
    out["I_x_fd"] = df["I"] * df["floor_distance"]
    out["size_x_I"] = df["size"] * df["I"]
    return out


def cv_r2(X, y, cv) -> float:
    return cross_val_score(LinearRegression(), X, y, cv=cv, scoring="r2").mean()


def analyse_regime(df_regime: pd.DataFrame) -> dict:
    df = add_inter(df_regime)
    y = df["makespan"]
    cv = KFold(n_splits=N_SPLITS, shuffle=True, random_state=RANDOM_STATE)

    feats_M1 = ["size"]
    feats_M2 = ["size", "floor_distance"]
    feats_M2c = ["size", "cross_floor"]
    feats_M3 = ["size", "floor_distance", "C", "I"]
    feats_M3plus = feats_M3 + ["C_x_I", "C_sq", "I_sq", "C_x_fd", "I_x_fd", "size_x_I"]

    r2_M1 = cv_r2(df[feats_M1], y, cv)
    r2_M2 = cv_r2(df[feats_M2], y, cv)
    r2_M2c = cv_r2(df[feats_M2c], y, cv)
    r2_M3 = cv_r2(df[feats_M3], y, cv)
    r2_M3plus = cv_r2(df[feats_M3plus], y, cv)

    # Coefficients on full data for inspection
    lr_m3 = LinearRegression().fit(df[feats_M3], y)
    coefs_m3 = dict(zip(feats_M3, [float(c) for c in lr_m3.coef_]))

    return {
        "r2_M1": float(r2_M1),
        "r2_M2": float(r2_M2),
        "r2_M2_cross": float(r2_M2c),
        "r2_M3": float(r2_M3),
        "r2_M3plus": float(r2_M3plus),
        "delta_M3_minus_M2": float(r2_M3 - r2_M2),
        "delta_M3_minus_M2_cross": float(r2_M3 - r2_M2c),
        "delta_M3plus_minus_M3": float(r2_M3plus - r2_M3),
        "coefs_M3": coefs_m3,
        "n": int(len(df)),
        "makespan_mean": float(y.mean()),
        "makespan_std": float(y.std()),
    }


def heatmap(by_regime: dict, value_key: str, title: str, out_path: Path) -> None:
    Es = sorted({int(k.split("_")[0][1:]) for k in by_regime})
    caps = sorted({int(k.split("_")[1][1:]) for k in by_regime})
    grid = np.zeros((len(caps), len(Es)))
    for i, cap in enumerate(caps):
        for j, E in enumerate(Es):
            key = f"E{E}_c{cap}"
            grid[i, j] = by_regime[key][value_key]

    fig, ax = plt.subplots(figsize=(6, 4))
    im = ax.imshow(grid, cmap="viridis", aspect="auto", origin="lower")
    ax.set_xticks(range(len(Es)))
    ax.set_xticklabels([f"E={e}" for e in Es])
    ax.set_yticks(range(len(caps)))
    ax.set_yticklabels([f"capacity={c}" for c in caps])
    ax.set_title(title)
    for i in range(len(caps)):
        for j in range(len(Es)):
            v = grid[i, j]
            ax.text(j, i, f"{v:+.4f}", ha="center", va="center",
                    color="white" if v < grid.mean() else "black", fontsize=10)
    plt.colorbar(im, ax=ax, label=value_key)
    plt.tight_layout()
    plt.savefig(out_path, dpi=120)
    plt.close()


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA)
    print(f"Loaded {len(df)} rows across {df['regime'].nunique()} regimes.")

    by_regime = {}
    print()
    print("=" * 100)
    print(f"{'regime':>10s} {'r2_M1':>9s} {'r2_M2':>9s} {'r2_M3':>9s} "
          f"{'r2_M3+':>9s} {'M3-M2':>10s} {'M3-M2c':>10s} {'M3+-M3':>10s}")
    print("=" * 100)
    for regime in sorted(df["regime"].unique(),
                        key=lambda s: (int(s.split("_")[1][1:]),
                                       int(s.split("_")[0][1:]))):
        sub = df[df["regime"] == regime].copy()
        res = analyse_regime(sub)
        by_regime[regime] = res
        print(f"{regime:>10s} {res['r2_M1']:>9.4f} {res['r2_M2']:>9.4f} "
              f"{res['r2_M3']:>9.4f} {res['r2_M3plus']:>9.4f} "
              f"{res['delta_M3_minus_M2']:>+10.4f} "
              f"{res['delta_M3_minus_M2_cross']:>+10.4f} "
              f"{res['delta_M3plus_minus_M3']:>+10.4f}")
    print("=" * 100)

    print()
    print("M3 coefficients per regime (sign + magnitude):")
    print(f"{'regime':>10s} {'size':>10s} {'fdist':>10s} {'C':>10s} {'I':>10s}")
    for regime, res in sorted(by_regime.items(),
                              key=lambda kv: (int(kv[0].split('_')[1][1:]),
                                              int(kv[0].split('_')[0][1:]))):
        c = res["coefs_M3"]
        print(f"{regime:>10s} {c['size']:>+10.3f} {c['floor_distance']:>+10.3f} "
              f"{c['C']:>+10.3f} {c['I']:>+10.3f}")

    # Decision gate
    max_gap = max(r["delta_M3_minus_M2"] for r in by_regime.values())
    best_regime = max(by_regime.items(), key=lambda kv: kv[1]["delta_M3_minus_M2"])[0]
    print()
    if max_gap >= 0.05:
        verdict = "PASSED"
        verdict_text = (
            f"H_v2.1 SUPPORTED: best regime '{best_regime}' has "
            f"M3-M2 = {max_gap:+.4f} >= 0.05. "
            "Paper 3 has a regime-dependent C/I story."
        )
    elif max_gap >= 0.02:
        verdict = "AMBIGUOUS"
        verdict_text = (
            f"H_v2.1 AMBIGUOUS: best gap = {max_gap:+.4f} in [0.02, 0.05). "
            f"Best regime '{best_regime}'. Modest signal — needs Phase 2/3 "
            "to confirm or trigger Scenario A rescue."
        )
    else:
        verdict = "REJECTED"
        verdict_text = (
            f"H_v2.1 REJECTED: best gap = {max_gap:+.4f} < 0.02 across all 6 regimes. "
            "Triggers Counterfactual Scenario A rescue (Phi as conceptual "
            "decomposition only). See novelty_analysis_and_contribution.md §8."
        )
    print(f"DECISION GATE: {verdict}")
    print(verdict_text)

    # Heatmaps
    heatmap(by_regime, "delta_M3_minus_M2",
            "M3 - M2 R2 increment (baseline = size + floor_distance)",
            FIG_DIR / "phase1_heatmap_M3_minus_M2.png")
    heatmap(by_regime, "r2_M3", "M3 cross-validated R2",
            FIG_DIR / "phase1_heatmap_r2_M3.png")
    heatmap(by_regime, "delta_M3_minus_M2_cross",
            "M3 - M2_cross R2 increment (v0.1-style baseline)",
            FIG_DIR / "phase1_heatmap_M3_minus_M2cross.png")

    out_json = OUT_DIR / "v0_2_phase1_regime_sweep.json"
    with out_json.open("w") as f:
        json.dump({
            "by_regime": by_regime,
            "max_M3_minus_M2": max_gap,
            "best_regime_M3_minus_M2": best_regime,
            "verdict": verdict,
            "verdict_text": verdict_text,
            "n_splits": N_SPLITS,
            "random_state": RANDOM_STATE,
        }, f, indent=2)
    print(f"\nSaved JSON to {out_json}")
    print(f"Saved heatmaps to {FIG_DIR}")


if __name__ == "__main__":
    main()
