"""
MVS v0.2 Phase 4 H1 — Full pre-registered P0 vs P1 experiment (14400 sims).

Pre-reg H1: destination-clustered batching (P1) reduces mean makespan vs
FIFO (P0) in regimes where the elevator lever dominates (E2_c2, E3_c2 per
M4 empirical), especially on Phi-favorable waves.

Design:
  - 3 regimes (E1_c2, E2_c2, E3_c2) x 2 elevator models (abstraction, batched)
    = 6 cells
  - 3 size bands (4, 6, 8)
  - 2 policies (P0 = fifo, P1 = cluster)
  - 2 arms (random, favorable-corner from Phi-advice)
  - 200 waves per (cell x size x policy x arm)
  => 3 * 2 * 3 * 2 * 2 * 200 = 14400 sims

Reuses candidate-wave pool and corner selection from Phase 4 v2 for
compatibility with M4 diagnostic numbers already in the paper.

Output: results/raw/mvs_v0_2_phase4_H1_samples.csv
"""
from __future__ import annotations

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
    favorable_corner,
    load_betas,
    materialise_wave,
    select_corner,
)
from src.simulator import simulate_wave

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RAW_DIR = RESULTS_DIR / "raw"

REGIMES = [(1, 2), (2, 2), (3, 2)]
ELEVATOR_MODELS = ["abstraction", "batched"]
SIZE_BANDS = [4, 6, 8]
POLICIES = ["fifo", "cluster"]
ARMS = ["random", "favorable"]
N_PER_ARM = 200


def run_arm(waves_df: pd.DataFrame, regime: Tuple[int, int], model: str,
            policy: str, order_pool, n_draw: int, seed: int) -> List[float]:
    rng = random.Random(seed)
    if len(waves_df) == 0:
        return []
    idxs = rng.choices(range(len(waves_df)), k=n_draw)
    E, cap = regime
    batched = (model == "batched")
    makespans = []
    for i in idxs:
        wave = materialise_wave(waves_df.iloc[i], order_pool)
        mk = simulate_wave(
            wave,
            n_amrs=N_AMRS,
            n_elevators=E,
            capacity=cap,
            batched=batched,
            policy=policy,
        )
        makespans.append(mk)
    return makespans


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    order_pool = build_order_pool(seed=43)
    betas = load_betas()

    total_sims = 3 * 2 * 3 * 2 * 2 * N_PER_ARM
    print("=" * 100)
    print(f"Phase 4 H1 FULL EXPERIMENT — {total_sims} sims")
    print("=" * 100)
    print(f"  6 cells (3 regimes x 2 models) x 3 sizes x 2 policies x 2 arms "
          f"x {N_PER_ARM} waves")
    print()

    # Build candidate pool per size + favorable corner per cell
    print("Building candidate pools per size...")
    pool_per_size = {}
    for size in SIZE_BANDS:
        pool_per_size[size] = build_candidate_waves(
            size, POOL_SIZE_PER_BAND, order_pool, seed=2026 + size)
        print(f"  size={size}: {len(pool_per_size[size])} candidate waves")

    print()
    print("Running arms...")
    rows = []
    t_total = time.time()

    for E, cap in REGIMES:
        regime_str = f"E{E}_c{cap}"
        for model in ELEVATOR_MODELS:
            beta_C = betas[(regime_str, model)]["C"]
            beta_I = betas[(regime_str, model)]["I"]
            fav_c_hi, fav_i_hi = favorable_corner(beta_C, beta_I)
            fav_label = ("HC" if fav_c_hi else "LC") + "_" + \
                        ("HI" if fav_i_hi else "LI")

            for size in SIZE_BANDS:
                cand = pool_per_size[size]
                fav_df = select_corner(cand, fav_c_hi, fav_i_hi)
                t0 = time.time()

                for policy in POLICIES:
                    for arm in ARMS:
                        arm_df = cand if arm == "random" else fav_df
                        seed = hash(
                            (E, cap, model, size, arm, policy)) & 0x7fff
                        mks = run_arm(arm_df, (E, cap), model, policy,
                                      order_pool, N_PER_ARM, seed)
                        for mk in mks:
                            rows.append({
                                "regime": regime_str,
                                "model": model,
                                "size": size,
                                "policy": policy,
                                "arm": arm,
                                "favorable_corner": fav_label,
                                "makespan": mk,
                            })

                el = time.time() - t0
                print(f"  {regime_str:6s} {model:11s} size={size}: "
                      f"fav={fav_label}  beta_C={beta_C:+.2f} "
                      f"beta_I={beta_I:+.2f}  ({el:.1f}s)")

    df = pd.DataFrame(rows)
    out_csv = RAW_DIR / "mvs_v0_2_phase4_H1_samples.csv"
    df.to_csv(out_csv, index=False)
    print()
    print(f"Total runtime: {time.time() - t_total:.1f}s")
    print(f"Saved {len(df)} rows to {out_csv}")


if __name__ == "__main__":
    main()
