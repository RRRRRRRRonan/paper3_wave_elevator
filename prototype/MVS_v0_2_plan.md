# Paper 3: MVS v0.2 Prototype Plan

**Placement**: `F:/paper3_wave_elevator/prototype/MVS_v0_2_plan.md`
**Status**: v0.2 blueprint — drafted 2026-04-21, after v0.1 red-flag result
**Purpose**: 从 v0.1 的 red flag 出发，**诊断性**地定位 C/I/T 到底在哪种 regime 下显现；并给 H1（战术 vs 操作层）做第一次真刀真枪的测试

---

## 1. v0.1 告诉了我们什么（起点）

### 1.1 v0.1 精准打到了什么
在 `3 层 × 5 AMR × 1 电梯 × capacity=1 × 确定性 × 线性加性 × 随机采样 wave` 这个极窄 regime 下：
- **M3 − M2 = +0.008**，落入"红灯"区
- `cross_floor` 与 `size` 高度共线（corr ≈ 0.78），baseline 设计有缺陷
- `size` 单独就吃掉了 75% 方差

### 1.2 v0.1 **完全没测**的问题
- 多电梯 / capacity > 1 下 C/I 是否出现
- 错峰释放下 T 是否重要
- 非线性模型（C×I 交互、XGBoost）是否捕捉到额外信号
- 战术 wave 决策相对于操作层优化是否有边际价值（H1）
- 随机服务时间下结论是否稳健

### 1.3 结论
v0.1 的 red flag **只证伪了"v0.1 regime 下的线性 surrogate"**，没证伪 Paper 3 的任何 Type A contribution。v0.2 的使命是**把诊断窗口打开**。

---

## 2. v0.2 的使命（和 v0.1 的本质区别）

| 维度 | v0.1 目的 | v0.2 目的 |
|---|---|---|
| 问题 | 三维特征有没有任何预测力？ | 三维特征**在哪种 regime** 有预测力？ |
| 产出 | 一个 R² 数字 | 一张 **regime × R² 增量** 的 heatmap |
| 决策 | go / red flag | scope Paper 3's Φ claim 到**具体 regime** |
| 类比 | "这药有效吗" | "这药在哪类病人有效" |

**核心洞察**：即使 Φ 只在某个 regime 有效，那也是 **regime-dependent** 的一个**独立 finding**（对应 C3-H2）。这本身就是 publishable insight。

---

## 3. 四条待验证假设

| 编号 | 假设 | 如果成立则证明 | v0.2 哪个 Phase 测 |
|---|---|---|---|
| **H_v2.1** | 去饱和（多电梯 / capacity > 1）后，C/I 的 R² 增量 ≥ 0.05 | Φ 的有效性是 regime-dependent，不是全局无效 | Phase 1 |
| **H_v2.2** | 非线性模型（RF/XGBoost）相比线性有 ≥ 0.05 R² 增益 | 线性加性是错的模型形式，C/I 存在交互效应 | Phase 0（免费） |
| **H_v2.3** | 错峰释放下 T 的 R² 增量 ≥ 0.03 | T 维度有经验基础，不只是理论概念 | Phase 2 |
| **H_v2.4** | 手工优化的 wave composition 相对随机 wave 有 ≥ 10% makespan 改善 | 战术层有边际价值，C3-H1 有希望 | Phase 4 |

**H_v2.2 的优先级特殊**：它**不需要任何新仿真**——直接在 v0.1 的 1000 样本上跑非线性模型。应**最先做**。

---

## 4. Scope

### 4.1 Included

| 组件 | v0.1 | v0.2 |
|---|---|---|
| 楼层数 F | 3 | **5** |
| AMR 数 N | 5 | **10** |
| Elevator 数 E | 1 | **{1, 2, 3}**（sweep）|
| Elevator capacity | 1 | **{1, 2}**（sweep）|
| 服务/电梯时间 | 确定性 | **确定性 + stochastic 对照组**（Phase 3）|
| Wave release | 所有 order 同时 | **staggered（带 intra-wave offset）**（Phase 2）|
| Wave composition | 随机采样 | **随机 + 手工极端**（Phase 4）|
| Operational baseline | FCFS | **FCFS + "better-than-FCFS"**（Phase 4）|
| 每 regime 样本数 | 1000 | **1000**（Phase 1-3）+ **~20 场景**（Phase 4）|

### 4.2 Deliberately Excluded (deferred to v0.3)

- ❌ 完整 Chakravarty-style SAT solver → v0.3（Phase 4 用简化版）
- ❌ ALNS / metaheuristic 上层优化 → v0.3
- ❌ Heterogeneous AMRs / charging → Paper 1 domain
- ❌ 动态订单到达（online） → v0.3
- ❌ Rolling horizon → v0.3
- ❌ 真实数据 → Month 3 case study
- ❌ 工业规模（≥ 50 orders / 10 层） → v1.0

---

## 5. 五阶段计划

### Phase 0 — 非线性诊断（**免费**，半天）

**Input**: `prototype/results/raw/mvs_v0_1_samples.csv`（已存在，1000 行）

**Action**:
1. 在 v0.1 数据上拟合 `RandomForestRegressor`、`GradientBoostingRegressor`、`XGBoost`
2. 对比 M3（线性）与非线性 R²
3. 抽取 tree model 的 feature importance
4. 加入交互项 `C*I`、`I^2`、`C*cross_floor` 跑线性回归，看是否显著

**Decision gate**:
- 非线性 R² − 线性 R² ≥ 0.05 → **H_v2.2 成立**，v0.2 后续所有 surrogate 都用非线性；可能改写 C2-M2 叙述为"三维特征 + 非线性 surrogate"
- 非线性 R² − 线性 R² < 0.02 → H_v2.2 不成立，C/I 在 v0.1 regime 真的无信号，必须靠 Phase 1 regime 变化

**Deliverable**: `prototype/results/v0_2_phase0_nonlinear.md`（1 页）

---

### Phase 1 — Regime sweep（**主菜**，3 天）

**Objective**: 测 H_v2.1。把 (E, capacity) 做成 2D sweep，看 C/I 的 R² 增量怎么随 regime 变化。

**Regime grid**:
```
E ∈ {1, 2, 3}   ×   capacity ∈ {1, 2}   =   6 regimes
```

**每个 regime 跑 1000 samples**（总共 6000 仿真，每个 < 1 秒→ 全部 < 1 小时）

**Code changes 需要**:
- [src/simulator.py](prototype/src/simulator.py)：
  - `ElevatorResource` → `ElevatorPool`（支持 E 个电梯；每个 request 选最早可用的）
  - 支持 capacity > 1：电梯可以"batch"同方向同楼层段的请求
- `experiments.py` 增加 regime 参数

**Analysis**:
- 对每个 regime 分别拟合 M3 − M2 增量
- 画 heatmap：x = E，y = capacity，色值 = R² 增量
- 找到 **"C/I 最显著"的 regime**

**Decision gate**:
- 至少一个 regime 的 R² 增量 ≥ 0.05 → **H_v2.1 成立**，Paper 3 有 regime-dependent 故事可讲
- 所有 regime 都 < 0.05 → Paper 3 需要**重大 pivot**，Φ 的"predictive surrogate"定位放弃，转向 Scenario A rescue（见 §8）

**Deliverable**: `prototype/results/v0_2_phase1_regime_sweep.md` + heatmap PNG

---

### Phase 2 — Temporal clustering（**给 T 一次真正机会**，2 天）

**Pre-req**: 在 Phase 1 找到的"most informative" regime 上做

**Action**:
1. 敲定 T 的具体公式（pre-reg §1.3 留了两个候选，此时选一个，锁定）
2. 修改 wave 生成：给每个 order 一个 `intra_wave_offset`，使 release 时间在 `[0, Δ_max]` 内错峰
3. 用**控制变量法**：固定 (size, cross_floor, C, I) 范围，只变 T，跑 500 waves
4. 也跑 1000 个自由采样 wave，让所有特征都变

**Analysis**:
- 检查 T 与 makespan 的相关性
- 拟合 M4 = M3 + T，看 R² 增量
- 检查 T 的预测方向是否与 pre-reg §1.3 预测一致（"高 T → 大 makespan"）

**Decision gate**:
- T 的 R² 增量 ≥ 0.03 且方向符合预测 → **H_v2.3 成立**，完整的三维框架有实证基础
- T 增量 < 0.01 → T 维度在 MVS scope 下无效，Paper 3 可能要降级到"二维 (C, I) + 其他维度"

**Deliverable**: `prototype/results/v0_2_phase2_temporal.md`

---

### Phase 3 — Stochastic robustness（**稳健性检查**，2 天）

**Objective**: 前两个 phase 的发现是否对服务时间噪声稳健？

**Action**:
1. 给 `service_time`、`speed_per_floor` 加高斯噪声（σ = 20% μ）
2. 在 Phase 1 最好的 regime 上重跑，每个 wave 跑 20 次 replication
3. 检查 R² 是否保持，feature 系数是否稳定

**Decision gate**:
- 加噪声后 R² 下降 < 0.1 → 结论稳健，继续
- R² 下降 ≥ 0.2 → MVS 结论对 deterministic 假设严重依赖，写论文时必须 scope 得很窄

**Deliverable**: 并入 `v0_2_phase1_regime_sweep.md` 的 robustness section

---

### Phase 4 — H1 第一次真正测试（**Paper 3 最重的 insight**，3 天）

**Objective**: 测 H_v2.4。给 H1（战术层 vs 操作层边际价值）做第一次对照实验。

**Design**:
- 固定同一批 30 个 orders
- **Arm A**（纯操作层）：把这 30 个 orders 作为**单个"mega wave"**交给操作层，跑 FCFS 和 "better-than-FCFS"（见下）
- **Arm B**（战术 + 操作）：**手工**分成 3 个 waves（故意构造：低 C / 低 I / 低 T 三种"好 wave"）→ 每个 wave 顺序交给操作层
- **Arm C**（随机战术 + 操作）：随机分成 3 个 waves，对比 Arm B

**"Better-than-FCFS" 简化版（v0.2 不做真 SAT）**:
- 给操作层加一条规则：当多个 AMR 同时等电梯时，按"离 source 最近的方向"优先
- 或：电梯"就近原则"——优先响应同方向请求
- 这不是 Chakravarty-optimal，但比 pure FCFS 强；足够做 H1 初步验证

**Analysis**:
- 对比 Arm A vs Arm B：arm B 比 arm A 快多少？→ 战术层的上限
- 对比 Arm B vs Arm C：手工好 wave 比随机 wave 快多少？→ 战术决策的价值
- Arm B - Arm A 的差值 = "tactical 可以拿到的，操作层拿不到的增益"

**Decision gate**:
- Arm B 比 Arm A 快 ≥ 10% → **H_v2.4 成立**，C3-H1 可以写进 Paper 3
- 差距 < 3% → 战术层在 MVS scope 无价值，C3-H1 需要等 v0.3 或放弃

**Deliverable**: `prototype/results/v0_2_phase4_tactical_vs_operational.md`

---

### Phase 5 — 综合报告（1 天）

**Action**:
1. 汇总四个 phase 的发现到 `mvs_results_v0_2.md`
2. 和 `intuitions_before_MVS.md` 的预测对照，列出 "Surprise #1-#N"
3. 更新 `novelty_analysis_and_contribution.md` 的 §8 counterfactual：哪些 scenario 真的发生了？
4. 提出 v0.3 scope proposal：基于 v0.2 发现，下一步扩什么？

**Advisor meeting artifact**（2 页 PDF）：
- v0.1 red flag + v0.2 regime-dependent 发现
- 对 Paper 3 三个 contribution 的影响评估
- 下一步（v0.3 / Paper 3 draft 启动）

---

## 6. 时间表（~10-12 工作日）

| Phase | 工作量 | 日期区间（相对） | 关键决策点 |
|---|---|---|---|
| Phase 0 | 0.5 天 | Day 1 | 非线性 ≥ 0.05 gain？|
| Phase 1 | 3 天 | Day 1-4 | 至少一 regime R² 增量 ≥ 0.05？|
| Phase 2 | 2 天 | Day 5-6 | T 增量 ≥ 0.03？|
| Phase 3 | 2 天 | Day 7-8 | 稳健性通过？|
| Phase 4 | 3 天 | Day 9-11 | 战术增益 ≥ 10%？|
| Phase 5 | 1 天 | Day 12 | advisor meeting 就绪 |

**总预算**：10-12 工作日。**给自己一周半的弹性缓冲**。

---

## 7. 产出清单

| 文件 | 状态 | 内容 |
|---|---|---|
| `prototype/src/simulator.py` | 更新 | 支持 E ≥ 1、capacity ≥ 1、stochastic option、staggered release |
| `prototype/src/features.py` | 更新 | T 公式锁定、加非线性特征（C*I 等）|
| `prototype/src/experiments.py` | 更新 | 支持 regime sweep |
| `prototype/src/analysis.py` | **新增** | 非线性模型拟合、ablation、heatmap |
| `prototype/src/tactical_arms.py` | **新增** | Phase 4 的三个 arm 实现 |
| `prototype/results/v0_2_phase0_nonlinear.md` | 新增 | |
| `prototype/results/v0_2_phase1_regime_sweep.md` | 新增 | + heatmap PNG |
| `prototype/results/v0_2_phase2_temporal.md` | 新增 | |
| `prototype/results/v0_2_phase4_tactical_vs_operational.md` | 新增 | |
| `prototype/mvs_results_v0_2.md` | 新增 | 综合报告 |
| `intuitions_before_MVS_v0_2.md` | **新增预注册** | Phase 0-4 **开跑前**的预测（不能重蹈 v0.1 没测 T 就乱预测的覆辙）|

---

## 8. 三条预警 / 避坑

### 8.1 Phase 4 的陷阱：Arm B 的"手工好 wave"容易偷跑
如果你自己知道 C/I/T 预测方向，手工构造"好 wave" 会**隐式用到**你想验证的规律。解决方案：把 Arm B 的 wave 分组**交给你没见过数据的人**（比如你另一个同学）构造，或用**确定性规则**（"按 source floor 分组"）构造。否则是循环论证。

### 8.2 Multi-elevator 调度规则要明确
E > 1 时电梯调度有多种选择（最近、FCFS 队列、同向优先……）。**v0.2 用最简：每个 request 选 `min(available_at)` 的电梯**。这个选择本身可能影响 C/I 信号——记得在 Phase 1 里做 ablation（选几种调度规则跑一遍）。

### 8.3 不要把 v0.2 膨胀成 v1.0
诱惑：既然要改 simulator，顺手做 rolling horizon、SAT、ALNS…… **不行**。v0.2 是**诊断**，每多一个 feature 都拉长"什么效应造成什么结果"的归因链。凡是超出 §4 Scope 的都推到 v0.3。

---

## 9. v0.2 失败场景（提前想好）

承接 [novelty_analysis_and_contribution.md §8](../novelty_analysis_and_contribution.md#L408)：

| 场景 | 触发条件 | Paper 3 应对 |
|---|---|---|
| **v0.2-A**：Phase 0 非线性大幅好转 | 非线性 R² 增量 ≥ 0.1 | Φ 的叙述从"线性 surrogate"升级为"三维结构化非线性 surrogate"，novelty 反而加强 |
| **v0.2-B**：Phase 1 找到 C/I 显著 regime | 某 regime R² 增量 ≥ 0.1 | Paper 3 scope 收紧到该 regime，C3-H2 自然变为主 insight |
| **v0.2-C**：Phase 4 战术层显著 | Arm B vs Arm A 差距 ≥ 10% | C3-H1 确认，Paper 3 claim 完整 |
| **v0.2-D**：Phase 1 / 2 / 4 全部 < 阈值 | 所有 R² 增量 < 0.03 | 触发 novelty_analysis §8 Scenario A rescue：Φ 作为 conceptual decomposition，Paper 3 降级到 mid-tier |
| **v0.2-E**：发现的 regime 与直觉完全相反 | 比如 E=3 时 C/I 比 E=1 时**更无效** | 这是**最有价值的 Surprise**，Paper 3 有 counterintuitive insight（C3-H3）|

---

## 10. 与 Paper 3 contributions 的对应关系

| Paper 3 claim | v0.2 哪个 phase 测 |
|---|---|
| **C1** 问题新颖性 | 不需要测（Type A） |
| **C2-M1** 两阶段架构 | Phase 4 的 Arm 对比隐式测试其必要性 |
| **C2-M2** Φ 的三维结构化 | Phase 0、1、2 共同测试 |
| **C2-M3** Φ 跑赢 ML baseline | 需要 v0.3（本版不做） |
| **C3-H1** 战术边际价值 | Phase 4（初版）|
| **C3-H2** Regime-dependent | Phase 1（核心）|
| **C3-H3** 反直觉最优 | 未做（需要 optimizer，v0.3）|

**v0.2 完成后，Paper 3 能**盖章**的 claim**：C1、C2-M1、C2-M2-regime-dependent、C3-H2（至少初步）

**v0.2 完成后，Paper 3 仍**待测**的 claim**：C2-M3、C3-H1（完整版）、C3-H3

---

## 11. Revision log

- **v0.2.draft (2026-04-21)**: Initial v0.2 plan, drafted after v0.1 red-flag result
- **v0.2.final (pending)**: After pre-registration for v0.2 is signed
- **v0.3 (pending)**: After v0.2 results

---

**End of MVS v0.2 Plan draft**
