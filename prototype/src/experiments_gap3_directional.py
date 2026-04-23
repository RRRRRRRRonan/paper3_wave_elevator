"""
MVS v0.2 Tier-1 Gap 3 — directional-elevator model (M4) vs baseline models
across all 6 cells (both abstraction and true-batching baselines).

Tests whether the directional extension preserves M5.1's per-wave
stochastic-dominance assumption (D) against each reference model:
  - Batched cells:       M_4 vs M_2 (true batching)
  - Abstraction cells:   M_4 vs M_1 (throughput abstraction)

Design (R3-style matched-wave pairing):
  - 3 regimes (E1_c2, E2_c2, E3_c2) x 2 reference models (abstraction, batched)
    = 6 cells
  - 5 arms (random + 4 corners), 200 waves
  - 6 cells x 5 arms x 200 paired = 6000 paired sims (12 000 total)

Per-cell dominance metrics:
  - P[M_4 >= M_ref] across all waves
  - Corner-argmin match: c*_{M_4} vs c*_{M_ref}

Output: results/v0_2_gap3_directional.json
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
OUT_JSON = RESULTS_DIR / "v0_2_gap3_directional.json"

REGIMES = [(1, 2), (2, 2), (3, 2)]
REF_MODELS = ["abstraction", "batched"]
ARMS = ["random", "HC_HI", "HC_LI", "LC_HI", "LC_LI"]
SIZE = 6
N_PER_ARM = 200
DIR_PENALTY = 3.0


def run_arm_paired(waves_df: pd.DataFrame, regime: Tuple[int, int],
                   ref_model: str, order_pool,
                   n_draw: int, seed: int) -> List[dict]:
    rng = random.Random(seed)
    if len(waves_df) == 0:
        return []
    idxs = rng.choices(range(len(waves_df)), k=n_draw)
    E, cap = regime
    batched_ref = (ref_model == "batched")
    rows = []
    for i in idxs:
        wave = materialise_wave(waves_df.iloc[i], order_pool)
        m_ref = simulate_wave(
            wave, n_amrs=N_AMRS, n_elevators=E, capacity=cap, batched=batched_ref,
        )
        m4 = simulate_wave(
            wave, n_amrs=N_AMRS, n_elevators=E, capacity=cap,
            directional=True, dir_switch_penalty=DIR_PENALTY,
        )
        rows.append({"m_ref": m_ref, "m4": m4})
    return rows


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    order_pool = build_order_pool(seed=43)

    total = len(REGIMES) * len(REF_MODELS) * len(ARMS) * N_PER_ARM * 2
    print("=" * 110)
    print(f"Gap 3 — directional (M_4) vs abstraction (M_1) and batched (M_2)")
    print(f"  dir_switch_penalty = {DIR_PENALTY} s, size={SIZE}")
    print(f"  6 cells (3 regimes x 2 ref models) x 5 arms x {N_PER_ARM} paired = "
          f"{total} total sims")
    print("=" * 110)

    cand = build_candidate_waves(SIZE, POOL_SIZE_PER_BAND, order_pool, seed=2026 + SIZE)
    arm_dfs = {
        "random": cand,
        "HC_HI": select_corner(cand, True, True),
        "HC_LI": select_corner(cand, True, False),
        "LC_HI": select_corner(cand, False, True),
        "LC_LI": select_corner(cand, False, False),
    }

    all_rows = []
    per_cell = []
    t_total = time.time()

    for E, cap in REGIMES:
        regime_str = f"E{E}_c{cap}"
        for ref_model in REF_MODELS:
            cell_label = f"{regime_str}|{ref_model}"
            print(f"\nCell {cell_label} — M_4 vs M_ref ({ref_model})")
            arm_ref_med = {}
            arm_m4_med = {}
            arm_dom = {}
            for arm in ARMS:
                seed = hash((regime_str, ref_model, arm, SIZE)) & 0x7fff
                paired = run_arm_paired(arm_dfs[arm], (E, cap), ref_model,
                                        order_pool, N_PER_ARM, seed)
                mr = np.array([r["m_ref"] for r in paired])
                m4 = np.array([r["m4"] for r in paired])
                dom = float((m4 >= mr).mean())
                arm_ref_med[arm] = float(np.median(mr))
                arm_m4_med[arm] = float(np.median(m4))
                arm_dom[arm] = dom
                for a, b in zip(mr, m4):
                    all_rows.append({
                        "regime": regime_str, "ref_model": ref_model,
                        "arm": arm, "m_ref": a, "m4": b,
                    })
                print(f"  {arm:8s}  n={len(paired)}  "
                      f"med_ref={np.median(mr):7.2f}  med_m4={np.median(m4):7.2f}  "
                      f"P[m4>=m_ref]={dom:.1%}")

            corner_ref = {a: arm_ref_med[a] for a in ARMS if a != "random"}
            corner_m4 = {a: arm_m4_med[a] for a in ARMS if a != "random"}
            cstar_ref = min(corner_ref, key=corner_ref.get)
            cstar_m4 = min(corner_m4, key=corner_m4.get)
            argmin_match = (cstar_ref == cstar_m4)
            mean_dom = float(np.mean([arm_dom[a] for a in ARMS]))
            print(f"  c*_ref={cstar_ref}, c*_M4={cstar_m4}  "
                  f"{'(MATCH)' if argmin_match else '(FLIP)'}  "
                  f"mean P[m4>=m_ref]={mean_dom:.1%}")
            per_cell.append({
                "regime": regime_str, "ref_model": ref_model,
                "cstar_ref": cstar_ref, "cstar_M4": cstar_m4,
                "argmin_match": argmin_match,
                "mean_dominance_pct": mean_dom,
                "per_arm_dominance": arm_dom,
                "corner_medians_ref": corner_ref,
                "corner_medians_M4": corner_m4,
            })

    df = pd.DataFrame(all_rows)
    raw_csv = RAW_DIR / "mvs_v0_2_gap3_directional.csv"
    df.to_csv(raw_csv, index=False)

    print()
    print("=" * 110)
    print("Full 6-cell summary")
    print("=" * 110)
    print(f"{'cell':25s}  {'c*_ref':>8s}  {'c*_M4':>8s}  {'match':>6s}  "
          f"{'mean P[m4>=ref]':>15s}")
    n_match = 0
    for cell in per_cell:
        label = f"{cell['regime']}|{cell['ref_model']}"
        print(f"{label:25s}  {cell['cstar_ref']:>8s}  {cell['cstar_M4']:>8s}  "
              f"{'YES' if cell['argmin_match'] else 'no':>6s}  "
              f"{cell['mean_dominance_pct']:>14.1%}")
        if cell["argmin_match"]:
            n_match += 1

    overall_dom = float(np.mean([c["mean_dominance_pct"] for c in per_cell]))
    print()
    print(f"Argmin match: {n_match}/{len(per_cell)} cells")
    print(f"Overall P[m4 >= m_ref]: {overall_dom:.1%}")

    if overall_dom >= 0.90 and n_match == len(per_cell):
        verdict = ("CLEAN EXTENSION — M_4 dominates ref at >=90% and argmin invariant "
                   "in all 6 cells; M5.1 extends verbatim to {M_1, M_2, M_4}")
    elif overall_dom >= 0.75 and n_match >= len(per_cell) - 2:
        verdict = ("PARTIAL EXTENSION — M_4 dominates at >=75%; argmin invariant in "
                   f"{n_match}/{len(per_cell)} cells, matching Corollary M5.2's "
                   "stable-argmin condition (invariance concentrates in elevator-lever-"
                   "large cells where inter-corner gap dominates the ε-bound)")
    else:
        verdict = "SCOPE LIMIT — M_4 breaks dominance or argmin in majority of cells"
    print(f"Verdict: {verdict}")
    print(f"Runtime: {time.time() - t_total:.1f}s")

    out = {
        "generated": "2026-04-22",
        "purpose": "Gap 3 — directional extension across 6 cells (2 ref models x 3 regimes)",
        "dir_switch_penalty": DIR_PENALTY, "size": SIZE, "n_per_arm": N_PER_ARM,
        "per_cell": per_cell,
        "overall": {
            "n_cells": len(per_cell), "n_argmin_match": n_match,
            "mean_dominance_pct": overall_dom, "verdict": verdict,
        },
    }
    OUT_JSON.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nSaved {OUT_JSON}")
    print(f"Saved {raw_csv}")


if __name__ == "__main__":
    main()
