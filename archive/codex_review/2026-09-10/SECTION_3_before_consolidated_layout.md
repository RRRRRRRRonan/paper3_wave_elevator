---
title: "Section 3. Problem formulation / 问题建模"
date: 2026-09-07
status: "canonical bilingual manuscript draft"
scope: "fixed-size single-wave candidate and class selection"
implementation_alignment: "target specification for the Phase 1 simulator repair; production alignment and result recomputation remain separate"
---

# 3. Problem formulation / 问题建模

## 3.1 Problem setting and assumptions / 问题背景与假设

We consider a multi-story warehouse in which autonomous mobile robots (AMRs) transport orders between source and destination floors using shared elevators. An AMR travels to an order's source, collects the load, and delivers it to the destination. The same AMR serves the order through delivery and rides an elevator whenever a movement crosses floors. The orders released together form a wave. Their origins, destinations, and ready times determine the vertical transport requests generated during wave execution.

> **中文：** 本研究考虑一个多楼层仓库，自主移动机器人（AMR）利用共享电梯，在订单的起始楼层与目标楼层之间完成运输。AMR 首先前往订单起点取货，再将货物送至目标位置。同一 AMR 负责该订单直至交付完成，并在跨楼层移动时搭乘电梯。共同释放的订单构成一个波次，其起点、终点和就绪时刻决定波次执行过程中产生的垂直运输请求。

The warehouse management system selects a wave of fixed size from a finite pool of candidate waves. Resource quantities and operational rules are given, so the decision concerns which orders enter the wave. The main formulation selects a structural class, defined by the floor distribution and directional balance of its candidate waves, and implements that choice through a fixed within-class selection rule. Direct selection of a concrete candidate wave provides a finite-pool benchmark.

> **中文：** 仓库管理系统从有限候选波次池中选择一个固定规模的波次。资源数量和运行规则均已给定，因此决策关注哪些订单进入该波次。主模型选择一个结构类别，该类别由其候选波次的楼层分布和方向平衡特征定义，并通过固定的类内选择规则落实为具体波次。直接选择某个候选波次则用于建立有限候选池基准。

Each decision instance concerns one isolated wave released at time \(t_W\). Every available order has a known source floor, destination floor, ready-time offset, and immutable identifier. An order with ready-time offset \(r_o\geq0\) becomes eligible for processing at \(t_W+r_o\). All AMRs and elevator resources are initially available at a common floor \(f^0\), with no outstanding reservations. The evaluation ends when all selected orders have been delivered; no other wave shares its resources during this interval.

> **中文：** 每个决策实例针对一个在时刻 \(t_W\) 释放的独立波次。每个可用订单的起始楼层、目标楼层、就绪时间偏移量和不可变标识符均为已知信息。就绪时间偏移量为 \(r_o\geq0\) 的订单在 \(t_W+r_o\) 时具备处理资格。所有 AMR 和电梯资源初始时均位于同一楼层 \(f^0\)，处于可用状态且没有尚待执行的预约。评价在全部所选订单完成交付时结束，期间没有其他波次共享这些资源。

Intra-floor movement and handling are represented by fixed pickup and drop-off service durations. Elevator travel time is proportional to the number of floors traversed, and each trip includes loading and unloading. The elevator evaluators differ in their representation of capacity and trip-time variability. They map each candidate wave to its completion time under the same wave-level decision conditions.

> **中文：** 楼层内移动与操作由固定的取货和交付服务时长表示。电梯运行时间与跨越的楼层数成正比，每次行程还包含装载与卸载过程。不同电梯评估器对容量和行程时间波动采用不同表示，并在相同的波次层决策条件下，将候选波次映射为其完成时间。

## 3.2 Notation / 记号

Tables 3.1 and 3.2 summarize the basic indices and input parameters. Candidate-wave descriptors and operational state quantities are introduced with their definitions in Sections 3.3 and 3.4.

> **中文：** 表 3.1 和表 3.2 汇总基础索引与输入参数。候选波次描述指标和运行状态量分别在第 3.3 节与第 3.4 节中随其定义引入。

Table 3.1. Basic indices and sets.

> **中文：** 表 3.1 基础索引与集合。

| Symbol / 符号 | Definition / 定义 |
|---|---|
| \(f\in\mathcal F=\{1,\ldots,F\}\) | warehouse-floor index / 仓库楼层索引 |
| \(o\in\mathcal O\) | order index in the available order pool / 可用订单池中的订单索引 |
| \(a\in\mathcal A=\{1,\ldots,A\}\) | AMR index / AMR 索引 |
| \(e\in\mathcal E=\{1,\ldots,E\}\) | physical-elevator index / 实体电梯轿厢索引 |
| \(k\in\mathcal K=\{1,\ldots,K\}\) | candidate-wave index, shared by all evaluators / 所有评估器共用的候选波次索引 |
| \(q\in\mathcal Q\) | selectable structural-class label / 可选结构类别标签 |
| \(m\in\mathcal M=\{M_1,M_2,M_3\}\) | elevator-evaluator index / 电梯评估器索引 |

Table 3.2. Input parameters.

> **中文：** 表 3.2 输入参数。

| Symbol / 符号 | Definition / 定义 |
|---|---|
| \(F\) | number of warehouse floors / 仓库楼层数 |
| \(A\) | number of AMRs / AMR 数量 |
| \(E\) | number of physical elevator cars / 实体电梯轿厢数量 |
| \(c\) | maximum number of AMRs sharing one physical elevator trip / 单次实体电梯行程可搭载的最大 AMR 数量 |
| \(n\) | fixed number of orders in a wave / 波次中的固定订单数量 |
| \(K\) | number of candidate waves in the finite pool / 有限候选池中的候选波次数量 |
| \(t_W\) | decision and release epoch of the wave / 波次决策与释放时刻 |
| \(f^0\in\mathcal F\) | common initial floor of AMRs and elevator resources / AMR 与电梯资源的统一初始楼层 |
| \(\iota_o\) | immutable and unique identifier of order \(o\) / 订单 \(o\) 的不可变唯一标识符 |
| \(s_o,d_o\in\mathcal F\) | source and destination floors of order \(o\) / 订单 \(o\) 的起始楼层与目标楼层 |
| \(r_o\geq0\) | order-ready offset relative to \(t_W\) / 相对于 \(t_W\) 的订单就绪时间偏移量 |
| \(\gamma>0\) | elevator travel time per traversed floor / 电梯每跨越一层的运行时间 |
| \(\tau^L,\tau^U>0\) | elevator loading and unloading durations / 电梯装载与卸载时长 |
| \(\tau^P,\tau^D>0\) | AMR pickup and drop-off service durations / AMR 取货与交付服务时长 |
| \(\alpha\in(0,0.5)\) | tail probability for structural-class construction / 构建结构类别所采用的尾部概率 |
| \(\sigma>0\) | lognormal phase-time noise parameter under \(M_3\) / \(M_3\) 下阶段时间的对数正态噪声参数 |

The resource counts, capacity, and candidate-pool size are positive integers, and \(1\leq n\leq|\mathcal O|\). All service durations and time offsets use the same time unit.

> **中文：** 资源数量、容量和候选池规模均为正整数，且 \(1\leq n\leq|\mathcal O|\)。所有服务时长和时间偏移量采用同一时间单位。

## 3.3 Candidate waves and structural classes / 候选波次与结构类别

### 3.3.1 Candidate waves / 候选波次

Each candidate \(k\in\mathcal K\) is an unordered set \(W^k\subseteq\mathcal O\) containing \(n\) orders. The finite pool is generated before selection and held fixed across evaluators. Its order membership is represented by the incidence parameter \(\delta_{ok}\):

> **中文：** 每个候选波次 \(k\in\mathcal K\) 是包含 \(n\) 个订单的无序集合 \(W^k\subseteq\mathcal O\)。有限候选池在选择决策之前生成，并在各评估器之间保持不变。归属参数 \(\delta_{ok}\) 表示订单是否属于该候选波次：

\[
|W^k|=n,\qquad
\delta_{ok}=
\begin{cases}
1, & o\in W^k,\\
0, & o\notin W^k,
\end{cases}
\qquad o\in\mathcal O,\ k\in\mathcal K.
\tag{1}
\]

### 3.3.2 Wave descriptors / 波次描述指标

The floor distribution of a wave is measured using both endpoints of every order. For a candidate wave \(W\), let \(p_f(W)\) be the proportion of its \(2|W|\) endpoints located on floor \(f\):

> **中文：** 波次的楼层分布通过每个订单的起点和终点共同衡量。对于候选波次 \(W\)，令 \(p_f(W)\) 表示其 \(2|W|\) 个端点中位于楼层 \(f\) 的比例：

\[
p_f(W)=\frac{1}{2|W|}
\sum_{o\in W}\left[\mathbb I(s_o=f)+\mathbb I(d_o=f)\right],
\qquad f\in\mathcal F,
\tag{2}
\]

where \(\mathbb I(\cdot)\) is the indicator function. Endpoint dispersion is represented by the entropy

> **中文：** 其中，\(\mathbb I(\cdot)\) 为示性函数。端点离散度用以下熵值表示：

\[
C(W)=-\sum_{f\in\mathcal F}p_f(W)\log p_f(W),
\qquad 0\log0=0.
\tag{3}
\]

Here \(\log\) denotes the natural logarithm. Larger \(C\) reflects greater diversity in the endpoint distribution across floor labels, arising from broader support or a more even distribution. It describes how endpoints are distributed among floors; travel distances are determined by the numerical differences between the relevant floor indices.

> **中文：** 此处 \(\log\) 表示自然对数。较大的 \(C\) 表示端点在楼层标签上的分布具有更高的多样性，这可以来自更广的分布范围或更均匀的分布。该指标描述端点如何分布于各楼层；运输距离则由相关楼层索引之间的数值差确定。

Directional imbalance measures the asymmetry between upward and downward order movements. Their counts are

> **中文：** 方向不平衡度衡量订单上行移动与下行移动之间的不对称程度，两类订单的数量分别为：

\[
N^\uparrow(W)=\sum_{o\in W}\mathbb I(d_o>s_o),
\qquad
N^\downarrow(W)=\sum_{o\in W}\mathbb I(d_o<s_o).
\tag{4}
\]

The absolute difference is normalized by the number of cross-floor orders:

> **中文：** 将两类订单数量之差的绝对值除以跨楼层订单总数，得到：

\[
I(W)=
\begin{cases}
\dfrac{|N^\uparrow(W)-N^\downarrow(W)|}
{N^\uparrow(W)+N^\downarrow(W)},
& N^\uparrow(W)+N^\downarrow(W)>0,\\
0, & N^\uparrow(W)+N^\downarrow(W)=0.
\end{cases}
\tag{5}
\]

Thus \(I\in[0,1]\), with zero indicating balanced cross-floor counts or the absence of cross-floor orders, and one indicating movement in only one direction. Same-floor orders do not contribute to either count.

> **中文：** 因此，\(I\in[0,1]\)。取值为零表示跨楼层订单的上、下行数量相同，或不存在跨楼层订单；取值为一表示跨楼层订单仅沿一个方向移动。同层订单不计入任何一类方向数量。

Ready-time dispersion measures how order eligibility is spread within the wave. With \(\bar r_W=|W|^{-1}\sum_{o\in W}r_o\), define

> **中文：** 就绪时间离散度衡量波次内订单获得处理资格的时间分散程度。令 \(\bar r_W=|W|^{-1}\sum_{o\in W}r_o\)，定义：

\[
T(W)=
\begin{cases}
\dfrac{\sqrt{|W|^{-1}\sum_{o\in W}(r_o-\bar r_W)^2}}{\bar r_W},
& \bar r_W>0,\\
0, & \bar r_W=0.
\end{cases}
\tag{6}
\]

Smaller \(T\) indicates more compact ready-time offsets relative to their mean. When all orders are ready at the release epoch, \(T=0\). The resulting descriptor vector is

> **中文：** 较小的 \(T\) 表示相对于均值更集中的就绪时间偏移量。当所有订单均在波次释放时刻就绪时，\(T=0\)。由此得到描述指标向量：

\[
\Phi(W)=\bigl(C(W),I(W),T(W)\bigr).
\tag{7}
\]

### 3.3.3 Structural classes and within-class selection / 结构类别与类内选择

The class construction uses the lower and upper tails of \(C\) and \(I\); \(T\) records temporal variation separately. For descriptor \(X\in\{C,I\}\), let \(Q_u(X)\) denote its empirical \(u\)-quantile over the candidate pool. A common tail probability \(\alpha\) defines four candidate-index sets:

> **中文：** 结构类别由 \(C\) 和 \(I\) 的下尾部与上尾部构建，\(T\) 则单独记录时间差异。对于指标 \(X\in\{C,I\}\)，令 \(Q_u(X)\) 表示其在候选池中的经验 \(u\) 分位数。统一的尾部概率 \(\alpha\) 定义以下四个候选索引集合：

\[
\begin{aligned}
\mathcal K_{\mathrm{HC}}&=\{k\in\mathcal K:C(W^k)\geq Q_{1-\alpha}(C)\},\\
\mathcal K_{\mathrm{LC}}&=\{k\in\mathcal K:C(W^k)\leq Q_\alpha(C)\},\\
\mathcal K_{\mathrm{HI}}&=\{k\in\mathcal K:I(W^k)\geq Q_{1-\alpha}(I)\},\\
\mathcal K_{\mathrm{LI}}&=\{k\in\mathcal K:I(W^k)\leq Q_\alpha(I)\}.
\end{aligned}
\tag{8}
\]

A corner class consists of candidates lying in a tail region of both descriptors. The labels \(\mathrm{HH},\mathrm{HL},\mathrm{LH},\mathrm{LL}\) record the tails of \(C\) and \(I\), respectively, with candidate-index supports

> **中文：** 一个角点类别由在两个指标上均处于某一尾部区域的候选波次组成。标签 \(\mathrm{HH},\mathrm{HL},\mathrm{LH},\mathrm{LL}\) 的第一、第二个字母分别表示 \(C\) 和 \(I\) 所处的尾部，对应候选索引支持集为：

\[
\begin{aligned}
\mathcal K_{\mathrm{HH}}&=\mathcal K_{\mathrm{HC}}\cap\mathcal K_{\mathrm{HI}},&
\mathcal K_{\mathrm{HL}}&=\mathcal K_{\mathrm{HC}}\cap\mathcal K_{\mathrm{LI}},\\
\mathcal K_{\mathrm{LH}}&=\mathcal K_{\mathrm{LC}}\cap\mathcal K_{\mathrm{HI}},&
\mathcal K_{\mathrm{LL}}&=\mathcal K_{\mathrm{LC}}\cap\mathcal K_{\mathrm{LI}}.
\end{aligned}
\tag{9}
\]

The selectable labels form \(\mathcal Q=\{q\in\{\mathrm{HH},\mathrm{HL},\mathrm{LH},\mathrm{LL}\}:\mathcal K_q\neq\varnothing\}\). A class-selection instance requires \(\mathcal Q\neq\varnothing\). Candidates outside all four intersections remain in the candidate pool but outside the corner classes. Because the tail inequalities include their thresholds, quantile ties can produce overlapping supports.

> **中文：** 可选类别标签构成集合 \(\mathcal Q=\{q\in\{\mathrm{HH},\mathrm{HL},\mathrm{LH},\mathrm{LL}\}:\mathcal K_q\neq\varnothing\}\)。类别选择实例要求 \(\mathcal Q\neq\varnothing\)。不属于上述四个交集的候选波次仍保留在候选池中，但不属于角点类别。由于尾部不等式包含阈值处的取值，分位数并列可能造成支持集重叠。

Each selectable class is implemented by uniform sampling over its candidate indices. The fixed within-class distribution is

> **中文：** 每个可选类别通过对其候选索引进行均匀抽样来落实为具体波次。固定的类内分布为：

\[
\nu_q(k)=
\begin{cases}
\dfrac{1}{|\mathcal K_q|}, & k\in\mathcal K_q,\\
0, & k\notin\mathcal K_q,
\end{cases}
\qquad q\in\mathcal Q,\ k\in\mathcal K.
\tag{10}
\]

Selecting class \(q\) therefore leads to a draw \(\kappa\sim\nu_q\) and the release of \(W^\kappa\). The class choice determines the distribution of the released wave, while its within-class sampling rule remains fixed.

> **中文：** 因此，选定类别 \(q\) 后，按照 \(\kappa\sim\nu_q\) 抽取候选索引，并释放波次 \(W^\kappa\)。类别选择决定实际释放波次所服从的分布，类内抽样规则本身保持固定。

## 3.4 Operational evaluation / 运行评价

### 3.4.1 Processing sequence and AMR assignment / 处理序列与 AMR 分配

The evaluator reserves resources order by order. For candidate \(k\), let \(j\in\mathcal J_n=\{1,\ldots,n\}\) index positions in the processing sequence

> **中文：** 评估器逐个订单进行资源预约。对于候选波次 \(k\)，令 \(j\in\mathcal J_n=\{1,\ldots,n\}\) 表示以下处理序列中的位置：

\[
\pi(W^k)=\left(o_1^k,\ldots,o_n^k\right)
=\operatorname{sort}_{o\in W^k}(r_o,\iota_o).
\tag{11}
\]

Orders are sorted by increasing ready-time offset, with ties resolved by increasing immutable order identifier. All evaluators use this sequence. Each order's complete route is reserved before the next order is considered. Reservation order therefore follows \(\pi(W^k)\), while the generated request timestamps need not be globally increasing.

> **中文：** 订单首先按照就绪时间偏移量升序排列，偏移量相同时按照不可变订单标识符升序排列。所有评估器使用同一序列。当前订单的完整路径完成预约后，评估器才处理下一个订单。因此，预约顺序遵循 \(\pi(W^k)\)，但所生成请求的时间戳不必在全局范围内单调递增。

Fix a candidate \(k\), evaluator \(m\), and, where applicable, a random realization \(\xi\). These indices are suppressed on operational state quantities below. Let \(H_a^{j-1}\) and \(G_a^{j-1}\) be AMR \(a\)'s next availability time and associated floor after the first \(j-1\) orders have been reserved, initially \(H_a^0=t_W\) and \(G_a^0=f^0\). Order \(o_j^k\) is assigned to the earliest-available AMR and begins at

> **中文：** 固定候选波次 \(k\)、评估器 \(m\)，以及适用时的随机实现 \(\xi\)，下文在运行状态量中省略这些下标。令 \(H_a^{j-1}\) 和 \(G_a^{j-1}\) 分别表示前 \(j-1\) 个订单完成预约后，AMR \(a\) 的下一可用时刻及其对应楼层，初始值为 \(H_a^0=t_W\) 和 \(G_a^0=f^0\)。订单 \(o_j^k\) 分配给最早可用的 AMR，其开始时刻为：

\[
a_j=\underset{a\in\mathcal A}{\operatorname{lex\,arg\,min}}
(H_a^{j-1},a),
\qquad
t_j^0=\max\{H_{a_j}^{j-1},\,t_W+r_{o_j^k}\}.
\tag{12}
\]

The AMR index resolves equal availability times. The maximum in Equation (12) enforces both resource availability and order readiness.

> **中文：** AMR 索引用于确定可用时刻相同时的分配顺序。式（12）中的最大值同时满足资源可用条件和订单就绪条件。

An elevator request specifies an origin \(g\), a destination \(h\neq g\), and a request time \(t\). Let \(\mathbf S_m\) contain the elevator reservation state. The request updates this state and returns a completion time:

> **中文：** 一次电梯请求由起始楼层 \(g\)、不同于起点的目标楼层 \(h\) 以及请求时刻 \(t\) 构成。令 \(\mathbf S_m\) 包含电梯预约状态，该请求更新状态并返回完成时刻：

\[
(\widehat t,\mathbf S_m^+)
=\mathscr R_m(\mathbf S_m,g,h,t;\xi).
\tag{13}
\]

Within a fixed evaluation, \(\mathcal R_m(g,h,t)\) denotes the returned time \(\widehat t\), with every call replacing \(\mathbf S_m\) by \(\mathbf S_m^+\). The assigned AMR first reaches the order's source and completes pickup:

> **中文：** 在固定的一次评价中，以 \(\mathcal R_m(g,h,t)\) 表示返回时刻 \(\widehat t\)，每次调用后均以 \(\mathbf S_m^+\) 替换 \(\mathbf S_m\)。所分配的 AMR 首先到达订单起始楼层并完成取货：

\[
t_j^S=
\begin{cases}
\mathcal R_m(G_{a_j}^{j-1},s_{o_j^k},t_j^0),
& G_{a_j}^{j-1}\neq s_{o_j^k},\\
t_j^0, & G_{a_j}^{j-1}=s_{o_j^k},
\end{cases}
\qquad
t_j^P=t_j^S+\tau^P.
\tag{14}
\]

It then reaches the destination and completes delivery:

> **中文：** 随后，AMR 到达目标楼层并完成交付：

\[
t_j^D=
\begin{cases}
\mathcal R_m(s_{o_j^k},d_{o_j^k},t_j^P),
& s_{o_j^k}\neq d_{o_j^k},\\
t_j^P, & s_{o_j^k}=d_{o_j^k},
\end{cases}
\qquad
t_j^C=t_j^D+\tau^D.
\tag{15}
\]

Equations (14) and (15) activate an elevator request only when a movement crosses floors. A same-floor order can still require an initial elevator trip if its assigned AMR is on a different floor. Pickup and drop-off advance the AMR clock by their fixed service durations.

> **中文：** 式（14）和式（15）仅在某次移动跨越楼层时触发电梯请求。对于同层订单，如果所分配的 AMR 位于其他楼层，仍可能需要先乘电梯到达取货楼层。取货与交付过程按照各自固定的服务时长推进 AMR 时钟。

After delivery, the assigned AMR becomes available at the destination:

> **中文：** 交付完成后，所分配的 AMR 在目标楼层重新变为可用状态：

\[
H_{a_j}^{j}=t_j^C,\qquad
G_{a_j}^{j}=d_{o_j^k}.
\tag{16}
\]

For every \(a\neq a_j\), \(H_a^j=H_a^{j-1}\) and \(G_a^j=G_a^{j-1}\). Thus each order updates the state of its assigned AMR, and subsequent assignments use the resulting availability times.

> **中文：** 对于所有 \(a\neq a_j\)，均有 \(H_a^j=H_a^{j-1}\) 和 \(G_a^j=G_a^{j-1}\)。因此，每个订单更新其所分配 AMR 的状态，后续分配则使用更新后的可用时刻。

### 3.4.2 Throughput abstraction \(M_1\) / 吞吐能力抽象 \(M_1\)

Evaluator \(M_1\) represents \(E\) elevators of capacity \(c\) by \(Ec\) independent single-request service slots, indexed by \(v\in\mathcal V_1=\{1,\ldots,Ec\}\). Each slot has a next availability time \(B_v\) and a floor \(G_v\) associated with that availability, initially \(B_v=t_W\) and \(G_v=f^0\). A request uses

> **中文：** 评估器 \(M_1\) 将 \(E\) 部容量为 \(c\) 的电梯表示为 \(Ec\) 个相互独立、每次处理一个请求的服务槽，其索引为 \(v\in\mathcal V_1=\{1,\ldots,Ec\}\)。每个服务槽具有下一可用时刻 \(B_v\) 及该时刻对应的楼层 \(G_v\)，初始值为 \(B_v=t_W\) 和 \(G_v=f^0\)。请求选择以下服务槽：

\[
v^\star=\underset{v\in\mathcal V_1}{\operatorname{lex\,arg\,min}}(B_v,v).
\tag{17}
\]

Its completion time is

> **中文：** 该请求的完成时刻为：

\[
\mathcal R_{M_1}(g,h,t)
=\max\{t,B_{v^\star}\}
+\gamma|G_{v^\star}-g|
+\tau^L+\gamma|g-h|+\tau^U.
\tag{18}
\]

Equation (18) combines waiting for availability, empty repositioning to the request origin, loading, travel to the destination, and unloading. The selected slot is updated to \(B_{v^\star}\leftarrow\mathcal R_{M_1}(g,h,t)\) and \(G_{v^\star}\leftarrow h\); all other slots retain their states. Capacity is represented by the number of parallel slots, and each request reserves its own trip.

> **中文：** 式（18）依次包含等待资源可用、空载调位至请求起点、装载、运行至目标楼层以及卸载过程。所选服务槽更新为 \(B_{v^\star}\leftarrow\mathcal R_{M_1}(g,h,t)\) 和 \(G_{v^\star}\leftarrow h\)，其他服务槽状态保持不变。容量通过并行服务槽数量表示，每个请求单独预约一次行程。

### 3.4.3 Co-occupancy evaluator \(M_2\) / 同乘评估器 \(M_2\)

Evaluator \(M_2\) uses \(E\) physical cars, each accommodating at most \(c\) AMRs on a trip. For each car \(e\), the evaluator stores its next availability \(B_e\), associated floor \(G_e\), and latest reserved trip. That trip is described by its origin-destination pair \((\bar s_e,\bar d_e)\), loading-end time \(L_e\), completion time \(D_e\), and reserved occupancy \(P_e\). Initially, \(B_e=D_e=t_W\), \(G_e=f^0\), no trip pair is stored, \(L_e=-\infty\), and \(P_e=0\).

> **中文：** 评估器 \(M_2\) 使用 \(E\) 个实体轿厢，每次行程最多搭载 \(c\) 个 AMR。对于每个轿厢 \(e\)，评估器保存其下一可用时刻 \(B_e\)、对应楼层 \(G_e\) 以及最近一次预约行程。该行程由起讫楼层组合 \((\bar s_e,\bar d_e)\)、装载结束时刻 \(L_e\)、完成时刻 \(D_e\) 和已预约搭载数量 \(P_e\) 描述。初始时，\(B_e=D_e=t_W\)、\(G_e=f^0\)，尚未保存行程起讫组合，且 \(L_e=-\infty\)、\(P_e=0\)。

A request can share a stored trip when its origin and destination match, capacity remains, and it is ready no later than loading ends. The boardable-car set is

> **中文：** 当请求的起讫楼层与已保存行程一致、行程仍有剩余容量，且请求就绪时刻不晚于装载结束时刻时，该请求可以与其他 AMR 同乘。可登梯轿厢集合为：

\[
\mathcal B(g,h,t)=
\{e\in\mathcal E:(\bar s_e,\bar d_e)=(g,h),\ P_e<c,\ t\leq L_e\}.
\tag{19}
\]

If \(\mathcal B(g,h,t)\neq\varnothing\), the lowest-index eligible car is selected:

> **中文：** 若 \(\mathcal B(g,h,t)\neq\varnothing\)，则选择其中索引最小的轿厢：

\[
e^\star=\min\mathcal B(g,h,t),\qquad
\mathcal R_{M_2}(g,h,t)=D_{e^\star},\qquad
P_{e^\star}\leftarrow P_{e^\star}+1.
\tag{20}
\]

The joining request shares the trip's stored completion time, and its other reservation quantities remain unchanged. A request that is ready before loading begins can wait for that trip.

> **中文：** 加入行程的请求共享该行程已保存的完成时刻，行程的其他预约量保持不变。在装载开始之前就绪的请求可以等待该行程。

When \(\mathcal B(g,h,t)=\varnothing\), the request creates a new trip on the earliest-available car, with equal availability resolved by car index:

> **中文：** 当 \(\mathcal B(g,h,t)=\varnothing\) 时，请求在最早可用的轿厢上建立新行程；多个轿厢可用时刻相同时，按照轿厢索引确定选择：

\[
e^\star=\underset{e\in\mathcal E}{\operatorname{lex\,arg\,min}}(B_e,e).
\tag{21}
\]

Using the car's pre-update state, the new loading-end and completion times are

> **中文：** 利用该轿厢更新前的状态，新行程的装载结束时刻和完成时刻分别为：

\[
\begin{aligned}
L_{e^\star}&=\max\{t,B_{e^\star}\}
+\gamma|G_{e^\star}-g|+\tau^L,\\
D_{e^\star}&=L_{e^\star}+\gamma|g-h|+\tau^U.
\end{aligned}
\tag{22}
\]

The evaluator returns \(\mathcal R_{M_2}(g,h,t)=D_{e^\star}\) and updates the car's reservation record:

> **中文：** 评估器返回 \(\mathcal R_{M_2}(g,h,t)=D_{e^\star}\)，并更新该轿厢的预约记录：

\[
B_{e^\star}\leftarrow D_{e^\star},\qquad
G_{e^\star}\leftarrow h,\qquad
(\bar s_{e^\star},\bar d_{e^\star})\leftarrow(g,h),\qquad
P_{e^\star}\leftarrow1.
\tag{23}
\]

Equations (21) to (23) reserve successive trips without overlapping their use of the same car. The new trip replaces that car's stored trip record, and subsequent requests test Equation (19) against the latest record of each car. Here \(G_e\) is the floor reached at the next availability time, and \(P_e\) counts AMRs reserved on the stored trip.

> **中文：** 式（21）至式（23）依次预约行程，同一轿厢的不同预约行程在资源占用时间上不重叠。新行程替换该轿厢原先保存的行程记录，后续请求依据各轿厢的最新记录检查式（19）。其中，\(G_e\) 是轿厢在下一可用时刻到达的楼层，\(P_e\) 则统计已预约加入所存行程的 AMR 数量。

### 3.4.4 Stochastic evaluator \(M_3\) / 随机评估器 \(M_3\)

Evaluator \(M_3\) retains the car-assignment, boarding, and capacity rules of \(M_2\). Each new trip receives four independent phase multipliers \(Z^{\mathrm{rep}},Z^{\mathrm{load}},Z^{\mathrm{trav}},Z^{\mathrm{unload}}\), corresponding to empty repositioning, loading, loaded travel, and unloading. Multipliers are independent across trips and satisfy

> **中文：** 评估器 \(M_3\) 保留 \(M_2\) 的轿厢分配、登梯和容量规则。每个新行程获得四个相互独立的阶段乘数 \(Z^{\mathrm{rep}},Z^{\mathrm{load}},Z^{\mathrm{trav}},Z^{\mathrm{unload}}\)，分别对应空载调位、装载、载货运行和卸载。不同行程之间的乘数也相互独立，并满足：

\[
\log Z\sim\mathcal N\left(-\frac{\sigma^2}{2},\sigma^2\right),
\qquad \mathbb E[Z]=1.
\tag{24}
\]

The loading-end and completion times of a new trip become

> **中文：** 新行程的装载结束时刻和完成时刻相应变为：

\[
\begin{aligned}
L_{e^\star}&=\max\{t,B_{e^\star}\}
+\gamma|G_{e^\star}-g|Z^{\mathrm{rep}}
+\tau^L Z^{\mathrm{load}},\\
D_{e^\star}&=L_{e^\star}
+\gamma|g-h|Z^{\mathrm{trav}}
+\tau^U Z^{\mathrm{unload}}.
\end{aligned}
\tag{25}
\]

The reservation update follows Equation (23). Both a newly reserved request and a joining request return \(\mathcal R_{M_3}(g,h,t)=D_{e^\star}\). Requests joining the same trip share this stored completion time, with no additional phase draws. Waiting follows from resource availability, while pickup and drop-off durations remain fixed.

> **中文：** 预约状态按照式（23）更新。新预约请求和加入现有行程的请求均返回 \(\mathcal R_{M_3}(g,h,t)=D_{e^\star}\)。加入同一行程的请求共享这一已保存的完成时刻，不额外抽取阶段乘数。等待时间由资源可用性决定，取货和交付时长保持固定。

Let \(\xi\in\Xi\) represent the collection of phase multipliers used in a wave evaluation, where \(\Xi\) is the realization space. The phase-noise source is independent of the within-class candidate draw \(\kappa\). Conditional on a candidate and a realization, the reservation relations determine all order completion times.

> **中文：** 令 \(\xi\in\Xi\) 表示一次波次评价所使用的阶段乘数集合，其中 \(\Xi\) 为随机实现空间。阶段噪声来源与类内候选索引抽样 \(\kappa\) 相互独立。在候选波次和随机实现给定后，预约关系确定全部订单的完成时刻。

### 3.4.5 Wave completion measure / 波次完成指标

Restoring the candidate, evaluator, and realization indices gives the order completion time \(t^C_{jkm}(\xi)\). Wave makespan measures elapsed time from release until the last selected order is delivered:

> **中文：** 恢复候选波次、评估器和随机实现下标后，得到订单完成时刻 \(t^C_{jkm}(\xi)\)。波次完工期衡量从释放至最后一个所选订单完成交付所经过的时间：

\[
Y_{km}(\xi)
=C_{\max}(W^k;m,\xi)
=\max_{j\in\mathcal J_n}t^C_{jkm}(\xi)-t_W.
\tag{26}
\]

For \(M_1\) and \(M_2\), the outcome is deterministic and the argument \(\xi\) is omitted. Under \(M_3\), Equation (26) defines the makespan for one phase-time realization.

> **中文：** 对于 \(M_1\) 和 \(M_2\)，结果为确定值，省略参数 \(\xi\)。在 \(M_3\) 下，式（26）给出一次阶段时长随机实现对应的波次完工期。

## 3.5 Selection formulations / 选择模型

### 3.5.1 Selection variables / 选择变量

The class formulation chooses a structural class, while the candidate benchmark chooses a particular wave. Table 3.3 lists their variables. Operational assignments and reservation times are supplied by Section 3.4 and determine the performance coefficients used in these formulations.

> **中文：** 类别模型选择一个结构类别，候选波次基准则选择一个具体波次。表 3.3 列出两种模型的变量。运行分配和预约时刻由第 3.4 节给出，并据此确定选择模型使用的绩效系数。

Table 3.3. Variables in the class and candidate formulations.

> **中文：** 表 3.3 类别模型与候选波次模型中的变量。

| Variable / 变量 | Domain / 取值域 | Definition / 定义 |
|---|---|---|
| \(y_q\) | \(\{0,1\}\) | 1 if structural class \(q\) is selected / 选择结构类别 \(q\) 时取 1 |
| \(\eta^Q\) | \(\mathbb R_+\) | auxiliary upper bound on the selected class's medians across evaluators / 所选类别在各评估器下完工期中位数的辅助上界 |
| \(z_k\) | \(\{0,1\}\) | 1 if candidate wave \(k\) is selected / 选择候选波次 \(k\) 时取 1 |
| \(x_o\) | \(\{0,1\}\) | linked indicator that order \(o\) belongs to the selected candidate / 订单 \(o\) 属于所选候选波次的联动指示变量 |
| \(\eta^C\) | \(\mathbb R_+\) | auxiliary upper bound on the selected candidate's scores across evaluators / 所选候选波次在各评估器下得分的辅助上界 |

### 3.5.2 Robust structural-class selection / 鲁棒结构类别选择

The performance of a class is the median makespan induced by its fixed release distribution. When the median is non-unique, we use the midpoint of its median interval. For \(q\in\mathcal Q\) and \(m\in\mathcal M\), define

> **中文：** 一个类别的绩效由其固定释放分布所产生的波次完工期中位数衡量。中位数不唯一时，取中位数区间的中点。对于 \(q\in\mathcal Q\) 和 \(m\in\mathcal M\)，定义：

\[
\mu_{qm}^{0.5}
=\operatorname{Med}_{\kappa\sim\nu_q,\,\xi}
\left[Y_{\kappa m}(\xi)\right].
\tag{27}
\]

For \(M_1\) and \(M_2\), variation in Equation (27) arises from the candidate draw. Under \(M_3\), the distribution includes both candidate variation and phase-time noise. The median is taken over this joint outcome distribution.

> **中文：** 对于 \(M_1\) 和 \(M_2\)，式（27）中的差异来自候选波次抽样。在 \(M_3\) 下，分布同时包含候选波次差异和阶段时间噪声，中位数针对这一联合结果分布计算。

Let \(\mathcal M_D=\{M_1,M_2\}\) be the deterministic evaluator family. The robust class decision minimizes the larger of its two median makespans:

> **中文：** 令 \(\mathcal M_D=\{M_1,M_2\}\) 表示确定性评估器族。鲁棒类别决策最小化其在两个评估器下完工期中位数中的较大值：

\[
q^\star\in
\arg\min_{q\in\mathcal Q}
\max_{m\in\mathcal M_D}\mu_{qm}^{0.5}.
\tag{28}
\]

An equivalent binary selection formulation is

> **中文：** 等价的二元选择模型为：

\[
\begin{aligned}
\min_{y,\eta^Q}\quad & \eta^Q\\
\text{s.t.}\quad
& \sum_{q\in\mathcal Q}y_q=1,\\
& \eta^Q\geq\sum_{q\in\mathcal Q}\mu_{qm}^{0.5}y_q,
&& m\in\mathcal M_D,\\
& y_q\in\{0,1\},
&& q\in\mathcal Q,\\
& \eta^Q\geq0.
\end{aligned}
\tag{29}
\]

The first constraint selects exactly one nonempty class. The score constraints bound \(\eta^Q\) below by that class's median under each evaluator. Minimization makes \(\eta^Q\) equal to the largest of those medians. The selected class is implemented using Equation (10), and \(M_3\) evaluates its stochastic performance.

> **中文：** 第一条约束选择且仅选择一个非空类别。得分约束要求 \(\eta^Q\) 不小于该类别在各评估器下的完工期中位数。最小化目标使 \(\eta^Q\) 等于这些中位数中的最大值。所选类别按照式（10）落实为具体波次，\(M_3\) 则用于评价其随机绩效。

### 3.5.3 Candidate-wave benchmarks / 候选波次基准

Direct candidate selection uses the deterministic scores

> **中文：** 直接选择候选波次时，采用以下确定性得分：

\[
\ell_{km}=C_{\max}(W^k;m),
\qquad k\in\mathcal K,\ m\in\mathcal M_D.
\tag{30}
\]

For a prespecified nonempty family \(\mathcal M_R\subseteq\mathcal M_D\), the finite-pool benchmark is

> **中文：** 对于预先指定的非空评估器族 \(\mathcal M_R\subseteq\mathcal M_D\)，有限候选池基准为：

\[
\min_{k\in\mathcal K}\max_{m\in\mathcal M_R}\ell_{km}.
\tag{31}
\]

Setting \(\mathcal M_R=\{m\}\) gives the single-evaluator pool optimum, while \(\mathcal M_R=\mathcal M_D\) gives the two-evaluator robust benchmark. In both cases, the search domain is the given finite candidate pool. The corresponding selection formulation is

> **中文：** 令 \(\mathcal M_R=\{m\}\) 得到单一评估器下的候选池最优值，令 \(\mathcal M_R=\mathcal M_D\) 则得到两个评估器下的鲁棒基准。两种情况下的搜索范围均为给定的有限候选波次池，对应选择模型为：

\[
\begin{aligned}
\min_{z,x,\eta^C}\quad & \eta^C\\
\text{s.t.}\quad
& \sum_{k\in\mathcal K}z_k=1,\\
& x_o=\sum_{k\in\mathcal K}\delta_{ok}z_k,
&& o\in\mathcal O,\\
& \sum_{o\in\mathcal O}x_o=n,\\
& \eta^C\geq\sum_{k\in\mathcal K}\ell_{km}z_k,
&& m\in\mathcal M_R,\\
& z_k\in\{0,1\},
&& k\in\mathcal K,\\
& x_o\in\{0,1\},
&& o\in\mathcal O,\\
& \eta^C\geq0.
\end{aligned}
\tag{32}
\]

The first constraint selects one candidate. The membership equalities link \(x_o\) to that candidate's order set, and the cardinality equality records the fixed wave size. Because every candidate already contains \(n\) orders, this cardinality equality is implied by candidate selection and membership. The score constraints and objective then minimize the selected candidate's worst score over \(\mathcal M_R\).

> **中文：** 第一条约束选择一个候选波次。归属等式将 \(x_o\) 与该候选波次的订单集合联动，数量等式记录固定波次规模。由于每个候选波次已经包含 \(n\) 个订单，该数量等式可由候选选择与归属关系推出。得分约束与目标函数共同最小化所选候选波次在 \(\mathcal M_R\) 上的最不利得分。
