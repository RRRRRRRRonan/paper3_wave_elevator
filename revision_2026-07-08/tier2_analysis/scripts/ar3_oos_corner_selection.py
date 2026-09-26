"""
Amendment A-R3 (2026-07-08): out-of-sample evaluation of the corner selection
inside M_Phi (and H_up). Reanalysis ONLY.

Input: raw/mvs_v0_5_phase5_blockA.csv (72 sub-cells x 5 arms x 200 waves).

Per sub-cell: split each arm's waves 50/50 (seed 20260708). On the TRAIN half
determine q_min_train (argmin of corner medians) and q_max_train (argmax).
On the TEST half evaluate:
  M_Phi_oos = (m_test[q_phi] - m_test[q_min_train]) / m0_test
  H_up_oos  = (m_test[q_max_train] - m0_test) / m0_test
q_phi = stored favorable_corner (fixed ex ante, NOT refit).
In-sample values recomputed on the full sample (match the stored artefact).

Locked reporting rule (amendment A-R3): report both directions; if mean M_Phi
shrinks > 25% relative, section 5 quotes the out-of-sample value alongside.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "prototype" / "results" / "raw"
OUT = Path(__file__).resolve().parents[1] / "outputs"
SEED = 20260708
CORNERS = ["HC_HI", "HC_LI", "LC_HI", "LC_LI"]


def main() -> None:
    rng = np.random.default_rng(SEED)
    df = pd.read_csv(RAW / "mvs_v0_5_phase5_blockA.csv")

    rows = []
    for (cid, model, size), g in df.groupby(["config_id", "model", "size"]):
        fav = g["favorable_corner"].iloc[0]
        tr, te = {}, {}
        for arm in CORNERS + ["random"]:
            x = g[g["arm"] == arm]["makespan"].to_numpy(float)
            perm = rng.permutation(len(x))
            half = len(x) // 2
            tr[arm], te[arm] = x[perm[:half]], x[perm[half:]]

        # in-sample (full sample, matches stored artefact)
        m_q = {c: float(np.median(g[g["arm"] == c]["makespan"]))
               for c in CORNERS}
        m0 = float(np.median(g[g["arm"] == "random"]["makespan"]))
        q_min_in = min(m_q, key=m_q.get)
        q_max_in = max(m_q, key=m_q.get)
        H_in = (m_q[q_max_in] - m0) / m0
        M_in = (m_q[fav] - m_q[q_min_in]) / m0

        # train-fit, test-evaluate
        mtr = {c: float(np.median(tr[c])) for c in CORNERS}
        q_min_tr = min(mtr, key=mtr.get)
        q_max_tr = max(mtr, key=mtr.get)
        mte = {c: float(np.median(te[c])) for c in CORNERS}
        m0te = float(np.median(te["random"]))
        M_oos = (mte[fav] - mte[q_min_tr]) / m0te
        H_oos = (mte[q_max_tr] - m0te) / m0te
        q_min_te = min(mte, key=mte.get)
        q_max_te = max(mte, key=mte.get)

        rows.append({
            "config_id": int(cid), "model": model, "size": int(size),
            "M_Phi_in": M_in, "M_Phi_oos": M_oos,
            "H_up_in": H_in, "H_up_oos": H_oos,
            "GAP_in": H_in + M_in, "GAP_oos": H_oos + M_oos,
            "qmin_train_neq_test": bool(q_min_tr != q_min_te),
            "qmax_train_neq_test": bool(q_max_tr != q_max_te),
        })

    mM_in = float(np.mean([r["M_Phi_in"] for r in rows]))
    mM_oos = float(np.mean([r["M_Phi_oos"] for r in rows]))
    mH_in = float(np.mean([r["H_up_in"] for r in rows]))
    mH_oos = float(np.mean([r["H_up_oos"] for r in rows]))
    shrink_M = (mM_in - mM_oos) / mM_in if mM_in else float("nan")
    shrink_H = (mH_in - mH_oos) / mH_in if mH_in else float("nan")
    n_qmin_flip = sum(r["qmin_train_neq_test"] for r in rows)
    n_qmax_flip = sum(r["qmax_train_neq_test"] for r in rows)
    n_M_neg = sum(r["M_Phi_oos"] < 0 for r in rows)

    out = {
        "amendment": "A-R3", "date_executed": "2026-07-08", "seed": SEED,
        "note": ("q_phi (favorable_corner) fixed ex ante and NOT refit; the "
                 "data-fitted objects are q_min/q_max. Negative M_Phi_oos "
                 "means the train-selected oracle corner was not the test "
                 "argmin (winner's-curse correction)."),
        "mean_M_Phi_in": mM_in, "mean_M_Phi_oos": mM_oos,
        "rel_shrink_M_Phi": shrink_M,
        "mean_H_up_in": mH_in, "mean_H_up_oos": mH_oos,
        "rel_shrink_H_up": shrink_H,
        "n_qmin_train_neq_test": n_qmin_flip,
        "n_qmax_train_neq_test": n_qmax_flip,
        "n_M_Phi_oos_negative": n_M_neg,
        "materially_different_M_Phi": bool(abs(shrink_M) > 0.25),
        "capacity_share_in": mH_in / (mH_in + mM_in),
        "capacity_share_oos": mH_oos / (mH_oos + mM_oos),
        "per_subcell": rows,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "ar3_oos_corner_selection.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)

    print("A-R3 out-of-sample corner-selection evaluation (72 sub-cells)")
    print(f"  mean M_Phi  in-sample {mM_in:.4f}  ->  OOS {mM_oos:.4f}  "
          f"(rel shrink {100*shrink_M:+.1f}%)")
    print(f"  mean H_up   in-sample {mH_in:.4f}  ->  OOS {mH_oos:.4f}  "
          f"(rel shrink {100*shrink_H:+.1f}%)")
    print(f"  q_min train!=test in {n_qmin_flip}/72, q_max in {n_qmax_flip}/72; "
          f"M_Phi_oos < 0 in {n_M_neg}/72")
    print(f"  capacity share: in-sample {out['capacity_share_in']:.3f}  "
          f"OOS {out['capacity_share_oos']:.3f}")
    print(f"  materially different (>25% rule): "
          f"{out['materially_different_M_Phi']}")
    print(f"\nSaved {path}")


if __name__ == "__main__":
    main()
