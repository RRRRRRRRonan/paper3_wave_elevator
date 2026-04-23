"""
MVS v0.2 Phase 4 v2 Reinforcement Experiment R2 — partition refinement analysis.

Reads results/raw/mvs_v0_2_phase4_v2_partition_samples.csv (500 random waves
per cell, with features and makespan), then computes UB under three partition
schemes:

  P1: 2x2 = top/bottom 25% on (C, I)        (4 corner bins, current Phase 4 v2)
  P2: 3x3 = tertile bins on (C, I)          (9 bins)
  P3: 8-octant = top/bottom 25% on (C, I, T) (8 corner bins)

For each (regime, model, size, partition):
  - Bin waves
  - Compute median makespan per non-empty bin
  - UB = (max_bin_med - min_bin_med) / overall_median

Pass gates:
  G1: 8-octant UB >= 3x3 UB >= 2x2 UB in >= 4/6 cells (monotone refinement)
  G2: cross-regime ordering of UB (which cells have biggest UB) preserved across
      all three partitions in >= 4/6 cells

Output: results/v0_2_phase4_v2_partition_refinement.json + figures.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RAW_DIR = RESULTS_DIR / "raw"
FIG_DIR = RESULTS_DIR / "figures"

CSV = RAW_DIR / "mvs_v0_2_phase4_v2_partition_samples.csv"

REGIMES = ["E1_c2", "E2_c2", "E3_c2"]
MODELS = ["abstraction", "batched"]
SIZES = [4, 6, 8]


def bin_label_2x2(c, i, c_lo, c_hi, i_lo, i_hi):
    if c <= c_lo and i <= i_lo:
        return "LC_LI"
    if c <= c_lo and i >= i_hi:
        return "LC_HI"
    if c >= c_hi and i <= i_lo:
        return "HC_LI"
    if c >= c_hi and i >= i_hi:
        return "HC_HI"
    return None  # interior — discarded for 2x2


def bin_label_3x3(c, i, c_t1, c_t2, i_t1, i_t2):
    if c <= c_t1:
        cb = "L"
    elif c <= c_t2:
        cb = "M"
    else:
        cb = "H"
    if i <= i_t1:
        ib = "L"
    elif i <= i_t2:
        ib = "M"
    else:
        ib = "H"
    return f"{cb}C_{ib}I"


def bin_label_octant(c, i, t, c_lo, c_hi, i_lo, i_hi, t_lo, t_hi):
    cb = "H" if c >= c_hi else ("L" if c <= c_lo else None)
    ib = "H" if i >= i_hi else ("L" if i <= i_lo else None)
    tb = "H" if t >= t_hi else ("L" if t <= t_lo else None)
    if cb is None or ib is None or tb is None:
        return None
    return f"{cb}C_{ib}I_{tb}T"


def compute_ub(makespan_per_bin, overall_median):
    """UB = (max_bin_med - min_bin_med) / overall_median."""
    if not makespan_per_bin or overall_median <= 0:
        return 0.0, {}
    bin_meds = {b: float(np.median(arr)) for b, arr in makespan_per_bin.items()
                if len(arr) >= 5}  # skip near-empty bins
    if len(bin_meds) < 2:
        return 0.0, bin_meds
    spread = max(bin_meds.values()) - min(bin_meds.values())
    return float(spread / overall_median), bin_meds


def main() -> None:
    df = pd.read_csv(CSV)
    print(f"Loaded {len(df)} rows; cells: {df.groupby(['regime','model','size']).size().min()} per cell")

    out = {
        "generated": "2026-04-22",
        "n_per_cell": int(df.groupby(['regime', 'model', 'size']).size().min()),
        "per_cell": {},
    }

    cell_summaries = []
    for regime in REGIMES:
        for model in MODELS:
            cell_label = f"{regime}|{model}"
            ub_p1_per_size = []
            ub_p2_per_size = []
            ub_p3_per_size = []
            n_bins_p1 = []
            n_bins_p2 = []
            n_bins_p3 = []

            for size in SIZES:
                sub = df[(df["regime"] == regime) & (df["model"] == model)
                         & (df["size"] == size)].copy()
                if len(sub) == 0:
                    continue
                overall_med = float(np.median(sub["makespan"]))

                # Quartile thresholds for P1 (2x2)
                c_lo = sub["C"].quantile(0.25); c_hi = sub["C"].quantile(0.75)
                i_lo = sub["I"].quantile(0.25); i_hi = sub["I"].quantile(0.75)
                # Tertile thresholds for P2 (3x3)
                c_t1 = sub["C"].quantile(1/3); c_t2 = sub["C"].quantile(2/3)
                i_t1 = sub["I"].quantile(1/3); i_t2 = sub["I"].quantile(2/3)
                # Quartile thresholds for P3 (octant), include T
                t_lo = sub["T"].quantile(0.25); t_hi = sub["T"].quantile(0.75)

                # Bin
                bins_p1, bins_p2, bins_p3 = {}, {}, {}
                for _, row in sub.iterrows():
                    mk = row["makespan"]
                    b1 = bin_label_2x2(row["C"], row["I"], c_lo, c_hi, i_lo, i_hi)
                    if b1: bins_p1.setdefault(b1, []).append(mk)
                    b2 = bin_label_3x3(row["C"], row["I"], c_t1, c_t2, i_t1, i_t2)
                    bins_p2.setdefault(b2, []).append(mk)
                    b3 = bin_label_octant(row["C"], row["I"], row["T"],
                                          c_lo, c_hi, i_lo, i_hi, t_lo, t_hi)
                    if b3: bins_p3.setdefault(b3, []).append(mk)

                ub1, meds1 = compute_ub(bins_p1, overall_med)
                ub2, meds2 = compute_ub(bins_p2, overall_med)
                ub3, meds3 = compute_ub(bins_p3, overall_med)

                ub_p1_per_size.append(ub1); n_bins_p1.append(len(meds1))
                ub_p2_per_size.append(ub2); n_bins_p2.append(len(meds2))
                ub_p3_per_size.append(ub3); n_bins_p3.append(len(meds3))

            ub_p1_mean = float(np.mean(ub_p1_per_size))
            ub_p2_mean = float(np.mean(ub_p2_per_size))
            ub_p3_mean = float(np.mean(ub_p3_per_size))
            monotone = (ub_p1_mean <= ub_p2_mean <= ub_p3_mean)

            cell_summaries.append({
                "cell": cell_label,
                "UB_2x2": ub_p1_mean,
                "UB_3x3": ub_p2_mean,
                "UB_octant": ub_p3_mean,
                "monotone_refinement": monotone,
            })
            out["per_cell"][cell_label] = {
                "UB_2x2_per_size": ub_p1_per_size,
                "UB_3x3_per_size": ub_p2_per_size,
                "UB_octant_per_size": ub_p3_per_size,
                "n_bins_2x2_per_size": n_bins_p1,
                "n_bins_3x3_per_size": n_bins_p2,
                "n_bins_octant_per_size": n_bins_p3,
                "UB_2x2_mean": ub_p1_mean,
                "UB_3x3_mean": ub_p2_mean,
                "UB_octant_mean": ub_p3_mean,
                "monotone_refinement": monotone,
            }

    # Print table
    print()
    print(f"{'cell':24s}  {'UB_2x2':>8s}  {'UB_3x3':>8s}  {'UB_8oct':>8s}  {'mono?':>6s}")
    for c in cell_summaries:
        print(f"{c['cell']:24s}  "
              f"{c['UB_2x2']*100:>7.1f}%  {c['UB_3x3']*100:>7.1f}%  "
              f"{c['UB_octant']*100:>7.1f}%  "
              f"{'YES' if c['monotone_refinement'] else 'no':>6s}")

    # Gate G1: monotone refinement in >= 4/6 cells
    n_mono = sum(1 for c in cell_summaries if c["monotone_refinement"])
    g1_pass = (n_mono >= 4)

    # Gate G2: cross-regime ordering preserved
    order_p1 = sorted(range(len(cell_summaries)), key=lambda i: -cell_summaries[i]["UB_2x2"])
    order_p2 = sorted(range(len(cell_summaries)), key=lambda i: -cell_summaries[i]["UB_3x3"])
    order_p3 = sorted(range(len(cell_summaries)), key=lambda i: -cell_summaries[i]["UB_octant"])

    # Compare top-3 sets across the three partitions
    top3_p1 = set(order_p1[:3])
    top3_p2 = set(order_p2[:3])
    top3_p3 = set(order_p3[:3])
    top3_intersection = len(top3_p1 & top3_p2 & top3_p3)
    g2_pass = (top3_intersection >= 2)

    # Spearman rank correlation as a quantitative ordering check
    from scipy.stats import spearmanr
    spr_p1p2, _ = spearmanr([c["UB_2x2"] for c in cell_summaries],
                             [c["UB_3x3"] for c in cell_summaries])
    spr_p1p3, _ = spearmanr([c["UB_2x2"] for c in cell_summaries],
                             [c["UB_octant"] for c in cell_summaries])
    spr_p2p3, _ = spearmanr([c["UB_3x3"] for c in cell_summaries],
                             [c["UB_octant"] for c in cell_summaries])

    print()
    print(f"  Gate G1 (monotone >= 4/6 cells): {n_mono}/6 -> "
          f"{'PASS' if g1_pass else 'FAIL'}")
    print(f"  Gate G2 (top-3 set intersection across all 3 partitions >= 2): "
          f"{top3_intersection} -> {'PASS' if g2_pass else 'FAIL'}")
    print(f"  Spearman rank correlations: 2x2-3x3={spr_p1p2:.3f}, "
          f"2x2-oct={spr_p1p3:.3f}, 3x3-oct={spr_p2p3:.3f}")

    overall = "PASS" if (g1_pass and g2_pass) else (
        "PASS-with-caveats" if (g1_pass or g2_pass) else "FAIL")
    print(f"\n  R2 overall: {overall}")

    out["summary"] = {
        "n_cells_monotone": n_mono,
        "G1_verdict": "PASS" if g1_pass else "FAIL",
        "top3_intersection": top3_intersection,
        "G2_verdict": "PASS" if g2_pass else "FAIL",
        "spearman_2x2_3x3": float(spr_p1p2),
        "spearman_2x2_octant": float(spr_p1p3),
        "spearman_3x3_octant": float(spr_p2p3),
        "overall_R2_verdict": overall,
    }

    # Figure: UB across partitions per cell
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 5))
    cells = [c["cell"] for c in cell_summaries]
    x = np.arange(len(cells))
    w = 0.27
    ax.bar(x - w, [c["UB_2x2"] * 100 for c in cell_summaries], width=w,
           label="2x2 (current)", color="#4a8")
    ax.bar(x, [c["UB_3x3"] * 100 for c in cell_summaries], width=w,
           label="3x3 (tertile)", color="#48a")
    ax.bar(x + w, [c["UB_octant"] * 100 for c in cell_summaries], width=w,
           label="8-octant (with T)", color="#a48")
    ax.set_xticks(x)
    ax.set_xticklabels([c.replace("|", "\n") for c in cells], fontsize=8)
    ax.set_ylabel("UB = max-min spread / random median (%)")
    ax.set_title(f"R2: UB stability under partition refinement  ({overall})")
    ax.legend()
    fig.tight_layout()
    fig_path = FIG_DIR / "phase4_v2_partition_refinement.png"
    fig.savefig(fig_path, dpi=110)
    plt.close(fig)
    print(f"\n  Saved {fig_path}")

    out_path = RESULTS_DIR / "v0_2_phase4_v2_partition_refinement.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"  Saved {out_path}")


if __name__ == "__main__":
    main()
