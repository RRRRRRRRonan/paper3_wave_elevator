"""
Amendment A-R1 (2026-07-08): partition-sensitivity of the capacity-share reading.

Reanalysis ONLY. Inputs (existing artefacts):
  prototype/results/raw/mvs_v0_5_phase5_ablation_scheme.csv   (A4 data: 6 configs,
      size 16, model M2, schemes 2x2_CI / 3x3_CI / 2x2x2_CIT, each with its own
      200-wave random arm)
  prototype/results/raw/mvs_v0_5_phase5_blockA.csv             (72 sub-cells, 2x2)

Per (config, scheme):
  m_0   = median makespan of the scheme's random arm
  m_q   = median makespan per corner
  H_up  = (m_qmax - m_0) / m_0        structural ceiling (partition-intrinsic)
  S_or  = (m_0 - m_qmin) / m_0        oracle-recoverable slack (partition-intrinsic)
  UB    = H_up + S_or
  capacity share = H_up / UB

Reference (2x2 only, Block A): Phi-rule share H_up / (H_up + M_Phi).

Locked decision rule (amendment A-R1): headline kept only if H_up/UB > 0.5 in
>= 5/6 configs under EVERY stored scheme.

Bootstrap: 1000 reps, seed 20260708, percentile 95% CI on the capacity share.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
RESULTS = ROOT / "prototype" / "results"
OUT = Path(__file__).resolve().parents[1] / "outputs"
SEED = 20260708
N_BOOT = 1000

CORNERS_2X2 = ["HC_HI", "HC_LI", "LC_HI", "LC_LI"]


def shares(m_q: dict, m0: float):
    q_max = max(m_q, key=m_q.get)
    q_min = min(m_q, key=m_q.get)
    H_up = (m_q[q_max] - m0) / m0
    S_or = (m0 - m_q[q_min]) / m0
    UB = H_up + S_or
    cap = H_up / UB if UB > 0 else float("nan")
    return H_up, S_or, UB, cap, q_max, q_min


def main() -> None:
    rng = np.random.default_rng(SEED)
    df = pd.read_csv(RESULTS / "raw" / "mvs_v0_5_phase5_ablation_scheme.csv")

    rows = []
    for (cid, scheme), g in df.groupby(["config_id", "scheme"]):
        corners = sorted(c for c in g["corner"].unique() if c != "random")
        arms = {c: g[g["corner"] == c]["makespan"].to_numpy(float)
                for c in corners}
        rnd = g[g["corner"] == "random"]["makespan"].to_numpy(float)
        m_q = {c: float(np.median(arms[c])) for c in corners}
        m0 = float(np.median(rnd))
        H_up, S_or, UB, cap, qmax, qmin = shares(m_q, m0)

        boot = np.empty(N_BOOT)
        for b in range(N_BOOT):
            mb = {c: float(np.median(rng.choice(arms[c], len(arms[c]))))
                  for c in corners}
            m0b = float(np.median(rng.choice(rnd, len(rnd))))
            _, _, ubb, capb, _, _ = shares(mb, m0b)
            boot[b] = capb
        lo, hi = (float(x) for x in np.nanpercentile(boot, [2.5, 97.5]))

        rows.append({
            "config_id": int(cid), "scheme": scheme, "n_corners": len(corners),
            "m0": m0, "H_up": H_up, "S_oracle": S_or, "UB": UB,
            "capacity_share": cap, "cap_ci_lo": lo, "cap_ci_hi": hi,
            "q_max": qmax, "q_min": qmin,
            "capacity_dominant": bool(cap > 0.5),
        })

    # decision rule per scheme
    schemes = sorted({r["scheme"] for r in rows})
    rule = {}
    for s in schemes:
        sub = [r for r in rows if r["scheme"] == s]
        n_dom = sum(r["capacity_dominant"] for r in sub)
        rule[s] = {"n_configs": len(sub), "n_capacity_dominant": n_dom,
                   "meets_5_of_6": bool(n_dom >= 5)}
    headline_survives = all(v["meets_5_of_6"] for v in rule.values())

    # reference: Phi-rule-based share on the same 6 configs (Block A, 2x2,
    # model=batched to match the ablation's M2; both sizes) and the full
    # 72-sub-cell mean shares
    dfa = pd.read_csv(RESULTS / "raw" / "mvs_v0_5_phase5_blockA.csv")
    ref_rows = []
    for (cid, model, size), g in dfa.groupby(["config_id", "model", "size"]):
        fav = g["favorable_corner"].iloc[0]
        m_q = {c: float(np.median(g[g["arm"] == c]["makespan"]))
               for c in CORNERS_2X2}
        m0 = float(np.median(g[g["arm"] == "random"]["makespan"]))
        q_max = max(m_q, key=m_q.get)
        q_min = min(m_q, key=m_q.get)
        H_up = (m_q[q_max] - m0) / m0
        M_phi = (m_q[fav] - m_q[q_min]) / m0
        gap = H_up + M_phi
        ref_rows.append({
            "config_id": int(cid), "model": model, "size": int(size),
            "H_up": H_up, "M_Phi": M_phi, "GAP": gap,
            "phi_rule_capacity_share": H_up / gap if gap > 0 else float("nan"),
        })
    mean_H = float(np.mean([r["H_up"] for r in ref_rows]))
    mean_M = float(np.mean([r["M_Phi"] for r in ref_rows]))

    out = {
        "amendment": "A-R1", "date_executed": "2026-07-08",
        "seed": SEED, "n_boot": N_BOOT,
        "note": ("Schemes from stored A4 ablation data (6 configs, size 16, "
                 "M2). Terciles are OUT OF SCOPE (no stored data; amendment "
                 "B-6). capacity_share = H_up/UB is partition-intrinsic; the "
                 "Phi-rule share H_up/(H_up+M_Phi) is only defined for the "
                 "2x2 scheme where favorable_corner exists."),
        "per_config_scheme": rows,
        "decision_rule": rule,
        "headline_survives_all_schemes": headline_survives,
        "blockA_reference": {
            "mean_H_up_72subcells": mean_H, "mean_M_Phi_72subcells": mean_M,
            "phi_rule_capacity_share_of_mean_GAP": mean_H / (mean_H + mean_M),
            "per_subcell": ref_rows,
        },
    }
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "ar1_partition_sensitivity.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)

    print("A-R1 partition sensitivity (capacity share = H_up/UB)")
    print(f"{'config':>6} {'scheme':>10} {'H_up':>7} {'S_or':>7} "
          f"{'share':>6} {'95% CI':>16} {'dom':>4}")
    for r in sorted(rows, key=lambda r: (r["scheme"], r["config_id"])):
        print(f"{r['config_id']:>6} {r['scheme']:>10} {r['H_up']:>7.3f} "
              f"{r['S_oracle']:>7.3f} {r['capacity_share']:>6.2f} "
              f"[{r['cap_ci_lo']:>5.2f}, {r['cap_ci_hi']:>5.2f}] "
              f"{'yes' if r['capacity_dominant'] else 'NO':>4}")
    print("\ndecision rule per scheme (capacity-dominant in >=5/6 configs):")
    for s, v in rule.items():
        print(f"  {s:>10}: {v['n_capacity_dominant']}/{v['n_configs']} "
              f"-> {'MEETS' if v['meets_5_of_6'] else 'FAILS'}")
    print(f"\nheadline survives all schemes: {headline_survives}")
    print(f"Block A 72-sub-cell Phi-rule share of mean GAP: "
          f"{mean_H/(mean_H+mean_M):.3f} (H_up {mean_H:.4f} / M_Phi {mean_M:.4f})")
    print(f"\nSaved {path}")


if __name__ == "__main__":
    main()
