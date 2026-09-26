> 提取说明：本文件由 `Section 4.docx (2026-05-28, archived)` 自动提取（2026-07-19），仅用于修订对照。Word 公式（OMML）被压平成行内文本，格式细节以 docx 为准。


## Methodology

Section 3 cast the wave release coordination problem as a simulation-based decision problem with a combinatorial decision space and an objective Cmax(W;M) realized by an event-driven simulator. Direct enumeration is intractable, so this section develops two analytical tools that operate on the structured representation Φ(W) of Section 3 and on a finite partition of Φ-space. The first, a Bound-and-Gap framework (Section 4.1), decomposes the value of wave-structure information into two non-negative components and rests on a decomposition theorem together with an equivalent to Smart-Predict-then-Optimize regret on a partition-constant predictor class. The second, a Model-Dominance Hedge Rule (Section 4.2), reduces the dispatch decision under elevator-model uncertainty to a closed-form policy and rests on a minimax-collapse theorem together with an equivalence to a Wasserstein distributionally robust solution under chain dominance. Each tool is stated here as a theorem with a proof sketch; Section 4.3 lists the structural predictions that Section 5 tests.

### 4.1 The Bound-and-Gap framework

The Bound-and-Gap framework identifies, for any warehouse cell, whether the binding constraint on makespan reduction is elevator-side capacity or the feature representation Φ. It does so by partitioning the makespan improvement attainable from knowing a wave’s Φ-coordinates into two non-negative components: a ceiling Hup that no Φ-policy can reach, and a slack MΦ that a better Φ-policy can capture; their relative magnitudes determine which lever is dominant. Section 4.1.1 formalizes the partition as GAP=Hup+MΦ (Proposition 1). Section 4.1.2 establishes that M_Φ coincides with the Smart-Predict-then-Optimize regret of a partition-constant predictor (Theorem 1), placing the framework within the prediction-to-decision regret literature. Section 4.1.3 turns the pair (Hup, MΦ) into a four-quadrant diagnostic table.

4.1.1 Decomposing the value of wave-structure information

This subsection introduces the four corners on which the decomposition operates, defines the gap between an oracle benchmark and a Φ-informed policy on those corners, and decomposes that gap into two non-negative components with distinct operational meanings.

Consider a fixed (regime, model, size) cell. Φ-space is partitioned by a finite scheme Q; the working instance throughout the paper is the 2×2 quartile partition of the (C, I) plane into four corners Q={HC∙HI, HC∙LI, LC∙HI, LC∙LI}. For each corner q∈Q, let mq denote the corner-conditional median makespan of waves drawn from q, and m0 the median makespan of a wave drawn at random from the unpartitioned pool.

Three corners drive the decomposition. The first two are oracle corners: corners that would be chosen by a hypothetical decision-maker who already knew the per-corner median makespans (mq)q∈Q. Such an oracle would always release waves from the best corner qmin =argminqmq, and the worst corner qmax =argmaxqmq quantifies the spread the partition is capable of revealing. The third is the Φ-informed corner qΦ: the corner that a Φ-informed policy actually selects, from the sign pattern of an OLS fit on the cell. In words: qmin and qmax are what the partition reveals in principle (a benchmark only an oracle could attain); qΦ is what the partition reveals in practice (what a working Φ-policy achieves on real data).

These three corners define the framework’s three central quantities. The oracle upper bound UB measures the full spread the partition reveals to an oracle; the Φ-informed lower bound LB measures what a Φ-policy actually captures; and their difference is the gap between oracle and practice:

UB=mqmax-mqminm0, LB=m0-mqΦm0, GAP=UB-LB

Proposition 1 (Bound-and-Gap decomposition). For any cell and any finite partition Q,

GAP=Hup+MΦ, Hup=mqmax-m0m0, MΦ=mqΦ-mqminm0

Proof. Substituting the definitions,

UB-LB=mqmax-mqminm0-m0-mqΦm0=mqmax-m0m0+mqΦ-mqminm0=Hup+MΦ

Both components are non-negative by construction (mqmax≥m0 and mqΦ≥mqmin), so GAP≥0, with equality only when the partition is degenerate. The two components carry distinct operational meanings:

Hup (partition-intrinsic upper-tail headroom) is the relative makespan penalty of the worst corner against the unpartitioned baseline. It is present even when Φ selects perfectly, and no policy operating on Φ can reduce it (e.g., elevator-side capacity).

MΦ (Φ-policy miss) is the relative cost of Φ selecting qΦ rather than the oracle-best corner qmin. A better Φ-policy can, in principle, reduce it.

Section 5 reports the empirical magnitudes of both components on the grid.

4.1.2 The policy component is an SPO regret

The policy component MΦ admits a second reading that situates the Bound-and-Gap framework inside the prediction-to-decision regret literature. Treat which corner to release a wave from as a decision over Q; the true per-corner cost vector is c=(mq)q∈Q, and the oracle decision is

z*c=argminq∈Qmq

Following Elmachtoub & Grigas (2020), the Smart-Predict-then-Optimize (SPO) loss of any predictor c∈RQ against the true cost c is the realized-minus-oracle cost of the corner it induces:

lSPOc, c=cz*c-cz*c=mz*c-mqmin

4.4

A partition-constant predictor is a cost vector that is constant on each corner, the natural predictor class on a finite partition. The Φ-informed predictor, denoted cΦ​, is the partition-constant predictor whose induced decision is qΦ​.

Theorem 1 (SPO-regret equivalence). The policy component MΦ​ of the Bound-and-Gap decomposition equals the SPO regret of the Φ-induced partition-constant predictor, normalized by m0:

MΦ=mqΦ-mqminm0=lSPOcΦ, cm0

Proof sketch. The Φ-informed predictor induces the decision qΦ, and the oracle induces qmin by definition. Substituting into (4.4) gives lSPOcΦ, c=mqΦ-mqmin, and dividing by m0​ reproduces MΦ​ in (4.2). The equivalence is structural rather than asymptotic; it holds at every cell of the partition.

Theorem 1 positions the Bound-and-Gap framework as the partition perspective on SPO: the prediction-to-decision regret literature bounds an algorithm's loss at training time over a hypothesis class, where MΦ​ is a post-hoc information-value gap on a fixed partition. The cell-median is used throughout for consistency with this equivalence, which is stated for the median; the cell-mean version yields a parallel result. The contribution of the Bound-and-Gap framework is therefore not the SPO regret itself, which is a known object, but the decomposition that separates the SPO regret MΦ from an independent partition-intrinsic headroom Hup​.

4.1.3 Reading the decomposition

Because Hup and MΦ are non-negative and independently interpretable, their pair gives a structural reading of where a cell's wave-design value sits. Table 1 maps the four regions of (Hup, MΦ) to four operational interpretations.

Table 1. Reading the Bound-and-Gap decomposition

Hup

MΦ

Interpretation

Large

Small

Φ is already near-optimal; the residual is structural, and elevator-side capacity is the lever

Small

Large

Corners are flat and Φ is miscalibrated; feature engineering is the lever

Large

Large

The partition contrast is high and Φ misses it; feature expansion is the priority

Small

Small

The partition gives little leverage; wave design is not the lever here

The two components also respond differently to refinement of the partition.

Corollary 1 (refinement monotonicity). If a partition Q' refines Q, then Hup(Q')≥Hup(Q) — refinement of the partition can only raise the worst-corner median against the unpartitioned baseline. The policy component MΦ​ carries no such guarantee, because qΦ​ is itself a partition-dependent choice.

The two readings in Table 1 are of components, not of which operating regime a given dispatch policy will favor; Section 5 shows the realized value of structured wave-and-dispatch design to be broad across regimes rather than sharply regime-specific.

Fig. 1 The Bound-and-Gap decomposition on a stylized (regime, model, size) sub-cell. The four corner medians mqmin, mqΦ, m0, mqmax tile the oracle spread UB into three contiguous segments (MΦ, LB, Hup), along a relative make-span number line. Proposition 1 reads off the equality GAP=Hup+MΦ=UB-LB; both MΦ and Hup​ are non-negative by construction.

### 4.2 The Model-Dominance Hedge Rule

The Model-Dominance Hedge Rule delivers, under operator uncertainty over which member of the elevator-model family M={M1, M2, M3} governs the warehouse subsystem (Assumption A5), a closed-form wave-release decision that requires no online identification of M. We construct the rule in three steps. Section 4.2.1 sets up the decision problem the rule is meant to solve (the minimax wave-corner selection under elevator-model uncertainty) and identifies its load-bearing condition, per-wave chain dominance. Section 4.2.2 derives the rule itself: under chain dominance, the minimax collapses to a closed-form decision that simultaneously solves a Wasserstein-1 distributionally robust problem (Theorem 2), placing the rule within the distributionally robust optimization literature. Section 4.2.3 extends the rule’s validity to settings where chain dominance holds only approximately, via a one-sided worst-case bound (Corollary 2).

4.2.1 Model uncertainty and the minimax corner

The elevator model M∈M is exogenous to wave composition (Assumption A5), and the operator is not assumed to identify M online. The natural conservative response is the minimax wave-corner selection

c*=argminc∈QmaxM∈Ms[Cmax(W;M)|W∈c]

where s is any monotone summary statistic of the make-span distribution, which median, mean, or any quantile. Evaluated naively, c* requires the operator to compute s under every M∈M and select against the worst. The Hedge Rule removes that requirement by exploiting a structural relation among the models in M.

The load-bearing condition is chain dominance: for every wave W,

Cmax(W;M1)≤Cmax(W;M2), almost surely,

with M3​ the stochastic extension of M2 obtained by adding lognormal noise of scale σM3​​ to the timing primitives (3.7). In other words, throughput aggregation never overstates make-span relative to true co-occupancy batching, because aggregating per-AMR throughput absorbs the trip-time penalty that explicit co-occupancy charges per elevator trip. Chain dominance is an empirical claim about the model family M; Section 5 verifies it on matched waves at publication scale (99.2% average, 96.0% worst cell).

4.2.2 Collapse under chain dominance and its DRO equivalence

Theorem 2 (minimax collapse and Wasserstein-DRO equivalence). Under chain dominance (4.7), the minimax corner selection (4.6) collapses to the corner optimal for the dominant model,

c*=argminc∈Qs[Cmax(W;M2)|W∈c]

and this corner coincides with the solution of the Wasserstein-1 distributionally robust problem with ambiguity ball BρcM1={Q:W1)(M1, Q)≤ρc} of corner-calibrated radius ρc=W1(M1, M2|c), centred at the nominal model M1:

argminc∈Q
