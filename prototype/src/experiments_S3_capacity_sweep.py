"""
MVS v0.2 Tier-1.5 S3 — Capacity sweep c in {2, 3, 4, 5}.

Tests whether (a) the M_2 >= M_1 dominance assumption (Proposition M5.1's
core condition) extends beyond c=2, and (b) the Hedge Rule's corner-argmin
is invariant at higher capacities.

Design (R3-style matched-wave pairing):
  - Fix E = 2 (the middle regime)
  - Sweep c in {2, 3, 4, 5}
  - 5 arms (random + 4 corners), 200 waves per arm, size = 6
  - 4 capacities x 5 arms x 200 paired = 4 000 paired sims (8 000 total)

Per-capacity metrics:
  - P[M_2 >= M_1] across all waves
  - c*_{M_2} and c*_{M_1}: argmin of corner medians under each model
  - Argmin match: does M5 collapse rule hold?

Output: results/v0_2_S3_capacity_sweep.json
"""
from __future__ import annotations

import json
import random
import time
from pathlib import Path
from typing import List, Tuple

import numpy as np
import pandas as pd

from src.experiments_v0_2 import N_AMRS, build_order_pool
from src.experiments_phase4_v2 import (
    POOL_SIZE_PER_BAND,
    build_candidate_waves,
    materialise_wave,
    select_corner,
)
from src.simulator import simulate_wave

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RAW_DIR = RESULTS_DIR / "raw"
OUT_JSON = RESULTS_DIR / "v0_2_S3_capacity_sweep.json"

E_FIXED = 2
CAPACITIES = [2, 3, 4, 5]
ARMS = ["random", "HC_HI", "HC_LI", "LC_HI", "LC_LI"]
SIZE = 6
N_PER_ARM = 200


def run_arm_paired(waves_df: pd.DataFrame, E: int, cap: int,
                   order_pool, n_draw: int, seed: int) -> List[dict]:
    rng = random.Random(seed)
    if len(waves_df) == 0:
        return []
    idxs = rng.choices(range(len(waves_df)), k=n_draw)
    rows = []
    for i in idxs:
        wave = materialise_wave(waves_df.iloc[i], order_pool)
        m1 = simulate_wave(wave, n_amrs=N_AMRS, n_elevators=E, capacity=cap,
                           batched=False)
        m2 = simulate_wave(wave, n_amrs=N_AMRS, n_elevators=E, capacity=cap,
                           batched=True)
        rows.append({"m1": m1, "m2": m2})
    return rows


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    order_pool = build_order_pool(seed=43)

    print("=" * 110)
    print(f"S3 — capacity sweep for E = {E_FIXED}, sizes=[{SIZE}]")
    print(f"  Capacities: {CAPACITIES}; 5 arms x 200 paired sims = "
          f"{len(CAPACITIES) * 5 * N_PER_ARM * 2} total sims")
    print("=" * 110)

    cand = build_candidate_waves(SIZE, POOL_SIZE_PER_BAND, order_pool, seed=2026 + SIZE)
    arm_dfs = {
        "random": cand,
        "HC_HI": select_corner(cand, True, True),
        "HC_LI": select_corner(cand, True, False),
        "LC_HI": select_corner(cand, False, True),
        "LC_LI": select_corner(cand, False, False),
    }

    all_rows = []
    per_cap = []
    t_total = time.time()

    for cap in CAPACITIES:
        print(f"\ncapacity = {cap}")
        arm_m1_med = {}
        arm_m2_med = {}
        arm_dom = {}
        for arm in ARMS:
            seed = hash((E_FIXED, cap, arm, SIZE, "S3")) & 0x7fff
            paired = run_arm_paired(arm_dfs[arm], E_FIXED, cap, order_pool,
                                    N_PER_ARM, seed)
            m1 = np.array([r["m1"] for r in paired])
            m2 = np.array([r["m2"] for r in paired])
            dom = float((m2 >= m1).mean())
            arm_m1_med[arm] = float(np.median(m1))
            arm_m2_med[arm] = float(np.median(m2))
            arm_dom[arm] = dom
            for a, b in zip(m1, m2):
                all_rows.append({
                    "capacity": cap, "arm": arm, "m1": a, "m2": b,
                })
            print(f"  {arm:8s}  med_m1={np.median(m1):7.2f}  med_m2={np.median(m2):7.2f}  "
                  f"P[m2>=m1]={dom:.1%}")

        corner_m1 = {a: arm_m1_med[a] for a in ARMS if a != "random"}
        corner_m2 = {a: arm_m2_med[a] for a in ARMS if a != "random"}
        cstar_m1 = min(corner_m1, key=corner_m1.get)
        cstar_m2 = min(corner_m2, key=corner_m2.get)
        argmin_match = (cstar_m1 == cstar_m2)
        mean_dom = float(np.mean(list(arm_dom.values())))
        print(f"  c*_M1={cstar_m1}  c*_M2={cstar_m2}  "
              f"{'(MATCH)' if argmin_match else '(FLIP)'}  mean dom={mean_dom:.1%}")
        per_cap.append({
            "capacity": cap,
            "cstar_M1": cstar_m1, "cstar_M2": cstar_m2,
            "argmin_match": argmin_match,
            "mean_dominance_pct": mean_dom,
            "per_arm_dominance": arm_dom,
            "corner_medians_M1": corner_m1,
            "corner_medians_M2": corner_m2,
        })

    df = pd.DataFrame(all_rows)
    raw_csv = RAW_DIR / "mvs_v0_2_S3_capacity_sweep.csv"
    df.to_csv(raw_csv, index=False)

    print()
    print("=" * 110)
    print("Capacity-sweep summary")
    print("=" * 110)
    print(f"{'c':>3s}  {'c*_M1':>8s}  {'c*_M2':>8s}  {'argmin match':>12s}  "
          f"{'mean P[m2>=m1]':>14s}")
    n_match = 0
    for r in per_cap:
        print(f"{r['capacity']:>3d}  {r['cstar_M1']:>8s}  {r['cstar_M2']:>8s}  "
              f"{'YES' if r['argmin_match'] else 'no':>12s}  "
              f"{r['mean_dominance_pct']:>13.1%}")
        if r["argmin_match"]:
            n_match += 1

    overall_dom = float(np.mean([r["mean_dominance_pct"] for r in per_cap]))
    print()
    print(f"Argmin match: {n_match}/{len(per_cap)} capacities")
    print(f"Overall dominance: {overall_dom:.1%}")

    if overall_dom >= 0.95 and n_match == len(per_cap):
        verdict = ("CLEAN EXTENSION TO c>2 — M5.1 dominance (D) and Hedge Rule "
                   "argmin-invariance both hold across c in {2, 3, 4, 5}; closed-form "
                   "collapse generalises beyond the c=2 case")
    elif overall_dom >= 0.90 and n_match >= len(per_cap) - 1:
        verdict = ("STRONG EXTENSION — M5.1 dominance holds; argmin invariant in "
                   f"{n_match}/{len(per_cap)} capacities; report single-capacity "
                   "boundary in §8")
    else:
        verdict = ("SCOPE LIMIT — M5 framework requires c=2 scope statement")
    print(f"Verdict: {verdict}")
    print(f"\nRuntime: {time.time() - t_total:.1f}s")

    out = {
        "generated": "2026-04-22",
        "purpose": "S3: capacity sweep beyond c=2",
        "E_fixed": E_FIXED, "capacities": CAPACITIES, "size": SIZE,
        "n_per_arm": N_PER_ARM,
        "per_capacity": per_cap,
        "overall": {
            "n_argmin_match": n_match, "n_total": len(per_cap),
            "mean_dominance_pct": overall_dom, "verdict": verdict,
        },
    }
    OUT_JSON.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"Saved {OUT_JSON}")
    print(f"Saved {raw_csv}")


if __name__ == "__main__":
    main()
