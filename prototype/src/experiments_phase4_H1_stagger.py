"""
MVS v0.2 Phase 4 H1 — P0 vs P1 under non-trivial T-stagger (Gap 2 cross-check).

Re-runs the full 14 400-simulation H1 experiment with per-order release_time
drawn from a lognormal inter-arrival process at CV = 0.5 (Appendix A.2 shows
the M4 corner-argmin is stable for the majority of cells at this CV). Tests
whether the H1 "tactical-operational substitutability map" from T=0 survives
T > 0, i.e. whether destination-clustered batching (P1) still beats FIFO
(P0) precisely in the elevator-lever-dominated cells under realistic order
arrival patterns.

Design mirrors experiments_phase4_H1.py:
  - 3 regimes x 2 models x 3 sizes x 2 policies x 2 arms x 200 waves
  - stagger CV = 0.5 applied to each wave before simulation
  - 14 400 sims

Output: results/raw/mvs_v0_2_phase4_H1_stagger_samples.csv
"""
from __future__ import annotations

import math
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
    select_corner,
)
from src.simulator import Order, Wave, simulate_wave

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RAW_DIR = RESULTS_DIR / "raw"

REGIMES = [(1, 2), (2, 2), (3, 2)]
ELEVATOR_MODELS = ["abstraction", "batched"]
SIZE_BANDS = [4, 6, 8]
POLICIES = ["fifo", "cluster"]
ARMS = ["random", "favorable"]
N_PER_ARM = 200
STAGGER_CV = 0.5


def lognormal_sigma_for_cv(cv: float) -> float:
    return math.sqrt(math.log(1.0 + cv * cv)) if cv > 0 else 0.0


def stagger_orders(orders: List[Order], cv: float, rng: random.Random) -> List[Order]:
    if cv <= 0:
        return [Order(o.id, o.source_floor, o.dest_floor, release_time=0.0)
                for o in orders]
    sigma = lognormal_sigma_for_cv(cv)
    mu = -0.5 * sigma * sigma
    t = 0.0
    out = []
    for o in orders:
        t += math.exp(rng.gauss(mu, sigma))
        out.append(Order(o.id, o.source_floor, o.dest_floor, release_time=t))
    return out


def run_arm(waves_df: pd.DataFrame, regime: Tuple[int, int], model: str,
            policy: str, order_pool: List[Order], n_draw: int,
            cv: float, seed: int) -> List[float]:
    rng = random.Random(seed)
    if len(waves_df) == 0:
        return []
    idxs = rng.choices(range(len(waves_df)), k=n_draw)
    E, cap = regime
    batched = (model == "batched")
    mks = []
    for i in idxs:
        base = [order_pool[j] for j in waves_df.iloc[i]["idxs"]]
        staggered = stagger_orders(base, cv, rng)
        wave = Wave(orders=staggered, release_time=0.0)
        mk = simulate_wave(
            wave, n_amrs=N_AMRS, n_elevators=E, capacity=cap, batched=batched,
            policy=policy,
        )
        mks.append(mk)
    return mks


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    order_pool = build_order_pool(seed=43)
    betas = load_betas()

    total = 3 * 2 * 3 * 2 * 2 * N_PER_ARM
    print("=" * 100)
    print(f"Phase 4 H1 STAGGER — T-stagger CV = {STAGGER_CV}")
    print(f"  6 cells x 3 sizes x 2 policies x 2 arms x {N_PER_ARM} waves = {total} sims")
    print("=" * 100)

    pool_per_size = {s: build_candidate_waves(s, POOL_SIZE_PER_BAND, order_pool,
                                              seed=2026 + s)
                     for s in SIZE_BANDS}

    rows = []
    t_total = time.time()

    for E, cap in REGIMES:
        regime_str = f"E{E}_c{cap}"
        for model in ELEVATOR_MODELS:
            bc = betas[(regime_str, model)]["C"]
            bi = betas[(regime_str, model)]["I"]
            fav_c_hi, fav_i_hi = favorable_corner(bc, bi)
            fav_label = ("HC" if fav_c_hi else "LC") + "_" + ("HI" if fav_i_hi else "LI")
            for size in SIZE_BANDS:
                cand = pool_per_size[size]
                fav_df = select_corner(cand, fav_c_hi, fav_i_hi)
                t0 = time.time()
                for policy in POLICIES:
                    for arm in ARMS:
                        arm_df = cand if arm == "random" else fav_df
                        seed = hash((E, cap, model, size, arm, policy,
                                     STAGGER_CV)) & 0x7fff
                        mks = run_arm(arm_df, (E, cap), model, policy,
                                      order_pool, N_PER_ARM, STAGGER_CV, seed)
                        for mk in mks:
                            rows.append({
                                "regime": regime_str, "model": model, "size": size,
                                "policy": policy, "arm": arm,
                                "favorable_corner": fav_label, "makespan": mk,
                                "stagger_cv": STAGGER_CV,
                            })
                el = time.time() - t0
                print(f"  {regime_str:6s} {model:11s} size={size}: "
                      f"fav={fav_label}  ({el:.1f}s)")

    df = pd.DataFrame(rows)
    out_csv = RAW_DIR / "mvs_v0_2_phase4_H1_stagger_samples.csv"
    df.to_csv(out_csv, index=False)
    print()
    print(f"Total runtime: {time.time() - t_total:.1f}s")
    print(f"Saved {len(df)} rows to {out_csv}")


if __name__ == "__main__":
    main()
