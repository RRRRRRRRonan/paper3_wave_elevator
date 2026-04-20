# Reading Log: Lenoble, Frein & Hammami (2018)

**Full citation**: Lenoble, N., Frein, Y., & Hammami, R. (2018). Order batching in an automated warehouse with several vertical lift modules: Optimization and experiments with real data. *European Journal of Operational Research*, 267(3), 958–976. DOI: 10.1016/j.ejor.2017.12.037

**Read date**: 2026-04-20（初读）| 2026-04-__（精读待补）
**Relevance rating for Paper 3**: ⭐⭐⭐⭐⭐（最重要的前沿工作之一，必须精确定位）
**Status**: Draft — by Claude，待我精读后补充标注和修正

---

## 1. Problem

**他们在研究什么？**

在配备 Vertical Lift Module（VLM）的仓库中做 order batching。具体场景：

- VLM 是一种 AS/RS，结构是一排垂直排列的 tray（抽屉），一个机械提取臂（lift）可以把指定的 tray 送到 picker 面前
- Picker 站在 VLM 前不动，所有商品由机械臂送到他面前
- 一个仓库可能有 1–4 台 VLM 并排放置
- 问题：给定一组 customer orders，如何把这些 orders 分成若干 batch，使得总 completion time（picker 完成所有 order 的总时间）最小

**为什么有意思？**

这是一个真实工业问题。法国医院、瑞士精密仪器公司的实际 WMS 在用这个方法做 batching。Lenoble 的 PhD 是跟 KLS Logistic Systems（法国一家 WMS 公司）做的 industrial CIFRE PhD。

**问题的关键结构**：
- 每个 order 由若干 order lines 组成；每个 order line 要从某个 tray 取某个 product
- Picker 要等 tray 被机械臂送出来才能取货（waiting time）
- 多台 VLM 允许 "masked time"（picker 在一台 VLM 取货时另一台机械臂在换 tray）
- 同一 tray 如果服务多个 order → 减少 tray visit 总数 → 减少 completion time

---

## 2. Method

### 2.1 理论核心：等价性定理

**Proposition 1（单 VLM）**：最小化 total completion time **等价于**最小化所有 batch 的 tray visit 总数 $\sum_{b} K^b$。证明基于 picker 始终在等 tray 这一事实，所以 completion time 本质上是 tray 访问次数 × 单次换 tray 时间。

**Proposition 2（多 VLM，可忽略 picking time）**：最小化 total completion time **等价于**最小化"每个 batch 内访问 tray 数最多的那台 VLM 的 tray 数"之和 $\sum_b K_1^b$。关键洞察：multi-VLM 场景下 masked time 可以掩盖部分 waiting time，所以 makespan 被"最忙的那台 VLM"主导。

**Proposition 3（多 VLM，per-tray picking time 正比于 lines）**：这种情况没有简单等价性，但作者证明 $\sum_b K_1^b$ 与 completion time **正相关**，因此仍可作为优化目标。

**这是他们整个工作的数学支柱**——它把一个复杂的 completion time 最小化问题 **归约** 为一个标准的组合优化问题（最小化 tray 数）。

### 2.2 MILP 模型

**决策变量**：
- $x_{nb} = 1$ 如果 order $n$ 在 batch $b$
- $T_{kb} = 1$ 如果 tray $k$ 被 batch $b$ 访问（单 VLM 情形）
- $T_{kvb} = 1$ 如果 VLM $v$ 的 tray $k$ 被 batch $b$ 访问（多 VLM 情形）

**约束**：
- 每个 batch ≤ $S$ 个 orders（S 是 batch size，由 picking area 物理决定）
- 每个 order 恰好在一个 batch
- Tray 变量由 order 分配决定（线性约束）

**目标函数**：
- 单 VLM：minimize $\sum_b \sum_k T_{kb}$
- 多 VLM：minimize $\sum_b \max_v (\sum_k T_{kvb})$（后者需要线性化技巧）

### 2.3 Metaheuristic

对于大规模 instance（60+ orders），Cplex 求解太慢。作者测试了 SA、Tabu Search、GA，**最终选择 Simulated Annealing**。

SA 的关键参数：
- 初始温度 $T_0 = 0.1$，终止温度 $T_F = 0.01$，降温因子 $0.9995$
- 初始解 = 公司当前的 batching 方法
- Neighbor move = SWAP（随机选两个 order 位置交换 batch 号）
- 停止条件 = 时间限制（1 min 或 5 min，KLS 公司的业务要求）

---

## 3. Result

### 3.1 Numerical results

**数据来源**：两家公司的真实数据
- 法国医院：S=6，V=1 or 2，7-10 天的 order log
- 瑞士精密仪器公司：S=8，V=1 or 4，7-11 天的 order log

**主要节省（vs 公司现有 "first come first served" 方法）**：

| 场景 | 公司 | CT1（忽略 picking）| CT3（真实 picking p=0.2r）|
|---|---|---|---|
| 1 VLM | 法国医院 | 33% | 27% |
| 1 VLM | 瑞士公司 | 27% | 22% |
| 多 VLM | 法国医院 | 40%+ | 32% |
| 多 VLM | 瑞士公司 | 30%+ | 24% |

**规律发现**：
- **Insight L1**：订单数越多 → 节省越大（因为"兼容订单"的概率上升）
- **Insight L2（反直觉！）**：订单的 line 数越多 → 节省**越小**（line 多 → 每个 order 跨越 tray 多 → 兼容性下降）
- **Insight L3**：多 VLM 场景节省大于单 VLM，因为 masked time 利用更充分

### 3.2 Metaheuristic 性能

- SA 跑 1 分钟 → 平均 Efficiency Rate = 100.71%（比 Cplex 跑 1 小时还好）
- SA 跑 5 分钟 → 平均 ER = 102.22%
- 关键：SA 在 Cplex 无法优化的大规模 instance 上显著优于 Cplex
- 已部署到 KLS Logistic Systems 的 WMS 产品中（实际工业使用）

---

## 4. Relevance to my Paper 3

### 4.1 高度相关的点（必须认真对待）

- **关键词表面重合**：他们用 "order batching"、"vertical"；我也用 "wave"（= batch）、"vertical"
- **优化目标相同类别**：他们 minimize completion time；我 minimize makespan / weighted tardiness
- **方法论家族相同**：他们用 MILP + SA；我可能也用 MILP + metaheuristic（加上 surrogate）
- **工业应用驱动**：他们跟 WMS 公司合作；我跟 AMR 公司合作

**如果审稿人读过这篇论文，会第一反应联想到它。所以必须在 Related Work 明确划清界限。**

### 4.2 根本性不同的点

| 维度 | Lenoble 2018 | 我的 Paper 3 |
|---|---|---|
| "Vertical" 的含义 | 一台 VLM 内 tray 的机械运动 | 建筑物多层楼间 AMR 货流 |
| 搬运主体 | 固定 picker（1 人）+ 1-4 VLM 机械臂 | 20-50 柔性 AMR fleet + 2-3 共享电梯 |
| 争用模式 | Picker 串行访问 VLM；VLM 内部机械臂串行换 tray | 多 AMR 并发争用电梯（方向+容量冲突）|
| 决策变量 | Order → batch 分配（$x_{nb}$）| Order → wave 分配 + wave 释放时刻 $\tau_w$ |
| 时间建模 | Static offline batching | Wave with explicit release timing |
| 决策层级 | 单层（tactical batching）| 两层（tactical wave + operational fleet）|
| 等价性定理是否成立 | ✅ 成立（通过 Prop 1-3 证明）| ❌ 不成立（耦合太复杂）|

### 4.3 一句话差异总结

> Lenoble 2018 优化的是"picker 如何少等 tray"；我优化的是"AMR fleet 如何少挤电梯 + WMS 如何释放 wave 不制造电梯拥塞"。

两者在问题结构上完全不同，但在**方法论哲学**上有共性——都想找到一个可计算的 proxy 来近似 completion time。

---

## 5. What I can borrow

### 5.1 写作结构上可借鉴

- **论文 outline**：§1 Introduction → §2 Related Work → §3 Problem with 1 unit → §4 Problem with multiple units → §5 Metaheuristic → §6 Conclusion。这是一个清晰的"从简到繁"叙事。
- **Proposition + Proof + Example 的组合**：先给 Prop，再给证明附录，再在正文给 intuitive example。这种写法对工业 OR 期刊（EJOR）特别友好。
- **Managerial insight 表格**：他们用 "effect of order number" 和 "effect of lines per order" 两个表格清晰地展示规律。Paper 3 我应该模仿——用"effect of vertical imbalance"、"effect of elevator capacity"类似的 table。
- **Industry collaborator framing**：在 Introduction 里说"我们被 KLS Logistic Systems 要求研究..."。我可以说"我们被 [公司名] 要求研究..."——这给了 research motivation 一个具体 anchor。

### 5.2 方法论上可借鉴

- **归约思想**：他们把 completion time 归约到 tray count。我的 surrogate $\Phi$ 本质上是类似的归约思想——把 makespan 归约到"三维特征的简单函数"。我可以在 Paper 3 §4.2 引用他们作为"归约型 proxy 方法"的先例。
- **Deterministic + real data 的两步验证**：他们先用 toy-size instance 展示最优性，再用 real data 展示实用价值。我可以采用同样的 structure（Section 5 为 synthetic experiments，Section 6 为 case study）。
- **Efficiency Rate 作为 metric**：他们定义 ER = 1 - (MFV - Cplex_result) / Cplex_result 来度量 metaheuristic 相对 exact solver 的性能。我可以类似地定义 "Vertical-Aware Gain Rate" 或类似指标。

### 5.3 Cite 这篇论文的具体位置

- **Introduction §1.1**（background on warehouse automation）：cite 作为 VLM batching 的开创性工作
- **Related Work §2.2**（order batching literature）：详细对比，划清界限
- **Methodology §4.2**（why surrogate works）：cite 作为 "reduction-based proxy" 的先例
- **Discussion §7**：对比 managerial insights，声明 "complement not contradict"

---

## 6. What I must differentiate from

### 6.1 必须在 Introduction 说清楚的差异（具体 wording）

**Draft wording**（这段直接放进 Paper 3 Intro §1.3 或 Related Work §2.3）：

> "Our problem is distinct from the closely related but structurally different problem studied by Lenoble et al. (2018), who address order batching in warehouses equipped with vertical lift modules (VLMs). In their setting, 'vertical' refers to the mechanical motion of trays inside a single VLM device, served by a stationary picker. The resource in contention is a mechanical tray-extractor, and the decision is a single-stage combinatorial optimization: which customer orders to group so as to minimize redundant tray visits.
>
> In our setting, 'vertical' refers to inter-floor material flows in a multi-storey warehouse, where a flexible fleet of mobile robots (AMRs) competes for shared freight elevator capacity. Three structural differences follow: (i) the service resource is a batch-capacity, direction-reversible elevator rather than a serial tray-extractor; (ii) the transport agents are a flexible fleet of concurrent AMRs rather than a single sequential picker; (iii) the decision is two-stage—tactical wave composition and release jointly shape the downstream operational execution.
>
> These structural differences have a consequential methodological implication: Lenoble et al.'s elegant reductions (e.g., Proposition 2: minimizing completion time ≡ minimizing max-VLM tray-visit count) **do not transfer** to our setting, where completion time depends on multi-agent congestion dynamics that defy closed-form characterization. Our methodology thus departs from pure MILP formulations and adopts a surrogate-based two-stage framework."

### 6.2 审稿人质疑的预案

如果审稿人说 **"这不就是 Lenoble 2018 的多层扩展？"**——答案是：

不是维度扩展，是**对象替换**。他们的 VLM 是一个机械设备，我的 elevator 是一个多 agent 共享的建筑物资源。他们的 picker 是单一串行执行者，我的 AMR fleet 是并发决策者。他们的等价性定理依赖于单 picker 假设；一旦有多 agent 并发，这个归约就失效。

---

## 7. Open questions about their work

读完之后我还不确定的问题（留给精读时回答）：

1. **他们的 picker 从一台 VLM 走到下一台 VLM 的时间真的可以忽略吗？**（他们假设 "pod size is small"）—— 如果我们仿真发现这个时间不可忽略，我们的 elevator 建模会怎么不同？
2. **他们的 SA metaheuristic 为什么用 SWAP 而不是其他 neighborhood？**——如果我用 ALNS，destroy-repair 的 operator 设计需要考虑 wave 内的楼层分布。
3. **他们的 "masked time" 概念能不能迁移到电梯场景？**——电梯载着 AMR 上下楼时，其他 AMR 在做什么？这里也许有类似的并行性可以挖掘。
4. **他们的 real data 有多少 orders per day？**——我的仿真 instance scale 怎么参照？他们最大 192 orders/day；我的 wave scale 应该是这个量级吗？
5. **Stochastic 版本他们讨论过吗？**（conclusion 说是 future work）—— 我是否应该直接跳到 stochastic，还是和他们一样先做 deterministic？

---

## 8. To-do for next reading session

- [ ] 精读 Proposition 1, 2, 3 的证明（§Appendix A, B, C）
- [ ] 精读 §5 metaheuristic 的 SA 参数选择和 SWAP 操作
- [ ] 在 §3.3.2.4 和 §4.3.2.4 读 Effect-of-N-orders 的统计分析方法，看我 Paper 3 能不能借鉴
- [ ] 对比我的 problem formulation draft（`formulations/problem_formulation_v0_1_DRAFT.md`），把 Lenoble 的 notation convention 抽取出来（哪些 notation 我可以沿用，哪些必须改）

---

## 9. Log of revisions to this reading log

- **v0.1 (2026-04-20)**: Initial draft by Claude based on full-text reading of the paper
- **v0.2 (pending)**: Refine after my own careful second reading
- **v0.3 (pending)**: Add cross-reference to `novelty_analysis_and_contributions.md`

---

**End of Lenoble 2018 reading log v0.1**