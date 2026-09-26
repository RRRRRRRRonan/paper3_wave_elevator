---
title: "Pre-registered amendment F (2026-07-08): test-retest reliability and wave-budget study"
parent: "paper_draft/phase5_scaleup_preregistration.md (LOCKED 2026-05-19); idea #4 of CONTRIBUTION-IDEAS-2026-07-08.md"
date: 2026-07-08
status: "DRAFTED AND DATED BEFORE EXECUTION. Registers replicate seeds, statistics, gates, and the sub-sampling grid BEFORE any simulation."
author_signoff: "SIGNED (Shiyue Hu, 2026-07-08). Authorization given by explicit author instruction in the 2026-07-08 working session (recorded in EXECUTION-LOG.md); countersigned by the assistant on the author's behalf. The author retains the final pre-submission read of every locked rule."
---

# Amendment F: seed-level reliability of the Bound-and-Gap diagnostic

## Design (locked)

- Scope: ALL 18 publication-scale configs (decided here, before running;
  compute is trivial on this simulator).
- R = 8 independent replicates. Replicate r (r = 1..8) reruns the COMPLETE
  Block-A diagnostic pipeline with base seed S_r = 20260800 + r replacing
  SEED_BASE everywhere (order pool seed S_r + config_id; candidate/train/
  arm/sim seeds via the harness _seed() formula with S_r as base). Seeds
  are disjoint from Phase 5 (20260519) and amendments A/B (20260708/9).
- Per replicate and config, TWO measurands:
  (i) truncated-corner Phi-rule capacity share: mean over the 4
      (model, size) sub-cells of H_up/(H_up + M_Phi), Block-A protocol
      (5 arms x 200 waves, models {M1, M2}, sizes {8, 30},
      favorable_corner refit per replicate);
  (ii) covering 2x2 median-split share H_up/UB on a 2,000-wave random
      sample at size 16 under M2 (b13-style; the guarantee-bearing metric
      per Theorem R). Added per the idea-#1 review decision.
- Sub-sampling grid (measurand i recomputed using the first N waves per
  arm): N in {50, 100, 200}. 400 is not available (200 waves per arm);
  the grid is locked as stated.
- Runtime: wall-clock per replicate diagnostic logged (free by-product,
  closes the runtime-reporting blind spot).

## Statistics (locked)

Per measurand: ICC(2,1) (two-way random effects, absolute agreement,
config x replicate matrix), SEM = SD_within * sqrt(1 - ICC), minimum
detectable difference MDD95 = 1.96 * sqrt(2) * SEM, and per-config verdict
unanimity (capacity-dominant iff share > 0.5; unanimous = same verdict in
8/8 replicates). Wave-budget N* per config = smallest N in the grid at
which the verdict matches the N = 200 verdict in all 8 replicates
(descriptive).

## Gates (locked)

- "Reliable in resolved regimes": ICC(2,1) >= 0.75 for measurand (i)
  computed over the RESOLVED configs (fixed ex ante: configs with >= 3/4
  sub-cells D1-d resolved in the stored Phase 5 blockA artefact; per
  v0_5_phase5_blockA.json that set is
  {0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 13, 14, 15, 16}, 15 configs;
  excluded: 9 (1/4), 10 (2/4), 17 (2/4)) (pre-execution correction
  2026-07-08: an earlier draft of this file misquoted the set as 8
  configs; corrected against the artefact before any simulation ran),
  AND verdict unanimity in >= 15/18 configs.
- Any outcome is reported as measured; low ICC triggers the pre-committed
  reading "the sub-sampling curve gives the wave budget N* that restores
  reliability", not a wording retreat elsewhere. H-D1/H-D2 verdicts are
  not re-judged.

## Disclosures

Replicates run on the CURRENT production simulator, i.e. before the B-14
tie-break stabilization; the heap-dependent tie exposure documented in
BUGREPORT-2026-07-08 applies to all replicates equally and is part of what
"test-retest under operational conditions" measures. Pool-size sensitivity
is OUT of scope (B-6 ii).
