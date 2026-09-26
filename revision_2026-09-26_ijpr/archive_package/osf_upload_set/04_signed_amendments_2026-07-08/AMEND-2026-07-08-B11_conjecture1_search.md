---
title: "Pre-registered amendment B-11 (2026-07-08): certified instance search for Conjecture 1"
parent: "paper_draft/phase5_scaleup_preregistration.md (LOCKED 2026-05-19); idea #2 of CONTRIBUTION-IDEAS-2026-07-08.md; W3_prop2_induction.md Remark X.3"
date: 2026-07-08
status: "DRAFTED AND DATED BEFORE EXECUTION. Registers the instance class, enforcement protocol, classifiers, fidelity gate, and reporting rules BEFORE the search runs."
author_signoff: "SIGNED (Shiyue Hu, 2026-07-08). Authorization given by explicit author instruction in the 2026-07-08 working session (recorded in EXECUTION-LOG.md); countersigned by the assistant on the author's behalf. The author retains the final pre-submission read of every locked rule."
---

# Amendment B-11: certified enumeration for the E >= 2 chain-dominance question

## Question

W3's Proposition 2 (restated) proves chain dominance under (a),(b),(c*),(d);
at E = 1 the weaker (a),(b),(c),(d) suffice. Remark X.3 leaves OPEN whether
per-trip condition (c) (plus (d)) suffices at E >= 2. This search settles the
question over a certified finite instance class, or exhibits Example X.3.

## Instance class (locked)

Common: floors 1..6, all AMRs / M1 slots / M2 elevators start at floor 1,
availability 0; service_time 5 s; c = 2; policy fifo; deterministic models
M1 (E*c single-rider slots) and M2 (E batching elevators); order pairs
(s, d) with s != d (30 pairs); first order release r1 = 0 always.

- Class W2 (exhaustive): |wave| = 2, ordered pairs 30^2, r2 in
  {0,1,2,3,4,5,7,10}, n_amrs in {1,2}, E in {1,2}.        28,800 instances.
- Class W3 (exhaustive): |wave| = 3, ordered 30^3, (r2, r3) in {0,2,5}^2,
  n_amrs in {1,3}, E in {1,2}.                          1,944,000 instances.
- Class W4 (seeded sample): |wave| = 4, N = 150,000 instances sampled with
  numpy default_rng(20260708): orders uniform over 30^4, (r2,r3,r4) uniform
  over {0,1,2,3,5,7,10}^3, n_amrs uniform {1,2,4}, E uniform {1,2}.

> **Dated correction (2026-07-08, post-execution, factual)**: the W3 count
> above is an arithmetic error in this registration document. The locked
> class DEFINITION (the enumerated sets, unchanged) yields
> 30^3 x 9 x 2 x 2 = 972,000 instances, not 1,944,000; the census total is
> therefore 1,150,800, not 2,122,800. The class as executed is exactly the
> class as registered; only the derived count stated here was wrong.

## Enforcement protocol (locked)

Per instance: (1) run M2 with the FREE earliest-available-AMR rule
(min (current_time, id)), record its order-to-AMR assignment; (2) replay
BOTH models under that recorded assignment (hypotheses (a) and (b) enforced
by construction; the M2 replay is identical to its free run).

## Classifiers (locked; evaluated on the enforced pair)

- (c) per-member: every M2 trip carrying k >= 2 requests with shared
  completion T satisfies T >= D_M1(r) for each member r.
- (c*): every boarded request r satisfies D_M1(r) <= y_(1), the smallest M2
  elevator availability recorded immediately before r's dispatch step.
- (d): every request served fresh in both models satisfies
  reposition_M1(r) <= reposition_M2(r) (floor distance of the actually
  selected serving unit to the request origin).
- Violation: C_max(M1) > C_max(M2) + 1e-9.

## Fidelity gate (locked; runs BEFORE the census)

The search uses a mirror implementation of simulate_wave's fifo walk with
event logging. On 2,000 random FREE-assignment instances drawn from the
class (seed 20260708), the mirror's makespan must equal
src.simulator.simulate_wave to within 1e-9 under BOTH models. Any mismatch
HALTS the census; the mirror is fixed and the gate re-run before any census
result is looked at.

## Locked reporting rules

1. E = 1 self-test: instances with (a),(b),(c),(d) enforced/holding and a
   dominance violation must number ZERO (the E = 1 case is proved). Any hit
   is escalated as a proof-or-implementation discrepancy BEFORE any other
   result is used; the census is not reported until resolved.
2. E = 2, (c)+(d) hold, violation found: Conjecture 1 in its (c)-form is
   REFUTED; the minimal witness (fewest orders, then smallest C_max(M2)) is
   extracted as Example X.3, verified by direct simulate_wave calls, and the
   manuscript ships the (c*) theorem with X.3 completing the necessity
   taxonomy. This outcome is reported as a positive resolution, not a
   failure.
3. E = 2, (c*)+(d) hold, violation found: the drafted general theorem
   (W3-E2) is CONTRADICTED; escalate to the Prong A verification memo; the
   manuscript falls back to the E = 1 proposition + Conjecture 1 wording
   until resolved.
4. No violations under the respective conditions anywhere: the manuscript
   may state "verified by exhaustive enumeration over [the W2/W3 class] and
   150,000 sampled |wave| = 4 instances (2,122,800 instances, both E
   levels)"; the class definition is quoted with the claim. This is a
   certification, not a proof, and is labelled as such.
5. Census counts (violations by condition profile and channel) are reported
   in full whichever way they fall.

## Addendum (2026-07-08, same day, registered BEFORE execution): E = 3 slice

Motivation: the Prong A verification memo (W9) resolves Remark X.3 with a
new Lemma 6, upgrading Conjecture 1 to a theorem for ALL E under
(a),(b),(c),(d). The memo's own computational corroboration was not
persisted as a reproducible artifact; this addendum registers a
reproducible E = 3 corroboration slice using the same fidelity-gated
harness as the main census.

- Class W3E3 (seeded sample): 200,000 instances, E = 3, c = 2, floors 1..6;
  |wave| uniform in {2,3,4}; orders uniform over the 30 pairs; r1 = 0,
  later releases uniform over {0,1,2,3,5,7,10}; n_amrs uniform in
  {1,2,3,4}; numpy default_rng(20260709).
- Fidelity gate: 1,000 free-assignment E = 3 instances vs
  src.simulator.simulate_wave under both models, tolerance 1e-9; mismatch
  halts the slice.

  > **Dated note (2026-07-08, after the first gate run, before any census
  > numbers were looked at)**: the gate FAILED at trial 252 and halted as
  > registered. Root cause: a production defect, heap-dependent tie-breaking
  > by `id(e)` in both elevator pools, documented with an in-process
  > nondeterminism reproduction in
  > `BUGREPORT-2026-07-08_tiebreak_nondeterminism.md` (production itself
  > returns 43.0 or 48.0 for the same wave depending on heap state; the
  > code comment documents index-order intent). The reference
  > implementation for this gate is therefore REDEFINED as production with
  > the one-line index-stable tie-break applied via harness-side
  > monkeypatch (the documented intent); the mirror is unchanged. Follow-up
  > registered as B-14 in the bug report.
- Locked expectations: (i) ZERO dominance violations among instances where
  (c) and (d) hold (the Lemma 6 theorem's prediction); any hit escalates as
  a contradiction of the theorem back to the verification memo before
  anything is reported. (ii) Descriptive: the count of instances where
  boarding occurs with (c) holding but (c*) failing (the coverage gap that
  the Lemma 6 form closes relative to the (c*) form) is reported, whatever
  it is.
