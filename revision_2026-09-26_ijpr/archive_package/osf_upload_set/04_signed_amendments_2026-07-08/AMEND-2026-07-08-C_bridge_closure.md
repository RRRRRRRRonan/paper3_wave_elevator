---
title: "Pre-registered amendment C (2026-07-08): bridge-closure experiments"
parent: "paper_draft/phase5_scaleup_preregistration.md (LOCKED 2026-05-19); ideas #5 and #3 of CONTRIBUTION-IDEAS-2026-07-08.md"
date: 2026-07-08
status: "DRAFTED AND DATED BEFORE EXECUTION. C-1 (P9 SPO+) and C-4 (U_c tightness) registered here; C-2/C-3 reserved."
author_signoff: "SIGNED (Shiyue Hu, 2026-07-08). Authorization given by explicit author instruction in the 2026-07-08 working session (recorded in EXECUTION-LOG.md); countersigned by the assistant on the author's behalf. The author retains the final pre-submission read of every locked rule."
---

# Amendment C: closing the SPO and DRO bridges

## C-1: P9 SPO+ delegation test (idea #5)

**Question**: the manuscript's SPO bridge (demoted Proposition 3) claims the
policy-recoverable slack M_Phi "can be recovered by existing
predict-then-optimize methods". Demonstrate or bound this with ONE
off-the-shelf decision-focused learner.

**Design (locked)**:
- P9 = linear predictor on standardized Phi = (C, I, T) trained with the
  SPO+ surrogate loss (Elmachtoub and Grigas 2022), subgradient
  z*(2c_hat - c) - z*(c) where z* is bottom-k selection.
- Information parity with P5/P6: per Block B cell (6 E=2 configs x sizes
  {8, 30}, model M2), P9 uses the IDENTICAL candidate pool (seed
  _seed(cid, 1, size)) and the IDENTICAL 200-wave simulated training sample
  (Random(seed+1) stream, exactly the fit_predictors draw). No extra
  simulations for training.
- Hyperparameters fixed a priori, no tuning: features standardized over the
  3,000-candidate pool; k_train = 13 (the pool-selection fraction 200/3000
  applied to the 200-wave training sample); step size 0.05; 300 subgradient
  iterations; beta initialized at 0. Registered fallback if the final beta
  is exactly 0: report as such (no second learner is tried).
- Implementation self-test (part of the protocol): before the real gate is
  read, the fitter must recover the correct bottom-k selection on synthetic
  data whose cost is exactly linear in the features (5 trials, in-sample
  and out-of-sample overlap reported).

  > **Dated note (2026-07-08)**: the first run of this protocol FAILED the
  > implementation self-test (bottom-k overlap 0.00, |beta| divergent): the
  > subgradient update had the wrong sign (gradient ascent). The sign was
  > corrected, the self-test re-run, and the census re-executed. The first
  > run's adverse numbers (median R = -4.31) are an artifact of the
  > defective learner, are superseded, and are retained in the execution
  > log for audit. No hyperparameter, seed, or gate was changed.
- Deployment: P9 selects the 200 lowest-predicted waves from the full pool;
  each selected wave simulated under M2 with the Block B sim-seed pattern
  at policy index 8 (seed + 13*9 arm stream, seed + 2003 + 8 sim stream).
- Reference quantities per cell from the stored Block A raw CSV (model
  batched, same candidate pools): m_fav (favorable-corner arm median),
  m_qmin (oracle-corner arm median), m_0 (random arm median).

**Metric (locked)**: per cell, recovery fraction
R = (m_fav - m_P9) / (m_fav - m_qmin), with m_P9 the median of P9's 200
evaluated waves. Reported unclipped; R > 1 (beyond the partition-constant
budget) is reported as such and never becomes a new headline. Cells where
m_fav = m_qmin (zero budget) are excluded from gates and listed.

**Gates (locked wording ladder)**:
- median R >= 0.5 over gated cells AND R > 0 in >= 10/12: the manuscript
  may say "M_Phi is recoverable by an off-the-shelf predict-then-optimize
  method".
- 0 < median R < 0.5: "partially recoverable".
- otherwise: the bridge is scoped as a positioning identity and the adverse
  result reported in section 6.
- P9 NEVER enters the pre-registered H-Policy win matrix or any Phase 5
  verdict; it gets its own exhibit beside Table 4. Descriptive extras
  (P9-vs-P5/P6 win counts, runtime per fit) reported without gates.

## C-4: realized price of robustness and U_c tightness (idea #3)

**Design (locked)**:
- Data: stored Block C matched waves (configs {1,3,5,7,9,11}, size 16,
  arms = 4 corners) for M1/M2; ONE new matched-wave sweep for M3 with
  sigma in {0.1, 0.2, 0.3} on the same waves and seed pattern
  (seed + 700_003 + model_idx*9973 + wid, model indices 3/4/5 for the
  three sigmas), ~43,200 new sims.
- Per config and per true model theta in {M1, M2, M3(0.1), M3(0.2),
  M3(0.3)}: corner medians m_q(theta); regret(rule, theta) =
  (m_{q_rule}(theta) - min_q m_q(theta)) / m_0, with m_0 the config's
  random-arm M2 median (blockC convention). Rules compared on identical
  data: Hedge (argmin under M2), oracle-M1 corner, equal-weight
  average-model corner.
- Realized price of robustness per config = max over theta of
  regret(Hedge, theta). Tightness ratio tau = realized price / U_c(0.05)
  (blockC.py:53 implementation unchanged).
- eps sensitivity grid registered now: eps in {0.02, 0.05, 0.10} reported
  descriptively; the gate uses eps = 0.05 only.

> **Dated note (2026-07-08, after the reconstruction fidelity check halted
> the first C-4 run, before any tightness number was computed)**: the
> reconstruction check found 30-32 mismatches out of 12,000 (varying
> BETWEEN reconstruction runs), ALL in M2, concentrated in configs 1/5/7.
> M1 matched 12,000/12,000 exactly, which pins the wave compositions and
> the seed streams as correct; the M2 discrepancies are the documented
> id(e) tie-break nondeterminism (BUGREPORT-2026-07-08) expressing itself
> in the stored artefact vs fresh processes, and constitute the first
> measured exposure rate (~0.27% of Block C M2 values). Amended data
> policy, fixed before computing any result: M1/M2 quantities (corner
> medians, m_0, U_c) are taken from the STORED artefact of record; the new
> M3 sweeps run on the reconstructed waves (compositions verified via the
> M1 match); the M2 mismatch count is reported and must stay below 1%
> (else halt). Corner-median stability under the mismatches is verified
> and reported.

**Gates (locked)**: "the certificate is informative" requires
U_c(0.05) >= realized price in >= 5/6 configs (validity) AND
tau in [0.5, 1] (within 2x of realized) in >= 4/6 configs (informativeness).
Only validity failing is reported as a bound violation (would contradict
Corollary 2's premises; escalate to theory). Only informativeness failing:
"valid but conservative certificate", with measured tau. The known
3.4%/3.5% caliber inconsistency is fixed in this exhibit's caption (3.4% =
config 7 Hedge corner LC_HI; 3.5% = config 7 global-max corner LC_LI).
