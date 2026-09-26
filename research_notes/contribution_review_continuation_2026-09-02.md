# 三点贡献续审与项目恢复报告

**审查日期：** 2026-09-02  
**审查对象：** 当前 Word 主稿、`paper_draft/manuscript`、`revision_0719`、`revision_2026-07-08`、`prototype/src`、`prototype/results`、既有 2026-08-06 审查，以及截至审查日可检索的 2025–2026 前沿论文。  
**审查性质：** 证据链审计，不改写论文正文，不重新解释预注册门槛。  
**投稿级结论：** **目前不具备送审条件，建议 Major Revision。** 狭义问题场景仍可能有创新性，C2 有可保留的理论/诊断核心；但 C1 的模型范围尚未自洽，C3 的“容量 versus 政策”结论不由现有指标识别，三条贡献也都没有在最新 DOCX 中形成完整闭环。

---

## 1. 阶段性产出扫描：工作做到哪里了

### 1.1 已完成

1. 2026-08-06 已经做过一次强对抗式贡献审查：`research_notes/contribution_review_2026-08-06.md`。当时三条贡献大多被判为 conditional，而不是 fail。
2. 大部分关键补充实验已经实际执行，而不是仍在计划中：Theorem R、全电梯数 Lemma、test–retest、P9、Hedge 实付代价、B-1/B-2/B-3/B-5 等均可在 `revision_2026-07-08/EXECUTION-LOG.md` 和 `prototype/results` 找到。
3. 2026-09-02 对 Abstract 与 Introduction 做了第一轮降调和双口径修复：
   - `paper_draft/manuscript/abstract_v1.1_250w.md`
   - `paper_draft/manuscript/introduction_v1.1.md`
4. 发布模拟器的内置 sanity checks 本次重新运行，全部通过。这只能证明实现对若干手算小例和内部不变量一致，不能证明它忠实代表真实并发仓库。

### 1.2 未完成且直接影响本次判断

1. 根目录 DOCX 是 11 页、5,417 词、最后修改于 2026-08-09 的半稿；只有 Abstract、§1、§2、§3和参考文献，没有 §4、§5、§6、Appendix，也没有结果表或结果图。
2. 9 月 2 日更新后的 Abstract/Introduction 尚未同步回 Word，且索引仍标记为待作者重新批准。
3. §4–§6 的现有 Markdown 仍是旧稿或拼装材料，不是统一后的最终正文：
   - §4 仍保留旧版三条件 Prop. 2、过强的 DRO/`U_c` 表述；
   - §5 仍把 72% 解释为容量主导，并遗漏 test–retest、covering 口径、P8/P9、Hedge 代价与 DES 的完整结果；
   - §6 仍把已经执行的 B-2/B-3/B-5 写成 pending/future，并以“buy capacity”收束。
4. 发布模拟器仍在多个位置用 Python 对象 `id(e)` 进行并列破平（`prototype/src/simulator.py`: 135, 337, 375, 426, 526），与正文拟采用的稳定索引破平不一致。分析 harness 的修复没有进入主模拟器。
5. 实验台账也未完全与代码对齐：设计表把 AMR 水平写成 `{5,10,20}`，代码实际为 `{5,15,30}`；Block C 的 6,000 matched-wave rows 若逐行评估 3 个模型应计为 18,000 model evaluations，摘要的 106,800 需要明确采用“模型评估次数”而非数据行数。

**恢复时的事实源优先级：**

1. `research_notes/contribution_review_2026-08-06.md`：既有实质裁定；
2. `paper_draft/manuscript/00_INDEX.md`：当前组装状态，但其中“§2 已全部应用”和“Prop. 2 已升级”两项本身不可靠；
3. `revision_2026-07-08/tier1_manuscript/W10_final_integration.md`：模块冲突裁定；
4. `revision_2026-07-08/EXECUTION-LOG.md` 与原始 JSON/CSV：实验是否执行、结果为何的事实源。

---

## 2. 三条贡献 × 五项要求：更新后的总矩阵

标记含义：**支持**＝现有证据足以维持；**条件支持**＝缩小声明并完成指定修复后可维持；**不支持**＝现有定义/设计不能推出该声明；**未闭环**＝项目中可能有材料，但最新 DOCX 没有完整论证链。

| 贡献 | 1. 创新与前沿 | 2. 模型正确搭建背景 | 3. 方法合理解决问题 | 4. 结论正确证实 | 5. 论述路线完整 |
|---|---|---|---|---|---|
| **C1 问题建模** | **条件支持**：狭义场景缺口仍 plausible，但“never/only in isolation”过强 | **不支持（需大修）**：单波/多波、两阶段、时间特征及物理过程不自洽 | **不支持（当前）**：只选单波/类别，未求解声称的完整协调问题 | **条件支持**：现有合成结果说明问题有信号，但 DES 排序保真不足 | **未闭环**：Word 到 §3 即止 |
| **C2 两个分析工具** | **条件支持**：真正可卖的是条件性 sample-path dominance 与诊断协议；多项“定理”本身偏定义/直接推论 | **条件支持**：依赖一个尚未充分验证的闭式模型类 | **条件支持**：数学骨架可修，但旧 Prop. 2、DRO、`U_c` 和类内选波仍有缺口 | **条件支持**：预注册 Hedge gates 通过，但大量结果是内部一致性，不是独立效度 | **未闭环**：方法、证明、完整实验均未进入 DOCX |
| **C3 capacity-versus-policy 诊断** | **条件支持（仅问题重要）**：管理问题有价值，但当前度量不识别它 | **不支持**：容量不是决策变量，也没有容量投资/成本模型 | **不支持**：`H_up` 不是容量反事实 | **不支持**：72% 不能推出容量主导或购买容量 | **未闭环**：从指标定义到管理建议发生因果跳跃 |

**相较 2026-08-06 审查的最重要更新：C3 应从 conditional 下调为当前“不支持”。** 原审查已经发现测量不稳健；本次继续追到定义后，发现它不是单纯稳健性不足，而是 estimand 与结论不一致。

---

## 3. 贡献 1：问题建模

### 3.1 创新度与前沿性

狭义缺口仍有希望：本次定向检索尚未发现与“上游单波 composition + floor-confined flexible AMR fleet + building-level shared freight elevators”完全相同的模型。可是以下前沿研究已经明显逼近边界：

- 2026 MAPF-E 已经显式建模多机器人与电梯冲突；
- 2026 WareRover 已经联合 order scheduling 与低层 MAPF/congestion；
- 2025 多层配送机器人工作已经联合 floor-based parcel grouping、路径与电梯选择；
- 2025 多层 shuttle/lift 工作已联合请求序列、设备选择和路径；
- 2026 RMFS 工作已联合 wave 内订单分配、货架选择和机器人调度。

因此不能再写“wave composition 与 elevator **never** coupled”或四元素“**only** studied in isolation”。可防守的说法是：**现有相邻工作通常固定请求集，或不同时具有 floor-confined flexible AMRs、共享楼宇货梯和上游 wave-composition 决策；本文研究这一特定交叉点。** 完整检索记录见 `sources/frontier_novelty_audit_2026-09-02.md`。

### 3.2 模型能否正确搭建背景

当前模型有六个阻断项：

1. **单波模型被写成两阶段/多波 scheduler。** Word 的核心变量是单波订单选择 `x_o`，但覆盖约束和文字又涉及所有 `W_omega`。若研究完整规划期，应使用类似 `x_{o,omega}`、波序、释放时刻与服务约束；若只研究单波，应删除“full scheduler/coordination”含义并明确给定候选池与波规模。
2. **目标会选择“容易的订单”。** 在允许波规模变化、又只最小化当前波 makespan 时，模型倾向选择最小波或最容易订单；没有迟交、公平、全订单覆盖的跨波代价，不能代表运营上的 wave release。
3. **“两阶段耦合”没有显式进入模型。** 运营 dispatch 被固定，AMR/elevator 约束主要藏在黑箱模拟器中。可以称“上游选择在固定运营规则下评估”，不能称已联合优化两阶段。
4. **时间口径矛盾。** 同时释放与非零 `r_o`/diurnal temporal clustering 并存；`T = sigma_r / mu_r` 衡量相对离散度，数值越高并不天然表示“更紧密的 burst”。主模型又曾声称 `T=0`，而 6 个 diurnal 配置实际非零。
5. **物理构念不充分。** 楼层端点熵 `C` 不能区分 `{1,2}` 与 `{1,10}` 的距离；“floor-confined AMR”与 AMR 经电梯移动到 source/destination floor 的叙述需定义交接或跨层机制；所有资源从一楼冷启动也必须作为显式假设。
6. **仿真保真度不足以支持强现实结论。** B-5 的闭式模型与 DES 排名相关仅约 0.45–0.68，闭式 makespan 约高估 25%–37%。dominance 符号大体转移，但候选波/角点排序未被可靠保留。因此当前证据最多支持“该闭式模型类中的现象”。

### 3.3 方法是否解决原问题

当前工具最终选择的是一个 `Phi` profile/corner，不是具体订单集合，也没有解释如何从候选订单池稳定构造满足该 profile、规模、覆盖和窗口约束的 `W`。P7 局部搜索和 P9 波级策略恰好显示：类内选择仍含有大量可利用结构。故“corner choice”只能是筛选层或 policy class，不是原 wave-composition 问题的完整求解器。

### 3.4 结论与论述链

合成实验确实说明 wave composition 会改变模型中的 makespan，但不能反过来验证问题背景中的现实瓶颈、参数范围或“两阶段 scheduler”表述。DOCX 没有 §4–§6 和结论，故路线停在“动机 → 初步形式化”，缺少“求解 → 验证 → 边界 → 结论”。

**C1 最终判定：有可保留的 scoped problem contribution，但必须先决定到底是单波选择问题，还是完整多波调度问题。**

---

## 4. 贡献 2：Bound-and-Gap 与 Model-Dominance Hedge Rule

### 4.1 创新到底在哪里

现有 §4 把不同强度的内容都以 theorem/contribution 定价，容易被审稿人拆解：

- `GAP = H_up + M_Phi` 是代数恒等分解；
- `M_Phi` 等于同一 oracle/selected corner 定义下的 SPO loss，主要是重命名/解释；
- 给定某一模型逐点最坏后，minimax 外层选择退化到该模型的最优角点，是直接推论；
- 用每个 corner 的候选模型距离校准 Wasserstein 半径，再得到与其中最坏模型一致，独立信息有限；
- nested partition 下的单调性是有用性质，但与经典 partition refinement/Blackwell-information 思路相邻。

方法前沿还必须正面比较 coefficient of prescriptiveness（Bertsimas–Kallus 2020；Jiang–Tian–Wang 2026）、VSS/EVPI，以及已有 stochastic-dominance DRO 的闭式结果。不能仅与 SPO 和一般 DRO 做宽泛连接。

最可能形成真正理论增量的是：**在具体电梯模型下，给出正确而非循环的 sample-path dominance 条件与失败机制，并把它转化为可审计的 model-risk release protocol。** 这应成为 C2 主轴，其余恒等式和直接推论降为 supporting properties。

### 4.2 正确性与适用性

1. **Prop. 2 被过度计费。** 三个充分条件联合出现不足 1%，而经验 dominance 为 99.2%；后者不能称为 Prop. 2 的验证或解释。旧证明中“唯一失败渠道”也已被后续检查推翻，必须采用最终全-E、两失败渠道版本，并在正文明确“充分但远非必要”。
2. **DRO 结果更像一致性检查。** 6/6 Hedge = DRO 在使用同一组候选分布和由其校准的半径时并非强独立验证。需要说明 ambiguity set 如何在部署前估计，最好做 train/calibration/test 分离；否则只称 analytical equivalence/check。
3. **`U_c(epsilon)` 不是策略最坏损失。** 它是 dominant-model 角点中位数的单边扰动量。只有再加角点排序 margin 条件，才能推出选择不变；不得直接称“following the rule 的 worst-case loss bound”。
4. **Theorem R 只适用于 nested covering refinement。** 现有 2×2 到截断 3×3 的对比不嵌套，不能验证该定理；必须用真正 covering/nested 的分区系列。
5. **目标统计量不统一。** 正式模型写 expected makespan，而工具主要以 median 建立；M3 为 lognormal 噪声时二者可能给出不同角点，理论与实验必须选一个并一致。
6. **实用性有限但可诚实报告。** P5 对 P7 为 0/12 胜、约高 46%，只回收约 19% 的 P0→P7 gap。Hedge 相对最佳单模型规则在 5/6 配置零代价、config 11 约 2.63%，且存在 worst-regret dominated 情形。这不否定诊断贡献，但否定“competitive policy/近乎免费普遍稳健”的广义表述。
7. **统计单位存在伪重复风险。** 角点内 200 个 wave 是从有限角池有放回抽取；冻结种子复核中，每个 200 行 cell 只有约 78–169 个唯一 wave，且同一 configuration/订单池还被多个 size/model 分析共享。现有 bootstrap、Mann–Whitney、Wilson 等步骤把这些行近似当独立观测，会低估不确定性。应保存 `candidate_id`，按 seed/config/order-pool 聚类重采样，或生成多个独立 order pools 并使用层级模型。
8. **基线命名夸大算法强度。** P5 的实现是 OLS 系数符号决定角点，不是“cell-median learner”；P6 是普通 squared-error `DecisionTreeRegressor`，不宜称为真正的 SPO-Tree；P7 只是 40 轮局部搜索，不能称 optimum。所有结论表必须按“规则/回归树/启发式局部搜索”准确命名，并补入 P8/P9。

### 4.3 现有结果究竟证实了什么

- H-D2 按预注册四项 gate 为 PASS；matched-wave dominance 平均 99.2%，worst cell 96%，24/24 cell FOSD、6/6 collapse/DRO match。这支持“在指定合成网格和闭式模型类中，排序规律很强”。
- 它不证明 Prop. 2 条件普遍成立，不证明现场仓库采用同一模型排序，也不证明 DRO ambiguity set 在新数据中有校准效度。
- DES 对 dominance 符号提供了辅助支持，但对具体候选排序的保真不足。因此结论必须限制到 synthetic/model-class evidence。
- 现有显著性/置信区间还需在考虑共享订单池和重复 wave 后重新计算；在完成 clustered reanalysis 前，不应继续加码“稳定”“普遍”一类统计语言。

**C2 最终判定：可救且可能成为论文的理论核心，但必须重排理论层级、去掉验证恒等式式的卖点，并完成主稿集成。**

---

## 5. 贡献 3：为何当前 capacity-versus-policy 结论不成立

### 5.1 核心识别错误

现有定义为：

`H_up = (m_qmax - m_0) / m_0`

其中 `m_qmax` 是最差 profile corner 的中位 makespan，`m_0` 是随机池基线。它测量的是：**最差 wave-profile corner 相对随机基线的上尾惩罚**。

它不是以下任一量：

- 增加一台 elevator 的边际收益；
- 增大每趟容量 `c` 的收益；
- 增加 AMR 的收益；
- 物理容量影子价格；
- 任意 wave policy 都不可恢复的损失。

因此 `H_up/GAP ≈ 72%` 不能推出“capacity binding”“capacity-side headroom”或“operator should buy capacity”。甚至在字面上，大 `H_up` 首先表示选择很差的 wave composition 可以显著恶化 makespan，仍然是 composition 相关变异。

### 5.2 现有实验也没有补上这一缺口

1. `E=1` 与 `E=2` 虽在配置网格中出现，但对应配置的订单池/seed 不是严格 matched counterfactual；不能将跨配置差直接解释为容量效应。
2. Supp-2 的 `c={2,3,4,5}` sweep 检验的是 model dominance 是否持续，不是扩容相对 policy 的收益。
3. 没有共同成本/预算尺度，也没有 elevator wait、utilization、queue length、shadow price 等真正的容量瓶颈指标。
4. 预注册 `Phi` 口径给出约 72%，covering oracle 口径约 47% 且 SE 约 0.14；test–retest ICC 约 0.01，covering ICC 约 −0.03。容量/政策标签并非测量稳定量。
5. P9 在 7/12 cell 超过 corner oracle，说明 `H_up` 并非“任何 Phi/wave-level policy 都不可恢复”；最多只能说某个固定 coarse partition 的 partition-constant corner rule 不可恢复。
6. operational clustered dispatch 的平均改善约 10.2%，反而大于全部 tactical mean GAP 约 6.0%。这直接要求删除“wave composition largely fixes makespan before any AMR moves”以及“两个层次不能分开却固定运营层”的强表述。

### 5.3 两条可选修复路线

**路线 A：保留 capacity-versus-policy 贡献。** 需要新增、明确标记为补充预注册或探索性的 matched intervention study：

1. 对完全相同的订单池、波、release times、服务噪声和随机种子，比较 `E/c/fleet` 改变前后；
2. 定义 `Delta_cap` 与 `Delta_policy`，在同一基线和同一统计量下比较；
3. 报告置信区间、异质性和 DES 复核；
4. 若要给投资建议，按吞吐增益/成本或预算归一化；
5. 同时报告等待、利用率和队列等瓶颈诊断量。

**路线 B：不新增大实验，改写贡献。** 删除 capacity/buy-capacity 因果结论，将 C3 改为：**partition-relative policy-resolution and instrument-sensitivity diagnosis**。并列报告 prereg `Phi` 72% 与 covering 47%，将 ICC FAIL 作为重要发现，结论是“粗粒度诊断对表示和测量方案敏感，不能据此做容量投资决定”。

就当前项目成熟度，**路线 B 更快、更可信**；路线 A 才能保留原管理标题，但工作量和验证要求明显更高。

---

## 6. 结论能否正确证实三点贡献

### 6.1 可以诚实声称的结果

- 闭式模拟器的内部小例与 sanity checks 通过；
- 72/72 decomposition 和 SPO equality 计算一致，但它们是构造/定义层面的检查；
- H-D1 signal-resolution 为 57/72，低于预注册 58/72 门槛，必须标为 **PARTIAL**；
- H-D2 四门为 **PASS**，dominance 是强而非完美的合成规律；
- capacity-versus-policy 的结论对 measurement/partition 不稳定；
- DES cross-validation 不支持“排序忠实代理”，仅对 dominance/sign 和部分效果给辅助支持；
- P7/P8/P9 和 operational dispatch 说明 coarse profile rule 不是主要可实现绩效上限。

### 6.2 当前摘要/讨论不能继续使用的结论

- “elevator capacity is the primary bottleneck”作为普遍事实；
- “wave composition largely fixes makespan before any AMR moves”；
- “72% structural ceiling means capacity dominates policy”；
- “operator should buy capacity rather than tune composition”；
- “no wave-level policy can recover `H_up`”；
- “Prop. 2 explains the 99.2% dominance”；
- “6/6 DRO match independently validates robustness”；
- “`U_c` bounds the worst-case loss of following the rule”。

这些句子应删除或替换为具有明确条件、对象和测量口径的版本。

---

## 7. 每条贡献的完整论述路线

### C1 应有链条

`真实运营现象与证据` → `精确的相邻文献边界` → `明确 RQ1 与研究范围（单波 or 多波）` → `自洽变量/假设/目标` → `可执行的具体 wave 构造方法` → `校准与 DES/真实数据效度` → `只在证据范围内结论`

**当前断点：** RQ/范围含混、模型与目标矛盾、方法只到 corner、外部效度不足、DOCX 无结果/结论。

### C2 应有链条

`model-class uncertainty/政策价值问题` → `既有 CoP/VSS/EVPI/SPO/DRO 基线` → `定义（不冒充验证）` → `非平凡主定理：dominance 条件与失败机制` → `minimax/DRO 推论` → `独立校准与 out-of-sample test` → `Hedge 实付代价和失败区间` → `适用边界`

**当前断点：** 理论层级混乱、旧 Prop. 2 未替换、DRO 校准循环、`U_c` 误读、方法/证明/结果未进入 Word。

### C3 应有链条

`管理问题：增加容量还是改善 policy` → `明确 estimand 和共同基线` → `matched interventions` → `不确定性/成本归一化` → `瓶颈机制指标` → `稳健性与 DES/现场验证` → `容量投资建议`

**当前断点：** 第一步之后直接用一个 upper-tail partition statistic 代替容量反事实，后续全部结论失去识别基础。

---

## 8. 建议的贡献重构

如果不新增大规模容量因果实验，建议仍保留“三点”，但换成下面的结构：

1. **C1 — Scoped problem/benchmark.** 提出在固定运营规则下、共享楼宇货梯约束的单波 composition benchmark；明确它不是完整 rolling-horizon scheduler。
2. **C2 — Dominance mechanism and robust selection.** 以条件性 sample-path dominance、两类失败机制及其 minimax 选择推论为核心；Bound-and-Gap、SPO equality、refinement 和 DRO relation 降为诊断/解释属性。
3. **C3 — Empirical boundary and measurement sensitivity.** 在预注册合成网格中报告 dominance 的强度、Hedge 的真实代价、coarse policy 与局部搜索的差距，以及 partition/test–retest/DES 对结论的影响；不再声称已经识别容量投资优先级。

若坚持原 C3，则必须完成第 5.3 节路线 A，之后才能恢复“capacity-versus-policy”这个名字。

---

## 9. 继续工作的优先顺序

### P0：先冻结声明，不再继续润色摘要

1. 选择 C3 路线 A 或 B；在此之前，Abstract/Introduction/Discussion 中所有 capacity-side 句子都不应视为定稿。
2. 明确 C1 是单波选择还是完整多波调度。该选择决定变量、目标、约束和标题含义。

### P1：修模型与实现

1. 统一 expected/median 目标；
2. 修复 `x_o`/`x_{o,omega}` 与跨波覆盖；
3. 统一 simultaneous release、`r_o`、diurnal 和 `T`；
4. 明确 AMR 跨层/交接及 cold-start；
5. 更换稳定索引 tie-break，并重跑受影响结果或证明结果哈希不变；
6. 修正 AMR 水平、evaluation count 和 P5/P6/P7 名称等台账/实现差异；
7. 给参数提供真实数据、文献或 sensitivity grounding；
8. 将 DES 作为 validity boundary，而非未来工作。

### P2：重建 §4 的理论层级

1. 恒等式标为 identity/diagnostic definition；
2. 把最终全-E dominance 命题及两失败渠道作为主定理；
3. 报告充分条件低覆盖率；
4. 修正 `U_c`；
5. 只对 nested partitions 使用 Theorem R；
6. 对 DRO 做 calibration/test 分离，或降为 analytical equivalence。

### P3：把已完成证据一次性整合进 §5–§6

必须纳入：H-D1 PARTIAL、双口径 72%/47%、ICC FAIL、P7/P8/P9、enumeration anchor、Hedge 实付代价、B-5 DES、operational dispatch 10.2%、所有已执行而旧稿仍称 pending 的修正项。预注册、补充预注册与事后探索必须分栏标记。

同时应在保存 `candidate_id` 后重做聚类/层级不确定性分析。若复算改变任何门槛判定，按原预注册规则报告改变，不得以旧行级区间覆盖新结果。

### P4：重写前沿定位并生成完整 DOCX

1. 加入 2025–2026 近邻文献逐项对照表；
2. 比较 CoP、VSS/EVPI、SPO、partition refinement 和 stochastic-dominance DRO；
3. 删除 first-ever/never/only 类绝对化措辞；
4. 组装 Abstract–Appendix 后再做一次全文交叉引用、数字、符号和声明审计。

---

## 10. 最终回答

1. **创新度足够、基于前沿？** 狭义 C1 与修正后的 C2 有条件成立；现稿的绝对化 novelty 和 C3 的方法 novelty 不成立。前沿综述需更新至 2026。
2. **模型正确搭建背景？** 尚未。动机合理，但形式化范围、时间逻辑、两阶段含义和物理过程存在重大不一致。
3. **方法合理解决问题？** 部分。C2 的 dominance 核心可解决“候选模型间如何稳健选 profile”，但没有解决完整 wave construction；C3 方法不识别容量 versus 政策。
4. **结论正确证实三点贡献？** 尚未。C2 有条件的合成证据最强；C1 外部效度有限；C3 的主结论不由数据和定义推出。Word 还没有结果与结论章节。
5. **每条贡献论述路线完整？** 均不完整。C1 在模型—验证处断裂，C2 在最终理论—独立验证—主稿集成处断裂，C3 在 estimand 定义处即断裂。

**最稳妥的下一步不是继续扩写，而是先完成两个决策：将研究范围锁定为单波 benchmark；将 C3 改成 measurement-sensitivity contribution。** 做完这两项，再整合已经完成的实验，论文才会从“材料很多但相互冲突”变成一条可以被审稿人逐段验证的证据链。
