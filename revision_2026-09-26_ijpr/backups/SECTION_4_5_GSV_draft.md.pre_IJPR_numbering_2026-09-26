---
title: "Section 4.5 draft: generate, screen, and verify release procedure (with Algorithm 1)"
date: 2026-09-26
status: "DRAFT for author review. Inserted into Methodology.docx with tracked changes (author authorization of 2026-09-26: §4 supplements by track changes). Equations are placeholders for MathType; their numbers are set after the remainder of §4.3.2 and §4.4 are inserted."
sources: "STORY_CONTRACT.md §3 (C3 wording) and §8 (wording rules); paper_draft/phase6_method_study_protocol.md §3.4, §3.5, §5, §7.1; TERMINOLOGY.md; Section 3 Eqs. (1), (16), (17); Section 4.3 Proposition 3"
notation: "Checked on 2026-09-26 against the FINAL Section 3 (Problem formulation.docx; bilingual mirror revision_2026-09-24/section3_bilingual_2026-09-24.md) and the current Section 4 (revision_2026-09-02/SECTION_4_METHODOLOGY.md). New symbols, all unused there: the augmented pool K+ with parts K^seq and K^con (k indexes candidates as in Section 3; G_tau is a trip's request group in Section 4; a superscript C could read as a complement or as the C axis), the screening key psi_k (s_o is a source floor), the shortlist K^V of size K_V (Section 3 uses calligraphic S for its option set, Table 3.3 and Equation (32); K = |K| is the pool size), the released candidate k^dagger, the screening regret Reg(K_V) (r_o is a ready offset), the smallest adequate size K_V^star, and M_2^DES for the event-driven evaluator (E is the number of elevators). Prose names: shortlist size = k and screening regret = r(k) in the protocol, the code, and TERMINOLOGY."
---

# 4.5 Generate, screen, and verify release procedure / 生成、筛选、验证释放流程

The class-selection procedure of Section 4.1 releases a wave drawn from a class, and every such rule is bounded by the pool optimum of Equation (17). This section describes a release procedure that works with individual candidates instead. It generates candidate waves, screens them with a closed-form evaluator, and verifies a short list with an event-driven evaluator before release. The dispatch rule of Section 3 stays fixed; the procedure changes only the released wave, that is, its order set and its processing sequence.

> **中文：** 第 4.1 节的类别选择流程从某个类别中抽取释放波次，而任何此类规则都以式 (17) 的池内最优为界。本节给出一个直接面向单个候选波次的释放流程：先生成候选波次，再用闭式评估器筛选，最后在释放前用事件驱动评估器验证一个短名单。第 3 节的调度规则保持不变，流程只改变释放的波次，即其订单集合与处理序列。

The generate, screen, and verify (GSV) procedure has three steps (Algorithm 1). The generation step adds to the random pool candidates designed around the co-occupancy mechanism of Section 4.3. The screening step ranks every candidate with a closed-form evaluator, which is inexpensive enough to apply to thousands of candidates. The verification step evaluates the best-ranked candidates with an event-driven evaluator, in which AMRs act concurrently, and releases the best of them. The closed-form evaluators therefore serve as a filter, and the event-driven evaluator makes the final choice.

> **中文：** 生成、筛选、验证（GSV）流程分为三步（算法 1）。生成步骤在随机候选池之外，加入围绕第 4.3 节同乘机制设计的候选。筛选步骤用闭式评估器为全部候选排序，其计算代价低到足以处理数千个候选。验证步骤用 AMR 并发运行的事件驱动评估器评价排名靠前的候选，并释放其中最好的一个。因此，闭式评估器起过滤作用，最终选择由事件驱动评估器作出。

## 4.5.1 Candidate generation / 候选生成

The augmented pool is

> **中文：** 扩充后的候选池为

$$
\mathcal K^{+}=\mathcal K\,\cup\,\mathcal K^{\mathrm{seq}}\,\cup\,\mathcal K^{\mathrm{con}}. \qquad \text{[Eq. GSV-1]}
$$

Its first part is the random pool \(\mathcal K\) of Section 3.3.1 with the recorded sequences \(\pi^k\). The second part, \(\mathcal K^{\mathrm{seq}}\), re-sequences each random candidate. The sequence-aware re-ordering keeps the order set \(W^k\) and changes only the sequence. It groups orders with the same source and destination floors into blocks of at most \(c\) orders, so that their elevator requests can share an \(M_2\) trip. It then orders the blocks by readiness and, among equally ready blocks, links each block's destination floor to the source floor of the next block, which reduces empty repositioning. The third part, \(\mathcal K^{\mathrm{con}}\), contains \(K'\) candidates from a co-ride-aware constructive generator. Starting from a random cross-floor order, the generator repeatedly adds the order that completes a partly filled co-ride block, connects to a source or destination floor already in the wave, and introduces the fewest new floors. Each constructed order set is then sequenced by the same re-ordering. Both operators target the mechanism isolated in Section 4.3: requests with the same source and destination that arrive within one loading window share a trip under \(M_2\), and linked floors shorten repositioning. Appendix X specifies both operators, including their tie rules.

> **中文：** 候选池的第一部分是第 3.3.1 节的随机候选池 \(\mathcal K\)，保留记录序列 \(\pi^k\)。第二部分 \(\mathcal K^{\mathrm{seq}}\) 对每个随机候选重新排序：序列感知重排保持订单集合 \(W^k\) 不变，只改变序列。它把起讫楼层相同的订单按不超过 \(c\) 个一组分块，使其电梯请求能够共享同一 \(M_2\) 行程；再按就绪时间为各块排序，并在就绪时间相同的块之间，让前一块的目的楼层衔接下一块的起始楼层，以减少空驶调位。第三部分 \(\mathcal K^{\mathrm{con}}\) 包含同乘感知构造生成器产生的 \(K'\) 个候选：从一个随机的跨楼层订单出发，生成器逐次加入能补全未满同乘块、与波次中已有起讫楼层相衔接、且新增楼层最少的订单；每个构造出的订单集合再用同一重排方法确定序列。两个算子都针对第 4.3 节分离出的机制：在 \(M_2\) 下，起讫相同且在同一装载窗口内到达的请求共享行程，楼层衔接则缩短调位。附录 X 给出两个算子的完整规则（含并列处理）。

## 4.5.2 Closed-form screening / 闭式筛选

Each candidate \(k\in\mathcal K^{+}\) is scored in closed form as in Equation (16), \(\ell_{km}=C_{\max}(W^k,\pi^k;m)\) for \(m\in\mathcal M_D\). The screening key is the \(M_2\) score,

> **中文：** 每个候选 \(k\in\mathcal K^{+}\) 按式 (16) 以闭式计算得分 \(\ell_{km}=C_{\max}(W^k,\pi^k;m)\)，\(m\in\mathcal M_D\)。筛选键取 \(M_2\) 得分：

$$
\psi_k=\ell_{kM_2},\qquad k\in\mathcal K^{+}. \qquad \text{[Eq. GSV-2]}
$$

This choice applies the robust objective of Section 3.4.2 to single candidates.

> **中文：** 这一选择是把第 3.4.2 节的鲁棒目标用于单个候选的结果。

**Candidate-level reduction.** For any candidate set \(\mathcal K'\subseteq\mathcal K^{+}\) on which \(\ell_{kM_1}\le\ell_{kM_2}\) holds for every candidate,

> **中文：** **候选层面的简化。** 对任一候选集合 \(\mathcal K'\subseteq\mathcal K^{+}\)，若其中每个候选都满足 \(\ell_{kM_1}\le\ell_{kM_2}\)，则

$$
\arg\min_{k\in\mathcal K'}\ \max_{m\in\mathcal M_D}\ \ell_{km}
=\arg\min_{k\in\mathcal K'}\ \ell_{kM_2}. \qquad \text{[Eq. GSV-3]}
$$

**Proof.** The ordering gives \(\max_{m\in\mathcal M_D}\ell_{km}=\ell_{kM_2}\) for every \(k\in\mathcal K'\), so both minimizations have the same objective. \(\square\)

> **中文：** **证明。** 排序关系使每个 \(k\in\mathcal K'\) 都有 \(\max_{m\in\mathcal M_D}\ell_{km}=\ell_{kM_2}\)，两个最小化问题的目标函数相同。\(\square\)

Proposition 3 gives sufficient conditions for the per-candidate ordering, and Section 4.3.2 identifies the two mechanisms that can reverse it. Where reversals are more likely, as on candidates built to create shared trips, the procedure can screen with the minimax key \(\psi_k=\max_{m\in\mathcal M_D}\ell_{km}\) instead; Section 5 states which key the registered study uses and the rule that decides it. Ties in \(\psi_k\) are broken by a fixed random order of the candidates. Candidates with the same sequence of source floors, destination floors, and ready offsets receive the same score from every evaluator, so they count once. The shortlist \(\mathcal K^{\mathrm V}\) contains the first \(K_{\mathrm V}\) distinct sequences in increasing order of \(\psi_k\).

> **中文：** 命题 3 给出逐候选排序成立的充分条件，第 4.3.2 节则指出可能使其反转的两种机制。在反转更可能出现的候选上（例如为制造共享行程而构造的候选），流程可以直接改用极小极大筛选键 \(\psi_k=\max_{m\in\mathcal M_D}\ell_{km}\)；第 5 节说明登记研究采用哪个筛选键以及决定它的规则。\(\psi_k\) 相同时按一个固定的随机顺序处理。起始楼层、目的楼层与就绪偏移序列完全相同的候选在所有评估器下得分相同，只计一次。短名单 \(\mathcal K^{\mathrm V}\) 由按 \(\psi_k\) 升序排列的前 \(K_{\mathrm V}\) 个不同序列组成。

## 4.5.3 Event-driven verification and release / 事件驱动验证与释放

The closed-form evaluators of Section 3.5 process the recorded sequence one order at a time, assigning each order to the earliest available AMR. The verification evaluator executes the same \(M_2\) rules as an event-driven simulation. AMRs claim orders in the recorded sequence, act concurrently, wait for each order's ready time, and request elevators in time order; a request boards an open trip with the same source and destination while its loading window is open, and otherwise takes the earliest available car. We denote this evaluator by \(M_2^{\mathrm{DES}}\) and its makespan by \(\ell_{kM_2^{\mathrm{DES}}}\). The procedure evaluates every shortlisted candidate and releases

> **中文：** 第 3.5 节的闭式评估器沿记录序列逐个处理订单，把每个订单指派给最早可用的 AMR。验证评估器以事件驱动仿真的方式执行同一套 \(M_2\) 规则：AMR 按记录序列认领订单并发运行，等待各订单就绪，按请求时间先后使用电梯；若存在起讫楼层相同、装载窗口尚未关闭的在途行程，请求即加入该行程，否则使用最早可用的轿厢。该评估器记为 \(M_2^{\mathrm{DES}}\)，其完工期记为 \(\ell_{kM_2^{\mathrm{DES}}}\)。流程评价短名单中的每个候选，并释放

$$
k^{\dagger}\in\arg\min_{k\in\mathcal K^{\mathrm V}}\ \ell_{kM_2^{\mathrm{DES}}}, \qquad \text{[Eq. GSV-4]}
$$

with ties broken by the same fixed order. The screening regret

> **中文：** 并列时仍按同一固定顺序处理。筛选遗憾

$$
\operatorname{Reg}(K_{\mathrm V})=\frac{\ell_{k^{\dagger}M_2^{\mathrm{DES}}}-\min_{k\in\mathcal K^{+}}\ell_{kM_2^{\mathrm{DES}}}}{\min_{k\in\mathcal K^{+}}\ell_{kM_2^{\mathrm{DES}}}} \qquad \text{[Eq. GSV-5]}
$$

measures how much of the value available in \(\mathcal K^{+}\) under the verification evaluator the shortlist retains. Because the shortlists are nested, \(\operatorname{Reg}(K_{\mathrm V})\) does not increase with \(K_{\mathrm V}\), and it is zero once \(\mathcal K^{\mathrm V}\) contains every distinct sequence. The smallest shortlist size whose regret falls within a stated tolerance, \(K_{\mathrm V}^{\star}\), indicates how far closed-form screening can be trusted as a filter for the verification evaluator; Section 5 estimates \(\operatorname{Reg}(K_{\mathrm V})\) and \(K_{\mathrm V}^{\star}\).

> **中文：** 衡量短名单在验证评估器下保留了 \(\mathcal K^{+}\) 中多少可得价值。由于短名单彼此嵌套，\(\operatorname{Reg}(K_{\mathrm V})\) 随 \(K_{\mathrm V}\) 增大而不增加，并在 \(\mathcal K^{\mathrm V}\) 包含全部不同序列时为零。筛选遗憾落在给定容差内的最小短名单规模 \(K_{\mathrm V}^{\star}\) 表明：闭式筛选在多大程度上可以作为验证评估器的过滤器。第 5 节估计 \(\operatorname{Reg}(K_{\mathrm V})\) 与 \(K_{\mathrm V}^{\star}\)。

Per released wave, the procedure uses \(|\mathcal K^{+}|\) closed-form evaluations under \(M_2\) (and under \(M_1\) for candidates screened with the minimax key) and \(K_{\mathrm V}\) event-driven evaluations. The three evaluators thus form a fidelity ladder. \(M_1\) and \(M_2\) filter candidates quickly, and \(M_2^{\mathrm{DES}}\) makes the final choice. Section 4.3 determines which closed-form evaluator is the conservative filter. The regret \(\operatorname{Reg}(K_{\mathrm V})\) measures how well that filter ranks candidates for the verification evaluator.

> **中文：** 每释放一个波次，流程需要 \(|\mathcal K^{+}|\) 次 \(M_2\) 闭式评价（采用极小极大筛选键的候选还需 \(M_1\) 评价）和 \(K_{\mathrm V}\) 次事件驱动评价。三个评估器由此构成保真阶梯：\(M_1\) 与 \(M_2\) 快速过滤候选，\(M_2^{\mathrm{DES}}\) 作最终选择。第 4.3 节决定哪一个闭式评估器是保守的过滤器，\(\operatorname{Reg}(K_{\mathrm V})\) 则衡量该过滤器为验证评估器排序候选的准确程度。

## Algorithm 1 / 算法 1

```
Algorithm 1. Generate, screen, and verify (GSV) release of one wave
Input:  order pool O; wave size n; car capacity c; numbers of random and
        constructed candidates K and K'; shortlist size K_V; fixed tie order
Output: released wave (W, pi)

 1: Draw K random candidates (W^k, pi^k) as in Section 3.3.1                  (generate)
 2: For each random candidate, form its sequence-aware re-ordering
 3: Build K' candidates with the co-ride-aware constructive generator;
    sequence each by the same re-ordering
 4: K+ <- random, re-ordered, and constructed candidates
 5: For every k in K+, compute the screening key psi_k (Eq. GSV-2),             (screen)
    or the minimax key for candidates screened with it
 6: Rank K+ by psi_k, ties by the fixed order; K^V <- the first K_V distinct sequences
 7: For every k in K^V, evaluate l_k under M2-DES                                  (verify)
 8: Release the k in K^V with the smallest l_k, ties by the fixed order (Eq. GSV-4)
```

> **中文：** 算法 1. 用"生成、筛选、验证"（GSV）释放一个波次。输入：订单池、波次规模 \(n\)、轿厢容量 \(c\)、随机与构造候选数 \(K\) 与 \(K'\)、短名单规模 \(K_{\mathrm V}\)、固定的并列顺序。输出：释放的波次 \((W,\pi)\)。第 1 至 4 行生成候选；第 5、6 行筛选；第 7、8 行验证并释放。

Algorithm 1 lists the steps for one wave. Lines 1 to 4 build the augmented pool of Equation (GSV-1). Line 2 leaves every order set unchanged, so the re-ordered candidates isolate the effect of the processing sequence, and line 3 adds order sets chosen for co-occupancy. Line 5 is the only step that touches every candidate, which is why it uses a closed-form evaluator. Line 6 counts distinct sequences, so the verification budget is not spent on duplicates, which constructed candidates in particular can produce. Lines 7 and 8 spend the event-driven evaluations only on the shortlist. The fixed tie order in lines 6 and 8 makes the released wave reproducible and prevents any candidate source from being favored by its position. When waves are released consecutively, each evaluation in lines 5 and 7 is made after the waves already released, so that AMR and elevator states carry over; Section 5 describes this warm-start use.

> **中文：** 算法 1 列出释放一个波次的步骤。第 1 至 4 行构建式 (GSV-1) 的扩充候选池。第 2 行不改变任何订单集合，因此重排候选单独体现处理序列的作用；第 3 行加入为同乘而挑选的订单集合。第 5 行是唯一需要处理全部候选的步骤，所以采用闭式评估器。第 6 行按不同序列计数，避免验证预算花在重复候选上（构造候选尤其容易重复）。第 7、8 行只对短名单使用事件驱动评价。第 6、8 行的固定并列顺序使释放结果可复现，也避免任何候选来源因排列位置而占优。连续释放多个波次时，第 5、7 行的每次评价都在已释放波次之后进行，使 AMR 与电梯状态得以延续；第 5 节说明这种热启动用法。

---

## Notes for the author (not for the manuscript)

1. **Equations to create in MathType** (placeholders in Word are highlighted and carry a comment): GSV-1 to GSV-5 above. Their numbers follow the last equation of §4.4 once the remainder of §4.3.2 (current md Eq. 47) and §4.4 (md Eqs. 48 to 58, subject to the IJPR renumbering in MASTER §00.5) are inserted; with the md numbering unchanged they would be (59) to (63).
2. **Label of the candidate-level reduction.** In the proposed IJPR numbering (MASTER §00.5) it becomes Corollary 1(b), with Theorem 2's class-level statement as Corollary 1(a). Until that numbering is confirmed it is a bold run-in paragraph.
3. **Symbols.** \(\mathcal K^{+}\), \(\mathcal K^{\mathrm{seq}}\), \(\mathcal K^{\mathrm{con}}\), \(\psi_k\), \(\mathcal K^{\mathrm V}\), \(K_{\mathrm V}\), \(k^{\dagger}\), \(\operatorname{Reg}(K_{\mathrm V})\), \(K_{\mathrm V}^{\star}\), and \(M_2^{\mathrm{DES}}\) are new and unused in the final Section 3 (the `Problem formulation.docx` text, mirrored in `revision_2026-09-24/section3_bilingual_2026-09-24.md`) and in the current Section 4. The first two drafts were checked against the superseded `SECTION_3_MODEL_FORMULATION.md` (now in `archive/revision_2026-09-02/`); the final Section 3 uses \(\mathcal S\) for the option set of Table 3.3 and Equation (32), so the shortlist is now \(\mathcal K^{\mathrm V}\), whose size is \(K_{\mathrm V}\). The same check shows that \(\delta\) is free in the final Section 3; \(\operatorname{Reg}(K_{\mathrm V})\) is kept because it names the quantity, and \(r\) and \(k\) are taken (\(r_o\), the candidate index). A superscript C on \(\mathcal K\) could be read as a complement or as the C axis, hence \(\mathcal K^{\mathrm{con}}\). \(K\) is the pool size \(|\mathcal K|\) of Section 3, so \(K'\) and \(K_{\mathrm V}\) follow the same convention for counts. \(k^{\dagger}\) and \(K_{\mathrm V}^{\star}\) reuse the decorations of \(m^{\dagger}\) and \(q^{\star}\) in Section 4 for a distinguished member and a selected value. In the protocol, the code, and TERMINOLOGY the shortlist size is called k and the screening regret r(k).
4. **"Appendix X"** is the appendix that will hold the exact P10 and P11 rules (protocol §5.1 and §5.3). Replace X when the appendix letters are fixed (plan v2 §2).
5. **Pointers needing destinations:** Section 3.5 (closed-form evaluators) exists; "Section 5" (registered key rule, warm start, \(\operatorname{Reg}(K_{\mathrm V})\), \(K_{\mathrm V}^{\star}\)) is written after Study 2.
6. **Wording checks done:** C3 wording of STORY_CONTRACT §3; no claim that the constructor adds value (STORY_CONTRACT §8 rule C3 decides that after Study 2); "sequence-aware re-ordering" and "co-ride-aware constructive generator" as in TERMINOLOGY; no "optimal", no em dash, American spelling; the dispatch rule stays fixed.
