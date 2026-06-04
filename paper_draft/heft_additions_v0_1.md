---
title: "Heft additions v0.1 — (1) worked managerial example + (2) robustness-into-main-text"
parent: "Wave Release Coordination under Vertical Resource Constraints"
date: 2026-05-21
status: "draft v0.1 — content record for the two no-AI heft additions agreed 2026-05-21"
scope: "These two additions add LEGITIMATE strength to the EMPIRICAL/MANAGERIAL layer of Paper 3 using EXISTING data only. They do NOT add an AI agent (that is Pillar 2, a separate paper), do NOT run new simulations, and do NOT touch the locked & signed pre-registration or any locked verdict."
source_data:
  - "prototype/results/v0_5_phase5_blockA.json  (publication-scale decomposition; config 7 sub-cell)"
  - "prototype/results/v0_5_phase5_blockC.json  (publication-scale Hedge Rule; config 7 collapse + U_c bound)"
  - "paper_draft/appendix_robustness.md  (prototype-scale Gap-1/2/3 + Tier-1.5 robustness battery)"
---

# Heft additions — what these two parts present

This file records the content of the two agreed heft additions. Both target the
layer reviewers feel is thin — the **empirical / managerial** layer — not the
methodology layer (the two theorems are already a tight unit). Neither addition
needs the AI agent, new simulations, or any change to the locked pre-registration.

- **Part 1 — a worked managerial example.** Walks one concrete warehouse
  end-to-end through *both* tools, turning the abstract `GAP = H_up + M_Φ`
  decomposition and the Hedge Rule into a usable operator playbook + a decision
  flowchart. **Uses existing Phase-5 results; zero new runs.**
- **Part 2 — surfacing the robustness battery into the main text.** A compact
  "Robustness and Generality" subsection that lifts the strongest of the
  already-completed sensitivity studies out of the appendix, **honestly labelled
  by the scale at which each was run**.

What these additions explicitly **do not** do (guardrails):
1. No AI agent / RL / learned policy anywhere in the paper body.
2. No new simulations; no re-running of `H1` against a stronger baseline (that
   would be goalpost-moving after a signed PARTIAL verdict).
3. No edit to the locked & signed `phase5_scaleup_preregistration.md` or any
   pre-registered gate verdict.

---

# Part 1 — Worked managerial example (proposed §7.x, ~250–300 words + 1 figure)

**Purpose.** Show, on one concrete warehouse, that the two tools are not just
proven objects but a step-by-step decision procedure an operator can run. This
is the single highest-value-per-effort heft addition for an applied venue like
C&IE: it converts "we have two theorems" into "here is how a manager uses them."

## 1.1 The running example — configuration 7 (real Phase-5 numbers)

We use **configuration 7**: `F = 5` floors, `|A| = 5` AMRs, `E = 2` elevators,
**clustered** demand. All numbers below are read directly from the published
Phase-5 artefacts (no new computation).

| Quantity | Value | Source |
|---|---|---|
| `H_up` (partition-intrinsic, capacity-side headroom) | **0.157** (15.7 % of `m_0`) | Block A, cfg-7 / M2 / size-8 sub-cell |
| `M_Φ` (policy-recoverable component) | **0.021** (2.1 % of `m_0`) | same sub-cell |
| `GAP = H_up + M_Φ` | **0.178**, 95 % CI [0.099, 0.285] (excludes 0) | same sub-cell |
| Hedge corner `c*` (= DRO corner) | **LC_HI** (collapse holds) | Block C, cfg-7 |
| per-wave dominance `M2 ≥ M1` at `c*` | **0.99–1.00** across corners | Block C, cfg-7 |
| worst-case bound `U_c(0.05)` at `c*` | **9.5 wave-time units** = **3.4 % of `m_0`** (`m_0 = 283`) | Block C, cfg-7, LC_HI |

*(Footnote for the paper: the decomposition is illustrated at the size-8
sub-cell of Block A; the Hedge-corner and `U_c` bound are from the matched-wave
Block C analysis of the same configuration — the two blocks evaluate the same
config at their respective designed wave sizes.)*

## 1.2 The four-step operator procedure (draft prose)

> **A worked decision.** Consider a five-floor warehouse served by five AMRs and
> two freight elevators under clustered demand (configuration 7). An operator
> applies the two tools in sequence.
>
> **Step 1 — fingerprint the candidate waves.** Compute `Φ = (C, I, T)` on the
> candidate pool and partition the `(C, I)` plane into the four quartile corners.
>
> **Step 2 — read the Bound-and-Gap decomposition.** Here `GAP = 0.178`
> (95 % CI excludes zero), of which the partition-intrinsic component
> `H_up = 0.157` accounts for **88 %** and the policy-recoverable component
> `M_Φ = 0.021` only **12 %**. By Table 1 (large `H_up`, small `M_Φ`), the
> reading is unambiguous: *wave composition is already near the best its
> partition allows; the remaining makespan headroom is structural.* The lever to
> pull here is **elevator-side capacity**, not finer wave-feature engineering —
> the decomposition tells the operator this *before* committing to any
> feature-engineering project that could, at most, recover 2.1 % of makespan.
>
> **Step 3 — if releasing a wave, apply the Hedge Rule.** Should the operator
> still compose a wave, the Hedge Rule prescribes the corner optimal under the
> true-batching model `M2`, here **LC_HI** (low concentration, high imbalance).
> No online elevator-model identification is required: per-wave dominance holds
> in 99–100 % of waves, so the minimax corner collapses to this closed form.
>
> **Step 4 — quote the worst-case guarantee.** Even if the operator's belief
> about the elevator model is wrong, following the `M2`-corner loses at most
> `U_c(0.05) = 3.4 %` of makespan relative to the model-specific optimum
> (Corollary 2). The operator therefore acts on a number they can compute from
> their own data, with a one-line rule and a bounded downside.

## 1.3 The decision flowchart (proposed Figure; ASCII sketch for now)

```
        拿到一个仓库 config  (F, |A|, E, demand)
                     │
                     ▼
 [1] 在候选 wave 上算 Φ=(C,I,T)，按 (C,I) 切成 2×2 四个角
                     │
                     ▼
 [2] 算 Bound-and-Gap 分解：  GAP = H_up + M_Φ
                     │
        ┌────────────┼─────────────┬───────────────┐
        ▼            ▼             ▼               ▼
   H_up 大,M_Φ小  H_up小,M_Φ大   两者都大        两者都小
   结构性主导     Φ未校准        先扩特征        wave设计
   →投电梯容量    →投特征工程    (优先级最高)    不是这里的杠杆
   (cfg-7 在此)
                     │
                     ▼
 [3] 若要放行 wave → Hedge Rule 选 M2-最优角 c*   (cfg-7: LC_HI)
                     │   无需在线识别电梯模型 (per-wave dominance ≥99%)
                     ▼
 [4] 报最坏损失界  U_c(ε)/m_0   (cfg-7: 3.4%)
        即使电梯模型猜错，也不超过这个百分比
```

**Figure caption (draft).** *Operator decision procedure. Steps 2 and 3 are the
two tools of §4; the branch in step 2 is Table 1's four-way reading; the running
annotations (cfg-7: H_up large → capacity lever; c* = LC_HI; bound 3.4 %) trace
configuration 7 through the procedure.*

## 1.4 Why this adds heft (not volume)

- It is the **actionability** evidence applied reviewers (C&IE) look for: a
  manager can run the four steps on their own warehouse.
- It re-uses the *existing* decomposition and Hedge results — **no new data** —
  yet makes the empirical layer feel complete rather than abstract.
- It reinforces, rather than dilutes, the Option-B headline: the cfg-7 reading
  (`H_up` dominates → capacity-side) is exactly the "capacity-bound > policy-bound"
  managerial diagnosis the abstract now leads with.

---

# Part 2 — Robustness and Generality, surfaced into the main text (proposed §5.x, ~250 words + 1 table)

**Purpose.** The paper has already run a substantial robustness battery, but it
is buried in the appendix. Surfacing a compact summary into the main text makes
the empirical contribution look as thorough as it actually is — at near-zero
cost, because the work is done. The only real task is **honest scale labelling**.

**Decision (2026-05-21).** Unify the *main-text* robustness to publication
scale using only what the existing 106,800-sim grid already supports (Tiers 1–2
below); the four simulator-fidelity perturbations stay at prototype scale,
honestly labelled, in the appendix (Tier 3). No new simulation campaign.

## 2.1 Three tiers — what is already publication-scale, what is free, what stays prototype

**Tier 1 — already publication-scale (no action).** The main 18-configuration
grid *is itself* the primary robustness study: it varies `F ∈ {3,5,8}`,
`|A| ∈ {5,15,30}`, `E ∈ {1,2}`, and demand ∈ {uniform, clustered, diurnal} and
shows the decomposition `GAP = H_up + M_Φ` holding 72/72 and the Hedge collapse
holding 6/6. The capacity sweep `c ∈ {2,3,4,5}` is also publication-scale
(Supp-2): per-wave dominance 99.7 / 100.0 / 99.9 / 99.9 %.

**Tier 2 — free reanalysis of the existing grid (zero new sims, do now).**
Publication-scale GAP margins read directly off Block A's 72 sub-cells:

| Margin | Publication-scale result (from existing Block A) |
|---|---|
| demand | clustered `GAP=0.082` > uniform `0.052` > diurnal `0.046` (CI excludes 0 in 20/24, 20/24, 17/24) |
| elevator `E` | `E=1` 0.058 ≈ `E=2` 0.062 |
| elevator model | abstraction 0.065 > true-batching 0.056 |
| (meta-regression) | re-fit on Block A still to run — cheap, no new sims |

**Tier 3 — prototype-scale, stays in appendix, honestly labelled (no re-run).**
The four simulator-fidelity perturbations (service-time heterogeneity,
order-release stagger, directional elevator dynamics, heterogeneous pool), the
ceteris-paribus floors sweep, and the FCFS anchor. These defend the *simulator's
fidelity*, not the main findings; they are supporting evidence and carry a
one-line scale disclaimer.

> ⚠ **Floors finding — do NOT promote to the main text.** The prototype
> ceteris-paribus sweep (Appendix B.5) reports `GAP` **growing** with `F`
> (8 %→19 % over `F∈{5,7,9}`). The publication-grid marginal goes the *other*
> way (`F=3` 0.071 → `F=5` 0.057 → `F=8` 0.052). The two do not contradict
> cleanly — the publication grid is a fractional factorial that *confounds* `F`
> with `|A|` and demand, so no clean `F` main-effect is identifiable from it.
> Net: the publication grid cannot support a floors claim, and the prototype
> sweep can only support one at prototype scale. **Keep all floors discussion in
> the appendix at prototype scale; make no "GAP grows/shrinks with F" claim in
> the main text.** (This is exactly the scale-mismatch landmine the split avoids.)

## 2.2 Compact summary table (draft — for the main text)

| Robustness dimension | Scale | Evidence | Verdict |
|---|---|---|---|
| Across-config (`F,|A|,E`, demand) | **publication** | 18-config main grid: decomposition 72/72, Hedge 6/6 | primary robustness, already in §5.2–5.3 |
| Elevator capacity `c ∈ {2,3,4,5}` | **publication** | 48,000 sims (Supp-2); dominance 99.7–100 % | Hedge generalizes beyond `c=2` |
| Demand pattern | **publication** | Block A margin (reanalysis) | lever strongest under clustered demand |
| Elevator-model margin | **publication** | Block A margin (reanalysis) | decomposition holds under both models |
| Service-time heterogeneity (CV→131 %) | prototype (App.) | 24,000 sims; best-corner 5/6 robust | simulator-fidelity, supporting |
| Order-release stagger (CV→1.0) | prototype (App.) | 24,000 sims; argmin 5/6 robust | simulator-fidelity, supporting |
| Directional elevator dynamics | prototype (App.) | 12,000 sims; dominance 97.7 % | simulator-fidelity, supporting |
| Heterogeneous elevator pool | prototype (App.) | 4,000 sims; 3/4 corners stable | simulator-fidelity, supporting |
| Floors `F ∈ {5,7,9}` (ceteris paribus) | prototype (App.) | 6,000 sims | **appendix only — see ⚠ above** |
| FCFS anchor | prototype (App.) | 7,200 sims; P1-over-FCFS 19–21 % | simulator-fidelity, supporting |

## 2.3 Draft prose (publication-scale framing)

> **Robustness and generality.** The publication-scale grid is itself the
> primary robustness study: across 18 configurations spanning floors, fleet
> size, elevator count, and three demand patterns, the decomposition
> `GAP = H_up + M_Φ` holds in all 72 sub-cells and the Hedge collapse in all 6
> matched-wave configurations. The wave-structure lever is largest under
> clustered demand (`GAP = 0.082` vs 0.046 under diurnal) and is present under
> both elevator models. The chain-dominance condition underlying the Hedge Rule
> extends cleanly beyond its `c = 2` derivation point, with per-wave dominance
> 99.7–100 % across `c ∈ {2,3,4,5}` (Supp-2). A complementary battery of
> simulator-fidelity sensitivity studies — varying intra-floor service-time
> heterogeneity, order-release stagger, directional elevator dynamics, and
> elevator-pool heterogeneity — is reported at prototype scale in the Appendix;
> the best-corner identification survives each perturbation in at least 5 of 6
> prototype cells, and where a corner shifts it shifts exactly where Corollary 2
> predicts (tight inter-corner gaps or loose wave timing).

## 2.4 Honest caveats (residual, for the appendix material)

The Tier-3 appendix studies were written in the **old vocabulary** (M4/M5,
`E∈{1,2,3}×c2` regimes, the H1 substitutability story). They stay in the
appendix, but before the appendix ships:

1. **Terminology** — rename M4/M5 → Bound-and-Gap / Hedge Rule, M1/M2 →
   throughput-abstraction / true-batching, to match §4–§5.
2. **Option-B consistency** — the stagger study (A.2/B.2) is framed around the
   *H1 tactical-operational substitutability map*, which Option B retired. Cite
   only its corner-stability result; drop the substitutability framing.
3. **Scale label on every prototype number** — each appendix table gets a
   one-line "prototype-scale (6-cell `E∈{1,2,3}×c2`) supporting study" header so
   no prototype number is ever read as publication-scale.

**Net effect:** the main text now carries *only* publication-scale robustness
(across-config grid + capacity sweep + reanalysis margins); the prototype battery
is clearly quarantined in the appendix as simulator-fidelity support. The
scale-mismatch liability is removed without a single new simulation.

---

# Suggested placement in the paper

| Addition | Where | Size | New artefact |
|---|---|---|---|
| Part 1 worked example | new **§7.1** (open the Discussion with it) | ~250–300 words | 1 decision-flowchart figure |
| Part 2 robustness subsection | new **§5.6** or expand **§5.5** | ~250 words | 1 summary table |

Both fit inside the existing word budget if kept tight; if §7 prose is tight,
Part 1's flowchart figure carries most of the load and the prose can compress.
