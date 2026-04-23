"""
MVS v0.2 Tier-1.5 B1 — Heterogeneous elevator pool.

Real multi-storey AMR warehouses typically mix freight and passenger
elevators with different capacities. v0.2 main experiments use
homogeneous pools (all elevators same cap). This experiment adds a
heterogeneous-pool simulator (ElevatorPoolBatchedHeterogeneous) and
tests:

  (1) M_2 dominance (Prop M5.1's assumption D): does batching dominance
      hold under heterogeneous capacities?
  (2) M4 GAP corner-argmin invariance: does the best corner under
      heterogeneous pool match the homogeneous baseline?
  (3) Wave-level makespan comparison: when does heterogeneity help vs hurt?

Design:
  - Homogeneous reference: E=3, cap=[2,2,2] (total capacity = 6)
  - Heterogeneous configs (matched total capacity 6-8):
      * cap=[2,2,2] (homogeneous, baseline)
      * cap=[1,2,3] (spread, same total)
      * cap=[2,3,3] (biased up, total=8)
      * cap=[1,3,4] (extreme spread, total=8)
  - 5 arms (random + 4 corners) x 200 waves at size = 6
  - 4 configs x 5 arms x 200 = 4 000 sims

Output: results/v0_2_B1_heterogeneous_pool.json
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
OUT_JSON = RESULTS_DIR / "v0_2_B1_heterogeneous_pool.json"

CONFIGS = [
    {"name": "homog_2-2-2", "capacities": [2, 2, 2], "total": 6},
    {"name": "hetero_1-2-3", "capacities": [1, 2, 3], "total": 6},
    {"name": "hetero_2-3-3", "capacities": [2, 3, 3], "total": 8},
    {"name": "hetero_1-3-4", "capacities": [1, 3, 4], "total": 8},
]
ARMS = ["random", "HC_HI", "HC_LI", "LC_HI", "LC_LI"]
SIZE = 6
N_PER_ARM = 200


def run_arm(waves_df: pd.DataFrame, capacities: List[int],
            order_pool, n_draw: int, seed: int) -> List[float]:
    rng = random.Random(seed)
    if len(waves_df) == 0:
        return []
    idxs = rng.choices(range(len(waves_df)), k=n_draw)
    mks = []
    for i in idxs:
        wave = materialise_wave(waves_df.iloc[i], order_pool)
        mk = simulate_wave(
            wave, n_amrs=N_AMRS,
            heterogeneous_capacities=capacities,
        )
        mks.append(mk)
    return mks


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    order_pool = build_order_pool(seed=43)

    print("=" * 110)
    print("B1 — Heterogeneous elevator pool")
    print("=" * 110)
    for c in CONFIGS:
        print(f"  {c['name']:18s}  capacities={c['capacities']}  total={c['total']}")
    print(f"\n  5 arms x 200 waves x 4 configs = {4 * 5 * N_PER_ARM} sims")

    cand = build_candidate_waves(SIZE, POOL_SIZE_PER_BAND, order_pool, seed=2026 + SIZE)
    arm_dfs = {
        "random": cand,
        "HC_HI": select_corner(cand, True, True),
        "HC_LI": select_corner(cand, True, False),
        "LC_HI": select_corner(cand, False, True),
        "LC_LI": select_corner(cand, False, False),
    }

    rows = []
    per_config = []
    t_total = time.time()

    for cfg in CONFIGS:
        print(f"\nConfig: {cfg['name']}  capacities={cfg['capacities']}")
        arm_med = {}
        for arm in ARMS:
            seed = hash((cfg["name"], arm, SIZE, "B1")) & 0x7fff
            mks = run_arm(arm_dfs[arm], cfg["capacities"], order_pool, N_PER_ARM, seed)
            arm_med[arm] = float(np.median(mks))
            for mk in mks:
                rows.append({
                    "config": cfg["name"],
                    "capacities": str(cfg["capacities"]),
                    "total_cap": cfg["total"],
                    "arm": arm, "makespan": mk,
                })
            print(f"  {arm:8s}  median={np.median(mks):7.2f}  mean={np.mean(mks):7.2f}")
        corner_med = {a: arm_med[a] for a in ARMS if a != "random"}
        gap = max(corner_med.values()) - min(corner_med.values())
        rand_med = arm_med["random"]
        gap_pct = 100.0 * gap / rand_med if rand_med > 0 else 0.0
        best = min(corner_med, key=corner_med.get)
        print(f"  best corner: {best}  GAP={gap:.2f} ({gap_pct:.2f}%)")
        per_config.append({
            "name": cfg["name"], "capacities": cfg["capacities"],
            "total_cap": cfg["total"],
            "arm_medians": arm_med, "GAP": gap, "GAP_pct": gap_pct,
            "best_corner": best,
            "random_median": rand_med,
        })

    df = pd.DataFrame(rows)
    raw_csv = RAW_DIR / "mvs_v0_2_B1_heterogeneous.csv"
    df.to_csv(raw_csv, index=False)

    print()
    print("=" * 110)
    print("Heterogeneous vs homogeneous comparison")
    print("=" * 110)
    baseline = per_config[0]  # homog_2-2-2
    print(f"{'config':18s}  {'total':>6s}  {'best':>6s}  {'GAP%':>6s}  "
          f"{'med_random':>10s}  {'Δ vs homog':>10s}")
    stability = []
    for cfg in per_config:
        delta = cfg["random_median"] - baseline["random_median"]
        stable = (cfg["best_corner"] == baseline["best_corner"])
        stability.append(stable)
        print(f"{cfg['name']:18s}  {cfg['total_cap']:>6d}  "
              f"{cfg['best_corner']:>6s}  {cfg['GAP_pct']:>5.2f}%  "
              f"{cfg['random_median']:>10.2f}  {delta:>+10.2f}")

    print()
    n_stable = sum(stability)
    print(f"Corner argmin stable vs homogeneous: {n_stable}/{len(per_config)} configs")
    if n_stable == len(per_config):
        verdict = ("HETEROGENEITY ROBUST — M4 best-corner identification invariant "
                   "across heterogeneous pool configurations; framework applies to "
                   "realistic AMR warehouse elevator mixes")
    elif n_stable >= len(per_config) - 1:
        verdict = ("MOSTLY ROBUST — 1 config shifts best corner; report per-pool "
                   "scope in §8")
    else:
        verdict = ("HETEROGENEITY-SENSITIVE — M4 corner ordering depends on pool "
                   "composition; requires pool-specific re-evaluation")
    print(f"Verdict: {verdict}")

    print(f"\nRuntime: {time.time() - t_total:.1f}s")

    out = {
        "generated": "2026-04-22",
        "purpose": "B1: heterogeneous elevator pool sensitivity",
        "configs": CONFIGS, "arms": ARMS, "size": SIZE, "n_per_arm": N_PER_ARM,
        "per_config": per_config,
        "summary": {
            "n_configs": len(per_config),
            "n_stable_argmin": n_stable,
            "verdict": verdict,
        },
    }
    OUT_JSON.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"Saved {OUT_JSON}")
    print(f"Saved {raw_csv}")


if __name__ == "__main__":
    main()
