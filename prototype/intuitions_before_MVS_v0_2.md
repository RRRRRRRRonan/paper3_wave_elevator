# My Intuitions Before MVS v0.2 Phases 1.5 / 2 / 3 / 4 (Pre-registration document)

**Placement**: `F:/paper3_wave_elevator/prototype/intuitions_before_MVS_v0_2.md`
**Status**: Pre-registration — drafted 2026-04-21, after Phase 0 and Phase 1 outcomes.
**Companion**: [intuitions_before_MVS.md](intuitions_before_MVS.md) (closed; covers v0.1 + Phases 0–1).

---

## Why This Document Exists

Phase 0 and Phase 1 of v0.2 produced enough surprises (two sign reversals, one mechanism confirmed in direction but off by an order of magnitude) that my prior intuitions are no longer the right reference for the remaining phases. Continuing to evaluate Phase 2 / 3 / 4 against [intuitions_before_MVS.md](intuitions_before_MVS.md) would be evaluating new evidence against intuitions I have already updated — which destroys the point of pre-registration.

**This document records my updated predictions, conditional on:**
- v0.1 results (recorded in [intuitions_before_MVS.md §8.1–§8.5](intuitions_before_MVS.md#section-8))
- Phase 0 results ([§8.6](intuitions_before_MVS.md#section-86))
- Phase 1 results ([§8.7](intuitions_before_MVS.md#section-87))

**Same commitment as the v0.1 pre-reg**: I will not edit §1–§6 of this document after the corresponding phase runs. Contradictions go in §7 as Surprise #11, #12, ... continuing the v0.1 numbering.

---

## 0. What's already known (recap, do not predict again)

These are facts going into v0.2's remaining phases:

| Fact | Source |
|---|---|
| `size` alone explains 75–90% of makespan variance across regimes | v0.1, Phase 1 |
| Linear and tree models tie at R² ≈ 0.82 on v0.1 data | Phase 0 |
| C×I interaction coefficient ≈ 0 on v0.1 data | Phase 0 |
| C and I are collinear with size+cross_floor in v0.1 | Phase 0 |
| `floor_distance` is a less-collinear baseline than `cross_floor` (corr 0.83 vs 0.97) but still highly collinear with size | Phase 1 |
| β(C) < 0 in all 6 (E, capacity) regimes tested (uniform-floor waves are faster) | Phase 1 |
| β(I) < 0 in all 6 regimes (one-directional waves are faster than balanced) | Phase 1 |
| M3−M2 increment grows monotonically with bottleneck relief (0.0012 → 0.0121, 10×) but never crosses +0.02 | Phase 1 |
| Capacity in current implementation is a throughput abstraction (E=2,c=1 ≡ E=1,c=2) | Phase 1 caveat |

---

## 1. Phase 1.5 — True-batching capacity semantics

**What changes**: replace the throughput-abstraction capacity model with a co-occupancy batching model. When elevator at floor S is requested by AMR_i going to D_i, scan the queue for other AMRs requesting (S → D) with same direction; up to `capacity − 1` of them ride together, sharing one `reposition + load + travel + unload` cycle.

**Re-runs**: regimes E1_c2, E2_c2, E3_c2 (the three capacity > 1 regimes). E*_c1 results unchanged.

### 1.1 Will β(C) flip back positive under true batching?

- [ ] Yes, β(C) becomes positive in c=2 regimes
      - Reasoning: concentrated waves (low C) have more (S,D) duplicates → more batching opportunities → faster
- [x] **β(C) stays negative but the magnitude shrinks**
      - Reasoning: AMR-fleet parallelism (the mechanism behind Phase 1's β(C)<0) is structural; batching helps low-C waves but not enough to overturn the fleet-parallelism advantage of high-C waves. Net: β(C) less negative, still negative.
- [ ] β(C) stays negative with same magnitude
      - Reasoning: throughput abstraction was a faithful proxy for capacity effects on this metric

**Confidence**: 2/5. I can construct plausible mechanisms for all three outcomes.

### 1.2 Will the M3 − M2 increment in c=2 regimes grow under true batching?

- [x] Yes, by **+0.005 to +0.02**
      - Reasoning: true batching makes (S,D) pattern matter more, which is exactly what C and I encode. So C/I should gain marginal predictive power.
- [ ] Yes, by ≥ +0.05 (would push at least one regime over the H_v2.1 threshold)
- [ ] No change or negative (throughput abstraction was already capturing the relevant effect)

**Confidence**: 2/5.

### 1.3 If Phase 1.5 still leaves all increments < +0.05

This is the **decisive negative result** for C2-M2-as-predictive-surrogate. After this, no regime in the tested space rescues the surrogate framing. Locked outcome: commit to Scenario A rescue ([novelty_analysis_and_contribution.md §8](../novelty_analysis_and_contribution.md#L408)).

---

## 2. Phase 2 — Temporal clustering (T)

**Pre-condition**: only run Phase 2 if Phase 1.5 confirms (or not) the C/I sign story. T should be tested **on the regime where C/I are most informative** (currently E3_c2, possibly different after 1.5).

### 2.1 T sign

The original §1.3 prediction was β(T) > 0 (confidence 3) based on queueing theory: concentrated release → burst → queue grows non-linearly. In light of Phase 1's two sign reversals, I'm now less confident this intuition will survive contact with N=10 AMRs and a relieved bottleneck.

- [x] β(T) > 0 (concentrated release → larger makespan)
      - Reasoning: queueing-theory mechanism is robust. The bottleneck-relief regime weakens but does not eliminate it: even with 6 effective slots (E3_c2), 10 simultaneous AMR requests still saturate.
- [ ] β(T) ≈ 0 (no signal in MVS scope)
      - Reasoning: with E3_c2 nearly de-bottlenecked, intra-wave timing might not matter
- [ ] β(T) < 0 (counterintuitive)
      - Reasoning: cannot construct a mechanism, but Phase 1 taught me to leave this open

**Confidence**: 2/5 (downgraded from original 3).

### 2.2 T increment magnitude

Plan threshold: M4 − M3 ≥ +0.03 → H_v2.3 supported.

- [ ] +0.05 or more — strong signal
- [x] **+0.01 to +0.03 — modest**, below threshold but directionally consistent
- [ ] < +0.01 — no signal

**Confidence**: 2/5. Honest position: given Phase 1 incrementals were 10× lower than predicted, my prior on Phase 2 is "small."

### 2.3 If β(T) flips negative

That would be Surprise #11. Mechanism candidate to look for: staggered release lets the elevator/AMR fleet idle between bursts, accumulating slack — waste, not relief.

---

## 3. Phase 3 — Stochastic robustness

Add Gaussian noise σ = 20% μ to `service_time` and `speed_per_floor`. Run on Phase 1.5's "best" regime (highest M3 − M2). 20 replications per wave.

### 3.1 R² degradation

For Phase 1's E3_c2 baseline R² = 0.598 → noisy R² of:

- [ ] 0.55 – 0.60 (small drop, ≤ 0.05)
- [x] **0.45 – 0.55 (moderate drop, 0.05 – 0.15)**
      - Reasoning: 20% noise on per-trip times propagates through ~5–10 trips per wave; CLT keeps the wave-level noise around 5–10%, which absorbs ~10pp of variance previously attributed to features.
- [ ] < 0.45 (severe drop, ≥ 0.15) — would mean v0.2's findings are deterministic-regime-only

**Confidence**: 3/5.

### 3.2 Sign stability for β(C), β(I)

This is the test I most care about — if signs flip under noise, the Phase 1 sign-reversal story is fragile.

- [x] **Both signs stay negative** (the Phase 1 finding generalises)
      - Reasoning: the AMR-fleet-parallelism mechanism is geometric, not timing-related; adding noise to per-trip times shouldn't change which waves run in parallel.
- [ ] β(I) stays negative, β(C) flips positive
      - Reasoning: noise might break parallel coordination, hurting uniform waves more
- [ ] Both signs become indistinguishable from zero (CIs cross 0)
      - Reasoning: the effects were small to begin with

**Confidence**: 3/5.

### 3.3 If signs flip under noise

That would be Surprise #12 and would force pre-Paper-3-draft a Phase 3.5 (interaction of regime × stochasticity) before claiming any C/I sign result.

---

## 4. Phase 4 — Tactical vs operational (H1)

Three arms (per [MVS_v0_2_plan.md §5 Phase 4](MVS_v0_2_plan.md)):
- **Arm A**: 30 orders as one mega-wave to the operational layer
- **Arm B**: same 30 orders manually split into 3 "good" waves (low-C, low-I, low-T deliberate)
- **Arm C**: same 30 orders randomly split into 3 waves

### 4.1 Arm B vs Arm A makespan gap

Plan threshold: ≥ 10% → H_v2.4 supported.

- [ ] ≥ 15% — strong tactical-layer value
- [ ] 5 – 15% — moderate (Arm B beats Arm A)
- [x] **0 – 5%** — small or null gap
      - Reasoning: Phase 1 just told me C and I have very small marginal predictive power even after bottleneck relief. If the surrogate is small, the optimization-over-surrogate is small. **Critically**, the Arm B "good wave" criterion is "low C, low I" — but Phase 1 says β(C) < 0 means HIGH C is faster, and β(I) < 0 means HIGH I is faster. So the plan's "good wave" criterion is exactly backwards.
- [ ] **Negative** (Arm B slower than Arm A) — counterintuitive
      - Reasoning: same as above — if the plan's "good wave" definition is inverted, Arm B will systematically pick worse waves than random Arm C.

**Update to plan §5 Phase 4 Arm B definition**: before running Phase 4, the "good wave" criterion must be **reversed** in light of Phase 1: high C, high I, low T (T direction unchanged from §2). I commit to applying this update to the experiment script before running, and recording the original-vs-updated definition transparently in the Phase 4 deliverable.

**Confidence in 4.1 ranking**: 2/5. The crux is whether wave-composition decisions matter at all when fleet-parallelism dominates the elevator bottleneck.

### 4.2 Arm B vs Arm C (manual vs random tactical)

Even if Arm B vs Arm A is small, Arm B vs Arm C tests whether "knowing C, I, T" gives any tactical advantage over random waves.

- [ ] Arm B beats Arm C by ≥ 5% (knowing the features helps)
- [x] **Arm B beats Arm C by 1 – 5%** (small but positive)
- [ ] Arm B and Arm C are indistinguishable
- [ ] Arm B is **worse** than Arm C (the features are misleading)

**Confidence**: 2/5.

### 4.3 If Arm B is worse than both A and C

This is the **C3-H3 jackpot scenario**: the Φ decomposition gives advice that is actually worse than ignoring it. Would be Surprise #13 and an extremely publishable counterintuitive finding ("interpretable wave features mislead human operators when fleet parallelism dominates"). Low prior probability, high information value if observed.

---

## 5. R² aggregate prediction (Phase 1.5 + Phase 2)

Successor to [intuitions_before_MVS.md §3](intuitions_before_MVS.md). Predictions are for the best regime found in the relevant phase (currently E3_c2).

| Model | v0.1 actual | Phase 1 actual (E3_c2) | My pred for Phase 1.5 (true batching, c=2) | My pred for Phase 2 best regime |
|---|---|---|---|---|
| M1 (size) | 0.752 | 0.584 | 0.55–0.62 | 0.55–0.65 |
| M2 (size + floor_distance) | n/a | 0.588 | 0.56–0.63 | 0.56–0.66 |
| M3 (+C, +I) | 0.817 | 0.600 | 0.58–0.66 | 0.58–0.68 |
| M4 (+T) | n/a | n/a | n/a | 0.60–0.70 |

**Predicted M4 − M3 (T's incremental contribution)**: +0.02 (consistent with §2.2 modest band).

---

## 6. Decision gates I am pre-committing to

| Phase | Metric | Pass threshold | Outcome if fail |
|---|---|---|---|
| 1.5 | best M3−M2 across c=2 regimes | ≥ +0.05 | C2-M2 surrogate framing definitively retired; no further surrogate work in v0.2 |
| 2 | M4 − M3 | ≥ +0.03 | T deferred to v0.3; Φ written as 2D (C, I) decomposition only |
| 3 | R² drop after noise | ≤ 0.10 AND signs stable | If R² OK but signs flip → Surprise #12, escalate. If R² drops > 0.10 → MVS conclusions scoped to deterministic regime in Paper 3. |
| 4 | Arm B − Arm A | ≥ 10% (relative) | C3-H1 deferred to v0.3; Paper 3 reframes as Φ-as-decomposition + C3-H3 only |

I commit to **stopping further v0.2 experiments** after Phase 4 and writing the v0.2 synthesis ([prototype/mvs_results_v0_2.md](mvs_results_v0_2.md)) regardless of which gates pass — even if everything fails, the failure pattern itself is the v0.2 deliverable.

---

## 7. Surprise log slot (to be filled post-phase)

Reserved for Surprise #11+. Numbering continues from [intuitions_before_MVS.md §8.7](intuitions_before_MVS.md) (last Surprise was #10).

(Empty until Phase 1.5 runs.)

---

## 8. Commitment

I commit to:

- [x] Not editing §1–§6 of this document after the corresponding phase runs
- [x] Recording contradictions as Surprise #11, #12, ... in §7 of this document
- [x] Treating any contradiction as a finding, not as a bug — only after sanity checks rule out implementation errors
- [x] Updating Phase 4's Arm B "good wave" criterion in light of Phase 1's sign reversals **before** running Phase 4, and documenting the change transparently
- [x] Stopping v0.2 after Phase 4 deliverables, regardless of outcome — no scope creep into v0.3 mid-sprint

**Signed**: shiyuehu (shiyuehu828@gmail.com)
**Date**: 2026-04-21

---

## 9. Revision Log

- **v0.2.0 (2026-04-21)**: Drafted after Phase 0 + Phase 1 outcomes; signed before Phase 1.5 / 2 / 3 / 4 are run

---

**End of pre-registration v0.2.**
