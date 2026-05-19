"""
MVS v0.5 Phase 5 W6 — Block A decomposition analysis (Table 1, H-D1 gate).

Per (config, model, size) sub-cell of mvs_v0_5_phase5_blockA.csv (72 sub-cells)
computes the Bound-and-Gap decomposition GAP = H_up + M_Phi, the SPO-regret
equivalence, and a 95 % bootstrap CI on GAP. Evaluates pre-registered gates:

  D1-a  GAP = H_up + M_Phi  ==  UB - LB           (exact, 72/72)
  D1-b  H_up >= 0  and  M_Phi >= 0                (72/72)
  D1-c  M_Phi == SPO_regret(Phi predictor)        (exact, 72/72)
  D1-d  95 % bootstrap CI on GAP excludes 0       (>= 58/72, the real test)

Output: results/v0_5_phase5_blockA.json
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
CSV = RESULTS_DIR / "raw" / "mvs_v0_5_phase5_blockA.csv"
CORNERS = ["HC_HI", "HC_LI", "LC_HI", "LC_LI"]
N_BOOT = 1000
SEED = 20260519


def decompose(m_q: dict, m0: float, fav: str):
    q_max = max(m_q, key=m_q.get)
    q_min = min(m_q, key=m_q.get)
    H_up = (m_q[q_max] - m0) / m0
    M_phi = (m_q[fav] - m_q[q_min]) / m0
    UB = (m_q[q_max] - m_q[q_min]) / m0
    LB = (m0 - m_q[fav]) / m0
    return H_up, M_phi, UB, LB, q_max, q_min


def main() -> None:
    df = pd.read_csv(CSV)
    rng = np.random.default_rng(SEED)

    rows = []
    for (cid, model, size), g in df.groupby(["config_id", "model", "size"]):
        fav = g["favorable_corner"].iloc[0]
        arms = {c: g[g["arm"] == c]["makespan"].to_numpy(float) for c in CORNERS}
        rnd = g[g["arm"] == "random"]["makespan"].to_numpy(float)
        m_q = {c: float(np.median(arms[c])) for c in CORNERS}
        m0 = float(np.median(rnd))
        H_up, M_phi, UB, LB, qmax, qmin = decompose(m_q, m0, fav)
        GAP = H_up + M_phi
        spo = (m_q[fav] - m_q[qmin]) / m0          # SPO loss of the Phi predictor

        boot = np.empty(N_BOOT)
        for b in range(N_BOOT):
            mb = {c: float(np.median(rng.choice(arms[c], size=len(arms[c]),
                                                replace=True)))
                  for c in CORNERS}
            m0b = float(np.median(rng.choice(rnd, size=len(rnd), replace=True)))
            hb, mpb, _, _, _, _ = decompose(mb, m0b, fav)
            boot[b] = hb + mpb
        lo, hi = (float(x) for x in np.percentile(boot, [2.5, 97.5]))

        rows.append({
            "config_id": int(cid), "F": int(g["F"].iloc[0]),
            "n_amrs": int(g["n_amrs"].iloc[0]),
            "n_elevators": int(g["n_elevators"].iloc[0]),
            "demand": g["demand"].iloc[0], "model": model, "size": int(size),
            "H_up": H_up, "M_Phi": M_phi, "GAP": GAP, "SPO_regret": spo,
            "gap_ci_lo": lo, "gap_ci_hi": hi,
            "d1a": bool(abs(GAP - (UB - LB)) < 1e-9),
            "d1b": bool(H_up >= -1e-12 and M_phi >= -1e-12),
            "d1c": bool(abs(M_phi - spo) < 1e-12),
            "d1d": bool(lo > 0.0),
        })

    n = len(rows)
    g_a = sum(r["d1a"] for r in rows)
    g_b = sum(r["d1b"] for r in rows)
    g_c = sum(r["d1c"] for r in rows)
    g_d = sum(r["d1d"] for r in rows)
    d1d_thresh = int(np.ceil(0.80 * n))
    verdict = ("PASS" if (g_a == n and g_b == n and g_c == n
                          and g_d >= d1d_thresh) else "PARTIAL")

    # surprise-log hook: does GAP fall as F grows?
    Fs = np.array([r["F"] for r in rows], float)
    GAPs = np.array([r["GAP"] for r in rows], float)
    gap_F_corr = float(np.corrcoef(Fs, GAPs)[0, 1])

    print("=" * 80)
    print("Phase 5 W6 — Block A decomposition (H-D1)")
    print("=" * 80)
    print(f"  sub-cells: {n}")
    print(f"  D1-a GAP=H_up+M_Phi exact:        {g_a}/{n}")
    print(f"  D1-b H_up>=0, M_Phi>=0:           {g_b}/{n}")
    print(f"  D1-c M_Phi==SPO_regret exact:     {g_c}/{n}")
    print(f"  D1-d GAP 95% CI excludes 0:       {g_d}/{n}  "
          f"(gate >= {d1d_thresh})")
    print(f"  H-D1 verdict:                     {verdict}")
    print(f"  mean GAP={np.mean(GAPs):.4f}  mean H_up="
          f"{np.mean([r['H_up'] for r in rows]):.4f}  "
          f"mean M_Phi={np.mean([r['M_Phi'] for r in rows]):.4f}")
    print(f"  surprise hook corr(F, GAP) = {gap_F_corr:+.3f}")

    # per-demand aggregate
    print("\n  per-demand mean GAP / D1-d pass rate:")
    by_demand = {}
    for dem in ["uniform", "clustered", "diurnal"]:
        sub = [r for r in rows if r["demand"] == dem]
        mg = float(np.mean([r["GAP"] for r in sub]))
        dd = sum(r["d1d"] for r in sub)
        by_demand[dem] = {"mean_GAP": mg, "n": len(sub), "d1d_pass": dd}
        print(f"    {dem:10s} mean GAP={mg:.4f}  D1-d {dd}/{len(sub)}")

    out = {
        "generated": "2026-05-19", "block": "A", "hypothesis": "H-D1",
        "n_subcells": n,
        "gates": {"D1a": g_a, "D1b": g_b, "D1c": g_c, "D1d": g_d,
                  "D1d_threshold": d1d_thresh},
        "verdict": verdict,
        "mean_GAP": float(np.mean(GAPs)),
        "corr_F_GAP": gap_F_corr,
        "by_demand": by_demand,
        "per_subcell": rows,
    }
    out_path = RESULTS_DIR / "v0_5_phase5_blockA.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved {out_path}")


if __name__ == "__main__":
    main()
