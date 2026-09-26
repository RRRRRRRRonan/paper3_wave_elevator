---
title: "Appendix: Proof of Proposition 2 (conditional chain dominance), v1.0 skeleton"
parent: "Wave Release Coordination under Vertical Resource Constraints, Appendix"
date: 2026-06-05
status: "v1.0 PROOF SKELETON. Lemmas + coupling structure + necessity remark are laid out; the request-by-request induction is sketched and flagged for tightening. +0 fallback: if the induction does not close cleanly, the result still publishes as a sufficient-condition proposition with the empirical 99.2% as its condition-frequency."
companion: "Methodology/proposition2_chain_dominance_v1.0.md (the §4.2.1 statement + sketch)"
scope: "Theory only, no new simulation. The empirical side (condition-(c) frequency + batch-overtaking verification) is in Experiments/chain_dominance_empirical_v1.0.md."
---

# Appendix X. Proof of Proposition 2 (conditional chain dominance)

## X.1 Setup and notation

Fix a wave `W = {o_1, …, o_n}` and an operational dispatch (FIFO or cluster).
Both models are driven by the *same* pending-order list and the *same* AMR pool
`A`; the only difference is the elevator subsystem.

- **`M1` (throughput abstraction):** `ElevatorPool(E, c)` instantiates
  `S := E·c` independent single-rider slots. A slot request `(f_amr, f_tgt, t)`
  returns `unload_end` of a full five-phase trip and is assigned to the slot
  with the earliest availability.
- **`M2` (true batching):** `ElevatorPoolBatched(E, c)` instantiates `E`
  elevators. A request `(src, dst, t)` *boards* an in-progress trip iff that
  trip matches `(src, dst)`, has fewer than `c` riders, and `t` precedes its
  loading-window close; otherwise it dispatches a new trip on the
  earliest-available elevator.

For request `r`, write `D^{M}(r)` for its delivery (completion) time under model
`M`. The makespan is `C_max(W; M) = max_{r} D^{M}(r) − τ_W`.

A single trip's duration, from elevator floor `f_e` serving `(src, dst)`, is
```
δ(f_e, src, dst) = |f_e − src|·s  (reposition)  + ℓ  (load)
                 + |src − dst|·s  (travel)       + u  (unload),
```
with per-floor speed `s` and constants `ℓ, u`. **`δ` does not depend on the
number of riders** (load/unload are per-trip constants in both models).

## X.2 Lemma 1 (per-trip parity)

*From the same elevator position, a trip serving `(src, dst)` has identical
duration `δ(f_e, src, dst)` under `M1` and `M2`.*

Immediate from the definition of `δ`: both models use the same five-phase timing
and the same per-trip constants; rider count enters neither. This is the elevator
analogue of batch-processing machines whose batch time is independent of the
number of jobs (Lee, Uzsoy and Martin-Vega, 1992). ∎

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

## X.6 Stochastic extension (`M3`) and linkage to Corollary 2

Under `M3`, each phase duration is scaled by an independent lognormal multiplier,
so Lemma 1's per-trip parity fails: two trips with identical `(f_e, src, dst)`
can have different durations under `M1`/`M3`. Proposition 2 therefore does not
extend to `M3`; the approximate dominance `P[C_max(W;M2) ≥ C_max(W;M1)] ≥ 1 − ε`
is handled by Corollary 2's one-sided bound `U_c(ε)` (§4.2.3). This keeps the
deterministic sample-path argument ({`M1`, `M2`}) cleanly separated from the
stochastic residual (`M3`), as flagged in §4.2.1.

## X.7 What this proof does and does not claim

- **Does:** establish `C_max(W; M1) ≤ C_max(W; M2)` as a sample-path theorem
  under (a)–(c); identify the unique failure mode (batch-overtaking); explain the
  observed 99.2% as the condition-(c)-satisfaction frequency.
- **Does not:** claim unconditional almost-sure dominance (false on the data);
  claim a tighter numerical bound than the existing `U_c`/`Δ_c` (their looseness
  under strong dominance is unchanged and is "appropriately soft" in the
  knife-edge regime); touch the locked pre-registration or any D2 gate verdict.
