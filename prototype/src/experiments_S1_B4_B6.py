"""
S1-4 / S1-5 -- Execution of AMEND-B B-4 (robustness battery) and B-6(ii)
(candidate/order-pool sensitivity), as registered by the 2026-09-26 execution
note.

Registration:
  revision_2026-09-26_ijpr/amendments/AMEND-2026-09-26-S1C_execution_note_B4_B6.md
  (adds no design/gate/reporting rule of its own -- it fixes two previously
  unspecified execution details and points at the ORIGINAL signed design in
  revision_2026-07-08/amendments/AMEND-2026-07-08-B_deferred_experiments.md,
  sections B-4 and B-6(ii)).
Guard key: "S1C" (author_signoff of the EXECUTION NOTE is
"PENDING (acknowledgement only; the designs and gates were signed on
2026-07-08)" as of 2026-09-26 -- so even though B-4/B-6's own DESIGN was
signed 2026-07-08, `registration_guard.require_signed("S1C")` reads the
EXECUTION NOTE's own front matter, which is still PENDING, and stops. This
is the guard key the task brief specifies for S1-4/S1-5.

S1-4 (B-4): directional switch penalty 3s, heterogeneous capacities [1, 3],
service_sigma in {0.2, 0.5}; matched waves on the 6 Block C configs via
`_seed(cid, 99, 16)`; per-wave M2>=M1 rate per variant + Hedge/DRO agreement
per config; gate >= 90% average and >= 80% worst cell per variant.

S1-5 (B-6(ii)): Block A on configs 1 and 7, one factor at a time around the
default (candidate pool 3,000, order pool 600): candidate pool 1,500 and 6,000
at order pool 600, order pool 300 and 1,200 at candidate pool 3,000; each
(configuration, model, size) cell compared with its own default; pool
robustness claimed only if at least 5/6 of the 32 (cell, setting) pairs keep
the favourable corner, q_max, and q_min (execution note S1C, item 2).

Real mode never executes tonight: `require_signed("S1C")` stops the script
first. Self-test mode patches `phase5_config.SEED_BASE` to
`registration_guard.TOY_SEED_BASE`, uses tiny configs/n_per_arm/pool sizes,
and writes only to registration_guard.scratch_dir().

Run:
  python -m src.experiments_S1_B4_B6             # stops at the guard
  python -m src.experiments_S1_B4_B6 --selftest  # toy run to scratch
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd

from src import phase5_config as cfg
from src.analysis_phase5_blockA import CORNERS, decompose
from src.demand_patterns import generate_pool
from src.experiments_phase5 import _config_fields, _seed, run_corner_block
from src.experiments_S1_blockC_ext import blockC_style_unit
from src.registration_guard import TOY_SEED_BASE, require_signed, scratch_dir
from src.simulator import simulate_wave
from src.wave_policies import build_candidates, corner_positions, materialise

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RAW_DIR = RESULTS_DIR / "raw"
REG_PATH = (Path(__file__).resolve().parents[2] / "revision_2026-09-26_ijpr"
            / "amendments" / "AMEND-2026-09-26-S1C_execution_note_B4_B6.md")
B4_DESIGN_PATH = (Path(__file__).resolve().parents[2] / "revision_2026-07-08"
                 / "amendments" / "AMEND-2026-07-08-B_deferred_experiments.md")

ARMS = ["random"] + CORNERS
HETEROGENEOUS_CAPACITIES = [1, 3]     # S1C note item 2: smaller cap first
DIR_SWITCH_PENALTY = 3.0
SERVICE_SIGMAS = [0.2, 0.5]
VARIANTS = (["directional", "heterogeneous"]
           + [f"service_sigma_{s}" for s in SERVICE_SIGMAS])
BLOCK_C_SIZE = 16


def _sha256_file(path: Path) -> str:
    """Line-ending-normalized SHA-256 (the guard's definition), so
    recorded hashes match MANIFEST_SIGNED.json."""
    from src.registration_guard import sha256_file
    return sha256_file(path)


# ==========================================================================
# S1-4 (B-4): robustness battery
# ==========================================================================

def _sim_variant(wave, config: dict, variant: str, model: str,
                 rng: random.Random) -> float:
    """M1/M2 makespan under one B-4 variant.

    REGISTRATION NOTE (experiments_S1_B4_B6.py, _sim_variant): B-4's design
    names M1 ("the same variant parameters where the simulator supports it")
    without saying what M1 becomes for the "directional" and "heterogeneous"
    variants specifically. `ElevatorPoolDirectional` and
    `ElevatorPoolBatchedHeterogeneous` are both extensions of the BATCHED
    family only (src/simulator.py); `ElevatorPool` (the M1 throughput
    abstraction) has no direction-switch-penalty parameter and no per-slot
    heterogeneous-capacity parameter at all -- there is no simulator feature
    to give M1 for these two variants, and the task's own instructions say
    "do not invent new simulator features." Implemented literally: for
    "directional" and "heterogeneous", M1 is the ORDINARY throughput
    abstraction at the Block C baseline capacity (unchanged from the D2-a
    comparison), and only M2 carries the variant; the robustness question
    this measures is "does the D2-a M1<=M2 ordering survive M2 becoming
    more realistic", not a parameter-matched M1-vs-M2 pair. For
    "service_sigma", `service_sigma` IS a simulate_wave parameter independent
    of `batched`, so both M1 and M2 genuinely carry the SAME variant
    parameter, and the comparison is a true matched pair.
    """
    kw = dict(n_amrs=config["n_amrs"], n_elevators=config["n_elevators"],
             capacity=cfg.CAPACITY, rng=rng)
    if variant == "directional":
        if model == "M1":
            return simulate_wave(wave, batched=False, **kw)
        return simulate_wave(wave, directional=True,
                            dir_switch_penalty=DIR_SWITCH_PENALTY, **kw)
    if variant == "heterogeneous":
        if model == "M1":
            return simulate_wave(wave, batched=False, **kw)
        kw2 = dict(kw)
        kw2.pop("capacity")
        return simulate_wave(wave, heterogeneous_capacities=
                            HETEROGENEOUS_CAPACITIES, **kw2)
    if variant.startswith("service_sigma"):
        sigma = float(variant.rsplit("_", 1)[1])
        return simulate_wave(wave, batched=(model == "M2"),
                            service_sigma=sigma, **kw)
    raise ValueError(f"unknown variant {variant!r}")


def run_variant(configs: List[dict], variant: str, n_per_arm: int,
                cand_n: int) -> pd.DataFrame:
    rows = []
    for config in configs:
        pool = generate_pool(config["demand"], config["F"], cfg.ORDER_POOL_SIZE,
                             seed=cfg.SEED_BASE + config["config_id"],
                             **cfg.DEMAND_PARAMS[config["demand"]])
        seed = _seed(config["config_id"], 99, BLOCK_C_SIZE)   # Block C convention
        cand = build_candidates(pool, BLOCK_C_SIZE, cand_n, random.Random(seed))
        for ai, arm in enumerate(ARMS):
            pos = corner_positions(cand, arm)
            arm_rng = random.Random(seed + 13 * (ai + 1))
            for wid in range(n_per_arm):
                p = int(arm_rng.choice(pos))
                wave = materialise(cand.iloc[p], pool)
                # common random numbers: M1 and M2 draw the same service-noise
                # sequence (two draws per order, same FIFO order), so the
                # per-wave M1/M2 comparison isolates the elevator model
                # (execution note AMEND-2026-09-26-S1C, item 2)
                rng1 = random.Random(seed + 800_003 + 31 * wid)
                rng2 = random.Random(seed + 800_003 + 31 * wid)
                m1 = _sim_variant(wave, config, variant, "M1", rng1)
                m2 = _sim_variant(wave, config, variant, "M2", rng2)
                rows.append({**_config_fields(config), "variant": variant,
                           "arm": arm, "wave_id": wid, "candidate_id": p,
                           "cand_seed": seed, "makespan_M1": m1,
                           "makespan_M2": m2})
    return pd.DataFrame(rows)


def summarize_variant(df: pd.DataFrame) -> dict:
    cell_rows = []
    for (cid, corner), g in df[df["arm"] != "random"].groupby(["config_id", "arm"]):
        t1 = g["makespan_M1"].to_numpy(float)
        t2 = g["makespan_M2"].to_numpy(float)
        cell_rows.append({"config_id": int(cid), "corner": corner,
                        "perwave_dom": float(np.mean(t2 >= t1))})
    avg = float(np.mean([c["perwave_dom"] for c in cell_rows]))
    worst = float(np.min([c["perwave_dom"] for c in cell_rows]))
    gate = bool(avg >= 0.90 and worst >= 0.80)
    hedge_dro = []
    for cid, g in df.groupby("config_id"):
        u = blockC_style_unit(g)
        hedge_dro.append({"config_id": int(cid),
                        "c_star_Hedge_mean": u["c_star_Hedge_mean"],
                        "c_star_DRO": u["c_star_DRO"],
                        "collapse": u["collapse_mean"]})
    return {"per_cell": cell_rows, "avg_dominance": avg, "worst_cell": worst,
           "gate_pass": gate, "hedge_dro_per_config": hedge_dro,
           "n_collapse": sum(h["collapse"] for h in hedge_dro),
           "n_configs": len(hedge_dro)}


def run_s1_4(configs: List[dict], n_per_arm: int, cand_n: int,
            selftest: bool) -> dict:
    results = {}
    for variant in VARIANTS:
        df = run_variant(configs, variant, n_per_arm, cand_n)
        out_dir = scratch_dir() if selftest else RAW_DIR
        if not selftest:
            RAW_DIR.mkdir(parents=True, exist_ok=True)
        csv_path = out_dir / f"mvs_v0_5_phase5_S1-4_B4_{variant}.csv"
        df.to_csv(csv_path, index=False)
        summary = summarize_variant(df)
        summary["csv_path"] = str(csv_path)
        results[variant] = summary
    overall_gate = all(r["gate_pass"] for r in results.values())
    return {"variants": results, "all_variants_pass_gate": overall_gate,
           "n_block_c_configs": len(configs)}


# ==========================================================================
# S1-5 (B-6(ii)): candidate/order-pool sensitivity
# ==========================================================================

# S1-5 design, fixed by the execution note AMEND-2026-09-26-S1C (item 2), which
# replaces the helper agent's paired and config-pooled reading (2026-09-26):
# one factor at a time around the Phase 5 default (candidate pool 3,000, order
# pool 600): candidate pool 1,500 and 6,000 at order pool 600; order pool 300
# and 1,200 at candidate pool 3,000. Each (configuration, model, size) cell is
# compared with its OWN default setting, recomputed in the same run; a
# (cell, setting) pair is stable when the favourable corner, q_max, and q_min
# all equal the default's. Pool-robustness is claimed only if at least 5/6 of
# the tested (cell, setting) pairs are stable (B-6(ii) locked rule).
DEFAULT_SETTING = (600, 3000)                                   # (order, candidate)
OFAT_SETTINGS = [(600, 1500), (600, 6000), (300, 3000), (1200, 3000)]
S1_5_CONFIG_IDS = [1, 7]


def _block_a_identities(configs, order_pool, cand_pool, n_per_arm, train_sample):
    saved_order_pool = cfg.ORDER_POOL_SIZE
    cfg.ORDER_POOL_SIZE = order_pool
    try:
        dfA = run_corner_block(configs, cfg.BLOCK_A["models"],
                               cfg.BLOCK_A["sizes"], cfg.BLOCK_A["arms"],
                               n_per_arm, cand_pool, train_sample)
    finally:
        cfg.ORDER_POOL_SIZE = saved_order_pool
    out = {}
    for (cid, model, size), g in dfA.groupby(["config_id", "model", "size"]):
        fav = g["favorable_corner"].iloc[0]
        m_q = {c: float(np.median(g[g["arm"] == c]["makespan"])) for c in CORNERS}
        m0 = float(np.median(g[g["arm"] == "random"]["makespan"]))
        H_up, M_phi, UB, LB, qmax, qmin = decompose(m_q, m0, fav)
        out[(int(cid), model, int(size))] = {
            "order_pool_size": order_pool, "candidate_pool": cand_pool,
            "config_id": int(cid), "model": model, "size": int(size),
            "favorable_corner": fav, "q_max": qmax, "q_min": qmin,
            "H_up": H_up, "M_Phi": M_phi, "GAP": H_up + M_phi}
    return out


def run_s1_5(all_configs: List[dict], n_per_arm: int, train_sample: int,
             selftest: bool, default=DEFAULT_SETTING, ofat=OFAT_SETTINGS) -> dict:
    configs = [c for c in all_configs if c["config_id"] in S1_5_CONFIG_IDS]
    if not configs:            # selftest: toy config array may not have 1/7
        configs = all_configs[:1]
    base = _block_a_identities(configs, *default, n_per_arm, train_sample)
    rows, pairs = list(base.values()), []
    for setting in ofat:
        res = _block_a_identities(configs, *setting, n_per_arm, train_sample)
        rows += list(res.values())
        for key, r in res.items():
            d = base[key]
            same = {k: r[k] == d[k] for k in ("favorable_corner", "q_max", "q_min")}
            pairs.append({"config_id": key[0], "model": key[1], "size": key[2],
                          "order_pool_size": setting[0],
                          "candidate_pool": setting[1], **same,
                          "stable": all(same.values())})
    n_stable = sum(p["stable"] for p in pairs)
    share = n_stable / len(pairs) if pairs else None
    return {"design": "one factor at a time around (order 600, candidate 3000)",
            "default_setting": list(default), "tested_settings": [list(x) for x in ofat],
            "settings": rows, "pairs": pairs, "n_pairs": len(pairs),
            "n_stable": n_stable, "share_stable": share,
            "per_identity_share": {k: (sum(p[k] for p in pairs) / len(pairs)
                                       if pairs else None)
                                   for k in ("favorable_corner", "q_max", "q_min")},
            "pool_robustness_claim": bool(share is not None and share >= 5 / 6),
            "config_ids_used": [c["config_id"] for c in configs]}


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--selftest", action="store_true")
    args = p.parse_args()

    require_signed("S1C", selftest=args.selftest)

    if args.selftest:
        cfg.SEED_BASE = TOY_SEED_BASE
        all_configs = cfg.make_config_array()[:4]
        s1_4_configs = all_configs
        n_per_arm, cand_n, train_sample = 5, 80, 20
    else:
        all_configs = cfg.make_config_array()
        e2 = cfg.e2_subset(all_configs)
        s1_4_configs = e2[: cfg.BLOCK_C["n_configs"]]
        n_per_arm, cand_n = cfg.N_PER_ARM, cfg.CANDIDATE_POOL
        train_sample = cfg.TRAIN_SAMPLE

    s1_4 = run_s1_4(s1_4_configs, n_per_arm, cand_n, args.selftest)
    s1_5 = run_s1_5(all_configs, n_per_arm, train_sample, args.selftest)

    out_dir = scratch_dir() if args.selftest else RESULTS_DIR
    meta = {"registration_sha256": _sha256_file(REG_PATH),
           "b4_b6_design_sha256": _sha256_file(B4_DESIGN_PATH),
           "code_sha256": _sha256_file(Path(__file__)),
           "selftest": args.selftest}

    s1_4_path = out_dir / "v0_5_phase5_S1-4_B4.json"
    with open(s1_4_path, "w", encoding="utf-8") as f:
        json.dump({**meta, **s1_4}, f, indent=2, default=str)
    s1_5_path = out_dir / "v0_5_phase5_S1-5_B6ii.json"
    with open(s1_5_path, "w", encoding="utf-8") as f:
        json.dump({**meta, **s1_5}, f, indent=2, default=str)

    print(f"S1-4/S1-5 {'[selftest] ' if args.selftest else ''}wrote "
         f"{s1_4_path} and {s1_5_path}")


if __name__ == "__main__":
    main()
