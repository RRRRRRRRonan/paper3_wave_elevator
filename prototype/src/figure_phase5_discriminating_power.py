"""
Figure 3b -- Bound-and-Gap discriminating power (section 5.2).

Caterpillar plot of the 72 Block A sub-cells: each sub-cell's GAP point estimate
with its 95% bootstrap CI, sorted by GAP, coloured by the D1-d outcome (CI
excludes 0 = resolved; else unresolved). It visualizes that the unresolved
sub-cells are the low-GAP ones (rank-AUC 0.92), i.e. the decomposition returns
null exactly where the value of wave structure is genuinely near zero.

Supplementary to Figure 3 (the F / |A| GAP landscape); it does not replace it.

Run from the prototype/ directory:  python -m src.figure_phase5_discriminating_power
"""
from __future__ import annotations

import json
import statistics as st
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

RESULTS = Path(__file__).resolve().parents[1] / "results"
FIG_DIR = RESULTS / "figures"


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(RESULTS / "v0_5_phase5_blockA.json") as f:
        ps = json.load(f)["per_subcell"]

    cells = sorted(ps, key=lambda c: c["GAP"])
    n = len(cells)
    ys = list(range(1, n + 1))
    gaps = [c["GAP"] for c in cells]
    lo = [max(0.0, c["GAP"] - c["gap_ci_lo"]) for c in cells]
    hi = [max(0.0, c["gap_ci_hi"] - c["GAP"]) for c in cells]
    passed = [c["gap_ci_lo"] > 0 for c in cells]
    colors = ["#2ca02c" if p else "#9a9a9a" for p in passed]

    P = [c["GAP"] for c in cells if c["gap_ci_lo"] > 0]
    F = [c["GAP"] for c in cells if c["gap_ci_lo"] <= 0]
    med_p, med_f = st.median(P), st.median(F)
    auc = sum(1 for a in P for b in F if a > b) / (len(P) * len(F))

    fig, ax = plt.subplots(figsize=(7.4, 8.6))
    for y, g, l, h, col in zip(ys, gaps, lo, hi, colors):
        ax.errorbar(g, y, xerr=[[l], [h]], fmt="o", ms=3.2, color=col,
                    ecolor=col, elinewidth=0.9, capsize=1.6, alpha=0.85)
    ax.axvline(0, color="black", lw=1.0, zorder=1)
    ax.axvline(med_f, color="#9a9a9a", ls=":", lw=1.3)
    ax.axvline(med_p, color="#2ca02c", ls=":", lw=1.3)
    ax.text(med_f, n + 1.4, f"unresolved\nmedian {med_f:.3f}", color="#5f5f5f",
            ha="center", va="bottom", fontsize=8.5)
    ax.text(med_p, n + 1.4, f"resolved\nmedian {med_p:.3f}", color="#2ca02c",
            ha="center", va="bottom", fontsize=8.5)

    leg = [
        Line2D([0], [0], marker="o", color="#2ca02c", lw=0,
               label=f"resolved, CI excludes 0  (n = {len(P)})"),
        Line2D([0], [0], marker="o", color="#9a9a9a", lw=0,
               label=f"unresolved  (n = {len(F)})"),
    ]
    ax.legend(handles=leg, loc="lower right", fontsize=9, framealpha=0.95)
    ax.set_xlabel("GAP (relative makespan) with 95% bootstrap CI")
    ax.set_ylabel("Block A sub-cell, sorted by GAP")
    ax.set_title(
        "Bound-and-Gap discriminating power: the unresolved sub-cells are the "
        "low-GAP ones\n"
        "rank-AUC  P[GAP(resolved) > GAP(unresolved)] = "
        f"{auc:.2f};  median separation {med_p / med_f:.1f}x",
        fontsize=10.5)
    ax.set_ylim(0, n + 6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

    fig.tight_layout()
    out = FIG_DIR / "phase5_fig3b_discriminating_power.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  saved {out}")
    print(f"  resolved n={len(P)} medGAP={med_p:.4f} | unresolved n={len(F)} "
          f"medGAP={med_f:.4f} | AUC={auc:.3f}")


if __name__ == "__main__":
    main()
