"""
MVS v0.2 Phase 4 v2 Reinforcement Experiment R2 — GAP partition refinement.

Defuses reviewer objection: "why 4 corners and not 9 or 16?"

Tests UB stability under three partition schemes of (C, I, T) wave-feature space:
  - 2x2 = top/bottom 25% on C, I  (current Phase 4 v2)
  - 3x3 = tertile bins on C, I    (3x3=9 cells)
  - 8-octant = top/bottom 25% on C, I, T (2x2x2=8 cells)

Method (sample-efficient):
  Simulate 500 random waves per (regime, model, size). Each wave has features
  (C, I, T) computed at sample time. After simulation, RE-BIN the same waves
  under each of the three partition schemes and compute UB per scheme.

  This avoids re-simulating; partitioning is a post-hoc relabel of the same
  makespan distribution.

  In c=2 sweep: 6 cells x 3 sizes x 500 waves = 9 000 sims (~1-2 minutes).

Output:
  results/raw/mvs_v0_2_phase4_v2_partition_samples.csv
  (re-binning + UB computation done by analysis_phase4_v2_partition.py)
"""
from __future__ import annotations

import random
import time
from pathlib import Path

import pandas as pd

from src.experiments_v0_2 import N_AMRS, build_order_pool
from src.features import compute_all_features
from src.simulator import Order, Wave, simulate_wave

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RAW_DIR = RESULTS_DIR / "raw"

REGIMES = [(1, 2), (2, 2), (3, 2)]
ELEVATOR_MODELS = ["abstraction", "batched"]
SIZE_BANDS = [4, 6, 8]

N_PER_CELL = 500


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    order_pool = build_order_pool(seed=43)

    print("R2 — Partition refinement sample generation")
    print(f"  6 cells x 3 sizes x {N_PER_CELL} waves = {6 * 3 * N_PER_CELL} sims")
    print()

    rows = []
    t_start = time.time()
    for E, cap in REGIMES:
        regime_str = f"E{E}_c{cap}"
        for model in ELEVATOR_MODELS:
            batched = (model == "batched")
            for size in SIZE_BANDS:
                t0 = time.time()
                rng = random.Random(hash((E, cap, model, size, "partition")) & 0x7FFF)
                for k in range(N_PER_CELL):
                    idxs = rng.sample(range(len(order_pool)), size)
                    orders = [order_pool[i] for i in idxs]
                    wave = Wave(orders=orders, release_time=0.0)
                    feats = compute_all_features(wave)
                    mk = simulate_wave(
                        wave,
                        n_amrs=N_AMRS,
                        n_elevators=E,
                        capacity=cap,
                        batched=batched,
                    )
                    rows.append({
                        "regime": regime_str,
                        "model": model,
                        "size": size,
                        "wave_id": k,
                        "C": feats["C"],
                        "I": feats["I"],
                        "T": feats["T"],
                        "cross_floor": feats["cross_floor"],
                        "floor_distance": feats["floor_distance"],
                        "makespan": mk,
                    })
                el = time.time() - t0
                print(f"  {regime_str:6s} {model:11s} size={size}: {el:.1f}s")

    df = pd.DataFrame(rows)
    out_path = RAW_DIR / "mvs_v0_2_phase4_v2_partition_samples.csv"
    df.to_csv(out_path, index=False)
    print()
    print(f"Total runtime: {time.time() - t_start:.1f}s")
    print(f"Saved {len(df)} rows to {out_path}")


if __name__ == "__main__":
    main()
