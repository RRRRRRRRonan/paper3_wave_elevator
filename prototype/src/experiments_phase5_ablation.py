"""
MVS v0.5 Phase 5 — ablation + P7 optimization-baseline experiments.

Pre-registered as an AMENDMENT (pre-reg §9, 2026-05-19): added before the W6
confirmatory analysis to strengthen the design. These experiments touch none
of the locked H-D1 / H-D2 / H-Policy gates — they are additional analyses.

  run_p7              -- P7 local-search optimizer on the Block B (config,size)
                         cells, so the P5-vs-P7 comparison is cell-matched.
  run_scheme_ablation -- the same candidate pool partitioned three ways
                         (2x2 on C/I, 3x3 on C/I, 2x2x2 on C/I/T) to ablate
                         partition granularity (A4) and the T dimension (A2).

Run:  python -m src.experiments_phase5_ablation
"""
from __future__ import annotations

import random
import time
from pathlib import Path

import numpy as np
import pandas as pd

from src import phase5_config as cfg
from src.demand_patterns import generate_pool
from src.experiments_phase5 import _config_fields, _seed, sim_makespan
from src.wave_policies import (build_candidates, materialise,
                               optimize_wave_localsearch)

RAW_DIR = Path(__file__).resolve().parents[1] / "results" / "raw"

SCHEMES = ["2x2_CI", "3x3_CI", "2x2x2_CIT"]
ABLATION_SIZE = 16          # T-meaningful wave size for the scheme ablation
P7_ITER = 40                # modest local-search budget (a practical optimum)


def _bin(values: np.ndarray, n_bins: int) -> np.ndarray:
    """Assign each value to a quantile bin 0..n_bins-1."""
    qs = [np.quantile(values, i / n_bins) for i in range(1, n_bins)]
    return np.digitize(values, qs)


def scheme_corners(cand: pd.DataFrame, scheme: str) -> dict:
    """{corner_label: row positions} for a partition scheme (plus 'random')."""
    out = {"random": np.arange(len(cand))}
    C, I, T = cand["C"].to_numpy(), cand["I"].to_numpy(), cand["T"].to_numpy()
    if scheme == "2x2_CI":
        axes = [("C", _bin(C, 2)), ("I", _bin(I, 2))]
        grid = [(c, i) for c in range(2) for i in range(2)]
    elif scheme == "3x3_CI":
        axes = [("C", _bin(C, 3)), ("I", _bin(I, 3))]
        grid = [(c, i) for c in range(3) for i in range(3)]
    elif scheme == "2x2x2_CIT":
        axes = [("C", _bin(C, 2)), ("I", _bin(I, 2)), ("T", _bin(T, 2))]
        grid = [(c, i, t) for c in range(2) for i in range(2) for t in range(2)]
    else:
        raise ValueError(f"unknown scheme {scheme!r}")
    for combo in grid:
        mask = np.ones(len(cand), dtype=bool)
        label = []
        for (name, binned), b in zip(axes, combo):
            mask &= (binned == b)
            label.append(f"{name}{b}")
        pos = np.where(mask)[0]
        out["_".join(label)] = pos if len(pos) else np.arange(len(cand))
    return out


def run_p7(configs, sizes, n_per_arm, n_iter) -> pd.DataFrame:
    """P7 local-search reference on each (config, size); model fixed = batched."""
    rows = []
    for config in configs:
        pool = generate_pool(config["demand"], config["F"], cfg.ORDER_POOL_SIZE,
                             seed=cfg.SEED_BASE + config["config_id"],
                             **cfg.DEMAND_PARAMS[config["demand"]])
        for size in sizes:
            seed = _seed(config["config_id"], 88, size)
            search_rng = random.Random(seed)
            sim_rng = random.Random(seed + 1)

            def sim_fn(w, _c=config, _r=sim_rng):
                return sim_makespan(w, _c, "batched", _r)

            for wid in range(n_per_arm):
                mk, _ = optimize_wave_localsearch(pool, size, sim_fn,
                                                  search_rng, n_iter)
                rows.append({**_config_fields(config), "size": size,
                             "policy": "P7_localsearch", "wave_id": wid,
                             "makespan": mk})
    return pd.DataFrame(rows)


def run_scheme_ablation(configs, size, n_per_arm, cand_n) -> pd.DataFrame:
    """One candidate pool per config, partitioned by 3 schemes; model = batched."""
    rows = []
    for config in configs:
        pool = generate_pool(config["demand"], config["F"], cfg.ORDER_POOL_SIZE,
                             seed=cfg.SEED_BASE + config["config_id"],
                             **cfg.DEMAND_PARAMS[config["demand"]])
        seed = _seed(config["config_id"], 77, size)
        cand = build_candidates(pool, size, cand_n, random.Random(seed))
        sim_rng = random.Random(seed + 1)
        for si, scheme in enumerate(SCHEMES):
            for ci, (corner, pos) in enumerate(scheme_corners(cand, scheme).items()):
                arm_rng = random.Random(seed + 1000 * (si + 1) + 7 * (ci + 1))
                for _ in range(n_per_arm):
                    p = int(arm_rng.choice(pos))
                    mk = sim_makespan(materialise(cand.iloc[p], pool),
                                      config, "batched", sim_rng)
                    rows.append({**_config_fields(config), "size": size,
                                 "scheme": scheme, "corner": corner,
                                 "makespan": mk})
    return pd.DataFrame(rows)


def main() -> None:
    configs = cfg.e2_subset(cfg.make_config_array())[:cfg.BLOCK_B["n_configs"]]
    t0 = time.time()
    print("Phase 5 ablation + P7  (pre-reg §9 amendment)")
    dfP7 = run_p7(configs, cfg.BLOCK_B["sizes"], cfg.N_PER_ARM, P7_ITER)
    dfS = run_scheme_ablation(configs, ABLATION_SIZE, cfg.N_PER_ARM,
                              cfg.CANDIDATE_POOL)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    dfP7.to_csv(RAW_DIR / "mvs_v0_5_phase5_ablation_P7.csv", index=False)
    dfS.to_csv(RAW_DIR / "mvs_v0_5_phase5_ablation_scheme.csv", index=False)
    print(f"  P7: {len(dfP7)} optimised waves "
          f"| scheme ablation: {len(dfS)} sims")
    print(f"  done in {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
