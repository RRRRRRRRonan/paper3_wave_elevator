---
title: "Section 3. Problem Formulation / 问题建模"
date: 2026-09-04
status: "canonical manuscript draft"
scope: "fixed-size single-wave candidate and class selection"
implementation_alignment: "target specification for the Phase 1 simulator repair"
---

# 3. Problem Formulation / 问题建模

This study formulates wave composition as a finite selection problem coupled with a fixed operational evaluator. A decision instance contains an order pool, a fixed wave size, a warehouse configuration, and a specified family of elevator models. The tactical decision selects either a concrete candidate wave or a structural wave class. A canonical serial resource-reservation rule then maps the selected orders to AMR and elevator completion times. The resulting formulation separates the composition decision from the operational mechanism used to evaluate it.

> **中文：** 本研究将波次构成建模为一个与固定运行评估器相结合的有限选择问题。一个决策实例包含订单池、固定波次规模、仓库配置以及指定的电梯模型族。战术决策选择一个具体候选波次或一个波次结构类别。随后，规范的串行资源预约规则将所选订单映射为 AMR 和电梯的完成时间。由此，模型将波次构成决策与用于评价该决策的运行机制区分开来。

## 3.1 Indices and sets / 索引与集合

The basic indices and their domains are listed below. Candidate-wave construction and structural-class membership are defined in Sections 3.2.2 and 3.2.3, respectively.

> **中文：** 基础索引及其取值范围如下。候选波次的构成和结构类别的归属分别在第 3.2.2 节和第 3.2.3 节中定义。

| Symbol / 符号 | Definition / 定义 |
|---|---|
| \(f\in\mathcal F=\{1,\ldots,F\}\) | warehouse-floor index / 仓库楼层索引 |
| \(o\in\mathcal O\) | order index in the available order pool / 可用订单池中的订单索引 |
| \(a\in\mathcal A=\{1,\ldots,A\}\) | AMR index / AMR 索引 |
| \(e\in\mathcal E=\{1,\ldots,E\}\) | physical-elevator index under \(M_2\) and \(M_3\) / \(M_2\) 和 \(M_3\) 下的实体电梯索引 |
| \(v\in\mathcal V_1=\{1,\ldots,Ec\}\) | virtual single-request elevator-slot index under \(M_1\) / \(M_1\) 下的虚拟单请求电梯服务槽索引 |
| \(k\in\mathcal K=\{1,\ldots,K\}\) | candidate-wave index, common to all evaluators / 所有评估器共用的候选波次索引 |
| \(j\in\mathcal J_n=\{1,\ldots,n\}\) | position index in the canonical processing sequence / 规范处理序列中的位置索引 |
| \(q\in\mathcal Q\) | selectable structural-class label / 可选结构类别标签 |
| \(m\in\mathcal M=\{M_1,M_2,M_3\}\) | elevator-evaluator index / 电梯评估器索引 |

## 3.2 Parameters / 参数

### 3.2.1 Warehouse, order, and service parameters / 仓库、订单与服务参数

| Symbol / 符号 | Definition / 定义 |
|---|---|
| \(F\) | number of warehouse floors / 仓库楼层数 |
| \(A\) | number of AMRs / AMR 数量 |
| \(E\) | number of physical elevator cars / 实体电梯轿厢数量 |
| \(c\) | maximum AMR occupancy of one physical elevator trip / 单次实体电梯行程可搭载的最大 AMR 数量 |
| \(n\) | fixed number of orders in a wave / 一个波次中的固定订单数量 |
| \(t_W\) | common decision and release epoch of the selected wave / 所选波次的统一决策与释放时刻 |
| \(f^0\) | common initial floor of the AMRs and elevator resources / AMR 与电梯资源的统一初始楼层 |
| \(\iota_o\) | immutable and unique identifier of order \(o\) / 订单 \(o\) 的不可变唯一标识符 |
| \(s_o\) | source floor of order \(o\) / 订单 \(o\) 的起始楼层 |
| \(d_o\) | destination floor of order \(o\) / 订单 \(o\) 的目标楼层 |
| \(r_o\geq 0\) | order-ready offset relative to \(t_W\) / 相对于 \(t_W\) 的订单就绪时间偏移量 |
| \(\gamma\) | elevator travel time per traversed floor / 电梯每跨越一层的运行时间 |
| \(\tau^L\) | elevator loading time / 电梯装载时间 |
| \(\tau^U\) | elevator unloading time / 电梯卸载时间 |
| \(\tau^P\) | AMR pickup-service time / AMR 取货服务时间 |
| \(\tau^D\) | AMR drop-off-service time / AMR 交付服务时间 |
| \(\sigma\) | lognormal phase-time noise parameter under \(M_3\) / \(M_3\) 下阶段时间的对数正态噪声参数 |
| \(\alpha\) | lower-tail probability used to construct the structural classes / 用于构建结构类别的下尾概率 |

Order \(o\) becomes eligible at \(t_W+r_o\). Thus, \(r_o\) is an observed order attribute at the wave decision epoch. The publication-scale evaluator uses \(f^0=1\), \(\gamma=5\) s per floor, \(\tau^L=\tau^U=2\) s, and \(\tau^P=\tau^D=5\) s. The principal stochastic specification uses \(\sigma=0.20\).

> **中文：** 订单 \(o\) 在 \(t_W+r_o\) 时具备处理资格。因此，\(r_o\) 是波次决策时刻已观测到的订单属性。论文所报告的评估器参数设置为 \(f^0=1\)、\(\gamma=5\) 秒/层、\(\tau^L=\tau^U=2\) 秒以及 \(\tau^P=\tau^D=5\) 秒。主要随机设定采用 \(\sigma=0.20\)。

### 3.2.2 Candidate waves and canonical sequence / 候选波次与规范序列

The candidate pool contains \(K\) generated waves indexed by \(\mathcal K\). For each \(k\in\mathcal K\), let \(W^k\subseteq\mathcal O\) denote the unordered set of orders in candidate wave \(k\), with \(|W^k|=n\). Its operational processing sequence is determined by

> **中文：** 候选池包含由 \(\mathcal K\) 索引的 \(K\) 个已生成波次。对于每个 \(k\in\mathcal K\)，令 \(W^k\subseteq\mathcal O\) 表示候选波次 \(k\) 所包含的无序订单集合，并满足 \(|W^k|=n\)。其运行处理序列由下式确定：

\[
\pi(W^k)=\left(o_1^k,\ldots,o_n^k\right)
=\operatorname{sort}_{o\in W^k}\left(r_o,\iota_o\right),
\tag{1}
\]

where sorting is lexicographic: orders are first ranked by ready-time offset \(r_o\), and equal offsets are resolved by immutable order identifier \(\iota_o\). All three elevator evaluators use this sequence.

> **中文：** 其中采用字典序排序：首先依据就绪时间偏移量 \(r_o\) 排序，当偏移量相同时，再依据不可变订单标识符 \(\iota_o\) 确定先后顺序。三种电梯评估器均采用该序列。

For use in the candidate-selection constraints, the composition of \(W^k\) is represented by the derived incidence parameter

> **中文：** 为构建候选波次选择约束，使用以下派生归属参数表示 \(W^k\) 的订单构成：

\[
\delta_{ok}=
\begin{cases}
1, & o\in W^k,\\
0, & o\notin W^k.
\end{cases}
\tag{2}
\]

### 3.2.3 Wave descriptors and structural classes / 波次描述指标与结构类别

For a wave \(W\), define the share of source and destination endpoints located on floor \(f\) as

> **中文：** 对于波次 \(W\)，将位于楼层 \(f\) 的起点与终点所占比例定义为：

\[
p_f(W)=\frac{1}{2|W|}
\sum_{o\in W}
\left[
\mathbb I(s_o=f)+\mathbb I(d_o=f)
\right].
\tag{3}
\]

The endpoint-dispersion descriptor is

> **中文：** 端点离散度指标定义为：

\[
C(W)=-\sum_{f\in\mathcal F}p_f(W)\log p_f(W).
\tag{4}
\]

Higher \(C\) indicates that order endpoints occupy a broader set of floor labels. Physical floor-to-floor distance enters the operational evaluator through \(|s_o-d_o|\).

> **中文：** 较高的 \(C\) 表明订单端点分布于更广泛的楼层标签集合。实际楼层间距离通过 \(|s_o-d_o|\) 进入运行评估器。

Let

> **中文：** 令：

\[
N^{\uparrow}(W)=\sum_{o\in W}\mathbb I(d_o>s_o),
\qquad
N^{\downarrow}(W)=\sum_{o\in W}\mathbb I(d_o<s_o).
\]

Directional imbalance is

> **中文：** 方向不平衡度定义为：

\[
I(W)=
\begin{cases}
\dfrac{\left|N^{\uparrow}(W)-N^{\downarrow}(W)\right|}
{N^{\uparrow}(W)+N^{\downarrow}(W)},
& N^{\uparrow}(W)+N^{\downarrow}(W)>0,\\[8pt]
0, & N^{\uparrow}(W)+N^{\downarrow}(W)=0.
\end{cases}
\tag{5}
\]

Same-floor orders do not enter either directional count. Let \(\bar r_W=|W|^{-1}\sum_{o\in W}r_o\). Relative ready-time dispersion is

> **中文：** 同层订单不计入任一方向的订单数量。令 \(\bar r_W=|W|^{-1}\sum_{o\in W}r_o\)，则相对就绪时间离散度定义为：

\[
T(W)=
\begin{cases}
\dfrac{
\sqrt{|W|^{-1}\sum_{o\in W}(r_o-\bar r_W)^2}
}{\bar r_W},
& \bar r_W>0,\\[10pt]
0, & \bar r_W=0.
\end{cases}
\tag{6}
\]

Lower \(T\) represents more compact ready offsets relative to their mean; higher \(T\) represents greater relative dispersion. The complete descriptor vector is

> **中文：** 较低的 \(T\) 表示相对于均值更为集中的就绪时间偏移量；较高的 \(T\) 表示更大的相对离散程度。完整的描述指标向量为：

\[
\Phi(W)=\bigl(C(W),I(W),T(W)\bigr).
\tag{7}
\]

The principal corner design uses \(C\) and \(I\). For a tail probability \(\alpha\in(0,0.5)\), let \(Q_u(X)\) denote the empirical \(u\)-quantile of descriptor \(X\) in the candidate pool. Define

> **中文：** 主要角点设计采用 \(C\) 和 \(I\)。对于尾部概率 \(\alpha\in(0,0.5)\)，令 \(Q_u(X)\) 表示候选池中指标 \(X\) 的经验 \(u\) 分位数。定义：

\[
\begin{aligned}
\mathcal K_{\mathrm{HC}}&=\{k:C(W^k)\geq Q_{1-\alpha}(C)\},
&\mathcal K_{\mathrm{LC}}&=\{k:C(W^k)\leq Q_{\alpha}(C)\},\\
\mathcal K_{\mathrm{HI}}&=\{k:I(W^k)\geq Q_{1-\alpha}(I)\},
&\mathcal K_{\mathrm{LI}}&=\{k:I(W^k)\leq Q_{\alpha}(I)\}.
\end{aligned}
\tag{8}
\]

The four possible class labels are \(\mathrm{HH}\), \(\mathrm{HL}\), \(\mathrm{LH}\), and \(\mathrm{LL}\), where the first letter records the tail of \(C\) and the second records the tail of \(I\). Their candidate-index supports are

> **中文：** 四个可能的类别标签为 \(\mathrm{HH}\)、\(\mathrm{HL}\)、\(\mathrm{LH}\) 和 \(\mathrm{LL}\)，其中第一个字母表示 \(C\) 所处的尾部，第二个字母表示 \(I\) 所处的尾部。各类别对应的候选索引支持集为：

\[
\begin{aligned}
\mathcal K_{\mathrm{HH}}&=\mathcal K_{\mathrm{HC}}\cap\mathcal K_{\mathrm{HI}},
&\mathcal K_{\mathrm{HL}}&=\mathcal K_{\mathrm{HC}}\cap\mathcal K_{\mathrm{LI}},\\
\mathcal K_{\mathrm{LH}}&=\mathcal K_{\mathrm{LC}}\cap\mathcal K_{\mathrm{HI}},
&\mathcal K_{\mathrm{LL}}&=\mathcal K_{\mathrm{LC}}\cap\mathcal K_{\mathrm{LI}}.
\end{aligned}
\]

The structural-class label set is \(\mathcal Q=\{q\in\{\mathrm{HH},\mathrm{HL},\mathrm{LH},\mathrm{LL}\}:\mathcal K_q\neq\varnothing\}\). Quantile ties can place a candidate index in more than one support set, so the sets \(\mathcal K_q\) may overlap. The main implementation uses \(\alpha=0.25\). Descriptor \(T\) is activated in the designated staggered-readiness analyses.

> **中文：** 结构类别标签集合定义为 \(\mathcal Q=\{q\in\{\mathrm{HH},\mathrm{HL},\mathrm{LH},\mathrm{LL}\}:\mathcal K_q\neq\varnothing\}\)。分位数处的并列值可能使同一候选索引进入多个支持集，因此，各 \(\mathcal K_q\) 可以重叠。主要实现采用 \(\alpha=0.25\)。指标 \(T\) 用于指定的错峰就绪分析。

For each \(q\in\mathcal Q\), the fixed within-class candidate distribution is uniform on \(\mathcal K_q\):

> **中文：** 对于每个 \(q\in\mathcal Q\)，固定的类内候选波次分布在 \(\mathcal K_q\) 上取均匀分布：

\[
\nu_q(k)=
\begin{cases}
\dfrac{1}{|\mathcal K_q|}, & k\in\mathcal K_q,\\[6pt]
0, & k\notin\mathcal K_q.
\end{cases}
\tag{9}
\]

After class \(q\) is selected, \(\kappa\sim\nu_q\) denotes the candidate index drawn from \(\mathcal K_q\), and \(W^{\kappa}\) is the wave released for execution.

> **中文：** 选定类别 \(q\) 后，\(\kappa\sim\nu_q\) 表示从 \(\mathcal K_q\) 中抽取的候选索引，\(W^{\kappa}\) 则是实际释放执行的波次。

## 3.3 Decision Variables / 决策变量

Two formulations operate at different decision resolutions. The candidate formulation selects one concrete wave from the finite pool. The class formulation selects one structural class and applies the within-class rule in Equation (9).

> **中文：** 两种模型分别对应不同的决策层级。候选波次模型从有限候选池中选择一个具体波次；类别模型选择一个结构类别，并应用式（9）所定义的类内规则。

| Variable / 变量 | Domain / 取值域 | Definition / 定义 |
|---|---|---|
| \(z_k\) | \(\{0,1\}\) | 1 if candidate wave \(k\) is selected / 若选择候选波次 \(k\)，则取 1 |
| \(x_o\) | \(\{0,1\}\) | 1 if order \(o\) belongs to the selected candidate wave / 若订单 \(o\) 属于所选候选波次，则取 1 |
| \(y_q\) | \(\{0,1\}\) | 1 if structural class \(q\) is selected / 若选择结构类别 \(q\)，则取 1 |
| \(\eta^C\) | \(\mathbb R_+\) | largest candidate score over the specified evaluator family / 所选候选波次在指定评估器族上的最大得分 |
| \(\eta^Q\) | \(\mathbb R_+\) | largest class-level median over the specified evaluator family / 所选结构类别在指定评估器族上的最大波次完工期中位数 |

AMR assignments, elevator assignments, boarding decisions, and trip times are generated by the fixed evaluator. They are operational state quantities. The tactical optimization variables are \(z_k\), \(x_o\), and \(y_q\).

> **中文：** AMR 分配、电梯分配、登梯决策和行程时间均由固定评估器生成，属于运行状态量。战术层优化的决策变量为 \(z_k\)、\(x_o\) 和 \(y_q\)。

## 3.4 Assumptions / 模型假设

**A1. Single-wave decision horizon.** Each instance begins at \(t_W\) and ends when every order in the selected wave is complete. All performance measures refer to this isolated wave, and no other wave overlaps its evaluation interval.

> **中文：** **A1. 单波次决策时域。** 每个实例始于 \(t_W\)，并在所选波次中的全部订单完成时结束。所有绩效指标均针对该独立波次计算，评估期间不存在其他波次与之重叠。

**A2. Known candidate information.** The source floor, destination floor, ready offset, and immutable identifier of every available order are known when the candidate waves are generated.

> **中文：** **A2. 候选信息已知。** 在生成候选波次时，每个可用订单的起始楼层、目标楼层、就绪时间偏移量及不可变标识符均为已知信息。

**A3. Canonical processing order.** All evaluators process each candidate wave according to the common sequence \(\pi(W^k)\) defined in Equation (1).

> **中文：** **A3. 规范处理顺序。** 所有评估器均按照式（1）定义的统一序列 \(\pi(W^k)\) 处理每个候选波次。

**A4. Cold-start resource state.** At \(t_W\), every AMR and elevator resource is available at floor \(f^0\). The instance begins without inherited resource reservations or unfinished orders.

> **中文：** **A4. 冷启动资源状态。** 在 \(t_W\) 时刻，所有 AMR 和电梯资源均位于楼层 \(f^0\) 且处于可用状态。实例开始时不存在从前序波次继承的资源预约或未完成订单。

**A5. AMR mobility and service.** An AMR remains assigned to an order through drop-off and rides the elevator during cross-floor movements. It may therefore serve orders on different floors. The principal evaluator aggregates intra-floor travel and handling into the fixed pickup and drop-off durations \(\tau^P\) and \(\tau^D\). An elevator request is generated whenever the AMR's current floor differs from the next required floor.

> **中文：** **A5. AMR 移动与服务。** 从开始处理订单直至完成交付，同一 AMR 始终负责该订单，并在跨楼层移动时搭乘电梯。因此，一个 AMR 可以服务位于不同楼层的订单。主评估器将楼层内移动和操作时间合并为固定的取货时长 \(\tau^P\) 与交付时长 \(\tau^D\)。当 AMR 当前所在楼层与下一任务所需楼层不同时，系统生成一次电梯请求。

**A6. Fixed AMR assignment.** Orders are considered in canonical order. Each order is assigned to the AMR with the smallest current availability time; an availability tie is resolved by AMR index. Order processing begins at the larger of the assigned AMR's availability time and \(t_W+r_o\).

> **中文：** **A6. 固定 AMR 分配规则。** 订单按照规范顺序依次处理。每个订单分配给当前最早可用的 AMR；若多个 AMR 的可用时间相同，则按照 AMR 索引确定分配对象。订单处理开始时间取该 AMR 的可用时间与 \(t_W+r_o\) 中的较大值。

**A7. Serial resource reservation.** Each order is advanced through its complete route before the next canonical order is considered. Elevator requests update the selected resource state in this reservation order. The generated request timestamps need not be globally increasing.

> **中文：** **A7. 串行资源预约。** 当前订单沿完整路径完成资源预约后，模型才处理规范顺序中的下一个订单。电梯请求按照该预约顺序更新所选资源的状态，由此生成的请求时间戳不必在全局范围内单调递增。

**A8. Stable elevator selection.** Equal elevator availability is resolved by virtual-slot index under \(M_1\) and by car index under \(M_2\) and \(M_3\). When several cars have an open scheduled loading window for the same origin-destination request, the lowest-index boardable car is selected.

> **中文：** **A8. 稳定电梯选择规则。** 当电梯可用时间相同时，\(M_1\) 按虚拟服务槽索引确定优先级，\(M_2\) 和 \(M_3\) 按电梯轿厢索引确定优先级。当多个轿厢对同一起讫楼层请求均存在开放的已排程装载窗口时，选择索引最小的可登梯轿厢。

**A9. Throughput abstraction \(M_1\).** The \(E\) elevators with capacity \(c\) are represented by \(Ec\) independent single-request virtual slots. Each slot has its own location and availability clock. Separate requests occupy separate virtual trips.

> **中文：** **A9. 吞吐能力抽象 \(M_1\)。** 将 \(E\) 部容量为 \(c\) 的电梯表示为 \(Ec\) 个相互独立、每次处理一个请求的虚拟服务槽。每个服务槽拥有独立的位置状态和可用时钟，不同请求占用不同的虚拟行程。

**A10. Co-occupancy evaluator \(M_2\).** The evaluator contains \(E\) physical cars, each with capacity \(c\). A request may join a scheduled trip when its origin and destination match, its request time is no later than the trip's loading-end time, and residual capacity is available. A request that cannot join such a trip initiates a new reservation on the earliest-available car.

> **中文：** **A10. 同乘评估器 \(M_2\)。** 该评估器包含 \(E\) 个实体轿厢，每个轿厢的容量为 \(c\)。当某请求的起始楼层和目标楼层与已排程行程一致、请求时刻不晚于该行程的装载结束时刻，且轿厢仍有剩余容量时，该请求可以加入该行程。无法加入现有行程的请求将在最早可用的轿厢上建立新的资源预约。

**A11. Stochastic evaluator \(M_3\).** Evaluator \(M_3\) retains the assignment, boarding, and capacity rules of \(M_2\). The repositioning, loading, loaded-travel, and unloading durations of every new trip receive mean-one lognormal multipliers that are independent across phases and trips. For each phase multiplier \(Z\),

> **中文：** **A11. 随机评估器 \(M_3\)。** 评估器 \(M_3\) 沿用 \(M_2\) 的分配、登梯和容量规则。每个新行程的空载调位、装载、载货运行和卸载时长均乘以均值为 1 的对数正态随机因子，各随机因子在不同阶段和不同行程之间相互独立。对于任一阶段乘数 \(Z\)，有

\[
\log Z\sim\mathcal N\left(-\frac{\sigma^2}{2},\sigma^2\right),
\qquad
\mathbb E[Z]=1.
\tag{10}
\]

The phase multipliers generated during one complete \(M_3\) wave evaluation form a realization \(\xi\in\Xi\), where \(\Xi\) is the corresponding realization space.

> **中文：** 一次完整的 \(M_3\) 波次评价中生成的全部阶段乘数共同构成一个随机实现 \(\xi\in\Xi\)，其中 \(\Xi\) 表示相应的随机实现空间。

Waiting time follows from the resource availability clock. Pickup and drop-off times retain their fixed values in the principal specification.

> **中文：** 等待时间由资源可用时钟确定。主模型中的取货和交付时长保持为固定值。

**A12. Evaluator exogeneity.** The resource configuration, operational rule, and evaluator parameters remain fixed while the tactical wave decision changes. Wave composition determines the elevator request stream received by the evaluator.

> **中文：** **A12. 评估器外生性。** 当战术层波次决策发生变化时，资源配置、运行规则和评估器参数保持不变。波次构成决定评估器接收的电梯请求流。

**A13. Fixed within-class implementation.** Every selectable class contains at least one candidate. A selected class is converted to a concrete release by the distribution \(\nu_q\) in Equation (9). The within-class candidate draw and the \(M_3\) phase-time realization are independent.

> **中文：** **A13. 固定类内实施规则。** 每个可选类别至少包含一个候选波次。所选类别通过式（9）中的分布 \(\nu_q\) 转换为一个具体的待释放候选波次。类内候选波次抽样与 \(M_3\) 的阶段时长随机实现相互独立。

## 3.5 Objective Functions / 目标函数

### 3.5.1 Wave Makespan / 波次完工期

Let \(t^{C}_{jkm}(\xi)\) denote the completion time of the order in canonical position \(j\) of candidate \(k\) under evaluator \(m\). The realized wave makespan is

> **中文：** 令 \(t^{C}_{jkm}(\xi)\) 表示候选波次 \(k\) 中处于规范位置 \(j\) 的订单在评估器 \(m\) 下的完成时刻。一次实现下的波次完工期定义为

\[
Y_{km}(\xi)
=C_{\max}(W^k;m,\xi)
=\max_{j\in\mathcal J_n}t^{C}_{jkm}(\xi)-t_W.
\tag{11}
\]

The outcome is deterministic under \(M_1\) and \(M_2\). Under \(M_3\), \(\xi\) indexes the phase-time realization.

> **中文：** 在 \(M_1\) 和 \(M_2\) 下，该结果为确定性结果；在 \(M_3\) 下，\(\xi\) 表示阶段时长的随机实现。

### 3.5.2 Candidate-Wave Benchmark / 候选波次基准

Let \(\mathcal M_D=\{M_1,M_2\}\subset\mathcal M\) denote the deterministic evaluator family. For \(m\in\mathcal M_D\), define the deterministic candidate score

> **中文：** 令 \(\mathcal M_D=\{M_1,M_2\}\subset\mathcal M\) 表示确定性评估器族。对于 \(m\in\mathcal M_D\)，定义确定性候选波次得分为

\[
\ell_{km}=C_{\max}(W^k;m).
\tag{12}
\]

The single-evaluator finite-pool benchmark is

> **中文：** 单一评估器下的有限候选池基准为

\[
\min_{k\in\mathcal K}\ \ell_{km}.
\tag{13}
\]

For a prespecified nonempty evaluator family \(\varnothing\neq\mathcal M_R\subseteq\mathcal M_D\), the robust candidate benchmark is

> **中文：** 对于预先指定的非空评估器族 \(\varnothing\neq\mathcal M_R\subseteq\mathcal M_D\)，鲁棒候选波次基准为

\[
\min_{k\in\mathcal K}\ \max_{m\in\mathcal M_R}\ell_{km}.
\tag{14}
\]

The term *pool optimum* denotes the optimum obtained over the candidate waves indexed by \(\mathcal K\).

> **中文：** 术语“候选池最优值”（*pool optimum*）表示在由 \(\mathcal K\) 索引的候选波次中取得的最优值。

### 3.5.3 Robust Class-Selection Objective / 鲁棒类别选择目标

For class \(q\) and evaluator \(m\), define

> **中文：** 对于类别 \(q\) 和评估器 \(m\)，定义

\[
\mu_{qm}^{0.5}
=\operatorname{Med}_{\kappa\sim\nu_q,\,\xi}
\left[Y_{\kappa m}(\xi)\right].
\tag{15}
\]

For \(M_1\) and \(M_2\), the distribution in Equation (15) is induced by the within-class candidate rule. Under \(M_3\), it includes both candidate variation and stochastic trip durations. The superscript \(0.5\) identifies the median estimand.

> **中文：** 对于 \(M_1\) 和 \(M_2\)，式（15）中的分布由类内候选波次规则产生；在 \(M_3\) 下，该分布同时包含候选波次差异和随机行程时长。上标 \(0.5\) 表明该待估量为中位数。

Equation (15) is the primary policy-level estimand.

> **中文：** 式（15）给出了策略层主要待估量。

The median-minimax class problem over the deterministic evaluator family is

> **中文：** 确定性评估器族上的中位数极小极大类别选择问题为

\[
q^{\star}\in
\arg\min_{q\in\mathcal Q}
\max_{m\in\mathcal M_D}\mu_{qm}^{0.5}.
\tag{16}
\]

After \(q^{\star}\) is selected, the release rule draws \(\kappa\sim\nu_{q^{\star}}\). Evaluator \(M_3\) supplies the stochastic performance assessment of the selected class.

> **中文：** 选定 \(q^{\star}\) 后，释放规则按照 \(\kappa\sim\nu_{q^{\star}}\) 抽取具体候选波次。评估器 \(M_3\) 用于评估所选类别的随机绩效。

## 3.6 Constraints / 约束条件

### 3.6.1 Operational state relations / 运行状态关系

Fix candidate \(k\), evaluator \(m\), and realization \(\xi\). Their indices are suppressed on all operational state quantities in this subsection. At the start of a wave, AMR \(a\) has availability \(H_a^0=t_W\) and location \(G_a^0=f^0\). For \(o_j^k=\pi_j(W^k)\), the assigned AMR is

> **中文：** 固定候选波次 \(k\)、评估器 \(m\) 和随机实现 \(\xi\)。本小节在所有运行状态量中省略这些下标。在波次开始时，AMR \(a\) 的可用时刻为 \(H_a^0=t_W\)，所在楼层为 \(G_a^0=f^0\)。对于 \(o_j^k=\pi_j(W^k)\)，所分配的 AMR 为

\[
a_j=
\underset{a\in\mathcal A}{\operatorname{lex\,arg\,min}}
\left(H_a^{j-1},a\right),
\tag{17}
\]

and the earliest start of the order is

> **中文：** 该订单的最早开始时刻为

\[
t_j^0=\max\left\{H_{a_j}^{j-1},\ t_W+r_{o_j^k}\right\}.
\tag{18}
\]

Let \(\mathbf S_m\) denote the complete state of the elevator resources under evaluator \(m\). A request is the state transition

> **中文：** 令 \(\mathbf S_m\) 表示评估器 \(m\) 下电梯资源的完整状态。一次电梯请求对应以下状态转移：

\[
(\widehat t,\mathbf S_m^+)
=\mathscr R_m(\mathbf S_m,g,h,t;\xi),
\]

where \(g\), \(h\), and \(t\) are the origin floor, destination floor, and request time, \(\widehat t\) is the request completion time, and \(\mathbf S_m^+\) is the updated state. For compactness, \(\mathcal R_m(g,h,t)\) denotes \(\widehat t\) within the fixed evaluation, and every call replaces \(\mathbf S_m\) by \(\mathbf S_m^+\). The assigned AMR reaches the order's source at

> **中文：** 其中，\(g\)、\(h\) 和 \(t\) 分别为起始楼层、目标楼层和请求时刻；\(\widehat t\) 为请求完成时刻；\(\mathbf S_m^+\) 为更新后的状态。为简化记号，在固定的一次评估中以 \(\mathcal R_m(g,h,t)\) 表示 \(\widehat t\)，并在每次调用后以 \(\mathbf S_m^+\) 替换 \(\mathbf S_m\)。所分配的 AMR 到达订单起始楼层的时刻为

\[
t_j^S=
\begin{cases}
\mathcal R_m(G_{a_j}^{j-1},s_{o_j^k},t_j^0),
& G_{a_j}^{j-1}\neq s_{o_j^k},\\
t_j^0,
& G_{a_j}^{j-1}=s_{o_j^k}.
\end{cases}
\tag{19}
\]

Pickup ends at

> **中文：** 取货服务的结束时刻为

\[
t_j^P=t_j^S+\tau^P.
\tag{20}
\]

The assigned AMR reaches the destination at

> **中文：** 所分配的 AMR 到达订单目标楼层的时刻为

\[
t_j^D=
\begin{cases}
\mathcal R_m(s_{o_j^k},d_{o_j^k},t_j^P),
& s_{o_j^k}\neq d_{o_j^k},\\
t_j^P,
& s_{o_j^k}=d_{o_j^k}.
\end{cases}
\tag{21}
\]

The order completion and AMR-state update are

> **中文：** 订单完成时刻及 AMR 状态更新为

\[
t_j^C=t_j^D+\tau^D,
\tag{22}
\]

\[
H_{a_j}^{j}=t_j^C,
\qquad
G_{a_j}^{j}=d_{o_j^k}.
\tag{23}
\]

For every \(a\neq a_j\), \(H_a^j=H_a^{j-1}\) and \(G_a^j=G_a^{j-1}\).

> **中文：** 对于所有 \(a\neq a_j\)，均有 \(H_a^j=H_a^{j-1}\) 和 \(G_a^j=G_a^{j-1}\)，即未被分配该订单的 AMR 状态保持不变。

Restoring the suppressed indices gives \(t_{jkm}^{C}(\xi)=t_j^C\), which is the completion quantity used in Equation (11).

> **中文：** 恢复被省略的下标后，可得 \(t_{jkm}^{C}(\xi)=t_j^C\)，这正是式（11）所使用的订单完成时刻。

Under \(M_1\), let \(B_v\) and \(G_v\) denote the availability time and location of virtual slot \(v\). Initially, \(B_v=t_W\) and \(G_v=f^0\). A request is assigned by

> **中文：** 在 \(M_1\) 下，令 \(B_v\) 和 \(G_v\) 分别表示虚拟服务槽 \(v\) 的可用时刻和所在楼层。初始时，\(B_v=t_W\) 且 \(G_v=f^0\)。电梯请求按照下式分配：

\[
v^{\star}=
\underset{v\in\mathcal V_1}{\operatorname{lex\,arg\,min}}
\left(B_v,v\right),
\tag{24}
\]

and completes at

> **中文：** 该请求的完成时刻为

\[
\mathcal R_1(g,h,t)
=\max\{t,B_{v^{\star}}\}
+\gamma|G_{v^{\star}}-g|
+\tau^L
+\gamma|g-h|
+\tau^U.
\tag{25}
\]

After Equation (25), \(B_{v^{\star}}\leftarrow\mathcal R_1(g,h,t)\) and \(G_{v^{\star}}\leftarrow h\).

> **中文：** 执行式（25）后，更新 \(B_{v^{\star}}\leftarrow\mathcal R_1(g,h,t)\) 和 \(G_{v^{\star}}\leftarrow h\)。

Under \(M_2\), let \(B_e\), \(G_e\), \((\bar s_e,\bar d_e)\), \(L_e\), \(D_e\), and \(P_e\) denote car \(e\)'s availability time, location, scheduled trip pair, loading-end time, trip-completion time, and current occupancy. Initially, \(B_e=D_e=t_W\), \(G_e=f^0\), \((\bar s_e,\bar d_e)=\varnothing\), \(L_e=-\infty\), and \(P_e=0\). For request \((g,h,t)\), define the boardable-car set

> **中文：** 在 \(M_2\) 下，令 \(B_e\)、\(G_e\)、\((\bar s_e,\bar d_e)\)、\(L_e\)、\(D_e\) 和 \(P_e\) 分别表示电梯轿厢 \(e\) 的可用时刻、所在楼层、已排程行程的起终点组合、装载结束时刻、行程完成时刻和当前搭载的 AMR 数量。初始时，\(B_e=D_e=t_W\)、\(G_e=f^0\)、\((\bar s_e,\bar d_e)=\varnothing\)、\(L_e=-\infty\) 且 \(P_e=0\)。对于请求 \((g,h,t)\)，可登梯轿厢集合定义为

\[
\mathcal B(g,h,t)=
\left\{
e\in\mathcal E:
(\bar s_e,\bar d_e)=(g,h),\ P_e<c,\ t\leq L_e
\right\}.
\tag{26}
\]

If \(\mathcal B(g,h,t)\neq\varnothing\), the request selects

> **中文：** 若 \(\mathcal B(g,h,t)\neq\varnothing\)，则该请求选择

\[
e^{\star}=\min\mathcal B(g,h,t),
\tag{27}
\]

receives \(\mathcal R_2(g,h,t)=D_{e^{\star}}\), the trip's stored completion time, and updates \(P_{e^{\star}}\leftarrow P_{e^{\star}}+1\).

> **中文：** 该请求获得该行程已存储的完成时刻 \(\mathcal R_2(g,h,t)=D_{e^{\star}}\)，并更新 \(P_{e^{\star}}\leftarrow P_{e^{\star}}+1\)。

If \(\mathcal B(g,h,t)=\varnothing\), a new trip is assigned by

> **中文：** 若 \(\mathcal B(g,h,t)=\varnothing\)，则按照下式为新行程分配电梯：

\[
e^{\star}=
\underset{e\in\mathcal E}{\operatorname{lex\,arg\,min}}
\left(B_e,e\right),
\tag{28}
\]

with loading-end and completion times

> **中文：** 该新行程的装载结束时刻和完成时刻分别为

\[
L_{e^{\star}}
=\max\{t,B_{e^{\star}}\}
+\gamma|G_{e^{\star}}-g|
+\tau^L,
\tag{29}
\]

\[
D_{e^{\star}}
=L_{e^{\star}}
+\gamma|g-h|
+\tau^U.
\tag{30}
\]

The car state is updated as

> **中文：** 电梯轿厢状态更新为

\[
B_{e^{\star}}\leftarrow D_{e^{\star}},
\quad
G_{e^{\star}}\leftarrow h,
\quad
(\bar s_{e^{\star}},\bar d_{e^{\star}})\leftarrow(g,h),
\quad
P_{e^{\star}}\leftarrow1.
\tag{31}
\]

The completion returned by a newly reserved trip is \(\mathcal R_2(g,h,t)=D_{e^{\star}}\).

> **中文：** 新预约行程返回的完成时刻为 \(\mathcal R_2(g,h,t)=D_{e^{\star}}\)。

Under \(M_3\), Equations (26) to (28) retain the same assignment and boarding conditions. For each new trip, let \(Z^{\mathrm{rep}},Z^{\mathrm{load}},Z^{\mathrm{trav}},Z^{\mathrm{unload}}\) be independent multipliers satisfying Equation (10). Equations (29) and (30) become

> **中文：** 在 \(M_3\) 下，式（26）至式（28）保持相同的分配与登梯条件。对于每个新行程，令 \(Z^{\mathrm{rep}}\)、\(Z^{\mathrm{load}}\)、\(Z^{\mathrm{trav}}\) 和 \(Z^{\mathrm{unload}}\) 为满足式（10）的相互独立乘数。此时，式（29）和式（30）改写为

\[
L_{e^{\star}}
=\max\{t,B_{e^{\star}}\}
+\gamma|G_{e^{\star}}-g|Z^{\mathrm{rep}}
+\tau^L Z^{\mathrm{load}},
\tag{32}
\]

\[
D_{e^{\star}}
=L_{e^{\star}}
+\gamma|g-h|Z^{\mathrm{trav}}
+\tau^U Z^{\mathrm{unload}}.
\tag{33}
\]

The returned completion time is the stored \(D_{e^{\star}}\), both for a request that joins an open loading window and for a newly reserved trip.

> **中文：** 无论请求加入一个开放的装载时间窗，还是形成一个新预约行程，返回值均为已存储的完成时刻 \(D_{e^{\star}}\)。

### 3.6.2 Candidate-selection constraints / 候选波次选择约束

The robust candidate objective in Equation (14) has the epigraph formulation

> **中文：** 式（14）中的鲁棒候选波次目标可改写为如下上图（epigraph）形式：

\[
\min_{z,x,\eta^C}\ \eta^C
\tag{34}
\]

subject to

> **中文：** 约束条件如下：

\[
\sum_{k\in\mathcal K}z_k=1,
\tag{35}
\]

\[
x_o=\sum_{k\in\mathcal K}\delta_{ok}z_k,
\qquad o\in\mathcal O,
\tag{36}
\]

\[
\sum_{o\in\mathcal O}x_o=n,
\tag{37}
\]

\[
\eta^C\geq
\sum_{k\in\mathcal K}\ell_{km}z_k,
\qquad m\in\mathcal M_R,
\tag{38}
\]

\[
z_k\in\{0,1\},
\qquad
x_o\in\{0,1\},
\qquad
\eta^C\geq0.
\tag{39}
\]

For the single-evaluator benchmark in Equation (13), Equation (38) is replaced by the objective \(\min\sum_{k\in\mathcal K}\ell_{km}z_k\).

> **中文：** 对于式（13）中的单一评估器基准，以目标函数 \(\min\sum_{k\in\mathcal K}\ell_{km}z_k\) 替代式（38）。

### 3.6.3 Class-selection constraints / 结构类别选择约束

The class objective in Equation (16) has the epigraph formulation

> **中文：** 式（16）中的结构类别目标可写为以下上图形式：

\[
\min_{y,\eta^Q}\ \eta^Q
\tag{40}
\]

subject to

> **中文：** 约束条件如下：

\[
\sum_{q\in\mathcal Q}y_q=1,
\tag{41}
\]

\[
\eta^Q\geq
\sum_{q\in\mathcal Q}\mu_{qm}^{0.5}y_q,
\qquad m\in\mathcal M_D,
\tag{42}
\]

\[
y_q\in\{0,1\},
\qquad
\eta^Q\geq0.
\tag{43}
\]

## 3.7 Constraint explanation / 约束解释

Equation (17) assigns each canonical-order position to the earliest-available AMR. The AMR index in the lexicographic key gives a unique assignment when availability times coincide. Equation (18) combines AMR availability with order eligibility, so service starts at or after the ready epoch \(t_W+r_o\).

> **中文：** 式（17）将规范顺序中的每个位置分配给最早可用的 AMR。字典序键中的 AMR 索引保证多个 AMR 可用时刻相同时仍能得到唯一分配。式（18）同时考虑 AMR 可用性和订单就绪条件，因此服务开始时刻不会早于就绪时刻 \(t_W+r_o\)。

Equations (19) to (23) describe an order's two possible vertical movements. The first moves the assigned AMR from its current floor to the order's source. The second moves the loaded AMR from the source to the destination. A movement is activated whenever its two endpoints differ. Consequently, a same-floor order can still require an initial elevator trip when the assigned AMR begins on another floor. Pickup and drop-off advance the AMR clock by fixed service durations.

> **中文：** 式（19）至式（23）描述了订单可能涉及的两次垂直移动。第一次将所分配的 AMR 从当前楼层移动到订单起始楼层；第二次将载货 AMR 从起始楼层移动到目标楼层。只要一次移动的起终点不同，就会触发电梯请求。因此，即使订单的起始楼层和目标楼层相同，当所分配的 AMR 初始位于其他楼层时，仍可能需要先乘坐一次电梯。取货与交付服务按照固定服务时长推进 AMR 时钟。

Equations (24) and (25) implement the \(M_1\) throughput abstraction. Capacity enters through \(Ec\) independent virtual slots. Each slot retains its own floor and availability state, and the slot index resolves equal availability. The resulting evaluator represents aggregate vertical throughput at the request level.

> **中文：** 式（24）和式（25）实现 \(M_1\) 的吞吐能力抽象。容量通过 \(Ec\) 个相互独立的虚拟服务槽进入模型。每个服务槽保留自己的楼层和可用状态，并以服务槽索引处理可用时刻相同的情况。由此得到的评估器在单次请求层面表示汇总后的垂直运输吞吐能力。

Equations (26) to (31) implement same-origin, same-destination co-occupancy under \(M_2\). Equation (26) admits a request to a scheduled trip only while the loading window is open and residual capacity remains. Equation (27) fixes the result when several cars can accept the request. Equations (28) to (31) create and update a new trip when the boardable set is empty. Evaluator \(M_3\) preserves these feasibility conditions while Equations (32) and (33) introduce phase-level duration variability.

> **中文：** 式（26）至式（31）实现 \(M_2\) 下同起点、同终点的同乘机制。式（26）规定，只有在装载时间窗仍开放且电梯仍有剩余容量时，请求才能加入已排程行程。式（27）确定多台电梯均可接受该请求时的选择结果。当可登梯轿厢集合为空时，式（28）至式（31）建立并更新一个新行程。\(M_3\) 保留这些可行性条件，并通过式（32）和式（33）引入行程阶段层面的时长波动。

Equation (35) selects exactly one candidate wave. Equation (36) converts candidate selection into order-membership variables, and Equation (37) records the fixed wave size. Equations (38) and (39) form the worst-evaluator candidate score. For the selected candidate, \(\eta^C\) is bounded below by its score under every evaluator in \(\mathcal M_R\); minimizing \(\eta^C\) therefore minimizes the largest of those scores.

> **中文：** 式（35）选择且仅选择一个候选波次。式（36）将候选波次选择转换为订单归属变量，式（37）记录固定的波次规模。式（38）和式（39）构成最不利评估器下的候选波次得分。对于被选候选波次，\(\eta^C\) 不小于其在 \(\mathcal M_R\) 中任一评估器下的得分；因此，最小化 \(\eta^C\) 等价于最小化这些得分中的最大值。

Equation (41) selects exactly one structural class. Equation (42) applies the epigraph construction to the class-level median makespan. The resulting decision minimizes the largest median over \(M_1\) and \(M_2\). Equation (9) then maps the selected class to a concrete candidate release. This provides a complete path from the robust structural decision to an executable single-wave release.

> **中文：** 式（41）选择且仅选择一个结构类别。式（42）采用上图变换表示类别层波次完工期中位数。由此得到的决策最小化 \(M_1\) 与 \(M_2\) 下两个中位数中的较大者。随后，式（9）将被选类别映射为一个具体候选波次并执行释放，从而形成从鲁棒结构决策到可执行单波次释放的完整路径。

The candidate and class formulations answer two complementary questions. Equations (34) to (39) identify the best available concrete wave in a finite pool and provide the pool benchmark used in empirical comparisons. Equations (40) to (43) choose a structural class using the primary median estimand and supply the decision problem addressed by the hedge method.

> **中文：** 候选波次模型与结构类别模型回答两个互补问题。式（34）至式（39）从有限候选池中识别可用的最优具体波次，并给出经验比较所采用的候选池基准。式（40）至式（43）使用主要的中位数待估量选择结构类别，从而给出对冲方法所求解的决策问题。
