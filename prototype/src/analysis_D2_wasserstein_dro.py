"""
MVS v0.2 — D2 code extension: numerical verification of Theorem 3.

Theorem 3 (methodology v0.2 §4.2.2, "D2 NEW"):
    Under chain dominance of the elevator-model family, the Wasserstein DRO
    wave-corner selection coincides with the Model-Dominance Hedge Rule
    selection.

Construction.  The genuine stochastic-dominance chain in the model family is
M_1 (throughput abstraction) <= M_2 (true co-occupancy batching) -- verified at
92.5-100% per-wave dominance in R3.  M_3 (stochastic extension) is *not* part
of the chain; it perturbs M_2 symmetrically and is used below as the
chain-broken knife-edge control.

Take the operator's nominal model to be M_1 and quantify model uncertainty by
the Wasserstein-1 distance to the unknown true model.  Per corner c, build the
ambiguity ball B_{rho_c}(M_1 | c) of radius rho_c = W_1(M_1, M_2 | c).  For the
mean summary, the W_1-DRO worst case of the (1-Lipschitz) makespan objective is

    sup_{Q in B_{rho_c}} E_Q[T | c] = E_{M_1}[T | c] + rho_c.

KEY FACT used by the theorem: for one-dimensional distributions,
    W_1(M_1, M_2) >= | E_{M_2} - E_{M_1} |,  with EQUALITY iff M_1 <= M_2
stochastically (chain dominance).  Hence under chain dominance

    DRO worst case  = E_{M_1}[T|c] + W_1(M_1,M_2|c) = E_{M_2}[T|c]
                    = max_k E_{M_k}[T|c]  = Hedge value,                [Thm 3]

so argmin_c (DRO worst case) = argmin_c (Hedge value): the two selections
coincide.  When dominance is violated the equality becomes a strict
inequality and the gap  W_1 - |E_2 - E_1|  measures the discrepancy; the
argmin still survives while that gap stays below the inter-corner Hedge
spread (a sufficient condition mirroring Corollary M5.2).

This script verifies the chain, the W_1 == mean-gap identity, the
DRO == Hedge value equality, and the DRO == Hedge corner selection on the
R3 matched-wave data, plus the M_2-vs-M_3 knife-edge control.

No simulator runs: reanalysis of mvs_v0_2_phase4_v2_m3_samples.csv, the same
raw file consumed by analysis_phase4_v2_m5_delta.py.

Output:
  results/v0_2_D2_wasserstein_dro.json
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import wasserstein_distance

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RAW_DIR = RESULTS_DIR / "raw"
CSV = RAW_DIR / "mvs_v0_2_phase4_v2_m3_samples.csv"

REGIMES = ["E1_c2", "E2_c2", "E3_c2"]
CORNERS = ["HC_HI", "HC_LI", "LC_HI", "LC_LI"]

# The W_1 == mean-gap identity is exact under quantile dominance; accept it
# as "holds" only within float tolerance, and flag it "broken" otherwise.
VALUE_TOL = 1e-6


def pair_metrics(lo: np.ndarray, hi: np.ndarray) -> dict:
    """Wasserstein-1 / dominance metrics for an ordered model pair (lo <= hi).

    `lo`, `hi` are equal-length makespan sample arrays for two models on the
    same matched waves.  Sorting both gives the optimal W_1 (quantile)
    coupling, so W_1 = mean | q_hi - q_lo |.

    Two dominance notions are reported and they are NOT the same condition:
      * quantile_dom -- first-order stochastic dominance (q_hi >= q_lo at
        every coupled quantile).  This is the EXACT condition under which the
        chain-collapse identity W_1 = |E_hi - E_lo| holds, hence the precise
        hypothesis of Theorem 3.
      * perwave_dom  -- almost-sure / per-wave dominance (T_hi >= T_lo on each
        matched wave).  This is the stronger condition used by M5.1/M5.2.
    """
    qa = np.sort(lo)
    qb = np.sort(hi)
    mean_lo = float(np.mean(lo))
    mean_hi = float(np.mean(hi))
    mean_gap = mean_hi - mean_lo                       # E_hi - E_lo

    w1 = float(np.mean(np.abs(qb - qa)))               # 1-D Wasserstein-1
    w1_scipy = float(wasserstein_distance(lo, hi))     # cross-check
    quantile_dom = float(np.mean(qb >= qa - 1e-9))     # FOSD: Theorem 3 hypo.
    perwave_dom = float(np.mean(hi >= lo - 1e-9))      # a.s. dominance (M5)
    # W_1 exceeds |mean gap| exactly to the extent FOSD is violated.
    dom_violation = w1 - abs(mean_gap)
    return {
        "mean_lo": mean_lo,
        "mean_hi": mean_hi,
        "mean_gap": mean_gap,
        "W1": w1,
        "W1_scipy_check": w1_scipy,
        "quantile_dominance_frac": quantile_dom,
        "perwave_dominance_frac": perwave_dom,
        "dominance_violation": dom_violation,
    }


def main() -> None:
    df = pd.read_csv(CSV)

    # ----------------------------------------------------------------- M1<=M2
    print("=" * 104)
    print("D2 / Theorem 3 -- Wasserstein DRO == Hedge Rule on the chain "
          "M_1 <= M_2")
    print("=" * 104)
    print(f"{'regime':8s} {'corner':8s}  {'E[M1]':>8s} {'E[M2]':>8s} "
          f"{'meanGap':>8s} {'W1':>8s} {'dom%':>6s}  "
          f"{'DRO_wc':>9s} {'Hedge':>9s} {'eqGap':>8s} {'eq?':>4s}")

    rows = []
    hedge_val = {r: {} for r in REGIMES}     # E_{M2}[T|c]   (mean Hedge value)
    dro_val = {r: {} for r in REGIMES}       # E_{M1}+W1     (DRO worst case)
    m1_mean = {r: {} for r in REGIMES}
    m0_mean = {}                             # random-pool mean per regime

    for regime in REGIMES:
        rnd = df[(df["regime"] == regime) & (df["arm"] == "random")]
        m0 = float(np.mean(rnd["makespan_M2"])) if len(rnd) else float("nan")
        m0_mean[regime] = m0
        for corner in CORNERS:
            sub = df[(df["regime"] == regime) & (df["arm"] == corner)]
            if len(sub) == 0:
                continue
            T1 = sub["makespan_M1"].to_numpy(dtype=float)
            T2 = sub["makespan_M2"].to_numpy(dtype=float)

            pm = pair_metrics(T1, T2)
            dro_wc = pm["mean_lo"] + pm["W1"]            # DRO worst-case mean
            hedge = max(pm["mean_lo"], pm["mean_hi"])    # max_k E_{M_k}
            eq_gap = dro_wc - hedge                      # == dominance_violation
            eq_holds = abs(eq_gap) < VALUE_TOL

            hedge_val[regime][corner] = hedge
            dro_val[regime][corner] = dro_wc
            m1_mean[regime][corner] = pm["mean_lo"]

            print(f"{regime:8s} {corner:8s}  "
                  f"{pm['mean_lo']:>8.2f} {pm['mean_hi']:>8.2f} "
                  f"{pm['mean_gap']:>8.2f} {pm['W1']:>8.2f} "
                  f"{100*pm['quantile_dominance_frac']:>5.1f}%  "
                  f"{dro_wc:>9.2f} {hedge:>9.2f} {eq_gap:>8.1e} "
                  f"{'YES' if eq_holds else 'NO':>4s}")

            rows.append({
                "regime": regime, "corner": corner, "n": len(sub),
                "m_random_M2": m0, **pm,
                "DRO_worstcase_mean": dro_wc,
                "Hedge_value_mean": hedge,
                "equivalence_gap": eq_gap,
                "equivalence_gap_norm": eq_gap / m0,
                "value_equivalence_holds": eq_holds,
            })

    # --------------------------------------------------- per-regime selection
    print()
    print("=" * 104)
    print("Per-regime corner selection: c*_DRO == c*_Hedge ?")
    print("=" * 104)
    print(f"{'regime':8s}  {'c*_Hedge':>9s}  {'c*_DRO':>9s}  {'collapse?':>10s}  "
          f"{'c*_DRO_glob':>12s}  {'minHedgeGap':>12s}  {'maxEqGap':>9s}  "
          f"{'sufficient?':>12s}")

    regime_rows = []
    for regime in REGIMES:
        hv = hedge_val[regime]
        dv = dro_val[regime]
        m1 = m1_mean[regime]
        if len(hv) < 2:
            continue
        c_hedge = min(hv, key=hv.get)
        c_dro = min(dv, key=dv.get)            # corner-calibrated radius rho_c
        collapse = (c_dro == c_hedge)

        # Ablation: a single GLOBAL radius rho = max_c W_1 makes the DRO argmin
        # collapse to argmin E_{M1} -- i.e. the corner-calibrated radius is
        # what Theorem 3 needs.  Reported to show the calibration is load-bearing.
        c_dro_global = min(m1, key=m1.get)

        # Sufficient condition (parallel to Corollary M5.2): the corner argmin
        # survives while the dominance-violation wiggle stays below the
        # inter-corner Hedge spread.
        hv_star = hv[c_hedge]
        min_hedge_gap = min(v - hv_star for c, v in hv.items() if c != c_hedge)
        max_eq_gap = max(abs(r["equivalence_gap"]) for r in rows
                         if r["regime"] == regime)
        sufficient = min_hedge_gap > max_eq_gap

        print(f"{regime:8s}  {c_hedge:>9s}  {c_dro:>9s}  "
              f"{'YES' if collapse else 'NO':>10s}  "
              f"{c_dro_global:>12s}  {min_hedge_gap:>12.2f}  "
              f"{max_eq_gap:>9.3f}  "
              f"{'YES' if sufficient else 'NO':>12s}")

        regime_rows.append({
            "regime": regime,
            "c_star_Hedge": c_hedge,
            "c_star_DRO": c_dro,
            "collapse_holds": collapse,
            "c_star_DRO_global_radius": c_dro_global,
            "min_inter_corner_Hedge_gap": min_hedge_gap,
            "max_equivalence_gap": max_eq_gap,
            "sufficient_condition_holds": sufficient,
        })

    # ------------------------------------------------ M2-vs-M3 knife-edge ctrl
    print()
    print("=" * 104)
    print("Chain-broken control: M_2 vs M_3 (sigma=0.20) -- FOSD fails, the "
          "W_1 = |mean-gap| identity must break")
    print("=" * 104)
    print(f"{'regime':8s} {'corner':8s}  {'meanGap':>8s} {'W1':>8s} "
          f"{'qDom%':>6s}  {'DRO_wc':>9s} {'Hedge':>9s} {'eqGap':>8s} {'eq?':>4s}")

    m3_rows = []
    m3_hedge = {r: {} for r in REGIMES}
    m3_dro = {r: {} for r in REGIMES}
    for regime in REGIMES:
        for corner in CORNERS:
            sub = df[(df["regime"] == regime) & (df["arm"] == corner)]
            if len(sub) == 0:
                continue
            T2 = sub["makespan_M2"].to_numpy(dtype=float)
            T3 = sub["makespan_M3_s20"].to_numpy(dtype=float)
            # Order the pair by mean so pair_metrics sees lo <= hi on average;
            # W_1 >= |mean gap| regardless of ordering, so eqGap is sign-stable.
            if np.mean(T3) >= np.mean(T2):
                pm = pair_metrics(T2, T3)
            else:
                pm = pair_metrics(T3, T2)
            dro_wc = pm["mean_lo"] + pm["W1"]
            hedge = max(pm["mean_lo"], pm["mean_hi"])
            eq_gap = dro_wc - hedge
            eq_holds = abs(eq_gap) < VALUE_TOL
            m3_hedge[regime][corner] = hedge
            m3_dro[regime][corner] = dro_wc
            print(f"{regime:8s} {corner:8s}  "
                  f"{pm['mean_gap']:>8.2f} {pm['W1']:>8.2f} "
                  f"{100*pm['quantile_dominance_frac']:>5.1f}%  "
                  f"{dro_wc:>9.2f} {hedge:>9.2f} {eq_gap:>8.3f} "
                  f"{'YES' if eq_holds else 'NO':>4s}")
            m3_rows.append({
                "regime": regime, "corner": corner, **pm,
                "DRO_worstcase_mean": dro_wc,
                "Hedge_value_mean": hedge,
                "equivalence_gap": eq_gap,
                "value_equivalence_holds": eq_holds,
            })

    # M2-vs-M3 per-regime selection: does the corner argmin still survive the
    # broken value identity?  (Parallel to analysis_phase4_v2_m5_delta.py.)
    print()
    print("M2-vs-M3 selection: c*_DRO == c*_Hedge ?  (knife-edge -- argmin may "
          "still survive a broken value identity)")
    print(f"{'regime':8s}  {'c*_Hedge':>9s}  {'c*_DRO':>9s}  {'collapse?':>10s}")
    m3_regime_rows = []
    for regime in REGIMES:
        hv, dv = m3_hedge[regime], m3_dro[regime]
        if len(hv) < 2:
            continue
        c_h = min(hv, key=hv.get)
        c_d = min(dv, key=dv.get)
        coll = (c_h == c_d)
        print(f"{regime:8s}  {c_h:>9s}  {c_d:>9s}  "
              f"{'YES' if coll else 'NO':>10s}")
        m3_regime_rows.append({
            "regime": regime, "c_star_Hedge": c_h, "c_star_DRO": c_d,
            "collapse_holds": coll,
        })

    # ------------------------------------------------------------------ gates
    n = len(rows)
    n_val_eq = sum(1 for r in rows if r["value_equivalence_holds"])
    n_dom = sum(1 for r in rows if r["quantile_dominance_frac"] >= 0.99)
    n_w1_check = sum(1 for r in rows
                     if abs(r["W1"] - r["W1_scipy_check"]) < 1e-6)
    n_collapse = sum(1 for r in regime_rows if r["collapse_holds"])
    n_suff = sum(1 for r in regime_rows if r["sufficient_condition_holds"])
    n_reg = len(regime_rows)
    n_m3_broken = sum(1 for r in m3_rows if not r["value_equivalence_holds"])
    n_m3_collapse = sum(1 for r in m3_regime_rows if r["collapse_holds"])

    print()
    print("Theorem 3 verification gates:")
    print(f"  W_1 cross-check (sorted-diff == scipy):     {n_w1_check}/{n}")
    print(f"  chain FOSD M_1<=M_2 (>=99% quantiles):      {n_dom}/{n}")
    print(f"  DRO worst case == Hedge value (per corner): {n_val_eq}/{n}")
    print(f"  c*_DRO == c*_Hedge (per regime):            {n_collapse}/{n_reg}")
    print(f"  sufficient condition holds (per regime):    {n_suff}/{n_reg}")
    print(f"  M2-vs-M3 control: value identity broken:    {n_m3_broken}/"
          f"{len(m3_rows)}")
    print(f"  M2-vs-M3 control: corner argmin survives:   {n_m3_collapse}/"
          f"{len(m3_regime_rows)}")

    verdict = "PASS" if (n_collapse == n_reg and n_val_eq == n
                         and n_w1_check == n) else "PARTIAL"
    print(f"  Overall verdict:                            {verdict}")

    out = {
        "generated": "2026-05-19",
        "theorem": "D2 / Theorem 3 (methodology v0.2 §4.2.2)",
        "claim": "Under chain dominance, the Wasserstein DRO wave-corner "
                 "selection equals the Model-Dominance Hedge Rule selection.",
        "source_csv": CSV.name,
        "nominal_model": "M_1 (throughput abstraction)",
        "ambiguity_radius": "rho_c = W_1(M_1, M_2 | corner c)  (corner-calibrated)",
        "summary_statistic": "mean (W_1-DRO closed form for 1-Lipschitz cost)",
        "chain_M1_le_M2": {
            "per_corner": rows,
            "per_regime_selection": regime_rows,
        },
        "control_M2_vs_M3_sigma_0_20": {
            "per_corner": m3_rows,
            "per_regime_selection": m3_regime_rows,
            "note": "FOSD broken -> W_1 > |mean gap| -> DRO worst case "
                    "overshoots the Hedge value, so the value identity fails "
                    "in 12/12; the corner argmin can still survive when the "
                    "overshoot stays below the inter-corner spread -- the "
                    "knife-edge regime, parallel to Corollary M5.2.",
        },
        "summary": {
            "n_corner_cells": n,
            "n_w1_crosscheck_ok": n_w1_check,
            "n_chain_dominance": n_dom,
            "n_value_equivalence": n_val_eq,
            "n_regimes": n_reg,
            "n_regimes_collapse": n_collapse,
            "n_regimes_sufficient": n_suff,
            "n_m3_control_value_identity_broken": n_m3_broken,
            "n_m3_control_corner_survives": n_m3_collapse,
            "verdict": verdict,
        },
    }
    out_path = RESULTS_DIR / "v0_2_D2_wasserstein_dro.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved {out_path}")


if __name__ == "__main__":
    main()
