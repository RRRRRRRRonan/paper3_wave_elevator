---
title: "Section 4 — Methodology (draft v0.1)"
parent: "Wave Release Coordination under Vertical Resource Constraints"
date: 2026-05-20
status: "draft v0.1 — two tools, Option-B contribution structure; D1/D2 shipped as theorems"
basis: "methodology_v0_2.md scaffold; theorems_m4.md, theorems_m5.md (full proofs)"
numbering: "Table 1 is the §4 diagnostic table; §5 tables follow as Tables 2-4. §4 is figure-free."
note: "Φ and the elevator models M1/M2/M3 are defined in §3; the finite Φ-space partition is introduced in §4.1.1. §4 builds the two tools on §3's objects."
---

# Section 4 — Methodology

Section 3 cast wave release coordination as a stochastic optimization whose
objective `C_max(W; M)` is simulator-realized and whose decision space is
combinatorial. Rather than search that space directly, we develop two
analytical tools that operate on the structured representation `Φ(W)` and on a
finite partition of `Φ`-space. The first, a **Bound-and-Gap framework**,
decomposes the value of wave-structure information into two non-negative
components and rests on a decomposition theorem (§4.1). The second, a
**Model-Dominance Hedge Rule**, resolves uncertainty over the elevator model
into a single closed-form dispatch decision and rests on a minimax-collapse
theorem (§4.2). Each tool is stated as a theorem here and validated at
publication scale in Section 5; §4.3 states the predictions that link the two.

## 4.1 The Bound-and-Gap framework

### 4.1.1 Decomposing the value of wave-structure information

Fix a `(regime, model, size)` cell. Partition `Φ`-space by a finite scheme
`Q`; the working instance is the `2×2` quartile partition of the `(C, I)`
plane into four corners `Q = {HC·HI, HC·LI, LC·HI, LC·LI}`. Let `m_q` denote
the corner-conditional **median** makespan of waves drawn from corner `q`, and
`m_0` the median makespan of a wave drawn at random from the unpartitioned
pool. Two extreme corners — `q_max = argmax_q m_q` and `q_min = argmin_q m_q` —
bound what the partition can reveal; a third, `q_Φ`, is the corner a
Φ-informed policy selects from the sign pattern of an ordinary-least-squares
fit on the cell. Define the **oracle upper bound**, the **Φ-informed lower
bound**, and their **gap**:

> `UB = (m_q_max − m_q_min) / m_0`,  `LB = (m_0 − m_q_Φ) / m_0`,
> `GAP = UB − LB`.

**Proposition 1 (Bound-and-Gap decomposition).** *For any cell and any finite
partition `Q`,*

> `GAP = H_up + M_Φ`,  *where*  `H_up = (m_q_max − m_0)/m_0`  *and*
> `M_Φ = (m_q_Φ − m_q_min)/m_0`.

*Proof.* Substituting the definitions, `UB − LB = (m_q_max − m_q_min)/m_0 −
(m_0 − m_q_Φ)/m_0 = (m_q_max − m_0)/m_0 + (m_q_Φ − m_q_min)/m_0`. ∎

Because `m_q_max ≥ m_0` and `m_q_Φ ≥ m_q_min` by construction, **both
components are non-negative**: `GAP ≥ 0`, and it is strictly positive whenever
the partition is non-degenerate. The two components have distinct readings.
`H_up` is the *partition-intrinsic upper-tail headroom* — the relative makespan
penalty of the worst corner, structural and present even when `Φ` selects
perfectly. `M_Φ` is the *Φ-policy miss* — the relative cost of `Φ` choosing
its corner rather than the oracle-best one, a residual that better feature
engineering can recover (Figure 1).

### 4.1.2 The policy component is an SPO regret

The policy component admits a second reading that places the framework inside
the predict-then-optimize literature. Treat "which corner to release a wave
from" as a decision over `Q`; the true cost vector is `(m_q)_{q∈Q}` and the
oracle solves `argmin_q m_q`. A *partition-constant predictor* is any cost
vector that is constant on each corner — the natural predictor class on a
finite partition — and its Smart-Predict-then-Optimize (SPO) loss is the
realized-minus-oracle cost of the corner it induces.

**Theorem 1 (D1 — SPO-regret equivalence).** *The policy component `M_Φ`
equals the SPO regret of the Φ-induced partition-constant predictor, namely
`(m_q_Φ − m_q_min)/m_0`.*

*Proof sketch.* The Φ-informed predictor induces the decision `q_Φ`; its SPO
loss against the true cost vector is `m_q_Φ − m_q_min`; normalizing by `m_0`
gives `M_Φ` directly (full statement and proof in Appendix). ∎

Theorem 1 positions the Bound-and-Gap framework as the *partition perspective*
on SPO: where the prediction-to-decision regret literature bounds an
algorithm's loss at training time, `M_Φ` is a post-hoc information-value gap on
a fixed partition. The cell-median is used throughout for consistency with this
equivalence, which is stated for the median.

### 4.1.3 Reading the decomposition

Because `H_up` and `M_Φ` are non-negative and independently interpretable,
their pair is a structural reading of where a cell's wave-design value sits.
Table 1 maps the four regions of `(H_up, M_Φ)` to an interpretation.

**Table 1. Reading the Bound-and-Gap decomposition.**

| `H_up` | `M_Φ` | Interpretation |
|---|---|---|
| large | small | Φ already near-optimal; the residual is structural — elevator-side capacity is the lever |
| small | large | corners are flat and Φ is miscalibrated — feature engineering is the lever |
| large | large | high partition contrast and Φ misses it — feature expansion is the priority |
| small | small | the partition gives little leverage — wave design is not the lever here |

**Corollary 1 (refinement monotonicity).** *If a partition `Q'` refines `Q`,
then `H_up(Q') ≥ H_up(Q)`* — refinement can only raise the worst-corner
median. The policy component `M_Φ` carries no such guarantee. Table 1 is a
reading of the *components*, not a predictor of which regime a given operating
policy will favour; Section 5 shows the realized value of structured design to
be broad rather than sharply regime-specific.

**Figure 1.** The Bound-and-Gap decomposition on a stylized
`(regime, model, size)` sub-cell. The four corner medians
(`m_{q_min}`, `m_{q_Φ}`, `m_0`, `m_{q_max}`) tile the oracle spread `UB` into
three contiguous segments — `M_Φ`, `LB`, `H_up` — and the gap is the sum of
the two outside tiles: `GAP = M_Φ + H_up = UB − LB`. *(Source:
`prototype/results/figures/fig_bound_and_gap_schematic.png`; generator
`prototype/src/figure_methodology_schematics.py`.)*

## 4.2 The Model-Dominance Hedge Rule

### 4.2.1 Model uncertainty and the minimax corner

The elevator model is exogenous to wave composition (§3, Assumption A5), but an
operator may not know which model `M ∈ {M1, M2, M3}` describes their
warehouse. The conservative response is the **minimax wave-corner selection**

> `c* = argmin_{c∈Q} max_{M∈ℳ} s[ C_max(W; M) | W ∈ c ]`,

where `s` is any monotone summary statistic of the makespan distribution
(median, mean, or any quantile). Evaluated naively, `c*` requires the operator
to identify the true model online. The Hedge Rule removes that requirement by
exploiting a structural relation among the models.

The load-bearing condition is **chain dominance**: for every wave `W`,
`C_max(W; M1) ≤ C_max(W; M2)` almost surely — throughput aggregation never
over-states makespan relative to true co-occupancy batching — with `M3` the
stochastic extension of `M2`. The condition is an empirical claim about the
model family, verified in Section 5.

### 4.2.2 Collapse under chain dominance and its DRO equivalence

**Theorem 2 (D2 — minimax collapse and DRO equivalence).** *Under chain
dominance, the minimax corner collapses to the corner optimal for the
dominant model,*

> `c* = argmin_{c∈Q} s[ C_max(W; M2) | W ∈ c ]`,

*and this corner coincides with the solution of the Wasserstein
distributionally-robust problem whose ambiguity ball, centred at the
nominal model and sized to the model-discrepancy radius, contains the family.*

*Proof sketch.* Monotonicity of `s` carries the per-wave dominance to the
conditional statistics, so `max_M s[·|c] = s[C_max(·; M2)|c]` for every
corner, and the outer `argmin` reduces accordingly. For the second clause, the
Wasserstein-1 distance between the nominal and dominant models equals their
mean gap exactly under dominance, so the worst case over the ambiguity ball is
attained at the dominant model; the two `argmin`s therefore agree (full proof
in Appendix). ∎

Theorem 2 yields a **closed-form dispatch policy** (Figure 2): release waves
from the corner that is optimal under the true-batching model `M2` — no
online model identification, and no distributionally-robust optimization to
solve. Where robust scheduling hedges over a parameter within one model class,
this rule hedges across *structurally distinct* model classes by exploiting a
verified dominance.

**Figure 2.** The Model-Dominance Hedge Rule. (a) Chain dominance of `M2`
over `M1` in cumulative-distribution terms: `F_{M_1}(t) ≥ F_{M_2}(t)`
pointwise, so `M2` is stochastically larger and the worst case in the
Wasserstein-1 ball `B_ρ(M1)` of radius `ρ = W₁(M1, M2)` is attained at `M2`
(Theorem 2's DRO clause). (b) The closed-form decision flow: verify chain
dominance empirically, then follow the `M2`-optimal corner; no online model
identification is required. *(Source:
`prototype/results/figures/fig_hedge_rule_schematic.png`; generator
`prototype/src/figure_methodology_schematics.py`.)*

### 4.2.3 Approximate dominance and the worst-case bound

Exact almost-sure dominance is a strong assumption; the stochastic model `M3`
satisfies it only approximately. **Corollary 2 (one-sided ε-bound)** weakens
the hypothesis to `P[ C_max(W;M2) ≥ C_max(W;M1) ] ≥ 1 − ε`. Then the
per-corner median gap is bounded by a one-sided quantity
`U_c(ε) = F₂⁻¹(½ + ε) − F₂⁻¹(½)`, computable from the makespan quantiles
alone, and the collapse of Theorem 2 remains exact whenever the inter-corner
gaps in the dominant-model ranking exceed `max_c U_c(ε)`. The worst-case loss
from following the rule when the operator's model is in fact mis-specified is
thus bounded by a quantity the operator can evaluate from their own data.

## 4.3 From tools to predictions

The two tools yield predictions that Section 5 tests at publication scale.
Proposition 1 and Theorem 1 predict that `GAP = H_up + M_Φ` and `M_Φ = ` SPO
regret hold *exactly* on every cell — a structural claim, not a statistical
one. Corollary 1 predicts `H_up` grows under partition refinement. Theorem 2
predicts the Wasserstein-DRO corner and the Hedge corner coincide whenever
chain dominance holds, and Corollary 2 predicts the regimes in which the
collapse is exact versus knife-edge. Section 5 evaluates each prediction
against a pre-registered acceptance gate.

---

*Full proofs:* `paper_draft/theorems_m4.md` (Proposition 1, Theorem 1,
Corollary 1) and `paper_draft/theorems_m5.md` (Theorem 2, Corollary 2);
numerical verification in `prototype/results/v0_2_D1_spo_equivalence.json`
and `v0_2_D2_wasserstein_dro.json`.
