"""
S1-11 completion [NS] -- the S1-11 quantities that the run of 2026-09-26
(EXECUTION-LOG entry 55) did not produce (entry 57):

  (1) "Per pool, the S1-2 quantities": the covering partitions (2 x 2, 3 x 3,
      4 x 4) and the minimax-reduction (Theorem 2) quantities on full classes,
      for all 216 pools (36 new configurations and the 18 Phase 5
      configurations, both seed models, n in {8, 30}).
  (2) "the two-factor interaction table for F x demand": the balanced
      full-factorial interaction contrasts (cell mean - F mean - demand mean
      + grand mean) beside the cell means already reported, per (model, size)
      slice, for log median makespan and GAP.

The pools are re-enumerated with the unchanged functions of
experiments_S1_enumeration (imported, not copied): enumerate_pool,
fit_phi_beta, favorable_label, corner_family_quantities, covering_partition,
theorem2_full_classes. Check that stops the run (real mode): the corner
quantities of every pool (m0, class medians, GAP of the full-pool-fit corner)
and both pool optima must equal the stored S1-11 output
(v0_5_phase5_S1-11_factorial.json) exactly.

Modes:
  python -m src.experiments_S1_completion_s1_11 --selftest  # toy seeds, 2 configs, scratch
  python -m src.experiments_S1_completion_s1_11 --dry-run   # registered pools, 2 configs, scratch
  python -m src.experiments_S1_completion_s1_11             # real: writes
      results/v0_5_phase5_S1-11_factorial_completion.json
"""
from __future__ import annotations

import argparse
import json
import os
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

from src import experiments_S1_enumeration as en
from src import phase5_config as cfg
from src.experiments_phase5 import MODEL_TAG
from src.registration_guard import (TOY_SEED_BASE, code_provenance, require_checkbox,
                                    require_signed, scratch_dir, sha256_file)
from src.wave_policies import favorable_label, fit_phi_beta

RESULTS_DIR = en.RESULTS_DIR
OUT_NAME = "v0_5_phase5_S1-11_factorial_completion.json"
STORED_NAME = "v0_5_phase5_S1-11_factorial.json"


def _pool_task(config: dict, size: int, cand_n: int, seed_model: str,
               seed_base: int) -> dict:
    cfg.SEED_BASE = seed_base                     # worker processes start fresh
    pr = en.enumerate_pool(config, size, cand_n, seed_model, "A")
    mk = pr["makespans"][MODEL_TAG[seed_model]]
    beta = fit_phi_beta(pr["cand"], mk)
    fav = favorable_label(beta)
    cq = en.corner_family_quantities(pr["cand"], mk, {"full_pool_fit": fav})
    return {"config_id": config["config_id"], "seed_model": seed_model, "size": size,
            "F": config["F"], "n_amrs": config["n_amrs"],
            "n_elevators": config["n_elevators"], "demand": config["demand"],
            "optimum_M1": en.pool_optimum(pr["makespans"]["M1"]),
            "optimum_M2": en.pool_optimum(pr["makespans"]["M2"]),
            "corner_quantities_this_model": cq,
            "covering_partitions_this_model": {n: en.covering_partition(pr["cand"], mk, n, beta)
                                               for n in (2, 3, 4)},
            "theorem2_full_classes": en.theorem2_full_classes(
                pr["cand"], pr["makespans"]["M1"], pr["makespans"]["M2"])}


def interaction_contrasts(summary_rows: list) -> dict:
    """Balanced two-factor F x demand contrasts per response, per slice."""
    df = pd.DataFrame(summary_rows)
    out = {}
    for resp in ("log_median_makespan", "GAP"):
        grand = float(df[resp].mean())
        f_mean = df.groupby("F")[resp].mean()
        d_mean = df.groupby("demand")[resp].mean()
        cells = df.groupby(["F", "demand"])[resp].agg(["mean", "size"])
        out[resp] = {
            "grand_mean": grand,
            "cell_mean": {f"{f}|{d}": float(r["mean"]) for (f, d), r in cells.iterrows()},
            "cell_n": {f"{f}|{d}": int(r["size"]) for (f, d), r in cells.iterrows()},
            "interaction_contrast": {f"{f}|{d}": float(r["mean"] - f_mean[f] - d_mean[d] + grand)
                                     for (f, d), r in cells.iterrows()},
        }
    return out


def _same(a, b) -> bool:
    return json.dumps(a, sort_keys=True, default=str) == json.dumps(b, sort_keys=True, default=str)


def check_against_stored(pools: list, stored: dict) -> dict:
    by_key = {(p["config_id"], p["seed_model"], p["size"]): p for p in stored["pools"]}
    n = 0
    for p in pools:
        s = by_key.get((p["config_id"], p["seed_model"], p["size"]))
        if s is None:
            raise SystemExit(f"S1-11 completion STOP: pool {p['config_id']}/{p['seed_model']}/"
                             f"{p['size']} is not in the stored S1-11 output")
        for k in ("optimum_M1", "optimum_M2", "corner_quantities_this_model"):
            if not _same(p[k], s[k]):
                raise SystemExit(f"S1-11 completion STOP: {k} of pool {p['config_id']}/"
                                 f"{p['seed_model']}/{p['size']} differs from the stored output")
        n += 1
    if n != len(stored["pools"]):
        raise SystemExit(f"S1-11 completion STOP: {n} pools re-enumerated, stored output has "
                         f"{len(stored['pools'])}")
    return {"pools_checked": n, "all_equal_to_stored_S1-11_output": True}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    g = p.add_mutually_exclusive_group()
    g.add_argument("--selftest", action="store_true")
    g.add_argument("--dry-run", action="store_true")
    p.add_argument("--workers", type=int, default=max(1, min(16, (os.cpu_count() or 2) - 2)))
    args = p.parse_args()

    require_signed("S1B", selftest=args.selftest)
    require_checkbox("S1B", "S1-11 included", "yes", selftest=args.selftest)

    if args.selftest:
        seed_base, cand_n, sizes = TOY_SEED_BASE, 80, [8]
        configs = en.make_s1_11_configs()[:1] + cfg.make_config_array()[:1]
    else:
        seed_base, cand_n, sizes = cfg.SEED_BASE, cfg.CANDIDATE_POOL, [8, 30]
        configs = en.make_s1_11_configs() + cfg.make_config_array()
        if args.dry_run:
            configs = configs[:1] + configs[36:37]
    jobs = [(c, n, cand_n, sm, seed_base) for c in configs for n in sizes
            for sm in ("abstraction", "batched")]
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        pools = list(ex.map(_pool_task, *zip(*jobs)))

    slices = {}
    for m in ("M1", "M2"):
        for n in sizes:
            rows = [{"F": q["F"], "demand": q["demand"],
                     "log_median_makespan": float(np.log(q["corner_quantities_this_model"]["m0"])),
                     "GAP": q["corner_quantities_this_model"]["decompositions"]["full_pool_fit"]["GAP"]}
                    for q in pools if MODEL_TAG[q["seed_model"]] == m and q["size"] == n]
            slices[f"{m}_n{n}"] = {"n_configs": len(rows), **interaction_contrasts(rows)}

    stored_path = RESULTS_DIR / STORED_NAME
    if args.selftest or args.dry_run:
        checks = "skipped (selftest or dry run: subset of pools)"
    else:
        checks = check_against_stored(pools, json.loads(stored_path.read_text("utf-8")))

    reg = en.REG_PATH
    result = {
        "item": "S1-11 completion (per-pool covering partitions and Theorem 2 quantities; "
                "F x demand interaction contrasts)",
        "registration_sha256": sha256_file(reg),
        "code_sha256": sha256_file(Path(__file__)), **code_provenance(),
        "input_sha256": ({} if args.selftest else {STORED_NAME: sha256_file(stored_path)}),
        "selftest": args.selftest, "dry_run": args.dry_run, "cand_n": cand_n, "sizes": sizes,
        "checks": checks,
        "label": "closed-form descriptive layer on the full factorial (S1-11 reporting rule); "
                 "not compared with the locked verdicts",
        "M_Phi_note": "covering-partition M_Phi(P) uses the extreme bin in the direction of the "
                      "fitted signs (a labelled generalization of the corner rule, as in S1-2)",
        "pools": pools,
        "F_x_demand_by_slice": slices,
    }
    out_path = (scratch_dir() if (args.selftest or args.dry_run) else RESULTS_DIR) / OUT_NAME
    out_path.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(f"S1-11 completion {'[selftest] ' if args.selftest else '[dry run] ' if args.dry_run else ''}"
          f"wrote {out_path} ({len(pools)} pools)")


if __name__ == "__main__":
    main()
