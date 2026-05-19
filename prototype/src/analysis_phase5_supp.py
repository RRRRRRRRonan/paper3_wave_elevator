"""
MVS v0.5 Phase 5 — supplementary-experiment analysis (pre-reg §9.2 gates).

Supp-1 (C3-1, C3-3): H1 at publication scale — marginal value of clustering
  MV = (median T_fifo - median T_cluster) / median T_fifo, related to the
  Block A H_up (the elevator-lever headroom).
Supp-2 (C3-2): capacity sweep — per-wave M2 >= M1 at c in {2,3,4,5}.

Gates (pre-reg §9.2):
  Supp1-a  Pearson(H_up, MV) < 0 on the phi-corner arm
  Supp1-b  MV regime-conditional (MV > 1 % in a strict subset of cells)
  Supp2-a  per-wave M2>=M1 >= 90 % avg, >= 80 % worst, at each c in {3,4,5}

Output: results/v0_5_phase5_supp.json
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RAW = RESULTS_DIR / "raw"


def analyse_supp1() -> dict:
    df = pd.read_csv(RAW / "mvs_v0_5_supp1_h1scale.csv")
    blockA = json.loads((RESULTS_DIR / "v0_5_phase5_blockA.json")
                        .read_text(encoding="utf-8"))
    h_up = {(r["config_id"], r["size"]): r["H_up"]
            for r in blockA["per_subcell"] if r["model"] == "batched"}

    rows = []
    for (cid, size, arm), g in df.groupby(["config_id", "size", "arm"]):
        med_fifo = float(np.median(g[g["ops_policy"] == "fifo"]["makespan"]))
        med_clu = float(np.median(g[g["ops_policy"] == "cluster"]["makespan"]))
        mv = (med_fifo - med_clu) / med_fifo
        rows.append({"config_id": int(cid), "size": int(size), "arm": arm,
                     "median_fifo": med_fifo, "median_cluster": med_clu,
                     "MV": mv, "H_up": h_up.get((cid, size))})

    phi = [r for r in rows if r["arm"] == "phi_corner"]
    H = np.array([r["H_up"] for r in phi], float)
    MV = np.array([r["MV"] for r in phi], float)
    pearson = (float(np.corrcoef(H, MV)[0, 1])
               if np.std(H) > 0 and np.std(MV) > 0 else float("nan"))
    n_help = sum(r["MV"] > 0.01 for r in phi)
    supp1a = bool(pearson < 0)
    supp1b = bool(0 < n_help < len(phi))
    return {"per_cell": rows, "n_phi_cells": len(phi),
            "pearson_Hup_MV": pearson, "n_MV_gt_1pct": n_help,
            "mean_MV_phi": float(np.mean(MV)),
            "supp1a_pass": supp1a, "supp1b_pass": supp1b,
            "verdict": "PASS" if (supp1a and supp1b) else "PARTIAL"}


def analyse_supp2() -> dict:
    df = pd.read_csv(RAW / "mvs_v0_5_supp2_capacity.csv")
    cells = []
    for (cid, c, arm), g in df.groupby(["config_id", "capacity", "arm"]):
        pw = float(np.mean(g["makespan_M2"].to_numpy(float)
                           >= g["makespan_M1"].to_numpy(float)))
        cells.append({"config_id": int(cid), "capacity": int(c),
                      "arm": arm, "perwave_dom": pw})
    by_c = {}
    for c in sorted(df["capacity"].unique()):
        sub = [x["perwave_dom"] for x in cells if x["capacity"] == c]
        by_c[int(c)] = {"avg": float(np.mean(sub)),
                        "worst": float(np.min(sub)), "n_cells": len(sub)}
    supp2a = all(by_c[c]["avg"] >= 0.90 and by_c[c]["worst"] >= 0.80
                 for c in (3, 4, 5))
    return {"per_capacity": by_c, "per_cell": cells,
            "supp2a_pass": bool(supp2a),
            "verdict": "PASS" if supp2a else "PARTIAL"}


def main() -> None:
    s1 = analyse_supp1()
    s2 = analyse_supp2()

    print("=" * 78)
    print("Phase 5 supplementary analysis (pre-reg §9.2)")
    print("=" * 78)
    print("\nSupp-1  H1 at publication scale (C3-1, C3-3)")
    print(f"  phi-corner cells: {s1['n_phi_cells']}  "
          f"mean MV = {100*s1['mean_MV_phi']:+.2f} %")
    print(f"  Supp1-a  Pearson(H_up, MV) = {s1['pearson_Hup_MV']:+.3f}  "
          f"-> {'PASS' if s1['supp1a_pass'] else 'FAIL'} (gate < 0)")
    print(f"  Supp1-b  MV > 1 % in {s1['n_MV_gt_1pct']}/{s1['n_phi_cells']} "
          f"cells  -> {'PASS' if s1['supp1b_pass'] else 'FAIL'} "
          f"(regime-conditional)")
    print(f"  Supp-1 verdict: {s1['verdict']}")

    print("\nSupp-2  capacity sweep (C3-2)")
    for c, v in s2["per_capacity"].items():
        print(f"  c = {c}:  per-wave M2>=M1  avg = {v['avg']:.3f}  "
              f"worst = {v['worst']:.3f}  ({v['n_cells']} cells)")
    print(f"  Supp2-a  dominance >= 90%/80% at c in {{3,4,5}}: "
          f"{'PASS' if s2['supp2a_pass'] else 'FAIL'}")
    print(f"  Supp-2 verdict: {s2['verdict']}")

    out = {"generated": "2026-05-19",
           "purpose": "Phase 5 supplementary experiments for C3 "
                      "(pre-reg §9.2 amendment).",
           "Supp1_H1_at_scale": s1, "Supp2_capacity_sweep": s2}
    out_path = RESULTS_DIR / "v0_5_phase5_supp.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved {out_path}")


if __name__ == "__main__":
    main()
