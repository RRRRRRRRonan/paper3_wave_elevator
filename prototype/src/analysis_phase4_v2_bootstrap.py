"""
MVS v0.2 Phase 4 v2 Reinforcement Experiment R1 — Bootstrap CIs on GAP & beta(C).

Defuses reviewer objection: "5.83% mean GAP is within simulation noise."

Inputs:
  - results/raw/mvs_v0_2_phase4_v2_samples.csv    (Phase 4 v2 wave-design samples)
  - results/raw/mvs_v0_2_phase1_5_batched_samples.csv (Phase 1.5 batched-fit samples)

Outputs:
  - results/v0_2_phase4_v2_gap_bootstrap.json
  - results/figures/phase4_v2_gap_ci.png

Method:
  GAP CI per cell:
    For each (regime, model, size):
      For B=1000 bootstrap iterations:
        - Resample (with replacement) the 200 makespans within each arm
        - Compute UB, LB, GAP
      Report median, 2.5%, 97.5%, fraction-positive
    Average over sizes (within-cell mean of bootstrap estimates) for cell GAP_mean CI.

  beta(C) sign-stability CI:
    For each c=2 regime, batched fit:
      For B=1000 iterations:
        - Resample (size, makespan, C, I, T, ...) rows with replacement (pair-bootstrap)
        - Refit OLS makespan ~ size + C + I + T + cross_floor + floor_distance
        - Record sign(beta_C)
      Report fraction with beta_C < 0, fraction with beta_C > 0.

Pass gates (per intuitions §11.10 R1):
  - GAP CI excludes 0 in >= 4/6 cells
  - For each c=2 batched fit, sign of beta_C is stable in >= 90% of bootstrap replicates
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

CSV_P4 = RAW_DIR / "mvs_v0_2_phase4_v2_samples.csv"
CSV_P15 = RAW_DIR / "mvs_v0_2_phase1_5_batched_samples.csv"

REGIMES = ["E1_c2", "E2_c2", "E3_c2"]
MODELS = ["abstraction", "batched"]
SIZES = [4, 6, 8]
CORNERS = ["HC_HI", "HC_LI", "LC_HI", "LC_LI"]

N_BOOT = 1000
RNG_SEED = 20260422


def gap_one_iter(rng, sub_random, sub_corners, fav_label):
    """Compute one bootstrap (UB, LB, GAP) for a single (regime, model, size)."""
    rand_resampled = rng.choice(sub_random, size=len(sub_random), replace=True)
    rand_med = float(np.median(rand_resampled))
    if rand_med <= 0:
        return 0.0, 0.0, 0.0

    corner_meds = {}
    for c, arr in sub_corners.items():
        boot = rng.choice(arr, size=len(arr), replace=True)
        corner_meds[c] = float(np.median(boot))

    ub = (max(corner_meds.values()) - min(corner_meds.values())) / rand_med
    lb = (rand_med - corner_meds[fav_label]) / rand_med
    gap = ub - lb
    return ub, lb, gap


def bootstrap_gap(df: pd.DataFrame) -> dict:
    """Per (regime, model) cell, bootstrap GAP averaging within sizes."""
    rng = np.random.default_rng(RNG_SEED)
    out = {}

    for regime in REGIMES:
        for model in MODELS:
            cell_label = f"{regime}|{model}"
            cell = df[(df["regime"] == regime) & (df["model"] == model)]
            if len(cell) == 0:
                continue
            fav = cell["favorable_corner"].iloc[0]

            cell_gap_means = np.empty(N_BOOT)
            cell_ub_means = np.empty(N_BOOT)
            cell_lb_means = np.empty(N_BOOT)

            # Pre-extract arrays to avoid repeated DataFrame indexing
            data_per_size = {}
            for size in SIZES:
                sub = cell[cell["size"] == size]
                data_per_size[size] = {
                    "random": sub[sub["arm"] == "random"]["makespan"].to_numpy(),
                    "corners": {
                        c: sub[sub["arm"] == c]["makespan"].to_numpy()
                        for c in CORNERS
                    },
                }

            for b in range(N_BOOT):
                gap_per_size = []
                ub_per_size = []
                lb_per_size = []
                for size in SIZES:
                    ub, lb, gap = gap_one_iter(
                        rng,
                        data_per_size[size]["random"],
                        data_per_size[size]["corners"],
                        fav,
                    )
                    ub_per_size.append(ub)
                    lb_per_size.append(lb)
                    gap_per_size.append(gap)
                cell_gap_means[b] = np.mean(gap_per_size)
                cell_ub_means[b] = np.mean(ub_per_size)
                cell_lb_means[b] = np.mean(lb_per_size)

            ci_lo, ci_hi = np.quantile(cell_gap_means, [0.025, 0.975])
            ub_lo, ub_hi = np.quantile(cell_ub_means, [0.025, 0.975])
            lb_lo, lb_hi = np.quantile(cell_lb_means, [0.025, 0.975])
            frac_pos = float(np.mean(cell_gap_means > 0))

            out[cell_label] = {
                "favorable_corner": fav,
                "GAP_median": float(np.median(cell_gap_means)),
                "GAP_mean": float(np.mean(cell_gap_means)),
                "GAP_CI95": [float(ci_lo), float(ci_hi)],
                "GAP_excludes_zero": bool(ci_lo > 0),
                "GAP_frac_positive": frac_pos,
                "UB_median": float(np.median(cell_ub_means)),
                "UB_CI95": [float(ub_lo), float(ub_hi)],
                "LB_median": float(np.median(cell_lb_means)),
                "LB_CI95": [float(lb_lo), float(lb_hi)],
            }
    return out


def bootstrap_beta_signs(df_p15: pd.DataFrame) -> dict:
    """Pair-bootstrap OLS refit for c=2 batched fits; track sign(beta_C)."""
    from numpy.linalg import lstsq

    rng = np.random.default_rng(RNG_SEED + 1)
    out = {}

    feature_cols = ["size", "C", "I", "T", "cross_floor", "floor_distance"]
    target_col = "makespan"

    # Phase 1.5 CSV has columns: regime, wave_idx, makespan, C, I, T, size, ...
    for regime in REGIMES:
        # Phase 1.5 CSV uses suffix "_batched" on regime label
        sub = df_p15[df_p15["regime"] == f"{regime}_batched"]
        if len(sub) == 0:
            sub = df_p15[df_p15["regime"] == regime]
        if len(sub) == 0:
            print(f"  WARN: no Phase 1.5 rows for {regime}")
            continue

        # Confirm available columns; handle missing T/cross_floor/floor_distance gracefully
        available = [c for c in feature_cols if c in sub.columns]
        X_all = sub[available].to_numpy(dtype=float)
        y_all = sub[target_col].to_numpy(dtype=float)
        # Add intercept column
        X_all = np.column_stack([np.ones(len(X_all)), X_all])
        c_idx = available.index("C") + 1  # +1 for intercept

        signs = np.empty(N_BOOT, dtype=int)
        beta_c_vals = np.empty(N_BOOT)
        n = len(X_all)
        for b in range(N_BOOT):
            idx = rng.integers(0, n, size=n)
            Xb = X_all[idx]
            yb = y_all[idx]
            coefs, *_ = lstsq(Xb, yb, rcond=None)
            beta_c = coefs[c_idx]
            beta_c_vals[b] = beta_c
            signs[b] = int(np.sign(beta_c))

        frac_neg = float(np.mean(signs < 0))
        frac_pos = float(np.mean(signs > 0))
        ci_lo, ci_hi = np.quantile(beta_c_vals, [0.025, 0.975])
        out[regime] = {
            "n_obs": int(n),
            "available_features": available,
            "beta_C_median": float(np.median(beta_c_vals)),
            "beta_C_CI95": [float(ci_lo), float(ci_hi)],
            "frac_neg_sign": frac_neg,
            "frac_pos_sign": frac_pos,
            "sign_stable": bool(max(frac_neg, frac_pos) >= 0.90),
            "dominant_sign": ("neg" if frac_neg > frac_pos else "pos"),
        }
    return out


def main() -> None:
    df_p4 = pd.read_csv(CSV_P4)
    df_p15 = pd.read_csv(CSV_P15)

    print("=" * 88)
    print("R1 — Bootstrap CIs on GAP and beta(C)")
    print("=" * 88)
    print(f"  N_BOOT = {N_BOOT}")
    print(f"  Phase 4 v2 rows: {len(df_p4)}; Phase 1.5 rows: {len(df_p15)}")
    print()

    print("Bootstrapping GAP per cell...")
    gap_results = bootstrap_gap(df_p4)

    print()
    print(f"{'cell':24s}  {'fav':6s}  {'GAP%':>8s}  {'CI95%':>20s}  "
          f"{'excl 0?':>8s}  {'P>0':>6s}")
    n_excl_zero = 0
    for cell, r in gap_results.items():
        excl = "YES" if r["GAP_excludes_zero"] else "no"
        if r["GAP_excludes_zero"]:
            n_excl_zero += 1
        print(f"{cell:24s}  {r['favorable_corner']:6s}  "
              f"{r['GAP_median']*100:>7.2f}%  "
              f"[{r['GAP_CI95'][0]*100:>5.2f}%, {r['GAP_CI95'][1]*100:>5.2f}%]  "
              f"{excl:>8s}  {r['GAP_frac_positive']:>6.2f}")
    print()
    n_cells = len(gap_results)
    print(f"  Cells with CI excluding 0: {n_excl_zero}/{n_cells}")

    if n_cells > 0:
        gap_gate = (n_excl_zero >= 4)
        gap_verdict = "PASS" if gap_gate else "FAIL"
    else:
        gap_verdict = "NO DATA"
    print(f"  R1-GAP gate (>= 4/{n_cells}): {gap_verdict}")

    print()
    print("Bootstrapping beta(C) sign stability for c=2 batched fits...")
    sign_results = bootstrap_beta_signs(df_p15)

    print()
    print(f"{'regime':8s}  {'beta_C med':>11s}  {'CI95':>22s}  "
          f"{'frac_neg':>9s}  {'frac_pos':>9s}  {'stable?':>8s}")
    n_stable = 0
    for regime, r in sign_results.items():
        s = "YES" if r["sign_stable"] else "no"
        if r["sign_stable"]:
            n_stable += 1
        print(f"{regime:8s}  {r['beta_C_median']:>+11.3f}  "
              f"[{r['beta_C_CI95'][0]:>+8.2f},{r['beta_C_CI95'][1]:>+8.2f}]  "
              f"{r['frac_neg_sign']:>9.2f}  {r['frac_pos_sign']:>9.2f}  "
              f"{s:>8s}")

    n_regimes = len(sign_results)
    print()
    print(f"  Regimes with stable sign (>=90%): {n_stable}/{n_regimes}")
    sign_gate = (n_stable >= n_regimes)  # all c=2 regimes should be stable
    sign_verdict = "PASS" if sign_gate else "FAIL"
    print(f"  R1-Sign gate (all {n_regimes} stable): {sign_verdict}")

    overall = "PASS" if (gap_verdict == "PASS" and sign_verdict == "PASS") else (
        "PASS-with-caveats" if (gap_verdict == "PASS" or sign_verdict == "PASS")
        else "FAIL")
    print()
    print(f"  R1 overall: {overall}")

    # ----- Figure: GAP CI bar chart -----
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 4.5))
    cells = list(gap_results.keys())
    medians = [gap_results[c]["GAP_median"] * 100 for c in cells]
    los = [gap_results[c]["GAP_CI95"][0] * 100 for c in cells]
    his = [gap_results[c]["GAP_CI95"][1] * 100 for c in cells]
    err_lo = [m - lo for m, lo in zip(medians, los)]
    err_hi = [hi - m for hi, m in zip(his, medians)]
    colors = ["#2a7" if gap_results[c]["GAP_excludes_zero"] else "#c83"
              for c in cells]
    ax.bar(range(len(cells)), medians, yerr=[err_lo, err_hi], color=colors,
           capsize=5, error_kw={"lw": 1.2})
    ax.axhline(0, color="k", lw=0.7)
    ax.set_xticks(range(len(cells)))
    ax.set_xticklabels([c.replace("|", "\n") for c in cells], fontsize=8)
    ax.set_ylabel("Bootstrap GAP (% of random median)")
    ax.set_title(f"R1: GAP bootstrap CI per cell (B={N_BOOT}). Green = CI excludes 0.")
    fig.tight_layout()
    fig_path = FIG_DIR / "phase4_v2_gap_ci.png"
    fig.savefig(fig_path, dpi=110)
    plt.close(fig)
    print(f"\n  Saved {fig_path}")

    # ----- Save JSON -----
    out = {
        "generated": "2026-04-22",
        "n_bootstrap": N_BOOT,
        "rng_seed": RNG_SEED,
        "GAP_per_cell": gap_results,
        "beta_C_signs_per_regime": sign_results,
        "summary": {
            "n_cells_GAP_CI_excludes_zero": n_excl_zero,
            "n_cells_total": n_cells,
            "GAP_verdict": gap_verdict,
            "n_regimes_sign_stable": n_stable,
            "n_regimes_total": n_regimes,
            "sign_verdict": sign_verdict,
            "overall_R1_verdict": overall,
        },
    }
    out_path = RESULTS_DIR / "v0_2_phase4_v2_gap_bootstrap.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"  Saved {out_path}")


if __name__ == "__main__":
    main()
