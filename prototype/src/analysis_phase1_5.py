"""
MVS v0.2 Phase 1.5 analysis.

Compares true-batching (ElevatorPoolBatched) to Phase 1 throughput-abstraction
on the three c>=2 regimes. Reports:

 1. Mean/median makespan delta (batched - abstraction) per regime
 2. Pearson corr of makespans across the matched waves
 3. Model ladder R^2 (M1/M2/M3) on batched data + M3 - M2 increment
 4. Physical-unit betas and 95% bootstrap CIs for M3 fits on batched data
 5. Decision gate: best M3-M2 >= +0.05 -> predictive-surrogate rescued

Output: results/v0_2_phase1_5_true_batching.json and figures/.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold, cross_val_score

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RAW_DIR = RESULTS_DIR / "raw"
FIG_DIR = RESULTS_DIR / "figures"

PHASE1_CSV = RAW_DIR / "mvs_v0_2_phase1_samples.csv"
BATCHED_CSV = RAW_DIR / "mvs_v0_2_phase1_5_batched_samples.csv"

M1_FEATS = ["size"]
M2_FEATS = ["size", "cross_floor", "floor_distance"]
M3_FEATS = ["size", "cross_floor", "floor_distance", "C", "I"]
PHYS_FEATS = ["size", "floor_distance", "C", "I"]


def cv_r2(df: pd.DataFrame, feats, target="makespan", n_splits=5, seed=42):
    X = df[feats].to_numpy()
    y = df[target].to_numpy()
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=seed)
    scores = cross_val_score(LinearRegression(), X, y, cv=kf, scoring="r2")
    return float(np.mean(scores))


def fit_betas(df, feats, target="makespan"):
    X = df[feats].to_numpy()
    y = df[target].to_numpy()
    mdl = LinearRegression().fit(X, y)
    return {f: float(c) for f, c in zip(feats, mdl.coef_)}


def bootstrap_betas(df, feats, n_iter=500, seed=0, target="makespan"):
    rng = np.random.default_rng(seed)
    n = len(df)
    all_coefs = []
    for _ in range(n_iter):
        idx = rng.integers(0, n, n)
        sub = df.iloc[idx]
        X = sub[feats].to_numpy()
        y = sub[target].to_numpy()
        mdl = LinearRegression().fit(X, y)
        all_coefs.append(mdl.coef_)
    arr = np.array(all_coefs)
    out = {}
    for j, f in enumerate(feats):
        col = arr[:, j]
        out[f] = {
            "mean": float(col.mean()),
            "lo": float(np.percentile(col, 2.5)),
            "hi": float(np.percentile(col, 97.5)),
        }
    return out


def main() -> None:
    p1 = pd.read_csv(PHASE1_CSV)
    pb = pd.read_csv(BATCHED_CSV)

    # Strip the _batched suffix for matching; pb regime becomes e.g. E1_c2
    pb["regime_base"] = pb["regime"].str.replace("_batched", "", regex=False)

    regimes = ["E1_c2", "E2_c2", "E3_c2"]
    results = {
        "generated": "2026-04-21",
        "description": "Phase 1.5 batched vs throughput-abstraction comparison for c=2 regimes",
        "per_regime": {},
        "summary": {},
    }

    # Prepare paired-plot figure
    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    summary_rows = []

    for i, r in enumerate(regimes):
        abs_df = p1[p1["regime"] == r].sort_values("wave_id").reset_index(drop=True)
        bat_df = pb[pb["regime_base"] == r].sort_values("wave_id").reset_index(drop=True)

        assert len(abs_df) == len(bat_df), f"length mismatch at {r}"
        assert (abs_df["wave_id"].to_numpy() == bat_df["wave_id"].to_numpy()).all()

        delta = bat_df["makespan"].to_numpy() - abs_df["makespan"].to_numpy()
        pearson = float(np.corrcoef(abs_df["makespan"], bat_df["makespan"])[0, 1])

        r2_m1 = cv_r2(bat_df, M1_FEATS)
        r2_m2 = cv_r2(bat_df, M2_FEATS)
        r2_m3 = cv_r2(bat_df, M3_FEATS)
        m3_minus_m2 = r2_m3 - r2_m2

        betas = fit_betas(bat_df, PHYS_FEATS)
        boot = bootstrap_betas(bat_df, PHYS_FEATS, n_iter=500, seed=0)

        # also betas on abstraction for reference
        betas_abs = fit_betas(abs_df, PHYS_FEATS)

        per = {
            "makespan_abstraction": {
                "mean": float(abs_df["makespan"].mean()),
                "median": float(abs_df["makespan"].median()),
                "std": float(abs_df["makespan"].std()),
            },
            "makespan_batched": {
                "mean": float(bat_df["makespan"].mean()),
                "median": float(bat_df["makespan"].median()),
                "std": float(bat_df["makespan"].std()),
            },
            "delta_batched_minus_abstraction": {
                "mean": float(delta.mean()),
                "median": float(np.median(delta)),
                "std": float(delta.std()),
                "frac_batched_larger": float((delta > 0).mean()),
            },
            "pearson_makespans": pearson,
            "r2_cv": {"M1": r2_m1, "M2": r2_m2, "M3": r2_m3, "M3_minus_M2": m3_minus_m2},
            "betas_batched_ols": betas,
            "betas_bootstrap": boot,
            "betas_abstraction_ols_for_ref": betas_abs,
        }
        results["per_regime"][r] = per

        summary_rows.append({
            "regime": r,
            "mk_abs_median": per["makespan_abstraction"]["median"],
            "mk_bat_median": per["makespan_batched"]["median"],
            "delta_median": per["delta_batched_minus_abstraction"]["median"],
            "pearson": pearson,
            "M3-M2_abs": None,
            "M3-M2_bat": m3_minus_m2,
            "betaC_abs": betas_abs["C"],
            "betaC_bat": betas["C"],
        })

        # paired scatter
        ax = axes[i]
        ax.scatter(abs_df["makespan"], bat_df["makespan"], s=4, alpha=0.4)
        lo = min(abs_df["makespan"].min(), bat_df["makespan"].min())
        hi = max(abs_df["makespan"].max(), bat_df["makespan"].max())
        ax.plot([lo, hi], [lo, hi], "k--", lw=0.8)
        ax.set_xlabel("throughput-abstraction makespan (s)")
        ax.set_ylabel("true-batching makespan (s)")
        ax.set_title(f"{r}  r={pearson:.3f}  med_delta={per['delta_batched_minus_abstraction']['median']:+.1f}")

    fig.tight_layout()
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig_path = FIG_DIR / "phase1_5_paired_makespan.png"
    fig.savefig(fig_path, dpi=110)
    plt.close(fig)
    print(f"Saved paired-makespan figure: {fig_path}")

    # betaC comparison figure
    fig2, ax = plt.subplots(figsize=(7, 4))
    xs = np.arange(len(regimes))
    b_abs = [results["per_regime"][r]["betas_abstraction_ols_for_ref"]["C"] for r in regimes]
    b_bat = [results["per_regime"][r]["betas_batched_ols"]["C"] for r in regimes]
    ax.bar(xs - 0.18, b_abs, width=0.34, label="abstraction", color="#7a9")
    ax.bar(xs + 0.18, b_bat, width=0.34, label="batched", color="#c76")
    ax.axhline(0, color="k", lw=0.5)
    ax.set_xticks(xs)
    ax.set_xticklabels(regimes)
    ax.set_ylabel("beta(C) [s / nat]")
    ax.set_title("beta(C): throughput-abstraction vs true-batching")
    ax.legend()
    fig2.tight_layout()
    fig2_path = FIG_DIR / "phase1_5_betaC_comparison.png"
    fig2.savefig(fig2_path, dpi=110)
    plt.close(fig2)
    print(f"Saved betaC comparison figure: {fig2_path}")

    # Decision gate
    max_m3_minus_m2 = max(results["per_regime"][r]["r2_cv"]["M3_minus_M2"] for r in regimes)
    max_regime = max(regimes, key=lambda r: results["per_regime"][r]["r2_cv"]["M3_minus_M2"])
    if max_m3_minus_m2 >= 0.05:
        verdict = "SURROGATE_RESCUED"
    elif max_m3_minus_m2 >= 0.02:
        verdict = "AMBIGUOUS"
    else:
        verdict = "SURROGATE_FINAL_REJECTED"

    # Sign of beta(C) under batched
    betaC_signs = {r: np.sign(results["per_regime"][r]["betas_batched_ols"]["C"]) for r in regimes}
    betaC_abs_signs = {r: np.sign(results["per_regime"][r]["betas_abstraction_ols_for_ref"]["C"]) for r in regimes}
    sign_agreement = {r: bool(betaC_signs[r] == betaC_abs_signs[r]) for r in regimes}

    results["summary"] = {
        "max_M3_minus_M2_batched": float(max_m3_minus_m2),
        "max_regime": max_regime,
        "decision_gate_verdict": verdict,
        "betaC_sign_abstraction": {r: int(v) for r, v in betaC_abs_signs.items()},
        "betaC_sign_batched": {r: int(v) for r, v in betaC_signs.items()},
        "betaC_sign_agreement": sign_agreement,
        "paired_summary_table": summary_rows,
    }

    # Print report
    print()
    print("=" * 90)
    print("Phase 1.5 summary")
    print("=" * 90)
    print(f"{'regime':8s} {'mk_abs_med':>10s} {'mk_bat_med':>10s} {'delta_med':>10s} "
          f"{'pearson':>8s} {'M3-M2_bat':>10s} {'betaC_abs':>10s} {'betaC_bat':>10s}")
    for row in summary_rows:
        print(f"{row['regime']:8s} {row['mk_abs_median']:>10.2f} {row['mk_bat_median']:>10.2f} "
              f"{row['delta_median']:>+10.2f} {row['pearson']:>8.3f} "
              f"{row['M3-M2_bat']:>+10.4f} {row['betaC_abs']:>+10.2f} {row['betaC_bat']:>+10.2f}")
    print()
    print(f"  Max M3-M2 across batched c=2 regimes: {max_m3_minus_m2:+.4f}  (at {max_regime})")
    print(f"  Decision gate: {verdict}")
    for r in regimes:
        agree = "same sign" if sign_agreement[r] else "SIGN FLIPPED"
        print(f"    {r}: betaC abs={betaC_abs_signs[r]:+.0f}, batched={betaC_signs[r]:+.0f} ({agree})")

    out_path = RESULTS_DIR / "v0_2_phase1_5_true_batching.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    main()
