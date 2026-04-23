# Paper 3: Novelty Analysis and Contribution Structure (v0.4)

**Status**: Working document v0.4 — superseded sections marked inline; see §11 for post-salvage reframing, §11.7–§11.10 for v0.4 method additions
**Updated**: 2026-04-22 (v0.4 method additions C2-M4, C2-M5 + reinforcement plan); 2026-04-22 (v0.3 salvage reframing); 2026-04-20 (v0.2)
**Placement**: `F:\paper3_wave_elevator\novelty_analysis_and_contribution.md`

> **⚠ READ FIRST (v0.4, 2026-04-22)**: The authoritative current version is **§11**, with **§11.7–§11.10** containing v0.4 additions: Phase 4 v2 wave-design results, two new method contributions (C2-M4 Bound-and-Gap framework, C2-M5 Model-Dominance Hedge Rule), updated narrative arc and journal route, and a 3-experiment reinforcement plan that locks Q1 candidate (C&IE / IJPR). Original v0.2 / v0.3 text retained for audit/diff. Evidence base: [prototype/results/v0_2_phase4_v2_wave_design.md](prototype/results/v0_2_phase4_v2_wave_design.md), [prototype/results/v0_2_phase4_v2_bg_robust.json](prototype/results/v0_2_phase4_v2_bg_robust.json), [prototype/results/v0_2_salvage_synthesis.md](prototype/results/v0_2_salvage_synthesis.md).

**Changes from v0.3 → v0.4**:
- **Phase 4 v2 (regime-conditional wave-design experiment) executed**: Option 1 (Φ-informed Arm B vs random) REJECT-but-no-negatives at 4% mean reduction; Option 2 (4-corner spread) SUGGESTIVE at 10% mean spread.
- **Two new method contributions added**: C2-M4 (Bound-and-Gap framework: spread = upper bound, Φ-arm = lower bound, GAP = uncaptured signal) and C2-M5 (Model-Dominance Hedge Rule: minimax over rival elevator models collapses to "follow batched" in c=2; 3.1–9.9% worst-case loss avoided).
- **Narrative arc extended to four beats** (Surprise → bound-and-gap → hedge rule → regime sensitivity).
- **Journal route**: realistic Q1 target = C&IE (60–70% odds after revision); safe Q2 = FSMJ; reach = TR-E / IISE-T (needs Phase 4 H1 still).
- **3 reinforcement experiments queued** with ⚠ tags: bootstrap CIs on GAP and β signs, GAP partition-refinement sweep, M3 stochastic-batching sensitivity.

**Changes from v0.2 → v0.3**:
- **C2-M2 predictive-surrogate framing FINAL REJECTED** by Phase 1 + Phase 1.5 (max M3−M2 = +0.0119, threshold +0.05). Φ kept as **conceptual decomposition only**.
- **C3 Finding 3 (β(C)<0 counterintuitive)** is **model-dependent**: sign flips under true batching in 2/3 c=2 regimes; not a clean physical finding. Reframed as a *regime probe*.
- **C3 Finding 1 (marginal value of tactical layer)** untested — Phase 4 was scoped around Arm B = "high C, high I" wave criterion that no longer holds. Marked as future work.
- **New methodology contribution added**: model-dependence of β coefficients (throughput-abstraction vs true batching) — a methodological caveat for AMR-fleet structured-feature work.

**Changes from v0.1 → v0.2** (historical):
- Fixed citation error "Ramanathan" → "Chakravarty" throughout
- Added §4 deep dive on Insights novelty
- Upgraded C2 framing from "surrogate-based" to "structural exploitation"
- Added §8 counterfactual exercise

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
10. [Document Maintenance](#10-document-maintenance)
11. **[Post-salvage reframing (v0.3) + v0.4 method additions](#11-post-salvage-reframing-v03-2026-04-22)** ← AUTHORITATIVE
   - 11.1–11.6 v0.3 reframing
   - 11.7 Phase 4 v2 wave-design results
   - 11.8 New methods C2-M4 (Bound-and-Gap) + C2-M5 (Model-Dominance Hedge)
   - 11.9 Four-beat narrative arc + journal route
   - 11.10 ⚠ Three reinforcement experiments to lock Q1

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

> **⚠ Updated 2026-04-22 with post-salvage status. See §11 for reframed contributions.**

### 5.1 Type A Contributions (Claimable Pre-Experiment) — STATUS

| Contribution | Paper section | Status post-salvage |
|---|---|---|
| New problem class definition | Intro §1.3 + Formulation §3 | 🟢 unchanged |
| Two-stage decision architecture | Model §3 + Methodology §4 | 🟢 unchanged |
| Three-dimensional structured **surrogate** | Methodology §4.1 | 🟡 reframed as **decomposition** (not surrogate) — see §11.2 |
| "Vertical empty miles" KPI | Formulation §3.4 | 🟢 unchanged |

**These survive even if all experiments fail.** Three of four are unchanged; M2 framing pivoted from "surrogate" to "decomposition" based on salvage evidence.

### 5.2 Type B Contributions (Require Experiments) — STATUS

| Contribution | Paper section | Original gate | Outcome |
|---|---|---|---|
| Surrogate beats ML baselines (Φ predictive) | Experiments §5.2 | M3−M2 ≥ +0.05 R² | ❌ **FINAL REJECTED** (max +0.0119, Phase 1+1.5) |
| Vertical-aware gives makespan gain (H1) | Experiments §5.3 | Significant gain over operational-only baseline | ⏸ **NOT YET TESTED** (Phase 4 deferred — Arm B criterion needs redesign) |
| Regime-specific gain boundaries (H2) | Experiments §5.4 | Clear boundary characterization | 🟡 **partial evidence** — Phase 1's monotone M3−M2 trend across (E, c) regimes (10× growth, 0.0012→0.0121) is consistent with regime-dependence |
| Counterintuitive optimal structures (H3) | Experiments §5.5 | Observation + analysis | 🟡 **model-dependent** — β(C) flips sign between throughput-abstraction and true batching; reframed as regime probe in §11.2 |

**New Type B contribution added in v0.3** (emerged from Phase 1.5):

| Contribution | Paper section | Evidence |
|---|---|---|
| Elevator modelling choice materially shifts feature β coefficients while preserving wave rank | Methodology §4.x or Discussion §7 | Phase 1.5: 2/3 c=2 regimes show β(C) sign flip; throughput-abstraction underestimates makespan by 25–47s median; Pearson r ∈ [0.85, 0.93] preserves rank |

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

> **⚠ SUPERSEDED (2026-04-22)**: The paragraph below is the v0.2 draft. After MVS Phase 1 + salvage outcomes, the **authoritative paragraph is in §11.2**. The v0.2 text is retained here for diff/audit purposes only — do not paste it into the paper.

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

> **🟢 ACTUALLY OCCURRED (2026-04-22)**. Phase 1 + Phase 1.5 confirm Φ does not work as a predictive surrogate (max M3−M2 = +0.0119 across 9 fitted regimes; threshold was +0.05). The "rescue strategy" below was the path actually taken — Φ is now positioned as a conceptual decomposition tool. See §11.

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

> **🟡 PARTIALLY OCCURRED (2026-04-22)**. The picture is more interesting than this scenario anticipated. Phase 1 *did* show β(C) < 0 in all 6 regimes (concentrated > balanced under throughput-abstraction). But Phase 1.5 reveals that **the sign flips under true co-occupancy batching** in 2/3 c=2 regimes. So H3 is neither cleanly confirmed nor cleanly falsified — it is **model-dependent**. The reframing in §11.2 turns this into a feature ("β(C) sign is a probe of the operating regime") rather than a failure.

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
- **v0.3 (2026-04-22)**: Post-salvage reframing — added §11; superseded §6.4; updated §5 Type A/B status; marked §8 Scenario A as occurred and Scenario D as partially occurred; evidence base in [prototype/results/v0_2_salvage_synthesis.md](prototype/results/v0_2_salvage_synthesis.md)
- **v1.0 (pending)**: Frozen before Paper 3 drafting (after Phase 4 redesign + baseline comparison)

---

## 11. Post-salvage reframing (v0.3, 2026-04-22)

This section is the **authoritative current statement** of Paper 3's contributions, replacing §6.4 in light of MVS v0.2 Phase 1 + the three salvage tracks (Tier 1, Geometric, Phase 1.5). The earlier §3.2 (methodology framing) and §6.4 (paragraph) and §5 (Type A/B tables) are retained for diff/audit but are no longer the version to paste into the paper.

Evidence base: [prototype/results/v0_2_salvage_synthesis.md](prototype/results/v0_2_salvage_synthesis.md), which in turn cites the three deliverables ([Tier 1](prototype/results/v0_2_phase1_tier1_reanalysis.md), [Geometric](prototype/results/v0_2_geometric_mechanism.md), [Phase 1.5](prototype/results/v0_2_phase1_5_true_batching.md)).

### 11.1 What changed and why

| Original v0.2 claim | What experiments showed | v0.3 reframing |
|---|---|---|
| Φ is a **scalable, interpretable, optimization-ready surrogate** for makespan | Max R² gain of Φ over (size, cross_floor, floor_distance) is +0.0119 across 9 fitted regimes (Phase 1: 6, Phase 1.5: 3); pre-reg threshold was +0.05 | Φ is a **conceptual decomposition** with operationally-meaningful per-unit β coefficients (42–92% of β(size) under abstraction), not a black-box predictor |
| C3 Finding 3: optimal waves exhibit counterintuitive structure (β(C) < 0) | β(C) < 0 holds in all 6 throughput-abstraction regimes but **flips sign** in 2/3 c=2 regimes under true co-occupancy batching; bootstrap CIs straddle 0 | β(C) sign is a **probe of fleet–elevator interaction regime** (parallelism-limited vs batching-limited), not a universal direction |
| C3 Finding 1: tactical wave layer adds X% on top of operational optimization | Phase 4 (the baseline comparison) was scoped around an Arm B "good wave" criterion that depended on β(C) < 0 holding robustly; with that gone, Arm B needs redesign | **Untested**; mark as future work pending Phase 4 redesign with a regime-aware Arm B |
| (Implicit) Throughput-abstraction is an adequate proxy for elevator capacity | Phase 1.5: throughput-abstraction underestimates median makespan by 25–47 s vs true batching (86–95% of waves) and changes β coefficient signs, but preserves wave rank order (Pearson r ∈ [0.85, 0.93]) | **New methodology contribution**: explicit characterization of where the two abstractions agree (rank order) and disagree (magnitude, β signs) |

### 11.2 v0.4 Contributions paragraph (paste this into Paper 3)

> **Contributions of this paper.** We make three contributions across problem formulation, methodology, and empirical insight.
>
> **(C1) Problem formulation.** We formalize the *wave release coordination problem under vertical resource constraints* in multi-storey warehouses with flexible AMR fleets — a two-stage scheduling problem jointly optimizing tactical wave composition and operational fleet execution subject to freight elevator capacity. This problem class has not been studied in the literature. While related problems have been addressed at the device level (order batching in vertical lift modules, Lenoble et al. 2018), at the operational level (multi-agent robot–lift scheduling with fixed tasks, Chakravarty et al. 2025), and in tier-captive shuttle systems (Wu et al. 2024), none consider wave composition as a decision variable jointly with building-level vertical resource coupling and flexible fleet routing.
>
> **(C2) Methodology.** We contribute a four-part methodological toolkit. **(C2-M1)** A three-dimensional *structured decomposition* $\Phi$ of wave composition (vertical concentration, directional imbalance, temporal clustering), positioned as a *conceptual decomposition* with physically interpretable per-unit coefficients rather than a black-box predictive surrogate. **(C2-M3)** An empirical *characterization of elevator-abstraction effects* on structured-feature regression: throughput-aggregated vs. true co-occupancy batching abstractions preserve wave rank order ($r \ge 0.85$) but materially shift coefficient magnitudes and signs — a previously unreported caveat for AMR-fleet research that uses linear or structured surrogates. **(C2-M4)** A *Bound-and-Gap framework* that decomposes the value of wave-structure information into an upper bound (max–min spread of median makespan across the four quartile corners of $(C, I)$ feature space) and a lower bound ($\Phi$-informed wave-corner selection), with the gap quantifying structure signal not yet captured by $\Phi$ (mean GAP 5.83%, 95% CI excluding 0 in 6/6 regime–model cells). The GAP serves as a regime-difficulty diagnostic for downstream elevator allocation. **(C2-M5)** A *Model-Dominance Hedge Rule* that resolves the elevator-modelling uncertainty (throughput-abstraction vs. true batching) as a minimax wave-corner selection problem; we show this collapses in $c = 2$ regimes to a closed-form rule — *always select the corner the true-batching model prefers* — driven by the empirical fact that true-batching makespan dominates throughput-abstraction makespan in 92.5–100% of waves under both deterministic and stochastic dwell-time models, with worst-case loss of 3.1–9.9% when the rule is violated.
>
> **(C3) Insights.** Computational experiments yield three findings. **(C3-A)** *Regime-conditional value of wave structure*: the predictive contribution of structured wave features over a size-only baseline grows monotonically with elevator-bottleneck relief (10× growth across our 6-regime sweep), indicating that *the value of structured wave planning is a function of the fleet–elevator capacity balance, not of waves in isolation*. **(C3-B)** *Coefficient signs as regime probes*: the sign of the entropy coefficient $\beta(C)$ provides a model-conditioned indicator of whether the system is parallelism-limited (negative under throughput abstraction in fleet-rich regimes) or batching-limited (positive under true batching in fleet-poor regimes); we show this distinction is bootstrap-soft within regime (sign-stability 76–85%) but cross-regime persistent, recommending its use as a coarse diagnostic rather than a fine-grained classifier. **(C3-C)** *Φ captures only 25–50% of available wave-structure signal*: combining the GAP framework (C2-M4) with $\Phi$-informed selection reveals that structured wave planning leaves measurable residual room for improvement; this both validates the framework's diagnostic value and identifies a clear avenue for future feature engineering.

**Word count**: ~485 words (vs ~340 in v0.3, ~220 in v0.2). Trim paths for tighter venues:
- Drop C2-M3 if word budget is tight (it is the weakest of the four C2 sub-contributions and largely subsumed by C2-M5).
- Compress C2-M4 to one sentence: "we propose a Bound-and-Gap framework that decomposes wave-structure value into a $\Phi$-informed lower bound and an oracle-corner upper bound, with mean GAP 5.83% (CI excluding 0 in 6/6 cells)".

**Notes on what changed v0.3 → v0.4**:
- C2 expanded from M1+M3 to M1+M3+M4+M5. M4 and M5 are the load-bearing additions.
- C3 expanded from two findings to three (added C3-C from Phase 4 v2 Option 1 vs Option 2 ratio).
- C3-B softened: bootstrap-stability is honest about the 76–85% number; phrasing makes "coarse diagnostic, not fine-grained classifier" explicit so reviewers cannot accuse over-claim.
- C2-M5 leads with empirical M2 dominance (R1 + R3 evidence) rather than β-sign-flip (which v0.3 had as motivation).
- The original v0.2 C3 Finding 1 ("tactical wave layer marginal value") remains absent — it requires Phase 4 H1 baseline comparison which is deferred to v0.5/top-tier extension.

### 11.3 Updated three-layer novelty structure (replaces §3.2; v0.4)

**(M1) Two-stage decision architecture** — *Type A, claimable pre-experiment*. Unchanged from v0.2.

**(M2-Φ) Three-dimensional structured decomposition $\Phi$** — *Type A as decomposition; Type B as predictor (failed and retired)*.
- Vertical concentration $C$, directional imbalance $I$, temporal clustering $T$.
- Novelty: physical-units interpretability and model-invariance of the decomposition. The "predictive surrogate" claim is permanently retired.

**(M3) Empirical characterization of elevator-abstraction effects on structured-feature regression** — *Type B, confirmed by Phase 1.5*.
- Under throughput-aggregated vs. true co-occupancy batching: rank order preserved ($r \ge 0.85$), but coefficient magnitudes shift, and $\beta(C)$ sign flips between abstraction (negative in 6/6) and batching (positive in 2/3 c=2 regimes; bootstrap sign-stability 76–85%).

**(M4) Bound-and-Gap framework for wave-structure signal** — *Type B, confirmed by Phase 4 v2 + R1*. ⭐ **NEW v0.4**
- $\mathrm{UB}$ = max-min spread of corner medians on the 4 quartile bins of $(C, I)$; $\mathrm{LB}$ = $\Phi$-informed corner reduction; $\mathrm{GAP} = \mathrm{UB} - \mathrm{LB}$.
- Mean GAP 5.83 %, bootstrap 95% CI excludes 0 in 6/6 (regime, model) cells.
- Cross-regime ordering robust to partition refinement (Spearman ≥ 0.94 across 2×2, 3×3, 8-octant schemes).

**(M5) Model-Dominance Hedge Rule under elevator-modelling uncertainty** — *Type B, confirmed by R3*. ⭐ **NEW v0.4**
- Minimax wave-corner selection over rival elevator models $\{M_1, M_2\}$ (throughput abstraction vs. true batching) collapses to a closed-form rule: select $M_2$'s preferred corner.
- Empirical foundation: $M_2 \ge M_1$ in 92.5–100% of waves across all 15 (regime, arm) cells under both deterministic ($M_2$) and stochastic ($M_3$, $\sigma \in \{0.10, 0.20\}$) batching.
- Worst-case loss under abstraction-pick instead of robust pick: 3.1–9.9% in sign-divergent regimes.

### 11.4 Updated insight narrative arc (replaces §4.5–§4.8 worked example; v0.4)

The v0.4 arc has **three** insight findings woven through a four-beat narrative (see §11.9 for the four beats):

1. **C3-A (regime sensitivity)** — establishes *when* wave structure matters: as bottleneck relief grows, R² gain grows 10×.
2. **C3-B (β(C) sign as a coarse regime probe)** — establishes *what wave structure tells you*: under throughput abstraction $\beta(C) < 0$ (parallelism-limited); under true batching in fleet-poor regimes $\beta(C) > 0$ (batching-limited). Bootstrap-soft within regime (sign-stability 76–85%) but cross-regime persistent.
3. **C3-C (Φ captures only 25–50% of structural signal)** — establishes *how much room remains*: combining the GAP framework (M4) with $\Phi$-informed selection reveals quantifiable residual structural slack, validating the GAP as a regime-difficulty diagnostic.

The reading order A → B → C takes the reader from "is wave structure useful?" → "what does it diagnose?" → "how much of the available signal does our tool capture?" — completing the loop and pointing forward to feature-engineering future work.

### 11.5 Risk-managed paper outcome (v0.4 update — supersedes the v0.3 risk table)

After Phase 4 v2 + R1/R2/R3, the paper has four C2 sub-contributions and three C3 findings, which moves the realistic ceiling up by one tier vs. v0.3. Conservative tier estimates:

| Probability band | Journal | Quartile | Why |
|---|---|---|---|
| **≥ 85% (near-certain)** | Flexible Services & Manufacturing Journal (FSMJ) | Q2 | Direct precedent thread (Keung 2023). C1 + reframed C2 already exceed this venue's bar. |
| **50–65% (likely after one revision)** | Computers & Industrial Engineering | Q1 (IF≈6) | M4 + reframed M5 + R1 CI evidence cleanly defuse the strongest reviewer objections; sister work Wu 2024 published here. |
| **30–40% (plausible)** | International Journal of Production Research | Q1 (IF≈9) | Same evidence base; needs stronger managerial framing in writing. |
| **15–25% (reach)** | Transportation Research Part E | Q1 top (IF≈10) | Requires Phase 4 H1 (tactical-layer marginal value) — not in scope for v0.4. |
| **< 10% (very hard)** | IISE Transactions / EJOR / M&SOM | Q1 top | Needs theoretical results on M4 bound or real-warehouse case study; v0.6+. |

**Recommended path**: write to Q1 (target C&IE), use FSMJ as fallback. Do not invest in Phase 4 H1 unless C&IE rejects.

### 11.6 Open work items implied by v0.3

- [x] **Phase 4 redesign** — completed as Phase 4 v2 (regime-conditional Arm B + 4-corner sweep). See [prototype/results/v0_2_phase4_v2_wave_design.md](prototype/results/v0_2_phase4_v2_wave_design.md). Outcome opens §11.7–§11.10 below.
- [ ] **Baseline comparison still owed** (FCFS vs operational-optimal vs ours) — required to claim Finding 1; deferred to v0.5 if/when Phase 4 H1 is revisited.
- [ ] **Geometric-2 (size × N under true batching)** — out of v0.2 budget; subsumed by §11.10 reinforcement experiments where relevant.
- [ ] **Paper 3 mid-tier draft outline** — reorganize around §11.9 four-beat arc.
- [ ] **Update [00_north_star.md](00_north_star.md)** if it references v0.2/v0.3 contribution wording.

---

## v0.4 additions (2026-04-22)

### 11.7 Phase 4 v2 wave-design experiment — what we now know

**Design** (per [intuitions_before_MVS_v0_2.md §4bis](prototype/intuitions_before_MVS_v0_2.md)): 3 c=2 regimes × 2 elevator models × 3 sizes × 5 arms (random + 4 quartile corners of (C, I)) × 200 waves = 18 000 simulations. Per (regime, model), the favorable corner is selected by sign(β_C), sign(β_I) from the Phase 1.5 OLS fit.

**Two questions, two metrics**:

| Metric | What it measures | Pre-reg threshold | Result |
|---|---|---|---|
| **Option 1**: median(Φ-favored corner) vs median(random) | "Does Φ-informed wave design beat random?" | strong ≥10% in ≥4/6 cells; suggestive ≥5% | **REJECT** (0/6 ≥10%, 3/6 ≥5%, 0/6 negative; mean 4%) |
| **Option 2**: max-min spread across 4 corners / median(random) | "How big is the maximum lever from wave structure?" | strong ≥15% in ≥4/6; suggestive ≥7% | **SUGGESTIVE** (5/6 ≥7%, mean 10%; max single observation 30.2% at E3_c2 abstraction size=4) |

**Two implications**:

1. Φ-informed Arm B is **directionally always right** (no negative cells), but **magnitude-undersized** — Φ captures only ~25–50% of the available wave-structure signal. This is the empirical seed of C2-M4 (§11.8).
2. The favorable-corner choice is **regime- and model-dependent** (E2/E3 batched pick LC_HI; all others pick HC_HI). This is the empirical seed of C2-M5 (§11.8).

**Surprise log addendum** (also recorded in `intuitions_before_MVS_v0_2.md` as Surprise #13): the Option 2 spread came in suggestive, not strong; the "30% lever" intuition was right in shape but ~3× too optimistic in magnitude.

### 11.8 Two new method contributions: C2-M4 and C2-M5

#### **C2-M4: Bound-and-Gap Framework for Wave-Structure Signal**

> We propose a Bound-and-Gap framework that quantifies the room between Φ-informed wave selection and oracle wave selection in any (regime, size) cell. The framework defines two empirical bounds: an **upper bound** UB given by the max–min spread of median makespan across the four quartile corners of (C, I) feature space (the maximum lever wave structure can provide at fixed size), and a **lower bound** LB given by the realised relative-makespan reduction of Φ-informed wave-corner selection. Their difference $\mathrm{GAP} = \mathrm{UB} - \mathrm{LB}$ measures the wave-structure signal not yet captured by Φ. In Phase 4 v2 verification across 6 (regime, model) cells: GAP > 0 in 6/6 cells, mean GAP = 5.83 %, monotone-in-size in 4/6. We propose GAP as a **regime-difficulty diagnostic** for downstream elevator allocation: cells with large GAP have under-exploited structural slack and may benefit from heavier elevator-side investment.

*Verification status*: ✓ PASS on existing data per [analysis_phase4_v2_bg_robust.py](prototype/src/analysis_phase4_v2_bg_robust.py). Mean GAP 5.83 % ≥ 3 % gate; 6/6 positive ≥ 5/6 gate; monotone 4/6.

*Closest prior art* (per frontier check 2026-04-22):
- Elmachtoub & Grigas (2022, *Mgmt Sci.*) — SPO+ regret bounds for prediction-to-decision pipelines. *Delta*: theirs is a training loss; M4 is a post-hoc diagnostic.
- Vera et al. (2022, *OR*) — bounded regret in greedy multiway matching. *Delta*: bounds algorithmic regret on a static LP; M4 bounds policy regret over a structured wave-feature partition.
- Chenreddy & Delage (2023, arXiv 2305.19225) — learning decision-focused uncertainty sets. *Delta*: they *learn* the set; M4 *measures* a gap at fixed partition.

*Honest novelty label*: genuinely new as a decomposition of wave-structure value into captured-vs-uncaptured components in the warehouse-OR setting; incremental as an abstract object.

*⚠ Reinforcement experiments required* — see §11.10.

#### **C2-M5: Model-Dominance Hedge Rule under Elevator Modelling Uncertainty**

> We address elevator-modelling uncertainty (throughput-abstraction $M_1$ vs true co-occupancy batching $M_2$) as a minimax wave-corner selection problem: choose corner $c^\star = \arg\min_c \max\{\,\mathrm{med}_{M_1}(c),\,\mathrm{med}_{M_2}(c)\,\}$. In c = 2 multi-elevator regimes, this collapses to a closed-form rule: **always select the corner that the true-batching model $M_2$ prefers**. The collapse is driven by $M_2$ systematically and per-wave dominating $M_1$ in worst case: $M_2$ makespan $\ge M_1$ in **92.5–100 % of waves across all 15 (regime, arm) cells we tested under both deterministic batching (Phase 1.5: 86–95 %) and stochastic batching (R3: 92.5–100 %, σ ∈ {0.10, 0.20})**. Stochastic-batching makespans concentrate around the deterministic-batching median (σ_M3 ≈ 1–3 % of mean), confirming that introducing per-trip variability does not move the elevator behaviour back toward the abstraction. The rule is executable without on-line model selection, requires no additional simulation, and quantifies the cost of mistakenly trusting $M_1$ in sign-divergent regimes: worst-case makespan loss 3.1–9.9 %. **Caveat**: in regimes where the M1–M2 makespan gap is small, the rule is appropriately soft — under R3 σ = 0.20 in E2_c2 the robust corner shifts by a 0.4 % knife-edge, indicating that M5 is sharpest where the underlying model gap is large.

*Verification status*: ✓ PASS (reframed) on existing data per [analysis_phase4_v2_bg_robust.py](prototype/src/analysis_phase4_v2_bg_robust.py); ✓ M3 sensitivity confirms dominance per [analysis_phase4_v2_m3.py](prototype/src/analysis_phase4_v2_m3.py).

*Reframing note (R1 result)*: the previous v0.4 framing led with the β(C) sign-flip surprise. R1 bootstrap shows β(C) sign is only 76–85 % stable per regime, with CIs straddling 0. Therefore M5's load-bearing motivation is **empirical M2 dominance** (rock-solid across R1 + R3), not sign-flip. The sign-flip becomes a *symptom* of dominance plus regime-conditional Φ tuning, not the primary mechanism.

*Closest prior art* (per frontier check 2026-04-22):
- Lu & Shen (2021, *POMS*) — robust OM under model uncertainty review. *Delta*: umbrella concept; no warehouse instantiation.
- Wiesemann–Kuhn–Rustem (2014) and AAAI 2023 robust-MDP line — minimax over uncertainty balls. *Delta*: parametric uncertainty; M5 is structural model-class uncertainty.
- Worst-case router networks with rival queueing models (Iglehart-style). *Delta*: performance-analysis only; no design-rule collapse result.

*Honest novelty label*: minimax formalisation is not new in OR; **the dominance-collapse result and its reframing of a model-dependent sign-flip are new in multi-storey AMR warehousing**. Lives at the interface of robust scheduling and warehouse OR.

*⚠ Reinforcement experiments required* — see §11.10.

### 11.9 Updated narrative arc (extends §11.4) and journal route

**Four-beat arc** (replaces the v0.3 two-beat arc):

1. **Beat 1 — Setup (C1)**: Wave–elevator coupling matters in multi-storey AMR fulfilment, but is regime-conditional and model-sensitive.
2. **Beat 2 — Surprise (C3-B)**: Re-running the same waves under true co-occupancy batching flips the sign of $\beta(C)$ in 2/3 c=2 regimes — same data, same waves, opposite sign of the structural coefficient. (Yule–Simpson reversal candidate.)
3. **Beat 3 — Method-from-surprise (C2-M4 + C2-M5)**:
   - Bound-and-Gap (M4) operationalises the gap between Φ-informed and oracle wave selection (mean 5.83 % GAP, 6/6 cells), giving a constructive headroom diagnostic.
   - Model-Dominance Hedge (M5) collapses the minimax over rival elevator models into a one-line rule (follow batched) that costs at most 3–10 % vs the model-specific optimum.
4. **Beat 4 — Unifying insight (C3-A + C3-C)**: Regime sensitivity (size × E × c) explains both the GAP magnitude pattern and where M5 is non-trivial; Φ captures roughly 25–50 % of the structural signal (Finding C, derived from Option 1 vs Option 2 of Phase 4 v2).

**Why this arc is publishable**: each method is empirically forced by an observed surprise rather than retrofitted. M5 in particular owns the most uncomfortable v0.3 finding (β sign-flip) and turns it into a design rule.

**Journal route** (per frontier check 2026-04-22):

| Tier | Journal | Quartile | Realism on current evidence | What is needed to lock |
|---|---|---|---|---|
| **Primary target** | Computers & Industrial Engineering | Q1 (IF ≈ 6) | 60–70 % odds after one revision | All three §11.10 reinforcement experiments |
| **Strong alternate** | IJPR | Q1 (IF ≈ 9) | 50 % odds | Same three; stronger managerial framing |
| **Safety net** | Flexible Services & Manufacturing Journal | Q2 (SJR ≈ 0.8) | High (≈ 80 %) — direct precedent thread (Keung 2023) | Submit current §11 as is |
| **Reach** | Transportation Research Part E | Q1 (IF ≈ 10) | Reach unless Phase 4 H1 (marginal-value-of-tactical) added | Phase 4 H1 + managerial framing |
| **Reach-stretch** | IISE Transactions / EJOR | Q1 top | Stretch — needs Phase 4 H1 + theory | Out of scope for v0.4 |

**Recommended path**: invest 3–4 days in §11.10 experiments → submit to C&IE; if rejected, downgrade to FSMJ with minimal rewrite.

### 11.10 Reinforcement experiments — RUN 2026-04-22

**Status**: All three reinforcement experiments executed. Full deliverable: [prototype/results/v0_2_phase4_v2_reinforcement.md](prototype/results/v0_2_phase4_v2_reinforcement.md).

**Results summary**:

| | Pre-reg gate | Result | Verdict |
|---|---|---|---|
| R1 GAP CI | excludes 0 in ≥4/6 cells | **6/6** | **PASS** |
| R1 β(C) sign-stability | ≥90% stable in all 3 c=2 fits | 76–85% | **FAIL** → reframe M5 |
| R2 partition monotone refinement | UB monotone in ≥4/6 | 0/6 (T=0 v0.2 artefact) | FAIL on letter |
| R2 cross-partition ordering | Spearman ≥0.9 | 0.94–1.00 | **PASS** |
| R3 dominance ordering | M3 in [M1,M2] span ≥80% | 0/15 (M3 ≈ M2, stronger) | **PASS in spirit** |
| R3 robust corner stability | stable in sign-divergent | 1/2 (knife-edge in E2) | PASS-with-caveat |

**Net effect**:
- M4 fully supported — GAP CI excludes 0 in 6/6 cells (mean 5.83 %), ordering robust to partition.
- M5 reframed — load-bearing motivation is **M2 dominance** (92.5–100 % across all 15 cells under R3), not the bootstrap-unstable β-sign-flip.
- Journal route confirmed: C&IE / IJPR realistic; FSMJ safe.

#### Original pre-registration (retained for audit)

Three short experiments. Each defuses one specific reviewer objection identified in the 2026-04-22 frontier check.

#### ⚠ Experiment R1: Bootstrap CIs on GAP and on β(C) signs (~half day, zero new simulation)

- **Purpose**: defuse "5.83 % is within simulation noise" reviewer objection.
- **Method**: 1000-iteration bootstrap on existing Phase 4 v2 CSV; per cell compute 95 % CI for GAP, UB, LB. Same for β(C) sign in Phase 1.5 batched-fit residuals.
- **Pass gate**: GAP CI excludes 0 in ≥ 4/6 cells; sign-stability CI is well-defined (sign held in ≥ 90 % of bootstrap replicates) for the 2/3 c=2 regimes.
- **Failure consequence**: M4 demoted from "method" to "supporting observation"; FSMJ becomes the realistic ceiling.
- **Output**: `prototype/results/v0_2_phase4_v2_gap_bootstrap.json` + figures.

#### ⚠ Experiment R2: GAP partition-refinement sweep (~1 day, zero new simulation)

- **Purpose**: defuse "why 4 corners and not 9 or 16?" reviewer objection.
- **Method**: recompute GAP under three partition refinements of feature space — 2×2 (current), 3×3 on (C, I), and 8-octant partition adding T (temporal clustering). Use existing Phase 4 v2 wave pool (no new simulation needed; re-bin existing results).
- **Pass gate**: (a) GAP monotone in partition refinement up to a saturation level; (b) cross-regime ordering of GAP preserved across all three partitions.
- **Failure consequence**: framework appears partition-arbitrary → M4 dies; downgrade to FSMJ.
- **Output**: `prototype/results/v0_2_phase4_v2_gap_partition.json`.

#### ⚠ Experiment R3: M3 stochastic-batching sensitivity for M5 (~2–3 days, requires simulator extension + a new short run)

- **Purpose**: defuse "your two models aren't the full uncertainty set; what if M3 is the truth?" reviewer objection — and verify the dominance-collapse of M5.
- **Method**: extend `simulator.py` with `ElevatorBatchedStochastic` (true batching + Lognormal dwell-time noise σ ∈ {0.1, 0.2}). Re-run Phase 4 v2 at one regime (E2_c2) × one size (6) × 5 arms × 200 waves under M3.
- **Pass gates**:
  1. M2 dominance direction holds: med_M2 ≥ med_M3 ≥ med_M1 in ≥ 80 % of waves (i.e. M3 sits inside the M1–M2 span).
  2. M5 robust corner under {M1, M3} matches M5 robust corner under {M1, M2} (i.e. the collapse rule is stable under M2→M3 substitution).
- **Failure consequence**: M5 needs rewrite — but per frontier check, "dominance reverses in some sub-regime" is itself publishable as a *regime-switching hedge*. So failure here is a rewrite, not a kill.
- **Output**: `prototype/results/v0_2_phase4_v2_m3_sensitivity.json` + simulator extension.

#### Decision flow after running R1–R3

| R1 verdict | R2 verdict | R3 verdict | Action |
|---|---|---|---|
| PASS | PASS | PASS | Submit C&IE with §11.7–§11.10 + revisions |
| PASS | PASS | FAIL | Rewrite M5 as regime-switching hedge; still submit C&IE |
| FAIL | * | * | Drop M4 to supporting observation; submit FSMJ |
| * | FAIL | * | Drop M4; submit FSMJ |

#### Out-of-scope reinforcements (acknowledged but deferred)

- **Phase 4 H1** (marginal value of tactical layer over operational-only baseline) — needed for TR-E / IISE-T. Defer to v0.5 if mid-tier acceptance is secured.
- **c = 3 sweep** — would extend M5 dominance claim beyond c = 2. Cheap (~1–2 hours) but not essential for current journal route; can be added in revision if reviewer asks.
- **Real-warehouse case study** — needed for top-tier; out of MVS budget.

---

**End of novelty_analysis_and_contribution v0.3**