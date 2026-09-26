---
title: "Paper 3 — Canonical terminology and naming conventions"
purpose: "Single source of truth for terminology, so wording stays consistent across the manuscript and across work sessions. When in doubt, use the LEFT-hand canonical term; never drift to a listed deprecated/avoid term."
status: "living note; update here when a naming decision is made, then sync the one-line memory pointer"
last_updated: 2026-09-26
change_note: "2026-09-26 (IJPR v2, draft pending author review; previous version backed up at revision_2026-09-26_ijpr/backups/TERMINOLOGY.md.orig_2026-09-26). Removed the retired capacity headline (H_up as capacity-side; 'capacity-bound > policy-bound'; '~72% capacity-side dominant'); renamed T to ready-time dispersion; replaced 'two analytical tools' by the IJPR contribution structure; added Study 2 terms (GSV, P10, P11, fidelity ladder, abstraction bias, screening regret, k*, DL_m); aligned theorem names with SECTION_4_METHODOLOGY.md and the proposed IJPR numbering. Same night, after the independent review: GSV definition includes P10(R); added P7-matched, P8-verify(20), P10g wording, sequence signature, execution robustness."
---

# Paper 3 — Canonical Terminology

A reference for keeping wording consistent. Each row: **canonical term** | what it means | deprecated / do-not-use. Scientific meaning is ruled by `revision_2026-09-02/MASTER_REVISION_BY_SECTION.md` (§0.2, §2.4) and by `revision_2026-09-26_ijpr/STORY_CONTRACT.md`; this file rules names and wording only.

## 1. Contribution structure (IJPR version, 2026-09-26)

| Canonical | Meaning | Do NOT use |
|---|---|---|
| **C1 problem and benchmark** | single-wave composition under shared freight elevators as selection over candidate waves; a candidate fixes the order set and its processing sequence; fixed dispatch rule; reproducible synthetic benchmark | "two-stage scheduler", "joint scheduling" |
| **C2 elevator-model risk** | conditional sample-path ordering between M1 and M2 (any E, any c), two reversal mechanisms, abstraction bias, and the resulting conservative screening | "the two tools" |
| **C3 generate, screen, and verify (GSV) release procedure** | mechanism-aware generation, closed-form screening under M2, event-driven verification of a shortlist; evaluated along the fidelity ladder; Study 1 diagnostics as validity boundary | "optimal procedure", "algorithm that solves the problem" |
| **Study 1** | preregistered Phase 5 diagnostic study plus registered re-analyses; verdicts locked | "the main experiment" (ambiguous) |
| **Study 2** | registered Phase 6 method study (`paper_draft/phase6_method_study_protocol.md`) | "follow-up tuning", "extra experiments" |

- Retired (do not use as a contribution label): **"two analytical tools"**, **"capacity-versus-policy diagnosis"**, **"capacity-bound > policy-bound"**.

## 2. Analytical objects and the release procedure

| Canonical | Meaning | Do NOT use |
|---|---|---|
| **Bound-and-Gap decomposition** | partition-relative diagnostic: `GAP = H_up + M_Φ` (= UB − LB) over the corner-class family; its preregistered utility gate was not met (H-D1 PARTIAL), so it is described as a **prototype-regime diagnostic** (preregistration line 213) | "M4", "tool that measures what is reachable", "capacity diagnosis" |
| **Model-Dominance Hedge Rule** (short: **Hedge Rule**) | when class medians are ordered (M1 ≤ M2), minimax class selection over {M1, M2} equals the M2-best class; a corollary of the ordering | "M5", "dispatch rule", "Theorem" (it is corollary-level) |
| **generate, screen, and verify (GSV) procedure** | Study 2 method: (1) generate candidates G = R ∪ P10(R) ∪ P11 (random pool, its P10 re-orderings, and the P11 constructions), (2) screen all in closed form under M2 and keep the first k distinct sequence signatures, (3) verify them by DES-M2 and release the DES-best | "GSV algorithm" as if exact |
| **P10 sequence-aware re-ordering** | deterministic operator that re-orders a candidate's processing sequence: same-(src, dst) orders adjacent, groups chained destination-to-origin, readiness respected | "clustered dispatch" (that is the operational `policy="cluster"` flag) |
| **P11 co-ride-aware constructive generator** | builds candidate waves from the order pool to create co-rides and avoid adverse repositioning; hyperparameters locked by a registered training-pool rule | "optimizer" |
| **shortlist size k**, **recovery shortlist size k\*** | k = number of distinct screened candidates (sequence signatures) sent to DES; k\* = smallest k whose screening regret is within the G3 tolerance (max{2%, 1 s / optimum} in protocol draft 3) | |
| **screening regret r(k)** | (DES-M2 makespan of the DES-best among the first k distinct signatures by the screening key − DES-M2 optimum over the candidate set) / that optimum | |
| **fidelity ladder** | evaluators ordered by fidelity: M1 → M2 → DES-M1 → DES-M2 | |
| **manuscript symbols for GSV (§4.5, added 2026-09-26)** | code/protocol name → manuscript symbol: candidate set G → augmented pool 𝒦⁺ = 𝒦 ∪ 𝒦^seq ∪ 𝒦^con (k indexes candidates); screening key → ψ_k; shortlist size k → K_V (K = \|𝒦\| is the pool size in Section 3); shortlist → 𝒦^V (so K_V = \|𝒦^V\|); released candidate → k†; screening regret r(k) → Reg(K_V); recovery size k\* → K_V^⋆; DES-M2 → M₂^DES with makespan ℓ_{kM₂^DES}. Checked against the final Section 3 (`Problem formulation.docx`, mirror `revision_2026-09-24/section3_bilingual_2026-09-24.md`) and `SECTION_4_METHODOLOGY.md`: 𝒮 is Section 3's option set (Table 3.3, Eq. (32)); G_τ, k, s_o, r_o, ρ_q, Δ_H, and ε are already used; a superscript C could read as a complement | 𝒮, r, s, or 𝒢 for any GSV quantity in manuscript prose |
| **decision loss DL_m** | DES-M2 makespan of the pool optimum chosen under evaluator m, relative to the DES-M2 pool optimum | "regret" in prose (see §4 wording rule) |
| **abstraction bias B** | per wave, (C_max under M2 − C_max under M1) / C_max under M1 | "error of M1" |

## 3. Elevator evaluators

| Canonical | Meaning | Do NOT use |
|---|---|---|
| **M1 / throughput abstraction** | `E × c` independent single-rider slots | "abstraction" alone when ambiguous; "physical model" |
| **M2 / true co-occupancy batching** | `E` cars; a request boards a stored trip with the same (src, dst), spare capacity, and request time no later than the end of loading | "batched" alone when ambiguous |
| **M3 / stochastic batching** | M2 with mean-one lognormal multipliers on the four trip phases (σ = 0.20 in Block C) | "noisy model" |
| **closed-form sequential time-accumulator** | the production evaluator family (`simulator.py`) behind M1, M2, M3 | "event-driven simulator" (forbidden for these) |
| **DES-M1 / DES-M2** | the event-driven evaluator (`src/des_evaluator.py`, modularized from the B-5 heapq engine; concurrent AMRs; FIFO elevator queue) under M1 or M2 rules. Study 2 uses the **board-first** M2 rule (a matching request boards an open trip before any free car is dispatched, as in the closed-form M2); B-5 did not board onto trips opened in the same service pass (see protocol §3.5 and S1-12) | "SimPy model" (B-5 used heapq, not SimPy); "the B-5 engine" for the Study 2 evaluator |

- The family is written **{M1, M2, M3}**; in the Abstract unpack it in words.

## 4. The structured representation Φ

| Canonical | Meaning | Do NOT use |
|---|---|---|
| **Φ = (C, I, T)** | three descriptors of a wave | "surrogate", "predictor of makespan" |
| **C = endpoint dispersion** (plain prose: **vertical spread**) | Shannon entropy of the endpoint floor distribution; **HIGH C = endpoints spread over many floors**; carries no distance information | ⚠ "vertical concentration" (REVERSED MEANING) |
| **I = directional imbalance** | up-versus-down asymmetry of cross-floor orders | |
| **T = ready-time dispersion** | coefficient of variation of ready-time offsets; high T = dispersed; 0 when all orders are ready at release; not used in the corner classes | "temporal clustering" (retired 2026-09-26) |

- Φ is a **structured decomposition**, not a predictive surrogate. Never write "Φ predicts makespan". Use **selects / represents / characterizes**.
- **corner class** = a tail intersection of C and I (HH, HL, LH, LL); **cell** = a unit of a covering partition (Theorem 1 / refinement); **setting** = configuration × evaluator × wave size (replaces "sub-cell").

## 5. Decomposition components (Study 1)

| Canonical | Meaning | Notes |
|---|---|---|
| **GAP** | UB − LB = `H_up + M_Φ` | a partition-relative quantity; mean 0.060 at publication scale |
| **H_up = upper-tail headroom** | (worst class median − pool median) / pool median, relative to the corner-class family; can be negative | NOT capacity-side; NOT "unrecoverable by any policy" (P9 beats the corner oracle in 7/12 cells) |
| **M_Φ = class-selection miss** | (selected class median − best class median) / pool median | equals the class-action SPO loss (definitional) |
| **share readings** | H_up / GAP is about 72% under the preregistered Φ rule and about 47% under the covering partition | always report both; never call either a "capacity share"; test–retest ICC ≈ 0.01 / −0.03 |

- **"regret" wording rule:** keep "SPO loss / regret" only in formal statements; in the Abstract and plain prose use **"decision loss"** / 中文 **"决策损失"**.

## 6. Layers and "policy" (keep distinct)

| Canonical | Belongs to | Meaning |
|---|---|---|
| **tactical layer** | the problem | which orders are released together **and in which processing sequence** (the fixed dispatch rule processes orders in release sequence) |
| **operational layer** | the problem | dispatch of AMRs and elevator service under a fixed rule (`policy="fifo"` held fixed; `policy="cluster"` is the Supp-1 alternative, reported as a boundary) |

- Do not write "two-stage". Canonical bridge sentence: *"We hold the dispatch rule fixed and study the tactical release decision."*
- **"policy" is double-edged, always disambiguate.** Tactical = **wave-release policy** / 中文 **放行策略** (P0 to P11, the Hedge Rule's output, GSV); operational = **dispatch rule** / **operational dispatch** / 中文 **操作阶段调度**. Never call the Hedge Rule, P10, or GSV a "dispatch policy".
- Policy names: P5 = OLS-sign corner rule; P6 = squared-error decision-tree comparator (not "SPO-Tree"); P7 = 40-iteration local-search reference (not "optimum"); **P7-matched** = budget-matched multi-start local search with the same P10 operator and the same verification step as GSV (Study 2's search comparator); P8 = savings-style heuristic; **P8-verify(20)** = the 20 best P8 candidates, re-ordered by P10 and verified by DES-M2 (Study 2's comparator at equal verification budget); P9 = wave-level SPO+ policy; **P10g** = grouping with readiness ordering but no chaining, used only for the chaining increment; **pool optimum** only for an enumerated candidate pool.
- **Sequence signature**: the ordered (source, destination, ready offset) list of a candidate; candidates with equal signatures are the same wave for every evaluator, and shortlists count distinct signatures.
- **Execution robustness**: re-evaluation of released waves by evaluators that did not select them (DES-M2 with phase noise, DES-M2 under the B-5 boarding semantics); gate wordings say "under the event-driven evaluator".

## 7. Evaluator ordering (formerly "chain dominance")

| Canonical | Meaning |
|---|---|
| **evaluator ordering** | per wave, `C_max(W; M1) ≤ C_max(W; M2)` (the throughput abstraction is optimistic) |
| **ordering theorem** | the conditional all-E, all-c result with conditions (a) to (d): **Theorem 1** of the manuscript since 2026-09-27 (renamed from Proposition 3 after the author's verification of Appendix A, MATH_VERIFICATION_LOG rows 4 to 12); SECTION_4_METHODOLOGY.md and the signed registrations still call it Proposition 3 |
| **batch overtaking**, **adverse repositioning** | the two reversal channels; with aligned sequence and assignment they are exhaustive (18 and 2 of 20 enforced-run violations; "all violations are overtaking" is RETIRED) |

- Report separately: condition coverage (joint conditions hold in < 1% of waves) and ordering frequency (99.2% of matched waves). Never "the theorem explains 99.2%".
- ⚠ The "single-rider model is optimistic" sign is the mirror image of classic elevator round-trip-time batching results; always state the two setup assumptions (same-(src, dst) boarding; E·c versus E servers).
- In the Abstract, refer to it descriptively, not by number.

## 8. Verdicts (report honestly, never re-judge)

H-D1 **PARTIAL** (57/72 against 58/72) [PR-C]; H-D2 **PASS** under its four Block C gates [PR-C]; H-Policy **Partial** [PR-C]; H-D3 **model-sensitive** [PR-E]; Supp-1 **PARTIAL**, Supp-2 **PASS** [AM2]; Amendment F reliability **FAIL**, C-4 informativeness **FAIL**, B-5 ordinal fidelity **FAIL** [NS]. Study 2 verdicts use the wording ladders of the Phase 6 protocol.

## 9. Scale labels and result prefixes (NEVER mix unlabelled)

| Canonical | Meaning |
|---|---|
| **publication scale** | Phase 5, 18-config grid, 106,800 model evaluations, `v0_5_phase5_*.json` |
| **prototype scale** | Phase 4 v2, the older 6-cell `E∈{1,2,3}×c2` grid, `v0_2_*`, old M4/M5 naming |
| **Study 2 scale** | Phase 6, 18 configs × 8 independent order pools, `v0_6_phase6_*.json` |
| **calibrated case** (third scale) | literature-calibrated configurations (config_id ≥ 100), `v0_6_case_*.json`; only "within publicly documented ranges" |
| **small-instance census** | B-11 exhaustive census (wave sizes 2 to 4); belongs to no grid |

- Evidence tags follow master §0.3 ([PR-C] [PR-E] [AM1] [AM2] [RA] [NS] [EXP] [QA]); Study 2 items carry [NS] plus the protocol item number (e.g. [NS] P6-G2).

## 10. Writing-style rules

- **No em-dashes (—) anywhere** in the manuscript. Use commas, parentheses, colons, or sentence splits. Keep hyphens in compound terms (Bound-and-Gap, five-phase, AMR-elevator) and `--` page ranges in BibTeX.
- **Chinese version of any bilingual passage:** plain words, no math symbols (Φ → "三维描述"; H_up → "上尾余量"; M_Φ → "选类失误"; GAP → "差距"). Keep proper method names (Bound-and-Gap, Hedge Rule, generate, screen, and verify, Wasserstein, Smart-Predict-then-Optimize).
- Citation years: the formal journal year, not the arXiv year (Elmachtoub and Grigas **2022**; Vera et al. **2021**).
- Never write "calibrated to a facility"; write "parameters set within publicly documented ranges".

## 11. Quick checklist (scan before finalizing any section)

- [ ] Contributions stated exactly as in STORY_CONTRACT.md §3; no "two analytical tools", no capacity diagnosis.
- [ ] H_up called upper-tail headroom; both share readings (72% and 47%) given together; no "capacity-side".
- [ ] C = endpoint dispersion / vertical spread (high = spread out); T = ready-time dispersion.
- [ ] Φ described as a decomposition, never "predicts makespan".
- [ ] Every "policy" disambiguated (release policy versus dispatch rule); no "two-stage".
- [ ] The closed-form evaluator is never called event-driven; DES means the event-driven evaluator of `src/des_evaluator.py` (modularized from the B-5 heapq engine, board-first M2 rule); "B-5 semantics" names the old boarding rule.
- [ ] "regret" only in formal statements; prose uses "decision loss".
- [ ] Ordering theorem named descriptively in the Abstract; condition coverage and ordering frequency reported separately.
- [ ] All verdicts reported as locked; Study 2 results use the protocol ladders.
- [ ] Every number carries its scale label and evidence tag.
- [ ] Zero em-dashes; Chinese passages symbol-free; journal citation years.
