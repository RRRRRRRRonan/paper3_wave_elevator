# Reading Log: Boysen, Schneider & Žulj (2025) — VERIFIED

**Full citation**: Boysen, N., Schneider, M., & Žulj, I. (2025). Energy management for electric vehicles in facility logistics: A survey from an operational research perspective. *European Journal of Operational Research* (Invited Review, Article in Press). Received 14 Mar 2025, Accepted 17 Dec 2025. Published open access **CC-BY-4.0**.

**Placement**: `F:\paper3_wave_elevator\papers\reading_log_boysen_schneider_zulj_2025.md`
**Read date**: 2026-04-24（Claude full-text 精读 via PDF）
**Relevance rating for Paper 3**: ⭐⭐⭐（secondary positioning anchor；AMR survey reference；**不提供**wave composition 或 multi-storey coordination 的 flag）
**Status**: **VERIFIED** — 精读完整版本

---

## 0. 与"50 years"综述的区分（关键）

⚠ 这篇**不是** Boysen & de Koster (2025) "50 years of warehousing research"（那篇 DOI 10.1016/j.ejor.2024.03.026，EJOR 320(3) 449–464）。这两篇**是两本不同的 EJOR 综述，由重合的作者群在 2025 年前后发表**：

| 维度 | Boysen & de Koster 2025（50-years）| Boysen, Schneider & Žulj 2025（Energy）|
|---|---|---|
| **Topic** | Warehouse OR 50 年演化（通用 warehouse 综述）| Electric vehicles 在 facility logistics 中的能源管理 |
| **Scope** | 所有 warehouse 问题类 | 聚焦 energy 维度 across vehicle types |
| **Classification** | 三代演化（basic / extended / robotized）| 按 vehicle type（towing truck / crane / forklift / tugger train / AGV+AMR / drone）|
| **Research agenda** | Warehousing 未来方向（可能 flag multi-storey AMR coordination）| Energy-specific 未来方向（节能、充电、混合策略）|
| **Paper 3 positioning** | **Primary anchor**（若拿到 PDF 可验证情形 A/B/C）| **Secondary anchor**（AMR survey reference + Žulj 2022 forward citation 入口）|

**现状**：papers/ 仅有这篇 (Energy)，50-years 的 PDF 未收到 —— 详见 [reading_log_boysen_dekoster_2025.md](reading_log_boysen_dekoster_2025.md)（stub，保留待用户补 PDF）。

---

## 1. Problem — 这篇的覆盖范围

**Scope（§2）**：
- **Facility logistics** = 厂内/仓内/港内 material handling（对比 public roads）
- **Electric vehicles** = battery-electric（排除 permanent power grid 的 crane 等）
- Vehicle types surveyed: towing truck / crane+forklift / tugger train / AGV+shuttle+AMR+pallet truck / drone
- **Energy aspects** = energy demand + energy supply + their impact on classical logistics decisions

**Framework（Fig. 1 radar chart）**：
- (a) Decision tasks: fleet sizing / routing / path planning / charging device location / sizing / scheduling
- (b) Energy demand: job-related / flexible / constant + intra-day / inter-day
- (c) Energy supply: battery swap / plug-in / inductive + restricted / unlimited capacity + linear / non-linear charging
- (d) Solution methods: analytical / queuing / machine learning / deterministic / stochastic / simulation

**Four contributions**（§1 原文）：
1. Classify OR literature on energy-aware decisions for common vehicle types
2. Identify 尚未被处理的 research gaps per vehicle category
3. Cross-vehicle perspectives (spillover effects)
4. Comprehensive future research agenda

---

## 2. Structure（章节与页码）

- §1 Introduction
- §2 Scope and framework of survey
- §3 Towing trucks
- §4 Lifting vehicles: Cranes and forklifts
- §5 Tugger trains
- **§6 Horizontal movement by AGVs, shuttles, AMRs, and pallet trucks** ← **对 Paper 3 最相关**
- §7 Drones
- §8 Literature summary and future research needs
  - §8.1 Problem-oriented research agenda
  - §8.2 Method-oriented research agenda
- Table 2: comprehensive literature table（每篇 reviewed paper 逐项标记）

---

## 3. Key content for Paper 3

### 3.1 §6 AMR-relevant references (verbatim 有用的 citation 入口)

综述提到的 AMR-related 工作（精读 §6）：
- **Muller 1983**: AGV 原型（1955 首次引入）
- **Fragapane et al. 2021** (*EJOR* 294(2), 405–426): planning and control of AMRs for intralogistics — literature review and research agenda
- **Löffler, Boysen & Schneider 2022** (*INFORMS JoC* 34(1), 440–462): Picker routing in AGV-assisted order picking
- **Löffler, Boysen & Schneider 2023** (*Transportation Science* 57(4), 979–998): Human-robot cooperation — coordinating autonomous mobile robots and human pickers
- **Boysen et al. 2023** (*EJOR* 307(3), 1374–1390): A review of synchronization problems in parts-to-picker warehouses
- **Azadeh, De Koster & Roy 2019** (*Transportation Science* 53(4), 917–945): Robotized and automated warehouse systems — review and recent developments
- **⭐ Žulj, Salewski, Goeke & Schneider 2022** (*EJOR* 298(1), 182–201): **Order batching and batch sequencing in an AMR-assisted picker-to-parts system** — **this is the exact Žulj paper the workdoc flagged**
- **Zou et al. 2018a** (*Transportation Science* 52(4), 788–811): Operating policies in **robotic compact storage and retrieval systems** — multi-tier vehicle-based warehousing
- **Tappia et al. 2017** (*Transportation Science* 51(1), 269–295): Modeling, analysis, design insights for shuttle-based compact storage — multi-tier

**§6 原文关键段落**（Paper 3 定位用）：
> "AMRs based on sensors and machine vision allow a flexible adaption of travel paths in a dynamic environment (Fragapane et al., 2021). ... The next evolutionary stage is AMRs ... other material-handling vehicles applied in picking processes, where products demanded by customer orders are collected from multiple storage positions."

**观察**：§6 不讨论 multi-storey AMR 或 wave composition，但提供了 Paper 3 需要的 Žulj 2022 完整引用。

### 3.2 §8 Future research agenda — 对 Paper 3 的 flag 程度

**§8.1 Problem-oriented agenda**（§8.1 原文 verbatim）：
- **Layout design**
- **Storage assignment**
- **Job selection**: "which to transform this add-on flexibility into significant energy savings remains a challenging research task"
- **Job preemption**: "systematic evaluation of the possible energy savings enabled by preemptive transport job processing is a valid task for future research"

**§8.2 Method-oriented agenda**：
- Enhanced simulation optimization
- Enriched queuing networks
- Machine-learning-enhanced combinatorial optimization

**⚠ 关键观察**：这篇综述**不显式 flag** multi-storey AMR wave composition 或 elevator coordination。它的 future research agenda 聚焦：
- Energy-specific angles (charging strategies, energy savings)
- Cross-vehicle planning problems
- Methodological complexity of integrating energy-aware objectives

对 Paper 3 而言，§8 **不是直接可用的"open agenda 权威背书"**。如果我们要 positioning anchor 说"multi-storey AMR wave composition 是 flagged open agenda"，需要 Boysen & de Koster 2025 (50-years) 那一篇（PDF 未到）。

### 3.3 Cross-vehicle insights 对 Paper 3 可借鉴的一条

**Spillover effects between public road transport and facility logistics** (§1 & §8)：
- Facility logistics 有 closed control (central fleet management), public roads 没有
- 这暗示 tactical coordination 在 facility logistics 里有可能，在 public roads 里没机会

**对 Paper 3 的类比**：我们的 multi-storey warehouse 也是 closed control setting，tactical wave composition 在这里是可实现的 operational lever。这是一个弱 positioning 语言（"similar to how centralized control in facility logistics enables tactical coordination, ..."）但可用。

---

## 4. Relevance to my Paper 3 — 总体定位

### 4.1 这篇的作用：**secondary** anchor

直接价值：
1. **Žulj 2022 的完整 citation 入口** —— 这是 Paper 3 planar AMR-OB 线的关键 reference
2. **AMR survey 语言**（§6 的 taxonomy / terminology 可 borrow 作 intro-side 中性 wording）
3. **作者权威**（Boysen 是 warehousing OR 顶级作者之一）

**不能**做的事：
- ❌ **不能**作为"multi-storey AMR wave composition 作为 open agenda" 的 flag —— 他们没写
- ❌ **不能**支撑情形 A/B/C 的任何一种 positioning 语言 —— 他们不谈 wave composition
- ❌ **不能**作为 §1.2 intro 的 hook —— 他们是 energy survey，与 Paper 3 的 makespan-coordination topic 轴不同

### 4.2 Paper 3 里怎么用它

**§3 Related Work 里**（不在 §1.2 intro 里）提一句：
> "The recent invited review by Boysen, Schneider, and Žulj (2025) surveys OR approaches for energy management across facility-logistics vehicle types, including AMRs; while energy aspects are outside our scope, their review positions AMR fleet coordination as an active direction."

这句话**诚实**：我们不 claim 他们 flagged 我们的问题；我们 claim 他们是 AMR fleet coordination 这个更宽 direction 的 authoritative survey。

**Žulj 2022 的引用** 应当放在 §1.1 / §1.2 planar thread（已完成）+ §3 Related Work 的 "Planar picker-to-parts" 行（已完成）。

### 4.3 如果之后拿到 50-years PDF

优先级：拿到 50-years 后，替换/升级 §3 Related Work 的 authoritative anchor 为 50-years（那篇对 warehouse class 演化的 classification 更直接对应 Paper 3 positioning）。当前这篇（Energy）降为 secondary reference。

---

## 5. What I can borrow

- **Žulj 2022 的完整 citation**（已 borrow 到 bib + §1.1/§1.2/§1.4/§3 outline）
- **"Facility logistics" 语汇** 作为 multi-storey warehouse 的 categorical name（Paper 3 v0.2 可考虑用）
- **§6 的 AMR sub-taxonomy**（AGVs vs shuttles vs AMRs vs pallet trucks）—— Paper 3 §4.1 可 explicitly position 为 "AMR fleet"（flexible, non-captive）而非 "shuttle"（tier-captive）

---

## 6. What I must NOT do with this paper

1. ❌ **不要**用这篇作为 Paper 3 §1.2 opening hook —— topic 不匹配 (energy vs makespan-coordination)
2. ❌ **不要**声明他们 flagged multi-storey AMR coordination —— 他们没有
3. ❌ **不要**混淆它与 50-years survey —— 它们是两篇

### 6.1 审稿人预案

**Q**: "Paper 3 为什么不引 Boysen-Schneider-Žulj 2025 的 energy management survey？"

**A**: 引了 —— 在 §3 Related Work 的 "AMR fleet coordination" 相关段落里提及；但 energy 维度在 Paper 3 scope 之外（我们的 objective 是 makespan，不是 energy consumption），所以 intro §1.2 不 hook 这一篇。

**Q**: "那你们为什么不引 Boysen & de Koster 的 50-years 综述？"

**A**:（v0.1 草稿时点）—— 50-years PDF 当前未收到，等用户完成 download 后精读再更新 §3 Related Work positioning anchor。**当前 intro 不依赖这篇 anchor**（lean-intro 原则）。

---

## 7. Open questions

1. §8.1 Problem-oriented agenda 是否在 "Job selection" 段落暗示了 batching/grouping decision？—— 精读 §8.1 第 (iii) 子节确认："job selection" 讨论的是 **to perform or delay a job**（timing），不是 "which orders to co-release"（composition）—— 所以不构成对 Paper 3 的 open-agenda flag
2. §6 末尾谈到 "congestion ... affected by warehouse layout" —— 这与 Paper 3 §8 L1（simulator-only, no real warehouse data）的 future work 有联系
3. §8.2 ML-enhanced combinatorial optimization —— 暗示 Paper 3 future work 可以把 Φ-informed corner selection 改造为 ML-oracle version

---

## 8. Key takeaways

- ⭐ **Žulj 2022 的完整 citation 是这篇最大价值**（已用到 Paper 3）
- 作为 positioning anchor **弱**（energy vs coordination 不同轴）
- Paper 3 当前 §1.2 已按 lean-intro 原则**不 hook** 这篇；§3 Related Work 或 §7 Discussion 可做 secondary reference
- 如果未来 50-years PDF 到位，primary anchor 位置让给 50-years；这篇保留为 secondary

---

## 9. Log of revisions

- **v0.1 (2026-04-24)**: 初稿 by Claude，精读全 16 页（§1–§8 + Table 2 + references）完成。§0 建立与 50-years 的 disambiguation；§1–§3 精读内容 verified；§4.2 确认 Paper 3 当前 lean-intro 策略正确（不 hook 此篇）。

---

**End of Boysen, Schneider & Žulj 2025 (Energy) reading log v0.1 (verified)**
