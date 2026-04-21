"""
MVS v0.2 Phase 1 — regime sweep experiment runner.

Sweeps (n_elevators, capacity) over {1,2,3} x {1,2} = 6 regimes.
For each regime, generates 1000 random waves (fixed seed schedule so that
waves are matched across regimes — same wave content, different regime).

Physical parameters per plan §4.1: F=5 floors, N=10 AMRs, pool_size=30,
wave size range 3-8 (same as v0.1). Everything else deterministic.

Output: prototype/results/raw/mvs_v0_2_phase1_samples.csv
"""
from __future__ import annotations

import random
import time
from pathlib import Path
from typing import List, Tuple

import pandas as pd

from src.features import compute_all_features
from src.simulator import Order, Wave, simulate_wave

# v0.2 Phase 1 parameters
N_FLOORS = 5
N_AMRS = 10
POOL_SIZE = 30
WAVE_SIZE_MIN = 3
WAVE_SIZE_MAX = 8
N_SAMPLES = 1000
RESULTS_DIR = Path(__file__).resolve().parents[1] / "results" / "raw"

REGIMES: List[Tuple[int, int]] = [
    (1, 1),
    (2, 1),
    (3, 1),
    (1, 2),
    (2, 2),
    (3, 2),
]


def build_order_pool(pool_size: int = POOL_SIZE, seed: int = 43) -> List[Order]:
    """Generate `pool_size` orders with random (source, dest) floors in {1..F}.

    Exclude trivial (1,1) orders.
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


def generate_wave_specs(n_samples: int, seed: int = 2026) -> List[Tuple[int, List[int]]]:
    """Return list of (wave_size, [pool_indices]) so that waves are matched
    across regimes. We only vary (E, capacity); the wave content itself
    stays identical across regimes for clean paired comparisons.
    """
    rng = random.Random(seed)
    specs: List[Tuple[int, List[int]]] = []
    for _ in range(n_samples):
        size = rng.randint(WAVE_SIZE_MIN, WAVE_SIZE_MAX)
        idxs = rng.sample(range(POOL_SIZE), size)
        specs.append((size, idxs))
    return specs


def run_regime(
    regime: Tuple[int, int],
    pool: List[Order],
    specs: List[Tuple[int, List[int]]],
) -> pd.DataFrame:
    E, cap = regime
    rows = []
    for wave_id, (size, idxs) in enumerate(specs):
        orders = [pool[i] for i in idxs]
        wave = Wave(orders=orders, release_time=0.0)
        makespan = simulate_wave(
            wave,
            n_amrs=N_AMRS,
            n_elevators=E,
            capacity=cap,
        )
        feats = compute_all_features(wave)
        rows.append(
            {
                "regime": f"E{E}_c{cap}",
                "n_elevators": E,
                "capacity": cap,
                "wave_id": wave_id,
                **feats,
                "makespan": makespan,
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    pool = build_order_pool(seed=43)
    specs = generate_wave_specs(n_samples=N_SAMPLES, seed=2026)

    print(f"Regime sweep: {len(REGIMES)} regimes × {N_SAMPLES} samples")
    print(f"Parameters: F={N_FLOORS}, N_AMRs={N_AMRS}, pool={POOL_SIZE}, "
          f"wave size in [{WAVE_SIZE_MIN}, {WAVE_SIZE_MAX}]")
    print("=" * 72)
    print(f"{'Regime':10s} {'E':>3s} {'cap':>4s} {'n':>6s} "
          f"{'mk_min':>8s} {'mk_med':>8s} {'mk_max':>8s} {'runtime':>9s}")
    print("=" * 72)

    all_dfs = []
    total_start = time.time()
    for regime in REGIMES:
        start = time.time()
        df = run_regime(regime, pool, specs)
        elapsed = time.time() - start
        print(
            f"{df['regime'].iloc[0]:10s} {regime[0]:>3d} {regime[1]:>4d} "
            f"{len(df):>6d} {df['makespan'].min():>8.1f} "
            f"{df['makespan'].median():>8.1f} {df['makespan'].max():>8.1f} "
            f"{elapsed:>8.2f}s"
        )
        all_dfs.append(df)
    total_elapsed = time.time() - total_start
    print("=" * 72)
    print(f"Total runtime: {total_elapsed:.1f}s")

    combined = pd.concat(all_dfs, ignore_index=True)
    out_path = RESULTS_DIR / "mvs_v0_2_phase1_samples.csv"
    combined.to_csv(out_path, index=False)
    print(f"\nSaved {len(combined)} rows to {out_path}")

    print("\nFeature summary (across all regimes, same waves):")
    print(combined[combined["regime"] == "E1_c1"][
        ["size", "cross_floor", "floor_distance", "C", "I"]
    ].describe().round(3))

    print("\nFeature collinearity (on E1_c1 subset):")
    subset = combined[combined["regime"] == "E1_c1"][
        ["size", "cross_floor", "floor_distance", "C", "I", "makespan"]
    ]
    print(subset.corr().round(3))


if __name__ == "__main__":
    main()
