"""
MVS v0.2 Phase 4 H1 — Figure: P1 (cluster) vs P0 (fifo) delta with 95% CIs.

Renders two panels (random arm, favorable arm) of caterpillar plots showing
mean(P1) - mean(P0) with paired-bootstrap 95% CIs per (cell, size).

Output: results/figures/phase4_H1_delta.png
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
SUMMARY_JSON = RESULTS_DIR / "v0_2_phase4_H1_summary.json"
FIG_DIR = RESULTS_DIR / "figures"
FIG_PATH = FIG_DIR / "phase4_H1_delta.png"


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    data = json.loads(SUMMARY_JSON.read_text(encoding="utf-8"))
    rows = data["per_arm_size"]

    fig, axes = plt.subplots(1, 2, figsize=(12, 6), sharey=True)

    for ax, arm in zip(axes, ["random", "favorable"]):
        sub = [r for r in rows if r["arm"] == arm]
        labels = []
        deltas = []
        los = []
        his = []
        colors = []
        for r in sub:
            label = f"{r['regime']}|{r['model'][:4]} s{r['size']}"
            labels.append(label)
            deltas.append(r["delta"])
            los.append(r["ci_lo"])
            his.append(r["ci_hi"])
            if r["sig_P1_better"]:
                colors.append("#1b7837")  # green
            elif r["sig_P1_worse"]:
                colors.append("#b2182b")  # red
            else:
                colors.append("#888888")  # gray

        y = np.arange(len(labels))
        ax.axvline(0, color="black", linewidth=0.8, linestyle="--")
        for i in range(len(labels)):
            ax.plot([los[i], his[i]], [y[i], y[i]],
                    color=colors[i], linewidth=2)
            ax.scatter(deltas[i], y[i], color=colors[i], s=30, zorder=3)
        ax.set_yticks(y)
        ax.set_yticklabels(labels, fontsize=8)
        ax.set_xlabel("mean(P1) - mean(P0)  [time units]")
        ax.set_title(f"arm = {arm}")
        ax.grid(True, axis="x", alpha=0.3)

    fig.suptitle(
        "Phase 4 H1: destination-clustered batching (P1) vs FIFO (P0)\n"
        "green = P1 significantly better, red = P1 significantly worse, gray = n.s. (95% paired bootstrap)",
        fontsize=11,
    )
    fig.tight_layout()
    fig.savefig(FIG_PATH, dpi=150, bbox_inches="tight")
    print(f"Saved {FIG_PATH}")


if __name__ == "__main__":
    main()
