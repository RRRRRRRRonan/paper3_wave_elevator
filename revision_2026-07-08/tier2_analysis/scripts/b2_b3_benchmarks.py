"""
Amendments B-2 (enumeration benchmark) and B-3 (P8 savings heuristic),
2026-07-08. Protocols and dated variant notes in
AMEND-2026-07-08-B_deferred_experiments.md (locked before execution).
"""
from __future__ import annotations

import json
import random
import sys
import time
from collections import Counter
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
RES = ROOT / "prototype" / "results"


def enumerate_pool(config, size, model="batched"):
    """Simulate EVERY candidate wave once; return sorted makespans + best."""
    cid = config["config_id"]
    pool = generate_pool(config["demand"], config["F"], cfg.ORDER_POOL_SIZE,
                         seed=cfg.SEED_BASE + cid,
                         **cfg.DEMAND_PARAMS[config["demand"]])
    seed = _seed(cid, 1, size)
    cand = build_candidates(pool, size, cfg.CANDIDATE_POOL,
                            random.Random(seed))
    rng = random.Random(seed + 424242)      # unused by deterministic models
    mks = np.array([sim_makespan(materialise(row, pool), config, model, rng)
                    for _, row in cand.iterrows()])
    return cand, pool, mks


def run_b2() -> dict:
    configs = {c["config_id"]: c for c in cfg.make_config_array()}
    blockB = json.loads((RES / "v0_5_phase5_blockB.json").read_text(encoding="utf-8"))
    cellB = {(c["config_id"], c["size"]): c for c in blockB["per_cell"]}
    dfA = pd.read_csv(RAW / "mvs_v0_5_phase5_blockA.csv")

    rows = []
    for cid in (0, 1):
        config = configs[cid]
        _, _, mks = enumerate_pool(config, 8)
        best = float(mks.min())
        med_pool = float(np.median(mks))
        g = dfA[(dfA["config_id"] == cid) & (dfA["model"] == "batched")
                & (dfA["size"] == 8)]
        fav = g["favorable_corner"].iloc[0]
        m_fav = float(np.median(g[g["arm"] == fav]["makespan"]))
        m0 = float(np.median(g[g["arm"] == "random"]["makespan"]))
        row = {"config_id": cid, "E": config["n_elevators"],
               "pool_optimum": best, "pool_median": med_pool,
               "m0_random": m0,
               "P5_proxy_favarm_median": m_fav,
               "gap_P5_pct": 100 * (m_fav - best) / best}
        if (cid, 8) in cellB:
            c = cellB[(cid, 8)]
            row["P5_blockB"] = c["P5_phi"]
            row["P6_blockB"] = c["P6_spo_tree"]
            row["P7_blockB"] = c["P7_localsearch"]
            row["gap_P5_blockB_pct"] = 100 * (c["P5_phi"] - best) / best
            row["gap_P6_pct"] = 100 * (c["P6_spo_tree"] - best) / best
            row["gap_P7_pct"] = 100 * (c["P7_localsearch"] - best) / best
        rows.append(row)
    return {"cells": rows,
            "note": ("pool optimum over the full 3,000-candidate pool "
                     "(dated note in AMEND-B); policy values are medians of "
                     "200 released waves, the optimum is a single wave: the "
                     "gap anchors scale, it is not a like-for-like ratio")}


def run_b3() -> dict:
    configs = [c for c in cfg.make_config_array()
               if c["config_id"] in (1, 3, 5, 7, 9, 11)]
    blockB = json.loads((RES / "v0_5_phase5_blockB.json").read_text(encoding="utf-8"))
    cellB = {(c["config_id"], c["size"]): c for c in blockB["per_cell"]}
    POLS = ["P0_random", "P1_dest_cluster", "P2_cardinality", "P3_dir_balanced",
            "P4_temporal", "P5_phi", "P6_spo_tree", "P7_localsearch"]

    def p8_score(wave_orders):
        travel = sum(abs(o.source_floor - o.dest_floor) for o in wave_orders)
        groups = Counter((o.source_floor, o.dest_floor) for o in wave_orders)
        savings = sum((n // 2) * abs(s - d) for (s, d), n in groups.items())
        dsts = [o.dest_floor for o in wave_orders]
        return travel - savings + 0.5 * (max(dsts) - min(dsts))

    cells = []
    for config in configs:
        cid = config["config_id"]
        pool = generate_pool(config["demand"], config["F"],
                             cfg.ORDER_POOL_SIZE, seed=cfg.SEED_BASE + cid,
                             **cfg.DEMAND_PARAMS[config["demand"]])
        for size in (8, 30):
            seed = _seed(cid, 1, size)
            cand = build_candidates(pool, size, cfg.CANDIDATE_POOL,
                                    random.Random(seed))
            scores = np.array([p8_score(materialise(row, pool).orders)
                               for _, row in cand.iterrows()])
            pick = np.argsort(scores, kind="stable")[:cfg.N_PER_ARM]
            sim_rng = random.Random(seed + 2003 + 9)
            mks = [sim_makespan(materialise(cand.iloc[int(p)], pool),
                                config, "batched", sim_rng) for p in pick]
            m_p8 = float(np.median(mks))
            ref = cellB[(cid, size)]
            cells.append({"config_id": cid, "size": size, "m_P8": m_p8,
                          **{p: ref[p] for p in POLS}})

    wins = {p: sum(c["m_P8"] < c[p] for c in cells) for p in POLS}
    grand = {p: float(np.mean([c[p] for c in cells])) for p in POLS}
    grand["P8"] = float(np.mean([c["m_P8"] for c in cells]))
    return {"per_cell": cells, "P8_wins_vs": {p: f"{w}/12"
                                              for p, w in wins.items()},
            "grand_mean_median": grand}


def main() -> None:
    t0 = time.time()
    b2 = run_b2()
    print("B-2 enumeration benchmark (pool optimum, size 8, M2):")
    for r in b2["cells"]:
        extra = (f"  P5(B) +{r['gap_P5_blockB_pct']:.1f}%  "
                 f"P6 +{r['gap_P6_pct']:.1f}%  P7 +{r['gap_P7_pct']:.1f}%"
                 if "P7_blockB" in r else "")
        print(f"  cfg {r['config_id']} (E={r['E']}): optimum "
              f"{r['pool_optimum']:.0f}, random median {r['m0_random']:.0f}, "
              f"P5(favarm) +{r['gap_P5_pct']:.1f}%{extra}")
    b3 = run_b3()
    print("\nB-3 P8 savings heuristic (Block B protocol, 12 cells):")
    print(f"  grand means: P8 {b3['grand_mean_median']['P8']:.1f} | " +
          " | ".join(f"{p.split('_')[0]} {v:.1f}"
                     for p, v in b3["grand_mean_median"].items()
                     if p != "P8"))
    print(f"  P8 wins vs: {b3['P8_wins_vs']}")

    out = {"amendments": "B-2 + B-3", "date_executed": "2026-07-08",
           "B2": b2, "B3": b3,
           "runtime_seconds": round(time.time() - t0, 1)}
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "b2_b3_benchmarks.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    print(f"\nSaved {path}  ({out['runtime_seconds']}s)")


if __name__ == "__main__":
    main()
