---
title: "§4.2.1 Proposition 2 (conditional chain dominance): statement + proof sketch, v1.0"
parent: "Wave Release Coordination under Vertical Resource Constraints, §4 Methodology"
date: 2026-06-05
status: "v1.0 draft to insert into §4.2.1, BEFORE Theorem 2 (§4.2.2). Full proof skeleton lives in Appendix/chain_dominance_proof_v1.0.md."
placement: >
  §4.2.1 currently introduces chain dominance as an empirical claim ("verified in Section 5",
  section4_draft_v0_1.md:130-134). This file UPGRADES that claim into Proposition 2, a sample-path
  sufficient-condition result, placed immediately after the chain-dominance condition is stated and
  before Theorem 2 invokes it. Numbering: Proposition 2 (Proposition 1 = Bound-and-Gap decomposition, §4.1).
honesty: >
  The result is necessarily CONDITIONAL, not unconditional: M1 has E*c independent serving slots while
  M2 has only E elevators, so dominance is a structural "fewer servers + opportunistic batching never beats
  more servers" statement, not an identity coupling. Unconditional almost-sure dominance is FALSE (the data
  show 99.2%, not 100%); the violations are exactly the batch-overtaking events the proposition excludes.
  The proof establishes the LOGIC; it does not claim a smaller numerical bound and does not contradict the data.
---

# §4.2.1 insertion: Proposition 2 (conditional chain dominance)

> *Drop-in text. Place after the sentence introducing chain dominance and before
> Theorem 2. Replaces the current "The condition is an empirical claim ...
> verified in Section 5."*

The load-bearing condition for the Hedge Rule is **chain dominance**: for every
wave `W`, `C_max(W; M1) ≤ C_max(W; M2)`, with `M3` the stochastic extension of
`M2`. Rather than assert this empirically, we establish it as a sample-path
result under two transparent conditions, and characterize precisely when it can
fail.

Recall the two deterministic models (§3). `M1` (throughput abstraction) is
realized by `E·c` independent single-rider serving slots, each executing a full
five-phase trip (wait → reposition → load → travel → unload). `M2` (true
co-occupancy batching) is realized by `E` physical elevators, each carrying up
to `c` requests that share one `(src, dst)`-matched trip; non-matching requests
queue for the next trip. Both run the *same* operational dispatch on the *same*
wave, driven by one pending-order list and one AMR pool.

**Definition (batch-overtaking).** On a given sample path, a batched `M2` trip
`τ` that carries `k ≥ 2` matching requests *batch-overtakes* if the shared
completion time of `τ` is strictly earlier than the completion time of those
same `k` requests when each is served on its own `M1` slot, that is, the
synchronized `M2` batch finishes the group before `M1`'s staggered parallel
slots do.

**Proposition 2 (conditional chain dominance).** *Fix a wave `W` and process it
under `M1` and `M2` with (a) the same order-processing sequence and (b) the same
AMR-to-order assignment. If (c) no `M2` trip batch-overtakes on this sample
path, then `C_max(W; M1) ≤ C_max(W; M2)`.*

*Proof sketch.* Two facts drive the argument (full proof in Appendix).
*Per-trip parity (Lemma 1):* a trip serving a given `(src, dst)` from a given
elevator position has identical five-phase duration under `M1` and `M2`,
because the phase durations depend on floors and the per-trip load/unload
constants, not on the number of riders. *Server-count monotonicity (Lemma 2):*
at every instant the number of in-flight requests under `M2` is at most
`E·c`, the number of `M1` slots, so `M1` never has to queue a request that `M2`
is serving, so `M1`'s waiting times are pointwise no larger. Coupling the two
timelines request by request, each request completes under `M1` no later than
under `M2`, *unless* a batched `M2` trip finishes its group earlier than `M1`'s
parallel slots, which is exactly the batch-overtaking event excluded by (c). Taking the
maximum over requests gives `C_max(W; M1) ≤ C_max(W; M2)`. ∎

**Why the conditions are necessary, not cosmetic.** Because `M1` instantiates
`E·c` servers and `M2` only `E`, dominance is a structural inequality ("fewer
elevators with opportunistic batching never beat more independent slots"), not
an identity. It therefore cannot hold *unconditionally*: a synchronized `M2`
batch can occasionally finish a makespan-determining group before `M1`'s
staggered slots, which is precisely batch-overtaking. Section 5 measures the
frequency at which condition (c) holds, namely `99.2%` of waves on average and at
least `96.0%` in the worst cell, and verifies that the residual `≤ 4%` of violating
waves are batch-overtaking events, as the proposition predicts.

**Stochastic extension.** Under `M3`, independent lognormal noise on each phase
breaks the per-trip parity of Lemma 1, so Proposition 2 does not apply directly;
the resulting approximate dominance is handled by Corollary 2's one-sided bound
`U_c(ε)` (§4.2.3), which is where the `M3` residual is routed throughout.

**Literature grounding.** Proposition 2 is a sample-path coupling result in the
spirit of stochastic-comparison theory (Stoyan, 1983; Shaked and Shanthikumar,
2007). Its mechanism is server-count monotonicity: more parallel single-rider
servers weakly reduce makespan (Moyal, 2013; Smith and Whitt, 1981), combined
with the compatibility-constrained batching of incompatible families (Uzsoy,
1995; Lee, Uzsoy and Martin-Vega, 1992), under which unmatched requests cannot
co-ride and `M2` serializes. The per-trip duration being independent of rider
count is the elevator analogue of batch-processing machines whose batch time
does not grow with the number of jobs (Lee, Uzsoy and Martin-Vega, 1992), and
the compatibility restriction mirrors the shareability condition in ride-pooling
(Santi et al., 2014), under which co-riding helps only requests that share an
origin and destination. The conditional one-model-dominates-another form follows
the bulk-queue stochastic-comparison template of Adan and van der Wal (1989);
see Deb and Serfozo (1973) and Chaudhry and Templeton (1983) for the
wait-to-batch delay penalty. The result is stated conditionally on a common
dispatch order with no batch-overtaking: consistent with Moyal's (2013) failure
of the comparison under non-greedy allocation and with the regime-dependence of
multi-server ordering (Scheller-Wolf, 2003), the small (about 0.8 %) violation
rate from synchronized batch completion is expected, not anomalous.

**A note on the sign.** This direction, in which the throughput abstraction is
the optimistic (faster) model, is the mirror image of the classic elevator
round-trip-time result that batching same-destination passengers reduces stops
and round-trip time (Kuusinen et al., 2012; So and Al-Sharif, 2019). The sign
reverses here because of two modelling assumptions we state explicitly: (a)
batching is admissible only for requests sharing the same `(src, dst)`; and (b)
the throughput model `M1` instantiates `E·c` independent single-rider servers
while `M2` has only `E` batching servers, with identical per-trip duration.
Under (a) and (b), the extra single-rider parallelism of `M1` weakly dominates
the batching economy of `M2`, except on the batch-overtaking sample paths that
Proposition 2 excludes. Stating (a) and (b) up front pre-empts the
elevator-traffic reader for whom the unqualified claim would read as
counter-intuitive.

---

## Knock-on edits this insertion requires

- **§4.2.1 / Abstract verbs:** "empirical claim / verified in Section 5" →
  "proven under conditions (with empirical condition-satisfaction frequency
  99.2%)".
- **§4.2.2 Theorem 2 opening:** "Under chain dominance" → "Under the conditional
  chain dominance of Proposition 2 (empirically holding in 99.2% of waves)".
- **§4.3 (from tools to predictions):** add Proposition 2's prediction (the
  violation set equals the batch-overtaking set) to the list Section 5 tests.
- **§4 end "Full proofs:" pointer:** add
  `Appendix/chain_dominance_proof_v1.0.md`.
- Scope: all edits live in §4 / §5 / Appendix. The pre-registration, §3, and the
  D2 PASS verdict are untouched; the 99.2% / 96.0% / FOSD 24/24 / collapse 6/6
  numbers are preserved as the empirical face of the proposition.
