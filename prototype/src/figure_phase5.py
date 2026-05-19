"""
MVS v0.5 Phase 5 W6 — figures.

Figure 1 — GAP across the configuration space (vs F and vs |A|, by demand).
           Pre-reg §6 listed a (F,|A|) heatmap; the L18 fractional design ties
           demand to (F,|A|) so a heatmap is mostly empty — a scatter vs each
           factor, coloured by demand, conveys the same landscape honestly.
Figure 2 — P5-vs-P6 paired median makespan (the D1 cell-median differentiator).

Output: results/figures/phase5_fig1_gap_landscape.png
        results/figures/phase5_fig2_p5_vs_p6.png
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
FIG_DIR = RESULTS_DIR / "figures"

DEMAND_COLOR = {"uniform": "#1f77b4", "clustered": "#ff7f0e",
                "diurnal": "#2ca02c"}


def fig1_gap_landscape() -> None:
    rows = json.loads((RESULTS_DIR / "v0_5_phase5_blockA.json")
                      .read_text(encoding="utf-8"))["per_subcell"]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    for ax, factor, label in [(axes[0], "F", "floors  F"),
                              (axes[1], "n_amrs", "AMRs  |A|")]:
        for dem, col in DEMAND_COLOR.items():
            xs = [r[factor] + (hash(dem) % 5 - 2) * 0.06
                  for r in rows if r["demand"] == dem]
            ys = [r["GAP"] for r in rows if r["demand"] == dem]
            ax.scatter(xs, ys, c=col, label=dem, alpha=0.7, s=34,
                       edgecolors="none")
        ax.axhline(0.0, color="grey", lw=0.8, ls="--")
        ax.set_xlabel(label)
        ax.set_ylabel("GAP = H_up + M_Phi")
        ax.set_title(f"GAP vs {label.split()[0]}")
        ax.legend(fontsize=8, title="demand")
    fig.suptitle("Phase 5 — Bound-and-Gap across the 72 sub-cells", y=1.02)
    fig.tight_layout()
    out = FIG_DIR / "phase5_fig1_gap_landscape.png"
    fig.savefig(out, dpi=130, bbox_inches="tight")
    plt.close(fig)
    print(f"  saved {out}")


def fig2_p5_vs_p6() -> None:
    cells = json.loads((RESULTS_DIR / "v0_5_phase5_blockB.json")
                       .read_text(encoding="utf-8"))["per_cell"]
    p6 = [c["P6_spo_tree"] for c in cells]
    p5 = [c["P5_phi"] for c in cells]
    lo = min(min(p5), min(p6)) * 0.97
    hi = max(max(p5), max(p6)) * 1.03
    fig, ax = plt.subplots(figsize=(5.2, 5.0))
    ax.plot([lo, hi], [lo, hi], color="grey", ls="--", lw=1,
            label="P5 = P6")
    ax.scatter(p6, p5, c="#d62728", s=46, alpha=0.8, edgecolors="none")
    ax.set_xlabel("P6 (SPO-Tree, cell-mean) median makespan")
    ax.set_ylabel("P5 (Φ-informed, cell-median) median makespan")
    ax.set_title("Figure 2 — P5 vs P6 (D1 differentiator)\n"
                 "points below the line: P5 faster")
    ax.set_xlim(lo, hi)
    ax.set_ylim(lo, hi)
    ax.legend(fontsize=9)
    fig.tight_layout()
    out = FIG_DIR / "phase5_fig2_p5_vs_p6.png"
    fig.savefig(out, dpi=130, bbox_inches="tight")
    plt.close(fig)
    print(f"  saved {out}")


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    print("Phase 5 W6 figures:")
    fig1_gap_landscape()
    fig2_p5_vs_p6()


if __name__ == "__main__":
    main()
