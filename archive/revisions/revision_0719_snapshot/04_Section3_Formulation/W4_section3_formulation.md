---
title: "W4: Section 3 (Problem Formulation) full draft + notation table"
date: 2026-07-08
sources consulted:
  - "f:/Paper 3/CLAUDE.md"
  - "f:/Paper 3/paper_draft/TERMINOLOGY.md"
  - "f:/Paper 3/paper_draft/methodology_v0_2.md"
  - "f:/Paper 3/paper_draft/section4_draft_v0_1.md"
  - "f:/Paper 3/paper_draft/section5_draft_v0_1.md"
  - "f:/Paper 3/paper_draft/Introduction/introduction_v1.0.md"
  - "f:/Paper 3/paper_draft/theorems_m5.md (U_c(eps) formal definition)"
  - "f:/Paper 3/prototype/src/simulator.py (engine semantics, phase constants)"
  - "f:/Paper 3/prototype/src/features.py (exact C, I, T definitions)"
  - "f:/Paper 3/prototype/src/wave_policies.py (FILTER_Q, corner scheme, q_Phi sign rule, P0-P7)"
  - "f:/Paper 3/prototype/src/phase5_config.py (grid factors, pool sizes)"
  - "scratchpad/panel_completeness.json (fatal flaw 1, required additions 1-2)"
status: "draft for author review"
---

# W4 revision document: Section 3 (Problem Formulation)

This document supplies the complete, manuscript-ready Section 3 that the completeness audit identified as missing (panel_completeness fatal flaw 1, CRITICAL: "no Section 3 ... where Phi, M1/M2/M3, and all assumptions must live"). It is written to slot between the Related Works section (Section 2) and the existing Section 4 draft (`paper_draft/section4_draft_v0_1.md`), whose frontmatter already assumes "Φ and the elevator models M1/M2/M3 are defined in §3" and whose §4.2.1 cites "(§3, Assumption A5)". The assumptions list below is numbered so that A5 is exactly the model-exogeneity assumption §4.2.1 cites. Edits 1 to 5 are the five subsections (all new text); Edit 6 is a one-sentence consistency fix to the §5.1 opener that Section 3 makes mandatory.

Approximate prose length of Edits 1 to 4 combined: about 1,650 words, within the 1,500 to 1,800 target; Edit 5 is the notation table.

---

# 编辑 1: 新增 §3.1 System and problem statement

## 修改前 (BEFORE)

(no existing text; new section)

## 修改后 (AFTER)

# Section 3. Problem Formulation

## 3.1 System and problem statement

We consider a multi-story order-fulfillment facility with `F` stacked floors. A fleet `A` of `|A|` autonomous mobile robots (AMRs) performs all material handling. Within a floor an AMR moves freely; to change floors it must ride one of `E` shared freight elevators, each with per-trip capacity `c`. The elevators are the system's vertical bottleneck: every cross-floor movement occupies an elevator for a full trip cycle, and AMRs queue whenever no elevator is available.

An order `o = (s_o, d_o, r_o)` requests transport from a source floor `s_o` to a destination floor `d_o`, and becomes available `r_o` time units after its wave is released (`r_o = 0` throughout the main design; staggered releases appear only in designated studies). A wave `W = {o_1, ..., o_n}` is a finite set of `n` orders released together at a common release epoch `t_W`. Serving an order requires an AMR to reach the source floor (riding an elevator if it is on a different floor), pick the item up, reach the destination floor (riding an elevator whenever `s_o ≠ d_o`), and drop it off. Each elevator trip decomposes into five phases: wait (until an elevator becomes available), reposition (the elevator travels empty to the boarding floor), load (2 s), travel (loaded movement to the destination floor), and unload (2 s); reposition and travel take 5 s per floor traversed.

The decision architecture has two stages. The tactical stage decides wave composition: which orders to release together. The operational stage dispatches the AMR fleet that delivers the released orders through the shared elevators. This paper holds the operational stage fixed and studies the tactical stage. In the fixed dispatch rule, orders are processed in wave sequence, each is assigned to the earliest-free AMR, and elevator requests are served first-come-first-served; a destination-clustered dispatch variant appears only in one supplementary comparison in Section 5.4. What makes the tactical stage consequential is the coupling between the stages: wave composition fixes the profile of elevator work (how many cross-floor transitions, in which directions, with what temporal stagger) before the fleet scheduler acts.

The objective is the wave makespan

> `C_max(W; M) = max_{o ∈ W} (completion time of o) − t_W`,

the time to complete the last order of the wave, evaluated under an elevator model `M ∈ {M1, M2, M3}` (Section 3.3). The tactical problem is: given a candidate set of feasible waves (Section 3.4), select the wave, or the class of wave structures, that minimizes a summary statistic of `C_max(W; M)`. This is a stochastic optimization over a combinatorial decision space with a simulator-realized objective, and it is hard on two counts. First, the decision space is combinatorial (all size-`n` subsets of an order pool) and `C_max` admits no closed form in the composition variables; it is available only by running the evaluation engine of Section 3.3. Second, the elevator model `M` is itself uncertain: the operator does not know which member of `{M1, M2, M3}` describes their installation, and under `M3` the objective is stochastic even for a fixed wave. Section 4 develops two analytical tools, one diagnostic and one prescriptive, that address these two difficulties on a structured representation of `W` rather than on the raw combinatorial space.

## 理由 (RATIONALE)

对应 panel_completeness 致命缺陷 1（CRITICAL：手稿没有 §3，Φ、电梯模型与全部假设无处安放）与 required_additions 第 1 条。本小节交付任务要求的全部要素：F 层、|A| 台 AMR、E 部容量为 c 的共享货梯、五阶段电梯行程、两阶段决策架构（战术层为决策变量、操作层固定）、以及 makespan 目标 C_max(W;M)。末段刻意呼应 §4 开头那句 "Section 3 cast wave release coordination as a stochastic optimization whose objective C_max(W; M) is simulator-realized and whose decision space is combinatorial"，使现有 §4 草稿无需改动即可衔接。全文无破折号，"stage" 只用于问题、"tool" 只用于贡献，符合 TERMINOLOGY.md。

---

# 编辑 2: 新增 §3.2 The wave representation Phi and the corner partition

## 修改前 (BEFORE)

(no existing text; new section)

## 修改后 (AFTER)

## 3.2 The wave representation `Φ = (C, I, T)` and the corner partition

Each wave is summarized by three interpretable coordinates, `Φ(W) = (C(W), I(W), T(W))`.

**Vertical spread `C`.** Collect the multiset of floor visits of `W`: for each of the `n` orders, both its source and its destination floor, giving `2n` visits. Let `p_f` be the fraction of visits on floor `f`. Then

> `C(W) = − Σ_{f=1}^{F} p_f ln p_f`,

the Shannon entropy of the floor-visit distribution. `C` ranges from 0, when all activity sits on a single floor, to `ln F`, when visits are spread uniformly across all floors. High `C` therefore means the wave's activity is spread across many floors; low `C` means it sits on few. We stress the direction because it is easy to invert: `C` measures spread, not the opposite.

**Directional imbalance `I`.** Let `N_up = |{o ∈ W : d_o > s_o}|` and `N_down = |{o ∈ W : d_o < s_o}|`; same-floor orders are excluded. Then

> `I(W) = |N_up − N_down| / (N_up + N_down)`,

with `I(W) = 0` when the wave has no cross-floor orders. `I = 1` means all vertical traffic flows one way; `I = 0` means the two directions are balanced.

**Temporal clustering `T`.** `T(W)` is the coefficient of variation of the within-wave release offsets `{r_o}`: the standard deviation of the offsets divided by their mean, set to 0 when the mean offset is 0. In the main design all orders share `r_o = 0`, so `T` is identically zero; it activates only in the staggered-release studies and is retained as the third coordinate for completeness.

`Φ` is a structured representation of wave composition: a decomposition of what kind of wave is being released into physically interpretable coordinates. It is not a predictive surrogate, and the paper makes no claim that `Φ` predicts makespan. Its role is to organize the candidate space so that the value of wave structure can be measured (Section 4.1) and a robust wave structure selected (Section 4.2).

**The corner partition.** Fix a candidate pool of waves (Section 3.4) and a truncation quantile of 0.25 (the constant `FILTER_Q` in the implementation). Writing `C^{(u)}` for the pool `u`-quantile of `C` and likewise for `I`, define the tail sets `HC = {C ≥ C^{(0.75)}}`, `LC = {C ≤ C^{(0.25)}}`, `HI = {I ≥ I^{(0.75)}}`, and `LI = {I ≤ I^{(0.25)}}`. The working partition is the `2×2` quartile-corner scheme

> `Q = {HC·HI, HC·LI, LC·HI, LC·LI}`,

each corner `q ∈ Q` being the intersection of one `C`-tail with one `I`-tail. The corners are non-covering by construction: a wave whose `C` or `I` falls in the interquartile band belongs to no corner, so `Q` deliberately contrasts extreme wave structures rather than tiling the pool (under independent coordinates each corner holds roughly 6% of the candidates). We refer to `Q` as the partition of `Φ`-space with the interquartile remainder left unassigned; every quantity in Section 4 uses only the corner-conditional statistics and the pool-level statistic, so the remainder plays no role.

A `Φ`-informed wave-release policy selects one corner, the favorable corner `q_Φ`, by a sign rule: fit an ordinary-least-squares regression of realized makespan on `(1, C, I)` over a small simulated training sample of candidates, and select the corner that descends both coefficients (the high-`C` corner if the `C` coefficient is negative, otherwise the low-`C` corner, and analogously for `I`). Only the two coefficient signs are used; the fitted values themselves play no role in any result.

## 理由 (RATIONALE)

对应 panel_completeness required_additions 第 1 条（"Phi = (C, I, T) definitions" 必须以手稿正文形式存在）。三个定义逐一从 `prototype/src/features.py` 转写为数学式：C 为楼层访问分布（源、目的楼层各计一次，共 2n 次）的香农熵，I 为 |N_up − N_down|/(N_up + N_down)（同层订单剔除），T 为波内释放偏移的变异系数（未错峰时恒为零）。按 TERMINOLOGY.md 的红线，C 命名为 "vertical spread" 且明确 "high C = spread"，并加了一句方向警示；Φ 明确声明为表示/分解而非预测替身。2×2 角点分割按任务要求显式给出 FILTER_Q = 0.25 截断与"非覆盖"性质（取自 `wave_policies.py` 的 `corner_positions`），q_Φ 的 OLS 符号规则取自 `favorable_label` / `fit_phi_beta`，措辞用 "selects" 而非任何预测性动词。

---

# 编辑 3: 新增 §3.3 Elevator models and the evaluation engine

## 修改前 (BEFORE)

(no existing text; new section)

## 修改后 (AFTER)

## 3.3 Elevator models `{M1, M2, M3}` and the evaluation engine

Three elevator models realize the vertical resource; they differ in how faithfully per-trip capacity is represented.

**`M1` (throughput abstraction).** Capacity is modelled as aggregate throughput: the `E` elevators of capacity `c` behave as `E·c` independent single-rider servers. Each elevator request is assigned to the earliest-available server, which executes the five-phase trip for that single request. `M1` captures the bottleneck-relief effect of capacity without co-occupancy: two requests never share a physical trip.

**`M2` (true co-occupancy batching).** The `E` elevators are `E` servers, each carrying up to `c` requests per trip. A new request boards an in-progress trip if and only if it matches the trip's origin-destination pair `(src, dst)`, arrives while the trip's loading window is still open (no later than the trip's loading end), and fewer than `c` riders are aboard; boarding requests share the trip's completion time. A request that cannot board is dispatched as a new trip on the earliest-available elevator. `M2` is the reference model: it realizes physical co-occupancy, at the price of making capacity usable only by structurally matching requests.

**`M3` (stochastic batching).** `M3` is `M2` with lognormal multiplicative noise: each of the four duration phases of every trip (reposition, load, travel, unload) is scaled by an independent lognormal multiplier with mean one and parameter `σ` (`σ = 0.20` at publication scale). Setting `σ = 0` recovers `M2` exactly, and the noise is driven by a seeded generator, so all runs are reproducible.

Two further variants, an elevator with a direction-switch penalty and a pool with heterogeneous per-elevator capacities, are used only in the appendix robustness studies; both reproduce `M2` exactly at their identity settings.

**The evaluation engine.** `C_max(W; M)` is realized by a deterministic, closed-form, sequential time-accumulator; it is explicitly not an event-driven concurrent simulation. The engine walks the wave's orders one at a time in release sequence. Each order is assigned to the earliest-free AMR (ties broken by index), whose clock then advances through at most two elevator trips and two service operations: ride to the source floor if the AMR is elsewhere, a constant 5 s pickup, ride to the destination floor whenever `s_o ≠ d_o`, and a constant 5 s drop-off. Every elevator trip accumulates the five phases of Section 3.1 in closed form: wait until the assigned server (a slot under `M1`, a car under `M2`/`M3`) is available, reposition at 5 s per floor, load 2 s, travel at 5 s per floor, unload 2 s. All AMRs and elevators start at floor 1 at the release epoch, and the wave makespan is the latest order completion minus `t_W`. Under `M1` and `M2` the engine is fully deterministic: identical inputs yield identical makespans, which is what permits exact per-wave model comparisons on matched waves in Section 5.3. Under `M3` it is reproducibly stochastic.

The engine rests on five assumptions.

- **A1 (sequential order processing).** Orders are processed in wave sequence with greedy earliest-free AMR assignment; there is no event-driven concurrency beyond the availability clocks of AMRs and elevator servers.
- **A2 (deterministic phase constants).** Elevator kinematics are constant: 5 s per floor for reposition and travel, 2 s load, 2 s unload. `M3` relaxes determinism multiplicatively while preserving the phase structure.
- **A3 (constant intra-floor service).** Intra-floor handling is a constant 5 s per pickup and per drop-off; no path planning, floor congestion, or pick-time variance is modelled. A service-time noise variant is examined in the appendix.
- **A4 (fixed operational stage).** The dispatch rule of the operational stage is held fixed as described in Section 3.1; wave composition is the only decision under study.
- **A5 (elevator-model exogeneity).** The elevator model `M` is exogenous to wave composition: composing a wave changes the work the elevators receive, not the physics by which they serve it. This is the assumption under which model uncertainty can be treated as a hedging problem in Section 4.2.

These choices trade fleet-level concurrency for exactness: makespans are exactly reproducible, hand-verifiable on small instances, and cheap enough to evaluate at the scale of Section 5 (106,800 simulations at publication scale).

## 理由 (RATIONALE)

对应 panel_completeness required_additions 第 1 条中的关键纠错要求：仿真器必须"正确地标注为 closed-form sequential time-accumulator，而非 event-driven"（现有 §5.1 开头恰恰写错了，见编辑 6）。三个模型定义逐一对照 `simulator.py`：M1 = `ElevatorPool`（E·c 个独立单乘客服务位），M2 = `ElevatorPoolBatched`（E 台电梯、(src,dst) 匹配且装载窗口未关才可同乘），M3 = `ElevatorPoolStochasticBatched`（对 reposition/load/travel/unload 四个时长阶段乘均值为 1 的对数正态噪声，σ=0.20 为 publication scale 取值）。假设编号刻意使 A5 = 电梯模型外生，与 §4.2.1 已有引用 "(§3, Assumption A5)" 精确对齐，避免改动 §4。扩展模型（方向切换惩罚、异质容量）一句带过并注明只用于附录稳健性研究。

---

# 编辑 4: 新增 §3.4 The candidate-pool protocol

## 修改前 (BEFORE)

(no existing text; new section)

## 修改后 (AFTER)

## 3.4 The candidate-pool protocol

All wave-release policies studied in this paper are selection rules over one shared candidate pool. For each warehouse configuration, a combination of `F`, `|A|`, `E`, and a demand pattern (at publication scale: `F ∈ {3, 5, 8}`, `|A| ∈ {5, 15, 30}`, `E ∈ {1, 2}`, `c = 2`, and demand pattern ∈ {uniform, clustered, diurnal}, where clustered places 80% of demand on 20% of floors and diurnal places 70% of releases in a peak window covering 30% of the horizon; the fractional design over these factors is described in Section 5.1), an order pool of 600 orders is drawn from the configuration's demand pattern, and 3,000 candidate waves of a fixed size are sampled uniformly from that order pool (wave sizes 8 and 30 in the decomposition and contest blocks, 16 in the model-chain block; all values publication scale).

Every wave-release policy in the Section 5 contest, from the random baseline `P0`, through the structured heuristics `P1` (destination-clustered composition), `P2` (low cross-floor count), `P3` (direction-balanced), and `P4` (temporally tight), to the `Φ`-corner rule `P5`, the SPO-Tree comparator `P6`, and the local-search reference `P7`, selects the waves it releases from this same pool. The quartile corners of Section 3.2 are likewise carved from this pool, and 200 selected waves per arm are evaluated by the engine. Rules that require fitting (the sign rule for `q_Φ` behind `P5`, and `P6`) are fit on a training sample of 200 simulated candidate waves.

The shared pool is what makes the contest fair: because every rule chooses from the same finite set of candidate waves, differences in realized makespan are attributable to the selection rule alone, not to differences in how candidates were generated. The full protocol, including pool sizes, arms, and acceptance gates, was fixed in a pre-registration signed before the production runs (Section 5.1).

## 理由 (RATIONALE)

对应任务要求的 3.4 小节与 panel_completeness required_additions 第 3 条的前半（因子水平、池规模需要有正文出处；分块与 aliasing 细节留给 §5.1，避免重复）。数值全部取自 `phase5_config.py`：ORDER_POOL_SIZE=600、CANDIDATE_POOL=3000、N_PER_ARM=200、TRAIN_SAMPLE=200、因子水平与 DEMAND_PARAMS，并按规则逐一标注 publication scale。P0-P7 的枚举与"共享候选池保证竞赛公平"的表述取自 `wave_policies.py` 模块文档与预注册 §3.4。战术规则一律称 wave-release policy，操作层不在此处出现，符合 TERMINOLOGY.md 第 5 节。

---

# 编辑 5: 新增 §3.5 Notation

## 修改前 (BEFORE)

(no existing text; new section)

## 修改后 (AFTER)

## 3.5 Notation

Table N summarizes the notation used in Sections 3 to 5. Formal statements in Section 4.2 index corners by `c`, following the theorem statements; per-trip capacity `c` always appears either with an explicit numerical value or inside the pair `(E, c)`, so the two uses are disambiguated by context.

**Table N. Notation.**

| Symbol | Meaning | Introduced |
|---|---|---|
| `F` | number of floors (publication scale: `F ∈ {3, 5, 8}`) | §3.1 |
| `A`, `\|A\|` | AMR fleet and its size (publication scale: `\|A\| ∈ {5, 15, 30}`) | §3.1 |
| `E` | number of shared freight elevators (publication scale: `E ∈ {1, 2}`) | §3.1 |
| `c` | per-trip elevator capacity (`c = 2` in the main grid; `c ∈ {2, 3, 4, 5}` in the capacity sweep) | §3.1 |
| `o = (s_o, d_o, r_o)` | order: source floor, destination floor, release offset | §3.1 |
| `W`, `n`, `t_W` | wave, its size, its release epoch | §3.1 |
| `M`, `ℳ` | elevator model and the model family `ℳ = {M1, M2, M3}` | §3.1, §3.3 |
| `C_max(W; M)` | wave makespan under model `M`: latest order completion minus `t_W` | §3.1 |
| `σ` | lognormal noise parameter of `M3` (`σ = 0.20` at publication scale) | §3.3 |
| `Φ = (C, I, T)` | three-dimensional wave representation | §3.2 |
| `C` | vertical spread: Shannon entropy of the floor-visit distribution; high `C` = activity spread across many floors | §3.2 |
| `I` | directional imbalance: `\|N_up − N_down\| / (N_up + N_down)` | §3.2 |
| `T` | temporal clustering: coefficient of variation of within-wave release offsets; 0 for unstaggered waves | §3.2 |
| `Q` | the corner partition of `Φ`-space; working instance the `2×2` quartile scheme `{HC·HI, HC·LI, LC·HI, LC·LI}` | §3.2 |
| `q` (formal statements: `c`) | a corner of `Q` | §3.2 |
| `q_Φ` | favorable corner: the corner the `Φ`-informed wave-release policy selects by the OLS sign rule | §3.2 |
| `m_q` | corner-conditional median makespan of waves from corner `q` | §4.1.1 |
| `m_0` | median makespan of a wave drawn at random from the unpartitioned pool | §4.1.1 |
| `q_max`, `q_min` | corners attaining the largest and smallest corner median, `argmax_q m_q` and `argmin_q m_q` | §4.1.1 |
| `UB` | oracle upper bound `(m_{q_max} − m_{q_min}) / m_0` | §4.1.1 |
| `LB` | `Φ`-informed lower bound `(m_0 − m_{q_Φ}) / m_0` | §4.1.1 |
| `GAP` | value of wave structure, `GAP = UB − LB = H_up + M_Φ` | §4.1.1 |
| `H_up` | structural ceiling `(m_{q_max} − m_0) / m_0`: partition-intrinsic, capacity-side, unrecoverable by any policy acting on `Φ` | §4.1.1 |
| `M_Φ` | policy-recoverable slack `(m_{q_Φ} − m_{q_min}) / m_0`; equals the decision loss of the `Φ`-induced corner choice in the predict-then-optimize sense (Theorem 1) | §4.1.1 |
| `s[·]` | monotone summary statistic of the makespan distribution (median in the main text) | §4.2.1 |
| `c*` | minimax corner: the corner the Model-Dominance Hedge Rule releases waves from | §4.2.1 |
| `ε` | per-wave dominance violation mass: `P[C_max(W; M2) < C_max(W; M1)]` | §4.2.3 |
| `F_{2}^{c}` | corner-conditional makespan distribution function under `M2` for corner `c` | §4.2.3 |
| `U_c(ε)` | one-sided worst-case median bound for corner `c`: `U_c(ε) = (F_2^c)^{-1}(1/2 + ε) − (F_2^c)^{-1}(1/2)` (Corollary 2) | §4.2.3 |
| `ρ_c` | Wasserstein-1 model-discrepancy radius for corner `c`: the `W_1` distance between the corner-conditional makespan laws under the nominal and dominant models, sizing the ambiguity ball in Theorem 2's distributionally-robust clause | §4.2.2 |

## 理由 (RATIONALE)

对应 panel_completeness required_additions 第 2 条（"Notation table in Section 3: all symbols"）。表中覆盖了任务清单列出的全部符号（Phi、C、I、T、q、Q、GAP、H_up、M_Phi、UB、LB、m_0、m_q、q_min、q_max、q_Phi、U_c(eps)、C_max(W;M)、rho_c、F、|A|、E、c），并补入 §4-§5 实际用到的 ℳ、s[·]、c*、ε、F_2^c、σ、t_W。M_Phi 一行按 TERMINOLOGY.md 的 regret 用语规则写成 "decision loss ... in the predict-then-optimize sense"，"SPO regret" 一词只留在 §4 的正式定理陈述中。表首加了一句 corner 下标 c 与容量 c 的消歧说明（§4.2 的极小极大式沿用定理文档的 c 记号），这是现有 §4 草稿遗留的记号冲突，见 open issues。

---

# 编辑 6: §5.1 开头一句与 §3 的一致性修正

## 修改前 (BEFORE)

来源: `f:/Paper 3/paper_draft/section5_draft_v0_1.md`, 约第 24 至 26 行:

> The event-driven simulator of Section 4 realizes the wave makespan
> `C_max(W; M)` under the three elevator models: `M1` (throughput aggregation),
> `M2` (true co-occupancy batching), and `M3` (stochastic batching).

## 修改后 (AFTER)

> The closed-form sequential simulator of Section 3 realizes the wave makespan
> `C_max(W; M)` under the three elevator models: `M1` (throughput abstraction),
> `M2` (true co-occupancy batching), and `M3` (stochastic batching).

## 理由 (RATIONALE)

新的 §3.3 明确声明评估引擎"explicitly not an event-driven concurrent simulation"（这也是 panel_completeness required_additions 第 1 条点名要求修正的错误标注："fix the Section 5.1 opener"）。若不同步修改 §5.1 的开头句，手稿将出现直接自相矛盾。同时把 "Section 4" 改为 "Section 3"（模型定义现已在 §3），并把 "throughput aggregation" 统一为 TERMINOLOGY.md 的规范名 "throughput abstraction"。注意：若另一修订任务同时改写 §5.1，以该任务为准，此编辑只需保证这三处（closed-form sequential、Section 3、throughput abstraction）不丢失。

---

# 附注（不属于任何单一编辑，供作者定稿时统筹）

1. **§4.1.1 的部分重复。** 现有 §4.1.1 开头再次介绍 2×2 四分位角点分割（"the working instance is the 2×2 quartile partition ..."）。§3.2 定稿后，§4.1.1 的这半句可缩为一个回指（例如 "Partition Φ-space by the quartile-corner scheme Q of Section 3.2"），并可顺带删去 §4 草稿 frontmatter 中 "the finite Φ-space partition is introduced in §4.1.1" 一句。本文档未直接改 §4，留作者决定。
2. **corner 记号统一。** §4.1 用 `q` 索引角点，§4.2 的正式陈述用 `c`（与容量 `c` 冲突）。§3.5 表中已按现状消歧；若作者愿意，将 §4.2 的角点索引统一改为 `q`（`q*`、`U_q(ε)`、`ρ_q`）是更干净的方案，但牵动定理文档与图 2 说明文字，工作量更大。
3. **`ρ_c` 的精确定义需作者核对。** 现有草稿中只有图 2 说明文字里出现过全局半径 `ρ = W₁(M1, M2)`；`ρ_c`（逐角点半径）是按 Theorem 2 的 DRO 从句合理外推的定义，请对照附录中 Theorem 2 的完整证明（`theorems_m5.md` 及其正式化版本）确认是逐角点还是全局半径，再定表中该行措辞。
