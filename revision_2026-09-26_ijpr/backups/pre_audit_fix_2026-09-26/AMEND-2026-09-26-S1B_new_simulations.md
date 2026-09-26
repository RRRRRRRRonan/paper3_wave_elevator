---
title: "Registered new simulations for Study 1 (2026-09-26): S1-2, S1-3, S1-8, S1-9, S1-11, S1-12"
parent: "paper_draft/phase5_scaleup_preregistration.md (LOCKED 2026-05-19); revision_2026-07-08/amendments/ (six signed amendments)"
date: 2026-09-26
status: "DRAFT, prepared overnight by the assistant at the author's request. NOT signed. NOTHING executed. No candidate pool listed below has been enumerated, and no Block A or B regeneration has been run."
author_signoff: "PENDING"
evidence_tags: "[NS] for S1-2, S1-3, S1-8, S1-11; [QA] for S1-9 and S1-12"
---

# Registered new simulations for Study 1

## 中文摘要

- 本文件登记六项需要新仿真的研究一工作：S1-2 全池枚举（精确的类别中位数与池内最优）；S1-3 Block C 扩展到其余 12 个配置与规模 8、30；S1-8 最好的波次在 (C, I) 平面的位置；S1-9 修复破平后重跑 Block A/B（先写报告规则）；S1-11 另外两个 1/3 分数的闭式描述层（对应 D-D）；S1-12 用修正后的登梯规则重跑 B-5 的 DES 对照（夜间模块化 DES 时发现 B-5 在同一服务轮里不让第二个同路线请求搭上刚派出的车，新规则与闭式 M2 一致；旧判定保留，新数并列）。
- 全部用当前生产模拟器（2026-09-11 已修破平），全部是描述性结果，没有新门槛，不改任何锁定判定。
- 计算量都在分钟到一小时级别。
- 你要确认：S1-11 是否做（取决于 D-D）；S1-9 的新旧并列规则；S1-2 中"有利角类"取已存的还是全池重拟合（我建议两者都报，主用已存的）。

## General rules

1. Simulator: production `simulate_wave` as of the G0 code freeze (tie-break fixed 2026-09-11), deterministic M1 and M2; M3 only where stated.
2. No stored artefact is overwritten. Outputs: `results/v0_5_phase5_S1-<item>_*.json` and `results/raw/mvs_v0_5_phase5_S1-<item>_*.csv`.
3. None of these items has a gate. Each is descriptive and reported beside the locked verdicts, never merged into their counts.
4. Every output records its code hash, input hashes, and the SHA-256 of this registration.

---

## S1-2. Full-pool enumeration [NS]

**Pools.** The stored Phase 5 candidate pools, regenerated from their seeds:
- Block A: for every configuration (0 to 17), model m ∈ {abstraction, batched}, and size n ∈ {8, 30}: `build_candidates(pool, n, 3000, Random(_seed(cid, MODEL_IDX[m], n)))` on the Phase 5 order pool (seed SEED_BASE + cid). 72 pools. The Block B pools are the batched Block A pools of configurations 1, 3, 5, 7, 9, 11 (same seeds), so they are included.
- Block C: `_seed(cid, 99, 16)` for configurations 1, 3, 5, 7, 9, 11. 6 pools.
- The enumeration uses the current simulator; the regeneration checks that tie it to the stored rows are listed below.

**Evaluation.** Every candidate of every pool under M1 and M2 (78 × 3,000 × 2 = 468,000 closed-form runs).

**Quantities per pool.**
- Exact class medians of the four corners and of the whole pool; exact H_up, M_Φ, GAP with (i) the stored favourable corner, which is primary because it is the corner the preregistered rule actually chose (Block A pools only, under the model the pool was seeded for; Block C has no stored corner), and (ii) the corner from `fit_phi_beta` on the full pool, secondary (and the only one for Block C); exact corner sizes and pairwise overlaps (overlaps arise only from quantile ties).
- Pool optimum (lowest makespan and its tie count) under each model.
- Covering partitions: exact class medians on the 2 × 2, 3 × 3, and 4 × 4 quantile partitions of (C, I) over the full pool (binning rule of `experiments_phase5_ablation._bin`, as used by A-R1), with H_up(P), S_or(P), UB(P) = H_up(P) + S_or(P), and the share H_up(P)/UB(P) of Corollary 1 in `SECTION_4_METHODOLOGY.md` §4.2.3 (diagnostic resolution) and of A-R1. M_Φ(P) is also reported, with the favourable cell defined as the extreme bin in the direction of the fitted signs; this generalizes the corner rule and is labelled as such.
- Minimax-reduction quantities (Theorem 2 in `SECTION_4_METHODOLOGY.md` §4.4.1, planned as Corollary 1(a) in the IJPR numbering) on full classes: the per-candidate ordering rate M1 ≤ M2, the minimax corner on class medians and on class means (the D2-d basis), and the one-sided bound U_c(0.05) computed on full classes.
- For the 12 Block B cells: the gap of the stored P5, P6, P7, P8, and P9 cell medians (M2; P8 from `b2_b3_benchmarks.json`, P9 from `amendC1_p9_spoplus.json`) to the exact pool optimum, (value − optimum) / optimum. The stored medians predate the 2026-09-11 tie-break fix while the optimum uses the current simulator; this is stated with the table. P7 searches the whole order pool, so its gap can be negative; this is reported as it falls.
- Regeneration checks: Block A pools against the stored Block A rows (differences at consequential ties are counted, not errors); Block C pools against `mvs_v0_5_phase5_blockC_tiebreakfix.csv`, which uses the current simulator semantics, so every value must agree exactly; any disagreement stops the run.

**Reporting rule (locked).** Sampled values (the locked analyses) and exact values are shown side by side, labelled "sampled, preregistered" and "exact enumeration, [NS]". No locked count is recomputed from exact values.

**Prior exposure.** Pool optima are known for two cells (configuration 0, size 8, E = 1: 70; configuration 1, size 8: 38; AMEND-B B-2). No other quantity here has been computed.

---

## S1-3. Block C coverage extension [NS]

**Design.** `run_chain_block` (unchanged code; matched waves; models M1, M2, M3 with σ = 0.20) on:
- the 12 configurations not in Block C (all E = 1 configurations 0, 2, …, 16, and the F = 8, E = 2 configurations 13, 15, 17) at size 16; and
- all 18 configurations at sizes 8 and 30.
Seeds follow the Block C convention `_seed(cid, 99, n)`; 5 arms × 200 waves; candidate pool 3,000. The 6 original configurations at size 16 are not rerun. 48 (configuration, size) units × 1,000 waves × 3 models = 144,000 runs.

**Quantities.** The D2-a per-wave ordering rate and D2-b FOSD rate per cell; D2-c U_c(0.05); the Hedge corner (means and medians), the DRO corner and their collapse; second-place margin, clustered stability, and the minimax-regret corner (S1-6 definitions); abstraction bias B per wave (TH-2).

**Reporting rule (locked).** The locked H-D2 verdict (PASS on 6 configurations at size 16) is unchanged. The extension is reported as a separate block titled "coverage extension", with its own counts and the same thresholds shown for reference only ("would meet the D2-a threshold in x of y units"). If any extension unit falls below the D2-a thresholds, it is reported in §5.5 as a boundary of the ordering result.

---

## S1-8. Where the best waves are [NS; depends on S1-2]

**Design.** For each of the 72 Block A pools (under its own model) and the 6 Block C pools (under M2): the top 1% of candidates by makespan (the 30 lowest; ties at the cut-off included and counted).

**Quantities.** Share of top-1% candidates inside the favourable corner (the full-pool-fit corner for every pool; for Block A pools also the stored corner), inside any corner, and in each cell of the 4 × 4 (C, I) quartile grid; enrichment ratio of each grid cell (share divided by the cell's share of the pool). Faceted by configuration.

**Wording rule (locked).** The text says the best waves "concentrate in the favourable corner" only if the median share inside the full-pool-fit favourable corner exceeds 0.5 across the 78 pools; otherwise it reports the share and says the best waves "are spread across classes".

---

## S1-9. Tie-break regeneration of Blocks A and B [QA]

**Design.** Re-run `run_corner_block` (Block A), `run_policy_block` (Block B), and the P7 ablation with the current simulator, identical seeds and code paths, writing to `mvs_v0_5_phase5_blockA_tiebreakfix.csv`, `..._blockB_tiebreakfix.csv`, `..._ablation_P7_tiebreakfix.csv`. Analyse them with the unchanged analysis scripts, writing to `*_tiebreakfix.json` (the stored JSONs are not touched). This completes B-14, which regenerated Block C only.

**Reporting rule (locked before running).**
1. The verdicts of record are those computed from the stored artefacts.
2. The regenerated gate counts and cell values are reported beside them in the registration appendix, with the B-14 exposure statistic (15.6% of elevator requests faced an availability tie, 5.1% a tie between units on different floors).
3. If a regenerated gate count differs from the stored one, the manuscript states both counts in the main text next to the verdict, with the direction of the change. If a verdict tier would differ, the main text says so explicitly and explains that the preregistered analysis was run on the stored artefact.
4. Headline numbers in the text come from the stored artefacts; regenerated values appear as a robustness column.

**Prior exposure.** B-14 showed identical Block C gate verdicts before and after the fix and an unchanged smoke slice of Block A. Blocks A and B at full scale have not been regenerated.

---

## S1-12. B-5 cross-check rerun under the corrected DES-M2 boarding rule [QA]

**Background.** While modularizing the B-5 engine for Study 2 (`src/des_evaluator.py`, 2026-09-26), the assistant found that B-5's service pass boarded requests only onto trips opened before the pass, so two matching requests served in the same pass while two cars were free rode separately. The M2 rule of Section 3 (and the closed-form evaluator) boards first. DES-M1 is unaffected. With `b5_compat=True` the new module reproduces B-5 exactly (800/800 toy cases); in the module's self-test (seed 424,244) the corrected rule changes 73 of 400 DES-M2 cases and 0 of 400 DES-M1 cases. No Phase 5 wave has been run under the corrected rule.

**Design.** Rerun the B-5 protocol exactly (configurations 1, 7, 11; size 16; Block C candidate pools `_seed(cid, 99, 16)`; the random arm for all three and the four corners for configuration 7; 200 waves per arm; closed-form M1, M2 and DES-M1, DES-M2) with `des_makespan(..., b5_compat=False)`, writing `prototype/results/v0_5_phase5_S1-12_b5_boardfirst.json` (general rule 2; the stored B-5 output is not touched). The output records the SHA-256 of this registration, of the stored B-5 output, and the code tree hash. The closed-form side uses the current simulator.

**Reporting rule (locked before running).** Identical to S1-9: the B-5 verdict of record stays (Spearman gate not met; DES ordering 0.98 to 1.00; "faithful ordinal proxy" not supported). The rerun values (Spearman ρ per configuration, DES ordering rate, mean DES-M2 against closed-form M2, the configuration 7 DES decomposition) are reported beside the stored ones; if the gate outcome would differ, the main text says so next to the verdict.

---

## S1-11. Complementary fractions, closed-form descriptive layer [NS; only if D-D1 is signed]

**Design.** The two 1/3 fractions not run in Phase 5: demand index = (F index + A index + j) mod 3 for j = 1, 2, crossed with E ∈ {1, 2}: 36 configurations with ids 18 to 53 (id = 18·j + the position the configuration would have in `make_config_array()`). Order pools: `generate_pool(demand, F, 600, seed = SEED_BASE + id)`, as in Phase 5. Candidate pools: `build_candidates(pool, n, 3000, Random(_seed(id, MODEL_IDX[m], n)))` for both seed models m, n ∈ {8, 30}. Every candidate evaluated under M1 and M2 (144 pools × 3,000 × 2 = 864,000 runs); each pool is summarised under its own model, as in Block A. The 18 Phase 5 configurations are re-enumerated in the same run (deterministic, identical to S1-2), so the table covers the full 54-configuration factorial.

**Quantities.** Per pool, the S1-2 quantities (favourable corner from the full-pool fit). Across the 54 configurations, separately for each (model, size) slice (M1 or M2 × n = 8 or 30): main effects of F, |A|, E, and demand on the log median makespan and on GAP (balanced full-factorial contrasts; descriptive, no tests); the two-factor interaction table for F × demand. The script refuses to run unless the S1-11 box below is ticked.

**Reporting rule (locked).** Reported as "closed-form descriptive layer on the full factorial". It does not re-estimate any preregistered quantity and is not compared with the locked verdicts. The limitation sentence on the confounding of F with |A| and demand in the Phase 5 fraction stays in the paper.

---

## Sign-off

```
Author: ____________________  Date: ____________
```
To sign: in one edit, tick the S1-11 box below, set `author_signoff` to "SIGNED (<name>, <date>)", and replace the `status` line; then run `make_manifest.py SIGNED`. The file's SHA-256 is recorded in `MANIFEST_SIGNED.json` and on OSF, never in this file, and the file is not edited afterwards.
```
S1-11 included (D-D1 signed):  [ ] yes  [ ] no
```
