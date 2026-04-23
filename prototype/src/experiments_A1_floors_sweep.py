"""
MVS v0.2 Tier-1.5 A1 — Floors sweep (F in {5, 7, 9}).

v0.2 main experiments use F=5. Extends to F=7 and F=9 to test whether the
M4 GAP framework and M5 dominance rule scale to more realistic building
heights (5-10 floors is typical for multi-storey AMR deployments).

Design:
  - 3 floor counts: F in {5, 7, 9}
  - Fix E=2, cap=2 (E2_c2, the middle regime)
  - Regenerate order pool per F
  - Build fresh candidate pool per F
  - 5 arms x 200 waves, both abstraction and batched models
  - Size = 6
  - 3 F x 2 models x 5 arms x 200 = 6 000 sims

Per-F metrics:
  - GAP per cell
  - Best corner identification stability
  - P[M_2 >= M_1] dominance

Output: results/v0_2_A1_floors_sweep.json
"""
from __future__ import annotations

import json
import random
import time
from pathlib import Path
from typing import List, Tuple

import numpy as np
import pandas as pd

from src.features import compute_all_features
from src.simulator import Order, Wave, simulate_wave

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RAW_DIR = RESULTS_DIR / "raw"
OUT_JSON = RESULTS_DIR / "v0_2_A1_floors_sweep.json"

FLOORS = [5, 7, 9]
E_FIXED = 2
CAP = 2
N_AMRS = 10
POOL_SIZE = 30
SIZE = 6
N_PER_ARM = 200
ARMS = ["random", "HC_HI", "HC_LI", "LC_HI", "LC_LI"]
HIGH_Q = 0.75
LOW_Q = 0.25
POOL_SIZE_PER_BAND = 3000


def build_order_pool(pool_size: int, n_floors: int, seed: int) -> List[Order]:
    rng = random.Random(seed)
    out = []
    for i in range(pool_size):
        while True:
            src = rng.randint(1, n_floors)
            dst = rng.randint(1, n_floors)
            if not (src == 1 and dst == 1):
                break
        out.append(Order(id=i, source_floor=src, dest_floor=dst))
    return out


def build_candidate_waves(size: int, n: int, order_pool: List[Order],
                          seed: int) -> pd.DataFrame:
    rng = random.Random(seed)
    rows = []
    for k in range(n):
        idxs = rng.sample(range(len(order_pool)), size)
        orders = [order_pool[i] for i in idxs]
        wave = Wave(orders=orders, release_time=0.0)
        feats = compute_all_features(wave)
        rows.append({
            "wave_id": k, "size": size,
            "C": feats["C"], "I": feats["I"],
            "floor_distance": feats["floor_distance"],
            "cross_floor": feats["cross_floor"],
            "idxs": tuple(idxs),
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


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 100)
    print(f"A1 — Floors sweep F in {FLOORS}, fixed E={E_FIXED}, cap={CAP}")
    print(f"  6 000 sims across 3 F x 2 models x 5 arms x {N_PER_ARM}")
    print("=" * 100)

    per_F = []
    t_total = time.time()

    for F in FLOORS:
        print(f"\nF = {F}  (order pool with N_FLOORS={F})")
        pool = build_order_pool(POOL_SIZE, F, seed=43 + F)
        cand = build_candidate_waves(SIZE, POOL_SIZE_PER_BAND, pool,
                                     seed=2026 + SIZE + F * 100)
        arm_dfs = {
            "random": cand,
            "HC_HI": select_corner(cand, True, True),
            "HC_LI": select_corner(cand, True, False),
            "LC_HI": select_corner(cand, False, True),
            "LC_LI": select_corner(cand, False, False),
        }

        for model in ["abstraction", "batched"]:
            batched = (model == "batched")
            arm_medians = {}
            paired_m1m2 = []  # for dominance
            for arm in ARMS:
                rng = random.Random(hash((F, model, arm, "A1")) & 0x7fff)
                arm_df = arm_dfs[arm]
                if len(arm_df) == 0:
                    continue
                idxs = rng.choices(range(len(arm_df)), k=N_PER_ARM)
                mks = []
                for i in idxs:
                    row = arm_df.iloc[i]
                    orders = [pool[j] for j in row["idxs"]]
                    wave = Wave(orders=orders, release_time=0.0)
                    mk = simulate_wave(wave, n_amrs=N_AMRS, n_elevators=E_FIXED,
                                       capacity=CAP, batched=batched)
                    mks.append(mk)
                arm_medians[arm] = float(np.median(mks))

            corner_meds = {a: arm_medians[a] for a in ARMS if a != "random"}
            gap = max(corner_meds.values()) - min(corner_meds.values())
            rand_med = arm_medians["random"]
            gap_pct = 100.0 * gap / rand_med if rand_med > 0 else 0.0
            best_corner = min(corner_meds, key=corner_meds.get)
            print(f"  {model:11s}  best={best_corner}  GAP={gap:.2f} ({gap_pct:.2f}%)  "
                  f"med_random={rand_med:.2f}")

            per_F.append({
                "F": F, "model": model,
                "arm_medians": arm_medians,
                "GAP": gap, "GAP_pct": gap_pct,
                "best_corner": best_corner,
            })

    print()
    print("=" * 100)
    print("Floors sweep summary — best corner stability")
    print("=" * 100)
    print(f"{'F':>3s}  {'model':>12s}  {'best corner':>12s}  {'GAP%':>6s}  {'med_rand':>9s}")
    for r in per_F:
        print(f"{r['F']:>3d}  {r['model']:>12s}  {r['best_corner']:>12s}  "
              f"{r['GAP_pct']:>5.2f}%  {r['arm_medians']['random']:>9.2f}")

    # Check: does best_corner stay the same across F, per model?
    by_model = {}
    for r in per_F:
        by_model.setdefault(r["model"], []).append(r)
    print()
    stability = {}
    for model, rs in by_model.items():
        bests = [r["best_corner"] for r in rs]
        stable = (len(set(bests)) == 1)
        stability[model] = stable
        print(f"  {model}: best corners across F = {bests} — "
              f"{'STABLE' if stable else 'SHIFTS'}")

    all_stable = all(stability.values())
    if all_stable:
        verdict = ("F SCALING CLEAN — M4 best-corner identification invariant from F=5 "
                   "to F=9 in both elevator models; framework scales to realistic "
                   "building heights")
    else:
        verdict = ("F-DEPENDENT — best corner shifts across F in at least one model; "
                   "requires F-range scope statement")
    print(f"\nVerdict: {verdict}")
    print(f"Runtime: {time.time() - t_total:.1f}s")

    out = {
        "generated": "2026-04-22",
        "purpose": "A1: floors sweep F in {5,7,9} at E=2, cap=2",
        "floors": FLOORS, "E": E_FIXED, "cap": CAP, "size": SIZE,
        "n_per_arm": N_PER_ARM,
        "per_F": per_F,
        "stability_per_model": stability,
        "verdict": verdict,
    }
    OUT_JSON.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"Saved {OUT_JSON}")


if __name__ == "__main__":
    main()
