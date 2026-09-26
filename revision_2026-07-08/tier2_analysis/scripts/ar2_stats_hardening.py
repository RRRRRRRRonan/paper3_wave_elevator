"""
Amendment A-R2 (2026-07-08): statistical hardening. Reanalysis ONLY.

Inputs:
  raw/mvs_v0_5_phase5_blockB.csv + raw/mvs_v0_5_phase5_ablation_P7.csv
  raw/mvs_v0_5_phase5_blockC.csv
  raw/mvs_v0_5_phase5_blockA.csv

Outputs (ar2_stats_hardening.json):
  1. Wilson 95% CIs on all pairwise Block B win fractions (n = 12 cells).
  2. Per-cell Mann-Whitney U (two-sided) for all policy pairs, BH-FDR q=0.05
     across the whole family; plus across-cell Wilcoxon signed-rank on the 12
     paired cell medians per pair, BH across the 28 pairs.
  3. Wilson 95% CIs on Block C per-wave M2>=M1 dominance per (config, corner)
     and pooled.
  4. D1-d multiplicity sensitivity: one-sided bootstrap p per sub-cell
     (same estimator as analysis_phase5_blockA.py), BH-FDR q=0.05 across 72.
     PRE-REGISTERED VERDICT (57/72 PARTIAL) IS NOT RE-JUDGED.
  5. H-D3 bootstrap CI on mean corner-ranking Spearman rho.

Locked: seed 20260708, 1000 bootstrap reps, no verdict changes.
"""
from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu, spearmanr, wilcoxon

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "prototype" / "results" / "raw"
OUT = Path(__file__).resolve().parents[1] / "outputs"
SEED = 20260708
N_BOOT = 1000
CORNERS = ["HC_HI", "HC_LI", "LC_HI", "LC_LI"]
POLICIES = ["P0_random", "P1_dest_cluster", "P2_cardinality", "P3_dir_balanced",
            "P4_temporal", "P5_phi", "P6_spo_tree", "P7_localsearch"]


def wilson(k: int, n: int, z: float = 1.959964):
    if n == 0:
        return float("nan"), float("nan")
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return float(c - h), float(c + h)


def bh_fdr(pvals: list, q: float = 0.05):
    """Return boolean list: rejected under Benjamini-Hochberg at level q."""
    m = len(pvals)
    order = np.argsort(pvals)
    rejected = [False] * m
    k_star = 0
    for rank, idx in enumerate(order, start=1):
        if pvals[idx] <= q * rank / m:
            k_star = rank
    for rank, idx in enumerate(order, start=1):
        if rank <= k_star:
            rejected[idx] = True
    return rejected


def main() -> None:
    rng = np.random.default_rng(SEED)
    OUT.mkdir(parents=True, exist_ok=True)

    # ---- Block B: samples per (config, size, policy) -----------------------
    dfB = pd.read_csv(RAW / "mvs_v0_5_phase5_blockB.csv")
    dfP7 = pd.read_csv(RAW / "mvs_v0_5_phase5_ablation_P7.csv")
    cells = sorted({(int(c), int(s))
                    for c, s in dfB[["config_id", "size"]].drop_duplicates()
                    .itertuples(index=False)})
    samp = {}
    for (cid, size) in cells:
        gB = dfB[(dfB["config_id"] == cid) & (dfB["size"] == size)]
        for p in POLICIES[:-1]:
            samp[(cid, size, p)] = gB[gB["policy"] == p]["makespan"].to_numpy(float)
        g7 = dfP7[(dfP7["config_id"] == cid) & (dfP7["size"] == size)]
        samp[(cid, size, "P7_localsearch")] = g7["makespan"].to_numpy(float)

    pairs = list(combinations(POLICIES, 2))

    # 1. win fractions + Wilson CIs (n = 12 cells)
    win_ci = []
    for i, j in pairs:
        k = sum(float(np.median(samp[(c, s, i)]))
                < float(np.median(samp[(c, s, j)])) for c, s in cells)
        lo, hi = wilson(k, len(cells))
        win_ci.append({"i": i, "j": j, "wins_i": int(k), "n": len(cells),
                       "win_frac": k / len(cells),
                       "wilson_lo": lo, "wilson_hi": hi})

    # 2a. per-cell Mann-Whitney, BH across the whole family
    mw = []
    for (cid, size) in cells:
        for i, j in pairs:
            x, y = samp[(cid, size, i)], samp[(cid, size, j)]
            stat, p = mannwhitneyu(x, y, alternative="two-sided")
            mw.append({"config_id": cid, "size": size, "i": i, "j": j,
                       "U": float(stat), "p": float(p),
                       "median_i": float(np.median(x)),
                       "median_j": float(np.median(y))})
    rej = bh_fdr([r["p"] for r in mw])
    for r, rj in zip(mw, rej):
        r["significant_BH05"] = bool(rj)
    n_sig = sum(rej)

    # 2b. across-cell Wilcoxon signed-rank on 12 paired cell medians per pair
    wsr = []
    for i, j in pairs:
        di = [float(np.median(samp[(c, s, i)])) for c, s in cells]
        dj = [float(np.median(samp[(c, s, j)])) for c, s in cells]
        diff = np.array(di) - np.array(dj)
        if np.allclose(diff, 0):
            stat, p = float("nan"), 1.0
        else:
            stat, p = wilcoxon(diff)
        wsr.append({"i": i, "j": j, "W": float(stat), "p": float(p),
                    "mean_diff": float(np.mean(diff))})
    rej_w = bh_fdr([r["p"] for r in wsr])
    for r, rj in zip(wsr, rej_w):
        r["significant_BH05"] = bool(rj)

    # ---- Block C: dominance Wilson CIs -------------------------------------
    dfC = pd.read_csv(RAW / "mvs_v0_5_phase5_blockC.csv")
    dom_ci = []
    k_all = n_all = 0
    worst = None
    for (cid, arm), g in dfC.groupby(["config_id", "arm"]):
        if arm == "random":
            continue
        T1 = g["makespan_M1"].to_numpy(float)
        T2 = g["makespan_M2"].to_numpy(float)
        k = int(np.sum(T2 >= T1)); n = len(g)
        lo, hi = wilson(k, n)
        dom_ci.append({"config_id": int(cid), "corner": arm, "k": k, "n": n,
                       "dom_frac": k / n, "wilson_lo": lo, "wilson_hi": hi})
        k_all += k; n_all += n
        if worst is None or k / n < worst["dom_frac"]:
            worst = dom_ci[-1]
    lo_all, hi_all = wilson(k_all, n_all)

    # ---- D1-d multiplicity sensitivity --------------------------------------
    dfA = pd.read_csv(RAW / "mvs_v0_5_phase5_blockA.csv")
    d1d = []
    for (cid, model, size), g in dfA.groupby(["config_id", "model", "size"]):
        fav = g["favorable_corner"].iloc[0]
        arms = {c: g[g["arm"] == c]["makespan"].to_numpy(float) for c in CORNERS}
        rnd = g[g["arm"] == "random"]["makespan"].to_numpy(float)
        boot = np.empty(N_BOOT)
        for b in range(N_BOOT):
            mb = {c: float(np.median(rng.choice(arms[c], len(arms[c]))))
                  for c in CORNERS}
            m0b = float(np.median(rng.choice(rnd, len(rnd))))
            qmax = max(mb, key=mb.get); qmin = min(mb, key=mb.get)
            boot[b] = (mb[qmax] - m0b) / m0b + (mb[fav] - mb[qmin]) / m0b
        p_one = float((1 + np.sum(boot <= 0.0)) / (N_BOOT + 1))
        d1d.append({"config_id": int(cid), "model": model, "size": int(size),
                    "p_boot_onesided": p_one})
    rej_d = bh_fdr([r["p_boot_onesided"] for r in d1d])
    for r, rj in zip(d1d, rej_d):
        r["resolved_BH05"] = bool(rj)
    n_resolved_bh = sum(rej_d)

    # ---- H-D3 rho bootstrap CI ----------------------------------------------
    model_cols = [("makespan_M1", "M1"), ("makespan_M2", "M2"),
                  ("makespan_M3_s20", "M3")]
    cfgs = sorted(dfC["config_id"].unique())
    arm_data = {(int(c), a): dfC[(dfC["config_id"] == c) & (dfC["arm"] == a)]
                [[m for m, _ in model_cols]].to_numpy(float)
                for c in cfgs for a in CORNERS}
    rho_boot = np.empty(N_BOOT)
    for b in range(N_BOOT):
        rhos = []
        for c in cfgs:
            med = {}
            for ai, a in enumerate(CORNERS):
                d = arm_data[(c, a)]
                idx = rng.integers(0, len(d), len(d))
                med[a] = np.median(d[idx], axis=0)   # per model column
            base = [med[a][0] for a in CORNERS]
            for m_i in (1, 2):
                rhos.append(spearmanr(base, [med[a][m_i] for a in CORNERS])
                            .statistic)
        rho_boot[b] = float(np.mean(rhos))
    rho_lo, rho_hi = (float(x) for x in np.percentile(rho_boot, [2.5, 97.5]))
    # point estimate (no resampling)
    rhos_pt = []
    for c in cfgs:
        med = {a: np.median(arm_data[(c, a)], axis=0) for a in CORNERS}
        base = [med[a][0] for a in CORNERS]
        for m_i in (1, 2):
            rhos_pt.append(spearmanr(base, [med[a][m_i] for a in CORNERS])
                           .statistic)
    rho_point = float(np.mean(rhos_pt))

    out = {
        "amendment": "A-R2", "date_executed": "2026-07-08",
        "seed": SEED, "n_boot": N_BOOT,
        "note": ("Sensitivity/uncertainty reporting only. Pre-registered "
                 "verdicts unchanged: H-D1 PARTIAL (57/72), H-D2 PASS, "
                 "H-Policy Partial."),
        "blockB_win_wilson": win_ci,
        "blockB_mannwhitney_BH": {"n_tests": len(mw), "n_significant": n_sig,
                                  "tests": mw},
        "blockB_wilcoxon_cellmedians_BH": wsr,
        "blockC_dominance_wilson": {
            "per_cell": dom_ci,
            "pooled": {"k": k_all, "n": n_all, "dom_frac": k_all / n_all,
                       "wilson_lo": lo_all, "wilson_hi": hi_all},
            "worst_cell": worst},
        "d1d_multiplicity": {"n_resolved_prereg": 57,
                             "n_resolved_BH05": n_resolved_bh,
                             "per_subcell": d1d},
        "hd3_rho": {"point": rho_point, "ci_lo": rho_lo, "ci_hi": rho_hi},
    }
    path = OUT / "ar2_stats_hardening.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)

    print("A-R2 statistical hardening")
    print(f"  Block B: {len(mw)} Mann-Whitney tests, significant after "
          f"BH(0.05): {n_sig}")
    key_pairs = [("P5_phi", "P0_random"), ("P5_phi", "P1_dest_cluster"),
                 ("P5_phi", "P6_spo_tree"), ("P5_phi", "P7_localsearch"),
                 ("P2_cardinality", "P5_phi")]
    for i, j in key_pairs:
        r = next(r for r in win_ci
                 if (r["i"], r["j"]) in ((i, j), (j, i)))
        f_ij = r["win_frac"] if r["i"] == i else 1 - r["win_frac"] \
            if not np.isnan(r["win_frac"]) else float("nan")
        print(f"  win {i} vs {j}: {f_ij:.2f}  "
              f"(Wilson CI of stored orientation [{r['wilson_lo']:.2f}, "
              f"{r['wilson_hi']:.2f}], i={r['i']})")
    print(f"  Block C pooled dominance: {k_all}/{n_all} = {k_all/n_all:.4f} "
          f"Wilson [{lo_all:.4f}, {hi_all:.4f}]")
    print(f"  worst cell: config {worst['config_id']} {worst['corner']} "
          f"{worst['dom_frac']:.3f} [{worst['wilson_lo']:.3f}, "
          f"{worst['wilson_hi']:.3f}]")
    print(f"  D1-d resolved: pre-reg 57/72; BH-FDR(0.05) sensitivity: "
          f"{n_resolved_bh}/72 (verdict NOT re-judged)")
    print(f"  H-D3 mean Spearman rho = {rho_point:.3f} "
          f"95% CI [{rho_lo:.3f}, {rho_hi:.3f}]")
    print(f"\nSaved {path}")


if __name__ == "__main__":
    main()
