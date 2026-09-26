"""
Amendment C-1 (2026-07-08): P9 SPO+ delegation test.
Protocol EXACTLY as registered in AMEND-2026-07-08-C_bridge_closure.md.

P9 = linear SPO+ on standardized Phi, information parity with P5/P6
(identical candidate pool + identical 200-wave training sample), bottom-k
deployment, recovery fraction R vs the stored Block A references.
"""
from __future__ import annotations

import json
import random
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "prototype"))

from src import phase5_config as cfg                      # noqa: E402
from src.demand_patterns import generate_pool             # noqa: E402
from src.experiments_phase5 import _seed, sim_makespan    # noqa: E402
from src.wave_policies import build_candidates, materialise  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "outputs"
RAW = ROOT / "prototype" / "results" / "raw"
K_TRAIN = 13
STEP = 0.05
ITERS = 300
K_DEPLOY = 200
PI_P9 = 8


def spo_plus_fit(X: np.ndarray, c: np.ndarray) -> np.ndarray:
    """Linear SPO+ subgradient descent for bottom-k selection."""
    n, p = X.shape
    beta = np.zeros(p)

    def zstar(cost):
        sel = np.zeros(n)
        sel[np.argsort(cost, kind="stable")[:K_TRAIN]] = 1.0
        return sel

    # SPO+ subgradient (Elmachtoub & Grigas 2022): d/dc_hat = 2(z*(c) -
    # z*(2c_hat - c)); descent therefore moves beta ALONG X^T (z*(2c_hat-c)
    # - z*(c)). Dated correction 2026-07-08: the first implementation used
    # the negated update (gradient ascent), caught by the synthetic
    # linear-ground-truth self-test BEFORE any gate wording was adopted;
    # see the amendment's dated note. The factor 2 is absorbed in STEP.
    z_c = zstar(c)
    for _ in range(ITERS):
        c_hat = X @ beta
        g_vec = zstar(2 * c_hat - c) - z_c
        beta += STEP * (X.T @ g_vec)
    return beta


def main() -> None:
    t0 = time.time()
    configs = [c for c in cfg.make_config_array()
               if c["config_id"] in (1, 3, 5, 7, 9, 11)]
    dfA = pd.read_csv(RAW / "mvs_v0_5_phase5_blockA.csv")

    cells, n_sims = [], 0
    for config in configs:
        cid = config["config_id"]
        pool = generate_pool(config["demand"], config["F"],
                             cfg.ORDER_POOL_SIZE, seed=cfg.SEED_BASE + cid,
                             **cfg.DEMAND_PARAMS[config["demand"]])
        for size in (8, 30):
            seed = _seed(cid, 1, size)               # model batched = idx 1
            cand = build_candidates(pool, size, cfg.CANDIDATE_POOL,
                                    random.Random(seed))
            # identical training draw as fit_predictors (rng = Random(seed+1))
            rng_t = random.Random(seed + 1)
            n_tr = min(cfg.TRAIN_SAMPLE, len(cand))
            idx_tr = [rng_t.randrange(len(cand)) for _ in range(n_tr)]
            sub = cand.iloc[idx_tr].reset_index(drop=True)
            c_train = np.array([
                sim_makespan(materialise(row, pool), config, "batched", rng_t)
                for _, row in sub.iterrows()])
            n_sims += n_tr

            feats = cand[["C", "I", "T"]].to_numpy(float)
            mu, sd = feats.mean(axis=0), feats.std(axis=0)
            sd[sd == 0] = 1.0
            Xall = (feats - mu) / sd
            Xtr = Xall[idx_tr]

            beta = spo_plus_fit(Xtr, c_train)
            pred = Xall @ beta
            deploy = np.argsort(pred, kind="stable")[:K_DEPLOY]

            arm_rng = random.Random(seed + 13 * (PI_P9 + 1))   # unused draw
            sim_rng = random.Random(seed + 2003 + PI_P9)
            mks = [sim_makespan(materialise(cand.iloc[int(p)], pool),
                                config, "batched", sim_rng)
                   for p in deploy]
            n_sims += len(mks)
            m_p9 = float(np.median(mks))

            g = dfA[(dfA["config_id"] == cid) & (dfA["model"] == "batched")
                    & (dfA["size"] == size)]
            fav = g["favorable_corner"].iloc[0]
            m_q = {c: float(np.median(g[g["arm"] == c]["makespan"]))
                   for c in ("HC_HI", "HC_LI", "LC_HI", "LC_LI")}
            m0 = float(np.median(g[g["arm"] == "random"]["makespan"]))
            m_fav, m_qmin = m_q[fav], min(m_q.values())
            budget = m_fav - m_qmin
            R = (m_fav - m_p9) / budget if budget > 1e-9 else None
            cells.append({
                "config_id": cid, "size": size, "m_fav": m_fav,
                "m_qmin": m_qmin, "m0": m0, "m_P9": m_p9,
                "budget_abs": budget, "M_Phi": budget / m0,
                "R": R, "beta": [float(b) for b in beta],
                "beta_zero": bool(np.allclose(beta, 0.0)),
            })
            rtag = f"{R:.2f}" if R is not None else "excl"
            print(f"  cfg {cid} size {size}: m_fav {m_fav:.1f} "
                  f"m_qmin {m_qmin:.1f} m_P9 {m_p9:.1f}  R={rtag}")

    gated = [c["R"] for c in cells if c["R"] is not None]
    med_R = float(np.median(gated))
    n_pos = sum(r > 0 for r in gated)
    if med_R >= 0.5 and n_pos >= 10:
        wording = "recoverable by an off-the-shelf predict-then-optimize method"
    elif med_R > 0:
        wording = "partially recoverable"
    else:
        wording = "bridge scoped as positioning identity; adverse result to section 6"

    out = {
        "amendment": "C-1", "date_executed": "2026-07-08",
        "hyperparams": {"k_train": K_TRAIN, "step": STEP, "iters": ITERS,
                        "k_deploy": K_DEPLOY, "features": "standardized C,I,T"},
        "n_new_sims": n_sims,
        "per_cell": cells,
        "n_gated_cells": len(gated), "excluded_cells": 12 - len(gated),
        "median_R": med_R, "n_R_positive": n_pos,
        "locked_wording": wording,
        "runtime_seconds": round(time.time() - t0, 1),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "amendC1_p9_spoplus.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    print(f"\nC-1 P9 SPO+ delegation test: median R = {med_R:.2f}, "
          f"R > 0 in {n_pos}/{len(gated)} gated cells")
    print(f"  locked wording: {wording}")
    print(f"Saved {path}  ({out['runtime_seconds']}s, {n_sims} new sims)")


if __name__ == "__main__":
    main()
