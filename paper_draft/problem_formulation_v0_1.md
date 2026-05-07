---
title: "Wave Release Coordination under Vertical Resource Constraints in Multi-Story AMR Warehouses"
section: "§3. Problem Formulation prose draft v0.2"
date: 2026-05-07
status: "MILP-style structured formulation: separate blocks for Sets, Parameters, Decision Variable, Structured-feature representation, Elevator models, Objective, Constraints"
---

# §3. Problem Formulation *(target ~750 words; current ≈ 870)*

We consider a multi-story warehouse where floor-bound AMRs share a small number of freight elevators across floors. Orders arrive over time, each with a known source floor and destination floor. A *wave* is a subset of orders released into the system simultaneously at the start of a release window. The system performance metric is the wave makespan, the time at which the last order in the wave is delivered, given a fixed operational dispatch policy.

This setting decomposes naturally into two coupled decision layers. The *tactical* layer chooses which orders to bundle into a wave $W$, namely the wave composition decision. The *operational* layer determines, given $W$, which AMR picks which order and which AMRs ride which elevator together. We focus the analytical effort on the tactical layer and treat the operational layer through a fixed dispatch policy (capacity-bounded FIFO boarding; full simulator details appear in §5). The two layers are coupled through the makespan: a wave whose composition is structured to ease the downstream dispatch yields a smaller makespan than an unstructured wave of the same size.

**Sets and indexes.**
- $\mathcal{O}$: set of all orders, indexed by $o$
- $\mathcal{F} = \{1, 2, \ldots, F\}$: set of floors, indexed by $f$
- $\mathcal{A}$: AMR fleet, indexed by $a$
- $\mathcal{E}$: set of elevators, indexed by $e$
- $\mathcal{M} = \{M_1, M_2, M_3\}$: elevator-model set, indexed by $m$

**Parameters.**
- $F \in \mathbb{Z}_{\geq 2}$: number of floors
- $|\mathcal{A}|$: AMR fleet size
- $E$: number of elevators
- $c \in \mathbb{Z}_{\geq 1}$: per-trip elevator capacity
- $s_o \in \mathcal{F}$: source floor of order $o$
- $d_o \in \mathcal{F}, d_o \neq s_o$: destination floor of order $o$
- $r_o \in \mathbb{R}_{\geq 0}$: release time of order $o$
- $W_{\min}, W_{\max} \in \mathbb{Z}_{\geq 1}$: lower and upper bounds on wave cardinality
- $\tau_w \in \mathbb{R}_{\geq 0}$: start time of release window for wave $w$
- $\Delta \in \mathbb{R}_{> 0}$: length of release window
- $\sigma_{M_3} \in \{0.10, 0.20\}$: lognormal noise scale under stochastic model $M_3$

**Decision variable.** The tactical decision variable is the wave composition $W \subseteq \mathcal{O}$, the subset of orders released together within the current wave window. An equivalent binary representation is $x_o \in \{0, 1\}$ with $x_o = 1$ iff $o \in W$.

**Structured-feature representation.** Rather than working in the raw $|\mathcal{O}|$-dimensional decision space, we summarize each candidate wave by a three-dimensional fingerprint $\Phi(W) = (C(W), I(W), T(W))$:
- *Vertical concentration* $C(W) = 1 - H_{\text{dst}}(W) / \log_2 F$, where $H_{\text{dst}}(W)$ is the Shannon entropy of the destination-floor distribution within the wave; high $C$ means orders share few destination floors.
- *Directional imbalance* $I(W) = \big| |W^{\uparrow}| - |W^{\downarrow}| \big| / |W|$, where $W^{\uparrow}$ and $W^{\downarrow}$ are the up- and down-going subsets; high $I$ means the wave is dominated by a single direction.
- *Temporal clustering* $T(W) = \sigma_r(W) / \mu_r(W)$, the coefficient of variation of per-order release timestamps within the wave; high $T$ means orders arrive in tight bursts.

The three axes correspond to three orthogonal physical mechanisms (multi-floor spread, up-versus-down asymmetry, temporal bunching) by which wave composition affects vertical-resource stress. We treat $\Phi$ as a *conceptual* decomposition rather than a predictive surrogate: each axis carries a clear physical unit and operational meaning.

**Elevator models.** The dispatch policy is realized through a simulator under one of three elevator models:
- $M_1$ (*throughput aggregation*): each elevator is modeled as a server with a per-AMR throughput rate that absorbs batched-trip efficiency into a single multiplier.
- $M_2$ (*true co-occupancy batching*): at each elevator, the next $c$ AMRs in the queue board together and ride as a unit, with realistic per-trip capacity, dwell time, and direction handling.
- $M_3$ (*stochastic batching*): extends $M_2$ with lognormal noise on per-trip duration at scale $\sigma_{M_3}$, used in §5 for robustness sensitivity.

$M_1$ and $M_2$ are both well-attested in the warehouse OR literature; the *structural* disagreement between throughput aggregation and explicit co-occupancy is the methodological gap our Hedge Rule (§4) resolves.

**Objective function.** Minimize the expected wave makespan under the chosen elevator model:
$$
\min_{W \subseteq \mathcal{O}} \; \mathbb{E}\!\left[\mathcal{T}(W) \,\big|\, M\right], \tag{1}
$$
where $\mathcal{T}(W) := \max_{o \in W} t^{\text{deliver}}_o(W; M)$ is the wave makespan, $t^{\text{deliver}}_o(W; M)$ is the simulator-realized delivery time of order $o$ under model $M$, and the expectation is over operational stochasticity (AMR pickup times, elevator dwell times, and, under $M_3$, lognormal noise).

**Constraints.** The wave composition $W$ is subject to the constraints (2)–(6) below: (2)–(5) are tactical-layer feasibility conditions on $W$, while (6) is operational feasibility realized through the simulator under model $M$ rather than as a formal optimization constraint.

$$
\begin{gather}
W_{\min} \leq |W| \leq W_{\max}, \tag{2} \\
r_o \in [\tau_w, \tau_w + \Delta], \quad \forall o \in W, \tag{3} \\
\sum_{w} \mathbf{1}[o \in W_w] = 1, \quad \forall o \in \mathcal{O}, \tag{4} \\
x_o \in \{0, 1\}, \quad \forall o \in \mathcal{O}, \tag{5} \\
n_{\text{aboard}}(e, t) \leq c, \quad \forall e \in \mathcal{E}, \; \forall t. \tag{6}
\end{gather}
$$

Constraint (2) bounds wave cardinality between the warehouse's operating envelope: $W_{\min}$ prevents under-utilized release windows, and $W_{\max}$ respects picking-station throughput and elevator-queue saturation. Constraint (3) is temporal feasibility: each order's release time $r_o$ must lie inside the wave's release window of length $\Delta$. Constraint (4) requires the sequence of waves to partition $\mathcal{O}$, with no order skipped or double-served, where $W_w$ is the wave released at $\tau_w$ and $\mathbf{1}[\cdot]$ is the indicator function. Constraint (5) defines the binary inclusion indicator, equivalently $W = \{o \in \mathcal{O} : x_o = 1\}$. Constraint (6) caps the per-trip elevator load $n_{\text{aboard}}(e, t)$; the simulator additionally encodes three operational invariants not exposed as formal optimization constraints: single-order AMR carriage (one AMR carries at most one order at a time), source-before-destination floor sequencing (an AMR visits $s_o$ before $d_o$), and capacity-bounded FIFO queue discipline (AMRs board in arrival order, up to $c$). These invariants are realized through $\mathcal{T}(W)$'s simulator implementation.

Together, equation (1) subject to constraints (2)–(6) defines the *wave release coordination problem under vertical resource constraints*. Direct solution of this stochastic optimization is challenging on two counts: $\mathcal{T}(W)$ is simulator-realized under $M$ rather than closed-form in $W$, and the decision space (subsets of $\mathcal{O}$) is combinatorial in $|\mathcal{O}|$. §4 therefore develops two analytical tools that operate on the structured-feature representation $\Phi(W)$ instead: a Bound-and-Gap decomposition theorem that bounds the value of structured information under any fixed feature partition of $\Phi$ space, and a Model-Dominance Hedge Rule that resolves structural disagreement among $\{M_1, M_2, M_3\}$ via a closed-form decision. The four problem-defining elements identified in §1 and §2 (wave composition as decision variable, multi-story deployment, flexible AMR fleet, shared-elevator capacity coupling) are now jointly formalized within this two-stage scheduler.
