---
title: "Story contract (IJPR version)"
date: 2026-09-26
status: "SIGNED 2026-09-26，与 01_DECISIONS_TO_SIGN.md 一同签署；以英文为约束性原文；签字后不再改动。"
role: "全文唯一的故事契约。摘要、§1 到 §6、亮点、cover letter 都必须与本文件一致；与本文件冲突的旧稿句子一律按本文件改写。"
supersedes: "主控 MASTER_REVISION_BY_SECTION.md §2.2（贡献）、§2.3（研究问题）、§2.1（题目）；plan_section3_section4_v0_2.md §0 第 13 行的'两个简单可用的诊断工具'。"
keeps_in_force: "主控 §0.2 审计事实、§0.3 证据标签、§2.4 禁用表述、§1.4 冲突裁决；冻结的 Phase 5 预注册与 2026-07-08 的六份修正案。"
author_signoff: "SIGNED (Shiyue Hu, 2026-09-26). Authorization given by explicit author instruction in the 2026-09-26 working session, after the author's review of the pre-signing audit and its diffs; the assistant entered the signature at that instruction."
---

# Story contract (IJPR version)

> **中文：** 故事契约（IJPR 版）。
>
> **语言说明：** 本文件以英文为约束性原文；引用块中的中文译文仅供阅读，两者如有出入，以英文为准。

## 1. The paper in one sentence

> **中文：** 1. 一句话概括本文

**English.** In multi-story AMR warehouses whose fleet shares building freight elevators, this paper studies how to compose a release wave, what a wrong elevator model costs, and how much value a generate, screen, and verify release procedure recovers.

**中文。** 在 AMR 车队共享楼宇货梯的多层仓库里，本文研究怎样组成一个释放波次、电梯模型选错会付出什么代价，以及一个"生成、筛选、验证"的释放流程能拿回多少价值。

**Paper type.** Decision-aid paper with two studies: Study 1 is the preregistered diagnostic study (Phase 5; verdicts reported as locked); Study 2 is the registered method study (Phase 6 protocol).

> **中文：** **论文类型。** 决策辅助型论文，包含两个研究：研究一是预注册的诊断研究（Phase 5；判定按锁定的结果报告）；研究二是登记的方法研究（Phase 6 协议）。

## 2. Title candidates (decision D-E: fixed after Study 2)

> **中文：** 2. 题目候选（决定 D-E：研究二完成后确定）

1. Wave composition under shared elevators in multi-story AMR warehouses: elevator-model risk and a generate, screen, and verify release procedure
2. Composing AMR waves for shared freight elevators: abstraction bias, hedged screening, and mechanism-aware sequencing
3. Generate, screen, verify: wave composition under elevator-model uncertainty in multi-story AMR warehouses

> **中文：**
> 1. 多层 AMR 仓库中共享电梯下的波次组成：电梯模型风险与一个"生成、筛选、验证"的释放流程
> 2. 为共享货梯组成 AMR 波次：抽象偏差、对冲式筛选与机制感知的序列安排
> 3. 生成、筛选、验证：多层 AMR 仓库中电梯模型不确定下的波次组成

Rule (master §3.1): every action word in the title must have a decision variable in §3, a method in §4, and direct evidence in §5.

> **中文：** 规则（主控 §3.1）：题目中的每个动作词，都必须在 §3 有对应的决策变量、在 §4 有对应的方法、在 §5 有直接证据。

When the §8 C3 constructor rule drops "mechanism-aware", candidate 2 is excluded. Under scenario C of §8 the title is not taken from these candidates but follows the v1 plan framing.

> **中文：** 当 §8 的"C3 构造器"规则去掉 "mechanism-aware"（机制感知）时，候选 2 被排除。在 §8 的情景 C 下，题目不从这三个候选中选取，而是遵循 v1 计划的框架。

## 3. Contributions (the only version used anywhere)

> **中文：** 3. 贡献（全文任何地方只用这一版）

**C1. Problem and benchmark.** We formulate single-wave composition for a floor-confined AMR fleet that shares building freight elevators as a selection problem over candidate waves, where a candidate fixes both the order set and its processing sequence under a fixed dispatch rule. We construct a reproducible synthetic benchmark with three elevator evaluators and a primary median makespan metric.

> **中文：** **C1. 问题与基准。** 对于在楼层内行驶、跨层须共用楼宇货梯的 AMR 车队，我们把单个波次的组成问题表述为在候选波次上的选择问题：每个候选同时确定订单集合及其处理序列，调度规则固定不变。我们构建一个可复现的合成基准，包含三个电梯评估器，以完工期中位数为主要指标。

**C2. Elevator-model risk.** We prove a conditional sample-path ordering between the throughput abstraction and true co-occupancy batching for any number of elevators and any car capacity, identify the two reversal mechanisms, which are exhaustive under aligned sequences and AMR assignments, and quantify the resulting abstraction bias. The ordering makes screening candidates under the co-occupancy evaluator a conservative, minimax choice.

> **中文：** **C2. 电梯模型风险。** 我们证明吞吐能力抽象与真实同乘批运之间的条件性样本路径排序，对任意电梯数与任意轿厢容量成立；指出两种反转机制（它们在序列与 AMR 分配对齐时是穷尽的），并量化由此产生的抽象偏差。这一排序使得在同乘评估器下筛选候选成为保守的、极小极大意义下的选择。

**C3. A generate, screen, and verify release procedure.** We propose a release procedure that generates candidate waves with a mechanism-aware constructor, screens them in closed form under the co-occupancy evaluator, and verifies a shortlist by event-driven simulation. A registered computational study evaluates the procedure against random, class-based, heuristic, and search policies along a fidelity ladder from closed-form evaluators to event-driven simulation, on independent order pools and on a literature-calibrated case, and reports the preregistered class diagnostics as its validity boundary.

> **中文：** **C3. 生成、筛选、验证的释放流程。** 我们提出一个释放流程：用机制感知的构造器生成候选波次，在同乘评估器下以闭式方法筛选，再用事件驱动仿真验证短名单。一项登记的计算研究沿着从闭式评估器到事件驱动仿真的保真阶梯，在独立的订单池和基于文献校准的案例上，把该流程与随机、基于类别、启发式和搜索策略进行比较，并把预注册的类别诊断作为该流程的有效性边界加以报告。

Pricing rules:
- C2's theorem is the ordering result (currently Proposition 3 in SECTION_4_METHODOLOGY.md; becomes Theorem 1 only after Appendix A is assembled and read through by the author, TH-1).
- The minimax reduction is a corollary of the ordering, not a stand-alone theorem.
- Bound-and-Gap is introduced as a partition-relative diagnostic; the sentence introducing it states that its preregistered utility gate was not met (57/72 against 58/72) and that it is treated as a prototype-regime diagnostic (preregistration line 213).
- DRO appears once, as a remark with a pointer to Fu, Li and Zhang (2024). The U_c certificate appears once, as a boundary statement in §5.5.

> **中文：** 表述分寸规则（每项贡献说到什么程度）：
> - C2 的定理就是排序结果（目前为 SECTION_4_METHODOLOGY.md 中的命题 3；只有在附录 A 组装完成并经作者通读后才改称定理 1，见 TH-1）。
> - 极小极大化简是排序结果的推论，不是独立的定理。
> - Bound-and-Gap 作为相对于分区的诊断引入；引入它的那句话要写明，其预注册的效用门槛未达到（57/72，门槛为 58/72），并把它当作原型规模范围内的诊断（预注册第 213 行）。
> - DRO 只出现一次，以注的形式出现，并指向 Fu, Li and Zhang (2024)。U_c 证书只出现一次，作为 §5.5 中的边界陈述。

## 4. Research questions

> **中文：** 4. 研究问题

- **RQ1.** How much does wave composition affect makespan under shared elevators, and how much of that effect comes from the order set as opposed to the processing sequence?
- **RQ2.** Does the choice of elevator evaluator change the release decision, in which direction, and under what verifiable conditions is the co-occupancy evaluator the conservative choice?
- **RQ3.** How much of the composition value does a generate, screen, and verify procedure capture, how large a shortlist does event-driven verification need, and where do the closed-form diagnostics stop being reliable?

> **中文：**
> - **RQ1.** 在共享电梯下，波次组成对完工期的影响有多大？这一影响中，多少来自订单集合，多少来自处理序列？
> - **RQ2.** 电梯评估器的选择会不会改变释放决策？朝哪个方向改变？在哪些可以验证的条件下，同乘评估器是保守的选择？
> - **RQ3.** "生成、筛选、验证"流程能获得组成价值中的多少？事件驱动验证需要多大的短名单？闭式诊断从哪里开始不再可靠？

| RQ | Answered in | Evidence (tags) |
|---|---|---|
| RQ1 | §5.2 (Study 1 diagnostics), §5.3 (set versus sequence, sequence lever) | Block A/B [PR-C]; S1-1, S1-2, S1-5, S1-7, S1-8, S1-9, S1-11 (S1-11 only if D-D1 is signed) [RA]/[NS]/[QA]; Study 2 S2-1, S2-2 [NS] |
| RQ2 | §4.3 to §4.4 (theory), §5.2 (Block C), §5.3 (fidelity ladder, ordering on constructed waves) | H-D2 [PR-C]; S1-3, S1-4, S1-6, S1-12, TH-2 [NS]/[QA]/[RA]; Study 2 S2-5, S2-6 [NS] |
| RQ3 | §5.3 (GSV main experiment, screening regret, warm start, execution robustness), §5.4 (case), §5.5 (boundaries) | Study 2 S2-3, S2-4, S2-7, S2-8, S2-9, S2-10 [NS]; ICC, OOS, B-5 [NS]/[RA] |

> **中文：**
>
> | 研究问题 | 回答位置 | 证据（标签） |
> |---|---|---|
> | RQ1 | §5.2（研究一的诊断）、§5.3（订单集合与序列的比较、序列杠杆） | Block A/B [PR-C]；S1-1、S1-2、S1-5、S1-7、S1-8、S1-9、S1-11（S1-11 仅在 D-D1 签字时做）[RA]/[NS]/[QA]；研究二 S2-1、S2-2 [NS] |
> | RQ2 | §4.3 至 §4.4（理论）、§5.2（Block C）、§5.3（保真阶梯、构造波次上的排序） | H-D2 [PR-C]；S1-3、S1-4、S1-6、S1-12、TH-2 [NS]/[QA]/[RA]；研究二 S2-5、S2-6 [NS] |
> | RQ3 | §5.3（GSV 主实验、筛选遗憾、热启动、执行稳健性）、§5.4（案例）、§5.5（边界） | 研究二 S2-3、S2-4、S2-7、S2-8、S2-9、S2-10 [NS]；ICC、OOS、B-5 [NS]/[RA] |

Study 2 item numbers (S2-1 to S2-10) are defined in the Phase 6 protocol §1.1. The protocol's §1 restates the RQs in its own words; this contract's wording prevails.

> **中文：** 研究二的条目编号（S2-1 至 S2-10）在 Phase 6 协议 §1.1 中定义。协议 §1 用自己的话复述了各研究问题；以本契约的措辞为准。

## 5. Roles of the two studies

> **中文：** 5. 两个研究的角色

| | Study 1 | Study 2 |
|---|---|---|
| What it is | The preregistered Phase 5 diagnostic study plus registered re-analyses | The registered Phase 6 method study |
| Registration | Phase 5 preregistration (2026-05-19), amendments of 2026-07-08, registrations of 2026-09-26 | `paper_draft/phase6_method_study_protocol.md` |
| Verdict status | Locked verdicts never change; re-analyses reported beside them | Own gates and wording ladders, locked at signing |
| Role in the story | Shows what coarse class rules and closed-form diagnostics can and cannot do; motivates Study 2 | Delivers and tests the method |
| Borrowing rule | Study 1 results may motivate Study 2 but never confirm it; Study 2 results never re-judge Study 1 | Same |
| Conflicts | If the two point in opposite directions, both are reported with their scope; Study 1 verdicts stand; no averaging | Same |

> **中文：**
>
> | | 研究一 | 研究二 |
> |---|---|---|
> | 是什么 | 预注册的 Phase 5 诊断研究，加上登记的重分析 | 登记的 Phase 6 方法研究 |
> | 登记 | Phase 5 预注册（2026-05-19）、2026-07-08 的修正案、2026-09-26 的登记文件 | `paper_draft/phase6_method_study_protocol.md` |
> | 判定状态 | 锁定的判定永不改变；重分析与之并列报告 | 自有的门槛与措辞梯级，签字时锁定 |
> | 在故事中的角色 | 说明粗粒度的类别规则与闭式诊断能做什么、不能做什么；为研究二提供动机 | 交付并检验方法 |
> | 借用规则 | 研究一的结果可以为研究二提供动机，但永远不能证实它；研究二的结果永远不重新评判研究一 | 同左 |
> | 冲突 | 两者方向相反时，各自连同适用范围一并报告；研究一的判定不变；不取平均 | 同左 |

## 6. Section-by-section completion gates

> **中文：** 6. 各部分的完成标准

| Part | Done when |
|---|---|
| Abstract | Six-sentence logic (plan v2 W-8); ≤ 250 words; no citations; no em dash; contains one Study 1 boundary result and the Study 2 headline; uses §3 of this contract verbatim in substance |
| Highlights | 5 bullets ≤ 85 characters each; no forbidden phrase |
| §1 | States decision maker (WMS wave release), decision frequency, deliverable; the gap comes from the positioning matrix; RQ1 to RQ3 stated; C1 to C3 as in §3 above |
| §2 | Six subsections of master §5.1; positioning matrix with 15 rows including Gallien and Weber (2010), RAWSim-O (2017), Fan, Hong and Zhang (2020), Ren et al. (2025), Wang et al. (2025); no "never / only in isolation" |
| §3 | Current docx plus the sentences of plan v2 W-1 and the pool-augmentation sentence (see §9 below); every "Section 5" pointer has a destination |
| §4 | 4.1 diagnostic; 4.2 refinement; 4.3 ordering with two channels and abstraction bias; 4.4 conservative selection and screening guarantee; 4.5 GSV with algorithm box and companion text; 4.6 what Section 5 tests |
| §5 | 5.1 design, registration layers, counting units, coverage matrix, evidence-tag column; 5.2 Study 1; 5.3 Study 2; 5.4 case; 5.5 boundaries; every number reproducible from JSON |
| §6 | One paragraph per RQ; the release procedure as operational steps with run times; limitations; future work without completed items |
| Appendices A to H | As listed in plan v2 §2 |

> **中文：**
>
> | 部分 | 完成标准 |
> |---|---|
> | 摘要 | 六句逻辑（计划 v2 W-8）；不超过 250 词；不引文献；不用 em dash（长破折号）；包含一个研究一的边界结果和研究二的主结论；实质内容与本契约 §3 一致 |
> | 亮点 | 5 条，每条不超过 85 个字符；不含禁用表述 |
> | §1 | 写明决策者（WMS 的波次释放）、决策频率和交付物；研究空白来自定位对照表；列出 RQ1 至 RQ3；C1 至 C3 与上文 §3 一致 |
> | §2 | 主控 §5.1 的六个小节；定位对照表 15 行，包括 Gallien and Weber (2010)、RAWSim-O (2017)、Fan, Hong and Zhang (2020)、Ren et al. (2025)、Wang et al. (2025)；不用 "never / only in isolation"（"从未／只被孤立研究"）这类说法 |
> | §3 | 现行 docx，加上计划 v2 W-1 的句子和候选池扩充的那一句（见下文 §9）；每个指向 "Section 5" 的引用都有落点 |
> | §4 | 4.1 诊断；4.2 细化；4.3 排序，含两个反转渠道与抽象偏差；4.4 保守选择与筛选保证；4.5 GSV，含算法框与配套文字；4.6 第 5 节检验什么 |
> | §5 | 5.1 设计、登记层次、计数单位、覆盖矩阵、证据标签栏；5.2 研究一；5.3 研究二；5.4 案例；5.5 边界；每个数字都能由 JSON 复现 |
> | §6 | 每个研究问题一段；把释放流程写成带运行时间的操作步骤；局限；未来工作中不列已经完成的事项 |
> | 附录 A 至 H | 按计划 v2 §2 所列 |

## 7. Forbidden or limited phrases

> **中文：** 7. 禁用或限用的表述

Master §2.4 and §3.2 in full, plus: "calibrated to a facility"; "the procedure is optimal"; "the sequence policy replaces dispatch"; "the ordering always holds"; "Study 2 confirms Study 1". Also retired: "capacity-bound > policy-bound", "two analytical tools" as the contribution, "temporal clustering" (use "ready-time dispersion"), "vertical concentration" (use "endpoint dispersion" or "vertical spread").

> **中文：** 主控 §2.4 与 §3.2 全部适用，另加："calibrated to a facility"（已按某个设施校准）；"the procedure is optimal"（该流程是最优的）；"the sequence policy replaces dispatch"（序列策略取代调度）；"the ordering always holds"（该排序总是成立）；"Study 2 confirms Study 1"（研究二证实了研究一）。同时停用："capacity-bound > policy-bound"（运力受限大于策略受限）；把 "two analytical tools"（两个分析工具）当作贡献；"temporal clustering"（改用 "ready-time dispersion"，就绪时间离散度）；"vertical concentration"（改用 "endpoint dispersion" 端点离散度，或 "vertical spread" 垂直分布）。禁用的是英文原词。

## 8. How the story changes with the Study 2 outcome

> **中文：** 8. 故事如何随研究二的结果变化

Revised 2026-09-26 after two independent reviews, before any result. The rules below are exhaustive and are applied mechanically to the gate tiers of record of the Phase 6 protocol §7 (the DES-M2 tiers; the execution-robustness evaluators of §7.3 affect wording only, as stated below); the scenario and every wording choice follow from the tiers, so no story is chosen after the results.

> **中文：** 2026-09-26 经两轮独立审查后修订，当时尚无任何结果。下列规则穷尽所有情况，并机械地应用于 Phase 6 协议 §7 中记录在案的门槛档位（即 DES-M2 下的档位；§7.3 的执行稳健性评估器只影响措辞，见下文）。情景和每一处措辞都由档位决定，因此不会在看到结果之后再挑选故事。

**Step 1, method strength (from G2, G2′, G3):**
- *strong*: G2 upper, G3 upper, and G2′ middle or upper;
- *moderate*: G2 and G3 both middle or upper, but not strong;
- *weak*: G2 lower or G3 lower.

> **中文：** **第 1 步，方法强度（由 G2、G2′、G3 决定）：**
> - *强*：G2 上档、G3 上档，且 G2′ 为中档或上档；
> - *中等*：G2 与 G3 都在中档或上档，但不满足"强"；
> - *弱*：G2 下档或 G3 下档。

**Step 2, scenario (method strength × G1 tier), every combination covered:**

> **中文：** **第 2 步，情景（方法强度 × G1 档位），覆盖所有组合：**

| Method strength | G1 upper | G1 middle | G1 lower |
|---|---|---|---|
| strong | A | B | B |
| moderate | B | B | B |
| weak | C | C | C |

> **中文：**
>
> | 方法强度 | G1 上档 | G1 中档 | G1 下档 |
> |---|---|---|---|
> | 强 | A | B | B |
> | 中等 | B | B | B |
> | 弱 | C | C | C |

| Scenario | Story |
|---|---|
| A | Contributions as in §3; C3 is a full method contribution; IJPR |
| B | C3 becomes "fidelity ladder plus screen and verify"; the sequence result is reported as an RQ1 finding at its G1 tier; the constructor wording follows rule C3 below; IJPR with a thinner method claim |
| C | Study 2 reported in full as a boundary of the procedure; the paper returns to the insight framing of the v1 plan (C&IE); the title is not taken from the §2 candidates but follows the v1 plan framing |

> **中文：**
>
> | 情景 | 故事 |
> |---|---|
> | A | 贡献如 §3 所述；C3 是完整的方法贡献；投 IJPR |
> | B | C3 改为"保真阶梯加筛选与验证"；序列结果作为 RQ1 的发现，按其 G1 档位报告；构造器的措辞遵循下文的"C3 构造器"规则；投 IJPR，方法主张较弱 |
> | C | 研究二完整报告，作为该流程的边界；论文回到 v1 计划的洞见型框架（投 C&IE）；题目不从 §2 的候选中选取，而是遵循 v1 计划的框架 |

**Wording rules that apply in every scenario:**
- **G2′ lower:** the paper states that a budget-matched multi-start local search with the same verification step outperforms GSV's generator, presents the generator as one design choice within the screen-and-verify frame, and does not claim that constructed candidates beat search.
- **C2 (G4):** G4 upper: "the ordering persists on candidates built to create co-rides". G4 middle: the ordering "weakens on constructed candidates", and GSV screens them with max{M1, M2} (§5.5 of the protocol). G4 lower: the conservative choice of M2 is stated only for candidate sets not built to exploit co-occupancy; for constructed candidates the paper states that the choice of elevator model matters. The minimax-reduction corollary stays, as a conditional statement.
- **C2 (G8):** G8 upper: "selecting with the throughput abstraction costs more than selecting with co-occupancy". G8 middle: "often costs more". G8 lower: the paper reports the abstraction bias (TH-2) but makes no decision-loss claim in favour of M2.
- **C3 screening key:** if G4 is below its upper tier, GSV screens constructed and re-sequenced candidates with max{M1, M2}; C3 then says "closed-form screening with the conservative key max{M1, M2}" instead of "screening under the co-occupancy evaluator".
- **C3 constructor:** "mechanism-aware construction" is claimed to add value only if adding P11 to R lowers the DES-M2 makespan of GSV(20) by at least 1% (mean over cells) and at least 10% of GSV(20) releases come from P11 (both reported by `analysis_phase6.py` as `C3_wording_inputs`, computed with the headline screening key). Otherwise the paper states that the constructor did not add value beyond random generation with re-ordering, and C3's wording drops "mechanism-aware constructor" in favour of "generate, screen, and verify". The same 1% rule decides whether re-ordering is said to add value within GSV (adding P10 to R).
- **Execution robustness (protocol §7.3):** when a gate's tier is lower under an execution-robustness evaluator than under DES-M2, the text states both tiers together, and the abstract uses the lowest tier among the §7.3 evaluators; for G1 the comparison is made on the paired sigma = 0 subsample of protocol §7.3.
- **Study 1 versus Study 2:** when the two point in opposite directions, both are reported with their scope (candidate population, evaluator, scale); Study 1 verdicts stand; the two are not averaged.
- **Calibrated case not run:** if the calibrated case is not run (decision D-K not signed, or protocol §14 contingency), C3 drops the words "and on a literature-calibrated case", the §6 row for §5 reads 5.4 as one paragraph recording the drop and its reason, and the RQ3 row loses "§5.4 (case)" and S2-8; removing P9 (D-L) changes no wording.

> **中文：** **在任何情景下都适用的措辞规则：**
> - **G2′ 下档：** 论文写明，采用同样验证步骤、预算匹配的多起点局部搜索优于 GSV 的生成器；把生成器表述为"筛选与验证"框架中的一种设计选择；不声称构造候选胜过搜索。
> - **C2（G4）：** G4 上档：写 "the ordering persists on candidates built to create co-rides"（排序在为制造同乘而构造的候选上仍然成立）。G4 中档：排序 "weakens on constructed candidates"（在构造候选上减弱），GSV 对这些候选用 max{M1, M2} 筛选（协议 §5.5）。G4 下档：只对并非为利用同乘而构造的候选集合陈述"M2 是保守选择"；对构造候选，论文写明电梯模型的选择会影响结果。极小极大化简的推论保留，作为条件性陈述。
> - **C2（G8）：** G8 上档：写 "selecting with the throughput abstraction costs more than selecting with co-occupancy"（用吞吐能力抽象做选择比用同乘做选择代价更大）。G8 中档：写 "often costs more"（往往代价更大）。G8 下档：论文报告抽象偏差（TH-2），但不提出支持 M2 的决策损失主张。
> - **C3 筛选键：** 若 G4 低于上档，GSV 对构造候选和重排候选用 max{M1, M2} 筛选；此时 C3 写 "closed-form screening with the conservative key max{M1, M2}"（用保守键 max{M1, M2} 做闭式筛选），而不写 "screening under the co-occupancy evaluator"（在同乘评估器下筛选）。
> - **C3 构造器：** 只有同时满足两条，才声称 "mechanism-aware construction"（机制感知构造）增加了价值：把 P11 加入 R 使 GSV(20) 的 DES-M2 完工期至少降低 1%（对各格取平均），并且 GSV(20) 释放的波次中至少 10% 来自 P11（两项都由 `analysis_phase6.py` 以 `C3_wording_inputs` 报告，按主筛选键计算）。否则论文写明，构造器在"随机生成加重排"之外没有增加价值，C3 的措辞去掉 "mechanism-aware constructor"，改用 "generate, screen, and verify"。同样的 1% 规则决定是否声称重排在 GSV 内增加了价值（把 P10 加入 R）。
> - **执行稳健性（协议 §7.3）：** 某个门槛在执行稳健性评估器下的档位低于 DES-M2 下的档位时，正文同时写出两个档位，摘要采用 §7.3 各评估器中最低的档位；对 G1，比较在协议 §7.3 的配对 sigma = 0 子样本上进行。
> - **研究一与研究二：** 两者方向相反时，各自连同适用范围（候选总体、评估器、规模）一并报告；研究一的判定不变；两者不取平均。
> - **校准案例未运行：** 若校准案例未运行（决定 D-K 未签字，或触发协议 §14 的应急条款），C3 去掉 "and on a literature-calibrated case"（以及在基于文献校准的案例上）这几个词，§6 中 §5 那一行的 5.4 改为一段记录未做的事实及其原因，RQ3 行去掉 "§5.4 (case)" 与 S2-8；去掉 P9（D-L）不改变任何措辞。

All three stories and all wording rules are pre-committed; none requires re-running or retuning anything.

> **中文：** 三个故事和全部措辞规则都已事先承诺；任何一项都不需要重新运行或重新调参。

## 9. Propagation list (files that must reflect this contract)

> **中文：** 9. 传播清单（必须与本契约保持一致的文件）

| File | Change | Status tonight |
|---|---|---|
| revision_2026-09-02/MASTER_REVISION_BY_SECTION.md | IJPR v2 overlay (§00) superseding §2.1 to §2.3; pointers | done (draft; backup kept) |
| paper_draft/TERMINOLOGY.md | retired capacity headline; new terms | done (draft; backup kept) |
| CLAUDE.md | venue, contributions, naming, Study 2 guard | done (draft; backup kept) |
| revision_2026-09-24/plan_section3_section4_v0_2.md line 13 | "two simple usable diagnostic tools" | superseded by this contract; the plan file itself is left untouched as history |
| archive/paper_draft/storyline_motivation_to_contribution_v1.md (formerly in paper_draft/) | capacity storyline | superseded (master §1.3); folded into archive/ on 2026-09-26, content untouched |
| Problem formulation.docx | plan v2 W-1 sentences plus: "Section 5 also evaluates pools augmented with constructed and re-sequenced candidates (Study 2)." at the end of 3.3.1 | NOT edited (docx edits need the author's go-ahead) |
| abstract, introduction, related works drafts | rewrite per §6 above | later weeks |

> **中文：**
>
> | 文件 | 改动 | 当晚状态 |
> |---|---|---|
> | revision_2026-09-02/MASTER_REVISION_BY_SECTION.md | IJPR v2 覆盖层（§00）取代 §2.1 至 §2.3；加指针 | 已完成（草稿；保留备份） |
> | paper_draft/TERMINOLOGY.md | 停用 capacity 主结论；新增术语 | 已完成（草稿；保留备份） |
> | CLAUDE.md | 期刊、贡献、命名、研究二守卫 | 已完成（草稿；保留备份） |
> | revision_2026-09-24/plan_section3_section4_v0_2.md 第 13 行 | "two simple usable diagnostic tools"（两个简单可用的诊断工具） | 已被本契约取代；计划文件本身作为历史保持不动 |
> | archive/paper_draft/storyline_motivation_to_contribution_v1.md（原位于 paper_draft/） | capacity 故事线 | 已被取代（主控 §1.3）；2026-09-26 折叠进 archive/，内容未改 |
> | Problem formulation.docx | 计划 v2 W-1 的句子，另在 3.3.1 末尾加一句："Section 5 also evaluates pools augmented with constructed and re-sequenced candidates (Study 2)."（第 5 节还评估加入构造候选与重排候选后的扩充候选池（研究二）。） | 未修改（修改 docx 需要作者同意） |
> | 摘要、引言、相关工作草稿 | 按上文 §6 改写 | 后续几周 |

## 10. Sign-off

> **中文：** 10. 签字（作者姓名与日期）

To sign: in one edit, fill the line below, set `author_signoff` to "SIGNED (<name>, <date>)", and replace the `status` line; then run, from the repository root, `python "revision_2026-09-26_ijpr/archive_package/make_manifest.py" SIGNED`; then open `MANIFEST_SIGNED.md` and confirm that the signoff column of every registration starts with SIGNED or ACKNOWLEDGED (the guard does not recognise curly quotes).

> **中文：** 签法：在同一次编辑里填好下面一行，把 front matter 的 author_signoff 改为 "SIGNED (你的名字, 日期)"，并改掉 status 行；然后全部签完后在仓库根目录运行 `python "revision_2026-09-26_ijpr/archive_package/make_manifest.py" SIGNED`，然后打开 `MANIFEST_SIGNED.md`，确认每份登记文件的 signoff 栏都以 SIGNED 或 ACKNOWLEDGED 开头（守卫不认中文弯引号）。

Author: Shiyue Hu Date: 2026-09-26
