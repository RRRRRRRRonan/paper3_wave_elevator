"""
Study 1 display completion -- registered displays and fields that the run of
2026-09-26 (EXECUTION-LOG entry 55) did not produce (entry 57). Every number
is read from a stored Phase 5 artefact or from an output of that run, or is
computed by the unchanged Phase 5 analysis code; nothing is re-estimated.

  s1-2   S1B S1-2 reporting rule: sampled (preregistered) and exact
         (enumeration, [NS]) values side by side -- Block A GAP decomposition,
         Block C D2 quantities and Hedge corners, covering partitions against
         A-R1, Block B gap to the pool optimum.
  s1-6   S1A S1-6 display: one row per configuration, with the S1-3 [NS]
         extension rows added, labels decided on the class-median basis.
  s1-9   S1B S1-9: (a) cell values of the stored and regenerated Blocks A and
         B side by side; (b) the unchanged analysis_phase5_ablation run on the
         regenerated Block A, B and P7 CSVs (first checked to reproduce the
         stored v0_5_phase5_ablation.json from the stored CSVs), written to
         v0_5_phase5_ablation_tiebreakfix.json; (c) the provenance record that
         general rule 4 asks for, for the *_tiebreakfix files of S1-9.
  s1-12  S1B S1-12: the pinned-hash field, the proxy flag derived from the
         registered gates, and a check of the tie-break-only column against
         the stored B-5 output.
  th-2   S1A TH-2 display: facets E, F, n (Block C with the S1-3 [NS] rows)
         and c (Supp-2), each as drawn and deduplicated by candidate where
         identifiers exist; reversal shares; cross-reference of the reversal
         waves with the B-1 channel decomposition; figure in Times New Roman.

Modes (for every command):
  --selftest   helper functions on fabricated frames, figure to scratch
  --dry-run    registered inputs read only, outputs to scratch
  (none)       real: writes the files named in each command under results/
"""
from __future__ import annotations

import argparse
import importlib
import json
import random
import shutil
import tempfile
import warnings
from datetime import date
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

from src.analysis_phase5_blockA import CORNERS, decompose
from src.registration_guard import code_provenance, require_signed, scratch_dir, sha256_file

PROTO = Path(__file__).resolve().parents[1]
REPO = PROTO.parent
RESULTS_DIR = PROTO / "results"
RAW_DIR = RESULTS_DIR / "raw"
FIG_DIR = RESULTS_DIR / "figures"
TIER2 = REPO / "revision_2026-07-08" / "tier2_analysis" / "outputs"
REG = {"S1A": REPO / "revision_2026-09-26_ijpr" / "amendments" / "AMEND-2026-09-26-S1A_reanalyses.md",
       "S1B": REPO / "revision_2026-09-26_ijpr" / "amendments" / "AMEND-2026-09-26-S1B_new_simulations.md"}
BLOCK_C_CONFIGS = [1, 3, 5, 7, 9, 11]
STAB_THRESHOLD, MARGIN_THRESHOLD = 0.80, 0.01          # S1-6 wording rule (locked)


def _load(path: Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _meta(reg_key: str, inputs: dict, mode: str) -> dict:
    return {"registration_sha256": sha256_file(REG[reg_key]),
            "code_sha256": sha256_file(Path(__file__)), **code_provenance(),
            "input_sha256": {k: sha256_file(p) for k, p in inputs.items()},
            "mode": mode}


def _write(obj: dict, name: str, mode: str, subdir: Optional[str] = None) -> Path:
    base = scratch_dir() if mode != "real" else (RESULTS_DIR if subdir is None else RESULTS_DIR / subdir)
    base.mkdir(parents=True, exist_ok=True)
    path = base / name
    path.write_text(json.dumps(obj, indent=2, default=str), encoding="utf-8")
    return path


# ==========================================================================
# s1-2: sampled (preregistered) against exact (enumeration) side by side
# ==========================================================================

def sampled_blockA_corners(blockA_csv: pd.DataFrame) -> dict:
    """Sampled class medians, favourable corner, q_max and q_min per sub-cell,
    recomputed from the stored Block A rows with the stored decompose()."""
    out = {}
    for (cid, model, size), g in blockA_csv.groupby(["config_id", "model", "size"]):
        fav = g["favorable_corner"].iloc[0]
        m_q = {c: float(g[g["arm"] == c]["makespan"].median()) for c in CORNERS}
        m0 = float(g[g["arm"] == "random"]["makespan"].median())
        H_up, M_phi, UB, LB, qmax, qmin = decompose(m_q, m0, fav)
        out[(int(cid), str(model), int(size))] = {
            "favorable": fav, "m0": m0, "class_medians": m_q, "H_up": H_up,
            "M_Phi": M_phi, "GAP": H_up + M_phi, "q_max": qmax, "q_min": qmin}
    return out


def cmd_s1_2(mode: str) -> list:
    inputs = {"blockA_json": RESULTS_DIR / "v0_5_phase5_blockA.json",
              "blockA_csv": RAW_DIR / "mvs_v0_5_phase5_blockA.csv",
              "blockC_json": RESULTS_DIR / "v0_5_phase5_blockC.json",
              "S1-2": RESULTS_DIR / "v0_5_phase5_S1-2_enumeration.json",
              "A-R1": TIER2 / "ar1_partition_sensitivity.json"}
    a_json, e, c_json, ar1 = (_load(inputs["blockA_json"]), _load(inputs["S1-2"]),
                              _load(inputs["blockC_json"]), _load(inputs["A-R1"]))
    sampled = sampled_blockA_corners(pd.read_csv(inputs["blockA_csv"]))
    locked = {(r["config_id"], r["model"], r["size"]): r for r in a_json["per_subcell"]}

    rows_a = []
    for p in e["pools"]:
        if p["block"] != "A":
            continue
        k = (p["config_id"], p["seed_model"], p["size"])
        s, lk = sampled[k], locked[k]
        # the recomputed sampled values must equal the locked JSON's values
        for q in ("H_up", "M_Phi", "GAP"):
            if abs(s[q] - lk[q]) > 1e-12:
                raise SystemExit(f"S1-2 table STOP: sampled {q} of {k} differs from the locked JSON")
        cq = p["corner_quantities_this_model"]
        ds, df_ = cq["decompositions"]["stored"], cq["decompositions"]["full_pool_fit"]
        cov = p["covering_partitions_this_model"]
        rows_a.append({
            "config_id": k[0], "model": k[1], "size": k[2],
            "sampled_preregistered": {"favorable": s["favorable"], "m0": s["m0"],
                                      "q_max": s["q_max"], "q_min": s["q_min"],
                                      "H_up": s["H_up"], "M_Phi": s["M_Phi"], "GAP": s["GAP"],
                                      "gap_ci": [lk["gap_ci_lo"], lk["gap_ci_hi"]], "d1d": lk["d1d"]},
            "exact_enumeration_NS": {
                "m0": cq["m0"], "class_medians": cq["class_medians"],
                "stored_corner": {q: ds[q] for q in ("favorable", "q_max", "q_min", "H_up", "M_Phi", "GAP")},
                "full_pool_fit_corner": {q: df_[q] for q in ("favorable", "q_max", "q_min", "H_up", "M_Phi", "GAP")},
                "covering_share_H_up_over_UB": {n: cov[n]["share_H_up_over_UB"] for n in ("2", "3", "4")},
                "optimum_M1": p["optimum_M1"]["optimum"], "optimum_M2": p["optimum_M2"]["optimum"]},
            "favorable_stored_equals_full_pool_fit": ds["favorable"] == df_["favorable"],
        })

    def pooled(rows, getter):
        h = [getter(r)["H_up"] for r in rows]
        m = [getter(r)["M_Phi"] for r in rows]
        return {"mean_H_up": float(np.mean(h)), "mean_M_Phi": float(np.mean(m)),
                "mean_GAP": float(np.mean(h) + np.mean(m)),
                "H_up_share_of_mean_GAP": float(np.mean(h) / (np.mean(h) + np.mean(m))),
                "n_M_Phi_zero": int(sum(x == 0 for x in m))}

    summary_a = {
        "n_subcells": len(rows_a),
        "sampled_preregistered": pooled(rows_a, lambda r: r["sampled_preregistered"]),
        "exact_stored_corner_NS": pooled(rows_a, lambda r: r["exact_enumeration_NS"]["stored_corner"]),
        "exact_full_pool_fit_corner_NS": pooled(rows_a, lambda r: r["exact_enumeration_NS"]["full_pool_fit_corner"]),
        "n_favorable_stored_equals_full_pool_fit": int(sum(r["favorable_stored_equals_full_pool_fit"] for r in rows_a)),
        "n_q_max_sampled_equals_exact_stored_corner": int(sum(
            r["sampled_preregistered"]["q_max"] == r["exact_enumeration_NS"]["stored_corner"]["q_max"] for r in rows_a)),
        "n_q_min_sampled_equals_exact_stored_corner": int(sum(
            r["sampled_preregistered"]["q_min"] == r["exact_enumeration_NS"]["stored_corner"]["q_min"] for r in rows_a)),
    }
    shares = {n: [r["exact_enumeration_NS"]["covering_share_H_up_over_UB"][n] for r in rows_a
                  if r["exact_enumeration_NS"]["covering_share_H_up_over_UB"][n] is not None]
              for n in ("2", "3", "4")}
    summary_a["exact_covering_share_median_NS"] = {n: float(np.median(v)) for n, v in shares.items()}

    # Block C: locked D2 quantities (sampled, 200 waves per corner) against full classes
    d2 = {(r["config_id"], r["corner"]): r for r in c_json["H_D2"]["per_cell"]}
    coll = {r["config_id"]: r for r in c_json["H_D2"]["per_config_collapse"]}
    ra = {r["config_id"]: r for r in c_json["RA_median_hedge_sensitivity"]["per_config"]}
    ar1_rows = {(r["config_id"], r["scheme"]): r for r in ar1["per_config_scheme"]}
    rows_c = []
    for p in e["pools"]:
        if p["block"] != "C":
            continue
        cid, th = p["config_id"], p["theorem2_full_classes"]
        per_corner = []
        for c in CORNERS:
            s, x = d2[(cid, c)], th["per_corner"][c]
            per_corner.append({"corner": c,
                               "sampled_ordering_rate": s["perwave_dom"],
                               "exact_ordering_rate_full_class_NS": x["ordering_rate_M1_le_M2"],
                               "sampled_U_c_005": s["U_c_005"],
                               "exact_U_c_005_full_class_NS": x["U_c_0.05"]})
        cov = p["covering_partitions_this_model"]
        rows_c.append({
            "config_id": cid, "per_corner": per_corner,
            "hedge_corner_mean_basis": {"sampled_preregistered_D2d": coll[cid]["c_star_Hedge"],
                                        "exact_full_class_NS": th["minimax_corner_mean_basis"]},
            "hedge_corner_median_basis": {"sampled_RA_2026-09-11": ra[cid]["c_star_Hedge_median"],
                                          "exact_full_class_NS": th["minimax_corner"]},
            "covering_share_H_up_over_UB": {
                "2x2": {"sampled_A-R1": ar1_rows[(cid, "2x2_CI")]["capacity_share"],
                        "exact_NS": cov["2"]["share_H_up_over_UB"]},
                "3x3": {"sampled_A-R1": ar1_rows[(cid, "3x3_CI")]["capacity_share"],
                        "exact_NS": cov["3"]["share_H_up_over_UB"]},
                "4x4": {"sampled_A-R1": None, "exact_NS": cov["4"]["share_H_up_over_UB"]}},
        })
    summary_c = {
        "n_configs": len(rows_c),
        "n_hedge_mean_basis_agree": int(sum(r["hedge_corner_mean_basis"]["sampled_preregistered_D2d"]
                                            == r["hedge_corner_mean_basis"]["exact_full_class_NS"] for r in rows_c)),
        "n_hedge_median_basis_agree": int(sum(r["hedge_corner_median_basis"]["sampled_RA_2026-09-11"]
                                              == r["hedge_corner_median_basis"]["exact_full_class_NS"] for r in rows_c)),
        "sampled_ordering_rate_average": float(np.mean([x["sampled_ordering_rate"] for r in rows_c for x in r["per_corner"]])),
        "exact_ordering_rate_average_NS": float(np.mean([x["exact_ordering_rate_full_class_NS"] for r in rows_c for x in r["per_corner"]])),
        "exact_ordering_rate_worst_NS": float(np.min([x["exact_ordering_rate_full_class_NS"] for r in rows_c for x in r["per_corner"]])),
        "A-R1_note": "A-R1 used the stored A4 ablation scheme data (sampled arms, size 16, M2); the exact "
                     "values are the full Block C pools of S1-2 (size 16, M2)",
    }
    out = {"item": "S1-2 side-by-side display", **_meta("S1B", inputs, mode),
           "labels": {"sampled": "sampled, preregistered", "exact": "exact enumeration, [NS]"},
           "reporting_rule": "No locked count is recomputed from exact values.",
           "blockA": {"summary": summary_a, "per_subcell": rows_a},
           "blockC": {"summary": summary_c, "per_config": rows_c},
           "blockB_gap_to_optimum": {"rows": e["block_b_gap_to_optimum"],
                                     "note": "sampled policy medians (stored, pre tie-break fix) against "
                                             "the exact pool optimum (current simulator)"}}
    paths = [_write(out, "v0_5_phase5_S1-2_side_by_side.json", mode)]
    flat = [{"config_id": r["config_id"], "model": r["model"], "size": r["size"],
             **{f"sampled_{q}": r["sampled_preregistered"][q] for q in
                ("favorable", "q_max", "q_min", "H_up", "M_Phi", "GAP")},
             **{f"exact_stored_{q}": r["exact_enumeration_NS"]["stored_corner"][q] for q in
                ("q_max", "q_min", "H_up", "M_Phi", "GAP")},
             **{f"exact_fit_{q}": r["exact_enumeration_NS"]["full_pool_fit_corner"][q] for q in
                ("favorable", "H_up", "M_Phi", "GAP")},
             **{f"exact_cov{n}_share": r["exact_enumeration_NS"]["covering_share_H_up_over_UB"][n]
                for n in ("2", "3", "4")}} for r in rows_a]
    csv_dir = scratch_dir() if mode != "real" else RAW_DIR
    csv_path = csv_dir / "mvs_v0_5_phase5_S1-2_side_by_side_blockA.csv"
    pd.DataFrame(flat).to_csv(csv_path, index=False)
    return paths + [csv_path]


# ==========================================================================
# s1-6: display with the S1-3 [NS] extension rows
# ==========================================================================

def s1_6_row(mean_b: dict, median_b: dict) -> dict:
    """One display row; labels on the class-median basis (locked wording rule)."""
    lab = {"not_stable_under_resampling": median_b["hedge_stability"] < STAB_THRESHOLD,
           "near_tie": median_b["second_place_margin"] < MARGIN_THRESHOLD}
    mean_lab = {"not_stable_under_resampling": mean_b["hedge_stability"] < STAB_THRESHOLD,
                "near_tie": mean_b["second_place_margin"] < MARGIN_THRESHOLD}
    return {
        "hedge_corner": {"mean": mean_b["hedge_corner"], "median": median_b["hedge_corner"]},
        "minimax_regret_corner": {"mean": mean_b["minimax_regret_corner"],
                                  "median": median_b["minimax_regret_corner"]},
        "agree_hedge_vs_minimax_regret": {"mean": mean_b["hedge_corner"] == mean_b["minimax_regret_corner"],
                                          "median": median_b["hedge_corner"] == median_b["minimax_regret_corner"]},
        "agree_mean_vs_median_hedge": mean_b["hedge_corner"] == median_b["hedge_corner"],
        "second_place_margin": {"mean": mean_b["second_place_margin"], "median": median_b["second_place_margin"]},
        "hedge_stability": {"mean": mean_b["hedge_stability"], "median": median_b["hedge_stability"]},
        "minimax_regret_stability": {"mean": mean_b["minimax_regret_stability"],
                                     "median": median_b["minimax_regret_stability"]},
        "labels_median_basis": lab,
        "label_differs_on_mean_basis": {k: mean_lab[k] != lab[k] for k in lab},
    }


def cmd_s1_6(mode: str) -> list:
    inputs = {"S1-6": RESULTS_DIR / "v0_5_phase5_S1-6_minimax_stability.json",
              "S1-3": RESULTS_DIR / "v0_5_phase5_S1-3_blockC_ext.json"}
    s6, s3 = _load(inputs["S1-6"]), _load(inputs["S1-3"])
    rows = []
    for source in ("primary_stored", "secondary_tiebreakfix"):
        by = {}
        for r in s6["per_config_basis"]:
            if r["source"] == source:
                by.setdefault(r["config_id"], {})[r["basis"]] = r
        for cid in sorted(by):
            rows.append({"block": "C", "source": source, "config_id": cid, "size": 16, "tag": "[RA]",
                         **s1_6_row(by[cid]["mean"], by[cid]["median"])})
    for u in s3["units"]:
        mb, db = u["s1_6_mean_basis"], u["s1_6_median_basis"]
        flat = lambda b: {**b["full_data"], "hedge_stability": b["hedge_stability"],
                          "minimax_regret_stability": b["minimax_regret_stability"]}
        rows.append({"block": "C extension (S1-3)", "source": "current simulator", "config_id": u["config_id"],
                     "size": u["size"], "tag": "[NS] extension row", **s1_6_row(flat(mb), flat(db))})

    def tally(rs):
        return {"n": len(rs),
                "n_not_stable_median_basis": int(sum(r["labels_median_basis"]["not_stable_under_resampling"] for r in rs)),
                "n_near_tie_median_basis": int(sum(r["labels_median_basis"]["near_tie"] for r in rs)),
                "n_mean_median_hedge_agree": int(sum(r["agree_mean_vs_median_hedge"] for r in rs)),
                "n_hedge_equals_minimax_regret_median": int(sum(r["agree_hedge_vs_minimax_regret"]["median"] for r in rs))}
    out = {"item": "S1-6 display with S1-3 extension rows", **_meta("S1A", inputs, mode),
           "wording_rule": "labels decided on the class-median basis; class-mean values in the same row; "
                           "disagreements stated in the same sentence; prior-exposed configurations labelled",
           "locked_D2d_collapse": s6["locked_D2d_collapse"],
           "tally": {"block_C_primary": tally([r for r in rows if r["source"] == "primary_stored"]),
                     "block_C_secondary": tally([r for r in rows if r["source"] == "secondary_tiebreakfix"]),
                     "extension_NS": tally([r for r in rows if r["tag"].startswith("[NS]")])},
           "rows": rows}
    return [_write(out, "v0_5_phase5_S1-6_display_with_extension.json", mode)]


# ==========================================================================
# s1-9: cell side by side, ablation on regenerated CSVs, provenance
# ==========================================================================

def _run_ablation(raw_files: dict) -> dict:
    """Run the unchanged analysis_phase5_ablation.main on the given raw CSVs in
    a temporary folder, with a freshly imported module (its bootstrap RNG is a
    module-level generator seeded at import, as in the stored run)."""
    from src import analysis_phase5_ablation as abl
    abl = importlib.reload(abl)
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        raw = tmp / "raw"
        raw.mkdir()
        for name, src_path in raw_files.items():
            shutil.copyfile(src_path, raw / name)
        abl.RAW, abl.RESULTS_DIR = raw, tmp
        abl.main()
        return json.loads((tmp / "v0_5_phase5_ablation.json").read_text("utf-8"))


def _canon(o) -> str:
    return json.dumps(o, sort_keys=True, default=str)


def cmd_s1_9(mode: str) -> list:
    names = {"A": "mvs_v0_5_phase5_blockA.csv", "B": "mvs_v0_5_phase5_blockB.csv",
             "P7": "mvs_v0_5_phase5_ablation_P7.csv", "S": "mvs_v0_5_phase5_ablation_scheme.csv"}
    fix = {"A": RAW_DIR / "mvs_v0_5_phase5_blockA_tiebreakfix.csv",
           "B": RAW_DIR / "mvs_v0_5_phase5_blockB_tiebreakfix.csv",
           "P7": RAW_DIR / "mvs_v0_5_phase5_ablation_P7_tiebreakfix.csv"}
    inputs = {"stored_blockA_json": RESULTS_DIR / "v0_5_phase5_blockA.json",
              "stored_blockB_json": RESULTS_DIR / "v0_5_phase5_blockB.json",
              "stored_ablation_json": RESULTS_DIR / "v0_5_phase5_ablation.json",
              "regen_blockA_json": RESULTS_DIR / "v0_5_phase5_blockA_tiebreakfix.json",
              "regen_blockB_json": RESULTS_DIR / "v0_5_phase5_blockB_tiebreakfix.json",
              "S1-9_comparison": RESULTS_DIR / "v0_5_phase5_S1-9_comparison.json",
              **{f"stored_{k}_csv": RAW_DIR / v for k, v in names.items()},
              **{f"regen_{k}_csv": v for k, v in fix.items()}}
    sa, sb = _load(inputs["stored_blockA_json"]), _load(inputs["stored_blockB_json"])
    ra, rb = _load(inputs["regen_blockA_json"]), _load(inputs["regen_blockB_json"])

    # (a) cell values side by side
    reg_a = {(r["config_id"], r["model"], r["size"]): r for r in ra["per_subcell"]}
    cells_a = []
    for r in sa["per_subcell"]:
        g = reg_a[(r["config_id"], r["model"], r["size"])]
        cells_a.append({"config_id": r["config_id"], "model": r["model"], "size": r["size"],
                        **{f"{q}_stored": r[q] for q in ("H_up", "M_Phi", "GAP", "gap_ci_lo", "d1d")},
                        **{f"{q}_regenerated": g[q] for q in ("H_up", "M_Phi", "GAP", "gap_ci_lo", "d1d")},
                        "changed": any(r[q] != g[q] for q in ("H_up", "M_Phi", "GAP", "gap_ci_lo", "gap_ci_hi", "d1d"))})
    reg_b = {(r["config_id"], r["size"]): r for r in rb["per_cell"]}
    cells_b = []
    for r in sb["per_cell"]:
        g = reg_b[(r["config_id"], r["size"])]
        pol = [k for k in r if k not in ("config_id", "size")]
        cells_b.append({"config_id": r["config_id"], "size": r["size"],
                        "stored": {k: r[k] for k in pol}, "regenerated": {k: g[k] for k in pol},
                        "changed_policies": [k for k in pol if r[k] != g[k]]})
    win_changes = [{"row": i, "col": j, "stored": sb["win_matrix"][i][j], "regenerated": rb["win_matrix"][i][j]}
                   for i in sb["win_matrix"] for j in sb["win_matrix"][i]
                   if _canon(sb["win_matrix"][i][j]) != _canon(rb["win_matrix"][i][j])]
    summary_b = {k: {"stored": sb.get(k), "regenerated": rb.get(k)}
                 for k in ("P5_vs_P0", "P5_vs_P1", "P5_vs_P6", "P5_vs_P7", "P5_above_P7_frac", "band",
                           "mean_median_makespan")}

    # (b) ablation: reproduction check on the stored CSVs, then the regenerated CSVs
    stored_abl = _load(inputs["stored_ablation_json"])
    before = sha256_file(inputs["stored_ablation_json"])
    repro = _run_ablation({names[k]: RAW_DIR / names[k] for k in names})
    if _canon(repro) != _canon(stored_abl):
        raise SystemExit("S1-9 completion STOP: the unchanged ablation analysis does not reproduce "
                         "the stored v0_5_phase5_ablation.json from the stored CSVs")
    regen_abl = _run_ablation({names["A"]: fix["A"], names["B"]: fix["B"], names["P7"]: fix["P7"],
                               names["S"]: RAW_DIR / names["S"]})
    if sha256_file(inputs["stored_ablation_json"]) != before:
        raise SystemExit("S1-9 completion STOP: the stored ablation JSON changed during the run")
    regen_abl["regenerated_on"] = date.today().isoformat()
    regen_abl["note"] = ("computed by the unchanged analysis_phase5_ablation on the S1-9 regenerated "
                         "Block A, Block B and P7 CSVs; A2 and A4 use the stored scheme CSV, which S1-9 "
                         "does not regenerate; the 'generated' field is hard-coded in that code")
    regen_abl["provenance"] = _meta("S1B", {**{f"regen_{k}_csv": v for k, v in fix.items()},
                                            "stored_scheme_csv": RAW_DIR / names["S"]}, mode)
    abl_path = _write(regen_abl, "v0_5_phase5_ablation_tiebreakfix.json", mode)
    p7_side = {k: {"stored": stored_abl["P7_reference"][k], "regenerated": regen_abl["P7_reference"][k]}
               for k in ("mean_P5_above_P7", "mean_P5_capture", "n_cells")}
    other_side = {abl_key: {"stored": {k: v for k, v in stored_abl[abl_key].items() if not isinstance(v, (list, dict))},
                            "regenerated": {k: v for k, v in regen_abl[abl_key].items() if not isinstance(v, (list, dict))}}
                  for abl_key in ("A1_feature", "A2_T_dimension", "A3_estimator", "A4_granularity")}

    # (c) provenance for the S1-9 files (general rule 4)
    cmp_ = _load(inputs["S1-9_comparison"])
    s19_files = {p.name: p for p in (fix["A"], fix["B"], fix["P7"], inputs["regen_blockA_json"],
                                     inputs["regen_blockB_json"], inputs["S1-9_comparison"])}
    provenance = {"files": {n: sha256_file(p) for n, p in s19_files.items()},
                  "written_by": "src/experiments_S1_tiebreak_regen.py (run of 2026-09-26, EXECUTION-LOG 55)",
                  "code_tree_sha256_at_S1-9_run": cmp_.get("code_tree_sha256"),
                  "code_sha256_of_S1-9_script_at_run": cmp_.get("code_sha256"),
                  "registration_S1B_sha256": sha256_file(REG["S1B"]),
                  "stored_inputs_sha256": {n: sha256_file(inputs[n]) for n in
                                           ("stored_blockA_json", "stored_blockB_json", "stored_ablation_json")},
                  "note": "the *_tiebreakfix.json files are written by the unchanged Phase 5 analysis code, "
                          "which records no hashes; this record supplies them (S1B general rule 4)"}

    out = {"item": "S1-9 completion", **_meta("S1B", inputs, mode),
           "reporting_rule": "verdicts of record from the stored artefacts; regenerated values are a "
                             "robustness column beside them (S1-9 rules 1 to 4)",
           "b14_exposure": cmp_.get("b14_exposure"),
           "gates": {"blockA": {"stored": sa["gates"], "regenerated": ra["gates"],
                                "verdict_stored": sa["verdict"], "verdict_regenerated": ra["verdict"]},
                     "blockB": summary_b},
           "blockA_cells": {"n_changed": int(sum(c["changed"] for c in cells_a)), "cells": cells_a},
           "blockB_cells": {"n_changed": int(sum(bool(c["changed_policies"]) for c in cells_b)), "cells": cells_b,
                            "win_matrix_changes": win_changes},
           "ablation": {"reproduction_check": "the unchanged analysis reproduces the stored "
                                              "v0_5_phase5_ablation.json exactly from the stored CSVs",
                        "P7_reference": p7_side, "other_ablations": other_side,
                        "output": abl_path.name},
           "provenance_of_S1-9_files": provenance}
    return [_write(out, "v0_5_phase5_S1-9_completion.json", mode), abl_path]


# ==========================================================================
# s1-12: supplement
# ==========================================================================

def cmd_s1_12(mode: str) -> list:
    inputs = {"S1-12": RESULTS_DIR / "v0_5_phase5_S1-12_b5_boardfirst.json",
              "stored_B5": TIER2 / "b5_des_crossvalidation.json"}
    s, b5 = _load(inputs["S1-12"]), _load(inputs["stored_B5"])
    rows, all_equal = [], True
    for cid, r in s["per_config"].items():
        st = b5["per_config"][cid]
        eq = {"rho_M1": r["rho_M1_tiebreak_only"] == st["rho_M1"],
              "rho_M2": r["rho_M2_tiebreak_only"] == st["rho_M2"],
              "cf_mean_M2": r["cf_mean_M2"] == st["cf_mean_M2"],
              "des_mean_M2_b5_rule": r["des_mean_M2_b5_rule"] == st["des_mean_M2"]}
        all_equal &= all(eq.values())
        rows.append({"config_id": cid, "tie_break_only_equals_stored_B5": eq,
                     "rho_M2": {"stored_B5": st["rho_M2"], "tie_break_only": r["rho_M2_tiebreak_only"],
                                "board_first": r["rho_M2"]},
                     "des_ordering_rate": {"stored_B5": st["des_dominance"], "board_first": r["des_dominance"]}})
    g = s["gates_for_reference_only"]
    out = {"item": "S1-12 supplement", **_meta("S1B", inputs, mode),
           "code_tree_sha256_of_S1-12_run": s.get("code_tree_sha256"),
           "gates_for_reference_only": g,
           "faithful_ordinal_proxy_supported": bool(g["rho_ge_09_every_config"] and g["des_dominance_ge_090"]),
           "verdict_of_record": "B-5 unchanged: Spearman gate not met; DES ordering 0.98 to 1.00; "
                                "'faithful ordinal proxy' not supported",
           "des_ordering_rate_range": {"stored_B5": [min(b5["per_config"][c]["des_dominance"] for c in b5["per_config"]),
                                                     max(b5["per_config"][c]["des_dominance"] for c in b5["per_config"])],
                                       "board_first": [min(r["des_dominance"] for r in s["per_config"].values()),
                                                       max(r["des_dominance"] for r in s["per_config"].values())]},
           "tie_break_only_column_equals_stored_B5": all_equal,
           "statement_check": ("The registration expected the rerun to change two things at once (tie-break fix "
                               "and boarding rule). The tie-break-only column equals the stored B-5 values"
                               + (" exactly" if all_equal else " only in part")
                               + ", so the stored B-5 closed-form mirror already used the current semantics and "
                                 "the difference between the stored and board-first columns is the boarding rule."),
           "per_config": rows}
    return [_write(out, "v0_5_phase5_S1-12_supplement.json", mode)]


# ==========================================================================
# th-2: complete display
# ==========================================================================

def _stats(b: pd.Series) -> dict:
    return {"n": int(len(b)), "median_B": float(b.median()),
            "iqr_B": [float(b.quantile(0.25)), float(b.quantile(0.75))],
            "reversal_share": float((b < 0).mean())}


def facet(df: pd.DataFrame, by: str, dedup_keys: Optional[list]) -> dict:
    out = {}
    for lvl, g in df.groupby(by):
        entry = {"as_drawn": _stats(g["B"])}
        if dedup_keys:
            entry["deduplicated"] = _stats(g.drop_duplicates(subset=dedup_keys)["B"])
        entry["n_from_block_C"] = int((g["source"] == "Block C").sum()) if "source" in g else None
        entry["n_from_S1-3_NS"] = int((g["source"] == "S1-3 [NS]").sum()) if "source" in g else None
        out[str(lvl)] = entry
    return out


def th2_frames() -> tuple:
    inputs = {"blockC_tiebreakfix": RAW_DIR / "mvs_v0_5_phase5_blockC_tiebreakfix.csv",
              "S1-3": RAW_DIR / "mvs_v0_5_phase5_S1-3_blockC_ext.csv",
              "supp2": RAW_DIR / "mvs_v0_5_supp2_capacity.csv",
              "B-1": TIER2 / "b1_matched_assignment.json",
              "TH-2_run_output": RESULTS_DIR / "v0_5_phase5_TH-2_abstraction_bias.json"}
    c = pd.read_csv(inputs["blockC_tiebreakfix"])
    c["B"] = (c["makespan_M2"] - c["makespan_M1"]) / c["makespan_M1"]
    c["source"] = "Block C"
    x = pd.read_csv(inputs["S1-3"])
    x["B"] = (x["makespan_M2"] - x["makespan_M1"]) / x["makespan_M1"]
    if not np.allclose(x["B"], x["abstraction_bias"], atol=1e-12):
        raise SystemExit("TH-2 completion STOP: recomputed B differs from the S1-3 abstraction_bias column")
    x["source"] = "S1-3 [NS]"
    s2 = pd.read_csv(inputs["supp2"])
    s2["B"] = (s2["makespan_M2"] - s2["makespan_M1"]) / s2["makespan_M1"]
    return inputs, c, x, s2


def th2_result(c: pd.DataFrame, x: pd.DataFrame, s2: pd.DataFrame, b1: Optional[dict]) -> dict:
    cols = ["config_id", "size", "arm", "candidate_id", "n_elevators", "F", "B", "source"]
    merged = pd.concat([c[cols], x[cols]], ignore_index=True)
    key = ["config_id", "size", "arm", "candidate_id"]
    head = c[(c["size"] == 16) & c["config_id"].isin(BLOCK_C_CONFIGS)]
    res = {
        "headline_unchanged": {"median_B": float(head["B"].median()),
                               "iqr_B": [float(head["B"].quantile(0.25)), float(head["B"].quantile(0.75))],
                               "n": int(len(head))},
        "facet_E_merged": facet(merged, "n_elevators", key),
        "facet_F_merged": facet(merged, "F", key),
        "facet_n_merged": facet(merged, "size", key),
        "facet_F_block_C_only": facet(c, "F", key),
        "facet_c_supp2": facet(s2, "capacity", None),
        "labels": {
            "merged_facets": "Block C rows (tie-break-fixed, size 16) plus S1-3 extension rows, marked [NS]",
            "deduplicated": "one row per distinct candidate within (configuration, size, arm)",
            "facet_c_supp2": "Supp-2 rows, generated 2026-05-19 with the simulator before the 2026-09-11 "
                             "tie-break fix; no candidate identifiers, so rows as drawn only",
            "F_confounding": "F is confounded with |A| and demand in the Phase 5 fraction; the F facet is "
                             "not an F main effect"},
    }
    if b1 is not None:
        rev = c[c["B"] < 0][["config_id", "arm", "wave_id"]]
        rev_keys = {(int(r.config_id), str(r.arm), int(r.wave_id)) for r in rev.itertuples()}
        viol = {(int(v["config_id"]), str(v["arm"]), int(v["wave_id"])): v["channel"] for v in b1["violations"]}
        both = rev_keys & set(viol)
        by_channel = {}
        for k in both:
            by_channel[viol[k]] = by_channel.get(viol[k], 0) + 1
        res["B-1_cross_reference"] = {
            "TH-2_reversal_waves_block_C": len(rev_keys),
            "B-1_violations": len(viol),
            "in_both": len(both),
            "in_both_by_B-1_channel": by_channel,
            "B-1_channels_all_violations": b1["violation_channels"],
            "B-1_base_rate_all_waves": b1["base_rate_all_waves"],
            "note": "B-1 (2026-07-08) replays the Block C waves with a fidelity-gated mirror under enforced "
                    "matched assignment; TH-2 reversals are rows with M2 < M1 in the tie-break-fixed Block C "
                    "CSV. The two instruments differ, so the overlap is a cross-reference, not an identity."}
    return res


def th2_figure(res: dict, out_png: Path) -> Path:
    """Four facets at printed width (15 cm), Times New Roman, labels >= 7 pt."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        plt.rcParams.update({"font.family": "Times New Roman", "font.size": 8,
                             "pdf.fonttype": 42, "ps.fonttype": 42})
        panels = [("facet_E_merged", "Number of elevators, E", True),
                  ("facet_F_merged", "Number of floors, F", True),
                  ("facet_n_merged", "Orders per wave, n", True),
                  ("facet_c_supp2", "Elevator capacity, c", False)]
        fig, axes = plt.subplots(1, 4, figsize=(15 / 2.54, 6.2 / 2.54), sharey=False)
        for ax, (k, title, ns) in zip(axes, panels):
            f = res[k]
            lv = sorted(f, key=float)
            xs = np.arange(len(lv))
            for off, kind, color, marker, lab in ((-0.12, "as_drawn", "#1f4e79", "o", "as drawn"),
                                                  (0.12, "deduplicated", "#c55a11", "s", "each distinct wave once")):
                if kind not in f[lv[0]]:
                    continue
                med = np.array([100 * f[l][kind]["median_B"] for l in lv])
                lo = np.array([100 * f[l][kind]["iqr_B"][0] for l in lv])
                hi = np.array([100 * f[l][kind]["iqr_B"][1] for l in lv])
                ax.errorbar(xs + off, med, yerr=[med - lo, hi - med], fmt=marker, ms=3.5,
                            capsize=2.5, lw=0.9, color=color, label=lab)
            ax.axhline(0, color="0.6", lw=0.6, ls="--")
            ax.set_xticks(xs)
            ax.set_xticklabels(lv)
            ax.set_xlabel(title)
            ax.tick_params(labelsize=7.5)
            note = "Block C + S1-3 [NS]\n(current simulator)" if ns else "Supp-2\n(simulator of 19 May 2026)"
            ax.set_title(note, fontsize=7)
        axes[0].set_ylabel("Abstraction bias B (%)\nmedian and interquartile range")
        handles, labels = axes[0].get_legend_handles_labels()
        fig.legend(handles, labels, loc="upper center", ncol=2, fontsize=7, frameon=False)
        fig.tight_layout(w_pad=0.6, rect=(0, 0, 1, 0.9))
        out_png.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_png, dpi=600)
        fig.savefig(out_png.with_suffix(".pdf"))
        plt.close(fig)
    return out_png


def cmd_th2(mode: str) -> list:
    inputs, c, x, s2 = th2_frames()
    res = th2_result(c, x, s2, _load(inputs["B-1"]))
    stored_run = _load(inputs["TH-2_run_output"])
    if abs(stored_run["headline"]["median_B"] - res["headline_unchanged"]["median_B"]) > 1e-12:
        raise SystemExit("TH-2 completion STOP: headline differs from the TH-2 output of the run")
    fig_dir = scratch_dir() if mode != "real" else FIG_DIR
    png = th2_figure(res, fig_dir / "TH-2_abstraction_bias_complete.png")
    out = {"item": "TH-2 complete display", **_meta("S1A", inputs, mode),
           "wording_rule": "the headline x (unchanged) is the median over the primary Block C rows as drawn; "
                           "facet medians are reported in the figure, not merged into x",
           **res, "figure": [png.name, png.with_suffix(".pdf").name]}
    return [_write(out, "v0_5_phase5_TH-2_abstraction_bias_complete.json", mode), png]


# ==========================================================================
# self-test
# ==========================================================================

def selftest() -> list:
    rng = random.Random(9201)            # fixture seed, unrelated to any registered seed
    rows = []
    for cid in (1, 3):
        for arm in ["random"] + CORNERS:
            for w in range(30):
                cand = rng.randrange(8)
                m1 = 100 + cand + rng.uniform(-1, 1)
                rows.append({"config_id": cid, "size": 16, "arm": arm, "wave_id": w, "candidate_id": cand,
                             "n_elevators": 2, "F": 3 if cid == 1 else 5,
                             "makespan_M1": m1, "makespan_M2": m1 * (1 + rng.uniform(-0.05, 0.6))})
    c = pd.DataFrame(rows)
    c["B"] = (c["makespan_M2"] - c["makespan_M1"]) / c["makespan_M1"]
    c["source"] = "Block C"
    x = c.copy()
    x["size"], x["n_elevators"], x["source"] = 8, 1, "S1-3 [NS]"
    s2 = pd.DataFrame([{"capacity": cap, "B": rng.uniform(0, 1.2)} for cap in (2, 3, 4, 5) for _ in range(20)])
    b1 = {"violations": [{"config_id": 1, "arm": "LC_HI", "wave_id": 3, "channel": "batch_overtaking"}],
          "violation_channels": {"batch_overtaking": 1}, "base_rate_all_waves": {}}
    res = th2_result(c, x, s2, b1)
    assert set(res["facet_n_merged"]) == {"8", "16"}
    assert "deduplicated" in res["facet_E_merged"]["1"]
    assert "deduplicated" not in res["facet_c_supp2"]["2"]
    row = s1_6_row({"hedge_corner": "LC_HI", "minimax_regret_corner": "LC_HI", "second_place_margin": 0.02,
                    "hedge_stability": 0.9, "minimax_regret_stability": 0.9},
                   {"hedge_corner": "HC_HI", "minimax_regret_corner": "LC_HI", "second_place_margin": 0.005,
                    "hedge_stability": 0.5, "minimax_regret_stability": 0.7})
    assert row["labels_median_basis"] == {"not_stable_under_resampling": True, "near_tie": True}
    assert row["label_differs_on_mean_basis"] == {"not_stable_under_resampling": True, "near_tie": True}
    assert row["agree_mean_vs_median_hedge"] is False
    png = th2_figure(res, scratch_dir() / "TH-2_abstraction_bias_complete_selftest.png")
    print("  [OK] display helpers (facets, deduplication, B-1 cross-reference, S1-6 labels, figure)")
    return [png]


COMMANDS = {"s1-2": ("S1B", cmd_s1_2), "s1-6": ("S1A", cmd_s1_6), "s1-9": ("S1B", cmd_s1_9),
            "s1-12": ("S1B", cmd_s1_12), "th-2": ("S1A", cmd_th2)}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("cmd", choices=list(COMMANDS) + ["all"])
    g = p.add_mutually_exclusive_group()
    g.add_argument("--selftest", action="store_true")
    g.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    if args.selftest:
        for path in selftest():
            print(f"display completion [selftest] wrote {path}")
        return
    mode = "dry_run" if args.dry_run else "real"
    for name in (list(COMMANDS) if args.cmd == "all" else [args.cmd]):
        reg_key, fn = COMMANDS[name]
        require_signed(reg_key)
        for path in fn(mode):
            print(f"display completion [{name}]{' [dry run]' if args.dry_run else ''} wrote {path}")


if __name__ == "__main__":
    main()
