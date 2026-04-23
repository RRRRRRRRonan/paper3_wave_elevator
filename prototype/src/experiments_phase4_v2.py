"""
MVS v0.2 Phase 4 v2 — Wave-design experiment.

Tests two questions in one sweep (per intuitions_before_MVS_v0_2.md §4bis):

  Option 1: Does Phi-derived "informed" Arm B beat random Arm A?
  Option 2: How big is the maximum lever between (C, I) corner extremes?

Design:
  - 3 c=2 regimes (E1_c2, E2_c2, E3_c2) x 2 elevator models
    (throughput-abstraction, true-batching) = 6 cells
  - 3 size bands: 4, 6, 8 (fixed within band)
  - 5 arms per (cell x size): random, HC_HI, HC_LI, LC_HI, LC_LI
  - 200 waves per arm

Wave generation:
  - For each size, build a candidate pool of ~3000 random waves from the
    same order pool used in Phase 1
  - Compute (C, I) for each
  - Top/bottom 25% on C => HC / LC bins; same on I
  - Corner waves = intersection of bins; sample 200 per corner per size
  - "Random" arm = random 200 from the unfiltered pool at that size

Per-cell favorable-corner lookup:
  - From results/v0_2_phase1_5_true_batching.json (which contains both
    abstraction and batched betas for the 3 c=2 regimes), pick the corner
    that maximises predicted-makespan-reduction:
        favorable = (sign(beta_C) < 0 ? HC : LC, sign(beta_I) < 0 ? HI : LI)

Output: results/raw/mvs_v0_2_phase4_v2_samples.csv
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
from src.features import compute_all_features
from src.simulator import Order, Wave, simulate_wave

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RAW_DIR = RESULTS_DIR / "raw"

REGIMES = [(1, 2), (2, 2), (3, 2)]
ELEVATOR_MODELS = ["abstraction", "batched"]
SIZE_BANDS = [4, 6, 8]

POOL_SIZE_PER_BAND = 3000  # candidate waves per size before quartile filtering
N_PER_ARM = 200            # waves drawn per arm per (regime, model, size)

# Quartile cutoffs (top/bottom 25%)
HIGH_Q = 0.75
LOW_Q = 0.25


def build_candidate_waves(size: int, n: int, order_pool: List[Order],
                          seed: int) -> pd.DataFrame:
    """Generate `n` random waves of fixed `size`, return DataFrame with C, I."""
    rng = random.Random(seed)
    rows = []
    for k in range(n):
        idxs = rng.sample(range(len(order_pool)), size)
        orders = [order_pool[i] for i in idxs]
        wave = Wave(orders=orders, release_time=0.0)
        feats = compute_all_features(wave)
        rows.append({
            "wave_id": k,
            "size": size,
            "C": feats["C"],
            "I": feats["I"],
            "floor_distance": feats["floor_distance"],
            "cross_floor": feats["cross_floor"],
            "idxs": tuple(idxs),  # for reconstruction
        })
    return pd.DataFrame(rows)


def select_corner(df: pd.DataFrame, c_high: bool, i_high: bool) -> pd.DataFrame:
    c_cut_hi = df["C"].quantile(HIGH_Q)
    c_cut_lo = df["C"].quantile(LOW_Q)
    i_cut_hi = df["I"].quantile(HIGH_Q)
    i_cut_lo = df["I"].quantile(LOW_Q)
    c_mask = df["C"] >= c_cut_hi if c_high else df["C"] <= c_cut_lo
    i_mask = df["I"] >= i_cut_hi if i_high else df["I"] <= i_cut_lo
    return df[c_mask & i_mask].copy()


def load_betas() -> dict:
    """Load beta(C), beta(I) from Phase 1.5 JSON for both abstraction & batched.

    Returns dict[(regime_str, model)] = {'C': float, 'I': float}.
    """
    p15 = RESULTS_DIR / "v0_2_phase1_5_true_batching.json"
    with open(p15, encoding="utf-8") as f:
        data = json.load(f)
    out = {}
    for r in ["E1_c2", "E2_c2", "E3_c2"]:
        per = data["per_regime"][r]
        out[(r, "abstraction")] = {
            "C": per["betas_abstraction_ols_for_ref"]["C"],
            "I": per["betas_abstraction_ols_for_ref"]["I"],
        }
        out[(r, "batched")] = {
            "C": per["betas_batched_ols"]["C"],
            "I": per["betas_batched_ols"]["I"],
        }
    return out


def favorable_corner(beta_C: float, beta_I: float) -> Tuple[bool, bool]:
    """Return (c_high, i_high) for the corner Phi-advice would pick."""
    return (beta_C < 0, beta_I < 0)


def materialise_wave(row, order_pool: List[Order]) -> Wave:
    orders = [order_pool[i] for i in row["idxs"]]
    return Wave(orders=orders, release_time=0.0)


def run_arm(waves_df: pd.DataFrame, regime: Tuple[int, int], model: str,
            order_pool: List[Order], n_draw: int, seed: int) -> List[float]:
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
        )
        makespans.append(mk)
    return makespans


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    order_pool = build_order_pool(seed=43)
    betas = load_betas()

    print("Phase 4 v2: regime-conditional wave-design experiment")
    print(f"  3 regimes x 2 elevator models x 3 sizes x 5 arms x {N_PER_ARM} waves "
          f"= {3*2*3*5*N_PER_ARM} simulations")
    print()

    # 1. Build candidate pools per size and select corners
    print("Building candidate pools and selecting corners...")
    pool_per_size = {}
    corners_per_size = {}
    for size in SIZE_BANDS:
        cand = build_candidate_waves(size, POOL_SIZE_PER_BAND, order_pool,
                                      seed=2026 + size)
        pool_per_size[size] = cand
        corners = {
            "HC_HI": select_corner(cand, True, True),
            "HC_LI": select_corner(cand, True, False),
            "LC_HI": select_corner(cand, False, True),
            "LC_LI": select_corner(cand, False, False),
        }
        corners_per_size[size] = corners
        print(f"  size={size}: corner sizes "
              f"HC_HI={len(corners['HC_HI'])} HC_LI={len(corners['HC_LI'])} "
              f"LC_HI={len(corners['LC_HI'])} LC_LI={len(corners['LC_LI'])}")

    # 2. Run arms per (regime, model, size)
    print()
    print("Running arms...")
    rows = []
    total_start = time.time()
    for E, cap in REGIMES:
        regime_str = f"E{E}_c{cap}"
        for model in ELEVATOR_MODELS:
            beta_C = betas[(regime_str, model)]["C"]
            beta_I = betas[(regime_str, model)]["I"]
            fav_c_hi, fav_i_hi = favorable_corner(beta_C, beta_I)
            fav_label = ("HC" if fav_c_hi else "LC") + "_" + ("HI" if fav_i_hi else "LI")
            for size in SIZE_BANDS:
                t0 = time.time()
                # Random arm
                rand_mks = run_arm(pool_per_size[size], (E, cap), model,
                                   order_pool, N_PER_ARM, seed=hash((E, cap, model, size, "rand")) & 0x7fff)
                for mk in rand_mks:
                    rows.append({"regime": regime_str, "model": model, "size": size,
                                 "arm": "random", "favorable_corner": fav_label, "makespan": mk})
                # 4 corners
                for corner_label, cdf in corners_per_size[size].items():
                    cmks = run_arm(cdf, (E, cap), model, order_pool, N_PER_ARM,
                                   seed=hash((E, cap, model, size, corner_label)) & 0x7fff)
                    for mk in cmks:
                        rows.append({"regime": regime_str, "model": model, "size": size,
                                     "arm": corner_label, "favorable_corner": fav_label,
                                     "makespan": mk})
                el = time.time() - t0
                print(f"  {regime_str:6s} {model:11s} size={size}: "
                      f"fav={fav_label}  beta_C={beta_C:+.2f} beta_I={beta_I:+.2f}  "
                      f"({el:.1f}s)")

    df = pd.DataFrame(rows)
    out_path = RAW_DIR / "mvs_v0_2_phase4_v2_samples.csv"
    df.to_csv(out_path, index=False)
    print()
    print(f"Total runtime: {time.time() - total_start:.1f}s")
    print(f"Saved {len(df)} rows to {out_path}")


if __name__ == "__main__":
    main()
