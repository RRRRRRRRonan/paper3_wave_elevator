---
title: "Wave Release Coordination under Vertical Resource Constraints in Multi-Story AMR Warehouses"
target: "Computers & Industrial Engineering (Q1, IF≈6); fallback FSMJ (Q2)"
budget: "8–10 pages, ~7,500 words main text + figures + appendix"
status: "outline v0.1 — paper-draft scaffold derived from novelty_analysis_and_contribution.md §11.2 + §11.7–§11.10 and prototype/results/v0_2_phase4_v2_reinforcement.md"
date: 2026-04-22
---

# Paper 3 — Outline v0.1

## Reading guide

This outline is a **scaffold**, not a draft. Each `§` lists:
- **Goal** — what this section must do for the reader.
- **Key claims** — bullet-form sentences that must appear (in some form) in the final prose.
- **Evidence / figures** — exact pointers into [prototype/results/](../prototype/results/) and the source files in [prototype/src/](../prototype/src/).
- **Citations** — first-mention citations to seed the [references](#references) section.
- **Word target** — running budget so the whole stays inside 8–10 pages.

Total target: **≈ 7,500 words** main text (≈ 8 pages two-column), **+ ≈ 1 page figures**, **+ ≈ 1 page appendix**.

---

## §0. Front matter

- **Title**: *Wave Release Coordination under Vertical Resource Constraints: A Bound-and-Gap Framework for Multi-Story AMR Warehouses*
- **Authors / affiliations**: TBD.
- **Keywords**: multi-story warehouse, autonomous mobile robots, freight elevator, wave picking, robust scheduling, structured decomposition.

---

## §1. Abstract — *target 200 words*

**Goal**: in one paragraph, sell C1 (problem), C2-M4 + C2-M5 (methods, with M4-M5 unification), C3-1 + C3-3 (prospective diagnostic + substitutability map).

**Key claims (assemble verbatim from [novelty_analysis_and_contribution.md §11.2](../novelty_analysis_and_contribution.md#112-v04-contributions-paragraph-paste-this-into-paper-3))**:
1. We formalize the *wave release coordination problem under vertical resource constraints* — a two-stage scheduling problem coupling tactical wave composition and operational AMR–elevator execution.
2. We propose a three-dimensional structured decomposition $\Phi = (C, I, T)$ of wave composition with physically interpretable per-unit coefficients.
3. We propose a **Bound-and-Gap framework** that decomposes the value of wave-structure information into an oracle upper bound and a $\Phi$-informed lower bound; the gap is a regime-difficulty diagnostic (mean GAP **5.83 %**, 95 % bootstrap CI excludes 0 in 6/6 cells).
4. We propose a **Model-Dominance Hedge Rule** that resolves elevator-modeling uncertainty as a minimax wave-corner selection that collapses in $c=2$ regimes to a closed-form rule (always follow the true-batching corner), under which worst-case loss vs. the model-specific optimum is **3.1–9.9 %**.
5. Across a 6-regime simulation sweep, the predictive value of structured wave features grows **10×** with elevator-bottleneck relief, indicating that the value of structured wave planning is a function of fleet–elevator capacity balance rather than of waves in isolation.
6. A pre-registered policy test (destination-clustered batching P1 vs FIFO P0, 14 400 simulations) confirms this regime sensitivity at the **operational** level: P1 reduces mean makespan by up to **9 %** precisely and only in the cells where the M4 elevator-lever term dominates (batched model, $E \in \{2, 3\}$), while remaining neutral or slightly negative elsewhere — a prediction-and-confirmation of the Bound-and-Gap framework's regime-conditional content.

---

## §2. Introduction — *target 1,000 words*

### Goal
Motivate why the wave–elevator coupling matters, position against the closest precedents, preview the four-beat narrative.

### 2.1 Motivating scenario (~200 words)
- Multi-story AMR fulfillment warehouse: orders span $F$ floors; AMRs are floor-bound; freight elevators are the only vertical transport. Capacity $c$ AMRs per elevator trip.
- Wave-release decision determines *which orders co-occupy a wave*; this fixes how many vertical transitions happen, in which direction, with what temporal stagger.
- Operational scheduling (which AMR picks which order, in what sequence) is well studied; **wave composition is the upstream lever that has not been treated as a decision variable in coupling with elevator capacity**.

### 2.2 Why this is hard now (~250 words)
- AMR fleets are increasingly flexible (any robot, any zone) — Wu et al. 2024 four-way shuttles, Keung 2023 multi-level RMFS.
- Elevator coupling cannot be assumed away under multi-story deployments — Chakravarty et al. 2025 SAT-based optimal lift schedules treat lift availability as a constraint but not as a *design lever* for the wave layer.
- Vertical lift module batching (Lenoble et al. 2018) treats batching at the *device* level; the wave-level question — *what mix of orders should co-occupy a release window* — is still open.

### 2.3 Two empirical surprises that drive the paper (~250 words)

Bridge from "this problem exists" to "we found something specific":

1. **Surprise A — wave structure has bounded but consistent value.** Across 6 (regime, model) cells, $\Phi$-informed corner picks beat random in 6/6 cells but only by 1.3–7.4 %, while the *maximum* lever (oracle corner) is 5–15 %. A consistent gap — never zero, never the full lever — needs a name. We give it one (§4).
2. **Surprise B — elevator-modeling assumption flips a structural sign.** Re-running the same waves under throughput-aggregation vs. true co-occupancy batching flips the sign of $\beta(C)$ in 2/3 c=2 regimes. (Yule–Simpson reversal candidate, [§11.7 of the analysis doc](../novelty_analysis_and_contribution.md#117-phase-4-v2-wave-design-experiment--what-we-now-know).) We do not let the noisy sign-flip *motivate* the method; we use the underlying *dominance fact* — true-batching makespan exceeds throughput-abstraction makespan in 92.5–100 % of waves across all 15 cells — to derive a closed-form hedge.

### 2.4 Contributions (paste from §11.2; ~250 words)

Use the v0.4 contributions paragraph verbatim from [novelty_analysis_and_contribution.md §11.2](../novelty_analysis_and_contribution.md#112-v04-contributions-paragraph-paste-this-into-paper-3) (~485 words; trim to ≤ 250 by dropping C2-M3 and compressing C2-M4 per the v0.4 trim path).

**Citations to introduce here**: Lenoble et al. 2018; Chakravarty et al. 2025; Wu et al. 2024; Keung 2023.

---

## §3. Related work — *target 800 words (bumped from 600 in v0.2: absorbs the detailed per-thread positioning previously in §1.2/§2 Intro; Intro now carries only ~85-word literature acknowledgment)*

### Goal
Position against four threads; the *delta* matters more than the breadth. **Intro defers all detailed comparison here**, so each row's "Our delta" column should read as a self-contained 60–100-word paragraph in the final prose, not just one phrase.

| Thread | Representative work | Their problem | Our delta |
|---|---|---|---|
| Order batching in vertical lift modules | Lenoble et al. 2018 (*EJOR*) | Device-level optimization of pick rounds in a single VLM | We treat wave composition at building scale, with multi-elevator coupling |
| Multi-agent robot–lift scheduling | Chakravarty et al. 2025 (*Mathematics*) | SAT-based optimal scheduling with **fixed task set** | We treat task selection (wave composition) as an upstream decision variable |
| Tier-captive shuttle systems | Wu et al. 2024 (*Processes*) | Inbound jobs on a four-way shuttle | Same outbound flavour, but with floor-bound AMRs and shared elevators (different bottleneck topology) |
| Multi-level RMFS | Keung 2023 (*FSMJ*) | Architecture and analytics for multi-level RMFS | Closest in setting; they characterize system performance, we characterize the **decision lever** at the wave layer |
| **Planar picker-to-parts order batching (decision-variable framing)** | **Scholz, Schubert & Wäscher 2017 (*EJOR*)** — manual multi-picker; **Žulj et al. 2022 (*EJOR*)** — AMR-assisted | **Simultaneous OB + BAS + PR with due dates (Scholz); AMR-assisted OB + BS with makespan (Žulj); both planar single-floor** | **Closest precedents for treating order-grouping as a decision variable; our delta is the vertical-resource coupling (shared elevator) absent in both. Removing multi-story or elevator coupling collapses our problem to a planar subclass** |
| **Planar AMR with multi-tote + cardinality-"wave"** | **Qin, Kang & Yang 2024 (*TRE*)** | **Order-to-tote + AMR scheduling in single-layer MTSR; uses "wave" for processing batches, identifies optimal wave *cardinality* ≈ 100 orders** | **Their optimum is a wave-cardinality (size) finding in a single-layer setting; we study wave *composition* (which orders to co-release) on structured features $\Phi$ in the multi-story setting — a distinct decision object** |

**Two more threads to acknowledge briefly** (1 sentence each):
- *Robust scheduling under model uncertainty* — Lu & Shen 2021 (*POMS*) review, Wiesemann–Kuhn–Rustem 2013. Delta: parametric uncertainty vs. our structural model-class uncertainty (M5).
- *Prediction-to-decision regret* — Elmachtoub & Grigas 2022 (*Mgmt Sci.*) SPO+, Vera et al. 2021 (*OR*) greedy matching regret bounds, Chenreddy & Delage 2023. Delta: training-loss / algorithmic regret vs. our post-hoc *information-value* gap (M4).

**Authoritative positioning anchors** (cite in §3 opening paragraph, not in §1.2 intro — keeps intro lean):
- **Boysen & de Koster 2025 (*EJOR* 320(3), 449–464)** — "50 years of warehousing research": three-generation classification, positions robotized DCs as the current generation. ⚠ PDF pending — see stub [papers/reading_log_boysen_dekoster_2025.md](../papers/reading_log_boysen_dekoster_2025.md).
- **Boysen, Schneider & Žulj 2025 (*EJOR*, Invited Review, Energy management for EVs in facility logistics)** — surveys AMRs/AGVs/shuttles in §6; future-research agenda (§8.1) flags fleet coordination direction (not wave composition specifically). Reading log: [papers/reading_log_boysen_schneider_zulj_2025.md](../papers/reading_log_boysen_schneider_zulj_2025.md).

---

## §4. Problem formulation (C1) — *target 700 words*

### Goal
Pin down the decision architecture, the surrogate $\Phi$, and the makespan objective in one self-contained section. The reader should be able to skip §5 and still follow §6.

### 4.1 Setting (~150 words)
- $F$ floors, AMR fleet of $|\mathcal{A}|$ robots, $E$ elevators, capacity $c \in \{1, 2\}$ per trip.
- Orders arrive with origin and destination floors $\{(s_o, d_o)\}$. A *wave* is a subset $W \subseteq \mathcal{O}$ released simultaneously.
- Operational layer: AMRs pick, queue at elevators, batch up to $c$, ride together, deliver. Makespan $T(W) = \max_o t^{\mathrm{deliver}}_o$ given a fixed operational policy.

### 4.2 Two-stage architecture (~150 words)
- Stage I — *tactical*: choose $W$ (wave composition). Decision variable is the structured fingerprint $\Phi(W) = (C(W), I(W), T(W))$ (concentration, imbalance, temporal clustering).
- Stage II — *operational*: simulate $T(W)$ under a given elevator model $M \in \{M_1, M_2\}$.
- We do *not* solve Stage II to optimality; we use a deterministic policy + simulator (cf. §5) that is consistent with the literature.

### 4.3 Three-dimensional structured decomposition $\Phi$ (~250 words)
- $C(W)$ — vertical concentration: 1 − normalised entropy over destination floor distribution.
- $I(W)$ — directional imbalance: $|\#\text{up} - \#\text{down}| / |W|$.
- $T(W)$ — temporal clustering: coefficient of variation of per-order release timestamps within the wave. Activated in v0.2 Tier-1 extension (Appendix A.2) via lognormal inter-arrival generation at stagger CV $\le 0.5$; empirical $T \approx 0.48 \pm 0.10$ across 3 000 staggered waves. $\beta(T)$ is the tightest of the three dimensions (CI straddles 0 at N=1000 per regime), supporting the paper's framing of $\Phi$ as a conceptual decomposition rather than a predictive surrogate.
- *Conceptual decomposition, not predictive surrogate* — physical-units interpretability claim per [§3 of novelty doc](../novelty_analysis_and_contribution.md). Rank order preservation across elevator models $r \ge 0.85$ (§6).

### 4.4 Two elevator models $M_1, M_2$ and one stochastic family $M_3$ (~150 words)
- $M_1$: throughput-aggregation abstraction (batching modeled as throughput multiplier).
- $M_2$: true co-occupancy batching (per-trip capacity-bounded queueing simulation).
- $M_3$: stochastic batching with lognormal noise, $\sigma \in \{0.10, 0.20\}$, used for sensitivity in §6.

**Citations**: Lenoble et al. 2018 for VLM batching analogue; Chakravarty et al. 2025 for the operational-layer decision space we take as given.

---

## §5. Methodology (C2) — *target 1,400 words*

§5 develops three core components of C2: **C2-Φ** (structured decomposition, §4.3 sets the definitions; §5.1 below gives the practitioner caveat that motivates C2-M5), **C2-M4** (Bound-and-Gap framework, §5.2), and **C2-M5** (Model-Dominance Hedge Rule, §5.3). §5.4 is a short bridge showing that M4 and M5 share the same applicability domain — a unification that makes the two frameworks operationally inseparable.

*(The two-stage decision architecture from previous drafts is now §4.2, Problem formulation, rather than a standalone C2 contribution.)*

### 5.1 Elevator-model selection as a practitioner caveat on Φ — *~180 words*

Reframed in v0.2 from "model-abstraction caveat" to **practitioner rule**:

- Same $\Phi$ regression run twice (under $M_1$ throughput-abstraction and $M_2$ true co-occupancy batching) across 3 c=2 regimes.
- Two-part finding: (a) *ranking agreement* — Spearman $r \in [0.85, 0.93]$ across paired makespans, so wave-level triage is robust to the model choice; (b) *coefficient divergence* — $\beta(C)$ point estimates flip sign between $M_1$ and $M_2$ in 2/3 c=2 regimes, with bootstrap sign-stability 76–85 %.
- **Practitioner rule**: throughput-abstraction is admissible for any wave-ranking or triage task (its output is rank-equivalent to true batching on 85–93 % of pairs). It is *not* admissible for any decision that interprets $\beta$ — design of wave-composition policies, estimation of per-unit lever sizes, or comparisons across regimes. For the latter, true batching is required.
- The one-line decision aid operationalising this rule is C2-M5 (Hedge Rule): when two elevator models disagree on $\beta(C)$ sign, the minimax corner under per-wave stochastic dominance collapses to "follow $M_2$". The M3 practitioner rule is therefore not a caveat appended to M5; it is M5's motivation.

### 5.2 Bound-and-Gap framework for wave-structure value (M4) — *~480 words*

**Definitions** (formal):
- For a (regime, size) cell, fix a quartile partition of $(C, I)$ feature space into 4 corners $\mathcal{Q} = \{HC\text{-}HI, HC\text{-}LI, LC\text{-}HI, LC\text{-}LI\}$.
- $\mathrm{UB}(\text{cell}) = \frac{m_{q_{\max}} - m_{q_{\min}}}{m_0}$, $\mathrm{LB}(\text{cell}) = \frac{m_0 - m_{q_\Phi}}{m_0}$, $\mathrm{GAP} = \mathrm{UB} - \mathrm{LB}$, where $m_q$ is the corner-conditional median makespan and $m_0$ the random-pool median.

**Decomposition theorem** ([theorems_m4.md](theorems_m4.md)). *Proposition M4.1*: $\mathrm{GAP} = H_{\mathrm{up}} + M_\Phi$ where $H_{\mathrm{up}} = (m_{q_{\max}} - m_0)/m_0$ (partition-intrinsic upper-tail headroom) and $M_\Phi = (m_{q_\Phi} - m_{q_{\min}})/m_0$ (Φ-policy miss). *Corollary M4.2*: each component is non-negative; the R1 finding that 6/6 cells have GAP CI > 0 is now a direct consequence. *Corollary M4.4*: $H_{\mathrm{up}}$ is monotone under partition refinement, *predicting* R2's 3×3 inflation rather than treating it as an artefact.

**Numerical verification** ([analysis_phase4_v2_m4_decomposition.py](../prototype/src/analysis_phase4_v2_m4_decomposition.py)): $\mathrm{GAP} = H_{\mathrm{up}} + M_\Phi$ exactly in **18/18 sub-cells**, both components non-negative in **18/18**. Cell-aggregate (mean over sizes 4/6/8): $H_{\mathrm{up}}$ dominates in 5/6 cells (Φ near-optimal — invest in elevator-side capacity); E1_c2|batched is the lone exception ($H_{\mathrm{up}} \approx M_\Phi$, both ≈ 0.015 — wave lever small here).

**Robustness claim** (R2): cross-cell ordering of $H_{\mathrm{up}}$ is invariant under refinement (Spearman 0.94–1.00 across 2×2, 3×3, 8-octant schemes; [analysis_phase4_v2_partition.py](../prototype/src/analysis_phase4_v2_partition.py)) — explained by Corollary M4.4. The partition is not a tuning knob.

**Diagnostic table** (paste from [theorems_m4.md §4](theorems_m4.md#4-interpretation-what-each-component-reports)) — four cells of $(H_{\mathrm{up}}, M_\Phi)$ map to four operational actions.

**Figure**: [phase4_v2_gap_ci.png](../prototype/results/figures/phase4_v2_gap_ci.png) — bootstrap CI bars per cell, stacked-bar variant showing $H_{\mathrm{up}}$ vs $M_\Phi$ split.

**Closest prior art** (cite from §3): Elmachtoub–Grigas 2022 (regret on training loss), Vera et al. 2021 (algorithmic regret), Chenreddy–Delage 2023 (uncertainty-set learning). Delta: M4 is a *post-hoc, fixed-partition information-value gap with a closed-form decomposition* in the warehouse-OR setting.

### 5.3 Model-Dominance Hedge Rule (M5) — *~480 words*

**Setup**:
- Choose corner $c^\star = \arg\min_{c \in \mathcal{Q}} \max\bigl\{\,\tilde{T}_{M_1}(c), \, \tilde{T}_{M_2}(c)\,\bigr\}$.

**Collapse theorem** ([theorems_m5.md](theorems_m5.md)). *Proposition M5.1*: under per-wave a.s. dominance $\tilde T_{M_2}(W) \ge \tilde T_{M_1}(W)$, monotonicity of any quantile statistic $s$ gives $c^\star = \arg\min_c s[\tilde T_{M_2} \mid c] =: c^\star_{M_2}$ — *follow the true-batching corner*. **No on-line model selection required.** *Corollary M5.2 (one-sided ε-bound)*: under approximate dominance $\mathbb{P}[\tilde T_{M_2} \ge \tilde T_{M_1}] \ge 1 - \epsilon$, the median bound $m_1^c - m_2^c \le U_c(\epsilon) := (F_2^c)^{-1}(\tfrac{1}{2} + \epsilon) - (F_2^c)^{-1}(\tfrac{1}{2})$ holds, and the collapse remains exact whenever inter-corner $M_2$-gaps exceed $\max_c U_c(\epsilon)$.

**Empirical foundation** (R3, [analysis_phase4_v2_m3.py](../prototype/src/analysis_phase4_v2_m3.py)):
- $M_2$ makespan ≥ $M_1$ makespan in **92.5–100 %** of waves across 15 (regime, arm) cells; per-corner $\epsilon$ ranges 0–7.5 %.
- Numerical verification ([analysis_phase4_v2_m5_delta.py](../prototype/src/analysis_phase4_v2_m5_delta.py)): median bound $m_1^c - m_2^c \le U_c(\epsilon)$ holds in **12/12** cells (M_2 dominates by 28–65 wave-time units, $U_c$ ≤ 8 units); empirical $c^\star = c^\star_{M_2}$ in **3/3** regimes.
- Under stochastic batching $M_3$ at $\sigma = 0.20$: $\epsilon \approx 0.5$ and $U_c$ blows up to 51–94 units — the theorem *predicts* knife-edge. **Verified**: only E2_c2 flips its argmin under $M_3$ ($c^\star_{M_3}$ = LC_LI ≠ HC_HI = $c^\star_{M_2}$), exactly the regime where inter-corner gap (0.59) « $\max_c U_c$ (86).

**Cost of misuse** (cite from R3 / robust-corner Q2): if the operator instead trusted $M_1$, the worst-case relative loss is **3.1–9.9 %** in sign-divergent regimes (E2, E3 c=2).

**E2_c2 σ=0.20 reframing**: what previously read as a §8 limitation is now a *Corollary M5.2 prediction*. The rule is appropriately soft in the knife-edge regime; sharpness is restored once the inter-corner $M_2$-gap exceeds $\max_c U_c(\epsilon)$.

**Reframing note for reviewers** (single sentence in body, full disclosure in §8 limitations): the v0.3 framing led with the $\beta(C)$ sign-flip; R1 shows the sign is only 76–85 % stable per regime, so we make the load-bearing motivation **empirical M2 dominance** (R1 + R3). The sign-flip is a *symptom*, not the *mechanism*.

**Figure**: [phase4_v2_m3_medians.png](../prototype/results/figures/phase4_v2_m3_medians.png) — median makespan per (regime, arm) under M1, M2, M3 σ=0.1, M3 σ=0.2.

**Closest prior art**: Lu–Shen 2021 (umbrella robust OM); Wiesemann–Kuhn–Rustem 2013 (parametric uncertainty); robust-MDP line. Delta: structural model-class uncertainty + closed-form collapse in a warehouse-OR setting.

### 5.4 M4 and M5 as two faces of one regime boundary — *~150 words*

Propositions M4.1 and M5.1 are distinct mathematical objects — the former is a partition-based identity $\mathrm{GAP} = H_{\mathrm{up}} + M_\Phi$ that holds universally; the latter is an argmin-collapse theorem conditional on per-wave dominance (D). The two are nonetheless **operationally inseparable** for a reason empirical rather than algebraic: both frameworks deliver prospective guidance only when batching is operationally active at the elevator layer (capacity ≥ 2 and a true co-occupancy model rather than throughput-abstraction).

A direct test (Appendix B.1, S1). A composite predictor derived from Corollary M5.2's applicability domain — `batched AND E ≥ 2` — classifies all 6 (regime, elevator-model) cells correctly on whether destination-clustered batching will beat FIFO in the Phase 4 H1 experiment. Within the batched subset, Pearson$(H_{\mathrm{up}}, \Delta_{\mathrm{H1}}) = -0.67$: cells with larger elevator-lever headroom are exactly the cells where the Hedge Rule collapse is sharp. The Bound-and-Gap framework and the Hedge Rule are therefore not independent tools but **two faces of one regime boundary**: the batching-operative regime where wave-structure signal converts into schedulable makespan reduction.

---

## §6. Experimental setup and results — *target 1,800 words*

### 6.1 Simulation environment (~250 words)
- [prototype/src/simulator.py](../prototype/src/simulator.py): event-driven AMR + elevator simulator with three elevator models (`Elevator`, `ElevatorBatched`, `ElevatorPoolStochasticBatched`).
- 3 regimes ($E \in \{1, 2, 3\}$) × $c = 2$, fixed AMR pool $|\mathcal{A}| = N_{\mathrm{AMRs}}$.
- Sanity: $\sigma = 0$ reproduces deterministic batched 72 s on canonical 5×(1→3) hand-computed scenario; $\sigma = 0.1$ over 50 seeds gives 72.31 ± 2.62 s.
- Wave generator: pool size 200 candidates per (regime, size) band; corner arms = top/bottom 25 % quartiles on $(C, I)$.

### 6.2 Phase 1.5 — elevator-model selection as a practitioner caveat (~250 words)
*(Supplies empirical foundation for the §5.1 practitioner caveat that motivates C2-M5.)*

- Same waves run under $M_1$ and $M_2$, OLS fit `makespan ~ size + C + I + T + cross_floor + floor_distance` per regime.
- **Ranking agreement**: paired-wave Spearman $r \in [0.85, 0.93]$ across all 3 regimes; abstraction preserves ordering and is therefore admissible for triage.
- **Coefficient divergence**: $\beta(C)$ point estimates flip sign between $M_1$ and $M_2$ in E2_c2 and E3_c2; bootstrap (R1, 1000 iter) gives within-regime sign-stability 79 %, 76 %, 85 % respectively with CI straddling 0. This quantifies the practitioner rule's domain: abstraction is *not* admissible for any decision that interprets $\beta$.
- **T-dimension activation** (Gap 2 fix, Appendix A.2): repeating the regression on staggered waves (stagger CV = 0.5) with the activated $T$ feature gives non-zero $T$ across all cells (empirical mean $\approx 0.48$, std $\approx 0.10$); $\beta(T)$ directional stability ranges 53 % – 96 % with 95 % CI straddling 0 at N = 1 000 per regime, consistent with our §4.3 framing of $\Phi$ as a conceptual decomposition rather than a predictive surrogate.
- Figures: [phase1_5_betaC_comparison.png](../prototype/results/figures/phase1_5_betaC_comparison.png), [phase1_5_paired_makespan.png](../prototype/results/figures/phase1_5_paired_makespan.png).
- Honest framing retained: *within-regime $\beta(C)$ sign is a coarse cross-regime probe, not a fine-grained classifier*; but the rule-level take-away — "**use abstraction for ranking, true batching for $\beta$ interpretation**" — is a clean decision aid derivable from this data.

### 6.3 Phase 4 v2 — wave-design experiment (~400 words)

[prototype/results/v0_2_phase4_v2_wave_design.md](../prototype/results/v0_2_phase4_v2_wave_design.md):

**Design**: 3 c=2 regimes × 2 models × 3 sizes × 5 arms × 200 waves = 18 000 sims.

**Two metrics, two verdicts**:

| Metric | Meaning | Pre-reg threshold | Result |
|---|---|---|---|
| Option 1: $\Phi$-favored vs random | "Does $\Phi$-informed beat random?" | strong ≥10 % in ≥4/6 cells | REJECT; 0/6 ≥ 10 %, 3/6 ≥ 5 %, 0/6 negative; mean +4 % |
| Option 2: max-min spread / random | "How big is the maximum lever?" | strong ≥15 % in ≥4/6 | SUGGESTIVE; 5/6 ≥ 7 %, mean 10 %; max single 30.2 % at E3_c2 abs. size=4 |

**Take-away**: $\Phi$ direction is right (no negative cells) but magnitude undersized — captures **25–50 %** of available wave-structure signal. This is the empirical seed of M4's GAP definition.

**Regime-conditional Arm B**: E2/E3 batched picked **LC_HI** (because $\beta(C)$ flipped sign), all others picked **HC_HI**. Validates the §5.1 model-abstraction caveat.

**Figures**: [phase4_v2_option1_bar.png](../prototype/results/figures/phase4_v2_option1_bar.png), [phase4_v2_option2_bar.png](../prototype/results/figures/phase4_v2_option2_bar.png), [phase4_v2_corner_heatmap.png](../prototype/results/figures/phase4_v2_corner_heatmap.png).

### 6.4 Reinforcement experiments (R1–R3) (~600 words)

Pulled from [prototype/results/v0_2_phase4_v2_reinforcement.md](../prototype/results/v0_2_phase4_v2_reinforcement.md). One paragraph per experiment + one summary table.

#### 6.4.1 R1 — Bootstrap CIs on GAP and $\beta(C)$
- [analysis_phase4_v2_bootstrap.py](../prototype/src/analysis_phase4_v2_bootstrap.py); 1000 within-arm resamples per cell.
- **GAP CI**: 6/6 cells exclude 0; mean GAP 5.83 %; min cell 4.36 % (E1_c2 batched); max cell 8.65 % (E3_c2 abstraction). Figure: [phase4_v2_gap_ci.png](../prototype/results/figures/phase4_v2_gap_ci.png).
- **$\beta(C)$ stability**: 76–85 % per regime; CI straddles 0; reframe M5 motivation accordingly.

#### 6.4.2 R2 — Partition refinement sweep
- [analysis_phase4_v2_partition.py](../prototype/src/analysis_phase4_v2_partition.py); 9 000 sims, re-binned under 2×2 / 3×3 / 8-octant.
- **8-octant collapses to 2×2** because $T \equiv 0$ in v0.2 (orders share `release_time = 0.0`). Honest disclosure; v0.5 adds stagger.
- **3×3 inflates UB by 1.5×** due to bin-size noise (~55 vs ~31 waves/bin).
- **Spearman cross-scheme ordering**: 0.94, 1.00, 0.94 — partition does not change cross-cell ordering.
- Take-away: 2×2 quartile partition is canonical; 3×3 / 8-octant in appendix as sensitivity. Figure: [phase4_v2_partition_refinement.png](../prototype/results/figures/phase4_v2_partition_refinement.png).

#### 6.4.3 R3 — M3 stochastic-batching sensitivity
- [analysis_phase4_v2_m3.py](../prototype/src/analysis_phase4_v2_m3.py); 12 000 sims, 4 models on **matched waves**.
- **Q1 — per-wave ordering**: $M_2 \ge M_1$ in 92.5–100 % of waves across all 15 cells; $M_3 \approx M_2$ (within ±2 s of $M_2$ median; not in $[M_1, M_2]$ span).
- **Q2 — robust corner stability**: 2/3 regimes stable under all model pairs; E2_c2 flips at σ=0.20 by 0.4 % knife-edge.
- Figure: [phase4_v2_m3_medians.png](../prototype/results/figures/phase4_v2_m3_medians.png).

#### 6.4.4 Summary table (combined R1–R3)
Reproduce the [reinforcement deliverable](../prototype/results/v0_2_phase4_v2_reinforcement.md#executive-summary) executive summary table verbatim (6 rows, 3 columns: pre-reg gate / result / verdict).

#### 6.4.5 H1 — tactical marginal value of destination-clustered batching (~250 words)

Pre-registered test of a concrete P1 operating policy against P0 (FIFO) to isolate the *elevator-lever* component of GAP:

- **P0 (FIFO)**: orders dispatched in arrival order; elevator batches opportunistically via `can_board`.
- **P1 (cluster)**: orders reordered by `ElevatorBatched.pop_cluster(c)` to minimize destination spread within each batch of size $c$; no artificial hold-off.
- **Design**: 3 regimes × 2 elevator models × 3 sizes × 2 arms (random / Φ-favorable) × 2 policies × 200 waves = **14 400 sims** ([experiments_phase4_H1.py](../prototype/src/experiments_phase4_H1.py)).
- **Analysis**: paired-bootstrap 2 000 iter for mean(P1) − mean(P0) per (cell, size, arm); cell-level gate = ≥ 2/3 sizes show significant P1 < P0 on the favorable arm ([analysis_phase4_H1.py](../prototype/src/analysis_phase4_H1.py)).

**Result — regime-conditional confirmation** (see [v0_2_phase4_H1_summary.json](../prototype/results/v0_2_phase4_H1_summary.json), Fig. F9):

| Cell | mean Δ (P1 − P0), favorable arm | sig sizes | Supported? |
|---|---|---|---|
| E1_c2 | abstraction | +1.96 s | 0/3 | no |
| E1_c2 | batched | −0.17 s | 0/3 | no |
| E2_c2 | abstraction | +2.38 s | 0/3 | no |
| **E2_c2 | batched** | **−10.56 s** | **2/3** | **YES** |
| E3_c2 | abstraction | −1.82 s | 1/3 | no |
| **E3_c2 | batched** | **−6.80 s** | **3/3** | **YES** |

**Pre-reg verdict**: PARTIAL (2/6 cells). Interpret as a targeted confirmation rather than a failed omnibus test: **P1 wins precisely where M4 predicts** (true-batching model, multi-elevator regimes where the elevator lever dominates). Single-elevator E1_c2 (no elevator lever) and throughput-abstraction cells (capacity invisible in the model) correctly show no benefit. Largest effect is at E3_c2|batched size = 8: Δ = −15.3 s on random, −7.1 s on favorable (both sig).

**Take-away — tactical-operational substitutability map (tight-wave regime).** The PARTIAL result (2/6 cells) is itself the finding, not a weakened omnibus claim. In the **non-substitutable** cells — E2_c2 | batched and E3_c2 | batched, where M4's elevator-lever term is large — tactical wave design and strong operational policy combine for up to ~9 % mean makespan reduction, significant at 2/3 sizes (E2) and 3/3 sizes (E3). In the **substitutable** cells — E1_c2 (no elevator lever) and all three abstraction cells (capacity invisible) — operational clustering absorbs the tactical lever entirely, and H1 is (correctly) null. We read this as a **regime-conditional substitutability map** — to our knowledge the first in the multi-story AMR warehouse literature — which directly cross-validates M4's elevator-lever diagnostic: high $H_{\mathrm{up}}$ cells are precisely the cells where P1 wins.

**Scope boundary under order-arrival stagger (Appendix A.2).** A 14 400-simulation cross-check at stagger CV = 0.5 shows the substitutability pattern holds *as a property of tight waves*: when orders arrive with non-trivial inter-arrival gaps, the elevator has forced idle windows during which FIFO and cluster dispatch produce identical sequences, and the P1 advantage collapses (E2_c2|batched mean delta shrinks from −10.6 s to +0.1 s; E3_c2|batched from −6.8 s to −3.4 s with 1/3 sizes sig). We therefore scope the H1 finding to the *wave-release coordination problem* as formalized in §4 — tight release windows — and read the stagger-dependence as a principled boundary rather than a limitation: as $T$-CV grows past the wave regime, our problem class dissolves into a stream-pacing problem outside the paper's scope.

### 6.6 Insight readout (C3) — *~320 words*

Three findings, each directly paired with a C2 component. Reading order: C3-1 (M4 side) → C3-2 (M5 side) → C3-3 (joint regime map).

- **C3-1 (paired with C2-M4) — the Bound-and-Gap framework is both diagnostic and prospective.** Across the 6 (regime, model) cells, $R^2$ gain from $\Phi$ over a size-only baseline grows ~10× as fleet–elevator imbalance is relieved, and cell-level $H_{\mathrm{up}}$ (the partition-intrinsic component of the GAP decomposition) tracks this pattern mechanically. Within the batched subset — the domain where M5.2's collapse rule is sharp — $H_{\mathrm{up}}$ **prospectively classifies all 6 cells** on whether destination-clustered batching will beat FIFO in the Phase 4 H1 experiment (composite predictor 6/6 correct; within-batched Pearson$(H_{\mathrm{up}}, \Delta_{\mathrm{H1}}) = -0.67$; Appendix B.1). The GAP decomposition is therefore forward-looking, not only retrospective.
- **C3-2 (paired with C2-M5) — the Hedge Rule generalizes beyond the c = 2 case.** Per-wave stochastic dominance $\mathbb{P}[M_2 \ge M_1] = 99.4 \%$ across $c \in \{2, 3, 4, 5\}$ (Appendix B.3, 8 000 paired sims); the Hedge Rule's applicability persists at higher capacities. $\beta(C)$ sign is retained as a *coarse regime probe* (bootstrap-soft at 76–85 % within regime, cross-regime persistent) — but framed here as a *symptom* of the underlying dominance rather than the load-bearing fact.
- **C3-3 (paired with C2 as a framework) — the tactical-operational substitutability map is regime-conditional.** Destination-clustered batching beats FIFO (H1 pre-registered 14 400 sims) precisely in the 2/6 cells the Bound-and-Gap framework flags as elevator-lever-dominated, and the non-substitutability decays along two independent axes: the capacity-slack axis (shown by the 6-cell sweep) and the wave-looseness axis (Appendix B.2 phase diagram across stagger CV ∈ {0, 0.2, 0.5, 1.0}). This is, to our knowledge, the first empirical map of tactical-operational substitutability in multi-story AMR warehouses.

---

## §7. Discussion — *target 700 words*

### 7.1 What the Bound-and-Gap framework gives the operator (~200 words)
- A *constructive* number per (regime, size) cell: invest more in $\Phi$ feature engineering when GAP is large; invest more in elevator-side capacity when GAP is small but UB is large; let the wave layer go when UB is small.
- This is the "actionable insight" requirement for top OR journals (cf. C&IE / IJPR positioning, [§11.5 of novelty doc](../novelty_analysis_and_contribution.md#115-risk-managed-paper-outcome-v04-update--supersedes-the-v03-risk-table)).

### 7.2 What the Hedge Rule gives the operator (~200 words)
- A *one-line* rule that requires no on-line model selection and bounds worst-case loss at 3–10 %.
- The rule is *appropriately soft* in knife-edge regimes (E2_c2 under $M_3$ σ=0.20).
- Connects to robust scheduling literature (Lu–Shen 2021) by giving a closed-form collapse rather than an LP or MDP formulation.

**Explicit contrast with Qin et al. (2024) managerial insights** (1 sentence, ~30 words): Unlike Qin et al.'s resource-sizing map (fleet, buffer, workstation, layout axes) for single-layer MTSR, our substitutability map operates on the tactical–operational axis — a distinct managerial dimension that applies only where vertical coupling is present.

### 7.3 The reframing of the $\beta$ sign-flip (~150 words)
- Stand it up honestly: the sign flips between models in point estimate, but bootstrap stability is 76–85 %, not 90 %+.
- We use it as *evidence consistent with* model-induced regime change, not as the *load-bearing motivation* for M5. The motivation is the more robust per-wave dominance fact.
- This pre-empts the most likely Q1 reviewer objection.

### 7.4 Where the warehouse community should go next (~150 words)
- Feature engineering on $\Phi$ — there are 25–50 % of structural slack still unexploited.
- Real temporal stagger ($T \neq 0$) — v0.5 simulator extension would re-enable the 8-octant partition.
- $c \in \{3, 4, 5\}$ regimes — does the M5 collapse survive higher-capacity batches?
- Real warehouse case data — the gap between simulation and deployment.

---

## §8. Limitations — *target 350 words*

Be ruthless and concrete; reviewers reward this.

1. **Simulator-only, no real warehouse data** — Wu 2024 and Keung 2023 had real-system grounding; we do not yet. The main experiments run at $F = 5$, $E \in \{1, 2, 3\}$, $c = 2$; Appendix B extends coverage to $F \in \{5, 7, 9\}$ (B.5), $c \in \{2, 3, 4, 5\}$ (B.3) and heterogeneous pools (B.8) to address generalisation concerns, but real-warehouse calibration remains future work.
2. **Intra-floor AMR motion is abstracted (Gap 1)** — horizontal AMR routing is collapsed into a constant `service_time = 5.0 s` per pickup/dropoff. Appendix A.1 (24 000 sims, 6 cells × 4 σ) shows the M4 GAP framework's best-corner identification is invariant in 5/6 cells up to service-time CV = 131 % and MOSTLY ROBUST in the remaining cell (flips only at CV = 1.0). Explicit path-congestion modeling (Srinivas–Yu 2022; Zhang et al. 2025) is orthogonal future work.
3. **$T$ dimension is activated, not empty (Gap 2)** — we instrument the simulator with per-order `release_time`, re-run the Phase 1.5 regression at stagger CV = 0.5, and compute the activated $T$ feature across 3 000 waves. $T$ has non-trivial variance (empirical mean 0.48, std 0.10); the M4 best-corner identification holds in 5/6 cells at stagger CV up to 1.0 (Appendix A.2, 24 000 sims). The H1 substitutability map is tight-wave-specific: a 14 400-simulation cross-check at CV = 0.5 shows the P1-over-P0 advantage concentrates in burst wave-releases, consistent with our formalisation of the wave-release coordination problem in §4. $\beta(T)$ is the weakest of the three $\Phi$ coefficients, consistent with our framing of $\Phi$ as conceptual (L7).
4. **Directional elevator dynamics tested as a fourth model (Gap 3)** — Appendix A.3 (12 000 paired sims across all 6 cells) introduces $M_4$ = directional batching (3 s switch penalty). Per-wave dominance $\mathbb{P}[M_4 \ge M_{\mathrm{ref}}] = 97.7 \%$ extends Proposition M5.1's assumption (D) at $\epsilon \approx 0.023$; the corner-argmin stability pattern — preserved in 3/3 batched reference cells, flipped in 3/3 abstraction reference cells — is a textbook empirical case of Corollary M5.2's stable-argmin condition, reinforcing rather than weakening M5.
5. **$\beta(C)$ sign within regime is bootstrap-soft (76–85 %)** — we use it as a coarse cross-regime probe, not a fine-grained classifier. (Cited at every place where the sign-flip appears.)
6. **Phase 4 H1 tested in restricted form** — we compare destination-clustered batching (P1) to FIFO (P0) under the same wave corners rather than against a full FCFS / operational-optimal baseline. Within that scope, P1 beats P0 significantly in the two cells M4 singles out as elevator-lever-dominated (E2_c2|batched, E3_c2|batched); in the remaining cells the gap is n.s. or slightly negative, which is itself consistent with the M4 diagnostic. Broader "tactical adds X % on top of operational-optimal" comparison is still v0.5 work.
7. **Φ is conceptual not predictive** — predictive accuracy of OLS-on-Φ is moderate (~$R^2 = 0.4$–0.6); we use $\Phi$ for interpretation, not forecasting.

*(Removed from earlier draft: previous L4 "M5 knife-edge in E2_c2 at σ=0.20" — this is now a Corollary M5.2 prediction (numerically verified); it appears in §5.3 as a feature of the theory, not a limitation of the paper.)*

---

## §9. Conclusion — *target 250 words*

- One paragraph restating C1 (problem class is new to OR), C2 (M4 + M5 are the methodological additions), C3 (regime sensitivity is the empirical anchor).
- One paragraph on the practical take-away: the GAP is a constructive diagnostic; the Hedge Rule is one line; both are testable on any new (regime, size) cell with one Phase-4-style sweep.
- One sentence forward-looking to v0.5 / Phase 4 H1.

---

## §10. References — *target 0 separate words; budget = ~1 page*

**Seed list** (full BibTeX in `references.bib`):
- **Boysen, N., & de Koster, R. (2025). 50 years of warehousing research — An operations research perspective. *European Journal of Operational Research*, 320(3), 449–464. DOI: 10.1016/j.ejor.2024.03.026** (open access; ⚠ PDF pending — see [reading log stub](../papers/reading_log_boysen_dekoster_2025.md))
- **Boysen, N., Schneider, M., & Žulj, I. (2025). Energy management for electric vehicles in facility logistics: A survey from an operational research perspective. *European Journal of Operational Research* (Invited Review, CC-BY-4.0)** — see [reading log](../papers/reading_log_boysen_schneider_zulj_2025.md)
- Chakravarty, A. et al. (2025). Toward Optimal Multi-Agent Robot and Lift Schedules via Boolean Satisfiability. *Mathematics*, MDPI. [PDF in papers/](../papers/)
- Chenreddy, A., & Delage, E. (2023). End-to-end conditional robust optimization. arXiv:2305.19225.
- Elmachtoub, A. N., & Grigas, P. (2022). Smart "Predict, then Optimize". *Management Science* 68(1), 9–26.
- Keung, K. L. (2023). Multi-level RMFS architecture and analytics. *FSMJ*.
- Lenoble, N., Frein, Y., Hammami, R. (2018). Order batching in an automated warehouse with several vertical lift modules: Optimization and experiments with real data. *EJOR*. [PDF in papers/](../papers/)
- Lu, M., & Shen, Z.-J. M. (2021). A review of robust operations management under model uncertainty. *POMS* 30(6), 1927–1943.
- **Qin, Z., Kang, Y., & Yang, P. (2024). Making better order fulfillment in multi-tote storage and retrieval autonomous mobile robot systems. *Transportation Research Part E*, 192, 103752** (planar MTSR neighbor — see [reading log](../papers/reading_log_qin_kang_yang_2024.md))
- **Scholz, A., Schubert, D., & Wäscher, G. (2017). Order picking with multiple pickers and due dates — Simultaneous solution of Order Batching, Batch Assignment and Sequencing, and Picker Routing Problems. *European Journal of Operational Research*, 263(2), 461–478** (planar manual multi-picker OB precedent — see [reading log](../papers/reading_log_scholz_et_al_2017.md))
- Vera, A., Banerjee, S., & Gurvich, I. (2021). Online allocation and pricing: Constant regret via Bellman inequalities. *Operations Research* 69(3), 821–840. https://doi.org/10.1287/opre.2020.2061
- Wiesemann, W., Kuhn, D., & Rustem, B. (2013). Robust Markov decision processes. *Mathematics of Operations Research* 38(1), 153–183. https://doi.org/10.1287/moor.1120.0566
- Wu, J. et al. (2024). Research on Inbound Jobs' Scheduling in Four-Way-Shuttle-Based Storage System. *Processes*, MDPI. [PDF in papers/](../papers/)
- **Žulj, I., Salewski, H., Goeke, D., & Schneider, M. (2022). Order batching and batch sequencing in an AMR-assisted picker-to-parts system. *European Journal of Operational Research*, 298(1), 182–201** (planar AMR-assisted OB precedent)

---

## §11. Appendix — *target 600 words; ~1 page*

### A. Simulator validation
Hand-computed 5×(1→3) scenario: deterministic batched = 72 s; stochastic σ=0.1 over 50 seeds = 72.31 ± 2.62 s.

### B. Pre-registration record
Quote the Phase 4 v2 §4bis pre-reg from [intuitions_before_MVS_v0_2.md](../prototype/intuitions_before_MVS_v0_2.md) and the §11.10 reinforcement-experiment pre-reg, with one line per gate × result.

### C. R2 partition refinement — full table
2×2 / 3×3 / 8-octant per cell, with the $T = 0$ disclosure footnote.

### D. R3 dominance ordering — full table
All 15 (regime, arm) cells with %M2≥M1, %M3 in [M1, M2] span, and median makespans for M1 / M2 / M3a / M3b.

### E. Bootstrap implementation notes
- 1000 iterations, within-arm resampling of 200 makespans per arm.
- Pair-bootstrap OLS refit for $\beta(C)$.
- Random seeds and source files: [analysis_phase4_v2_bootstrap.py](../prototype/src/analysis_phase4_v2_bootstrap.py).

---

## Writing checklist

A section is **done** when *all* of the following are true:

- [ ] Word count is within ±15 % of the target above.
- [ ] Every claim references either an equation in the paper, a results JSON in [prototype/results/](../prototype/results/), or a citation in §10.
- [ ] Every figure mentioned has a caption that says (i) what is plotted, (ii) what regime / model, (iii) what to look at first.
- [ ] Acronyms expanded at first use (AMR, RMFS, VLM, OLS, CI).
- [ ] No claim of *predictive* surrogate for $\Phi$ — only *conceptual decomposition*.
- [ ] No claim that $\beta(C)$ sign is *the* mechanism for M5 — only *consistent with* dominance.
- [ ] Every limitation in §8 is referenced from the body.
- [ ] All five v0.4 trim paths from [§11.2 of novelty doc](../novelty_analysis_and_contribution.md#112-v04-contributions-paragraph-paste-this-into-paper-3) are honoured: drop C2-M3 if word budget tight, compress C2-M4 to one sentence in abstract, etc.

## Per-section word target table

| Section | Target words | Cumulative |
|---|---|---|
| §1 Abstract | 240 | 240 |
| §2 Introduction | 825 | 1 065 |
| §3 Related work | 800 | 1 865 |
| §4 Problem formulation | 700 | 2 565 |
| §5 Methodology | 1 400 | 3 965 |
| §6 Experiments + results | 1 800 | 5 765 |
| §7 Discussion | 700 | 6 465 |
| §8 Limitations | 350 | 6 815 |
| §9 Conclusion | 250 | 7 065 |
| §10 References | (separate) | 7 065 |
| §11 Appendix | 600 | 7 665 |

**Total**: ~7 600 words main + 1 page figures + 1 page appendix = **~10 pages** at C&IE two-column format.

---

## Figure inventory

Eight figures planned, in this order in the paper. Six already exist; two are new for the paper (caption-only here).

| # | Figure file | Used in § | Caption hook |
|---|---|---|---|
| F1 | (new) System diagram | §2.1 | $F$-floor warehouse, AMRs, freight elevators |
| F2 | [phase1_5_paired_makespan.png](../prototype/results/figures/phase1_5_paired_makespan.png) | §6.2 | $M_1$ vs $M_2$ paired makespan; rank order preserved |
| F3 | [phase1_5_betaC_comparison.png](../prototype/results/figures/phase1_5_betaC_comparison.png) | §6.2 | $\beta(C)$ flips sign across $M_1 \to M_2$ |
| F4 | [phase4_v2_option2_bar.png](../prototype/results/figures/phase4_v2_option2_bar.png) | §6.3 | Corner spread (Option 2) per cell — UB visual |
| F5 | [phase4_v2_corner_heatmap.png](../prototype/results/figures/phase4_v2_corner_heatmap.png) | §6.3 | Per-cell × per-size × per-corner makespan heatmap |
| F6 | [phase4_v2_gap_ci.png](../prototype/results/figures/phase4_v2_gap_ci.png) | §6.4.1 / §5.2 | GAP bootstrap CIs, 6/6 cells exclude 0 |
| F7 | [phase4_v2_partition_refinement.png](../prototype/results/figures/phase4_v2_partition_refinement.png) | §6.4.2 | UB under 2×2 / 3×3 / 8-octant partitions |
| F8 | [phase4_v2_m3_medians.png](../prototype/results/figures/phase4_v2_m3_medians.png) | §6.4.3 / §5.3 | Median makespan under M1/M2/M3 σ=0.1/M3 σ=0.2 |
| F9 | [phase4_H1_delta.png](../prototype/results/figures/phase4_H1_delta.png) | §6.4.5 | P1 − P0 delta with 95 % paired-bootstrap CIs per (cell, size, arm); green = sig P1 better |
| F10 | (new) substitutability phase diagram | App B.2 | H1 P1-vs-P0 supported/not grid across 6 cells × 4 stagger CVs |
| F11 | (new) cross-cell meta β surface | App B.7 | β(C) surface from unified meta-regression vs per-cell fits |

---

## Drafting plan (the next 2 weeks)

1. **Day 1–2** — flesh §4 + §5 (problem + methodology). These are the load-bearing sections; everything else hangs off them.
2. **Day 3–4** — pull §6 from the existing [reinforcement deliverable](../prototype/results/v0_2_phase4_v2_reinforcement.md) and [Phase 4 v2 wave-design write-up](../prototype/results/v0_2_phase4_v2_wave_design.md).
3. **Day 5** — write §1 abstract + §2 intro (last, once the rest is locked).
4. **Day 6** — §3 related work, §7 discussion.
5. **Day 7** — §8 limitations, §9 conclusion, §11 appendix.
6. **Day 8** — figures + references + first internal pass.
7. **Day 9–10** — buffer / advisor read / revisions.

**Stop signal for outline → draft**: once §5 (methodology) text is locked, do not change M4 / M5 definitions even if a reviewer simulation hints at a refinement. Refinements go in v0.2 of the draft, not v0.1.
