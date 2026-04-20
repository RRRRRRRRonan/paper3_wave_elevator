# Reading Log: Wu, Zhang, Li, Zhang, Zhao, Zhang & He (2024)

**Full citation**: Wu, Z., Zhang, Y., Li, L., Zhang, Z., Zhao, B., Zhang, Y., & He, X. (2024). Research on Inbound Jobs' Scheduling in Four-Way-Shuttle-Based Storage System. *Processes*, 12(1), 223. DOI: 10.3390/pr12010223

**Placement**: 追加到 `F:\paper3_wave_elevator\01_reading_log.md`
**Read date**: 2026-04-20（初读 by Claude）| 2026-04-__（精读待补）
**Relevance rating for Paper 3**: ⭐⭐⭐⭐（结构相近的工业 warehouse 调度工作，共享 FFSP framing）
**Status**: Draft — by Claude，待用户精读后补充和修正

---

## 1. Problem

**他们在研究什么？**

四向穿梭车仓储系统（Four-Way-Shuttle-Based Storage and Retrieval System, FWSBS/RS）的 **inbound job scheduling**。具体：

- FWSBS/RS 是一种**多层立体仓库**系统
- 核心设备：**垂直 elevators** + **水平 four-way shuttles**（可前后左右四向移动）+ 三维货架
- **Inbound operation**：货物从 I/O 工作站 → 通过 elevator 升到目标楼层 → four-way shuttle 水平运送到目标储位
- 问题：给定一批 inbound cargo，如何调度 elevator 和 shuttle 使得 **makespan 最小**

**为什么重要？**

FWSBS/RS 是 **AS/RS 的新变种**，比传统 AS/RS 和 SBS/RS 更灵活：
- 传统 AS/RS：stacker crane 一次只能服务一个 aisle
- SBS/RS：shuttle 被限制在特定 aisle 和 tier
- **FWSBS/RS**：shuttle 可四向移动，但**仍然是 layer-captive**（每层有自己的 shuttles）

作者的核心 motivation：**缺乏针对 multi-elevator + multi-shuttle 并行运作的调度研究**。

---

## 2. Method

### 2.1 关键建模决定：Flexible Flow-Shop Scheduling Problem (FFSP)

他们把 inbound scheduling 建模为 **FFSP**：
- 货物 = 工件
- Inbound workflow 分三阶段：**picking（拣选）→ lifting（升降）→ transportation（水平运送）**
- 每个阶段都有 parallel machines（多个 picker / elevator / shuttle）
- 目标：minimize maximum completion time (makespan) = $T_{sum} = \min(\max(T_k))$

### 2.2 设备运动时间建模（很详细）

他们**认真考虑了加速/减速**：
- 两种运动模式：(a) 加速-减速（未达最大速度）；(b) 加速-匀速-减速（达到最大速度）
- 临界距离 $S_0 = v^2_{\max} / a$
- 公式 (2)(3)(4) 分别给出 shuttle 的 X 方向、Y 方向、elevator 的 Z 方向运动时间

**这个细节建模是他们的一个特色**——比多数仓库调度论文更精细。

### 2.3 算法设计：DELO-GA（Double-layer Encoded Local Optimization GA）

核心 idea：
- **Double-layer chromosome**：
  - OS layer（Order-Sorting）：货物排序
  - MS layer（Machine-Sorting）：设备分配
- 两层同时编码，增加搜索空间维度

- **POX crossover operator**：随机分割 OS 基因，跨 parent 复制
- **Simulated Annealing 内嵌**：每代 GA 之后用 SA 做局部搜索
- **目的**：克服传统 GA 的 premature convergence 和弱 local search

### 2.4 Benchmark 验证

- **小规模（10 jobs）**：与 enumeration method（穷举）比较——DELO-GA 30 次试验中找到最优解的次数 ≥ ACO 和 GA 的 7 倍
- **Taillard FFSP benchmark**（20×5, 20×10, 50×5）：DELO-GA 的 ARPD (Average Relative Percentage Deviation) < 4%
- **大规模（最多 100 jobs）**：DELO-GA 比 ACO 快 26.6%，比传统 GA 快 18.4%；solution error 仅 0.88%（对比 ACO 2.51%、GA 2.40%）

---

## 3. Result

### 3.1 规模测试

| Scale (jobs) | DELO-GA best | DELO-GA time (s) |
|---|---|---|
| 20 | 210.83 | 12.81 |
| 40 | 411.31 | 24.93 |
| 60 | 613.83 | 57.41 |
| 80 | 811.31 | 75.95 |
| 100 | 1013.83 | 92.25 |

**观察**：100 jobs 在 92 秒内求解——这是一个**工业规模**级别的 instance。

### 3.2 Layout 鲁棒性测试

他们测试了 18 种 layout（不同的 layer 数 M、sub-aisle 数 T、每列 position 数 P）：
- DELO-GA 在所有 18 个 layout 上 MD (Mean Deviation) < 4
- 系统**对 layout 变化稳健**

---

## 4. Relevance to my Paper 3

### 4.1 Structural 相似的地方

- **Multi-layer vertical warehouse**：多层立体仓库 ✓
- **Elevator as vertical resource**：电梯作为垂直资源 ✓
- **Makespan 最小化**：目标函数一样 ✓
- **NP-hard scheduling**：问题复杂度类别一样 ✓
- **Heuristic/metaheuristic methodology**：方法论家族一样 ✓
- **FFSP framing**：他们用 FFSP——**这是一个值得考虑借鉴的 framing**

### 4.2 决定性差异

| 维度 | Wu et al. 2024 | 我的 Paper 3 |
|---|---|---|
| **Transport agent** | **Aisle/tier captive shuttle**（一层一组，不跨层）| **Flexible mobile robot fleet**（全仓库可移动）|
| **任务源** | Inbound jobs（外部给定）| **Wave composition（内生决策）** |
| **决策层级** | Single-stage（job assignment + sequencing）| **Two-stage（tactical + operational）** |
| **Wave 概念** | ❌ 没有 | ✅ 核心决策 |
| **Shuttle coordination** | 层内 shuttle 独立工作 | **AMR 跨层、争用共享电梯** |
| **Release timing** | ❌ 不优化 | ✅ 显式优化 |

### 4.3 一句话差异总结

> Wu 2024 回答："给定一批 inbound jobs，如何在固定的多设备系统里 scheduling 才最快？"
> 我的 Paper 3 回答："订单应该怎么分组、怎么释放，才能让柔性 fleet 和共享电梯系统表现最佳？"

**关键差异**：
- Wu 的 shuttle 是 **tier-captive** 的——它属于某一层，不会跨层
- 我的 AMR 是 **fleet-flexible** 的——它在整个仓库中移动
- Wu 不需要建模 shuttle 之间的争用（因为它们隔离）
- 我必须建模 AMR 之间的电梯争用（因为它们并发）

### 4.4 Wu 2024 的局限就是我的机会

1. **任务外生**：Wu 假设 inbound jobs 给定，但 WMS 可以控制 wave composition
2. **固定设备**：Wu 的 shuttle 固定在每层，没有 agent 并发争用问题
3. **没有时间维度**：他们优化一批 jobs 的 makespan，没有 "当前 wave 如何影响下一 wave" 的考虑

---

## 5. What I can borrow

### 5.1 **最重要的借鉴**：FFSP framing 可以部分使用

Wu 把问题建模为 FFSP 非常干净。我可以借用这个 framing 描述**下层 operational 子问题**：
- Stage 1: Wave composition 决策（tactical）—— **这是我独有的，不 FFSP**
- Stage 2: Fleet-elevator execution（operational）—— **可以 FFSP-ify**：
  - Sub-stage 2a: AMR pickup at source floor（parallel machines = AMR fleet）
  - Sub-stage 2b: Elevator transport（parallel machines = elevators）
  - Sub-stage 2c: AMR delivery at destination floor（parallel machines = AMR fleet）

**如果我用这个 framing**，Wu 2024 就成了我 Stage 2 的直接参考。

### 5.2 设备运动建模可借鉴

他们的加速/减速建模（公式 2-4）比多数仓库论文细致。如果我 Paper 3 要做高精度仿真，应该参考这个：
- 临界距离 $S_0 = v^2_{\max}/a$
- 两种运动模式：未达最大速度 vs 达到最大速度
- 我应该在 `problem_formulation` 里加一个 note 标记这个细节

### 5.3 Benchmark strategy 可借鉴

- 小规模：enumeration method 作为上限参照
- 中规模：Taillard benchmark 做 ARPD 对比
- 大规模：自己生成 instance，metaheuristic 比较

**我的实验 strategy 可以 mirror 这个**：
- 小规模（10-20 订单）：exact MILP 作为上限
- 中规模（50-100 订单）：Chakravarty-style SAT 作为 operational baseline
- 大规模（200-500 订单）：我的 surrogate + ALNS 对比 DELO-GA

### 5.4 DELO-GA 作为 methodology baseline

**我必须和 DELO-GA 比较性能**。具体来说：
- 我的 surrogate-based two-stage method 应该在 makespan 或 computation time 上打败 DELO-GA
- 如果 DELO-GA 已经能做 100 jobs in 92s，我的 method 应该能做 300+ jobs 在合理时间内，或者在小规模上更准

---

## 6. What I must differentiate from

### 6.1 必须写进 Paper 3 Introduction 的 distinction（英文 wording）

> "Wu et al. (2024) investigate inbound-job scheduling in four-way-shuttle-based storage and retrieval systems (FWSBS/RS), formulating the problem as a flexible flow-shop scheduling problem with tier-captive shuttles and multiple elevators. Our work differs along two fundamental dimensions:
>
> (i) **Transport agent topology**: their shuttles are **tier-captive** (confined to a specific layer), whereas our AMRs form a **fleet-flexible** system in which robots traverse the entire warehouse. This changes the nature of elevator contention: in Wu et al., each elevator serves a defined set of tier-captive shuttles; in our setting, elevators are shared resources subject to concurrent, dynamic demand from any AMR in the fleet.
>
> (ii) **Decision scope**: Wu et al. treat the inbound job set as exogenous and optimize its scheduling; we treat **wave composition as an upstream decision variable**, introducing a tactical layer above the operational scheduling problem they address."

### 6.2 审稿人质疑的预案

**Q**: "Wu 2024 已经解决了多层仓库 + elevator 的 scheduling 问题，你的工作是什么？"

**A**: Wu 2024 的 shuttle 是 tier-captive 的——每层有自己的 shuttles，不跨层。这意味着 elevator 的 demand 是 deterministic 的：一个 job 来了，对应层的 shuttle 就等着。我们的 AMR 是 fleet-flexible 的——它们跨层移动，在 aisle 内自由路径，对 elevator 的争用是 **concurrent and dynamic** 的。这根本性地改变了问题的结构。此外，我们把 wave composition 本身作为决策变量，而他们假设 jobs 外生给定。

**Q**: "你能不能直接用他们的 DELO-GA 作为 baseline？"

**A**: 可以 adapt，但需要注意我们的问题是两阶段的。DELO-GA 只处理下层 operational 问题。我们的 surrogate-based method 的 Type A 贡献（两阶段架构、三维特征）是 DELO-GA 无法涵盖的。

---

## 7. Open questions about their work

1. 他们的 tier-captive shuttle 真的只待在一层吗？实际 FWSBS/RS 是否支持 shuttle 跨层？如果支持，他们的 framing 就变成了我们的问题。
2. 他们的 makespan 数字（100 jobs in 1013.83s = 10.14s/job）比较长——是不是 shuttle 速度假设太慢？我在对比时需要 normalize。
3. 他们的 DELO-GA 收敛快但 sub-optimality 是 0.88%——这个 gap 在大 instance 上会放大吗？
4. 没有讨论 **inbound × outbound 同时进行**的场景——真实仓库经常混合。

---

## 8. Key takeaways / reference for Paper 3

- **Wu 2024 是我 Stage 2 (operational) 子问题的 FFSP framing 参考**
- 他们的 DELO-GA 是**大规模 metaheuristic baseline 候选**
- 他们的 acceleration/deceleration 建模可以借鉴（如果我要做高精度仿真）
- 在 Paper 3 里把他们定位为 "tier-captive shuttle 系统"，我的 "fleet-flexible AMR 系统"是不同问题类
- 他们的 benchmark structure（small-scale exhaustive, medium Taillard, large self-generated）是好的 template

---

## 9. Log of revisions

- **v0.1 (2026-04-20)**: Initial draft by Claude after full-text reading
- **v0.2 (pending)**: Refine after second reading, check details of double-layer encoding
- **v0.3 (pending)**: Cross-reference with my own problem formulation to decide whether to adopt FFSP framing

---

**End of Wu et al. 2024 reading log v0.1**