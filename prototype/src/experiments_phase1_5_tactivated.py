"""
MVS v0.2 Tier-1 Gap 2 extension — Phase 1.5 re-run with T dimension activated.

Closes the "T empty promise" gap: re-run the 3 c=2 regimes with staggered
per-order release_times so that temporal_clustering(wave) is non-zero,
then fit OLS `makespan ~ size + C + I + T + cross_floor + floor_distance`
and report beta(T) significance alongside beta(C), beta(I).

Design:
  - 3 c=2 regimes (E1_c2, E2_c2, E3_c2), batched model
  - Wave specs identical to Phase 1.5 for matched wave IDs
  - Each wave has per-order inter-arrival from Lognormal(mean=1, CV=0.5)
    (chosen as the largest CV empirically supported by Gap 2 sensitivity
    without corner-argmin flip)
  - 2000 samples per regime (matches Phase 1.5 N_SAMPLES)
  - OLS + bootstrap CI on each coefficient

Output:
  - results/raw/mvs_v0_2_phase1_5_tactivated_samples.csv
  - results/v0_2_phase1_5_tactivated.json (coefficient table + R^2)
"""
from __future__ import annotations

import json
import math
import random
import time
from pathlib import Path
from typing import List, Tuple

import numpy as np
import pandas as pd

from src.experiments_v0_2 import (
    N_AMRS,
    N_SAMPLES,
    build_order_pool,
    generate_wave_specs,
)
from src.features import compute_all_features
from src.simulator import Order, Wave, simulate_wave

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RAW_DIR = RESULTS_DIR / "raw"
OUT_JSON = RESULTS_DIR / "v0_2_phase1_5_tactivated.json"

BATCHED_REGIMES = [(1, 2), (2, 2), (3, 2)]
STAGGER_CV = 0.5  # empirically supported (Gap 2 sensitivity: argmin-stable)

FEATURES = ["size", "cross_floor", "floor_distance", "C", "I", "T"]


def stagger_orders(orders: List[Order], cv: float, rng: random.Random) -> List[Order]:
    """Per-order release_times from lognormal inter-arrival (mean 1, given CV)."""
    if cv <= 0:
        return [Order(o.id, o.source_floor, o.dest_floor, release_time=0.0)
                for o in orders]
    sigma = math.sqrt(math.log(1.0 + cv * cv))
    mu = -0.5 * sigma * sigma
    t = 0.0
    out = []
    for o in orders:
        t += math.exp(rng.gauss(mu, sigma))
        out.append(Order(o.id, o.source_floor, o.dest_floor, release_time=t))
    return out


def run_regime(regime: Tuple[int, int], pool: List[Order],
               specs, seed: int) -> pd.DataFrame:
    E, cap = regime
    rng = random.Random(seed)
    rows = []
    for wave_id, (size, idxs) in enumerate(specs):
        base_orders = [pool[i] for i in idxs]
        staggered = stagger_orders(base_orders, STAGGER_CV, rng)
        wave = Wave(orders=staggered, release_time=0.0)
        mk = simulate_wave(
            wave, n_amrs=N_AMRS, n_elevators=E, capacity=cap, batched=True,
        )
        feats = compute_all_features(wave)
        rows.append({
            "regime": f"E{E}_c{cap}",
            "wave_id": wave_id,
            **feats,
            "makespan": mk,
        })
    return pd.DataFrame(rows)


def ols_with_bootstrap(df: pd.DataFrame, n_boot: int = 500, seed: int = 42):
    """Return {coef_name: (est, lo, hi, sign_stability)} plus R^2 on OLS."""
    X = df[FEATURES].to_numpy(dtype=float)
    y = df["makespan"].to_numpy(dtype=float)
    X_with_intercept = np.column_stack([np.ones(len(X)), X])
    coef, *_ = np.linalg.lstsq(X_with_intercept, y, rcond=None)
    y_pred = X_with_intercept @ coef
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")

    rng = np.random.default_rng(seed)
    n = len(df)
    boot_coefs = np.zeros((n_boot, X_with_intercept.shape[1]))
    for i in range(n_boot):
        idx = rng.integers(0, n, size=n)
        c, *_ = np.linalg.lstsq(X_with_intercept[idx], y[idx], rcond=None)
        boot_coefs[i] = c
    names = ["intercept"] + FEATURES
    result = {}
    for j, name in enumerate(names):
        lo, hi = np.percentile(boot_coefs[:, j], [2.5, 97.5])
        sign_stability = float((np.sign(boot_coefs[:, j]) == np.sign(coef[j])).mean())
        result[name] = {
            "estimate": float(coef[j]),
            "ci_lo": float(lo),
            "ci_hi": float(hi),
            "sign_stability": sign_stability,
        }
    return result, r2


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    pool = build_order_pool(seed=43)
    specs = generate_wave_specs(n_samples=N_SAMPLES, seed=2026)

    print("=" * 110)
    print(f"Phase 1.5 T-activated re-run — stagger CV = {STAGGER_CV}, "
          f"{N_SAMPLES} waves x 3 regimes")
    print("=" * 110)

    all_dfs = []
    regime_results = {}
    t_total = time.time()

    for regime in BATCHED_REGIMES:
        E, cap = regime
        regime_str = f"E{E}_c{cap}"
        df = run_regime(regime, pool, specs, seed=2026 + E)
        all_dfs.append(df)
        t_cv_in_df = df["T"].describe()
        coefs, r2 = ols_with_bootstrap(df)
        regime_results[regime_str] = {
            "n": int(len(df)),
            "T_stats": {
                "mean": float(df["T"].mean()),
                "std": float(df["T"].std()),
                "p25": float(df["T"].quantile(0.25)),
                "p75": float(df["T"].quantile(0.75)),
            },
            "R2": r2,
            "coefficients": coefs,
        }
        print(f"\n{regime_str}  R^2 = {r2:.3f}  T empirical mean = {df['T'].mean():.3f}  "
              f"T std = {df['T'].std():.3f}")
        print(f"  {'feature':12s}  {'beta':>9s}  {'95% CI':>22s}  {'sign_stab':>10s}")
        for feat in FEATURES:
            c = coefs[feat]
            ci = f"[{c['ci_lo']:+.3f}, {c['ci_hi']:+.3f}]"
            star = " *" if (c["ci_lo"] > 0 or c["ci_hi"] < 0) else ""
            print(f"  {feat:12s}  {c['estimate']:>+9.3f}  {ci:>22s}  "
                  f"{c['sign_stability']:>9.1%}{star}")

    df_all = pd.concat(all_dfs, ignore_index=True)
    raw_csv = RAW_DIR / "mvs_v0_2_phase1_5_tactivated_samples.csv"
    df_all.to_csv(raw_csv, index=False)

    # Summary table focusing on beta(T)
    print()
    print("=" * 110)
    print("beta(T) summary across regimes")
    print("=" * 110)
    print(f"{'regime':8s}  {'beta_T':>8s}  {'95% CI':>24s}  {'sig':>5s}  "
          f"{'sign_stab':>10s}")
    n_sig_T = 0
    for regime_str, res in regime_results.items():
        c = res["coefficients"]["T"]
        ci = f"[{c['ci_lo']:+.3f}, {c['ci_hi']:+.3f}]"
        sig = c["ci_lo"] > 0 or c["ci_hi"] < 0
        if sig:
            n_sig_T += 1
        print(f"{regime_str:8s}  {c['estimate']:>+8.3f}  {ci:>24s}  "
              f"{'YES' if sig else 'no':>5s}  {c['sign_stability']:>9.1%}")
    print()
    print(f"Regimes where beta(T) is significant (CI excludes 0): {n_sig_T}/3")

    if n_sig_T >= 2:
        verdict = ("T ACTIVATED — T carries measurable regression signal in >= 2/3 "
                   "regimes; Phi = (C, I, T) 3D claim substantiated")
    elif n_sig_T == 1:
        verdict = ("T ACTIVATED BUT WEAK — signal present in 1/3; report as "
                   "regime-conditional contribution of T")
    else:
        verdict = ("T STILL WEAK — non-zero by construction but not significant at "
                   "CV = 0.5; scope restriction remains")
    print(f"Verdict: {verdict}")
    print(f"Total runtime: {time.time() - t_total:.1f}s")

    out = {
        "generated": "2026-04-22",
        "purpose": "Tier-1 Gap 2 extension: Phase 1.5 re-run with T dimension activated",
        "stagger_cv": STAGGER_CV,
        "n_samples_per_regime": N_SAMPLES,
        "per_regime": regime_results,
        "summary": {
            "n_regimes_beta_T_significant": n_sig_T,
            "verdict": verdict,
        },
    }
    OUT_JSON.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nSaved {OUT_JSON}")
    print(f"Saved {raw_csv}")


if __name__ == "__main__":
    main()
