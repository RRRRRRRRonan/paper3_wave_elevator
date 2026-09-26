---
title: "Section 4.5 draft: generate, screen, and verify release procedure (with Algorithm 1)"
date: 2026-09-26
status: "DRAFT for author review. Inserted into Methodology.docx with tracked changes (author authorization of 2026-09-26: §4 supplements by track changes). Revised the same day to the IJPR numbering of master §00.5 (candidate-level reduction = Corollary 1(b) in §4.4.1; equations (54) to (57), set as Word equations) together with week3/SECTION_4_3_2_to_4_6_draft.md."
sources: "STORY_CONTRACT.md §3 (C3 wording) and §8 (wording rules); paper_draft/phase6_method_study_protocol.md §3.4, §3.5, §5, §7.1; TERMINOLOGY.md; Section 3 Eqs. (1), (16), (17); Section 4.3 Proposition 3"
notation: "Checked on 2026-09-26 against the FINAL Section 3 (Problem formulation.docx; bilingual mirror revision_2026-09-24/section3_bilingual_2026-09-24.md) and the current Section 4 (revision_2026-09-02/SECTION_4_METHODOLOGY.md). New symbols, all unused there: the augmented pool K+ with parts K^seq and K^con (k indexes candidates as in Section 3; G_tau is a trip's request group in Section 4; a superscript C could read as a complement or as the C axis), the screening key psi_k (s_o is a source floor), the shortlist K^V of size K_V (Section 3 uses calligraphic S for its option set, Table 3.3 and Equation (32); K = |K| is the pool size), the released candidate k^dagger, the screening regret Reg(K_V) (r_o is a ready offset), the smallest adequate size K_V^star, and M_2^DES for the event-driven evaluator (E is the number of elevators). Prose names: shortlist size = k and screening regret = r(k) in the protocol, the code, and TERMINOLOGY."
---

# 4.5 Generate, screen, and verify release procedure / 生成、筛选、验证释放流程

The class-selection procedure of Section 4.1 releases a wave drawn from a class, and no such rule can release a wave whose score under an evaluator \(m\in\mathcal M_D\) is below the pool optimum of Equation (17) for that evaluator. This section describes a release procedure that works with individual candidates instead. It generates candidate waves, screens them with a closed-form evaluator, and verifies a shortlist with an event-driven evaluator before release. The dispatch rule of Section 3 stays fixed; the procedure changes only the released wave, that is, its order set and its processing sequence.

> **中文：** 第 4.1 节的类别选择流程从某个类别中抽取释放波次，而任何此类规则释放的波次，其在评估器 \(m\in\mathcal M_D\) 下的得分都不会低于该评估器在式 (17) 中的池内最优。本节给出一个直接面向单个候选波次的释放流程：先生成候选波次，再用闭式评估器筛选，最后在释放前用事件驱动评估器验证一个短名单。第 3 节的调度规则保持不变，流程只改变释放的波次，即其订单集合与处理序列。

The generate, screen, and verify (GSV) procedure has three steps (Algorithm 1). The generation step adds to the random pool candidates designed around the two mechanisms of Section 4.3. The screening step ranks every candidate with a closed-form evaluator, which is inexpensive enough to apply to thousands of candidates. The verification step evaluates the best-ranked candidates with an event-driven evaluator, in which AMRs act concurrently, and releases the best of them. The closed-form evaluators therefore serve as a filter, and the event-driven evaluator makes the final choice.

> **中文：** 生成、筛选、验证（GSV）流程分为三步（算法 1）。生成步骤在随机候选池之外，加入围绕第 4.3 节两种机制设计的候选。筛选步骤用闭式评估器为全部候选排序，其计算代价低到足以处理数千个候选。验证步骤用 AMR 并发运行的事件驱动评估器评价排名靠前的候选，并释放其中最好的一个。因此，闭式评估器起过滤作用，最终选择由事件驱动评估器作出。

## 4.5.1 Candidate generation / 候选生成

The augmented pool is

> **中文：** 扩充后的候选池为

$$
\mathcal K^{+}=\mathcal K\,\cup\,\mathcal K^{\mathrm{seq}}\,\cup\,\mathcal K^{\mathrm{con}}. \tag{54}
$$

Its first part is the random pool \(\mathcal K\) of Section 3.3.1 with the recorded sequences \(\pi^k\). The second part, \(\mathcal K^{\mathrm{seq}}\), re-sequences each random candidate. The sequence-aware re-ordering keeps the order set \(W^k\) and changes only the sequence. It groups orders with the same source and destination floors into blocks of at most \(c\) orders, so that their elevator requests can share an \(M_2\) trip. It then orders the blocks by readiness and, among equally ready blocks, chooses next the block whose source floor equals, or else is nearest to, the destination floor of the previous block, which is intended to reduce empty repositioning. The third part, \(\mathcal K^{\mathrm{con}}\), contains \(K'\) candidates from a co-ride-aware constructive generator. Starting from a random cross-floor order, the generator repeatedly adds the order with the highest weighted score. The score rewards completing a partly filled co-ride block and chaining to the wave (the order's source is the destination of an order already in the wave, or its destination is the source of one), and it penalizes endpoint floors new to the wave; the weights are fixed by a registered tuning rule on training pools, and ties are broken at random. Each constructed order set is then sequenced by the same re-ordering. For \(k\in\mathcal K^{\mathrm{seq}}\cup\mathcal K^{\mathrm{con}}\), \(\pi^k\) denotes the sequence set by the re-ordering; every evaluator processes it in place of the recorded sequence of Equation (1), and the statements of Section 3 about recorded sequences refer to the random pool \(\mathcal K\). Both operators target the mechanisms of Section 4.3: under \(M_2\), requests with the same source and destination that are issued no later than the end of a trip's loading, while the car has free capacity, share the trip, and linked floors can shorten repositioning. Appendix X specifies both operators, including their tie rules.

> **中文：** 候选池的第一部分是第 3.3.1 节的随机候选池 \(\mathcal K\)，保留记录序列 \(\pi^k\)。第二部分 \(\mathcal K^{\mathrm{seq}}\) 对每个随机候选重新排序：序列感知重排保持订单集合 \(W^k\) 不变，只改变序列。它把起讫楼层相同的订单按不超过 \(c\) 个一组分块，使其电梯请求能够共享同一 \(M_2\) 行程；再按就绪时间为各块排序，并在就绪时间相同的块之间，优先选取起始楼层等于（否则最接近）上一块目的楼层的块，意在减少空驶调位。第三部分 \(\mathcal K^{\mathrm{con}}\) 包含同乘感知构造生成器产生的 \(K'\) 个候选：从一个随机的跨楼层订单出发，生成器逐次加入加权得分最高的订单。得分奖励补全未满的同乘块以及与波次衔接（该订单的起点是波次中某订单的终点，或其终点是某订单的起点），并惩罚波次中新增的端点楼层；权重由在训练池上已登记的调参规则确定，并列时随机选取。每个构造出的订单集合再用同一重排方法确定序列。对 \(k\in\mathcal K^{\mathrm{seq}}\cup\mathcal K^{\mathrm{con}}\)，\(\pi^k\) 表示重排给出的序列；所有评估器都用它代替式 (1) 的记录序列，第 3 节关于记录序列的陈述只针对随机候选池 \(\mathcal K\)。两个算子都针对第 4.3 节的机制：在 \(M_2\) 下，起讫相同、发出时刻不晚于某行程装载结束且轿厢尚有余量的请求共享该行程，楼层衔接则可以缩短调位。附录 X 给出两个算子的完整规则（含并列处理）。

## 4.5.2 Closed-form screening / 闭式筛选

Each candidate \(k\in\mathcal K^{+}\) is scored in closed form as in Equation (16), \(\ell_{km}=C_{\max}(W^k,\pi^k;m)\) for \(m\in\mathcal M_D\). The screening key is the \(M_2\) score,

> **中文：** 每个候选 \(k\in\mathcal K^{+}\) 按式 (16) 以闭式计算得分 \(\ell_{km}=C_{\max}(W^k,\pi^k;m)\)，\(m\in\mathcal M_D\)。筛选键取 \(M_2\) 得分：

$$
\psi_k=\ell_{kM_2},\qquad k\in\mathcal K^{+}. \tag{55}
$$

This choice applies the robust objective of Section 3.4.2 to single candidates: if \(\ell_{kM_1}\le\ell_{kM_2}\) holds for every candidate of \(\mathcal K^{+}\), the \(M_2\) key and the minimax key \(\max_{m\in\mathcal M_D}\ell_{km}\) coincide on \(\mathcal K^{+}\) (Corollary 1(b)), so they give the same ranking and the same shortlist.

> **中文：** 这一选择是把第 3.4.2 节的鲁棒目标用于单个候选：若 \(\mathcal K^{+}\) 中每个候选都满足 \(\ell_{kM_1}\le\ell_{kM_2}\)，则 \(M_2\) 筛选键与极小极大筛选键 \(\max_{m\in\mathcal M_D}\ell_{km}\) 在 \(\mathcal K^{+}\) 上重合（推论 1(b)），因此给出相同的排序与相同的短名单。

Theorem 1 gives sufficient conditions for the per-candidate ordering, and Section 4.3.2 identifies the two mechanisms that can reverse it. Re-sequenced and constructed candidates are built to create shared trips, so the ordering may fail more often on them. The procedure can therefore use the conservative key \(\psi_k=\max_{m\in\mathcal M_D}\ell_{km}\) for \(k\in\mathcal K^{\mathrm{seq}}\cup\mathcal K^{\mathrm{con}}\), keeping \(\psi_k=\ell_{kM_2}\) for \(k\in\mathcal K\); this key equals the minimax key on all of \(\mathcal K^{+}\) when the ordering holds on \(\mathcal K\). Section 5 states which key the registered study uses and the rule that decides it. Ties in \(\psi_k\) are broken by a fixed random order of the candidates. Candidates with the same sequence of source floors, destination floors, and ready offsets receive the same score from every evaluator, so they count once. The shortlist \(\mathcal K^{\mathrm V}\) contains the first \(K_{\mathrm V}\) distinct sequences in increasing order of \(\psi_k\).

> **中文：** 定理 1 给出逐候选排序成立的充分条件，第 4.3.2 节则指出可能使其反转的两种机制。重排候选与构造候选本就是为制造共享行程而设计的，排序在它们上面可能更常失效。因此，流程可以对 \(k\in\mathcal K^{\mathrm{seq}}\cup\mathcal K^{\mathrm{con}}\) 改用保守筛选键 \(\psi_k=\max_{m\in\mathcal M_D}\ell_{km}\)，而对 \(k\in\mathcal K\) 保留 \(\psi_k=\ell_{kM_2}\)；当排序在 \(\mathcal K\) 上成立时，这一筛选键在整个 \(\mathcal K^{+}\) 上等于极小极大筛选键。第 5 节说明登记研究采用哪个筛选键以及决定它的规则。\(\psi_k\) 相同时按一个固定的随机顺序处理。起始楼层、目的楼层与就绪偏移序列完全相同的候选在所有评估器下得分相同，只计一次。短名单 \(\mathcal K^{\mathrm V}\) 由按 \(\psi_k\) 升序排列的前 \(K_{\mathrm V}\) 个不同序列组成。

## 4.5.3 Event-driven verification and release / 事件驱动验证与释放

The closed-form evaluators of Section 3.5 process a candidate's sequence \(\pi^k\) one order at a time, assigning each order to the earliest available AMR. The verification evaluator executes the same \(M_2\) rules as an event-driven simulation. AMRs claim orders in the sequence \(\pi^k\), act concurrently, wait for each order's ready time, and request elevators in time order; a request boards an open trip with the same source and destination while its loading window is open and the car has free capacity, and otherwise takes the earliest available car. We denote this evaluator by \(M_2^{\mathrm{DES}}\) and its makespan by \(\ell_{kM_2^{\mathrm{DES}}}\). The two evaluators can rank the same candidates differently; one reason is that the closed-form evaluators reserve elevator resources in the order of the sequence rather than in the time order of the requests. In the registered event-driven cross-check on publication-scale waves, rerun with the boarding rule used here, the closed-form ranking does not meet the registered criterion for a faithful ordinal proxy of the event-driven ranking (Section 5.5). The release decision is therefore made under \(M_2^{\mathrm{DES}}\). The procedure evaluates every shortlisted candidate and releases

> **中文：** 第 3.5 节的闭式评估器沿候选的序列 \(\pi^k\) 逐个处理订单，把每个订单指派给最早可用的 AMR。验证评估器以事件驱动仿真的方式执行同一套 \(M_2\) 规则：AMR 按序列 \(\pi^k\) 认领订单并发运行，等待各订单就绪，按请求时间先后使用电梯；若存在起讫楼层相同、装载窗口尚未关闭且轿厢尚有余量的在途行程，请求即加入该行程，否则使用最早可用的轿厢。该评估器记为 \(M_2^{\mathrm{DES}}\)，其完工期记为 \(\ell_{kM_2^{\mathrm{DES}}}\)。两个评估器可能对同一批候选给出不同的排序；原因之一是闭式评估器按序列的顺序、而不是按请求发生的时间顺序预约电梯资源。在已登记的发表规模事件驱动交叉检验中（已按本文的登梯规则重跑），闭式排序未达到作为事件驱动排序的可靠顺序代理的登记准则（第 5.5 节）。因此释放决策在 \(M_2^{\mathrm{DES}}\) 下作出。流程评价短名单中的每个候选，并释放

$$
k^{\dagger}\in\underset{k\in\mathcal K^{\mathrm V}}{\mathrm{arg\,min}}\;\ell_{kM_2^{\mathrm{DES}}}, \tag{56}
$$

with ties broken by the same fixed order. The screening regret

> **中文：** 并列时仍按同一固定顺序处理。筛选遗憾

$$
\operatorname{Reg}(K_{\mathrm V})=\Bigl(\ell_{k^{\dagger}M_2^{\mathrm{DES}}}-\min_{k\in\mathcal K^{+}}\ell_{kM_2^{\mathrm{DES}}}\Bigr)\Big/\min_{k\in\mathcal K^{+}}\ell_{kM_2^{\mathrm{DES}}} \tag{57}
$$

is the relative excess of the released candidate's makespan over the best makespan in \(\mathcal K^{+}\) under the verification evaluator. Because the shortlists are nested, \(\operatorname{Reg}(K_{\mathrm V})\) does not increase with \(K_{\mathrm V}\), and it is zero once \(\mathcal K^{\mathrm V}\) contains every distinct sequence. The smallest shortlist size whose regret falls within a stated tolerance, \(K_{\mathrm V}^{\star}\), indicates how far closed-form screening can be trusted as a filter for the verification evaluator; Section 5 estimates \(\operatorname{Reg}(K_{\mathrm V})\) and \(K_{\mathrm V}^{\star}\).

> **中文：** 是释放候选的完工期相对于验证评估器下 \(\mathcal K^{+}\) 中最优完工期的相对超出量。由于短名单彼此嵌套，\(\operatorname{Reg}(K_{\mathrm V})\) 随 \(K_{\mathrm V}\) 增大而不增加，并在 \(\mathcal K^{\mathrm V}\) 包含全部不同序列时为零。筛选遗憾落在给定容差内的最小短名单规模 \(K_{\mathrm V}^{\star}\) 表明：闭式筛选在多大程度上可以作为验证评估器的过滤器。第 5 节估计 \(\operatorname{Reg}(K_{\mathrm V})\) 与 \(K_{\mathrm V}^{\star}\)。

Per released wave, the procedure uses at most \(|\mathcal K^{+}|\) closed-form evaluations under \(M_2\) (and under \(M_1\) for candidates screened with the conservative key) and at most \(K_{\mathrm V}\) event-driven evaluations. \(M_1\), \(M_2\), and \(M_2^{\mathrm{DES}}\) are thus rungs of a fidelity ladder: the closed-form score filters candidates quickly, and \(M_2^{\mathrm{DES}}\) makes the final choice. Section 4.3 gives conditions under which \(M_2\) is the larger, and hence conservative, closed-form score, and Section 5 measures how often it is. The regret \(\operatorname{Reg}(K_{\mathrm V})\) measures how well the filter ranks candidates for the verification evaluator.

> **中文：** 每释放一个波次，流程至多需要 \(|\mathcal K^{+}|\) 次 \(M_2\) 闭式评价（采用保守筛选键的候选还需 \(M_1\) 评价）和至多 \(K_{\mathrm V}\) 次事件驱动评价。\(M_1\)、\(M_2\) 与 \(M_2^{\mathrm{DES}}\) 由此构成保真阶梯上的几级：闭式得分快速过滤候选，\(M_2^{\mathrm{DES}}\) 作最终选择。第 4.3 节给出 \(M_2\) 为较大（因而保守）闭式得分的条件，第 5 节度量这种情形出现的频率。\(\operatorname{Reg}(K_{\mathrm V})\) 衡量该过滤器为验证评估器排序候选的准确程度。

## Algorithm 1 / 算法 1

```
Algorithm 1. Generate, screen, and verify (GSV) release of one wave
Input:  order pool O; wave size n; system parameters of Section 3.2 (including car
        capacity c); numbers of random and constructed candidates K and K';
        shortlist size K_V; fixed tie order
Output: released wave (W, pi)

 1: Draw K random candidates (W^k, pi^k) as in Section 3.3.1                  (generate)
 2: For each random candidate, form its sequence-aware re-ordering
 3: Build K' candidates with the co-ride-aware constructive generator;
    sequence each by the same re-ordering
 4: K+ <- random, re-ordered, and constructed candidates
 5: For every k in K+, compute the screening key psi_k (Equation (55)),         (screen)
    or the conservative key for re-ordered and constructed candidates
 6: Rank K+ by psi_k, ties by the fixed order; K^V <- the first K_V distinct sequences
 7: For every k in K^V, evaluate l_k under M2-DES                                  (verify)
 8: Release the k in K^V with the smallest l_k, ties by the fixed order (Equation (56))
```

> **中文：** 算法 1. 用"生成、筛选、验证"（GSV）释放一个波次。输入：订单池、波次规模 \(n\)、第 3.2 节的系统参数（含轿厢容量 \(c\)）、随机与构造候选数 \(K\) 与 \(K'\)、短名单规模 \(K_{\mathrm V}\)、固定的并列顺序。输出：释放的波次 \((W,\pi)\)。第 1 至 4 行生成候选；第 5、6 行筛选（重排与构造候选可用保守筛选键）；第 7、8 行验证并释放。

Algorithm 1 lists the steps for one wave. Lines 1 to 4 build the augmented pool of Equation (54). Line 2 leaves every order set unchanged, so the re-ordered candidates isolate the effect of the processing sequence, and line 3 adds order sets chosen for co-occupancy. Line 5 is the only evaluation step that touches every candidate, which is why it uses a closed-form evaluator. Line 6 counts distinct sequences, so the verification budget is not spent on duplicates, which constructed candidates in particular can produce. Lines 7 and 8 spend the event-driven evaluations only on the shortlist. The fixed tie order in lines 6 and 8 makes the released wave reproducible and prevents any candidate source from being favored by its position. When waves are released consecutively, the evaluations in lines 5 and 7 are made on the candidate appended to the waves already released, as one concatenated sequence evaluated from the common initial state; AMR and elevator states thus carry over, and Theorem 1 applies to the concatenation. Section 5 describes this warm-start use.

> **中文：** 算法 1 列出释放一个波次的步骤。第 1 至 4 行构建式 (54) 的扩充候选池。第 2 行不改变任何订单集合，因此重排候选单独体现处理序列的作用；第 3 行加入为同乘而挑选的订单集合。第 5 行是唯一需要评价全部候选的步骤，所以采用闭式评估器。第 6 行按不同序列计数，避免验证预算花在重复候选上（构造候选尤其容易重复）。第 7、8 行只对短名单使用事件驱动评价。第 6、8 行的固定并列顺序使释放结果可复现，也避免任何候选来源因排列位置而占优。连续释放多个波次时，第 5、7 行的评价针对"已释放波次加上该候选"串接而成的序列，从共同初始状态出发进行；AMR 与电梯状态由此得以延续，定理 1 也适用于串接后的序列。第 5 节说明这种热启动用法。

The procedure acts on the tactical release decision only. In the closed-form evaluators, the procedure and the clustered dispatch rule examined in Section 5.5 both act through the processing sequence; they differ in which layer sets it. The procedure sets the sequence at release, whereas clustered dispatch is an operational rule, equivalent in the evaluator to clustering the elevator's waiting queue, that serves here as an operational reference. Section 5 reports the closed-form effect of re-ordering at release next to that of clustered dispatch, each labeled with the scale at which it was measured, without ranking the two.

> **中文：** 该流程只作用于战术层的释放决策。在闭式评估器中，该流程与第 5.5 节考察的聚类派单规则都通过处理序列起作用，区别在于由哪一层确定序列：流程在释放时确定序列，而聚类派单是运营层规则（在评估器中等价于对电梯等待队列做聚类），在这里作为运营层的参照。第 5 节把释放时重排的闭式效果与聚类派单的效果并列报告，各自注明测得时所用的规模，不对两者排序。

---

## Notes for the author (not for the manuscript)

1. **Equations.** (54) to (57), numbered after §4.4 under the IJPR numbering of MASTER §00.5 (decided 2026-09-26). In Word they are native Word equations with the same MathType-style number field as Equations (33) to (46); MathType's Convert Equations turns them into MathType objects in one step if a uniform format is wanted. The old GSV-3 is now Equation (50), Corollary 1(b), in §4.4.1.
2. **Label of the candidate-level reduction.** Corollary 1(b), stated and proved in §4.4.1 with Theorem 2's class-level statement as Corollary 1(a) (decided 2026-09-26); §4.5.2 cites it.
3. **Symbols.** \(\mathcal K^{+}\), \(\mathcal K^{\mathrm{seq}}\), \(\mathcal K^{\mathrm{con}}\), \(\psi_k\), \(\mathcal K^{\mathrm V}\), \(K_{\mathrm V}\), \(k^{\dagger}\), \(\operatorname{Reg}(K_{\mathrm V})\), \(K_{\mathrm V}^{\star}\), and \(M_2^{\mathrm{DES}}\) are new and unused in the final Section 3 (the `Problem formulation.docx` text, mirrored in `revision_2026-09-24/section3_bilingual_2026-09-24.md`) and in the current Section 4. The first two drafts were checked against the superseded `SECTION_3_MODEL_FORMULATION.md` (now in `archive/revision_2026-09-02/`); the final Section 3 uses \(\mathcal S\) for the option set of Table 3.3 and Equation (32), so the shortlist is now \(\mathcal K^{\mathrm V}\), whose size is \(K_{\mathrm V}\). The same check shows that \(\delta\) is free in the final Section 3; \(\operatorname{Reg}(K_{\mathrm V})\) is kept because it names the quantity, and \(r\) and \(k\) are taken (\(r_o\), the candidate index). A superscript C on \(\mathcal K\) could be read as a complement or as the C axis, hence \(\mathcal K^{\mathrm{con}}\). \(K\) is the pool size \(|\mathcal K|\) of Section 3, so \(K'\) and \(K_{\mathrm V}\) follow the same convention for counts. \(k^{\dagger}\) and \(K_{\mathrm V}^{\star}\) reuse the decorations of \(m^{\dagger}\) and \(q^{\star}\) in Section 4 for a distinguished member and a selected value. In the protocol, the code, and TERMINOLOGY the shortlist size is called k and the screening regret r(k).
4. **"Appendix X"** is the appendix that will hold the exact P10 and P11 rules (protocol §5.1 and §5.3). Replace X when the appendix letters are fixed (plan v2 §2).
5. **Pointers needing destinations:** Section 3.5 (closed-form evaluators) exists; "Section 5" (registered key rule, warm start, \(\operatorname{Reg}(K_{\mathrm V})\), \(K_{\mathrm V}^{\star}\)) is written after Study 2.
6. **Wording checks done:** C3 wording of STORY_CONTRACT §3; no claim that the constructor adds value (STORY_CONTRACT §8 rule C3 decides that after Study 2); "sequence-aware re-ordering" and "co-ride-aware constructive generator" as in TERMINOLOGY; no "optimal", no em dash, American spelling; the dispatch rule stays fixed.

7. **Revision 2 (after two independent reviews, 2026-09-26).** Corrected against protocol §5.1, §5.3, §5.5 and §9 and Equation (25) of Section 3: the P11 description (a weighted score, not three joint conditions), the P10 chaining rule (equal or nearest source floor), the boarding condition (issued no later than the end of loading, free capacity), and the warm start (one concatenated sequence from the common initial state). The screening guarantee is stated on the whole screened pool (Corollary 1(b) concerns the argmin; the shortlist needs the keys to coincide on every candidate). The conservative key is defined for re-sequenced and constructed candidates only, as protocol §5.5 and STORY_CONTRACT §8 register it; the G4 outcome is not presumed. Re-sequenced sequences are reconciled with Section 3's recorded sequences (the Section 3 pool-augmentation sentence of STORY_CONTRACT §9 is still to be applied to Problem formulation.docx). The B-5 statement is limited to the registered cross-check. "The three evaluators" (Section 3.5.1 uses it for M1, M2, M3) is replaced by the rungs of the fidelity ladder; Section 4.3 gives conditions, Section 5 measures frequencies. The operational-lever paragraph now says why clustered dispatch is an operational reference in this model and matches the registered G1 companion (closed-form values side by side, each with its scale, not ranked). Equation (57) ends without a period, and Reg is described as a relative excess.

**R. Theorem 1 (2026-09-27).** After the author's verification (MATH_VERIFICATION_LOG rows 4 to 12), "Proposition 3" is renamed "Theorem 1" in the manuscript text of this file (2 English and 2 Chinese occurrences); older labels in the notes above are kept as written.
