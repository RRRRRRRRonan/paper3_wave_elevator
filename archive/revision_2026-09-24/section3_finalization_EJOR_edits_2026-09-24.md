---
title: "Section 3 定稿核查与 EJOR 逐句修改对照"
date: 2026-09-24
basis: "F:/Paper 3/Problem formulation.docx（2026-09-24 16:35，11 页，242 个公式对象）；§4 基准 F:/Paper 3/Methodology.docx（2026-09-17）；代码 prototype/src/simulator.py、features.py、wave_policies.py；引文原文 papers/Chakravarty2025.pdf、papers/Tdumadze2023.pdf、papers/Bartholdi2019.pdf，So & Al-Sharif (2019) 开放获取全文与 Crossref 记录"
companion: "全文中英对照：section3_bilingual_2026-09-24.md"
scope: "只作逐句修改，不改变小节结构、公式内容与公式编号 (1) 到 (32)"
---

# Section 3 定稿核查与 EJOR 逐句修改对照

## 1. 定稿判定

**结论：修改 6 项必改后即可定稿。** 其余 27 项为 EJOR 风格与表述准确性的建议（另撤回 1 项），不改变任何公式、编号或结构，可按需取舍。

**自 9 月 14 日版以来已完成的项目**（计划 v0.2 的 §3 清单全部落实）：

| 计划项 | 状态 |
|---|---|
| S3-1 $\mathcal J_n=\{1,\ldots,n\}$ 花括号 | 已改 |
| S3-2 表 3.2 的 $r_o$ 改称 ready-time offset | 已改 |
| S3-3 表 3.3 标题句点 | 已改 |
| S3-4 $T$ 的名称与"不进入角类"一句 | 已改 |
| S3-5 分位数插值位置 $1+(K-1)u$ | 已改 |
| S3-6 式 (31) 与引导句同页 | 已解决（现同在第 10 页） |
| S3-7 $M_1$、$M_2$ 的文献锚点 | 已加，但引文与原文不符，见 R-25、R-27 |

**代码一致性**：式 (1) 到 (32) 与生产代码逐项一致，本轮未发现新的模型或代码不符。

**排版**：除式 (7) 外（R-34），全部 32 个编号公式、242 个公式对象、正文与三张表均已逐项对照 PDF 核对。

**修改项分级**

| 级别 | 编号 | 说明 |
|---|---|---|
| 必改·引文 | R-25、R-27 | 今天加入的三条引用与原文不符，属事实错误 |
| 必改·与 §4 对齐 | R-04、R-14、R-21 | §3 的表述与 Methodology.docx 不一致 |
| 必改·排版 | R-34 | 式 (7) 的 MathType 对象中，括号被排进上标 |
| 建议·准确性 | R-02、R-07、R-12、R-13、R-15、R-26、R-30、R-32 | 表述不精确或指代不清，内容本身正确 |
| 建议·EJOR 风格 | R-01、R-03、R-05、R-06、R-08 至 R-11、R-16 至 R-20、R-23、R-24、R-28、R-29、R-31 | 简洁性、句式、术语一致 |
| 撤回 | R-22 | 3.5 标题保持现状 |
| 格式·组稿时处理 | R-33 | 表格编号改为全文连续编号 |

**引文核查依据（R-25、R-27）**

| 文献 | 原文 | 结论 |
|---|---|---|
| Bartholdi & Hackman (2019) | 全书 5 处 "elevator" 均在第 17 章，定性说明多层设施中 "Freight elevators are likely to be bottlenecks to material flow"；没有把电梯容量表示为并行槽位的模型 | 不支持"$M_1$ is the throughput-aggregation convention of Bartholdi & Hackman (2019)" |
| Chakravarty et al. (2025) | "It is assumed that a lift can only service one robot at a time." "Extending the framework to handle shared rides ... is considered out of scope for this paper." | 支持"单机器人乘梯"，恰与同乘相反，不能用于 $M_2$ |
| Tadumadze et al. (2023) | 假设 A2 "Isolated warehouse levels: We do not allow robots and pods to switch warehouse levels, e.g., via an elevator." | 该文没有电梯，不能用于 $M_2$ |
| So & Al-Sharif (2019) | 目的地群控的实时分配："Once a passenger arrives at the main terminal and registers his/her destination floor, the corresponding elevator of that sector ... is assigned to this landing call. This process continues until P number of landing calls has been assigned to a particular elevator." | 支持"同一起点的请求按目的地分配到轿厢、至多达到容量"，可作为 $M_2$ 的依据 |

另：`references_chain_dominance.bib` 中 `so2019calculation` 的 DOI 写作 10.1016/j.jobe.2018.12.018，该号属于另一篇论文；Crossref 记录为 **10.1016/j.jobe.2019.01.013**（Journal of Building Engineering 22, 549–561），需一并更正。根目录全文 docx 的旧 §3（A5 段）有同样的错误归属，不要再复用该段。

**与 §4 的依赖**：§3 有两处指向 §4 的内容，即 3.4.2 的 "complementary distributional analysis in Section 4"（均值型 Wasserstein 比较）和鲁棒选择在评估器有序时的简化结论。二者都在 SECTION_4_METHODOLOGY.md 的 4.4 中，而 Methodology.docx 目前止于 4.3.2。按计划 v0.2 的 S4-2 补齐 4.4 后，这些引用才在 docx 层面成立；§3 本身不需要为此改动。

---

## 2. 翻译

全部内容（正文、图注、三张表、32 个公式）的中英对照见 [section3_bilingual_2026-09-24.md](section3_bilingual_2026-09-24.md)。译文对应的是 16:35 版原文；各段后以〔R-xx〕标出本文件中的修改建议，修改后的中文见下文各条。

---

## 3. 逐句修改对照

公式与符号按 Word 中的 MathType 对象以 LaTeX 书写；"修改前"均逐字取自 16:35 版 docx。

### 3.1 Problem setting and assumptions

#### R-01｜建议·风格｜3.1 第 1 段（整段）

**修改前**
> We consider a multi-story warehouse in which autonomous mobile robots (AMRs) transport orders between source and destination floors. The elevators are shared by all AMRs and are the only means of changing floors, so they are the vertical resource for which the AMRs contend. An AMR travels to an order's source, collects the load, and delivers it to the destination. The orders released together form a wave. Their origins, destinations, and ready times determine the vertical transport requests generated during wave execution. Fig. 1(a) sketches this setting.

**修改后**
> We consider a multi-story warehouse in which a fleet of autonomous mobile robots (AMRs) transports orders between source and destination floors. To serve an order, an AMR travels to the source floor, collects the load, and delivers it to the destination floor. A set of elevators shared by all AMRs provides the only means of changing floors, so the elevators are the vertical resource for which the AMRs compete. Orders released together form a wave, and their source floors, destination floors, and ready times determine the elevator requests generated when the wave is executed. Fig. 1(a) illustrates this setting.

**中文（修改后）**
> 本文考虑一个多层仓库，其中一支自主移动机器人（AMR）车队在订单的起始楼层与目标楼层之间运输订单。为完成一个订单，AMR 前往起始楼层取货，再将货物送至目标楼层。所有 AMR 共享一组电梯，电梯是跨楼层移动的唯一途径，因此构成 AMR 相互竞争的垂直资源。同时释放的订单构成一个波次，这些订单的起始楼层、目标楼层与就绪时间决定了波次执行过程中产生的电梯请求。图 1(a) 展示了这一场景。

**理由**：原段先写 "source and destination floors"，后写 "origins, destinations"，而后文 "origin-destination" 专指电梯请求的 $(g,h)$，订单端点应统一用 source/destination floor。"The elevators" 首次出现即用定冠词；"vertical transport requests" 与 3.5.1 的 "elevator request" 不一致。调整后先说明 AMR 如何完成订单，再引出电梯约束，符合漏斗顺序。

#### R-02｜建议·准确性｜图 1 图注

**修改前**
> Fig. 1. (a) Multi-story warehouse with an AMR fleet sharing $E$ elevators; a wave is a set of orders with source and destination floors, and AMRs change floors only by elevator trips; all resources start on the common floor $f^0$ at the release epoch $t_W$. (b) Serial reservation of one order $o_j^k$ under $M_2$: the AMR clock (available at $H_{a_j}^{j-1}$, ready at $t_W+r_o$, start $t_j^0$, pickup, delivery) and the five phases of the loaded elevator trip (wait, reposition, load, travel, unload); a request with the same origin-destination pair may join the trip until loading ends at $L_e$. Durations are illustrative.

**修改后**
> Fig. 1. Problem setting and serial reservation of one order. (a) A multi-story warehouse in which an AMR fleet shares $E$ elevators. A wave is a set of orders with source and destination floors; AMRs change floors only by elevator trips, and all resources start on a common floor $f^0$ at the release epoch $t_W$. (b) Reservation of one order under the true co-occupancy batching evaluator $M_2$ (Section 3.5.1). The panel shows the clock of the assigned AMR (availability, readiness, start, pickup, and delivery), the waiting time, and the four phases of the loaded elevator trip (repositioning, loading, travel, and unloading). A request with the same origin and destination floors can join the trip while capacity remains, until loading ends at $L_e$. Durations are illustrative.

**中文（修改后）**
> 图 1. 问题场景与单个订单的串行预约。(a) 多层仓库中，AMR 车队共享 $E$ 台电梯。一个波次是一组具有起始楼层和目标楼层的订单；AMR 只能通过电梯行程换层，所有资源在释放时刻 $t_W$ 均位于共同楼层 $f^0$。(b) 真实同乘批处理评估器 $M_2$（第 3.5.1 节）下单个订单的预约。图中给出被指派 AMR 的时钟（可用、就绪、开始、取货与交付）、等待时间，以及载货电梯行程的四个阶段（空驶调位、装载、运行与卸载）。起点和终点楼层相同的请求，在容量未满时可于装载在 $L_e$ 结束之前加入该行程。图中时长仅作示意。

**理由**：图 1 出现在 3.1，而 $o_j^k$、$H_{a_j}^{j-1}$、$t_j^0$、$M_2$ 的定义在 3.2 到 3.5；Elsevier 要求图注自足，改为文字说明并指向定义所在小节（符号仍保留在图内）。"five phases" 改为"等待时间与四个阶段"，与 A5 和式 (30) 的四个乘子一致。

#### R-03｜建议·风格（内容增补，需作者确认）｜3.1 第 2 段第 5、7 句

**修改前（第 5 句，保留不改；在其后插入新句）**
> The main formulation selects a structural class, defined by the floor distribution and directional balance of its candidate waves, and implements that choice through a fixed within-class selection rule.

**插入（第 5 句之后）**
> Formulating the decision over classes ties the release choice to interpretable properties of a wave. Because the classes are defined by quantiles within the pool, the same class definitions apply to any pool in which every class is nonempty.

**修改前（第 7 句）**
> Direct candidate selection provides a finite-pool benchmark whose exact value is obtained by evaluating all candidates under the specified evaluator.

**修改后（第 7 句）**
> Direct candidate selection is specific to one pool and provides a finite-pool benchmark, whose exact value is obtained by evaluating all candidates under the specified evaluator.

**中文（修改后）**
> 插入句：以类别为决策层次，使释放选择对应于波次的可解释性质。由于类别由池内分位数定义，只要每个类别都非空，同一组类别定义即可用于任意候选池。
> 第 7 句：直接选择候选波次只针对一个候选池，因而提供一个有限池基准，其精确值通过在指定评估器下评价全部候选波次得到。

**理由**：EJOR 要求说明建模选择的理由（"We use X because Y"）。现稿只说明在类别层面决策，没有说明原因；9 月 11 日版的理由"逐一排序候选需要评价整个池"已不成立（闭式评估器对 3000 个候选的全池评估不到一秒）。新理由只依赖定义：类别由 $C$、$I$ 两个可解释指标的池内分位数定义，因而对任何各类别均非空的候选池都有意义（3.3.3 要求每个类别非空）；池内最优只属于一个池。该句不引用任何实验结果。

#### R-04｜必改·与 §4 对齐｜3.1 第 2 段第 6 句

**修改前**
> Class-level performance is estimated from evaluated samples and compared across elevator representations.

**修改后**
> Class-level performance is obtained by evaluating the candidates of each class, exactly or from a sample, and is compared across elevator representations.

**中文（修改后）**
> 类别层面的绩效通过评价各类别中的候选波次得到（可精确计算，也可抽样估计），并在不同电梯表示之间进行比较。

**理由**：Methodology.docx 4.1.1 的式 (33) 在类支撑集上逐一评价候选、精确得到确定性评估器下的类别中位数，式 (34) 才是抽样估计；§3 只写"由样本估计"，与 §4 不一致。

**R-03 与 R-04 合并后的 3.1 第 2 段全文（便于整段粘贴）**
> The warehouse management system selects, at the release epoch, a wave of fixed size $n$ from a finite pool of $K$ candidate waves. Resource quantities and operational rules are given, so the decision concerns which orders enter the wave. The fixed size keeps candidates comparable and rules out shortening the completion time by releasing fewer orders. The order data and the candidate pool are known at the release epoch, whereas the representation of the elevator subsystem is uncertain and is described by a family of evaluators. The main formulation selects a structural class, defined by the floor distribution and directional balance of its candidate waves, and implements that choice through a fixed within-class selection rule. Formulating the decision over classes ties the release choice to interpretable properties of a wave. Because the classes are defined by quantiles within the pool, the same class definitions apply to any pool in which every class is nonempty. Class-level performance is obtained by evaluating the candidates of each class, exactly or from a sample, and is compared across elevator representations. Direct candidate selection is specific to one pool and provides a finite-pool benchmark, whose exact value is obtained by evaluating all candidates under the specified evaluator. The decision problem is to choose the class whose median wave makespan is smallest under the least favorable evaluator; the benchmark selects, for a given evaluator, the candidate whose makespan is smallest (Section 3.4).

### 3.2 Notation and decision variables

#### R-05｜建议·风格｜3.2.2 小节标题

**修改前**：3.2.2 Selection variables
**修改后**：3.2.2 Decision variables
**中文**：3.2.2 决策变量
**理由**：与 3.2 标题 "Notation and decision variables" 一致；EJOR 模型章节惯用 "decision variables"。

#### R-06｜建议·风格｜3.2.2 正文

**修改前**
> The decision of the class formulation is the class label $q\in\mathcal Q$, and the decision of the candidate benchmark is the candidate index $k\in\mathcal K$. Both decisions select one element from a finite set. The class decision solves Equation (15), while the candidate decision attains the minimum in Equation (17). Equation (32) expresses both decisions through a common binary program using the variables in Table 3.3. Their score coefficients are supplied by the operational evaluation of Section 3.5.

**修改后**
> The class formulation chooses a class label $q\in\mathcal Q$, and the candidate benchmark chooses a candidate index $k\in\mathcal K$; each decision selects one element of a finite set. Section 3.4 states the two decisions as optimization problems, and Section 3.5.1 writes both as one binary program in the variables of Table 3.3, with score coefficients supplied by the operational evaluation.

**中文（修改后）**
> 类别模型选择一个类别标签 $q\in\mathcal Q$，候选基准选择一个候选下标 $k\in\mathcal K$；两者都是从有限集合中选取一个元素。第 3.4 节把这两个决策写成优化问题，第 3.5.1 节再用表 3.3 的变量把二者写成同一个二元规划，其得分系数由运行评价给出。

**理由**：原段五句中有三句指向读者尚未见到的式 (15)、(17)、(32)，改为指向小节；"Their score coefficients" 中 Their 指代不清。

#### R-07｜建议·准确性｜表 3.2 的 $\sigma$ 行

**修改前**：$\sigma>0$ | lognormal phase-time noise parameter under $M_3$
**修改后**：$\sigma>0$ | standard deviation of the logarithm of each phase multiplier under $M_3$
**中文**：$M_3$ 下各阶段乘子对数的标准差
**理由**：由式 (2) $\log Z\sim\mathcal N(-\sigma^2/2,\sigma^2)$，$\sigma$ 的含义可以写准确。

#### R-08｜建议·风格｜表 3.3 的 $w_s$ 行

**修改前**：$w_s$ | $\{0,1\}$ | 1 if option $s$ of the index set $\mathcal S$ is selected ($\mathcal S=\mathcal Q$ for classes, $\mathcal S=\mathcal K$ for candidates)
**修改后**：$w_s$ | $\{0,1\}$ | 1 if option $s\in\mathcal S$ is selected, and 0 otherwise ($\mathcal S=\mathcal Q$ for the class formulation, $\mathcal S=\mathcal K$ for the candidate benchmark)
**中文**：若选中选项 $s\in\mathcal S$ 则取 1，否则取 0（类别模型中 $\mathcal S=\mathcal Q$，候选基准中 $\mathcal S=\mathcal K$）
**理由**：EJOR 对二元变量的标准释义为 "equals 1 if …, and 0 otherwise"。

#### R-09｜建议·风格｜3.2.3 第 2 段（整段）

**修改前**
> Conditional on the selected order set, each permutation is equally likely under the candidate-generation procedure. Each candidate retains its recorded sequence across evaluators, so their comparison uses the same prescribed order sequence. Variation in these recorded sequences contributes to within-class outcome variation. All class and candidate results use the recorded sequences; Section 5 reports an alternative operational dispatch rule that reorders the sequence as a separately labeled robustness check.

**修改后**
> Under the generation procedure, the recorded sequence $\pi^k$ is equally likely to be any permutation of the order set $W^k$. Because each candidate keeps its recorded sequence under every evaluator, differences between evaluators on the same candidate do not arise from resequencing. Across candidates, the sequences vary and contribute to the outcome variation within a class. All class and candidate results use the recorded sequences; Section 5 reports one alternative operational dispatch rule, which reorders the sequence, as a separately labeled robustness check.

**中文（修改后）**
> 在候选生成过程中，记录序列 $\pi^k$ 等可能地取订单集合 $W^k$ 的任一排列。由于每个候选在所有评估器下保持同一记录序列，同一候选在不同评估器之间的差异并非来自序列的重排。不同候选的序列各不相同，这构成类内结果变异的一部分。所有类别与候选结果均采用记录序列；第 5 节另报告一种会重排序列的运行层调度规则，作为单独标注的稳健性检验。

**理由**："their comparison" 指代不清，且与上段 "shared by all evaluators" 重复；"Conditional on the selected order set" 中的 selected 易与决策层的"选择"混淆。注意：同一序列仍会影响两个评估器各自的完工时间及其差值（能否同乘取决于请求顺序），所以只能说差异不来自重排，不能说不受排序影响。

#### R-10｜建议·风格｜3.2.3 第 4 段第 2、3 句

**修改前**
> The phase-noise source is independent of the within-class candidate draw $\kappa\sim\nu_q$ introduced in Section 3.3.3. Given a candidate wave k, an evaluator m, and a phase-time realization $\xi$ when $m=M_3$, the operational rules determine all state quantities and order completion times.

**修改后**
> The phase multipliers are independent of the within-class candidate draw $\kappa\sim\nu_q$ introduced in Section 3.3.3. Given a candidate $k$, an evaluator $m$, and, when $m=M_3$, a phase-time realization $\xi$, the operational rules determine all state quantities and order completion times.

**中文（修改后）**
> 阶段乘子与第 3.3.3 节引入的类内候选抽样 $\kappa\sim\nu_q$ 相互独立。给定候选 $k$、评估器 $m$，以及当 $m=M_3$ 时的阶段时长实现 $\xi$，运行规则即可确定全部状态量与订单完成时间。

**理由**："phase-noise source" 不是已定义的对象；$k$ 是下标而非波次；docx 中此处的 k、m 为正文字母，应改为数学对象。

### 3.3 Candidate waves and structural classes

#### R-11｜建议·风格｜3.3.1 第 1、3 句

**修改前（第 1 句）**
> Each candidate index $k\in\mathcal K$ identifies an unordered order set $W^k\subseteq\mathcal O$ containing $n$ orders and its recorded processing sequence $\pi^k$.

**修改后（第 1 句）**
> Each candidate index $k\in\mathcal K$ identifies an order set $W^k\subseteq\mathcal O$ and its recorded processing sequence $\pi^k$.

**修改前（第 3 句）**
> Whenever two evaluators are compared on the same decision, as in the robust selection of Section 3.4.2, the same pool is used for both; Section 5 states, for each experimental block, whether the pool is shared across evaluators.

**修改后（第 3 句）**
> Evaluators compared on the same decision, as in the robust selection of Section 3.4.2, use the same pool; Section 5 states whether the pools of each experiment are shared across evaluators.

**中文（修改后）**
> 第 1 句：每个候选下标 $k\in\mathcal K$ 对应一个订单集合 $W^k\subseteq\mathcal O$ 及其记录的处理序列 $\pi^k$。
> 第 3 句：在同一决策下比较的评估器（如第 3.4.2 节的鲁棒选择）使用同一候选池；第 5 节说明各项实验的候选池是否在评估器之间共享。

**理由**："unordered order set" 冗余，订单数 $n$ 已由式 (3) 规定，一处定义即可；"experimental block" 是第 5 节的实验术语，模型章节改为一般表述。

#### R-12｜建议·准确性｜3.3.2 第 3 段第 3 至 5 句（并建议在 "Directional imbalance" 前分段）

**修改前**
> It describes how endpoints are distributed among floors; travel distances are determined by the numerical differences between the relevant floor indices. Directional imbalance measures the asymmetry between upward and downward order movements. Their counts are

**修改后**
> $C$ depends only on how endpoints are distributed over the floors, not on the distances between them; travel distances enter the evaluation through the floor differences in Equations (24), (28), and (30).
>
> Directional imbalance measures the asymmetry between upward and downward order movements. The numbers of upward and downward orders are

**中文（修改后）**
> $C$ 只取决于端点在各楼层上的分布，而与楼层之间的距离无关；行程距离通过式 (24)、(28) 与 (30) 中的楼层差进入评价。
>
> 方向失衡度衡量订单上行与下行移动之间的不对称程度。上行与下行订单的数量分别为

**理由**：原句以解释性口吻说明 $C$ 不含距离信息，改为直接陈述并指出距离进入模型的位置（AGENT.md 第 2 条）；"Their counts" 指代不清；$C$ 与 $I$ 各是一个定义，分段后每段一职。

#### R-13｜建议·准确性｜3.3.2 第 5 段第 3、4 句（并建议在此处分段）

**修改前**
> The ready-time dispersion $T$ measures how order eligibility is spread within the wave. The mean ready-time offset is $\bar r_W=|W|^{-1}\sum_{o\in W}r_o$, and its relative dispersion is defined as

**修改后**
> The ready-time dispersion $T$ measures how order eligibility is spread within the wave. The mean ready-time offset is $\bar r_W=|W|^{-1}\sum_{o\in W}r_o$, and $T$ is the coefficient of variation of the offsets:

**中文（修改后）**
> 就绪时间离散度 $T$ 衡量波次内订单可处理时刻的分散程度。平均就绪时间偏移为 $\bar r_W=|W|^{-1}\sum_{o\in W}r_o$，$T$ 为各偏移量的变异系数：

**理由**："its relative dispersion" 中 its 语法上指均值，含义不通；直接说明式 (8) 是变异系数，与 `features.py` 的实现一致。

#### R-14｜必改·与 §4 对齐｜3.3.3 第 2 段第 2 句

**修改前**
> The labels $\mathrm{HH},\mathrm{HL},\mathrm{LH},\mathrm{LL}$ record the tails of $C$ and $I$, respectively (written HC-HI, HC-LI, LC-HI, LC-LI, in the same order, where Sections 4 and 5 report per-corner results), with candidate-index supports

**修改后**
> In the labels $\mathrm{HH},\mathrm{HL},\mathrm{LH},\mathrm{LL}$, the first letter records the tail of $C$ and the second the tail of $I$. Section 5 writes these labels as HC-HI, HC-LI, LC-HI, and LC-LI, respectively. The candidate-index supports are

**中文（修改后）**
> 在标签 $\mathrm{HH},\mathrm{HL},\mathrm{LH},\mathrm{LL}$ 中，第一个字母表示 $C$ 所处的尾部，第二个字母表示 $I$ 所处的尾部。第 5 节将这些标签依次写作 HC-HI、HC-LI、LC-HI 和 LC-LI。各类别的候选下标支撑集为

**理由**：Methodology.docx 全文没有使用 HC-HI 这组标签（§4 以 $q_{\min}$、$q_{\max}$、$b_q$ 表述），"Sections 4 and 5" 与 §4 不符；长括号插入语不符合 EJOR 的简洁要求，"respectively" 的对应关系也不清楚。第 5 节现有底稿与结果表写作 HC_HI 或 HC·HI，定稿时须统一为 HC-HI（记入 §5 交接）。

#### R-15｜建议·准确性｜3.3.3 第 3 段（整段，拆为两段）

**修改前**
> The selectable labels form $\mathcal Q=\{\mathrm{HH},\mathrm{HL},\mathrm{LH},\mathrm{LL}\}$, the corner labels of Equation (11). A class-selection instance requires $\mathcal K_q\ne\varnothing$ for every $q\in\mathcal Q$, so that the class median of Equation (14) is defined for every selectable class. For continuous, independent descriptors the fraction of the pool in each class is of order $\alpha^2$; it can differ from this value when $C$ and $I$ are dependent, and also when the descriptors take few distinct values, because the inclusive thresholds in Equation (10) place every candidate tied at a threshold into the tail set. Candidates outside all four intersections remain in the candidate pool but outside the corner classes, so the classes do not cover the pool. Because the tail inequalities include their thresholds, quantile ties can produce overlapping supports, in which case a candidate belongs to more than one class; this affects the sampling distributions below but not their definitions. Section 5 reports the realized class sizes and overlaps. Each selectable class is implemented by uniform sampling over its candidate indices. The fixed within-class distribution is

**修改后**
> The selectable labels form $\mathcal Q=\{\mathrm{HH},\mathrm{HL},\mathrm{LH},\mathrm{LL}\}$. A class-selection instance requires $\mathcal K_q\ne\varnothing$ for every $q\in\mathcal Q$, so that the class median in Equation (14) is defined for every selectable class. For continuous and independent descriptors, each class contains approximately a fraction $\alpha^2$ of the pool. The fraction can differ when $C$ and $I$ are dependent. It can also differ when a descriptor takes few distinct values, because the inclusive thresholds in Equation (10) assign every candidate tied at a threshold to the tail set. The classes need not cover the pool, since candidates outside the four intersections belong to no class. Conversely, when ties make the lower and upper thresholds of a descriptor coincide, a candidate can belong to more than one class. Section 5 reports the realized class sizes and overlaps.
>
> Each selectable class is implemented by uniform sampling over its candidate indices, with the fixed within-class distribution

**中文（修改后）**
> 可选标签集合为 $\mathcal Q=\{\mathrm{HH},\mathrm{HL},\mathrm{LH},\mathrm{LL}\}$。一个类别选择实例要求对每个 $q\in\mathcal Q$ 都有 $\mathcal K_q\ne\varnothing$，以保证式 (14) 中的类别中位数对每个可选类别都有定义。当两个描述指标连续且相互独立时，每个类别约占候选池的 $\alpha^2$。若 $C$ 与 $I$ 相关，这一比例可能偏离该值。当某一描述指标的取值很少时，比例同样可能偏离，因为式 (10) 的阈值包含等号，恰好落在阈值上的候选都被划入尾部集合。各类别不必覆盖整个候选池，落在四个交集之外的候选不属于任何类别。反之，当并列值使某一描述指标的下、上阈值重合时，一个候选可能同时属于多个类别。第 5 节报告实际的类别规模与重叠情况。
>
> 每个可选类别通过在其候选下标上均匀抽样来实施，固定的类内分布为

**理由**：原段同时承担定义 $\mathcal Q$、非空条件、规模近似、不覆盖、重叠、第 5 节指引与类内规则七项职责，拆为两段。"of order $\alpha^2$" 不精确。"this affects the sampling distributions below but not their definitions" 属预设质疑的解释性说明。由于 $\alpha<0.5$，同一候选同属两个尾部只可能发生在该指标的 $Q_\alpha$ 与 $Q_{1-\alpha}$ 相等时，原文 "quantile ties can produce overlapping supports" 没有说明这一条件。紧接式 (11) 的 "the corner labels of Equation (11)" 可删。

#### R-16｜建议·风格｜3.3.3 第 4 段第 1、2 句

**修改前**
> Selecting class q therefore leads to a draw $\kappa\sim\nu_q$ and the release of $W^\kappa$. The class choice determines the distribution of the released wave, while its within-class sampling rule remains fixed.

**修改后**
> Selecting class $q$ releases the wave $W^\kappa$ with $\kappa\sim\nu_q$. The class choice thus determines the distribution of the released wave, while the within-class rule is fixed.

**中文（修改后）**
> 选择类别 $q$ 即释放波次 $W^\kappa$，其中 $\kappa\sim\nu_q$。因此，类别选择决定所释放波次的分布，而类内规则保持固定。

**理由**：更简洁；"its within-class sampling rule" 中 its 指代类别选择，含义不准；docx 中此处的 q 为正文字母，应改为数学对象。

### 3.4 Objective functions

#### R-17｜建议·风格｜3.4.1 第 1 句

**修改前**
> Restoring the candidate, evaluator, and realization indices gives the order completion time $t^C_{jkm}(\xi)$.

**修改后**
> With the candidate, evaluator, and phase-time realization made explicit, $t^C_{jkm}(\xi)$ denotes the completion time of the order in position $j$ of candidate $k$ (Section 3.5.1).

**中文（修改后）**
> 在显式写出候选、评估器与阶段时长实现后，$t^C_{jkm}(\xi)$ 表示候选 $k$ 中位于第 $j$ 个位置的订单的完成时间（第 3.5.1 节）。

**理由**："Restoring … indices" 依赖读者记得 3.2.3 末句的省略约定；改为直接说明该符号的含义与定义位置。

#### R-18｜建议·风格｜3.4.2 第 1 段第 2 句

**修改前**
> The median is the statistic for which the class-level decomposition of Section 4 is stated and the statistic that Section 5 estimates per class, so using it here keeps the decision problem, the analysis, and the experiments on one estimand.

**修改后**
> We use the median because Section 4 states its class-level diagnosis for it and Section 5 reports it for each class, so the decision problem, the analysis, and the experiments share one estimand.

**中文（修改后）**
> 采用中位数，是因为第 4 节的类别层面诊断以中位数表述，第 5 节也按类别报告中位数，从而使决策问题、分析与实验使用同一个估计目标。

**理由**："We use X because Y" 是 EJOR 说明建模选择的常用句式；与 §4 的 "class-relative performance diagnosis" 用词一致。理由仍是一致性而非稳健性，符合预注册修正案 A3 的限制。

#### R-19｜建议·风格｜3.4.2 第 2 段最后两句

**修改前**
> This mean is used in the complementary distributional analysis in Section 4 and its numerical assessment in Section 5. The class-selection objective in this formulation uses the median defined in Equation (14).

**修改后**
> This mean enters the complementary distributional analysis of Section 4 and its numerical assessment in Section 5; the class-selection objective uses the median.

**中文（修改后）**
> 该均值用于第 4 节的补充分布分析及其在第 5 节的数值评估；类别选择目标使用中位数。

**理由**：原末句与本小节首句 "The performance of a class is the median makespan" 重复。不写 "only"，因为第 5 节还会报告策略层面的均值。本句所指的补充分布分析在 SECTION_4_METHODOLOGY.md 的 4.4.3，尚未并入 Methodology.docx（原句同样依赖这一点，见第 1 节"与 §4 的依赖"）。

#### R-20｜建议·风格｜3.4.2 第 3 段第 3、4 句

**修改前**
> Its two members are distinct hypotheses about how elevator capacity acts, parallel slots under $M_1$ versus shared trips under $M_2$, and this is the uncertainty the robust selection covers. $M_3$ retains the reservation rules of $M_2$ and adds mean-one phase multipliers (Equation (2)), so it is a perturbation of $M_2$ rather than a third capacity hypothesis; it assesses a selected class under trip-time variability, and Section 4 characterizes the ordering within $\mathcal M_D$.

**修改后**
> Its two members represent two hypotheses on how elevator capacity acts: as parallel single-request slots under $M_1$ or as shared trips under $M_2$. The robust selection hedges against this structural uncertainty, and Section 4.3 gives sufficient conditions under which the two evaluators are ordered. $M_3$ retains the reservation rules of $M_2$ and adds mean-one phase multipliers (Equation (2)). It is therefore a perturbation of $M_2$ rather than a third capacity hypothesis, and it is used to assess a selected class under trip-time variability.

**中文（修改后）**
> 这两个成员代表关于电梯容量如何起作用的两种假说：在 $M_1$ 下表现为并行的单请求槽位，在 $M_2$ 下表现为共享行程。鲁棒选择针对的正是这一结构性不确定性，第 4.3 节给出两个评估器有序的充分条件。$M_3$ 沿用 $M_2$ 的预约规则，并加入均值为 1 的阶段乘子（式 (2)）。因此，$M_3$ 是 $M_2$ 的扰动，而不是第三种容量假说，它用于评估所选类别在行程时长波动下的表现。

**理由**："and this is the uncertainty the robust selection covers" 口语化；原句末 "and Section 4 characterizes the ordering within $\mathcal M_D$" 接在 $M_3$ 的句子里，主语错位，移到 $\mathcal M_D$ 的句子中；"characterizes" 也言过其实，Methodology.docx 的 4.3 只给出排序的充分条件与反转机制。

#### R-21｜必改·与 §4 对齐｜3.4.2 第 4 段第 1 句

**修改前**
> The class medians are not observed at the release epoch; Section 5 estimates them from evaluated samples of each class, and Section 4 analyzes selection rules that act on such estimates.

**修改后**
> The class medians are not observed at the release epoch; Section 4.1 obtains them by evaluating the candidates of each class, exactly or by sampling, and applies the selection rule to the resulting scores.

**中文（修改后）**
> 类别中位数在释放时刻不可观测；第 4.1 节通过评价各类别的候选波次得到这些中位数（精确计算或抽样估计），并将选择规则作用于所得分数。

**理由**：与 R-04 同；对应 Methodology.docx 的式 (33) 到 (35)。该段第 2 句（$q_\Phi$）不变。

### 3.5 Constraints and their explanation

#### R-22｜撤回｜3.5 各级标题

原建议把 3.5、3.5.1、3.5.2 分别改为 "Operational evaluation and constraints"、"Reservation rules and constraints"、"Interpretation"。撤回理由：EJOR 写作规范的模型模板本身把这一部分称为 "Constraints"，主控 §6 也按现标题记录了你确认的结构，现标题可以保留。若仍想改名，须同步主控，且 3.5.2 宜用 "Interpretation of the rules"，不要单用 "Interpretation"。

#### R-23｜建议·风格｜3.5.1 第 1 段（整段）

**修改前**
> The evaluators are deterministic serial reservation models, apart from the phase noise of $M_3$: they do not simulate concurrent execution, and the request timestamps generated along the processing sequence need not be globally increasing; Fig. 1(b) illustrates the reservation of one order. Section 5 cross-validates them against an event-driven simulation that is built on the same physical specification but executes trips concurrently.

**修改后**
> The three evaluators are serial reservation models, deterministic except for the phase multipliers of $M_3$. Orders are reserved one at a time along the processing sequence, so the evaluators do not simulate concurrent execution, and the request times they generate need not increase along the sequence. Fig. 1(b) illustrates the reservation of one order. Section 5 cross-validates the evaluators against an event-driven simulation that uses the same physical specification but executes trips concurrently.

**中文（修改后）**
> 三个评估器均为串行预约模型，除 $M_3$ 的阶段乘子外都是确定性的。订单沿处理序列逐一预约，因此评估器并不模拟并发执行，其生成的请求时刻也不必沿序列递增。图 1(b) 展示了单个订单的预约过程。第 5 节以一个事件驱动仿真对评估器进行交叉验证，该仿真采用相同的物理设定，但行程并发执行。

**理由**：原句冒号后连接两个结论，没有给出原因；改为先说明"逐单预约"，再给出两个后果。

#### R-24｜建议·风格｜"Processing sequence and AMR assignment" 段第 2 句

**修改前**
> The quantities $H_a^{j-1}$ and $G_a^{j-1}$ denote AMR a's next availability time and associated floor after the first $j-1$ orders have been reserved, respectively, with initial values $H_a^0=t_W$ and $G_a^0=f^0$.

**修改后**
> After the first $j-1$ orders have been reserved, $H_a^{j-1}$ denotes the next availability time of AMR $a$ and $G_a^{j-1}$ the floor at which it becomes available; initially, $H_a^0=t_W$ and $G_a^0=f^0$.

**中文（修改后）**
> 在前 $j-1$ 个订单完成预约后，$H_a^{j-1}$ 表示 AMR $a$ 的下一可用时刻，$G_a^{j-1}$ 表示其届时所在的楼层；初始时 $H_a^0=t_W$，$G_a^0=f^0$。

**理由**："respectively" 远离所对应的两个符号，难以对应；docx 中 "AMR a" 的 a 为正文字母，应改为数学对象。

#### R-25｜必改·引文｜吞吐抽象 $M_1$ 段末句

**修改前**
> $M_1$ is the throughput-aggregation convention of Bartholdi & Hackman (2019) .

**修改后**
> Each slot carries one request per trip, the single-rider assumption that Chakravarty et al. (2025) adopt for multi-robot lift scheduling, in which each lift serves one robot at a time.

**中文（修改后）**
> 每个槽位每趟行程只载一个请求，这与 Chakravarty et al. (2025) 在多机器人电梯调度中采用的单乘假设相同，即每台电梯一次只服务一台机器人。

**理由**：Bartholdi & Hackman (2019) 没有把电梯容量表示为并行槽位的模型（见第 1 节核查表），原句是错误归属；另有两处格式问题（"&" 为 APA 写法，EJOR 叙述式引用用 "and"；"(2019)" 与句点之间多一个空格）。替换句的依据是 Chakravarty et al. (2025) 原文 "It is assumed that a lift can only service one robot at a time."。改写后只把"单乘"归于该文，不暗示该文用并行槽位表示容量（该文的电梯容量为 1）。若不需要文献锚点，也可直接删除此句。

#### R-26｜建议·准确性｜真实同乘批处理 $M_2$ 段的两处

**修改前（登乘条件句）**
> A request can share a stored trip when its origin and destination match, capacity remains, and it is ready no later than loading ends.

**修改后**
> A request can share a stored trip when its origin and destination match those of the trip, the trip has remaining capacity, and the request time is no later than the end of loading.

**修改前（加入后的两句）**
> The joining request shares the trip's stored completion time, and its other reservation quantities remain unchanged. A joining request may have a request time earlier than the start of the stored trip; it then waits for that trip and shares its completion time.

**修改后**
> The joining request shares the trip's stored completion time; apart from the occupancy update in Equation (26), the car's reservation record is unchanged. A request may also join a trip that starts after its request time, in which case it waits for that trip.

**中文（修改后）**
> 登乘条件句：当请求的起点与终点和已存行程一致、该行程仍有剩余容量，且请求时刻不晚于装载结束时刻时，请求可共享该行程。
> 加入后的两句：加入的请求共享该行程已存的完成时刻；除式 (26) 中的占用数更新外，轿厢的预约记录保持不变。请求也可以加入一个在其请求时刻之后才开始的行程，此时该请求等待这一行程。

**理由**：式 (25) 比较的是请求时刻 $t\le L_e$，"it is ready no later than loading ends" 与之不精确对应；"its other reservation quantities" 中 its 应指轿厢；原第二句重复了"共享完成时刻"。

#### R-27｜必改·引文｜真实同乘批处理 $M_2$ 段末句

**修改前**
> $M_2$ follows the explicit co-occupancy convention used for shared lifts and vehicles (Chakravarty et al., 2025; Tadumadze et al., 2023).

**修改后**
> $M_2$ shares a trip only among requests with the same origin and destination. This is a restricted form of the destination-based grouping of destination group control, in which requests from a common origin are assigned to cars by destination until the car capacity is reached (So and Al-Sharif, 2019).

**中文（修改后）**
> $M_2$ 只在起点和终点都相同的请求之间共享行程。这是目的地群控按目的地编组的一种受限形式；在目的地群控中，来自同一起点的请求按目的地分配到轿厢，直至达到轿厢容量（So and Al-Sharif, 2019）。

**理由**：Chakravarty et al. (2025) 假设每台电梯一次只服务一台机器人，并明确把同乘列为范围之外；Tadumadze et al. (2023) 假设楼层隔离、不经电梯换层。两者都不支持同乘约定。So & Al-Sharif (2019) 的实时分配规则是"乘客在大堂登记目的地后，被分配到覆盖该目的地所在分区的电梯，直至该电梯被分配满 P 个呼叫"，支持修改后的表述；"restricted form" 说明 $M_2$ 只合并同一起终点对，比目的地群控的分区编组更严格。需同时把 bib 中该条目的 DOI 更正为 10.1016/j.jobe.2019.01.013。Word 中原句的 $M_2$ 公式对象与 "follows" 之间没有空格，查找时请搜 "follows the explicit co-occupancy convention"。

#### R-28｜建议·风格｜"Resource conditions" 段第 2 句

**修改前**
> In addition, trips reserved on the same car (or slot under $M_1$) do not overlap: a new trip begins its empty repositioning no earlier than $B_e$ (formally, at $\max\{t,B_e\}$), where $B_e$ is the completion time of that car's previous trip.

**修改后**
> In addition, trips reserved on the same car, or on the same slot under $M_1$, do not overlap. Each new trip begins its empty repositioning at $\max\{t,B_e\}\ge B_e$, where $B_e$ is the completion time of the previous trip on that car ($B_v$ for a slot under $M_1$).

**中文（修改后）**
> 此外，同一轿厢（在 $M_1$ 下为同一槽位）上预约的行程互不重叠。每趟新行程的空驶调位开始于 $\max\{t,B_e\}\ge B_e$，其中 $B_e$ 为该轿厢上一趟行程的完成时刻（在 $M_1$ 下为槽位的 $B_v$）。

**理由**：两层括号插入语改为因果句，含义不变。

#### R-29｜建议·风格｜3.5.2 "Processing sequence and AMR assignment" 段第 1 句

**修改前**
> The processing sequence is the candidate-specific permutation $\pi^k$ in Equation (1) and remains unchanged by order readiness; an order that is not yet eligible holds its assigned AMR until $t_W+r_o$, which the maximum in Equation (18) enforces together with resource availability.

**修改后**
> The processing sequence is the candidate-specific permutation $\pi^k$ in Equation (1) and is not reordered by readiness. An order that is not yet eligible holds its assigned AMR until $t_W+r_o$, which the maximum in Equation (18) enforces together with resource availability.

**中文（修改后）**
> 处理序列即式 (1) 中各候选特有的排列 $\pi^k$，不会按就绪时间重新排序。尚未具备处理资格的订单会占用其被指派的 AMR，直至 $t_W+r_o$，这一点由式 (18) 中的最大值运算与资源可用性共同保证。

**理由**："remains unchanged by order readiness" 不是地道的英文表达。

#### R-30｜建议·准确性｜3.5.2 吞吐抽象 $M_1$ 段

**修改前**
> Equation (24) charges every request the full five-phase trip, so capacity acts only through the number of slots that can serve requests at the same time; two requests with the same origin and destination never share a trip.

**修改后**
> Equation (24) charges every request its waiting time and a complete trip of repositioning, loading, loaded travel, and unloading. Capacity therefore acts only through the number of slots that can serve requests at the same time, and two requests with the same origin and destination never share a trip.

**中文（修改后）**
> 式 (24) 为每个请求计入其等待时间，以及由空驶调位、装载、载货运行和卸载组成的一趟完整行程。因此，容量只通过可同时服务请求的槽位数量起作用，即使两个请求的起点和终点相同，也不会共享行程。

**理由**："five-phase trip" 与 A5 把行程描述为四段、式 (30) 的四个乘子不一致；等待不属于行程的物理阶段，改为分别列出。

#### R-31｜建议·风格｜3.5.2 真实同乘批处理 $M_2$ 段

**修改前**
> Elevator requests are processed in the prescribed reservation sequence. When the boardable-car set in Equation (25) is nonempty, the request joins the lowest-index eligible car and shares its stored completion time. Otherwise, Equations (27)–(29) reserve a new trip on the earliest-available car, with repositioning starting no earlier than that car's recorded availability. The boarding test takes priority over new-trip assignment, so an eligible shared trip is selected even when a dedicated trip on another car could finish sooner.

**修改后**
> Trips are reserved in the order of the processing sequence, so a new trip starts only after the trips already reserved on its car have been completed, even when its request time is earlier. The boarding test in Equation (25) also takes priority over new-trip assignment in Equations (27)–(29), so an eligible shared trip is selected even when a dedicated trip on another car could finish sooner.

**中文（修改后）**
> 行程按处理序列的顺序预约，因此即使新行程的请求时刻更早，它也只能在其轿厢上已预约行程完成之后开始。此外，式 (25) 的登乘检验优先于式 (27)–(29) 的新行程分配，因此即使另一轿厢上的专用行程能更早完成，也会选择符合条件的共享行程。

**理由**：原段第 2、3 句复述 3.5.1 的规则；解释小节应说明规则的后果（按序预约与登乘优先），而不重述规则本身。

#### R-32｜建议·准确性｜3.5.2 随机批处理 $M_3$ 段

**修改前**
> Waiting follows from resource availability, while pickup and drop-off durations remain fixed.

**修改后**
> Only the four elevator trip phases carry multipliers. Waiting times carry none and change only as a consequence of the perturbed durations of earlier trips, while pickup and drop-off durations remain fixed.

**中文（修改后）**
> 只有电梯行程的四个阶段带有乘子。等待时间本身不带乘子，只因此前行程时长的扰动而间接变化；取货与卸货时长保持不变。

**理由**："Waiting follows from resource availability" 含义模糊，没有说明扰动作用于哪些时长。等待时间 $\max\{t,B_e\}-t$ 中的请求时刻 $t$ 与可用时刻 $B_e$ 都会因此前行程的扰动而变化，登乘判断也以扰动后的 $L_e$ 为准。与代码一致：噪声只在新行程派车时施加于四个阶段，服务时长不扰动。

#### R-34｜必改·排版｜式 (7) 的 MathType 对象

**问题**：式 (7) 中 8 处 $N^{\uparrow}(W)$、$N^{\downarrow}(W)$ 的左括号被排进了上标，以上标字号印出，看起来像 $N^{\uparrow(}W)$；右括号正常。式 (6) 中同一符号排版正确。
**改法**：在 MathType 中打开式 (7)，把每个左括号从上标槽移回基线，使其与式 (6) 的写法一致。
**应为**

$$
I(W)=\begin{cases}\dfrac{\left|N^{\uparrow}(W)-N^{\downarrow}(W)\right|}{N^{\uparrow}(W)+N^{\downarrow}(W)}, & N^{\uparrow}(W)+N^{\downarrow}(W)>0,\[3mm] 0, & N^{\uparrow}(W)+N^{\downarrow}(W)=0.\end{cases}\tag{7}
$$

**理由**：读者会把 "↑(" 读成一个上标，括号的配对也显得错位。

### 全局

#### R-33｜格式·组稿时处理｜表格编号

**修改前**：Table 3.1、Table 3.2、Table 3.3（表题与 3.2.1、3.2.2、"Selection program" 段中的引用）
**修改后**：按全文出现顺序连续编号，如 Table 1、Table 2、Table 3
**理由**：Elsevier 期刊（含 EJOR、C&IE）要求表格在全文中连续编号，不按章节编号。若第 2 节按主控计划加入文献对照表，§3 的三张表应依次为 Table 2 至 Table 4。图已按 Fig. 1、Fig. 2 连续编号，无需改动。

**不需改动的全局项**：正文统一使用 "Equation (n)"，与 Methodology.docx 一致，保持即可；全节无破折号，拼写均为美式。
