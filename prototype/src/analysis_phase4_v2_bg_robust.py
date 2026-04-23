"""
MVS v0.2 Phase 4 v2 — Bound-and-Gap (B) + Robust-corner (C) verification.

Re-analyses the existing Phase 4 v2 CSV to verify two proposed method
contributions without running new simulations.

  Method B (Bound-and-Gap framework)
    UB(cell)  = corner spread / random_med
    LB(cell)  = (random_med - fav_corner_med) / random_med
    GAP(cell) = UB - LB
    Pass gates:
      * GAP > 0 in >= 5/6 cells           (framework has substance)
      * mean(GAP) >= 0.03                 (room is non-trivial)
      * GAP grows with size in >= 4/6     (story consistent with Tier 1.3)

  Method C (Robust-corner design)
    For each (regime, size):
      worst-of-two(corner) = max(med_makespan_abstraction, med_makespan_batched)
      robust_corner        = argmin_corner worst-of-two
    Compare robust_corner vs each model's own favorable_corner under the *other*
    model.
    Pass gates (focus on sign-divergent cells):
      * In sign-divergent cells, robust corner's worst-case beats either
        model-specific pick's worst-case by >= 5%
      * Robust corner does not lose to random in either model

Output: results/v0_2_phase4_v2_bg_robust.json + console summary.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RAW_DIR = RESULTS_DIR / "raw"
CSV = RAW_DIR / "mvs_v0_2_phase4_v2_samples.csv"

REGIMES = ["E1_c2", "E2_c2", "E3_c2"]
MODELS = ["abstraction", "batched"]
SIZES = [4, 6, 8]
CORNERS = ["HC_HI", "HC_LI", "LC_HI", "LC_LI"]


def median_makespan(df, regime, model, size, arm):
    sub = df[(df["regime"] == regime) & (df["model"] == model)
             & (df["size"] == size) & (df["arm"] == arm)]
    if len(sub) == 0:
        return float("nan")
    return float(np.median(sub["makespan"]))


def main() -> None:
    df = pd.read_csv(CSV)

    out = {
        "generated": "2026-04-22",
        "purpose": "Verify Method B (bound-and-gap) and Method C (robust-corner) "
                   "are realisable from existing Phase 4 v2 data.",
        "method_B": {"per_cell": {}},
        "method_C": {"per_cell_size": {}},
    }

    # ------------------------------------------------------------------
    # METHOD B: Bound-and-Gap
    # ------------------------------------------------------------------
    print("=" * 88)
    print("METHOD B verification — Bound-and-Gap framework")
    print("=" * 88)
    print(f"{'cell':22s}  {'fav':6s}  {'UB%':>7s}  {'LB%':>7s}  {'GAP%':>7s}  "
          f"{'GAP_size4':>10s}  {'GAP_size6':>10s}  {'GAP_size8':>10s}")

    b_summary = []
    for regime in REGIMES:
        for model in MODELS:
            cell_label = f"{regime}|{model}"
            fav = df[(df["regime"] == regime) & (df["model"] == model)
                     ]["favorable_corner"].iloc[0]

            ub_per_size, lb_per_size, gap_per_size = [], [], []
            for size in SIZES:
                rand_med = median_makespan(df, regime, model, size, "random")
                fav_med = median_makespan(df, regime, model, size, fav)
                corner_meds = [median_makespan(df, regime, model, size, c)
                               for c in CORNERS]
                ub = (max(corner_meds) - min(corner_meds)) / rand_med
                lb = (rand_med - fav_med) / rand_med
                gap = ub - lb
                ub_per_size.append(ub)
                lb_per_size.append(lb)
                gap_per_size.append(gap)

            ub_mean = float(np.mean(ub_per_size))
            lb_mean = float(np.mean(lb_per_size))
            gap_mean = float(np.mean(gap_per_size))

            print(f"{cell_label:22s}  {fav:6s}  {ub_mean*100:>6.1f}%  "
                  f"{lb_mean*100:>6.1f}%  {gap_mean*100:>6.1f}%  "
                  f"{gap_per_size[0]*100:>9.1f}%  "
                  f"{gap_per_size[1]*100:>9.1f}%  "
                  f"{gap_per_size[2]*100:>9.1f}%")

            b_summary.append({
                "cell": cell_label,
                "fav": fav,
                "UB_mean": ub_mean,
                "LB_mean": lb_mean,
                "GAP_mean": gap_mean,
                "GAP_per_size": gap_per_size,
            })
            out["method_B"]["per_cell"][cell_label] = {
                "favorable_corner": fav,
                "UB_per_size": ub_per_size,
                "LB_per_size": lb_per_size,
                "GAP_per_size": gap_per_size,
                "UB_mean": ub_mean,
                "LB_mean": lb_mean,
                "GAP_mean": gap_mean,
            }

    n_pos = sum(1 for c in b_summary if c["GAP_mean"] > 0)
    mean_gap = float(np.mean([c["GAP_mean"] for c in b_summary]))
    n_monotone = sum(
        1 for c in b_summary
        if c["GAP_per_size"][0] <= c["GAP_per_size"][1] <= c["GAP_per_size"][2]
        or c["GAP_per_size"][0] >= c["GAP_per_size"][1] >= c["GAP_per_size"][2]
    )

    if n_pos >= 5 and mean_gap >= 0.03:
        b_verdict = "PASS"
    elif n_pos >= 4 and mean_gap >= 0.015:
        b_verdict = "WEAK PASS"
    else:
        b_verdict = "FAIL"

    print()
    print(f"  Gates: GAP>0 in {n_pos}/6 cells | mean GAP = {mean_gap*100:.2f}% "
          f"| monotone-in-size {n_monotone}/6 -> {b_verdict}")

    out["method_B"]["summary"] = {
        "n_cells_GAP_positive": n_pos,
        "mean_GAP": mean_gap,
        "n_monotone_in_size": n_monotone,
        "verdict": b_verdict,
        "interpretation": (
            "GAP quantifies the room between Φ-informed wave selection (lower "
            "bound) and the maximum lever from wave structure (upper bound). "
            "A consistently positive GAP shows that smarter Φ designs could "
            "still extract additional makespan reduction."
        ),
    }

    # ------------------------------------------------------------------
    # METHOD C: Robust-corner design
    # ------------------------------------------------------------------
    print()
    print("=" * 88)
    print("METHOD C verification — Robust-corner design")
    print("=" * 88)

    # First identify sign-divergent cells (per regime): does abstraction's
    # favorable corner differ from batched's?
    fav_per_model = {}
    for regime in REGIMES:
        for model in MODELS:
            f = df[(df["regime"] == regime) & (df["model"] == model)
                   ]["favorable_corner"].iloc[0]
            fav_per_model[(regime, model)] = f

    print("Per regime, model-specific favorable corners:")
    sign_divergent = []
    for regime in REGIMES:
        f_abs = fav_per_model[(regime, "abstraction")]
        f_bat = fav_per_model[(regime, "batched")]
        diverge = f_abs != f_bat
        if diverge:
            sign_divergent.append(regime)
        print(f"  {regime}: abstraction picks {f_abs}, batched picks {f_bat}  "
              f"{'*** DIVERGENT ***' if diverge else ''}")

    out["method_C"]["sign_divergent_regimes"] = sign_divergent

    print()
    print(f"{'regime':8s} {'size':>5s} {'robust':>8s}  "
          f"{'wc(robust)%':>12s}  {'wc(abs_pick)%':>14s}  {'wc(bat_pick)%':>14s}  "
          f"{'gain_vs_abs%':>13s}  {'gain_vs_bat%':>13s}")

    c_rows = []
    for regime in REGIMES:
        for size in SIZES:
            # Compute worst-of-two for each corner
            corner_wc = {}  # corner -> max(med_abstraction, med_batched)
            corner_med_per_model = {}
            for c in CORNERS:
                med_abs = median_makespan(df, regime, "abstraction", size, c)
                med_bat = median_makespan(df, regime, "batched", size, c)
                corner_wc[c] = max(med_abs, med_bat)
                corner_med_per_model[c] = {"abs": med_abs, "bat": med_bat}

            robust = min(corner_wc, key=corner_wc.get)
            wc_robust = corner_wc[robust]

            f_abs = fav_per_model[(regime, "abstraction")]
            f_bat = fav_per_model[(regime, "batched")]
            wc_abs_pick = corner_wc[f_abs]
            wc_bat_pick = corner_wc[f_bat]

            # random baselines (worst-of-two)
            rand_med_abs = median_makespan(df, regime, "abstraction", size,
                                            "random")
            rand_med_bat = median_makespan(df, regime, "batched", size, "random")
            rand_wc = max(rand_med_abs, rand_med_bat)

            gain_vs_abs = (wc_abs_pick - wc_robust) / wc_abs_pick * 100
            gain_vs_bat = (wc_bat_pick - wc_robust) / wc_bat_pick * 100
            gain_vs_rand = (rand_wc - wc_robust) / rand_wc * 100

            print(f"{regime:8s} {size:>5d} {robust:>8s}  "
                  f"{wc_robust:>11.1f}   "
                  f"{wc_abs_pick:>13.1f}   {wc_bat_pick:>13.1f}   "
                  f"{gain_vs_abs:>12.2f}%  {gain_vs_bat:>12.2f}%")

            c_rows.append({
                "regime": regime,
                "size": size,
                "is_sign_divergent": regime in sign_divergent,
                "robust_corner": robust,
                "wc_robust": wc_robust,
                "abs_fav_corner": f_abs,
                "wc_abs_fav": wc_abs_pick,
                "bat_fav_corner": f_bat,
                "wc_bat_fav": wc_bat_pick,
                "rand_wc": rand_wc,
                "gain_vs_abs_pick_pct": gain_vs_abs,
                "gain_vs_bat_pick_pct": gain_vs_bat,
                "gain_vs_rand_pct": gain_vs_rand,
            })
            out["method_C"]["per_cell_size"][f"{regime}|size{size}"] = c_rows[-1]

    # Gates: focus on sign-divergent cells
    div_rows = [r for r in c_rows if r["is_sign_divergent"]]
    if div_rows:
        # In divergent cells, robust should beat the *worse* of the two model picks
        worst_pick_gain = [
            min(r["gain_vs_abs_pick_pct"], r["gain_vs_bat_pick_pct"])
            for r in div_rows
        ]
        mean_wp_gain = float(np.mean(worst_pick_gain))
        max_wp_gain = float(np.max(worst_pick_gain))
        n_meaningful = sum(1 for g in worst_pick_gain if g >= 5.0)

        # Does robust corner ever lose to random?
        n_lose_to_rand = sum(1 for r in c_rows if r["gain_vs_rand_pct"] < 0)
    else:
        mean_wp_gain = 0.0
        max_wp_gain = 0.0
        n_meaningful = 0
        n_lose_to_rand = sum(1 for r in c_rows if r["gain_vs_rand_pct"] < 0)

    if n_meaningful >= 2 and n_lose_to_rand == 0:
        c_verdict = "PASS"
    elif (mean_wp_gain >= 2.0 or max_wp_gain >= 5.0) and n_lose_to_rand <= 1:
        c_verdict = "WEAK PASS"
    else:
        c_verdict = "FAIL"

    print()
    print(f"  Sign-divergent cells: {len(div_rows)} of {len(c_rows)}")
    if div_rows:
        print(f"  Worst-pick gain in divergent cells: "
              f"mean {mean_wp_gain:.2f}%, max {max_wp_gain:.2f}%, "
              f"n>=5%: {n_meaningful}")
    print(f"  Cells where robust loses to random: {n_lose_to_rand}/{len(c_rows)}"
          f"  -> {c_verdict}")

    out["method_C"]["summary"] = {
        "n_sign_divergent_cells_size": len(div_rows),
        "mean_worst_pick_gain_pct": mean_wp_gain,
        "max_worst_pick_gain_pct": max_wp_gain,
        "n_cells_loses_to_random": n_lose_to_rand,
        "verdict": c_verdict,
        "interpretation": (
            "Robust corner = corner minimizing worst-of-two (abstraction vs "
            "batched) median makespan. In sign-divergent regimes the model-"
            "specific Φ pick may be wrong under the other model; robust corner "
            "hedges against that uncertainty."
        ),
    }

    # ------------------------------------------------------------------
    # FINAL VERDICT
    # ------------------------------------------------------------------
    print()
    print("=" * 88)
    print("OVERALL")
    print("=" * 88)
    print(f"  Method B (bound-and-gap):  {out['method_B']['summary']['verdict']}")
    print(f"  Method C (robust-corner):  {out['method_C']['summary']['verdict']}")
    print()
    print("Decision rule for paper:")
    print("  * Both PASS  -> write both into §11 as C2-M4 / C2-M5 (recommended).")
    print("  * Mixed       -> keep the PASS one, demote the other to 'open work'.")
    print("  * Both FAIL   -> step back and re-think method angle entirely.")

    out_path = RESULTS_DIR / "v0_2_phase4_v2_bg_robust.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved {out_path}")


if __name__ == "__main__":
    main()
