---
title: "Pre-registered amendment B-13 (2026-07-08): Theorem R validation, nested covering partitions"
parent: "paper_draft/phase5_scaleup_preregistration.md (LOCKED 2026-05-19); idea #1 of CONTRIBUTION-IDEAS-2026-07-08.md"
date: 2026-07-08
status: "DRAFTED AND DATED BEFORE EXECUTION. Registers the simulation protocol and the falsifiable predictions of Theorem R (refinement monotonicity for covering partitions) BEFORE any simulation is run. Absorbs the RECHECK-proposed B-9 (covering-partition H_up >= 0 verification): B-9 is superseded by this item."
author_signoff: "SIGNED (Shiyue Hu, 2026-07-08). Authorization given by explicit author instruction in the 2026-07-08 working session (recorded in EXECUTION-LOG.md); countersigned by the assistant on the author's behalf. The author retains the final pre-submission read of every locked rule."
---

# Amendment B-13: nested covering-partition validation of Theorem R

## Theory being tested (statement registered here; proof drafted separately)

For a finite candidate pool with per-wave makespans and COVERING partitions Q
of the (C, I) plane (every wave assigned to exactly one cell):

- Lemma R.1 (bracketing; = W2's Lemma C.1): min_q m_q <= m_0 <= max_q m_q,
  with m_q the cell median, m_0 the pool median (inf-convention medians at
  population level; empirical check uses np.median with the convention
  footnote inherited from W2).
- **Theorem R (refinement monotonicity)**: if covering Q' refines covering Q,
  then max_q m_q is nondecreasing and min_q m_q is nonincreasing under the
  refinement; hence H_up(Q') >= H_up(Q) >= 0, S_or(Q') >= S_or(Q) >= 0, and
  UB = H_up + S_or is nondecreasing. (H_up = (max_q m_q - m_0)/m_0;
  S_or = (m_0 - min_q m_q)/m_0.)
- Remark R.3 (scope): NO ordering is implied between non-nested partitions
  (e.g. median 2x2 vs tercile 3x3). The A-R1 cross-scheme swings occurred
  between non-nested truncated schemes and are consistent with this.
- Positioning: the paper's FILTER_Q = 0.25 corner scheme equals the four
  corner cells of the covering 4x4 quartile grid with the middle 12 cells
  dropped (contrast-maximizing, non-covering special case).

## Simulation protocol (locked)

- Configs: the six Block C configs (E = 2): config_ids {1, 3, 5, 7, 9, 11}.
- Wave size 16; models M1 (abstraction) and M2 (batched); capacity c = 2.
- Pools and candidates EXACTLY as the Phase 5 harness: generate_pool with
  seed SEED_BASE + config_id; build_candidates(pool, 16, 3000,
  Random(_seed(cid, 99, 16))) with the model-independent Block C seed, so
  waves are matched across models.
- Sample: N = 2000 candidates drawn uniformly without replacement from the
  3000 (numpy default_rng seed 20260708), each simulated once under M1 and
  once under M2 (sim rng seeds: Random(_seed(cid, 99, 16) + 500000 + i) per
  wave i, shared across models so the wave, not the noise, differs).
  Total 6 x 2000 x 2 = 24,000 sims.
- Partitions computed post-hoc on the sample's (C, I):
  - Nested family: Q0 trivial; Q1 = 2x2 split at sample medians;
    Q2 = 4x4 split at sample quartiles (25/50/75). Q2 refines Q1 by
    construction (median is a quartile boundary).
  - Non-nested comparison point: 3x3 tercile grid (reported, explicitly
    outside Theorem R's guarantee).
  - Cells with fewer than 30 sampled waves are flagged "thin" and reported
    but excluded from no check (they stay in; thinness is disclosure only).

## Locked falsifiable predictions

Per (config, model) cell, 12 cells total:

- P1: H_up(Q1) >= 0 and H_up(Q2) >= 0.            [24 checks]
- P2: H_up(Q2) >= H_up(Q1).                        [12 checks]
- P3: S_or(Q2) >= S_or(Q1).                        [12 checks]
- P4 (descriptive, no gate): tercile 3x3 values are unconstrained relative
  to Q1/Q2; any non-monotone position is consistent with Remark R.3.

**Locked adjudication rule**: a violated check whose bootstrap 95% CI of the
violated difference (1000 reps, seed 20260708, resampling waves within cells)
includes 0 is reported as "consistent within sampling noise". A violation
whose CI excludes 0 in the wrong direction FALSIFIES the population-to-sample
transfer for that cell and is reported as such; the population theorem is
unaffected (it is proved, not tested), but the manuscript's empirical
paragraph must then state the observed finite-sample deviation. No wording
about A-R1 or the capacity-share headline changes as a result of this
experiment in either direction: the headline conditionalization stands.

## Reporting

One JSON (b13_theoremR_validation.json), one table, one figure (H_up and
S_or vs nest level per config, nested family as connected points, tercile as
a detached marker). All 48 checks reported pass/noise/fail with counts.
