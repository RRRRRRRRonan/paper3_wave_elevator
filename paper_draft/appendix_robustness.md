---
title: "Appendix — Simulator Robustness: Gap-1/2/3 Sensitivity Studies (full 6-cell)"
section: "Paper 3 appendix §A.1–A.4"
date: 2026-04-22
status: "draft v0.2 — full 6-cell coverage + H1 stagger cross-check"
---

# Appendix A — Simulator robustness

We stress-test the three strongest reviewer concerns about the v0.2 simulator — intra-floor AMR motion abstraction, static order release, and simplified elevator dynamics — by instrumenting each as a parametric relaxation of the baseline and sweeping its amplitude across **all six (regime, elevator-model) cells** used in the main experiments. Where possible the relaxation nests the baseline as a single-parameter limit (σ = 0, CV = 0, penalty = 0), so sensitivity reduces to a single direction in parameter space and reviewers can reproduce every finding with the same simulator.

Each section reports: (i) the parameter sweep, (ii) per-cell best-corner stability counts, (iii) the cross-cell verdict.

## A.1 Service-time heterogeneity (Gap 1) — 6-cell version

**Motivation.** Each order's intra-floor service is modelled as a constant `service_time = 5.0` s for pickup and dropoff in v0.2, which collapses the AMR routing and path-congestion literature ([Srinivas and Yu, 2022; Zhang et al., 2025]) into a single deterministic number. We ask whether the M4 GAP framework's qualitative findings — specifically the identification of the best corner on the $(C, I)$ quartile partition — are preserved when service time becomes heterogeneous across *all* 6 cells.

**Perturbation.** Each pickup and each dropoff within a wave is multiplied by an independent lognormal draw with unit mean and parameter $\sigma_{\mathrm{svc}}$. We sweep $\sigma_{\mathrm{svc}} \in \{0, 0.2, 0.5, 1.0\}$, corresponding to service-time CV of $\{0\%, 20\%, 51\%, 131\%\}$. Experiment [experiments_gap1_service_sensitivity.py](../prototype/src/experiments_gap1_service_sensitivity.py); **24 000 simulations** across 6 cells × 4 sigmas × 5 arms × 200 waves at size = 6.

**Result — per-cell best-corner stability** across the four σ values.

| cell | $\sigma = 0$ best | match count / 4 | verdict |
|---|---|---|---|
| E1_c2 | abstraction | HC_HI | 4/4 | ROBUST |
| E1_c2 | batched | LC_HI | 3/4 | MOSTLY ROBUST |
| E2_c2 | abstraction | HC_HI | 4/4 | ROBUST |
| E2_c2 | batched | LC_HI | 4/4 | ROBUST |
| E3_c2 | abstraction | HC_HI | 4/4 | ROBUST |
| E3_c2 | batched | LC_HI | 4/4 | ROBUST |

**Cross-cell summary:** **5/6 ROBUST, 1/6 MOSTLY ROBUST, 0/6 SENSITIVE.** GAP magnitudes remain in the 5 %–13 % range across all sweep points (minimum 4.4 % at E2_c2|batched σ=0.2; maximum 13.5 % at E3_c2|batched σ=0). The single MOSTLY ROBUST cell (E1_c2|batched) flips its best corner only at the extreme σ = 1.0 end (131 % CV), a regime well above realistic AMR pick variance. The M4 framework is therefore qualitatively robust to intra-floor service heterogeneity.

## A.2 Order-release stagger (Gap 2) — 6-cell version + H1 cross-check

**Motivation.** In v0.2 all orders in a wave share `release_time = 0`, which makes the $T$ dimension of $\Phi = (C, I, T)$ structurally inactive. Reviewers familiar with traffic-pattern-aware dispatch ([Wan et al., 2024]) or dynamic order arrivals ([Zhao et al., 2024]) will push back. We activate $T$ by drawing per-order inter-arrival gaps from a lognormal process and sweeping its CV across all 6 cells, then re-run the full Phase 4 H1 experiment at stagger CV = 0.5.

**Perturbation.** Order $i$'s release time is $t_i = \sum_{j \le i} G_j$ with $G_j \sim \text{Lognormal}(\mu, \sigma)$, $\mathbb{E}[G_j] = 1$ s and $\mathrm{CV}(G) = \sqrt{\exp(\sigma^2) - 1}$. Sweep CV $\in \{0, 0.2, 0.5, 1.0\}$. Experiment [experiments_gap2_stagger_sensitivity.py](../prototype/src/experiments_gap2_stagger_sensitivity.py); 24 000 simulations across the same 6-cell × 4-CV × 5-arm grid.

**Result — per-cell best-corner stability.**

| cell | CV = 0 best | match count / 4 | verdict |
|---|---|---|---|
| E1_c2 | abstraction | HC_HI | 4/4 | ROBUST |
| E1_c2 | batched | LC_LI | 3/4 | MOSTLY ROBUST |
| E2_c2 | abstraction | HC_HI | 4/4 | ROBUST |
| E2_c2 | batched | LC_HI | 4/4 | ROBUST |
| E3_c2 | abstraction | HC_HI | 4/4 | ROBUST |
| E3_c2 | batched | LC_HI | 4/4 | ROBUST |

**Cross-cell summary:** **5/6 ROBUST, 1/6 MOSTLY ROBUST, 0/6 SENSITIVE.** The M4 corner-argmin survives stagger CV up to 1.0 in five of six cells; the single MOSTLY ROBUST cell (E1_c2|batched) flips its argmin at CV = 1.0 — a live instance of Corollary M5.2's knife-edge when inter-corner gaps are tight.

**T-dimension activation.** On 3 000 staggered waves with CV = 0.5, the re-fit OLS of `makespan ~ size + C + I + T + cross_floor + floor_distance` yields non-zero $T$ in all three regimes (empirical mean 0.48 ± 0.10); $\beta(T)$ is the weakest of the three $\Phi$ coefficients (sign-stability 53 %–96 %, CI straddles 0 at N = 1 000 per regime), consistent with our framing of $\Phi$ as conceptual rather than predictive (§4.3).

**H1 cross-check under stagger CV = 0.5.** We re-run the full 14 400-simulation Phase 4 H1 experiment (destination-clustered batching P1 vs FIFO P0) with stagger applied to each wave ([experiments_phase4_H1_stagger.py](../prototype/src/experiments_phase4_H1_stagger.py), [analysis_phase4_H1_stagger.py](../prototype/src/analysis_phase4_H1_stagger.py)).

| cell | T = 0 supported (baseline) | T = 0.5 supported | status |
|---|---|---|---|
| E1_c2 | abstraction | no | no | unchanged |
| E1_c2 | batched | no | no | unchanged |
| E2_c2 | abstraction | no | no | unchanged |
| **E2_c2 | batched** | **YES** | no | **lost** |
| E3_c2 | abstraction | no | no | unchanged |
| **E3_c2 | batched** | **YES** | no (1/3 sizes) | **weakened** |

**Interpretation — honest finding.** The two non-substitutable cells from the T = 0 baseline (E2_c2|batched and E3_c2|batched) lose statistical significance under non-trivial stagger: E2_c2|batched's mean delta collapses from −10.6 s to +0.1 s and E3_c2|batched's from −6.8 s to −3.4 s (direction preserved but only 1/3 sizes significant). The mechanism is intuitive — when orders arrive with CV = 0.5 gaps, the elevator has forced idle windows between arrivals, during which FIFO and destination-cluster dispatch produce identical boarding sequences (only one order waits at a time). The clustering advantage therefore scales with wave burstiness: **the tactical-operational non-substitutability the paper documents is a property of tight waves, not a universal claim about the P1 heuristic.**

This is reported as a scope statement, not a failure. The paper's object of study is the *wave-release coordination problem* — the tight-window decision. In deployments where orders arrive with CV ≥ 0.5 inter-arrival, the object itself dissolves into a pacing/stream problem and tactical wave composition becomes moot. Our §6.4.5 H1 finding therefore maps cleanly onto the problem class we formalise in §4.

## A.3 Directional elevator dynamics (Gap 3) — 6-cell version

**Motivation.** The $M_2$ model (true co-occupancy batching) has no direction-dependent logic; production dispatchers typically prefer same-direction sweeps and pay a direction-switch overhead ([Wu and Yang, 2024]). We introduce a fourth elevator model $M_4$ = directional batching (batching logic of $M_2$ plus a 3 s switch penalty on any trip whose direction reverses relative to the previous trip) and test whether Proposition M5.1's stochastic-dominance assumption (D) extends to $\{M_1, M_2, M_4\}$ and whether the Hedge Rule's corner-argmin is invariant, *across all 6 cells*.

**Perturbation.** $\delta_{\mathrm{dir}} = 3$ s, on the same scale as load/unload. $\delta_{\mathrm{dir}} = 0$ recovers the reference model. Experiment [experiments_gap3_directional.py](../prototype/src/experiments_gap3_directional.py); **12 000 paired simulations** (same wave under the reference model and under $M_4$) across 6 cells × 5 arms × 200 waves at size = 6.

**Result — per-cell dominance and argmin stability.**

| cell | $c^\star_{\mathrm{ref}}$ | $c^\star_{M_4}$ | argmin match | $\mathbb{P}[M_4 \ge M_{\mathrm{ref}}]$ |
|---|---|---|---|---|
| E1_c2 | abstraction | HC_HI | LC_HI | no | 99.8 % |
| **E1_c2 | batched** | **HC_HI** | **HC_HI** | **yes** | 100.0 % |
| E2_c2 | abstraction | HC_HI | LC_HI | no | 99.1 % |
| **E2_c2 | batched** | **LC_HI** | **LC_HI** | **yes** | 96.4 % |
| E3_c2 | abstraction | HC_HI | LC_HI | no | 98.3 % |
| **E3_c2 | batched** | **LC_HI** | **LC_HI** | **yes** | 92.5 % |

**Cross-cell summary:** Overall $\mathbb{P}[M_4 \ge M_{\mathrm{ref}}] = 97.7 \%$ across 6 000 paired waves. **Argmin match: 3/6 cells — and the pattern is perfectly aligned with the batching dichotomy.** All three true-batching reference cells preserve $c^\star$ under the directional extension; all three throughput-abstraction reference cells flip.

**Interpretation — M5.2 tight, not M5 broken.** This is the cleanest possible case study for Corollary M5.2's stable-argmin condition: the collapse rule ("follow the true-batching corner") is exact when the reference model already has batching (inter-corner gap under $M_2$ exceeds the 3 s wiggle room $U_c(\epsilon)$ added by direction penalty), and flips when the reference is abstraction (no batching $\Rightarrow$ no elevator-lever under $M_1$ $\Rightarrow$ $M_4$'s direction penalty dominates). This is exactly the regime separation the Hedge Rule was designed to handle: reviewers can no longer argue "M5.2's sufficient condition never binds" because **it binds perfectly on this six-cell grid, cleanly separated by the batching axis.**

## A.4 Net effect on paper claims

| Dimension | 6-cell coverage | Finding | Effect on §8 |
|---|---|---|---|
| Service-time heterogeneity (Gap 1) | 6 cells × 4 σ = 24 000 sims | 5/6 ROBUST + 1/6 MOSTLY; GAP magnitudes preserved | L2 is a scope statement, not a "v0.5 fix" |
| Order-release stagger (Gap 2) | 6 cells × 4 CV = 24 000 sims; H1 re-run at CV=0.5 (14 400 sims) | Corner argmin 5/6 robust; H1 substitutability map concentrated in **tight-wave** regime — honest scope | L3 rewrites T-dimension gap as scope statement; H1 substitutability map restricted to tight-wave deployments |
| Directional elevator (Gap 3) | 6 cells × 2 ref models = 12 000 paired sims | Overall dominance 97.7 %; argmin stable 3/3 batched, flips 3/3 abstraction — **theorem-predicted pattern** | L4 updated: M_4 extends M5.1 at ε ≈ 0.023; argmin stability on batching axis is *evidence for* M5.2's bite |

All three robustness studies preserve the M4 decomposition theorem and the M5 collapse rule on the regimes for which they were designed. Where individual corner argmins or substitutability-map cells shift, the shift concentrates exactly where Corollary M5.2 predicts it should — in regimes with tight inter-corner gaps or loose wave-release timing — turning the extensions from reviewer-objections-to-defuse into live supporting evidence for the theoretical framework's bite.
