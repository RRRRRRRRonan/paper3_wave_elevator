---
title: "W9 (Prong A): Independent verification of the W3 request-by-request induction, and resolution of Remark X.3"
date: 2026-07-08
date_note: "aligned to the revision package's provenance date; the original stamp read 2026-07-18 (triple-check consistency finding)"
status: "verification memo; contains a proposed new Lemma 6 that closes the open question, for author review"
adversarial_verification_2026_07_08: >
  Lemma 6 and the case-B corollary SURVIVE dedicated refutation
  (math-breakers workflow wf_f78feb73-6ef): 120,000 coupled walks at
  E in {2,3,4}, c in {2,3}, 201,894 boarding events with per-step checks
  of every inequality in the proof, zero violations; the bound is attained
  with equality and never exceeded; tie-break agnosticism confirmed
  analytically and mechanically (including the Remark X.3 break pattern:
  never approached, max observed count 1 = the lemma's cap). The induction
  components (Lemmas 3-5, cases F/B, condition (d)) also SURVIVE (~1.5M
  further instances). Two presentational fixes required before splicing
  (corollary hypothesis list; the "fix a step k" import sentence): see
  W10 section 2. The B-11 census, its E=3 addendum, and B-1's operational
  measurement independently corroborate (jointly ~1.35M + 200k + 6k
  instances, zero support-set violations). Author duty: read-through of
  section 5.2 plus the W10 fixes.
verified_against: "f:/Paper 3/prototype/src/simulator.py (ground truth for all semantic claims)"
target_document: "f:/Paper 3/revision_2026-07-08/tier1_manuscript/W3_prop2_induction.md (Edits W3-E1 through W3-E5)"
method: >
  Every [VERIFY] tag checked line by line against simulator.py. Lemma 4
  checked by hand on six multisets and by 20,000 randomized cases. The full
  induction stress-tested by an instrumented dual simulator (cross-validated
  against simulate_wave) on 110,000 randomly generated verification waves at
  E in {1,2,3}, c in {1,2,3}, with per-step condition and invariant checks.
  Verification waves are hand-constructed or randomly generated minimal
  instances, neither publication scale nor prototype scale.
harness: "scratchpad/verify_w3.py (session scratchpad; results quoted inline below)"
headline: >
  (1) Every component of Edit W3-E2 is VERIFIED as stated; no false step was
  found. (2) The open question of Remark X.3 is RESOLVED in the positive
  direction: the invariant-breaking state is unreachable. A new counting
  lemma (Lemma 6, "recency of late completions") shows the per-trip
  condition (c) suffices for ALL E, so Conjecture 1 of Edit W3-E4 is
  provable and the (c*) strengthening is unnecessary. (3) One overclaim in
  Edit W3-E5's proposed text must be fixed (ordering frequency is not the
  condition frequency). (4) Minor: the code's availability tie-break is
  id(e)-based, not list-order; the proof is tie-break agnostic but the
  manuscript should state a tie-break convention.
---

# W9: Verification of the Proposition 2 induction (Prong A)

## 1. Per-component verdict table

| # | Component (W3 draft location) | Verdict | Note |
|---|---|---|---|
| 1 | Edit W3-E1, corrected Lemma 2 (server-count bound only) | VERIFIED | Correction is right and necessary; the v1.0 second clause is false (Example X.2 refutes it with zero queueing) |
| 2 | X.4.1 condition (a), common processing sequence | VERIFIED | Stronger than stated: in this sequential simulator the processing sequence is timing-independent by construction, for both fifo and cluster walks |
| 3 | X.4.1 condition (b), common AMR assignment | VERIFIED | Genuine restriction; AMR argmin at line 659 depends on timing |
| 4 | X.4.1 condition (c) per-member form | VERIFIED | Well-defined; covers dispatcher and boarders of every multi-rider trip |
| 5 | X.4.1 condition (c*), and its [VERIFY] tag on board()/available_at | VERIFIED | Lines 178-197: dispatch sets available_at = unloading_end = trip_completion; board() only increments trip_passengers; E = 1 equivalence (c) = (c*) confirmed |
| 6 | X.4.1 condition (d), no adverse repositioning | VERIFIED | Well-defined without any slot-to-elevator matching; see Section 4, question 4, for the tie-break caveat |
| 7 | X.4.1 c = 1 remark (models coincide) | VERIFIED with caveat | True given a common tie-break convention; exact equality in 20,000 random waves; see Section 6.3 |
| 8 | X.4.2 Lemma 3 (structural identity) incl. edge cases | VERIFIED | Lines 663-671; AMR floor after an order equals the order's destination floor in all cases, including src = dst |
| 9 | X.4.3 (I1) from (I2), AMR-side monotonicity | VERIFIED | Lines 659-676: request times are compositions of max-with-constant and plus-constant on earlier completions |
| 10 | X.4.3 Lemma 4 (min-replacement identity), incl. i = n boundary | VERIFIED | Hand-worked multisets in Section 4, question 1; 20,006 cases, 0 failures |
| 11 | X.4.3 Lemma 5 (dominance propagation), E-prefix sufficiency | VERIFIED | The E smallest M1 slots suffice; the (E+1)-th slot enters only inside a min; see Section 4, question 2 |
| 12 | X.4.4 base case | VERIFIED | Pool initial_floor = initial_amr_floor on every construction path (lines 597-631), so all units co-located at availability 0 |
| 13 | X.4.5 case F (fresh-fresh) | VERIFIED | Uses exactly (I1), (I3) coordinate 1, (d), Lemma 1 parity, Lemma 5(i) |
| 14 | X.4.6 case B (M2 boarding) under (c*) | VERIFIED | Needs exactly (c*) and T(tau) >= y_(1); board() leaves the M2 vector unchanged; see Section 4, question 3 |
| 15 | Case F/B exhaustiveness | VERIFIED | ElevatorPool (lines 128-136) has no boarding path |
| 16 | X.4.7 conclusion, makespan monotonicity | VERIFIED | Order finish = last request completion + service constant; monotone |
| 17 | Corollary X.1 (E = 1 under (a),(b),(c),(d)) | VERIFIED | 30,000-wave search at E = 1: (c) and (c*) never disagreed; 0 violations in 1,990 condition-satisfying waves |
| 18 | Corollary X.2 (no-boarding waves) incl. reposition caveat | VERIFIED | Reposition legs call the same pool.request (line 664) and are batchable |
| 19 | Remark X.3 break-state arithmetic | VERIFIED | The four-number instance breaks (I3) exactly as claimed |
| 20 | Remark X.3 open question (does (c) suffice at E >= 2?) | RESOLVED: YES | The break state is unreachable; new Lemma 6 closes case B under (c) for all E; Conjecture 1 is provable. Section 5 |
| 21 | Example X.1 (26 vs 24) | VERIFIED | Reproduced via simulate_wave: M1 = 26.0, M2 = 24.0 |
| 22 | Example X.2 (103 vs 68) | VERIFIED | Reproduced via simulate_wave: M1 = 103.0, M2 = 68.0; falsifies the unconditioned Prop 2 and the "only failure channel" claim; (d) is mandatory |
| 23 | Edit W3-E4 fallback text | SUPERSEDED | Internally consistent, but Conjecture 1 is now provable; shipping it as a conjecture would understate a theorem |
| 24 | Edit W3-E5 splice | GAP (one sentence) | Final sentence equates ordering frequency with condition frequency; false in general, sufficiency only gives an inequality. Section 6.1 |

No ERROR verdicts: no false step was found anywhere in Edit W3-E2. The two
GAP-level findings (rows 23 and 24) are in the surrounding proposed prose,
not in the mathematics.

## 2. Code-semantics verification (all [VERIFY] tags)

Ground truth: `f:/Paper 3/prototype/src/simulator.py`.

1. **Five-phase trip parity (Lemma 1 input).** `Elevator.request` (lines
   77-92) and `ElevatorBatched.dispatch` (lines 182-197) compute the
   identical formula: wait_start = max(request_time, available_at), then
   reposition |floor - src| * speed, load 2, travel |src - dst| * speed,
   unload 2. Rider count never enters a duration. VERIFIED.
2. **board() semantics.** Lines 178-180: increments trip_passengers, returns
   trip_completion, does not touch available_at, current_floor, or
   trip_loading_end. Since dispatch sets available_at = unloading_end =
   trip_completion (lines 191, 195), the boardable trip's completion always
   equals its elevator's current available_at (the boardable trip is by
   construction the elevator's most recent one, because dispatch overwrites
   the trip state). VERIFIED.
3. **Boarding predicate.** `can_board` (lines 170-176): same (src, dst),
   trip_passengers < capacity, request_time <= trip_loading_end (non-strict,
   line 175; Example X.1's boarding at 7 <= 7 depends on this). With
   capacity = 1 the predicate is unsatisfiable after any dispatch (1 < 1
   fails), so c = 1 disables boarding entirely. VERIFIED.
4. **Pool dispatch rules.** M1: `ElevatorPool.request` (lines 128-136)
   always dispatches fresh on the argmin of (available_at, id(e)). M2:
   `ElevatorPoolBatched.request` (lines 366-376) scans elevators in list
   order for a boardable trip first, then dispatches fresh on the argmin of
   (available_at, id(e)). The boarded elevator need not be the earliest
   available; several elevators can carry matching boardable trips and the
   first in list order wins. The induction only uses T(tau) >= y_(1), which
   holds for any of them. VERIFIED.
5. **Main loop request recursion.** Lines 647-678. Order processing sequence
   is timing-independent (the while loop consumes pending/cluster_buffer
   with no reference to clocks), so condition (a) holds by construction for
   both walks; the cluster selection (lines 649-654) reads only floor
   pairs. AMR selection (line 659) is min by (current_time, id), which is
   timing-dependent: condition (b) is the genuine hypothesis. Pickup
   request time t = max(amr.current_time, wave.release_time +
   order.release_time) (lines 660-661); reposition request only when
   amr.current_floor != source (lines 663-665); delivery request only when
   source != dest (lines 669-671); service constants added at lines 667 and
   673; AMR ready time and order finish at lines 675-676. All operations
   are monotone nondecreasing in the entering completions, which is exactly
   what (I1)-from-(I2) needs. Edge cases of Lemma 3 confirmed: src = dst
   generates no delivery request; AMR already at source generates no
   reposition request; in every case the AMR's floor after an order equals
   the order's destination floor, so the floor-identity induction goes
   through. VERIFIED.
6. **Request program order vs request times.** Because the simulator is a
   sequential accumulator, requests are issued and served in program order
   even when their request times are non-monotone (a later-program-order
   request can carry an earlier clock time). The induction is over program
   order, matching the code. The draft is consistent with this; worth one
   explicit sentence in the manuscript so a reviewer does not look for an
   event-driven timeline.

## 3. Detailed findings on the proof components

### 3.1 Edit W3-E1 (Lemma 2 correction): VERIFIED

The v1.0 clause "M1's per-request queueing delay is pointwise <= that of
M2" is false as an unconditional consequence of server counts: Example X.2
has no queueing under M1 at all (both slots idle at the request) and still
reverses the makespan through the position channel. The corrected Lemma 2
keeps only the true in-transit bound N^{M2}(t) <= E*c (each elevator
carries at most c riders, enforced by can_board). The Remark's two coupling
channels (position, batching) are exactly the two mechanisms the examples
exhibit. This edit should be applied as written.

### 3.2 The invariants and bookkeeping lemmas: VERIFIED

(I1) from (I2): verified against lines 659-676 (see Section 2, item 5).
Note the within-step dependency is also covered: an order's delivery
request time is the same order's reposition completion plus the service
constant, and the reposition request precedes the delivery request in the
request sequence, so the (I2) prefix is available when needed.

Lemma 4: verified by hand and by 20,006 randomized cases (0 failures),
including duplicates, v equal to the minimum, v larger than the maximum,
and n = 1. The premise v >= z_(1) holds in every application because a
completion is never earlier than the availability of the serving unit
(completion >= wait_start = max(request_time, availability) >=
availability).

Lemma 5: verified, including the i = E boundary with y_(E+1) = +infinity
and the length condition m >= E + 1 (= E*c with c >= 2), which is used
exactly once, at coordinate E of Lemma 4 applied to X.

### 3.3 Base case, case F, case B under (c*): VERIFIED

Base: all serving units co-located (pool initial_floor = initial_amr_floor
on every construction path, lines 597-631) with availability 0; the first
request time contains no earlier completion; ties in the argmin are
harmless because all candidate units are identical.

Case F: the chain max(t1, x_(1)) <= max(t2, y_(1)) (from (I1) and (I3)
coordinate 1), plus reposition comparison from (d), plus per-trip parity,
yields D1 <= D2; Lemma 5(i) restores (I3) with u = D1 <= v = D2 and both
replacements at the respective minima (both dispatch rules are argmin
rules).

Case B: (c*) gives D1 <= y_(1) <= T(tau) = D2, and Lemma 5(ii) restores
(I3). The bookkeeping claims about board() are exactly right in the code.
The draft's theorem under (a), (b), (c*), (d) is correct as stated, for
all E and c >= 2.

## 4. The five special-attention questions

### Question 1: Lemma 4 boundary i = n and the +infinity convention

Verified. Hand-worked examples (formula value shown per coordinate):

- Z = (1, 3, 5), v = 4: true Z' = (3, 4, 5); formula gives min(3, max(1,4))
  = 3, min(5, max(3,4)) = 4, min(inf, max(5,4)) = 5. Match, boundary i = 3
  exercised.
- Z = (1, 3, 5), v = 10: true Z' = (3, 5, 10); formula gives 3, 5,
  min(inf, max(5,10)) = 10. Match; v above the maximum lands at the top via
  the +infinity convention.
- Z = (2, 2, 7), v = 2 (v equal to the deleted minimum, with duplicate):
  true Z' = (2, 2, 7); formula gives 2, 2, 7. Match.
- Z = (1), v = 9 (n = 1, the pure boundary): true Z' = (9); formula
  min(inf, max(1, 9)) = 9. Match.

Plus 20,000 randomized multisets with duplicates, 0 failures. The proof's
two-branch argument is airtight for multisets; "delete one instance of
z_(1)" is the right multiset semantics for what the pool actually does.

### Question 2: Lemma 5 and the E*c vs E length mismatch

The E-prefix comparison is sufficient, and this is not an accident. In the
restoration step, coordinate i of the new M1 prefix is
min(x_(i+1), max(x_(i), u)): the only place the (E+1)-th smallest M1 slot
enters is inside the outer min at coordinate E, and a min can only lower
the left-hand side, so no information about slots E+1 through E*c is ever
needed. Conversely the invariant cannot be thinned below E coordinates:
restoring coordinate i consumes coordinate i+1 of the pre-state, so the
prefix length must reach the length of Y, and Y has exactly E entries
(padding beyond E is what the y_(E+1) = +infinity convention already
does). The step case needs no additional slots. The one place the extra
slots matter at all is the existence of x_(E+1) (hence m >= E + 1, hence
the c >= 2 hypothesis, with c = 1 handled separately by exact equality).

### Question 3: Case B bookkeeping

Verified in code: board() (lines 178-180) does not mutate available_at, so
the M2 availability vector is unchanged through a boarding, and T(tau)
equals the boarded elevator's current available_at because dispatch set
available_at = trip_completion (lines 191, 195) and the boardable trip is
always the elevator's most recent. The invariant restoration in case B
under (c*) consumes exactly two facts: (c*) itself (u = D1 <= y_(1), used
both for the (I2) extension and for Lemma 5(ii)) and T(tau) >= y_(1)
(T is an entry of the availability vector). Nothing else is used; in
particular it does not matter which matching elevator the list-order scan
boards. Under the weaker per-trip (c), restoration additionally needs the
counting argument of Section 5.

### Question 4: Well-definedness of condition (d)

Well-defined. The "unit actually selected" under each model is the argmin
of (available_at, tie-break) within that model's own fleet; no matching
between M1 slots and M2 elevators is assumed or needed, and the definition
compares two realized reposition distances on the same request. One
genuine caveat: the code breaks availability ties by id(e) (lines 135,
375), which is deterministic within a process but is a CPython memory
artifact, not list order; the comment at line 134 claiming "ties broken by
slot order (stable)" is not guaranteed by the implementation. I confirmed
this matters observationally: in 25 of 6,000 cross-checked random waves,
an availability tie interacting with the list-order boarding scan produced
a different (equally valid) M2 trajectory under a different tie-break
(e.g. one probe wave gave M2 = 37.4 under index tie-break and M2 = 43.0
under the in-process id ordering; M1 = 33.0 <= both). The proof is
tie-break agnostic (Lemmas 4 and 5 are multiset statements; case B uses
only T >= y_(1)), so Proposition 2 covers every tie-break. But because
condition (d) is defined relative to the realized execution, the
manuscript should state a tie-break convention explicitly (recommend:
lowest unit index) and ideally the code comment should be fixed to match.

### Question 5: Remark X.3

Resolved; see Section 5. Outcome: reachability FAILS, the invariant can be
repaired by a counting argument rather than by strengthening (c) to (c*),
and the general theorem holds under (a), (b), (c), (d). No wave-level
counterexample exists at any E under those four conditions (proof below,
corroborated by 60,000-wave search at E in {2,3} with zero violations).

## 5. Resolution of Remark X.3: the break state is unreachable, and (c) suffices for all E

### 5.1 Reproduction of the break arithmetic

State: sorted M1 slots X = (0, 6, 9, 9), sorted M2 elevators Y = (5, 6),
boarding on the trip completing at T = 6 with D1 = 6. Check: (I3) holds
before (0 <= 5, 6 <= 6); per-trip (c) holds (6 <= 6); (c*) fails
(6 > y_(1) = 5); after replacing the M1 minimum with 6, the prefix is
(6, 6) against (5, 6) and coordinate 1 breaks. Confirmed exactly as the
draft states. (Two side observations: with the default constants no
completion of 6 can exist at all, since the shortest possible trip takes
2 + 5 + 2 = 9 seconds; and the deeper point below kills the pattern at any
scaling of the constants.)

### 5.2 Why the state cannot arise: recency of late completions

The following lemma is the missing structural fact. It is stated in
manuscript-ready form (target: Appendix X.4, replacing Remark X.3).

**Lemma 6 (recency of late completions).** *Fix a step k of the induction
and suppose (I2) holds for every request served before step k. Let
y_(1) <= ... <= y_(E) be the current M2 elevator availabilities and
x_(1) <= ... <= x_(E*c) the current M1 slot availabilities. For a
threshold y, write N1(y) for the number of M1 slots with availability
strictly greater than y, and P2(y) for the total passenger count of the
current (most recent) trips of those M2 elevators whose availability
strictly exceeds y. Then N1(y_(i)) <= P2(y_(i)) for every i, and in
particular N1(y_(i)) <= (E - i) * c.*

*Proof.* Four observations.

1. Each M2 elevator's availability is nondecreasing over the run: a fresh
   dispatch sets it to the new trip's completion, which is at least the
   wait start (at least the previous availability) plus a positive trip
   duration, and a boarding leaves it unchanged. [Code: lines 182-197 and
   178-180.]
2. Any M2 trip that is not the most recent trip of its elevator completed
   no later than the current fleet minimum y_(1). When the elevator's next
   trip was dispatched, the earliest-availability rule selected that
   elevator, so its availability at that moment, which equals the earlier
   trip's completion, was less than or equal to every elevator's
   availability at that moment; and every availability has only grown
   since, by observation 1. [Code: every M2 fresh dispatch goes through
   the argmin at line 375.]
3. Hence any previously served request whose M2 completion exceeds y_(i)
   was served, fresh or boarding, on the most recent trip of an elevator
   whose current availability exceeds y_(i): its trip's completion equals
   that elevator's current availability. There are at most E - i such
   elevators, and each most recent trip carries at most c requests, so at
   most P2(y_(i)) <= (E - i) * c previously served requests have M2
   completion above y_(i).
4. Each M1 slot's availability is either 0 or the M1 completion of the
   last request served on that slot, and distinct slots serve disjoint
   request sets. By (I2), any prior request with M1 completion above
   y_(i) also has M2 completion above y_(i). Combining with observation 3,
   N1(y_(i)) <= P2(y_(i)). *(End of proof.)*

**Corollary (case B closes under the per-trip condition (c), all E).**
*Let request r_k board trip tau, on the elevator whose current
availability is T. Boarding requires spare capacity, so tau carries at
most c - 1 requests at this moment. For every rank i with y_(i) < T, the
boarded elevator is among those counted by P2(y_(i)), so
N1(y_(i)) <= (E - i) * c - 1 <= E * c - i - 1, hence x_(i+1) <= y_(i).
Now perform the update: M1 replaces x_(1) by u = D^{M1}(r_k), with u <= T
by the per-member form of (c), and the M2 vector is unchanged. By Lemma 4,
x'_(i) = min(x_(i+1), max(x_(i), u)). For every rank with y_(i) >= T,
max(x_(i), u) <= max(y_(i), T) = y_(i). For every rank with y_(i) < T,
x'_(i) <= x_(i+1) <= y_(i). All E coordinates of (I3) are restored, and
(I2) extends by D^{M1}(r_k) <= T = D^{M2}(r_k).* *(End of corollary.)*

The two arithmetic facts used: "at most E*c - i - 1 slots above y_(i)
implies x_(i+1) <= y_(i)" (definition of order statistics), and
(E - i) * c - 1 <= E * c - i - 1, which is equivalent to i * (c - 1) >= 0
and always true. Note the corollary consumes only the per-member form of
(c) for the boarder; the dispatcher of tau was handled by case F when tau
was dispatched.

**Consequence.** Replacing the draft's case B (which uses (c*) and Lemma
5(ii)) by the corollary above, the full induction of Edit W3-E2 goes
through under (a), (b), (c), (d) for every E >= 1 and every c >= 2, with
c = 1 exact equality as before. Conjecture 1 of Edit W3-E4 is therefore a
theorem, and the strengthened condition (c*) can be dropped from the
statement entirely (it survives only as a proof-internal device if the
author prefers the (c*) route; it is no longer needed).

**Why the Remark X.3 state is unreachable.** The instance X = (0, 6, 9, 9),
Y = (5, 6), T = 6 requires three M1 slots strictly above y_(1) = 5. By
Lemma 6 at a boarding step at E = 2, c = 2, at most
(E - 1) * c - 1 = 1 previously served request can have completion above
y_(1) (members of the single most recent trip of the non-minimum elevator,
minus the seat the boarder is about to take), so at most one slot can sit
above y_(1). Three is impossible. The same counting kills every scaled
variant of the pattern; the break is an artifact of treating the
availability vectors as free parameters, which the dispatch dynamics do
not permit.

### 5.3 Computational corroboration

Instrumented dual simulator (exact replica of the simulate_wave loop with
per-step logging, cross-validated against simulate_wave; index tie-break),
random verification waves, conditions checked per step. These are
verification-harness ensembles, neither publication scale nor prototype
scale; frequencies describe the harness distribution only.

E in {2, 3}, c in {2, 3}, 60,000 waves (floors up to 8, 2 to 6 orders,
staggered releases, dedicated or shared AMRs):

- 56,914 waves satisfied (b) on the free run (3,068 dropped; (a) holds by
  construction).
- 13,596 waves satisfied (b), (c), (d): dominance violations 0, (I3)
  breaks 0.
- Of those, 8,661 waves (2,342 at E = 3) contained at least one boarding
  where (c) holds but (c*) fails: these are reachable waves that the
  draft's (c*)-theorem does NOT cover and the Lemma 6 version does.
  Dominance held in all of them.
- Lemma 6's inequality checked at every step at which the (I2) prefix
  held, across all 60,000 waves: 0 violations.
- The (d) channel is live and frequent: among 35,787 waves with (c)
  holding and (d) failing, 5,844 violated dominance.

E = 1, 30,000 waves: (c) and (c*) never disagreed (equivalence
confirmed); 1,990 waves satisfied (b), (c), (d), dominance violations 0.

c = 1, 20,000 waves at E in {1, 2, 3}: M1 and M2 makespans exactly equal
in all (the equality remark).

Examples X.1 and X.2 re-confirmed against simulate_wave: 26.0 vs 24.0 and
103.0 vs 68.0.

A minimal reachable wave exhibiting the coverage gap between (c) and
(c*), useful as a worked illustration next to Lemma 6: E = 2, c = 2, four
orders (1 to 8), (1 to 2), (1 to 2), (1 to 8), all released at 0, four
AMRs. Requests all issue at t = 5; the two (1,2) requests share one
elevator's trip (completion 14) and the two (1,8) requests share the
other's (completion 44); under M1 all four run on the four slots with the
same completions 44, 14, 14, 44. Conditions (b), (c), (d) hold; (c*)
fails at the fourth request (D1 = 44 > y_(1) = 14); (I3) never breaks;
makespans are equal at 49. Verified through simulate_wave.

## 6. New issues found (outside the X.4 mathematics)

### 6.1 Edit W3-E5, final sentence: ordering frequency is not condition frequency (GAP, must fix)

The proposed replacement text ends: "The 99.2% is therefore a measurement
of how often the exclusion conditions are met on freely simulated waves,
not an unexplained shortfall from 100%." This repeats, in weakened form,
the error the edit is correcting. Proposition 2 is a sufficiency result,
so it implies only: ordering frequency >= condition frequency. The two
are far apart in practice: in the harness ensemble, (c) and (d) jointly
held on about 24% of (b)-satisfying waves while the ordering held on far
more (in particular on 84% of the waves where (d) failed). The condition
frequency on Block C waves has never been measured. Suggested
replacement sentence: "The 99.2% is a measurement of how often the
per-wave ordering itself holds on freely simulated waves; the exclusion
conditions are sufficient, not necessary, so their satisfaction frequency
is a lower bound on, not an estimate of, this number." The rest of Edit
W3-E5 (positive identification, not exclusion; the classifier amendment)
is consistent and unaffected.

### 6.2 Edit W3-E4: supersession, not error

If Lemma 6 is adopted, the fallback's Conjecture 1 paragraph and the
sentence "identifies the single bookkeeping step at which the per-trip
form (c) is not known to suffice" become obsolete: the bookkeeping step
is now closed. The E = 1 proposition-plus-conjecture split is no longer
the honest-minimum statement; the honest-minimum statement is the general
theorem.

### 6.3 Tie-break specification (MINOR, patchable in one sentence)

The c = 1 equality remark and condition (d) both implicitly reference the
realized selection among availability ties. The code's tie-break is
id(e)-based (lines 135, 375), deterministic per process but not the list
order the line-134 comment claims. Patch: state in X.4.1 that ties in the
earliest-availability rule are broken by a fixed unit index in both
models (and, if desired, fix the comment or the key to
(e.available_at, index) in a future code revision; the theorem itself is
tie-break agnostic, so no result depends on this).

### 6.4 Publication-scale linkage (context note)

Block C is entirely E = 2 (phase5_config e2_subset). Under the draft's
(c*) theorem this regime was covered only by a conjecture; under Lemma 6
it is covered by the theorem. This removes the awkward scope note in Edit
W3-E4 ("the measured regime is covered by the conjecture, not by the
proved case") entirely.

## 7. Final assessment: which statement to ship

Three options, in decreasing order of mathematical strength:

1. **General theorem under (a), (b), (c), (d), all E, via Lemma 6**
   (recommended). Every component is now verified twice: analytically
   against the code semantics, and computationally with zero violations in
   110,000 verification waves across E in {1, 2, 3}. The theorem's
   headline condition is the same per-trip batch-overtaking condition (c)
   already defined in Section 4.2.1, so no re-plumbing of the manuscript's
   definitions is needed; the only additions are condition (d) (mandatory
   in any case, by Example X.2) and Lemma 6 in the appendix. Block C's
   E = 2 regime is covered by the theorem, not a conjecture.
2. **The draft's theorem under (a), (b), (c*), (d)** (verified correct,
   but strictly weaker). It leaves reachable waves uncovered (8,661 of
   13,596 condition-satisfying harness waves contain a (c*)-violating
   boarding) and forces the manuscript to define a fleet-state condition
   (c*) that differs from the Section 4.2.1 per-trip definition.
3. **E = 1 proposition plus Conjecture 1** (Edit W3-E4). Mathematically
   safe but now needlessly weak: it labels as a conjecture something
   provable, and concedes the measured E = 2 regime.

The mathematically safest option is option 1, conditional on one thing:
the author hand-verifies Lemma 6's four observations and the corollary's
two inequalities (about half a page; every code-facing claim is cited to
lines above). If the author wants a belt-and-suspenders path, ship option
1 and keep the (c*) argument as a remark ("an alternative proof of case B
under the stronger per-boarding condition (c*) avoids Lemma 6"), which
costs three sentences.

Required knock-on edits if option 1 ships: (i) Edit W3-E2's X.4.1 drops
(c*) from the hypothesis list (or keeps it as a proof-internal
definition); (ii) Remark X.3 is replaced by Lemma 6 and its corollary,
with the unreachability paragraph of Section 5.2 above as the explanatory
remark; (iii) Edit W3-E4's Proposition-plus-Conjecture split collapses
back into a single Proposition 2 under (a), (b), (c), (d), with the
necessity examples unchanged; (iv) Edit W3-E5's final sentence is
replaced per Section 6.1; (v) the Section 4.2.2 Theorem 2 cross-reference
reverts to citing Proposition 2 alone. Items (i) to (v) touch only
documents already slated for revision; nothing touches the
pre-registration or any gate verdict.

## 8. How to re-run this verification

Harness: `scratchpad/verify_w3.py` (session scratchpad; self-contained,
inserts `f:/Paper 3/prototype` on sys.path). Parts: (1) Examples X.1/X.2
via simulate_wave; (2) Lemma 4 randomized identity check; (4) the
60,000-wave conditioned search with per-step (b)/(c)/(c*)/(d)/(I3)/Lemma-6
checks, cross-validated against simulate_wave; (5) the targeted
(c)-holds-(c*)-fails wave. The E = 1 and c = 1 supplements are one-off
scripts using the same `analyze` entry point. All checks are deterministic
given the seeds in the file.
