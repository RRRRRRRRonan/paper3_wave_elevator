---
title: "Paper §1–§3 Structural Documentation"
subtitle: "Wave Release Coordination under Vertical Resource Constraints in Multi-Story AMR Warehouse"
date: 2026-05-23
purpose: "为论文 Abstract 到 Section 3 的每一部分提供主要内容说明、作用定位、关键 claim 与 contributions 映射；作为后续 revision 的查阅参考。"
status: "对应 docx 当前定稿（2026-05-23）"
---

# Paper §1–§3 结构说明文件

## 全文 contributions 锚点

在阅读各部分内容前，先确立三条 contributions 的标准表述，后续每一部分的说明都会回引到这三条：

| 编号 | 名称 | 标准表述 |
|---|---|---|
| **C1** | Problem formulation | 把 wave release coordination 形式化为一个两阶段调度器，将战术层 wave composition 与运营层 AMR-elevator 调度解耦，并施加每趟电梯硬容量约束；该形式化整合了四个之前在文献中被分别处理的要素：wave composition、multi-story deployment、flexible AMR fleets、shared-elevator capacity |
| **C2** | Methodology | 开发两个解析工具，每个都以定理形式给出：Bound-and-Gap 分解定理（含 SPO regret 等价）+ Model-Dominance Hedge Rule（含 Wasserstein DRO 等价）；framework 定位为 **diagnostic rather than prescriptive** |
| **C3** | Managerial implications | 从两个工具分别得出两个运营层面的产出：(i) 结构化的"wave 设计价值账本"，把上界 H_up 与可恢复项 M_Φ 分开；(ii) 闭式分派策略，附带最坏情况损失上界表达式 U_c(ε) |

---

## 整体结构图

```
Abstract                                    [1 段]
   ↓
§1 Introduction                             [9 段]
   ├─ Para 1–2: motivation
   ├─ Para 3:   gap + literature touch + two structural findings
   ├─ Para 4:   two-tools preview (findings → methods)
   ├─ Para 5:   Contribution heading — Problem formulation (C1)
   ├─ Para 6:   Contribution heading — Methodology (C2)
   ├─ Para 7:   Contribution heading — Managerial implications (C3)
   ├─ Para 8:   reframing + operational implication
   └─ Para 9:   roadmap
   ↓
§2 Related Works                            [7 段]
   ├─ Para 1: framing（三步走）
   ├─ Para 2: 三本综述
   ├─ Para 3: 物理基础设施线（多层 AMR + 电梯群控）
   ├─ Para 4: wave/order batching 线（战术决策变量）
   ├─ Para 5: RL/数据驱动线
   ├─ Para 6: 三条方法学线（D1 / D2 / contrast）
   └─ Para 7: 收束
   ↓
§3 Problem Formulation                      [8 小节]
   ├─ Setup (双层分解)
   ├─ Sets and indexes
   ├─ Parameters
   ├─ Decision variable
   ├─ Assumptions A1–A5
   ├─ Structured-feature representation Φ
   ├─ Elevator models {M1, M2, M3}
   ├─ Objective function
   └─ Constraints
```

逻辑链：**motivation → gap → findings → methods → contributions（嵌入 novelty）→ formulation**。Abstract 是这条链的压缩版本（跳过 findings）；§1 是完整版；§2 支撑 gap；§3 落实 C1。

---

## 1. Abstract

**主要内容**

单段 abstract，按以下结构展开：

1. **Motivation**（前 2 句）：多层仓库 + AMR + 电梯成为 binding constraint；wave composition 决定下游调度难度。
2. **Gap statement**（第 3 句）：joint study 在文献中是 open research direction（用 hedged 表述 "appears to be"）。
3. **Formulation = C1**（第 4 句）：把这个 gap 形式化为 two-stage scheduler。
4. **Methods = C2**（第 5–7 句）：Bound-and-Gap decomposition theorem + Model-Dominance Hedge Rule；Φ=(C, I, T) 的三个轴名（vertical activity diversity, directional imbalance, temporal clustering）；hedge 部分附带 closed-form worst-case loss expression。
5. **Validation**（第 8 句）：pre-registered, publication-scale simulation study。
6. **Managerial outcomes = C3**（末句）：(i) 结构化价值账本 + (ii) 闭式 dispatch policy。

**作用**：用一段话把全文 motivation + gap + 三条 contributions 压缩呈现，供编辑和 reviewer 第一轮筛选。

**对应 contributions**：C1 + C2 + C3 全部覆盖。

**关键 claim 摘录**（英文原文，方便核对）：

> "The joint study of the coupling between wave composition and elevator capacity appears to be an open research direction in the multi-story AMR warehouse literature."

> "two managerial outcomes: from the decomposition, (i) a structural account of the value of wave design, separating a partition-intrinsic upper-tail component from a component a better policy can recover; and from the hedge rule, (ii) a closed-form dispatch policy that operators apply without identifying the true elevator model online, together with a closed-form expression for its worst-case loss against any model-specific optimum."

**一致性约束**：abstract 与 §3 必须用相同的 Φ 轴名（vertical activity diversity / directional imbalance / temporal clustering）；abstract 与 §1 contributions 段必须都说 "two managerial outcomes"。

---

## 2. §1 Introduction

### 2.1 Para 1–2 — Motivation（动机）

**主要内容**：

- Para 1：电商驱动 → 配送中心向城市靠近 → 土地受限 → 出现多层立体仓 → AMR 在每层做水平移动 + 共享电梯做层间移动 → **瓶颈从地面空间或机器人数量转移到电梯容量**。
- Para 2：运营商用 wave 来管理这个瓶颈，wave composition 决定了下游电梯需求强度；当前实践用启发式分批（按目的地楼层、按运输截止时间、按到达顺序）；wave 层是**最经济的瓶颈缓解杠杆**——重新分批不需要改变楼层布局或增加机器人。

**作用**：建立读者对 problem 的物理直觉，把"为什么这件事重要"讲清楚。这两段决定 reviewer 是否愿意继续读下去。

**对应 contributions**：motivates 全部三条，特别为 C1 铺垫"四个要素的整合"。

**关键 claim 摘录**：

> "The main bottleneck has shifted from floor space or the number of robots to elevator capacity"

> "the wave layer is the most cost-effective way to relieve a vertical bottleneck"

### 2.2 Para 3 — Gap + Literature Touch + Two Structural Findings

**主要内容**：分三层叠加。

第一层（gap statement）：
- 当前实践是启发式 → 提议建立一个把战术决策与运营后果联系起来的框架。
- 四个要素 "have been studied largely in isolation"（已 hedged）。

第二层（简短文献回顾）：
- Chakravarty 2025（lift 作为固定 wave 上的约束）
- Nicolas 2018（设备级 VLM batching）
- Wu 2024 + Tadumadze 2023（tier-captive RMFS）
- Qin/Scholz/Žulj（planar AMR fulfillment 的 cardinality 决策）
- 两条方法论线：SPO regret + robust scheduling under model uncertainty
- 总结："The wave–elevator coupling thus falls between three established threads rather than within any of them."

第三层（**两个结构性发现，这是 findings → methods 链的起点**）：
- **Finding 1**：wave composition 对 makespan 有"small but systematic effect"，方向 varies across regimes → framework must measure regime-conditional value.
- **Finding 2**：在 {M1, M2, M3} 这个 elevator model 家族下，per-wave 随机占优秩序以高经验频率成立 → 开启了无须在线模型识别的闭式决策规则的可能性。
- 注："Specific magnitudes and dominance frequencies are reported in Section 5"——这是一个 **forward-promise**，§5 必须如实兑现。

**作用**：把 motivation 收口为 gap，再把 gap 与 findings 衔接，为下一段两个工具的引入做铺垫。

**对应 contributions**：motivates C1（gap）+ motivates C2（findings 直接对应两个工具）。

**一致性约束**：
- "two structural features" 必须对应 §1 Para 4 的 "two analytical tools"；
- "Specific magnitudes ... reported in Section 5" 是 forward-promise，§5 必须报 D1-d 57/72 = 79.2%、D2-a 99.2%/96.0% 等具体数字。

### 2.3 Para 4 — Two-Tools Preview

**主要内容**：

- 第一句开门见山："We develop two analytical tools to address these features."
- 工具 1：**Bound-and-Gap framework** — 把 wave-structure 信息价值分解为两个非负分量（partition-intrinsic upper-tail + recoverable policy component）。
- 工具 2：**Model-Dominance Hedge Rule** — 闭式 dispatch policy，处理"哪个 elevator model 描述当前仓库"的不确定性，告诉运营商发哪一波，同时 bound the cost of being wrong。

**作用**：建立 findings → methods 的一对一映射——Finding 1 → Tool 1，Finding 2 → Tool 2。

**对应 contributions**：直接预告 C2（两个 tools）。

**改进建议**（之前讨论过的）：当前 Para 4 的 finding↔tool 对应是隐含的；可改成显式 "The first feature motivates the Bound-and-Gap framework; the second motivates the Hedge Rule"。

### 2.4 Para 5 — Contribution Heading: Problem Formulation (C1)

**主要内容**：

形式化 wave-release coordination problem 为 two-stage scheduler，**decouples** tactical wave composition from operational AMR-elevator execution，subject to a hard per-trip elevator-capacity bound。把四个要素 **integrates into a single coupled system**，使 wave-elevator interaction 显式化。

**作用**：C1 的正式声明段。

**关键区分**：
- "decouples" 指的是**决策层之间**（战术 vs 运营）
- "integrates" 指的是**问题要素之间**（四个 isolated threads 合在一起）
- 两者在不同层面，不矛盾

### 2.5 Para 6 — Contribution Heading: Methodology (C2)

**主要内容**：

- 两个工具各自以定理形式给出。
- Tool 1（Bound-and-Gap）：splits into partition-intrinsic upper-tail + recoverable policy component；**by equivalence**，policy 分量 = SPO regret of partition-constant predictor class（这是 D1 bridge）。
- Tool 2（Hedge Rule）：minimax-collapse under per-wave stochastic dominance；**by equivalence**，under chain dominance 等于 Wasserstein DRO 解（这是 D2 bridge）。
- **定位**：framework 是 diagnostic rather than prescriptive；characterizes value 而非提供 solver；honest 承认 local-search optimizer 在 §5 outperforms its policy realization。

**作用**：C2 正式声明段，包含两条 equivalence theorems 与诚实的 diagnostic-not-prescriptive 定位。

**关键 claim**：

> "We position the framework as diagnostic rather than prescriptive: it characterizes where structural information adds value and bounds the cost of model misspecification, but it is not proposed as a competitive solver for wave composition; a local-search optimizer outperforms its policy realization, and we report this gap honestly in Section 5."

**forward-promise**：§5 必须明确呈现 P5 vs P7 = 46.4% 的 gap，不能软化。

### 2.6 Para 7 — Contribution Heading: Managerial Implications (C3)

**主要内容**：

- 两个工具均经过 pre-registered simulation 验证。
- 从 Bound-and-Gap 得 (i)：跨 operating regimes 的结构性价值账本，把 partition-intrinsic headroom 与可由更好策略恢复的部分分开。
- 从 Hedge Rule 得 (ii)：闭式 dispatch policy，不需要在线识别真实 elevator model，附带 closed-form worst-case loss expression；policy 的有效范围延伸到 c=2 之外的 capacity regime。

**作用**：C3 正式声明段。

**forward-promise**：
- "policy's domain of validity extends beyond the low-capacity regime" → §5 必须报 c ∈ {2,3,4,5} 的 Supp-2 实验（已 PASS 99.7%/98%）。

### 2.7 Para 8 — Reframing + Operational Implication

**主要内容**：

- "Together, these contributions reframe wave release in multi-story AMR warehouses as a **structured engineering decision rather than a heuristic one**."
- 运营层面含义：现有的 warehouse 数据可以用来支撑一个 quantified account of where structured wave design adds value + the worst-case cost of model misspecification。

**作用**：在 contributions 段之后给一个高层价值表述，把三条 contributions 收束为一句对运营商可理解的话。

### 2.8 Para 9 — Roadmap

**主要内容**：标准章节路径图（§2 related literature → §3 formulation → §4 tools → §5 experiments → §6 discussion + conclusion）。

**作用**：导航。

---

## 3. §2 Related Works

### 3.1 Para 1 — Framing

**主要内容**：宣告 §2 的三步走结构——三本综述 → 四条 problem-class threads（multi-story AMR & EGC、wave/order batching、tier-captive RMFS、data-driven fleet coordination）→ 三条 methodological strands（含 D1 / D2 / structural contrast）。

**作用**：让 reviewer 在第一段就知道 §2 的逻辑骨架，避免读着读着不知道走到哪了。

### 3.2 Para 2 — 三本综述

**主要内容**：
- **Boysen, de Koster, Weidinger (2019)** *EJOR* — 电商时代的仓储综述
- **Azadeh, De Koster, Roy (2019)** *Transportation Science* — robotized/automated warehouse 综述
- **Pardo et al. (2024)** *EJOR* — order batching 最新 taxonomy

收尾用 hedged statement："Within the scope of these surveys, we have not found the multi-story wave–elevator coupling treated as a standalone problem class."

**作用**：用三本权威综述定位 gap，避免 reviewer 怀疑 gap 是 self-serving。

### 3.3 Para 3 — 多层 AMR + 电梯群控

**主要内容**：把物理基础设施这一线的工作"piecewise 而不 jointly"地列出来：
- Chakravarty 2025（lift 优化在 fixed wave 下）
- Crites & Barto 1998 + Tsai 2025（电梯群控）
- Azadeh, Roy, De Koster 2019（vertical robotic storage）
- Wu 2024 + Tadumadze 2023（tier-captive RMFS）

收尾：tier-captive 与 flexible AMR 的本质差别是"layer-level operations decouple"vs"layer-level operations are coupled through shared elevator"。

**作用**：建立 C1 motivation 的第一支柱——物理基础设施的相关工作存在，但各自只覆盖一部分。

### 3.4 Para 4 — Wave/Order Batching 作为战术决策

**主要内容**：把 wave/order batching 这一线的工作梳理完整：
- 经典：Gademann 2001（wave picking + makespan）、Bozer-Kile 2008、Bartholdi-Hackman 2019
- 同目标函数：Ardjmand 2018（multi-picker wave picking makespan）
- E-commerce 扩展：Rasmi 2022、Schiffer 2022、Haouassi 2022
- AMR 变体：Scholz 2017（JOBASRP）、Žulj 2022、Qin 2024（multi-tote）
- 设备级（adjacent not parent）：Nicolas 2018（VLM）、Boysen-Fedtke-Weidinger 2018（automated sorting）
- 总结：Pardo 2024 taxonomy 将这些工作归在 tactical layer，"what is new in our setting is that the tactical decision is evaluated against a shared vertical resource that serves a building-wide AMR fleet"

**作用**：建立 C1 motivation 的第二支柱——wave composition 作为决策变量的传统是单层的。

**关键引文**：本段是 §2 字数最多的一段，承担 wave picking 文献覆盖完整性的责任。

### 3.5 Para 5 — RL / 数据驱动 Fleet Coordination

**主要内容**：承认存在一条 alternative paradigm：
- Crites & Barto 1998（RL 电梯调度，奠基）
- Ma 2025（end-to-end DRL AMR task allocation）
- Dhanaraj 2025、Wen & Ma 2024、Wesselhöft 2022

定位：complementary rather than competing。两条理由：(1) Bound-and-Gap 的 diagnostic value 不能迁移到学得的策略；(2) Hedge Rule 不需要训练数据，可作为任何学得策略的部署基准。

**作用**：承认 RL 路线的存在，但同时把自己的解析路线定位为可互补的，避免 reviewer 用"用 RL 不就行了？"反问。

### 3.6 Para 6 — 三条方法学线（D1 / D2 / structural contrast）

**主要内容**：三条线，前两条是 bridge（D1, D2），第三条是 structural contrast：

- **第一条（D1 bridge）**：prediction-to-decision regret（Chenreddy-Delage 2024、Elmachtoub-Grigas 2020、Vera 2020）。Theorem 1 给这个 regret 一个 partition perspective：policy-slack 分量 M_Φ **equals** SPO regret of partition-constant predictor class。
- **第二条（D2 bridge）**：Wasserstein DRO（Blanchet-Murthy 2019、Gao-Kleywegt 2023、Mohajerin Esfahani-Kuhn 2018；底层 Delage-Ye 2010、Bertsimas-Brown-Caramanis 2011）。Theorem 2 表明在 chain dominance 下，minimax wave-corner selection **coincides with** Wasserstein DRO 解。
- **第三条（structural contrast）**：robust scheduling under parametric model uncertainty（Lu-Shen 2021、Wiesemann 2013）。本工作的不确定性是 structurally distinct models，不是同一 model class 内的参数变化。

**作用**：这是 §2 最关键的一段——把 D1/D2 显化为对现有 OR 方法论的延伸，给 C2 的 novelty claim 提供文献定位。

**一致性约束**：本段的 "equals" 和 "coincides with" 措辞要与 §4 Theorem 1 / Theorem 2 的结论严格对应，措辞不能比 §4 强。

### 3.7 Para 7 — 收束

**主要内容**：四条 problem-class threads 各覆盖一面、合起来不覆盖全；方法学线提供分析基础（前两条是 bridge，第三条是 contrast）；具体的 empirical findings 推到 §5/§6；接下来 §3 形式化、§4 开发工具。

**作用**：把 §2 收束并 hand-off 到 §3。

---

## 4. §3 Problem Formulation

### 4.1 Setup（前两段）

**主要内容**：
- 物理设定：F 层、E 部共享货梯、|A| 个 floor-bound AMR、每趟电梯至多 c 个 AMR、orders 在 horizon 上 arrive。
- 性能指标：wave makespan = 最后一个 order 被送达的时间。
- 两层分解：tactical（wave composition，本文焦点）+ operational（AMR-to-order assignment、boarding 顺序，委托给确定性策略 + 仿真器）。
- 两层通过 makespan 耦合。

**作用**：把 abstract / intro 描述的物理系统落到形式化定义的起点。

**对应 contributions**：是 C1 的核心载体。

### 4.2 Sets and Indexes

**主要内容**：O（orders）、F（floors）、A（AMR fleet）、E（elevators）、W（waves over horizon）、t（continuous time）、M = {M1, M2, M3}（elevator model set）。

**作用**：明确符号系统，避免后续混淆。

**一致性约束**：M 集合用 calligraphic 或确保和文中其他位置一致；|A| 是 fleet size、A 是 fleet 集合，注意区分。

### 4.3 Parameters

**主要内容**：按四类分组——
- 物理基础设施（deterministic）：F、|A|、|E|、c
- 时间参数（在 M1/M2 下 deterministic，M3 下 stochastic）：τ_s、τ_e、τ_d
- Order 属性：s_o（源楼层）、d_o（目标楼层，**允许 d_o = s_o 同层 order**）、r_o（释放时间）
- Wave-release 控制（运营商可设）：W_min、W_max、τ_ω、Δ
- 随机规格：σ_M3 ∈ {0.10, 0.20}

**作用**：把所有 model 输入参数显式列出。

**一致性约束**：同层 order 允许（d_o = s_o）这一点在 I(W) 的定义中要呼应（同层 order 从分子和分母都剔除）。

### 4.4 Decision Variable

**主要内容**：x_o ∈ {0, 1}，wave 包含指示符。运营层无决策变量（A1–A3 已固定调度策略）。本文 contribution 是上游战术层，运营层 lift-scheduling 已被现有工作（Chakravarty 2025）覆盖。

**作用**：明确"只有一个决策变量"，保持 §3 干净。

### 4.5 Assumptions A1–A5

**主要内容**：
- **A1** Single-order AMR carriage：每个 AMR 一次只运一单（parcel-scale 工业现状）
- **A2** Source-before-destination：硬物理约束
- **A3** Capacity-bounded FIFO boarding (default)：AMR 按到达顺序排队、按 capacity 上电梯；§5 评估 destination-clustered 替代方案作为 treatment factor（不升格为决策变量）
- **A4** Intra-floor travel collapsed into τ_s：不显式建层内拥堵
- **A5** Elevator model 是 warehouse 的固定属性、运营商在决策时未知：Hedge Rule 是对该 **epistemic uncertainty** 的回应

**作用**：明确 scope of validity。

**已知弱点**：A5 当前用 epistemic uncertainty framing（"运营商不知道哪个 M"），偏弱；推荐升级为 "robustness certificate" framing（"无论运营商相信哪个 M，闭式策略都附带 worst-case loss bound"）——见之前讨论过的修改建议。

### 4.6 Structured-Feature Representation Φ

**主要内容**：Φ(W) = (C(W), I(W), T(W))，三轴：

- **C(W)** = Shannon entropy（in natural log），axis name **"vertical activity diversity"**；over 源 + 目标楼层联合分布；C 高 = 楼层分布散；C 低 = 集中。**作为 conceptual measure of vertical activity，不是 [0,1] 上的标准化指标**。
- **I(W) ∈ [0, 1]** = directional imbalance；over cross-floor portion of W（同层 orders 从分子分母都剔除）；I 高 = 单向流；I 低 = 上下平衡。
- **T(W) ≥ 0** = temporal clustering = release time 的 coefficient of variation。T 高 = 时间集中爆发；T 低 = 时间均匀。

强调：Φ **不是独立决策变量**，是决策变量 {x_o} 的确定性函数。

**作用**：建立后续 §4 两个分析工具操作的特征空间。

**一致性约束**：
- C 轴名 "vertical activity diversity" 必须与 abstract 一致
- 同层 order 处理与 §3 parameters 中 d_o 定义一致

### 4.7 Elevator Models {M1, M2, M3}

**主要内容**：
- **M1**（throughput aggregation）：电梯抽象为一个 server with per-AMR throughput rate
- **M2**（true co-occupancy batching）：next c AMRs board together，realistic per-trip capacity / dwell / direction
- **M3**（stochastic batching）：M2 + per-trip duration 的 lognormal noise 在 σ_M3 量级

收尾："M1 and M2 are both well-attested in the warehouse OR literature; the structural disagreement ... is the methodological gap our Hedge Rule resolves."

**作用**：把 Hedge Rule 所面对的 "model class" 明确列出。

**一致性约束**：与 §2 Para 6 第三条线（structural model contrast）对应。

### 4.8 Objective Function

**主要内容**：min E[C_max(W; M, ξ)]，其中 ξ 是 operational randomness。在 M1 / M2 下 ξ 退化（deterministic makespan）；在 M3 下 ξ 收集 lognormal 扰动。保留 expectation 以使形式统一。**用 makespan 而非 average delivery time**——下一波要等当前波清空电梯容量才能启动。

**作用**：形式化目标函数；同时解释 makespan 的选择理由。

### 4.9 Constraints

**主要内容**：
- (2) cardinality bound：W_min ≤ |W| ≤ W_max
- (3) temporal feasibility：r_o ∈ [τ_ω, τ_ω + Δ]
- (4) horizon partition：每个 order 在整个 horizon 上恰好被一波 release。**§3 注明：we solve (1)-(6) one wave at a time，(4) 在跨波层面自动满足，本文余下部分的决策对象是 single wave's inclusion vector**。
- (5) binary indicator
- (6) per-trip capacity bound：**不作为形式化优化约束**，而是 A1–A3 调度策略下的 simulator-enforced invariant；|A| 同理

收尾段：(1)–(5) + invariants (6) + A1–A5 定义本问题；直接 enumeration 不可行 → §4 引入 Φ + 两个工具。

**作用**：完成 C1 的形式化收尾，并 hand-off 到 §4。

**一致性约束**：constraint (6) 的"simulator invariant 而非形式化约束"立场要与 A3 的 default policy 表述一致。

---

## 5. 跨章节一致性核对清单

下面这些是改一个地方就要同步改的其他地方。建议每次 revision 后过一遍：

### 5.1 术语统一

| 术语 | 标准 | 出现位置 |
|---|---|---|
| Φ 三轴名 | vertical activity diversity / directional imbalance / temporal clustering | Abstract, §3.6 |
| Managerial outcomes 数量 | **两个**（不是三个） | Abstract 末句, §1 Para 7 |
| Wiesemann 年份 | 当前 docx 写 2013，正式版应为 **2014** | §1 Para 3, §2 Para 6, References |
| Elmachtoub & Grigas 年份 | 当前 docx 不一致（line 13 写 2022、line 41 写 2020）| §1 Para 3, §2 Para 6, References |

### 5.2 Forward-Promises（§1–§3 中欠 §4–§6 的债）

| 出处 | 承诺 | §5/§6 必须兑现 |
|---|---|---|
| §1 Para 3 末 | "Specific magnitudes and dominance frequencies are reported in Section 5" | D1-d **57/72 = 79.2%**（near-miss by 1 cell, pre-reg 门槛 58/72）；D2-a **99.2% 平均 / 96.0% 最差**；D2-d **6/6 configs** |
| §1 Para 6（C2 段末） | "a local-search optimizer outperforms its policy realization, and we report this gap honestly in Section 5" | §5 必须有 P5 vs P7 = **46.4%** 的 gap 表 + honest commentary |
| §1 Para 7（C3 段末） | "the policy's domain of validity extends beyond the low-capacity regime" | §5 必须报 Supp-2 实验：c ∈ {2,3,4,5} 上 per-wave M2 ≥ M1 ≥ 99.7% 平均 / 98% 最差 |
| §3 A3（destination-clustered as §5 treatment） | A3 的 cluster 替代方案在 §5 评估 | §5 必须有 cluster vs FIFO 的对比；当前 Supp-1 显示 cluster 全局 +10.2% makespan 降低 |
| §2 Para 6（D1 bridge "M_Φ equals SPO regret"）| Theorem 1 的等价性 | §4 必须给完整证明；§5 D1-c 在 72/72 cells 上验证 |
| §2 Para 6（D2 bridge "coincides with Wasserstein DRO"）| Theorem 2 的等价性 | §4 必须给完整证明；§5 D2-d 在 6/6 configs 上验证 |

### 5.3 Findings → Methods → Contributions 映射

| Finding | Method | Contribution component |
|---|---|---|
| Finding 1（wave structure value varies across regimes）| Tool 1 = Bound-and-Gap | C2 first half + C3 outcome (i) |
| Finding 2（per-wave stochastic dominance with high freq）| Tool 2 = Hedge Rule | C2 second half + C3 outcome (ii) |

### 5.4 已知的 framing 弱点（建议改）

- **§3 A5 当前用 "epistemic uncertainty" framing**：偏弱；建议升级为 "robustness certificate" framing（在限定 model family {M1, M2, M3} 内、附带闭式 U_c(ε) 上界）。这一改动同时会影响 §1 Para 4 Tool 2 的描述与 §1 Para 7 C3 outcome (ii) 的表述，三处需同步修改。
- **§1 Para 4 finding↔tool 对应未显式**：建议加 "the first feature motivates the Bound-and-Gap framework; the second motivates the Hedge Rule" 这种明确的一对一映射句。

---

## 6. 这份文件怎么用

1. **Revision 时**：改任一段前，先到本文件查该段的"主要内容"和"对应 contributions"，确保改完后这两件事仍然成立。
2. **检查 forward-promise 时**：§4–§6 落地后，回到 §5.2 核对每一条承诺是否兑现，特别是 D1-d 79.2% 和 P5 vs P7 46.4% 这两个 honesty acid test。
3. **审稿人回应时**：reviewer 提到任何一段，能从本文件快速定位该段的设计意图和与 contributions 的关系。
4. **后续作者（合作者 / 师弟师妹）阅读时**：直接看本文件比看 docx 更快理解全文骨架。

---

**文件状态**：对应 docx 当前定稿（2026-05-23）。如后续 §1–§3 文本有修改，请同步更新本文件。
