"""
S1-3 -- Block C coverage extension [NS], plus the S1-6 stability/margin
extras and the TH-2 per-wave abstraction bias, computed on the SAME new data.

Registration: revision_2026-09-26_ijpr/amendments/AMEND-2026-09-26-S1B_new_simulations.md
("S1-3. Block C coverage extension [NS]"). S1-6's own definitions live in
AMEND-2026-09-26-S1A_reanalyses.md, but S1-3's text says its extension rows
carry S1-6 quantities too ("The Block C extension (S1-3) adds rows for the
other configurations, marked as [NS] extension rows") and TH-2 says the same
("S1-3 extension rows ... once S1-3 has run; marked [NS]"). Since running
`run_chain_block` on new configs/sizes is itself an S1-3 action, this whole
script is gated on the S1-3 registration, guard key "S1B".

Design (S1-3 "Design", unchanged code path `run_chain_block`):
  - the 12 configurations NOT in Block C (all E=1 configs, and the F=8,E=2
    configs) at size 16;
  - all 18 configurations at sizes 8 and 30.
  The 6 original Block C configs at size 16 are NOT rerun here.

Real mode runs only after `require_signed("S1B")` passes; the registered
run took place on 2026-09-26 (revision_2026-09-26_ijpr/study1_run_2026-09-26/). Self-test mode never touches prototype/results; it patches
`phase5_config.SEED_BASE` to `registration_guard.TOY_SEED_BASE`, uses a
handful of toy configs, and tiny n_per_arm / candidate-pool sizes.

Run:
  python -m src.experiments_S1_blockC_ext             # real run: writes into prototype/results/; only at the author's request
  python -m src.experiments_S1_blockC_ext --selftest  # toy run to scratch
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd
from scipy.stats import wasserstein_distance

from src import phase5_config as cfg
from src.analysis_phase5_blockA import CORNERS
from src.experiments_phase5 import run_chain_block
from src.registration_guard import code_provenance  # S1D: code-tree hash in every output
from src.registration_guard import TOY_SEED_BASE, require_signed, scratch_dir

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RAW_DIR = RESULTS_DIR / "raw"
REG_PATH = (Path(__file__).resolve().parents[2] / "revision_2026-09-26_ijpr"
            / "amendments" / "AMEND-2026-09-26-S1B_new_simulations.md")

MODELS = ["abstraction", "batched", "M3_s20"]
ARMS = ["random", "HC_HI", "HC_LI", "LC_HI", "LC_LI"]
EPS = 0.05
STAB_B = 2000
STAB_SEED = 20260928


# --------------------------------------------------------------------------
# Small utilities
# --------------------------------------------------------------------------

def _sha256_file(path: Path) -> str:
    """Line-ending-normalized SHA-256 (the guard's definition), so
    recorded hashes match MANIFEST_SIGNED.json."""
    from src.registration_guard import sha256_file
    return sha256_file(path)


def cluster_resample_indices(cluster_ids: np.ndarray,
                             rng: np.random.Generator) -> np.ndarray:
    """One clustered-bootstrap draw's row positions (S1-1 procedure, reused
    here per S1-6's 'clustered stability B=2000 seed 20260928')."""
    uniq, inverse = np.unique(cluster_ids, return_inverse=True)
    buckets = [np.where(inverse == k)[0] for k in range(len(uniq))]
    draw = rng.integers(0, len(uniq), size=len(uniq))
    return np.concatenate([buckets[k] for k in draw])


def _blockC_config_ids(configs: List[dict]) -> List[int]:
    """The 6 original Block C configs, by the SAME rule experiments_phase5
    uses (e2_subset(configs)[:BLOCK_C.n_configs]) -- not hardcoded, so it
    matches whatever `configs` actually is (real 18-config array or a toy
    selftest array)."""
    e2 = cfg.e2_subset(configs)
    return [c["config_id"] for c in e2[: cfg.BLOCK_C["n_configs"]]]


# --------------------------------------------------------------------------
# D2-a/b/c + Hedge/DRO, mirroring analysis_phase5_blockC.py, per (config,size)
# --------------------------------------------------------------------------

def blockC_style_unit(gc: pd.DataFrame) -> dict:
    """analysis_phase5_blockC.py's per-config loop body, applied to one
    (config_id, size) unit's matched-wave rows (all 5 arms present)."""
    m0 = float(np.median(gc[gc["arm"] == "random"]["makespan_M2"]))
    cells = {}
    dro = {}
    for corner in CORNERS:
        sub = gc[gc["arm"] == corner]
        T1 = sub["makespan_M1"].to_numpy(float)
        T2 = sub["makespan_M2"].to_numpy(float)
        qa, qb = np.sort(T1), np.sort(T2)
        perwave = float(np.mean(T2 >= T1))
        fosd = float(np.mean(qb >= qa - 1e-9))
        w1 = float(wasserstein_distance(T1, T2))
        U_c = float(np.quantile(T2, 0.5 + EPS) - np.quantile(T2, 0.5))
        cells[corner] = {"perwave_dom": perwave, "fosd": fosd, "W1": w1,
                        "U_c_005": U_c, "U_c_lt_5pct": bool(U_c < EPS * m0),
                        "fosd_ok": bool(fosd >= 0.99),
                        "mean_M1": float(np.mean(T1)), "mean_M2": float(np.mean(T2)),
                        "median_M1": float(np.median(T1)),
                        "median_M2": float(np.median(T2))}
        dro[corner] = (max(float(np.mean(T1)), float(np.mean(T2))),
                      float(np.mean(T1)) + w1)
    c_hedge_mean = min(dro, key=lambda c: dro[c][0])
    c_dro = min(dro, key=lambda c: dro[c][1])
    return {"m0": m0, "per_corner": cells,
           "c_star_Hedge_mean": c_hedge_mean, "c_star_DRO": c_dro,
           "collapse_mean": bool(c_hedge_mean == c_dro),
           "perwave_avg": float(np.mean([cells[c]["perwave_dom"] for c in CORNERS])),
           "perwave_worst": float(np.min([cells[c]["perwave_dom"] for c in CORNERS])),
           "n_fosd_ok": sum(cells[c]["fosd_ok"] for c in CORNERS),
           "n_Uc_ok": sum(cells[c]["U_c_lt_5pct"] for c in CORNERS)}


# --------------------------------------------------------------------------
# S1-6 extras: Hedge / minimax-regret corner, second-place margin, stability
# --------------------------------------------------------------------------

def hedge_and_minimax(v: Dict[str, Dict[str, float]]) -> dict:
    """v[corner]['M1'/'M2'] -> class statistic (mean OR median, caller's
    choice). Hedge corner, minimax-regret corner, second-place margin of the
    Hedge criterion (S1-6 "Quantities per configuration")."""
    hedge_crit = {c: max(v[c]["M1"], v[c]["M2"]) for c in CORNERS}
    hedge_corner = min(hedge_crit, key=hedge_crit.get)
    ranked = sorted(hedge_crit.values())
    margin = ((ranked[1] - ranked[0]) / ranked[0])if ranked[0] else float("nan")
    regret = {}
    for c in CORNERS:
        reg_by_model = []
        for m in ("M1", "M2"):
            vals = {c2: v[c2][m] for c2 in CORNERS}
            vmin = min(vals.values())
            reg_by_model.append((vals[c] - vmin) / vmin if vmin else float("nan"))
        regret[c] = max(reg_by_model)
    minimax_regret_corner = min(regret, key=regret.get)
    return {"hedge_corner": hedge_corner, "hedge_criterion": hedge_crit,
           "second_place_margin": margin,
           "minimax_regret_corner": minimax_regret_corner,
           "minimax_regret": regret}


def _class_stat_dict(gc: pd.DataFrame, agg) -> Dict[str, Dict[str, float]]:
    out = {}
    for corner in CORNERS:
        sub = gc[gc["arm"] == corner]
        out[corner] = {"M1": float(agg(sub["makespan_M1"].to_numpy(float))),
                      "M2": float(agg(sub["makespan_M2"].to_numpy(float)))}
    return out


def clustered_stability(gc: pd.DataFrame, agg, B: int, seed: int) -> dict:
    """Share of clustered-bootstrap replicates whose Hedge / minimax-regret
    corner equals the full-data one (S1-6 "Stability")."""
    full = hedge_and_minimax(_class_stat_dict(gc, agg))
    rng = np.random.default_rng(seed)
    arrays = {c: {"M1": gc[gc["arm"] == c]["makespan_M1"].to_numpy(float),
                 "M2": gc[gc["arm"] == c]["makespan_M2"].to_numpy(float),
                 "cluster": gc[gc["arm"] == c]["candidate_id"].to_numpy()}
             for c in CORNERS}
    n_hedge_match = 0
    n_minimax_match = 0
    for _ in range(B):
        v = {}
        for c in CORNERS:
            idx = cluster_resample_indices(arrays[c]["cluster"], rng)
            v[c] = {"M1": float(agg(arrays[c]["M1"][idx])),
                   "M2": float(agg(arrays[c]["M2"][idx]))}
        hm = hedge_and_minimax(v)
        n_hedge_match += int(hm["hedge_corner"] == full["hedge_corner"])
        n_minimax_match += int(hm["minimax_regret_corner"]
                               == full["minimax_regret_corner"])
    return {"full_data": full, "B": B, "seed": seed,
           "hedge_stability": n_hedge_match / B,
           "minimax_regret_stability": n_minimax_match / B}


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------

def run_extension(configs: List[dict], n_per_arm: int, cand_n: int,
                  stab_B: int, selftest: bool) -> tuple:
    block_c_ids = _blockC_config_ids(configs)
    not_in_blockC = [c for c in configs if c["config_id"] not in block_c_ids]

    df_size16 = run_chain_block(not_in_blockC, MODELS, [16], ARMS,
                                n_per_arm, cand_n)
    df_size16["extension_slice"] = "12_configs_size16"
    df_other_sizes = run_chain_block(configs, MODELS, [8, 30], ARMS,
                                     n_per_arm, cand_n)
    df_other_sizes["extension_slice"] = "18_configs_size8_30"
    df = pd.concat([df_size16, df_other_sizes], ignore_index=True)
    df["abstraction_bias"] = ((df["makespan_M2"] - df["makespan_M1"])
                              / df["makespan_M1"])

    units = []
    for (cid, size), gc in df.groupby(["config_id", "size"]):
        base = blockC_style_unit(gc)
        stab_mean = clustered_stability(gc, np.mean, stab_B, STAB_SEED)
        stab_med = clustered_stability(gc, np.median, stab_B, STAB_SEED)
        d2a = bool(base["perwave_avg"] >= 0.90 and base["perwave_worst"] >= 0.80)
        d2b = bool(base["n_fosd_ok"] >= 0.90 * len(CORNERS))
        d2c = bool(base["n_Uc_ok"] >= 0.80 * len(CORNERS))
        units.append({
            "config_id": int(cid), "size": int(size),
            "would_meet_D2a": d2a, "would_meet_D2b": d2b, "would_meet_D2c": d2c,
            **base,
            "s1_6_mean_basis": stab_mean, "s1_6_median_basis": stab_med,
            "abstraction_bias_median": float(gc["abstraction_bias"].median()),
            "abstraction_bias_iqr": [float(gc["abstraction_bias"].quantile(0.25)),
                                    float(gc["abstraction_bias"].quantile(0.75))],
            "abstraction_bias_reversal_share": float(
                (gc["abstraction_bias"] < 0).mean()),
        })

    n_units = len(units)
    n_d2a = sum(u["would_meet_D2a"] for u in units)
    n_d2b = sum(u["would_meet_D2b"] for u in units)
    n_d2c = sum(u["would_meet_D2c"] for u in units)
    below_threshold = [u for u in units if not (u["would_meet_D2a"]
                                                and u["would_meet_D2b"]
                                                and u["would_meet_D2c"])]
    summary = {
        "block_c_original_config_ids": block_c_ids,
        "n_units": n_units, "n_configs_size16_extension": len(not_in_blockC),
        "n_configs_other_sizes": len(configs),
        "would_meet_D2a": n_d2a, "would_meet_D2b": n_d2b, "would_meet_D2c": n_d2c,
        "n_below_any_threshold": len(below_threshold),
        "units_below_threshold": [{"config_id": u["config_id"], "size": u["size"]}
                                  for u in below_threshold],
        "units": units,
    }
    return df, summary


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--selftest", action="store_true")
    p.add_argument("--n-per-arm", type=int, default=None)
    p.add_argument("--cand-n", type=int, default=None)
    p.add_argument("--stab-b", type=int, default=None)
    args = p.parse_args()

    require_signed("S1B", selftest=args.selftest)

    if args.selftest:
        cfg.SEED_BASE = TOY_SEED_BASE
        configs = cfg.make_config_array()[:4]     # small but has >=1 E=1, E=2
        n_per_arm = args.n_per_arm or 6
        cand_n = args.cand_n or 80
        stab_B = args.stab_b or 100
    else:
        configs = cfg.make_config_array()
        n_per_arm = args.n_per_arm or cfg.N_PER_ARM
        cand_n = args.cand_n or cfg.CANDIDATE_POOL
        stab_B = args.stab_b or STAB_B

    df, summary = run_extension(configs, n_per_arm, cand_n, stab_B, args.selftest)

    if args.selftest:
        out_dir = scratch_dir()
    else:
        out_dir = RESULTS_DIR
        RAW_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = ((RAW_DIR if not args.selftest else out_dir)
               / "mvs_v0_5_phase5_S1-3_blockC_ext.csv")
    df.to_csv(csv_path, index=False)

    out = {"registration_sha256": _sha256_file(REG_PATH),
          "code_sha256": _sha256_file(Path(__file__)), **code_provenance(),
          "selftest": args.selftest, "n_per_arm": n_per_arm, "cand_n": cand_n,
          "stability_B": stab_B, "raw_csv": str(csv_path), **summary}
    json_path = out_dir / "v0_5_phase5_S1-3_blockC_ext.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, default=str)

    print(f"S1-3 {'[selftest] ' if args.selftest else ''}"
         f"wrote {csv_path} ({len(df)} matched-wave rows) and {json_path}")


if __name__ == "__main__":
    main()
