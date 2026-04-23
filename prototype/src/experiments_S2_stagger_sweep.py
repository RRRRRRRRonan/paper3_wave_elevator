"""
MVS v0.2 Tier-1.5 S2 — H1 stagger full CV sweep (substitutability phase diagram).

Extends the single-CV Phase 4 H1 stagger re-run to a 4-CV sweep
{0.0, 0.2, 0.5, 1.0}, producing a (regime, T-tightness) substitutability
phase diagram. Reviewer-facing deliverable: a heatmap showing where
tactical-operational non-substitutability is active in 2D parameter
space.

Design: 4 CVs x [14 400 H1 sims] = 57 600 sims total.
Each CV loop reuses the H1 wave pool / favorable-corner logic, applies
lognormal inter-arrival stagger, and re-fits the per-cell-aggregate
P1-vs-P0 comparison.

Output: results/v0_2_S2_stagger_phase_diagram.json
"""
from __future__ import annotations

import json
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
OUT_JSON = RESULTS_DIR / "v0_2_S2_stagger_phase_diagram.json"

REGIMES = [(1, 2), (2, 2), (3, 2)]
ELEVATOR_MODELS = ["abstraction", "batched"]
SIZE_BANDS = [4, 6, 8]
POLICIES = ["fifo", "cluster"]
ARMS = ["random", "favorable"]
N_PER_ARM = 200
STAGGER_CVS = [0.0, 0.2, 0.5, 1.0]
N_BOOT = 1000
RNG = np.random.default_rng(20260423)


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
            policy: str, order_pool: List[Order], n_draw: int, cv: float,
            seed: int) -> List[float]:
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


def paired_bootstrap_ci(p0, p1, n_boot=N_BOOT, alpha=0.05):
    n = min(len(p0), len(p1))
    p0, p1 = p0[:n], p1[:n]
    diffs = p1 - p0
    idx = RNG.integers(0, n, size=(n_boot, n))
    boot = diffs[idx].mean(axis=1)
    lo, hi = np.percentile(boot, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return float(diffs.mean()), float(lo), float(hi)


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    order_pool = build_order_pool(seed=43)
    betas = load_betas()

    pool_per_size = {s: build_candidate_waves(s, POOL_SIZE_PER_BAND, order_pool,
                                              seed=2026 + s) for s in SIZE_BANDS}

    print("=" * 100)
    print(f"S2 — H1 stagger phase diagram across CV ∈ {STAGGER_CVS}")
    total = len(STAGGER_CVS) * 3 * 2 * 3 * 2 * 2 * N_PER_ARM
    print(f"  Total sims: {total}")
    print("=" * 100)

    t_total = time.time()
    cv_to_cells = {}
    for cv in STAGGER_CVS:
        print(f"\nCV = {cv}")
        rows = []
        for E, cap in REGIMES:
            regime_str = f"E{E}_c{cap}"
            for model in ELEVATOR_MODELS:
                bc = betas[(regime_str, model)]["C"]
                bi = betas[(regime_str, model)]["I"]
                fav_c_hi, fav_i_hi = favorable_corner(bc, bi)
                for size in SIZE_BANDS:
                    cand = pool_per_size[size]
                    fav_df = select_corner(cand, fav_c_hi, fav_i_hi)
                    for policy in POLICIES:
                        for arm in ARMS:
                            arm_df = cand if arm == "random" else fav_df
                            seed = hash((E, cap, model, size, arm, policy, cv)) & 0x7fff
                            mks = run_arm(arm_df, (E, cap), model, policy,
                                          order_pool, N_PER_ARM, cv, seed)
                            for mk in mks:
                                rows.append({
                                    "cv": cv, "regime": regime_str, "model": model,
                                    "size": size, "policy": policy, "arm": arm,
                                    "makespan": mk,
                                })

        df_cv = pd.DataFrame(rows)
        # Cell-level aggregation on favorable arm
        cells_this_cv = []
        for E, cap in REGIMES:
            regime_str = f"E{E}_c{cap}"
            for model in ELEVATOR_MODELS:
                cell = f"{regime_str}|{model}"
                deltas = []
                n_sig = 0
                for size in SIZE_BANDS:
                    sub = df_cv[(df_cv["regime"] == regime_str) & (df_cv["model"] == model)
                                & (df_cv["size"] == size) & (df_cv["arm"] == "favorable")]
                    p0 = sub[sub["policy"] == "fifo"]["makespan"].to_numpy()
                    p1 = sub[sub["policy"] == "cluster"]["makespan"].to_numpy()
                    delta, lo, hi = paired_bootstrap_ci(p0, p1)
                    deltas.append(delta)
                    if hi < 0:
                        n_sig += 1
                mean_delta = float(np.mean(deltas))
                supported = (n_sig >= 2)
                cells_this_cv.append({
                    "cell": cell, "mean_delta_favorable": mean_delta,
                    "n_sizes_sig": n_sig, "supported": supported,
                })
                print(f"  {cell:25s}  delta={mean_delta:+.2f}  n_sig={n_sig}/3  "
                      f"{'SUPP' if supported else 'not'}")
        cv_to_cells[cv] = cells_this_cv

    # Build phase diagram: cells x CVs, cell value = supported?
    print()
    print("=" * 100)
    print("SUBSTITUTABILITY PHASE DIAGRAM (cells x T-stagger CV)")
    print("=" * 100)
    cell_names = [c["cell"] for c in cv_to_cells[STAGGER_CVS[0]]]
    print(f"{'cell':25s}  " + "  ".join(f"CV={cv:.1f}" for cv in STAGGER_CVS))
    for name in cell_names:
        row = []
        for cv in STAGGER_CVS:
            cell = next(c for c in cv_to_cells[cv] if c["cell"] == name)
            sup = cell["supported"]
            row.append("SUPP" if sup else " -- ")
        print(f"{name:25s}  " + "    ".join(row))

    print()
    print("Delta values (mean over 3 sizes, favorable arm):")
    print(f"{'cell':25s}  " + "  ".join(f"CV={cv:.1f}" for cv in STAGGER_CVS))
    for name in cell_names:
        row = []
        for cv in STAGGER_CVS:
            cell = next(c for c in cv_to_cells[cv] if c["cell"] == name)
            row.append(f"{cell['mean_delta_favorable']:+6.2f}")
        print(f"{name:25s}  " + "  ".join(row))

    out = {
        "generated": "2026-04-22",
        "purpose": "S2: H1 stagger phase diagram across CV sweep",
        "stagger_cvs": STAGGER_CVS,
        "per_cv": {str(cv): cv_to_cells[cv] for cv in STAGGER_CVS},
    }
    OUT_JSON.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nRuntime: {time.time() - t_total:.1f}s")
    print(f"Saved {OUT_JSON}")


if __name__ == "__main__":
    main()
