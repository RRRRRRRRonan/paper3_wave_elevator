---
title: "Phase 6 registered protocol, Study 2: the generate, screen, and verify release procedure"
parent: "paper_draft/phase5_scaleup_preregistration.md (LOCKED 2026-05-19); revision_2026-07-08/amendments/ (six signed amendments); revision_2026-09-24/readiness_assessment_CIE_IJPR_2026-09-26.md Part 2 v2; revision_2026-09-26_ijpr/STORY_CONTRACT.md"
date: 2026-09-26
status: "DRAFT, prepared overnight by the assistant at the author's request; NOT signed; NOTHING executed. No Study 2 test pool has been generated, and no quantity defined here has been computed on any pool."
author_signoff: "PENDING. Required before any Study 2 driver runs (enforced by src/registration_guard.py)."
lock_stages: "L1 = everything in this file (design, arms, metrics, gates, analysis, contingencies), locked at signature. L2 = the P11 hyperparameters and the calibrated-case parameter table, fixed by the rules in §6.4 and §11.3 before any test pool is generated, and recorded as a dated addendum (Appendix L2) appended to this file."
evidence_tag: "[NS] P6-<item>"
---

# Phase 6 registered protocol: Study 2

## 中文摘要（供作者审阅；正式条款以英文为准）

- **研究什么：** 研究二评价"生成、筛选、验证"（GSV）释放流程：生成候选（随机池 + P10 重排版本 + P11 构造候选），在同乘模型 M2 下闭式筛选，前 k 名交给事件驱动仿真（DES）验证，释放 DES 最优者。
- **怎么做：** 18 个配置 × 每配置 8 个独立订单池 × 波次规模 {8, 16, 30} = 432 个决策；全部候选在 M1、M2、DES-M1、DES-M2 下评价；另有集合对序列分解、热启动五波链、文献校准案例、运行时间。
- **门槛：** G1 序列杠杆、G2 与节约法 P8 的比较、G2′ 与同预算局部搜索 P7-matched 的比较、G3 筛选短名单、G4 构造候选上的排序率、G5 热启动、G6 集合对序列、G7 案例（无门槛）、G8 保真阶梯。每个门槛只决定措辞档位，不触发重跑或调参。
- **核对时新加的三处（请重点看）：** (1) Phase 5 里局部搜索 P7 已在 12/12 格胜过 P8，所以 G2′ 改用"同预算"的 P7-matched（同样 6,200 次闭式评估 + 20 次 DES 验证），不再和单次 40 步搜索的中位数比；(2) 生成器消融（只用 R、R+P10、R+P11）从同一次全枚举里直接算，不增加仿真，也不改变主结论口径（主结论固定为 GSV(20) 在 G 上）；(3) 订单池种子不能用"S_p + 配置号"，否则第 c 个配置的第 p+1 个池与第 c+1 个配置的第 p 个池相同（配置 2j 与 2j+1 只差 E），已改为 Phase 5 的混合公式。
- **你要确认的：** §7 各门槛数值与理由；§2 事先已知结果的披露是否完整；§11 案例（取决于 D-K）；§14 的应急条款；§5.4 的调参规则。
- **锁定分两步：** 签字即锁定本文件全部内容（L1）；第 4 周按 §6.4 的规则只用训练池锁定 P11 超参数和案例参数表（L2），然后才生成测试池种子。

---

## 1. Purpose and questions

Study 2 evaluates a release procedure for the single-wave composition problem of Section 3. It addresses:

- **RQ1 (method part).** How much of the makespan variation among candidate waves comes from the processing sequence rather than the order set, and how much does a sequence-aware re-ordering at release recover?
- **RQ2 (method part).** Does screening under the throughput abstraction M1 cost more decision loss than screening under co-occupancy M2, and does the M1 ≤ M2 ordering persist on candidates that are constructed to create co-rides?
- **RQ3.** How much of the value of the candidate pool does the generate, screen, and verify (GSV) procedure capture under event-driven execution, how large a shortlist does verification need, and do the results survive consecutive waves and a literature-calibrated case?

Study 2 does not re-judge any Study 1 verdict and does not use any Study 1 result as confirmation.

## 2. Prior exposure disclosure

The following results relevant to Study 2 were seen by the authors before this protocol was written. They inform the design and thresholds; they are disclosed so that readers can judge which Study 2 outcomes were foreseeable.

| Seen result | Source | Relevance |
|---|---|---|
| Phase 5 Blocks A, B, C under the closed-form evaluators (M1, M2, M3), including P0 to P6 medians on the 12 Block B cells (grand means: P0 317.6, P2 299.2, P5 303.6) | `prototype/results/v0_5_phase5_*.json` [PR-C]/[AM1] | Baseline levels for G2 |
| P8 savings heuristic beats P5 in 10/12 Block B cells (grand mean 288.4 versus 303.6); P9 beats P5 in 9/12 cells and beats the best corner (realized) in 7/12 | `b2_b3_benchmarks.json#B3`, `amendC1_p9_spoplus.json` [NS] | Strength of the G2 comparators |
| **P7 local search (median of 200 runs of 40 iterations under M2) is below P8 in 12/12 Block B cells (grand mean 224.6 versus 288.4)** | `b2_b3_benchmarks.json#B3` [AM1]/[NS] | **G2′: local search is known to be far stronger than every class rule. G2′ therefore uses a budget-matched local search (P7-matched, §4), not the Phase 5 single-run median** |
| Pool optimum for 2 cells (config 0, size 8, E = 1: optimum 70 versus pool median 165; config 1, size 8: optimum 38 versus P7 56, +47.4%, and P5 94, +147%) | `b2_b3_benchmarks.json#B2` [NS] | Scale of possible gains |
| **Clustered operational dispatch (`policy="cluster"`, pop_cluster) lowers the closed-form M2 median by 10.2% on the Φ-corner arm (12/12 cells above 1%) and 10.5% on the random arm (11/12)** | `v0_5_phase5_supp.json#Supp1_H1_at_scale` [AM2] | **G1: P10 applies a related grouping at release time. Under the closed-form evaluator a similar gain is therefore expected; G1 is evaluated under DES-M2, and the closed-form value is descriptive and flagged as prior-exposed** |
| DES cross-check on configs 1, 7, 11 (uniform, clustered, uniform; size 16; random arm): per-wave DES dominance 0.98 to 1.00; Spearman ρ between closed-form and DES makespans 0.45 to 0.68; mean DES-M2 makespans 22.8% to 37.3% below closed-form M2 | `b5_des_crossvalidation.json` [NS] | G3 and G8: closed-form rankings are known to be imperfect proxies for DES rankings over whole pools; nothing is known about the top of the distribution. No diurnal configuration was in the cross-check; ready times were exercised only by the single-AMR self-tests (see §12 item 2) |
| Informal audit numbers from 2026-09-25 (unregistered, [EXP]): median per-wave (M2 − M1)/M1 = 41% on the tie-break-fixed Block C CSV; Φ-corner advantage over random in the Supp-1 data 7.47% (FIFO) and 7.12% (cluster) as means of per-cell ratios (4.86% and 4.25% as ratios of grand means); candidate-cluster bootstrap D1-d 52 to 55/72; corner-choice stability 0.43 to 0.78 in 5/6 configurations | readiness assessment Part 1 [EXP] | G4 expectations on random candidates; G1 context. These numbers are registered for re-analysis in Study 1 (S1-1, S1-6, S1-7, TH-2) and are not results of either study |

| Code self-tests (2026-09-26): the drivers were run end to end on two toy configurations that are not in the design (901: F = 5, 5 AMRs, E = 2, uniform; 902: F = 3, 15 AMRs, E = 1, diurnal), toy seeds (base 424,242), K = 120, K′ = 20, untuned P11 weights (2, 1, 0.5). The assistant saw the outputs while debugging, including the M1 ≤ M2 share: 147 of 160 toy P11 candidates (92%) against 955 of 960 toy random candidates, and the tier labels printed by the analysis self-test on 8 toy decisions (G1 middle, G2 upper, G2′ upper, G3 upper, G4 middle, G5 upper, G6 middle, G8 middle). With K = 120, K′ = 20, and configurations outside the design, these carry no information about the registered runs | scratch directory of the overnight job, not archived as results | G4: a toy signal that the ordering may weaken on constructed candidates. No threshold or wording was changed after these runs; all gates were written before them. Two clarifications were written after the first toy run: G6 averages the cell values (one toy decision's share, 0.59, had been printed), and G3 uses k* under the headline screening key of §5.5 |

Not computed on any registered pool before signature: anything involving P10, P11, GSV, full-pool DES enumeration, set-versus-sequence variance, warm-start chains, or the calibrated case.

## 3. Design

### 3.1 Configurations
The 18 Phase 5 configurations (`prototype/results/configs_v0_5.json`, unchanged; generated by `make_config_array()`): F ∈ {3, 5, 8}, |A| ∈ {5, 15, 30}, E ∈ {1, 2}, demand ∈ {uniform, clustered, diurnal} as a one-third fraction; c = 2. Calibrated case configurations 100 and 101 are defined in §11.

### 3.2 Order pools and seeds
- **Derived seeds:** `seed6(base, config_id, stream, size)` = the Phase 5 harness `_seed()` formula with `base` in place of `SEED_BASE`: base + config_id · 100003 + (stream + 1) · 37 + (size + 1) · 37², modulo 2³¹. Streams: 89 order pool (size argument 0); 90 random candidate pool; 91 set-versus-sequence candidate draw; 92 permutations; 93 P11 generation; 94 P5/P9 training sample; 95 P7 runs; 96 R-verify draws; 98 tie-breaking permutation; 100 + s warm-start step s (s = 1, …, 5).
- **Test pools:** 8 independent order pools per configuration. Base seeds S_p = 20260900 + p for p = 1, …, 8. Order pool: `generate_pool(demand, F, 600, seed = seed6(S_p, config_id, 89, 0), **DEMAND_PARAMS[demand])`. (The simpler rule S_p + config_id was rejected: it gives the same seed to pool p + 1 of configuration c and pool p of configuration c + 1, and configurations 2j and 2j + 1 differ only in E, so the two pools would be identical.)
- **Training pools (P11 tuning only):** 2 per configuration, base seeds S_t = 20260950 + t for t = 1, 2, same generator and streams. Training pools are never used for any Study 2 result.
- **Bootstrap seed:** 20260926.
- **Ties.** Every ranking in this protocol (screening, verification, optima, P8 and P9 scores) breaks ties by a fixed uniformly random permutation of the decision's candidates (stream 98), so no candidate source is favoured by its index. Tie counts are reported.
- Seed ranges are disjoint from Phase 5 (20260519 + id), Amendments A and B (20260708, 20260709), and Amendment F (20260801 to 20260808).
- **Test-pool seeds are not used, and no test pool is generated, before Appendix L2 is appended and dated.**

### 3.3 Wave sizes
n ∈ {8, 16, 30}. Warm-start chains use n = 16 only.

### 3.4 Candidate sets per decision
A **decision** is a triple (configuration, test pool, size): 18 × 8 × 3 = 432 decisions.
- R: K = 3,000 random candidates, `build_candidates(pool, n, 3000, Random(seed6(S_p, cid, 90, n)))`; the processing sequence is the recorded draw order (Section 3.2.3).
- P10(R): the P10 re-ordering (§5.1) of every candidate in R (3,000 derived candidates; same order sets, new sequences).
- P11: K' = 200 constructed candidates (§5.3).
- **G = R ∪ P10(R) ∪ P11** (6,200 candidates; duplicates of identical (set, sequence) pairs are kept and counted).

### 3.5 Evaluators
- **M1, M2:** production `simulate_wave` (tie-break fixed on 2026-09-11), `policy="fifo"`, deterministic.
- **DES-M1, DES-M2:** the B-5 event-driven engine (heapq; concurrent AMRs claim orders in sequence and wait for each order's ready time; elevator queue served in FIFO order by request time), modularized in `src/des_evaluator.py` with its self-tests (§12). Deterministic. Phase constants are parameters with the production defaults (5 s per floor, 2 s load, 2 s unload, 5 s AMR service).
- **DES-M2 boarding rule (a correction to B-5, found while modularizing on 2026-09-26, before any Study 2 run).** Each queued request, in FIFO order, first boards an open trip with the same (source, destination), free capacity, and an open loading window, including a trip dispatched earlier in the same service pass, and only otherwise takes the earliest-free unit. This is the M2 rule of Section 3 and of the closed-form evaluator. The B-5 engine boarded only onto trips opened before the service pass, so two matching requests served in the same pass while two cars were free rode separately (hand-computed case: makespan 43 under B-5 against 24 under the M2 rule and the closed form). The difference affects DES-M2 only (DES-M1 is identical) and changed the makespan in 104 of 600 randomized toy waves. B-5's semantics remain available as `b5_compat=True`; Study 2 uses the corrected rule throughout, and the B-5 numbers in §2 were produced under the old rule.
- M3 is not used in Study 2.
- Every candidate in G is evaluated under all four evaluators (full enumeration).

### 3.6 Fixed dispatch
The dispatch rule is FIFO over the release sequence in all arms. `policy="cluster"` appears only as the Supp-1 reference row next to G1.

## 4. Arms

| Arm | Output per decision | Evaluator access before release | Budget per decision |
|---|---|---|---|
| P0 random | distribution: uniform over R; reported as its DES-M2 median | none | 0 |
| P2 cardinality rule | distribution: uniform over the candidates of R whose cross-floor count is at or below its 25% quantile (Phase 5 definition, ties included) | none | 0 |
| P5 Φ-corner rule | distribution: uniform over the favourable corner of R; the corner is chosen by the Phase 5 `fit_predictors` protocol from a 200-draw M2 training sample of R (with replacement, stream 94) | 200 M2 (training) | 200 M2 |
| P8-200 | distribution: the 200 lowest P8 scores in R (Block B definition) | none | 0 |
| P8-1 | single wave: the lowest P8 score in R | none | 0 |
| P9-200, P9-1 | as P8, ranked by the AMEND-C SPO+ predictor (standardized C, I, T; k_train 13; step 0.05; 300 iterations) trained on the stream-94 sample | 200 M2 (training) | 200 M2 |
| P7-run | Phase 5 definition: 8 local-search runs, each 40 iterations from a random start over the 600-order pool (at most 41 M2 evaluations per run); distribution over the 8 end-point waves; descriptive, for continuity with Phase 5. These are the first 8 runs of the P7-matched search (same stream 95, identical to 8 sequential calls of `optimize_wave_localsearch`) | M2 | ≤ 328 M2 |
| **P7-matched** (comparator for G2′) | multi-start local search (same move, stream 95) run until 6,200 M2 evaluations are spent (the last run is truncated); the 20 lowest-M2 distinct end-point waves (ties by discovery order) are evaluated under DES-M2 and the DES-M2-best is released. Equivalently, GSV with local-search end-points as the generator | M2; DES-M2 on 20 | 6,200 M2 + 20 DES |
| P0+P10, P5+P10, P8+P10 | the same distributions with every candidate replaced by its P10 re-ordering (P8+P10 re-orders the P8-200 set) | as the base arm | as the base arm |
| P0+P10g | P0 with every candidate replaced by its P10g re-ordering (grouping without readiness or chaining); evaluated under M2 and DES-M2 outside G; descriptive, for the chaining increment | none | 0 |
| P11-1 | single wave: the P11 candidate with the lowest M2 makespan | M2 | 200 M2 |
| **GSV(k)**, k ∈ {1, 5, 10, 20, 50, 100, 6200} | single wave: screen G by M2, evaluate the top k under DES-M2, release the DES-M2-best (§5.5) | M2 on G; DES-M2 on k | 6,200 M2 + k DES |
| R-verify(k), same k grid (k ≤ 3,000) | single wave: DES-M2-best among k candidates drawn uniformly without replacement from R (stream 96) | DES-M2 on k | k DES |
| Generator ablations GSV_R(k), GSV_R+P10(k), GSV_R+P11(k) | GSV with G replaced by R, by R ∪ P10(R), or by R ∪ P11 | as GSV on the smaller set | 3,000, 6,000, or 3,200 M2 + k DES |

Anchors: the M2 optimum over G (= GSV(1)), the DES-M2 optimum over G (= GSV(6200)), and the DES-M2 optimum over R.

For distribution arms, the reported value is the median DES-M2 makespan over the arm's distribution (exact, because every candidate is enumerated). For single-wave arms it is the DES-M2 makespan of the released wave. Every arm is also reported under M2 so that Study 2 values can be placed next to Study 1.

Budget column: the evaluator calls a deployment of the arm would need before release. The study itself enumerates every candidate under every evaluator for measurement; that enumeration is not part of any arm's budget. The generator ablations and GSV at all k are computed from the same enumeration, so they add no evaluator runs and no forking: the headline procedure is GSV(20) on G, fixed here.

## 5. Procedure specifications

### 5.1 P10 sequence-aware re-ordering (deterministic)
Input: a wave with orders (s_o, d_o, r_o) and recorded sequence π; car capacity c; initial floor f⁰ = 1.
1. Split orders into cross-floor groups by (s, d) and same-floor orders (s = d). Within a group, order by ready time and then by position in π (with zero ready offsets this is the order of π; ordering by readiness first makes P10 idempotent, which a group kept in π order is not when ready times differ).
2. Split each group, in that order, into blocks of at most c consecutive orders; a block is a co-ride unit.
3. Block ready time = the largest r_o in the block.
4. Order the blocks: primary key ascending block ready time; among blocks with equal ready time, a chain rule starting at the current floor (initially f⁰): take the block whose source equals the current floor; if none, the block whose source is nearest to the current floor (smallest |s − current floor|); ties by larger block, then lexicographically smaller (s, d), then earliest position in π. After placing a block, the current floor becomes its destination.
5. Insert each same-floor order immediately after the first placed block whose destination equals its floor and whose ready time does not exceed the order's ready time; otherwise append at the end, ordered by ready time and then π. Several same-floor orders attached to one block follow that block in the order (ready time, π).
6. **P10g** (grouping only, used for the chaining increment): steps 1 to 3, blocks ordered by ready time and then by the earliest position in π; same-floor orders kept at their π positions.

With all ready offsets zero (uniform and clustered demand), step 4 reduces to pure chaining; with diurnal ready times it reduces mostly to ordering blocks by readiness. This is a registered design choice; its effect by demand pattern is reported.

### 5.2 Order set of P10 candidates
P10 never changes the order set; C, I, T are therefore unchanged, and corner membership is inherited from R.

### 5.3 P11 co-ride-aware constructive generator
Input: order pool O, size n, capacity c, weights (α, β, γ), random stream.
1. Start with one cross-floor order drawn uniformly from O.
2. Until |W| = n, add the order o ∉ W with the highest score, ties broken uniformly at random:
   score(o) = α · 1[s_o ≠ d_o and m(s_o, d_o) is not a multiple of c] + β · 1[s_o equals the destination of an order in W, or d_o equals the source of an order in W] − γ · (number of floors in {s_o, d_o} not yet among the endpoint floors of W),
   where m(s, d) is the number of orders in W with source s and destination d. The first term rewards completing a partly filled co-ride block; with c = 2 it is 1 when W holds an odd number of orders with the same (s, d).
3. Apply P10 to the completed set to obtain the sequence (π = construction order).
4. Repeat with K' = 200 independent streams: candidate j (j = 0 to 199) uses `random.Random(seed6(base, config_id, 93, n) + 7919·(j + 1))`.
The generator does not use ready times; readiness enters through P10. Duplicated order sets among the 200 are kept and counted.

### 5.4 Stage L2 tuning rule for P11 (locked now, executed before test pools exist)
- Grid: α ∈ {1, 2, 4}, β ∈ {0.5, 1, 2}, γ ∈ {0, 0.5, 1} (27 triples).
- Data: the 2 training pools of every configuration and every size (18 × 2 × 3 = 108 training instances).
- For each triple and instance: generate 200 P11 candidates; evaluate under M2 only; score = 10th percentile of their M2 makespans divided by the M2 median of a 3,000-candidate random pool built from the same training pool (stream 90 with the training base).
- Selected triple = lowest mean score over the 108 instances; ties by the lexicographically smallest (α, β, γ).
- No DES is run in tuning. All 27 scores, the selected triple, the code hash, and the date are recorded in Appendix L2 before any test-pool seed is used.

### 5.5 GSV
For each decision: evaluate every candidate of G under M2; sort ascending (ties by the stream-98 permutation); take the top k; evaluate them under DES-M2; release the DES-M2-best (ties by the same permutation). If G4 falls in its middle or lower tier (§7), the screening key for candidates from P10(R) and P11 becomes max{M1, M2}; the headline GSV then uses that key, and the M2-key results are reported beside it (pre-commitment D-F).

## 6. Set-versus-sequence decomposition (S2-1)
For each decision: draw 200 candidates uniformly without replacement from R (stream 91); for each, evaluate the recorded sequence and 20 random permutations (stream 92) under M2 and DES-M2 (21 sequences per candidate). Sequence share s = σ²_within / (σ²_within + σ²_between) from a one-way random-effects decomposition over (candidate, sequence), with the ANOVA estimators σ²_within = MSW and σ²_between = max{0, (MSB − MSW)/21}. Report s per cell and per demand pattern.

## 7. Gates and wording ladders (locked at signature)

**Units.** Cell = (configuration, size), 54 cells; the cell value is the mean over its 8 test pools. Configuration-level values average the three sizes (18 units).

| Gate | Quantity | Upper tier | Middle tier | Lower tier |
|---|---|---|---|---|
| **G1 sequence lever** | relative reduction of the DES-M2 median of P0+P10 versus P0, mean over 54 cells, with sign agreement (share of cells with a reduction) | ≥ 7.5% and sign ≥ 75%: "re-ordering at release is a first-order lever under concurrent execution, of the same size as the closed-form gain of clustered dispatch" | 2.5% to 7.5%, or ≥ 7.5% with sign < 75%: "re-ordering at release gives a moderate reduction under concurrent execution" | < 2.5%: "under concurrent execution the release sequence is a small lever" |
| **G2 versus the savings heuristic** | share of cells where the cell mean of GSV(20) is below the cell mean of P8-best (per pool, the lower of the P8-200 median and P8-1, a choice that favours P8) | ≥ 75%: "outperforms the strongest simulator-free heuristic" | 50% to 75%: "comparable to the strongest simulator-free heuristic" | < 50%: "does not outperform the strongest simulator-free heuristic; reported as a boundary of the procedure" |
| **G2′ versus local search** | share of cells where the cell mean of GSV(20) is below the cell mean of P7-matched (same M2 and DES budgets) | ≥ 50%: "matches or beats a budget-matched local search" | 25% to 50%: "approaches a budget-matched local search" | < 25%: "a budget-matched local search remains stronger" |
| **G3 screening fidelity** | per decision k\* = smallest k in the grid with r(k) ≤ 2% (relative to the DES-M2 optimum over G); per cell the median k\* over pools | median k\* ≤ 20 in ≥ 80% of cells: "a shortlist of 20 suffices" | median k\* ≤ 50 in ≥ 80% of cells: "a shortlist of 50 suffices" | otherwise: "closed-form screening is not a reliable pre-filter at shortlist sizes up to 100" |
| **G4 ordering on constructed candidates** | share of P11 candidates (all decisions) with M1 ≤ M2 | ≥ 95%: "the ordering persists on candidates built to create co-rides" | 80% to 95%: "the ordering weakens on constructed candidates; screening uses max{M1, M2} for them" | < 80%: "the choice of elevator model matters once composition exploits co-occupancy" |
| **G5 warm start** | (a) share of warm-state candidate evaluations with M1 ≤ M2 at steps 2 to 5; (b) share of chain units (configuration × pool × release variant, 288 units) where the five-wave completion time of the GSV(20) chain is below the mean of the three P0 chains | (a) ≥ 95% and (b) ≥ 80%: "robust to warm starts" | one of (a), (b) met: "partially robust to warm starts" | neither: "single-wave results do not transfer to consecutive waves" |
| **G6 set versus sequence** | sequence share s under DES-M2, mean over the 54 cells (M2 descriptive) | > 0.5: "sequence dominates" | 0.2 to 0.5: "set and sequence both matter" | < 0.2: "the order set dominates" |
| **G7 calibrated case** | none | descriptive only | | |
| **G8 fidelity ladder** | share of cells with DL_M1 > DL_M2 | ≥ 75%: "screening with the throughput abstraction costs more than screening with co-occupancy" | 50% to 75%: "often costs more" | < 50%: "no systematic difference" |

Definitions: r(k) = (DES-M2 makespan of GSV(k) − DES-M2 optimum over G) / DES-M2 optimum over G. DL_m = (DES-M2 makespan of the evaluator-m optimum over G − DES-M2 optimum over G) / DES-M2 optimum over G, for m ∈ {M1, M2, DES-M1}; when several candidates tie at the evaluator-m minimum, the numerator uses their mean DES-M2 makespan (the expected value under random tie-breaking), and the number of tied candidates is reported.

Threshold rationale (fixed before any Study 2 result): G1's 7.5% and 2.5% are about three quarters and one quarter of the prior-exposed 10.2% closed-form gain of clustered dispatch; G3's 2% regret is roughly one loading plus one unloading phase (4 s) on the size-16 DES-M2 makespans of the B-5 cross-check (means 147 to 237 s); G4's and G5(a)'s 95% sit below the 98% to 100% per-wave ordering rates seen on random candidates; G2 and G8 use three quarters of cells as the upper tier, G2′ one half because the comparator is a search method with the same budget.

**No gate has a pass or fail consequence beyond its wording tier.** No tier triggers a rerun, a retune, a new arm, or a change of any other gate.

Descriptive companions reported with each gate (no tiers): G1 under M2 closed form (next to the Supp-1 value, flagged as prior-exposed), P5+P10 versus P5, P8+P10 versus P8-200, P10 versus P10g (chaining increment), results by demand pattern; G2 and G2′ with evaluator budgets; G3 with r(k) curves and k\* relative to the optimum over R; G4 on P10(R) and under DES-M1 ≤ DES-M2; G8 levels of DL_M2 and DL_DES-M1.

## 8. Statistical analysis
- Independent unit: the order pool. Cell-level 95% intervals by bootstrap over the 8 pools (B = 2,000, seed 20260926).
- Pairwise comparisons at configuration level (18 paired values, averaging sizes), Wilcoxon signed-rank, Holm correction within the family {GSV(20) versus P8-best, versus P7-matched, versus P5, versus R-verify(20); P0+P10 versus P0; P5+P10 versus P5}, α = 0.05. Per-size results reported as sensitivity.
- Every quantity is reported in seconds and as a percentage.

## 9. Warm-start chains (S2-7)
- Per (configuration, test pool, release variant): chains of 5 waves at n = 16 for arms P0 (3 replicate chains), P5 (3 replicate chains), and GSV(20) (1 chain). Chain randomness for arm a (0 = P0, 1 = P5, 2 = GSV) and replicate j at step s uses the seed seed6(S_p, config_id, 100 + s, 16) + 1000·a + 100·j.
- Step s draws a fresh 3,000-candidate random pool from the orders of the test pool not yet released by that chain. P0 releases a uniform draw from it. P5 releases a uniform draw from its favourable corner, using the corner already chosen for the same (configuration, pool) at size 16 in the single-wave study (no refit). GSV(20) adds the P10 re-orderings and 200 P11 candidates and applies §5.5 with every evaluation made after the chain's realized prefix.
- Release epochs: variant A, wave s + 1 is released when all previously released orders are complete; variant B, wave s + 1 is released at the previous release epoch plus half of the time from that epoch to the completion of all released orders (overlap). Completion is measured under DES-M2, the stand-in for execution, and the same epochs are used for every evaluator.
- Evaluation by concatenation: the released waves are concatenated in release order with absolute ready offsets and evaluated by the unchanged evaluators, so AMR and elevator states carry over exactly (G0 item 5). Metrics: the five-wave completion time (G5(b)) and, descriptively, the incremental completion C(prefix s + 1) − C(prefix s).
- G5(a) uses 300 candidates drawn uniformly from the GSV chain's step pool at each of steps 2 to 5; each candidate is appended to that chain's realized prefix and the whole concatenation is evaluated under M1 and under M2 (the ordering from the common cold start at time 0, applied to the longer sequence). The same comparison on increments (completion with the candidate minus completion of the prefix, per evaluator) is reported descriptively.
- Implementation streams (fixed): P11 candidate j at step s uses the chain seed + 1 + 7919·(j + 1); ties use the chain seed + 2; the G5(a) sample uses the chain seed + 3.

## 10. Runtime and scalability (S2-9)
Configurations {1, 7, 17}, one test pool each, K ∈ {1,000, 3,000, 10,000}, n ∈ {8, 16, 30, 60}: wall-clock of generation, screening, and verification per decision, and per candidate. Descriptive.

## 11. Literature-calibrated case (S2-8; depends on decision D-K)

### 11.1 Scenario
Configuration 100: F = 3, |A| = 30, E = 2, c = 2. Configuration 101: F = 3, |A| = 30, E = 3, c = 2. Three-story robotic warehouses with two or three freight elevators are documented in public cases (for example the Quicktron and LH three-floor site; Prologis Georgetown, three floors with three freight elevators).

### 11.2 Order flow
Public order data (UCI Online Retail II, CC BY 4.0). Each invoice line becomes one load. Outbound loads (share 0.8) move from the storage floor of the stock code to floor 1 (packing and shipping); inbound replenishment loads (share 0.2) move from floor 1 to the storage floor. Storage floor = 2 + (SHA-256 of the stock code, read as an integer, modulo (F − 1)). Direction is assigned per line by a Bernoulli(0.8) draw on the same stream. Each case test pool is 600 lines drawn without replacement from one trading day with at least 600 lines, the day and the lines drawn on stream 89. Ready offsets: zero in the primary run; in a sensitivity run, the invoice-time rank of each line within its pool is scaled linearly to [0, 50] s (the Phase 5 diurnal horizon). These mappings are researcher assumptions and are stated as such in the paper.

### 11.3 Parameter table (Stage L2)
Travel time per floor, loading and unloading time, and AMR service time are set to the midpoints of the ranges documented in public freight-elevator specifications (KONE and Schindler product data; Peters round-trip-time decomposition) and fixed in Appendix L2 with sources before any case pool is generated. Sensitivity runs at both ends of each range are reported.

### 11.4 Runs and reporting
8 test pools per case configuration (pool seeds seed6(S_p, 100, 89, 0) and seed6(S_p, 101, 89, 0)), sizes {8, 16, 30}, all arms of §4, all evaluators with the case parameters. Descriptive (G7). Wording: "parameters set within publicly documented ranges"; never "calibrated to a facility".

## 12. Code freeze and validation (G0; before Appendix L2)
1. `python -m src.simulator` passes all hand-computed targets.
2. `src/des_evaluator.py` self-tests pass: a single order equals the closed-form value exactly; single-AMR waves (with and without ready times) equal the closed-form value exactly; the B-5 self-test battery passes; hand-computed multi-AMR cases pass (two AMRs sharing one M2 car; a ready time that delays a claim; M1 slots serving in parallel; the boarding-rule case of §3.5, 24 versus 43); with `b5_compat=True` the module reproduces the B-5 engine exactly on randomized toy waves.
3. `simulate_wave` with the new optional timing arguments at their defaults reproduces the previous outputs exactly on randomized toy waves (non-registered seeds).
4. P10, P10g, and P11 unit tests on hand-built instances pass; P10 is idempotent on its own output; P11 returns n distinct orders.
5. Concatenation equivalence: a one-wave chain equals `simulate_wave` exactly.
6. The code state is hashed (git commit or a tree hash) and the hash is written into Appendix L2.

## 13. Outputs and reporting commitments
- Results (written by `src/experiments_phase6.py` and `src/analysis_phase6.py`): `prototype/results/v0_6_phase6_L2_tuning.json` (Stage L2), `v0_6_phase6_main.json` (every decision: all arms, GSV at every k, ablations, anchors, ladder, ordering counts, set-versus-sequence), `v0_6_phase6_warmstart.json`, `v0_6_phase6_runtime.json`, `v0_6_case_*.json`, and `v0_6_phase6_gates.json` (G1 to G8 with tiers and the descriptive companions); raw candidate rows in `results/raw/mvs_v0_6_phase6_candidates.csv.gz` (configuration, pool base, size, candidate index, source R/P10/P11, parent, M1, M2, DES-M1, DES-M2, C, I, T, cross-floor count).
- Every file records its generation time, code hash, and the SHA-256 of this protocol.
- All arms, configurations, sizes, and gates are reported in full, favourable or not. No result is dropped for being unfavourable.
- Study 2 is labelled [NS] P6-<item> throughout the manuscript and never presented as confirming Study 1.

## 14. Contingencies and deviations
- **P9 (decision D-L).** If P9 cannot run at Study 2 scale by the code freeze, it is removed before any Study 2 result is computed, and the removal is recorded in the deviation log with its reason.
- **Calibrated case (decision D-K).** If D-K is not signed or the data cannot be obtained under its license, §11 is dropped before any Study 2 result is computed, and the drop is recorded.
- **Runtime.** Measured on toy waves (2026-09-26): about 0.3 ms per DES-M2 run at n = 16 and 0.75 ms at n = 30, so full enumeration is expected to take hours, not days. If the timing of the first configuration nevertheless projects a total wall-clock above 48 hours, full DES enumeration of G is replaced by DES evaluation of a pre-specified subset (the top 500 of G by M2 plus 500 candidates drawn uniformly from G), and G3, G8, and the anchors are then defined on that subset. The switch is recorded before the run continues.
- **Bugs.** A bug found after runs is fixed, the whole affected block is rerun, and both versions are reported.
- **Deviation log.** Every deviation from this protocol is logged with date, reason, and effect in `revision_2026-09-26_ijpr/EXECUTION-LOG.md` and summarized in the manuscript's registration appendix.

## 15. What Study 2 will not do
It will not change any Phase 5 file, verdict, or configuration; use M3; test capacity interventions; add arms after signature; tune anything on test pools; or present any Study 2 quantity as confirming a Study 1 verdict.

## 16. Sign-off

```
Design, arms, metrics, gates, and analysis (L1) reviewed and locked:  [ ]  ______________  date ________
Decisions D-K (case) and D-L (P9) as recorded in 01_DECISIONS_TO_SIGN:  [ ]  ______________  date ________
SHA-256 of this file at signature:  ________________________________________________
OSF registration identifier (decision D-J):  _______________________
```

---

## Appendix L2 — Stage L2 addendum (to be appended and dated in week 4, before any test pool exists)

```
L2 status: PENDING   (change to "L2 status: SIGNED (<name>, <date>)" when complete; src/registration_guard.py reads this line before any test pool is generated)
Date:
Code hash (G0 item 6):
G0 checks 1 to 5: pass / fail (with log reference)
P11 tuning: 27 scores (table), selected (alpha, beta, gamma):
Case parameter table (travel per floor, load, unload, service; value, range, source):
Confirmation that no test-pool seed has been used before this date:
Signature:
```
