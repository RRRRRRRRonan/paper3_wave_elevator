---
title: "Section 4 completion draft: remainder of 4.3.2, 4.4 (IJPR numbering), 4.5 (revised), 4.6"
date: 2026-09-26
status: "DRAFT for author review, revision 2 (after two independent reviews on 2026-09-26). Inserted into Methodology.docx as tracked changes (W-3), after the paragraph that opens Section 4.3.2. Single source for the Word text: the builder reads the English paragraphs and equations of this file."
numbering: "MASTER_REVISION_BY_SECTION.md §00.5 as decided on 2026-09-26: Theorem 2 -> Corollary 1(a), candidate-level reduction -> Corollary 1(b), Corollary 2 kept (quantile bound moved out of Section 4), Corollary 3 -> Remark 2, Corollary 4 deleted. In Section 4.2, Proposition 2 -> Remark 1 and Theorem 1 with Corollary 1 -> Proposition 2 (edited in place in Word). Proposition 3 keeps its label until TH-1."
sources: "revision_2026-09-02/SECTION_4_METHODOLOGY.md §4.3.2 and §4.4 (equations 47 to 58); week3/SECTION_4_5_GSV_draft.md; STORY_CONTRACT.md §3, §6, §7; master §0.2, §0.3, §2.4; TERMINOLOGY.md (batch overtaking, adverse repositioning, abstraction bias B); AMEND-2026-07-08-B11 (census class and reporting rule 4) and b11_conj1_census.json; AMEND-2026-07-08-B item B-1 with its second addendum (iv) and b1_matched_assignment.json; Phase 6 protocol §5, §7, §9; Fu, Li and Zhang (2024), MSOM 26(5): 1962-1977, doi 10.1287/msom.2023.0159 (Crossref, checked 2026-09-26)."
---

# 4.3.2 (continued) Reversal mechanisms and class-level implications / 排序反转机制及类别层面的推论（续）

<!-- The Word file already holds the heading and the first paragraph of Section 4.3.2, which contains the setup and both examples ("Two small instances isolate ..." to "... the unfavorable repositioning distance in (d)."). The text below continues it. -->

The examples show why (c) and (d) enter the sufficient conditions of Theorem 1: each example violates exactly one of them and reverses the ordering, so neither condition can be dropped. Conversely, a violated condition need not produce a reversal. The first example is a batch overtaking, in which a shared \(M_2\) trip overtakes its corresponding \(M_1\) requests; the second is an adverse repositioning. When AMR assignments differ, request alignment itself must also be examined.

> **中文：** 两个实例说明了条件（c）与（d）为何进入定理 1 的充分条件：每个实例恰好违反其中一个条件，并且都出现了排序反转，因此两个条件都不能去掉。反过来，条件被违反并不一定导致反转。第一个实例是批次超越（共享的 \(M_2\) 行程超越了对应的 \(M_1\) 请求），第二个实例是不利调位。若 AMR 指派不同，还需另行检查请求是否对应。

Two registered checks [NS] concern whether these two mechanisms are exhaustive. An exhaustive enumeration of 1,000,800 instances with two or three orders, together with a seeded sample of 150,000 four-order instances (six floors, car capacity 2, cross-floor orders, one or two elevators, AMR counts and ready offsets on fixed grids; Appendix B), found no makespan reversal among instances that satisfy (a) to (d); this is a certification on that class, not a proof. On the 6,000 matched-wave draws of the preregistered ordering test (publication scale, counted with multiplicity; Section 5.2), replayed with common AMR assignments, each of the 20 reversals violates (c) or (d): 18 violate (c), and in the other 2, (c) holds and (d) fails.

> **中文：** 两项已登记的检查 [NS] 考察这两个机制是否穷尽了反转的来源。对 1,000,800 个两单或三单实例的穷举，加上 150,000 个四单实例的固定种子抽样（六层楼、轿厢容量 2、跨楼层订单、一台或两台电梯，AMR 数量与就绪偏移取固定网格；附录 B），在满足条件（a）至（d）的实例中没有发现任何完工期反转；这是在该实例类上的核验，而不是证明。在以相同 AMR 指派重放的预注册排序检验的 6,000 次匹配波次抽取上（发表规模，按含重复的抽取计数；第 5.2 节），20 次反转中的每一次都违反（c）或（d）：18 次违反（c），其余 2 次（c）成立而（d）不成立。

The same replay shows that the sufficient conditions are restrictive. On these draws, (c) fails on 12.7% and (d) on 99.4%, so (a) to (d) hold jointly on fewer than 1% of them, whereas the makespan ordering holds on 99.7% of them with common assignments; with the free assignments of the preregistered test, the reported per-wave ordering rate is 99.2% (Section 5.2). The ordering therefore holds far more often than the conditions certify, and Section 5 reports the frequency of the conditions and the frequency of the ordering separately.

> **中文：** 同一次重放也表明这些充分条件相当严格。在这些抽取上，（c）在 12.7% 上不成立，（d）在 99.4% 上不成立，因此（a）至（d）同时成立的不到 1%；而在相同指派下，完工期排序在 99.7% 上成立；在预注册检验的自由指派下，报告的逐波次排序率为 99.2%（第 5.2 节）。可见排序成立的频率远高于条件所能保证的范围；第 5 节分别报告条件成立的频率与排序成立的频率。

The abstraction bias of candidate \(k\) is \(B_k=\bigl[C_{\max}(W^k,\pi^k;M_2)-C_{\max}(W^k,\pi^k;M_1)\bigr]/C_{\max}(W^k,\pi^k;M_1)\), the relative amount by which the throughput abstraction understates the co-occupancy makespan; it is nonnegative whenever Equation (46) holds.

> **中文：** 候选 \(k\) 的抽象偏差为 \(B_k=\bigl[C_{\max}(W^k,\pi^k;M_2)-C_{\max}(W^k,\pi^k;M_1)\bigr]/C_{\max}(W^k,\pi^k;M_1)\)，即吞吐量抽象相对于同乘完工期的低估比例；只要式 (46) 成立，它就非负。

For a class \(q\), the same draw \(\kappa\sim\nu_q\) is evaluated under both deterministic evaluators. If conditions (a) to (d) of Theorem 1 hold for every candidate in \(\mathcal{K}_q\), then \(Y_{\kappa M_1}\le Y_{\kappa M_2}\) almost surely. The class distribution function is \(F_{qi}(t)=\Pr_{\kappa\sim\nu_q}(Y_{\kappa M_i}\le t)\). The almost-sure comparison implies first-order stochastic ordering and, consequently, midpoint-median ordering:

> **中文：** 对类别 \(q\)，同一次抽取 \(\kappa\sim\nu_q\) 在两个确定性评估器下评价。若定理 1 的条件（a）至（d）对 \(\mathcal{K}_q\) 中每个候选都成立，则几乎必然有 \(Y_{\kappa M_1}\le Y_{\kappa M_2}\)。类别分布函数记为 \(F_{qi}(t)=\Pr_{\kappa\sim\nu_q}(Y_{\kappa M_i}\le t)\)。几乎必然的比较蕴含一阶随机排序，进而蕴含中点中位数的排序：

$$
F_{q1}(t)\ge F_{q2}(t)\quad\text{for all }t,\qquad \mu_{qM_1}^{0.5}\le\mu_{qM_2}^{0.5}. \tag{47}
$$

Fig. 4 contrasts the sufficient ordering conditions with the two reversal mechanisms.

> **中文：** 图 4 对比了排序的充分条件与两种反转机制。

![Fig. 4](revision_2026-09-02/figures/section4_2026-09-14/fig4_ordering_mechanisms_v1.png)

CAPTION: Fig. 4. Conditional ordering and two reversal mechanisms. (a) From a common initial state, the same recorded sequence and AMR assignments, together with no batch overtaking and no \(M_1\) repositioning disadvantage, imply request and wave completion ordering. The conditions holding for every candidate in a class also imply class-median ordering. (b) Batch overtaking gives wave makespans of 26 s under \(M_1\) and 24 s under \(M_2\). (c) Adverse repositioning gives 103 s and 68 s, respectively; event times are exact, while horizontal spacing is schematic. These examples violate different sufficient conditions; a violated condition alone does not guarantee reversal.

> **中文：** 图 4. 条件性排序与两种反转机制。(a) 从共同初始状态出发，相同的记录序列与 AMR 指派，加上没有批次超越、\(M_1\) 没有调位劣势，蕴含请求与波次完成时刻的排序；若这些条件对类别内每个候选都成立，还蕴含类别中位数的排序。(b) 批次超越使波次完工期在 \(M_1\) 下为 26 秒、在 \(M_2\) 下为 24 秒。(c) 不利调位分别给出 103 秒与 68 秒；事件时刻精确，水平间距为示意。两个实例违反的是不同的充分条件；仅有条件被违反并不保证发生反转。

# 4.4 Properties of robust selection / 稳健选择的性质

## 4.4.1 Reduction under ordered evaluator scores / 评估器得分有序时的简化

The procedure in Section 4.1 compares both deterministic class medians. The ordering analysis in Section 4.3 motivates examining when one evaluator alone determines the robust score. The relevant medians, robust score, and conservative choice are denoted by

> **中文：** 第 4.1 节的流程比较两个确定性评估器的类别中位数。第 4.3 节的排序分析引出一个问题：何时单个评估器就决定了稳健得分。相关的中位数、稳健得分与保守选择记为

$$
a_q=\mu_{qM_1}^{0.5},\qquad b_q=\mu_{qM_2}^{0.5},\qquad V_q=\max\{a_q,b_q\},\qquad q_H\in\underset{q\in\mathcal{Q}}{\mathrm{arg\,min}}\;b_q. \tag{48}
$$

Here \(b_q\) specializes the fixed-evaluator notation of Section 4.2 to \(M_2\). We refer to \(q_H\) as the \(M_2\)-based conservative choice. The same question arises for single candidates, whose scores \(\ell_{km}\), \(m\in\mathcal{M}_D\), under the serial reservation (closed-form) evaluators of Section 3.5 are defined in Equation (16).

> **中文：** 这里 \(b_q\) 是第 4.2 节固定评估器记号在 \(M_2\) 下的特例。我们称 \(q_H\) 为基于 \(M_2\) 的保守选择。同样的问题也出现在单个候选上，其在第 3.5 节串行预约（闭式）评估器下的得分 \(\ell_{km}\)（\(m\in\mathcal{M}_D\)）由式 (16) 定义。

**Corollary 1 (conditional minimax reduction).** (a) If Equation (47) holds for every \(q\in\mathcal{Q}\), or more generally if \(a_q\le b_q\) for every \(q\in\mathcal{Q}\), then the robust class objective equals the \(M_2\) median class by class, and

> **中文：** **推论 1（条件性极小极大归约）。** (a) 若式 (47) 对每个 \(q\in\mathcal{Q}\) 成立，或更一般地，若对每个 \(q\in\mathcal{Q}\) 都有 \(a_q\le b_q\)，则稳健类别目标逐类等于 \(M_2\) 中位数，且

$$
\underset{q\in\mathcal{Q}}{\mathrm{arg\,min}}\;\max\{a_q,b_q\}=\underset{q\in\mathcal{Q}}{\mathrm{arg\,min}}\;b_q. \tag{49}
$$

(b) If a finite nonempty candidate set \(\tilde{\mathcal{K}}\) satisfies \(\ell_{kM_1}\le\ell_{kM_2}\) for every \(k\in\tilde{\mathcal{K}}\), then

> **中文：** (b) 若有限非空候选集合 \(\tilde{\mathcal{K}}\) 对每个 \(k\in\tilde{\mathcal{K}}\) 都满足 \(\ell_{kM_1}\le\ell_{kM_2}\)，则

$$
\underset{k\in\tilde{\mathcal{K}}}{\mathrm{arg\,min}}\;\underset{m\in\mathcal{M}_D}{\max}\;\ell_{km}=\underset{k\in\tilde{\mathcal{K}}}{\mathrm{arg\,min}}\;\ell_{kM_2}. \tag{50}
$$

**Proof.** (a) Equation (47) gives \(a_q\le b_q\). The ordering gives \(V_q=b_q\) for every selectable class, so both minimizations have the same objective. (b) The per-candidate ordering gives \(\max_{m\in\mathcal{M}_D}\ell_{km}=\ell_{kM_2}\) for every \(k\in\tilde{\mathcal{K}}\), and the same argument applies. \(\square\) Theorem 1 supplies, through Equation (47), one sufficient route to the premise of (a) and, directly, one route to the premise of (b). Both premises can also be checked on the class medians or on the candidate scores, without requiring request-level ordering for every candidate. With a common tie convention, both minimizations return the same class or candidate.

> **中文：** **证明。** (a) 式 (47) 给出 \(a_q\le b_q\)。该排序对每个可选类别给出 \(V_q=b_q\)，因此两个最小化问题的目标相同。(b) 逐候选的排序对每个 \(k\in\tilde{\mathcal{K}}\) 给出 \(\max_{m\in\mathcal{M}_D}\ell_{km}=\ell_{kM_2}\)，同理可得。\(\square\) 定理 1 通过式 (47) 为 (a) 的前提提供了一条充分途径，并直接为 (b) 的前提提供了一条途径。两个前提也可以直接在类别中位数或候选得分上核对，而不必要求每个候选都满足请求层面的排序。在相同的并列处理约定下，两个最小化问题返回同一个类别或候选。

Part (b) underlies the screening step of Section 4.5. If \(\ell_{kM_1}\le\ell_{kM_2}\) for every candidate of a screened pool, the \(M_2\) score and the minimax score coincide on that pool, so they give the same ranking and, with a common tie order, the same shortlist of every size. Checking the premise requires the \(M_1\) scores, and so do conditions (c) and (d) of Theorem 1, which are assessed on the paired reservation paths; screening by the \(M_2\) score alone therefore rests on the ordering being assumed, for example from ordering rates measured on comparable candidates, except when \(c=1\), where the two evaluators coincide. The same algebraic reduction applies to the estimated objective in Section 4.1 whenever the estimated class medians are ordered. Request-level condition checks, makespan-ordering frequencies, and class-median comparisons are recorded separately, preserving the distinction between the premise of Theorem 1 and the premise of Corollary 1.

> **中文：** (b) 部分是第 4.5 节筛选步骤的依据。若被筛选候选池中的每个候选都满足 \(\ell_{kM_1}\le\ell_{kM_2}\)，则 \(M_2\) 得分与极小极大得分在该池上重合，因而给出相同的排序，并在相同的并列顺序下给出任意规模都相同的短名单。核对这一前提本身需要 \(M_1\) 得分；定理 1 的条件（c）与（d）也要在成对的预约路径上核对，同样需要 \(M_1\)。因此，仅凭 \(M_2\) 得分筛选依赖于对排序成立的假定，例如依据在可比候选上测得的排序率；唯一的例外是 \(c=1\)，此时两个评估器完全一致。只要估计出的类别中位数有序，同样的代数归约也适用于第 4.1 节的估计目标。请求层面的条件核查、完工期排序频率与类别中位数比较分别记录，以区分定理 1 的前提与推论 1 的前提。

## 4.4.2 Departures from ordering and selection stability / 偏离排序时的选择稳定性

When some class medians reverse order, their effect on the robust objective can be represented exactly by the positive excess of the \(M_1\) median:

> **中文：** 当部分类别中位数的顺序反转时，它们对稳健目标的影响可以由 \(M_1\) 中位数的正超出量精确表示：

$$
e_q=[a_q-b_q]_+,\qquad [u]_+=\max\{u,0\},\qquad V_q=b_q+e_q. \tag{51}
$$

**Corollary 2 (excess loss and ranking stability).** For any \(M_2\)-optimal class \(q_H\), its excess robust objective satisfies

> **中文：** **推论 2（超额损失与排序稳定性）。** 对任一 \(M_2\) 最优类别 \(q_H\)，其稳健目标的超额满足

$$
0\le V_{q_H}-\min_{q\in\mathcal{Q}}V_q\le e_{q_H}. \tag{52}
$$

If \(q_H\) is the unique \(M_2\)-optimal class, its ranking margin is \(\Delta_H=\min_{q\ne q_H}(b_q-b_{q_H})\). This margin gives the sufficient condition

> **中文：** 若 \(q_H\) 是唯一的 \(M_2\) 最优类别，其排序余量为 \(\Delta_H=\min_{q\ne q_H}(b_q-b_{q_H})\)。该余量给出充分条件

$$
\Delta_H>e_{q_H}\;\Longrightarrow\;\underset{q\in\mathcal{Q}}{\mathrm{arg\,min}}\;V_q=\{q_H\}. \tag{53}
$$

**Proof.** Since \(V_q\ge b_q\ge b_{q_H}\), the optimal robust value is at least \(b_{q_H}\). Subtracting this lower bound from \(V_{q_H}=b_{q_H}+e_{q_H}\) gives Equation (52). Under the strict margin condition, every other class satisfies \(V_q\ge b_q>b_{q_H}+e_{q_H}=V_{q_H}\), proving Equation (53). \(\square\)

> **中文：** **证明。** 由 \(V_q\ge b_q\ge b_{q_H}\)，最优稳健值至少为 \(b_{q_H}\)。用 \(V_{q_H}=b_{q_H}+e_{q_H}\) 减去这一下界即得式 (52)。在严格余量条件下，其他每个类别都满足 \(V_q\ge b_q>b_{q_H}+e_{q_H}=V_{q_H}\)，从而证明式 (53)。\(\square\)

When the margin condition does not hold, the robust decision is obtained by comparing the full scores \(V_q\). Corollary 2 assesses excess performance loss relative to the two-model median-minimax optimum. Evaluator-specific regret, such as the \(M_1\) regret \(a_{q_H}-\min_q a_q\), makes a different comparison and is reported separately. Corollary 2 does not involve \(M_3\), whose class distribution in Equation (14) is assessed on its own.

> **中文：** 当余量条件不成立时，稳健决策需比较完整得分 \(V_q\) 得到。推论 2 衡量的是相对于两模型中位数极小极大最优值的超额绩效损失。评估器特定的遗憾，例如 \(M_1\) 遗憾 \(a_{q_H}-\min_q a_q\)，做的是另一种比较，另行报告。推论 2 不涉及 \(M_3\)；\(M_3\) 的类别分布（式 (14)）单独评估。

**Remark 2.** Under the ordering of Equation (47), the worst-case class mean over the 1-Wasserstein ball centered on the \(M_1\) class distribution, with radius equal to the 1-Wasserstein distance between the \(M_1\) and \(M_2\) class distributions, equals the \(M_2\) class mean, a mean-based counterpart of Corollary 1(a) and a simple instance of an analytical worst case under stochastic dominance (cf. Fu, Li and Zhang, 2024), whereas Equation (15) uses medians.

> **中文：** **注 2。** 在式 (47) 的排序下，以 \(M_1\) 类别分布为中心、半径等于 \(M_1\) 与 \(M_2\) 类别分布之间 1-Wasserstein 距离的球上，最坏情形的类别均值等于 \(M_2\) 类别均值；这是推论 1(a) 在均值上的对应结果，也是随机占优下最坏情形可解析求出的一个简单例子（参见 Fu, Li and Zhang, 2024），而式 (15) 使用的是中位数。

# 4.5 Generate, screen, and verify release procedure / 生成、筛选、验证释放流程

<!-- Section 4.5 is kept in week3/SECTION_4_5_GSV_draft.md (revised the same day). The builder takes Section 4.5 from that file. -->

# 4.6 What Section 5 tests / 第 5 节检验什么

Sections 4.1 to 4.5 contain two kinds of statements. Propositions 1 and 2, Theorem 1, Corollaries 1 and 2, and Remarks 1 and 2 hold on any candidate pool that satisfies their premises; Section 5 does not test them but measures how often their premises hold on the benchmark and what happens when they do not. The class diagnostic, the choice of evaluator, and the release procedure make empirical claims, and Section 5 examines each against registered criteria.

> **中文：** 第 4.1 至 4.5 节包含两类陈述。命题 1 与 2、定理 1、推论 1 与 2 以及注 1 与 2 在满足各自前提的任何候选池上都成立；第 5 节不检验它们，而是度量这些前提在基准上成立的频率，以及前提不成立时会发生什么。类别诊断、评估器的选择与释放流程则提出了经验性主张，第 5 节按已登记的准则逐一检验。

Study 1 (Section 5.2) reports, with its verdicts unchanged, the preregistered tests of the class diagnostic and class rule of Sections 4.1 and 4.2 and of the evaluator ordering behind Sections 4.3 and 4.4: how often \(\ell_{kM_1}\le\ell_{kM_2}\) holds per wave and how often the class distributions are ordered as Corollary 1(a) requires. It also reports how often conditions (a) to (d) hold and, as a registered re-analysis, the abstraction bias \(B_k\).

> **中文：** 研究一（第 5.2 节）按原判定报告第 4.1 与 4.2 节类别诊断与类别规则的预注册检验，以及第 4.3 与 4.4 节所依据的评估器排序的预注册检验：\(\ell_{kM_1}\le\ell_{kM_2}\) 在波次层面成立的频率，以及类别分布满足推论 1(a) 所需排序的频率。研究一还报告条件（a）至（d）成立的频率，并以已登记的重分析报告抽象偏差 \(B_k\)。

Study 2 (Section 5.3) evaluates the procedure of Section 4.5 against random, class-based, heuristic, and search policies. Under the event-driven evaluator, it asks how much the processing sequence alone changes makespan, whether closed-form screening of the augmented pool outperforms heuristic scoring at the same verification budget and how it compares with a budget-matched local search, how large a shortlist the verification step needs, and how much is lost by selecting with each closed-form evaluator. With the closed-form evaluators, it asks whether the ordering persists on candidates built to create shared trips. It also asks whether single-wave results carry over to consecutive waves, how robust the released waves are to execution noise, and how long each step takes. Section 5.4 applies the procedure to a literature-calibrated case, and Section 5.5 states where the closed-form diagnostics stop being reliable.

> **中文：** 研究二（第 5.3 节）将第 4.5 节的流程与随机、基于类别、启发式与搜索策略比较。在事件驱动评估器下，它考察：仅改变处理序列会使完工期改变多少；在相同验证预算下，对扩充候选池做闭式筛选是否优于启发式打分，与预算匹配的局部搜索相比又如何；验证步骤需要多大的短名单；用各闭式评估器选择会损失多少。在闭式评估器下，它考察在为制造同乘而构建的候选上排序是否仍成立。它还考察单波次结果能否延续到连续波次、释放的波次对执行噪声有多稳健，以及各步骤的耗时。第 5.4 节把该流程用于一个依据文献校准的案例，第 5.5 节说明闭式诊断在何处不再可靠。

## Notes for the author (not for the manuscript) / 作者说明（不进入论文）

1. **Numbering.** Applied as decided in master §00.5 (2026-09-26). In Section 4.2 of the Word file, three labels are edited in place as tracked changes: "Proposition 2 (class-action loss interpretation)" becomes "Remark 1", "Theorem 1 (nested-partition refinement)" becomes "Proposition 2", and "Corollary 1 (diagnostic resolution)." becomes the run-in heading "Diagnostic resolution." (its content is part of Proposition 2); "exact checks of Theorem 1" becomes "exact checks of Proposition 2". Equation numbers continue from (46): (47) to (53) here, (54) to (57) in Section 4.5.
2. **What left Section 4.** The midpoint quantile bound (old Equations (53) to (55), the U_c certificate) goes to an appendix and to one boundary sentence in Section 5.5 (TH-5). The mean-based Wasserstein comparison (old Equations (56) and (57), Corollary 3) is Remark 2 (TH-4); its Mohajerin Esfahani and Kuhn (2018) citation leaves Section 4. Corollary 4 (old Equation (58)) is deleted. Fig. 5 is not inserted. The clause "with \(\Delta_H=+\infty\) when only one class is selectable" is dropped, because Section 3.3.3 requires every class of \(\mathcal Q\) to be nonempty.
3. **Revision 2 (after two independent reviews, 2026-09-26).** The first version said that neither check explains how often the conditions hold; B-1's registered second addendum (iv) exists so that Section 4 can state it, so the base rates are now given (master §0.2: fewer than 1%). The census sentence now quotes the class and calls the result a certification (AMEND-B11 rule 4), and 1,000,800 of the 1,150,800 instances are exhaustive. The 18/2 split is stated as condition profiles, because the B-1 classifier tests (c) before (d). The abstraction bias is defined in Section 4.3.2 (STORY_CONTRACT §6 lists it under 4.3); its symbol \(B_k\) follows TERMINOLOGY ("abstraction bias B") and should not be confused with the availabilities \(B_v\), \(B_e\) of Section 3.5, which carry resource indices. The mechanism names follow TERMINOLOGY ("batch overtaking", "adverse repositioning"); Fig. 4's raster panels still read "Shared-trip reversal" and "Repositioning reversal" and are aligned in the figure pass. Corollary 1(b) uses \(\tilde{\mathcal K}\) instead of \(\mathcal K'\), because \(K'\) is the number of constructed candidates in Section 4.5. \(F_{qi}\) is now written with \(\Pr_{\kappa\sim\nu_q}\). Section 4.6 separates the event-driven questions from the closed-form one (G4) and names the comparators of C3.
4. **Wording checks done.** Proposition 3 is never called a theorem; no claim that the ordering always holds; condition coverage and ordering frequency are stated separately (master §2.4); scales are labelled (small census instances; publication-scale waves of the preregistered ordering test); evidence tag [NS] on the registered checks (master §0.3); no em dash; American spelling.
5. **Case sentence.** "Section 5.4 applies the procedure to a literature-calibrated case" holds under D-K as signed. If the case is dropped (STORY_CONTRACT §8, last rule), this sentence must be dropped as well; §8's list does not name Section 4.6.
6. **Pre-existing text, not changed.** The Section 4 introduction says "Two analyses support this selection framework" and then "the supporting roles of the three analyses", and Fig. 2 does not show Section 4.5. Both are the author's to align when Fig. 2 is redrawn.
7. **Revision 3 (second review round, 2026-09-26).** The examples paragraph now says that each example reverses the ordering (so neither condition can be dropped) and states the converse separately. The census class quotes its grids. The replay is counted in matched-wave draws with multiplicity, and the 99.2% free-assignment rate is stated beside the 99.7% common-assignment rate, as AMEND-B (B-1) requires. The M1-skip sentence is corrected: conditions (c) and (d) are themselves assessed on the paired paths, so Proposition 3 cannot spare the M1 run; only assumed ordering (or \(c=1\)) can. Remark 2 is one sentence again (master §00.5, decision 3). In Word, the author's sentence "the unfavorable repositioning distance in (d)" becomes "the adverse repositioning distance in (d)" (tracked), so that the mechanism names match TERMINOLOGY. For the figure pass: Fig. 4 panel (c) labels availabilities as a bare \(B\), which now clashes with the abstraction bias \(B_k\); relabel them \(B_v\), \(B_e\) as in Section 3.5.
8. **Appendix letters.** Appendix B holds the B-11 census summary (plan v2 §2); Appendix A §A.4 already holds both examples in full, so the plan's Appendix B entry for the examples can be dropped when the letters are fixed. The B-1 replay numbers belong to Section 5.2 (master §8.3).

**R. Theorem 1 (2026-09-27).** After the author's verification (MATH_VERIFICATION_LOG rows 4 to 12), "Proposition 3" is renamed "Theorem 1" in the manuscript text of this file (5 English and 5 Chinese occurrences); older labels in the notes above are kept as written.
