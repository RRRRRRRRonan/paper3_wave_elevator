---
title: "Wave Release Coordination under Vertical Resource Constraints in Multi-Storey AMR Warehouses"
section: "Abstract + Introduction prose draft v0.1"
date: 2026-04-22
status: "First prose pass — to be tightened against §6 numbers in v0.2"
---

# Abstract — *target 200 words; current 181*

Multi-storey warehouses staffed by floor-bound autonomous mobile robots (AMRs) couple wave-release decisions to a small number of freight elevators whose per-trip capacity is the binding constraint. We formalise this as the **wave release coordination problem under vertical resource constraints**: a two-stage scheduler that selects wave composition tactically and dispatches AMR–elevator execution operationally. We contribute: (i) a three-dimensional structured decomposition $\Phi = (C, I, T)$ with physically interpretable per-unit coefficients; (ii) a **Bound-and-Gap framework** whose decomposition theorem splits the value of wave-structure information into a partition-intrinsic upper bound and a $\Phi$-policy lower bound (mean GAP 5.83 %, CI excludes zero in 6/6 cells); (iii) a **Model-Dominance Hedge Rule** collapsing under per-wave stochastic dominance ($\mathbb{P}[M_2 \ge M_1] = 99.4 \%$ across $c \in \{2, 3, 4, 5\}$) to a closed-form rule with worst-case loss 3.1–9.9 %. Across 18 000 regime-sweep simulations, the predictive value of structured features grows ten-fold with elevator-bottleneck relief. A pre-registered 14 400-simulation policy test produces a **tactical-operational substitutability map**: destination-clustered batching cuts mean makespan up to 9 % exactly in the cells our framework flags prospectively (6/6 cells correctly classified). Robustness across ~170 000 total simulations covers building heights $F \in \{5, 7, 9\}$, heterogeneous elevator pools, and service-time CV up to 131 %.

---

# §1. Introduction

## 1.1 Motivating scenario *(target 200 words; current 196)*

Consider a multi-storey fulfilment warehouse with $F$ floors, $E$ freight elevators of per-trip capacity $c$, and a fleet of floor-bound AMRs. An order travels horizontally on its source floor, vertically by elevator, and horizontally on its destination floor; the elevator is the only vertical channel and is shared by the entire fleet. Operations managers control two layers. The **operational** layer assigns AMRs to orders and sequences elevator boardings — a problem with substantial existing literature, from order batching in vertical lift modules to SAT-based optimal robot–lift schedules. The **tactical** layer chooses *which orders co-occupy a release window* — what we call a wave. Wave composition determines how many vertical transitions the elevators must serve, in which directions, and with what temporal stagger; it therefore sets the difficulty of the operational problem before any robot moves. Despite this, wave composition has not been treated as a decision variable jointly with elevator capacity in the AMR-warehouse literature. The omission matters: the wave layer is the cheapest place to relieve a vertical bottleneck, because it costs only a re-batching of already-released orders, with no change to floor layout or fleet size.

## 1.2 Why this is hard now *(target 250 words; current 245)*

Three threads of recent work each touch part of this problem and stop short of the wave-elevator coupling.

Order batching for **vertical lift modules** [Lenoble et al., 2018] optimises pick rounds inside a single device; the relevant decision is which items to retrieve in one shuttle trip, not which orders to release into a building-scale wave. The mathematics is local to the device.

Multi-agent **robot–lift scheduling** [Chakravarty et al., 2025] takes a fixed task set and computes provably optimal lift schedules via Boolean satisfiability. Lift availability appears as a constraint, not as a design lever for the upstream wave layer; task selection is exogenous.

**Tier-captive shuttle systems** [Wu et al., 2024] and multi-level RMFS architectures [Keung, 2023] study performance with floor-attached transport (one shuttle per tier), where vertical coupling is structurally weaker. The closer setting — flexible AMRs that can occupy any floor and queue at any elevator — produces a different bottleneck topology that these analyses do not address.

Two further methodological threads bear on our framing. **Robust scheduling under model uncertainty** [Wiesemann et al., 2014; Lu and Shen, 2021] handles parametric uncertainty in known model classes, whereas the elevator literature offers genuinely *different* abstractions (throughput aggregation versus true co-occupancy batching) whose disagreement is structural, not parametric. **Prediction-to-decision regret** [Elmachtoub and Grigas, 2022; Vera et al., 2022] bounds algorithmic loss when a learned predictor drives a downstream optimiser; we are interested in a complementary quantity — the *information gap* between an oracle on the same feature partition and a $\Phi$-informed policy — that those bounds do not name.

## 1.3 Two empirical surprises that drive the paper *(target 250 words; current 248)*

Two specific findings from a 14 400-simulation sweep across six (regime, elevator-model) cells motivate the methodological apparatus.

**Surprise A — wave structure has bounded but consistent value.** A $\Phi$-informed corner pick beats a random wave in 6/6 cells, but the lift is only 1.3–7.4 %, while the *oracle* corner — the best of the four quartile bins on $(C, I)$ — wins 5–15 %. Neither zero nor full: the gap between informed policy and oracle is itself an object that needs a name and a decomposition. We provide both (§5.3): a Bound-and-Gap framework whose decomposition theorem $\mathrm{GAP} = H_{\mathrm{up}} + M_\Phi$ separates partition-intrinsic difficulty from $\Phi$-policy slack, and a partition-refinement corollary that explains, rather than rescues, the inflation of upper bounds under finer feature grids.

**Surprise B — elevator-modelling assumption flips a structural sign.** Re-running identical waves under throughput aggregation versus true co-occupancy batching flips the sign of the entropy coefficient $\beta(C)$ in 2 of 3 c=2 regimes. Bootstrap stability is 76–85 % within regime, so we treat the sign-flip as a coarse diagnostic, not a fine classifier; the load-bearing fact for our hedge rule is the underlying *per-wave dominance*: true-batching makespan exceeds throughput-abstraction makespan in 92.5–100 % of waves across all 15 cells. From this, the minimax wave-corner selection (§5.4) collapses in $c=2$ regimes to a one-line rule — *always pick the corner the true-batching model prefers* — with worst-case loss 3.1–9.9 %.

## 1.4 Contributions and roadmap *(target 300 words; current 301)*

We make three contributions.

**(C1) Problem formulation.** We formalise the wave release coordination problem under vertical resource constraints — a two-stage scheduler coupling tactical wave composition and operational AMR–elevator execution under a hard per-trip capacity. Related precedents address batching at the device level [Lenoble et al., 2018], optimal scheduling for fixed task sets [Chakravarty et al., 2025], or tier-captive transport [Wu et al., 2024; Keung, 2023]; none treat wave composition jointly with building-scale vertical coupling and flexible fleet routing.

**(C2) Methodology — three components.** **(C2-Φ)** A three-dimensional structured decomposition $\Phi = (C, I, T)$ — vertical concentration, directional imbalance, temporal clustering — with physically interpretable per-unit coefficients. (A methodological caveat: throughput-abstraction and true-batching regressions agree on wave rank order, $r \ge 0.85$, but disagree on $\beta(C)$ sign, *motivating* the hedge rule below.) **(C2-M4)** A **Bound-and-Gap framework** with a decomposition theorem $\mathrm{GAP} = H_{\mathrm{up}} + M_\Phi$ (non-negative components, partition-refinement monotonicity), converting the gap into a per-cell diagnostic. **(C2-M5)** A **Model-Dominance Hedge Rule**: under per-wave stochastic dominance, the minimax corner collapses to "follow $M_2$" with worst-case loss 3.1–9.9 %, and a one-sided $\varepsilon$-bound predicts when the collapse remains sharp. Two confirmations: M3 stochastic experiment exhibits the predicted knife-edge at E2_c2 $\sigma = 0.20$, and a directional-elevator extension ($\mathbb{P}[M_4 \ge M_2] = 97.7 \%$) has argmin stability tracking the batching axis exactly as Corollary M5.2 predicts. **M4 and M5 share the same applicability domain** (operationally active batching) — the Bound-and-Gap framework is prospective precisely where the Hedge Rule is sharp.

**(C3) Insights — three findings.** (i) $H_{\mathrm{up}}$ varies ten-fold with elevator-bottleneck relief and, **within M5's applicability domain, prospectively classifies all 6 cells** on whether destination-clustered batching will beat FIFO. (ii) $\mathbb{P}[M_2 \ge M_1] = 99.4 \%$ across $c \in \{2, 3, 4, 5\}$; the Hedge Rule generalises beyond the $c=2$ case it was derived for. (iii) A **tactical-operational substitutability map**: non-substitutability concentrates in the elevator-lever-dominated, tight-wave regime and decays along both the capacity-slack and wave-looseness axes.

The remainder of the paper develops C1 (§4), C2 (§5), and C3 (§6), discusses managerial implications (§7), states limitations (§8), and concludes (§9).
