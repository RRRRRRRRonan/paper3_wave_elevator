"""
S1-12 (AMEND-2026-09-26-S1B): the B-5 event-driven cross-check rerun under the
corrected DES-M2 boarding rule (src/des_evaluator.py, b5_compat=False).

Same design as AMEND-2026-07-08-B B-5: configurations 1, 7, 11; size 16; the
Block C candidate pools `_seed(cid, 99, 16)`; the random arm for all three
and the four corners for configuration 7; 200 waves per arm drawn exactly as
in b5_des_crossvalidation.py. Closed-form side: the current simulator.

Before anything else (real mode) the script re-runs the wave draws under
b5_compat=True and checks that the mean DES-M2 per configuration equals the
stored B-5 value; if not, it stops (the draws would not be the B-5 waves).
Output: prototype/results/v0_5_phase5_S1-12_b5_boardfirst.json (S1B general
rule 2; the stored B-5 output is never touched).

Run from prototype/:  python -m src.experiments_S1_b5_rerun [--selftest]
"""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

from src import phase5_config as cfg
from src.demand_patterns import generate_pool
from src.des_evaluator import des_makespan, wave_to_tuples
from src.experiments_phase5 import _seed
from src.experiments_phase6 import _write_json, code_tree_sha256
from src.registration_guard import (REGISTRATIONS, TOY_SEED_BASE, require_signed,
                                    scratch_dir, sha256_file)
from src.simulator import simulate_wave
from src.wave_policies import build_candidates, corner_positions, materialise

REPO = Path(__file__).resolve().parents[2]
B5_DIR = REPO / "revision_2026-07-08" / "tier2_analysis" / "outputs"
ARMS = ["random", "HC_HI", "HC_LI", "LC_HI", "LC_LI"]
TOL = 1e-9


def draw_waves(config, n_per_arm, cand_n):
    cid = config["config_id"]
    pool = generate_pool(config["demand"], config["F"], cfg.ORDER_POOL_SIZE,
                         seed=cfg.SEED_BASE + cid,
                         **cfg.DEMAND_PARAMS[config["demand"]])
    seed = _seed(cid, 99, 16)
    cand = build_candidates(pool, 16, cand_n, random.Random(seed))
    arms = ["random"] if cid != 7 else ARMS
    out = {}
    for ai, arm in enumerate(ARMS):
        if arm not in arms:
            continue
        pos = corner_positions(cand, arm)
        arm_rng = random.Random(seed + 13 * (ai + 1))
        out[arm] = [materialise(cand.iloc[int(arm_rng.choice(pos))], pool)
                    for _ in range(n_per_arm)]
    return out


def evaluate(config, waves, b5_compat):
    A, E = config["n_amrs"], config["n_elevators"]
    rows = []
    for w in waves:
        t = wave_to_tuples(w)
        rows.append({
            "cf_M1": simulate_wave(w, n_amrs=A, n_elevators=E, capacity=cfg.CAPACITY),
            "cf_M2": simulate_wave(w, n_amrs=A, n_elevators=E, capacity=cfg.CAPACITY,
                                   batched=True),
            "des_M1": des_makespan(t, A, E, cfg.CAPACITY, "M1", b5_compat=b5_compat),
            "des_M2": des_makespan(t, A, E, cfg.CAPACITY, "M2", b5_compat=b5_compat)})
    return rows


def summarise(config, arm_rows):
    rnd = arm_rows["random"]
    col = {k: np.array([r[k] for r in rnd]) for k in rnd[0]}
    res = {"rho_M1": float(spearmanr(col["cf_M1"], col["des_M1"]).statistic),
           "rho_M2": float(spearmanr(col["cf_M2"], col["des_M2"]).statistic),
           "des_dominance": float(np.mean(col["des_M2"] >= col["des_M1"] - TOL)),
           "cf_mean_M2": float(col["cf_M2"].mean()),
           "des_mean_M2": float(col["des_M2"].mean())}
    if config["config_id"] == 7 and len(arm_rows) == len(ARMS):
        m0 = float(np.median([r["des_M2"] for r in rnd]))
        mq = {a: float(np.median([r["des_M2"] for r in arm_rows[a]]))
              for a in ARMS[1:]}
        res["config7_des"] = {"des_H_up": (max(mq.values()) - m0) / m0,
                              "des_S_or": (m0 - min(mq.values())) / m0,
                              "des_m0": m0, "des_corner_medians": mq}
    return res


def main(argv=None) -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    require_signed("S1B", args.selftest)
    n_per_arm, cand_n = cfg.N_PER_ARM, cfg.CANDIDATE_POOL
    if args.selftest:
        cfg.SEED_BASE = TOY_SEED_BASE          # toy seeds only
        n_per_arm, cand_n = 12, 150
    configs = {c["config_id"]: c for c in cfg.make_config_array()}
    stored = None
    if not args.selftest:
        stored = json.loads((B5_DIR / "b5_des_crossvalidation.json")
                            .read_text("utf-8"))["per_config"]
    per_config, all_dom = {}, []
    for cid in (1, 7, 11):
        waves = draw_waves(configs[cid], n_per_arm, cand_n)
        # Reproduction pass under the old boarding rule (S1B, S1-12 Design):
        # its rows are kept, and their Spearman rho against the current
        # closed-form values is the tie-break-only column, so the boarding
        # effect is read as the difference to the b5_compat=False rho.
        chk = evaluate(configs[cid], waves["random"], b5_compat=True)
        if stored is not None:              # reproduction check of the draws
            mean_old = float(np.mean([r["des_M2"] for r in chk]))
            if abs(mean_old - stored[str(cid)]["des_mean_M2"]) > 1e-6:
                raise SystemExit(f"S1-12 STOP: config {cid} B-5 reproduction "
                                 f"failed ({mean_old} vs "
                                 f"{stored[str(cid)]['des_mean_M2']})")
        arm_rows = {a: evaluate(configs[cid], w, b5_compat=False)
                    for a, w in waves.items()}
        per_config[cid] = summarise(configs[cid], arm_rows)
        col = {k: np.array([r[k] for r in chk]) for k in chk[0]}
        per_config[cid]["rho_M1_tiebreak_only"] = float(
            spearmanr(col["cf_M1"], col["des_M1"]).statistic)
        per_config[cid]["rho_M2_tiebreak_only"] = float(
            spearmanr(col["cf_M2"], col["des_M2"]).statistic)
        per_config[cid]["des_mean_M2_b5_rule"] = float(col["des_M2"].mean())
        all_dom += [r["des_M2"] >= r["des_M1"] - TOL for r in arm_rows["random"]]
    rho_min = min(min(v["rho_M1"], v["rho_M2"]) for v in per_config.values())
    out = {"item": "S1-12", "boarding_rule": "board-first (b5_compat=False)",
           "selftest": args.selftest, "code_tree_sha256": code_tree_sha256(),
           "registration_S1B_sha256": sha256_file(REGISTRATIONS["S1B"]),
           "stored_B5_sha256": sha256_file(B5_DIR / "b5_des_crossvalidation.json"),
           "per_config": per_config, "min_spearman_rho": rho_min,
           "des_pooled_dominance": float(np.mean(all_dom)),
           "gates_for_reference_only": {
               "rho_ge_09_every_config": bool(rho_min >= 0.9),
               "des_dominance_ge_090": bool(np.mean(all_dom) >= 0.90)},
           "note": "B-5 verdict of record unchanged (reporting rule of S1-12)"}
    results = Path(__file__).resolve().parents[1] / "results"
    path = (scratch_dir() / "selftest_v0_5_phase5_S1-12_b5_boardfirst.json"
            if args.selftest else results / "v0_5_phase5_S1-12_b5_boardfirst.json")
    _write_json(out, path)
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
