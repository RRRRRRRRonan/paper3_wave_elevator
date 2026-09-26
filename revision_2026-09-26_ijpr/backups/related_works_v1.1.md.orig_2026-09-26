---
title: "Section 2: Related Works, v1.1, submission version (English only)"
parent: "Wave Release Coordination under Vertical Resource Constraints in Multi-Story AMR Warehouses"
date: 2026-07-31
status: "supersedes the English half of related_works_v1.0.md for the manuscript; v1.0 kept as the bilingual working copy"
changes: >
  (1) W7 Edit 1 applied: paragraph 3 (multi-story RMFS / shuttle) softened from "typically" to
  "most", Wang et al. (2025) inserted as the explicit exception to tier confinement, and the
  closing delta sentence rewritten ("a contention to be rescheduled after the request set is
  fixed"). Citation written "Wang et al. (2025)" per the five-author Crossref record (Wang, Tao,
  Chen, Zhu, Yang; C&IE 210:111559), NOT "Wang, Tao and Yang" as in W7's pre-check draft.
  (2) Adjudicated numbering (W10 section 5.1): "Theorem 1 gives this loss a partition
  perspective" -> Proposition 3; "Theorem 2 and Proposition 2 show" -> "Theorem 1, Corollary 3,
  and Proposition 2 show".
  (3) SCOPE FIX in the same sentence: v1.0 claimed the minimax selection "over {M1, M2, M3}"
  coincides with the DRO optimum; the exact theory covers the deterministic pair only (W1 Edit 3
  discipline), and the M1/M2/M3 codes are Section 3 vocabulary. Rewritten as "over the
  deterministic elevator models", code-free.
  (4) Theorem R analogue added to methodological thread 1 (03 checklist item 3, placed in
  Section 2 rather than 4.1.4): Blackwell's comparison of experiments + partition-based bounds
  for stochastic programs (Song and Luedtke, 2015, DOI 10.1137/140967337). Both need bib
  entries; flagged on the 09_References checklist.
  (5) "stated as a decision loss rather than as the retired Phi-predicts-makespan surrogate" ->
  "stated as a decision loss, not as a claim that Phi predicts makespan" (no project-history
  language in the manuscript).
  (6) "minimax wave-corner selection" -> "minimax wave-structure selection" ("corner" debuts in
  Section 4); "throughput aggregation" -> "throughput abstraction" (TERMINOLOGY canon);
  "Three surveys frame the landscape" -> "Recent surveys" (the list has four items).
  (7) English only; no em-dashes; Boysen and de Koster (2025) citation retained (author's full
  read remains on the W10 section 6.2 to-do list).
  (8) 2026-08-06 full-bibliography verification (workflow wf_4f2e56d7, 31 refs web-verified):
  "Chenreddy and Delage, 2023" corrected to "Chenreddy et al., 2022" (the 2023 two-author paper
  does not exist; content matches Chenreddy, Bandi and Delage, NeurIPS 2022); Wu citations
  disambiguated per APA same-surname rule to "Z. Wu et al. (2024)" (Zhaoyun Wu, Processes) and
  "J. Wu et al. (2025)" (Jingwen Wu, TR-E; the bib's wrong given names also fixed). All 31
  missing bib entries added to references_related_works.bib as the verified 2026-08-06 block.
---

# Section 2. Related Works (v1.1, submission version)

Our work sits at the intersection of several established bodies of literature,
each touching a part of the problem without addressing its joint form. We
position the contribution in two steps: recent surveys frame the warehouse-OR
landscape, then four problem-class threads whose intersection defines our gap,
and finally three methodological threads (two bridges and one contrast). Recent
surveys frame the landscape: Boysen and de Koster (2025) give a fifty-year,
three-generation classification that places robotized distribution centers as
the current generation; Boysen, de Koster and Weidinger (2019) survey
warehousing in the e-commerce era; Azadeh, De Koster and Roy (2019) review
robotized and automated warehouse systems; and Pardo et al. (2024) provide the
most recent taxonomy of the order-batching family. Within the scope of these
surveys we do not find wave-release coordination under shared, multi-story
elevator coupling treated as a standalone problem class, consistent with our
positioning this work as a formalization step.

Treating the composition of an order batch as a decision variable, not merely
its size, has a long tradition in warehouse OR, but almost entirely in planar or
device-level settings. Gademann et al. (2001) study wave picking with a makespan
objective in parallel-aisle warehouses; Bozer and Kile (2008) and the canonical
treatment of Bartholdi and Hackman (2019) embed the decision in walk-and-pick
systems; Ardjmand et al. (2018) minimize order-picking makespan with multiple
pickers (our objective, but single-floor and without a shared vertical
resource); and Rasmi et al. (2022), Schiffer et al. (2022) and Haouassi et al.
(2022) extend wave and order-line batching in e-commerce settings. AMR-assisted
variants enlarge the decision class: Scholz, Schubert and Wäscher (2017) jointly
solve order batching, batch assignment and picker routing; Žulj et al. (2022)
lift it to AMR-assisted picker-to-parts systems; and Qin, Kang and Yang (2024)
study a single-layer multi-tote system, use the word "wave" for processing
batches, and identify an optimal wave cardinality. At the device level, Lenoble,
Frein and Hammami (2018) study order batching across several vertical lift
modules, and Boysen, Fedtke and Weidinger (2018) the minimum order-spread
sequencing problem in automated sorting; the mathematics in both is internal to
a single device and does not generalize to multi-elevator capacity shared across
a horizontal AMR fleet. Recent RMFS batching work (e.g., Liu et al., 2025)
likewise targets single-tier picking throughput rather than vertical coupling.
Our delta is to represent wave composition through Φ in a multi-story setting so
that it shapes the elevator trip distribution; remove the multi-story dimension
or the shared elevator and our problem collapses to their planar subclass.

Multi-story Robotic Mobile Fulfillment Systems (RMFS) and multi-tier shuttle
systems make vertical transport explicit, but most decouple tiers by confining
shuttles or pods to a tier, or by modeling the lift as an exogenous queue, with
the task set given. Z. Wu et al. (2024) schedule inbound jobs in a four-way
shuttle system; Tadumadze et al. (2023) assign orders and pods to picking stations in a
multi-level RMFS; Lamballais, Roy and De Koster (2017) give queueing estimates
of RMFS performance. On the shuttle-based storage-and-retrieval (SBS/RS) side,
Tappia et al. (2017) provide the canonical queueing model of multi-tier compact
storage with lifts, and Chen et al. (2023) schedule retrieval requests under two
lifts to minimize makespan (the closest published analogue to ours, but
operational, with the task set given, and for SBS/RS rather than floor-bound
AMRs); more recent integrated work (J. Wu et al., 2025) still optimizes picking
and replenishment within a single tier. A recent exception to tier confinement is
Wang et al. (2025), who schedule retrievals in a four-directional shuttle-based
compact storage and retrieval system whose tier-to-tier shuttles traverse tiers
via two shared, heterogeneous lift types (shuttle lifts and bin lifts), jointly
deciding request sequencing and the coordinated shuttle and lift schedules that
minimize makespan, combining logic-based Benders decomposition with adaptive
large neighborhood search and tabu search. The decision layer, however, is
unchanged: the work remains at the operational stage, its retrieval-request set
is exogenous, no wave-composition decision exists upstream, and its
tier-to-tier shuttles are storage-and-retrieval devices rather than a
floor-bound AMR fleet contending for building-level freight elevators. Our
delta is to treat the cross-tier lift coupling as something an upstream
tactical decision, wave composition, can manage, rather than a contention to be
rescheduled after the request set is fixed.

The precedents closest to our physical setting treat the elevator as a contended
constraint under fixed wave content. Chakravarty et al. (2025) compute provably
optimal lift schedules for AMR fleets via Boolean satisfiability, with an
exogenous task set; Tsai et al. (2025) optimize elevator standby strategies in
smart buildings; and Richer, Bierlaire and Torres (2024) give an OR treatment of
static elevator dispatching under destination control. These works optimize lift
dispatch given an arrival process; we optimize the wave that generates it. A
parallel line controls warehouse fleets through learning rather than formal
optimization: Crites and Barto (1998) established the reinforcement-learning
treatment of elevator group control, and the line continues today
(traffic-pattern-aware deep RL dispatching, Wan, Lee and Shin, 2024; deep RL for
batch-order scheduling in RMFS, Cheng et al., 2024; multi-robot task allocation,
Ma et al., 2025, Dhanaraj et al., 2025, Wen and Ma, 2024; and an RL-for-AMR
-fleets survey, Wesselhöft et al., 2022). These methods learn dispatch
end-to-end at the operational layer and answer a different question from ours:
they expose neither the Bound-and-Gap structural-versus-recoverable split nor a
training-free closed-form reference, so we regard them as complementary rather
than competing. Finally, a note on sign: the classic elevator round-trip-time
(RTT) literature shows that batching same-destination passengers reduces stops
and round-trip time (Al-Sharif et al., 2014; So, Al-Sharif and Chan, 2022), that
is, an individual-rider model overstates travel time, whereas our chain
dominance runs the opposite way (true co-occupancy batching is weakly slower
than the throughput abstraction); the sign follows from two assumptions of our
setting, detailed in Section 4.

Three methodological threads ground our two tools; the first two are connected to
them by precise equivalences in Section 4, the third by a structural contrast.
First, the prediction-to-decision regret literature bounds the loss when a
learned predictor drives a downstream optimizer (Elmachtoub and Grigas, 2022;
Vera et al., 2021; Chenreddy et al., 2022), with recent decision-focused
-learning surveys (Mandi et al., 2024) and predict-then-optimize generalization
bounds (El Balghiti et al., 2023) characterizing the learnability of that loss.
Proposition 3 gives this loss a partition perspective: the policy slack `M_Φ` of
our decomposition equals the SPO loss of a partition-constant predictor, so
existing decision-focused methods can recover it, stated as a decision loss, not
as a claim that `Φ` predicts makespan. The resolution behavior of the
decomposition draws on a second classical idea, that refining a partition can
only sharpen what it reveals, familiar from Blackwell's comparison of
experiments (Blackwell, 1953) and from partition-based bounds for stochastic
programs (Song and Luedtke, 2015); Theorem R gives this monotonicity an exact
form for the ceiling component of our decomposition. Second, Wasserstein
distributionally-robust optimization hedges against the worst-case distribution
within a transport-distance ambiguity ball, typically reformulated as a convex
program (Mohajerin Esfahani and Kuhn, 2018; Blanchet and Murthy, 2019; Gao and
Kleywegt, 2023; with foundations in Delage and Ye, 2010, and Bertsimas et al.,
2011); the contextual-optimization survey of Sadana et al. (2025) unifies both
bridges within one literature. Theorem 1, Corollary 3, and Proposition 2 show
that our minimax wave-structure selection over the deterministic elevator
models coincides with this Wasserstein-DRO optimum and collapses to a
closed-form rule under conditional chain dominance. Third, robust scheduling
under model uncertainty (Lu and Shen, 2021; Wiesemann et al., 2013) hedges
parametric variation within a single agreed model class; our elevator-modeling
uncertainty is structurally different (the throughput abstraction and true
co-occupancy batching are qualitatively distinct models, not parameterizations
of one family), and the Model-Dominance Hedge Rule addresses exactly this
structural model-class uncertainty.

Collectively, the four problem-class threads each focus on a different facet of
the wave-elevator coupling; this paper integrates the four-way interaction of
wave composition, multi-story deployment, flexible AMR fleets and shared elevator
capacity into a single decision problem. The first two methodological threads
provide the frameworks our equivalence theorems extend, and the third positions
the tools against a competing approach.
