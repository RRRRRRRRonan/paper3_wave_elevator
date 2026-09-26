---
title: "W7: Related-works insertion (Wang, Tao & Yang 2025) + publication-scale Contributions paragraph"
date: 2026-07-08
sources_consulted:
  - "paper_draft/RelatedWorks/related_works_v1.0.md (full)"
  - "paper_draft/references_related_works.bib"
  - "paper_draft/Introduction/introduction_v1.0.md"
  - "novelty_analysis_and_contribution.md (section 11.2, outdated prototype-scale contributions paragraph)"
  - "paper_draft/storyline_motivation_to_contribution_v1.md (sections 5-6)"
  - "paper_draft/section5_draft_v0_1.md (number verification: 99.2%, 96.0%, 72/72, 57/72, 71.7%, AUC 0.92, six-configuration Block C)"
  - "paper_draft/TERMINOLOGY.md"
  - "scratchpad/readers_literature.json (audit: Wang, Tao & Yang 2025 finding; four-qualifier novelty verdict)"
status: "draft for author review"
scale_note: "All numbers in the AFTER texts are publication scale (Phase 5, v0_5, 18 configurations, 106,800 simulations). No prototype-scale (v0_2) numbers appear."
integration_note_2026_07_08: >
  AMENDMENT A-R1 (executed after this draft) fired its locked rule: the
  capacity-dominance reading is metric- and partition-conditional. In Edit
  6's Contributions block, the C3 sentence quoting "H_up about 72% of mean
  GAP" must add the qualifier "(Phi-rule share at the 2x2 partition; the
  share is regime-dependent under alternative partitions and metrics,
  Section 5.2)". Do not paste the block without this qualifier; see
  revision_2026-07-08/tables/T5_partition_sensitivity.md for the numbers.
---

# W7 修订文档：插入 Wang, Tao & Yang (2025) + 出版规模贡献段落

本文档包含 6 处编辑与 1 条标记说明。编辑 1 至 4 处理审计发现的文献缺口
(readers_literature.json: Wang, Tao & Yang 2025, threat = medium)；编辑 5 为新增
BibTeX 条目；编辑 6 为出版规模的 Contributions 段落，替换 Introduction 现有贡献
段落并同时取代 novelty 文档 11.2 节的原型规模段落；最后一节列出旧段落所在位置，
供作者标记为"已被取代"。所有 AFTER 文本均无破折号；数字全部为出版规模。

---

# Edit 1: Related Works 第 2 节（英文版）P2 段落，软化"限制在单层"表述并插入 Wang, Tao & Yang (2025)

Source: `f:\Paper 3\paper_draft\RelatedWorks\related_works_v1.0.md`, English version, approximately lines 141-156.

## 修改前 (BEFORE)

> Multi-story Robotic Mobile Fulfillment Systems (RMFS) and tier-captive shuttle
> systems make vertical transport explicit, but typically decouple tiers by
> confining shuttles or pods to a tier, or by modeling the lift as an exogenous
> queue, with the task set given. Wu et al. (2024) schedule inbound jobs in a
> four-way shuttle system; Tadumadze et al. (2023) assign orders and pods to
> picking stations in a multi-level RMFS; Lamballais, Roy and De Koster (2017)
> give queueing estimates of RMFS performance. On the shuttle-based
> storage-and-retrieval (SBS/RS) side, Tappia et al. (2017) provide the canonical
> queueing model of multi-tier compact storage with lifts, and Chen et al. (2023)
> schedule retrieval requests under two lifts to minimize makespan (the closest
> published analogue to ours, but operational, with the task set given, and for
> SBS/RS rather than floor-bound AMRs); more recent integrated work (Wu et al.,
> 2025) still optimizes picking and replenishment within a single tier. Our delta
> is to treat the cross-tier lift coupling as something an upstream tactical
> decision, wave composition, can manage, rather than decoupling the tiers to
> avoid it.

## 修改后 (AFTER)

Multi-story Robotic Mobile Fulfillment Systems (RMFS) and multi-tier shuttle
systems make vertical transport explicit, but most decouple tiers by confining
shuttles or pods to a tier, or by modeling the lift as an exogenous queue, with
the task set given. Wu et al. (2024) schedule inbound jobs in a four-way shuttle
system; Tadumadze et al. (2023) assign orders and pods to picking stations in a
multi-level RMFS; Lamballais, Roy and De Koster (2017) give queueing estimates
of RMFS performance. On the shuttle-based storage-and-retrieval (SBS/RS) side,
Tappia et al. (2017) provide the canonical queueing model of multi-tier compact
storage with lifts, and Chen et al. (2023) schedule retrieval requests under two
lifts to minimize makespan (the closest published analogue to ours, but
operational, with the task set given, and for SBS/RS rather than floor-bound
AMRs); more recent integrated work (Wu et al., 2025) still optimizes picking and
replenishment within a single tier. A recent exception to tier confinement is
Wang, Tao and Yang (2025), who schedule retrievals in a four-directional
shuttle-based compact storage and retrieval system whose tier-to-tier shuttles
traverse tiers via two shared, heterogeneous lift types (shuttle lifts and bin
lifts), jointly deciding request sequencing and the coordinated shuttle and lift
schedules that minimize makespan, combining logic-based Benders decomposition
with adaptive large neighborhood search and tabu search. The decision layer,
however, is unchanged: the work remains at the operational stage, its
retrieval-request set is exogenous, no wave-composition decision exists
upstream, and its tier-to-tier shuttles are storage-and-retrieval devices rather
than a floor-bound AMR fleet contending for building-level freight elevators.
Our delta is to treat the cross-tier lift coupling as something an upstream
tactical decision, wave composition, can manage, rather than a contention to be
rescheduled after the request set is fixed.

## 理由 (RATIONALE)

审计 readers_literature.json 发现 Wang, Tao & Yang (2025, C&IE, article
S0360835225007053, 2025 年 10 月见刊) 未收录于任何阅读日志或 bib 文件，而它发表在
本文的目标期刊上，且与 Qin et al. (2024) 共享末位作者 (P. Yang)，C&IE 审稿人很
可能知道它 (threat = medium)。其跨层四向穿梭车经由共享异构升降机在层间穿行，直接
削弱了原句"typically decouple tiers by confining shuttles or pods to a tier"的
概括，故将 "typically" 软化为 "most" 并显式引入该例外。差异化沿审计给出的四点：
仍属操作层、检索请求集外生、无波次构成决策、穿梭车不是楼面 AMR 机队。段尾
"Our delta" 句同步改写，因为"靠分层解耦来回避"已不再覆盖 Wang et al. 这一例外。

---

# Edit 2: Related Works 第 2 节（中文版）对应段落

Source: `f:\Paper 3\paper_draft\RelatedWorks\related_works_v1.0.md`, 中文版, approximately lines 48-57.

## 修改前 (BEFORE)

> 多层机器人移动履行系统(RMFS)与分层穿梭系统让垂直运输显式出现,但通常通过把
> 穿梭车或料箱限制在单层、或把电梯当作外生队列来解耦各层,且任务集给定。Wu et al.
> (2024) 研究四向穿梭系统的入库作业调度;Tadumadze et al. (2023) 研究多层 RMFS 的
> 订单与料箱到工作站分配;Lamballais, Roy and De Koster (2017) 给出 RMFS 性能的
> 排队估计。在分层存取系统(SBS/RS)一侧,Tappia et al. (2017) 给出含升降机的多层
> 紧凑存储的经典排队模型,Chen et al. (2023) 研究双升降机下的检索请求调度以最小化
> makespan(这是与我们最接近的已发表类比,但属操作层、任务集给定、且为 SBS/RS 而非
> 楼面 AMR);更新的整合式工作(Wu et al., 2025)仍是单层内的拣选与补货联合优化。
> 我们的差别是:把跨层的电梯耦合视为一个上游战术决策(波次构成)可以管理的对象,
> 而非靠分层解耦来回避。

## 修改后 (AFTER)

多层机器人移动履行系统(RMFS)与多层穿梭系统让垂直运输显式出现,但多数通过把
穿梭车或料箱限制在单层、或把电梯当作外生队列来解耦各层,且任务集给定。Wu et al.
(2024) 研究四向穿梭系统的入库作业调度;Tadumadze et al. (2023) 研究多层 RMFS 的
订单与料箱到工作站分配;Lamballais, Roy and De Koster (2017) 给出 RMFS 性能的
排队估计。在分层存取系统(SBS/RS)一侧,Tappia et al. (2017) 给出含升降机的多层
紧凑存储的经典排队模型,Chen et al. (2023) 研究双升降机下的检索请求调度以最小化
makespan(这是与我们最接近的已发表类比,但属操作层、任务集给定、且为 SBS/RS 而非
楼面 AMR);更新的整合式工作(Wu et al., 2025)仍是单层内的拣选与补货联合优化。
一个近期的例外是 Wang, Tao and Yang (2025):其四向穿梭紧凑存取系统中,跨层穿梭车
经由两类共享的异构升降机(穿梭车升降机与料箱升降机)在层间穿行,以逻辑 Benders
分解结合自适应大邻域搜索与禁忌搜索,联合决定检索请求排序与穿梭车、升降机的协同
调度以最小化 makespan。但其决策层次未变:仍属操作层,检索请求集外生给定,上游
不存在波次构成决策,其跨层穿梭车是存取器件而非争用楼宇级货梯的楼面 AMR 机队。
我们的差别是:把跨层的电梯耦合视为一个上游战术决策(波次构成)可以管理的对象,
而非在请求集固定之后再去重排的争用。

## 理由 (RATIONALE)

与编辑 1 完全平行,保持双语版本一致("通常"改"多数",插入例外并同步改写段尾
差别句)。中文段落按 TERMINOLOGY 第 9 节规则不含数学符号、不含破折号;保留
专名 (Benders, makespan, SBS/RS, AMR)。

---

# Edit 3: Introduction 第 1 节（英文版）四要素缺口句软化

Source: `f:\Paper 3\paper_draft\Introduction\introduction_v1.0.md`, English version, approximately lines 116-132 (the four-element gap paragraph; only the precedent sentences change).

## 修改前 (BEFORE)

> Four elements, namely wave composition, multi-story deployment, flexible AMR
> fleets, and shared-elevator capacity, have largely been studied in isolation.
> The closest precedents treat the lift as a constraint under fixed wave content
> (Chakravarty et al., 2025) or batch orders inside a single vertical lift module (VLM) (Lenoble et al., 2018);
> multi-story Robotic Mobile Fulfillment System (RMFS) work avoids the coupling by
> confining shuttles to a tier (Wu et al., 2024); planar AMR work optimizes wave
> cardinality on a single floor (Qin et al., 2024). Each of these precedents sidesteps the
> coupling by restricting the setting: fixing the wave content, or confining
> transport to a single device or a single tier.

## 修改后 (AFTER)

Four elements, namely wave composition, multi-story deployment, flexible AMR
fleets, and shared-elevator capacity, have largely been studied in isolation.
The closest precedents treat the lift as a constraint under fixed wave content
(Chakravarty et al., 2025) or batch orders inside a single vertical lift module
(VLM) (Lenoble et al., 2018); multi-story Robotic Mobile Fulfillment System
(RMFS) and shuttle work mostly avoids the coupling by confining shuttles to a
tier (Wu et al., 2024), and where recent work does let tier-to-tier shuttles
traverse tiers via shared heterogeneous lifts (Wang et al., 2025), its
retrieval-request set remains exogenous; planar AMR work optimizes wave
cardinality on a single floor (Qin et al., 2024). Each of these precedents
sidesteps the coupling by restricting the setting: fixing the wave content or
the request set, or confining transport to a single device or a single tier.

## 理由 (RATIONALE)

Introduction 中同样存在"confining shuttles to a tier"的无例外概括,与 Related
Works 的软化必须同步,否则两节自相矛盾。审计指出 Wang, Tao & Yang (2025) 的跨层
穿梭车部分推翻该概括 (readers_literature.json caveat (c)),但其请求集外生这一点
恰好强化了本文的缺口主张:即便升降机耦合被显式建模,波次构成仍无人作为决策变量。
总结句从"fixing the wave content"扩为"fixing the wave content or the request
set",使 Wang et al. 也被四要素缺口逻辑覆盖。四要素缺口主张本身
(four-qualifier form) 经审计确认在 2026 年 7 月仍然成立,无需改动。

---

# Edit 4: Introduction 第 1 节（中文版）对应句

Source: `f:\Paper 3\paper_draft\Introduction\introduction_v1.0.md`, 中文版, approximately lines 28-38 (only the precedent sentences change; the remainder of the paragraph is unchanged).

## 修改前 (BEFORE)

> 波次构成、多层部署、灵活 AMR 机队、共享电梯运力这四个要素,以往大多被分开研究。
> 最接近的先例要么把电梯当作固定波次内容下的约束(Chakravarty et al., 2025),要么
> 在单个垂直升降模块(VLM)内部做分批(Lenoble et al., 2018);多层机器人移动履行
> 系统(RMFS)的工作
> 通过把穿梭车限制在单层来回避耦合(Wu et al., 2024);平面 AMR 的工作只在单层上
> 优化波次基数(Qin et al., 2024)。这些先例各自通过限制设定来绕开这一耦合:固定波次
> 内容,或把运输限制在单一器件或单一楼层。

## 修改后 (AFTER)

波次构成、多层部署、灵活 AMR 机队、共享电梯运力这四个要素,以往大多被分开研究。
最接近的先例要么把电梯当作固定波次内容下的约束(Chakravarty et al., 2025),要么
在单个垂直升降模块(VLM)内部做分批(Lenoble et al., 2018);多层机器人移动履行
系统(RMFS)与穿梭系统的工作多通过把穿梭车限制在单层来回避耦合(Wu et al., 2024),
近期虽有工作让跨层穿梭车经由共享异构升降机在层间穿行(Wang et al., 2025),其检索
请求集仍是外生给定;平面 AMR 的工作只在单层上优化波次基数(Qin et al., 2024)。
这些先例各自通过限制设定来绕开这一耦合:固定波次内容或请求集,或把运输限制在
单一器件或单一楼层。

## 理由 (RATIONALE)

与编辑 3 平行,保持中英一致。中文版无数学符号、无破折号。

---

# Edit 5: 新增 BibTeX 条目 (references_related_works.bib)

Source: `f:\Paper 3\paper_draft\references_related_works.bib`. Insert in the "---- P2: multi-tier / RMFS / shared-lift ----" block, after the `chen2023retrieval` entry (around line 114) and before `wu2025joint`.

## 修改前 (BEFORE)

(no existing text; new entry)

## 修改后 (AFTER)

```bibtex
% NEW (revision 2026-07-08): found by literature audit; absent from all prior
% logs and bibs. NOT the same paper as the DROPPED fabricated "Wang et al. 2025"
% (sustainable RMFS pod repositioning; true authors Silva et al.) listed at the
% end of this file. Shares last author (P. Yang) with Qin, Kang & Yang (2024).
@article{wang2025retrieval,
  author  = {Wang, R. and Tao, P. and Yang, P.},
  title   = {Retrieval scheduling in four-directional shuttle-based compact storage and retrieval systems with heterogeneous lifts},
  journal = {Computers \& Industrial Engineering},
  year    = {2025},
  note    = {Article S0360835225007053}
  % CONFIRM before submission: DOI (resolve from Elsevier PII S0360835225007053;
  % published October 2025; earlier preprint SSRN 4798623), full author first
  % names, final volume and article number. Do not submit with the note field;
  % replace it with the resolved volume/article-number/DOI.
}
```

## 理由 (RATIONALE)

审计确认这是一篇真实存在、经网络检索验证的 C&IE 论文,但项目内所有 bib 与阅读
日志均未收录。条目使用姓名缩写而非猜测全名,DOI、卷号、文章号均按任务要求以
"% CONFIRM before submission" 标出,避免重蹈本项目此前"伪造署名"教训 (本 bib 文件
末尾 DROPPED 名单中已有一个不同的、被弃用的 "Wang et al. 2025",故加注区分,
bib key 采用 wang2025retrieval 以消歧)。

---

# Edit 6: 出版规模 Contributions 段落（替换 Introduction 英文版贡献段落）

Source: `f:\Paper 3\paper_draft\Introduction\introduction_v1.0.md`, English version, approximately lines 161-204. This AFTER text also supersedes the prototype-scale paragraph in `novelty_analysis_and_contribution.md` section 11.2 (see the final note below).

## 修改前 (BEFORE)

> This paper makes three contributions.
>
> **(C1) Problem formulation.** We formalize the wave-release coordination problem
> under vertical resource constraints as a two-stage scheduler in which a tactical
> stage composes waves and an operational stage delivers the released orders
> through shared elevators, the two stages coupled through shared elevator
> capacity. Prior work mostly sidesteps this coupling by simplifying the setting; our
> formulation models it explicitly.
>
> **(C2) Methodology.** We develop two analytical tools on the structured
> representation `Φ`. The first, the Bound-and-Gap decomposition (diagnostic),
> splits the value of wave design into a structural ceiling `H_up` that no policy
> acting on `Φ` can recover and a recoverable slack `M_Φ`; we prove (Theorem 1)
> that `M_Φ` is exactly a predict-then-optimize decision loss, the object studied
> as Smart-Predict-then-Optimize regret (Elmachtoub and Grigas, 2022), so it can
> be recovered with existing methods. The second, the
> Model-Dominance Hedge Rule (prescriptive), is a closed-form rule that selects
> which wave-structure to release from without identifying the true elevator model or solving a robust
> optimization program; we prove (Theorem 2) that, under a conditional per-wave
> dominance result we establish (Proposition 2), this simplest rule coincides
> exactly with the Wasserstein
> distributionally-robust optimum (Mohajerin Esfahani and Kuhn, 2018) and carries
> a computable worst-case-loss bound. The two tools act on the same representation
> and are complementary: the decomposition measures what a wave-structure choice
> is worth and how much is recoverable, while the Hedge Rule selects the robust
> one.
>
> **(C3) Validated insights.** We evaluate both tools in a pre-registered,
> large-scale simulation study (106,800 simulations across 18 configurations),
> and report each tool's outcome as it stands; the two differ. The
> Model-Dominance Hedge Rule passes
> every pre-registered gate: per-wave dominance holds in 99.2% of waves (96.0% in
> the worst cell) and across per-trip capacities `c ∈ {2,3,4,5}`, and its chosen
> structure matches the Wasserstein-DRO optimum in every configuration. The
> Bound-and-Gap identities hold exactly in all 72 sub-cells, with the
> capacity-side ceiling `H_up` accounting for about 72% of the mean value and
> dominating the smaller recoverable slack `M_Φ`; the statistical-resolution gate
> is met in 79% of sub-cells (a partial pass, one sub-cell short), and the
> unresolved sub-cells are those where the value is genuinely small, so the
> decomposition resolves wave-design value wherever that value is substantial. For
> these warehouses, the binding limitation on makespan is therefore predominantly
> capacity-side. This is precisely the tools' managerial payoff: they tell an
> operator, regime by regime, when smarter wave composition is worth the effort and
> when the lever is instead capacity or a finer partition.

## 修改后 (AFTER)

This paper makes three contributions.

**(C1) Problem formulation.** We formalize wave-release coordination under
vertical resource constraints as a two-stage scheduler: a tactical stage
composes waves; an operational stage dispatches a flexible AMR fleet through
shared freight elevators. Its four defining elements (wave composition as a
decision, multi-story deployment, a flexible AMR fleet, and shared elevator
capacity) have been studied only in isolation, with wave content or request set
fixed or transport confined to a single device or tier; our formulation models
the coupling explicitly.

**(C2) Methodology.** We develop two analytical tools on the wave representation
`Φ = (C, I, T)`. The Bound-and-Gap decomposition (diagnostic) splits the value
of wave structure, `GAP`, into a structural ceiling `H_up` that no wave-release
policy on `Φ` can recover and a recoverable slack `M_Φ`, with three
unconditional results: the decomposition identity (Proposition 1), the equality
of `M_Φ` and the predict-then-optimize decision loss of a partition-constant
predictor (Theorem 1; Elmachtoub and Grigas, 2022), and refinement monotonicity
of `H_up` (Corollary 1). The Model-Dominance Hedge Rule (prescriptive) selects
the wave-structure to release in closed form without identifying the true
elevator model: under the per-wave chain dominance we establish (Proposition 2),
minimax corner selection collapses to the corner optimal under true co-occupancy
batching and coincides with the Wasserstein distributionally-robust optimum
(Theorem 2; Mohajerin Esfahani and Kuhn, 2018), with a computable worst-case
bound `U_c(ε)` for approximate dominance (Corollary 2).

**(C3) Empirical capacity-versus-policy diagnosis.** A pre-registered
publication-scale study (18 configurations, 106,800 simulations) evaluates both
tools, verdicts reported as they stand. The Hedge Rule passes every gate:
per-wave dominance holds in 99.2% of waves (worst cell 96.0%) across the
six-configuration model-chain block; its corner matches the Wasserstein-DRO
optimum in all six configurations. Both Bound-and-Gap identities hold exactly in
all 72 sub-cells; `H_up` is about 72% of mean `GAP`; the resolution gate is met
in 57 of 72 (79%, reported as PARTIAL), and the unresolved sub-cells are
precisely the low-`GAP` ones (AUC 0.92), so the decomposition resolves value
wherever it is substantial. The binding limitation on makespan is thus
predominantly capacity-side: the tools tell an operator, regime by regime, when
smarter wave composition pays and when the lever is capacity or a finer
partition.

## 理由 (RATIONALE)

任务要求一段可同时取代 (a) Introduction 现有贡献段落与 (b) novelty 文档 11.2 节
原型规模段落的出版规模贡献陈述。相对现有 Introduction 版本的改动:C1 将四要素
缺口清单(四限定词形式,经审计确认成立)显式写入 C1 本体;C2 按 TERMINOLOGY 第 7
节把六个正式结果全部列入(命题 1 分解恒等式、定理 1 决策损失桥、推论 1 细化单调;
命题 2 链支配、定理 2 minimax 坍缩等于 Wasserstein-DRO、推论 2 最坏界),原版只列
两个定理;C3 补入任务指定的出版规模数字:逐波次支配 99.2% 归属于六配置模型链
区块(第 5 节 Block C)、恒等式 72/72 精确、分辨门槛 57/72 = 79% 如实报 PARTIAL
并配 AUC 0.92 的判别力框架。全部数字为出版规模 (Phase 5, v0_5),不含任何原型
规模数字;正文用"decision loss",不用"SPO regret"(该词保留给第 4 节正式陈述);
无破折号。正文词数约 350(shell 计数 358,其中数学记号约使计数偏高 8 至 10)。
原版中"across per-trip capacities c in {2,3,4,5}"因词数预算删去;如篇幅允许,
可在 C3 第二句句末以 "and across per-trip capacities `c ∈ {2,3,4,5}`" 恢复。

---

# 最后一条标记说明：旧的原型规模贡献段落所在位置（请标记为"已被取代"）

一行说明:旧的原型规模 (v0_2, M4/M5 命名) 贡献段落存在于两处,均应标注
"SUPERSEDED by revision_2026-07-08/tier1_manuscript/W7_relatedworks_contributions.md Edit 6 (publication scale)":
(1) `f:\Paper 3\novelty_analysis_and_contribution.md` 第 11.2 节 "v0.4 Contributions
paragraph (paste this into Paper 3)",约 617-637 行(其中 GAP 5.83%、92.5-100%、
3.1-9.9% 等均为原型规模数字,且使用已废弃的 "vertical concentration" 与
"C2-M4/C2-M5" 命名,绝不可再粘贴进论文);
(2) `f:\Paper 3\paper_draft\outline_v0_1.md` 第 2.4 节 "Contributions (paste from
§11.2; ~250 words)" 的 "paste verbatim" 指令,约 36 行与 68-70 行(该指令指向上述
过期段落,同样应作废)。

本文档依据任务授权只写入 revision_2026-07-08/tier1_manuscript/ 目录,未改动上述
两个文件;请作者自行添加取代标注。
