"""
Methodology schematic figures for §4.

  Figure 1 — Bound-and-Gap decomposition (§4.1.3): a stylized
             (regime, model, size) sub-cell illustrating
             GAP = H_up + M_Phi = UB − LB on a tiled number line.

  Figure 2 — Model-Dominance Hedge Rule (§4.2.2): chain dominance + the
             Wasserstein-DRO worst case + the closed-form decision flow.

Both figures use stylized illustrative values; the publication-scale empirical
quantities are in §5's figures (figure_phase5.py).
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch
from scipy.stats import norm

FIG_DIR = Path(__file__).resolve().parents[1] / "results" / "figures"


def fig1_bound_and_gap_schematic() -> None:
    """Figure 1 — Bound-and-Gap decomposition on a stylized sub-cell."""
    # Stylized illustrative values (the four corner medians partition the
    # UB span into M_Phi, LB, H_up in order from left to right).
    m_qmin, m_qphi, m_0, m_qmax = 92.0, 95.0, 100.0, 115.0
    UB = (m_qmax - m_qmin) / m_0
    LB = (m_0 - m_qphi) / m_0
    H_up = (m_qmax - m_0) / m_0
    M_phi = (m_qphi - m_qmin) / m_0
    GAP = H_up + M_phi  # = UB − LB

    fig, ax = plt.subplots(figsize=(10, 4.4))
    ax.axhline(0, color="black", linewidth=0.8, zorder=1)

    # marker ticks + labels
    markers = [
        (m_qmin, r"$m_{q_{\min}}$", "#2ca02c"),
        (m_qphi, r"$m_{q_\Phi}$",   "#ff7f0e"),
        (m_0,    r"$m_0$",          "#7f7f7f"),
        (m_qmax, r"$m_{q_{\max}}$", "#d62728"),
    ]
    for x, label, color in markers:
        ax.plot([x, x], [-0.07, 0.07], color=color, linewidth=3, zorder=3)
        ax.text(x, 0.11, label, ha="center", va="bottom",
                fontsize=12.5, color=color, fontweight="bold")

    # Three tiles below the line — M_Phi | LB | H_up
    y_tile = -0.16
    tile_h = 0.10
    tiles = [
        (m_qmin, m_qphi, "#ff7f0e", r"$M_\Phi$" + f"  = {M_phi:.2f}"),
        (m_qphi, m_0,    "#1f77b4", "LB"        + f"  = {LB:.2f}"),
        (m_0,    m_qmax, "#d62728", r"$H_{\mathrm{up}}$" + f"  = {H_up:.2f}"),
    ]
    for x1, x2, color, label in tiles:
        ax.add_patch(plt.Rectangle((x1, y_tile - tile_h), x2 - x1, tile_h,
                                   facecolor=color, edgecolor="black",
                                   linewidth=0.6, alpha=0.55))
        ax.text((x1 + x2) / 2, y_tile - tile_h / 2, label,
                ha="center", va="center", fontsize=10.5)

    # UB bracket above (full span)
    y_ub = 0.36
    ax.plot([m_qmin, m_qmin, m_qmax, m_qmax],
            [y_ub - 0.04, y_ub, y_ub, y_ub - 0.04],
            color="#8a2be2", linewidth=1.6)
    ax.text((m_qmin + m_qmax) / 2, y_ub + 0.04,
            f"UB = $(m_{{q_{{\\max}}}} - m_{{q_{{\\min}}}})\\,/\\,m_0$ = {UB:.2f}",
            ha="center", va="bottom", fontsize=11.5,
            color="#8a2be2", fontweight="bold")

    # GAP annotation
    ax.text((m_qmin + m_qmax) / 2, -0.46,
            f"GAP  =  $M_\\Phi + H_{{\\mathrm{{up}}}}$  =  UB $-$ LB  =  {GAP:.2f}",
            ha="center", va="center", fontsize=13, fontweight="bold",
            color="black",
            bbox=dict(boxstyle="round,pad=0.45", facecolor="white",
                      edgecolor="black", linewidth=1.1))

    ax.set_xlim(m_qmin - 4, m_qmax + 4)
    ax.set_ylim(-0.66, 0.66)
    ax.set_xlabel("Wave-conditional median makespan (relative scale)")
    ax.set_yticks([])
    ax.set_title("Bound-and-Gap decomposition on a stylized (regime, model, size) "
                 "sub-cell\n(Proposition 1: $\\mathrm{GAP} = "
                 "H_{\\mathrm{up}} + M_\\Phi$, both non-negative)",
                 fontsize=11)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)

    fig.tight_layout()
    out = FIG_DIR / "fig_bound_and_gap_schematic.png"
    fig.savefig(out, dpi=140, bbox_inches="tight")
    plt.close(fig)
    print(f"  saved {out}")


def fig2_hedge_rule_schematic() -> None:
    """Figure 2 — Hedge Rule chain dominance + closed-form decision rule."""
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.8))

    # --- Panel (a): chain dominance via CDFs ---
    ax = axes[0]
    x = np.linspace(120, 320, 500)
    F1 = norm.cdf(np.log(x), np.log(180), 0.15)
    F2 = norm.cdf(np.log(x), np.log(230), 0.15)
    ax.plot(x, F1, color="steelblue", linewidth=2.6,
            label=r"$F_{M_1}(t)$   throughput abstraction")
    ax.plot(x, F2, color="firebrick", linewidth=2.6,
            label=r"$F_{M_2}(t)$   true batching")
    ax.fill_between(x, F2, F1, where=(F1 >= F2),
                    alpha=0.15, color="gray")
    ax.text(258, 0.42,
            r"$F_{M_1}(t) \geq F_{M_2}(t)$" + "\n"
            r"$\Rightarrow\ M_2$ stochastically" + "\nlarger than $M_1$",
            fontsize=9.5, ha="left",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                      edgecolor="gray", alpha=0.9))
    ax.annotate("", xy=(245, 0.30), xytext=(180, 0.30),
                arrowprops=dict(arrowstyle="<->", color="black", linewidth=1.2))
    ax.text(212, 0.24, r"$\rho = W_1(M_1,\,M_2)$",
            ha="center", va="top", fontsize=10, fontstyle="italic")
    ax.set_xlabel("Makespan  $t$")
    ax.set_ylabel("CDF")
    ax.set_title("(a)  Chain dominance + Wasserstein-DRO ball:\n"
                 r"worst case in $B_\rho(M_1)$ attained at $M_2$",
                 fontsize=10.5)
    ax.legend(loc="lower right", fontsize=9)
    ax.grid(alpha=0.3)
    ax.set_xlim(120, 320)
    ax.set_ylim(0, 1.0)

    # --- Panel (b): decision flowchart ---
    ax = axes[1]
    ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    ax.axis("off")

    def box(x, y, w, h, text, color="white"):
        p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.14",
                           facecolor=color, edgecolor="black", linewidth=1.2)
        ax.add_patch(p)
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
                fontsize=9.8)

    box(0.5, 8.0, 9.0, 1.3,
        "Input:  wave $W$;  model family\n"
        r"$\mathcal{M} = \{M_1, M_2, M_3\}$",
        "#f0f0f0")
    box(0.5, 5.4, 9.0, 1.7,
        "Verify chain dominance:\n"
        r"$\mathrm{P}\,[\,C_{\max}(W; M_2) \geq C_{\max}(W; M_1)\,] \geq 1 - \varepsilon$"
        + "\n(empirical, Section 5.3)",
        "#fff4e6")
    box(0.5, 2.8, 9.0, 1.7,
        "Theorem 2  —  minimax collapse:\n"
        r"$c^{\star} = \arg\min_c\ s\,[\,C_{\max}(W; M_2)\ \mid\ c\,]$"
        + "\n(no online model identification)",
        "#e8f4e0")
    box(0.5, 0.5, 9.0, 1.2,
        r"Output:  dispatch corner $c^{\star}$",
        "#f0f0f0")

    for y_top, y_bot in [(8.0, 7.15), (5.4, 4.55), (2.8, 1.75)]:
        ax.annotate("", xy=(5, y_bot), xytext=(5, y_top),
                    arrowprops=dict(arrowstyle="->", color="black",
                                    linewidth=1.4))

    ax.set_title("(b)  Closed-form dispatch rule  (Theorem 2;\n"
                 "no online model selection)", fontsize=10.5)

    fig.tight_layout()
    out = FIG_DIR / "fig_hedge_rule_schematic.png"
    fig.savefig(out, dpi=140, bbox_inches="tight")
    plt.close(fig)
    print(f"  saved {out}")


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    print("Methodology schematic figures (§4):")
    fig1_bound_and_gap_schematic()
    fig2_hedge_rule_schematic()


if __name__ == "__main__":
    main()
