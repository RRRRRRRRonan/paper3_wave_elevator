"""
MVS v0.5 Phase 5 W6 — Block C model-chain analysis (Table 2, H-D2 + H-D3).

Reads the matched-wave mvs_v0_5_phase5_blockC.csv (makespan_M1/M2/M3_s20 on the
same waves). Evaluates:

  H-D2 (confirmatory)
    D2-a  per-wave M2 >= M1   >= 90 % avg over cells, >= 80 % worst cell
    D2-b  FOSD M1 <= M2 (quantile coupling) in >= 90 % of cells
    D2-c  one-sided U_c(0.05) < 5 % * m_0 in >= 80 % of cells
    D2-d  c*_DRO == c*_Hedge per config (Wasserstein-DRO == Hedge Rule)

  H-D3 (exploratory, non-gating)
    corner identity (q_max / q_min) invariance across M1/M2/M3, and
    corner-ranking Spearman rho vs M1 -> 'model-robust' or 'model-sensitive'.

Output: results/v0_5_phase5_blockC.json
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr, wasserstein_distance

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
CSV = RESULTS_DIR / "raw" / "mvs_v0_5_phase5_blockC.csv"
CORNERS = ["HC_HI", "HC_LI", "LC_HI", "LC_LI"]
MODELS = [("makespan_M1", "M1"), ("makespan_M2", "M2"),
          ("makespan_M3_s20", "M3")]
EPS = 0.05


def main() -> None:
    df = pd.read_csv(CSV)

    # ---- H-D2: per (config, corner) on matched M1/M2 -----------------------
    d2_cells = []
    dro = {}        # config -> {corner -> (hedge, dro)}
    for cid, gc in df.groupby("config_id"):
        m0 = float(np.median(gc[gc["arm"] == "random"]["makespan_M2"]))
        dro[cid] = {}
        for corner in CORNERS:
            sub = gc[gc["arm"] == corner]
            T1 = sub["makespan_M1"].to_numpy(float)
            T2 = sub["makespan_M2"].to_numpy(float)
            qa, qb = np.sort(T1), np.sort(T2)
            perwave = float(np.mean(T2 >= T1))
            fosd = float(np.mean(qb >= qa - 1e-9))
            w1 = float(wasserstein_distance(T1, T2))
            U_c = float(np.quantile(T2, 0.5 + EPS) - np.quantile(T2, 0.5))
            d2_cells.append({
                "config_id": int(cid), "corner": corner,
                "perwave_dom": perwave, "fosd": fosd,
                "W1": w1, "U_c_005": U_c, "m0": m0,
                "U_c_lt_5pct": bool(U_c < 0.05 * m0),
                "fosd_ok": bool(fosd >= 0.99),
            })
            dro[cid][corner] = (max(float(np.mean(T1)), float(np.mean(T2))),
                                float(np.mean(T1)) + w1)

    n_cells = len(d2_cells)
    perwave_avg = float(np.mean([c["perwave_dom"] for c in d2_cells]))
    perwave_worst = float(np.min([c["perwave_dom"] for c in d2_cells]))
    n_fosd = sum(c["fosd_ok"] for c in d2_cells)
    n_uc = sum(c["U_c_lt_5pct"] for c in d2_cells)

    d2d_rows = []
    for cid, cmap in dro.items():
        c_hedge = min(cmap, key=lambda c: cmap[c][0])
        c_dro = min(cmap, key=lambda c: cmap[c][1])
        d2d_rows.append({"config_id": int(cid), "c_star_Hedge": c_hedge,
                         "c_star_DRO": c_dro,
                         "collapse": bool(c_hedge == c_dro)})
    n_collapse = sum(r["collapse"] for r in d2d_rows)

    d2a = perwave_avg >= 0.90 and perwave_worst >= 0.80
    d2b = n_fosd >= 0.90 * n_cells
    d2c = n_uc >= 0.80 * n_cells
    d2d = n_collapse == len(d2d_rows)
    h_d2 = "PASS" if (d2a and d2b and d2c and d2d) else "PARTIAL"

    # ---- H-D3 (exploratory): corner identity / ranking across M1/M2/M3 -----
    d3_rows = []
    for cid, gc in df.groupby("config_id"):
        per_model = {}
        for col, name in MODELS:
            m_q = {c: float(np.median(gc[gc["arm"] == c][col]))
                   for c in CORNERS}
            per_model[name] = m_q
        qmax = {m: max(per_model[m], key=per_model[m].get) for m in per_model}
        qmin = {m: min(per_model[m], key=per_model[m].get) for m in per_model}
        base = [per_model["M1"][c] for c in CORNERS]
        rho = {m: float(spearmanr(base, [per_model[m][c] for c in CORNERS]).statistic)
               for m in ("M2", "M3")}
        d3_rows.append({
            "config_id": int(cid),
            "qmax_invariant": bool(len(set(qmax.values())) == 1),
            "qmin_invariant": bool(len(set(qmin.values())) == 1),
            "spearman_M2": rho["M2"], "spearman_M3": rho["M3"],
        })
    n_cfg = len(d3_rows)
    n_qmax = sum(r["qmax_invariant"] for r in d3_rows)
    n_qmin = sum(r["qmin_invariant"] for r in d3_rows)
    mean_rho = float(np.mean([r["spearman_M2"] for r in d3_rows]
                             + [r["spearman_M3"] for r in d3_rows]))
    identity_inv = sum(r["qmax_invariant"] and r["qmin_invariant"]
                       for r in d3_rows)
    h_d3_branch = ("model-robust" if (identity_inv >= 0.90 * n_cfg
                                      and mean_rho >= 0.8)
                   else "model-sensitive")

    print("=" * 80)
    print("Phase 5 W6 — Block C model chain (H-D2 + H-D3)")
    print("=" * 80)
    print(f"  H-D2 over {n_cells} (config,corner) cells:")
    print(f"    D2-a per-wave M2>=M1: avg={perwave_avg:.3f} "
          f"worst={perwave_worst:.3f}  -> {'PASS' if d2a else 'FAIL'}")
    print(f"    D2-b FOSD ok cells:   {n_fosd}/{n_cells}  "
          f"-> {'PASS' if d2b else 'FAIL'}")
    print(f"    D2-c U_c<5%*m0:       {n_uc}/{n_cells}  "
          f"-> {'PASS' if d2c else 'FAIL'}")
    print(f"    D2-d c*_DRO==c*_Hedge:{n_collapse}/{len(d2d_rows)}  "
          f"-> {'PASS' if d2d else 'FAIL'}")
    print(f"  H-D2 verdict: {h_d2}")
    print(f"\n  H-D3 (exploratory): qmax inv {n_qmax}/{n_cfg}, "
          f"qmin inv {n_qmin}/{n_cfg}, mean Spearman rho={mean_rho:+.3f}")
    print(f"  H-D3 branch: {h_d3_branch}")

    out = {
        "generated": "2026-05-19", "block": "C",
        "H_D2": {"n_cells": n_cells, "perwave_avg": perwave_avg,
                 "perwave_worst": perwave_worst, "n_fosd": n_fosd,
                 "n_U_c_ok": n_uc, "n_collapse": n_collapse,
                 "n_configs": len(d2d_rows),
                 "D2a": bool(d2a), "D2b": bool(d2b), "D2c": bool(d2c),
                 "D2d": bool(d2d), "verdict": h_d2,
                 "per_cell": d2_cells, "per_config_collapse": d2d_rows},
        "H_D3_exploratory": {"n_configs": n_cfg, "n_qmax_invariant": n_qmax,
                             "n_qmin_invariant": n_qmin,
                             "n_identity_invariant": identity_inv,
                             "mean_spearman_rho": mean_rho,
                             "branch": h_d3_branch, "per_config": d3_rows},
    }
    out_path = RESULTS_DIR / "v0_5_phase5_blockC.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved {out_path}")


if __name__ == "__main__":
    main()
