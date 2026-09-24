---
title: "路线 A 修改计划 — Section 3 与 Section 4（v0.1）"
date: 2026-09-24
status: "计划稿 v0.1 — 待作者拍板 §1 的五个决定后执行；§3/§4 的文本改动不依赖重跑，可立即开始"
purpose: "把 2026-09-24 审读中确认的 §3/§4 问题转成可执行的修改清单：逐项给出位置、现文、改后文本、原因、依赖。对 §4 给出重写后的正式陈述与完整证明，可直接粘贴。"
basis: "docx 定稿 §3 文本；paper_draft/section4_draft_v0_1.md；paper_draft/theorems_m4.md、theorems_m5.md；prototype/src/simulator.py、features.py、wave_policies.py、experiments_phase5.py、phase5_config.py；prototype/results/v0_5_phase5.md"
scope: "只覆盖 §3、§4 及其直接依赖（代码对齐、重跑、预注册修正案）。Abstract/§1/§2/§5 的连带修改只记录在 §6 传播清单，不在本轮执行。"
---

# 路线 A 修改计划：Section 3 + Section 4

## 0. 总原则与工作顺序

**路线 A 的定位（一句话）**：论文是"新问题框架 + 预注册大规模仿真 + 两个简单可用的诊断工具"的洞察型论文，目标 C&IE 首选、IJPR 备选。所有理论陈述必须与其证明强度相称；所有 §3 文本必须与 `prototype/src` 的实现逐字对齐。

**三条硬约束**

1. 正确性优先：审读中发现的两处理论缺口（非 partition 的角落划分；逐角落半径的 DRO 等价）必须修，与投稿去向无关。
2. 文本与代码对齐：§3 描述的每一条运营规则都要能在 `simulator.py` 里指出对应代码行。
3. 预注册纪律：划分方案的更改是协议修订，写入预注册 §9.3（本文件 §5 给出草稿），新旧方案的结果都保留。

**工作顺序（依赖关系）**

```
D0 五个决定（§1）
   ├─► D1 代码 + 重跑（§2）—— 后台跑，只影响 §5 的数字
   ├─► §3 文本修改（§3）—— 除相关系数一句外，不依赖重跑
   └─► §4 重写（§4）—— 纯理论，完全不依赖重跑
                └─► 传播到 Abstract/§1/§2/§5（§6，下一轮）
```

§3 和 §4 可以在重跑期间同步完成。

---

## 1. 先拍板的五个决定（D0）

| # | 决定 | 推荐 | 备选 | 影响范围 |
|---|---|---|---|---|
| D0-1 | 划分方案 | 主方案：每个 setting 内按 C、I 的中位数二分的 **2×2 partition**；细化用 **4×4 四分位 partition**（与 2×2 嵌套；其四个极角 cell 在定义上就是旧方案的四个 corner bin：上/下四分位的交集） | 零重跑方案：保留旧 corner arms，把 m_0 改成四个 corner 并集的中位数（"随机池"语义丢失，不推荐） | §4 全部；§5 Block A/C；预注册 |
| D0-2 | T 的定义与命名 | $T(W)=\sigma_r(W)/\Delta$，改名 **temporal dispersion**，高 T = 分散 | 极差版 $(\max r-\min r)/\Delta$ | §3；Abstract/§1/§2 的轴名；features.py；消融 A2 |
| D0-3 | 结果的编号与强度 | **Proposition 1** = Bound-and-Gap 分解；**Corollary 1** = 嵌套细化单调；**Remark 1** = SPO 解读；**Theorem 1** = Hedge Rule（collapse + 两个 regret 界）；**Corollary 2** = 近似支配；**Remark 2** = DRO 解读 | 若导师坚持"两个定理"，SPO 解读最多升为 Proposition 2，不可称 Theorem | §4；§1 C2 段；§2 方法学段；Abstract |
| D0-4 | 术语 | 划分单元叫 **cell**；实验单元叫 **setting**（= config × model × size，替代 "sub-cell"）；"two-stage scheduler" 改为 **two-layer formulation with a policy-fixed operational layer** | 划分单元叫 bin | §4、§5 全文替换 |
| D0-5 | 统计量 s | 主文用 **median**（lower median 约定，见 §2.3）；Proposition 1 与 Theorem 1 对 mean 和任意分位数同样成立，以一句话说明 | 主文用 mean（A3 消融显示更稳，但与 SPO 解读脱钩） | §3 目标函数；§4 |

---

## 2. 代码与重跑清单（D1）

只列必须项。所有新划分变体（2×2、4×4、仅 C、仅 I、加 T）都是对**同一份随机样本**的事后再分析，所以消融 A1/A2/A4 不再需要单独仿真。

### 2.1 代码修改

| # | 文件 | 修改 | 说明 |
|---|---|---|---|
| C-1 | `prototype/src/features.py` | 新增 `temporal_dispersion(wave, window_length)` = 释放偏移的总体标准差 / Δ；保留旧的 `temporal_clustering` 供旧 CSV 复现 | uniform/clustered 下 σ_r = 0，T = 0，与旧行为一致；diurnal 下 Δ 取 `DEMAND_PARAMS["diurnal"]["time_horizon"]` |
| C-2 | 新文件 `prototype/src/partition.py` | `grid_partition(cand, axes=("C","I"), cuts=(0.5,))` 返回阈值与 cell 标签；`cuts=(0.25,0.5,0.75)` 给 4×4；阈值只从该 setting 的随机样本计算一次并冻结 | 阈值是 Φ 空间上的固定切点，cell 是 Φ 的可测函数；cell 权重允许不等（Proposition 1 只要求每个 cell 权重为正） |
| C-3 | `prototype/src/wave_policies.py` | `corner_positions` 保留（P5/P6 的定义不变）；新增注释：P5 的选择集 = 4×4 partition 的极角 cell | Block B 不重跑 |
| C-4 | 新脚本 `experiments_v0_6_random_blocks.py` | Block A′：每个 setting 从候选池均匀抽 N 个波，**同一组波**在 M1、M2 下各仿真一次（matched）；Block C′：6 个 E=2 配置 × size 16 × {M1, M2, M3} matched。每行记录 wave_id、C、I、T、size、各模型 makespan | matched 设计让 Block A′ 同时服务 D1 与 D2-a/b |
| C-5 | 新脚本 `analysis_v0_6_decomposition.py` | 在 2×2 与 4×4 上算 m_q、m_0、V*、LB、H_up、M_Φ、UB、GAP；D1 四个 gate；bootstrap 时阈值固定、对样本重抽 | lower-median 约定下 D1-a/b 应为逐 setting 恒成立 |
| C-6 | 新脚本 `analysis_v0_6_hedge.py` | 在 Block C′ 上算 $v_k(q)$、$q_k^\star$、$\Delta_{12}(q_1^\star)$、$\delta_3$、$U_q(\varepsilon)$、实现的 regret；输出 Theorem 1 的界相对 m_0 的百分比 | 这是 §5 新的"worst-case loss"头条数字 |

### 2.2 重跑预算

| 方案 | Block A′ | Block C′ | 合计 | 说明 |
|---|---|---|---|---|
| 方案 1（够用） | 36 (config × size) × N=800 × 2 模型 = 57,600 | 6 × 800 × 3 = 14,400 | **72,000** | 2×2 每 cell ≈ 200；4×4 每 cell ≈ 50，细化检查偏弱 |
| 方案 2（推荐） | 36 × N=1,600 × 2 = 115,200 | 14,400 | **129,600** | 4×4 每 cell ≈ 100；与 Phase 5 的 106,800 同量级，约 1 到 1.5 周机时 |

Phase 5 的 106,800 次用了约一周（W5），按此估算。

### 2.3 统计约定（写进代码注释与 §5.1）

- cell 中位数与池中位数一律用 **lower median**：$m=\inf\{t:\hat F(t)\ge \tfrac12\}$，numpy 用 `np.quantile(x, 0.5, method="inverted_cdf")`。理由：池的经验分布恰好是各 cell 经验分布按 $n_q/N$ 加权的混合，Proposition 1 的证明在样本内逐字成立，D1-b 不再出现 "−ε" 的假违例。
- 阈值（切点）从整份样本算一次并冻结；bootstrap 只重抽波，不重算切点。
- ties 归入低侧 cell（C ≤ 阈值 → LC，I ≤ 阈值 → LI）。

---

## 3. §3 修改对照表

编号 S3-xx。每项含：位置 / 现文 / 改后 / 原因 / 依赖。英文为可粘贴文本。建议把 §3 改为编号小节 3.1–3.8（Elsevier 排版惯例），顺序见 §3.11。

### S3-01 开头段与两层架构

- **位置**：§3 第 2 段。
- **现文**："This setting decomposes naturally into two coupled decision layers. ... decisions we delegate to a deterministic dispatch policy, defaulting to capacity-bounded FIFO boarding under elevator model M∈M, **with full simulator details given in Section 4**. Section 5 additionally evaluates a destination-clustered alternative ..."
- **改后**：

> This setting decomposes into two coupled layers. The tactical layer chooses the wave composition $W$; it carries the only decision variable of the formulation. The operational layer executes $W$ under a fixed, deterministic dispatch policy, specified in Section 3.6 together with the three elevator models; it carries no decision variable. The two layers are coupled through the makespan: a composition that eases downstream dispatch yields a smaller makespan than an unstructured composition of the same cardinality. Section 5 additionally evaluates a destination-clustered dispatch variant as an experimental treatment factor, not as a decision variable.

- **原因**：§4 草稿里没有模拟器描述，"Section 4" 是悬空引用；"two-stage scheduler" 会引来"第二阶段在哪"的质疑。
- **依赖**：S3-07 新增小节 3.6。

### S3-02 集合与索引：消除符号冲突

- **位置**："Sets and indexes"。
- **现文**：F 既是楼层集合又是层数；A、E 同理；W 既是波次序列又是当前波；"M=M1, M2, M3" 缺花括号；t 作为集合列出。
- **改后**：

> $\mathcal{O}$: set of orders over the planning horizon, indexed by $o$.
> $\mathcal{F}=\{1,\dots,F\}$: set of floors, indexed by $f$.
> $\mathcal{A}$: AMR fleet, indexed by $a$; $|\mathcal{A}|$ is the fleet size.
> $\mathcal{E}$: set of elevators, indexed by $e$; $|\mathcal{E}|=E$.
> $\Omega$: index set of release windows (waves), indexed by $\omega$; $W_\omega\subseteq\mathcal{O}$ is the wave released in window $\omega$, and $W$ denotes the current wave.
> $\mathcal{M}=\{M_1,M_2,M_3\}$: family of elevator models, indexed by $k$.

- **原因**：审稿人与排版编辑都会标出集合/基数混用；W 的双重含义会让约束 (4) 难读。
- **依赖**：全 §3、§4 替换。

### S3-03 参数：与模拟器逐项对齐

- **位置**："Parameters"。
- **现文**：$\tau_d$ "elevator dwell time per stop"；"$\sigma_{M3}\in\{0.10,0.20\}$"；"under M3 the timing primitives $\tau_s,\tau_e,\tau_d$ become lognormally perturbed"；$d_o$ 行 "they contribute no elevator demand"。
- **改后**（只列改动的条目）：

> **Timing primitives.** $\tau_s>0$: per-event AMR service time at pickup and at drop-off. $\tau_e>0$: elevator travel time per floor, incurred both on loaded travel and on the empty repositioning of an elevator to the requesting floor. $\tau_\ell,\tau_u>0$: loading and unloading time per trip.
> **Order attributes.** $s_o\in\mathcal{F}$, $d_o\in\mathcal{F}$: source and destination floor. Same-floor orders ($d_o=s_o$) are admissible: they generate no loaded elevator trip, although the assigned AMR may still need an empty repositioning trip to reach $s_o$; they are excluded from the computation of $I(W)$. The trivial pair $(s_o,d_o)=(1,1)$ is excluded from $\mathcal{O}$. $r_o\ge0$: release offset of order $o$ from the start of its window.
> **Initial state.** At the start of a window all AMRs and all elevators are idle on floor 1 (Assumption A6).
> **Stochastic specification.** $\sigma>0$: scale of the lognormal perturbation under $M_3$. Under $M_1$ and $M_2$ all quantities are deterministic. Under $M_3$ the four phase durations of every elevator trip (repositioning, loading, travel, unloading) are multiplied by independent lognormal factors with unit mean and scale $\sigma$; service times $\tau_s$ are not perturbed. Numerical values are reported in Section 5.

- **原因**：代码里没有单一 $\tau_d$，而是 `load_time=2.0`、`unload_time=2.0`；空车调位也按 `speed_per_floor` 计时；Phase 5 只用 σ = 0.20 且 `service_sigma=0`（`experiments_phase5.py:69`）；同层订单确实可能触发空车调位（`simulator.py:660` 起的派车循环）。
- **依赖**：无。

### S3-04 决策变量段

- **位置**："Decision variable"。
- **现文**："... are fixed by the policy of Assumptions A1–A3 ..."
- **改后**："... are fixed by the operational policy of Section 3.6 (Assumptions A3, A4 and A6) ..."。其余保留。
- **原因**：与新的假设编号和新小节对应。

### S3-05 假设：编号 A1–A6，A3 对齐代码，A5 去掉结果预告，新增 A6

- **位置**："Assumptions"。docx 里是 Word 自动编号 "1."–"5."，正文引用 A1–A5。
- **改后**（Word 编号格式改为 `A%1.`，或手工写 A1–A6）：

> **A1. Single-order carriage.**（保留现文）
> **A2. Source-before-destination sequencing.**（保留现文）
> **A3. List-order assignment with FIFO elevator queueing (default).** Orders are assigned in release-list order to the earliest-available AMR. Elevator requests are served in request order by the earliest-available elevator, subject to the trip-sharing rule of the elevator model in force (Section 3.6). The destination-clustered alternative evaluated in Section 5 changes only the assignment order: it repeatedly assigns a group of $c$ pending orders with the smallest destination-floor spread instead of the next $c$ orders in list order.
> **A4. Intra-floor travel collapsed into service time.**（保留现文）
> **A5. Fixed but unidentified elevator model.** The elevator model $M\in\mathcal{M}$ is a structural property of the elevator subsystem (its trip-sharing logic and timing) and does not depend on the wave released; it is exogenous to the composition decision. The operator is not assumed to know $M$ or to be able to identify it online.
> **A6. Waves are evaluated in isolation.** At the release instant all AMRs and all elevators are idle on floor 1 and no order from an earlier window remains in the system. Interaction between consecutive windows is outside the scope of the formulation.
>
> **Remark 1.** Several conventions for shared elevators coexist in the warehouse-OR literature: throughput aggregation (Bartholdi & Hackman, 2019) and co-occupancy batching (Tadumadze et al., 2023; Chakravarty et al., 2025). Assumption A5 makes this modelling ambiguity part of the problem rather than a preliminary choice; Section 4.2 gives a decision rule whose worst-case loss over $\mathcal{M}$ is bounded without identifying $M$.

- **原因**：现 A3 说"queued AMRs board the next trip"，代码里没有这样的队列，cluster 策略改变的是订单到 AMR 的分配顺序（`simulator.py` 的 `pop_cluster`）；A5 现文后三句是结果预告，假设应为纯陈述；实验逐波独立、初始全在 1 层（`initial_amr_floor=1`），必须显式假设。
- **依赖**：S3-07。

### S3-06 结构特征 Φ：C 公式、T 重定义、"orthogonal"

- **位置**："Structured-feature representation"。
- **现文**（C）：docx 公式对象为 $C(W)=1-\sum_f p_f(W)\ln p_f(W)$。多了 "1"，与 `features.py:15` 的 $-\sum p\ln p$ 不符。
- **改后**（C）：

> **Vertical activity diversity** $C(W)\in[0,\ln F]$: the Shannon entropy of the empirical floor distribution over the union of source and destination floors of $W$,
> $$C(W)=-\sum_{f\in\mathcal{F}}p_f(W)\ln p_f(W),\qquad p_f(W)=\frac{|\{o\in W:s_o=f\}|+|\{o\in W:d_o=f\}|}{2|W|},$$
> with $0\ln0=0$. $C=0$ when all vertical activity is on one floor and $C=\ln F$ when it is spread uniformly over the $F$ floors. We use $C$ unnormalized because all comparisons are made within a fixed $F$.

- **现文**（T）："$T(W)=\sigma_r/\mu_r$ ... High T means orders arrive in tight bursts"。三个问题：(a) CV 随爆发在窗口中的位置变化，不是聚集度；(b) uniform 与 clustered 需求下所有 $r_o=0$，T ≡ 0，占 Phase 5 的 12/18 配置；(c) 解释方向与 `features.py:45` 注释相反。
- **改后**（T，按 D0-2）：

> **Temporal dispersion** $T(W)\in[0,\tfrac12]$: $T(W)=\sigma_r(W)/\Delta$, where $\sigma_r(W)$ is the standard deviation of the release offsets $\{r_o:o\in W\}$ within the window. $T$ is invariant to shifting all offsets by a constant; $T=0$ when the orders of $W$ are released simultaneously, and $T$ is largest when they split between the two ends of the window. Under demand patterns in which every order is available at the window start, $T\equiv0$ and $\Phi$ reduces to $(C,I)$. The partition on which Sections 4 and 5 operate is accordingly built on $(C,I)$; $T$ enters as a sensitivity axis (Section 5.5).

- **现文**（结尾）："The three axes are orthogonal: ..."
- **改后**：

> The three axes are conceptually distinct: floor spread, up-versus-down asymmetry, and temporal spread. On the candidate-wave pools of Section 5 they are also weakly correlated: $|\mathrm{corr}(C,I)|$ averages below 0.05 under uniform and diurnal demand (largest 0.13 in one setting) and 0.17 under clustered demand (largest 0.38), and correlations involving $T$ are below 0.08 wherever $T$ is non-degenerate. $C$ increases with $|W|$ (correlation 0.4–0.5), which is why every comparison in Sections 4 and 5 is made at fixed cardinality. We treat $\Phi$ as a conceptual decomposition rather than a predictive surrogate.

- **原因**：见各条。相关系数是 2026-09-24 用重生成的候选池算的，seed 与 Phase 5 不同，**正式数字待 Block A′ 跑完后用同一份样本重算再填**。
- **依赖**：C-1（T 的代码）；C-4（相关系数的正式数字）。I 的定义已与代码一致，不动。

### S3-07 新小节 3.6 "Operational layer and elevator models"（替换现 "Elevator models"）

- **位置**：现 "Elevator models" 小节整体替换，并前置派车逻辑。
- **改后**：

> **3.6 Operational layer and elevator models.** Given $W$, the operational layer is a fixed event-driven policy. Orders are taken in release-list order. Each order is assigned to the earliest-available AMR, which starts at $\max\{\text{its free time},\ \tau_\omega+r_o\}$. If the AMR is not on $s_o$ it requests an elevator trip to $s_o$, an empty repositioning move that consumes elevator capacity; it then spends $\tau_s$ at pickup, requests a trip from $s_o$ to $d_o$ if $d_o\ne s_o$, and spends $\tau_s$ at drop-off. The wave makespan $C_{\max}(W;M)$ is the last drop-off time measured from $\tau_\omega$.
>
> An elevator trip consists of an empty repositioning of the elevator to the requesting floor ($\tau_e$ per floor), a loading phase $\tau_\ell$, loaded travel ($\tau_e$ per floor) and an unloading phase $\tau_u$. Each elevator serves trips sequentially; a new trip is opened on the earliest-available elevator. The three elevator models differ only in whether and how a trip is shared:
>
> - $M_1$ (**throughput aggregation**): each elevator of capacity $c$ is replaced by $c$ independent single-AMR servers. Capacity acts as parallel throughput; no co-occupancy is represented. This is the aggregation convention of Bartholdi & Hackman (2019).
> - $M_2$ (**co-occupancy batching**): an AMR joins an elevator's current trip if the trip has the same origin and destination floors, carries fewer than $c$ AMRs, and has not yet finished loading; otherwise a new trip is opened. This is the explicit-batching convention of Tadumadze et al. (2023) and Chakravarty et al. (2025).
> - $M_3$ (**stochastic batching**): $M_2$ with each of the four phase durations of a trip multiplied by an independent lognormal factor with unit mean and scale $\sigma$.
>
> $M_1$ and $M_2$ are both used in the literature; their structural disagreement, throughput aggregation versus explicit co-occupancy, is the model uncertainty that Assumption A5 leaves open and Section 4.2 addresses. Parameter values are reported in Section 5.1.

- **原因**：现文的 M1 "per-AMR throughput rate ... single multiplier" 与代码不符（代码是 $E\cdot c$ 个独立单车位电梯，`ElevatorPool`）；M2 "the next c AMRs in the queue board together ... direction handling" 与代码不符（同乘条件是同一 (s,d) 且装载窗口未关闭，`ElevatorBatched.can_board`；Phase 5 未启用 `directional`）；M3 只扰动电梯四相位。
- **依赖**：无。

### S3-08 目标函数：统计量一般化，并接上 A5

- **位置**："Objective function"。
- **现文**：(1) 写为 $\min_{W\subseteq O}\mathbb{E}[C_{\max}(W;M,\xi)]$；后文 "the next wave cannot release until elevator capacity is freed by the current wave's completion"。
- **改后**：

> $$\min_{x\in\{0,1\}^{\mathcal{O}}:\ (2)\text{–}(5)}\ \ s\big[\,C_{\max}(W(x);M,\xi)\,\big]\tag{1}$$
> where $C_{\max}(W;M,\xi):=\max_{o\in W}t_o^{\mathrm{deliver}}(W;M,\xi)$, $\xi$ collects the operational randomness, and $s$ is a monotone summary statistic of the makespan distribution over $\xi$: the expectation, or the median used in Section 5. Under $M_1$ and $M_2$, $\xi$ is degenerate and $s[C_{\max}]=C_{\max}(W;M)$. Problem (1) is stated conditionally on $M$. Because Assumption A5 leaves $M$ unidentified at decision time, Section 4.2 replaces (1) by a minimax criterion over $\mathcal{M}$ and characterizes when the two coincide. We adopt the makespan rather than the average delivery time because the throughput of a release window is gated by its slowest order; under Assumption A6 the makespan is also the earliest time at which the next window finds the fleet and the elevators free.

- **原因**：§4 全部工具用中位数或单调统计量，(1) 用期望会被指不一致；A5 与 (1) 的张力需要一句过渡；"下一波必须等待"只有在 A6 下才成立。
- **依赖**：D0-5。

### S3-09 约束：(6) 降为正文，披露 Δ 与 (3) 在实验中的状态

- **位置**："Constraints"。
- **现文**：(6) $n_a^{\mathrm{board}}(e,t)\le c$ 作为编号约束，但 $n_a^{\mathrm{board}}$ 未定义；末段 "operational invariants ... FIFO boarding"。
- **改后**：保留 (2)–(5) 的编号与解释；删除编号的 (6)；把末段改为：

> The per-trip capacity bound (at most $c$ AMRs aboard any elevator at any time) and the fleet bound $|\mathcal{A}|$ are enforced by the dispatch policy of Section 3.6 inside the simulator; they are invariants of $C_{\max}(W;M)$ rather than constraints of the tactical problem, and we do not number them. In the computational study of Section 5 the window length $\Delta$ equals the demand horizon, so (3) is non-binding and the temporal structure of a wave is carried entirely by $T(W)$; wave cardinality is fixed per setting, so (2) is likewise non-binding there.

- **原因**：EJOR/C&IE 惯例不给非优化约束编号；候选波从整个订单池抽样（`wave_policies.build_candidates`），(3) 与 Δ 从未在实验中出现，必须披露。
- **依赖**：无。

### S3-10 过渡段：Φ 已在 §3 定义

- **位置**：§3 末段。
- **现文**："Section 4 therefore introduces a three-dimensional structured representation ... its formal definition and the partition scheme on which the tools operate are deferred to Section 4."
- **改后**：

> Equations (1)–(5), the operational policy of Section 3.6 and Assumptions A1–A6 define the wave release coordination problem under vertical resource constraints. Direct solution by enumeration over $x$ is impractical: the decision space is combinatorial in $|\mathcal{O}|$ and the objective is simulator-realized. Section 4 therefore works at the resolution of a finite partition of the $\Phi$-space defined in Section 3.5, on which it builds two analytical tools: a Bound-and-Gap decomposition of the value of wave-structure information, and a Model-Dominance Hedge Rule for the elevator-model uncertainty of Assumption A5.

- **原因**：现文与 3.5 已给出的正式定义矛盾。

### S3-11 新 §3 结构与字数目标

| 小节 | 内容 | 目标字数 |
|---|---|---|
| 3.1 Setting and two-layer structure | S3-01 | 250 |
| 3.2 Sets and parameters | S3-02、S3-03 | 350 |
| 3.3 Decision variable | S3-04 | 150 |
| 3.4 Assumptions | S3-05（A1–A6 + Remark 1） | 350 |
| 3.5 Structured-feature representation | S3-06 | 350 |
| 3.6 Operational layer and elevator models | S3-07 | 350 |
| 3.7 Objective and constraints | S3-08、S3-09 | 350 |
| 3.8 Transition | S3-10 | 100 |
| 合计 | | **≈ 2,250**（现 2,804） |

---

## 4. §4 重写方案

§4 是纯理论，不依赖重跑，可以立即重写。以下给出新目录与可粘贴的正式文本。旧草稿中被替换的内容：Theorem 1（SPO 等价）降为 Remark 1；Theorem 2 的 DRO 子句移出定理、降为 Remark 2；新增 Theorem 1 的 regret 界；Proposition 1 补正确的非负性证明；Corollary 1 补正确的证明并要求嵌套；Table 1 去掉"容量侧杠杆"的读法；"corner/sub-cell" 改为 "cell/setting"。

### 4.1 新目录

```
4. Two analytical tools on a partition of Φ-space
   4.1 Partition-level relaxation and the Bound-and-Gap decomposition
       4.1.1 Cells, cell values and three reference cells
       4.1.2 Proposition 1 and Corollary 1
       4.1.3 Reading the components (Table 1); Remark 1 (SPO regret)
   4.2 The Model-Dominance Hedge Rule
       4.2.1 Model family, per-wave order and the minimax cell
       4.2.2 Theorem 1 and Corollary 2
       4.2.3 Remark 2 (Wasserstein-DRO reading)
   4.3 What Section 5 tests
```

目标字数 1,800–2,000（现草稿约 1,700，但新增了证明；把 Table 1 与两个 Remark 写紧即可）。

### 4.2 开头段

> Section 3 cast wave release coordination as problem (1): a combinatorial decision whose objective is realized by the operational simulator. Rather than search the decision space directly, we work at the resolution of a finite partition of $\Phi$-space. Section 4.1 introduces the partition-level relaxation of (1) and decomposes the value of wave-structure information into two non-negative components (Proposition 1). Section 4.2 addresses the elevator-model uncertainty of Assumption A5 and gives a closed-form decision rule with a computable worst-case regret (Theorem 1). Section 4.3 lists what Section 5 tests.

### 4.3 §4.1.1 Cells, cell values and three reference cells

> Fix a setting: a warehouse configuration, an elevator model $M\in\mathcal{M}$ and a wave cardinality $n$. Let $\mathcal{W}_n$ be the admissible waves of cardinality $n$ and let $W\sim\mathrm{U}(\mathcal{W}_n)$ denote a wave drawn uniformly at random ("random release"). A finite partition $\mathcal{Q}=\{q_1,\dots,q_K\}$ of $\Phi$-space induces a partition of $\mathcal{W}_n$; we write $W\in q$ for $\Phi(W)\in q$ and require $w_q:=\mathbb{P}(W\in q)>0$ for every cell. In Section 5, $\mathcal{Q}$ is the $2\times2$ partition of the $(C,I)$ plane at the within-setting medians of $C$ and $I$, with cells HC·HI, HC·LI, LC·HI and LC·LI, and its nested $4\times4$ refinement at the quartiles, whose four extreme cells are the corner bins of the pilot study.
>
> For a monotone summary statistic $s$ (the median throughout Section 5; the mean and any fixed quantile are admissible) define the cell value and the pool value
> $$m_q:=s\big[\,C_{\max}(W;M)\ \big|\ W\in q\,\big],\qquad m_0:=s\big[\,C_{\max}(W;M)\,\big].$$
> The partition-level relaxation of (1) chooses a cell $q$ and releases a wave drawn uniformly from it; its value is $m_q$. Three cells serve as references: the oracle cell $q_{\min}:=\arg\min_q m_q$, the worst cell $q_{\max}:=\arg\max_q m_q$, and the cell $q_\Phi$ selected by a $\Phi$-informed rule (in Section 5, the sign pattern of an ordinary-least-squares fit of makespan on $(C,I)$ within the setting). Relative to random release, define the achievable value of cell selection, the realized value of the $\Phi$-rule, the downside exposure of the partition, the oracle spread and the gap:
> $$V^\star:=\frac{m_0-m_{q_{\min}}}{m_0},\qquad LB:=\frac{m_0-m_{q_\Phi}}{m_0},\qquad H_{\mathrm{up}}:=\frac{m_{q_{\max}}-m_0}{m_0},\qquad UB:=\frac{m_{q_{\max}}-m_{q_{\min}}}{m_0}=V^\star+H_{\mathrm{up}},\qquad GAP:=UB-LB.$$

**为什么这样定义**：旧草稿把 UB 叫 "oracle upper bound"，但 cell 规则相对随机释放能拿到的上限是 $V^\star=UB-H_{\mathrm{up}}$，不是 UB。把 $V^\star$ 显式定义出来，H_up 的含义就清楚了：它是"最差 cell 相对随机释放的惩罚"，即坏的波次组成会付出的代价，而不是"结构性剩余"或"容量侧上限"。

### 4.4 §4.1.2 Proposition 1 与 Corollary 1（含证明）

> **Proposition 1 (Bound-and-Gap decomposition).** Let $\mathcal{Q}$ be a finite partition of $\Phi$-space with $w_q>0$ for all $q$, let $s$ be the median, and let $q_\Phi$ be any cell. Then
> $$GAP=H_{\mathrm{up}}+M_\Phi,\qquad M_\Phi:=\frac{m_{q_\Phi}-m_{q_{\min}}}{m_0}=V^\star-LB,$$
> and both components are non-negative: $H_{\mathrm{up}}\ge0$ and $M_\Phi\ge0$. The same statements hold when $s$ is the mean or any fixed quantile.
>
> *Proof.* The identity is algebra: $UB-LB=(m_{q_{\max}}-m_0)/m_0+(m_{q_\Phi}-m_{q_{\min}})/m_0$. $M_\Phi\ge0$ because $m_{q_{\min}}=\min_q m_q\le m_{q_\Phi}$. For $H_{\mathrm{up}}\ge0$, let $F_q$ be the conditional distribution function of $C_{\max}(W;M)$ given $W\in q$ and $F_0=\sum_q w_qF_q$ that of the pool; the latter is the law of total probability and uses that $\mathcal{Q}$ covers $\mathcal{W}_n$. With $m_q=\inf\{t:F_q(t)\ge\tfrac12\}$ and $m^\star:=\max_q m_q$ we have $F_q(m^\star)\ge F_q(m_q)\ge\tfrac12$ for every $q$, hence $F_0(m^\star)=\sum_q w_qF_q(m^\star)\ge\tfrac12$ and $m_0\le m^\star=m_{q_{\max}}$. For the mean, $m_0=\sum_qw_qm_q\le\max_qm_q$; for the $\alpha$-quantile replace $\tfrac12$ by $\alpha$. $\square$
>
> Two readings follow. $M_\Phi$ is the part of the achievable value $V^\star$ that the $\Phi$-rule leaves on the table: a better rule on the same partition can recover it. $H_{\mathrm{up}}$ is the penalty of the worst cell relative to random release: no rule on $\mathcal{Q}$ can convert it into a gain, but any composition practice that lands in the worst cell pays it. The two components are therefore the upside a good rule can capture and the downside a bad rule can incur, and $UB=V^\star+H_{\mathrm{up}}$ is their sum.

**作者注（不进论文）**：证明依赖 $F_0=\sum_q w_qF_q$，即 $\mathcal{Q}$ 覆盖整个池。旧方案的四个 corner bin 只覆盖约四分之一的候选波，池中位数不是 corner 中位数的混合，所以 $H_{\mathrm{up}}\ge0$ 在旧方案下没有被证明，2/72 个负值不是"有限样本伪影"。这是改划分的原因，写进预注册修正案（§5）。

> **Corollary 1 (nested refinement).** If $\mathcal{Q}'$ refines $\mathcal{Q}$ (every cell of $\mathcal{Q}'$ lies inside a cell of $\mathcal{Q}$, both with positive weights), then $\max_{q'\in\mathcal{Q}'}m_{q'}\ge\max_{q\in\mathcal{Q}}m_q$ and $\min_{q'\in\mathcal{Q}'}m_{q'}\le\min_{q\in\mathcal{Q}}m_q$. Consequently $H_{\mathrm{up}}(\mathcal{Q}')\ge H_{\mathrm{up}}(\mathcal{Q})$, $V^\star(\mathcal{Q}')\ge V^\star(\mathcal{Q})$ and $UB(\mathcal{Q}')\ge UB(\mathcal{Q})$. No such monotonicity holds for $M_\Phi$.
>
> *Proof.* Each coarse cell $q$ is the mixture of the fine cells it contains, with weights $w_{q'}/w_q$. The argument of Proposition 1, applied inside $q$, gives $m_q\le\max_{q'\subseteq q}m_{q'}$; for the lower bound, if $t<\min_{q'\subseteq q}m_{q'}$ then $F_{q'}(t)<\tfrac12$ for every $q'\subseteq q$, so $F_q(t)<\tfrac12$ and $m_q\ge\min_{q'\subseteq q}m_{q'}$. Taking the maximum and the minimum over $q$ proves the two inequalities; the rest follows from the definitions, since $m_0$ does not depend on the partition. $\square$

**作者注**：旧草稿的证明 "a finer max is taken over a superset of values" 不成立（细 cell 的中位数不是粗 cell 中位数的超集），且旧消融 A4 用的 2×2 → 3×3 不嵌套（三分位切点不包含二分位切点），不构成对该推论的检验。新方案用 2×2（中位数）→ 4×4（四分位）。

### 4.5 §4.1.3 Table 1 改写与 Remark 1

> **Table 1. Reading the two components.**
>
> | $H_{\mathrm{up}}$ | $M_\Phi$ | Reading |
> |---|---|---|
> | large | small | The $\Phi$-rule is near-optimal at this resolution. The remaining spread is the downside of the partition: it can be reduced only by refining the partition or changing the feature set (Corollary 1), not by a better rule on $\mathcal{Q}$. |
> | small | large | Cells are similar in level but the $\Phi$-rule selects a poor one; recalibrating the rule is the lever. |
> | large | large | Both: refine the partition and recalibrate the rule. |
> | small | small | The partition carries little makespan information; composition along $\Phi$ is not a lever in this setting. |
>
> **Remark 1 (SPO-regret reading of $M_\Phi$).** Treat the choice of a cell as a decision over $\mathcal{Q}$ with true cost vector $(m_q)_{q\in\mathcal{Q}}$. For any partition-constant predictor $\hat c\in\mathbb{R}^{\mathcal{Q}}$, the SPO loss of Elmachtoub & Grigas (2022) is $m_{\arg\min\hat c}-m_{q_{\min}}$; the $\Phi$-rule is the predictor that induces $q_\Phi$, so its normalized SPO loss is exactly $M_\Phi$. This is a reading rather than a result: it locates $M_\Phi$ in the prediction-to-decision literature and makes precise what "policy-recoverable" means, namely the loss a better partition-constant predictor could remove, while $H_{\mathrm{up}}$ is a quantity that no predictor on $\mathcal{Q}$ can affect. The policy P5 of Section 5 is the $\Phi$-rule at the $4\times4$ resolution, so its SPO regret is $M_\Phi(4\times4)$.

**删除**：旧 Table 1 中 "elevator-side capacity is the lever" 与 "feature expansion is the priority" 等未经推导的处方；旧 §4.1.2 的 "Theorem 1 (D1)"。

### 4.6 §4.2.1 模型族、逐波序与极小极大 cell

> Let $v_k(q):=s[\,C_{\max}(W;M_k)\mid W\in q\,]$ for $k\in\{1,2,3\}$ and $q_k^\star:=\arg\min_q v_k(q)$, ties broken by a fixed order of the cells. Write $M_1\preceq M_2$ (per-wave dominance) if $C_{\max}(W;M_1)\le C_{\max}(W;M_2)$ almost surely for every $W\in\mathcal{W}_n$: aggregating throughput never overstates the makespan of explicit co-occupancy. $M_3$ is a stochastic perturbation of $M_2$ and is not assumed comparable with either model. Under Assumption A5 the conservative decision is the minimax cell $q^{\mathrm{mm}}:=\arg\min_q\max_k v_k(q)$; evaluating it naively requires the cell values under every model. The **Model-Dominance Hedge Rule** releases from $q_2^\star$, the cell optimal under $M_2$, and Theorem 1 states what this costs when $M_2$ is not the true model.

### 4.7 §4.2.2 Theorem 1 与 Corollary 2（含证明）

> **Theorem 1 (Model-Dominance Hedge Rule).** Let $s$ be monotone ($X\le Y$ almost surely implies $s[X]\le s[Y]$) and let $R_k:=v_k(q_2^\star)-v_k(q_k^\star)\ge0$ be the regret of the Hedge Rule when $M_k$ is the true model.
> (i) *Collapse.* If $M_1\preceq M_2$, then $\max_{k\in\{1,2\}}v_k(q)=v_2(q)$ for every $q$; hence the minimax cell over $\{M_1,M_2\}$ is $q_2^\star$, and $R_2=0$.
> (ii) *One-sided regret under dominance.* If $M_1\preceq M_2$, then $R_1\le\Delta_{12}(q_1^\star)\le\max_q\Delta_{12}(q)$, where $\Delta_{12}(q):=v_2(q)-v_1(q)\ge0$ is the inter-model gap in cell $q$.
> (iii) *Regret under an arbitrary model.* For any model $M'$ with cell values $v'$, and no order assumed, $R'\le2\delta'$ with $\delta':=\max_q|v'(q)-v_2(q)|$.
> Consequently the worst-case loss of the Hedge Rule over $\mathcal{M}$ is at most $\max\{\Delta_{12}(q_1^\star),\,2\delta_3\}$, where $\delta_3$ is the value of $\delta'$ for $M_3$; every term is computable from matched-wave simulation of the cell values.
>
> *Proof.* (i) For $W\in q$, per-wave dominance and monotonicity of $s$ give $v_1(q)\le v_2(q)$, so the maximum over $\{1,2\}$ equals $v_2(q)$ in every cell and the outer minimization reduces to $\arg\min_qv_2(q)$. (ii) $v_1(q_2^\star)\le v_2(q_2^\star)\le v_2(q_1^\star)=v_1(q_1^\star)+\Delta_{12}(q_1^\star)$: the first inequality is (i), the second is optimality of $q_2^\star$ under $M_2$. Subtracting $v_1(q_1^\star)$ gives the bound. (iii) Write $v'(q_2^\star)-v'(q'^\star)=[v'(q_2^\star)-v_2(q_2^\star)]+[v_2(q_2^\star)-v_2(q'^\star)]+[v_2(q'^\star)-v'(q'^\star)]$. The middle bracket is at most $0$ by optimality of $q_2^\star$ under $M_2$; each outer bracket is at most $\delta'$. $\square$
>
> Part (i) removes the need to identify the model: under dominance the conservative decision is the $M_2$-optimal cell, whatever the true model. Parts (ii) and (iii) price the rule. Dominance halves the generic bound of (iii) and localizes it at the single cell $q_1^\star$; for the perturbation $M_3$, which breaks pairwise dominance, the generic bound applies with $\delta_3$ the largest cell-wise discrepancy between $M_3$ and $M_2$. Where robust scheduling hedges over a parameter within one model class, the rule hedges across structurally distinct model classes by exploiting a verified order between them.
>
> **Corollary 2 (approximate dominance).** Let $s$ be the median and suppose $\mathbb{P}\big[C_{\max}(W;M_2)\ge C_{\max}(W;M_1)\ \big|\ W\in q\big]\ge1-\varepsilon$ for every $q$. Let $F_{2,q}$ be the conditional distribution function under $M_2$ and $U_q(\varepsilon):=F_{2,q}^{-1}(\tfrac12+\varepsilon)-F_{2,q}^{-1}(\tfrac12)$. Then $v_1(q)\le v_2(q)+U_q(\varepsilon)$ for every $q$; the collapse of Theorem 1(i) holds whenever $\min_{q\ne q_2^\star}\big[v_2(q)-v_2(q_2^\star)\big]>U_{q_2^\star}(\varepsilon)$; and $R_1\le\Delta_{12}(q_1^\star)+U_{q_2^\star}(\varepsilon)$.
>
> *Proof.* Since $\{X_1\le t\}\supseteq\{X_2\le t\}\cap\{X_2\ge X_1\}$, we have $F_{1,q}(t)\ge F_{2,q}(t)-\varepsilon$ for all $t$. At $t=F_{2,q}^{-1}(\tfrac12+\varepsilon)$ this gives $F_{1,q}(t)\ge\tfrac12$, hence $v_1(q)\le t=v_2(q)+U_q(\varepsilon)$. For the collapse, $v_2(q)\le\max_{k\in\{1,2\}}v_k(q)\le v_2(q)+U_q(\varepsilon)$ for every $q$, so $q_2^\star$ minimizes the maximum whenever its own upper envelope $v_2(q_2^\star)+U_{q_2^\star}(\varepsilon)$ lies below the lower envelope $v_2(q)$ of every other cell. The regret bound repeats the chain of Theorem 1(ii) with its first inequality replaced by $v_1(q_2^\star)\le v_2(q_2^\star)+U_{q_2^\star}(\varepsilon)$. $\square$

**作者注**：`theorems_m5.md` 中 Corollary M5.2 的证明在 $t=m_1^c$ 处取值，得到 "$F_2(m_1)\le\tfrac12+\varepsilon$"，这一步在 $F_1(m_1)>\tfrac12$（有原子）时不成立；应在 $t=F_2^{-1}(\tfrac12+\varepsilon)$ 处取值，如上。结论不变。

### 4.8 §4.2.3 Remark 2（DRO 解读，替换旧 Theorem 2 的 DRO 子句）

> **Remark 2 (a Wasserstein-DRO reading).** Take $s$ to be the mean and, for each cell $q$, an ambiguity ball of Wasserstein-1 radius $\rho_q$ around the conditional law of $C_{\max}(W;M_1)$ given $W\in q$. Because the identity map is 1-Lipschitz, the worst-case expected makespan over the ball is $v_1(q)+\rho_q$. Under first-order dominance of $M_2$ over $M_1$ within $q$, the Wasserstein-1 distance between the two conditional laws equals $v_2(q)-v_1(q)$, so calibrating $\rho_q$ to that distance makes the worst case coincide with $v_2(q)$ and the DRO decision with the Hedge cell. The coincidence is thus a consequence of a cell-by-cell calibration of the radius to the observed model discrepancy; with a single radius common to all cells the DRO decision reduces to $q_1^\star$. We do not claim an independent DRO guarantee; the remark locates the Hedge Rule relative to the distributionally robust literature of Section 2.

**作者注**：`analysis_D2_wasserstein_dro.py` 的注释已承认 "a single GLOBAL radius makes the DRO argmin collapse to argmin E_M1"。因此 D2-d（c*_DRO = c*_Hedge，6/6）在 FOSD 成立时是恒等式，不再作为 gate 报告；§5 只保留 D2-a/b/c。

### 4.9 §4.3 What Section 5 tests（改写）

> Section 5 evaluates the following. For Proposition 1, the identity $GAP=H_{\mathrm{up}}+M_\Phi$ and the non-negativity of both components hold in every setting by construction under the lower-median convention; they are reported as checks. The pre-registered gate is signal resolution: whether the 95 % bootstrap interval of $GAP$ excludes zero. For Corollary 1, $H_{\mathrm{up}}$, $V^\star$ and $UB$ are non-decreasing from the $2\times2$ to the nested $4\times4$ partition; the magnitudes are reported. For Theorem 1(i), the frequency of per-wave dominance and of first-order dominance within cells, and whether the minimax cell coincides with $q_2^\star$. For Theorem 1(ii)–(iii), the realized regrets against their bounds, and the size of the bounds relative to $m_0$, which is the paper's worst-case-loss figure. For Corollary 2, $U_q(\varepsilon)$ at the observed violation mass and whether the collapse condition is met or knife-edge.

### 4.10 图的调整

- **Figure 1**（分解示意）：把四个 corner 中位数改为 cell 中位数；在图上标出 $V^\star$、$H_{\mathrm{up}}$、$LB$、$M_\Phi$ 四段，$UB=V^\star+H_{\mathrm{up}}$。生成脚本 `figure_methodology_schematics.py` 相应改标签。
- **Figure 2(a)**（DRO 球）：删除。改为 regret 界示意：横轴四个 cell，两条折线 $v_1(q)$、$v_2(q)$，标出 $q_1^\star$、$q_2^\star$ 与 $\Delta_{12}(q_1^\star)$。**Figure 2(b)**（决策流程）保留，把 "verify chain dominance" 改为 "verify per-wave dominance; compute the bound of Theorem 1"。

---

## 5. 预注册修正案 §9.3 草稿

追加到 `paper_draft/phase5_scaleup_preregistration.md`：

> ## 9.3 Amendment 3 — partition scheme and T definition (2026-09-24)
>
> **Trigger.** A theorem audit on 2026-09-24 found that the non-negativity of $H_{\mathrm{up}}$ (Proposition 1) requires the partition to cover the candidate pool, because its proof writes the pool distribution as the mixture of the cell distributions. The quartile-corner arms of §2.3 cover roughly one quarter of the pool and are therefore not a partition; under them $H_{\mathrm{up}}\ge0$ is unproven, and the two negative values in Block A (D1-b, 70/72) are not attributable to sampling noise. The same audit found that the temporal feature $T$ (coefficient of variation of release times) is not invariant to the position of a release burst within the window and is identically zero under the uniform and clustered demand patterns.
>
> **Changes.** (a) The decomposition is re-evaluated on the $2\times2$ median-split partition of $(C,I)$ within each setting, with the nested $4\times4$ quartile partition as the refinement check (replacing 3×3). Cell and pool medians use the lower-median convention. (b) Blocks A and C are re-run with uniformly sampled candidate waves, matched across models, at $N$ waves per setting (Block A′: 72 settings × {M1, M2}; Block C′: the six E = 2 configurations at size 16 × {M1, M2, M3}). Block B is unchanged. (c) $T$ is redefined as the standard deviation of release offsets divided by the window length; the T ablation (A2) is re-run as a reanalysis on diurnal settings only. (d) Gate D2-d (DRO corner = Hedge corner) is withdrawn as a gate, since under first-order dominance it is an identity with a cell-calibrated radius; it is reported as a consistency remark. (e) A new reported quantity is added: the worst-case regret bound of Theorem 1, $\max\{\Delta_{12}(q_1^\star),2\delta_3\}$, relative to $m_0$.
>
> **Gates.** D1-a/b become construction checks. D1-c (SPO identity) is retained as a check. D1-d keeps the pre-registered 80 % bar and is re-evaluated on the new scheme; the outcome is reported whichever way it falls. D2-a/b/c are unchanged.
>
> **Transparency.** The original quartile-corner results (Tables 2–3 of draft v0.1) are retained in an appendix table alongside the new ones. This amendment was written before any Block A′/C′ simulation was run.

---

## 6. 传播清单（下一轮执行，本轮只记录）

| 位置 | 需要改的内容 | 触发项 |
|---|---|---|
| Abstract | 删重复句；292 词压到 ≤ 250；"two theorems" → "a decomposition proposition and a hedge theorem"；"chain of dominance across {M1, M2, M3}" → "per-wave dominance of M2 over M1, with M3 as a stochastic perturbation"；"closed-form worst-case loss" 现在由 Theorem 1(ii)(iii) 支撑，措辞改为 "a computable worst-case regret bound"；"temporal clustering" → "temporal dispersion"；"two-stage scheduler" → "two-layer formulation" | D0-2、D0-3、D0-4 |
| §1 C2 段 | 同上四处；去掉 "prove each as a theorem" | D0-3 |
| §1 两个 structural features 段 | "chain" 措辞同步 | D0-3 |
| §2 方法学段 | "Theorem 1 gives this regret a partition perspective" → "Remark 1 ..."；DRO 一段的 "Theorem 2 ... coincides ... collapsing the convex program into a closed-form rule" → "Remark 2 reads the rule as a DRO decision with a cell-calibrated radius"；开头与结尾的 "two ... by precise equivalences proven in Section 4" 改为 "connected ... by a regret identity and a calibration remark" | D0-3 |
| §5.1 | 描述 Block A′/C′ 的随机抽样 matched 设计、N、lower-median 约定；"simulator of Section 4" → "Section 3.6" | C-4、C-5 |
| §5.2 Table 2 | 新方案数字；D1-a/b 改为 checks；D1-d 重评 | C-5 |
| §5.3 Table 3 | 删 D2-d 行；新增 Theorem 1 的界与实现 regret 一行；H-D3 探针改述为 "$q_k^\star$ 随模型变化，因此界非平凡" | C-6 |
| §5.4.1 | 删除 "P5 只能拿到 M_Φ 份额、19% 与 72% 的结构性切片一致" 的论证：cell 规则的可达上限是 $V^\star=LB+M_\Phi$，与 $H_{\mathrm{up}}$ 无关；P7 是波级优化器，可越过任何 cell 中位数。改为直接报告 P5 相对 P7 的差距，并用 Table 1 的读法说明该 setting 的 $M_\Phi$ 是否已耗尽 | §4.5 |
| §5.5 | A1/A2/A4 改为对 Block A′ 样本的再分析；A4 改为 2×2 → 4×4 | C-5 |
| 全文 | "corner" → "cell"；"sub-cell" → "setting" | D0-4 |
| 参考文献 | Nicolas/Yannick/Ramzi → Lenoble, Frein & Hammami；Pardo 等补作者缩写（Pardo, E. G., Gil-Borrás, S., Alonso-Ayuso, A., & Duarte, A.），DOI 从 EJOR 313(1), 1–24 的官方页面核对后替换（现文的 10.13039/501100011033 是资助机构编号，不是 DOI）；Delage & Ye → OR 58(3) 2010, 595–612，删网页文字；Crites → Crites & Barto 1998, Machine Learning 33, 235–262；Tadumadze 2023a/b 补齐或合并；Elmachtoub & Grigas → Mgmt Sci 68(1) 2022；Vera et al. → OR 69(3) 2021；Blanchet & Murthy DOI 改为 10.1287/moor.2018.0936 | 独立任务 |

---

## 7. 验收清单

**§3**
- [ ] 每条运营规则能指到 `simulator.py` 的代码行（A3、3.6 的 M1/M2/M3）。
- [ ] $C(W)$ 公式无 "1−"；范围 $[0,\ln F]$ 已注明。
- [ ] $T$ 为平移不变量；已声明 uniform/clustered 下 $T\equiv0$，划分只用 $(C,I)$。
- [ ] 相关系数一句的数字来自 Block A′ 正式样本。
- [ ] 假设编号 A1–A6，A5 无结果预告，A6 已加。
- [ ] 目标 (1) 用单调统计量 $s$；A5 过渡句已加；(6) 已降为正文；Δ 与 (3) 的实验状态已披露。
- [ ] 集合与基数符号无冲突；无悬空的 "Section 4" 引用。
- [ ] 字数 ≤ 2,300。

**§4**
- [ ] 只有一个 Theorem（Hedge Rule）、一个 Proposition（分解）、两个 Corollary、两个 Remark。
- [ ] Proposition 1 的非负性证明使用混合分布，并声明覆盖性要求。
- [ ] Corollary 1 要求嵌套，证明使用 cell 内混合论证。
- [ ] Theorem 1 含 (i) collapse、(ii) 单侧 regret 界、(iii) 一般 regret 界；证明完整。
- [ ] Corollary 2 的证明在 $t=F_2^{-1}(\tfrac12+\varepsilon)$ 处取值。
- [ ] DRO 只以 Remark 出现，明确"逐 cell 校准半径"。
- [ ] Table 1 无"容量侧杠杆"类处方。
- [ ] §4.3 的检验列表与 §5 的 gate 一一对应；无 D2-d。
- [ ] 字数 1,800–2,000。

**流程**
- [ ] 预注册 §9.3 在 Block A′/C′ 启动前提交并 commit。
- [ ] 新旧方案结果并列保存于附录表。
