---
title: "Phase 6 registered protocol, Study 2: the generate, screen, and verify release procedure"
parent: "paper_draft/phase5_scaleup_preregistration.md (LOCKED 2026-05-19); revision_2026-07-08/amendments/ (six signed amendments); revision_2026-09-24/readiness_assessment_CIE_IJPR_2026-09-26.md Part 2 v2; revision_2026-09-26_ijpr/STORY_CONTRACT.md"
date: 2026-09-26
status: "SIGNED 2026-09-26 (L1); nothing executed as of 2026-09-26. D-M signed as option (b), identical to §7.1, so no §7 or code edit was needed. Prepared as draft 3 overnight at the author's request, revised after two independent reviews and a pre-signing audit (revision_2026-09-26_ijpr/helper_reports/), and signed after the author's review."
author_signoff: "SIGNED (Shiyue Hu, 2026-09-26). Authorization given by explicit author instruction in the 2026-09-26 working session, after the author's review of the pre-signing audit and its diffs; the assistant entered the signature at that instruction."
lock_stages: "L1 = this file. Its bytes are frozen at signature; the SHA-256 is recorded outside the file, in revision_2026-09-26_ijpr/archive_package/MANIFEST_SIGNED.json and on OSF, and src/registration_guard.py stops every registered run if the bytes change. L2 = paper_draft/phase6_protocol_L2_addendum.md (P11 weights, case parameters, code-freeze hash, OSF id), filled by the rules of §5.4, §11.3, and §12 before any test pool exists, signed separately, and pinned in MANIFEST_SIGNED_L2.json."
evidence_tag: "[NS] P6-<item>"
---

# Phase 6 registered protocol: Study 2

## 中文摘要（供作者审阅；正式条款以英文为准）

- **研究什么：** 研究二评价"生成、筛选、验证"（GSV）释放流程：生成候选（随机池 R、R 的 P10 重排版本、P11 构造候选），在同乘模型 M2 下闭式筛选，前 k 个**不同的**候选序列交给事件驱动仿真 DES-M2 验证，释放 DES 最优者。
- **规模：** 18 个配置 × 8 个独立测试订单池 × 波次规模 {8, 16, 30} = 432 个决策；全部候选在 M1、M2、DES-M1、DES-M2 下评价；另有集合对序列分解、热启动五波链、文献校准案例、运行时间。
- **门槛（只决定措辞档位）：** G1 序列杠杆；G2 与"P8 前 20 名 + 同样 20 次 DES 验证"（P8-verify）比较；G2′ 与同预算局部搜索 P7-matched 比较；G3 筛选短名单；G4 构造候选上的排序率；G5 热启动（保留单波优势的比例）；G6 集合对序列；G7 案例（无门槛）；G8 保真阶梯。
- **两轮独立审查后改了什么（同一夜、签字前、未见任何登记结果）：** (1) 签字后本文件一字不改，哈希记在文件外，OSF 编号与 L2 内容移到单独的 L2 附录并单独签字，守卫会核对哈希（换行符不影响哈希；签字后改动再重新登记也会被拦下）；(2) P7-matched 也能用 P10 重排，所有短名单按"序列签名"去重；(3) 新增 §7.3 执行稳健性检验（带相位噪声的 DES 与 B-5 语义），G1 在同一子样本上与无噪声基线比较；(4) G2 的对照改为 P8-verify(20)（同样的 DES 预算）；(5) G5(b) 改为"热启动下保留了多少单波优势"；(6) 热启动使用 G4 决定的筛选键；(7) G3 容差：第 1 稿 2%，第 2 稿 max{2%, 4 秒}（审查发现在真实最优值量级上相当于 3.6% 到 10.5%，过松），现为 max{2%, 1 秒}，签字时由你在 2% 与此之间选定（D-M）；(8) 这些门槛定义的改动都发生在看过玩具结果之后，§2 已逐条列明触发原因。
- **你要确认的：** §2 披露是否完整；§4 的对照与预算；§7 各门槛数值、措辞与理由；§7.3 稳健性规则；§11 案例（取决于 D-K）；§14 应急条款。

---

## 1. Purpose and questions

Study 2 evaluates a release procedure for the single-wave composition problem of Section 3. It addresses:

- **RQ1 (method part).** How much of the makespan variation among candidate waves comes from the processing sequence rather than the order set, and how much does a sequence-aware re-ordering at release recover?
- **RQ2 (method part).** Does selecting under the throughput abstraction M1 cost more decision loss than selecting under co-occupancy M2, and does the M1 ≤ M2 ordering persist on candidates constructed to create co-rides?
- **RQ3.** How much of the value of the candidate pool does the generate, screen, and verify (GSV) procedure capture under event-driven execution, how large a shortlist does verification need, and do the results survive consecutive waves, an independent execution check, and a literature-calibrated case?

Study 2 does not re-judge any Study 1 verdict and does not use any Study 1 result as confirmation.

### 1.1 Item map (used by STORY_CONTRACT.md)

| Item | Content | Where |
|---|---|---|
| S2-1 | Set-versus-sequence decomposition | §6, G6 |
| S2-2 | Sequence lever of P10 | §5.1, G1 |
| S2-3 | GSV main comparison | §4, §5.5, G2, G2′ |
| S2-4 | Screening shortlist and regret | G3 |
| S2-5 | Ordering on constructed candidates | G4 |
| S2-6 | Fidelity ladder | G8 |
| S2-7 | Warm start | §9, G5 |
| S2-8 | Literature-calibrated case | §11, G7 |
| S2-9 | Runtime and scalability | §10 |
| S2-10 | Execution robustness | §7.3 |

## 2. Prior exposure disclosure

The following results relevant to Study 2 were seen by the authors before this protocol was signed. They inform the design and thresholds; they are disclosed so that readers can judge which Study 2 outcomes were foreseeable.

| Seen result | Source | Relevance |
|---|---|---|
| Phase 5 Blocks A, B, C under the closed-form evaluators (M1, M2, M3), including P0 to P6 medians on the 12 Block B cells (grand means: P0 317.6, P2 299.2, P5 303.6) | `prototype/results/v0_5_phase5_*.json` [PR-C]/[AM1] | Baseline levels |
| P8 savings heuristic beats P5 in 10/12 Block B cells (grand mean 288.4 versus 303.6); P9 beats P5 in 9/12 cells and beats the best corner (realized) in 7/12 | `revision_2026-07-08/tier2_analysis/outputs/b2_b3_benchmarks.json#B3`, `revision_2026-07-08/tier2_analysis/outputs/amendC1_p9_spoplus.json` [NS] | Strength of the heuristic comparators |
| **P7 local search (median of 200 runs of 40 iterations per cell under M2) is below P8 in 12/12 Block B cells (grand mean 224.6 versus 288.4)** | `revision_2026-07-08/tier2_analysis/outputs/b2_b3_benchmarks.json#B3` [AM1]/[NS] | **Local search is far stronger than every class rule, so G2′ uses a budget-matched local search (P7-matched, §4), not the Phase 5 run median** |
| Pool optimum for 2 cells (config 0, size 8, E = 1: optimum 70 versus pool median 165; config 1, size 8: optimum 38 versus P7 56, +47.4%, and P5 94, +147%) | `revision_2026-07-08/tier2_analysis/outputs/b2_b3_benchmarks.json#B2` [NS] | Scale of possible gains; any procedure with thousands of evaluator calls is expected to beat simulator-free class rules, which is why G2 compares at equal verification budget (P8-verify) |
| **Clustered operational dispatch (`policy="cluster"`, pop_cluster) lowers the closed-form M2 median by 10.2% on the Φ-corner arm (12/12 cells positive and above 1%) and 10.5% on the random arm (12/12 positive, 10/12 above 1%)** | `v0_5_phase5_supp.json#Supp1_H1_at_scale` [AM2] | **P10 applies a related grouping at release time. Under the closed-form evaluator a similar gain is therefore expected; G1 is evaluated under DES-M2, and the closed-form value is descriptive and flagged as prior-exposed** |
| DES cross-check on configs 1, 7, 11 (uniform, clustered, uniform; size 16; random arm): per-wave DES ordering 0.98 to 1.00; Spearman ρ between closed-form and DES makespans 0.45 to 0.68; mean DES-M2 makespans 22.8% to 37.3% below closed-form M2 (all under the B-5 boarding semantics, §3.5) | `revision_2026-07-08/tier2_analysis/outputs/b5_des_crossvalidation.json` [NS] | G3 and G8: closed-form rankings are imperfect proxies for DES rankings over whole pools; nothing is known about the top of the distribution. No diurnal configuration was in the cross-check; ready times were exercised only by single-AMR self-tests |
| Informal audit numbers from 2026-09-25 (unregistered, [EXP]): median per-wave (M2 − M1)/M1 = 41% on the tie-break-fixed Block C CSV; Φ-corner advantage over random in the Supp-1 data 7.47% (FIFO) and 7.12% (cluster) as means of per-cell ratios (4.86% and 4.25% as ratios of grand means); candidate-cluster bootstrap D1-d 52 to 55/72 and row-level 56 to 58/72 over seeds; corner-choice stability 0.43 to 0.78 in 5/6 configurations | readiness assessment Part 1 [EXP] | G4 expectations on random candidates; G1 context. Registered for re-analysis in Study 1 (S1-1, S1-6, S1-7, TH-2); results of neither study |
| Code self-tests (2026-09-26): the drivers were run end to end on two toy configurations outside the design (901: F = 5, 5 AMRs, E = 2, uniform; 902: F = 3, 15 AMRs, E = 1, diurnal), toy seeds (base 424,242), K = 120, K′ = 20, untuned P11 weights (2, 1, 0.5). The assistant saw, while debugging draft 1, the M1 ≤ M2 share of 147 of 160 toy P11 candidates (92%) against 955 of 960 toy random candidates, one toy set-versus-sequence share (0.59), and the tier labels of the draft-1 analysis self-test on 8 toy decisions (G1 middle, G2 upper, G2′ upper, G3 upper, G4 middle, G5 upper, G6 middle, G8 middle). An independent reviewer's toy check (seeds 555,xxx; K = 3,000; K′ = 200; weights (2, 1, 0.5)) found 9 to 15 distinct sequences among the M2 top 20 in 7 of 15 settings and as few as 32 distinct P11 sequences of 200. After the draft-2 fixes only structural checks (budgets, counts) were printed | job scratch folder; review report | These toy values carry no information about the registered runs (tiny K, configurations outside the design, draft-1 definitions). **Definitions changed after the toy runs had been seen, each triggered by an independent review rather than by a toy value:** G2 comparator (P8-best → P8-verify(20); stricter), G5(b) (five-wave completion against P0 → retention of the cold-start gain; stricter), G3 tolerance (2% in draft 1 → max{2%, 4 s / optimum} in draft 2 → max{2%, 1 s / optimum} in draft 3; see the next row), G1 and G8 wording, the de-duplication rule of §5.5, the §7.3 execution check, the G6 aggregation (mean over cells), the G3 key clarification, P7-matched receiving the P10 re-ordering operator inside its 6,200-evaluation budget (first review, item 2; stricter for GSV), G2′ counting ties as matches, at or below instead of the draft-1 below (second review, R2-9; looser for GSV; the toy G2′ label was already upper under the strict count), G5(a) sampling its 300 candidates from the random part R_s rather than from the whole candidate set that the draft-1 code sampled (first review, item 5), and the warm-start chains screening by the G4-decided headline key instead of always by M2 (first review, item 5). The author chooses at signing between the draft-1 G3 tolerance (2%) and the draft-3 one (decision D-M) |
| Second reviewer's toy-shaped runs (2026-09-26; toy seeds 777,xxx; toy configurations shaped like configs 0, 1, 9, 17; full K = 3,000): DES-M2 optimum over G of 38 to 111 s at n = 8 and 16, so the draft-2 tolerance max{2%, 4 s / optimum} equalled 3.6% to 10.5% and the 2% floor rarely bound; 84 to 149 distinct P11 signatures of 200; one config-17-shaped pool took 69 s for three sizes (about 3 hours projected for the main study) | review report | This is why draft 3 uses max{2%, 1 s / optimum} (2.6% at an optimum of 38 s, 2% from 50 s on): it keeps the 2% target and only guarantees one second, the time step of the evaluators when ready offsets are zero |

Not computed on any registered pool before signature: anything involving P10, P11, GSV, full-pool DES enumeration, set-versus-sequence variance, warm-start chains, the execution-robustness evaluators, or the calibrated case.

## 3. Design

### 3.1 Configurations
The 18 Phase 5 configurations (`prototype/results/configs_v0_5.json`, unchanged; generated by `make_config_array()`): F ∈ {3, 5, 8}, |A| ∈ {5, 15, 30}, E ∈ {1, 2}, demand ∈ {uniform, clustered, diurnal} as a one-third fraction; c = 2. Calibrated case configurations 100 and 101 are defined in §11.

### 3.2 Order pools and seeds
- **Derived seeds:** `seed6(base, config_id, stream, size)` = the Phase 5 harness `_seed()` formula with `base` in place of `SEED_BASE`: base + config_id · 100003 + (stream + 1) · 37 + (size + 1) · 37², modulo 2³¹. Streams: 87 robustness subsample; 89 order pool (size argument 0); 90 random candidate pool; 91 set-versus-sequence candidate draw; 92 permutations; 93 P11 generation; 94 P5/P9 training sample; 95 P7 runs; 96 R-verify order; 97 §14 subset draws; 98 tie-breaking permutation; 99 execution-robustness noise; 100 + s warm-start step s (s = 1, …, 5).
- **Test pools:** 8 independent order pools per configuration. Base seeds S_p = 20260900 + p for p = 1, …, 8. Order pool: `generate_pool(demand, F, 600, seed = seed6(S_p, config_id, 89, 0), **DEMAND_PARAMS[demand])`. (The simpler rule S_p + config_id was rejected: it gives pool p + 1 of configuration c the same seed as pool p of configuration c + 1, and configurations 2j and 2j + 1 differ only in E, so the two pools would be identical.)
- **Training pools (Stage L2 and the runtime projection only):** 2 per configuration, base seeds S_t = 20260950 + t for t = 1, 2, same generator and streams. Training pools are never used for any Study 2 result.
- **Bootstrap seeds:** 20260926 + cell index (cells sorted by configuration, then size).
- **Ties.** Every ranking over the candidates of a decision (screening, verification, optima, P8 and P9 scores, R-verify order) breaks ties by a fixed uniformly random permutation of the decision's candidates (stream 98), so no candidate source is favoured by its index. The one exception is P7-matched, whose end points lie outside the candidate set; they are ranked by discovery order. Tie counts are reported (§13).
- Base seeds are disjoint from Phase 5 (20260519 + id), Amendments A and B (20260708, 20260709), and Amendment F (20260801 to 20260808).
- **No test-pool seed is used, and no test pool is generated, before the L2 addendum is signed and pinned.**

### 3.3 Wave sizes
n ∈ {8, 16, 30}. Warm-start chains use n = 16 only.

### 3.4 Candidate sets per decision
A **decision** is a triple (configuration, test pool, size): 18 × 8 × 3 = 432 decisions.
- R: K = 3,000 random candidates, `build_candidates(pool, n, 3000, Random(seed6(S_p, cid, 90, n)))`; the processing sequence is the recorded draw order (manuscript Section 3.2.3).
- P10(R): the P10 re-ordering (§5.1) of every candidate in R (3,000 derived candidates; same order sets, new sequences).
- P11: K′ = 200 constructed candidates (§5.3).
- **G = R ∪ P10(R) ∪ P11** (6,200 candidates).
- **Sequence signature:** the ordered list of (source, destination, ready offset) of a candidate. Every evaluator sees only the signature, so candidates with equal signatures have equal values everywhere. Each distinct signature is evaluated once; the numbers of candidates and of distinct signatures are reported per source.

### 3.5 Evaluators
- **M1, M2:** production `simulate_wave` (tie-break fixed on 2026-09-11), `policy="fifo"`, deterministic.
- **DES-M1, DES-M2:** the B-5 event-driven engine (heapq; concurrent AMRs claim orders in sequence and wait for each order's ready time; elevator queue served in FIFO order by request time), modularized in `src/des_evaluator.py` with its self-tests (§12). Deterministic. Phase constants are parameters with the production defaults (5 s per floor, 2 s load, 2 s unload, 5 s AMR service).
- **DES-M2 boarding rule (a correction to B-5, found while modularizing on 2026-09-26, before any Study 2 run).** Each queued request, in FIFO order, first boards an open trip with the same (source, destination), free capacity, and an open loading window, including a trip dispatched earlier in the same service pass, and only otherwise takes the earliest-free unit. This is the M2 rule of Section 3 and of the closed-form evaluator. The B-5 engine boarded only onto trips opened before the service pass, so two matching requests served in the same pass while two cars were free rode separately (hand-computed case: makespan 43 under B-5 against 24 under the M2 rule and the closed form). DES-M1 is unaffected; in the module's self-test (seed 424,244) the rule changed 73 of 400 DES-M2 cases and 0 of 400 DES-M1 cases. B-5's semantics remain available as `b5_compat=True`; Study 2 uses the corrected rule, and the B-5 numbers in §2 were produced under the old rule (Study 1 item S1-12 reruns B-5 under the corrected rule).
- **Execution-robustness evaluators (§7.3):** DES-M2 with lognormal phase noise (every AMR service duration and every elevator phase, i.e. repositioning travel, loading, loaded travel, and unloading, multiplied by an independent mean-one factor exp(σZ − σ²/2), σ ∈ {0.1, 0.2}, drawn in event order), and DES-M2 under the B-5 boarding semantics. They are used only to re-evaluate released waves; they never select a wave.
- M3 is not used in Study 2.
- Every distinct signature in G is evaluated under M1, M2, DES-M1, and DES-M2 (full enumeration), unless the §14 subset contingency is triggered.

### 3.6 Fixed dispatch
The dispatch rule is FIFO over the release sequence in all arms. `policy="cluster"` appears only as the Supp-1 reference row next to G1.

## 4. Arms

| Arm | Output per decision | Evaluator access before release | Budget per decision |
|---|---|---|---|
| P0 random | distribution: uniform over R; reported as its DES-M2 median | none | 0 |
| P2 cardinality rule | distribution: uniform over the candidates of R whose cross-floor count is at or below its 25% quantile (Phase 5 definition, ties included) | none | 0 |
| P5 Φ-corner rule | distribution: uniform over the favourable corner of R; the corner is chosen by the Phase 5 `fit_predictors` protocol from a 200-draw M2 training sample of R (with replacement, stream 94). If the corner is empty for a decision, that decision has no P5 or P5+P10 value; it is excluded from every P5 and P5+P10 quantity (cell means, the §8 pairs GSV(20) versus P5 and P5+P10 versus P5, and the G1 P5+P10 companion), the exclusion is recorded in v0_6_phase6_main.json, and the number of such decisions is reported in v0_6_phase6_gates.json | 200 M2 (training) | 200 M2 |
| P8-200 | distribution: the 200 lowest P8 scores in R (Block B definition) | none | 0 |
| P8-1 | single wave: the lowest P8 score in R | none | 0 |
| **P8-verify(20)** (comparator for G2) | single wave: walk the P8 ranking of R, replace each candidate by its P10 re-ordering, keep the first 20 distinct signatures, evaluate them under DES-M2, release the DES-M2-best. Same verification budget as GSV(20) and the same free P10 operator, without closed-form screening | DES-M2 on 20 | 20 DES |
| P9-200, P9-1 | as P8, ranked by the AMEND-C SPO+ predictor (standardized C, I, T; k_train 13; step 0.05; 300 iterations) trained on the stream-94 sample | 200 M2 (training) | 200 M2 |
| P7-run | 8 local-search runs, each the Phase 5 run definition (40 iterations from a random start over the 600-order pool, at most 41 M2 evaluations; Phase 5 reported the median of 200 such runs per cell); distribution over the 8 end points; descriptive. These are the first 8 runs of the P7-matched search (same stream 95; identical to 8 sequential calls of `optimize_wave_localsearch`) | M2 | ≤ 328 M2 |
| **P7-matched** (comparator for G2′) | multi-start local search (same move, stream 95); after each completed run, the P10 re-ordering of its end point is also evaluated under M2 (the same free operator GSV has); runs continue until 6,200 M2 evaluations are spent (the last run truncated). The 20 lowest-M2 distinct signatures among end points and their re-orderings (ties by discovery order) are evaluated under DES-M2 and the DES-M2-best is released. Equivalently, GSV with local-search end points as the generator | M2; DES-M2 on 20 | 6,200 M2 + 20 DES |
| P0+P10, P5+P10, P8+P10 | the same distributions with every candidate replaced by its P10 re-ordering (P8+P10 re-orders the P8-200 set) | as the base arm | as the base arm |
| P0+P10g | P0 with every candidate replaced by its P10g re-ordering (grouping with readiness ordering, no chaining); evaluated under M2 and DES-M2 outside G; descriptive, for the chaining increment | none | 0 |
| P11-1 | single wave: the P11 candidate with the lowest M2 makespan | M2 | 200 M2 |
| **GSV(k)**, k ∈ {1, 5, 10, 20, 50, 100, 6200} | single wave: screen G by M2, take the first k distinct signatures, evaluate them under DES-M2, release the DES-M2-best (§5.5). When k exceeds the number of distinct signatures, all are verified and the actual k is reported | M2 on G; DES-M2 on k | 6,200 M2 + k DES (plus 3,200 M1 on the P10(R) and P11 candidates when the max{M1, M2} key is in force, §5.5) |
| R-verify(k), same k grid | single wave: the first k distinct signatures of R in a random order (stream 96), DES-M2-best released; the actual k is reported (at most the number of distinct signatures in R) | DES-M2 on k | k DES |
| Generator ablations GSV_R(k), GSV_R+P10(k), GSV_R+P11(k) | GSV with G replaced by R, by R ∪ P10(R), or by R ∪ P11 | as GSV on the smaller set | 3,000, 6,000, or 3,200 M2 + k DES |

Anchors: the M2 optimum over G (= GSV(1) under the M2 key; when the §5.5 key switch is in force, the headline-key GSV(1) is reported beside it), the DES-M2 optimum over G (= GSV at k equal to the number of distinct signatures), and the DES-M2 optimum over R.

For distribution arms, the reported value is the median DES-M2 makespan over the arm's distribution (exact, because every candidate is enumerated). For single-wave arms it is the DES-M2 makespan of the released wave. Every arm, including GSV and R-verify, also reports the M2 value of its released wave or its M2 median, so that Study 2 values can be placed next to Study 1.

Budget column: the evaluator calls a deployment of the arm would need before release. The study itself enumerates every candidate under every evaluator for measurement; that enumeration is not part of any arm's budget. The generator ablations and GSV at all k are computed from the same enumeration, so they add no evaluator runs and no forking: the headline procedure is GSV(20) on G, fixed here.

## 5. Procedure specifications

### 5.1 P10 sequence-aware re-ordering (deterministic)
Input: a wave with orders (s_o, d_o, r_o) and recorded sequence π; car capacity c; initial floor f⁰ = 1.
1. Split orders into cross-floor groups by (s, d) and same-floor orders (s = d). Within a group, order by ready time and then by position in π (with zero ready offsets this is the order of π; ordering by readiness first makes P10 idempotent, which a group kept in π order is not when ready times differ).
2. Split each group, in that order, into blocks of at most c consecutive orders; a block is a co-ride unit.
3. Block ready time = the largest r_o in the block.
4. Order the blocks: primary key ascending block ready time; among blocks with equal ready time, a chain rule starting at the current floor (initially f⁰): take the block whose source equals the current floor; if none, the block whose source is nearest to the current floor (smallest |s − current floor|); ties by larger block, then lexicographically smaller (s, d), then earliest position in π. After placing a block, the current floor becomes its destination.
5. Insert each same-floor order immediately after the first placed block whose destination equals its floor and whose ready time does not exceed the order's ready time; otherwise append at the end, ordered by ready time and then π. Several same-floor orders attached to one block follow that block in the order (ready time, π).
6. **P10g** (grouping with readiness ordering, no chaining; used for the chaining increment): steps 1 to 3, blocks ordered by ready time and then by the earliest position in π; same-floor orders kept at their π positions.

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
4. Repeat with K′ = 200 independent streams: candidate j (j = 0 to 199) uses `random.Random(seed6(base, config_id, 93, n) + 7919·(j + 1))`.
The generator does not use ready times; readiness enters through P10. Duplicate signatures among the 200 are kept, counted, and reported as the number of distinct P11 signatures.

### 5.4 Stage L2 tuning rule for P11 (locked now, executed before test pools exist)
- Grid: α ∈ {1, 2, 4}, β ∈ {0.5, 1, 2}, γ ∈ {0, 0.5, 1} (27 triples).
- Data: the 2 training pools of every configuration and every size (18 × 2 × 3 = 108 training instances).
- For each triple and instance: generate 200 P11 candidates; evaluate under M2 only; score = 10th percentile of their M2 makespans (numpy's default linear interpolation) divided by the M2 median of a 3,000-candidate random pool built from the same training pool (stream 90 with the training base).
- Selected triple = lowest mean score over the 108 instances; ties by the lexicographically smallest (α, β, γ).
- No DES is run in tuning. The code reads the selected triple from the L2 addendum; nothing is edited into the code after tuning, so the code hash recorded in L2 is the hash of the code that ran the tuning.

### 5.5 GSV
For each decision: evaluate every candidate of G under M2; rank by M2 (ties by the stream-98 permutation); walk the ranking and keep the first k distinct signatures; evaluate them under DES-M2; release the DES-M2-best (ties by the same permutation). The numbers of candidates scanned, distinct signatures verified, and candidates tied at the screening boundary and at the released value are reported. If G4 falls in its middle or lower tier (§7), the screening key for candidates from P10(R) and P11 becomes max{M1, M2}; the headline GSV (single-wave and warm-start) then uses that key, and the M2-key results are reported beside it (pre-commitment D-F).

## 6. Set-versus-sequence decomposition (S2-1)
For each decision: draw 200 candidates uniformly without replacement from R (stream 91); for each, evaluate the recorded sequence and 20 random permutations (stream 92) under M2 and DES-M2 (21 sequences per candidate). Sequence share s = σ²_within / (σ²_within + σ²_between) from a one-way random-effects decomposition over (candidate, sequence), with the ANOVA estimators σ²_within = MSW and σ²_between = max{0, (MSB − MSW)/21}. Report s per cell and per demand pattern.

## 7. Gates and wording ladders (locked at signature)

### 7.1 Units and definitions
- Cell = (configuration, size), 54 cells. **Cell value = the mean over the 8 test pools of the per-pool quantity** (for a ratio such as G1's reduction, the per-pool ratio is computed first, then averaged). Configuration-level values average the three sizes (18 units).
- r(k) = (DES-M2 makespan of GSV(k) − DES-M2 optimum over G) / DES-M2 optimum over G. The **regret tolerance** of G3 is max{2%, 1 s / DES-M2 optimum over G}: 2%, but never less than one second, the time step of the evaluators when ready offsets are zero (for an optimum of 38 s this is 2.6%; from 50 s on it is 2%). Draft 2's max{2%, 4 s / optimum} was dropped because it equals 3.6% to 10.5% at the optimum sizes seen in toy runs.
- DL_m = (DES-M2 makespan of the evaluator-m optimum over G − DES-M2 optimum over G) / DES-M2 optimum over G, for m ∈ {M1, M2, DES-M1}. DL is the loss of releasing the evaluator's single best candidate (k = 1). When several candidates tie at the evaluator-m minimum, the numerator uses their mean DES-M2 makespan (the expected value under random tie-breaking), and the number of tied candidates is reported.
- **Every gate sentence that reports a DES-M2 quantity (G1, G2, G2′, G3, G5(b), G6, G8) carries the qualifier "under the event-driven evaluator" in the manuscript**; §7.3 re-evaluates the released waves outside it. G4 and G5(a) compare the closed-form evaluators.
- The median k\* over the 8 pools of a cell is the average of the two middle values, so it can lie between grid values (for example 35 between 20 and 50); it is compared with 20 and 50 as it is.
- G4 counts candidates, duplicates included, as registered; the share among distinct P11 signatures is reported as a companion.
- **Scenario selection** in STORY_CONTRACT.md §8 uses the DES-M2 tiers of record; §7.3 affects wording only.

### 7.2 Gates

| Gate | Quantity | Upper tier | Middle tier | Lower tier |
|---|---|---|---|---|
| **G1 sequence lever** | per pool, the relative reduction of the DES-M2 median of P0+P10 against P0; mean over the 54 cells, with sign agreement (share of cells with a reduction) | ≥ 7.5% and sign ≥ 75%: "re-ordering at release is a first-order lever under the event-driven evaluator" | 2.5% to 7.5%, or ≥ 7.5% with sign < 75%: "re-ordering at release gives a moderate reduction under the event-driven evaluator" | < 2.5%: "under the event-driven evaluator the release sequence is a small lever" |
| **G2 screening versus heuristic scoring** | share of cells where the cell mean of GSV(20) is below the cell mean of P8-verify(20) (same 20 DES verifications and the same P10 operator; GSV additionally screens 6,200 candidates in closed form) | ≥ 75%: "closed-form screening of a generated set outperforms heuristic scoring at the same verification budget" | 50% to 75%: "closed-form screening is comparable to heuristic scoring at the same verification budget" | < 50%: "closed-form screening does not outperform heuristic scoring at the same verification budget; reported as a boundary of the procedure" |
| **G2′ versus local search** | share of cells where the cell mean of GSV(20) is at or below the cell mean of P7-matched (ties count as matches; same M2 and DES budgets, same P10 operator, same de-duplication) | ≥ 50%: "matches or beats a budget-matched local search" | 25% to 50%: "approaches a budget-matched local search" | < 25%: "a budget-matched local search remains stronger" |
| **G3 screening fidelity** | per decision k\* = smallest k in the grid with r(k) ≤ the regret tolerance (§7.1), under the headline screening key; per cell the median k\* over pools | median k\* ≤ 20 in ≥ 80% of cells: "a shortlist of 20 suffices" | median k\* ≤ 50 in ≥ 80% of cells: "a shortlist of 50 suffices" | otherwise: "closed-form screening does not bring the shortlist down to 50 in more than one fifth of the cells" |
| **G4 ordering on constructed candidates** | share of P11 candidates (all decisions) with M1 ≤ M2 | ≥ 95%: "the ordering persists on candidates built to create co-rides" | 80% to 95%: "the ordering weakens on constructed candidates; screening uses max{M1, M2} for them" | < 80%: "the choice of elevator model matters once composition exploits co-occupancy" |
| **G5 warm start** | (a) share of warm-state evaluations with M1 ≤ M2 at steps 2 to 5, on 300 candidates per step drawn from the step's random pool R_s; (b) median over chain units (configuration × pool × release variant) of the retention ratio R_u = mean over steps 2 to 5 of (mean P0 increment − GSV increment) divided by the step-1 gain (mean P0 increment − GSV increment at step 1); units with a non-positive step-1 gain are excluded and counted | (a) ≥ 95% and (b) ≥ 0.80: "the single-wave advantage is retained at warm state" | one of (a), (b) met: "partially retained at warm state" | neither: "single-wave results do not transfer to consecutive waves" |
| **G6 set versus sequence** | sequence share s under DES-M2, mean over the 54 cells (M2 descriptive) | > 0.5: "sequence dominates" | 0.2 to 0.5: "set and sequence both matter" | < 0.2: "the order set dominates" |
| **G7 calibrated case** | none | descriptive only | | |
| **G8 fidelity ladder** | share of cells with DL_M1 > DL_M2 | ≥ 75%: "selecting the evaluator's best candidate with the throughput abstraction costs more than selecting with co-occupancy" | 50% to 75%: "often costs more" | < 50%: "no systematic difference" |

**No gate has a pass or fail consequence beyond its wording tier.** No tier triggers a rerun, a retune, a new arm, or a change of any other gate. The only mechanical consequence is the D-F screening-key switch after G4 (§5.5).

### 7.3 Execution robustness (S2-10)
Because DES-M2 both selects (GSV, R-verify, P7-matched, P8-verify) and scores, the released waves are re-evaluated by evaluators that did not select them:
- **Waves:** the released waves of GSV(20) under both keys, GSV(1), P8-verify(20), P7-matched, P8-1, P9-1, and P11-1; and, for G1, 50 candidates of R (stream 87) with their P10 re-orderings.
- **Evaluators:** DES-M2 with phase noise σ = 0.1 and σ = 0.2 (§3.5), 20 replications each with noise seeds seed6(S_p, config_id, 99, n) + r, r = 0, …, 19, the same seeds for every wave of the decision (common seeds across arms), value = mean over replications; and DES-M2 under the B-5 boarding semantics (deterministic). The deterministic DES-M2 value (σ = 0) is recorded for the same waves as the baseline.
- **Reporting rule (locked):** G2 and G2′ shares and tiers are recomputed under each of the three evaluators and compared with their DES-M2 tiers. G1's mean, sign share, and tier are recomputed on the paired 50-candidate subsample under σ = 0 (baseline) and under each evaluator, and compared with the σ = 0 subsample tier, so that subsample noise is not mistaken for an evaluator effect. If a tier is lower under any evaluator, the main text states both tiers next to each other (and STORY_CONTRACT §8 puts the lower one in the abstract). The gate of record remains the DES-M2 tier.

### 7.4 Threshold rationale (fixed before any Study 2 result)
G1's 7.5% and 2.5% are about three quarters and one quarter of the prior-exposed 10.2% closed-form gain of clustered dispatch (used only to size the thresholds; the wording does not compare the two). G3's tolerance is explained in §7.1. G4's and G5(a)'s 95% sit below the 98% to 100% per-wave ordering rates seen on random candidates. G5(b)'s 0.80 asks that at least four fifths of the cold-start advantage survive at warm state. G2 and G8 use three quarters of cells as the upper tier, G2′ one half because the comparator is a search method with the same budget.

### 7.5 Descriptive companions (no tiers)
G1: under M2 closed form (next to the Supp-1 value, flagged as prior-exposed), P5+P10 versus P5, P8+P10 versus P8-200, P10 versus P10g (chaining increment), by demand pattern, and on the §7.3 subsample. G2: GSV(20) versus P8-best (per pool the lower of P8-200 and P8-1), whose outcome was foreseeable from §2 and is therefore not a gate. G2 and G2′: evaluator budgets. G3: r(k) curves and k\* relative to the DES-M2 optimum over R. G4: ordering on P10(R), under DES-M1 ≤ DES-M2, and the number of distinct P11 signatures. G5: the P11 ordering share at warm state. G8: levels of DL_M2 and DL_DES-M1. Generator ablations: GSV_R, GSV_R+P10, GSV_R+P11 at every k, and the share of GSV(20) releases whose candidate came from P11 (both feed the C3 wording rule of STORY_CONTRACT.md §8).

## 8. Statistical analysis
- Independent unit: the order pool. Cell-level 95% percentile intervals by bootstrap over the 8 pools (B = 2,000; seed 20260926 + cell index) for GSV(20), P0, P8-verify(20), P7-matched, and the per-pool G1 reduction.
- Pairwise comparisons at configuration level (18 paired values, averaging sizes and pools): Wilcoxon signed-rank test, two-sided, zero differences discarded (Wilcoxon's method), exact or normal-approximation p-value as chosen by SciPy's automatic rule (SciPy 1.14.1 installed on 2026-09-26; every output records the Python, NumPy, SciPy, and pandas versions); a comparison whose 18 differences are all zero gets p = 1 and stays in the family. Holm step-down with monotone adjusted p-values, α = 0.05, within the family {GSV(20) versus P8-verify(20), versus P7-matched, versus P5, versus R-verify(20); P0+P10 versus P0; P5+P10 versus P5}. The same family is reported per size as a sensitivity analysis (Holm within each size).
- Every quantity is reported in seconds and as a percentage.

## 9. Warm-start chains (S2-7)
- Run after the complete single-wave study and its G4, because the GSV chain uses the headline screening key of §5.5; the driver refuses to start unless the gates file was computed from the current main results (their SHA-256 is recorded in it).
- Per (configuration, test pool, release variant): chains of 5 waves at n = 16 for arms P0 (3 replicate chains), P5 (3 replicate chains, descriptive), and GSV(20) (1 chain). Chain randomness for arm a (0 = P0, 1 = P5, 2 = GSV) and replicate j at step s uses the seed seed6(S_p, config_id, 100 + s, 16) + 1000·a + 100·j.
- Step s draws a fresh 3,000-candidate random pool R_s from the orders of the test pool not yet released by that chain. P0 releases a uniform draw from it. P5 releases a uniform draw from its favourable corner, using the corner chosen for the same (configuration, pool) at size 16 in the single-wave study (no refit); if a step pool's corner is empty, that P5 chain stops and the stop is recorded. GSV(20) adds the P10 re-orderings and 200 P11 candidates and applies §5.5 (headline key, distinct signatures) with every evaluation made after the chain's realized prefix.
- Release epochs: variant A, wave s + 1 is released when all previously released orders are complete; variant B, wave s + 1 is released at the previous release epoch plus half of the time from that epoch to the completion of all released orders (overlap). Completion is measured under DES-M2, the stand-in for execution, and the same epochs are used for every evaluator.
- Evaluation by concatenation: the released waves are concatenated in release order with absolute ready offsets and evaluated by the unchanged evaluators, so AMR and elevator states carry over exactly (G0 item 5). Metrics: the incremental completion C(prefix s) − C(prefix s − 1) under DES-M2 (for G5(b)) and the five-wave completion time (descriptive).
- G5(a): 300 candidates drawn uniformly from R_s at each of steps 2 to 5 of the GSV chain; each is appended to the chain's realized prefix and the whole concatenation is evaluated under M1 and under M2 (the ordering from the common cold start at time 0, applied to the longer sequence). The P11 candidates of each step are compared in the same way (descriptive).
- Implementation streams (fixed): P11 candidate j at step s uses the chain seed + 1 + 7919·(j + 1); ties use the chain seed + 2; the G5(a) sample uses the chain seed + 3.

## 10. Runtime and scalability (S2-9)
Configurations {1, 7, 17}, one test pool each, K ∈ {1,000, 3,000, 10,000}, n ∈ {8, 16, 30, 60}: wall-clock of generation, screening, and verification per decision, and per candidate. Descriptive.

## 11. Literature-calibrated case (S2-8; depends on decision D-K)

### 11.1 Scenario
Configuration 100: F = 3, |A| = 30, E = 2, c = 2. Configuration 101: F = 3, |A| = 30, E = 3, c = 2. Three-story robotic warehouses with two or three freight elevators are documented in public cases (for example the Quicktron and LH three-floor site; Prologis Georgetown, three floors with three freight elevators).

### 11.2 Order flow and data cleaning
- Source: UCI Online Retail II (CC BY 4.0).
- Cleaning, in this order: drop cancellation invoices (invoice number starting with "C"); drop lines with non-positive quantity or price; keep only lines whose stock code begins with five digits (this removes postage, carriage, manual, bank-charge, discount, and test codes); drop exact duplicate lines.
- Eligible days: calendar days (invoice date) with at least 600 remaining lines. Each case test pool uses one eligible day drawn uniformly on stream 89 and 600 of its lines drawn without replacement on the same stream.
- Mapping: each line becomes one load. Outbound loads (share 0.8) move from the storage floor of the stock code to floor 1 (packing and shipping); inbound replenishment loads (share 0.2) move from floor 1 to the storage floor. Storage floor = 2 + (SHA-256 of the stock code, read as an integer, modulo (F − 1)). Direction is assigned per line by a Bernoulli(0.8) draw on the same stream.
- Ready offsets: zero in the primary run; in a sensitivity run, the invoice-time rank of each line within its pool is scaled linearly to [0, 50] s (the Phase 5 diurnal horizon), invoice-time ties broken by the line's position in the source file.
- These mappings are researcher assumptions and are stated as such in the paper.

### 11.3 Parameter table (Stage L2)
Travel time per floor, loading and unloading time, and AMR service time are set to the midpoints of the ranges documented in public freight-elevator specifications (KONE and Schindler product data; Peters round-trip-time decomposition) and fixed in the L2 addendum with sources before any case pool is generated, together with each documented range (low, high) and the switch `case_included` (yes only if D-K is signed and the data passed the §11.2 checks). The code reads them from the addendum. Sensitivity runs: each of the four parameters is set to the low and then the high end of its range, one at a time with the others at their midpoints, and the ready-offset sensitivity of §11.2 is run once; all sensitivity runs use n = 16, all 8 pools, and both case configurations (4 × 2 + 1 = 9 settings × 16 decisions).

### 11.4 Runs and reporting
8 test pools per case configuration (seeds seed6(S_p, 100, 89, 0) and seed6(S_p, 101, 89, 0)), sizes {8, 16, 30}, all arms of §4, all evaluators with the case parameters. Descriptive (G7). Wording: "parameters set within publicly documented ranges"; never "calibrated to a facility".

## 12. Code freeze and validation (G0; recorded in the L2 addendum)
1. `python -m src.simulator` passes all hand-computed targets.
2. `python -m src.des_evaluator` passes with no skipped test: a single order equals the closed-form value exactly; single-AMR waves (with and without ready times) equal the closed-form value exactly; hand-computed multi-AMR cases (two AMRs sharing one M2 car; a ready time that delays a claim; M1 slots serving in parallel; the boarding-rule case of §3.5, 24 versus 43); `b5_compat=True` reproduces the B-5 engine exactly on 800 randomized toy cases; the noise option reproduces the deterministic evaluator at σ = 0 and is reproducible by seed.
3. `simulate_wave` with explicit default phase times equals the call without them on 2,100 randomized toy calls across all pool types (shipped as `_test_timing_default_randomized`).
4. `python -m src.phase6_policies` passes with no skipped test: P10, P10g, and P11 on hand-built instances; P10 idempotent on its own output; P11 returns n distinct orders; P9 fit identical to the AMEND-C code; budgeted local search identical to `optimize_wave_localsearch` in its first run and exact in budget, also with the P10 end-point hook.
5. Concatenation equivalence: a one-wave chain equals `simulate_wave` and DES exactly.
6. Every driver stops at the guard in real mode and completes in `--selftest` mode. The guard checks, for the protocol, the decision sheet, the story contract, and the L2 addendum: signature, the hash pinned in the signed manifest (line-ending normalized), and that no superseded manifest shows a different signed version.
7. The code tree hash (one definition, `registration_guard.code_tree_sha256`, used by the drivers and the manifests) of the code that ran the tuning is written into the L2 addendum. Test-pool runs stop if the code differs from it, unless `--allow-code-change` names a dated deviation-log entry, which is then recorded in every output.

## 13. Outputs and reporting commitments
- Results (written by `src/experiments_phase6.py` and `src/analysis_phase6.py`): `prototype/results/v0_6_phase6_L2_tuning.json` (Stage L2 and the runtime projection), `v0_6_phase6_main.json` (every decision: all arms, GSV at every k with actual k and tie counts, ablations, anchors, ladder, ordering counts with distinct-signature counts, execution robustness, set-versus-sequence), `v0_6_phase6_warmstart.json`, `v0_6_phase6_runtime.json`, `v0_6_case_*.json`, and `v0_6_phase6_gates.json` (G1 to G8 with tiers, the §7.3 companions, tests, bootstrap intervals, budgets); raw candidate rows in `results/raw/mvs_v0_6_phase6_candidates.csv.gz` (configuration, pool base, size, candidate index, source R/P10/P11, parent, signature id, M1, M2, DES-M1, DES-M2, C, I, T, cross-floor count).
- Every file records its generation time, the code tree hash, the SHA-256 of this protocol and of the L2 addendum, whether the code matches the L2 hash, any code-change reference, and the library versions.
- The main study is written as one checkpoint part per configuration (`v0_6_phase6_main_part_c<id>.json` and the matching raw part) and merged into `v0_6_phase6_main.json` only when all 432 decisions are present exactly once; the analysis refuses an incomplete file.
- All arms, configurations, sizes, and gates are reported in full, favourable or not. No result is dropped for being unfavourable.
- Study 2 is labelled [NS] P6-<item> throughout the manuscript and never presented as confirming Study 1.

## 14. Contingencies and deviations
- **Runtime.** Measured on toy waves (2026-09-26): about 0.3 ms per DES-M2 run at n = 16 and 0.75 ms at n = 30, so full enumeration is expected to take hours. The binding projection is made during Stage L2 on a training pool of configuration 17 (the largest), timing one full decision per size and scaling to 18 × 8 pools. If it exceeds 48 hours, the subset mode is used for the whole study, set as `des_subset_mode: yes` in the L2 addendum before any test pool exists (the drivers read it there; there is no command-line switch in real runs; an empty `des_subset_mode` field is read as no): DES is evaluated for the top 500 distinct signatures under each screening key and under M1 (with every candidate tied at the M1 minimum, so DL_M1 is defined), 500 distinct signatures drawn uniformly (stream 97), every shortlist with k ≤ 100, and the P8-verify shortlist; distribution arms use a fixed 200-candidate subsample each (stream 97 with a fixed per-arm offset), and each re-ordered arm uses the images of its base arm's subsample, so G1 stays paired; values are shared by signature; shortlists with k > 100, G3, G8, and the anchors are then defined on the evaluated subset.
- **P9 (decision D-L).** If P9 cannot run at Study 2 scale by the code freeze, it is removed before any Study 2 result is computed, and the removal is recorded with its reason.
- **Calibrated case (decision D-K).** If D-K is not signed or the data cannot be obtained under its license, §11 is dropped before any Study 2 result is computed, and the drop is recorded.
- **Bugs.** A bug found after runs is fixed, the whole affected block is rerun, and both versions are reported.
- **Deviation log.** Every deviation from this protocol is logged with date, reason, and effect in `revision_2026-09-26_ijpr/EXECUTION-LOG.md` and summarized in the manuscript's registration appendix.

## 15. What Study 2 will not do, and conflicts with Study 1
It will not change any Phase 5 file, verdict, or configuration; use M3; test capacity interventions; add arms after signature; tune anything on test pools; or present any Study 2 quantity as confirming a Study 1 verdict.
If a Study 2 result points in the opposite direction of a Study 1 finding (for example the ordering weakening on constructed candidates while Study 1 shows it on random candidates), both are reported with their scope (candidate population, evaluator, scale); the Study 1 verdict stands, the two are not averaged, and the discussion states the scope difference.

## 16. Sign-off (L1)

```
Design, arms, metrics, gates, analysis, and contingencies (L1) reviewed and locked:       [x]  Shiyue Hu  date 2026-09-26
Decisions D-K (case), D-L (P9) and D-M (thresholds) as recorded in 01_DECISIONS_TO_SIGN:  [x]  Shiyue Hu  date 2026-09-26
```
To sign: in one edit, tick the boxes above, set `author_signoff` to "SIGNED (<name>, <date>)", and replace the `status` line (for example "SIGNED; nothing executed as of <date>"). If decision D-M selects the draft-1 tolerance (2%) or changes any §7.2 gate value, edit §7.1 and §7.2 to the chosen values in this same signing edit and set REGRET_TOL_ABS (0.0 for the draft-1 tolerance) and GATES in `prototype/src/phase6_config.py` to the same values before the code freeze of §12; the decision sheet and this protocol must agree at signature, because the guard compares hashes only. Run, from the repository root, `python "revision_2026-09-26_ijpr/archive_package/make_manifest.py" SIGNED`; then open `MANIFEST_SIGNED.md` and confirm that the signoff column of every registration starts with SIGNED or ACKNOWLEDGED (the guard does not recognise curly quotes). Then register the signed file on OSF. Do not edit this file afterwards: the guard stops every registered run if its bytes change, and a changed file cannot be re-pinned. The SHA-256 of this file is recorded in the manifest and on OSF; the OSF identifier is recorded in the L2 addendum and in the manuscript's registration appendix, never in this file.
