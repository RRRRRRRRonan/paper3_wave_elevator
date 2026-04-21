# Paper 3: Novelty Analysis and Contribution Structure (v0.2)

**Status**: Working document v0.2 (replaces v0.1)
**Updated**: 2026-04-20
**Placement**: `F:\paper3_wave_elevator\novelty_analysis_and_contributions_v0_2.md`
**Changes from v0.1**:
- **Fixed critical citation error**: "Ramanathan et al. 2025" → "Chakravarty et al. 2025" throughout (the first author is Arjo Chakravarty; Elara is the 4th/advisory author)
- **Added §4 deep dive on Insights novelty** (new section)
- **Upgraded C2 framing** from "surrogate-based" to "structural exploitation" after reading Chakravarty 2025 + Wu 2024
- **Upgraded C3 to "on top of" framing** after reading Chakravarty's 1.25×-4.34× benchmark data
- **Added §7 counterfactual exercise**: "If experiment Y fails, how does the contribution degrade?"

---

## Table of Contents

1. [Framing: What This Document Is and Is Not](#1-framing-what-this-document-is-and-is-not)
2. [Identified Direct Competitors](#2-identified-direct-competitors)
3. [Three-Layer Novelty Structure](#3-three-layer-novelty-structure)
4. **[Deep Dive: Understanding Insight Novelty](#4-deep-dive-understanding-insight-novelty)** (NEW)
5. [Type A / Type B Contribution Classification](#5-type-a--type-b-contribution-classification)
6. [Science-Grade Novelty Claim Templates](#6-science-grade-novelty-claim-templates)
7. [Defensive Q&A Preparation](#7-defensive-qa-preparation)
8. [Counterfactual Stress Test](#8-counterfactual-stress-test) (NEW)
9. [Next Steps](#9-next-steps)

---

## 1. Framing: What This Document Is and Is Not

### What it IS
- An internal working document to clarify Paper 3 positioning
- A tool for preparing advisor meetings and proposal writing
- A foundation for Paper 3 Introduction section

### What it is NOT
- **Not a replacement for Paper 3 Introduction**: The Contributions paragraph from this document goes into the paper; the layered analysis in §3–4 does NOT.
- **Not a "novelty" section in the paper**: Most top OR journals (EJOR, M&SOM, TRE) do not have a separate "Novelty" section. Novelty is embedded in the Contributions paragraph through comparative language.

### The Key Principle

> **Novelty is an *attribute*; Contributions are *statements*.**
>
> Novelty answers "is it new?" → Contributions answer "what did we do?"
>
> A Contribution *carries* novelty through how it is phrased—typically via gap-filling ("no prior work..."), distinction ("unlike X..."), or structural claim ("the formulation introduces...").

**In the paper, write only ONE Contributions paragraph. Do not write a separate Novelty paragraph.**

---

## 2. Identified Direct Competitors

Based on literature searches and full-text readings conducted 2026-04-20:

### 2.1 Lenoble, Frein & Hammami (2018), EJOR
**Title**: *Order batching in an automated warehouse with several vertical lift modules*

**Key overlap**: keyword "order batching" + "vertical"; MILP + metaheuristic methodology; total completion time objective

**Key distinctions from Paper 3**:
- Their "vertical" = tray motion inside a single VLM mechanical device
- Our "vertical" = inter-floor material flow in a multi-storey building
- Their agent = one stationary picker + 1-4 independent VLMs
- Our agent = 20-50 flexible AMRs + 2-3 shared elevators
- Their decision = single-stage offline batching
- Our decision = two-stage tactical wave + operational fleet

### 2.2 Chakravarty, Grey, Muthugala & Elara (2025), MDPI Mathematics
**Title**: *Toward Optimal Multi-Agent Robot and Lift Schedules via Boolean Satisfiability*

**IMPORTANT CITATION NOTE**: First author is **Chakravarty** (Arjo Chakravarty, Intrinsic/SUTD). Previous drafts mistakenly called this "Ramanathan et al." — this was my error and has been corrected throughout.

**Key overlap**: multi-robot + multi-lift scheduling; makespan minimization; "lift as bottleneck" motivation

**Key distinctions from Paper 3**:
- They: operational-level robot-to-lift assignment with pre-given tasks
- We: tactical-level wave composition + release decisions, generating the task set
- They: exact SAT/CP with optimality but capped at ~35 agents
- We: surrogate-based heuristic targeting hundreds of orders
- They: single snapshot optimization
- We: shift-level rolling horizon with explicit release timing

**Critical benchmark data from their paper** (anchoring for our H1):
- Hotel-4-3 (2 lifts, 4 robots): 3.33× speedup
- Hotel-5-4 (2 lifts, 5 robots): 4.34× speedup (maximum)
- Hotel-7-1 (2 lifts, 7 robots): 1.96×
- Hospital-7-1 (4 lifts, 7 robots): 2.30×
- Hospital-7-4: 1.00× (no improvement possible)

Their results set the reference for **operational-level gains**. Our H1 claim is about **marginal gains on top of this**.

### 2.3 Wu, Zhang, Li, Zhang, Zhao, Zhang & He (2024), MDPI Processes
**Title**: *Research on Inbound Jobs' Scheduling in Four-Way-Shuttle-Based Storage System*

**Key overlap**: multi-layer vertical warehouse + elevators; makespan objective; NP-hard scheduling framing; FFSP formulation

**Key distinctions from Paper 3**:
- Their transport agent = tier-captive shuttles (confined to a specific layer)
- Our transport agent = fleet-flexible AMRs (traversing the entire warehouse)
- Their task set = exogenous inbound jobs
- Our task set = endogenous, shaped by wave composition decisions
- Their architecture = single-stage FFSP
- Our architecture = two-stage (tactical + operational)

**Critical benchmark data** (for our scaling comparison):
- Their DELO-GA solves 100 jobs in ~92 seconds with makespan 1013.83s, solution error 0.88%
- This sets a reference for metaheuristic scalability at industrial scale

### 2.4 Adjacent Works (Less Direct)

- **2024-2025 RMFS / G2P joint optimization works**: All in planar (single-layer) settings. Do not address multi-storey constraints.
- **ASRS / VLM queueing literature**: Performance analysis of fixed infrastructure, no decision variable for wave composition.

---

## 3. Three-Layer Novelty Structure

Paper 3's novelty is strongest when all three layers hold simultaneously. The nature of each layer is different — **understanding these differences is essential** (see §4).

### 3.1 Problem Novelty — **STRONG**

**Defensible claim**:
> "To our knowledge, this paper is the first to treat **wave composition** as a decision variable in a **multi-storey AMR warehouse** setting with **flexible mobile robot fleets**, explicitly coupling upstream wave-release decisions with downstream fleet-elevator execution."

**Each qualifier is necessary** — removing any one makes the claim vulnerable:
- "wave composition" → differentiates from Chakravarty et al. (task-given)
- "multi-storey" → differentiates from planar RMFS/Kiva literature
- "flexible mobile robot fleets" → differentiates from Wu et al. (tier-captive shuttles) and Lenoble et al. (single picker)
- "coupling upstream with downstream" → differentiates from operational-only works

### 3.2 Methodology Novelty — **MEDIUM-STRONG** (Upgraded from v0.1)

Three components:

**(M1) Two-stage decision architecture**
- *Type A (claimable pre-experiment)*
- First to formalize the coupling between wave-level and fleet-level decisions
- Contrast: Lenoble 2018 (single-stage MILP), Chakravarty 2025 (single-stage CP/SAT), Wu 2024 (single-stage FFSP)

**(M2) Three-dimensional structured feature decomposition** ← KEY NOVELTY
- *Type A (claimable pre-experiment)*
- Vertical concentration $C$, directional imbalance $I$, temporal clustering $T$
- **The novelty here is NOT "we use a surrogate"** (surrogates are standard). **The novelty is "we exploit the physical structure of vertical resource demand to get a low-dimensional, interpretable surrogate."**
- Contrast: exact methods (Chakravarty 2025) don't need surrogates but don't scale; black-box ML surrogates scale but lack interpretability; our structured surrogate is a third path.

**(M3) Empirical performance of the surrogate**
- *Type B (requires experiments)*
- Claim: $\Phi$ outperforms ML baselines on ≥2 of 3 metrics (sample efficiency / extrapolation / interpretability)

### 3.3 Insight Novelty — **UNCERTAIN UNTIL EXPERIMENTS**

See §4 for full analysis. Three candidate insights (in order of achievability):

- **H1 (marginal value of tactical layer)** — high achievability, anchored by Chakravarty's 1.25-4.34× data
- **H2 (regime-dependence)** — medium-high achievability
- **H3 (counterintuitive optimal compositions)** — uncertain, bonus

---

## 4. Deep Dive: Understanding Insight Novelty (NEW)

This section exists because Insight novelty is the **most subtle and most important** of the three layers—and also the most commonly misunderstood.

### 4.1 The Essential Distinction

```
Problem novelty     = "I identified a new research object"
Methodology novelty = "I developed a new solution tool"
Insight novelty     = "I revealed a new piece of knowledge"
```

**Problem and Methodology novelty can be claimed pre-experiment.**
**Insight novelty MUST come from experimental results.**

### 4.2 Why Insights Matter Most in Top OR Journals

- **Technical papers** (Methodology-heavy) → published in AIES, Algorithmica, technical venues
- **Applied OR papers** (Problem + Methodology) → published in Computers & OR, IJPR, mid-tier
- **Scientific papers** (all three, especially Insight) → published in EJOR, M&SOM, TS, top-tier

**Top-tier reviewers ask: "After reading this paper, what do I *know* that I didn't know before?"** That question is answered by Insights, not by Methodology.

### 4.3 Three Types of Insights

| Type | Structure | Paper 3 instance | Dialogue partner |
|---|---|---|---|
| **Phenomenological** | "We observed X" | H1: tactical wave gives marginal gain | Chakravarty 2025 (they quantified operational gain) |
| **Regime-based** | "X holds in regime Y" | H2: gain largest under high-imbalance × tight-capacity | All "wave planning is useful" general claims |
| **Counterintuitive** | "Common belief is X, but actually Y" | H3: optimal waves may not be balanced | Industrial intuition ("balance is best") |

Each insight should explicitly address **a dialogue partner**—a specific prior claim or belief that the insight extends, refines, or challenges.

### 4.4 What Makes an Insight "Good"

Five criteria:

**Criterion 1: It's a knowledge statement, not an experimental result**

- ✗ Bad: "Our method outperforms baseline by 15%"
- ✓ Good: "Vertical structure of wave composition is a first-order determinant of makespan in multi-storey AMR systems"

**Criterion 2: It survives out of context**

A good insight can be told to a stranger outside your subfield, and they can understand why it's interesting.

**Criterion 3: It has a "dialogue partner"**

Every insight must answer "compared to what?" or "contrary to whose belief?"

**Criterion 4: It's falsifiable**

If experiments had gone differently, the insight would not have been claimed.

**Criterion 5: It has operational consequences**

Someone reading the insight can take an action based on it (e.g., a warehouse manager, a system designer).

### 4.5 Worked Example: How Finding 1 Becomes an Insight

**Setup**: Suppose experiments yield this data:

| Baseline | Makespan (s) |
|---|---|
| FCFS (no optimization) | 300 |
| Operational-only (Chakravarty-style SAT) | 200 |
| My method (wave + operational) | 175 |

**Weak presentation (just experimental result)**:
> "Our method achieves 175s makespan, 12.5% better than operational-only baseline."

**Strong presentation (Insight)**:
> "Of the total 125s reduction from FCFS to our full method, **operational-level optimization contributes 100s (80%)**, while **tactical wave-composition contributes the additional 25s (20%)**. This decomposition quantifies, for the first time, the marginal value of introducing a tactical decision layer on top of well-optimized operational scheduling in multi-storey AMR warehouses. The 4:1 ratio suggests that while operational-level scheduling remains the dominant lever, tactical wave planning captures a non-trivial residual gain that becomes increasingly valuable as operational optimization approaches its ceiling."

**Note the differences**:
- Weak version answers "how good is our method?"
- Strong version answers "what is the value of decision-layer hierarchy?"
- The weak version is about **a technical artifact**
- The strong version is about **a scientific quantity**

### 4.6 Writing Insights: Hedging vs. Overclaiming

Good Insight writing requires **hedging without weakening**:

- ✗ Overclaiming: "We prove that wave planning is always beneficial" (can be falsified in one counterexample)
- ✗ Under-claiming: "Our results suggest some possible benefit in certain cases" (too weak to publish)
- ✓ Balanced: "Our computational study reveals that wave composition decisions yield non-trivial makespan reductions in operationally-optimized multi-storey AMR warehouses, with magnitude and distribution characterized in §6"

**Keyword patterns that work**:
- "Our computational study reveals..."
- "We find that..."
- "Experiments quantify..."
- "The results show that, under [conditions], ..."

**Keyword patterns to avoid**:
- "We prove that..." (unless you actually prove it)
- "Always" / "Never" / "In all cases"
- "Dramatically" / "Substantially" (let the numbers speak)

### 4.7 When the Experiments Go Wrong

Critical: **some Insights will not survive experiments**. Your plan should handle this:

- If H1 is confirmed → Paper 3 is strong
- If H1 fails (no marginal gain) → **still a valid insight**: "We find that operational-level optimization captures nearly all the gain in multi-storey AMR systems; tactical wave composition provides marginal benefit only in [specific conditions]." This is a **negative result that is still publishable**.
- If H3 fails (optimal waves *are* balanced) → remove from Paper 3, save space for H1/H2 depth

**The point**: you don't need all three insights to succeed. You need the experimental design to produce *some* clear finding.

### 4.8 The Insight Narrative Arc

The three insights in C3 should form a narrative:

1. **Finding 1** establishes that the tactical layer *matters* (existence)
2. **Finding 2** characterizes *when* it matters most (regime)
3. **Finding 3** reveals a *surprising structural property* (depth)

Reading Finding 1 → 2 → 3 takes the reader from "does this work?" to "when?" to "why is it surprising?" This arc is what distinguishes a scientific contribution from a mere experimental report.

---

## 5. Type A / Type B Contribution Classification

### 5.1 Type A Contributions (Claimable Pre-Experiment)

| Contribution | Paper section | What makes it defensible |
|---|---|---|
| New problem class definition | Intro §1.3 + Formulation §3 | Formal definition + contrast table |
| Two-stage decision architecture | Model §3 + Methodology §4 | Mathematical structure alone |
| Three-dimensional structured surrogate | Methodology §4.1 | Physical/queueing justification |
| "Vertical empty miles" KPI | Formulation §3.4 | Clear definition + motivation |

**These survive even if all experiments fail.**

### 5.2 Type B Contributions (Require Experiments)

| Contribution | Paper section | Experiment must show |
|---|---|---|
| Surrogate beats ML baselines | Experiments §5.2 | ≥2 of 3 metrics win |
| Vertical-aware gives makespan gain | Experiments §5.3 | Statistically significant improvement |
| Regime-specific gain boundaries | Experiments §5.4 | Clear boundary characterization |
| Counterintuitive optimal structures | Experiments §5.5 or Obs. | Observation + analysis |

**These require experimental validation.**

### 5.3 Fallback Risk Management

| Experimental outcome | Paper 3 strategy |
|---|---|
| All Type B fail | Reframe as concept paper: "problem + architecture + features" → mid-tier journal |
| Partial Type B succeed | Adjust title/scope → e.g., "A new surrogate for warehouse performance prediction" |
| All Type B succeed | Target top-tier: EJOR, TRE, M&SOM |

---

## 6. Science-Grade Novelty Claim Templates

### 6.1 Gap-Filling (Safest)

```
While prior work has addressed X and Y,
no existing work has combined Z.
This paper fills that gap.
```

**Paper 3 application**:
> "While prior work has studied order batching in VLM systems (Lenoble et al., 2018), multi-agent robot-lift scheduling with fixed tasks (Chakravarty et al., 2025), and scheduling in tier-captive shuttle systems (Wu et al., 2024), no existing work treats wave composition as a decision variable jointly with downstream fleet-elevator congestion in multi-storey AMR warehouses with flexible mobile robot fleets. This paper fills that gap."

### 6.2 Three-Dimensional Distinction (Most Explicit)

```
Our work differs from [cited work] in three dimensions:
(i) ..., (ii) ..., (iii) ...
```

**Paper 3 application to Chakravarty 2025**:
> "Our work differs from Chakravarty et al. (2025) in three dimensions:
> (i) decision scope: tactical wave composition vs. operational robot-lift assignment;
> (ii) solution architecture: scalable surrogate-based heuristic vs. exact SAT/CP capped at ~35 agents;
> (iii) temporal horizon: shift-level rolling horizon vs. single-snapshot optimization."

### 6.3 Complement-Not-Contradict (For Insights)

When your findings align with prior work (extending rather than opposing):

> "Our findings complement, rather than contradict, the managerial insights of [prior work]. Specifically, they extend [scope] from [narrow domain] to [broader domain]."

---

## 6.4 Final Contributions Paragraph (TO PASTE INTO PAPER 3 INTRODUCTION)

This is the **ONE paragraph** that goes into the paper. It fuses problem + methodology + insight novelty into three contributions:

---

> **Contributions of this paper.** We make three contributions:
>
> **(C1) Problem formulation.** We formalize the *wave release coordination problem under vertical resource constraints* in multi-storey warehouses with flexible AMR fleets—a two-stage scheduling problem jointly optimizing tactical wave composition and operational fleet execution subject to freight elevator capacity. This problem class has not been studied in the literature. While related problems have been addressed at the device level (order batching in VLM systems, Lenoble et al. 2018), at the operational level (multi-agent robot-lift scheduling with fixed tasks, Chakravarty et al. 2025), and in tier-captive shuttle systems (Wu et al. 2024), none consider wave composition as a decision variable with building-level vertical resource coupling and flexible fleet routing.
>
> **(C2) Methodology.** We propose a three-dimensional structured surrogate model $\Phi$ that decomposes wave composition into vertical concentration, directional imbalance, and temporal clustering. Unlike exact SAT/CP approaches (Chakravarty et al. 2025) that guarantee optimality but scale only to tens of agents, and unlike black-box metaheuristics (e.g., DELO-GA, Wu et al. 2024) that scale but lack interpretability, our structured surrogate exploits **physical properties of the vertical resource** to offer a third path: scalable, interpretable, and optimization-ready.
>
> **(C3) Insights.** Computational experiments reveal three findings. First, tactical wave-composition decisions yield makespan improvements **on top of** operational lift optimization of the kind studied by Chakravarty et al. (2025), quantifying the marginal value of multi-layer decision hierarchy. Second, these marginal gains are regime-dependent, with largest benefits in high directional-imbalance × tight-capacity scenarios. Third, optimal wave compositions exhibit structural properties that extend, rather than contradict, the managerial insights of single-device batching (Lenoble et al. 2018) to the building level.

---

**Guidance for using this paragraph**:
- This is ~220 words. Top OR journal Contributions paragraphs are typically 150-300 words.
- Keep the three-part structure (C1/C2/C3).
- Adjust specific numbers only after experiments (e.g., "15-30%" appears nowhere yet — save it for §6 of the paper).
- Cite all three competitors (Lenoble, Chakravarty, Wu) in this paragraph. This is reviewer-proofing.

---

## 7. Defensive Q&A Preparation

Most likely reviewer challenges and their answers:

### Q1: "Isn't this just Lenoble 2018 extended to multiple floors?"

**A**: No. Lenoble 2018's "vertical" refers to mechanical tray motion inside a single VLM device, served by one stationary picker. Our "vertical" refers to inter-floor material flow in a multi-storey building served by a flexible AMR fleet. The equivalence theorems that underpin Lenoble's MILP reduction (completion time ≡ tray visit count) **do not hold** in our setting due to multi-agent concurrency and elevator capacity constraints.

### Q2: "Chakravarty 2025 already solves multi-robot lift scheduling optimally. What's your contribution?"

**A**: Chakravarty's exact method scales only to ~35 agents. Our industrial setting involves hundreds of orders and dozens of AMRs, beyond their tractability. More fundamentally, they treat the task set as exogenous—our problem asks the *prior* question: how should wave composition be decided in the first place? The tactical decisions we make *generate* the task sets their method could optimally schedule.

### Q3: "Why not just simulate everything and use RL?"

**A**: End-to-end RL cannot provide interpretable decision rules or structural insight. Our structured surrogate method delivers both a practical algorithm *and* an interpretable understanding of what drives performance—critical for industrial deployment and managerial decision-making. Furthermore, RL faces known challenges in cross-instance generalization and sample efficiency.

### Q4: "Why exactly these three dimensions (concentration, imbalance, clustering)?"

**A**: The choice stems from a queueing-theoretic analysis of elevator throughput. An elevator, as a batch-service direction-reversible resource, has effective throughput determined by three orthogonal factors: the concentration of demand across floors (affecting queue length), directional distribution (affecting direction-switching cost), and temporal distribution (affecting concurrent contention). We formalize this derivation in §4.2.

### Q5: "Real warehouses are stochastic; why deterministic?"

**A**: The v1 deterministic modeling is a *deliberate scope choice*. Stochastic extension is future work (discussed in §7). Our deterministic results serve as an **upper bound reference**; practical robust/online extensions do not change the problem's structural novelty.

### Q6: "Is your 15-30% improvement just operational optimization that Chakravarty already captures?"

**A**: No, our experiments explicitly distinguish baselines:
- Baseline 1: FCFS (no optimization) — lower bound
- Baseline 2: Operational-optimal (simulates Chakravarty-style SAT)
- Our method: Tactical + operational
The reported X% is **marginal gain over Baseline 2**, not over Baseline 1. This isolates the tactical-layer contribution.

---

## 8. Counterfactual Stress Test (NEW)

This section asks: **"If specific experimental results fail, how much of Paper 3 survives?"**

### Scenario A: Surrogate model $\Phi$ has poor predictive accuracy

- **Impact**: C2 (methodology) is weakened — the structured surrogate is just a concept, not a validated tool.
- **Survives**: C1 (problem formulation), two-stage architecture concept
- **Rescue strategy**: Replace $\Phi$ with a higher-dimensional learned model, but keep the three-dimensional decomposition as a *conceptual tool for understanding* rather than a *prediction tool*.
- **Paper outcome**: Still publishable in mid-tier (C1 + rearranged C2 + C3), not top-tier

### Scenario B: H1 fails — no marginal gain on top of operational optimization

- **Impact**: C3's Finding 1 inverts: "operational optimization captures nearly all gain, tactical layer contributes minimal"
- **Survives**: C1, C2 (as tools), C3's Findings 2-3 (if they hold)
- **Rescue strategy**: Reframe C3 as "When tactical wave planning matters, and when operational optimization suffices" — this is *itself* a valuable managerial insight.
- **Paper outcome**: Publishable in applied OR journals (IJPR, CIE) with reframed contribution

### Scenario C: H2 fails — gains are uniform across regimes

- **Impact**: C3's Finding 2 removed
- **Survives**: Everything else
- **Rescue strategy**: Focus on Findings 1 and 3 more deeply
- **Paper outcome**: Minimal impact

### Scenario D: H3 fails — optimal waves ARE balanced (no counterintuitive finding)

- **Impact**: C3's Finding 3 removed
- **Survives**: Everything else
- **Rescue strategy**: Replace with "our results confirm the managerial wisdom of balanced waves, but quantify the magnitude of the penalty for non-balance"
- **Paper outcome**: Minimal impact — negative result on H3 is itself a clean managerial message

### Scenario E: All Type B experiments fail

- **Impact**: Paper 3 becomes a "concept paper"
- **Survives**: C1 (problem novelty), M1 (two-stage architecture as concept), M2 (three-dimensional features as analytical framework)
- **Rescue strategy**: Retarget to "position paper" or "framework paper" venue
- **Paper outcome**: Still publishable, but as a shorter, more conceptual piece

### Key Takeaway

**Paper 3 is risk-managed**: even the worst-case experimental outcome (Scenario E) still yields a publishable paper, because the Type A contributions (problem + architecture + features) carry independent value. This is a sign that the research design is sound.

---

## 9. Next Steps

### 9.1 This Week (Week 2)

- [x] Read Chakravarty et al. 2025 (reading log complete)
- [x] Read Wu et al. 2024 (reading log complete)
- [x] Read Lenoble et al. 2018 (reading log complete)
- [ ] Correct "Ramanathan" → "Chakravarty" in all workspace files
- [ ] Begin MVS prototype (see `prototype/MVS_prototype_plan.md`)

### 9.2 Week 3-4

- [ ] Run MVS, produce R² analysis
- [ ] Based on MVS results, decide if three-dimensional feature decomposition is empirically supported
- [ ] Write 2-page "Why These Three Dimensions?" justification (for §4.2 of Paper 3)

### 9.3 Before First Advisor Meeting

- [ ] Final version of this document (v1.0) frozen
- [ ] Final Contributions paragraph polished
- [ ] Three reading logs complete
- [ ] MVS preliminary results ready

### 9.4 Before Paper 3 Draft Begins

- [ ] v0.2 problem formulation (non-draft) finalized
- [ ] MVS v0.2 complete (multi-elevator, stochastic)
- [ ] Baseline algorithm implementation complete (FCFS + operational-optimal)

---

## 10. Document Maintenance

- **v0.1 (2026-04-20 morning)**: Initial draft
- **v0.2 (2026-04-20 afternoon)**: Fixed Chakravarty citation; added §4 (Insight deep dive); added §8 (counterfactual); upgraded C2 framing
- **v0.3 (pending)**: After MVS results
- **v1.0 (pending)**: Frozen before Paper 3 drafting

---

**End of novelty_analysis_and_contributions v0.2**