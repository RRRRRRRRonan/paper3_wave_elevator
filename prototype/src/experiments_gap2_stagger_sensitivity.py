"""
MVS v0.2 Tier-1 Gap 2 — T-stagger sensitivity (full 6-cell version).

Reviewer concern (Wan et al. 2024, Zhao et al. 2024): orders all release at
t=0, so the T dimension of Phi = (C, I, T) is structurally inactive in v0.2.

Defence strategy: synthesise per-order release_times from a parametric
inter-arrival distribution, sweep CV across all 6 cells, check M4 best-
corner invariance.

Design:
  - 6 cells: 3 regimes x 2 models
  - size = 6
  - Inter-arrival CV in {0.0, 0.2, 0.5, 1.0}; rate = 1.0 (mean 1 s gap)
  - 5 arms (random + 4 corners) x 200 waves per arm
  - 6 cells x 4 CVs x 5 arms x 200 = 24 000 sims

Output: results/v0_2_gap2_stagger_sensitivity.json
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
    select_corner,
)
from src.simulator import Order, Wave, simulate_wave

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RAW_DIR = RESULTS_DIR / "raw"
OUT_JSON = RESULTS_DIR / "v0_2_gap2_stagger_sensitivity.json"

REGIMES = [(1, 2), (2, 2), (3, 2)]
MODELS = ["abstraction", "batched"]
SIZE = 6
CVS = [0.0, 0.2, 0.5, 1.0]
ARMS = ["random", "HC_HI", "HC_LI", "LC_HI", "LC_LI"]
N_PER_ARM = 200


def lognormal_sigma_for_cv(cv: float) -> float:
    if cv <= 0:
        return 0.0
    return math.sqrt(math.log(1.0 + cv * cv))


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


def materialise_staggered(row, order_pool: List[Order], cv: float,
                          rng: random.Random) -> Wave:
    base = [order_pool[i] for i in row["idxs"]]
    return Wave(orders=stagger_orders(base, cv, rng), release_time=0.0)


def run_arm(waves_df: pd.DataFrame, regime: Tuple[int, int], model: str,
            order_pool: List[Order], n_draw: int, cv: float, seed: int) -> List[float]:
    rng = random.Random(seed)
    if len(waves_df) == 0:
        return []
    idxs = rng.choices(range(len(waves_df)), k=n_draw)
    E, cap = regime
    batched = (model == "batched")
    mks = []
    for i in idxs:
        wave = materialise_staggered(waves_df.iloc[i], order_pool, cv, rng)
        mk = simulate_wave(
            wave, n_amrs=N_AMRS, n_elevators=E, capacity=cap, batched=batched,
        )
        mks.append(mk)
    return mks


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    order_pool = build_order_pool(seed=43)

    total = len(REGIMES) * len(MODELS) * len(CVS) * len(ARMS) * N_PER_ARM
    print("=" * 100)
    print(f"Gap 2 sensitivity (full 6 cells) — T-stagger CV sweep")
    print(f"  6 cells x {len(CVS)} CVs x {len(ARMS)} arms x {N_PER_ARM} waves = {total} sims")
    print("=" * 100)

    cand = build_candidate_waves(SIZE, POOL_SIZE_PER_BAND, order_pool, seed=2026 + SIZE)
    arm_dfs = {
        "random": cand,
        "HC_HI": select_corner(cand, True, True),
        "HC_LI": select_corner(cand, True, False),
        "LC_HI": select_corner(cand, False, True),
        "LC_LI": select_corner(cand, False, False),
    }

    all_rows = []
    all_cells = []
    t_total = time.time()

    for E, cap in REGIMES:
        regime_str = f"E{E}_c{cap}"
        for model in MODELS:
            cell_label = f"{regime_str}|{model}"
            print(f"\nCell {cell_label} (size={SIZE})")
            per_cv_summary = []
            cv0_best = None
            n_match = 0
            for cv in CVS:
                per_arm = {}
                for arm in ARMS:
                    seed = hash((regime_str, model, SIZE, arm, cv)) & 0x7fff
                    mks = run_arm(arm_dfs[arm], (E, cap), model, order_pool,
                                  N_PER_ARM, cv, seed)
                    per_arm[arm] = np.asarray(mks, dtype=float)
                    for mk in mks:
                        all_rows.append({
                            "regime": regime_str, "model": model, "size": SIZE,
                            "cv": cv, "arm": arm, "makespan": mk,
                        })
                meds = {a: float(np.median(per_arm[a])) for a in ARMS}
                corner_meds = {a: meds[a] for a in ARMS if a != "random"}
                gap = max(corner_meds.values()) - min(corner_meds.values())
                rand_med = meds["random"]
                gap_pct = 100.0 * gap / rand_med if rand_med > 0 else float("nan")
                best = min(corner_meds, key=corner_meds.get)
                if cv == CVS[0]:
                    cv0_best = best
                if best == cv0_best:
                    n_match += 1
                per_cv_summary.append({
                    "cv": cv, "medians": meds, "GAP": gap,
                    "GAP_pct": gap_pct, "best_corner": best,
                })
            status = ("ROBUST" if n_match == len(CVS)
                      else "MOSTLY_ROBUST" if n_match >= len(CVS) - 1
                      else "SENSITIVE")
            print(f"  cv0_best={cv0_best}  match={n_match}/{len(CVS)}  {status}")
            for s in per_cv_summary:
                print(f"    cv={s['cv']:.2f}  GAP={s['GAP']:.2f}  "
                      f"GAP%={s['GAP_pct']:.2f}  best={s['best_corner']}")
            all_cells.append({
                "regime": regime_str, "model": model, "size": SIZE,
                "cv0_best": cv0_best, "n_match": n_match, "n_total": len(CVS),
                "verdict": status, "per_cv": per_cv_summary,
            })

    df = pd.DataFrame(all_rows)
    raw_csv = RAW_DIR / "mvs_v0_2_gap2_stagger_sensitivity.csv"
    df.to_csv(raw_csv, index=False)

    print()
    print("=" * 100)
    print("Full 6-cell summary")
    print("=" * 100)
    print(f"{'cell':25s}  {'cv0_best':>10s}  {'n_match':>8s}  {'verdict':>14s}")
    n_robust = n_mostly = n_sensitive = 0
    for cell in all_cells:
        label = f"{cell['regime']}|{cell['model']}"
        print(f"{label:25s}  {cell['cv0_best']:>10s}  "
              f"{cell['n_match']:>3d}/{cell['n_total']:<3d}  {cell['verdict']:>14s}")
        if cell["verdict"] == "ROBUST":
            n_robust += 1
        elif cell["verdict"] == "MOSTLY_ROBUST":
            n_mostly += 1
        else:
            n_sensitive += 1

    print()
    print(f"Cell counts — ROBUST: {n_robust}/6, MOSTLY_ROBUST: {n_mostly}/6, "
          f"SENSITIVE: {n_sensitive}/6")
    if n_robust + n_mostly == len(all_cells):
        overall = ("T-stagger robustness holds across all 6 cells; M4 corner-argmin stable "
                   "for stagger CV up to 0.5-1.0 depending on cell")
    elif n_robust + n_mostly >= 5:
        overall = "Robust in majority of cells; sensitive cells quantified"
    else:
        overall = "Framework needs cell-specific T-stagger scope"
    print(f"Overall: {overall}")
    print(f"Runtime: {time.time() - t_total:.1f}s")

    out = {
        "generated": "2026-04-22",
        "purpose": "Gap 2 — T-stagger sensitivity across all 6 cells",
        "cvs": CVS, "arms": ARMS, "n_per_arm": N_PER_ARM, "size": SIZE,
        "per_cell": all_cells,
        "summary": {
            "n_robust": n_robust, "n_mostly": n_mostly,
            "n_sensitive": n_sensitive, "overall": overall,
        },
    }
    OUT_JSON.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nSaved {OUT_JSON}")
    print(f"Saved {raw_csv}")


if __name__ == "__main__":
    main()
