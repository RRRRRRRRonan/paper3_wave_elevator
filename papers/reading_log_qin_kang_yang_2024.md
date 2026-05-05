# Reading Log: Qin, Kang & Yang (2024) — VERIFIED

**Full citation**: Qin, Z., Kang, Y., & Yang, P. (2024). Making better order fulfillment in multi-tote storage and retrieval autonomous mobile robot systems. *Transportation Research Part E: Logistics and Transportation Review*, 192, 103752.

**Placement**: `F:\paper3_wave_elevator\papers\reading_log_qin_kang_yang_2024.md`
**Read date**: 2026-04-24（Claude full-text 精读 via PDF）
**Relevance rating for Paper 3**: ⭐⭐⭐⭐⭐（**最危险的 neighbor** —— 显式用 "wave" 术语 + 报告 "100 orders/wave" finding + 发在 Paper 3 reach target 期刊 TRE）
**Status**: **VERIFIED** — stub 已替换为精读后的内容

---

## 1. Problem — MTSRSP in MTSR AMR System

**Problem name**：Multi-workstation Order and Tote Sequencing and Robot Scheduling Problem (**MTSRSP**)

**System**（Fig. 2 确认 **single-layer** dual-block）：
- **Multi-Tote Storage and Retrieval (MTSR)** AMR system — AMR with multi-tote carry capability
- 多 workstation，每个 workstation 有 put wall (capacity C_w) + conveyor + picker
- Robot 有 buffer positions (capacity C_r tote per tour)
- Aisle width 2.5m, horizontal aisle 2m
- Robot speed 1.4 m/s（considering accel/decel）
- **无电梯**，**单层建筑**（Fig. 2 没有任何 vertical transition）

**Three major decisions（joint）**：
1. Orders → workstations assignment + sequencing
2. Tote sets → workstation sequencing (每 tote set 对应一次 robot tour)
3. Robot scheduling (which robot carries which tote set in what sequence) + routing (storage→workstation)

**Objective**: minimize makespan (完成 wave 内所有订单的总时间)

**🔑 显式使用 "wave" 术语**（这是对 Paper 3 最重要的发现）：

> "Order arrival: Orders arrive continuously. Order fulfillment is completed in **waves**. After completing the order fulfillment for the current wave, the succeeding wave is initiated"（§3.1）

> "The wave order O comprises four distinct orders"（§4.1.1）

> "vary both the total number of orders in a **wave**"（§5.4.3）

---

## 2. Method

### 2.1 MIP formulation (§3.2)
- 30 约束、~10 变量族
- Makespan objective: min C_max
- **|B| pre-set**: wave 内 tote set 数量是 parameter 不是 decision variable
- Linearize 非线性约束 (11)→(15)(16)(17)

### 2.2 I-ALNS heuristic (§4)

**三层结构**：
- Stage 1 (ISPDM)：Item Similarity and Popularity-Driven Method — greedy 构造 order sequence
- Stage 2 (IPDM)：Item Popularity-Driven Method — 给定 order sequence 生成 tote sequence
- Stage 3 (GA)：Genetic Algorithm — robot scheduling 给定 tote sequences（FJSP 类比）
- ALNS outer loop：destroy/repair operators on order sequence

**Destroy/repair operators**：
- Random / Fewest / Worst destroy
- Random / ISPDM / Greedy repair
- 100 iterations max，SA acceptance criterion

### 2.3 Numerical experiments (§5)

**Setting**：第三方物流公司 Shenzhen，B2C 订单（77.6% 单 line, 17.8% 双 line, 4.6% 三 line+）；7 天 × monthly 抽样

**12 instance groups**：SI1-SI4 (4-10 orders, 小), MI1-MI4 (15-50), LI1-LI4 (80-200)

**Comparison**: Gurobi (1800s cap) vs ISPDM/GA vs I-ALNS vs FCFS/UA (real warehouse rule)

---

## 3. Result — verified key numbers

### 3.1 Small scale (SI1-SI4) — I-ALNS vs Gurobi
- I-ALNS **matches Gurobi's optimal** within seconds (Gurobi 需要 2.5-200s)
- Gap range 0-1.85% to optimal

### 3.2 Medium scale (MI1-MI4)
- Gurobi 1800s timeout fails on MI3/MI4
- I-ALNS beats Gurobi by 10.76-14.24% when Gurobi does find feasible

### 3.3 Large scale (LI1-LI4) — I-ALNS vs FCFS/UA real rule
- **50.2% makespan reduction** in LI2 (120 orders) — this is the abstract-level headline claim
- Range: 44.65-50.20% across 8 large instance configurations

### 3.4 ⚠ **KEY managerial insights**（§5.4）

**(a) Robot number + buffer positions (§5.4.1)**：
- 10 robots × 8 buffers vs 2 robots × 2 buffers: makespan reduction from ~3335s → 907s (fourfold)
- **Buffer expansion alone**: 2→8 buffers on same 10 robots = **55.4% makespan reduction**
- Managerial insight: "enhancing buffer capacity more cost-effective than increasing fleet"

**(b) Workstation and put wall (§5.4.2)**：
- Put wall capacity from 2→5 boxes: strong effect
- Put wall capacity >10: additional workstations stop helping
- Workload balance ratio τ: **minimal impact** on makespan

**(c) ⚡ "Optimal wave size ≈ 100" (§5.4.3, Fig. 8)**：
- 原文（§5.4.3）: *"In the scenario with 10 robots, better order fulfillment performance is observed with order numbers ranging from 80 to 100"*
- 原文（§5.4.3）: *"in the scenario with 16 robots, the highest order fulfillment efficiency is achieved with order numbers between 100 and 120"*
- 原文（§6 Conclusion，managerial bullet）: *"setting the number of orders per wave to 100 can improve order fulfillment performance"*
- ⚠ **这是 Paper 3 工作文稿中 "empirically optimal wave size around 100 orders" 的真正来源** —— 来自 Qin 2024，不是 Scholz 2017

**(d) Warehouse layout (§5.4.4)**：
- 20×30 (aisles × storage, ratio 2.4) vs 6×100 (ratio 0.2): **26.3% makespan reduction** for 200 orders
- Managerial insight: "wider warehouse layouts are more efficient than narrow, elongated ones"

---

## 4. Relevance to my Paper 3

### 4.1 为什么这篇是 **最危险** 的 neighbor

三点叠加：
1. **显式用 "wave" 术语** —— 审稿人第一反应"你们和 Qin 都研究 wave 啊"
2. **发在 TRE**（Paper 3 的 reach target 期刊）
3. **报告 "100 orders/wave" 作为 managerial insight** —— 看起来和 Paper 3 的"wave structure"相关

### 4.2 Structural 差异（精读后，确认 4/5 维度差异存在）

| 维度 | Qin 2024 | Paper 3 |
|---|---|---|
| **Setting** | **Single-layer dual-block**（Fig. 2 无 elevator）| **Multi-storey** F∈{5,7,9} |
| **Vertical resource** | ❌ 无 | ✅ Shared elevator (binding) |
| **AMR type** | Multi-tote carry (C_r totes/tour) | Single-tote ride (1 order/elevator trip) |
| **"Wave" meaning** | **Processing batch size**（cardinality parameter）| **Tactical composition decision on Φ = (C, I, T)** |
| **Decision scope** | Order-to-workstation assignment + tote sequencing + robot scheduling（single-stage MIP）| Wave composition (tactical) + AMR–elevator dispatch (operational)（two-stage）|
| **Feature representation** | 无（订单直接由 item 类型决定）| Φ = (vertical concentration, directional imbalance, temporal clustering) |
| **"Optimal 100" nature** | **Cardinality optimum** —— 每 wave 多少 orders | 我们不研究 cardinality；研究 composition 的 corner selection |

### 4.3 一句话差异

> Qin et al. 2024 在 **single-layer multi-tote AMR** 系统中，联合优化 order-to-workstation assignment + tote sequencing + robot routing；他们的 "wave" 是 **processing batch**，report wave **size ≈ 100** 作为 cardinality optimum。
> Paper 3 在 **multi-storey AMR + shared elevator** 系统中，研究 wave **composition** 作为 tactical decision variable（which orders to co-release, on Φ = (C, I, T) structured features），目标是 makespan。
> **核心 delta**: (1) Qin 是 cardinality 参数化 + single-layer；我们是 composition 决策 + multi-storey + elevator coupling。(2) Qin 的 managerial map 在 fleet/buffer/workstation/layout 轴；我们的 map 在 tactical-operational 轴。

### 4.4 Qin 的局限 ↔ Paper 3 的机会

1. **Single-layer only** — multi-storey 问题他们不讨论
2. **"Wave" 作为 size parameter** — 没有讨论 wave 内部的 compositional structure（哪些 orders 一起）
3. **无 structured feature 分解** — 他们的"order characteristic" 只是 item 类型 × 单/双/三 line order 比例，没有 Φ-like 的 decomposition
4. **Managerial map 在 resource-sizing 轴** — fleet/buffer/workstation/layout；不在 tactical-operational 轴

---

## 5. What I can borrow

- **"100 orders/wave" 作为 planar MTSR benchmark** —— Paper 3 §6 或 §7 可引用为"对比基线：在 single-layer MTSR 下 cardinality 最优 ≈ 100；我们的 multi-storey setting 的 optimal wave size 结构不同（因为 elevator binding 改变 rule）"
- **I-ALNS framework** 作为 Paper 3 v0.5 scale-up 的 heuristic 候选（他们的 item-popularity-driven 可以改造为我们的 Φ-driven）
- **B2C order mix**（77.6% 单 line / 17.8% 双 / 4.6% 三+）—— Paper 3 future data calibration 可借 this 分布

---

## 6. What I must differentiate from

### 6.1 Paper 3 §1.2 现行 wording（verified 精读后 sharp 了）

§1.2 现在这样写（修订后）：
> "Concurrent work on planar multi-tote AMR fulfilment [Qin et al., 2024] uses the term *wave* for processing batches and identifies an operational optimum near 100 orders per wave in single-layer settings — a wave-**cardinality** finding. We instead study wave **composition** on structured features Φ as a tactical decision variable in the multi-storey setting, a distinct object."

这句话 explicitly call out："我们也用 wave 一词；他们的 100 是 cardinality；我们做的是 composition；这两个是 distinct objects"。

### 6.2 审稿人预案

**Q**: "Qin 2024 已经研究 wave 了，也给出了 '100 orders/wave' 的 insight，Paper 3 novelty 在哪？"

**A**: Qin et al. 的 "wave" 是 **processing batch**（一个 wave 等于一批并发处理的 orders），他们的 insight 是 **cardinality optimum**（"wave 里放 100 个 orders 最好"）。这是一个 **sizing 决策** —— 类比"fleet sizing"。

我们的 "wave composition" 是 **哪些 orders 被放入一个 wave 里**，作为 tactical decision variable，在 structured features Φ = (vertical concentration, directional imbalance, temporal clustering) 空间做 corner selection。这是 **composition 决策** —— 类比 "portfolio composition"。

两件事的数学对象完全不同：cardinality 是标量参数，composition 是 set-valued decision variable on structured features。此外他们的 single-layer 设定没有 elevator binding constraint —— 这恰好是 Paper 3 的 problem class 的 defining 特征。

**Q**: "Qin 报告 buffer/robot/workstation 的 managerial map，Paper 3 的 substitutability map 不就是同一类 insight？"

**A**: 不同 axes：
- Qin 的 map 在 **resource-sizing axes**（多少 robots / 多少 buffers / 多少 workstations / 什么 layout ratio）
- Paper 3 的 map 在 **tactical-operational axis**（tactical wave design vs operational dispatch 的 substitutability）

两者是 **orthogonal** 的 managerial dimensions。Paper 3 的 map 只在 elevator binding 存在时才有意义（单层无 vertical coupling 时 tactical lever 消失）。

---

## 7. Open questions about their work

1. 他们的 "100 orders/wave" 是对 makespan normalized by order count 的最优；绝对 makespan 仍然随 order 数上升 —— 这与 "wave 越大越好" 的直觉背离，值得深入
2. 他们没有 stagger 内部分析（所有 orders 同 wave 内视为 tight-release），与 Paper 3 §8 L3 stagger 讨论平行
3. Appendix A（GA details）未读；未来想用 I-ALNS 做 scale-up baseline 时可补读

---

## 8. Key takeaways

- ⭐ **最危险 neighbor**，因为 "wave" 术语重叠 + TRE 发表 + 有具体数字。但差异化干净（cardinality vs composition + single-layer vs multi-storey）。
- **"100 orders/wave" 来源已确认为 Qin 2024** —— 原工作文稿归到 Scholz 2017 是 misattribution，paper 正文当前修订已正确
- Paper 3 的 §1.2 当前 wording 已 sharp 出 cardinality vs composition 的差异
- §7 Discussion 已加入显式对比句（outline 已改）

---

## 9. Log of revisions

- **v0.1 (2026-04-24, AM)**: Stub by Claude，未精读
- **v0.2 (2026-04-24, PM)**: **VERIFIED** — 精读 23 页全文后补所有具体数字 + 确认 "100 orders" 来源；§6.1 确认 Paper 3 现行 wording 正确

---

**End of Qin, Kang & Yang 2024 reading log v0.2 (verified)**
