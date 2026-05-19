"""
MVS v0.5 Phase 5 — smoke-test verdict (pre-registration §7 gate S1-S4).

Reads the smoke-slice CSVs produced by `experiments_phase5.py smoke` and
evaluates the four directional checks that gate the full confirmatory run:

  S1 decomposition non-degenerate — GAP > 0 in >= 2/3 smoke configs
  S2 dominance direction          — batched >= abstraction (median proxy) in
                                     >= 80 % of (config, arm) cells
  S3 policy direction             — P5 median makespan <= P0 in >= 2/3 configs
  S4 demand patterns bite         — clustered or diurnal differs from uniform
                                     median makespan by >= 3 % (dedicated
                                     fixed-(F,|A|) mini-run)

Verdict PROCEED iff S1-S4 all pass; otherwise STOP — a legitimate pre-reg
pivot (revise the failing component, re-smoke; do not launch the full grid).

S2 note: the smoke Block A draws abstraction / batched on independent wave
samples, so S2 is a distributional (median) proxy here; the per-wave
dominance gate D2-a is evaluated on the matched-wave Block C at full scale.

Output:
  results/v0_5_phase5_smoke_verdict.json
"""
from __future__ import annotations

import json
import random
from pathlib import Path

import numpy as np
import pandas as pd

from src import phase5_config as cfg
from src.demand_patterns import generate_pool
from src.simulator import simulate_wave
from src.wave_policies import build_candidates, materialise

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RAW_DIR = RESULTS_DIR / "raw"
CORNERS = ["HC_HI", "HC_LI", "LC_HI", "LC_LI"]


def _median(df, **filt):
    sub = df
    for k, v in filt.items():
        sub = sub[sub[k] == v]
    return float(np.median(sub["makespan"])) if len(sub) else float("nan")


def check_s1(dfA: pd.DataFrame) -> dict:
    """GAP = H_up + M_Phi > 0 per smoke config (batched model)."""
    rows = []
    for cid in sorted(dfA["config_id"].unique()):
        sub = dfA[(dfA["config_id"] == cid) & (dfA["model"] == "batched")]
        if len(sub) == 0:
            continue
        m_q = {c: _median(sub, arm=c) for c in CORNERS}
        m_0 = _median(sub, arm="random")
        fav = sub["favorable_corner"].iloc[0]
        q_max = max(m_q, key=m_q.get)
        q_min = min(m_q, key=m_q.get)
        H_up = (m_q[q_max] - m_0) / m_0
        M_phi = (m_q[fav] - m_q[q_min]) / m_0
        gap = H_up + M_phi
        rows.append({"config_id": int(cid), "H_up": H_up, "M_Phi": M_phi,
                     "GAP": gap, "gap_positive": bool(gap > 1e-9)})
    n_pos = sum(r["gap_positive"] for r in rows)
    return {"per_config": rows, "n_gap_positive": n_pos, "n_configs": len(rows),
            "pass": bool(n_pos >= np.ceil(2 / 3 * len(rows)))}


def check_s2(dfA: pd.DataFrame) -> dict:
    """Distributional proxy: median(batched) >= median(abstraction) per (config, arm)."""
    rows = []
    for cid in sorted(dfA["config_id"].unique()):
        for arm in ["random"] + CORNERS:
            mb = _median(dfA[dfA["config_id"] == cid], model="batched", arm=arm)
            ma = _median(dfA[dfA["config_id"] == cid], model="abstraction",
                         arm=arm)
            rows.append({"config_id": int(cid), "arm": arm,
                         "median_batched": mb, "median_abstraction": ma,
                         "dominates": bool(mb >= ma - 1e-9)})
    n_dom = sum(r["dominates"] for r in rows)
    return {"per_cell": rows, "n_dominates": n_dom, "n_cells": len(rows),
            "frac": n_dom / len(rows), "pass": n_dom / len(rows) >= 0.80}


def check_s3(dfB: pd.DataFrame) -> dict:
    """P5 (phi) median makespan <= P0 (random) per smoke config."""
    rows = []
    for cid in sorted(dfB["config_id"].unique()):
        sub = dfB[dfB["config_id"] == cid]
        m_p5 = _median(sub, policy="P5_phi")
        m_p0 = _median(sub, policy="P0_random")
        rows.append({"config_id": int(cid), "median_P5": m_p5,
                     "median_P0": m_p0, "P5_le_P0": bool(m_p5 <= m_p0 + 1e-9)})
    n_ok = sum(r["P5_le_P0"] for r in rows)
    return {"per_config": rows, "n_P5_beats_P0": n_ok, "n_configs": len(rows),
            "pass": bool(n_ok >= np.ceil(2 / 3 * len(rows)))}


def check_s4(seed: int = 999) -> dict:
    """Dedicated fixed-(F,|A|) mini-run: do clustered / diurnal shift makespan?"""
    F, A, E, size, n_waves = 5, 15, 2, 8, 80
    meds = {}
    for pat in ["uniform", "clustered", "diurnal"]:
        pool = generate_pool(pat, F, cfg.ORDER_POOL_SIZE, seed=seed,
                             **cfg.DEMAND_PARAMS[pat])
        cand = build_candidates(pool, size, 400, random.Random(seed + 1))
        rng = random.Random(seed + 2)
        mks = [simulate_wave(materialise(cand.iloc[rng.randrange(len(cand))],
                                         pool),
                             n_amrs=A, n_elevators=E, capacity=cfg.CAPACITY,
                             batched=True, rng=rng)
               for _ in range(n_waves)]
        meds[pat] = float(np.median(mks))
    uni = meds["uniform"]
    diffs = {p: abs(meds[p] - uni) / uni for p in ("clustered", "diurnal")}
    return {"median_makespan": meds, "rel_diff_vs_uniform": diffs,
            "max_rel_diff": max(diffs.values()),
            "pass": max(diffs.values()) >= 0.03}


def main() -> None:
    dfA = pd.read_csv(RAW_DIR / "mvs_v0_5_phase5_smoke_blockA.csv")
    dfB = pd.read_csv(RAW_DIR / "mvs_v0_5_phase5_smoke_blockB.csv")

    s1 = check_s1(dfA)
    s2 = check_s2(dfA)
    s3 = check_s3(dfB)
    s4 = check_s4()

    print("=" * 78)
    print("Phase 5 SMOKE verdict — pre-registration §7 gate")
    print("=" * 78)

    print("\nS1  decomposition non-degenerate (GAP > 0, >= 2/3 configs)")
    for r in s1["per_config"]:
        print(f"    config {r['config_id']:2d}:  H_up={r['H_up']:+.4f}  "
              f"M_Phi={r['M_Phi']:+.4f}  GAP={r['GAP']:+.4f}  "
              f"{'OK' if r['gap_positive'] else 'degenerate'}")
    print(f"    -> {s1['n_gap_positive']}/{s1['n_configs']}  "
          f"{'PASS' if s1['pass'] else 'FAIL'}")

    print("\nS2  dominance direction (median batched >= abstraction, >= 80 %)")
    print(f"    -> {s2['n_dominates']}/{s2['n_cells']} cells "
          f"({100*s2['frac']:.0f} %)  {'PASS' if s2['pass'] else 'FAIL'}")

    print("\nS3  policy direction (P5 median <= P0, >= 2/3 configs)")
    for r in s3["per_config"]:
        print(f"    config {r['config_id']:2d}:  P5={r['median_P5']:.1f}  "
              f"P0={r['median_P0']:.1f}  "
              f"{'P5 wins' if r['P5_le_P0'] else 'P0 wins'}")
    print(f"    -> {s3['n_P5_beats_P0']}/{s3['n_configs']}  "
          f"{'PASS' if s3['pass'] else 'FAIL'}")

    print("\nS4  demand patterns bite (clustered/diurnal vs uniform >= 3 %)")
    for p, d in s4["rel_diff_vs_uniform"].items():
        print(f"    {p:9s}: median {s4['median_makespan'][p]:.1f}  "
              f"({100*d:+.1f} % vs uniform {s4['median_makespan']['uniform']:.1f})")
    print(f"    -> max {100*s4['max_rel_diff']:.1f} %  "
          f"{'PASS' if s4['pass'] else 'FAIL'}")

    gates = {"S1": s1["pass"], "S2": s2["pass"], "S3": s3["pass"],
             "S4": s4["pass"]}
    verdict = "PROCEED" if all(gates.values()) else "STOP"
    print("\n" + "=" * 78)
    print(f"SMOKE GATE: {verdict}   "
          + "  ".join(f"{k}={'pass' if v else 'FAIL'}"
                      for k, v in gates.items()))
    if verdict == "STOP":
        print("Pre-reg §8 stop rule 1: revise the failing component and "
              "re-smoke; do NOT launch the full grid.")
    else:
        print("Pre-reg §8 stop rule 2: full run may launch after the §10 "
              "author sign-off.")
    print("=" * 78)

    out = {
        "generated": "2026-05-19",
        "purpose": "Phase 5 smoke-test verdict against pre-registration §7.",
        "S1_decomposition": s1,
        "S2_dominance": s2,
        "S3_policy_direction": s3,
        "S4_demand_bite": s4,
        "gates": gates,
        "verdict": verdict,
    }
    out_path = RESULTS_DIR / "v0_5_phase5_smoke_verdict.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved {out_path}")


if __name__ == "__main__":
    main()
