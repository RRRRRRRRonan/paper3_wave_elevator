"""
MVS v0.2 Tier-1 Gap 1 — service-time heterogeneity sensitivity (full 6-cell).

Reviewer concern (Srinivas-Yu 2022, Zhang et al. 2025): intra-floor AMR
motion is abstracted as a constant `service_time`; horizontal congestion
and pick-time variance are not modelled.

Defence strategy: replace constant service_time with
`service_time x lognormal(mean=1, sigma=service_sigma)`, sweep sigma
across all 6 (regime, model) cells, check M4 best-corner invariance.

Design:
  - 6 cells: 3 regimes (E1_c2, E2_c2, E3_c2) x 2 models (abstraction, batched)
  - size = 6 (middle of 4/6/8; Phase 4 v2 showed size-invariance of ranking)
  - sigma_floor in {0.0, 0.2, 0.5, 1.0}
  - 5 arms (random + 4 corners) x 200 waves per arm
  - 6 cells x 4 sigmas x 5 arms x 200 = 24 000 sims

Output: results/v0_2_gap1_service_sensitivity.json
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
from src.experiments_phase4_v2 import (
    POOL_SIZE_PER_BAND,
    build_candidate_waves,
    materialise_wave,
    select_corner,
)
from src.simulator import simulate_wave

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RAW_DIR = RESULTS_DIR / "raw"
OUT_JSON = RESULTS_DIR / "v0_2_gap1_service_sensitivity.json"

REGIMES = [(1, 2), (2, 2), (3, 2)]
MODELS = ["abstraction", "batched"]
SIZE = 6
SIGMAS = [0.0, 0.2, 0.5, 1.0]
ARMS = ["random", "HC_HI", "HC_LI", "LC_HI", "LC_LI"]
N_PER_ARM = 200


def run_arm(waves_df: pd.DataFrame, regime: Tuple[int, int], model: str,
            order_pool, n_draw: int, sigma: float, seed: int) -> List[float]:
    rng = random.Random(seed)
    if len(waves_df) == 0:
        return []
    idxs = rng.choices(range(len(waves_df)), k=n_draw)
    E, cap = regime
    batched = (model == "batched")
    noise_rng = random.Random(seed + 9999)
    makespans = []
    for i in idxs:
        wave = materialise_wave(waves_df.iloc[i], order_pool)
        mk = simulate_wave(
            wave, n_amrs=N_AMRS, n_elevators=E, capacity=cap, batched=batched,
            service_sigma=sigma, rng=noise_rng if sigma > 0 else None,
        )
        makespans.append(mk)
    return makespans


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    order_pool = build_order_pool(seed=43)

    total = len(REGIMES) * len(MODELS) * len(SIGMAS) * len(ARMS) * N_PER_ARM
    print("=" * 100)
    print(f"Gap 1 sensitivity (full 6 cells) — service_sigma sweep")
    print(f"  6 cells x {len(SIGMAS)} sigmas x {len(ARMS)} arms x {N_PER_ARM} waves = {total} sims")
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
            per_sigma_summary = []
            sigma0_best = None
            n_match = 0
            for sigma in SIGMAS:
                per_arm = {}
                for arm in ARMS:
                    seed = hash((regime_str, model, SIZE, arm, sigma)) & 0x7fff
                    mks = run_arm(arm_dfs[arm], (E, cap), model, order_pool,
                                  N_PER_ARM, sigma, seed)
                    per_arm[arm] = np.asarray(mks, dtype=float)
                    for mk in mks:
                        all_rows.append({
                            "regime": regime_str, "model": model, "size": SIZE,
                            "sigma": sigma, "arm": arm, "makespan": mk,
                        })
                meds = {a: float(np.median(per_arm[a])) for a in ARMS}
                corner_meds = {a: meds[a] for a in ARMS if a != "random"}
                gap = max(corner_meds.values()) - min(corner_meds.values())
                rand_med = meds["random"]
                gap_pct = 100.0 * gap / rand_med if rand_med > 0 else float("nan")
                best = min(corner_meds, key=corner_meds.get)
                if sigma == SIGMAS[0]:
                    sigma0_best = best
                if best == sigma0_best:
                    n_match += 1
                per_sigma_summary.append({
                    "sigma": sigma, "medians": meds, "GAP": gap,
                    "GAP_pct": gap_pct, "best_corner": best,
                })
            status = ("ROBUST" if n_match == len(SIGMAS)
                      else "MOSTLY_ROBUST" if n_match >= len(SIGMAS) - 1
                      else "SENSITIVE")
            print(f"  sigma0_best={sigma0_best}  match={n_match}/{len(SIGMAS)}  {status}")
            for s in per_sigma_summary:
                print(f"    sigma={s['sigma']:.2f}  GAP={s['GAP']:.2f}  "
                      f"GAP%={s['GAP_pct']:.2f}  best={s['best_corner']}")
            all_cells.append({
                "regime": regime_str, "model": model, "size": SIZE,
                "sigma0_best": sigma0_best, "n_match": n_match,
                "n_total": len(SIGMAS), "verdict": status,
                "per_sigma": per_sigma_summary,
            })

    df = pd.DataFrame(all_rows)
    raw_csv = RAW_DIR / "mvs_v0_2_gap1_service_sensitivity.csv"
    df.to_csv(raw_csv, index=False)

    print()
    print("=" * 100)
    print("Full 6-cell summary")
    print("=" * 100)
    print(f"{'cell':25s}  {'sigma0_best':>12s}  {'n_match':>8s}  {'verdict':>14s}")
    n_robust = n_mostly = n_sensitive = 0
    for cell in all_cells:
        label = f"{cell['regime']}|{cell['model']}"
        print(f"{label:25s}  {cell['sigma0_best']:>12s}  "
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
        overall = "M4 GAP framework robust to service-time heterogeneity across all 6 cells"
    elif n_robust + n_mostly >= 5:
        overall = "Robust in majority of cells; sensitive cells quantified"
    else:
        overall = "Framework needs regime-conditional scope statement"
    print(f"Overall: {overall}")
    print(f"Runtime: {time.time() - t_total:.1f}s")

    out = {
        "generated": "2026-04-22",
        "purpose": "Gap 1 — service-time heterogeneity sensitivity across all 6 cells",
        "sigmas": SIGMAS, "arms": ARMS, "n_per_arm": N_PER_ARM, "size": SIZE,
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
