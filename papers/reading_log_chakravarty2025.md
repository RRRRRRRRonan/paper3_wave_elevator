# Reading Log: Chakravarty, Grey, Muthugala & Elara (2025)

**Full citation**: Chakravarty, A., Grey, M. X., Muthugala, M. A. V. J., & Elara, R. M. (2025). Toward Optimal Multi-Agent Robot and Lift Schedules via Boolean Satisfiability. *Mathematics*, 13(18), 3031. DOI: 10.3390/math13183031

**Placement**: 追加到 `F:\paper3_wave_elevator\01_reading_log.md`
**Read date**: 2026-04-20（初读 by Claude）| 2026-04-__（精读待补）
**Relevance rating for Paper 3**: ⭐⭐⭐⭐⭐（最接近的 operational-level 竞争者，必须精确对比）
**Status**: Draft — by Claude，待用户精读后补充和修正

---

## 1. Problem

**他们在研究什么？**

多机器人 + 多电梯场景下的 optimal scheduling。具体：

- $n$ 个机器人需要在不同楼层之间执行任务
- $l$ 个电梯为它们服务
- 每个电梯**一次只能服务一个机器人**（重要假设：no multi-robot ride）
- 目标：找到一个 schedule，使所有机器人任务的 makespan 最小
- 决策变量：每个机器人用哪台电梯 + 执行的时间顺序

**为什么重要？**

他们明确指出两个 motivating 场景：
- 医院：一台机器人运脏床单跨楼层，另一台机器人送餐到病房
- 建筑物有多个电梯时，机器人争用电梯成为关键瓶颈

**核心声明（论文的 starting point）**：
> "The use of lifts can become a crucial bottleneck for operations when the lifts are outnumbered by the robots that need to use them."

这是**和你 Paper 3 问题陈述完全一致**的驱动。你可以直接引用这句话作为 motivation。

---

## 2. Method

### 2.1 问题形式化

- 每个 request $R_i$ 有多个 alternatives $R_i(j)$，每个 alternative 对应一个电梯选择
- Alternative 的参数：$(s_{i,j}, l_{i,j}, r_{i,j}, d_{i,j})$
  - $s$：最早开始时间（由 A* 从起点到电梯算出）
  - $l$：最晚开始时间（由 deadline 约束）
  - $r$：哪台电梯
  - $d$：电梯服务时长（楼层数 × 单层时间）
- **Transition matrix $M$**：$M_{(i,j),(k,m)}$ 是选择 alternative $R_i(j)$ 后再选 $R_k(m)$ 的最小时间间隔——这是 state-dependent 的（电梯在不同楼层）

这个 formulation 是 **exact** 的——它能求解到最优。

### 2.2 两种 SAT 编码

**方法 A: Time-Expansion Graph (TEG)**
- 决策变量：$x_{i,j,t}$ = "request $i$ alternative $j$ is being serviced at time $t$"
- 每个时间步都有一个决策变量
- 约束：resource mutex, request mutex, assignment, duration, min-gap

**方法 B: Time-Ordered Encoding**
- 决策变量：$x_{i,j}$ = "alternative $R_i(j)$ is assigned"
- 加上 total ordering 变量 $X_{ijkm}$ = "$x_{ij}$ is scheduled after $x_{km}$"
- 通过 anti-symmetry, transitivity, connectedness 约束保证合法性
- 比 TEG 编码更紧凑，但求解更慢

### 2.3 Anytime 优化

- 用 **shrinking time window** 求最优：不断缩小搜索窗口直到不可行
- $2×$ suboptimal：把窗口按 2 分式缩小，大幅加速

---

## 3. Result

### 3.1 Synthetic benchmark

- **10 robots × 4 lifts**：optimization 相比 random walk 提升 **4× 到 8×**
- **15 robots × 6 lifts**：提升达 **6×**
- **25+ robots**：提升超过 **10×**

### 3.2 Real-world-inspired benchmark（**这是你必须关注的数据**）

**Hotel world**（2 lifts, 1 lobby）：

| Scenario | Greedy (s) | SAT Optimal (s) | Speed Up |
|---|---|---|---|
| Hotel-4-1 | 105 | 65 | 1.61× |
| Hotel-4-3 | 150 | 45 | 3.33× |
| Hotel-5-4 | 165 | 38 | **4.34×**（最大）|
| Hotel-7-1 | 255 | 130 | 1.96× |

**Hospital world**（4 lifts, 2 lobbies）：

| Scenario | Greedy (s) | SAT Optimal (s) | Speed Up |
|---|---|---|---|
| Hospital-4-1 | 60 | 48 | 1.25× |
| Hospital-7-1 | 180 | 78 | **2.30×**（最大）|
| Hospital-7-4 | 120 | 120 | 1.00×（无改进）|

**关键观察**：
- Lift 越少、agents 越多 → 优化空间越大
- Hotel 场景（2 lifts, 共享 lobby）比 Hospital（4 lifts, 分散 lobby）优化空间大
- **这给你的 H1 假设一个现成的 anchor**：lift bottleneck 越紧，optimization gain 越大

### 3.3 Scalability

- TEG 方法：25 agents 以内 scales well；30+ agents 在 5 分钟内无法求解
- Time-Ordered Encoding：不稳定，经常退化
- $2×$ suboptimal：把中规模问题求解时间缩短 5 倍
- **最大可处理规模**：~25-35 agents simultaneously requesting lifts

---

## 4. Relevance to my Paper 3

### 4.1 重合度很高的点

- **Multi-robot + multi-lift 系统**：问题对象完全一样
- **Makespan 最小化**：目标函数完全一样
- **Lift 作为瓶颈资源**：motivation 完全一样
- **Queueing contention**：问题结构完全一样

### 4.2 决定性差异

| 维度 | Chakravarty 2025 | 我的 Paper 3 |
|---|---|---|
| **任务集** | **外生给定**（每个 robot 的 task 已知）| **内生决策**（wave composition 是决策变量）|
| **决策层级** | Operational（robot-to-lift assignment）| **Tactical + Operational** |
| **求解方法** | Exact SAT/CP | Surrogate-based heuristic |
| **问题规模** | 25-35 agents 上限 | 目标：数百订单、数十 AMR |
| **时间维度** | Snapshot（一个时刻）| 班次尺度（滚动视角）|
| **Wave 概念** | ❌ 没有 | **✅ 核心决策** |
| **WMS 视角** | ❌ 没有 | **✅ 上游决策** |

### 4.3 一句话差异总结

> Chakravarty 2025 回答："给定一组任务，机器人应该怎么用电梯才最优？"
> 我的 Paper 3 回答："怎么组装任务、怎么释放任务，才能让电梯系统不拥塞？"

**他们的问题是我的下游子问题**——我优化的 wave composition 会**产生**他们的 input。

### 4.4 他们的局限性就是我的机会

1. **Scale 限制**：他们的 SAT 方法只能到 30 agents，工业场景需要数百订单——我的 surrogate-based 方法填这个空白
2. **Snapshot vs. Rolling horizon**：他们是一个时刻的优化，真实仓库是班次尺度的——我的 wave release timing 解决这个
3. **Exogenous vs. Endogenous tasks**：他们假设任务给定，但 WMS 上游可以控制任务组装——我的 wave composition 利用这个

---

## 5. What I can borrow

### 5.1 Problem formulation 上可借鉴

- **Request-Alternative 结构**：每个 robot 有多个 lift 选择，作为不同的 alternatives——这个 abstraction 优雅，我可以在 Paper 3 §3 借用（给出 credit）
- **Transition matrix $M$**：state-dependent 的 cost 建模——我的 fleet-elevator 耦合可以用类似概念

### 5.2 Baseline 上可借鉴

**重要**：我的 experiments 里**必须**包含一个 "operational-only" baseline，模拟 Chakravarty 2025 风格的下游优化（不优化 wave composition）。

**我的 experimental setup 应该是**：
1. Baseline 1: FCFS（完全不优化）— 最弱
2. Baseline 2: Operational-optimal（等价于 Chakravarty 的 SAT，但简化）— **关键 baseline**
3. My method: Wave-aware tactical + operational

**我声明的 X% improvement 必须是 method vs. Baseline 2，不能是 vs. Baseline 1**。否则 Reviewer 会说我的改善来自下游而非上游。

### 5.3 实验数据上可借鉴（可作为 anchor）

- Hotel (2 lift, 1 lobby, 7 robots): 1.96× = 49% makespan 减少
- Hospital (4 lift, 2 lobbies, 7 robots): 2.30× = 57% makespan 减少

**我的 H1（15-30%）是 Chakravarty 之上的 marginal gain**，应该比这些数字小——这是合理的，因为他们已经用 exact method 吃掉了大部分 gain。

### 5.4 写作结构上可借鉴

他们的 Related Work 只有 1 页半，非常 focused。对比三种 baseline（MILP, RL, CP-SAT）后迅速 position 自己。这是一个好的模板——**不要写过长的 Related Work**。

---

## 6. What I must differentiate from

### 6.1 必须写进 Paper 3 Introduction 的 distinction（英文 wording）

> "Our work differs from Chakravarty et al. (2025) in three fundamental dimensions:
>
> (i) **Decision scope**: they solve the *operational* problem of assigning pre-given robot tasks to specific lifts, while we solve the *tactical* problem of deciding which orders to release together as a wave, which in turn generates the task set for operational execution;
>
> (ii) **Solution architecture**: they employ exact SAT/CP encoding with provable optimality but bounded scalability (≤35 agents), whereas we develop a surrogate-based heuristic that scales to industrial-size instances (hundreds of orders, dozens of AMRs) by exploiting structural properties of vertical resource demand;
>
> (iii) **Temporal horizon**: they optimize a single snapshot, whereas we optimize over a shift-level horizon with explicit wave release timing.
>
> These differences make our work *complementary to* Chakravarty et al. (2025)—specifically, the operational optimization they address is a downstream sub-problem within our two-stage framework."

### 6.2 审稿人质疑的预案

**Q**: "Chakravarty 2025 已经证明 multi-robot + lift scheduling 可以 exactly solved 了。你的近似方法还有意义吗？"

**A**: 有。他们的 exact method 只能 scale 到 35 agents。我们的场景是 100-500 订单、20-50 AMR，exact method 不可行。此外，他们的 **snapshot optimization** 不包括 wave composition 决策——即使他们的方法能 scale，它也无法回答"订单应该怎么分组"的问题。

**Q**: "你的 X% 改善是不是就是 Chakravarty 式优化的一部分？"

**A**: 不是。我们的 experimental setup 显式区分了 operational baseline（simulating Chakravarty-style optimization）和 tactical+operational method。X% 是**在 operational optimal 之上的 marginal gain**——这是 Paper 3 独立的贡献。

---

## 7. Open questions about their work

1. 他们假设 **lift 一次只载一个 robot**——这在真实仓库可能不成立（货梯可以载多台 AMR）。我的 Paper 3 需要考虑这个扩展。
2. 他们的 $M$ transition matrix 是 precomputed 的。我的 scenario 里 AMR 的起止楼层是 wave composition 的结果——所以 $M$ 不是固定的，而是 wave-dependent。这是一个 interesting 的建模问题。
3. 他们的 benchmark 最多 7 tasks（"Hospital-7-1"）。真实仓库班次有数百 tasks。他们文章坦诚地说这是 computational limit——我的 method 必须能处理更大规模。
4. 他们没有 stochastic 处理——和 Lenoble 2018 一样。

---

## 8. Key takeaways / reference for Paper 3

- **Chakravarty et al. (2025) 是你的 operational baseline 的 anchor**
- 他们的 1.25×–4.34× 数字为你的 H1（15-30%）提供 empirical context
- 他们的 Request-Alternative 抽象可以借用（给 credit）
- 他们的 SAT/CP 方法在 scale 上失败——这是你 surrogate 方法的 positioning 基础
- 在 Paper 3 里把他们定位为 "complementary downstream sub-problem"，不是竞争者

---

## 9. Log of revisions

- **v0.1 (2026-04-20)**: Initial draft by Claude after full-text reading
- **v0.2 (pending)**: Refine after second reading, check proof of Proposition structure
- **v0.3 (pending)**: Cross-reference with my own operational baseline experiment design

---

**End of Chakravarty et al. 2025 reading log v0.1**