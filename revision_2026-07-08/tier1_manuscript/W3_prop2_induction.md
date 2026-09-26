---
title: "W3: Proposition 2 request-by-request induction (complete draft), necessity counterexamples, and +0 fallback"
date: 2026-07-08
status: "draft for author review"
verification_status: >
  DRAFT MATHEMATICS, NOT A FINAL PROOF. Every step marked [VERIFY] must be
  checked by the author before any of this text enters the manuscript. Two of
  the findings below (Example X.2 and Remark X.3) CONTRADICT the current
  Proposition 2 statement and the current Appendix skeleton; they are the most
  important content of this document and must be verified first, by hand and by
  the one-line simulator calls listed at the end.
integration_note_2026_07_08: >
  NUMERICAL VERIFICATION DONE (integrator, 2026-07-08, single deterministic
  simulate_wave calls, milliseconds): Example X.1 confirmed, M1 = 26.0 vs
  M2 = 24.0; Example X.2 confirmed, M1 = 103.0 vs M2 = 68.0. Open issues 1
  and 2 (numerical checks) are therefore RESOLVED; the hand-computed
  timelines match the simulator exactly. Example X.2's falsification of the
  current Proposition 2 statement STANDS: condition (d) is mandatory. The
  induction mathematics itself (open issues 3-5) still requires the author's
  human verification. Amendment B item B-1 has been extended the same day
  (before execution) with the three-way violation-channel classifier
  (batch-overtaking / adverse repositioning / other) and the locked rule that
  the "all violations are batch-overtaking" sentence is retired.
sources_consulted:
  - "f:/Paper 3/CLAUDE.md"
  - "f:/Paper 3/paper_draft/TERMINOLOGY.md"
  - "f:/Paper 3/paper_draft/Appendix/chain_dominance_proof_v1.0.md"
  - "f:/Paper 3/paper_draft/Methodology/proposition2_chain_dominance_v1.0.md"
  - "f:/Paper 3/paper_draft/section4_draft_v0_1.md (lines 115-170)"
  - "f:/Paper 3/paper_draft/Experiments/chain_dominance_empirical_v1.0.md"
  - "f:/Paper 3/prototype/src/simulator.py (Elevator, ElevatorPool, ElevatorBatched, ElevatorPoolBatched, simulate_wave)"
  - "f:/Paper 3/prototype/src/phase5_config.py (FACTOR_E = [1,2], CAPACITY = 2, Block C = E2 subset)"
  - "f:/Paper 3/prototype/src/demand_patterns.py (order (src,dst) uniform over feasible pairs; diurnal release times)"
  - "scratchpad/panel_theory.json (fatal flaw 3: skeleton shipped as proof; fatal flaw 4: hypotheses (a)/(b) not enforced in harness; required_additions 2 and 4; nice_to_have 2)"
addresses_audit_findings:
  - "panel_theory fatal flaw 3 (CRITICAL): Prop 2 rests on an admitted proof skeleton while section 4 says 'full proof in Appendix'"
  - "panel_theory required_additions item 2 (complete the X.4 induction or execute the +0 fallback)"
  - "panel_theory required_additions item 4 (worked counterexample establishing necessity of condition (c))"
  - "panel_theory fatal flaw 4 (MAJOR): empirical face of the theorem misaligned with its statement (knock-on to section 5.3 wording)"
scope_warning: >
  This document proposes edits to paper_draft/Appendix/chain_dominance_proof_v1.0.md,
  paper_draft/section4_draft_v0_1.md, and paper_draft/Experiments/chain_dominance_empirical_v1.0.md.
  NO file outside revision_2026-07-08/tier1_manuscript/ has been modified; all
  edits below are proposals quoted for the author to apply after verification.
  The pre-registration and all D2 gate numbers/verdicts are untouched.
---

# W3: Proposition 2 induction completion, counterexamples, and fallback

## Summary of findings (read this first)

While carrying out the X.4 induction against the simulator's exact semantics
(`prototype/src/simulator.py`), two facts emerged that go beyond "the skeleton
needs tightening":

1. **Proposition 2 as currently stated appears to be FALSE.** There is a
   two-order, one-AMR, `E = 1`, `c = 2` wave with *no batching event at all*
   (condition (c) vacuously satisfied, conditions (a) and (b) trivially
   satisfied) on which `C_max(W; M1) = 103 > 68 = C_max(W; M2)` by hand
   computation (Example X.2 below). The mechanism is *repositioning*: `M1`'s
   earliest-availability rule selects a slot by availability alone, ignoring
   floor position, and can commit a slot parked eight floors away while `M2`'s
   single elevator stands exactly at the request's origin. A fourth condition
   (d), "no adverse repositioning", is therefore *mandatory* in any correct
   restatement, including the fallback. The claim in the current Appendix X.5
   that batch-overtaking "is the *only* way dominance fails" is falsified by
   this example. [VERIFY: one `simulate_wave` call, listed at the end.]

2. **For `E >= 2`, the per-trip condition (c) is not known to suffice even
   with (d) added.** The availability-vector invariant that carries the
   induction is preserved through boarding events only under a strengthened
   condition (c*) ("no batch advantage"); at `E = 1`, (c*) is equivalent to
   (c), so the single-elevator case closes completely under (a), (b), (c),
   (d). At `E >= 2` there is a concrete four-number state instance where (c)
   holds but the invariant breaks (Remark X.3). Whether that break can
   propagate to an actual makespan violation on a reachable wave is OPEN.
   Note that Block C, where the publication-scale 99.2% condition frequency is
   measured, is entirely `E = 2` (`phase5_config.e2_subset`), so the measured
   regime is exactly the one where only the conjecture applies.

Consequences for the three requested deliverables:

- Deliverable 1 (the complete induction) is drafted below as Edit W3-E2. It
  proves the result under (a), (b), (c*), (d) for all `E`, with the
  (ii-a)/(ii-b) separation and the sorted availability-vector coupling the
  skeleton prescribed, plus corollaries for `E = 1` (under the original (c))
  and for no-boarding waves.
- Deliverable 2 (the batch-overtaking counterexample for necessity of (c)) is
  Example X.1 in Edit W3-E3, two orders, hand-computed timelines, makespans
  26 vs 24. A second example (X.2) establishes necessity of the new (d).
- Deliverable 3 (the +0 fallback) is Edit W3-E4. Given finding 1, the fallback
  is not merely a contingency: even the softened statement must carry
  condition (d), because the `E = 1` special case WITHOUT (d) is false.

---

# Edit W3-E1: Correct Lemma 2's over-claim (Appendix X.3)

Target file: `paper_draft/Appendix/chain_dominance_proof_v1.0.md`, lines 49-74.

## 修改前 (BEFORE)

```
## X.3 Lemma 2 (server-count monotonicity)

*At every time `t`, the number of requests in transit under `M2`, `N^{M2}(t)`,
satisfies `N^{M2}(t) ≤ E·c = S`, the `M1` slot count. Consequently, under the
common dispatch order, no request is forced to wait for a free server under `M1`
at a time when `M2` would have served it immediately; `M1`'s per-request queueing
delay is pointwise ≤ that of `M2`.*

The first clause holds because `M2` has `E` elevators each carrying at most `c`
riders, so at most `E·c` riders are in transit at once, and `M1` has exactly
`E·c` slots. The second clause follows because `M1`'s feasible set of
simultaneously-served requests (any subset of size ≤ `S`) contains `M2`'s (any
configuration of `E` trips, ≤ `S` riders). Greedy earliest-availability
assignment on the larger server set yields availability times pointwise no later
than on the smaller one. This server-count monotonicity, that more parallel
servers weakly reduce delay, is the queueing-theoretic core of the result
(Moyal, 2013; Smith and Whitt, 1981); the common-dispatch-order requirement is
precisely the condition under which the comparison can otherwise fail
(Moyal, 2013). ∎

> **Tightening note (v1.0 → v1.1).** Lemma 2's "pointwise ≤" clause is the step
> that needs the careful induction in X.4: the AMR pool couples elevator
> response times back into future AMR-to-order assignments, so "same dispatch
> order" (condition (a)) and "same AMR-to-order assignment" (condition (b)) are
> what keep the two timelines comparable. State them as standing hypotheses; do
> not attempt to prove dominance without them.
```

## 修改后 (AFTER)

```
## X.3 Lemma 2 (server-count bound)

*At every time `t`, the number of requests in transit under `M2`, `N^{M2}(t)`,
satisfies `N^{M2}(t) <= E*c = S`, the `M1` slot count.*

The claim holds because `M2` has `E` elevators each carrying at most `c`
riders, so at most `E*c` riders are in transit at once, and `M1` has exactly
`E*c` single-rider slots. ∎

**Remark (what Lemma 2 does not give).** A pure server-count comparison does
not by itself imply that `M1` serves every request no later than `M2`, for two
reasons that the induction in X.4 must handle explicitly. First, availability
is not the only server state: each serving unit also carries a floor position,
the reposition leg of the next trip depends on that position, and the
earliest-availability rule selects a server by availability alone. `M1` can
therefore commit a distant slot to a request while an `M2` elevator stands at
the request's origin floor; Example X.2 (Section X.5) shows this effect alone
can reverse the makespan ordering, which is why condition (d) below is part of
the hypothesis. Second, a boarding event lets `M2` serve a request without
consuming any additional server time, which advances `M2`'s availability
relative to `M1` for later requests; this is why the batching condition must
control not only the boarded group itself (condition (c)) but, for `E >= 2`,
the fleet state as well (condition (c*), Section X.4). The heuristic that more
parallel servers weakly reduce delay is classical (Smith and Whitt, 1981), and
so is the fact that greedy, state-blind allocation can defeat the comparison
(Moyal, 2013); conditions (a) to (d) are exactly the sample-path hypotheses
under which the comparison survives the elevator system's position and
batching couplings.
```

## 理由 (RATIONALE)

针对 panel_theory 致命缺陷 3（CRITICAL）：v1.0 的 Lemma 2 第二句（"M1 的逐请求排队延迟逐点小于等于 M2"）是骨架中被标记为"需要 X.4 仔细归纳"的那一步，而按现在的写法它是一个错误的断言：它只比较了可用时间，完全忽略了服务器的楼层位置。Example X.2（本文件 Edit W3-E3）给出了一个具体反例，其中 M1 没有任何排队等待、纯粹因为 earliest-availability 规则选中了停在远楼层的槽位而变慢。审稿人若核查此引理会直接发现假引理。修改后的 Lemma 2 只保留其真实内容（在途请求数上界），并用一段 Remark 明确指出归纳需要额外处理的两个耦合渠道，为 X.4 的不变量结构铺垫。

---

# Edit W3-E2: The complete request-by-request induction (replaces Appendix X.4)

Target file: `paper_draft/Appendix/chain_dominance_proof_v1.0.md`, lines 76-102.

DELIVERABLE 1. This is the full draft of the induction, following the
skeleton's own prescription: the inductive step is separated into (ii-a)
AMR-ready-time monotonicity and (ii-b) elevator-availability monotonicity,
each carried by its own invariant, with the availability comparison done on
sorted availability vectors. Two departures from the v1.0 plan were forced by
the mathematics and are flagged: condition (d) is new and mandatory
(Example X.2), and condition (c) is strengthened to (c*) for `E >= 2`
(Remark X.3).

## 修改前 (BEFORE)

```
## X.4 Proof of Proposition 2

Under hypotheses (a) same order-processing sequence, (b) same AMR-to-order
assignment, and (c) no batch-overtaking, we show `D^{M1}(r) ≤ D^{M2}(r)` for
every request `r`, by induction on the order in which requests are dispatched.

*Base.* The first dispatched request sees both subsystems idle at their initial
floor; by Lemma 1 its trip duration is identical, and its release/AMR-ready time
is identical by (a)–(b), so `D^{M1}(r_1) = D^{M2}(r_1)`.

*Step.* Assume `D^{M1}(r) ≤ D^{M2}(r)` for all requests dispatched before `r`.
The dispatch time of `r` is the max of (i) its AMR-ready time and (ii) its
elevator-availability time. By (a)–(b) and the induction hypothesis, (i) under
`M1` is ≤ that under `M2`. For (ii): by Lemma 2, `M1` has a slot free no later
than `M2` has an elevator free, UNLESS `r` belongs to a group that `M2` clears
via a single batched trip whose synchronized completion precedes `M1`'s
staggered group completion. That exception is exactly batch-overtaking, excluded
by (c). Hence (ii) under `M1` is ≤ that under `M2`, and by Lemma 1 the added
trip duration is equal, giving `D^{M1}(r) ≤ D^{M2}(r)`.

Taking the maximum over `r`, `C_max(W; M1) ≤ C_max(W; M2)`. ∎

> **Tightening note (v1.0 → v1.1).** The induction step folds the AMR-coupling
> and the elevator-coupling into one comparison; the clean version separates
> them into (ii-a) AMR-ready monotonicity and (ii-b) elevator-availability
> monotonicity, each carried by a separate invariant. Worth writing out fully
> before submission, but the structure above is the load-bearing logic.
```

## 修改后 (AFTER)

```
## X.4 Proof of Proposition 2 (request-by-request induction)

### X.4.1 Standing hypotheses and the two exclusion conditions

Fix a wave `W` and process it under `M1` and `M2` in the deterministic setting
(no phase noise, no service-time noise). The standing hypotheses are:

- **(a) common processing sequence:** the orders of `W` are walked in the same
  sequence under both models. For the FIFO walk this holds by construction; for
  the cluster walk it also holds by construction, because the cluster selection
  depends only on the pending orders' floor pairs, which are model-independent.
- **(b) common AMR-to-order assignment:** each order is served by the same AMR
  under both models. Unlike (a), this is a genuine restriction: the free
  earliest-available-AMR rule can assign differently across models because AMR
  ready times depend on elevator response times.

A *request* is a single elevator demand `(o, d, t)`: a reposition leg that
carries an AMR from its current floor `o` to an order's source floor `d`, or a
delivery leg from an order's source floor `o` to its destination floor `d`,
issued at request time `t`. Under `M1` every request is served by a fresh trip
on the earliest-available slot. Under `M2` a request first attempts to board an
in-progress trip (same `(o, d)`, fewer than `c` riders, request time no later
than the trip's loading-window close); otherwise it dispatches a fresh trip on
the earliest-available elevator. Write `D^{M}(r)` for the unload-end
(completion) of request `r` under model `M`.

For the current fleet state, let `x_(1) <= ... <= x_(E*c)` denote the sorted
slot availabilities under `M1` and `y_(1) <= ... <= y_(E)` the sorted elevator
availabilities under `M2`.

The two exclusion conditions, both sample-path events:

- **(c) no batch-overtaking (per-member form):** for every `M2` trip `tau`
  that carries a group `G` of `k >= 2` requests with shared completion
  `T(tau)`, we have `T(tau) >= D^{M1}(r)` for every `r in G`. This is
  equivalent to the group form in Section 4.2.1, because the group completes
  under `M1` at `max_{r in G} D^{M1}(r)`.
- **(c*) no batch advantage (strengthened form, used for `E >= 2`):** for
  every request `r` that boards an in-progress `M2` trip,
  `D^{M1}(r) <= y_(1)`, where `y_(1)` is the smallest elevator availability
  under `M2` at the step where `r` is dispatched. Since the boarded trip's
  elevator has availability `T(tau) >= y_(1)`, condition (c*) implies the
  per-member form of (c) for the boarded request. For `E = 1` the two
  conditions coincide, because the unique elevator's availability equals the
  boarded trip's completion. [VERIFY: `ElevatorBatched.dispatch` sets
  `available_at = unloading_end = trip_completion`, and `board()` returns
  `trip_completion` without changing `available_at`; simulator.py lines
  178-197.]
- **(d) no adverse repositioning:** for every request `r` served by fresh
  trips in both models, `|f^{M1}(r) - o(r)| <= |f^{M2}(r) - o(r)|`, where
  `f^{M}(r)` is the current floor of the serving unit actually selected under
  model `M` and `o(r)` is the request's origin floor. Example X.2 (Section
  X.5) shows (d) is not cosmetic: without it, dominance fails on a two-order
  wave with no batching at all.

**Proposition 2 (restated).** *Fix a wave `W` and process it under `M1` and
`M2` subject to (a) and (b). If (c*) and (d) hold on the sample path, then
`D^{M1}(r) <= D^{M2}(r)` for every request `r`, and consequently
`C_max(W; M1) <= C_max(W; M2)`. For `E = 1`, hypotheses (a), (b), (c), (d)
suffice, since (c*) and (c) coincide.*

For `c = 1` the two models coincide sample path by sample path (boarding is
impossible and both pools reduce to `E` identical single-rider servers under
the same earliest-availability rule), so the result holds with equality and we
assume `c >= 2` throughout. [VERIFY: with `capacity = 1`,
`ElevatorBatched.can_board` requires `trip_passengers < 1`, which fails after
any dispatch.]

### X.4.2 Lemma 3 (structural identity of the request sequence)

*Under (a) and (b), the two models generate the same finite request sequence
`r_1, ..., r_m`: the same number of requests, in the same order, with
identical origin and destination floors `(o(r_k), d(r_k))` and identical
issuing AMRs. Only the request times and completions may differ.*

*Proof.* Induct along the common walk. The `k`-th order processed and its
serving AMR are fixed by (a) and (b). An AMR's floor when it receives an order
equals the destination floor of the previous order it served (or the initial
floor if none), which by the inductive hypothesis is model-independent.
Whether the order generates a reposition request (AMR floor differs from the
source floor) and a delivery request (source differs from destination) is
therefore model-independent, as are all four floors involved. ∎
[VERIFY: edge cases: an order whose source equals its destination generates no
delivery request; an order whose source equals the AMR's floor generates no
reposition request; both are covered by the floor-identity induction, but
check against simulator.py lines 663-671.]

### X.4.3 The three invariants

After each step `k` (that is, after request `r_k` is served in both models),
we maintain:

- **(I1) request-time monotonicity:** `t^{M1}(r_j) <= t^{M2}(r_j)` for all
  `j <= k`.
- **(I2) completion monotonicity:** `D^{M1}(r_j) <= D^{M2}(r_j)` for all
  `j <= k`.
- **(I3) availability dominance (sorted prefix):** `x_(i) <= y_(i)` for all
  `i = 1, ..., E`, comparing the `E` smallest `M1` slot availabilities with
  the `E` elevator availabilities of `M2`, both sorted ascending.

(I1) is a consequence of (I2): every request time is produced from earlier
completions by the AMR-side recursion, which composes only monotone operations
(the max with an order's fixed absolute release time, and the addition of
fixed service constants), so completions ordered by (I2) yield request times
ordered the same way. [VERIFY against simulator.py lines 659-676: pickup
request time `t = max(amr.current_time, order_release_abs)`; delivery request
time = pickup return + service constant; AMR ready time after an order =
delivery return + service constant. All monotone nondecreasing in the entering
completions.]

**Lemma 4 (min-replacement identity).** *Let `Z` be a sorted multiset
`z_(1) <= ... <= z_(n)` and `v >= z_(1)`. Let `Z'` be `Z` with one instance of
`z_(1)` deleted and `v` inserted. Then for every `i <= n`,
`z'_(i) = min(z_(i+1), max(z_(i), v))`, with the convention
`z_(n+1) = +infinity`.*

*Proof.* After deleting `z_(1)` the sorted list is `z_(2) <= ... <= z_(n)`.
If `v > z_(i+1)`, the `i` smallest elements of `Z'` are `z_(2), ..., z_(i+1)`,
so `z'_(i) = z_(i+1)`; and `max(z_(i), v) = v > z_(i+1)` makes the right side
`z_(i+1)`. If `v <= z_(i+1)`, the `i` smallest elements of `Z'` are
`z_(2), ..., z_(i)` together with `v`, so `z'_(i) = max(z_(i), v)` (for
`i = 1` this reads `z'_(1) = min(z_(2), v)`, consistent with the formula since
`v >= z_(1)`); and the right side is `max(z_(i), v)` because
`max(z_(i), v) <= z_(i+1)`. ∎

**Lemma 5 (dominance propagation under min-replacement).** *Let `X` (length
`m >= E + 1`) and `Y` (length `E`) be sorted multisets with `x_(i) <= y_(i)`
for `i <= E`.*

*(i) (two-sided replacement) If `X' = X` with `x_(1)` replaced by `u >= x_(1)`
and `Y' = Y` with `y_(1)` replaced by `v >= y_(1)`, and `u <= v`, then
`x'_(i) <= y'_(i)` for all `i <= E`.*

*(ii) (one-sided replacement) If `X' = X` with `x_(1)` replaced by
`u <= y_(1)` and `Y' = Y`, then `x'_(i) <= y_(i)` for all `i <= E`.*

*Proof.* (i) By Lemma 4, `x'_(i) = min(x_(i+1), max(x_(i), u))` and
`y'_(i) = min(y_(i+1), max(y_(i), v))` with `y_(E+1) = +infinity`. For
`i < E`, `x_(i+1) <= y_(i+1)` by hypothesis; for `i = E`,
`x_(E+1) <= +infinity = y_(E+1)`. Also `max(x_(i), u) <= max(y_(i), v)`
termwise. A coordinatewise min of smaller terms is smaller. (ii) Here
`x'_(i) = min(x_(i+1), max(x_(i), u)) <= max(x_(i), u) <= max(y_(i), y_(1))
= y_(i)`, using `u <= y_(1) <= y_(i)`. ∎ The length condition `m >= E + 1`
holds because `m = E*c` and `c >= 2`. [VERIFY: the `u >= x_(1)` premise of
Lemma 4 holds in every application below because a completion is never earlier
than the availability of the server that produced it.]

### X.4.4 Base case

Before any request, every slot and every elevator is at the initial floor with
availability 0, so (I3) holds with equality and (I1), (I2) are vacuous. The
first request `r_1` has identical request time under both models (no earlier
completions enter its recursion), both serving units are at the same floor
with availability 0, and the four phase durations coincide (Lemma 1), so
`D^{M1}(r_1) = D^{M2}(r_1)`. Invariant (I3) is restored by Lemma 5(i) with
`u = v = D(r_1)`.

### X.4.5 Inductive step, case F: `r_k` is served by fresh trips in both models

Under `M1` the serving slot is the earliest-available one, with availability
`x_(1)` and floor `f1`; under `M2` the serving elevator is the
earliest-available one, with availability `y_(1)` and floor `f2`.

*(ii-a) AMR-ready comparison.* By (I2) up to `k - 1` and the monotone AMR-side
recursion, `t^{M1}(r_k) <= t^{M2}(r_k)` (invariant (I1) extended).

*(ii-b) elevator-availability comparison.* By (I3) at coordinate 1,
`x_(1) <= y_(1)`. Hence the wait-start satisfies
`max(t^{M1}(r_k), x_(1)) <= max(t^{M2}(r_k), y_(1))`.

*Reposition and parity.* The reposition legs add `s * |f1 - o(r_k)|` and
`s * |f2 - o(r_k)|` respectively; by condition (d) the `M1` leg is no longer.
The loading, travel, and unloading phases are identical in duration under both
models (Lemma 1: they depend only on the floors `(o(r_k), d(r_k))` and the
per-trip constants, not on rider count). Summing the five phases,
`D^{M1}(r_k) <= D^{M2}(r_k)`, extending (I2).

*Invariant maintenance.* `M1` replaces `x_(1)` by `u = D^{M1}(r_k)` and `M2`
replaces `y_(1)` by `v = D^{M2}(r_k)`, with `u >= x_(1)`, `v >= y_(1)`, and
`u <= v`. Lemma 5(i) restores (I3). ∎ (case F)

### X.4.6 Inductive step, case B: `r_k` boards an in-progress `M2` trip

Under `M2`, `r_k` boards trip `tau` and completes at the shared completion
`D^{M2}(r_k) = T(tau)`; the `M2` availability vector is unchanged, because the
boarded elevator's availability was already `T(tau)` when the trip was
dispatched. Under `M1`, `r_k` is served by a fresh trip on the
earliest-available slot, completing at `D^{M1}(r_k)`.

*(I2) extension.* Condition (c*) gives `D^{M1}(r_k) <= y_(1)`. Since the
boarded elevator's availability `T(tau)` is one of the entries of the `M2`
availability vector, `y_(1) <= T(tau)`, hence
`D^{M1}(r_k) <= T(tau) = D^{M2}(r_k)`.

*Invariant maintenance.* `M1` replaces `x_(1)` by `u = D^{M1}(r_k) <= y_(1)`;
`M2`'s vector is unchanged. Lemma 5(ii) restores (I3). ∎ (case B)

Note that `M1` never batches (single-rider slots), so cases F and B are
exhaustive. [VERIFY: `M2` attempts boarding before dispatching
(`ElevatorPoolBatched.request`, simulator.py lines 366-376); when several
elevators carry matching trips the first in list order is boarded, but the
argument above uses only `T(tau) >= y_(1)`, which holds for any of them.]

### X.4.7 Conclusion and corollaries

By induction, `D^{M1}(r) <= D^{M2}(r)` for every request. Each order's finish
time is a monotone function of its requests' completions (the same AMR-side
recursion plus service constants), so every order finishes under `M1` no later
than under `M2`; taking the maximum over orders,
`C_max(W; M1) <= C_max(W; M2)`. ∎

**Corollary X.1 (single-elevator case).** *For `E = 1`, hypotheses (a), (b),
(c), (d) imply `C_max(W; M1) <= C_max(W; M2)`.* With a single elevator,
`y_(1)` equals the boarded trip's completion `T(tau)`, so the per-member form
of (c) is exactly (c*), and the theorem applies.

**Corollary X.2 (no-boarding waves).** *If no request boards any `M2` trip on
the sample path, hypotheses (a), (b), (d) alone imply
`C_max(W; M1) <= C_max(W; M2)`,* since case B never occurs. A sufficient
screening condition at the composition level: if no two requests of the
realized request sequence share an origin-destination pair within one loading
window, boarding is impossible. Caution: this must be checked at the level of
*requests*, not orders, because reposition legs of distinct orders can also
share a floor pair and board together. [VERIFY this caveat against
`simulate_wave`: reposition legs call the same `pool.request` and are
batchable.]

**Remark X.3 (why (c) is strengthened to (c*) for `E >= 2`; OPEN).** Under the
per-trip condition (c) alone, case B still extends (I2)
(`D^{M1}(r_k) <= T(tau)` is exactly the per-member form of (c)), but the
availability invariant (I3) can break, because (c) bounds `D^{M1}(r_k)` by the
*boarded* elevator's availability and not by the fleet minimum `y_(1)`.
Concrete state instance with `E = 2`, `c = 2`: sorted `M1` availabilities
`(0, 6, 9, 9)`, sorted `M2` availabilities `(5, 6)`, a boarding event on the
trip completing at `T(tau) = 6` with `D^{M1}(r_k) = 6`. Condition (c) holds
(`6 <= 6`), yet after the step the `M1` prefix becomes `(6, 6)` against
`(5, 6)`, and `6 > 5` breaks (I3) at the first coordinate. Whether such a
state is reachable from a consistent wave history, and whether the broken
invariant can propagate into an actual `C_max` violation under (a), (b), (c),
(d), is OPEN; we have neither a proof that (c) suffices at `E >= 2` nor a
wave-level counterexample. [VERIFY / OPEN: this is the single remaining gap
between the per-trip condition used in Section 4.2.1 and the proof above. If
the author cannot close it, use the fallback statement (Edit W3-E4), which
presents the general-`E` case as a conjecture.]

### X.4.8 What the proof consumes and what it derives

Conditions (c*) and (d) are sample-path exclusions consumed exactly once each:
(d) at the reposition comparison of case F, (c*) at the completion and
invariant steps of case B. Everything else is derived: the structural identity
of the request sequence (Lemma 3), the propagation of the comparison through
the AMR pool (I1 from I2), the availability bookkeeping (Lemmas 4 and 5), and
the per-trip parity (Lemma 1). The content of the proposition is therefore a
*failure-mode classification*: under a common processing sequence and AMR
assignment, the makespan ordering can fail only through the batching channel
or the repositioning channel, and excluding those two channels forces
dominance. The two channels are exhibited by Examples X.1 and X.2 (Section
X.5), each on a two-order wave.
```

## 理由 (RATIONALE)

这是任务交付物 1，完成 panel_theory 致命缺陷 3 与 required_additions 第 2 项要求的 X.4 归纳：按骨架自己的处方拆分为 (ii-a) AMR 就绪单调性（不变量 I1/I2）与 (ii-b) 电梯可用性单调性（排序可用性向量的逐坐标比较，Lemma 4/5 的删最小插入引理），步骤按"新开行程 / 搭乘在途批次"分案。两个偏离骨架的地方是数学上被迫的：(1) 必须新增条件 (d)，因为 Example X.2 证明没有它命题为假（earliest-availability 规则不看楼层位置）；(2) E>=2 时批次案的不变量维持需要把 (c) 加强为 (c*)，E=1 时二者等价，故单电梯情形在原条件 (a)(b)(c) 加 (d) 下完全闭合。所有不确定步骤已用 [VERIFY] 标出并汇总于文末。此稿供作者验证，不是定稿证明。

---

# Edit W3-E3: Necessity of the conditions, with two worked counterexamples (replaces Appendix X.5)

Target file: `paper_draft/Appendix/chain_dominance_proof_v1.0.md`, lines 104-120.

DELIVERABLE 2 (Example X.1) plus the additional Example X.2 forced by finding
1. Both examples use the simulator's exact timing semantics and default
constants: elevator speed 5 s per floor, load 2 s, unload 2 s, per-stop
pickup/dropoff service 5 s, all AMRs and serving units initially at floor 1.
They are hand-constructed minimal instances, not drawn from any experiment
(neither publication scale nor prototype scale).

## 修改前 (BEFORE)

```
## X.5 Necessity of the conditions (why dominance is not unconditional)

Because `M1` has `S = E·c` servers and `M2` only `E`, dominance is a structural
inequality, not an identity. Conditions (a)–(b) are needed because the AMR pool
feeds elevator response times back into future assignments; without a common
dispatch order the two timelines are not comparable. Condition (c) is needed
because batching synchronizes a group's completion: when `M2` clears `k` matching
requests on one trip while `M1` serves them on slots that became free at
staggered times, `M2`'s group can finish first. This is the *only* way dominance
fails, which is why the empirical violation rate (Section 5: 0.8% of waves
overall, up to 4% in the worst cell) measures precisely the batch-overtaking
frequency, and why no unconditional almost-sure dominance theorem exists. That
the ordering between many small servers and fewer batched servers is
workload-dependent is itself established (Scheller-Wolf, 2003), so a conditional
dominance is the most one can claim; the bulk-queue stochastic-comparison
template of Adan and van der Wal (1989) is the closest precedent for this
conditional one-model-dominates-another form.
```

## 修改后 (AFTER)

```
## X.5 Necessity of the conditions (why dominance is not unconditional)

Because `M1` has `S = E*c` servers and `M2` only `E`, dominance is a
structural inequality, not an identity. Conditions (a) and (b) are needed
because the AMR pool feeds elevator response times back into future
assignments; without a common processing sequence and AMR assignment the two
timelines are not comparable. Conditions (c) and (d) each exclude a concrete
sample-path mechanism, and each is necessary: dropping either one admits a
two-order wave on which `C_max(W; M1) > C_max(W; M2)`. We give both waves
explicitly; each can be verified by a single deterministic simulator call.

### Example X.1 (batch-overtaking: condition (c) is necessary)

Configuration: `E = 1` elevator, capacity `c = 2`, two AMRs, floors within
`F = 3`. Wave: order 1 from floor 1 to floor 3, released at time 0; order 2
from floor 1 to floor 3, released at time 2. Conditions (a), (b) hold (FIFO
walk; each order has its own AMR), and condition (d) holds (both fresh-trip
comparisons below reposition over zero floors in both models). Both AMRs start
at their orders' source floor 1, so neither order generates a reposition
request; each generates one delivery request `(1 -> 3)`.

`M1` timeline (two single-rider slots A and B, both at floor 1, free at 0):

| request | slot | request time | wait until | reposition | load | travel (2 floors) | unload | completion |
|---|---|---|---|---|---|---|---|---|
| order 1, deliver `(1 -> 3)` | A | 5 | 5 (idle) | none | 5 to 7 | 7 to 17 | 17 to 19 | 19 |
| order 2, deliver `(1 -> 3)` | B | 7 | 7 (idle) | none | 7 to 9 | 9 to 19 | 19 to 21 | 21 |

Order 1 finishes at 19 + 5 = 24; order 2 at 21 + 5 = 26.
`C_max(W; M1) = 26`.

`M2` timeline (one batching elevator, capacity 2, at floor 1, free at 0):

| request | action | request time | wait | reposition | load | travel | unload | completion |
|---|---|---|---|---|---|---|---|---|
| order 1, deliver `(1 -> 3)` | fresh trip | 5 | none | none | 5 to 7 (window closes at 7) | 7 to 17 | 17 to 19 | 19 |
| order 2, deliver `(1 -> 3)` | boards the trip (matching pair, 1 rider < 2, request time 7 <= window close 7) | 7 | - | - | - | - | - | 19 |

Both orders finish at 19 + 5 = 24. `C_max(W; M2) = 24 < 26 = C_max(W; M1)`.

The mechanism is exactly batch-overtaking: the batched trip's shared
completion (19) precedes the group's `M1` completion (21), because the batch's
loading window opened when the elevator became free while order 2's private
`M1` slot cannot begin loading before order 2's own request at time 7. The
two-second makespan reversal equals the release stagger.

### Example X.2 (adverse repositioning: condition (d) is necessary, and the
per-trip condition (c) alone does not characterize the failure set)

Configuration: `E = 1` elevator, capacity `c = 2`, ONE AMR, floors within
`F = 8`. Wave: order 1 from floor 1 to floor 8, order 2 from floor 8 to floor
7, both released at time 0. Conditions (a), (b) hold trivially (FIFO walk,
single AMR). No `M2` trip ever carries two requests (the two floor pairs
differ), so condition (c) holds vacuously: there is no batching event on this
sample path at all.

`M1` timeline (slots A and B at floor 1, free at 0):

| request | slot | request time | wait until | reposition | load | travel | unload | completion |
|---|---|---|---|---|---|---|---|---|
| order 1, deliver `(1 -> 8)` | A | 5 | 5 (idle) | none | 5 to 7 | 7 to 42 (7 floors) | 42 to 44 | 44 |
| order 2, deliver `(8 -> 7)` | B (availability 0 < 44, so the earliest-availability rule selects B) | 54 | 54 (idle) | 54 to 89 (B climbs 7 floors from floor 1 to floor 8) | 89 to 91 | 91 to 96 (1 floor) | 96 to 98 | 98 |

The single AMR finishes order 1 at 44 + 5 = 49 at floor 8, starts order 2
there (source floor 8 equals the AMR's floor, so no reposition request),
completes pickup service at 54, and issues the delivery request at 54. Order 2
finishes at 98 + 5 = 103. `C_max(W; M1) = 103`.

`M2` timeline (one elevator at floor 1, free at 0):

| request | action | request time | wait until | reposition | load | travel | unload | completion |
|---|---|---|---|---|---|---|---|---|
| order 1, deliver `(1 -> 8)` | fresh trip | 5 | 5 (idle) | none | 5 to 7 | 7 to 42 | 42 to 44 | 44 |
| order 2, deliver `(8 -> 7)` | fresh trip (no match, window long closed) | 54 | 54 (elevator free at 44) | none (the elevator is already at floor 8) | 54 to 56 | 56 to 61 | 61 to 63 | 63 |

Order 2 finishes at 63 + 5 = 68. `C_max(W; M2) = 68 < 103 = C_max(W; M1)`.

The 35-second reversal is exactly the seven-floor reposition leg: `M1`'s
earliest-availability rule selects slot B (free since time 0) even though B is
parked at floor 1, while slot A and the `M2` elevator both stand at floor 8,
where the request originates. This example shows two things at once. First,
condition (d) is necessary: the wave satisfies (a), (b), and (c), and
dominance still fails. Second, batch-overtaking is NOT the only channel
through which dominance fails; the repositioning channel is independent of
batching and survives even at `E = 1`. Any statement of Proposition 2 must
therefore carry condition (d).

### Discussion

That the ordering between many small servers and fewer batched servers is
workload-dependent is itself established (Scheller-Wolf, 2003), so a
conditional dominance is the most one can claim; the bulk-queue
stochastic-comparison template of Adan and van der Wal (1989) is the closest
precedent for the conditional one-model-dominates-another form, and the
failure of server-count comparisons under state-blind allocation echoes Moyal
(2013). The empirical violation rate at publication scale (Section 5: 0.8% of
waves overall, up to 4% in the worst cell) measures the frequency of the union
of the two exclusion events on freely simulated waves; Section 5.3 reports the
per-channel classification of the violating traces.
```

## 理由 (RATIONALE)

交付物 2（Example X.1，条件 (c) 必要性）按任务要求给出 k=2 同 (src,dst) 订单落入同一装载窗口的最小反例，两模型完整五阶段时间表、手算 makespan 26 对 24。注意一个诚实的偏差：任务预设的机制是"第二单等待占用中的槽位"，但在位置对齐的最小配置里那样只会得到平局（两边行程同时刻开始）；严格反转来自装载窗口的"追溯搭乘"不对称（M2 的批次行程在电梯空闲时刻 5 即开始装载，o2 在窗口关闭瞬间搭上；M1 的私有槽位不能早于 o2 自己的请求时刻 7 开始装载）。Example X.2 是本次工作发现的新反例，证明当前 X.5"批次超越是唯一失效渠道"的断言为假、条件 (d) 必要，直接响应 panel_theory required_additions 第 4 项并超出其预期。两例均可用一次 simulate_wave 调用验证（见文末 open issues），本次未运行任何模拟。

---

# Edit W3-E4: The +0 fallback for Section 4.2.1 (softened claim, proof for the single-elevator case, general case as conjecture)

Target file: `paper_draft/section4_draft_v0_1.md`, lines 130-165.

DELIVERABLE 3. Ready to paste if the author cannot close (or chooses not to
rely on) the general-`E` induction of Edit W3-E2. Two things make this
fallback different from the one anticipated in the v1.0 skeleton: condition
(d) must appear even in the special case (Example X.2 is an `E = 1`
counterexample without it), and the honest scope note must say that Block C,
where the 99.2% is measured, is entirely `E = 2`, so the measured regime is
covered by the conjecture, not by the proved case.

## 修改前 (BEFORE)

```
The load-bearing condition is **chain dominance**: for a fixed wave `W`,
`C_max(W; M1) ≤ C_max(W; M2)` (the throughput abstraction never over-states
makespan relative to true co-occupancy batching), with `M3` the stochastic
extension of `M2`. Rather than assert this empirically, we establish it as a
sample-path result under transparent conditions and characterize exactly when
it fails.

**Definition (batch-overtaking).** A batched `M2` trip carrying `k ≥ 2`
matching requests *batch-overtakes* if its shared completion time is strictly
earlier than the completion of those same `k` requests served on their own `M1`
slots: the synchronized `M2` batch finishes the group before `M1`'s staggered
parallel slots do.

**Proposition 2 (conditional chain dominance).** *Fix a wave `W` and process it
under `M1` and `M2` with (a) the same order-processing sequence and (b) the same
AMR-to-order assignment. If (c) no `M2` trip batch-overtakes on this sample
path, then `C_max(W; M1) ≤ C_max(W; M2)`.* The proof couples the two timelines
request by request: per-trip durations are identical under `M1` and `M2` (they
depend on floors and the load and unload constants, not on rider count), and at
every instant `M2` has at most the `E·c` in-flight requests that `M1`'s slots
can serve, so `M1` never queues a request that `M2` is serving; the only way a
request finishes earlier under `M2` is a batch-overtaking trip, which (c)
excludes (full proof in Appendix).

**Why the condition is structural, not cosmetic.** Because `M1` instantiates
`E·c` single-rider servers and `M2` only `E` batching servers, the dominance is
a structural inequality (more independent single-rider slots weakly beat fewer
batching servers), not a modelling identity. It therefore cannot hold
unconditionally, and batch-overtaking is the genuine channel that breaks it.
This is what makes the per-wave frequency reported in Section 5 a measurement,
not a self-consistency check. We keep two statements distinct: the *scalar,
sample-path* ordering of Proposition 2, whose frequency Section 5 reports, and
the *distribution-level* first-order stochastic dominance `F_{M1} ≥ F_{M2}` that
Theorem 2's distributionally-robust clause invokes; the latter holds exactly in
all 24 cells, while `M3`'s lognormal residual is routed to Corollary 2's bound
(§4.2.3).
```

## 修改后 (AFTER)

```
The load-bearing condition is **chain dominance**: for a fixed wave `W`,
`C_max(W; M1) <= C_max(W; M2)` (the throughput abstraction never over-states
makespan relative to true co-occupancy batching), with `M3` the stochastic
extension of `M2`. Rather than assert this globally, we state it as a
sufficient-condition result, prove it for the single-elevator case, exhibit
the two sample-path mechanisms by which it can fail, and measure how often the
conditions hold at publication scale.

**Definition (batch-overtaking).** A batched `M2` trip carrying `k >= 2`
matching requests *batch-overtakes* if its shared completion time is strictly
earlier than the completion of those same `k` requests served on their own
`M1` slots: the synchronized `M2` batch finishes the group before `M1`'s
staggered parallel slots do.

**Definition (adverse repositioning).** When a request is served by a fresh
trip in both models, the serving unit first repositions from its current floor
to the request's origin floor. Adverse repositioning occurs when the `M1` slot
selected by the earliest-availability rule stands strictly farther from the
origin than the `M2` elevator selected, so `M1` pays a longer reposition leg
for the same request.

**Proposition 2 (conditional chain dominance, single-elevator case).** *Fix a
wave `W` and process it under `M1` and `M2` with (a) the same order-processing
sequence, (b) the same AMR-to-order assignment, (c) no batch-overtaking, and
(d) no adverse repositioning on this sample path. If `E = 1` (any per-trip
capacity `c`), then `C_max(W; M1) <= C_max(W; M2)`.* The proof, given in the
Appendix, couples the two timelines request by request: per-trip loading,
travel, and unloading durations are identical under `M1` and `M2` (they depend
on floors and the load and unload constants, not on rider count), the
comparison propagates through the AMR pool by monotonicity, and conditions (c)
and (d) exclude exactly the two events at which the coupling can reverse. The
Appendix also gives two minimal two-order waves showing that (c) and (d) are
each necessary: dropping either one makes `C_max(W; M1) > C_max(W; M2)`
achievable.

**Conjecture 1 (general chain dominance).** *Under (a) to (d),
`C_max(W; M1) <= C_max(W; M2)` for every `E >= 1`.* The Appendix shows that
the same induction closes for arbitrary `E` under a strengthened form of the
batching condition, and identifies the single bookkeeping step at which the
per-trip form (c) is not known to suffice; we therefore state the general case
as a conjecture rather than a theorem. Its empirical support at publication
scale is direct: on matched waves in Block C (all configurations at `E = 2`),
the per-wave ordering `M2 >= M1` holds in 99.2% of waves on average and in at
least 96.0% of waves in the worst cell (Section 5).

**Why the conditions are structural, not cosmetic.** Because `M1` instantiates
`E*c` single-rider serving slots and `M2` only `E` batching elevators, the
dominance is a structural inequality (more independent single-rider slots
weakly beat fewer batching servers), not a modelling identity, and it cannot
hold unconditionally. Two sample-path mechanisms can break it. First, batching
synchronizes a group's completion, so a batched `M2` trip can finish a
makespan-determining group before `M1`'s staggered slots do; condition (c)
excludes exactly this event. Second, the earliest-availability rule selects a
serving unit by availability alone, ignoring floor position, so `M1` can
commit a poorly positioned slot to a request while an `M2` elevator stands at
the request's origin; condition (d) excludes exactly this event. Section 5
reports the per-wave frequency of the ordering itself and classifies the
violating waves by mechanism. We keep two statements distinct: the *scalar,
sample-path* ordering above, whose frequency Section 5 reports, and the
*distribution-level* first-order stochastic dominance `F_{M1} >= F_{M2}` that
Theorem 2's distributionally-robust clause invokes; the latter holds exactly
in all 24 publication-scale cells, while `M3`'s lognormal residual is routed
to Corollary 2's bound (§4.2.3).
```

## 理由 (RATIONALE)

交付物 3。这是 panel_theory 致命缺陷 3 的"+0 回退"路径：删除"full proof in Appendix"的全称断言，把命题降级为充分条件命题，只对可完全证明的 E=1 情形陈述为命题，一般情形明确标为 Conjecture 1，用 Block C（出版规模，全部 E=2）的 99.2%/96.0% 作为支持证据并如实注明被测量的正是猜想覆盖、而非已证情形覆盖的区间。与骨架原设想的回退有一处强制差异：条件 (d) 必须进入命题（Example X.2 是 E=1 的硬反例，没有 (d) 连特例都不成立）。"batch-overtaking is the genuine channel"与"measurement, not a self-consistency check"两句被删除或改写，前者被 Example X.2 证伪，后者按 panel_theory 缺陷 4（harness 未强制假设 (b)）目前缺乏支撑。下游连锁：§4.2.2 Theorem 2 开头的"Under the conditional chain dominance of Proposition 2"应相应改为引用"Proposition 2 and Conjecture 1"，列入 open issues。

---

# Edit W3-E5: Knock-on correction in the Section 5.3 splice (violating-wave classification claim)

Target file: `paper_draft/Experiments/chain_dominance_empirical_v1.0.md`, lines 35-43.

## 修改前 (BEFORE)

```
**Verifying the failure mode.** Proposition 2 predicts that every violating wave
is a *batch-overtaking* event, namely a synchronized `M2` batch completing a
makespan-determining group before `M1`'s staggered parallel slots. We inspect
the `≤ 0.8%` of violating waves (up to 4% in the worst cell) directly in the
matched-wave traces and confirm that each is driven by a batched `M2` trip whose
shared completion precedes the same requests' `M1` slot completions; none arise
from any other mechanism. The empirical violation set thus coincides with the
batch-overtaking set the proposition isolates, so the 99.2% is not an unexplained
shortfall from 100% but a measurement of how often condition (c) is met.
```

## 修改后 (AFTER)

```
**Verifying the failure mode.** The theory isolates two mechanisms by which
the per-wave ordering can fail: *batch-overtaking* (a synchronized `M2` batch
completes a makespan-determining group before `M1`'s staggered parallel slots;
condition (c)) and *adverse repositioning* (the earliest-availability rule
commits a poorly positioned `M1` slot while an `M2` elevator stands at the
request's origin; condition (d)). We inspect the `<= 0.8%` of violating waves
(up to 4% in the worst cell) directly in the matched-wave traces
(publication scale, Block C) and find that every violating wave contains a
batched `M2` trip whose shared completion precedes the same requests' `M1`
slot completions, that is, a positive identification of batch-overtaking on
each violating wave. A dedicated classifier for the repositioning mechanism
has not been run on these traces, so we report the batch-overtaking finding as
a positive identification, not as an exclusion of the second mechanism. The
99.2% is therefore a measurement of how often the exclusion conditions are
met on freely simulated waves, not an unexplained shortfall from 100%.
```

> Splice note (not manuscript text): the repositioning classifier, and the
> matched-assignment replay that enforces hypotheses (a) and (b) (panel_theory
> fatal flaw 4), should be filed together as a single dated, pre-analysis
> amendment before either is run, per the project's pre-registration
> discipline. Until they run, the manuscript must not claim "none arise from
> any other mechanism".

## 理由 (RATIONALE)

连锁修正：现行 §5.3 文本断言"没有任何违例来自其他机制"，但 Example X.2 证明第二个机制（adverse repositioning）在理论上真实存在，且现有的迹象检查只做了批次超越的正向识别、并未运行排除第二机制的分类器。按 panel_theory 缺陷 4 的精神，措辞改为"正向识别、非排除性结论"，既保留全部 D2 门槛数字与 PASS 判定（不重判），又不做数据尚未支撑的排除性断言。分类器与 matched-assignment 重放应作为带日期的预分析修正案先登记后运行。

---

# Open issues consolidated (must be resolved by the author before any edit lands)

1. **[CRITICAL, VERIFY FIRST] Example X.2 falsifies Proposition 2 as currently
   stated.** Verify by hand and then, when compute is free, by one call
   (milliseconds, run from `prototype/`):
   `w = Wave(orders=[Order(0,1,8,0.0), Order(1,8,7,0.0)], release_time=0.0)`;
   `simulate_wave(w, n_amrs=1, n_elevators=1, capacity=2, batched=False)`
   should return `103.0` and with `batched=True` should return `68.0`. If
   confirmed, conditions must be extended to include (d) in EVERY statement of
   Proposition 2, including the fallback.
2. **[VERIFY] Example X.1 arithmetic**:
   `w = Wave(orders=[Order(0,1,3,0.0), Order(1,1,3,2.0)], release_time=0.0)`;
   `simulate_wave(w, n_amrs=2, n_elevators=1, capacity=2, batched=False)`
   should return `26.0` and with `batched=True` should return `24.0`. Note
   order 2 uses `release_time = 2.0` (the documented Gap 2 feature); the
   boarding hinges on `request_time <= trip_loading_end` being non-strict
   (`7 <= 7`), simulator.py line 175.
3. **[OPEN] Remark X.3**: whether the per-trip condition (c) suffices at
   `E >= 2` (with (d)) is unresolved: the availability invariant provably
   breaks in a four-number state instance, but no reachable wave-level
   counterexample was constructed. Either close the gap (prove the state is
   unreachable, or prove dominance by another route) or adopt the fallback's
   conjecture framing. Block C is entirely `E = 2`, so this gap covers the
   measured 99.2% regime.
4. **[VERIFY] Lemma 3 edge cases** (orders with source equal to destination;
   orders whose source equals the AMR's floor) against simulator.py lines
   663-671, and the monotonicity audit of the AMR-side recursion (I1) against
   lines 659-676.
5. **[VERIFY] Lemma 4 / Lemma 5**: the min-replacement identity and the
   dominance-propagation corollary, including the `i = E` boundary with the
   `+infinity` convention, the premise `u >= x_(1)` (completions never precede
   the producing server's availability), and the `c >= 2` length condition.
6. **[VERIFY] Case B bookkeeping**: `board()` leaves the `M2` availability
   vector unchanged and returns the trip completion, which equals the boarded
   elevator's `available_at` (simulator.py lines 178-197); boarding is
   attempted before fresh dispatch and may pick a matching elevator that is
   not the earliest available (lines 366-376): confirm the argument only uses
   `T(tau) >= y_(1)`.
7. **[DECISION] Which statement ships**: Edit W3-E2's general theorem under
   (a), (b), (c*), (d) (requires the author to verify the full induction), or
   Edit W3-E4's fallback (E = 1 proposition plus Conjecture 1). The two are
   consistent; W3-E4 can ship now and be upgraded later.
8. **[AMENDMENT] Empirical re-audit**: the repositioning-channel classifier
   and the matched-assignment replay (enforcing (a)/(b), panel_theory flaw 4)
   should be registered as one dated pre-analysis amendment before running;
   Edit W3-E5's softened wording is written so it remains true whether or not
   that amendment is executed before submission.
9. **[MINOR] Terminology sweep**: after applying the edits, re-run the
   TERMINOLOGY.md pre-finalize checklist on the touched sections (no
   em-dashes were introduced; verify no stray ones remain in the surrounding
   text of section4_draft_v0_1.md, which currently uses en-dash-free but
   em-dash-containing constructions elsewhere).
