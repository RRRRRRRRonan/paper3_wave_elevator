"""B-14 production regeneration (2026-09-11) [QA].

Re-runs Block C (matched-wave M1/M2/M3, 6 E=2 configs, size 16) and the
pre-registration §7 smoke slice on the production simulator AFTER the
index-stable tie-break fix (BUGREPORT-2026-07-08_tiebreak_nondeterminism),
using the registered seed streams. Nothing stored on 2026-05-19 is
overwritten: the regenerated artefacts get a `_tiebreakfix` suffix (Block C)
or live under this folder (smoke), and every pre-registered gate verdict is
reported side by side with the stored one, per the B-14 locked reporting rule.

Run:  python revision_2026-09-02/qa_2026-09-11/regen_blockC_smoke_tiebreakfix.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PROTO = ROOT / "prototype"
sys.path.insert(0, str(PROTO))

from src import analysis_phase5_blockC as anC   # noqa: E402
from src import analysis_phase5_smoke as anS    # noqa: E402
from src import experiments_phase5 as xp        # noqa: E402
from src import phase5_config as cfg            # noqa: E402

QA = Path(__file__).resolve().parent
RAW = PROTO / "results" / "raw"
RES = PROTO / "results"


def _flatten(obj, prefix=""):
    out = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.update(_flatten(v, f"{prefix}{k}."))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out.update(_flatten(v, f"{prefix}{i}."))
    else:
        out[prefix[:-1]] = obj
    return out


def _diff_leaves(a, b, skip=("generated", "source_csv", "analysis_note")):
    fa, fb = _flatten(a), _flatten(b)
    keys = sorted(set(fa) | set(fb))
    diffs = []
    for k in keys:
        if k.split(".")[0] in skip:
            continue
        va, vb = fa.get(k, "<missing>"), fb.get(k, "<missing>")
        same = (isinstance(va, float) and isinstance(vb, float)
                and abs(va - vb) <= 1e-9) or va == vb
        if not same:
            diffs.append((k, va, vb))
    return diffs


def main() -> None:
    report = {"date": "2026-09-11", "label": "[QA] B-14 production regeneration"}
    configs = cfg.make_config_array()
    e2 = cfg.e2_subset(configs)

    # ------------------------------------------------------------------ Block C
    t0 = time.time()
    dfC = xp.run_chain_block(e2[:cfg.BLOCK_C["n_configs"]], cfg.BLOCK_C["models"],
                             cfg.BLOCK_C["sizes"], cfg.BLOCK_C["arms"],
                             cfg.N_PER_ARM, cfg.CANDIDATE_POOL)
    report["blockC_seconds"] = round(time.time() - t0, 1)
    newC = RAW / "mvs_v0_5_phase5_blockC_tiebreakfix.csv"
    dfC.to_csv(newC, index=False)

    old = pd.read_csv(RAW / "mvs_v0_5_phase5_blockC.csv")
    key = ["config_id", "arm", "wave_id"]
    m = old.merge(dfC, on=key, suffixes=("_old", "_new"))
    assert len(m) == len(old) == len(dfC), (len(m), len(old), len(dfC))
    rowcmp = {}
    for col in ("makespan_M1", "makespan_M2", "makespan_M3_s20"):
        d = (m[f"{col}_new"] - m[f"{col}_old"]).to_numpy(float)
        ch = np.abs(d) > 1e-9
        rowcmp[col] = {
            "rows": int(len(m)), "changed": int(ch.sum()),
            "changed_pct": round(float(100 * ch.mean()), 3),
            "min_diff": float(d[ch].min()) if ch.any() else 0.0,
            "max_diff": float(d[ch].max()) if ch.any() else 0.0,
            "changed_by_config": {int(c): int(n) for c, n in
                                  m.loc[ch].groupby("config_id").size().items()},
        }
    report["blockC_rowlevel"] = rowcmp

    newJ = RES / "v0_5_phase5_blockC_tiebreakfix.json"
    anC.main([str(newC), str(newJ)])
    J_old = json.load(open(RES / "v0_5_phase5_blockC.json", encoding="utf-8"))
    J_new = json.load(open(newJ, encoding="utf-8"))

    def gates(J):
        h, d3, ra = J["H_D2"], J["H_D3_exploratory"], J["RA_median_hedge_sensitivity"]
        return {
            "D2a_perwave_avg": round(h["perwave_avg"], 4),
            "D2a_perwave_worst": round(h["perwave_worst"], 4),
            "D2b_n_fosd": h["n_fosd"], "D2c_n_U_c_ok": h["n_U_c_ok"],
            "D2d_n_collapse": h["n_collapse"],
            "D2a": h["D2a"], "D2b": h["D2b"], "D2c": h["D2c"], "D2d": h["D2d"],
            "H_D2_verdict": h["verdict"],
            "hedge_corner_mean": {str(r["config_id"]): r["c_star_Hedge"]
                                  for r in h["per_config_collapse"]},
            "H_D3_branch": d3["branch"], "H_D3_qmax_inv": d3["n_qmax_invariant"],
            "H_D3_qmin_inv": d3["n_qmin_invariant"],
            "H_D3_mean_rho": round(d3["mean_spearman_rho"], 4),
            "RA_median_agree": ra["n_agree_with_mean_Hedge"],
            "hedge_corner_median": {str(r["config_id"]): r["c_star_Hedge_median"]
                                    for r in ra["per_config"]},
        }
    report["blockC_gates_stored_2026-05-19"] = gates(J_old)
    report["blockC_gates_tiebreakfix"] = gates(J_new)
    report["blockC_verdicts_identical"] = all(
        report["blockC_gates_stored_2026-05-19"][k] == report["blockC_gates_tiebreakfix"][k]
        for k in ("D2a", "D2b", "D2c", "D2d", "H_D2_verdict", "hedge_corner_mean",
                  "H_D3_branch", "hedge_corner_median"))

    # ------------------------------------------------------------------ smoke
    s = cfg.SMOKE
    slice_a = xp._span_demand(configs, s["n_configs"])
    slice_b = xp._span_demand(cfg.e2_subset(configs), s["n_configs"])
    t0 = time.time()
    dfA = xp.run_corner_block(slice_a, s["models"], [s["size"]], cfg.BLOCK_A["arms"],
                              s["n_per_arm"], s["candidate_pool"], s["train_sample"])
    dfB = xp.run_policy_block(slice_b, cfg.BLOCK_B["model"], [s["size"]],
                              s["n_per_arm"], s["candidate_pool"], s["train_sample"])
    report["smoke_seconds"] = round(time.time() - t0, 1)
    SMK = QA / "smoke_tiebreakfix"
    (SMK / "raw").mkdir(parents=True, exist_ok=True)
    dfA.to_csv(SMK / "raw" / "mvs_v0_5_phase5_smoke_blockA.csv", index=False)
    dfB.to_csv(SMK / "raw" / "mvs_v0_5_phase5_smoke_blockB.csv", index=False)

    def rowcmp_smoke(o, n, keycols, label_col=None):
        assert len(o) == len(n), (len(o), len(n))
        o, n = o.reset_index(drop=True), n.reset_index(drop=True)
        aligned = bool((o[keycols] == n[keycols]).all().all())
        d = n["makespan"].to_numpy(float) - o["makespan"].to_numpy(float)
        ch = np.abs(d) > 1e-9
        out = {"rows": int(len(o)), "keys_aligned": aligned,
               "changed": int(ch.sum()), "changed_pct": round(float(100 * ch.mean()), 3),
               "min_diff": float(d[ch].min()) if ch.any() else 0.0,
               "max_diff": float(d[ch].max()) if ch.any() else 0.0}
        if label_col:
            out[f"{label_col}_identical"] = bool((o[label_col] == n[label_col]).all())
        return out
    oldA = pd.read_csv(RAW / "mvs_v0_5_phase5_smoke_blockA.csv")
    oldB = pd.read_csv(RAW / "mvs_v0_5_phase5_smoke_blockB.csv")
    report["smoke_rowlevel_blockA"] = rowcmp_smoke(
        oldA, dfA, ["config_id", "model", "size", "arm"], "favorable_corner")
    report["smoke_rowlevel_blockB"] = rowcmp_smoke(
        oldB, dfB, ["config_id", "model", "size", "policy"])

    anS.RAW_DIR = SMK / "raw"
    anS.RESULTS_DIR = SMK
    anS.main()
    S_old = json.load(open(RES / "v0_5_phase5_smoke_verdict.json", encoding="utf-8"))
    S_new = json.load(open(SMK / "v0_5_phase5_smoke_verdict.json", encoding="utf-8"))
    diffs = _diff_leaves(S_old, S_new)
    report["smoke_verdict_leaf_diffs"] = [{"key": k, "stored": a, "tiebreakfix": b}
                                         for k, a, b in diffs]
    verdict_keys = [k for k in _flatten(S_old) if "verdict" in k.lower()
                    or k.lower().endswith(".pass") or k.lower().startswith("s")]
    report["smoke_verdict_stored"] = {k: _flatten(S_old)[k] for k in verdict_keys
                                      if not isinstance(_flatten(S_old)[k], (list, dict))}
    report["smoke_verdict_tiebreakfix"] = {k: _flatten(S_new).get(k) for k in verdict_keys}

    out = QA / "b14_production_equivalence.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 78)
    print("B-14 production regeneration summary")
    print("=" * 78)
    for col, r in rowcmp.items():
        print(f"  Block C {col:16} changed {r['changed']:5d}/{r['rows']} rows "
              f"({r['changed_pct']:.3f}%)  diff range [{r['min_diff']:+.1f}, {r['max_diff']:+.1f}]"
              f"  by config {r['changed_by_config']}")
    go, gn = report["blockC_gates_stored_2026-05-19"], report["blockC_gates_tiebreakfix"]
    for k in ("D2a_perwave_avg", "D2a_perwave_worst", "D2b_n_fosd", "D2c_n_U_c_ok",
              "D2d_n_collapse", "H_D2_verdict", "hedge_corner_mean", "H_D3_branch",
              "H_D3_qmax_inv", "H_D3_qmin_inv", "H_D3_mean_rho", "RA_median_agree",
              "hedge_corner_median"):
        flag = "" if go[k] == gn[k] else "   <-- differs"
        print(f"  {k:22} stored={go[k]}  fixed={gn[k]}{flag}")
    print(f"  Block C verdict set identical: {report['blockC_verdicts_identical']}")
    print(f"  smoke Block A rows changed: {report['smoke_rowlevel_blockA']}")
    print(f"  smoke Block B rows changed: {report['smoke_rowlevel_blockB']}")
    print(f"  smoke verdict leaf diffs (excluding dates): {len(diffs)}")
    for k, a, b in diffs[:40]:
        print(f"     {k}: {a} -> {b}")
    print(f"  wrote {out}")


if __name__ == "__main__":
    main()
