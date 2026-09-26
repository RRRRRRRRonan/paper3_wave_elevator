---
title: "Introduction (§1) v1.1, submission version (English only)"
parent: "Wave Release Coordination under Vertical Resource Constraints in Multi-Story AMR Warehouses"
date: 2026-07-19
status: "supersedes the English half of introduction_v1.0.md for the manuscript; v1.0 kept as the bilingual working copy"
changes: >
  (1) W7 Edit 6 contributions paragraph applied (publication-scale C1/C2/C3), upgraded to the
  adjudicated numbering per W10 section 5.1: SPO bridge = Proposition 3 (was "Theorem 1"),
  minimax collapse = Theorem 1, DRO certification = Corollary 3 (was "Theorem 2").
  (2) C2 upgraded to the final theory package: Proposition 2 stated as ALL-E with exactly two
  identified failure channels (Lemma 6 upgrade); Theorem R added, with Corollary 1 billed as its
  specialization (W10 rule: the same monotonicity is not stated twice); delegability sentence
  ("recovered with existing methods") retained, discharging the abstract-v1.7 handoff.
  (3) C3 rewritten A-R1-compliant: binary verdict seed-stable (unanimous in 15 of 18
  configurations); the numeric share stated as a resolution- and metric-indexed reading, and the
  72% figure carries the "pre-registered partition and median metric" qualifier; PARTIAL verdict
  and AUC 0.92 discriminating power kept; the c in {2,3,4,5} sweep restored per Edit 6's
  rationale option.
  (4) Motivation paragraph honesty fixes: "the candidate models rank" -> "the deterministic
  candidate models rank" (M3 is not dominance-comparable, per W1 Edit 3 scope discipline);
  "we prove it is the distributionally-robust optimum" -> "exactly the minimax choice ...
  coincides with a calibrated distributionally-robust optimum" (W1 Edit 14 style).
  (5) Citation fixes: Wu et al. 2024 -> 2025 (bib key wu2025joint, TR-E 194:103930); Lenoble et
  al. 2018 already correct (Nicolas parsing error fixed in v1.0); Elmachtoub and Grigas 2022.
  (6) English only, no em-dashes; abstract handoff obligations all discharged (Qin positioning in
  paragraph 3, closed-form in C2, delegability in C2).
  (16) REOPENED 2026-09-02 per contribution review Themes A/B/D/E6
  (research_notes/contribution_review_2026-08-06.md; PENDING AUTHOR RE-RATIFICATION). Six
  repairs. (A1) C2 rebilled: "Its guarantee rests on Proposition 2" DELETED (Prop 2's premises
  jointly hold on under 1% of waves; the 99.2% is an empirical regularity of the simulator, not
  a consequence of Prop 2). New billing: Theorem 1 stated conditionally ("Wherever that ordering
  holds, minimax corner selection provably collapses ..."), Proposition 2 as the mechanism
  result (verifiable sufficient conditions, all-E, only two identified failure channels), plus
  the honest sufficiency note "sufficient but far from necessary ... holds on almost every wave,
  including most waves where the conditions fail". (A2) Motivation paragraph: "with a computable
  worst-case-loss bound" DELETED (banned Cor 2 wording per W10; U_c bounds the M2-side corner
  -median perturbation, not the rule's worst-case loss); robustness claim made conditional ("on
  every wave where the ordering holds"). C2's Cor 2 sentence now states the bound's actual
  object. (D) "Corollary 1 applies this to the specific wave classes used in our experiments"
  was false (the truncated-corner instrument is non-covering; 2x2 to 3x3 is non-nested); now
  "applies this to the nested grouping families we validate in Section 5". (B1) Ceiling claim
  narrowed everywhere to the partition-constant class ("no partition-constant release policy" in
  C2, "no group-level release rule" in the motivation), because P9's wave-level policy beat the
  corner-oracle budget in 7/12 cells. (B2) C3 rewritten dual-instrument: capacity-dominance kept
  ONLY under the A-R1 qualifier (72% Phi-rule share), covering variant added (roughly 47%, SE
  0.14, neither side dominates), "capacity is the binding side" headline DELETED, Theorem R
  sentence scoped to the resolution dependence (it does not govern the instrument difference).
  (E5+E6) "passes every pre-registered test" -> "passes all four of its pre-registered tests"
  (C-4 informativeness threshold FAILED, reported in Section 5); delegability lowered to the
  locked ladder ("existing methods can target the slack; an off-the-shelf learner partially
  recovers it"), replacing "can be recovered with existing methods".
  (15) C3 evidence block de-jargoned (author feedback 2026-07-31): "passes every gate" ->
  "passes every pre-registered test"; "per-wave dominance ... six-configuration model-chain
  block" -> "the ordering it relies on holds in ... the six configurations where the models are
  compared" (leans on C2's chain-dominance introduction); "corner" -> "wave class" (continuity
  with C2/Theorem R sentence); "matches the Wasserstein-DRO optimum" -> "is the one a full
  distributionally-robust optimization would select"; "sub-cells" -> "experimental cells";
  "resolution gate ... PARTIAL" -> "statistical test resolves a nonzero value ... which we
  report as a partial pass"; AUC glossed as discriminating power; "finer partition" -> "finer
  grouping". All locked numbers and verdicts unchanged (99.2%, 96.0%, c 2-5, 6/6, 72/72, 57/72
  partial, AUC 0.92); formal vocabulary (gates, corners, sub-cells, PARTIAL, Block C) debuts in
  Section 5 where it is defined.
  (14) C3 share-qualifier sentence made plain (author feedback 2026-07-31): "a property of the
  measurement setup ... in the direction Theorem R predicts" -> "a measured share, not a
  universal constant. It changes when waves are grouped more finely or summarized with a
  different statistic, and Theorem R makes this dependence predictable rather than arbitrary."
  PRECISION NOTE: deliberately no direction claim for the SHARE itself. Theorem R's
  monotonicity is about the ceiling H_up (the numerator); the percentage H_up/GAP is not
  guaranteed monotone because GAP moves too. The abstract's and C2's "can only raise the
  ceiling" statements are about H_up and remain correct; do not copy that direction onto the
  72% share anywhere in the manuscript.
  (13) C3 opening made value-first (author feedback 2026-07-31): leads with the operator's
  investment question (smarter waves vs more capacity), then the stable answer; qualifier kept
  in the verdict sentence ("under the pre-registered wave grouping and the median metric"); the
  A-R1 indexing rendered in plain words ("a property of the measurement setup ... moving with
  how finely waves are grouped and with the chosen metric") with the Theorem R echo; added the
  28% complement for interpretability. Zero colons and semicolons retained.
  (12) C3 restructured headline-first (author feedback 2026-07-31): opening now states the
  main finding (stable answer to the capacity-versus-policy question), with the A-R1 qualifier
  attached IN the same sentence as the 72% figure ("under the pre-registered partition and the
  median metric"); evidence follows (study scale, Hedge gates, identities, PARTIAL), payoff
  closes; all semicolons and colons removed from the paragraph; "c in {2,3,4,5}" -> "per-trip
  capacities from 2 to 5"; "(worst cell 96.0%)" -> "at worst 96.0% in a single cell". All locked
  verdicts and numbers unchanged.
  (11) Proposition 2 sentence in C2 made plain (author feedback 2026-07-31): the noun pile
  "per-wave chain dominance result ... with exactly two identified failure channels" rewritten
  as two sentences that point back to paragraph 4's plain-language ordering ("this wave-by-wave
  ordering, called chain dominance"), name the term once, state the all-E scope, add "under
  verifiable conditions" (honest: Prop 2 is conditional, and testability is a selling point),
  and render the two-channel necessity as "the only two ways the ordering can fail".
  (10) Theorem R sentence in C2 made plain (author feedback 2026-07-31): "describes how the
  split moves as the partition is refined" -> "shows that grouping waves more finely can only
  raise the ceiling" (verbatim echo of the ratified abstract wording); "specialized to the
  implemented corners" -> "applies this to the specific wave classes used in our experiments"
  ("corners" is Section 3/4 vocabulary, not yet introduced in Section 1).
  (9) C2 de-fragmented (author feedback 2026-07-31): the two semicolon-nested mega-sentences
  rewritten as short complete sentences, one result per sentence, parallel billing ("The first
  ... is diagnostic." / "The second tool ... is prescriptive."); all eight formal results,
  delegability, all-E scope, two failure channels, and closed-form claim preserved verbatim in
  content.
  (8) Motivation-paragraph "exactly the minimax choice" -> "minimizes the worst-case makespan
  across the candidate models" (author feedback 2026-07-19, same policy as abstract v1.1d: plain
  meaning in narrative prose, the term minimax kept only in formal statements, i.e. C2's
  "minimax corner selection" and Section 4's Theorem 1).
  (7) Paragraph-3 coupling sentence rewritten (author feedback 2026-07-19): forward references
  removed ("the fleet scheduler", "the tactical and operational layers" belong to paragraph 4,
  which introduces the two-stage naming); the argument now uses only paragraph-2 concepts (wave
  composition, AMR dispatch), split into two sentences, with "We therefore formalize" making the
  gap-to-necessity-to-naming chain explicit.
word_note: "no journal word cap applies to Section 1; length is in the normal C&IE range"
---

# Section 1. Introduction (v1.1, submission version)

The growth of e-commerce and the demand for next-day delivery have pushed
distribution centers into dense urban areas where land is scarce and expansion
is constrained. Operators increasingly turn to multi-story fulfillment
buildings: floors stacked vertically, with autonomous mobile robots (AMRs)
handling horizontal movement on each floor and a few freight elevators
connecting them. The primary bottleneck has shifted from floor space or fleet
size to elevator capacity, and AMRs often idle while waiting for an elevator.

Operators relieve this congestion by releasing orders in waves: within a short
release window, a selected subset of orders is dispatched simultaneously. The
composition of each wave, that is, which orders to bundle, directly determines
how many vertical transitions the elevators must serve, in which directions, and
with what temporal stagger; it therefore sets the difficulty of the downstream
dispatch problem before any AMR moves. In current practice, wave composition is
set heuristically, by destination floor, carrier cutoff, or arrival order. Yet
the wave layer is the cheapest place to relieve a vertical bottleneck, because
re-batching already-released orders changes neither the layout nor the fleet
size.

Four elements, namely wave composition, multi-story deployment, flexible AMR
fleets, and shared-elevator capacity, have largely been studied in isolation.
The closest precedents treat the lift as a constraint under fixed wave content
(Chakravarty et al., 2025) or batch orders inside a single vertical lift module
(VLM) (Lenoble et al., 2018); multi-story Robotic Mobile Fulfillment System
(RMFS) work avoids the coupling by confining shuttles to a tier (Wu et al.,
2025); planar AMR work optimizes wave cardinality on a single floor (Qin et
al., 2024). Each of these precedents sidesteps the coupling by restricting the
setting: fixing the wave content, or confining transport to a single device or
a single tier. In the general setting we study, however, a flexible AMR
fleet shares building-wide elevators and wave composition is itself a decision.
The two choices then cannot be separated: the chosen wave fixes the elevator
trip distribution (how many vertical transitions, in which directions, with
what stagger) before any AMR is dispatched, so optimizing wave composition and
fleet dispatch in isolation loses exactly the bottleneck interaction that
matters. We therefore formalize the intersection of these four elements as the
wave-release coordination problem under vertical resource constraints;
Section 2 details the precedents.

The problem decomposes naturally into two stages: a tactical stage composes
each wave, and an operational stage dispatches the AMRs that deliver its orders
through the shared elevators. We hold the operational stage fixed and study the
tactical stage with two complementary analytical tools, both built on a
three-dimensional representation `Φ = (C, I, T)` of each wave: its vertical
spread `C`, directional imbalance `I`, and temporal clustering `T`. Two
structural features motivate the tools. First, the value that wave structure
can deliver varies across operating regimes. The shared elevator is the
bottleneck: in some regimes makespan is controlled by the elevator's capacity
and can be relieved only by adding capacity, while in others it depends on how
waves are composed, so the wave-release policy can relieve it. The value
therefore has two parts. One is fixed by capacity, and no group-level release
rule can recover it. The other is slack that a `Φ`-informed wave-release policy can
recover, the operational dispatch being held fixed. Which part dominates shifts
across regimes, so the value of composing waves must be measured before it is
pursued. Second, the operator does not know which elevator model is true, yet
on almost every wave the deterministic candidate models rank the makespans in
the same order. Among them the most conservative, true co-occupancy batching,
is weakly the slowest and serves as a worst-case reference. This ordering holds
wave by wave, not only on average. The operator can therefore score the
candidate waves against that single reference and release the one that
minimizes makespan under it. That choice is robust: on every wave where the
ordering holds, we prove it minimizes the worst-case makespan across the
candidate models and coincides with a calibrated distributionally-robust
optimum. The two tools act on the same
decision (which wave-structure to release): the first measures how much that
choice is worth and how much of it a group-level release rule can recover, and
the second uses the reference model to select the robust one.

This paper makes three contributions.

**(C1) Problem formulation.** We formalize wave-release coordination under
vertical resource constraints as a two-stage scheduler: a tactical stage
composes waves; an operational stage dispatches a flexible AMR fleet through
shared freight elevators. Its four defining elements (wave composition as a
decision, multi-story deployment, a flexible AMR fleet, and shared elevator
capacity) have been studied only in isolation, with wave content or request set
fixed or transport confined to a single device or tier; our formulation models
the coupling explicitly.

**(C2) Methodology.** We develop two analytical tools on the wave
representation `Φ = (C, I, T)`. The first, the Bound-and-Gap decomposition, is
diagnostic. It splits the value of wave structure, `GAP`, into a structural
ceiling `H_up` that no partition-constant release policy can recover and a
recoverable slack `M_Φ` (Proposition 1). We show that `M_Φ` equals the
predict-then-optimize decision loss of a partition-constant predictor
(Proposition 3; Elmachtoub and Grigas, 2022), so existing predict-then-optimize
methods can target the slack. In our experiments an off-the-shelf learner
partially recovers it (Section 5). A resolution theorem shows that grouping
waves more finely can only raise the ceiling (Theorem R), and Corollary 1
applies this to the nested grouping families we validate in Section 5. The
second tool, the Model-Dominance Hedge Rule, is prescriptive. It selects the
wave-structure to release in closed form, without identifying the true elevator
model. The rule is built on a wave-by-wave ordering, called chain dominance,
in which true co-occupancy batching is weakly the slowest candidate model on
each wave. Wherever that ordering holds, minimax corner selection provably
collapses to the corner optimal under true co-occupancy batching (Theorem 1)
and coincides with the corner-calibrated Wasserstein distributionally-robust
optimum (Corollary 3; Mohajerin Esfahani and Kuhn, 2018). Proposition 2
characterizes the ordering itself. It gives verifiable sufficient conditions
that hold for any number of elevators, and it proves that the ordering can
fail in only two identified ways. These conditions are sufficient but far from
necessary. In our simulations the ordering holds on almost every wave,
including most waves where the conditions fail (Section 5). When dominance
holds only approximately, Corollary 2 gives a computable upper bound `U_c(ε)`
on the resulting perturbation of the corner medians under true co-occupancy
batching.

**(C3) Empirical capacity-versus-policy diagnosis.** For an operator, the
practical question is whether makespan is better improved by composing waves
more smartly or by adding elevator capacity. Our main finding is that this
question has a measurable answer, and that the answer depends on how the value
of wave composition is split between the two sides. Under the pre-registered
wave grouping and the median metric, the capacity side dominates, with about
72% of the mean value of wave composition (`GAP`) sitting in the structural
ceiling and about 28% left as slack that a better release policy can still
claim. That verdict is stable across random seeds and unanimous in 15 of 18
configurations. Under a covering variant of the same measurement, defined in
Section 5, the ceiling's share is instead roughly 47% (standard error 0.14),
and neither side clearly dominates. The share is therefore a property of the
measurement, not a universal constant, and we report both readings side by
side. It also changes when waves are grouped more finely or summarized with a
different statistic, and Theorem R makes the resolution dependence predictable
rather than arbitrary. These findings come from a pre-registered
publication-scale study of 18 configurations and 106,800 simulations, with
every verdict reported as it stands. The Hedge Rule passes
all four of its pre-registered tests. The ordering it relies on holds in 99.2% of the
matched wave pairs in the six configurations where the models are compared,
never dropping below 96.0% in any single cell, and persists as elevator
capacity varies from 2 to 5 loads per trip. In all six of those
configurations, the wave class the rule selects is the one a full
distributionally-robust optimization would select. The decomposition's two
identities hold exactly in all 72 experimental cells. Its statistical test
resolves a nonzero value of wave composition in 57 of the 72 cells, which we
report as a partial pass. The unresolved cells are precisely those where the
value is smallest (discriminating power, AUC 0.92), so the decomposition
detects value wherever there is meaningful value to detect. Together, the
tools tell an operator, regime by regime, when smarter wave composition pays
and when the lever is instead more capacity or a finer grouping.

Section 2 reviews the related literature. Section 3 formulates the problem.
Section 4 develops the two tools. Section 5 presents the computational
experiments. Section 6 concludes.
