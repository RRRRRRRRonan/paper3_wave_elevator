"""
MVS v0.2 Phase 4 v2 analysis.

Reads results/raw/mvs_v0_2_phase4_v2_samples.csv and computes:

  Option 1 metric: median(Arm B = favorable corner) vs median(Arm A = random)
                   per (regime, model) cell, averaged over the 3 sizes
  Option 2 metric: max-min spread across the 4 corners per (regime, model, size),
                   relative to median(random)

Decision gates (per intuitions_before_MVS_v0_2.md §4bis):
  Option 1: >= 10% relative reduction in >= 4/6 cells -> strong
            >= 5% in >= 4/6 -> suggestive
            else -> reject
  Option 2: max-min >= 15% of median(random) in >= 4/6 cells -> strong
            >= 7% -> suggestive
            else -> reject

Output: results/v0_2_phase4_v2_wave_design.json + figures/.
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

CSV = RAW_DIR / "mvs_v0_2_phase4_v2_samples.csv"

REGIMES = ["E1_c2", "E2_c2", "E3_c2"]
MODELS = ["abstraction", "batched"]
SIZES = [4, 6, 8]
CORNERS = ["HC_HI", "HC_LI", "LC_HI", "LC_LI"]


def main() -> None:
    df = pd.read_csv(CSV)

    out = {
        "generated": "2026-04-22",
        "description": "Phase 4 v2 wave-design experiment: regime-conditional Arm B + 4-corner spread",
        "per_cell": {},
    }

    cell_summaries = []
    for regime in REGIMES:
        for model in MODELS:
            cell = df[(df["regime"] == regime) & (df["model"] == model)]
            fav_label = cell["favorable_corner"].iloc[0]
            cell_data = {
                "favorable_corner": fav_label,
                "by_size": {},
            }

            opt1_rel_per_size = []
            opt2_rel_per_size = []
            for size in SIZES:
                sub = cell[cell["size"] == size]
                rand_mks = sub[sub["arm"] == "random"]["makespan"].to_numpy()
                rand_med = float(np.median(rand_mks))

                fav_mks = sub[sub["arm"] == fav_label]["makespan"].to_numpy()
                fav_med = float(np.median(fav_mks))

                # Option 1: relative reduction (positive = Arm B faster than random)
                opt1_rel = (rand_med - fav_med) / rand_med if rand_med > 0 else 0.0
                opt1_rel_per_size.append(opt1_rel)

                corner_meds = {
                    c: float(np.median(sub[sub["arm"] == c]["makespan"]))
                    for c in CORNERS
                }
                spread = max(corner_meds.values()) - min(corner_meds.values())
                opt2_rel = spread / rand_med if rand_med > 0 else 0.0
                opt2_rel_per_size.append(opt2_rel)

                cell_data["by_size"][size] = {
                    "random_median": rand_med,
                    "favorable_median": fav_med,
                    "option1_rel_reduction": opt1_rel,
                    "corner_medians": corner_meds,
                    "corner_spread": spread,
                    "option2_rel_spread": opt2_rel,
                }

            cell_data["option1_avg_over_sizes"] = float(np.mean(opt1_rel_per_size))
            cell_data["option2_avg_over_sizes"] = float(np.mean(opt2_rel_per_size))
            out["per_cell"][f"{regime}|{model}"] = cell_data

            cell_summaries.append({
                "regime": regime,
                "model": model,
                "fav": fav_label,
                "opt1_avg": cell_data["option1_avg_over_sizes"],
                "opt2_avg": cell_data["option2_avg_over_sizes"],
            })

    # Decision gates
    opt1_strong = sum(1 for c in cell_summaries if c["opt1_avg"] >= 0.10)
    opt1_sugg = sum(1 for c in cell_summaries if c["opt1_avg"] >= 0.05)
    opt1_neg = sum(1 for c in cell_summaries if c["opt1_avg"] < 0.0)
    if opt1_strong >= 4:
        opt1_verdict = "STRONG"
    elif opt1_sugg >= 4:
        opt1_verdict = "SUGGESTIVE"
    else:
        opt1_verdict = "REJECT"

    opt2_strong = sum(1 for c in cell_summaries if c["opt2_avg"] >= 0.15)
    opt2_sugg = sum(1 for c in cell_summaries if c["opt2_avg"] >= 0.07)
    if opt2_strong >= 4:
        opt2_verdict = "STRONG"
    elif opt2_sugg >= 4:
        opt2_verdict = "SUGGESTIVE"
    else:
        opt2_verdict = "REJECT"

    out["summary"] = {
        "cells": cell_summaries,
        "option1": {
            "n_strong (>=10%)": opt1_strong,
            "n_suggestive (>=5%)": opt1_sugg,
            "n_negative (Arm B slower)": opt1_neg,
            "verdict": opt1_verdict,
        },
        "option2": {
            "n_strong (>=15%)": opt2_strong,
            "n_suggestive (>=7%)": opt2_sugg,
            "verdict": opt2_verdict,
        },
    }

    # Print human-readable summary
    print()
    print("=" * 88)
    print("Phase 4 v2 summary")
    print("=" * 88)
    print(f"{'regime':8s} {'model':12s} {'fav':6s}  "
          f"{'opt1 (Arm B vs rand)':>22s}  {'opt2 (corner spread)':>22s}")
    for c in cell_summaries:
        print(f"{c['regime']:8s} {c['model']:12s} {c['fav']:6s}  "
              f"{c['opt1_avg']*100:>20.1f}%  {c['opt2_avg']*100:>20.1f}%")
    print()
    print(f"  Option 1: {opt1_strong}/6 cells >= 10%, {opt1_sugg}/6 >= 5%, "
          f"{opt1_neg}/6 negative -> {opt1_verdict}")
    print(f"  Option 2: {opt2_strong}/6 cells >= 15%, {opt2_sugg}/6 >= 7% -> {opt2_verdict}")

    # Per-size table
    print()
    print("Per-size detail (Option 1 relative reduction):")
    print(f"{'cell':22s} {'size=4':>10s} {'size=6':>10s} {'size=8':>10s}")
    for c in cell_summaries:
        cell = out["per_cell"][f"{c['regime']}|{c['model']}"]
        s4 = cell["by_size"][4]["option1_rel_reduction"] * 100
        s6 = cell["by_size"][6]["option1_rel_reduction"] * 100
        s8 = cell["by_size"][8]["option1_rel_reduction"] * 100
        print(f"{c['regime']+'|'+c['model']:22s} {s4:>9.1f}% {s6:>9.1f}% {s8:>9.1f}%")

    print()
    print("Per-size detail (Option 2 corner spread):")
    print(f"{'cell':22s} {'size=4':>10s} {'size=6':>10s} {'size=8':>10s}")
    for c in cell_summaries:
        cell = out["per_cell"][f"{c['regime']}|{c['model']}"]
        s4 = cell["by_size"][4]["option2_rel_spread"] * 100
        s6 = cell["by_size"][6]["option2_rel_spread"] * 100
        s8 = cell["by_size"][8]["option2_rel_spread"] * 100
        print(f"{c['regime']+'|'+c['model']:22s} {s4:>9.1f}% {s6:>9.1f}% {s8:>9.1f}%")

    # ----- Figures -----
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    # Fig 1: Option 1 bar chart
    fig, ax = plt.subplots(figsize=(9, 4))
    labels = [f"{c['regime']}|{c['model'][:3]}" for c in cell_summaries]
    vals = [c["opt1_avg"] * 100 for c in cell_summaries]
    colors = ["#3a7" if v >= 10 else "#fa3" if v >= 5 else "#d33" if v >= 0 else "#933"
              for v in vals]
    ax.bar(labels, vals, color=colors)
    ax.axhline(10, color="#3a7", lw=0.8, ls="--", label="strong (>=10%)")
    ax.axhline(5, color="#fa3", lw=0.8, ls="--", label="suggestive (>=5%)")
    ax.axhline(0, color="k", lw=0.5)
    ax.set_ylabel("Arm B vs random — relative makespan reduction (%)")
    ax.set_title(f"Option 1: informed Arm B vs random  ({opt1_verdict})")
    ax.legend(loc="lower right", fontsize=8)
    plt.xticks(rotation=20, ha="right")
    fig.tight_layout()
    f1 = FIG_DIR / "phase4_v2_option1_bar.png"
    fig.savefig(f1, dpi=110)
    plt.close(fig)
    print(f"\nSaved {f1}")

    # Fig 2: Option 2 bar chart
    fig, ax = plt.subplots(figsize=(9, 4))
    vals2 = [c["opt2_avg"] * 100 for c in cell_summaries]
    colors2 = ["#3a7" if v >= 15 else "#fa3" if v >= 7 else "#d33" for v in vals2]
    ax.bar(labels, vals2, color=colors2)
    ax.axhline(15, color="#3a7", lw=0.8, ls="--", label="strong (>=15%)")
    ax.axhline(7, color="#fa3", lw=0.8, ls="--", label="suggestive (>=7%)")
    ax.set_ylabel("4-corner makespan spread (% of random median)")
    ax.set_title(f"Option 2: maximum lever from wave structure  ({opt2_verdict})")
    ax.legend(loc="upper right", fontsize=8)
    plt.xticks(rotation=20, ha="right")
    fig.tight_layout()
    f2 = FIG_DIR / "phase4_v2_option2_bar.png"
    fig.savefig(f2, dpi=110)
    plt.close(fig)
    print(f"Saved {f2}")

    # Fig 3: Corner heatmap per cell
    fig, axes = plt.subplots(2, 3, figsize=(12, 7), sharey=False)
    for idx, c in enumerate(cell_summaries):
        ax = axes[idx // 3, idx % 3]
        cell = out["per_cell"][f"{c['regime']}|{c['model']}"]
        # Build a 4 (corner) x 3 (size) table
        mat = np.array([
            [cell["by_size"][s]["corner_medians"][corner] for s in SIZES]
            for corner in CORNERS
        ])
        rand_meds = np.array([cell["by_size"][s]["random_median"] for s in SIZES])
        # Plot relative deviation from random as percent
        rel = (mat - rand_meds[None, :]) / rand_meds[None, :] * 100
        im = ax.imshow(rel, cmap="RdBu_r", vmin=-30, vmax=30, aspect="auto")
        ax.set_xticks(range(len(SIZES))); ax.set_xticklabels([f"size={s}" for s in SIZES])
        ax.set_yticks(range(len(CORNERS))); ax.set_yticklabels(CORNERS)
        ax.set_title(f"{c['regime']}  {c['model']}\nfav={c['fav']}", fontsize=9)
        for i in range(len(CORNERS)):
            for j in range(len(SIZES)):
                ax.text(j, i, f"{rel[i, j]:+.1f}%", ha="center", va="center", fontsize=7)
        if idx == 0:
            fig.colorbar(im, ax=axes.ravel().tolist(), shrink=0.6,
                         label="median makespan vs random (%)")
    fig.suptitle("Phase 4 v2 — corner makespan vs random, per cell", fontsize=11)
    f3 = FIG_DIR / "phase4_v2_corner_heatmap.png"
    fig.savefig(f3, dpi=110, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {f3}")

    # Save JSON
    out_path = RESULTS_DIR / "v0_2_phase4_v2_wave_design.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"Saved {out_path}")


if __name__ == "__main__":
    main()
