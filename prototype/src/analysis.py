"""
MVS v0.2 Phase 0 — non-linear diagnostic on v0.1 data.

Decision gate:
  - nonlinear R2 - linear R2 >= 0.05 -> H_v2.2 supported (use non-linear in v0.2)
  - nonlinear R2 - linear R2  < 0.02 -> H_v2.2 rejected (linear truly insufficient)

Input:  prototype/results/raw/mvs_v0_1_samples.csv  (1000 rows, from v0.1)
Output: prototype/results/v0_2_phase0_nonlinear.json (machine-readable)
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold, cross_val_score

DATA_PATH = Path(__file__).resolve().parents[1] / "results" / "raw" / "mvs_v0_1_samples.csv"
OUT_DIR = Path(__file__).resolve().parents[1] / "results"
RANDOM_STATE = 42
N_SPLITS = 5


def add_interactions(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["C_x_I"] = df["C"] * df["I"]
    out["I_sq"] = df["I"] ** 2
    out["C_sq"] = df["C"] ** 2
    out["C_x_crossfloor"] = df["C"] * df["cross_floor"]
    out["I_x_crossfloor"] = df["I"] * df["cross_floor"]
    out["size_x_I"] = df["size"] * df["I"]
    return out


def cv_r2(model, X, y, cv) -> float:
    return cross_val_score(model, X, y, cv=cv, scoring="r2").mean()


def main() -> None:
    df = pd.read_csv(DATA_PATH)
    y = df["makespan"]
    df_ext = add_interactions(df)

    base_cols = ["size", "cross_floor", "C", "I"]
    inter_cols = base_cols + ["C_x_I", "I_sq", "C_sq", "C_x_crossfloor", "I_x_crossfloor", "size_x_I"]

    X_base = df_ext[base_cols]
    X_inter = df_ext[inter_cols]
    cv = KFold(n_splits=N_SPLITS, shuffle=True, random_state=RANDOM_STATE)

    models = {
        "M1 linear (size)":               (LinearRegression(), df_ext[["size"]]),
        "M2 linear (size + cross_floor)": (LinearRegression(), df_ext[["size", "cross_floor"]]),
        "M3 linear (base)":               (LinearRegression(), X_base),
        "M3+ linear (+6 interactions)":   (LinearRegression(), X_inter),
        "RF (n=200)":                     (RandomForestRegressor(n_estimators=200, random_state=RANDOM_STATE, n_jobs=-1), X_base),
        "GBM (n=200, depth=3)":           (GradientBoostingRegressor(n_estimators=200, max_depth=3, random_state=RANDOM_STATE), X_base),
        "RF+interactions":                (RandomForestRegressor(n_estimators=200, random_state=RANDOM_STATE, n_jobs=-1), X_inter),
        "GBM+interactions":               (GradientBoostingRegressor(n_estimators=200, max_depth=3, random_state=RANDOM_STATE), X_inter),
    }

    results = {}
    print("=" * 62)
    print(f"{'Model':42s} {'CV R2':>10s}")
    print("=" * 62)
    for name, (model, X) in models.items():
        r2 = cv_r2(model, X, y, cv)
        results[name] = r2
        print(f"{name:42s} {r2:>10.4f}")
    print("=" * 62)

    linear_m3 = results["M3 linear (base)"]
    best_tree_base = max(results["RF (n=200)"], results["GBM (n=200, depth=3)"])
    best_tree_inter = max(results["RF+interactions"], results["GBM+interactions"])
    inter_linear = results["M3+ linear (+6 interactions)"]

    nonlinear_gap = best_tree_base - linear_m3
    interaction_linear_gap = inter_linear - linear_m3

    print()
    print(f"M3 linear (baseline):                  R2 = {linear_m3:.4f}")
    print(f"Best tree model on base features:      R2 = {best_tree_base:.4f}   (gap = {nonlinear_gap:+.4f})")
    print(f"Best tree model with interactions:     R2 = {best_tree_inter:.4f}")
    print(f"Linear with interaction terms:         R2 = {inter_linear:.4f}   (gap = {interaction_linear_gap:+.4f})")
    print()

    if nonlinear_gap >= 0.05:
        verdict = "PASSED"
        verdict_text = (
            "Non-linear gap >= 0.05 -> H_v2.2 supported. "
            "v0.2 Phase 1-4 should use non-linear surrogates."
        )
    elif nonlinear_gap >= 0.02:
        verdict = "AMBIGUOUS"
        verdict_text = (
            "Non-linear gap in [0.02, 0.05). Modest improvement; "
            "v0.2 may run both linear and non-linear in parallel."
        )
    else:
        verdict = "REJECTED"
        verdict_text = (
            "Non-linear gap < 0.02 -> H_v2.2 not supported. "
            "Non-linear modelling does not rescue v0.1 data; the signal limitation is structural, not functional-form."
        )
    print(f"DECISION GATE: {verdict}")
    print(verdict_text)

    # Permutation importance on RF (base features)
    rf = RandomForestRegressor(n_estimators=200, random_state=RANDOM_STATE, n_jobs=-1)
    rf.fit(X_base, y)
    perm = permutation_importance(rf, X_base, y, n_repeats=20, random_state=RANDOM_STATE, n_jobs=-1)
    print("\nPermutation importance (RF, base features, 20 repeats):")
    imp = {}
    for col, m, s in sorted(zip(X_base.columns, perm.importances_mean, perm.importances_std),
                            key=lambda x: -x[1]):
        print(f"  {col:15s} {m:+.4f}  (+- {s:.4f})")
        imp[col] = {"mean": float(m), "std": float(s)}

    # Interaction-term coefficients from M3+ linear (sign + magnitude)
    lr = LinearRegression().fit(X_inter, y)
    print("\nM3+ linear coefficients (including interactions):")
    coefs = {}
    for col, c in zip(X_inter.columns, lr.coef_):
        print(f"  {col:20s} {c:+8.4f}")
        coefs[col] = float(c)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with (OUT_DIR / "v0_2_phase0_nonlinear.json").open("w") as f:
        json.dump({
            "r2_cv": results,
            "m3_linear": linear_m3,
            "best_tree_base": best_tree_base,
            "best_tree_interactions": best_tree_inter,
            "interaction_linear": inter_linear,
            "nonlinear_gap": nonlinear_gap,
            "interaction_linear_gap": interaction_linear_gap,
            "verdict": verdict,
            "verdict_text": verdict_text,
            "permutation_importance_rf_base": imp,
            "m3plus_linear_coefficients": coefs,
        }, f, indent=2)

    print(f"\nResults saved to {OUT_DIR / 'v0_2_phase0_nonlinear.json'}")


if __name__ == "__main__":
    main()
