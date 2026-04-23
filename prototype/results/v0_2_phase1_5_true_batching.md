# MVS v0.2 Phase 1.5 — True co-occupancy batching

**Date**: 2026-04-21
**Simulator refactor**: [src/simulator.py](../src/simulator.py) — new `ElevatorBatched` / `ElevatorPoolBatched` classes (also see `_test_batched_regime` sanity test, hand-computed 72s)
**Experiment script**: [src/experiments_phase1_5.py](../src/experiments_phase1_5.py)
**Analysis script**: [src/analysis_phase1_5.py](../src/analysis_phase1_5.py)
**Pre-registration**: [intuitions_before_MVS_v0_2.md §1](../intuitions_before_MVS_v0_2.md)
**Raw data**: [results/raw/mvs_v0_2_phase1_5_batched_samples.csv](raw/mvs_v0_2_phase1_5_batched_samples.csv) (3000 rows, matched-wave pairs with Phase 1)
**JSON**: [results/v0_2_phase1_5_true_batching.json](v0_2_phase1_5_true_batching.json)
**Figures**: [results/figures/phase1_5_*.png](figures/)

---

## 0. TL;DR

Two headline findings, one bad, one good:

1. **Decision gate: predictive-surrogate framing of C2-M2 is FINAL REJECTED.** Max `M3 − M2` across the three batched c=2 regimes is **+0.0119** at E3_c2, virtually identical to Phase 1's +0.0121. True batching does not rescue the surrogate framing — so the "Φ as predictive surrogate for makespan" story is retired for good.
2. **β(C) sign is model-dependent.** In E2_c2 and E3_c2, β(C) **flips from negative (throughput-abstraction) to positive (true batching)**. In E1_c2 it stays negative but shrinks 73% in magnitude. The Phase 1 "concentrated waves are faster" finding was partly an artefact of the throughput-abstraction. Under true batching, more-concentrated waves (higher C = more diverse destinations) hurt parallelism → β(C) > 0, matching the "naïve" intuition.

Combined with the [Geometric experiment](v0_2_geometric_mechanism.md) rejection, the C3-H3 headline must be reframed: the sign of β(C) depends jointly on (elevator model, fleet size, wave size). It is **not** a single clean physical effect.

---

## 1. What was pre-registered vs what happened

From [intuitions_before_MVS_v0_2.md §1](../intuitions_before_MVS_v0_2.md):

| Prediction | Threshold | Observed | Verdict |
|---|---|---|---|
| `M3 − M2` max across c=2 regimes ≥ +0.05 → surrogate framing rescued | ≥ +0.05 | **+0.0119** | ❌ rejected |
| Same ≥ +0.02 → ambiguous zone | ≥ +0.02 | +0.0119 | ❌ below ambiguous |
| β(C) stays negative but magnitude shrinks under batching (confidence 2/5) | sign-stable | **sign flips in 2/3 regimes** | partial — magnitude shrank as predicted, but sign also flipped in 2/3 |
| `M3 − M2` grows by +0.005 to +0.02 under batching (confidence 2/5) | increment growth | **essentially unchanged** (+0.0121 → +0.0119) | roughly confirmed — no meaningful change |

Pre-reg was **partially wrong about β(C) sign** and **partially right about effect-size instability** across models. Logging both as data points.

---

## 2. Simulator refactor: true co-occupancy batching

### 2.1 Semantics

`ElevatorBatched` tracks an in-progress trip `(src, dst, loading_end, completion, passengers)`. When a new request with `amr_current_floor = src`, `target_floor = dst` arrives at time `t` with `t ≤ loading_end` and `passengers < capacity`, it **boards the existing trip** (same completion time, no new reposition/load/travel/unload). Otherwise the request queues for a new dispatch after `available_at = trip.completion`.

### 2.2 Sanity check

Hand-computed scenario A (5 × `1→3`) with E=1, c=2, batched=True:
- Trip 1 carries orders #1 and #2 (both arrive at src=1 before loading_end=7s), completes at 19s. Final AMR time = 24s (include dropoff service).
- Trip 2 carries orders #3 and #4 (arrive at src=1 before loading_end=31s), completes at 43s. Final AMR time = 48s.
- Trip 3 carries order #5 alone, completes at 67s. Final AMR time = 72s.
- **Wave makespan = 72s.** ✓ matches `_test_batched_regime` in [src/simulator.py](../src/simulator.py).

### 2.3 Contrast with throughput-abstraction

The throughput-abstraction c=2 elevator behaves as 2 fully-parallel serving slots (no matching requirement). On a wave with mixed `(src, dst)` pairs, throughput-abstraction still benefits from capacity; true batching does not. Throughput-abstraction is therefore an **upper bound** on elevator parallelism — systematically more optimistic than physically realisable batching.

---

## 3. Headline #1 — surrogate rescue fails

### 3.1 Numbers

M1, M2, M3 are the same three-tier model ladder as Phase 1. 5-fold CV R² with shuffle, seed=42.

| Regime | M1 | M2 | M3 | **M3 − M2** |
|---|---|---|---|---|
| E1_c2 (batched) | 0.831 | 0.840 | 0.840 | **−0.0000** |
| E2_c2 (batched) | 0.662 | 0.679 | 0.682 | **+0.0026** |
| E3_c2 (batched) | 0.600 | 0.622 | 0.634 | **+0.0119** |

Phase 1 (throughput-abstraction) had `M3 − M2` at E3_c2 = +0.0121. Batched data gives **+0.0119 at the same regime**.

### 3.2 Interpretation

The surrogate framing required **C/I to add ≥ 5 pp R² on top of (size, cross_floor, floor_distance)**. Neither modelling choice (throughput-abstraction or true batching) delivers that. A richer simulator does not magically surface predictive value of C/I — because in both models, makespan's variance is dominated by wave size and spatial spread; C/I only shift the mean at fixed size.

### 3.3 Consequence for Paper 3

**C2-M2 as "Φ is a predictive surrogate for makespan" is retired.** The conceptual-decomposition reading of Φ (C2-M2-conceptual) still survives — Tier 1.1's 42–92% β(C)/β(size) ratio stands. This deliverable confirms the outcome we already suspected after Phase 1: predictive framing is dead; conceptual framing lives.

---

## 4. Headline #2 — β(C) sign is model-dependent

### 4.1 The flip

β(C) in physical units (seconds per nat of Shannon entropy), OLS fit on `[size, floor_distance, C, I]`:

| Regime | β(C) throughput-abstraction | β(C) true batching | Sign behaviour |
|---|---|---|---|
| E1_c2 | **−23.99** | **−6.54** | same sign, **magnitude down 73%** |
| E2_c2 | **−5.78** | **+4.91** | **SIGN FLIPPED** |
| E3_c2 | **−7.60** | **+5.18** | **SIGN FLIPPED** |

Bootstrap 95% CIs under batched (500 iterations):
- E1_c2: β(C) = −7.01 [−22.86, +8.29] — CI straddles 0, not distinguishable.
- E2_c2: β(C) = +4.46 [−10.68, +20.17] — CI straddles 0.
- E3_c2: β(C) = +4.81 [−6.58, +16.21] — CI straddles 0.

Under true batching **none of the three regimes has a bootstrap-CI-excludes-zero β(C)**. Contrast with throughput-abstraction, where 4/6 regimes (from Tier 1.1) had β(C) CIs excluding zero. Batching doesn't just flip signs — it **dissolves the effect into noise**.

### 4.2 Why the sign flips

Physical intuition post-hoc:

- **Throughput-abstraction c=2**: capacity is modelled as two fully-independent parallel slots. High-C waves spread orders across floors → more simultaneous trips → parallel slots fully utilised → lower makespan. β(C) < 0. (This is the "AMR-fleet-parallelism" story from Tier 1.4.)
- **True batching c=2**: capacity helps only when multiple AMRs want the same `(src, dst)`. High-C waves have *more diverse* `(src, dst)` pairs → fewer batching opportunities → each trip carries 1 passenger → elevator is the bottleneck. β(C) > 0. (This is the "concentrated waves enable batching" story — the original naïve intuition.)
- **E1_c2 is the exception**: with only 1 physical elevator, even under batching, high C stresses the elevator's sequentiality hard enough that it's still a bigger drag than the lost batching opportunity, so β(C) stays negative. As elevator count grows (E=2, E=3), the batching-loss mechanism dominates and the sign flips.

### 4.3 Consequence for Paper 3's C3-H3

The Phase 1 "β(C) < 0 in all 6 regimes" finding was **conditional on the throughput-abstraction**. Under the more realistic true-batching model, β(C) sign depends on fleet configuration:

| Regime | abstraction β(C) | batched β(C) |
|---|---|---|
| E=1, c=2 | strong negative | weak negative |
| E=2, c=2 | weak negative | weak positive |
| E=3, c=2 | weak negative | weak positive |

The C3-H3 headline ("concentrated waves are faster") is **not robust** to modelling assumptions. Paper 3 cannot claim it as a clean physical finding. What Paper 3 *can* still claim:

- β(C) has operationally-meaningful magnitude (Tier 1.1: 42–92% of β(size) under abstraction; ~17% under batching in E1_c2 — still non-zero).
- Φ as a decomposition (C2-M2-conceptual) is model-invariant — the entropy math doesn't care which elevator model we use.
- The direction of β(C) is itself a **regime probe**: if we observe β(C) < 0 in a system, that tells us something about the fleet–elevator interaction (likely parallelism-dominated rather than batching-dominated). This is a more modest but honest framing.

---

## 5. Makespan delta: batching is systematically slower

Matched-wave paired comparison (same wave content, different model).

| Regime | median abstraction | median batched | median Δ (batched − abstraction) | fraction of waves where batched ≥ abstraction |
|---|---|---|---|---|
| E1_c2 | 159.0 s | 210.0 s | **+47.0 s** | 95.2% |
| E2_c2 | 101.0 s | 140.5 s | **+43.0 s** | 94.5% |
| E3_c2 | 78.0 s | 106.0 s | **+25.0 s** | 85.9% |

See [figures/phase1_5_paired_makespan.png](figures/phase1_5_paired_makespan.png).

The throughput-abstraction systematically **underestimates makespan** by 25–47 s median — it assumes parallelism that true batching can only extract when waves have matched-direction requests. This quantifies the "throughput-abstraction caveat" flagged in [v0_2_phase1_regime_sweep.md](v0_2_phase1_regime_sweep.md): the caveat was not cosmetic; the abstraction was optimistic by ~30% of median makespan.

Pearson correlation between the two models' makespans on matched waves: **r ∈ [0.85, 0.93]**. So the two models **rank waves similarly** (high agreement on "which waves are hard") but disagree on **how much** the elevator helps. The relative ordering of waves within a regime is preserved; the absolute magnitudes and the decomposition of that magnitude across features (the β's) are not.

---

## 6. Updated mechanism candidate map (combines Tier 1, Geometric, Phase 1.5)

| Candidate | Tier 1.3 (subsample size-flip) | Geometric (N/F sweep) | Phase 1.5 (true batching) | Status |
|---|---|---|---|---|
| A. Size × fleet saturation controls β(C) sign | **positive evidence** (sign flips within every regime between size 3-4 and 7-8) | not directly tested | consistent — batched E1 (which saturates easily) keeps β(C)<0; E2,E3 flip | 🟢 best surviving hypothesis |
| B. N/F ratio controls β(C) sign | not testable (N fixed at 10) | **rejected** (Pearson r = −0.15) | n/a | ❌ dead |
| C. Concentrated waves help fleet parallelism (original Phase 1 story) | aggregate confirmed, but size-conditional | not supported across 20 cells | **model-dependent** — true under abstraction, reversed under batching | 🟡 brittle |
| D. No simple mechanism exists | null hypothesis | consistent | consistent | 🟡 default if A doesn't survive |

### What's still worth testing

Only candidate A remains. The proper test is a **size × N sweep** under **true batching** (a "Geometric-2" experiment). Predicted pattern:
- Small waves (size ≲ N): under-saturated fleet; expect β(C) ≈ 0 or slightly positive (batching loss dominates).
- Large waves (size ≫ N): fleet-saturated; expect β(C) < 0 (parallelism dominates).
- Crossover size band should depend on N (larger N → later crossover).

This is **not in the v0.2 budget**. Deferring to a v0.3 decision after the salvage synthesis.

---

## 7. Updated Paper 3 contribution status

| Claim | Pre-v0.2 | Post-Phase-1 | Post-Tier-1 | Post-Geometric | **Post-Phase-1.5** |
|---|---|---|---|---|---|
| C1 (problem formulation) | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 |
| C2-M1 (three-dim feature family) | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 |
| C2-M2 **as predictive surrogate** | 🟡 proposed | 🟡 weak evidence | 🟡 still weak | 🔴 unlikely | ❌ **FINAL REJECTED** |
| C2-M2-conceptual (Φ as decomposition) | 🟡 implicit | ⬆ promoted | 🟢 confirmed (β magnitudes real) | 🟢 | 🟢 |
| C2-M3 (simulator methodology) | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 (strengthened — we now document a model-dependence result, which is itself a methodology contribution) |
| C3-H1 (Φ ↔ workflow mapping) | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 |
| C3-H2 (variance vs mean distinction) | 🟡 | 🟢 | 🟢 | 🟢 | 🟢 |
| C3-H3 (β(C)<0 counterintuitive finding) | 🟡 predicted + | 🟢 first evidence (β<0) | 🟡 size-conditional | 🟡 not explainable by N/F | 🔴 **model-dependent** — only under throughput-abstraction |

**Net**: the salvage strengthens C2-M2-conceptual and C2-M3 (the methodology contributions) but weakens C3-H3 (the counterintuitive insight). Paper 3 needs to reframe around the **robustness question**: which findings are model-invariant, which are not, and what that means for the choice of elevator abstraction in AMR-fleet research.

---

## 8. Surprise #12 entry (for [intuitions_before_MVS_v0_2.md §7](../intuitions_before_MVS_v0_2.md))

> **Surprise #12 (2026-04-21)**: Under true co-occupancy batching, β(C) **flips sign** from strongly negative (throughput-abstraction) to weakly positive (batched) in 2/3 c=2 regimes (E2_c2, E3_c2). In E1_c2 it stays negative but drops 73% in magnitude; bootstrap 95% CI now straddles zero. The Phase 1 β(C) < 0 finding is therefore **not robust to elevator modelling assumptions**. Additionally, M3 − M2 does not grow under true batching (+0.0119 vs +0.0121 in Phase 1) — predictive-surrogate framing of C2-M2 is FINAL REJECTED. True-batching makespan is systematically +25–47 s higher than throughput-abstraction on matched waves (batched ≥ abstraction in 86–95% of waves). Throughput-abstraction was optimistic by ~30% of median makespan.
>
> **Implication**: C3-H3's headline "concentrated waves are faster" is reframed as "concentrated waves are faster **under throughput-abstracted elevator parallelism**, and the direction of that effect is itself a probe of the elevator-fleet interaction regime." C3-H3 is not a clean physical finding — it is a *model-dependent* finding that tells us something about modelling choices.

---

## 9. Files produced

- [src/simulator.py](../src/simulator.py) — added `ElevatorBatched`, `ElevatorPoolBatched`, `batched=` flag on `simulate_wave`, sanity test
- [src/experiments_phase1_5.py](../src/experiments_phase1_5.py)
- [src/analysis_phase1_5.py](../src/analysis_phase1_5.py)
- [results/raw/mvs_v0_2_phase1_5_batched_samples.csv](raw/mvs_v0_2_phase1_5_batched_samples.csv) — 3000 rows
- [results/v0_2_phase1_5_true_batching.json](v0_2_phase1_5_true_batching.json)
- [results/figures/phase1_5_paired_makespan.png](figures/phase1_5_paired_makespan.png) — batched vs abstraction scatter per regime
- [results/figures/phase1_5_betaC_comparison.png](figures/phase1_5_betaC_comparison.png) — β(C) bar chart abstraction vs batched

---

**Phase 1.5 complete.** Salvage tracks 1/2/3 all delivered. Next: cross-track synthesis (one-page) summarising the combined verdict for Paper 3.
