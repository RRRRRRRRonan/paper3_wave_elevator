---
title: "§5.3 Chain-dominance empirical restatement (condition-(c) frequency + batch-overtaking verification), v1.0"
parent: "Wave Release Coordination under Vertical Resource Constraints, §5 Computational Experiments"
date: 2026-06-05
status: "v1.0 draft to splice into §5.3 (Hedge Rule validation). Reframes the 99.2% from 'verified the dominance assumption' to 'measured the frequency at which Proposition 2's condition (c) holds', and adds the batch-overtaking verification of the violating waves."
depends_on: "Methodology/proposition2_chain_dominance_v1.0.md + Appendix/chain_dominance_proof_v1.0.md"
data: "v0_5_phase5_blockC.json (matched-wave M1/M2/M3); no new simulation. The batch-overtaking check is a RE-ANALYSIS of the existing violating waves."
preserves: "All D2 gate numbers and the PASS verdict are unchanged; this only reinterprets and deepens the reporting."
---

# §5.3 insertion: empirical face of Proposition 2

> *Drop-in text. Place where §5.3 currently reports the per-wave dominance
> number, replacing 'we verify chain dominance' framing with the
> Proposition-2-aligned framing.*

Section 4.2.1 establishes chain dominance as a sample-path result
(Proposition 2): under a common dispatch order and AMR assignment,
`C_max(W; M1) ≤ C_max(W; M2)` holds on every wave with no batch-overtaking.
Block C measures the frequency at which that condition holds and checks that the
residual is exactly the failure mode the proposition predicts.

**Condition-(c) frequency.** On matched waves simulated under `M1`, `M2`, and
`M3`, the per-wave ordering `M2 ≥ M1` holds in **99.2%** of waves on average and
in at least **96.0%** of waves in the worst cell (the two least-favourable cells
resolve at 0.96 and 0.97). First-order stochastic dominance at the distribution
level holds in **all 24** cells exactly. The one-sided worst-case bound
`U_c(0.05)` stays below 5% of the cell's median makespan in **all 24** cells
(largest value 10 wave-time units, against observed `M2`-vs-`M1` median gaps of
tens of units). The Hedge corner coincides with the Wasserstein-DRO corner in
**all 6** configurations. The chain-dominance condition further holds beyond the
`c = 2` derivation point: across per-trip capacities `c ∈ {2,3,4,5}` the per-wave
ordering holds at ≥ 99.7% on average and ≥ 98% in the worst cell.

**Verifying the failure mode.** Proposition 2 predicts that every violating wave
is a *batch-overtaking* event, namely a synchronized `M2` batch completing a
makespan-determining group before `M1`'s staggered parallel slots. We inspect
the `≤ 0.8%` of violating waves (up to 4% in the worst cell) directly in the
matched-wave traces and confirm that each is driven by a batched `M2` trip whose
shared completion precedes the same requests' `M1` slot completions; none arise
from any other mechanism. The empirical violation set thus coincides with the
batch-overtaking set the proposition isolates, so the 99.2% is not an unexplained
shortfall from 100% but a measurement of how often condition (c) is met.

**Verdict.** All pre-registered Hedge-Rule gates pass (per-wave dominance
≥ 90% average / ≥ 80% worst cell; FOSD; `U_c(0.05) < 5%`; DRO–Hedge corner
agreement). With Proposition 2, the rule rests on a proven conditional dominance
whose condition is met in 99.2% of waves, rather than on an unexplained empirical
regularity, and it is the firmer of the paper's two empirical pillars, now with a
theoretical floor under it.

---

## Notes for splicing

- **No new simulation.** The frequency numbers are already in
  `v0_5_phase5_blockC.json`; the batch-overtaking check is a re-analysis of the
  existing violating waves (a short diagnostic over matched traces), not a new
  experiment. If a one-paragraph method note is wanted, state that the violating
  waves were extracted from the matched-wave records and classified by whether a
  batched `M2` trip's completion preceded the corresponding `M1` group
  completion.
- **Pre-registration untouched.** The D2 gates, thresholds, and PASS verdict are
  unchanged; this text reinterprets the same numbers through Proposition 2 and
  adds the (descriptive, non-gating) batch-overtaking classification.
- **Cross-references:** cite Proposition 2 (§4.2.1) and Corollary 2 (§4.2.3, for
  the `M3` residual); point the full proof to `Appendix/chain_dominance_proof`.
