"""
MVS v0.1 experiment runner.

Generates a pool of 30 orders, samples waves of size 3-8, runs the simulator,
computes features, and saves results to CSV for downstream analysis.
"""
from __future__ import annotations

import random
from pathlib import Path
from typing import List

import pandas as pd

from src.features import compute_all_features
from src.simulator import Order, Wave, simulate_wave

# v0.1 parameters
N_FLOORS = 3
N_AMRS = 5
POOL_SIZE = 30
WAVE_SIZE_MIN = 3
WAVE_SIZE_MAX = 8
N_SAMPLES_DEFAULT = 1000
RESULTS_DIR = Path(__file__).resolve().parents[1] / "results" / "raw"


def build_order_pool(pool_size: int = POOL_SIZE, seed: int = 42) -> List[Order]:
    """Generate `pool_size` orders with random (source, dest) floors.

    Per scope_rational.md: at least one endpoint must differ from floor 1
    (excludes trivial (1,1) orders). Same-floor orders on floors 2, 3 are kept
    because the AMR still needs the elevator to reach that floor.
    """
    rng = random.Random(seed)
    orders: List[Order] = []
    for i in range(pool_size):
        while True:
            src = rng.randint(1, N_FLOORS)
            dst = rng.randint(1, N_FLOORS)
            if not (src == 1 and dst == 1):
                break
        orders.append(Order(id=i, source_floor=src, dest_floor=dst))
    return orders


def generate_random_wave(
    pool: List[Order],
    wave_size: int,
    release_time: float,
    rng: random.Random,
) -> Wave:
    sampled = rng.sample(pool, wave_size)
    return Wave(orders=sampled, release_time=release_time)


def run_batch(n_samples: int, seed: int = 2026) -> pd.DataFrame:
    rng = random.Random(seed)
    pool = build_order_pool(seed=seed + 1)

    rows = []
    for i in range(n_samples):
        size = rng.randint(WAVE_SIZE_MIN, WAVE_SIZE_MAX)
        wave = generate_random_wave(pool, size, release_time=0.0, rng=rng)
        makespan = simulate_wave(wave, n_amrs=N_AMRS)
        feats = compute_all_features(wave)
        rows.append({"wave_id": i, **feats, "makespan": makespan})

    return pd.DataFrame(rows)


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    print("Step 1/2: quick run (n=100) to verify pipeline...")
    df_small = run_batch(n_samples=100, seed=1)
    print(f"  ran 100 waves; makespan: min={df_small['makespan'].min():.1f} "
          f"median={df_small['makespan'].median():.1f} "
          f"max={df_small['makespan'].max():.1f}")

    print("\nStep 2/2: full run (n=1000)...")
    df = run_batch(n_samples=1000, seed=2026)
    out_path = RESULTS_DIR / "mvs_v0_1_samples.csv"
    df.to_csv(out_path, index=False)

    print(f"\nSaved {len(df)} rows to {out_path}")
    print("\nSummary statistics:")
    print(df[["size", "cross_floor", "C", "I", "T", "makespan"]].describe().round(3))

    print("\nSanity: T variance should be 0 in v0.1:")
    print(f"  T variance = {df['T'].var():.6f} (expected 0.0)")
    print(f"\nSanity: makespan should correlate positively with cross_floor:")
    print(f"  corr(cross_floor, makespan) = {df['cross_floor'].corr(df['makespan']):.3f}")


if __name__ == "__main__":
    main()
