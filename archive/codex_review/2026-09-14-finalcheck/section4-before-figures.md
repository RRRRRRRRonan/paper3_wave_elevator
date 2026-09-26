---
title: "Section 4. Methodology / 方法"
date: 2026-09-11
status: "method-first bilingual manuscript draft"
model_contract: "SECTION_3_MODEL_FORMULATION.md, version dated 2026-09-10"
scope: "robust single-wave class selection with class-relative diagnosis and conditional evaluator-ordering analysis"
equation_numbering: "continues Section 3 from Equation (33)"
verification_status: "definitions and theoretical statements reconciled; production-code alignment, experiment recomputation, and final appendix integration remain separate"
---

# 4. Methodology / 方法

We use a simulation-based robust class-selection framework to determine the structural class from which a wave is released. Given the candidate pool and class definitions in Section 3, candidate waves are evaluated under the two deterministic elevator models using common order data and prescribed reservation rules. Each class is scored by the larger of its two median makespans. The framework selects the class with the smallest such score and implements the decision by drawing a candidate wave from its fixed within-class distribution.

> **中文：** 本研究采用基于模拟评价的鲁棒类别选择框架，确定释放波次所属的结构类别。在第 3 节给定的候选池和类别定义下，两个确定性电梯模型依据相同订单数据与规定的预约规则评价候选波次。每个类别以其在两个模型下完工期中位数中的较大值作为得分。该框架选择得分最小的类别，并按照固定的类内分布抽取候选波次，落实释放决策。

Two analyses support this selection framework. A class-level diagnostic measures performance differences across the selectable classes and the loss associated with a prespecified class-selection rule. A paired analysis of elevator requests establishes sufficient conditions for ordering the two evaluators and identifies mechanisms that can reverse that ordering. When the \(M_2\) median is no smaller in every selectable class, the robust decision reduces to selecting the class with the smallest \(M_2\) median; departures from this ordering are assessed through class-score differences and ranking margins.

> **中文：** 两项分析为该选择框架提供支持。类别层面的诊断衡量可选类别之间的绩效差异，以及预先规定的类别选择规则所产生的损失。电梯请求的配对分析建立两个评估器之间排序关系的充分条件，并说明可能导致排序反转的机制。当每个可选类别在 \(M_2\) 下的中位数均不小于其在 \(M_1\) 下的中位数时，鲁棒决策简化为选择 \(M_2\) 中位数最小的类别；偏离这一排序时，则通过类别得分差异和排序间隔分析选择的稳定性。

## 4.1 Robust class-selection procedure / 鲁棒类别选择流程

### 4.1.1 Candidate evaluation and class scores / 候选评价与类别得分

The procedure takes the candidate pool, structural classes, resource configuration, and within-class release distributions defined in Section 3 as inputs. Each candidate is evaluated under \(M_1\) and \(M_2\) using the same order sequence and initial state. For each class and evaluator, the deterministic median is obtained exactly from one equally weighted outcome per candidate in its support, retaining repeated outcome values:

> **中文：** 流程以第 3 节定义的候选池、结构类别、资源配置和类内释放分布为输入。每个候选均在相同订单序列和初始状态下接受 \(M_1\) 与 \(M_2\) 的评价。对于每个类别和评估器，支持集中的每个候选对应一个等权结果，确定性中位数由这些结果精确计算；不同候选即使具有相同结果值，也各自保留相应权重：

\[
\mu_{qm}^{0.5}
=\operatorname{Med}_{k\in\mathcal K_q}Y_{km},
\qquad m\in\mathcal M_D.
\tag{33}
\]

When class scores are estimated by sampling, \(R_q\) candidate indices \(\kappa_{qr}\sim\nu_q\) are drawn independently, and the same draws are used across evaluators. For evaluations under \(M_3\), phase-time realizations \(\xi_{qr}\) are independent across replications and independent of the candidate indices. The estimated class median is

> **中文：** 类别得分采用抽样估计时，\(R_q\) 个候选索引按照 \(\kappa_{qr}\sim\nu_q\) 独立抽取，各评估器使用同一组候选抽样结果。在 \(M_3\) 下进行评价时，阶段时间实现 \(\xi_{qr}\) 在不同重复之间相互独立，并且与候选索引独立。类别中位数的估计值为：

\[
\widehat\mu_{qm}^{0.5}
=\operatorname{Med}_{r=1,\ldots,R_q}
Y_{\kappa_{qr}m}(\xi_{qr}),
\tag{34}
\]

where \(\xi_{qr}\) is omitted for deterministic evaluators. For \(M_1\) and \(M_2\), candidate sampling is the source of variation in this estimate. Under \(M_3\), it also incorporates phase-time variation, matching the joint outcome distribution in Equation (14). All medians follow the midpoint convention in Section 3.4.2. Section 5 specifies the sampling sizes and uncertainty analysis.

> **中文：** 其中，确定性评估器的记号中不含 \(\xi_{qr}\)。对于 \(M_1\) 和 \(M_2\)，估计值中的变动来自候选抽样；在 \(M_3\) 下，估计还纳入阶段时间波动，与式（14）的联合结果分布保持一致。所有中位数均采用第 3.4.2 节的区间中点约定，抽样规模与不确定性分析在第 5 节说明。

### 4.1.2 Class selection and wave release / 类别选择与波次释放

For each class, the decision rule retains the larger median across \(\mathcal M_D=\{M_1,M_2\}\) and selects the class with the smallest retained value. Thus, the comparison is between evaluator-specific class medians. With exact scores, the selected class is \(q^\star\) from Equation (15). With estimated scores, the same rule gives

> **中文：** 对每个类别，决策规则取其在 \(\mathcal M_D=\{M_1,M_2\}\) 下中位数中的较大值，再选择该值最小的类别。因此，比较对象是不同评估器下的类别中位数。使用精确得分时，所选类别为式（15）中的 \(q^\star\)；使用估计得分时，同一规则给出：

\[
\widehat q\in\arg\min_{q\in\mathcal Q}
\max_{m\in\mathcal M_D}\widehat\mu_{qm}^{0.5}.
\tag{35}
\]

A fixed class-label order resolves ties in either minimization. The selected class is implemented through Equation (12), with \(\kappa\sim\nu_{q^\star}\) for the exact-score decision and \(\kappa\sim\nu_{\widehat q}\) for the estimated-score decision. The resulting wave \(W^\kappa\) is then released. This step maps the class decision to a concrete wave while preserving the specified within-class sampling rule.

> **中文：** 两种最小化均按照固定的类别标签顺序处理并列。所选类别通过式（12）落实为候选抽样：精确得分决策对应 \(\kappa\sim\nu_{q^\star}\)，估计得分决策对应 \(\kappa\sim\nu_{\widehat q}\)。相应波次 \(W^\kappa\) 随后被释放。这一步将类别决策转化为具体波次，同时保持给定的类内抽样规则。

The resulting output comprises the selected class, its release distribution, and its evaluated makespan profile. The direct candidate benchmark in Equations (16)–(17) provides a comparison with choosing an individual wave, while \(M_3\) assesses performance under phase-time variation. The same class-score data also support the performance diagnosis developed next.

> **中文：** 流程输出包括所选类别、该类别的释放分布及其评价得到的完工期表现。式（16）—（17）的直接候选基准提供与选择单个波次的比较，\(M_3\) 则评价阶段时间波动下的表现。同一组类别得分数据还用于下文的绩效诊断。

## 4.2 Class-relative performance diagnosis / 相对于类别族的绩效诊断

### 4.2.1 Reference scores and diagnostic decomposition / 参照得分与诊断分解

Alongside the robust decision, the evaluation outcomes quantify the performance differences between classes and the quality of a prespecified selection rule. For a fixed resource configuration, wave size, and evaluator \(m\), the class medians in Equation (14) provide the comparison scores. The reference choice draws uniformly from the entire candidate pool. This pool distribution is denoted by \(\nu_0\), while \(b_0\) and \(b_q\) denote the reference and class medians under the fixed evaluator:

> **中文：** 除用于鲁棒决策外，评价结果还用于量化类别之间的绩效差异，以及预先规定的选择规则的决策质量。在资源配置、波次规模和评估器 \(m\) 给定后，式（14）中的类别中位数作为比较得分。参照选择从整个候选池中均匀抽取波次。\(\nu_0\) 表示这一候选池分布，\(b_0\) 与 \(b_q\) 分别表示给定评估器下的参照中位数与类别中位数：

\[
\nu_0(k)=\frac{1}{K},\qquad
b_0=\operatorname{Med}_{\kappa\sim\nu_0,\,\xi}
Y_{\kappa m}(\xi),\qquad
b_q=\mu_{qm}^{0.5},\quad q\in\mathcal Q.
\tag{36}
\]

For \(M_1\) and \(M_2\), the pool reference is computed by complete candidate enumeration or estimated using draws from \(\nu_0\). Under \(M_3\), it is estimated from joint candidate and phase-time draws following Section 4.1. All medians use the midpoint convention in Section 3.4.2. Positive service durations and a nonempty wave give \(b_0>0\), so it can normalize comparisons across configurations. The best and worst selectable classes under this evaluator are denoted by

> **中文：** 对于 \(M_1\) 和 \(M_2\)，候选池参照通过枚举全部候选精确计算，或从 \(\nu_0\) 抽样估计。在 \(M_3\) 下，则按照第 4.1 节的候选与阶段时间联合抽样进行估计。所有中位数均采用第 3.4.2 节规定的区间中点约定。正的服务时长与非空波次保证 \(b_0>0\)，因此可用它对不同配置下的比较进行归一化。该评估器下绩效最好与最差的可选类别分别记为：

\[
q_{\min}\in\arg\min_{q\in\mathcal Q}b_q,
\qquad
q_{\max}\in\arg\max_{q\in\mathcal Q}b_q,
\qquad b_-=b_{q_{\min}},\quad b_+=b_{q_{\max}}.
\tag{37}
\]

The class returned by a prespecified selection rule using the descriptors \(\Phi\) is denoted by \(q_\Phi\in\mathcal Q\). Its fitting procedure, treatment of tied scores, and handling of empty corner supports form part of that rule. The diagnostic takes this rule's selected class as an input and compares it with both the class oracle \(q_{\min}\) and the pool reference. Here \(q_\Phi\) identifies the class selected by the rule being assessed, whereas \(q^\star\) and \(\widehat q\) identify the robust decisions defined above. The normalized class spread \(\mathrm{UB}\), the selected class's normalized gain \(\mathrm{LB}\), and their difference \(\mathrm{GAP}\) are defined as

> **中文：** 某个预先规定的、利用描述指标 \(\Phi\) 的选择规则所返回的类别记为 \(q_\Phi\in\mathcal Q\)。该规则包括拟合方式、得分并列处理方式以及角点支持集为空时的处理方式。诊断以该规则选定的类别为输入，分别与类别最优参照 \(q_{\min}\) 和候选池参照比较。此处的 \(q_\Phi\) 表示被评价规则的输出，\(q^\star\) 与 \(\widehat q\) 则表示上文定义的鲁棒决策。归一化类别跨度 \(\mathrm{UB}\)、所选类别的归一化收益 \(\mathrm{LB}\) 及两者之差 \(\mathrm{GAP}\) 定义为：

\[
\mathrm{UB}=\frac{b_+-b_-}{b_0},\qquad
\mathrm{LB}=\frac{b_0-b_{q_\Phi}}{b_0},\qquad
\mathrm{GAP}=\mathrm{UB}-\mathrm{LB}.
\tag{38}
\]

**Proposition 1 (diagnostic identity).** For any nonempty selectable class family and any selected class \(q_\Phi\), the diagnostic satisfies

> **中文：** **命题 1（诊断恒等式）。** 对任意非空可选类别族和任意所选类别 \(q_\Phi\)，上述诊断满足：

\[
\mathrm{GAP}=H_{\mathrm{up}}+M_\Phi,
\qquad
H_{\mathrm{up}}=\frac{b_+-b_0}{b_0},
\qquad
M_\Phi=\frac{b_{q_\Phi}-b_-}{b_0}.
\tag{39}
\]

**Proof.** Substituting Equation (38) gives \(b_+-b_--b_0+b_{q_\Phi}=(b_+-b_0)+(b_{q_\Phi}-b_-)\) in the numerator. Division by \(b_0\) yields Equation (39). \(\square\)

> **中文：** **证明。** 式（38）给出的分子为 \(b_+-b_--b_0+b_{q_\Phi}=(b_+-b_0)+(b_{q_\Phi}-b_-)\)。该分子与 \(b_0\) 的比值即为式（39）。\(\square\)

The two terms describe different comparisons. The class-family-relative upper-tail headroom \(H_{\mathrm{up}}\) locates the largest class median relative to the pool median. The class-selection miss \(M_\Phi\) measures the normalized excess median makespan of the selected class over the best class in the same family. Resource quantities and operational rules remain fixed in both comparisons. Because \(b_-\le b_{q_\Phi}\le b_+\),

> **中文：** 两个分量对应不同的比较关系。相对于类别族的上尾空间 \(H_{\mathrm{up}}\) 表示最大类别中位数与候选池中位数之间的差距；类别选择偏差 \(M_\Phi\) 衡量所选类别与同一类别族中最优类别之间的归一化完工期中位数差距。两项比较均保持资源数量和运行规则不变。由于 \(b_-\le b_{q_\Phi}\le b_+\)，有：

\[
\mathrm{UB}\ge0,\qquad 0\le M_\Phi\le\mathrm{UB}.
\tag{40}
\]

The signs of the other terms depend on the reference comparison: \(H_{\mathrm{up}}\ge0\) exactly when \(b_+\ge b_0\), and \(\mathrm{LB}\ge0\) exactly when the selected class's median is no greater than the pool median. The corner family in Section 3.3 need not cover the entire candidate pool and may have overlapping supports at tied thresholds. Its class medians therefore need not bracket \(b_0\); \(H_{\mathrm{up}}\) and \(\mathrm{GAP}\) can be negative. These values retain the signed comparisons defined in Equations (38)–(39).

> **中文：** 其余各项的符号取决于对应的参照比较：当且仅当 \(b_+\ge b_0\) 时，\(H_{\mathrm{up}}\ge0\)；当且仅当所选类别不劣于候选池中位数时，\(\mathrm{LB}\ge0\)。第 3.3 节的角点类别族不保证覆盖整个候选池，并且可能因阈值并列而出现支持集重叠。因此，各类别中位数不一定将 \(b_0\) 夹在其中，\(H_{\mathrm{up}}\) 与 \(\mathrm{GAP}\) 均可能为负。这些数值仍表示式（38）—（39）所定义的带符号比较。

### 4.2.2 Class-selection loss / 类别选择损失

The selection term also has a decision-loss interpretation. In predict-then-optimize, the Smart Predict-then-Optimize (SPO) loss evaluates the cost of the decision induced by predicted coefficients, relative to an optimal decision under the true coefficients ([Elmachtoub and Grigas, 2022](https://doi.org/10.1287/mnsc.2020.3922)). Here the actions are class labels. Their cost vector is \(\boldsymbol d=(b_q)_{q\in\mathcal Q}\), and a predicted class-score vector \(\widehat{\boldsymbol d}\) induces the choice \(q_\Phi\in\arg\min_q\widehat d_q\) under a fixed tie convention.

> **中文：** 选择分量还可以解释为决策损失。在先预测后优化框架中，Smart Predict-then-Optimize（SPO）损失衡量预测系数所诱导的决策，相对于真实系数下最优决策的成本差距（[Elmachtoub and Grigas, 2022](https://doi.org/10.1287/mnsc.2020.3922)）。在本研究中，决策动作是类别标签。类别成本向量为 \(\boldsymbol d=(b_q)_{q\in\mathcal Q}\)，预测的类别得分向量 \(\widehat{\boldsymbol d}\) 按固定的并列处理规则诱导选择 \(q_\Phi\in\arg\min_q\widehat d_q\)。

**Proposition 2 (class-action loss interpretation).** For the class decision induced by \(\widehat{\boldsymbol d}\), its SPO loss under \(\boldsymbol d\) satisfies

> **中文：** **命题 2（类别动作的损失解释）。** 对于 \(\widehat{\boldsymbol d}\) 诱导的类别决策，其在 \(\boldsymbol d\) 下的 SPO 损失满足：

\[
L_{\mathrm{SPO}}(\widehat{\boldsymbol d},\boldsymbol d)
=b_{q_\Phi}-\min_{q\in\mathcal Q}b_q
=b_0M_\Phi.
\tag{41}
\]

**Proof.** The selected action incurs cost \(b_{q_\Phi}\), and the oracle action incurs cost \(b_-\). Their difference is the numerator of \(M_\Phi\). \(\square\) Thus, \(M_\Phi\) evaluates the quality of a class decision on a fixed class-cost vector. A learning method can target this loss through the class scores it predicts; its training and generalization properties depend on the learning procedure and data design.

> **中文：** **证明。** 所选动作的成本为 \(b_{q_\Phi}\)，最优参照动作的成本为 \(b_-\)，两者之差即为 \(M_\Phi\) 的分子。\(\square\) 因此，\(M_\Phi\) 在固定的类别成本向量上评价类别决策的质量。学习方法可以通过预测类别得分来针对这一损失进行优化，其训练性质和泛化性质则取决于具体学习过程与数据设计。

### 4.2.3 Resolution of covering partitions / 覆盖分区的分辨率

The resolution analysis uses a finite, disjoint, covering partition \(\mathcal P\) of the same candidate pool to examine how classification detail changes the observed class spread. Each cell has positive probability under \(\nu_0\), and its outcome distribution is obtained by conditioning the same pool distribution and evaluator on that cell. Its midpoint median is denoted by \(b_p\). This construction preserves the mixture relationship between the pool and its cells, giving

> **中文：** 分辨率分析采用同一候选池上的有限、互斥且覆盖全部候选的分区 \(\mathcal P\)，以考察分类细度如何改变所观察到的类别跨度。每个分区单元在 \(\nu_0\) 下具有正概率，其结果分布由同一候选池分布和同一评估器在该单元上的条件分布得到，区间中点中位数记为 \(b_p\)。这一构造保留候选池与各单元之间的混合分布关系，从而有：

\[
\min_{p\in\mathcal P}b_p\le b_0\le\max_{p\in\mathcal P}b_p.
\tag{42}
\]

The bracketing property holds for the midpoint convention. In the proof of the upper inequality, \(t=\max_p b_p\), and \([u_p,v_p]\) denotes the median interval of cell \(p\). Every cell has cumulative probability at least one half at \(t\). If the pool midpoint exceeded \(t\), the pool's cumulative probability at \(t\) would equal one half, forcing the same equality in every positive-weight cell. Their median intervals would then have a common point, and the pool median interval would be their intersection. A cell attaining the largest lower endpoint would have a midpoint at least as large as the pool midpoint, contradicting the definition of \(t\). Reflection of the outcome variable gives the lower inequality.

> **中文：** 这一夹逼关系适用于区间中点约定。上界证明中，\(t=\max_p b_p\)，\([u_p,v_p]\) 表示单元 \(p\) 的中位数区间。每个单元在 \(t\) 处的累计概率均不小于二分之一。如果候选池中位数高于 \(t\)，则候选池在 \(t\) 处的累计概率必须恰为二分之一，进而所有具有正权重的单元在该点的累计概率也均等于二分之一。此时，各单元中位数区间具有公共点，候选池的中位数区间就是这些区间的交集。下端点最大的单元的中位数必不小于候选池中位数，与 \(t\) 的定义矛盾。结果变量的反射变换给出下界。

**Theorem 1 (nested-partition refinement).** The following result concerns finite covering partitions \(\mathcal P\) and \(\mathcal P'\) of the same candidate pool, with positive-probability cells and cell distributions induced by the same base distribution and evaluator. If \(\mathcal P'\) refines \(\mathcal P\), meaning that every cell of \(\mathcal P'\) lies within one cell of \(\mathcal P\), then

> **中文：** **定理 1（嵌套分区细化）。** 本结果针对同一候选池上的有限覆盖分区 \(\mathcal P\) 与 \(\mathcal P'\)，其中各单元具有正概率，且所有单元分布均由同一基础分布和同一评估器诱导。如果 \(\mathcal P'\) 是 \(\mathcal P\) 的细化，即 \(\mathcal P'\) 的每个单元均包含于 \(\mathcal P\) 的某个单元中，则：

\[
\max_{p'\in\mathcal P'}b_{p'}\ge\max_{p\in\mathcal P}b_p,
\qquad
\min_{p'\in\mathcal P'}b_{p'}\le\min_{p\in\mathcal P}b_p.
\tag{43}
\]

**Proof.** The outcome distribution in a parent cell is the mixture of the distributions in its children, with weights \(\nu_0(p')/\nu_0(p)\). Equation (42), applied within that parent, brackets its median by its smallest and largest child medians. The upper inequality for a parent attaining the largest coarse median and the lower inequality for a parent attaining the smallest coarse median establish the result. \(\square\)

> **中文：** **证明。** 每个父单元的结果分布都是其子单元分布的混合，权重为 \(\nu_0(p')/\nu_0(p)\)。式（42）保证该父单元的中位数位于最小与最大子单元中位数之间。上述上界在粗分区中中位数最大的父单元上成立，下界在中位数最小的父单元上成立，由此得到结论。\(\square\)

**Corollary 1 (diagnostic resolution).** Along a nested sequence of such partitions, \(H_{\mathrm{up}}(\mathcal P)\), the oracle gain \(S_{\mathrm{or}}(\mathcal P)=[b_0-\min_p b_p]/b_0\), and \(\mathrm{UB}(\mathcal P)=H_{\mathrm{up}}(\mathcal P)+S_{\mathrm{or}}(\mathcal P)\) are nonnegative and nondecreasing under refinement. This follows from Equations (42)–(43), with \(b_0\) fixed. The selection term \(M_\Phi\) additionally depends on the rule's choice at each resolution.

> **中文：** **推论 1（诊断分辨率）。** 沿上述分区构成的嵌套序列，\(H_{\mathrm{up}}(\mathcal P)\)、最优类别收益 \(S_{\mathrm{or}}(\mathcal P)=[b_0-\min_p b_p]/b_0\) 以及 \(\mathrm{UB}(\mathcal P)=H_{\mathrm{up}}(\mathcal P)+S_{\mathrm{or}}(\mathcal P)\) 均非负，且随细化不减。该结论直接来自式（42）—（43）和固定的 \(b_0\)。选择分量 \(M_\Phi\) 还取决于规则在各个分辨率下选择的类别。

The corner family \(\mathcal Q\) and the covering partition \(\mathcal P\) answer different diagnostic questions. The former compares selected tail combinations of \(C\) and \(I\); the latter tracks how a complete classification resolves variation across the whole pool. Resolution comparisons use genuinely nested boundaries and consistent allocation of threshold ties. At the sample level, exact checks of Theorem 1 partition the same weighted outcome sample so that each parent distribution remains the mixture of its children.

> **中文：** 角点类别族 \(\mathcal Q\) 与覆盖分区 \(\mathcal P\) 回答不同的诊断问题：前者比较 \(C\) 与 \(I\) 的特定尾部组合，后者考察完整分类如何逐步区分整个候选池中的差异。分辨率比较采用真正嵌套的边界，并对阈值并列使用一致的归属规则。在样本层面，对定理 1 的精确核查需要划分同一组带权结果样本，使父单元分布始终保持为其子单元分布的混合。

## 4.3 Conditional ordering of the deterministic evaluators / 确定性评估器的条件性排序

### 4.3.1 Coupled request comparison / 对应请求的耦合比较

The relative magnitudes of the two evaluator scores determine which model sets a class's robust score. To analyze this relationship, we compare their resource reservations. The deterministic evaluators represent elevator capacity through different resource states: \(M_1\) uses \(Ec\) independent single-request slots, whereas \(M_2\) uses \(E\) physical cars with shared trips. Their completion times depend jointly on request timing, resource availability, and stored destination floors. We compare the evaluators on the same candidate wave using the serial reservation rules of Section 3.5. A corresponding elevator request is denoted by \(\varrho\), and its unloading completion time under \(M_i\) by \(D_i(\varrho)\), for \(i\in\{1,2\}\).

> **中文：** 两个评估器得分的相对大小决定哪个模型给出某类别的鲁棒得分。为分析这一关系，本节比较两者的资源预约过程。两个确定性评估器通过不同的资源状态表示电梯容量：\(M_1\) 使用 \(Ec\) 个独立的单请求槽位，\(M_2\) 使用 \(E\) 个允许共享行程的实体轿厢。完工时刻共同取决于请求时刻、资源可用时刻以及保存的目标楼层。本节在同一候选波次上，按照第 3.5 节的串行预约规则比较两个评估器。\(\varrho\) 表示一个对应的电梯请求，\(D_i(\varrho)\) 表示其在 \(M_i\) 下的卸载结束时刻，其中 \(i\in\{1,2\}\)。

**Proposition 3 (conditional sample-path ordering).** The result applies to a candidate wave \(W^k\) evaluated from the common initial state in Section 3.1, for any \(E\ge1\) and \(c\ge1\). Its conclusion holds when the two deterministic evaluations satisfy conditions (a)–(d).

> **中文：** **命题 3（条件性样本路径排序）。** 本结果适用于从第 3.1 节规定的共同初始状态出发、对候选波次 \(W^k\) 进行评价的情形，其中 \(E\ge1\) 和 \(c\ge1\) 可任意取值。其结论以两个确定性评价过程满足条件（a）—（d）为前提。

(a) Both evaluators process orders in the same sequence \(\pi(W^k)\).

> **中文：** （a）两个评估器均按照同一序列 \(\pi(W^k)\) 处理订单。

(b) Each order is assigned to the same AMR in both evaluations.

> **中文：** （b）每个订单在两个评价过程中均分配给同一台 AMR。

(c) No shared \(M_2\) trip overtakes its corresponding \(M_1\) requests. For every \(M_2\) trip \(\tau\) containing at least two requests, \(\mathcal G_\tau\) denotes its request group and \(T_\tau\) its shared unloading completion time. The required relation is

> **中文：** （c）\(M_2\) 的共享行程不超越其对应的 \(M_1\) 请求。对于每个包含至少两个请求的 \(M_2\) 行程 \(\tau\)，\(\mathcal G_\tau\) 表示其请求组，\(T_\tau\) 表示共同的卸载结束时刻，相应条件为：

\[
\max_{\varrho\in\mathcal G_\tau}D_1(\varrho)\le T_\tau.
\tag{44}
\]

(d) Repositioning does not disadvantage \(M_1\) on requests for which both evaluators create a new trip. For each such request with origin floor \(g_\varrho\), \(G^{(i)}_{\mathrm{sel}}(\varrho)\) denotes the selected resource's stored floor immediately before its state update in \(M_i\). The required relation is

> **中文：** （d）对于两个评估器均新建行程的请求，调位距离不会使 \(M_1\) 处于不利地位。对于起点楼层为 \(g_\varrho\) 的此类请求，\(G^{(i)}_{\mathrm{sel}}(\varrho)\) 表示 \(M_i\) 中所选资源在状态更新前保存的楼层，相应条件为：

\[
\left|G^{(1)}_{\mathrm{sel}}(\varrho)-g_\varrho\right|
\le
\left|G^{(2)}_{\mathrm{sel}}(\varrho)-g_\varrho\right|.
\tag{45}
\]

Under these conditions, every corresponding elevator request and the wave makespan satisfy

> **中文：** 在这些条件下，每个对应电梯请求与波次完工期均满足：

\[
D_1(\varrho)\le D_2(\varrho),
\qquad
C_{\max}(W^k;M_1)\le C_{\max}(W^k;M_2).
\tag{46}
\]

Conditions (a) and (b) align the sequence, origins, and destinations of elevator requests, including the AMR's movement to an order's pickup floor. The canonical ordering in Equation (1) supplies (a). Condition (b) is an additional property of the paired evaluations because earlier elevator completions affect subsequent earliest-available-AMR choices. In (d), the stored floor is the resource's location at its recorded next-available time, as defined in Section 3.5. Conditions (c) and (d) are assessed on the paired reservation paths.

> **中文：** 条件（a）与（b）使电梯请求的顺序、起点和终点一一对应，其中也包括 AMR 前往订单取货楼层的移动。式（1）的规范排序保证条件（a）；条件（b）则是两个对应评价过程需要额外满足的性质，因为先前的电梯完工时刻会影响后续“最早可用 AMR”的选择。在条件（d）中，保存的楼层指第 3.5 节所定义的资源在其记录的下一可用时刻所处的楼层。条件（c）与（d）在两个对应的预约路径上进行判断。

**Proof sketch.** The proof proceeds by induction over the reservation sequence. The induction maintains the completion-time ordering for previous requests and the ordering of the earliest \(E\) resource availabilities: if \(x_{(1)}\le\cdots\le x_{(Ec)}\) and \(y_{(1)}\le\cdots\le y_{(E)}\) are the sorted \(M_1\) and \(M_2\) availability states, then \(x_{(i)}\le y_{(i)}\) for \(i=1,\ldots,E\). Common AMR assignments and the monotone service-time recursions give an earlier or equal request time under \(M_1\). When both evaluators create a new trip, this comparison, earliest availability, and (d) order the new completion times. Replacing the smallest availability in each list preserves the required ordering.

> **中文：** **证明思路。** 证明按照预约序列进行归纳。归纳同时维持先前请求的完工时刻排序，以及最早的 \(E\) 个资源可用时刻的排序：若 \(x_{(1)}\le\cdots\le x_{(Ec)}\) 与 \(y_{(1)}\le\cdots\le y_{(E)}\) 分别是排序后的 \(M_1\) 与 \(M_2\) 可用时刻状态，则对 \(i=1,\ldots,E\) 有 \(x_{(i)}\le y_{(i)}\)。相同的 AMR 分配与单调的服务时间递推保证 \(M_1\) 的对应请求时刻不晚于 \(M_2\)。当两个评估器均新建行程时，结合请求时刻比较、最早可用时刻和条件（d），可得到新完工时刻的排序；替换两个列表中的最小可用时刻后，所需排序保持成立。

For a request joining an existing \(M_2\) trip, condition (c) gives its completion-time comparison directly. The availability comparison follows from a counting argument. Any \(M_2\) trip already replaced by a later reservation completed no later than the current fleet minimum; hence completions above a threshold \(y_{(i)}\) can belong only to the latest trips of at most \(E-i\) cars. Those trips contain at most \((E-i)c\) requests. If the joining trip ends above that threshold, its spare place reduces the count of previous requests by one. Previous completion-time ordering transfers this count to the \(M_1\) slots, preserving \(x_{(i)}\le y_{(i)}\) after the new slot reservation. The AMR recursions then order every order completion, including orders that inherit earlier resource delays without making a new elevator request. Taking the maximum and subtracting the common \(t_W\) proves Equation (46). \(\square\)

> **中文：** 当请求加入已有的 \(M_2\) 行程时，条件（c）直接给出该请求的完工时刻比较。资源可用时刻的比较由计数论证得到。任何已被后续预约替代的 \(M_2\) 行程，其完工时刻均不晚于当前车队的最小可用时刻；因此，高于阈值 \(y_{(i)}\) 的完工请求只能属于至多 \(E-i\) 台轿厢的最新行程，这些行程至多包含 \((E-i)c\) 个请求。如果本次加入的行程在该阈值之后结束，其剩余位置会使先前请求数的上界再减少一。先前请求的完工时刻排序将这一计数界传递给 \(M_1\) 槽位，使新增槽位预约后仍满足 \(x_{(i)}\le y_{(i)}\)。AMR 递推进一步保持全部订单完工时刻的排序，其中也包括没有新增电梯请求、但继承先前资源延迟的订单。所有订单完工时刻的最大值在减去共同的 \(t_W\) 后，给出式（46）中的波次排序。\(\square\)

### 4.3.2 Reversal mechanisms and class-level implications / 排序反转机制及类别层面的推论

Two small instances isolate the roles of shared trips and repositioning. Both use \(t_W=0\), \(f^0=1\), \(E=1\), \(c=2\), \(\gamma=5\), \(\tau^L=\tau^U=2\), and \(\tau^P=\tau^D=5\), with times measured in seconds. Order identifiers follow the order in which the orders are described below.

> **中文：** 两个小规模实例分别说明共享行程与调位的作用。两者均采用 \(t_W=0\)、\(f^0=1\)、\(E=1\)、\(c=2\)、\(\gamma=5\)、\(\tau^L=\tau^U=2\) 和 \(\tau^P=\tau^D=5\)，时间单位为秒。订单标识符按照下文描述的订单先后排列。

In the first instance, \(F=3\) and \(A=2\). Two orders travel from floor 1 to floor 3, with ready-time offsets 0 and 2. Their delivery requests reach the elevator at times 5 and 7. Under \(M_1\), separate slots complete the trips at 19 and 21, and the wave finishes at 26. Under \(M_2\), the second request joins the first trip at its loading-end time 7. Both requests finish the elevator trip at 19, giving a wave makespan of 24. Thus, a shared trip can overtake a corresponding independent-slot request, violating (c).

> **中文：** 第一个实例中，\(F=3\)、\(A=2\)。两个订单均从第 1 层运往第 3 层，就绪时间偏移量分别为 0 和 2，其交付运输请求分别在时刻 5 和 7 到达电梯。在 \(M_1\) 下，两个独立槽位分别于 19 和 21 完成行程，波次于 26 完成。在 \(M_2\) 下，第二个请求恰好在装载结束时刻 7 加入第一个行程，两个请求均在 19 完成电梯运输，波次完工期为 24。因此，共享行程可以超越对应的独立槽位请求，使条件（c）失效。

In the second instance, \(F=8\) and \(A=1\). The first order travels from floor 1 to floor 8, and the second from floor 8 to floor 7; both have ready-time offset 0. The first order finishes at 49, and the second order's elevator request is issued at 54. Under \(M_1\), the earliest-available slot is the unused slot at floor 1. Its empty movement to floor 8 takes 35 seconds, producing a wave makespan of 103. Under \(M_2\), the car is already at floor 8, and the wave finishes at 68. No trip is shared; the reversal arises from the unfavorable repositioning distance in (d).

> **中文：** 第二个实例中，\(F=8\)、\(A=1\)。第一个订单从第 1 层运往第 8 层，第二个订单从第 8 层运往第 7 层，两者的就绪时间偏移量均为 0。第一个订单在 49 完成，第二个订单的电梯请求在 54 发出。在 \(M_1\) 下，最早可用的是仍位于第 1 层的未使用槽位，其空载前往第 8 层需要 35 秒，最终波次完工期为 103。在 \(M_2\) 下，轿厢已位于第 8 层，波次在 68 完成。此例没有共享行程，排序反转来自条件（d）中的不利调位距离。

The examples show why (c) and (d) enter the sufficient conditions in Proposition 3. With aligned order sequences and AMR assignments, a reversal must violate at least one of these two conditions, although their violation need not produce a reversal. When AMR assignments differ, request alignment itself must also be examined. This separates an audit of the theorem's conditions from the observed frequency of makespan ordering.

> **中文：** 这两个实例说明了命题 3 的充分条件为何需要包含（c）与（d）。在订单序列和 AMR 分配已对齐的前提下，排序反转必然伴随这两个条件中至少一个失效，但条件失效未必造成排序反转。如果 AMR 分配不同，还需要检查请求对应关系本身。因此，对定理条件的核查与对完工期排序出现频率的统计是两个不同的检查对象。

For a class \(q\), the same draw \(\kappa\sim\nu_q\) is evaluated under both deterministic evaluators. If conditions (a)–(d) of Proposition 3 hold for every candidate in \(\mathcal K_q\), then \(Y_{\kappa M_1}\le Y_{\kappa M_2}\) almost surely. The class-conditional cumulative distribution function is \(F_{qi}(t)=\Pr(Y_{\kappa M_i}\le t\mid q)\). The almost-sure comparison implies first-order stochastic ordering and, consequently, midpoint-median ordering:

> **中文：** 对于类别 \(q\)，两个确定性评估器对同一次抽样 \(\kappa\sim\nu_q\) 进行评价。如果 \(\mathcal K_q\) 中每个候选均满足命题 3 的条件（a）—（d），则 \(Y_{\kappa M_1}\le Y_{\kappa M_2}\) 几乎必然成立。类别条件累积分布函数为 \(F_{qi}(t)=\Pr(Y_{\kappa M_i}\le t\mid q)\)。上述几乎必然成立的比较进一步给出一阶随机排序及区间中点中位数的排序：

\[
F_{q1}(t)\ge F_{q2}(t)\quad\text{for all }t,
\qquad
\mu_{qM_1}^{0.5}\le\mu_{qM_2}^{0.5}.
\tag{47}
\]

## 4.4 Properties of robust class selection / 鲁棒类别选择的性质

### 4.4.1 Reduction under class-median ordering / 类别中位数有序时的简化

The procedure in Section 4.1 compares both deterministic class medians. The ordering analysis in Section 4.3 motivates examining when one evaluator alone determines the robust score. The relevant medians, robust score, and conservative choice are denoted by

> **中文：** 第 4.1 节的流程同时比较两个确定性类别中位数。第 4.3 节的排序分析用于考察仅由一个评估器确定鲁棒得分的条件。相应的中位数、鲁棒得分与保守选择的记号为：

\[
a_q=\mu_{qM_1}^{0.5},\qquad
b_q=\mu_{qM_2}^{0.5},\qquad
V_q=\max\{a_q,b_q\},\qquad
q_H\in\arg\min_{q\in\mathcal Q}b_q.
\tag{48}
\]

Here \(b_q\) specializes the fixed-evaluator notation of Section 4.2 to \(M_2\). We refer to \(q_H\) as the \(M_2\)-based conservative choice. Its relationship with the robust optimum depends on the class-score ordering.

> **中文：** 此处的 \(b_q\) 将第 4.2 节中固定评估器下的记号具体取为 \(M_2\) 的类别得分。\(q_H\) 称为基于 \(M_2\) 的保守选择，其与鲁棒最优解的关系取决于类别得分的排序。

**Theorem 2 (conditional minimax reduction).** If \(a_q\le b_q\) for every \(q\in\mathcal Q\), then the robust class objective equals the \(M_2\) median class by class, and

> **中文：** **定理 2（条件性极小极大简化）。** 如果对每个 \(q\in\mathcal Q\) 均有 \(a_q\le b_q\)，则鲁棒类别目标逐类等于 \(M_2\) 的中位数，并且：

\[
\arg\min_{q\in\mathcal Q}\max\{a_q,b_q\}
=\arg\min_{q\in\mathcal Q}b_q.
\tag{49}
\]

**Proof.** The assumed ordering gives \(V_q=b_q\) for every selectable class. Minimizing these identical class scores yields the same optimal set. \(\square\) Equation (47) supplies one sufficient route to the premise. The premise can also be checked directly on the class medians, without requiring request-level ordering for every candidate. With a common tie convention, both minimizations return the same class label.

> **中文：** **证明。** 给定排序保证每个可选类别均满足 \(V_q=b_q\)。逐类相同的得分对应相同的最优解集合。\(\square\) 式（47）提供了使该前提成立的一条充分路径。类别中位数的直接比较也可检验该前提，无需每个候选均满足请求层面的排序。相同的并列处理规则保证两种最小化返回同一类别标签。

The same algebraic reduction applies to the estimated objective in Section 4.1 whenever the estimated class medians are ordered. Statements about the underlying class distributions use their population scores or an explicit uncertainty analysis. Request-level condition checks, makespan-ordering frequencies, and class-median comparisons are recorded separately, preserving the distinction between the premise of Proposition 3 and the premise of Theorem 2.

> **中文：** 当估计的类别中位数满足排序时，相同的代数简化适用于第 4.1 节的估计目标。关于底层类别分布的结论则依据其总体得分或明确的不确定性分析。请求层面的条件核查、完工期排序频率以及类别中位数比较分别记录，从而区分命题 3 与定理 2 各自的前提。

### 4.4.2 Departures from ordering and selection stability / 偏离排序时的选择稳定性

When some class medians reverse order, their effect on the robust objective can be represented exactly by the positive excess of the \(M_1\) median:

> **中文：** 当部分类别的中位数排序发生反转时，可通过 \(M_1\) 中位数的正向超额，精确表示这种反转对鲁棒目标的影响：

\[
e_q=[a_q-b_q]_+,\qquad [u]_+=\max\{u,0\},
\qquad V_q=b_q+e_q.
\tag{50}
\]

**Corollary 2 (excess loss and ranking stability).** For any \(M_2\)-optimal class \(q_H\), its excess robust objective satisfies

> **中文：** **推论 2（超额损失与排序稳定性）。** 对任意 \(M_2\) 最优类别 \(q_H\)，其鲁棒目标的超额损失满足：

\[
0\le V_{q_H}-\min_{q\in\mathcal Q}V_q\le e_{q_H}.
\tag{51}
\]

If \(q_H\) is the unique \(M_2\)-optimal class, its ranking margin is \(\Delta_H=\min_{q\ne q_H}(b_q-b_{q_H})\), with \(\Delta_H=+\infty\) when only one class is selectable. This margin gives the sufficient condition

> **中文：** 如果 \(q_H\) 是唯一的 \(M_2\) 最优类别，其排序间隔为 \(\Delta_H=\min_{q\ne q_H}(b_q-b_{q_H})\)；只有一个可选类别时，该间隔取值 \(\Delta_H=+\infty\)。该间隔给出以下充分条件：

\[
\Delta_H>e_{q_H}
\quad\Longrightarrow\quad
\arg\min_{q\in\mathcal Q}V_q=\{q_H\}.
\tag{52}
\]

**Proof.** Since \(V_q\ge b_q\ge b_{q_H}\), the optimal robust value is at least \(b_{q_H}\). Subtracting this lower bound from \(V_{q_H}=b_{q_H}+e_{q_H}\) gives Equation (51). Under the strict margin condition, every other class satisfies \(V_q\ge b_q>b_{q_H}+e_{q_H}=V_{q_H}\), proving Equation (52). \(\square\)

> **中文：** **证明。** 由于 \(V_q\ge b_q\ge b_{q_H}\)，最优鲁棒目标值至少为 \(b_{q_H}\)。\(V_{q_H}=b_{q_H}+e_{q_H}\) 与该下界的差给出式（51）。在严格间隔条件下，其他每个类别均满足 \(V_q\ge b_q>b_{q_H}+e_{q_H}=V_{q_H}\)，因此式（52）成立。\(\square\)

Matched candidate evaluations provide a distributional bound on \(e_q\). When the outcome distribution has atoms, the midpoint convention is retained through the lower and upper quantile endpoints of the \(M_2\) class distribution, defined for \(0<p<1\) as

> **中文：** 同一候选的配对评价可进一步从分布层面界定 \(e_q\)。当结果分布包含离散概率质量时，区间中点约定通过 \(M_2\) 类别分布的下、上分位数端点得以保留；这些端点在 \(0<p<1\) 上定义为：

\[
Q_q^-(p)=\inf\{t:F_{q2}(t)\ge p\},\qquad
Q_q^+(p)=\inf\{t:F_{q2}(t)>p\},\qquad
Q_q^{\mathrm{mid}}(p)=\frac{Q_q^-(p)+Q_q^+(p)}{2}.
\tag{53}
\]

If the probability of a makespan-ordering violation under the common draw \(\kappa\sim\nu_q\) is at most \(\epsilon_q<1/2\), the event inclusion \(\{Y_{\kappa M_2}\le t\}\subseteq\{Y_{\kappa M_1}\le t\}\cup\{Y_{\kappa M_1}>Y_{\kappa M_2}\}\) gives

> **中文：** 在共同抽样 \(\kappa\sim\nu_q\) 下，如果完工期排序违反的概率不超过 \(\epsilon_q<1/2\)，则事件包含关系 \(\{Y_{\kappa M_2}\le t\}\subseteq\{Y_{\kappa M_1}\le t\}\cup\{Y_{\kappa M_1}>Y_{\kappa M_2}\}\) 给出：

\[
\Pr(Y_{\kappa M_1}>Y_{\kappa M_2}\mid q)\le\epsilon_q
\quad\Longrightarrow\quad
F_{q2}(t)\le F_{q1}(t)+\epsilon_q
\quad\text{for all }t.
\tag{54}
\]

Applying this inequality to both median endpoints and taking their midpoint yields \(a_q\le Q_q^{\mathrm{mid}}(1/2+\epsilon_q)\). Hence the positive excess in Equation (50) is bounded by

> **中文：** 该不等式分别界定中位数区间的两个端点，两端点的中点满足 \(a_q\le Q_q^{\mathrm{mid}}(1/2+\epsilon_q)\)。因此，式（50）中的正向超额满足：

\[
0\le e_q\le U_q^{\mathrm{mid}}(\epsilon_q),\qquad
U_q^{\mathrm{mid}}(\epsilon_q)
=Q_q^{\mathrm{mid}}(1/2+\epsilon_q)-b_q.
\tag{55}
\]

The condition \(\Delta_H>U_{q_H}^{\mathrm{mid}}(\epsilon_{q_H})\) therefore certifies that the \(M_2\)-optimal class remains the unique robust choice. The width of this bound depends on the distribution near its median as well as on the violation probability. A small violation probability alone can coexist with a large quantile gap. When the inequality does not hold, the robust decision is obtained by comparing the full scores \(V_q\).

> **中文：** 因此，条件 \(\Delta_H>U_{q_H}^{\mathrm{mid}}(\epsilon_{q_H})\) 可以保证 \(M_2\) 最优类别仍是唯一的鲁棒选择。该界的宽度同时取决于违反概率和中位数附近的分布形态；较小的违反概率仍可能对应较大的分位数间隙。当该不等式不成立时，鲁棒决策由完整得分 \(V_q\) 的比较确定。

These bounds assess excess performance loss relative to the two-model median-minimax optimum. Evaluator-specific regret, such as \(R_1(q_H)=a_{q_H}-\min_q a_q\), makes a different comparison and is evaluated separately. The stochastic evaluator \(M_3\) likewise retains its own class distribution from Equation (14).

> **中文：** 上述界衡量相对于两个模型中位数极小极大最优值的额外绩效损失。针对单个评估器的遗憾值，例如 \(R_1(q_H)=a_{q_H}-\min_q a_q\)，对应另一种比较，其评价与上述界分别进行。随机评估器 \(M_3\) 同样保留式（14）所定义的自身类别结果分布。

### 4.4.3 Mean-based distributional interpretation and model extension / 基于均值的分布解释与模型扩展

A complementary mean-based comparison connects the candidate-model family to a Wasserstein ambiguity set. Wasserstein distributionally robust optimization evaluates a decision against distributions within a prescribed distance of a reference law ([Mohajerin Esfahani and Kuhn, 2018](https://doi.org/10.1007/s10107-017-1172-1)). Here \(P_{qi}\) denotes the distribution of \(Y_{\kappa M_i}\) for \(\kappa\sim\nu_q\), and \(\bar\mu_{qi}\) denotes its mean. These finite-pool deterministic distributions have finite first moments.

> **中文：** 一项补充的均值比较可将候选模型族与 Wasserstein 模糊集联系起来。Wasserstein 分布鲁棒优化在距离参照分布不超过给定范围的分布集合上评价决策（[Mohajerin Esfahani and Kuhn, 2018](https://doi.org/10.1007/s10107-017-1172-1)）。在本研究中，\(P_{qi}\) 表示 \(\kappa\sim\nu_q\) 时 \(Y_{\kappa M_i}\) 的分布，\(\bar\mu_{qi}\) 表示其均值。这些由有限候选池与确定性评价产生的分布均具有有限一阶矩。

For distributions \(P\) and \(P'\), \(\Gamma(P,P')\) denotes their couplings, and the one-dimensional 1-Wasserstein distance is \(W_1(P,P')=\inf_{\lambda\in\Gamma(P,P')}\int|u-v|\,\mathrm d\lambda(u,v)\). The class-specific radius and ambiguity set are defined by

> **中文：** 分布 \(P\) 与 \(P'\) 的耦合集合记为 \(\Gamma(P,P')\)，一维 1-Wasserstein 距离定义为 \(W_1(P,P')=\inf_{\lambda\in\Gamma(P,P')}\int|u-v|\,\mathrm d\lambda(u,v)\)。各类别的校准半径与模糊集分别为：

\[
\rho_q=W_1(P_{q1},P_{q2}),\qquad
\mathfrak B_q=
\left\{P\in\mathscr P_1(\mathbb R_+):
W_1(P,P_{q1})\le\rho_q\right\},
\tag{56}
\]

where \(\mathscr P_1(\mathbb R_+)\) is the set of probability distributions on nonnegative makespans with finite first moments. The radius is calibrated separately for each class from its two candidate-model distributions, with \(P_{q1}\) as the center and \(P_{q2}\) on the boundary.

> **中文：** 其中，\(\mathscr P_1(\mathbb R_+)\) 表示定义在非负完工期上且具有有限一阶矩的概率分布集合。每个类别的半径均由其两个候选模型分布分别校准，以 \(P_{q1}\) 为中心，\(P_{q2}\) 位于球的边界。

**Corollary 3 (model-calibrated mean comparison).** If \(F_{q1}(t)\ge F_{q2}(t)\) for all \(t\) and every selectable class, then

> **中文：** **推论 3（模型校准的均值比较）。** 如果对所有 \(t\) 及每个可选类别均有 \(F_{q1}(t)\ge F_{q2}(t)\)，则：

\[
\sup_{P\in\mathfrak B_q}\mathbb E_P[Y]
=\bar\mu_{q1}+\rho_q
=\bar\mu_{q2}
=\max_{i\in\{1,2\}}\bar\mu_{qi},
\quad q\in\mathcal Q.
\tag{57}
\]

**Proof.** Under the stated stochastic ordering, the one-dimensional transport distance equals the mean difference: \(\rho_q=\int(F_{q1}-F_{q2})\,\mathrm dt=\bar\mu_{q2}-\bar\mu_{q1}\). For every admissible \(P\), coupling the two costs gives \(\mathbb E_P[Y]\le\bar\mu_{q1}+W_1(P,P_{q1})\le\bar\mu_{q1}+\rho_q\). The admissible distribution \(P_{q2}\) attains this upper bound. \(\square\)

> **中文：** **证明。** 在给定随机排序下，一维运输距离等于均值差：\(\rho_q=\int(F_{q1}-F_{q2})\,\mathrm dt=\bar\mu_{q2}-\bar\mu_{q1}\)。对于任意可行分布 \(P\)，通过耦合两个成本可得 \(\mathbb E_P[Y]\le\bar\mu_{q1}+W_1(P,P_{q1})\le\bar\mu_{q1}+\rho_q\)。可行分布 \(P_{q2}\) 恰好达到该上界。\(\square\)

Consequently, minimizing the worst mean over \(\mathfrak B_q\) selects the same optimal class set as minimizing the \(M_2\) mean. This relation concerns the mean-based counterpart of the selection problem; Equation (15) continues to use medians. The calibration uses the specified pair of evaluator distributions, while statistical calibration from observed warehouse data would define a different ambiguity-set construction.

> **中文：** 因此，在各类别的 \(\mathfrak B_q\) 上最小化最坏均值，与最小化 \(M_2\) 均值得到相同的最优类别集合。该关系针对选择问题的均值版本，式（15）仍采用中位数。这里的校准使用给定的两个评估器分布，而基于实际仓库观测数据进行统计校准，则属于另一种模糊集构造。

**Corollary 4 (extension to a finite evaluator family).** This result concerns a nonempty finite evaluator family \(\mathcal M^+\) whose class medians are defined under the same release distributions. If one member \(m^\dagger\in\mathcal M^+\) satisfies \(\mu_{qm}^{0.5}\le\mu_{qm^\dagger}^{0.5}\) for every \(q\) and every \(m\in\mathcal M^+\), then

> **中文：** **推论 4（向有限评估器族扩展）。** 本结果针对非空有限评估器族 \(\mathcal M^+\)，各评估器的类别中位数均基于相同释放分布定义。如果其中存在成员 \(m^\dagger\in\mathcal M^+\)，对每个 \(q\) 及每个 \(m\in\mathcal M^+\) 均满足 \(\mu_{qm}^{0.5}\le\mu_{qm^\dagger}^{0.5}\)，则：

\[
\arg\min_{q\in\mathcal Q}\max_{m\in\mathcal M^+}\mu_{qm}^{0.5}
=\arg\min_{q\in\mathcal Q}\mu_{qm^\dagger}^{0.5}.
\tag{58}
\]

The proof is the classwise substitution used in Theorem 2. If the largest-median evaluator varies by class, the appropriate score is instead the class-specific envelope \(\max_{m\in\mathcal M^+}\mu_{qm}^{0.5}\). Including \(M_3\) in this extension requires its own median comparisons.

> **中文：** 逐类代入给出与定理 2 相同的证明。如果中位数最大的评估器随类别变化，相应得分为逐类上包络 \(\max_{m\in\mathcal M^+}\mu_{qm}^{0.5}\)。将 \(M_3\) 纳入该扩展时，需要对其中位数另行比较。
