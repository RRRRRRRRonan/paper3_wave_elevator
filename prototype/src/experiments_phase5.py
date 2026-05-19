"""
MVS v0.5 Phase 5 harness — publication-scale validation grid.

Runs the three blocks of `phase5_scaleup_preregistration.md` §2.2:
  Block A — decomposition: corner arms x {M1, M2} x {8, 30}, 18 configs
  Block B — 7-policy contest: P0-P6 x {8, 30}, the E=2 config subset
  Block C — model chain: corner arms x {M1, M2, M3} x size 16, E=2 subset

Modes:
  smoke  -- the ~1/60 calibration slice (pre-reg §7)        [default, safe]
  full   -- the complete confirmatory grid                  [after §10 sign-off]

Nothing here is locked. Every knob lives in phase5_config.py; configs_v0_5.json
is regenerated from make_config_array() on every run and carries a DRAFT
marker until the pre-registration §10 author sign-off.

Run:  python -m src.experiments_phase5 [smoke|full]
"""
from __future__ import annotations

import json
import random
import sys
import time
from pathlib import Path
from typing import Dict, List

import pandas as pd

from src import phase5_config as cfg
from src.demand_patterns import generate_pool
from src.simulator import simulate_wave
from src.wave_policies import (POLICIES, build_candidates, corner_positions,
                               favorable_label, fit_phi_beta, fit_spo_tree,
                               materialise)

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RAW_DIR = RESULTS_DIR / "raw"

MODEL_IDX = {"abstraction": 0, "batched": 1, "M3_s20": 2}
MODEL_TAG = {"abstraction": "M1", "batched": "M2", "M3_s20": "M3_s20"}


# --------------------------------------------------------------------------
# Deterministic seeds (no hash() of strings -> reproducible across processes)
# --------------------------------------------------------------------------

def _seed(config_id: int, *parts: int) -> int:
    s = cfg.SEED_BASE + config_id * 100_003
    for i, p in enumerate(parts):
        s += (p + 1) * (37 ** (i + 1))
    return s % (2 ** 31)


# --------------------------------------------------------------------------
# Simulator binding
# --------------------------------------------------------------------------

def _elevator_kwargs(model: str) -> dict:
    if model == "abstraction":
        return {"batched": False}
    if model == "batched":
        return {"batched": True}
    if model == "M3_s20":
        return {"stochastic_sigma": cfg.M3_SIGMA}
    raise ValueError(f"unknown model {model!r}")


def sim_makespan(wave, config: dict, model: str, rng: random.Random) -> float:
    return simulate_wave(
        wave,
        n_amrs=config["n_amrs"],
        n_elevators=config["n_elevators"],
        capacity=cfg.CAPACITY,
        rng=rng,
        **_elevator_kwargs(model),
    )


def fit_predictors(cand: pd.DataFrame, pool, config: dict, model: str,
                   train_sample: int, seed: int):
    """Training pass: simulate `train_sample` candidate waves, fit beta + SPO-tree."""
    rng = random.Random(seed)
    n = min(train_sample, len(cand))
    sub = cand.iloc[[rng.randrange(len(cand)) for _ in range(n)]].reset_index(drop=True)
    mks = [sim_makespan(materialise(row, pool), config, model, rng)
           for _, row in sub.iterrows()]
    beta = fit_phi_beta(sub, mks)
    tree = fit_spo_tree(sub, mks, seed=seed)
    return beta, tree


def _config_fields(config: dict) -> dict:
    return {k: config[k] for k in
            ("config_id", "F", "n_amrs", "n_elevators", "demand")}


# --------------------------------------------------------------------------
# Block runners
# --------------------------------------------------------------------------

def run_corner_block(configs: List[dict], models: List[str], sizes: List[int],
                     arms: List[str], n_per_arm: int, cand_n: int,
                     train_sample: int) -> pd.DataFrame:
    """Blocks A / C: 5 corner arms x models x sizes. CSV schema matches Phase 4 v2."""
    rows = []
    for config in configs:
        pool = generate_pool(config["demand"], config["F"], cfg.ORDER_POOL_SIZE,
                             seed=cfg.SEED_BASE + config["config_id"],
                             **cfg.DEMAND_PARAMS[config["demand"]])
        for model in models:
            for size in sizes:
                seed = _seed(config["config_id"], MODEL_IDX[model], size)
                cand = build_candidates(pool, size, cand_n, random.Random(seed))
                beta, _ = fit_predictors(cand, pool, config, model,
                                         train_sample, seed + 1)
                fav = favorable_label(beta)
                for ai, arm in enumerate(arms):
                    pos = corner_positions(cand, arm)
                    arm_rng = random.Random(seed + 13 * (ai + 1))
                    sim_rng = random.Random(seed + 1009 + ai)
                    for _ in range(n_per_arm):
                        p = int(arm_rng.choice(pos))
                        mk = sim_makespan(materialise(cand.iloc[p], pool),
                                          config, model, sim_rng)
                        rows.append({**_config_fields(config), "model": model,
                                     "size": size, "arm": arm,
                                     "favorable_corner": fav, "makespan": mk})
    return pd.DataFrame(rows)


def run_policy_block(configs: List[dict], model: str, sizes: List[int],
                     n_per_arm: int, cand_n: int,
                     train_sample: int) -> pd.DataFrame:
    """Block B: the 7-policy contest P0-P6, operational dispatch fixed."""
    rows = []
    for config in configs:
        pool = generate_pool(config["demand"], config["F"], cfg.ORDER_POOL_SIZE,
                             seed=cfg.SEED_BASE + config["config_id"],
                             **cfg.DEMAND_PARAMS[config["demand"]])
        for size in sizes:
            seed = _seed(config["config_id"], MODEL_IDX[model], size)
            cand = build_candidates(pool, size, cand_n, random.Random(seed))
            beta, tree = fit_predictors(cand, pool, config, model,
                                        train_sample, seed + 1)
            ctx = {"beta_C": beta["beta_C"], "beta_I": beta["beta_I"],
                   "spo_tree": tree, "feature_cols": ("C", "I")}
            for pi, policy in enumerate(POLICIES):
                pol_rng = random.Random(seed + 13 * (pi + 1))
                sim_rng = random.Random(seed + 2003 + pi)
                draw = POLICIES[policy](cand, n_per_arm, pol_rng, ctx)
                for p in draw:
                    mk = sim_makespan(materialise(cand.iloc[p], pool),
                                      config, model, sim_rng)
                    rows.append({**_config_fields(config), "model": model,
                                 "size": size, "policy": policy,
                                 "makespan": mk})
    return pd.DataFrame(rows)


def run_chain_block(configs: List[dict], models: List[str], sizes: List[int],
                    arms: List[str], n_per_arm: int,
                    cand_n: int) -> pd.DataFrame:
    """Block C: matched-wave M1/M2/M3 on a SINGLE candidate pool per (config, size).

    Each drawn wave is simulated under EVERY model and emitted in wide format
    (makespan_M1 / makespan_M2 / makespan_M3_s20), so the same wave is compared
    across the chain — required for the D2-a per-wave dominance gate and the
    D3 corner-invariance probe. Schema mirrors mvs_v0_2_phase4_v2_m3_samples.csv.
    The candidate-pool seed is model-independent; that is what makes the waves
    matched (the W3 corner-block used a per-model seed and was NOT matched).
    """
    rows = []
    for config in configs:
        pool = generate_pool(config["demand"], config["F"], cfg.ORDER_POOL_SIZE,
                             seed=cfg.SEED_BASE + config["config_id"],
                             **cfg.DEMAND_PARAMS[config["demand"]])
        for size in sizes:
            seed = _seed(config["config_id"], 99, size)   # model-independent
            cand = build_candidates(pool, size, cand_n, random.Random(seed))
            for ai, arm in enumerate(arms):
                pos = corner_positions(cand, arm)
                arm_rng = random.Random(seed + 13 * (ai + 1))
                for wid in range(n_per_arm):
                    wave = materialise(cand.iloc[int(arm_rng.choice(pos))], pool)
                    rec = {**_config_fields(config), "size": size, "arm": arm,
                           "wave_id": wid}
                    for model in models:
                        m_rng = random.Random(seed + 700_003
                                               + MODEL_IDX[model] * 9973 + wid)
                        rec[f"makespan_{MODEL_TAG[model]}"] = sim_makespan(
                            wave, config, model, m_rng)
                    rows.append(rec)
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------
# Config-array artefact (regenerated, draft until §10)
# --------------------------------------------------------------------------

def write_config_array() -> List[dict]:
    configs = cfg.make_config_array()
    out = {
        "_status": "DRAFT — regenerated from phase5_config.make_config_array(); "
                   "tunable until the pre-registration §10 author sign-off, "
                   "NOT frozen.",
        "n_configs": len(configs),
        "configs": configs,
    }
    path = RESULTS_DIR / "configs_v0_5.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"  wrote {path} ({len(configs)} configs, draft)")
    return configs


# --------------------------------------------------------------------------
# Modes
# --------------------------------------------------------------------------

def _span_demand(configs: List[dict], n: int) -> List[dict]:
    """Pick up to n configs spanning distinct demand patterns (smoke S4 needs this)."""
    picked, seen = [], set()
    for c in configs:
        if c["demand"] not in seen:
            picked.append(c)
            seen.add(c["demand"])
        if len(picked) >= n:
            break
    return picked


def run_smoke() -> None:
    """Pre-reg §7 calibration slice — ~1/60 scale. Tunable via cfg.SMOKE."""
    configs = write_config_array()
    s = cfg.SMOKE
    slice_a = _span_demand(configs, s["n_configs"])
    slice_b = _span_demand(cfg.e2_subset(configs), s["n_configs"])
    t0 = time.time()
    print(f"Phase 5 SMOKE  (~1/60 scale; all knobs in phase5_config.py)")

    dfA = run_corner_block(slice_a, s["models"], [s["size"]],
                           cfg.BLOCK_A["arms"], s["n_per_arm"],
                           s["candidate_pool"], s["train_sample"])
    dfB = run_policy_block(slice_b, cfg.BLOCK_B["model"], [s["size"]],
                           s["n_per_arm"], s["candidate_pool"],
                           s["train_sample"])
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    dfA.to_csv(RAW_DIR / "mvs_v0_5_phase5_smoke_blockA.csv", index=False)
    dfB.to_csv(RAW_DIR / "mvs_v0_5_phase5_smoke_blockB.csv", index=False)
    print(f"  Block A slice: {len(dfA)} sims | Block B slice: {len(dfB)} sims")
    print(f"  total {len(dfA) + len(dfB)} sims in {time.time() - t0:.1f}s")
    print("  -> smoke verdict (pre-reg §7 S1-S4) is computed by W4 analysis.")


def run_full() -> None:
    """Confirmatory grid. Only after the pre-registration §10 sign-off."""
    configs = write_config_array()
    e2 = cfg.e2_subset(configs)
    t0 = time.time()
    print("Phase 5 FULL run")

    dfA = run_corner_block(configs, cfg.BLOCK_A["models"], cfg.BLOCK_A["sizes"],
                           cfg.BLOCK_A["arms"], cfg.N_PER_ARM,
                           cfg.CANDIDATE_POOL, cfg.TRAIN_SAMPLE)
    dfB = run_policy_block(e2[:cfg.BLOCK_B["n_configs"]], cfg.BLOCK_B["model"],
                           cfg.BLOCK_B["sizes"], cfg.N_PER_ARM,
                           cfg.CANDIDATE_POOL, cfg.TRAIN_SAMPLE)
    dfC = run_chain_block(e2[:cfg.BLOCK_C["n_configs"]], cfg.BLOCK_C["models"],
                          cfg.BLOCK_C["sizes"], cfg.BLOCK_C["arms"],
                          cfg.N_PER_ARM, cfg.CANDIDATE_POOL)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    dfA.to_csv(RAW_DIR / "mvs_v0_5_phase5_blockA.csv", index=False)
    dfB.to_csv(RAW_DIR / "mvs_v0_5_phase5_blockB.csv", index=False)
    dfC.to_csv(RAW_DIR / "mvs_v0_5_phase5_blockC.csv", index=False)
    # Block C is wide-format: each row carries one sim per model.
    nC = len(dfC) * len(cfg.BLOCK_C["models"])
    print(f"  Block A {len(dfA)} | Block B {len(dfB)} sims | "
          f"Block C {len(dfC)} matched-wave rows = {nC} sims")
    print(f"  total {len(dfA) + len(dfB) + nC} sims "
          f"in {time.time() - t0:.1f}s")


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "smoke"
    if mode == "smoke":
        run_smoke()
    elif mode == "full":
        run_full()
    else:
        raise SystemExit(f"unknown mode {mode!r} (use: smoke | full)")


if __name__ == "__main__":
    main()
