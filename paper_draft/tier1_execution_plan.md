---
title: "Tier 1 Execution Plan — Push C&IE acceptance odds from 50–65% to 70–80%"
scope: "3 focused weeks; three tasks A/B/C; pre-registered gates; explicit stop rules"
date: 2026-04-22
status: "active"
---

# Tier 1 Execution Plan

## 1. Why Tier 1 exists

Current state (post-R1/R2/R3 reinforcement): C&IE 50–65 %. The single biggest delta between current and 80 % is **Phase 4 H1** — the "tactical marginal value over operational-optimal baseline" question, which every Q1 reviewer asks and which we have not yet answered. Two smaller deltas are **theoretical formalisation** of M5 and M4, which elevate them from "empirical observations" to "propositions with proofs".

Limitations disclosure is the floor, not the ceiling — Tier 1 is about *eliminating* limitations rather than *apologising* for them.

## 2. Three tasks

| Task | Name | Type | Why | Expected lift |
|---|---|---|---|---|
| **A** | Phase 4 H1 — tactical marginal value under strong operational layer | Simulation | Closes the biggest C&IE reviewer gap: "is tactical still useful once operations is optimised?" | **+5–10 % in expectation, 0 % under REJECT (~30–40 % probability)** |
| **B** | M5 collapse — promote to proposition + proof | Analytical | Elevates M5 from empirical to theoretical. Under per-wave stochastic dominance, minimax over $\{M_1, M_2\}$ provably collapses to $M_2$-optimal corner | **+3–5 % (low-variance)** |
| **C** | M4 GAP lower bound theorem | Analytical | Even a loose bound $\mathrm{GAP} \ge f(\beta, \text{spread})$ transforms M4 from diagnostic to framework with theoretical grounding | +2–3 % (60 % success, so expected +1.2–1.8 %) |

**Baseline targets (pre-Tier 1)**: C&IE 50–65 %, IJPR 30–40 %, TR-E 15–25 %.
**Expected post-Tier 1 (honest)**: C&IE **68–76 %** in expectation; under Task A REJECT outcome, 60–68 %; under Task A strong/moderate outcome, 78–85 %. IJPR 45–55 % in expectation. TR-E 30–40 % in expectation.

**Calibration note (2026-04-22 correction)**: earlier pre-run estimates put Task A's expected lift at +10–12 %. After re-examining Phase 4 v2 P0 baseline distribution (3/6 cells hit ≥ 5 %, 0/6 hit ≥ 10 %) and P1's mechanism (destination-clustering helps Arm A more than Arm B, so it *shrinks* MV rather than growing it), a honest expectation has been reset. Thresholds and handling rules in [phase4_H1_preregistration.md](phase4_H1_preregistration.md) remain locked; only the pre-run probability belief has been updated.

## 3. Schedule

| Week | Days | Work | Output |
|---|---|---|---|
| **1** | Mon–Tue | Lock Task A [pre-registration](phase4_H1_preregistration.md) (done before Tier 1 starts). Implement destination-clustered elevator queue (strong operational policy P1) in [simulator.py](../prototype/src/simulator.py). Sanity-check vs. current P0. | Updated simulator + unit tests |
| 1 | Wed–Fri | Implement `experiments_phase4_H1.py` (6 cells × 3 sizes × 2 ops policies × 2 wave arms × 200 waves = 14 400 sims). Smoke-test at small sample. | Raw CSV + smoke plots |
| **2** | Mon–Wed | Full Task A run. Analysis script `analysis_phase4_H1.py`. Bootstrap CIs on marginal value. | `results/v0_2_phase4_H1_tactical_marginal.json` + `v0_2_phase4_H1.md` |
| 2 | Thu–Fri | Task B — write M5 collapse proposition + proof draft | `paper_draft/theorems_m5.md` |
| **3** | Mon–Wed | Task C — write M4 GAP lower bound proposition + proof draft | `paper_draft/theorems_m4.md` |
| 3 | Thu–Fri | Integrate A + B + C into outline §5.3, §5.4, §6.5 updates. Risk/odds reassessment. | `outline_v0_2.md` |

**3 weeks wall clock, ~40 active hours, no parallelism required.**

## 4. Dependency graph

```
Task A (simulation) ─── needed before ─── C3 reframing (if REJECT)
                                    │
Task B (M5 proof) ──── independent ──┼── outline §5.4 rewrite
                                    │
Task C (M4 proof) ──── independent ──┴── outline §5.3 rewrite
```

Only Task A is on the critical path. Tasks B and C are nail-file work that can happen during A's compute time.

## 5. Pre-registered gates

### Task A — Phase 4 H1
See [phase4_H1_preregistration.md](phase4_H1_preregistration.md). Three bands (strong / suggestive / reject), with paper-level handling for each.

### Task B — M5 collapse theorem
**Claim**: *Under per-wave stochastic dominance $\tilde{T}_{M_2}(W) \ge \tilde{T}_{M_1}(W)$ a.s. for every wave $W$, the minimax corner $c^\star = \arg\min_c \max_{M \in \{M_1, M_2\}} \tilde{T}_M(c)$ reduces to $c^\star_{M_2} = \arg\min_c \tilde{T}_{M_2}(c)$.*

**Pre-reg gate**: proof must fit in ≤ 1 page under assumptions already verified empirically in R3 (92.5–100 % dominance frequency).

**Fallback if proof fails**: demote M5 from "theorem-backed rule" back to "empirically motivated heuristic"; recover via Tier 1's 70 % floor plus honest empirical framing. No paper-level structural change.

### Task C — M4 GAP lower bound
**Claim** (target form): *$\mathrm{GAP}(\text{cell}) \ge g(\|\beta\|, \sigma_\Phi, \text{partition granularity})$ where $g$ is computable from the OLS fit alone.*

**Pre-reg gate**: if a non-trivial bound cannot be shown in 3 days of work, demote C to "empirical framework only" and keep only the statistical claim (6/6 CI excludes 0). This is a +0 % lift but no +0 % either — safe fallback.

## 6. Stop rules

**Stop Tier 1 and lock the draft** when **any** of the following is true:

1. Task A **strong** (≥ 10 % marginal in ≥ 4/6 cells) + B proof complete → acceptance estimate ≥ 80 %. Do not start Tier 2.
2. Task A **suggestive** (≥ 5 %) + B **and** C proofs complete → acceptance estimate ≈ 78 %. Do not start Tier 2 unless you have > 2 weeks budget.
3. Task A **reject** (< 2 % marginal in ≥ 4/6) → acceptance estimate drops to 45–55 %. **Stop, pivot narrative**: Paper becomes "tactical layer is absorbed by good operations except in X regimes where Φ still adds" — a different but honest paper. Do not add Tier 2 to rescue.
4. Week 3 Friday arrives regardless of outcome → stop. Moving the deadline is the single most common way to convert a 70 % paper into a never-submitted paper.

## 7. Risk list

| Risk | Prob. | Mitigation |
|---|---|---|
| P1 destination-clustered dispatch still produces identical makespan to P0 on our scenarios | 20 % | Add a second op-layer variant (e.g., myopic SPT) as backup; if both match P0, current simulator is already strong ops — run A as "P0-only" and reinterpret marginal value as an absolute claim |
| A shows REJECT because tactical value is fully absorbed | 25 % | Pre-registered narrative pivot (§6 Stop rule 3); write the pivot paragraph before running A so it does not feel reactive |
| B proof needs an assumption we cannot verify | 30 % | Demote to "empirical rule with sketched argument"; paper still stands |
| C proof is intractable | 40 % | Drop to §6 Stop rule 2 and proceed with A+B only |
| Week 3 blown | 15 % | Hard stop at Friday; ship with A + whichever of B/C is done |

## 8. Reporting cadence

- **End of Week 1**: 1-paragraph Slack-style note on simulator changes + smoke-test numbers.
- **End of Week 2**: full `v0_2_phase4_H1.md` deliverable + proof draft link.
- **End of Week 3**: odds reassessment table (update to this file's §2 "Expected post-Tier 1" row).

## 9. What comes after Tier 1

If Tier 1 lands in Stop rule 1 or 2 → **start drafting §4/§5/§6 of the paper** using the [outline](outline_v0_1.md). Do **not** start Tier 2 unless more than 2 weeks remain in the submission window.

Tier 2 tasks (c ∈ {1,3} sweep, temporal stagger, β sample scale-up) are explicitly **out of scope** for this plan.

---

## Appendix — budget reality check

| Task | Coding hours | Sim runtime (on local Windows) | Analysis hours | Total |
|---|---|---|---|---|
| A (simulator + experiment + analysis + writeup) | 16 | ~6 (serial) | 8 | 30 h |
| B (proof + writeup) | 0 | — | 4 | 4 h |
| C (proof attempt + writeup/demote) | 0 | — | 6 | 6 h |
| **Total** | 16 | 6 | 18 | **40 h** |

Fits in 3 weeks at ~14 h/week of focused work, leaving buffer for unexpected blockers.
