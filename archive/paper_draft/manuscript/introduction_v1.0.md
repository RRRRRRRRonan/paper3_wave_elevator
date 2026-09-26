---
title: "Introduction (§1), v1.0 reconstruction (bilingual: Chinese then English; structure unified with the Abstract; explicit C1/C2/C3)"
parent: "Wave Release Coordination under Vertical Resource Constraints in Multi-Story AMR Warehouses"
date: 2026-06-19
status: "v1.0 reconstruction. Mirrors the converged Abstract beat-for-beat (problem and gap -> two-stage decision and two tools -> contributions), then states C1/C2/C3 explicitly. Terminology per paper_draft/TERMINOLOGY.md."
notes: >
  Citation form: the PDF body's "Nicolas et al. (2018)" is a parsing error for Lenoble, N., Frein, Y., & Hammami, R. (2018, EJOR); corrected to "Lenoble et al., 2018" here.
  Citation years use the formal journal year (Elmachtoub & Grigas 2022; Mohajerin Esfahani & Kuhn 2018).
  No em-dashes; the Chinese version is symbol-free (Phi/H_up/M_Phi rendered in words); method names kept.
---

# Section 1. Introduction (v1.0)

## 中文版

电子商务与次日达需求把配送中心推向土地紧张、难以扩张的城市密集区。运营商越来越
多地采用多层订单履行建筑:楼层垂直堆叠,自主移动机器人(AMR)在每层处理水平
搬运,少数货运电梯连接各层。系统的主要瓶颈已从楼面空间或机队规模转移到电梯
运力,AMR 常常在等电梯时空闲。

运营商以"波次(wave)"放行订单来缓解这种拥塞:在一个短暂的放行窗口内,一批
选定的订单被同时投放。每个波次的构成,即把哪些订单捆在一起,直接决定了电梯需要
服务多少次垂直转移、朝哪些方向、以及在时间上多集中;因此它在任何 AMR 行动之前
就设定了下游调度问题的难度。当前实践中,波次构成多凭启发式规则(按目的楼层、按
承运截止、或按到达顺序)决定。然而波次层恰恰是缓解垂直瓶颈最廉价的着力点,因为
对已生成的订单重新分组既不改变布局、也不改变机队规模。

波次构成、多层部署、灵活 AMR 机队、共享电梯运力这四个要素,以往大多被分开研究。
最接近的先例要么把电梯当作固定波次内容下的约束(Chakravarty et al., 2025),要么
在单个垂直升降模块(VLM)内部做分批(Lenoble et al., 2018);多层机器人移动履行
系统(RMFS)的工作
通过把穿梭车限制在单层来回避耦合(Wu et al., 2024);平面 AMR 的工作只在单层上
优化波次基数(Qin et al., 2024)。这些先例各自通过限制设定来绕开这一耦合:固定波次
内容,或把运输限制在单一器件或单一楼层。但在我们研究的一般设定下(一支灵活 AMR
机队共享建筑级货梯,且波次构成本身就是决策),这一耦合便分不开:波次构成在机队
调度器行动之前就固定了电梯的行程分布(多少次垂直转移、朝哪些方向、多集中),
因此战术层与操作层无法各自单独优化而不丢失瓶颈交互。我们把这四个要素的交集形式化为"垂直资源
约束下的波次放行协调问题",第 2 节详述各先例。

该问题自然分为两个阶段:战术阶段构成每个波次,操作阶段则调度 AMR 经由共享电梯
把订单送达。我们固定操作阶段,集中研究战术阶段,为它提出两个互补的分析工具,
二者都建立在对每个波次的一个三维表示之上(垂直分散度、方向不平衡度、时间
聚集度)。两个结构性观察驱动这两个工具:其一,波次结构能带来的价值随场景而变。
共享电梯是瓶颈:在某些场景下,makespan 主要由电梯的运力决定,只能靠增加运力来
缓解;在另一些场景下,它更取决于波次如何构成,于是放行策略就能缓解。也就是说,
这份价值由两部分组成:一部分由运力决定、任何放行策略都无法回收,另一部分则是
可回收的余量,一个用好三维表示的放行策略就能把它收回(其间操作阶段的 AMR 调度
始终保持固定)。两者孰大孰小随场景而变,因此波次构成能带来多少价值,必须先
度量、再去争取。其二,运营者虽不知道真实电梯模型,但在几乎每个波次上,这几个
候选模型给出的 makespan 高低次序都一样:其中最保守的那个,即真实共占批处理,其
makespan 不小于其余模型,因而是最慢的、也即最坏情形,可作为一个保守的参照基准。
这一次序对每个波次都单独成立,而非只在平均意义上成立。因此只需拿这个参照基准
逐一衡量候选波次,挑出在它之下 makespan 最短的那一类波次结构。这样选出的结构
便是稳健之选:我们证明它就是分布鲁棒意义下的最优解,并带有一个可计算的最坏损失
上界。这两
个工具作用于同一个决策,即该从哪一类波次结构放行:第一个工具衡量这个选择值多少、
其中多少能由放行策略回收,第二个工具用上述参照基准选出稳健的那一个。

本文的贡献有三。

**(C1)问题形式化。** 我们把垂直资源约束下的波次放行协调问题形式化为一个两阶段
调度:战术阶段构成波次,操作阶段经由共享电梯把放行的订单送达,两阶段通过共享
电梯运力相耦合。以往研究多以简化设定回避这一耦合,
本形式化则将它显式纳入模型。

**(C2)方法。** 我们在波次构成的三维表示上提出两个分析工具。第一个是 Bound-and-Gap
分解(诊断性),它把波次设计的价值拆分为两部分:任何在该表示上操作的策略都无法
回收的结构性天花板,以及更好的策略仍可回收的余量;我们证明(定理 1)这块余量
恰好是"先预测、再优化"意义下的决策损失,也就是 Smart-Predict-then-Optimize 文献
研究的对象(Elmachtoub and Grigas, 2022),因而可直接交给已有方法来回收。第二个是 Model-Dominance Hedge Rule
(处方性),它是一条闭式规则,在无需识别真实电梯模型、也无需求解任何鲁棒优化程序的
前提下选出应从哪一类波次结构放行;我们证明(定理 2),在一个我们所确立的、带条件
的逐波次支配性结果(命题 2)之下,这条最简单的规则与 Wasserstein 分布鲁棒优化的
最优解完全一致
(Mohajerin Esfahani and Kuhn, 2018),并附带一个可计算的最坏损失上界。两个工具
作用于同一个表示且彼此互补:分解衡量某一选择值多少、其中多少可被回收,而 Hedge Rule 则选出稳健的那一个。

**(C3)经验洞见。** 我们以一项预注册的大规模仿真研究(18 种配置、共 106,800 次
仿真)评估两个工具,如实报告各自的结论;两者并不相同。Model-Dominance Hedge Rule 通过全部
预注册门槛:逐波次支配序在 99.2% 的波次上成立(最差单元 96.0%),并在每趟运力取
2 到 5 各值时都成立;其所选结构在每种配置下都与 Wasserstein 分布鲁棒最优解一致。
Bound-and-Gap 的两个恒等关系在全部 72 个子单元上精确成立,其中容量侧的结构性
天花板约占平均价值的 72%,主导较小的策略可回收余量;统计分辨门槛在 79% 的子单元
上达到(部分通过,差一个子单元),而未达到之处恰是价值本就很小的子单元,即该分解
在价值不可忽略之处都能将其分辨出来。对这些仓库而言,makespan 的约束性限制因此
主要在容量侧。而这正是这两个工具的管理价值:它们能逐场景告诉运营者,何时值得
投入更精细的波次构成、何时真正的杠杆其实是运力或分区细化,从而避免在波次构成
回收不了价值的地方白费力气。

第 2 节回顾相关文献;第 3 节形式化问题;第 4 节发展两个工具;第 5 节给出计算
实验;第 6 节总结。

---

## English version

The growth of e-commerce and the demand for next-day delivery have pushed
distribution centers into dense urban areas where land is scarce and expansion
is constrained. Operators increasingly turn to multi-story fulfillment
buildings: floors stacked vertically, with autonomous mobile robots (AMRs)
handling horizontal movement on each floor and a few freight elevators
connecting them. The primary bottleneck has shifted from floor space or fleet
size to elevator capacity, and AMRs often idle while waiting for an elevator.

Operators relieve this congestion by releasing orders in waves: within a short
release window, a selected subset of orders is dispatched simultaneously. The
composition of each wave, that is, which orders to bundle, directly determines
how many vertical transitions the elevators must serve, in which directions, and
with what temporal stagger; it therefore sets the difficulty of the downstream
dispatch problem before any AMR moves. In current practice, wave composition is
set heuristically, by destination floor, carrier cutoff, or arrival order. Yet
the wave layer is the cheapest place to relieve a vertical bottleneck, because
re-batching already-released orders changes neither the layout nor the fleet
size.

Four elements, namely wave composition, multi-story deployment, flexible AMR
fleets, and shared-elevator capacity, have largely been studied in isolation.
The closest precedents treat the lift as a constraint under fixed wave content
(Chakravarty et al., 2025) or batch orders inside a single vertical lift module (VLM) (Lenoble et al., 2018);
multi-story Robotic Mobile Fulfillment System (RMFS) work avoids the coupling by
confining shuttles to a tier (Wu et al., 2024); planar AMR work optimizes wave
cardinality on a single floor (Qin et al., 2024). Each of these precedents sidesteps the
coupling by restricting the setting: fixing the wave content, or confining
transport to a single device or a single tier. In the general setting we study,
however, where a flexible AMR fleet shares building-wide elevators and wave
composition is itself a decision, the coupling cannot be separated: wave
composition fixes the elevator trip distribution (how many vertical transitions,
in which directions, with what stagger) before the fleet scheduler acts, so the
tactical and operational layers cannot be optimized in isolation without losing
the bottleneck interaction. We formalize the intersection of
these four elements as the wave-release coordination problem under vertical
resource constraints; Section 2 details the precedents.

The problem decomposes naturally into two stages: a tactical stage composes each
wave, and an operational stage dispatches the AMRs that deliver its orders
through the shared elevators. We hold the operational stage fixed and study the
tactical stage with two complementary analytical tools, both built on a
three-dimensional representation `Φ = (C, I, T)` of each wave: its vertical
spread `C`, directional imbalance `I`, and temporal clustering `T`. Two
structural features motivate the tools. First, the value that wave structure can
deliver varies across operating regimes. The shared elevator is the bottleneck:
in some regimes makespan is controlled by the elevator's capacity and can be
relieved only by adding capacity, while in others it depends on how waves are
composed, so the wave-release policy can relieve it. The value therefore has two
parts. One is fixed by capacity, and no wave-release policy can recover it. The
other is slack that a `Φ`-informed wave-release policy can recover, the
operational dispatch being held fixed. Which part dominates shifts across
regimes, so the value of composing waves must be measured before it is pursued. Second, the
operator does not know which elevator model is true, yet on almost every wave the
candidate models rank the makespans in the same order. Among the candidate
models the most conservative, true co-occupancy batching, is weakly larger than
the others, hence the slowest, and serves as a worst-case reference. This
ordering holds wave by wave, not only on average. The operator can therefore
score the candidate waves against that single reference and release the one that
minimizes makespan under it. That choice is robust: we prove it is the
distributionally-robust optimum, with a computable worst-case-loss bound. The two tools act on the same decision (which
wave-structure to release): the first measures how much that choice is worth and
how much of it a wave-release policy can recover, and the second uses the
reference model to select the robust one.

This paper makes three contributions.

**(C1) Problem formulation.** We formalize the wave-release coordination problem
under vertical resource constraints as a two-stage scheduler in which a tactical
stage composes waves and an operational stage delivers the released orders
through shared elevators, the two stages coupled through shared elevator
capacity. Prior work mostly sidesteps this coupling by simplifying the setting; our
formulation models it explicitly.

**(C2) Methodology.** We develop two analytical tools on the structured
representation `Φ`. The first, the Bound-and-Gap decomposition (diagnostic),
splits the value of wave design into a structural ceiling `H_up` that no policy
acting on `Φ` can recover and a recoverable slack `M_Φ`; we prove (Theorem 1)
that `M_Φ` is exactly a predict-then-optimize decision loss, the object studied
as Smart-Predict-then-Optimize regret (Elmachtoub and Grigas, 2022), so it can
be recovered with existing methods. The second, the
Model-Dominance Hedge Rule (prescriptive), is a closed-form rule that selects
which wave-structure to release from without identifying the true elevator model or solving a robust
optimization program; we prove (Theorem 2) that, under a conditional per-wave
dominance result we establish (Proposition 2), this simplest rule coincides
exactly with the Wasserstein
distributionally-robust optimum (Mohajerin Esfahani and Kuhn, 2018) and carries
a computable worst-case-loss bound. The two tools act on the same representation
and are complementary: the decomposition measures what a wave-structure choice
is worth and how much is recoverable, while the Hedge Rule selects the robust
one.

**(C3) Validated insights.** We evaluate both tools in a pre-registered,
large-scale simulation study (106,800 simulations across 18 configurations),
and report each tool's outcome as it stands; the two differ. The
Model-Dominance Hedge Rule passes
every pre-registered gate: per-wave dominance holds in 99.2% of waves (96.0% in
the worst cell) and across per-trip capacities `c ∈ {2,3,4,5}`, and its chosen
structure matches the Wasserstein-DRO optimum in every configuration. The
Bound-and-Gap identities hold exactly in all 72 sub-cells, with the
capacity-side ceiling `H_up` accounting for about 72% of the mean value and
dominating the smaller recoverable slack `M_Φ`; the statistical-resolution gate
is met in 79% of sub-cells (a partial pass, one sub-cell short), and the
unresolved sub-cells are those where the value is genuinely small, so the
decomposition resolves wave-design value wherever that value is substantial. For
these warehouses, the binding limitation on makespan is therefore predominantly
capacity-side. This is precisely the tools' managerial payoff: they tell an
operator, regime by regime, when smarter wave composition is worth the effort and
when the lever is instead capacity or a finer partition.

Section 2 reviews the related literature. Section 3 formulates the problem.
Section 4 develops the two tools. Section 5 presents the computational
experiments. Section 6 concludes.
