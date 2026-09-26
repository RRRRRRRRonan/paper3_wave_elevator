---
title: "W5: Section 6 (Discussion, Limitations, Conclusion) full draft"
date: 2026-07-08
integration_note_2026_07_08: >
  AMENDMENT A-R1 EXECUTED AFTER THIS DRAFT WAS WRITTEN; ITS LOCKED RULE
  FIRED. Capacity share H_up/UB (oracle-slack metric, stored A4 data, 6
  configs, size 16, M2) exceeds 0.5 in only 2/6 configs under the 2x2 scheme
  and 4/6 under 3x3 (5/6 under 2x2x2 with T). Per the locked rule, every
  "about 72%" / capacity-side-dominance sentence in the AFTER texts below
  must carry the qualifier: "measured with the Phi-rule share
  H_up/(H_up + M_Phi) on the 72-sub-cell grid at the 2x2 partition; under
  the oracle-slack metric H_up/UB the dominance is regime-dependent
  (per-config shares 0.25 to 1.00, see the partition-sensitivity table)".
  Limitation (6) can now quote the actual outcome instead of only citing the
  amendment: use the numbers in
  revision_2026-07-08/tables/T5_partition_sensitivity.md. Open issue 9 is
  thereby resolved.
sources_consulted:
  - "f:/Paper 3/CLAUDE.md"
  - "f:/Paper 3/paper_draft/TERMINOLOGY.md"
  - "f:/Paper 3/paper_draft/outline_v0_1.md (sections 7-9: prototype-scale scaffold, superseded)"
  - "f:/Paper 3/paper_draft/section5_draft_v0_1.md (to avoid duplication; source of Table 2-4 numbers)"
  - "f:/Paper 3/paper_draft/section4_draft_v0_1.md (result numbering: Prop 1, Thm 1, Cor 1, Prop 2, Thm 2, Cor 2)"
  - "f:/Paper 3/paper_draft/storyline_motivation_to_contribution_v1.md (section 3 config-7 worked example; section 7 honest boundary)"
  - "f:/Paper 3/prototype/results/v0_5_phase5.md (gate verdicts: H-D1 PARTIAL 57/72, H-D2 PASS)"
  - "f:/Paper 3/prototype/results/v0_5_phase5_blockA.json (config 7 batched size 8: H_up 0.157, M_Phi 0.021, GAP 0.178, CI [0.099, 0.285])"
  - "f:/Paper 3/prototype/results/v0_5_phase5_blockC.json (config 7: U_c(0.05) = 9.5 on m_0 = 283 for the Hedge corner LC_HI; per-corner dominance 0.98-1.00)"
  - "f:/Paper 3/prototype/results/v0_5_phase5_supp.json + prototype/src/analysis_phase5_supp.py (Supp-1 mean MV 10.2%, 12/12 cells > 1%, verdict PARTIAL; Supp-2 capacity sweep 99.7-100.0%)"
  - "scratchpad/panel_completeness.json (fatal flaw 1: no Section 6/Discussion/Limitations; required addition 10)"
  - "scratchpad/panel_methods.json (flaws 1, 2, 4, 7: closed-form simulator unvalidated, pool-relative quantities, aliasing, external validity)"
  - "f:/Paper 3/revision_2026-07-08/amendments/AMEND-2026-07-08-A_reanalysis.md (item A-R1)"
  - "f:/Paper 3/revision_2026-07-08/amendments/AMEND-2026-07-08-B_deferred_experiments.md (items B-2, B-3, B-5, B-6)"
status: "draft for author review"
---

# W5. Section 6: Discussion, Limitations, and Conclusion (new manuscript section)

**Placement.** Insert as the final numbered section of the manuscript, directly after Section 5 (`paper_draft/section5_draft_v0_1.md`) and before the References. Word count of the manuscript text below: approximately 1,400 words, inside the 1,200-1,600 target.

**Scale convention.** Every number in the drafted text is labelled. All headline numbers are publication scale (Phase 5, 18-config grid, 106,800 simulations, `v0_5_phase5_*.json`); the single prototype-scale mention (the retired pilot expectation in 6.1) is labelled as such.

---

# Edit W5-1: New subsection 6.1, the managerial reading

## 修改前 (BEFORE)

(no existing text; new section)

The only precursor material is the prototype-scale scaffold in `paper_draft/outline_v0_1.md`, section 7 "Discussion" (approx. lines 291-314). That scaffold is bullet-point, uses retired M4/M5 naming and prototype-scale numbers (3-10% worst-case loss, 25-50% slack), and includes the prototype-era "substitutability map" reading that did not survive the publication-scale Supp-1 result. It is superseded, not edited, by the text below.

## 修改后 (AFTER)

# Section 6. Discussion, Limitations, and Conclusion

## 6.1 Managerial reading: a capacity-versus-policy diagnosis

Unless labelled otherwise, every number in this section is a publication-scale measurement from the Phase 5 grid (18 configurations, 106,800 pre-registered simulations; Section 5).

The paper's managerial deliverable is a diagnosis, not a makespan reduction. Across the 72 Block A sub-cells the mean value of wave structure is `GAP = 0.060`, that is, 6.0% of the random-pool median makespan, and the Bound-and-Gap decomposition splits it into `H_up = 0.043` and `M_Φ = 0.017`. About 72% of the mean gap is the structural ceiling: capacity-side headroom that no wave-release policy operating on the `(C, I)` partition can recover. About 28% is the policy component, the share that a better Φ-informed wave-release policy can recover, and the share that Theorem 1 identifies with the decision loss of a partition-constant predict-then-optimize step, so that recovering it can be handed to existing decision-focused methods (Elmachtoub and Grigas, 2022). The headline reading is capacity-bound over policy-bound: across this grid, the binding limitation on wave makespan sits predominantly on the capacity side, not in the sophistication of the wave-release policy.

Configuration 7 makes the diagnosis concrete (5 floors, 5 AMRs, 2 elevators, clustered demand; true-batching model M2, wave size 8; publication scale). The decomposition gives `GAP = 0.178` with a 95% bootstrap confidence interval of [0.099, 0.285] that excludes zero, split into `H_up = 0.157` (88% of the cell's gap) and `M_Φ = 0.021` (12%). Tool 1 therefore reads: wave composition matters here, but it is a small lever; a feature-engineering effort can chase at most 2.1% of makespan, while 15.7% is structural at this partition, so an operator who needs a large reduction should buy capacity rather than tune composition. Tool 2 then answers the release question that remains: the Hedge Rule selects the corner with low vertical spread and high directional imbalance (LC-HI, in the corner notation of Section 5), which coincides with the Wasserstein-DRO optimum for this configuration; per-wave dominance `M2 ≥ M1` holds in at least 98% of matched waves in every corner of this configuration, and the one-sided worst-case bound at the selected corner is `U_c(0.05) = 9.5` time units on a median makespan of 283, about 3.4%. The operator thus obtains a release choice that requires no elevator-model identification and carries a computable downside bound.

The decomposition also settles when to invest in wave composition at all. Where `M_Φ` is material, composition deserves active management, and Theorem 1 says the recoverable share is exactly what off-the-shelf predict-then-optimize training targets. Where `H_up` dominates, as it does on about 72% of the mean gap in this grid, the constructive options are capacity-side: relieve the elevator bottleneck, or refine the partition itself, since Corollary 1 guarantees the measured ceiling is monotone under refinement, so a finer wave-structure taxonomy exposes more of the gap to explicit management (Section 4 gives the four-quadrant diagnostic table). Even a null reading is informative: the 15 sub-cells whose gap the pre-registered gate leaves unresolved are almost exactly those where the gap is genuinely near zero (median `GAP` 0.017, against 0.064 for the 57 resolved sub-cells; rank statistic 0.92; Section 5.2), so the tool also tells the operator where wave composition is not worth managing.

Honesty requires one cross-layer comparison. A pre-registered supplementary experiment quantifies the operational dispatch lever that this paper deliberately holds fixed: replacing FIFO dispatch with destination-clustered dispatch lowers median makespan by a mean of 10.2% across the 12 tested cells, exceeding 1% in all 12 (publication scale). Two observations follow. First, this breadth corrects a prototype-scale expectation: the pilot (prototype scale, six-cell grid) had suggested the dispatch benefit was regime-conditional, and the pre-registered regime-conditionality gate returned PARTIAL at publication scale precisely because the effect turned out to be broad rather than conditional; we therefore retire the earlier regime-conditional reading rather than defend it. Second, the operational lever (10.2%) exceeds the entire mean tactical gap (6.0%). For practitioners the implication is blunt: the tactical wave-release lever studied here is modest and largely capacity-bound, and the largest single makespan lever inside the model sits in the operational stage. The tactical tools retain their value precisely because they are cheap diagnostics: they report whether composition is worth managing before anything is spent, and they price the robust release choice when it is. For research, the same comparison fixes the follow-up agenda: optimizing the operational stage, dispatch under elevator contention, is a separate decision problem with its own action space, and we scope it to a separate line of work rather than appending it to this one.

## 理由 (RATIONALE)

对应 panel_completeness 致命缺陷 1(手稿完全没有 Section 6 / Discussion / Limitations,属 CRITICAL)及其 required_additions 第 10 条(要求按 Supp-1 范式修正更新讨论)。同时落实 panel_methods 缺陷 7 的辩护方案:诚实重构价值主张,明确说出"+10.2% 操作层杠杆(本文固定不动)超过整个战术 GAP(6.0%)",并把它转化为后续操作层研究议程,而不是回避。config-7 数字逐项核对自 v0_5_phase5_blockA.json(H_up 0.157、M_Φ 0.021、GAP 0.178、CI [0.099, 0.285])与 blockC.json(LC_HI 角 U_c(0.05)=9.5、m_0=283,即 3.4%)。全文遵守 TERMINOLOGY.md:无破折号、C 为 vertical spread、Hedge Rule 只"释放波次"、平实语境用 decision loss 而非 SPO regret、每个数字带规模标签。

---

# Edit W5-2: New subsection 6.2, the limitations list

## 修改前 (BEFORE)

(no existing text; new section)

The only precursor is `paper_draft/outline_v0_1.md`, section 8 "Limitations" (approx. lines 317-329): a seven-item prototype-scale list in retired M4/M5 naming, keyed to Phase 4 v2 artefacts (Gap 1/2/3, H1, β(C) sign softness). It is superseded by the eight-item publication-scale list below, which incorporates the Phase 5 findings and the 2026-07-08 amendments.

## 修改后 (AFTER)

## 6.2 Limitations

We state eight limitations. Each ends with its consequence, and where a registered follow-up exists we cite the dated pre-registered amendment.

(1) **Single evaluation model.** All makespans are produced by one closed-form, sequential time-accumulator simulator, not by an event-driven concurrent model, so every reported phenomenon, including the 99.2% per-wave dominance frequency (publication scale), is so far a property of this model class; an event-driven cross-validation with locked acceptance gates is registered as amendment B-5 and pending execution.

(2) **Fully synthetic instances.** The grid contains no real warehouse trace, industrial layout, or vendor-calibrated parameters, so absolute effect sizes are model quantities, not field estimates.

(3) **Constant service times.** Loading and unloading are fixed at 2 s each and intra-floor handling at a constant per-order service time, with stochasticity confined to the M3 elevator-phase noise, so floor-level congestion and any effect driven by service-time variability lie outside the model.

(4) **Pool-relative quantities.** `GAP`, `H_up`, and `M_Φ` are defined relative to a shared sampled candidate pool, and the reference optimizer P7 is a 40-iteration local search rather than an exact optimum, so the 72/28 split is anchored to this pool; an enumeration benchmark over the pool and pool-sensitivity runs are registered as amendment items B-2 and B-6.

(5) **Aliased fractional design.** The 18 configurations form a one-third fraction with defining relation `demand_idx = (F_idx + A_idx) mod 3`, so the floor count `F` is confounded with fleet size `|A|` and demand pattern; no clean `F` main effect is identifiable, and every per-factor contrast in Section 5 is a mixture of aliased effects.

(6) **Partition-relative split.** The 72/28 capacity-versus-policy split is measured at the 2x2 quartile-corner partition, and Corollary 1 implies `H_up` moves monotonically under refinement, so the split is a property of the partition resolution as well as of the system; the partition-sensitivity reanalysis (amendment A, item A-R1) accompanies the headline for this reason.

(7) **Block B scope.** The seven-policy contest runs only under the true-batching model M2 with `E = 2` elevators and wave sizes {8, 30}, so its conclusions do not automatically extend to other elevator models, single-elevator regimes, or other wave sizes.

(8) **Grid-bound numbers.** The specific percentages reported (72%, 79.2%, 99.2%, 10.2%, 3.4%; all publication scale) are measurements of this grid, not universal constants: the tools generalize, because the decomposition is an identity, the theorems carry testable conditions, and both can be re-measured on any new facility with one sweep of the same protocol, but the numbers do not.

## 理由 (RATIONALE)

对应 panel_completeness required_additions 第 10 条明确点名的清单(simulator-only、无真实数据、常数服务时间、pool 相对定义、混叠部分因子设计、2x2 分区相对的 72/28、Block B 范围限制),外加任务规定的第 8 条"数字不泛化"(来自 storyline 第 7 节"诚实的边界")。第 (1) 条同时回应 panel_methods 致命缺陷 1(闭式模型未经外部验证且被误标为 event-driven):此处按正确名称"closed-form sequential time-accumulator"陈述,并援引已注册的 B-5 修正案;第 (4) 条回应其缺陷 2(pool 相对、无精确基准),援引 B-2/B-6;第 (5) 条回应其缺陷 4(混叠未披露),给出定义关系原文;第 (6) 条援引 2026-07-08 修正案 A 的 A-R1。每条一句后果,符合"reviewers reward this"的写法要求。

---

# Edit W5-3: New subsection 6.3, the conclusion

## 修改前 (BEFORE)

(no existing text; new section)

The precursor is `paper_draft/outline_v0_1.md`, section 9 "Conclusion" (approx. lines 333-337), a three-bullet prototype-scale scaffold. Superseded by the text below.

## 修改后 (AFTER)

## 6.3 Conclusion

This paper formalized wave release coordination under vertical resource constraints in multi-story AMR warehouses as a two-stage problem, held the operational stage fixed, and studied the tactical stage with two analytical tools defined on one structured representation `Φ = (C, I, T)`. The Bound-and-Gap decomposition is the diagnostic tool: it splits the value of wave structure into a structural ceiling `H_up` and a policy-recoverable component `M_Φ`, its two structural claims hold exactly in 72 of 72 publication-scale sub-cells, and its pre-registered signal-resolution gate resolved 57 of 72 sub-cells (79.2%), one sub-cell short of the pre-registered 58/72 bar, recorded as PARTIAL and not re-judged. The Model-Dominance Hedge Rule is the prescriptive tool: under chain dominance the minimax wave-structure choice collapses to the corner optimal under the true-batching model, coincides with the Wasserstein-DRO solution in all six tested configurations, and passed all four pre-registered gates (PASS), with per-wave dominance averaging 99.2% (96.0% in the worst cell) and persisting at 99.7% to 100.0% across per-trip capacities `c ∈ {2, 3, 4, 5}` (all publication scale).

The takeaway is one sentence: in elevator-constrained multi-story AMR warehouses, the makespan cost of a wave is bounded mainly by vertical capacity rather than by the sophistication of the wave-release policy, so an operator should measure the split first, recover the policy share with a closed-form robust rule where it is material, and direct the remaining effort at the capacity side.

Four lines of future work follow directly from the limitations. First, the operational stage: dispatch optimization under elevator contention, where the largest measured lever in our model sits (10.2%, publication scale), is a separate research problem and will be treated as such. Second, external validation: an event-driven cross-check of the closed-form simulator is registered with locked gates as amendment B-5. Third, realism: calibration against real warehouse traces and vendor specifications remains open. Fourth, method-internal sensitivity: tercile partitions and candidate-pool sensitivity are registered as amendment item B-6, and a published-heuristic comparator as item B-3, with hypotheses and reporting rules fixed before execution in every case.

## 理由 (RATIONALE)

对应 panel_completeness 致命缺陷 1(引言路线图承诺了不存在的 Section 6)。结论段严格按 TERMINOLOGY.md 第 7 节要求诚实复述判定:H-D1 PARTIAL(57/72,差一格,门槛不动)、H-D2 PASS,两工具结论不同如实并列,不重新裁决。未来工作四条与任务规定一致(操作层独立研究、DES 交叉验证 B-5、真实数据标定、terciles 与候选池敏感性 B-6),全部挂接到已注册的日期化修正案,避免出现"事后加实验"的印象。一句话结论与 storyline 第 0 节的主线一致,并把"容量侧主导"作为发现而非失败来收束。

---

# Pre-finalize check (TERMINOLOGY.md section 10)

- Tools named Bound-and-Gap decomposition / Model-Dominance Hedge Rule: yes, no M4/M5.
- C used only as vertical spread (LC-HI unpacked as "low vertical spread, high directional imbalance"): yes.
- Φ never "predicts": yes (selects, identifies, reports).
- Stage vs tool kept distinct; Hedge Rule releases waves, never a dispatch rule; operational rule called "dispatch": yes.
- "Decision loss" in prose, "SPO regret" reserved for Section 4: yes.
- H-D1 PARTIAL with discriminating-power framing; H-D2 PASS; no verdict re-judged: yes.
- Every number scale-labelled; the single prototype-scale mention is labelled: yes.
- Zero em-dashes: yes.
- Citation year Elmachtoub and Grigas 2022 (journal year): yes.
