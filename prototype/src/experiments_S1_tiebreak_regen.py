"""
S1-9 -- Tie-break regeneration of Blocks A and B [QA].

Registration: revision_2026-09-26_ijpr/amendments/AMEND-2026-09-26-S1B_new_simulations.md
("S1-9. Tie-break regeneration of Blocks A and B [QA]"). Guard key: "S1B"
(author_signoff PENDING as of 2026-09-26).

Re-runs `run_corner_block` (Block A), `run_policy_block` (Block B), and the
P7 ablation with the CURRENT simulator (the 2026-09-11 index-stable
tie-break fix), identical seeds and code paths to experiments_phase5.py /
experiments_phase5_ablation.py, writing to
mvs_v0_5_phase5_blockA_tiebreakfix.csv / ..._blockB_tiebreakfix.csv /
..._ablation_P7_tiebreakfix.csv. The unchanged gate logic of
analysis_phase5_blockA.py / analysis_phase5_blockB.py is then applied to
these NEW CSVs (their `main()` is called with its module-level input and output
paths redirected to a temporary folder, so the stored JSONs are never
written; their hashes are checked before and after). A side-by-side
comparison of stored vs regenerated gate counts is written alongside.

Real mode replays Block A + B at FULL scale under the REGISTERED seeds
(phase5_config.SEED_BASE, experiments_phase5._seed) -- exactly what Absolute
Rule 2 forbids running tonight. `require_signed("S1B", selftest=False)`
stops the script before any of this executes; the registration is unsigned.
Self-test mode patches `phase5_config.SEED_BASE` to
`registration_guard.TOY_SEED_BASE`, uses 1-2 tiny configs and small
n_per_arm / candidate-pool / P7-iteration counts, and writes only to
registration_guard.scratch_dir() -- never to prototype/results.

Run:
  python -m src.experiments_S1_tiebreak_regen             # stops at guard
  python -m src.experiments_S1_tiebreak_regen --selftest  # toy run to scratch
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tempfile
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

from src import phase5_config as cfg
from src.experiments_phase5 import run_corner_block, run_policy_block
from src.experiments_phase5_ablation import P7_ITER, run_p7
from src.registration_guard import TOY_SEED_BASE, require_signed, scratch_dir

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RAW_DIR = RESULTS_DIR / "raw"
REG_PATH = (Path(__file__).resolve().parents[2] / "revision_2026-09-26_ijpr"
            / "amendments" / "AMEND-2026-09-26-S1B_new_simulations.md")

# S1-9 "Prior exposure" (B-14, a fixed disclosed fact, not computed here).
B14_EXPOSURE = ("15.6% of elevator requests faced an availability tie, "
               "5.1% a tie between units on different floors")


def _sha256_file(path: Path) -> str:
    """Line-ending-normalized SHA-256 (the guard's definition), so
    recorded hashes match MANIFEST_SIGNED.json."""
    from src.registration_guard import sha256_file
    return sha256_file(path)


# --------------------------------------------------------------------------
# Simulation: identical code paths to experiments_phase5.run_full /
# experiments_phase5_ablation.main, against whatever `configs` is passed in
# (the real 18-config array, or a selftest toy slice).
# --------------------------------------------------------------------------

def regenerate_csvs(configs: list, n_per_arm: int, cand_n: int,
                    train_sample: int, sizes_a: list, sizes_b: list,
                    p7_iter: int) -> dict:
    e2 = cfg.e2_subset(configs)
    block_b_configs = e2[: cfg.BLOCK_B["n_configs"]] or e2 or configs[:1]
    dfA = run_corner_block(configs, cfg.BLOCK_A["models"], sizes_a,
                           cfg.BLOCK_A["arms"], n_per_arm, cand_n, train_sample)
    dfB = run_policy_block(block_b_configs, cfg.BLOCK_B["model"], sizes_b,
                           n_per_arm, cand_n, train_sample)
    dfP7 = run_p7(block_b_configs, sizes_b, n_per_arm, p7_iter)
    return {"blockA": dfA, "blockB": dfB, "blockP7": dfP7}


# --------------------------------------------------------------------------
# Gate analysis: the STORED analysis code itself (analysis_phase5_blockA.main,
# analysis_phase5_blockB.main), run on the regenerated CSVs. Both modules read
# their module-level paths at call time, so the paths are redirected to a
# temporary folder for the call and restored afterwards; the stored JSONs are
# hashed before and after and must be unchanged. (Replaces the helper agent's
# re-implementation of the gate logic, 2026-09-26: running the stored code is
# verifiably identical to the preregistered analysis.)
# --------------------------------------------------------------------------

def run_stored_analysis(csv_a: Path, csv_b: Path, csv_p7: Path):
    from src import analysis_phase5_blockA as ana_a
    from src import analysis_phase5_blockB as ana_b
    stored = [RESULTS_DIR / "v0_5_phase5_blockA.json",
              RESULTS_DIR / "v0_5_phase5_blockB.json"]
    before = {str(q): _sha256_file(q) for q in stored if q.exists()}
    saved = (ana_a.CSV, ana_a.RESULTS_DIR, ana_b.RAW, ana_b.RESULTS_DIR)
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        raw = tmp / "raw"
        raw.mkdir()
        shutil.copyfile(csv_b, raw / "mvs_v0_5_phase5_blockB.csv")
        shutil.copyfile(csv_p7, raw / "mvs_v0_5_phase5_ablation_P7.csv")
        try:
            ana_a.CSV, ana_a.RESULTS_DIR = Path(csv_a), tmp
            ana_b.RAW, ana_b.RESULTS_DIR = raw, tmp
            ana_a.main()
            ana_b.main()
            out_a = json.loads((tmp / "v0_5_phase5_blockA.json").read_text("utf-8"))
            out_b = json.loads((tmp / "v0_5_phase5_blockB.json").read_text("utf-8"))
        finally:
            ana_a.CSV, ana_a.RESULTS_DIR, ana_b.RAW, ana_b.RESULTS_DIR = saved
    after = {str(q): _sha256_file(q) for q in stored if q.exists()}
    if before != after:
        raise SystemExit("S1-9 STOP: a stored Phase 5 JSON changed during the "
                         "analysis call; restore it from git and investigate.")
    note = ("computed by the stored analysis code on the regenerated CSV; the "
            "'generated' field is hard-coded in that code and is not the run date")
    out_a["regenerated_on"] = out_b["regenerated_on"] = date.today().isoformat()
    out_a["note"] = out_b["note"] = note
    return out_a, out_b


# --------------------------------------------------------------------------
# Side-by-side comparison (real mode: reads the STORED analysis JSONs)
# --------------------------------------------------------------------------

def compare_to_stored(regen_a: dict, regen_b: dict) -> dict:
    stored_a_path = RESULTS_DIR / "v0_5_phase5_blockA.json"
    stored_b_path = RESULTS_DIR / "v0_5_phase5_blockB.json"
    stored_a = json.loads(stored_a_path.read_text(encoding="utf-8"))
    stored_b = json.loads(stored_b_path.read_text(encoding="utf-8"))
    cmp_a = {"stored": {"gates": stored_a["gates"], "verdict": stored_a["verdict"]},
           "regenerated": {"gates": regen_a["gates"], "verdict": regen_a["verdict"]},
           "D1d_delta": regen_a["gates"]["D1d"] - stored_a["gates"]["D1d"],
           "verdict_changed": stored_a["verdict"] != regen_a["verdict"]}
    cmp_b = {"stored": {"band": stored_b.get("band"),
                       "P5_vs_P0": stored_b.get("P5_vs_P0")},
           "regenerated": {"band": regen_b.get("band"),
                          "P5_vs_P0": regen_b.get("P5_vs_P0")},
           "band_changed": stored_b.get("band") != regen_b.get("band")}
    return {"blockA": cmp_a, "blockB": cmp_b, "b14_exposure": B14_EXPOSURE}


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--selftest", action="store_true")
    args = p.parse_args()

    require_signed("S1B", selftest=args.selftest)

    if args.selftest:
        cfg.SEED_BASE = TOY_SEED_BASE
        configs = cfg.make_config_array()[:4]
        n_per_arm, cand_n, train_sample, p7_iter = 5, 80, 20, 5
        sizes_a, sizes_b = [8], [8]
    else:
        configs = cfg.make_config_array()
        n_per_arm, cand_n = cfg.N_PER_ARM, cfg.CANDIDATE_POOL
        train_sample, p7_iter = cfg.TRAIN_SAMPLE, P7_ITER
        sizes_a, sizes_b = cfg.BLOCK_A["sizes"], cfg.BLOCK_B["sizes"]

    dfs = regenerate_csvs(configs, n_per_arm, cand_n, train_sample,
                          sizes_a, sizes_b, p7_iter)

    out_dir = scratch_dir() if args.selftest else RAW_DIR
    if not args.selftest:
        RAW_DIR.mkdir(parents=True, exist_ok=True)
    csv_paths = {
        "blockA": out_dir / "mvs_v0_5_phase5_blockA_tiebreakfix.csv",
        "blockB": out_dir / "mvs_v0_5_phase5_blockB_tiebreakfix.csv",
        "blockP7": out_dir / "mvs_v0_5_phase5_ablation_P7_tiebreakfix.csv",
    }
    dfs["blockA"].to_csv(csv_paths["blockA"], index=False)
    dfs["blockB"].to_csv(csv_paths["blockB"], index=False)
    dfs["blockP7"].to_csv(csv_paths["blockP7"], index=False)

    regen_a, regen_b = run_stored_analysis(csv_paths["blockA"],
                                           csv_paths["blockB"],
                                           csv_paths["blockP7"])

    json_out_dir = scratch_dir() if args.selftest else RESULTS_DIR
    json_paths = {
        "blockA": json_out_dir / "v0_5_phase5_blockA_tiebreakfix.json",
        "blockB": json_out_dir / "v0_5_phase5_blockB_tiebreakfix.json",
        "comparison": json_out_dir / "v0_5_phase5_S1-9_comparison.json",
    }
    with open(json_paths["blockA"], "w", encoding="utf-8") as f:
        json.dump(regen_a, f, indent=2, default=str)
    with open(json_paths["blockB"], "w", encoding="utf-8") as f:
        json.dump(regen_b, f, indent=2, default=str)

    meta = {"registration_sha256": _sha256_file(REG_PATH),
           "code_sha256": _sha256_file(Path(__file__)),
           "selftest": args.selftest,
           "csv_paths": {k: str(v) for k, v in csv_paths.items()}}
    if args.selftest:
        comparison = {
            **meta, "note": ("selftest: no stored blockA/blockB JSON exists "
                            "for toy data, so this reports the regenerated "
                            "gates alone (the real-mode path additionally "
                            "reads the STORED v0_5_phase5_blockA.json / "
                            "v0_5_phase5_blockB.json for a side-by-side "
                            "comparison -- forbidden to read tonight under "
                            "Absolute Rule 1, and never executed anyway "
                            "since the guard stops real mode first)."),
            "regenerated_blockA_gates": regen_a["gates"],
            "regenerated_blockA_verdict": regen_a["verdict"],
            "regenerated_blockB_band": regen_b.get("band"),
        }
    else:
        comparison = {**meta, **compare_to_stored(regen_a, regen_b)}
    with open(json_paths["comparison"], "w", encoding="utf-8") as f:
        json.dump(comparison, f, indent=2, default=str)

    print(f"S1-9 {'[selftest] ' if args.selftest else ''}wrote "
         f"{csv_paths['blockA']}, {csv_paths['blockB']}, "
         f"{csv_paths['blockP7']}, {json_paths['blockA']}, "
         f"{json_paths['blockB']}, {json_paths['comparison']}")


if __name__ == "__main__":
    main()
