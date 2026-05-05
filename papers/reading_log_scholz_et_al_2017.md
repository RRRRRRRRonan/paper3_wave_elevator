# Reading Log: Scholz, Schubert & Wäscher (2017) — VERIFIED

**Full citation**: Scholz, A., Schubert, D., & Wäscher, G. (2017). Order picking with multiple pickers and due dates — Simultaneous solution of Order Batching, Batch Assignment and Sequencing, and Picker Routing Problems. *European Journal of Operational Research*, 263(2), 461–478.

**Placement**: `F:\paper3_wave_elevator\papers\reading_log_scholz_et_al_2017.md`
**Read date**: 2026-04-24（Claude full-text 精读 via PDF）
**Relevance rating for Paper 3**: ⭐⭐⭐⭐（planar 多-picker OB 的 decision-variable 代表作；novelty 防御要点）
**Status**: **VERIFIED** — stub 已替换为精读后的内容

---

## 1. Problem — 他们研究的是 JOBASRP

他们把问题命名为 **JOBASRP**（Joint Order Batching, Assignment and Sequencing, and Routing Problem）—— **注意他们通篇用 "batch" 而不是 "wave"**。

**Setting（Fig. 1 two-block layout）**：
- 手动 picker-to-parts 系统，低层货架
- Two-block rectangular layout：m picking aisles × (q+1) cross aisles → 2q subaisles
- **Wide aisles**：假设 picker 可以在同一 picking aisle 内交错（overtake each other）
- Depot 位于前 cross aisle 最左侧 picking aisle 前

**Four interleaved decisions**（同时求解）：
1. **OBP**（Order Batching）：把顾客订单分组到 picking orders
2. **BASP**（Batch Assignment and Sequencing）：batch → picker + 每个 picker 内的 batch 顺序
3. **PRP**（Picker Routing）：每个 batch 的 picker tour
4. （Due-date 作为 objective 的基础：minimize total tardiness）

**Key assumptions**：
- Each order **不允许拆分** across batches（"splitting of customer orders is not allowed since it would result in an unacceptable sorting effort"）
- Picking device capacity C 以 **items 计**（常见假设，也可推广）
- Pickers **不能互相阻塞**（由宽走道假设）—— 问题 NP-hard（引 Chen et al. 2015）

---

## 2. Method

### 2.1 Mathematical model

- MILP formulation，§4 建模；变量数量随订单数 **polynomially** 增长（比 Henn 2015 的前模型更紧凑）
- 使用 **Steiner TSP** 表达 routing（picking aisles + cross aisles 作为 Steiner points）
- Objective (1): min Σ τ_n (总 tardiness)
- 18 约束（capacity, assignment, sequencing, due-date flow-based）

### 2.2 Variable Neighborhood Descent (VND) 启发式（§5）

**Initial solution**：两种 constructive 方法取 min：
- **ESDR-based**（earliest start date rule, 来自 Henn 2015）
- **Seed algorithm**（三步：assign→merge→sequence；考虑处理时间）

**Neighborhood structures**（6 个）：
- N1：batch re-sequencing within picker（改变 batch 在 picker 内的位置）
- N2：batch decomposition + re-insertion（把 batch 拆开重新分配 orders）
- N3/N4：单个 order 从一个 batch 移到另一 batch（同/异 picker）
- N5/N6：两个 order 交换 batch（同/异 picker）
- 使用 **Lin-Kernighan-Helsgaun** 作为 routing subroutine（very high quality）

### 2.3 Numerical experiments (§6)

**Instance classes** — 18 种 × 30 replications = 540 instances per problem class；共 3240 problem instances:
- Orders: **100 或 200**（注意：这是 instance size，不是 "optimal"）
- Pickers p ∈ {2, 3, 5}
- Device capacity C ∈ {45, 75} items
- MTCR γ ∈ {0.6, 0.7, 0.8}（tighter γ → tighter due dates）
- Block count q ∈ {1, 2, 3}
- 每订单 5–25 items（均匀分布）
- Items 类 A/B/C = 10%/30%/60% storage, demand share 52%/36%/12%（class-based）

---

## 3. Result — verified key numbers

### 3.1 VND vs exact (small instances, n ∈ {10, 20})
- **VND outperforms IP-solver（7200s time limit）**：average improvement 4.2–11.4% for n=10; 90.6–99.7% for n=50（medium-scale）
- IP-solver 在 n=50 时基本失效（tardiness 远超 VND）

### 3.2 VND vs ESDR baseline (large instances, n ∈ {100, 200})
- Total tardiness reduction: **51.5–95.2%** depending on problem class
- Number of pickers doesn't strongly impact improvement %; ranges 69.2–71.2% for 100 orders, 73.5–74.8% for 200 orders

### 3.3 VND vs sequential approach（把 OBP/BASP/PRP 分步解）
- Up to **84%** reduction in total tardiness from **holistic**（joint）solution vs sequential
- §7 结论语："dealing with the JOBASRP as a holistic problem is **inevitable** in order to obtain high-quality solutions"

### 3.4 **KEY NEGATIVE FINDING — no "optimal batch size ≈ 100" claim**
- ❌ Paper **不** report wave-size / batch-size optimum
- 100 和 200 只是 instance scale；并没有曲线显示最优 batch size
- ⚠️ **注意**：工作文稿中提到的 "empirically optimal wave size around 100 orders" 其实来自 **Qin 2024**，**不是** Scholz 2017。这在当前 paper 草稿中已修正。

---

## 4. Relevance to my Paper 3

### 4.1 为什么危险

**现在看清楚了**：Scholz 2017 明确把 order batching 作为 decision variable 并做 simultaneous 求解，和 BASP + PRP 耦合。Paper 3 如果声明"first to treat wave composition as decision variable" 而不加限定词，会被这一篇单点击穿。

### 4.2 关键差异（精读后确认，三点全成立）

| 维度 | Scholz 2017 | Paper 3 |
|---|---|---|
| **Setting** | Planar two-block single-floor | Multi-storey F∈{5,7,9} |
| **Vertical resource** | ❌ 无 | ✅ Shared elevator (binding) |
| **Agent** | Human picker with tour continuity + wide-aisle overtake | Flexible AMR fleet, 1 order/ride, cross-aisle via elevator |
| **Objective** | Total tardiness (due-date) | Makespan |
| **Decision scope** | OB + BAS + PR（single-stage simultaneous）| Wave composition (tactical) + AMR dispatch (operational)（two-stage）|
| **Feature representation** | None（直接决策订单分组）| Φ = (C, I, T) 结构化分解 |
| **Terminology** | "batch"（NOT wave）| "wave" for tactical release window |

### 4.3 一句话差异

> Scholz et al. 2017 在 **planar 单层手动 picker system** 中把 **batching + assignment + sequencing + routing** 作为联合 decision variable，minimize tardiness。
> Paper 3 在 **multi-storey AMR fleet + shared elevator** 系统中把 **wave composition on Φ** 作为 tactical decision variable（下层耦合 AMR–elevator dispatch），minimize makespan。
> **核心 delta：vertical resource coupling** —— 去掉 shared elevator，Paper 3 的问题直接坍塌到 Scholz 的 planar 子类。

---

## 5. What I can borrow

- **"Holistic vs sequential" argument**（§7 conclusion）：Scholz 用 up-to-84% reduction 论证 joint 求解的必要性。Paper 3 可以类比：*"analogous to the joint-vs-sequential gap reported by Scholz et al. (2017) in the planar setting, our two-stage coupling gains are only available when wave composition and operational dispatch are treated jointly."*
- **Steiner TSP routing** 作为 Paper 3 v0.5 operational subroutine 的候选
- **ESDR + Seed 双初始解策略** 可借鉴为 Paper 3 v0.5 ALNS 初始化

---

## 6. What I must differentiate from

### 6.1 Paper 3 §1.1 / §1.2 / §1.4 现行 wording 已反映此差异

- §1.1: "planar multi-picker ... settings [Scholz et al., 2017; Žulj et al., 2022]"
- §1.2: "planar picker-to-parts picking ... on a single floor with no shared vertical channel"
- §1.4 C1: "simultaneous batching–routing in planar picker-to-parts picking [Scholz et al., 2017; Žulj et al., 2022]"

### 6.2 审稿人预案

**Q**: "Scholz 2017 已经把 order batching 作为 decision variable 并解了，Paper 3 novelty 在哪？"

**A**: Scholz et al. 的工作在**平面单层手动 picker 系统**中做 OB + BAS + PR simultaneous optimization，没有任何 vertical resource，agent 是人，objective 是 tardiness。Paper 3 把 order grouping 作为 decision variable 这件事**并不是新的**；**新的是**在 multi-storey 下与 **shared elevator capacity coupling**（以及 flexible AMR fleet）联合处理的 tactical 问题类。去掉四限定词中任何一个，问题就 collapse 到一个已有前例（Scholz/Žulj/Qin/Wu/Chakravarty 之一）。四个都保留时，problem class 是未被处理的。

**Q**: "Scholz 的 MILP 能作 Paper 3 baseline 吗？"

**A**: 可以作为 **planar subroutine 的 exact 上界**。他们的 Steiner TSP 路由 formulation 嵌不进我们的 multi-storey + elevator capacity（vertical transitions 要额外变量），但 in single-floor sub-problem 可作 exact LP 参照。这是 v0.5 extension 工作，不是 v0.1 paper 范围。

**Q**: "你们的 objective 是 makespan 不是 tardiness，是不是避开了 Scholz 的主战场？"

**A**: Objective 差异 reflects setting：Scholz 的 due-date 反映 fresh-food / tight delivery 场景（§2.1 开篇 motivation 直接提到这一点）；我们的 makespan 反映 multi-storey fulfillment 的 end-of-wave 清空要求。两个 objective 在各自 problem class 下都是 standard；换 objective 不改变 problem class 的本质。

---

## 7. Open questions about their work

1. ✅ **原工作文稿 "optimal batch size ≈ 100" 来源不是 Scholz** — 已澄清，来自 Qin 2024
2. Instance scale 上限 n=200 — 对 Paper 3 regime 有参考（我们典型 wave size ~4–8 orders 每 wave，总 throughput 200 orders/shift 量级相符）
3. VND 在 n=200, p=5 上平均总 tardiness 3975 分钟 = 一个 picker 平均 13.25 分钟/订单 —— 可作 Paper 3 planar baseline 参考

---

## 8. Key takeaways

- ⭐ **Scholz 2017 = planar decision-variable-framing OB 的最强已发表前例**；Paper 3 的四限定词 novelty lock 必须主动 defend 这一点。
- **他们用 "batch" 不用 "wave"** —— 所以用 "wave" 不会和他们冲突，但 decision-variable 的 framing 必须显式差异化。
- **"joint vs sequential" 是他们的核心论点**；Paper 3 可借用语言但要 reframe 为 "tactical vs operational" 的两阶段 coupling。
- 数字 level：VND-vs-sequential 最高 84% —— 强 empirical 论据。Paper 3 的 H1 "9% mean makespan reduction in 2/6 cells" 数量级看起来弱，但我们的 gain 是 **tactical**（wave composition，不改设备不加 AMR）；与 Scholz 的 operational-internal gain 不可直接比较。

---

## 9. Log of revisions

- **v0.1 (2026-04-24, AM)**: Stub by Claude，未精读，§3/§6.1 wording 标 TODO
- **v0.2 (2026-04-24, PM)**: **VERIFIED** — 精读 18 页全文后补 §1/§2/§3 具体数字；纠正原工作文稿 "optimal batch size ≈ 100" 归属（来自 Qin 2024 不是 Scholz 2017）；§6.1 wording 保留现行版本（§1.1 / §1.2 / §1.4 已 sync）。

---

**End of Scholz et al. 2017 reading log v0.2 (verified)**
