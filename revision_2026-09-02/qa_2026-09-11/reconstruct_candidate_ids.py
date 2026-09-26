"""candidate_id reconstruction for the stored Phase 5 artefacts (2026-09-11) [QA].

The 2026-05-19 Block A / B / C CSVs do not record which candidate wave each
row simulated. Because every draw comes from a registered seed stream
(`experiments_phase5._seed`), the candidate index of every stored row can be
recovered by replaying the sampling RNGs WITHOUT re-simulating. This script
writes one sidecar CSV per block (row_index = 0-based position in the stored
CSV) and verifies the alignment by re-simulating a sample of rows under the
production simulator and comparing with the stored makespans.

Block B caveat: P5 uses the favourable corner of the shared training pass
(taken from the stored Block A label of the same (config, batched, size)
cell); P6 needs the SPO-tree, which is refit from a replayed training pass
(200 M2 simulations per cell). Both are verified by the re-simulation check.

Run:  python revision_2026-09-02/qa_2026-09-11/reconstruct_candidate_ids.py
"""
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PROTO = ROOT / "prototype"
sys.path.insert(0, str(PROTO))

from src import phase5_config as cfg                                   # noqa: E402
from src.demand_patterns import generate_pool                          # noqa: E402
from src.experiments_phase5 import (MODEL_IDX, _seed, fit_predictors,  # noqa: E402
                                    sim_makespan)
from src.wave_policies import (POLICIES, build_candidates,             # noqa: E402
                               corner_positions, materialise)

QA = Path(__file__).resolve().parent
RAW = PROTO / "results" / "raw"
CHECK_ROWS = (0, 1, 199)          # rows re-simulated per (cell, arm/policy)


def _pool(config):
    return generate_pool(config["demand"], config["F"], cfg.ORDER_POOL_SIZE,
                         seed=cfg.SEED_BASE + config["config_id"],
                         **cfg.DEMAND_PARAMS[config["demand"]])


def _verify(stored_rows, ids, cand, pool, config, model, stats):
    """Re-simulate CHECK_ROWS of a 200-row group and compare with stored makespans."""
    for wid in CHECK_ROWS:
        mk = sim_makespan(materialise(cand.iloc[ids[wid]], pool), config, model,
                          random.Random(0))
        stats["checked"] += 1
        if abs(mk - float(stored_rows[wid])) > 1e-9:
            stats["mismatch"] += 1


def block_a(configs):
    df = pd.read_csv(RAW / "mvs_v0_5_phase5_blockA.csv")
    n = cfg.N_PER_ARM
    side, stats, uniq = [], {"M1": {"checked": 0, "mismatch": 0},
                             "M2": {"checked": 0, "mismatch": 0}}, []
    tag = {"abstraction": "M1", "batched": "M2"}
    r = 0
    for config in configs:
        pool = _pool(config)
        for model in cfg.BLOCK_A["models"]:
            for size in cfg.BLOCK_A["sizes"]:
                seed = _seed(config["config_id"], MODEL_IDX[model], size)
                cand = build_candidates(pool, size, cfg.CANDIDATE_POOL, random.Random(seed))
                for ai, arm in enumerate(cfg.BLOCK_A["arms"]):
                    pos = corner_positions(cand, arm)
                    arm_rng = random.Random(seed + 13 * (ai + 1))
                    ids = [int(arm_rng.choice(pos)) for _ in range(n)]
                    grp = df.iloc[r:r + n]
                    assert (grp["config_id"] == config["config_id"]).all() and \
                        (grp["model"] == model).all() and (grp["size"] == size).all() and \
                        (grp["arm"] == arm).all(), f"Block A row order broke at row {r}"
                    _verify(grp["makespan"].to_numpy(float), ids, cand, pool, config,
                            model, stats[tag[model]])
                    uniq.append(len(set(ids)))
                    for j, p in enumerate(ids):
                        side.append({"row_index": r + j, "config_id": config["config_id"],
                                     "model": model, "size": size, "arm": arm,
                                     "candidate_id": p, "cand_seed": seed,
                                     "pool_seed": cfg.SEED_BASE + config["config_id"]})
                    r += n
    assert r == len(df), (r, len(df))
    pd.DataFrame(side).to_csv(RAW / "mvs_v0_5_phase5_blockA_candidate_ids.csv", index=False)
    return {"rows": r, "verify": stats, "unique_per_200_min": min(uniq),
            "unique_per_200_max": max(uniq)}


def block_b(configs, e2):
    df = pd.read_csv(RAW / "mvs_v0_5_phase5_blockB.csv")
    dfA = pd.read_csv(RAW / "mvs_v0_5_phase5_blockA.csv")
    n, model = cfg.N_PER_ARM, cfg.BLOCK_B["model"]
    side, uniq = [], []
    stats = {p: {"checked": 0, "mismatch": 0} for p in POLICIES}
    r = 0
    for config in e2[:cfg.BLOCK_B["n_configs"]]:
        pool = _pool(config)
        for size in cfg.BLOCK_B["sizes"]:
            seed = _seed(config["config_id"], MODEL_IDX[model], size)
            cand = build_candidates(pool, size, cfg.CANDIDATE_POOL, random.Random(seed))
            # favourable corner label as stored by Block A for the same training pass
            fav = dfA[(dfA["config_id"] == config["config_id"]) & (dfA["model"] == model)
                      & (dfA["size"] == size)]["favorable_corner"].iloc[0]
            beta, tree = fit_predictors(cand, pool, config, model, cfg.TRAIN_SAMPLE,
                                        seed + 1)
            refit_fav = (("HC" if beta["beta_C"] < 0 else "LC") + "_"
                         + ("HI" if beta["beta_I"] < 0 else "LI"))
            ctx = {"beta_C": -1.0 if fav.startswith("HC") else 1.0,
                   "beta_I": -1.0 if fav.endswith("HI") else 1.0,
                   "spo_tree": tree, "feature_cols": ("C", "I")}
            for pi, policy in enumerate(POLICIES):
                pol_rng = random.Random(seed + 13 * (pi + 1))
                ids = [int(p) for p in POLICIES[policy](cand, n, pol_rng, ctx)]
                grp = df.iloc[r:r + n]
                assert (grp["config_id"] == config["config_id"]).all() and \
                    (grp["size"] == size).all() and (grp["policy"] == policy).all(), \
                    f"Block B row order broke at row {r}"
                _verify(grp["makespan"].to_numpy(float), ids, cand, pool, config,
                        model, stats[policy])
                uniq.append(len(set(ids)))
                for j, p in enumerate(ids):
                    side.append({"row_index": r + j, "config_id": config["config_id"],
                                 "model": model, "size": size, "policy": policy,
                                 "candidate_id": p, "cand_seed": seed,
                                 "pool_seed": cfg.SEED_BASE + config["config_id"],
                                 "favorable_corner_stored": fav,
                                 "favorable_corner_refit": refit_fav})
                r += n
    assert r == len(df), (r, len(df))
    pd.DataFrame(side).to_csv(RAW / "mvs_v0_5_phase5_blockB_candidate_ids.csv", index=False)
    fav_agree = sum(1 for s in side[::n] if s["favorable_corner_stored"] == s["favorable_corner_refit"])
    return {"rows": r, "verify": stats, "unique_per_200_min": min(uniq),
            "unique_per_200_max": max(uniq),
            "refit_favourable_corner_matches_stored": f"{fav_agree}/{len(side[::n])} policy-cells"}


def block_c(e2):
    df = pd.read_csv(RAW / "mvs_v0_5_phase5_blockC.csv")
    n, size = cfg.N_PER_ARM, cfg.BLOCK_C["sizes"][0]
    side, uniq = [], []
    stats = {"M1": {"checked": 0, "mismatch": 0}, "M2": {"checked": 0, "mismatch": 0}}
    r = 0
    for config in e2[:cfg.BLOCK_C["n_configs"]]:
        pool = _pool(config)
        seed = _seed(config["config_id"], 99, size)
        cand = build_candidates(pool, size, cfg.CANDIDATE_POOL, random.Random(seed))
        for ai, arm in enumerate(cfg.BLOCK_C["arms"]):
            pos = corner_positions(cand, arm)
            arm_rng = random.Random(seed + 13 * (ai + 1))
            ids = [int(arm_rng.choice(pos)) for _ in range(n)]
            grp = df.iloc[r:r + n]
            assert (grp["config_id"] == config["config_id"]).all() and \
                (grp["arm"] == arm).all() and (grp["wave_id"].to_numpy() == range(n)).all(), \
                f"Block C row order broke at row {r}"
            _verify(grp["makespan_M1"].to_numpy(float), ids, cand, pool, config,
                    "abstraction", stats["M1"])
            _verify(grp["makespan_M2"].to_numpy(float), ids, cand, pool, config,
                    "batched", stats["M2"])
            uniq.append(len(set(ids)))
            for j, p in enumerate(ids):
                side.append({"row_index": r + j, "config_id": config["config_id"],
                             "size": size, "arm": arm, "wave_id": j,
                             "candidate_id": p, "cand_seed": seed,
                             "pool_seed": cfg.SEED_BASE + config["config_id"]})
            r += n
    assert r == len(df), (r, len(df))
    pd.DataFrame(side).to_csv(RAW / "mvs_v0_5_phase5_blockC_candidate_ids.csv", index=False)
    return {"rows": r, "verify": stats, "unique_per_200_min": min(uniq),
            "unique_per_200_max": max(uniq)}


def main() -> None:
    configs = cfg.make_config_array()
    e2 = cfg.e2_subset(configs)
    report = {"date": "2026-09-11", "label": "[QA] candidate_id reconstruction by seed replay",
              "check_rows_per_group": list(CHECK_ROWS),
              "note": ("mismatches under M2 are expected at the ~0.27% tie-sensitivity "
                       "rate of the stored artefacts (BUGREPORT-2026-07-08); M1 should "
                       "reproduce exactly")}
    report["blockA"] = block_a(configs)
    print("Block A:", json.dumps(report["blockA"]))
    report["blockB"] = block_b(configs, e2)
    print("Block B:", json.dumps(report["blockB"]))
    report["blockC"] = block_c(e2)
    print("Block C:", json.dumps(report["blockC"]))
    out = QA / "candidate_id_reconstruction_check.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
