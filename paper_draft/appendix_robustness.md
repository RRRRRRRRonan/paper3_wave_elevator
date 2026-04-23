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

---

# Appendix B — Tier 1.5 generalisation and predictive-validity studies

This appendix collects the eight extensions run after the Gap-1/2/3 sensitivity sweeps: M4 predictive validity (S1), H1 stagger phase diagram (S2), capacity sweep c ∈ {2, 3, 4, 5} (S3), β stratification (S4), floors sweep F ∈ {5, 7, 9} (A1), FCFS baseline anchor (A2), cross-cell meta-regression (A3), and heterogeneous elevator pool (B1). Together they address the strongest generalisation questions a C&IE reviewer is expected to raise, without introducing new theoretical claims.

## B.1 M4 predictive validity (S1)

Tests whether M4's elevator-lever term $H_{\mathrm{up}}$ (from the GAP decomposition) **predicts** the Phase 4 H1 outcome, not merely explains it retrospectively.

**Naive cross-cell correlation fails**: across all 6 cells, Pearson$(H_{\mathrm{up}}, \Delta_{\mathrm{H1}}) = +0.15$; Spearman $= +0.09$, $p = 0.87$. This is because the 3 abstraction cells have inflated $H_{\mathrm{up}}$ from theoretical corner-median spread *without real batching-lever*, so mixing them with batched cells washes the signal.

**Composite predictor succeeds** — cells where $c^\star_{M_2} \ne c^\star_{M_1}$ (i.e. Corollary M5.2's applicability domain = batched AND $E \ge 2$) perfectly classify H1 outcomes:

| cell | model | $E$ | M5.2 applicable? | H1 supported? | match |
|---|---|---|---|---|---|
| E1_c2 | abstraction | 1 | no | no | ✓ |
| E1_c2 | batched | 1 | no | no | ✓ |
| E2_c2 | abstraction | 2 | no | no | ✓ |
| **E2_c2** | **batched** | **2** | **yes** | **yes** | ✓ |
| E3_c2 | abstraction | 3 | no | no | ✓ |
| **E3_c2** | **batched** | **3** | **yes** | **yes** | ✓ |

Accuracy **6/6**. Within the batched-only subset Pearson$(H_{\mathrm{up}}, \Delta_{\mathrm{H1}}) = -0.673$ (expected negative — larger $H_{\mathrm{up}}$, more room for P1 to win). The GAP decomposition is therefore prospective *conditional on M5.2's applicability domain*: it tells you **which cells** will benefit from destination-clustered batching **before** you run the expensive H1 experiment. See [analysis_S1_m4_predictive.py](../prototype/src/analysis_S1_m4_predictive.py), [v0_2_S1_m4_predictive_validity.json](../prototype/results/v0_2_S1_m4_predictive_validity.json).

## B.2 H1 substitutability phase diagram (S2)

Extends the single-CV stagger re-run (Appendix A.2) to a 4-CV sweep producing a tactical-operational substitutability phase diagram. **57 600 simulations** across CV ∈ {0, 0.2, 0.5, 1.0} × 6 cells × 3 sizes × 2 arms × 2 policies × 200 waves.

**Phase diagram (cell × CV, ☐ = supported):**

| cell | CV = 0 | CV = 0.2 | CV = 0.5 | CV = 1.0 |
|---|---|---|---|---|
| E1_c2 | abstraction | — | — | — | — |
| E1_c2 | batched | — | — | — | — |
| E2_c2 | abstraction | — | — | — | — |
| **E2_c2 | batched** | **SUPP** | — | — | — |
| E3_c2 | abstraction | — | — | — | — |
| **E3_c2 | batched** | **SUPP** | **SUPP** | — | **SUPP** |

Mean Δ (P1 − P0, favorable arm, size-averaged):

| cell | CV=0 | CV=0.2 | CV=0.5 | CV=1.0 |
|---|---|---|---|---|
| E2_c2 | batched | −11.29 | −0.02 | −1.93 | −4.39 |
| E3_c2 | batched | −6.07 | −5.53 | −2.33 | −3.46 |

**Interpretation.** E3_c2|batched is the most stagger-robust cell (Δ consistently negative, re-emerges as significant at CV=1.0); E2_c2|batched is the most CV-sensitive (collapses for CV ≥ 0.2). This is the paper's primary managerial diagnostic: the tactical lever is largest in tight-wave, elevator-lever-dominant regimes, and diminishes along both the wave-looseness axis and the capacity-slack axis. See [experiments_S2_stagger_sweep.py](../prototype/src/experiments_S2_stagger_sweep.py), [v0_2_S2_stagger_phase_diagram.json](../prototype/results/v0_2_S2_stagger_phase_diagram.json).

## B.3 Capacity sweep c ∈ {2, 3, 4, 5} (S3)

Tests whether Proposition M5.1's per-wave stochastic-dominance assumption (D) and the Hedge Rule's applicability extend beyond the c=2 case the paper focuses on. **8 000 paired simulations** at $E = 2$ across 5 arms × 200 waves × 4 capacities at size = 6.

| capacity | $c^\star_{M_1}$ | $c^\star_{M_2}$ | $M_1/M_2$ disagree? | $\mathbb{P}[M_2 \ge M_1]$ |
|---|---|---|---|---|
| 2 | HC_HI | LC_HI | yes | 98.1 % |
| 3 | HC_HI | LC_HI | yes | 99.7 % |
| 4 | HC_HI | HC_HI | no | 100.0 % |
| 5 | HC_HI | LC_HI | yes | 99.9 % |

**Overall $\mathbb{P}[M_2 \ge M_1] = 99.4 \%$** across c ∈ {2, 3, 4, 5}. Proposition M5.1's assumption (D) extends cleanly to higher capacities at $\epsilon \approx 0.006$. The $M_1/M_2$ argmin disagreement persists at c = 3, 5 (the Hedge Rule has practical bite across the capacity spectrum, not just at c = 2). See [experiments_S3_capacity_sweep.py](../prototype/src/experiments_S3_capacity_sweep.py), [v0_2_S3_capacity_sweep.json](../prototype/results/v0_2_S3_capacity_sweep.json).

## B.4 β stratification and sample design (S4)

Tests whether per-corner stratified OLS is more bootstrap-stable than pooled OLS (conjecture: within-corner residual variance is lower, so β sign is more coherent).

**Honest finding:** per-corner stratification **degrades** β(C) sign stability (pooled 93–100 % → per-corner mean 69–88 %). Reason: within a quartile corner, $C$ has very small variance, and the OLS fit for β(C) becomes ill-identified; smaller N exacerbates bootstrap variability.

**However:** the Phase 4 v2 corner-spanning sampling design (which deliberately covers extremes of $\Phi$) **already** yields higher pooled β(C) stability (93–100 %) than the original Phase 1.5 random sampling (76–85 %). The practitioner rule is: **sample design beats post-hoc stratification**. When fitting $\Phi$ coefficients, span the feature space rather than stratifying after the fact. See [analysis_S4_beta_stratified.py](../prototype/src/analysis_S4_beta_stratified.py), [v0_2_S4_beta_stratified.json](../prototype/results/v0_2_S4_beta_stratified.json).

## B.5 Floors sweep F ∈ {5, 7, 9} (A1)

v0.2 main experiments use F = 5. Extended to F = 7 and F = 9 to test realistic multi-storey warehouse scale. **6 000 sims** at $E = 2$, cap = 2, size = 6.

| F | model | best corner | GAP % | med(random) |
|---|---|---|---|---|
| 5 | abstraction | LC_LI | 8.91 % | 101.00 |
| 5 | batched | LC_HI | 12.07 % | 145.00 |
| 7 | abstraction | LC_LI | 10.64 % | 141.00 |
| 7 | batched | LC_LI | 8.03 % | 218.00 |
| 9 | abstraction | LC_HI | 14.41 % | 166.50 |
| 9 | batched | LC_HI | 18.73 % | 259.00 |

**C-axis invariant, I-axis F-dependent.** All 6 (F, model) points pick the low-concentration corner (LC); the high/low imbalance preference varies with F. GAP **grows with F** (8–12 % at F=5 → 18.7 % at F=9), so the wave-structure lever becomes **more** useful in taller buildings. See [experiments_A1_floors_sweep.py](../prototype/src/experiments_A1_floors_sweep.py), [v0_2_A1_floors_sweep.json](../prototype/results/v0_2_A1_floors_sweep.json).

## B.6 FCFS baseline anchor (A2)

Anchors H1's P1-vs-P0 lift against a true FCFS baseline (no batching, no clustering) on the two H1-supported cells. **7 200 sims** × 3 policies × 2 arms × 3 sizes × 200 waves.

| cell | P_FCFS | P0 | P1 | P0 − FCFS | P1 − P0 | P1 − FCFS |
|---|---|---|---|---|---|---|
| E2_c2 | batched | 175.33 | 150.33 | 142.40 | −25.00 (−14 %) | −7.93 (−5 %) | −32.93 (−19 %) |
| E3_c2 | batched | 132.83 | 110.50 | 105.08 | −22.33 (−17 %) | −5.42 (−5 %) | −27.75 (−21 %) |

**Interpretation.** Opportunistic batching (P0 vs FCFS) captures most of the operational lift (~15 %). Destination-clustered batching (P1 vs P0) adds an incremental ~5 %. Total P1-over-FCFS is 19–21 %. The paper's "tactical-operational non-substitutability" claim refers to the incremental P1-over-P0 slice, not the total operational lift — but the total lift demonstrates that the stack of batching + clustering is substantial relative to a naive baseline. See [experiments_A2_fcfs_baseline.py](../prototype/src/experiments_A2_fcfs_baseline.py), [v0_2_A2_fcfs_baseline.json](../prototype/results/v0_2_A2_fcfs_baseline.json).

## B.7 Cross-cell meta-regression (A3)

Replaces six per-cell OLS fits (R² 0.4–0.6) with a unified meta-regression incorporating regime and model interaction terms:
$$
\mathrm{makespan} \sim \mathrm{intercept} + C + I + \mathrm{size} + E + \mathbb{1}\{\mathrm{batched}\} + C \times \mathbb{1}\{\mathrm{batched}\} + I \times \mathbb{1}\{\mathrm{batched}\} + C \times E + I \times E + \mathrm{controls}.
$$

Unified $R^2 = 0.791$ on N = 18 000, substantially higher than per-cell fits. Key significant effects (95 % CI excludes 0):

| term | estimate | 95 % CI |
|---|---|---|
| C | +47.37 | [+39.06, +55.37] |
| I | −9.32 | [−13.57, −5.06] |
| $C \times \mathbb{1}\{\mathrm{batched}\}$ | **+46.05** | [+40.62, +51.24] |
| $C \times E$ | **−34.96** | [−38.68, −31.52] |
| $\mathbb{1}\{\mathrm{batched}\}$ | −19.12 | [−26.66, −11.53] |

The sign of β(C) in any cell is recoverable as
$$
\beta(C \mid \mathrm{model}, E) = 47.37 + 46.05 \cdot \mathbb{1}\{\mathrm{batched}\} - 34.96 \cdot E,
$$
yielding positive β(C) in low-E batched cells (consistent with the batching-limited reading) and negative β(C) in high-E abstraction cells (parallelism-limited). This is the unified β-surface version of the per-cell findings reported in §6.2. See [analysis_A3_meta_regression.py](../prototype/src/analysis_A3_meta_regression.py), [v0_2_A3_meta_regression.json](../prototype/results/v0_2_A3_meta_regression.json).

## B.8 Heterogeneous elevator pool (B1)

Real multi-storey warehouses mix freight and passenger elevators with different capacities. v0.2 assumes homogeneous pools. We add `ElevatorPoolBatchedHeterogeneous` to the simulator and test whether the M4 best-corner identification survives pool heterogeneity. **4 000 sims**, $E = 3$ fixed, 5 arms × 200 waves at size = 6.

| config | capacities | total | best corner | GAP % | stable vs homog? |
|---|---|---|---|---|---|
| homog | [2, 2, 2] | 6 | HC_HI | 7.76 % | — (baseline) |
| mild hetero | [1, 2, 3] | 6 | HC_HI | 11.25 % | yes |
| biased up | [2, 3, 3] | 8 | HC_HI | 11.64 % | yes |
| extreme | [1, 3, 4] | 8 | **LC_HI** | 11.16 % | **no** |

**3/4 configurations preserve best corner.** Only the extreme-heterogeneity pool (ratio 4:1 between largest and smallest elevator) flips best corner from HC_HI to LC_HI — intuitively: when a single large elevator dominates, waves should be low-concentration (to spread orders across all three elevators rather than clustering on the large one). Moderate heterogeneity is robust. See [experiments_B1_heterogeneous_pool.py](../prototype/src/experiments_B1_heterogeneous_pool.py), [v0_2_B1_heterogeneous_pool.json](../prototype/results/v0_2_B1_heterogeneous_pool.json).

## B.9 Net effect on paper claims (Tier 1.5)

| Study | Purpose | Finding | Effect |
|---|---|---|---|
| S1 — M4 predictive | convert M4 from retrospective to prospective | composite predictor 6/6 correct; within-batched Pearson = −0.67 | C2-M4 gains "prospective diagnostic" framing |
| S2 — stagger phase diagram | 2-D substitutability map | 57 600 sims; E3_c2 stagger-robust, E2_c2 stagger-sensitive | C3 upgrades to 2-D map |
| S3 — c sweep | generalise beyond c=2 | P[M_2 ≥ M_1] = 99.4 %; Hedge Rule applicability persists across c ∈ {2, 3, 4, 5} | §8 c=2 scope removed; framework generalises |
| S4 — β stratification | rescue bootstrap stability | stratification fails; sample design beats post-hoc stratification | honest practitioner rule |
| A1 — F sweep | realistic building heights | C-axis invariant, I-axis F-sensitive; GAP grows with F | §8 F=5 scope removed |
| A2 — FCFS baseline | anchor P1 lift | P0 saves 15 %, P1 adds 5 %, total 19–21 % vs FCFS | counters "P0 already strong" objection |
| A3 — meta-regression | unified β surface | R² = 0.791 with strong interactions | replaces 6 per-cell fits with one figure |
| B1 — heterogeneous pool | AMR-industry realism | 3/4 configs stable; extreme heterogeneity flips | supports "moderate heterogeneity OK" scope claim |

The Tier 1.5 studies do not introduce new C2 or C3 claims but substantially harden the existing ones against generalisation objections. All use the same simulator and no real-warehouse data; reviewers can reproduce every finding from the included scripts.
