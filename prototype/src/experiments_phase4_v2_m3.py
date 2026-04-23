"""
MVS v0.2 Phase 4 v2 Reinforcement Experiment R3 — M3 stochastic-batching sensitivity.

Defuses reviewer objection: "your two models aren't the full uncertainty set;
what if M3 is the truth?" — and verifies M5 dominance-collapse holds.

Setup:
  - 3 regimes: E1_c2 (control, non-divergent), E2_c2, E3_c2 (divergent)
  - 1 size: 6 (middle band)
  - 5 arms: random + 4 corners (HC_HI, HC_LI, LC_HI, LC_LI)
  - 200 waves per arm (matched: same wave content simulated under all 4 models)
  - 4 elevator models per wave:
      M1 = throughput abstraction
      M2 = deterministic true batching
      M3a = stochastic batching, sigma=0.10
      M3b = stochastic batching, sigma=0.20

Output: results/raw/mvs_v0_2_phase4_v2_m3_samples.csv
  columns: regime, size, arm, wave_id, makespan_M1, makespan_M2,
           makespan_M3_s10, makespan_M3_s20
"""
from __future__ import annotations

import random
import time
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd

from src.experiments_v0_2 import N_AMRS, build_order_pool
from src.experiments_phase4_v2 import (
    POOL_SIZE_PER_BAND,
    build_candidate_waves,
    materialise_wave,
    select_corner,
)
from src.simulator import Order, Wave, simulate_wave

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RAW_DIR = RESULTS_DIR / "raw"

REGIMES = [(1, 2), (2, 2), (3, 2)]
SIZE_TARGET = 6
ARMS = ["random", "HC_HI", "HC_LI", "LC_HI", "LC_LI"]
N_PER_ARM = 200

NOISE_SIGMAS = [0.10, 0.20]


def simulate_one_wave_all_models(
    wave: Wave,
    E: int,
    cap: int,
    rng_m3a: random.Random,
    rng_m3b: random.Random,
) -> Dict[str, float]:
    return {
        "M1": simulate_wave(wave, n_amrs=N_AMRS, n_elevators=E, capacity=cap,
                            batched=False),
        "M2": simulate_wave(wave, n_amrs=N_AMRS, n_elevators=E, capacity=cap,
                            batched=True),
        "M3_s10": simulate_wave(wave, n_amrs=N_AMRS, n_elevators=E, capacity=cap,
                                 stochastic_sigma=NOISE_SIGMAS[0], rng=rng_m3a),
        "M3_s20": simulate_wave(wave, n_amrs=N_AMRS, n_elevators=E, capacity=cap,
                                 stochastic_sigma=NOISE_SIGMAS[1], rng=rng_m3b),
    }


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    order_pool = build_order_pool(seed=43)

    print("R3 — M3 stochastic-batching sensitivity")
    print(f"  3 regimes x 1 size (={SIZE_TARGET}) x {len(ARMS)} arms x "
          f"{N_PER_ARM} waves x 4 models = "
          f"{3 * len(ARMS) * N_PER_ARM * 4} simulations")
    print()

    # Build candidate pool at size=6 (same seed as Phase 4 v2)
    print(f"Building candidate pool at size={SIZE_TARGET}...")
    candidates = build_candidate_waves(
        SIZE_TARGET, POOL_SIZE_PER_BAND, order_pool,
        seed=2026 + SIZE_TARGET,
    )

    arms_dfs = {
        "random": candidates,
        "HC_HI": select_corner(candidates, True, True),
        "HC_LI": select_corner(candidates, True, False),
        "LC_HI": select_corner(candidates, False, True),
        "LC_LI": select_corner(candidates, False, False),
    }
    print(f"  corner sizes: HC_HI={len(arms_dfs['HC_HI'])} "
          f"HC_LI={len(arms_dfs['HC_LI'])} "
          f"LC_HI={len(arms_dfs['LC_HI'])} "
          f"LC_LI={len(arms_dfs['LC_LI'])}")

    print()
    print("Simulating arms under M1, M2, M3_s10, M3_s20...")
    rows = []
    t_start = time.time()
    for E, cap in REGIMES:
        regime_str = f"E{E}_c{cap}"
        for arm in ARMS:
            t0 = time.time()
            arm_df = arms_dfs[arm]
            sample_rng = random.Random(hash((E, cap, arm, "R3sample")) & 0x7FFF)
            idxs = sample_rng.choices(range(len(arm_df)), k=N_PER_ARM)
            # Per-arm RNGs for M3 (stable seed per regime+arm)
            rng_m3a = random.Random(hash((E, cap, arm, "M3a")) & 0xFFFFFF)
            rng_m3b = random.Random(hash((E, cap, arm, "M3b")) & 0xFFFFFF)
            for w_id, i in enumerate(idxs):
                wave = materialise_wave(arm_df.iloc[i], order_pool)
                mks = simulate_one_wave_all_models(wave, E, cap, rng_m3a, rng_m3b)
                rows.append({
                    "regime": regime_str,
                    "size": SIZE_TARGET,
                    "arm": arm,
                    "wave_id": w_id,
                    "makespan_M1": mks["M1"],
                    "makespan_M2": mks["M2"],
                    "makespan_M3_s10": mks["M3_s10"],
                    "makespan_M3_s20": mks["M3_s20"],
                })
            el = time.time() - t0
            print(f"  {regime_str:6s}  {arm:6s}: ({el:.2f}s)")

    df = pd.DataFrame(rows)
    out_path = RAW_DIR / "mvs_v0_2_phase4_v2_m3_samples.csv"
    df.to_csv(out_path, index=False)
    print()
    print(f"Total runtime: {time.time() - t_start:.1f}s")
    print(f"Saved {len(df)} rows to {out_path}")


if __name__ == "__main__":
    main()
