"""
MVS v0.5 Phase 5 W6 — Block B 7-policy contest (Table 3, H-Policy gate).

Reads mvs_v0_5_phase5_blockB.csv (P0-P6) and the P7 ablation CSV. Per
(config, size) cell computes each policy's median makespan, builds the 7x7
win-fraction matrix, and evaluates the pre-registered H-Policy bands:

  Policy-Strong  : P5 beats P0 >= 90 %, P1 >= 60 %, P6 >= 50 %
  Policy-Partial : P5 beats P0 >= 75 %, P1 >= 50 %
  Policy-Weak    : P5 fails to beat P0 in >= 75 % of cells

Also reports P5 vs P6 (the D1 differentiator) and P5 vs P7 (optimization gap).

Output: results/v0_5_phase5_blockB.json
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RAW = RESULTS_DIR / "raw"
POLICIES = ["P0_random", "P1_dest_cluster", "P2_cardinality",
            "P3_dir_balanced", "P4_temporal", "P5_phi", "P6_spo_tree"]


def main() -> None:
    dfB = pd.read_csv(RAW / "mvs_v0_5_phase5_blockB.csv")
    dfP7 = pd.read_csv(RAW / "mvs_v0_5_phase5_ablation_P7.csv")

    # per (config, size) median makespan for each policy
    cells = []
    for (cid, size), g in dfB.groupby(["config_id", "size"]):
        med = {p: float(np.median(g[g["policy"] == p]["makespan"]))
               for p in POLICIES}
        g7 = dfP7[(dfP7["config_id"] == cid) & (dfP7["size"] == size)]
        med["P7_localsearch"] = float(np.median(g7["makespan"]))
        cells.append({"config_id": int(cid), "size": int(size), **med})

    n = len(cells)
    allp = POLICIES + ["P7_localsearch"]

    # win-fraction matrix: win[i][j] = frac of cells where i's median < j's
    win = {i: {} for i in allp}
    for i in allp:
        for j in allp:
            if i == j:
                win[i][j] = float("nan")
            else:
                win[i][j] = float(np.mean([c[i] < c[j] for c in cells]))

    p5_v_p0 = win["P5_phi"]["P0_random"]
    p5_v_p1 = win["P5_phi"]["P1_dest_cluster"]
    p5_v_p6 = win["P5_phi"]["P6_spo_tree"]
    p5_v_p7 = win["P5_phi"]["P7_localsearch"]

    if p5_v_p0 >= 0.90 and p5_v_p1 >= 0.60 and p5_v_p6 >= 0.50:
        band = "Policy-Strong"
    elif p5_v_p0 >= 0.75 and p5_v_p1 >= 0.50:
        band = "Policy-Partial"
    elif p5_v_p0 < 0.25:                          # P5 fails P0 in >=75 %
        band = "Policy-Weak"
    else:
        band = "Policy-Partial (lower)"

    # P5 vs P7: how far above the local-search optimum, mean over cells
    p5_above_p7 = float(np.mean([(c["P5_phi"] - c["P7_localsearch"])
                                 / c["P7_localsearch"] for c in cells]))

    print("=" * 80)
    print("Phase 5 W6 — Block B 7-policy contest (H-Policy)")
    print("=" * 80)
    print(f"  {n} (config,size) cells")
    print(f"  P5 beats P0: {p5_v_p0:.2f}   P5 beats P1: {p5_v_p1:.2f}   "
          f"P5 beats P6: {p5_v_p6:.2f}   P5 beats P7: {p5_v_p7:.2f}")
    print(f"  P5 sits {100*p5_above_p7:.1f}% above the P7 local-search optimum")
    print(f"  H-Policy band: {band}")
    print("\n  win-fraction matrix (row beats column, fraction of cells):")
    hdr = "        " + " ".join(f"{p.split('_')[0]:>6s}" for p in allp)
    print(hdr)
    for i in allp:
        cellsr = " ".join(("   -  " if i == j
                           else f"{win[i][j]:6.2f}") for j in allp)
        print(f"  {i.split('_')[0]:>5s} {cellsr}")

    # mean makespan per policy (size-pooled, for the deliverable table)
    mean_med = {p: float(np.mean([c[p] for c in cells])) for p in allp}

    out = {
        "generated": "2026-05-19", "block": "B", "hypothesis": "H-Policy",
        "n_cells": n,
        "P5_vs_P0": p5_v_p0, "P5_vs_P1": p5_v_p1, "P5_vs_P6": p5_v_p6,
        "P5_vs_P7": p5_v_p7, "P5_above_P7_frac": p5_above_p7,
        "band": band,
        "win_matrix": win,
        "mean_median_makespan": mean_med,
        "per_cell": cells,
    }
    out_path = RESULTS_DIR / "v0_5_phase5_blockB.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved {out_path}")


if __name__ == "__main__":
    main()
