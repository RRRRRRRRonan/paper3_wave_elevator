"""
MVS v0.2 Phase 4 H1 — D3 smoke test (240 simulations).

Gate check before committing to the full 14400-sim pre-reg run.

Design (thin slice of full H1):
  - 3 regimes (E1_c2, E2_c2, E3_c2)
  - 1 elevator model (batched — cluster policy only matters with true batching)
  - 1 size band (6, the middle of 4/6/8)
  - 2 policies (P0 = fifo, P1 = cluster)
  - 2 arms (random, favorable_corner from Phi-advice)
  - 20 waves per cell x policy x arm
  => 3 * 1 * 1 * 2 * 2 * 20 = 240 sims

Purpose:
  Decide (D3 GATE) whether P1 (destination-clustered batching) produces a
  directionally meaningful mean-makespan reduction vs P0 (FIFO) before we
  spend compute on the full 14400-sim pre-registered experiment.

Exit criteria (pre-discussed):
  - If at least 2 of 3 cells show P1 mean makespan < P0 mean makespan on the
    favorable_corner arm by >= 1% in magnitude -> PROCEED to D4-D5
  - Otherwise -> STOP at smoke test; revisit P1 spec before locking pre-reg

Output: results/raw/mvs_v0_2_phase4_H1_smoke.csv plus a summary table.
"""
from __future__ import annotations

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
    materialise_wave,
    select_corner,
)
from src.simulator import simulate_wave

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RAW_DIR = RESULTS_DIR / "raw"

REGIMES = [(1, 2), (2, 2), (3, 2)]
MODEL = "batched"
SIZE = 6
POLICIES = ["fifo", "cluster"]
ARMS = ["random", "favorable"]
N_WAVES = 20


def run_arm(waves_df: pd.DataFrame, regime: Tuple[int, int], policy: str,
            order_pool, n_draw: int, seed: int) -> List[float]:
    rng = random.Random(seed)
    if len(waves_df) == 0:
        return []
    idxs = rng.choices(range(len(waves_df)), k=n_draw)
    E, cap = regime
    makespans = []
    for i in idxs:
        wave = materialise_wave(waves_df.iloc[i], order_pool)
        mk = simulate_wave(
            wave,
            n_amrs=N_AMRS,
            n_elevators=E,
            capacity=cap,
            batched=True,
            policy=policy,
        )
        makespans.append(mk)
    return makespans


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    order_pool = build_order_pool(seed=43)
    betas = load_betas()

    print("=" * 90)
    print("Phase 4 H1 SMOKE TEST — D3 gate check (240 sims)")
    print("=" * 90)
    print(f"  3 regimes x 1 model ({MODEL}) x 1 size ({SIZE}) "
          f"x 2 policies x 2 arms x {N_WAVES} waves = {3*2*2*N_WAVES} sims")
    print()

    # Build candidate pool for size 6 and select favorable corners per cell
    print(f"Building candidate pool (size={SIZE}, n={POOL_SIZE_PER_BAND})...")
    cand = build_candidate_waves(SIZE, POOL_SIZE_PER_BAND, order_pool,
                                 seed=2026 + SIZE)

    rows = []
    t_total = time.time()
    for E, cap in REGIMES:
        regime_str = f"E{E}_c{cap}"
        beta_C = betas[(regime_str, MODEL)]["C"]
        beta_I = betas[(regime_str, MODEL)]["I"]
        fav_c_hi, fav_i_hi = favorable_corner(beta_C, beta_I)
        fav_label = ("HC" if fav_c_hi else "LC") + "_" + ("HI" if fav_i_hi else "LI")
        fav_df = select_corner(cand, fav_c_hi, fav_i_hi)

        print(f"  {regime_str}  beta_C={beta_C:+.2f} beta_I={beta_I:+.2f} "
              f"-> fav={fav_label} ({len(fav_df)} waves)")

        for policy in POLICIES:
            for arm in ARMS:
                arm_df = cand if arm == "random" else fav_df
                seed = hash((E, cap, MODEL, SIZE, arm, policy)) & 0x7fff
                t0 = time.time()
                mks = run_arm(arm_df, (E, cap), policy, order_pool, N_WAVES, seed)
                for mk in mks:
                    rows.append({
                        "regime": regime_str,
                        "model": MODEL,
                        "size": SIZE,
                        "policy": policy,
                        "arm": arm,
                        "favorable_corner": fav_label,
                        "makespan": mk,
                    })
                print(f"    policy={policy:8s} arm={arm:10s}  "
                      f"mean={np.mean(mks):7.2f}  n={len(mks)}  "
                      f"({time.time()-t0:.1f}s)")

    df = pd.DataFrame(rows)
    out_csv = RAW_DIR / "mvs_v0_2_phase4_H1_smoke.csv"
    df.to_csv(out_csv, index=False)
    print()
    print(f"Total runtime: {time.time() - t_total:.1f}s")
    print(f"Saved {len(df)} rows to {out_csv}")

    # ------- D3 GATE summary -------
    print()
    print("=" * 90)
    print("D3 GATE SUMMARY — P1 (cluster) vs P0 (fifo)")
    print("=" * 90)
    print(f"{'regime':8s} {'arm':10s}  {'P0_fifo':>8s}  {'P1_cluster':>10s}  "
          f"{'delta':>8s}  {'rel%':>7s}  {'dir':>5s}")

    summary = []
    for E, cap in REGIMES:
        regime_str = f"E{E}_c{cap}"
        for arm in ARMS:
            sub = df[(df["regime"] == regime_str) & (df["arm"] == arm)]
            m_p0 = sub[sub["policy"] == "fifo"]["makespan"].mean()
            m_p1 = sub[sub["policy"] == "cluster"]["makespan"].mean()
            delta = m_p1 - m_p0
            rel = delta / m_p0 if m_p0 > 0 else float("nan")
            direction = "P1<P0" if delta < 0 else ("P1>P0" if delta > 0 else "equal")
            print(f"{regime_str:8s} {arm:10s}  {m_p0:>8.2f}  {m_p1:>10.2f}  "
                  f"{delta:>+8.2f}  {rel:>+7.2%}  {direction:>5s}")
            summary.append({
                "regime": regime_str, "arm": arm,
                "mean_P0": m_p0, "mean_P1": m_p1,
                "delta": delta, "rel": rel,
            })

    # Gate check: >=2 of 3 cells show P1 beats P0 by >=1% on favorable arm
    fav_rows = [s for s in summary if s["arm"] == "favorable"]
    wins = [s for s in fav_rows if s["rel"] <= -0.01]
    print()
    print(f"Cells (favorable arm) with P1 beating P0 by >=1%: {len(wins)}/{len(fav_rows)}")
    if len(wins) >= 2:
        verdict = "PROCEED — P1 shows directional lift; continue to D4-D5 (full 14400 sim)"
    elif len(wins) == 1:
        verdict = ("MARGINAL — only 1 cell shows >=1% lift on favorable arm. "
                   "Inspect per-cell deltas before deciding D4-D5.")
    else:
        verdict = ("STOP — no cells show >=1% lift on favorable arm. "
                   "Revise P1 spec (e.g. tighten clustering objective) before pre-reg.")
    print(f"Verdict: {verdict}")


if __name__ == "__main__":
    main()
