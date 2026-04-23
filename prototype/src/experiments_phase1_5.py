"""
MVS v0.2 Phase 1.5 — true-batching re-run for c>=2 regimes.

Re-runs the three Phase 1 regimes with capacity >= 2 using the true
co-occupancy batching semantics (ElevatorPoolBatched). Waves are matched
(same content, same wave_id) to Phase 1 for paired comparison.

Regimes re-run: E1_c2, E2_c2, E3_c2.
Throughput-abstraction baseline comes from results/raw/mvs_v0_2_phase1_samples.csv.

Output: prototype/results/raw/mvs_v0_2_phase1_5_batched_samples.csv
"""
from __future__ import annotations

import time
from pathlib import Path

import pandas as pd

from src.experiments_v0_2 import (
    N_AMRS,
    N_SAMPLES,
    build_order_pool,
    generate_wave_specs,
)
from src.features import compute_all_features
from src.simulator import Wave, simulate_wave

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results" / "raw"
BATCHED_REGIMES = [(1, 2), (2, 2), (3, 2)]


def run_batched_regime(regime, pool, specs):
    E, cap = regime
    rows = []
    for wave_id, (size, idxs) in enumerate(specs):
        orders = [pool[i] for i in idxs]
        wave = Wave(orders=orders, release_time=0.0)
        mk = simulate_wave(
            wave,
            n_amrs=N_AMRS,
            n_elevators=E,
            capacity=cap,
            batched=True,
        )
        feats = compute_all_features(wave)
        rows.append(
            {
                "regime": f"E{E}_c{cap}_batched",
                "n_elevators": E,
                "capacity": cap,
                "batched": True,
                "wave_id": wave_id,
                **feats,
                "makespan": mk,
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    pool = build_order_pool(seed=43)
    specs = generate_wave_specs(n_samples=N_SAMPLES, seed=2026)

    print(f"Phase 1.5 batched: {len(BATCHED_REGIMES)} regimes x {N_SAMPLES} samples")
    print("=" * 72)
    print(f"{'Regime':20s} {'E':>3s} {'cap':>4s} {'n':>6s} "
          f"{'mk_min':>8s} {'mk_med':>8s} {'mk_max':>8s} {'runtime':>9s}")
    print("=" * 72)

    all_dfs = []
    total_start = time.time()
    for regime in BATCHED_REGIMES:
        start = time.time()
        df = run_batched_regime(regime, pool, specs)
        elapsed = time.time() - start
        print(
            f"{df['regime'].iloc[0]:20s} {regime[0]:>3d} {regime[1]:>4d} "
            f"{len(df):>6d} {df['makespan'].min():>8.1f} "
            f"{df['makespan'].median():>8.1f} {df['makespan'].max():>8.1f} "
            f"{elapsed:>8.2f}s"
        )
        all_dfs.append(df)
    total_elapsed = time.time() - total_start
    print("=" * 72)
    print(f"Total runtime: {total_elapsed:.1f}s")

    combined = pd.concat(all_dfs, ignore_index=True)
    out_path = RESULTS_DIR / "mvs_v0_2_phase1_5_batched_samples.csv"
    combined.to_csv(out_path, index=False)
    print(f"\nSaved {len(combined)} rows to {out_path}")


if __name__ == "__main__":
    main()
