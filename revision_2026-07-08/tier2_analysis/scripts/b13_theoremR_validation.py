"""
Amendment B-13 (2026-07-08): Theorem R validation on nested covering partitions.

Protocol EXACTLY as registered in AMEND-2026-07-08-B13_theoremR.md (locked
before execution): 6 Block C configs (E=2), size 16, matched M1/M2 on a
2,000-wave uniform sample from the Block C candidate pool; covering
partitions Q1 (2x2 median) nested in Q2 (4x4 quartile); tercile 3x3 as a
non-nested comparison; predictions P1-P3 with the bootstrap adjudication
rule; seed 20260708.
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
SEED = 20260708
N_SAMPLE = 2000
N_BOOT = 1000
MODELS = ["abstraction", "batched"]
MODEL_TAG = {"abstraction": "M1", "batched": "M2"}


def partition_labels(vals: np.ndarray, qs: list) -> np.ndarray:
    """Bin values by the given quantile boundaries (covering)."""
    edges = np.quantile(vals, qs)
    return np.searchsorted(edges, vals, side="right")


def cell_stats(labels_c, labels_i, mks):
    med = {}
    sizes = {}
    for c in np.unique(labels_c):
        for i in np.unique(labels_i):
            mask = (labels_c == c) & (labels_i == i)
            if mask.sum() > 0:
                med[(int(c), int(i))] = float(np.median(mks[mask]))
                sizes[(int(c), int(i))] = int(mask.sum())
    return med, sizes


def decomp(med: dict, m0: float):
    mx, mn = max(med.values()), min(med.values())
    return (mx - m0) / m0, (m0 - mn) / m0        # H_up, S_or


def main() -> None:
    t0 = time.time()
    configs = [c for c in cfg.make_config_array()
               if c["config_id"] in (1, 3, 5, 7, 9, 11)]
    rng_sample = np.random.default_rng(SEED)

    # ---- simulate the matched sample --------------------------------------
    frames = []
    for config in configs:
        cid = config["config_id"]
        pool = generate_pool(config["demand"], config["F"],
                             cfg.ORDER_POOL_SIZE, seed=cfg.SEED_BASE + cid,
                             **cfg.DEMAND_PARAMS[config["demand"]])
        seed = _seed(cid, 99, 16)                 # model-independent Block C seed
        cand = build_candidates(pool, 16, cfg.CANDIDATE_POOL,
                                random.Random(seed))
        idx = rng_sample.choice(len(cand), size=N_SAMPLE, replace=False)
        for i, p in enumerate(idx):
            row = cand.iloc[int(p)]
            wave = materialise(row, pool)
            rec = {"config_id": cid, "C": float(row["C"]),
                   "I": float(row["I"]), "T": float(row["T"])}
            for model in MODELS:
                rec[f"makespan_{MODEL_TAG[model]}"] = sim_makespan(
                    wave, config, model, random.Random(seed + 500_000 + i))
            frames.append(rec)
    df = pd.DataFrame(frames)
    n_sims = len(df) * len(MODELS)
    print(f"simulated {n_sims} matched makespans in {time.time()-t0:.1f}s")

    # ---- partitions and checks --------------------------------------------
    results, checks = [], []
    rng_boot = np.random.default_rng(SEED)
    for cid, g in df.groupby("config_id"):
        C, I = g["C"].to_numpy(), g["I"].to_numpy()
        labs = {
            "Q1_2x2": (partition_labels(C, [0.5]), partition_labels(I, [0.5])),
            "Q2_4x4": (partition_labels(C, [0.25, 0.5, 0.75]),
                       partition_labels(I, [0.25, 0.5, 0.75])),
            "T_3x3": (partition_labels(C, [1/3, 2/3]),
                      partition_labels(I, [1/3, 2/3])),
        }
        for model in MODELS:
            mks = g[f"makespan_{MODEL_TAG[model]}"].to_numpy(float)
            m0 = float(np.median(mks))
            vals = {}
            for name, (lc, li) in labs.items():
                med, sizes = cell_stats(lc, li, mks)
                H, S = decomp(med, m0)
                thin = sum(1 for v in sizes.values() if v < 30)
                vals[name] = {"H_up": H, "S_or": S, "UB": H + S,
                              "n_cells": len(med), "thin_cells": thin}
                results.append({"config_id": int(cid),
                                "model": MODEL_TAG[model], "partition": name,
                                "m0": m0, **vals[name]})

            # bootstrap distribution of the two nested differences +
            # the four levels (within-cell resampling, m0 from full resample)
            boot = {"dH": np.empty(N_BOOT), "dS": np.empty(N_BOOT),
                    "H1": np.empty(N_BOOT), "H2": np.empty(N_BOOT)}
            cellsets = {}
            for name in ("Q1_2x2", "Q2_4x4"):
                lc, li = labs[name]
                cellsets[name] = [mks[(lc == c) & (li == i)]
                                  for c in np.unique(lc)
                                  for i in np.unique(li)
                                  if ((lc == c) & (li == i)).sum() > 0]
            for b in range(N_BOOT):
                m0b = float(np.median(rng_boot.choice(mks, len(mks))))
                hh = {}
                for name in ("Q1_2x2", "Q2_4x4"):
                    meds = [float(np.median(rng_boot.choice(cell, len(cell))))
                            for cell in cellsets[name]]
                    hh[name] = ((max(meds) - m0b) / m0b,
                                (m0b - min(meds)) / m0b)
                boot["dH"][b] = hh["Q2_4x4"][0] - hh["Q1_2x2"][0]
                boot["dS"][b] = hh["Q2_4x4"][1] - hh["Q1_2x2"][1]
                boot["H1"][b] = hh["Q1_2x2"][0]
                boot["H2"][b] = hh["Q2_4x4"][0]

            def adjudicate(value_ok: bool, boot_arr, direction=1):
                """direction=1: predicted >= 0."""
                if value_ok:
                    return "pass"
                lo, hi = np.percentile(boot_arr * direction, [2.5, 97.5])
                return "noise" if hi >= 0 else "FAIL"

            H1, S1 = vals["Q1_2x2"]["H_up"], vals["Q1_2x2"]["S_or"]
            H2, S2 = vals["Q2_4x4"]["H_up"], vals["Q2_4x4"]["S_or"]
            checks.append({"config_id": int(cid), "model": MODEL_TAG[model],
                           "P1_Hup_Q1_nonneg": adjudicate(H1 >= 0, boot["H1"]),
                           "P1_Hup_Q2_nonneg": adjudicate(H2 >= 0, boot["H2"]),
                           "P2_Hup_monotone": adjudicate(H2 >= H1, boot["dH"]),
                           "P3_Sor_monotone": adjudicate(S2 >= S1, boot["dS"]),
                           "tercile_between": bool(
                               min(H1, H2) <= vals["T_3x3"]["H_up"]
                               <= max(H1, H2))})

    # ---- verdicts ----------------------------------------------------------
    def count(key):
        return {v: sum(1 for c in checks if c[key] == v)
                for v in ("pass", "noise", "FAIL")}

    summary = {k: count(k) for k in
               ("P1_Hup_Q1_nonneg", "P1_Hup_Q2_nonneg",
                "P2_Hup_monotone", "P3_Sor_monotone")}
    n_terc_inside = sum(c["tercile_between"] for c in checks)

    out = {
        "amendment": "B-13", "date_executed": "2026-07-08", "seed": SEED,
        "n_sims": n_sims, "n_sample_per_config": N_SAMPLE,
        "protocol": "AMEND-2026-07-08-B13_theoremR.md (locked before run)",
        "per_cell": results, "checks": checks, "check_summary": summary,
        "tercile_between_nest_levels": f"{n_terc_inside}/12",
        "runtime_seconds": round(time.time() - t0, 1),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "b13_theoremR_validation.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)

    print("\nB-13 Theorem R validation")
    print(f"{'cfg':>4} {'model':>6} {'H_up(2x2)':>10} {'H_up(4x4)':>10} "
          f"{'S_or(2x2)':>10} {'S_or(4x4)':>10} {'H(3x3)':>8}")
    by = {(r["config_id"], r["model"], r["partition"]): r for r in results}
    for cid in sorted({r["config_id"] for r in results}):
        for m in ("M1", "M2"):
            q1 = by[(cid, m, "Q1_2x2")]
            q2 = by[(cid, m, "Q2_4x4")]
            t3 = by[(cid, m, "T_3x3")]
            print(f"{cid:>4} {m:>6} {q1['H_up']:>10.4f} {q2['H_up']:>10.4f} "
                  f"{q1['S_or']:>10.4f} {q2['S_or']:>10.4f} "
                  f"{t3['H_up']:>8.4f}")
    print("\ncheck summary (12 cells):")
    for k, v in summary.items():
        print(f"  {k}: pass {v['pass']}, noise {v['noise']}, FAIL {v['FAIL']}")
    print(f"  tercile H_up inside nest bracket: {n_terc_inside}/12 "
          "(descriptive, no prediction)")
    print(f"\nSaved {path}  ({out['runtime_seconds']}s total)")


if __name__ == "__main__":
    main()
