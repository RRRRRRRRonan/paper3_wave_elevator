---
title: "Abstract v1.0 (condensed; critical-review fixes + filled quantitative findings + Proposition 2; no em-dashes; bilingual)"
parent: "Wave Release Coordination under Vertical Resource Constraints in Multi-Story AMR Warehouses"
date: 2026-06-05
status: "v1.0 (rev. condensed, no em-dash, bilingual) - ready to paste into the manuscript Abstract; supersedes the PDF Abstract with the [INSERT] placeholder"
changes: >
  (1) Fills the [INSERT KEY QUANTITATIVE FINDINGS] placeholder with real Phase-5 numbers.
  (2) Honest PASS (Hedge) / PARTIAL (Bound-and-Gap) split, no unqualified "Both tools are validated".
  (3) Introduces Phi before H_up/M_Phi; qualifier-locked novelty naming Qin et al. (2024).
  (4) Bound-and-Gap name justified by bounds + gap; M_Phi stated as the predict-then-optimize decision loss (the SPO objective; the formal term "SPO regret" stays in the Theorem 1 statement in section 4), delegable to existing methods.
  (5) Hedge Rule framed as ranking wave-structures under one dominant reference model (Proposition 2 conditional dominance).
  (6) No em-dashes (whole-paper rule); Chinese version follows each English paragraph, symbol-free.
  (7) Condensed from the long v1.0 draft (~470 to ~320 English words) on author request; substance and numbers retained.
source_numbers: "v0_5_phase5_blockA.json, v0_5_phase5_blockC.json, v0_5_phase5_supp.json"
---

# Abstract (v1.0, condensed)

*English paragraph first, Chinese version directly below it.*

---

In multi-story fulfillment warehouses, autonomous mobile robots (AMRs) are
confined to individual floors and share a few freight elevators, so elevator
capacity is the primary bottleneck. The first tactical decision, wave
composition (which orders to release together), largely fixes the makespan
before any AMR moves, yet prior work has not treated it as a decision variable
coupled to shared vertical transport: planar order-batching optimizes wave size
on a single floor (e.g., Qin et al., 2024), and multi-tier fulfillment confines
transport within a tier. We formalize this gap as the wave-release coordination
problem under vertical resource constraints, and address it with a two-stage
scheduler: a tactical stage composes each wave, and an operational stage
dispatches the AMRs that deliver its orders through the shared elevators.

在多层订单履行仓库中，AMR 被限制在各自楼层并共享少量货运电梯，因此电梯运力是
主要瓶颈。第一个战术决策是波次构成，即哪些订单一起放行，它在任何 AMR 行动之前
就基本决定了 makespan；但已有工作尚未把它当作与共享垂直运输相耦合的决策变量：
平面订单分批只在单层上优化波次规模（如 Qin et al., 2024），多层履行则把运输限制
在单一层内。我们将这一空白形式化为垂直资源约束下的波次放行协调问题，并用一个两阶段调度器
来处理：战术阶段负责构成每个波次，操作阶段则调度 AMR 经由共享电梯把波次中的
订单送达。

---

We hold the operational stage fixed and study the tactical stage with two
analytical tools, both built on a three-dimensional representation `Φ` of each
wave: its vertical spread, directional imbalance, and temporal clustering. The first, the Bound-and-Gap
decomposition, is diagnostic: it splits the value of wave composition into a
structural ceiling `H_up` that no policy on `Φ` can recover and a recoverable
slack `M_Φ`, and identifies `M_Φ` as a standard predict-then-optimize loss that
existing methods can close. The second, the Model-Dominance Hedge Rule, is
prescriptive: a closed-form rule that selects which wave-structure to release
from without identifying the true elevator model or solving a robust
optimization program. Under a conditional dominance result that we establish,
this simplest rule is provably the distributionally-robust optimum. The two tools act on the same representation and are complementary: the
decomposition measures what a wave-structure choice is worth and how much of it
is reachable, while the Hedge Rule selects the robust one.

我们固定操作阶段，用两个分析工具来研究战术阶段；这两个工具都建立在对每个波次的
一个三维表示之上：垂直分散度、方向不平衡度、时间聚集度。第一个是 Bound-and-Gap 分解，它是诊断性
的：把波次构成的价值拆分为任何策略都无法回收的结构性天花板与可被回收的余量，并
指出这块余量就是"预测后优化"（Smart-Predict-then-Optimize）框架下的决策损失，可
委托给已有方法来回收。第二个是 Model-Dominance Hedge Rule，它是处方性的：一条
闭式规则，在无需识别真实电梯模型、也无需求解任何鲁棒优化程序的前提下选出应从
哪一类波次结构放行。在我们所确立的一个带条件支配性结果之下，这条最简单的规则
可被证明就是分布鲁棒意义下的最优解。
这两个工具作用于同一个表示且彼此互补：分解衡量"某一波次结构选择值多少、其中
多少可被回收"，而 Hedge Rule 则选出稳健的那一个。

---

A pre-registered study of 106,800 simulations reports each tool's outcome as it stands, and the two differ: the
Hedge Rule passes every gate (per-wave dominance 99.2%, matching the
distributionally-robust optimum), while the Bound-and-Gap identities hold
exactly (72/72) and its resolution gate, met in 79% (a partial pass), fails only
where the gap is genuinely small. The binding limitation on makespan is
therefore predominantly capacity-side (the structural ceiling about 72% of
wave-design value), and the tools' value is to identify, regime by regime, when
wave composition is worth pursuing and when the lever is capacity instead.

一项预注册研究（共 106,800 次仿真）如实报告两个工具各自的结论，两者并不相同：Hedge Rule 通过全部门槛
（逐波次支配序 99.2%，且与分布鲁棒最优解一致），而 Bound-and-Gap 的恒等关系精确
成立（72/72），其分辨门槛在 79% 达到（部分通过），未达到之处恰是波次设计价值本就
很小的子单元。因此 makespan 的约束性限制主要在容量侧（结构性天花板约占波次设计
价值的 72%）；而这两个工具的价值，正在于逐场景指出何时值得投入波次构成、何时
真正的杠杆是运力。
