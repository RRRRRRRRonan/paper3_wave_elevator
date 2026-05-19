"""
MVS v0.5 Phase 5 — supplementary publication-scale experiments for C3.

Pre-registered as pre-reg §9.2 amendment (2026-05-19); design locked before
this run. Two experiments giving C3's managerial outcomes publication-scale
evidence:

  run_supp1 -- H1 at scale: P0 (FIFO) vs P1 (destination-clustered) operational
               dispatch across the 6 E=2 configs, matched waves (C3-1, C3-3).
  run_supp2 -- capacity sweep: matched-wave M1/M2 at c in {2,3,4,5} (C3-2).

Run:  python -m src.experiments_phase5_supp
"""
from __future__ import annotations

import random
import time
from pathlib import Path

import pandas as pd

from src import phase5_config as cfg
from src.demand_patterns import generate_pool
from src.experiments_phase5 import _config_fields, _seed, fit_predictors
from src.simulator import simulate_wave
from src.wave_policies import (CORNER_ARMS, build_candidates, corner_positions,
                               favorable_label, materialise)

RAW_DIR = Path(__file__).resolve().parents[1] / "results" / "raw"
CAPACITIES = [2, 3, 4, 5]
SUPP2_SIZE = 16


def run_supp1(configs, sizes, n_per_arm, cand_n, train_sample) -> pd.DataFrame:
    """H1 at publication scale: P0 (fifo) vs P1 (cluster), matched waves, M2."""
    rows = []
    for config in configs:
        pool = generate_pool(config["demand"], config["F"], cfg.ORDER_POOL_SIZE,
                             seed=cfg.SEED_BASE + config["config_id"],
                             **cfg.DEMAND_PARAMS[config["demand"]])
        for size in sizes:
            seed = _seed(config["config_id"], 55, size)
            cand = build_candidates(pool, size, cand_n, random.Random(seed))
            beta, _ = fit_predictors(cand, pool, config, "batched",
                                     train_sample, seed + 1)
            fav = favorable_label(beta)
            for ai, (arm_label, corner) in enumerate(
                    [("random", "random"), ("phi_corner", fav)]):
                pos = corner_positions(cand, corner)
                arm_rng = random.Random(seed + 17 * (ai + 1))
                draw = [int(arm_rng.choice(pos)) for _ in range(n_per_arm)]
                for oi, ops in enumerate(["fifo", "cluster"]):
                    sim_rng = random.Random(seed + 401 + oi)
                    for wid, p in enumerate(draw):
                        wave = materialise(cand.iloc[p], pool)
                        mk = simulate_wave(
                            wave, n_amrs=config["n_amrs"],
                            n_elevators=config["n_elevators"],
                            capacity=cfg.CAPACITY, batched=True,
                            policy=ops, rng=sim_rng)
                        rows.append({**_config_fields(config), "size": size,
                                     "arm": arm_label, "ops_policy": ops,
                                     "wave_id": wid, "makespan": mk})
    return pd.DataFrame(rows)


def run_supp2(configs, capacities, size, n_per_arm, cand_n) -> pd.DataFrame:
    """Capacity sweep: the same drawn waves simulated under M1 and M2 at each c."""
    rows = []
    for config in configs:
        pool = generate_pool(config["demand"], config["F"], cfg.ORDER_POOL_SIZE,
                             seed=cfg.SEED_BASE + config["config_id"],
                             **cfg.DEMAND_PARAMS[config["demand"]])
        seed = _seed(config["config_id"], 66, size)
        cand = build_candidates(pool, size, cand_n, random.Random(seed))
        for ci, c in enumerate(capacities):
            for ai, arm in enumerate(CORNER_ARMS):
                pos = corner_positions(cand, arm)
                arm_rng = random.Random(seed + 1000 * (ci + 1) + 17 * (ai + 1))
                for wid in range(n_per_arm):
                    wave = materialise(cand.iloc[int(arm_rng.choice(pos))], pool)
                    r1 = random.Random(seed + 5000 + ci * 100 + wid)
                    r2 = random.Random(seed + 9000 + ci * 100 + wid)
                    m1 = simulate_wave(wave, n_amrs=config["n_amrs"],
                                       n_elevators=config["n_elevators"],
                                       capacity=c, batched=False, rng=r1)
                    m2 = simulate_wave(wave, n_amrs=config["n_amrs"],
                                       n_elevators=config["n_elevators"],
                                       capacity=c, batched=True, rng=r2)
                    rows.append({**_config_fields(config), "capacity": c,
                                 "arm": arm, "wave_id": wid,
                                 "makespan_M1": m1, "makespan_M2": m2})
    return pd.DataFrame(rows)


def main() -> None:
    configs = cfg.e2_subset(cfg.make_config_array())[:cfg.BLOCK_B["n_configs"]]
    t0 = time.time()
    print("Phase 5 supplementary experiments (pre-reg §9.2)")
    df1 = run_supp1(configs, cfg.BLOCK_B["sizes"], cfg.N_PER_ARM,
                    cfg.CANDIDATE_POOL, cfg.TRAIN_SAMPLE)
    df2 = run_supp2(configs, CAPACITIES, SUPP2_SIZE, cfg.N_PER_ARM,
                    cfg.CANDIDATE_POOL)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    df1.to_csv(RAW_DIR / "mvs_v0_5_supp1_h1scale.csv", index=False)
    df2.to_csv(RAW_DIR / "mvs_v0_5_supp2_capacity.csv", index=False)
    print(f"  Supp-1: {len(df1)} sims | Supp-2: {len(df2)} matched-wave rows "
          f"= {2 * len(df2)} sims")
    print(f"  done in {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
