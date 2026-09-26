"""
S1-1 completion [RA] -- the parts of the registered S1-1 procedure that the
run of 2026-09-26 (EXECUTION-LOG entry 55) did not produce (entry 57):

  (1) S1A general rule 5: S1-1 re-analyses a locked verdict, so the stored
      artefact is primary and the tie-break-fixed data are secondary, "both
      versions are always reported". The run produced the secondary version
      for Block C only; this module runs the full Block A and Block B
      procedure on the tie-break-fixed CSVs written by S1-9
      (mvs_v0_5_phase5_blockA_tiebreakfix.csv, ..._blockB_tiebreakfix.csv,
      ..._ablation_P7_tiebreakfix.csv).
  (2) "the same for the deduplicated analysis": the 10-seed range of the
      deduplicated D1-d count (seeds 20260927 + i), for both versions.

Every statistic is computed by the unchanged functions of
analysis_S1_cluster_bootstrap (imported, not copied); seeds and B are the
registered ones. Independent seeds run in parallel processes; each call seeds
its own generator, so the values do not depend on the parallel schedule.

Checks that stop the run (real mode):
  - the tie-break-fixed CSVs join row by row to the stored candidate-id files
    on (config_id, model, size, arm/policy) AND carry the same candidate_id;
  - the secondary row-level D1-d count at seed 20260519, B = 1,000, equals the
    count the unchanged Phase 5 analysis gave on the same CSV in S1-9
    (v0_5_phase5_blockA_tiebreakfix.json);
  - the primary deduplicated analysis at seed 20260927 reproduces the stored
    S1-1 output (v0_5_phase5_S1-1_cluster_bootstrap.json) exactly.

Modes:
  python -m src.analysis_S1_completion_s1_1 --selftest   # fabricated data, scratch
  python -m src.analysis_S1_completion_s1_1 --dry-run    # registered inputs, small B, scratch
  python -m src.analysis_S1_completion_s1_1              # real: writes
      results/v0_5_phase5_S1-1_cluster_bootstrap_completion.json
"""
from __future__ import annotations

import argparse
import json
import os
import random
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

from src import analysis_S1_cluster_bootstrap as s11
from src.registration_guard import code_provenance, require_signed, scratch_dir, sha256_file

RESULTS_DIR = s11.RESULTS_DIR
RAW_DIR = s11.RAW_DIR
OUT_NAME = "v0_5_phase5_S1-1_cluster_bootstrap_completion.json"
REG_PATH = s11.REG_PATH
SEEDS = s11.SENSITIVITY_SEEDS                 # 20260927 + i, i = 0..9
REF_SEEDS = [s11.SEED_REF + i for i in range(10)]

_DATA: dict = {}


# --------------------------------------------------------------------------
# Inputs
# --------------------------------------------------------------------------

def _join_with_embedded_ids(df: pd.DataFrame, ids: pd.DataFrame, keys: list,
                            label: str) -> pd.DataFrame:
    """Join a tie-break-fixed CSV (which embeds candidate_id) to the stored
    candidate-id file by row position, checking the keys and candidate_id."""
    embedded = df["candidate_id"].to_numpy()
    joined = s11._check_join(df.drop(columns=["candidate_id", "cand_seed"]),
                             ids, keys, label)
    mism = np.where(joined["candidate_id"].to_numpy() != embedded)[0]
    if len(mism):
        raise SystemExit(f"S1-1 completion STOP: {label}: candidate_id differs from "
                         f"the stored candidate-id file at row {int(mism[0])}")
    return joined


def load_real() -> tuple:
    paths = {
        "blockA": RAW_DIR / "mvs_v0_5_phase5_blockA.csv",
        "blockA_ids": RAW_DIR / "mvs_v0_5_phase5_blockA_candidate_ids.csv",
        "blockA_tiebreakfix": RAW_DIR / "mvs_v0_5_phase5_blockA_tiebreakfix.csv",
        "blockB_ids": RAW_DIR / "mvs_v0_5_phase5_blockB_candidate_ids.csv",
        "blockB_tiebreakfix": RAW_DIR / "mvs_v0_5_phase5_blockB_tiebreakfix.csv",
        "blockB_P7_tiebreakfix": RAW_DIR / "mvs_v0_5_phase5_ablation_P7_tiebreakfix.csv",
        "stored_S1-1_output": RESULTS_DIR / "v0_5_phase5_S1-1_cluster_bootstrap.json",
        "S1-9_blockA_tiebreakfix_json": RESULTS_DIR / "v0_5_phase5_blockA_tiebreakfix.json",
    }
    d = {k: pd.read_csv(p) for k, p in paths.items() if p.suffix == ".csv"}
    a_primary = s11._check_join(d["blockA"], d["blockA_ids"],
                                ["config_id", "model", "size", "arm"], "Block A (primary)")
    a_secondary = _join_with_embedded_ids(
        d["blockA_tiebreakfix"], d["blockA_ids"],
        ["config_id", "model", "size", "arm"], "Block A (tie-break-fixed)")
    # the favourable corner and design columns must equal the stored rows too
    for col in ["config_id", "F", "n_amrs", "n_elevators", "demand", "model", "size",
                "arm", "favorable_corner"]:
        if not (a_secondary[col].astype(str).to_numpy()
                == a_primary[col].astype(str).to_numpy()).all():
            raise SystemExit(f"S1-1 completion STOP: Block A tie-break-fixed column {col!r} "
                             "differs from the stored Block A rows")
    b_secondary = _join_with_embedded_ids(
        d["blockB_tiebreakfix"], d["blockB_ids"],
        ["config_id", "model", "size", "policy"], "Block B (tie-break-fixed)")
    data = {"A_primary": a_primary, "A_secondary": a_secondary,
            "B_secondary": b_secondary, "P7_secondary": d["blockB_P7_tiebreakfix"]}
    refs = {"stored_s1_1": json.loads(paths["stored_S1-1_output"].read_text("utf-8")),
            "s1_9_d1d": json.loads(paths["S1-9_blockA_tiebreakfix_json"]
                                   .read_text("utf-8"))["gates"]["D1d"]}
    hashes = {k: sha256_file(p) for k, p in paths.items()}
    return data, refs, hashes


def load_selftest() -> tuple:
    rng = random.Random(9101)          # fixture seed, unrelated to any registered seed
    a, a_ids = s11._fabricate_blockA(rng)
    b, b_ids, p7 = s11._fabricate_blockB(rng)
    a_primary = s11._check_join(a, a_ids, ["config_id", "model", "size", "arm"], "A [selftest]")
    a_fix = a.copy()
    a_fix["makespan"] = a_fix["makespan"] + 0.25
    a_fix["candidate_id"], a_fix["cand_seed"] = a_ids["candidate_id"], 1
    b_fix = b.copy()
    b_fix["candidate_id"], b_fix["cand_seed"] = b_ids["candidate_id"], 1
    a_secondary = _join_with_embedded_ids(a_fix, a_ids, ["config_id", "model", "size", "arm"],
                                          "A fix [selftest]")
    b_secondary = _join_with_embedded_ids(b_fix, b_ids, ["config_id", "model", "size", "policy"],
                                          "B fix [selftest]")
    data = {"A_primary": a_primary, "A_secondary": a_secondary,
            "B_secondary": b_secondary, "P7_secondary": p7}
    return data, None, "n/a (selftest: fabricated in memory)"


# --------------------------------------------------------------------------
# Parallel tasks (top-level functions so that worker processes can pickle them)
# --------------------------------------------------------------------------

def _init_worker(data: dict) -> None:
    _DATA.update(data)


def _task(kind: str, version: str, seed: int, B: int) -> tuple:
    if kind == "row_level":
        return kind, version, seed, s11.reference_row_level_blockA(_DATA[f"A_{version}"], B, seed)
    if kind == "clustered":
        return kind, version, seed, s11.blockA_clustered(_DATA[f"A_{version}"], B, seed)
    if kind == "dedup":
        return kind, version, seed, s11.blockA_dedup_companion(_DATA[f"A_{version}"], B, seed)
    if kind == "blockB":
        return kind, version, seed, s11.blockB_clustered(_DATA["B_secondary"],
                                                         _DATA["P7_secondary"], B, seed)
    raise ValueError(kind)


def run(data: dict, B: int, B_ref: int, n_seeds: int, workers: int) -> dict:
    seeds, ref_seeds = SEEDS[:n_seeds], REF_SEEDS[:n_seeds]
    tasks = ([("dedup", "primary", s, B) for s in seeds]
             + [("row_level", "secondary", s, B_ref) for s in ref_seeds]
             + [("clustered", "secondary", s, B) for s in seeds]
             + [("dedup", "secondary", s, B) for s in seeds]
             + [("blockB", "secondary", s11.SEED_MAIN, B)])
    with ProcessPoolExecutor(max_workers=workers, initializer=_init_worker,
                             initargs=(data,)) as ex:
        results = list(ex.map(_task, *zip(*tasks)))
    got = {(k, v, s): r for k, v, s, r in results}

    def counts(kind, version, ss):
        c = [got[(kind, version, s)] if kind == "row_level" else
             got[(kind, version, s)]["d1d_count"] for s in ss]
        return {"seeds": ss, "d1d_counts": c, "range": [min(c), max(c)]}

    main_seed = s11.SEED_MAIN
    return {
        "primary_stored_data": {
            "deduplicated_seed_sensitivity": counts("dedup", "primary", seeds),
            "_dedup_main": got[("dedup", "primary", main_seed)],
        },
        "secondary_tiebreakfix_data": {
            "blockA": {
                "reference_row_level": {"B": B_ref, "seed": s11.SEED_REF,
                                        "d1d_count": got[("row_level", "secondary", s11.SEED_REF)],
                                        "seed_sensitivity": counts("row_level", "secondary", ref_seeds)},
                "clustered": {"B": B, "seed": main_seed,
                              **got[("clustered", "secondary", main_seed)]},
                "clustered_seed_sensitivity": counts("clustered", "secondary", seeds),
                "deduplicated_companion": {"B": B, "seed": main_seed,
                                           **got[("dedup", "secondary", main_seed)]},
                "deduplicated_seed_sensitivity": counts("dedup", "secondary", seeds),
            },
            "blockB": {"B": B, "seed": main_seed, **got[("blockB", "secondary", main_seed)]},
        },
    }


def check_real(out: dict, refs: dict) -> dict:
    """The registered-run checks of the module docstring; any failure stops."""
    sec = out["secondary_tiebreakfix_data"]["blockA"]["reference_row_level"]["d1d_count"]
    if sec != refs["s1_9_d1d"]:
        raise SystemExit(f"S1-1 completion STOP: secondary row-level D1-d {sec} differs from "
                         f"the S1-9 regenerated D1-d {refs['s1_9_d1d']}")
    stored = refs["stored_s1_1"]["blockA"]["deduplicated_companion"]
    mine = out["primary_stored_data"].pop("_dedup_main")
    if mine != stored:
        raise SystemExit("S1-1 completion STOP: the primary deduplicated analysis at seed "
                         "20260927 does not reproduce the stored S1-1 output")
    return {"secondary_row_level_equals_S1-9_regenerated_D1d": True,
            "primary_dedup_seed_20260927_reproduces_stored_S1-1_output": True,
            "stored_S1-1_primary_dedup_count": stored["d1d_count"]}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    g = p.add_mutually_exclusive_group()
    g.add_argument("--selftest", action="store_true")
    g.add_argument("--dry-run", action="store_true")
    p.add_argument("--B", type=int, default=None)
    p.add_argument("--workers", type=int, default=max(1, min(16, (os.cpu_count() or 2) - 2)))
    args = p.parse_args()

    require_signed("S1A", selftest=args.selftest)
    if args.selftest:
        data, refs, hashes = load_selftest()
        B, B_ref, n_seeds = args.B or 100, 100, 3
    else:
        data, refs, hashes = load_real()
        full = not args.dry_run
        B = args.B or (s11.B_MAIN if full else 100)
        B_ref, n_seeds = (s11.B_REF, 10) if full else (100, 3)
    out = run(data, B, B_ref, n_seeds, args.workers)
    if args.selftest or args.dry_run:
        out["primary_stored_data"].pop("_dedup_main")
        checks = "skipped (selftest or dry run: reduced B)"
    else:
        checks = check_real(out, refs)
    result = {
        "item": "S1-1 completion (S1A general rule 5 secondary version; deduplicated seed range)",
        "registration_sha256": sha256_file(REG_PATH),
        "code_sha256": sha256_file(Path(__file__)), **code_provenance(),
        "input_sha256": hashes, "selftest": args.selftest, "dry_run": args.dry_run,
        "B": B, "B_ref": B_ref, "n_seeds": n_seeds, "checks": checks,
        "labels": {"primary": "stored artefact behind the locked verdict (D1-d 57/72, PARTIAL)",
                   "secondary": "tie-break-fixed data (current simulator), S1A general rule 5; "
                                "computed after the primary results had been seen; cannot "
                                "change any locked verdict"},
        **out,
    }
    out_path = (scratch_dir() if (args.selftest or args.dry_run) else RESULTS_DIR) / OUT_NAME
    out_path.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(f"S1-1 completion {'[selftest] ' if args.selftest else '[dry run] ' if args.dry_run else ''}"
          f"wrote {out_path}")


if __name__ == "__main__":
    main()
