"""
Revision 2026-07-08: publication figures (amendment A-R4, presentation layer).

Reads only existing artefacts (v0_5_phase5_*.json). Outputs PNG to this folder.

Palette: Okabe-Ito (peer-reviewed colorblind-safe standard for print).
Node-based palette validator unavailable on this machine; Okabe-Ito is the
documented CVD-safe fallback. Categorical hues assigned in fixed order:
demand uniform=blue, clustered=orange, diurnal=green (never cycled).
Terminology per paper_draft/TERMINOLOGY.md: wave-release (never "dispatch")
for the tactical rule; C = vertical spread; no em-dashes in figure text.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RESULTS = ROOT / "prototype" / "results"

OI = {"blue": "#0072B2", "orange": "#E69F00", "skyblue": "#56B4E9",
      "green": "#009E73", "vermillion": "#D55E00", "purple": "#CC79A7",
      "gray": "#7F7F7F", "black": "#000000"}
DEMAND_COLOR = {"uniform": OI["blue"], "clustered": OI["orange"],
                "diurnal": OI["green"]}

plt.rcParams.update({
    "font.size": 10, "axes.titlesize": 11, "axes.labelsize": 10,
    "legend.fontsize": 9, "figure.dpi": 100, "savefig.dpi": 300,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.25, "grid.linewidth": 0.6,
})


def load(name: str) -> dict:
    return json.loads((RESULTS / name).read_text(encoding="utf-8"))


def save(fig, name: str):
    out = HERE / name
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"  saved {out}")


# ---------------------------------------------------------------- Figure 1 --
def fig1_system_schematic():
    """Two panels: (a) physical system; (b) two-stage decision architecture."""
    fig, axes = plt.subplots(1, 2, figsize=(12.6, 5.0),
                             gridspec_kw={"width_ratios": [1.15, 1.0]})

    # ---- (a) physical system ----
    ax = axes[0]
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    F = 4
    floor_h, floor_y0 = 1.9, 0.7
    shaft_x, shaft_w = 7.4, 1.15
    for f in range(F):
        y = floor_y0 + f * (floor_h + 0.12)
        ax.add_patch(Rectangle((0.6, y), 6.5, floor_h, facecolor="#F2F2F2",
                               edgecolor="black", linewidth=1.0))
        ax.text(0.75, y + floor_h - 0.32, f"floor {f + 1}", fontsize=8.5,
                color="#444444")
        for sx in (2.0, 3.4, 4.8):
            ax.add_patch(Rectangle((sx, y + 0.25), 0.75, 0.5,
                                   facecolor="#D9D9D9", edgecolor="#777777",
                                   linewidth=0.7))
        amr_y = y + 1.15
        for ax_x, c in ((2.6, OI["blue"]), (4.35, OI["blue"])):
            ax.add_patch(plt.Circle((ax_x, amr_y), 0.21, facecolor=c,
                                    edgecolor="white", linewidth=1.2,
                                    zorder=5))
    ax.text(3.85, floor_y0 + F * (floor_h + 0.12) + 0.25,
            "AMR fleet: floor-bound between elevator rides",
            ha="center", fontsize=9.5)
    # elevator shaft
    ax.add_patch(Rectangle((shaft_x, floor_y0), shaft_w,
                           F * (floor_h + 0.12) - 0.12,
                           facecolor="#FFF3DF", edgecolor="black",
                           linewidth=1.2))
    ax.add_patch(Rectangle((shaft_x + 0.13, floor_y0 + 1 * (floor_h + 0.12)
                            + 0.25), shaft_w - 0.26, 1.25,
                           facecolor=OI["orange"], edgecolor="black",
                           linewidth=1.0))
    ax.text(shaft_x + shaft_w / 2, floor_y0 - 0.42,
            "E shared freight elevators\n(capacity c, the bottleneck)",
            ha="center", va="top", fontsize=9.5)
    # 5-phase trip annotation
    steps = ["1 wait", "2 reposition", "3 load (2 s)", "4 travel",
             "5 unload (2 s)"]
    ax.text(9.15, 6.4, "elevator trip:\n" + "\n".join(steps), fontsize=8.6,
            va="top", ha="left",
            bbox=dict(boxstyle="round,pad=0.35", facecolor="white",
                      edgecolor="#999999"))
    ax.annotate("", xy=(shaft_x + shaft_w / 2, 7.6),
                xytext=(shaft_x + shaft_w / 2, 3.1),
                arrowprops=dict(arrowstyle="->", color=OI["vermillion"],
                                linewidth=1.8))
    ax.set_title("(a) Multi-story AMR warehouse with shared freight elevators")

    # ---- (b) two-stage decision architecture ----
    ax = axes[1]
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")

    def box(x, y, w, h, text, fc, fs=9.6):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.16",
                                    facecolor=fc, edgecolor="black",
                                    linewidth=1.1))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
                fontsize=fs)

    box(0.7, 7.7, 8.6, 1.8,
        "Tactical stage (STUDIED HERE)\nwave composition: which orders to "
        "release together\nrepresented by $\\Phi = (C, I, T)$", "#E3EEF7")
    box(0.7, 4.6, 8.6, 1.6,
        "wave fixes the elevator-trip demand\n(how many trips, directions, "
        "how spread across floors)", "#F7F7F7")
    box(0.7, 1.6, 8.6, 1.8,
        "Operational stage (HELD FIXED)\nAMR dispatch through the shared "
        "elevators\nunder elevator model $M \\in \\{M_1, M_2, M_3\\}$",
        "#FFF3DF")
    for y1, y2 in ((7.7, 6.3), (4.6, 3.5)):
        ax.annotate("", xy=(5.0, y2), xytext=(5.0, y1),
                    arrowprops=dict(arrowstyle="->", color="black",
                                    linewidth=1.5))
    ax.text(5.0, 0.75, "makespan $C_{\\max}(W; M)$", ha="center",
            fontsize=10.5, fontweight="bold")
    ax.annotate("", xy=(5.0, 1.0), xytext=(5.0, 1.55),
                arrowprops=dict(arrowstyle="->", color="black",
                                linewidth=1.5))
    ax.set_title("(b) Two-stage decision architecture")
    save(fig, "fig1_system_schematic.png")


# ---------------------------------------------------------------- Figure 2 --
def fig2_hedge_schematic_v2():
    """Hedge Rule schematic, rewritten wording: wave-release (not dispatch),
    model family scoped to {M1, M2} with M3 via the epsilon bound."""
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.8))

    ax = axes[0]
    x = np.linspace(120, 320, 500)
    F1 = norm.cdf(np.log(x), np.log(180), 0.15)
    F2 = norm.cdf(np.log(x), np.log(230), 0.15)
    ax.plot(x, F1, color=OI["blue"], linewidth=2.4,
            label="$F_{M_1}(t)$  throughput abstraction")
    ax.plot(x, F2, color=OI["vermillion"], linewidth=2.4,
            label="$F_{M_2}(t)$  true co-occupancy batching")
    ax.fill_between(x, F2, F1, where=(F1 >= F2), alpha=0.15, color="gray")
    ax.text(256, 0.44,
            "$F_{M_1}(t) \\geq F_{M_2}(t)$\n$\\Rightarrow M_2$ "
            "stochastically\nlarger than $M_1$",
            fontsize=9.5, ha="left",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                      edgecolor="gray", alpha=0.9))
    ax.annotate("", xy=(245, 0.30), xytext=(180, 0.30),
                arrowprops=dict(arrowstyle="<->", color="black",
                                linewidth=1.2))
    ax.text(212, 0.24, "$\\rho_q = W_1(M_1, M_2 \\mid q)$", ha="center",
            va="top", fontsize=10, fontstyle="italic")
    ax.set_xlabel("Makespan $t$")
    ax.set_ylabel("CDF")
    ax.set_title("(a) Chain dominance and the Wasserstein ball:\n"
                 "worst case in $B_{\\rho_q}(M_1)$ attained at $M_2$",
                 fontsize=10.5)
    ax.legend(loc="lower right", fontsize=9)
    ax.set_xlim(120, 320); ax.set_ylim(0, 1.0)

    ax = axes[1]
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")

    def box(x, y, w, h, text, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.14",
                                    facecolor=color, edgecolor="black",
                                    linewidth=1.2))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
                fontsize=9.6)

    box(0.5, 8.0, 9.0, 1.3,
        "Input: candidate wave structures (corners);\nrival models "
        "$\\{M_1, M_2\\}$ ($M_3$ via the $\\varepsilon$ bound)", "#F0F0F0")
    box(0.5, 5.4, 9.0, 1.7,
        "Verify chain dominance (Proposition 2 conditions;\nempirically "
        "$\\mathrm{P}[C_{\\max}(W; M_2) \\geq C_{\\max}(W; M_1)] = 0.992$,\n"
        "publication scale, Section 5.3)", "#FFF3DF")
    box(0.5, 2.8, 9.0, 1.7,
        "Minimax collapse (with Wasserstein-DRO certification):\n"
        "select the corner the true-batching model prefers,\nno model "
        "identification, no robust program solved", "#E6F2E6")
    box(0.5, 0.5, 9.0, 1.2,
        "Output: release corner $q^{\\star}$ with worst-case\nguarantee "
        "$U_q(\\varepsilon)$ (Corollary 2)", "#F0F0F0")
    for y_top, y_bot in [(8.0, 7.15), (5.4, 4.55), (2.8, 1.75)]:
        ax.annotate("", xy=(5, y_bot), xytext=(5, y_top),
                    arrowprops=dict(arrowstyle="->", color="black",
                                    linewidth=1.4))
    ax.set_title("(b) Closed-form wave-release rule\n(no online model "
                 "selection)", fontsize=10.5)
    fig.tight_layout()
    save(fig, "fig2_hedge_rule_schematic_v2.png")


# ---------------------------------------------------------------- Figure 3 --
def fig3_gap_by_demand():
    """GAP with 95% CI across 72 sub-cells, faceted by demand pattern
    (the pre-registered presentation; marginal F/|A| views are aliased)."""
    per = load("v0_5_phase5_blockA.json")["per_subcell"]
    demands = ["uniform", "clustered", "diurnal"]
    fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.2), sharey=True)
    for ax, dem in zip(axes, demands):
        sub = [r for r in per if r["demand"] == dem]
        sub.sort(key=lambda r: (r["config_id"], r["model"], r["size"]))
        cfgs = sorted({r["config_id"] for r in sub})
        xpos, seen = [], {}
        for r in sub:
            base = cfgs.index(r["config_id"])
            k = seen.get(r["config_id"], 0)
            seen[r["config_id"]] = k + 1
            xpos.append(base + (k - 1.5) * 0.16)
        col = DEMAND_COLOR[dem]
        for x, r in zip(xpos, sub):
            lo, hi = r["gap_ci_lo"], r["gap_ci_hi"]
            ax.plot([x, x], [lo, hi], color=col, linewidth=1.2, alpha=0.8,
                    zorder=2)
            if r["d1d"]:
                ax.plot(x, r["GAP"], "o", color=col, markersize=4.5,
                        markeredgecolor="white", markeredgewidth=0.6,
                        zorder=3)
            else:
                ax.plot(x, r["GAP"], "o", markerfacecolor="white",
                        markeredgecolor=col, markersize=4.5,
                        markeredgewidth=1.2, zorder=3)
        ax.axhline(0, color="black", linewidth=0.8)
        ax.set_xticks(range(len(cfgs)))
        ax.set_xticklabels([f"cfg {c}" for c in cfgs], fontsize=8.5)
        ax.set_title(f"{dem} demand", color=col, fontweight="bold")
        if ax is axes[0]:
            ax.set_ylabel("GAP (pool-relative)")
    filled = plt.Line2D([], [], marker="o", linestyle="", color="#555555",
                        markersize=5, label="resolved (95% CI excludes 0)")
    openm = plt.Line2D([], [], marker="o", linestyle="",
                       markerfacecolor="white", markeredgecolor="#555555",
                       markersize=5, label="unresolved")
    axes[1].legend(handles=[filled, openm], loc="upper right", frameon=True)
    fig.suptitle("GAP across the 72 sub-cells, faceted by demand pattern "
                 "(publication scale).\nFractional design aliases F, |A|, "
                 "and demand: facets are descriptive, not main effects.",
                 fontsize=10, y=1.04)
    fig.tight_layout()
    save(fig, "fig3_gap_by_demand.png")


# ---------------------------------------------------------------- Figure 4 --
def fig4_p5_vs_p6_signed():
    """Signed per-cell relative difference (P5 - P6)/P6, diverging bars."""
    cells = load("v0_5_phase5_blockB.json")["per_cell"]
    rows = [{"label": f"cfg {c['config_id']} / size {c['size']}",
             "diff": 100 * (c["P5_phi"] - c["P6_spo_tree"]) / c["P6_spo_tree"]}
            for c in cells]
    rows.sort(key=lambda r: r["diff"])
    y = np.arange(len(rows))
    vals = [r["diff"] for r in rows]
    colors = [OI["blue"] if v < -1e-9 else
              (OI["gray"] if abs(v) <= 1e-9 else OI["vermillion"])
              for v in vals]
    fig, ax = plt.subplots(figsize=(7.6, 5.2))
    ax.barh(y, vals, color=colors, edgecolor="white", linewidth=1.2,
            height=0.72)
    ax.axvline(0, color="black", linewidth=1.0)
    ax.set_yticks(y)
    ax.set_yticklabels([r["label"] for r in rows], fontsize=8.5)
    for yi, v in zip(y, vals):
        ax.text(v + (0.15 if v >= 0 else -0.15), yi, f"{v:+.1f}%",
                va="center", ha="left" if v >= 0 else "right", fontsize=8)
    n_p5 = sum(v < -1e-9 for v in vals)
    ax.set_xlabel("cell-median makespan difference (P5 $-$ P6) / P6, %")
    ax.set_title(f"$\\Phi$ corner rule (P5) vs SPO-Tree (P6) per cell:\n"
                 f"P5 lower in {n_p5}/{len(rows)} cells "
                 "(blue = P5 better, red = P6 better, gray = tie)")
    lim = max(abs(v) for v in vals) * 1.25
    ax.set_xlim(-lim, lim)
    fig.tight_layout()
    save(fig, "fig4_p5_vs_p6_signed_diff.png")


# ---------------------------------------------------------------- Figure 5 --
def fig5_decomposition_stacked():
    """H_up + M_Phi stacked per config (mean over the 4 sub-cells)."""
    per = load("v0_5_phase5_blockA.json")["per_subcell"]
    cfgs = sorted({r["config_id"] for r in per})
    hup, mphi, dem = [], [], []
    for c in cfgs:
        sub = [r for r in per if r["config_id"] == c]
        hup.append(np.mean([r["H_up"] for r in sub]))
        mphi.append(np.mean([r["M_Phi"] for r in sub]))
        dem.append(sub[0]["demand"])
    x = np.arange(len(cfgs))
    fig, ax = plt.subplots(figsize=(10.5, 4.4))
    ax.bar(x, hup, color=OI["blue"], edgecolor="white", linewidth=1.2,
           label="$H_{\\mathrm{up}}$ structural ceiling (capacity-side)")
    ax.bar(x, mphi, bottom=hup, color=OI["orange"], edgecolor="white",
           linewidth=1.2,
           label="$M_\\Phi$ policy-recoverable slack")
    mean_h = np.mean(hup); mean_m = np.mean(mphi)
    share = mean_h / (mean_h + mean_m)
    ax.axhline(mean_h + mean_m, color="black", linewidth=0.9,
               linestyle="--", alpha=0.6)
    ax.text(len(cfgs) - 0.4, mean_h + mean_m + 0.004,
            f"grid mean GAP = {mean_h + mean_m:.3f} "
            f"(capacity share {share:.0%}, $\\Phi$-rule metric)",
            ha="right", fontsize=9)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{c}\n{d[:4]}" for c, d in zip(cfgs, dem)],
                       fontsize=8)
    ax.set_xlabel("configuration (demand pattern abbreviated below)")
    ax.set_ylabel("pool-relative value of wave structure")
    ax.set_title("Bound-and-Gap decomposition per configuration, mean over "
                 "models {M1, M2} x sizes {8, 30}\n(publication scale; share "
                 "is partition-conditional, see the sensitivity table)")
    ax.legend(loc="upper right")
    fig.tight_layout()
    save(fig, "fig5_decomposition_stacked.png")


# ---------------------------------------------------------------- Figure 6 --
def fig6_policy_relative():
    """Distribution over 12 cells of cell-median makespan relative to P0."""
    cells = load("v0_5_phase5_blockB.json")["per_cell"]
    pols = ["P0_random", "P1_dest_cluster", "P2_cardinality",
            "P3_dir_balanced", "P4_temporal", "P5_phi", "P6_spo_tree",
            "P7_localsearch"]
    short = [p.split("_")[0] for p in pols]
    data = [[c[p] / c["P0_random"] for c in cells] for p in pols]
    fig, ax = plt.subplots(figsize=(9.6, 4.6))
    bp = ax.boxplot(data, positions=range(len(pols)), widths=0.55,
                    patch_artist=True, showfliers=False,
                    medianprops=dict(color="black", linewidth=1.4))
    hi_col = {"P5_phi": OI["blue"], "P7_localsearch": OI["orange"]}
    for patch, p in zip(bp["boxes"], pols):
        patch.set_facecolor(hi_col.get(p, "#DDDDDD"))
        patch.set_edgecolor("#555555")
    rng = np.random.default_rng(20260708)
    for i, d in enumerate(data):
        jitter = rng.uniform(-0.13, 0.13, len(d))
        ax.plot(np.array([i] * len(d)) + jitter, d, "o", markersize=3.4,
                color="#333333", alpha=0.55, zorder=3)
    ax.axhline(1.0, color="black", linewidth=0.9, linestyle="--", alpha=0.7)
    ax.set_xticks(range(len(pols)))
    ax.set_xticklabels(short)
    ax.set_ylabel("cell-median makespan relative to P0 (random)")
    ax.set_title("Wave-release policy contest over the 12 Block B cells "
                 "(publication scale).\nHighlighted: P5 $\\Phi$ corner rule "
                 "(blue) and P7 local-search reference (orange).")
    fig.tight_layout()
    save(fig, "fig6_policy_relative_distributions.png")


# ---------------------------------------------------------------- Figure 7 --
def fig7_decision_workflow():
    """Practitioner decision workflow with the config-7 worked example
    (publication-scale numbers from storyline / Block A+C artefacts)."""
    fig, ax = plt.subplots(figsize=(9.0, 7.6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 13.4); ax.axis("off")

    def box(x, y, w, h, text, fc, fs=9.4, ec="black"):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                                    facecolor=fc, edgecolor=ec,
                                    linewidth=1.15))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
                fontsize=fs)

    def arrow(x1, y1, x2, y2, label=""):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2),
                                     arrowstyle="-|>", mutation_scale=14,
                                     color="black", linewidth=1.3))
        if label:
            ax.text((x1 + x2) / 2 + 0.15, (y1 + y2) / 2, label, fontsize=8.8,
                    ha="left", va="center", fontstyle="italic")

    box(1.6, 12.0, 6.8, 1.1,
        "Warehouse instance: F floors, |A| AMRs, E elevators, demand",
        "#F0F0F0")
    box(1.6, 10.2, 6.8, 1.2,
        "[1] Compute $\\Phi = (C, I, T)$ on the candidate waves;\n"
        "partition by $(C, I)$ into 2x2 corners", "#E3EEF7")
    box(1.6, 8.0, 6.8, 1.5,
        "[2] Tool 1, Bound-and-Gap (diagnostic):\n"
        "$\\mathrm{GAP} = H_{\\mathrm{up}} + M_\\Phi$\n"
        "worked example config 7: $0.178 = 0.157 + 0.021$", "#E6F2E6")
    arrow(5.0, 12.0, 5.0, 11.4)
    arrow(5.0, 10.2, 5.0, 9.5)

    # branch
    box(0.4, 5.4, 4.3, 1.7,
        "$H_{\\mathrm{up}}$ dominant, $M_\\Phi$ small\n(config 7: 88% vs "
        "12%)\ncapacity is the lever:\nadd elevator capacity or\nrefine the "
        "partition", "#FFF3DF", fs=8.8)
    box(5.3, 5.4, 4.3, 1.7,
        "$M_\\Phi$ non-negligible\nwave composition is worth\npursuing: "
        "recover $M_\\Phi$ with\npredict-then-optimize methods", "#FFF3DF",
        fs=8.8)
    arrow(3.6, 8.0, 2.5, 7.1)
    arrow(6.4, 8.0, 7.5, 7.1)

    box(5.3, 3.1, 4.3, 1.5,
        "[3] Tool 2, Hedge Rule (prescriptive):\nrelease from the corner "
        "$M_2$ prefers\n(config 7: LC_HI, = DRO optimum)", "#E3EEF7", fs=8.8)
    arrow(7.5, 5.4, 7.5, 4.6)
    box(5.3, 0.9, 4.3, 1.4,
        "[4] Report the worst-case guarantee\n$U_q(0.05) = 3.4\\%$ of "
        "baseline makespan\n(config 7, publication scale)", "#F0F0F0",
        fs=8.8)
    arrow(7.5, 3.1, 7.5, 2.3)
    box(0.4, 0.9, 4.3, 1.4,
        "still releasing waves?\napply Tool 2 anyway:\nrobust corner at "
        "zero extra cost", "#F7F7F7", fs=8.8)
    arrow(2.5, 5.4, 2.5, 2.3)

    ax.set_title("Practitioner workflow: diagnose with Bound-and-Gap, "
                 "then release with the Hedge Rule\n(worked numbers: "
                 "configuration 7, publication scale)", fontsize=11)
    fig.tight_layout()
    save(fig, "fig7_decision_workflow.png")


def main():
    print("Revision 2026-07-08 figures:")
    fig1_system_schematic()
    fig2_hedge_schematic_v2()
    fig3_gap_by_demand()
    fig4_p5_vs_p6_signed()
    fig5_decomposition_stacked()
    fig6_policy_relative()
    fig7_decision_workflow()


if __name__ == "__main__":
    main()
