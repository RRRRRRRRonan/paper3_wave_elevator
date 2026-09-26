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
these NEW CSVs (both modules hard-code their input/output paths, so this
script reimplements their loop bodies against explicit paths rather than
calling their `main()`, which would silently overwrite the stored JSONs --
S1-9's own "Design": "the stored JSONs are not touched"). A side-by-side
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
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

from src import phase5_config as cfg
from src.analysis_phase5_blockA import CORNERS, decompose
from src.experiments_phase5 import run_corner_block, run_policy_block
from src.experiments_phase5_ablation import P7_ITER, run_p7
from src.registration_guard import TOY_SEED_BASE, require_signed, scratch_dir

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RAW_DIR = RESULTS_DIR / "raw"
REG_PATH = (Path(__file__).resolve().parents[2] / "revision_2026-09-26_ijpr"
            / "amendments" / "AMEND-2026-09-26-S1B_new_simulations.md")

N_BOOT_A = 1000          # analysis_phase5_blockA.N_BOOT, mirrored exactly
SEED_A = 20260519        # analysis_phase5_blockA.SEED, mirrored exactly
POLICIES_B = ["P0_random", "P1_dest_cluster", "P2_cardinality",
             "P3_dir_balanced", "P4_temporal", "P5_phi", "P6_spo_tree"]
# S1-9 "Prior exposure" (B-14, a fixed disclosed fact, not computed here).
B14_EXPOSURE = ("15.6% of elevator requests faced an availability tie, "
               "5.1% a tie between units on different floors")


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


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
# Block A analysis, mirroring analysis_phase5_blockA.main() exactly, against
# an explicit csv_path (that module hard-codes its path and cannot be called
# with one -- see module docstring).
# --------------------------------------------------------------------------

def analyze_blockA(df: pd.DataFrame) -> dict:
    rng = np.random.default_rng(SEED_A)
    rows = []
    for (cid, model, size), g in df.groupby(["config_id", "model", "size"]):
        fav = g["favorable_corner"].iloc[0]
        arms = {c: g[g["arm"] == c]["makespan"].to_numpy(float) for c in CORNERS}
        rnd = g[g["arm"] == "random"]["makespan"].to_numpy(float)
        m_q = {c: float(np.median(arms[c])) for c in CORNERS}
        m0 = float(np.median(rnd))
        H_up, M_phi, UB, LB, qmax, qmin = decompose(m_q, m0, fav)
        GAP = H_up + M_phi
        spo = (m_q[fav] - m_q[qmin]) / m0

        boot = np.empty(N_BOOT_A)
        for b in range(N_BOOT_A):
            mb = {c: float(np.median(rng.choice(arms[c], size=len(arms[c]),
                                                replace=True)))
                 for c in CORNERS}
            m0b = float(np.median(rng.choice(rnd, size=len(rnd), replace=True)))
            hb, mpb, *_ = decompose(mb, m0b, fav)
            boot[b] = hb + mpb
        lo, hi = (float(x) for x in np.percentile(boot, [2.5, 97.5]))

        rows.append({
            "config_id": int(cid), "F": int(g["F"].iloc[0]),
            "n_amrs": int(g["n_amrs"].iloc[0]),
            "n_elevators": int(g["n_elevators"].iloc[0]),
            "demand": g["demand"].iloc[0], "model": model, "size": int(size),
            "H_up": H_up, "M_Phi": M_phi, "GAP": GAP, "SPO_regret": spo,
            "gap_ci_lo": lo, "gap_ci_hi": hi,
            "d1a": bool(abs(GAP - (UB - LB)) < 1e-9),
            "d1b": bool(H_up >= -1e-12 and M_phi >= -1e-12),
            "d1c": bool(abs(M_phi - spo) < 1e-12),
            "d1d": bool(lo > 0.0),
        })

    n = len(rows)
    g_a = sum(r["d1a"] for r in rows)
    g_b = sum(r["d1b"] for r in rows)
    g_c = sum(r["d1c"] for r in rows)
    g_d = sum(r["d1d"] for r in rows)
    d1d_thresh = int(np.ceil(0.80 * n)) if n else 0
    verdict = ("PASS" if (n and g_a == n and g_b == n and g_c == n
                         and g_d >= d1d_thresh) else "PARTIAL")
    Fs = np.array([r["F"] for r in rows], float)
    GAPs = np.array([r["GAP"] for r in rows], float)
    gap_F_corr = float(np.corrcoef(Fs, GAPs)[0, 1]) if n > 1 else float("nan")

    by_demand = {}
    for dem in ["uniform", "clustered", "diurnal"]:
        sub = [r for r in rows if r["demand"] == dem]
        if not sub:
            continue
        by_demand[dem] = {"mean_GAP": float(np.mean([r["GAP"] for r in sub])),
                         "n": len(sub), "d1d_pass": sum(r["d1d"] for r in sub)}

    return {"generated": date.today().isoformat(), "block": "A",
           "hypothesis": "H-D1", "n_subcells": n,
           "gates": {"D1a": g_a, "D1b": g_b, "D1c": g_c, "D1d": g_d,
                    "D1d_threshold": d1d_thresh},
           "verdict": verdict, "mean_GAP": float(np.mean(GAPs)) if n else None,
           "corr_F_GAP": gap_F_corr, "by_demand": by_demand, "per_subcell": rows}


# --------------------------------------------------------------------------
# Block B analysis, mirroring analysis_phase5_blockB.main() exactly.
# --------------------------------------------------------------------------

def analyze_blockB(dfB: pd.DataFrame, dfP7: pd.DataFrame) -> dict:
    cells = []
    for (cid, size), g in dfB.groupby(["config_id", "size"]):
        med = {p: float(np.median(g[g["policy"] == p]["makespan"]))
              for p in POLICIES_B if (g["policy"] == p).any()}
        g7 = dfP7[(dfP7.config_id == cid) & (dfP7["size"] == size)]
        if len(g7):
            med["P7_localsearch"] = float(np.median(g7["makespan"]))
        cells.append({"config_id": int(cid), "size": int(size), **med})

    n = len(cells)
    allp = [p for p in POLICIES_B + ["P7_localsearch"]
           if all(p in c for c in cells)]
    win = {i: {} for i in allp}
    for i in allp:
        for j in allp:
            win[i][j] = (float("nan") if i == j
                        else float(np.mean([c[i] < c[j] for c in cells])))

    out = {"generated": date.today().isoformat(), "block": "B",
          "hypothesis": "H-Policy", "n_cells": n, "win_matrix": win}
    if "P5_phi" in allp:
        p5v0 = win["P5_phi"].get("P0_random")
        p5v1 = win["P5_phi"].get("P1_dest_cluster")
        p5v6 = win["P5_phi"].get("P6_spo_tree")
        p5v7 = win["P5_phi"].get("P7_localsearch")
        if p5v0 is not None and p5v1 is not None and p5v6 is not None:
            if p5v0 >= 0.90 and p5v1 >= 0.60 and p5v6 >= 0.50:
                band = "Policy-Strong"
            elif p5v0 >= 0.75 and p5v1 >= 0.50:
                band = "Policy-Partial"
            elif p5v0 < 0.25:
                band = "Policy-Weak"
            else:
                band = "Policy-Partial (lower)"
            out.update({"P5_vs_P0": p5v0, "P5_vs_P1": p5v1, "P5_vs_P6": p5v6,
                      "P5_vs_P7": p5v7, "band": band})
    out["mean_median_makespan"] = {p: float(np.mean([c[p] for c in cells]))
                                   for p in allp}
    out["per_cell"] = cells
    return out


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

    regen_a = analyze_blockA(dfs["blockA"])
    regen_b = analyze_blockB(dfs["blockB"], dfs["blockP7"])

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
