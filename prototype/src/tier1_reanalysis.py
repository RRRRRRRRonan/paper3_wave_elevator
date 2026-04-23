"""
MVS v0.2 Phase 1 — Tier 1 reanalysis (exploratory, no new data).

Re-cuts the existing 6000-row Phase 1 dataset under four exploratory lenses,
per pre-registration in intuitions_before_MVS_v0_2.md §1bis:

  1. Physical-unit beta reporting (seconds per natural-unit feature change),
     with bootstrap 95% CIs.
  2. Bootstrap CIs for R2 increments (M3 - M2).
  3. Controlled-subsample analysis: fix size in narrow bins, refit C/I.
  4. Geometric-mechanism reanalysis: relate beta(C) to N/F ratio across
     the 6 regimes (only 6 points; suggestive only).

Outputs:
  results/v0_2_phase1_tier1_reanalysis.json
  results/figures/tier1_*.png
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
RNG = np.random.default_rng(42)
N_BOOT = 500
N_AMRS_PHASE1 = 10
N_FLOORS_PHASE1 = 5


def fit_beta(df: pd.DataFrame, feats: list, y: str = "makespan") -> dict:
    lr = LinearRegression().fit(df[feats], df[y])
    return {f: float(c) for f, c in zip(feats, lr.coef_)}


def bootstrap_betas(df: pd.DataFrame, feats: list, n: int = N_BOOT) -> dict:
    """Return per-feature bootstrap mean and 95% CI for the beta coefficient."""
    n_rows = len(df)
    samples = {f: [] for f in feats}
    for _ in range(n):
        idx = RNG.integers(0, n_rows, size=n_rows)
        sub = df.iloc[idx]
        b = fit_beta(sub, feats)
        for f in feats:
            samples[f].append(b[f])
    out = {}
    for f in feats:
        arr = np.array(samples[f])
        out[f] = {
            "mean": float(arr.mean()),
            "ci_low": float(np.percentile(arr, 2.5)),
            "ci_high": float(np.percentile(arr, 97.5)),
        }
    return out


def bootstrap_r2_increment(df: pd.DataFrame, feats_full: list, feats_base: list,
                          n: int = N_BOOT) -> dict:
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    n_rows = len(df)
    deltas = []
    for _ in range(n):
        idx = RNG.integers(0, n_rows, size=n_rows)
        sub = df.iloc[idx]
        r2_full = cross_val_score(LinearRegression(), sub[feats_full],
                                  sub["makespan"], cv=cv, scoring="r2").mean()
        r2_base = cross_val_score(LinearRegression(), sub[feats_base],
                                  sub["makespan"], cv=cv, scoring="r2").mean()
        deltas.append(r2_full - r2_base)
    arr = np.array(deltas)
    return {
        "mean": float(arr.mean()),
        "ci_low": float(np.percentile(arr, 2.5)),
        "ci_high": float(np.percentile(arr, 97.5)),
    }


def controlled_subsample_fit(df: pd.DataFrame, size_band: tuple) -> dict:
    """Fit M3 on waves where size in size_band; report C, I betas + R2."""
    sub = df[(df["size"] >= size_band[0]) & (df["size"] <= size_band[1])].copy()
    if len(sub) < 30:
        return {"n": int(len(sub)), "skipped": True}
    feats = ["floor_distance", "C", "I"]
    lr = LinearRegression().fit(sub[feats], sub["makespan"])
    r2 = lr.score(sub[feats], sub["makespan"])
    coefs = {f: float(c) for f, c in zip(feats, lr.coef_)}
    return {"n": int(len(sub)), "coefs": coefs, "r2_in_sample": float(r2)}


def regime_to_n_over_f(regime: str, n_amrs: int = N_AMRS_PHASE1,
                       f_floors: int = N_FLOORS_PHASE1) -> float:
    """For Phase 1 data, N=10, F=5, so N/F=2 across all regimes.
    The varying quantity is N / effective_slots = N / (E*c).
    Use that as the geometric ratio.
    """
    parts = regime.split("_")
    E = int(parts[0][1:])
    cap = int(parts[1][1:])
    return n_amrs / (E * cap)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA)
    regimes = sorted(df["regime"].unique(),
                    key=lambda s: (int(s.split("_")[1][1:]), int(s.split("_")[0][1:])))

    feats_M3 = ["size", "floor_distance", "C", "I"]
    feats_M2 = ["size", "floor_distance"]

    # ---- 1. Physical-unit betas with bootstrap CIs ----
    print("=" * 84)
    print("Tier 1.1 — physical-unit betas with bootstrap 95% CIs (seconds per unit)")
    print("=" * 84)
    print(f"{'regime':>10s} {'beta(size)':>20s} {'beta(fdist)':>20s} {'beta(C)':>20s} {'beta(I)':>20s}")
    physunit = {}
    for regime in regimes:
        sub = df[df["regime"] == regime].copy()
        b = bootstrap_betas(sub, feats_M3)
        physunit[regime] = b
        def fmt(d):
            return f"{d['mean']:+7.2f} [{d['ci_low']:+6.2f},{d['ci_high']:+6.2f}]"
        print(f"{regime:>10s} {fmt(b['size']):>20s} {fmt(b['floor_distance']):>20s} "
              f"{fmt(b['C']):>20s} {fmt(b['I']):>20s}")

    # Pre-registered prediction check (Tier 1, single prediction):
    # |beta(C)| / |beta(size)| >= 0.30 in at least 4 regimes
    ratio_check = []
    for regime in regimes:
        b = physunit[regime]
        ratio = abs(b["C"]["mean"]) / abs(b["size"]["mean"])
        ratio_check.append((regime, ratio, ratio >= 0.30))
    n_pass = sum(1 for _, _, p in ratio_check if p)
    pred_held = n_pass >= 4
    print()
    print("Pre-registered Tier 1 prediction: |b(C)|/|b(size)| &gt;= 0.30 in &gt;= 4 of 6 regimes")
    for r, ratio, p in ratio_check:
        print(f"  {r:>8s}: ratio = {ratio:.2f} {'PASS' if p else 'fail'}")
    print(f"  -&gt; prediction {'HELD' if pred_held else 'FAILED'} ({n_pass}/6)")

    # ---- 2. Bootstrap CI for M3 - M2 increment ----
    print()
    print("=" * 84)
    print("Tier 1.2 — Bootstrap 95% CIs for the R2 increment M3 - M2")
    print("=" * 84)
    print(f"{'regime':>10s} {'M3-M2 mean':>15s} {'CI low':>10s} {'CI high':>10s} {'CI excludes 0?':>16s}")
    inc_ci = {}
    for regime in regimes:
        sub = df[df["regime"] == regime].copy()
        ci = bootstrap_r2_increment(sub, feats_M3, feats_M2, n=200)
        inc_ci[regime] = ci
        excl = (ci["ci_low"] > 0) or (ci["ci_high"] < 0)
        print(f"{regime:>10s} {ci['mean']:>+15.4f} {ci['ci_low']:>+10.4f} "
              f"{ci['ci_high']:>+10.4f} {'YES' if excl else 'no':>16s}")

    # ---- 3. Controlled subsample analysis ----
    print()
    print("=" * 84)
    print("Tier 1.3 — Controlled subsample fits (fix size band, look at C/I residual signal)")
    print("=" * 84)
    bands = [(3, 4), (5, 6), (7, 8)]
    csub = {}
    for regime in regimes:
        csub[regime] = {}
        sub = df[df["regime"] == regime].copy()
        print(f"\nRegime {regime}:")
        for band in bands:
            res = controlled_subsample_fit(sub, band)
            key = f"size_{band[0]}_{band[1]}"
            csub[regime][key] = res
            if res.get("skipped"):
                print(f"  size in [{band[0]},{band[1]}]: skipped (n={res['n']})")
            else:
                c = res["coefs"]
                print(f"  size in [{band[0]},{band[1]}] (n={res['n']:>4d}): "
                      f"R2={res['r2_in_sample']:.3f} "
                      f"b(fd)={c['floor_distance']:+6.2f} "
                      f"b(C)={c['C']:+7.2f} b(I)={c['I']:+7.2f}")

    # ---- 4. Geometric mechanism (only 6 points; suggestive) ----
    print()
    print("=" * 84)
    print("Tier 1.4 — Geometric mechanism: b(C) vs N/(E*c) ratio across 6 regimes")
    print("=" * 84)
    points = []
    for regime in regimes:
        ratio = regime_to_n_over_f(regime)
        b = physunit[regime]["C"]["mean"]
        points.append((regime, ratio, b))
    print(f"{'regime':>10s} {'N/(E*c)':>10s} {'b(C)':>10s}")
    for r, ratio, b in points:
        print(f"{r:>10s} {ratio:>10.2f} {b:>+10.2f}")
    arr_x = np.array([p[1] for p in points])
    arr_y = np.array([p[2] for p in points])
    if len(np.unique(arr_x)) > 1:
        corr = float(np.corrcoef(arr_x, arr_y)[0, 1])
        print(f"\nPearson correlation(N/(E*c), b(C)) = {corr:+.3f}")
        print("  Note: only 6 data points; this is suggestive, not confirmatory.")
        print("  Geometric experiment §1ter will sweep (N, F) directly to test the mechanism.")
    else:
        corr = None

    # Plots
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for r, ratio, b in points:
        ax.scatter(ratio, b, s=80, label=r)
        ax.annotate(r, (ratio, b), fontsize=8, xytext=(5, 5), textcoords="offset points")
    ax.set_xlabel("N_AMRs / (n_elevators x capacity)")
    ax.set_ylabel("b(C) — seconds per nat (in M3 fit)")
    ax.axhline(0, color="grey", lw=0.5)
    ax.set_title("Tier 1.4: b(C) vs effective fleet/slot ratio (6 Phase-1 regimes)")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "tier1_4_betaC_vs_NoverEc.png", dpi=120)
    plt.close()

    # Beta(size) bar plot per regime, with C and I overlaid
    fig, ax = plt.subplots(figsize=(8, 4.5))
    x = np.arange(len(regimes))
    w = 0.25
    ax.bar(x - w, [physunit[r]["size"]["mean"] for r in regimes], w, label="b(size)")
    ax.bar(x, [physunit[r]["C"]["mean"] for r in regimes], w, label="b(C)")
    ax.bar(x + w, [physunit[r]["I"]["mean"] for r in regimes], w, label="b(I)")
    ax.set_xticks(x)
    ax.set_xticklabels(regimes, rotation=20)
    ax.axhline(0, color="grey", lw=0.5)
    ax.set_ylabel("b (seconds per unit feature)")
    ax.set_title("Tier 1.1: physical-unit b across regimes")
    ax.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "tier1_1_beta_physunits.png", dpi=120)
    plt.close()

    out = {
        "physical_units_betas": physunit,
        "preregistered_tier1_prediction": {
            "rule": "|b(C)|/|b(size)| &gt;= 0.30 in &gt;= 4 of 6 regimes",
            "per_regime": [{"regime": r, "ratio": ratio, "passes": p}
                           for r, ratio, p in ratio_check],
            "n_passing": int(n_pass),
            "verdict": "HELD" if pred_held else "FAILED",
        },
        "r2_increment_bootstrap_ci": inc_ci,
        "controlled_subsample_fits": csub,
        "geometric_suggestive": {
            "points": [{"regime": r, "n_over_ec": ratio, "beta_C": b}
                       for r, ratio, b in points],
            "pearson_corr": corr,
        },
    }
    out_json = OUT_DIR / "v0_2_phase1_tier1_reanalysis.json"
    with out_json.open("w") as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved JSON to {out_json}")
    print(f"Saved figures to {FIG_DIR}")


if __name__ == "__main__":
    main()
