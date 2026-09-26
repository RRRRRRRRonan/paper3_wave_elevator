---
title: "签字前审查修正的全部差异（2026-09-26）"
status: "供作者复核；左为审查前（你已审过的版本），右为现状"
---

# 签字前审查修正的全部差异

审查结论与逐条依据见 `presign_audit_2026-09-26.md`。下面是六份待签文件和四个代码文件相对于 `backups/pre_audit_fix_2026-09-26/` 的统一差异（`-` 行为修改前，`+` 行为修改后，各带 2 行上下文）。

## 01_DECISIONS_TO_SIGN.md

```diff
--- before
+++ after
@@ -18,5 +18,5 @@
 | 选项 | 内容 |
 |---|---|
-| A1（推荐） | 放弃"两个简单可用的诊断工具"。采用三条贡献：C1 问题与基准；C2 电梯模型风险（排序定理、抽象偏差、筛选保证）；C3 "生成、筛选、验证"释放流程与保真阶梯。Bound-and-Gap 在引入处写明预注册第 213 行的弱化表述（partition-relative, prototype-regime diagnostic）。 |
+| A1（推荐） | 放弃"两个简单可用的诊断工具"。采用三条贡献：C1 问题与基准；C2 电梯模型风险（排序定理、抽象偏差、筛选保证）；C3 "生成、筛选、验证"释放流程与保真阶梯。Bound-and-Gap 在引入处写明弱化表述（预注册第 213 行的 prototype-regime diagnostic，以及主控的 partition-relative 定性）。 |
 | A2 | 保留"两个工具"的卖点 |
 
@@ -63,5 +63,5 @@
 | 选项 | 内容 |
 |---|---|
-| E1（推荐） | 研究二出结果后，在故事契约 §2 的三个候选里定 |
+| E1（推荐） | 研究二出结果后，在故事契约 §2 的三个候选里定（若落入契约 §8 的情景 C，则不取自这三个候选，按 v1 计划的框架另定；契约 §8 的 C3 构造器规则去掉 mechanism-aware 时，候选 2 不选） |
 | E2 | 现在定 |
 
@@ -109,5 +109,5 @@
 | 选项 | 内容 |
 |---|---|
-| I1（推荐） | 登记文件作为独立文件放在 `revision_2026-09-26_ijpr/amendments/` 与 `paper_draft/phase6_method_study_protocol.md`，冻结的 Phase 5 预注册一字不改；签字后可在预注册 §9 末尾追加一行指针（可选） |
+| I1（推荐） | 登记文件作为独立文件放在 `revision_2026-09-26_ijpr/amendments/` 与 `paper_draft/phase6_method_study_protocol.md`，冻结的 Phase 5 预注册一字不改、保持字节级不变，不追加任何指针；指向 2026-09-26 登记文件的指针写在手稿的登记附录中 |
 | I2 | 追加进预注册 §9.3 等小节（plan v0.2 §4 原来的写法） |
 
@@ -125,5 +125,5 @@
 | J4（推荐，作者 2026-09-26 选定） | OSF 登记（禁运至论文接收，接收时结束禁运，供读者核对登记内容）；投稿时代码与数据以保密补充材料提供给编辑和审稿人；发表后代码与数据按合理请求由作者提供，不存放公开仓库 |
 
-补充（审查后）：签字后先运行 `make_manifest.py SIGNED` 生成签字清单（守卫据此核对哈希，文件签字后改一个字节都会被拦下），再上传 OSF；第 4 周的 L2 附录单独签字、运行 `make_manifest.py SIGNED_L2`，并作为 OSF 更新登记。
+补充（审查后）：签字后先在仓库根目录运行 `python "revision_2026-09-26_ijpr/archive_package/make_manifest.py" SIGNED` 生成签字清单（守卫据此核对哈希，文件签字后改一个字节都会被拦下），再上传 OSF；第 4 周的 L2 附录单独签字、运行 `python "revision_2026-09-26_ijpr/archive_package/make_manifest.py" SIGNED_L2`，并作为 OSF 更新登记。
 
 **推荐：** J4（作者 2026-09-26 选定）。登记用 OSF（预注册社区的通行做法），设禁运至论文接收：接收前不公开，但登记时间戳可验证；接收时结束禁运，让读者能核对登记内容（登记公开不等于代码公开）。投稿时代码与数据以保密补充材料交给编辑和审稿人；发表后按合理请求由作者提供，不存放公开仓库。数据可得性声明（英文稿）："The simulation code and the generated data that support the findings of this study are available from the corresponding author upon reasonable request. The study's registrations are available on OSF at [link]." 前提：投稿前核对 IJPR 执行的 Taylor & Francis 数据共享政策档次；若为 "Basic" 或 "Share upon reasonable request"，J4 可行；若要求公开存放（"Publicly available" 或更严格），改用 J3（接收后在 Zenodo 发布）。为能按请求提供论文所用的确切版本，投稿时保存代码发布包及其哈希（P-6）。若期刊采用双盲评审：签字件含作者姓名，OSF 的匿名只读链接遮不住附件里的签名，因此审稿版稿件只写"已在 OSF 登记（禁运至发表）"，链接只给编辑。（2026-09-26 按作者意见两次修订：先把 Zenodo 由"投稿时"改为"接收后"，再改为 J4，按请求提供代码。）
@@ -162,9 +162,9 @@
 
 **G3 容差需要你二选一（已披露的背景见协议 §2）：**
-- (a) 2%（第 1 稿）：严格；在 8 单波次上最优值约 40 到 60 秒，2% 只有约 1 秒，几乎要求精确找到最优；
+- (a) 2%（第 1 稿）：严格；发表规模 B-2 的两格 8 单最优值为 70 与 38 秒（协议 §2），2% 只有约 1 秒，几乎要求精确找到最优；
 - (b) max{2%, 1 秒 / 最优值}（第 3 稿，推荐）：保持 2% 的目标，只保证至少 1 秒（零就绪时间时评估器的时间步长）；最优值 38 秒时为 2.6%，50 秒以上即为 2%。
 第 2 稿曾用 max{2%, 4 秒 / 最优值}，第二轮审查发现它在玩具规模上相当于 3.6% 到 10.5%，过松，已放弃。这几次改动都发生在看过玩具结果之后，触发原因是两轮审查而不是玩具数值；协议 §2 如实列明。
 
-**推荐：** 按协议草案签，G3 选 (b)；若要改，只改数值，不改指标定义。
+**推荐：** 按协议草案签，G3 选 (b)；若要改，只改数值，不改指标定义。若选 (a) 或改动 §7 任一门槛数值，须在同一次签字编辑里把协议 §7.1（G3 容差句）和 §7.2 对应门槛改成所选值，并在 G0 代码冻结前把 `prototype/src/phase6_config.py` 中的 REGRET_TOL_ABS（选 (a) 时改为 0.0）与 GATES 改成同一值；决定单与协议在签字时必须一致，守卫只核对哈希，不会发现两者矛盾。
 
 **作者决定：** ______________________
@@ -178,3 +178,3 @@
 作者：____________________　　日期：____________
 
-签字方法：在同一次编辑里填好各条决定、在上面签名、把本文件 front matter 的 `author_signoff` 改为 `"SIGNED (你的名字, 日期)"` 并更新 `status` 行；故事契约、协议与研究一登记文件也各自这样签。全部签完后在仓库根目录运行 `make_manifest.py SIGNED`。签字清单生成后，这些文件都不能再改（守卫会拦下任何改动，改动后重新登记也会被识别）；如需改动，写新的带日期修正案。助手不会在你签字后改动这些文件。
+签字方法：在同一次编辑里填好各条决定、在上面签名、把本文件 front matter 的 `author_signoff` 改为 `"SIGNED (你的名字, 日期)"` 并更新 `status` 行；故事契约、协议与研究一登记文件也各自这样签。全部签完后在仓库根目录运行 `python "revision_2026-09-26_ijpr/archive_package/make_manifest.py" SIGNED`，然后打开 `MANIFEST_SIGNED.md`，确认每份登记文件的 signoff 栏都以 SIGNED 或 ACKNOWLEDGED 开头（守卫不认中文弯引号）。签字清单生成后，这些文件都不能再改（守卫会拦下任何改动，改动后重新登记也会被识别）；如需改动，写新的带日期修正案。助手不会在你签字后改动这些文件。
```

## STORY_CONTRACT.md

```diff
--- before
+++ after
@@ -44,4 +44,8 @@
 > **中文：** 规则（主控 §3.1）：题目中的每个动作词，都必须在 §3 有对应的决策变量、在 §4 有对应的方法、在 §5 有直接证据。
 
+When the §8 C3 constructor rule drops "mechanism-aware", candidate 2 is excluded. Under scenario C of §8 the title is not taken from these candidates but follows the v1 plan framing.
+
+> **中文：** 当 §8 的"C3 构造器"规则去掉 "mechanism-aware"（机制感知）时，候选 2 被排除。在 §8 的情景 C 下，题目不从这三个候选中选取，而是遵循 v1 计划的框架。
+
 ## 3. Contributions (the only version used anywhere)
 
@@ -52,7 +56,7 @@
 > **中文：** **C1. 问题与基准。** 对于在楼层内行驶、跨层须共用楼宇货梯的 AMR 车队，我们把单个波次的组成问题表述为在候选波次上的选择问题：每个候选同时确定订单集合及其处理序列，调度规则固定不变。我们构建一个可复现的合成基准，包含三个电梯评估器，以完工期中位数为主要指标。
 
-**C2. Elevator-model risk.** We prove a conditional sample-path ordering between the throughput abstraction and true co-occupancy batching for any number of elevators and any car capacity, identify the only two reversal mechanisms, and quantify the resulting abstraction bias. The ordering makes screening candidates under the co-occupancy evaluator a conservative, minimax choice.
-
-> **中文：** **C2. 电梯模型风险。** 我们证明吞吐能力抽象与真实同乘批运之间的条件性样本路径排序，对任意电梯数与任意轿厢容量成立；指出仅有的两种反转机制，并量化由此产生的抽象偏差。这一排序使得在同乘评估器下筛选候选成为保守的、极小极大意义下的选择。
+**C2. Elevator-model risk.** We prove a conditional sample-path ordering between the throughput abstraction and true co-occupancy batching for any number of elevators and any car capacity, identify the two reversal mechanisms, which are exhaustive under aligned sequences and AMR assignments, and quantify the resulting abstraction bias. The ordering makes screening candidates under the co-occupancy evaluator a conservative, minimax choice.
+
+> **中文：** **C2. 电梯模型风险。** 我们证明吞吐能力抽象与真实同乘批运之间的条件性样本路径排序，对任意电梯数与任意轿厢容量成立；指出两种反转机制（它们在序列与 AMR 分配对齐时是穷尽的），并量化由此产生的抽象偏差。这一排序使得在同乘评估器下筛选候选成为保守的、极小极大意义下的选择。
 
 **C3. A generate, screen, and verify release procedure.** We propose a release procedure that generates candidate waves with a mechanism-aware constructor, screens them in closed form under the co-occupancy evaluator, and verifies a shortlist by event-driven simulation. A registered computational study evaluates the procedure against random, class-based, heuristic, and search policies along a fidelity ladder from closed-form evaluators to event-driven simulation, on independent order pools and on a literature-calibrated case, and reports the preregistered class diagnostics as its validity boundary.
@@ -87,7 +91,7 @@
 | RQ | Answered in | Evidence (tags) |
 |---|---|---|
-| RQ1 | §5.2 (Study 1 diagnostics), §5.3 (set versus sequence, sequence lever) | Block A/B [PR-C]; S1-1, S1-2, S1-8 [RA]/[NS]; Study 2 S2-1, S2-2 [NS] |
-| RQ2 | §4.3 to §4.4 (theory), §5.2 (Block C), §5.3 (fidelity ladder, ordering on constructed waves) | H-D2 [PR-C]; S1-3, S1-12, TH-2 [NS]/[QA]/[RA]; Study 2 S2-5, S2-6 [NS] |
-| RQ3 | §5.3 (GSV main experiment, screening regret, warm start, execution robustness), §5.4 (case), §5.5 (boundaries) | Study 2 S2-3, S2-4, S2-7, S2-8, S2-10 [NS]; ICC, OOS, B-5 [NS]/[RA] |
+| RQ1 | §5.2 (Study 1 diagnostics), §5.3 (set versus sequence, sequence lever) | Block A/B [PR-C]; S1-1, S1-2, S1-5, S1-7, S1-8, S1-9, S1-11 (S1-11 only if D-D1 is signed) [RA]/[NS]/[QA]; Study 2 S2-1, S2-2 [NS] |
+| RQ2 | §4.3 to §4.4 (theory), §5.2 (Block C), §5.3 (fidelity ladder, ordering on constructed waves) | H-D2 [PR-C]; S1-3, S1-4, S1-6, S1-12, TH-2 [NS]/[QA]/[RA]; Study 2 S2-5, S2-6 [NS] |
+| RQ3 | §5.3 (GSV main experiment, screening regret, warm start, execution robustness), §5.4 (case), §5.5 (boundaries) | Study 2 S2-3, S2-4, S2-7, S2-8, S2-9, S2-10 [NS]; ICC, OOS, B-5 [NS]/[RA] |
 
 > **中文：**
@@ -95,11 +99,11 @@
 > | 研究问题 | 回答位置 | 证据（标签） |
 > |---|---|---|
-> | RQ1 | §5.2（研究一的诊断）、§5.3（订单集合与序列的比较、序列杠杆） | Block A/B [PR-C]；S1-1、S1-2、S1-8 [RA]/[NS]；研究二 S2-1、S2-2 [NS] |
-> | RQ2 | §4.3 至 §4.4（理论）、§5.2（Block C）、§5.3（保真阶梯、构造波次上的排序） | H-D2 [PR-C]；S1-3、S1-12、TH-2 [NS]/[QA]/[RA]；研究二 S2-5、S2-6 [NS] |
-> | RQ3 | §5.3（GSV 主实验、筛选遗憾、热启动、执行稳健性）、§5.4（案例）、§5.5（边界） | 研究二 S2-3、S2-4、S2-7、S2-8、S2-10 [NS]；ICC、OOS、B-5 [NS]/[RA] |
-
-Study 2 item numbers (S2-1 to S2-10) are defined in the Phase 6 protocol §1.1.
-
-> **中文：** 研究二的条目编号（S2-1 至 S2-10）在 Phase 6 协议 §1.1 中定义。
+> | RQ1 | §5.2（研究一的诊断）、§5.3（订单集合与序列的比较、序列杠杆） | Block A/B [PR-C]；S1-1、S1-2、S1-5、S1-7、S1-8、S1-9、S1-11（S1-11 仅在 D-D1 签字时做）[RA]/[NS]/[QA]；研究二 S2-1、S2-2 [NS] |
+> | RQ2 | §4.3 至 §4.4（理论）、§5.2（Block C）、§5.3（保真阶梯、构造波次上的排序） | H-D2 [PR-C]；S1-3、S1-4、S1-6、S1-12、TH-2 [NS]/[QA]/[RA]；研究二 S2-5、S2-6 [NS] |
+> | RQ3 | §5.3（GSV 主实验、筛选遗憾、热启动、执行稳健性）、§5.4（案例）、§5.5（边界） | 研究二 S2-3、S2-4、S2-7、S2-8、S2-9、S2-10 [NS]；ICC、OOS、B-5 [NS]/[RA] |
+
+Study 2 item numbers (S2-1 to S2-10) are defined in the Phase 6 protocol §1.1. The protocol's §1 restates the RQs in its own words; this contract's wording prevails.
+
+> **中文：** 研究二的条目编号（S2-1 至 S2-10）在 Phase 6 协议 §1.1 中定义。协议 §1 用自己的话复述了各研究问题；以本契约的措辞为准。
 
 ## 5. Roles of the two studies
@@ -205,5 +209,5 @@
 | A | Contributions as in §3; C3 is a full method contribution; IJPR |
 | B | C3 becomes "fidelity ladder plus screen and verify"; the sequence result is reported as an RQ1 finding at its G1 tier; the constructor wording follows rule C3 below; IJPR with a thinner method claim |
-| C | Study 2 reported in full as a boundary of the procedure; the paper returns to the insight framing of the v1 plan (C&IE) |
+| C | Study 2 reported in full as a boundary of the procedure; the paper returns to the insight framing of the v1 plan (C&IE); the title is not taken from the §2 candidates but follows the v1 plan framing |
 
 > **中文：**
@@ -213,5 +217,5 @@
 > | A | 贡献如 §3 所述；C3 是完整的方法贡献；投 IJPR |
 > | B | C3 改为"保真阶梯加筛选与验证"；序列结果作为 RQ1 的发现，按其 G1 档位报告；构造器的措辞遵循下文的"C3 构造器"规则；投 IJPR，方法主张较弱 |
-> | C | 研究二完整报告，作为该流程的边界；论文回到 v1 计划的洞见型框架（投 C&IE） |
+> | C | 研究二完整报告，作为该流程的边界；论文回到 v1 计划的洞见型框架（投 C&IE）；题目不从 §2 的候选中选取，而是遵循 v1 计划的框架 |
 
 **Wording rules that apply in every scenario:**
@@ -221,6 +225,7 @@
 - **C3 screening key:** if G4 is below its upper tier, GSV screens constructed and re-sequenced candidates with max{M1, M2}; C3 then says "closed-form screening with the conservative key max{M1, M2}" instead of "screening under the co-occupancy evaluator".
 - **C3 constructor:** "mechanism-aware construction" is claimed to add value only if adding P11 to R lowers the DES-M2 makespan of GSV(20) by at least 1% (mean over cells) and at least 10% of GSV(20) releases come from P11 (both reported by `analysis_phase6.py` as `C3_wording_inputs`, computed with the headline screening key). Otherwise the paper states that the constructor did not add value beyond random generation with re-ordering, and C3's wording drops "mechanism-aware constructor" in favour of "generate, screen, and verify". The same 1% rule decides whether re-ordering is said to add value within GSV (adding P10 to R).
-- **Execution robustness (protocol §7.3):** when a gate's tier is lower under an execution-robustness evaluator than under DES-M2, the text states both tiers together, and the abstract uses the lower one.
+- **Execution robustness (protocol §7.3):** when a gate's tier is lower under an execution-robustness evaluator than under DES-M2, the text states both tiers together, and the abstract uses the lowest tier among the §7.3 evaluators; for G1 the comparison is made on the paired sigma = 0 subsample of protocol §7.3.
 - **Study 1 versus Study 2:** when the two point in opposite directions, both are reported with their scope (candidate population, evaluator, scale); Study 1 verdicts stand; the two are not averaged.
+- **Calibrated case not run:** if the calibrated case is not run (decision D-K not signed, or protocol §14 contingency), C3 drops the words "and on a literature-calibrated case", the §6 row for §5 reads 5.4 as one paragraph recording the drop and its reason, and the RQ3 row loses "§5.4 (case)" and S2-8; removing P9 (D-L) changes no wording.
 
 > **中文：** **在任何情景下都适用的措辞规则：**
@@ -230,6 +235,7 @@
 > - **C3 筛选键：** 若 G4 低于上档，GSV 对构造候选和重排候选用 max{M1, M2} 筛选；此时 C3 写 "closed-form screening with the conservative key max{M1, M2}"（用保守键 max{M1, M2} 做闭式筛选），而不写 "screening under the co-occupancy evaluator"（在同乘评估器下筛选）。
 > - **C3 构造器：** 只有同时满足两条，才声称 "mechanism-aware construction"（机制感知构造）增加了价值：把 P11 加入 R 使 GSV(20) 的 DES-M2 完工期至少降低 1%（对各格取平均），并且 GSV(20) 释放的波次中至少 10% 来自 P11（两项都由 `analysis_phase6.py` 以 `C3_wording_inputs` 报告，按主筛选键计算）。否则论文写明，构造器在"随机生成加重排"之外没有增加价值，C3 的措辞去掉 "mechanism-aware constructor"，改用 "generate, screen, and verify"。同样的 1% 规则决定是否声称重排在 GSV 内增加了价值（把 P10 加入 R）。
-> - **执行稳健性（协议 §7.3）：** 某个门槛在执行稳健性评估器下的档位低于 DES-M2 下的档位时，正文同时写出两个档位，摘要采用较低者。
+> - **执行稳健性（协议 §7.3）：** 某个门槛在执行稳健性评估器下的档位低于 DES-M2 下的档位时，正文同时写出两个档位，摘要采用 §7.3 各评估器中最低的档位；对 G1，比较在协议 §7.3 的配对 sigma = 0 子样本上进行。
 > - **研究一与研究二：** 两者方向相反时，各自连同适用范围（候选总体、评估器、规模）一并报告；研究一的判定不变；两者不取平均。
+> - **校准案例未运行：** 若校准案例未运行（决定 D-K 未签字，或触发协议 §14 的应急条款），C3 去掉 "and on a literature-calibrated case"（以及在基于文献校准的案例上）这几个词，§6 中 §5 那一行的 5.4 改为一段记录未做的事实及其原因，RQ3 行去掉 "§5.4 (case)" 与 S2-8；去掉 P9（D-L）不改变任何措辞。
 
 All three stories and all wording rules are pre-committed; none requires re-running or retuning anything.
@@ -267,3 +273,7 @@
 > **中文：** 10. 签字（作者姓名与日期）
 
+To sign: in one edit, fill the line below, set `author_signoff` to "SIGNED (<name>, <date>)", and replace the `status` line; then run, from the repository root, `python "revision_2026-09-26_ijpr/archive_package/make_manifest.py" SIGNED`; then open `MANIFEST_SIGNED.md` and confirm that the signoff column of every registration starts with SIGNED or ACKNOWLEDGED (the guard does not recognise curly quotes).
+
+> **中文：** 签法：在同一次编辑里填好下面一行，把 front matter 的 author_signoff 改为 "SIGNED (你的名字, 日期)"，并改掉 status 行；然后全部签完后在仓库根目录运行 `python "revision_2026-09-26_ijpr/archive_package/make_manifest.py" SIGNED`，然后打开 `MANIFEST_SIGNED.md`，确认每份登记文件的 signoff 栏都以 SIGNED 或 ACKNOWLEDGED 开头（守卫不认中文弯引号）。
+
 Author: ____________________ Date: ____________
```

## phase6_method_study_protocol.md

```diff
--- before
+++ after
@@ -53,11 +53,11 @@
 |---|---|---|
 | Phase 5 Blocks A, B, C under the closed-form evaluators (M1, M2, M3), including P0 to P6 medians on the 12 Block B cells (grand means: P0 317.6, P2 299.2, P5 303.6) | `prototype/results/v0_5_phase5_*.json` [PR-C]/[AM1] | Baseline levels |
-| P8 savings heuristic beats P5 in 10/12 Block B cells (grand mean 288.4 versus 303.6); P9 beats P5 in 9/12 cells and beats the best corner (realized) in 7/12 | `b2_b3_benchmarks.json#B3`, `amendC1_p9_spoplus.json` [NS] | Strength of the heuristic comparators |
-| **P7 local search (median of 200 runs of 40 iterations per cell under M2) is below P8 in 12/12 Block B cells (grand mean 224.6 versus 288.4)** | `b2_b3_benchmarks.json#B3` [AM1]/[NS] | **Local search is far stronger than every class rule, so G2′ uses a budget-matched local search (P7-matched, §4), not the Phase 5 run median** |
-| Pool optimum for 2 cells (config 0, size 8, E = 1: optimum 70 versus pool median 165; config 1, size 8: optimum 38 versus P7 56, +47.4%, and P5 94, +147%) | `b2_b3_benchmarks.json#B2` [NS] | Scale of possible gains; any procedure with thousands of evaluator calls is expected to beat simulator-free class rules, which is why G2 compares at equal verification budget (P8-verify) |
+| P8 savings heuristic beats P5 in 10/12 Block B cells (grand mean 288.4 versus 303.6); P9 beats P5 in 9/12 cells and beats the best corner (realized) in 7/12 | `revision_2026-07-08/tier2_analysis/outputs/b2_b3_benchmarks.json#B3`, `revision_2026-07-08/tier2_analysis/outputs/amendC1_p9_spoplus.json` [NS] | Strength of the heuristic comparators |
+| **P7 local search (median of 200 runs of 40 iterations per cell under M2) is below P8 in 12/12 Block B cells (grand mean 224.6 versus 288.4)** | `revision_2026-07-08/tier2_analysis/outputs/b2_b3_benchmarks.json#B3` [AM1]/[NS] | **Local search is far stronger than every class rule, so G2′ uses a budget-matched local search (P7-matched, §4), not the Phase 5 run median** |
+| Pool optimum for 2 cells (config 0, size 8, E = 1: optimum 70 versus pool median 165; config 1, size 8: optimum 38 versus P7 56, +47.4%, and P5 94, +147%) | `revision_2026-07-08/tier2_analysis/outputs/b2_b3_benchmarks.json#B2` [NS] | Scale of possible gains; any procedure with thousands of evaluator calls is expected to beat simulator-free class rules, which is why G2 compares at equal verification budget (P8-verify) |
 | **Clustered operational dispatch (`policy="cluster"`, pop_cluster) lowers the closed-form M2 median by 10.2% on the Φ-corner arm (12/12 cells positive and above 1%) and 10.5% on the random arm (12/12 positive, 10/12 above 1%)** | `v0_5_phase5_supp.json#Supp1_H1_at_scale` [AM2] | **P10 applies a related grouping at release time. Under the closed-form evaluator a similar gain is therefore expected; G1 is evaluated under DES-M2, and the closed-form value is descriptive and flagged as prior-exposed** |
-| DES cross-check on configs 1, 7, 11 (uniform, clustered, uniform; size 16; random arm): per-wave DES ordering 0.98 to 1.00; Spearman ρ between closed-form and DES makespans 0.45 to 0.68; mean DES-M2 makespans 22.8% to 37.3% below closed-form M2 (all under the B-5 boarding semantics, §3.5) | `b5_des_crossvalidation.json` [NS] | G3 and G8: closed-form rankings are imperfect proxies for DES rankings over whole pools; nothing is known about the top of the distribution. No diurnal configuration was in the cross-check; ready times were exercised only by single-AMR self-tests |
+| DES cross-check on configs 1, 7, 11 (uniform, clustered, uniform; size 16; random arm): per-wave DES ordering 0.98 to 1.00; Spearman ρ between closed-form and DES makespans 0.45 to 0.68; mean DES-M2 makespans 22.8% to 37.3% below closed-form M2 (all under the B-5 boarding semantics, §3.5) | `revision_2026-07-08/tier2_analysis/outputs/b5_des_crossvalidation.json` [NS] | G3 and G8: closed-form rankings are imperfect proxies for DES rankings over whole pools; nothing is known about the top of the distribution. No diurnal configuration was in the cross-check; ready times were exercised only by single-AMR self-tests |
 | Informal audit numbers from 2026-09-25 (unregistered, [EXP]): median per-wave (M2 − M1)/M1 = 41% on the tie-break-fixed Block C CSV; Φ-corner advantage over random in the Supp-1 data 7.47% (FIFO) and 7.12% (cluster) as means of per-cell ratios (4.86% and 4.25% as ratios of grand means); candidate-cluster bootstrap D1-d 52 to 55/72 and row-level 56 to 58/72 over seeds; corner-choice stability 0.43 to 0.78 in 5/6 configurations | readiness assessment Part 1 [EXP] | G4 expectations on random candidates; G1 context. Registered for re-analysis in Study 1 (S1-1, S1-6, S1-7, TH-2); results of neither study |
-| Code self-tests (2026-09-26): the drivers were run end to end on two toy configurations outside the design (901: F = 5, 5 AMRs, E = 2, uniform; 902: F = 3, 15 AMRs, E = 1, diurnal), toy seeds (base 424,242), K = 120, K′ = 20, untuned P11 weights (2, 1, 0.5). The assistant saw, while debugging draft 1, the M1 ≤ M2 share of 147 of 160 toy P11 candidates (92%) against 955 of 960 toy random candidates, one toy set-versus-sequence share (0.59), and the tier labels of the draft-1 analysis self-test on 8 toy decisions (G1 middle, G2 upper, G2′ upper, G3 upper, G4 middle, G5 upper, G6 middle, G8 middle). An independent reviewer's toy check (seeds 555,xxx; K = 3,000; K′ = 200; weights (2, 1, 0.5)) found 9 to 15 distinct sequences among the M2 top 20 in 7 of 15 settings and as few as 32 distinct P11 sequences of 200. After the draft-2 fixes only structural checks (budgets, counts) were printed | job scratch folder; review report | These toy values carry no information about the registered runs (tiny K, configurations outside the design, draft-1 definitions). **Definitions changed after the toy runs had been seen, each triggered by an independent review rather than by a toy value:** G2 comparator (P8-best → P8-verify(20); stricter), G5(b) (five-wave completion against P0 → retention of the cold-start gain; stricter), G3 tolerance (2% in draft 1 → max{2%, 4 s / optimum} in draft 2 → max{2%, 1 s / optimum} in draft 3; see the next row), G1 and G8 wording, the de-duplication rule of §5.5, the §7.3 execution check, the G6 aggregation (mean over cells) and the G3 key clarification. The author chooses at signing between the draft-1 G3 tolerance (2%) and the draft-3 one (decision D-M) |
+| Code self-tests (2026-09-26): the drivers were run end to end on two toy configurations outside the design (901: F = 5, 5 AMRs, E = 2, uniform; 902: F = 3, 15 AMRs, E = 1, diurnal), toy seeds (base 424,242), K = 120, K′ = 20, untuned P11 weights (2, 1, 0.5). The assistant saw, while debugging draft 1, the M1 ≤ M2 share of 147 of 160 toy P11 candidates (92%) against 955 of 960 toy random candidates, one toy set-versus-sequence share (0.59), and the tier labels of the draft-1 analysis self-test on 8 toy decisions (G1 middle, G2 upper, G2′ upper, G3 upper, G4 middle, G5 upper, G6 middle, G8 middle). An independent reviewer's toy check (seeds 555,xxx; K = 3,000; K′ = 200; weights (2, 1, 0.5)) found 9 to 15 distinct sequences among the M2 top 20 in 7 of 15 settings and as few as 32 distinct P11 sequences of 200. After the draft-2 fixes only structural checks (budgets, counts) were printed | job scratch folder; review report | These toy values carry no information about the registered runs (tiny K, configurations outside the design, draft-1 definitions). **Definitions changed after the toy runs had been seen, each triggered by an independent review rather than by a toy value:** G2 comparator (P8-best → P8-verify(20); stricter), G5(b) (five-wave completion against P0 → retention of the cold-start gain; stricter), G3 tolerance (2% in draft 1 → max{2%, 4 s / optimum} in draft 2 → max{2%, 1 s / optimum} in draft 3; see the next row), G1 and G8 wording, the de-duplication rule of §5.5, the §7.3 execution check, the G6 aggregation (mean over cells), the G3 key clarification, P7-matched receiving the P10 re-ordering operator inside its 6,200-evaluation budget (first review, item 2; stricter for GSV), G2′ counting ties as matches, at or below instead of the draft-1 below (second review, R2-9; looser for GSV; the toy G2′ label was already upper under the strict count), G5(a) sampling its 300 candidates from the random part R_s rather than from the whole candidate set that the draft-1 code sampled (first review, item 5), and the warm-start chains screening by the G4-decided headline key instead of always by M2 (first review, item 5). The author chooses at signing between the draft-1 G3 tolerance (2%) and the draft-3 one (decision D-M) |
 | Second reviewer's toy-shaped runs (2026-09-26; toy seeds 777,xxx; toy configurations shaped like configs 0, 1, 9, 17; full K = 3,000): DES-M2 optimum over G of 38 to 111 s at n = 8 and 16, so the draft-2 tolerance max{2%, 4 s / optimum} equalled 3.6% to 10.5% and the 2% floor rarely bound; 84 to 149 distinct P11 signatures of 200; one config-17-shaped pool took 69 s for three sizes (about 3 hours projected for the main study) | review report | This is why draft 3 uses max{2%, 1 s / optimum} (2.6% at an optimum of 38 s, 2% from 50 s on): it keeps the 2% target and only guarantees one second, the time step of the evaluators when ready offsets are zero |
 
@@ -106,5 +106,5 @@
 | P0 random | distribution: uniform over R; reported as its DES-M2 median | none | 0 |
 | P2 cardinality rule | distribution: uniform over the candidates of R whose cross-floor count is at or below its 25% quantile (Phase 5 definition, ties included) | none | 0 |
-| P5 Φ-corner rule | distribution: uniform over the favourable corner of R; the corner is chosen by the Phase 5 `fit_predictors` protocol from a 200-draw M2 training sample of R (with replacement, stream 94) | 200 M2 (training) | 200 M2 |
+| P5 Φ-corner rule | distribution: uniform over the favourable corner of R; the corner is chosen by the Phase 5 `fit_predictors` protocol from a 200-draw M2 training sample of R (with replacement, stream 94). If the corner is empty for a decision, that decision has no P5 or P5+P10 value; it is excluded from every P5 and P5+P10 quantity (cell means, the §8 pairs GSV(20) versus P5 and P5+P10 versus P5, and the G1 P5+P10 companion), the exclusion is recorded in v0_6_phase6_main.json, and the number of such decisions is reported in v0_6_phase6_gates.json | 200 M2 (training) | 200 M2 |
 | P8-200 | distribution: the 200 lowest P8 scores in R (Block B definition) | none | 0 |
 | P8-1 | single wave: the lowest P8 score in R | none | 0 |
@@ -116,9 +116,9 @@
 | P0+P10g | P0 with every candidate replaced by its P10g re-ordering (grouping with readiness ordering, no chaining); evaluated under M2 and DES-M2 outside G; descriptive, for the chaining increment | none | 0 |
 | P11-1 | single wave: the P11 candidate with the lowest M2 makespan | M2 | 200 M2 |
-| **GSV(k)**, k ∈ {1, 5, 10, 20, 50, 100, 6200} | single wave: screen G by M2, take the first k distinct signatures, evaluate them under DES-M2, release the DES-M2-best (§5.5). When k exceeds the number of distinct signatures, all are verified and the actual k is reported | M2 on G; DES-M2 on k | 6,200 M2 + k DES |
+| **GSV(k)**, k ∈ {1, 5, 10, 20, 50, 100, 6200} | single wave: screen G by M2, take the first k distinct signatures, evaluate them under DES-M2, release the DES-M2-best (§5.5). When k exceeds the number of distinct signatures, all are verified and the actual k is reported | M2 on G; DES-M2 on k | 6,200 M2 + k DES (plus 3,200 M1 on the P10(R) and P11 candidates when the max{M1, M2} key is in force, §5.5) |
 | R-verify(k), same k grid | single wave: the first k distinct signatures of R in a random order (stream 96), DES-M2-best released; the actual k is reported (at most the number of distinct signatures in R) | DES-M2 on k | k DES |
 | Generator ablations GSV_R(k), GSV_R+P10(k), GSV_R+P11(k) | GSV with G replaced by R, by R ∪ P10(R), or by R ∪ P11 | as GSV on the smaller set | 3,000, 6,000, or 3,200 M2 + k DES |
 
-Anchors: the M2 optimum over G (= GSV(1)), the DES-M2 optimum over G (= GSV at k equal to the number of distinct signatures), and the DES-M2 optimum over R.
+Anchors: the M2 optimum over G (= GSV(1) under the M2 key; when the §5.5 key switch is in force, the headline-key GSV(1) is reported beside it), the DES-M2 optimum over G (= GSV at k equal to the number of distinct signatures), and the DES-M2 optimum over R.
 
 For distribution arms, the reported value is the median DES-M2 makespan over the arm's distribution (exact, because every candidate is enumerated). For single-wave arms it is the DES-M2 makespan of the released wave. Every arm, including GSV and R-verify, also reports the M2 value of its released wave or its M2 median, so that Study 2 values can be placed next to Study 1.
@@ -183,5 +183,5 @@
 | **G2 screening versus heuristic scoring** | share of cells where the cell mean of GSV(20) is below the cell mean of P8-verify(20) (same 20 DES verifications and the same P10 operator; GSV additionally screens 6,200 candidates in closed form) | ≥ 75%: "closed-form screening of a generated set outperforms heuristic scoring at the same verification budget" | 50% to 75%: "closed-form screening is comparable to heuristic scoring at the same verification budget" | < 50%: "closed-form screening does not outperform heuristic scoring at the same verification budget; reported as a boundary of the procedure" |
 | **G2′ versus local search** | share of cells where the cell mean of GSV(20) is at or below the cell mean of P7-matched (ties count as matches; same M2 and DES budgets, same P10 operator, same de-duplication) | ≥ 50%: "matches or beats a budget-matched local search" | 25% to 50%: "approaches a budget-matched local search" | < 25%: "a budget-matched local search remains stronger" |
-| **G3 screening fidelity** | per decision k\* = smallest k in the grid with r(k) ≤ the regret tolerance (§7.1), under the headline screening key; per cell the median k\* over pools | median k\* ≤ 20 in ≥ 80% of cells: "a shortlist of 20 suffices" | median k\* ≤ 50 in ≥ 80% of cells: "a shortlist of 50 suffices" | otherwise: "closed-form screening is not a reliable pre-filter at shortlist sizes up to 100" |
+| **G3 screening fidelity** | per decision k\* = smallest k in the grid with r(k) ≤ the regret tolerance (§7.1), under the headline screening key; per cell the median k\* over pools | median k\* ≤ 20 in ≥ 80% of cells: "a shortlist of 20 suffices" | median k\* ≤ 50 in ≥ 80% of cells: "a shortlist of 50 suffices" | otherwise: "closed-form screening does not bring the shortlist down to 50 in more than one fifth of the cells" |
 | **G4 ordering on constructed candidates** | share of P11 candidates (all decisions) with M1 ≤ M2 | ≥ 95%: "the ordering persists on candidates built to create co-rides" | 80% to 95%: "the ordering weakens on constructed candidates; screening uses max{M1, M2} for them" | < 80%: "the choice of elevator model matters once composition exploits co-occupancy" |
 | **G5 warm start** | (a) share of warm-state evaluations with M1 ≤ M2 at steps 2 to 5, on 300 candidates per step drawn from the step's random pool R_s; (b) median over chain units (configuration × pool × release variant) of the retention ratio R_u = mean over steps 2 to 5 of (mean P0 increment − GSV increment) divided by the step-1 gain (mean P0 increment − GSV increment at step 1); units with a non-positive step-1 gain are excluded and counted | (a) ≥ 95% and (b) ≥ 0.80: "the single-wave advantage is retained at warm state" | one of (a), (b) met: "partially retained at warm state" | neither: "single-wave results do not transfer to consecutive waves" |
@@ -257,5 +257,5 @@
 
 ## 14. Contingencies and deviations
-- **Runtime.** Measured on toy waves (2026-09-26): about 0.3 ms per DES-M2 run at n = 16 and 0.75 ms at n = 30, so full enumeration is expected to take hours. The binding projection is made during Stage L2 on a training pool of configuration 17 (the largest), timing one full decision per size and scaling to 18 × 8 pools. If it exceeds 48 hours, the subset mode is used for the whole study, set as `des_subset_mode: yes` in the L2 addendum before any test pool exists (the drivers read it there; there is no command-line switch in real runs): DES is evaluated for the top 500 distinct signatures under each screening key and under M1 (with every candidate tied at the M1 minimum, so DL_M1 is defined), 500 distinct signatures drawn uniformly (stream 97), every shortlist with k ≤ 100, and the P8-verify shortlist; distribution arms use a fixed 200-candidate subsample each (stream 97 with a fixed per-arm offset), and each re-ordered arm uses the images of its base arm's subsample, so G1 stays paired; values are shared by signature; shortlists with k > 100, G3, G8, and the anchors are then defined on the evaluated subset.
+- **Runtime.** Measured on toy waves (2026-09-26): about 0.3 ms per DES-M2 run at n = 16 and 0.75 ms at n = 30, so full enumeration is expected to take hours. The binding projection is made during Stage L2 on a training pool of configuration 17 (the largest), timing one full decision per size and scaling to 18 × 8 pools. If it exceeds 48 hours, the subset mode is used for the whole study, set as `des_subset_mode: yes` in the L2 addendum before any test pool exists (the drivers read it there; there is no command-line switch in real runs; an empty `des_subset_mode` field is read as no): DES is evaluated for the top 500 distinct signatures under each screening key and under M1 (with every candidate tied at the M1 minimum, so DL_M1 is defined), 500 distinct signatures drawn uniformly (stream 97), every shortlist with k ≤ 100, and the P8-verify shortlist; distribution arms use a fixed 200-candidate subsample each (stream 97 with a fixed per-arm offset), and each re-ordered arm uses the images of its base arm's subsample, so G1 stays paired; values are shared by signature; shortlists with k > 100, G3, G8, and the anchors are then defined on the evaluated subset.
 - **P9 (decision D-L).** If P9 cannot run at Study 2 scale by the code freeze, it is removed before any Study 2 result is computed, and the removal is recorded with its reason.
 - **Calibrated case (decision D-K).** If D-K is not signed or the data cannot be obtained under its license, §11 is dropped before any Study 2 result is computed, and the drop is recorded.
@@ -270,6 +270,6 @@
 
 ```
-Design, arms, metrics, gates, analysis, and contingencies (L1) reviewed and locked:  [ ]  ______________  date ________
-Decisions D-K (case) and D-L (P9) as recorded in 01_DECISIONS_TO_SIGN:                [ ]  ______________  date ________
+Design, arms, metrics, gates, analysis, and contingencies (L1) reviewed and locked:       [ ]  ______________  date ________
+Decisions D-K (case), D-L (P9) and D-M (thresholds) as recorded in 01_DECISIONS_TO_SIGN:  [ ]  ______________  date ________
 ```
-To sign: in one edit, tick the boxes above, set `author_signoff` to "SIGNED (<name>, <date>)", and replace the `status` line (for example "SIGNED; nothing executed as of <date>"); then run `make_manifest.py SIGNED` and register the signed file on OSF. Do not edit this file afterwards: the guard stops every registered run if its bytes change, and a changed file cannot be re-pinned. The SHA-256 of this file and the OSF identifier are recorded in the manifest, on OSF, and in the L2 addendum, never in this file.
+To sign: in one edit, tick the boxes above, set `author_signoff` to "SIGNED (<name>, <date>)", and replace the `status` line (for example "SIGNED; nothing executed as of <date>"). If decision D-M selects the draft-1 tolerance (2%) or changes any §7.2 gate value, edit §7.1 and §7.2 to the chosen values in this same signing edit and set REGRET_TOL_ABS (0.0 for the draft-1 tolerance) and GATES in `prototype/src/phase6_config.py` to the same values before the code freeze of §12; the decision sheet and this protocol must agree at signature, because the guard compares hashes only. Run, from the repository root, `python "revision_2026-09-26_ijpr/archive_package/make_manifest.py" SIGNED`; then open `MANIFEST_SIGNED.md` and confirm that the signoff column of every registration starts with SIGNED or ACKNOWLEDGED (the guard does not recognise curly quotes). Then register the signed file on OSF. Do not edit this file afterwards: the guard stops every registered run if its bytes change, and a changed file cannot be re-pinned. The SHA-256 of this file is recorded in the manifest and on OSF; the OSF identifier is recorded in the L2 addendum and in the manuscript's registration appendix, never in this file.
```

## AMEND-2026-09-26-S1A_reanalyses.md

```diff
--- before
+++ after
@@ -20,5 +20,5 @@
 
 1. Locked verdicts are unchanged: H-D1 PARTIAL (D1-d 57/72 against a gate of 58/72), H-D2 PASS, H-Policy and Supp verdicts as stored. Every item below is reported next to the locked result, never in place of it.
-2. Inputs are the stored artefacts listed per item, read only. Stored artefacts are never overwritten; outputs go to new files named `v0_5_phase5_S1-<item>_*.json`.
+2. Inputs are the stored artefacts listed per item, read only. Stored artefacts are never overwritten; outputs go to new files named `v0_5_phase5_<item>_*.json` (item = S1-1, S1-6, S1-7 or TH-2; TH-2 writes `v0_5_phase5_TH-2_abstraction_bias.json` and its figure under `results/figures/`).
 3. Every output file records the SHA-256 of each input file and of this registration.
 4. Informal values computed before this registration (the 2026-09-25 audit, readiness assessment Part 1) are disclosed per item. They are not results and are not quoted in the manuscript.
@@ -63,9 +63,9 @@
 - Stability = share of clustered bootstrap replicates (the S1-1 procedure, B = 2,000, seed 20260928) in which the Hedge corner equals the full-data Hedge corner; the same for the minimax-regret corner.
 
-**Display.** One table row per configuration: Hedge corner (mean, median), minimax-regret corner (mean, median), agreement flags, margin, stability. The Block C extension (S1-3) adds rows for the other configurations, marked as [NS] extension rows.
+**Display.** One table row per configuration: Hedge corner (mean, median), minimax-regret corner (mean, median), agreement flags, margin (mean, median), stability (mean, median). The Block C extension (S1-3) adds rows for the other configurations, marked as [NS] extension rows.
 
-**Wording rule (locked).** A Hedge choice with stability below 0.80 is described as "not stable under resampling" for that configuration; a margin below 1% is described as "a near tie". The locked D2-d collapse count (6/6) is reported unchanged. Disclosure: the 0.80 threshold was set after the informal stabilities 0.43 to 0.78 (5 of 6 configurations) had been seen, so the "not stable" outcome for those configurations is foreseeable and is labelled prior-exposed in the manuscript.
+**Wording rule (locked).** A Hedge choice with stability below 0.80 is described as "not stable under resampling" for that configuration; a margin below 1% is described as "a near tie". Both labels are decided on the class-median basis (the Section 3 decision statistic, the basis of the disclosed prior-exposure margins); the class-mean values are reported in the same row beside them, and where the two bases give a different Hedge corner or a different label the manuscript states the disagreement in the same sentence. The locked D2-d collapse count (6/6, class-mean basis) is reported unchanged. Disclosure: the 0.80 threshold was set after the informal stabilities 0.43 to 0.78 (0.43 to 0.78 in 5 of 6 configurations in the readiness record; the master's summary of the same audit records the six-configuration range as 0.43 to 0.94; no per-configuration artefact of that informal computation is stored) had been seen, and the 1% threshold was set after the stored median margins (0.96%, 0.84%, and 0.14% below it; 1.04% just above) had been seen, so the "not stable" and "near tie" outcomes for those configurations are foreseeable and are labelled prior-exposed in the manuscript.
 
-**Prior exposure.** The stored [RA] median block (2026-09-11) gives median margins of 2.29%, 5.59%, 0.96%, 1.04%, 0.84%, and 0.14% and median and mean Hedge corners that disagree in one configuration (5/6 agree). The 2026-09-25 audit computed informal clustered selection stabilities of 0.43 to 0.78 in 5 of 6 configurations. The minimax-regret corner has not been computed.
+**Prior exposure.** The stored [RA] median block (2026-09-11) gives median margins of 2.29%, 5.59%, 0.96%, 1.04%, 0.84%, and 0.14% and median and mean Hedge corners that disagree in one configuration (5/6 agree). The 2026-09-25 audit computed informal clustered selection stabilities of 0.43 to 0.78 in 5 of 6 configurations (readiness assessment Part 1, line 117); the master's summary of the same audit records the range over all six configurations as 0.43 to 0.94 (MASTER_REVISION_BY_SECTION.md §00.3), so the 0.80 threshold lies between the five low values and the one high value; no per-configuration artefact of that informal computation is stored, and the informal values were computed on the tie-break-fixed CSV, the secondary data here. The minimax-regret corner has not been computed.
 
 ---
@@ -95,7 +95,7 @@
 - Supp-2 capacity rows (`mvs_v0_5_supp2_capacity.csv`, c ∈ {2, 3, 4, 5}, size 16) for the capacity facet. These rows carry no candidate identifiers, so the capacity facet uses rows as drawn.
 
-**Display.** Distribution of B over waves (rows as drawn, and deduplicated by candidate where identifiers exist), faceted by E, F, n (from S1-3), and c (from Supp-2); median and interquartile range per facet; share of waves with B < 0 (reversals), cross-referenced with the B-1 channel decomposition.
+**Display.** Distribution of B over waves (rows as drawn, and deduplicated by candidate where identifiers exist), faceted by E and F (Block C rows plus the S1-3 extension rows, marked [NS]; Block C alone has E = 2 and F in {3, 5}, so these two facets are informative only after S1-3 has run and are then built on the merged rows), n (from S1-3), and c (from Supp-2); median and interquartile range per facet; share of waves with B < 0 (reversals), cross-referenced with the B-1 channel decomposition.
 
-**Wording rule (locked).** "In this benchmark the throughput abstraction is optimistic by a median of x% (interquartile range a% to b%)", with x from the primary Block C data at size 16. Facet medians are reported in the figure, not merged into x.
+**Wording rule (locked).** "In this benchmark the throughput abstraction is optimistic by a median of x% (interquartile range a% to b%)", with x the median of B over the rows as drawn of the primary (tie-break-fixed) Block C data at size 16, all six configurations (1, 3, 5, 7, 9, 11) and all five arms pooled (200 rows per arm, 1,000 rows per configuration, 6,000 rows in total; repeated candidates keep their multiplicity, so the four corner arms weigh 4:1 against the random arm). The deduplicated median (one row per distinct candidate within configuration and arm) and the secondary (stored CSV) as-drawn median are reported beside x, never in its place. Facet medians are reported in the figure, not merged into x.
 
 **Prior exposure.** The 2026-09-25 audit computed an informal median B of 41% on the tie-break-fixed Block C CSV. No facet has been computed.
@@ -108,3 +108,3 @@
 Author: ____________________  Date: ____________
 ```
-To sign: in one edit, set `author_signoff` to "SIGNED (<name>, <date>)" and replace the `status` line; then run `make_manifest.py SIGNED`. The file's SHA-256 is recorded in `MANIFEST_SIGNED.json` and on OSF, never in this file, and the file is not edited afterwards.
+To sign: in one edit, set `author_signoff` to "SIGNED (<name>, <date>)" and replace the `status` line; then Run, from the repository root, `python "revision_2026-09-26_ijpr/archive_package/make_manifest.py" SIGNED`; then open `MANIFEST_SIGNED.md` and confirm that the signoff column of every registration starts with SIGNED or ACKNOWLEDGED (the guard does not recognise curly quotes). The file's SHA-256 is recorded in `MANIFEST_SIGNED.json` and on OSF, never in this file, and the file is not edited afterwards.
```

## AMEND-2026-09-26-S1B_new_simulations.md

```diff
--- before
+++ after
@@ -19,5 +19,5 @@
 ## General rules
 
-1. Simulator: production `simulate_wave` as of the G0 code freeze (tie-break fixed 2026-09-11), deterministic M1 and M2; M3 only where stated.
+1. Simulator: production `simulate_wave` at the code tree hash recorded in MANIFEST_SIGNED.json, or at a later hash whose difference from it touches no file that the Study 1 scripts import (each output records the hash of the code that ran next to the pinned one, and any difference is listed in EXECUTION-LOG.md before the result is used) (tie-break fixed 2026-09-11), deterministic M1 and M2; M3 only where stated.
 2. No stored artefact is overwritten. Outputs: `results/v0_5_phase5_S1-<item>_*.json` and `results/raw/mvs_v0_5_phase5_S1-<item>_*.csv`.
 3. None of these items has a gate. Each is descriptive and reported beside the locked verdicts, never merged into their counts.
@@ -38,5 +38,5 @@
 - Exact class medians of the four corners and of the whole pool; exact H_up, M_Φ, GAP with (i) the stored favourable corner, which is primary because it is the corner the preregistered rule actually chose (Block A pools only, under the model the pool was seeded for; Block C has no stored corner), and (ii) the corner from `fit_phi_beta` on the full pool, secondary (and the only one for Block C); exact corner sizes and pairwise overlaps (overlaps arise only from quantile ties).
 - Pool optimum (lowest makespan and its tie count) under each model.
-- Covering partitions: exact class medians on the 2 × 2, 3 × 3, and 4 × 4 quantile partitions of (C, I) over the full pool (binning rule of `experiments_phase5_ablation._bin`, as used by A-R1), with H_up(P), S_or(P), UB(P) = H_up(P) + S_or(P), and the share H_up(P)/UB(P) of Corollary 1 in `SECTION_4_METHODOLOGY.md` §4.2.3 (diagnostic resolution) and of A-R1. M_Φ(P) is also reported, with the favourable cell defined as the extreme bin in the direction of the fitted signs; this generalizes the corner rule and is labelled as such.
+- Covering partitions: exact class medians on the 2 × 2, 3 × 3, and 4 × 4 quantile partitions of (C, I) over the full pool (binning rule of `experiments_phase5_ablation._bin`, as used by A-R1), with H_up(P), S_or(P), UB(P) = H_up(P) + S_or(P), and the share H_up(P)/UB(P) of Corollary 1 in `SECTION_4_METHODOLOGY.md` §4.2.3 (diagnostic resolution; label of the 2026-09-14 version; planned to be folded, together with Theorem 1, into Proposition 2 in the IJPR numbering, master §00.5) and of A-R1. M_Φ(P) is also reported, with the favourable cell defined as the extreme bin in the direction of the fitted signs; this generalizes the corner rule and is labelled as such.
 - Minimax-reduction quantities (Theorem 2 in `SECTION_4_METHODOLOGY.md` §4.4.1, planned as Corollary 1(a) in the IJPR numbering) on full classes: the per-candidate ordering rate M1 ≤ M2, the minimax corner on class medians and on class means (the D2-d basis), and the one-sided bound U_c(0.05) computed on full classes.
 - For the 12 Block B cells: the gap of the stored P5, P6, P7, P8, and P9 cell medians (M2; P8 from `b2_b3_benchmarks.json`, P9 from `amendC1_p9_spoplus.json`) to the exact pool optimum, (value − optimum) / optimum. The stored medians predate the 2026-09-11 tie-break fix while the optimum uses the current simulator; this is stated with the table. P7 searches the whole order pool, so its gap can be negative; this is reported as it falls.
@@ -90,7 +90,7 @@
 **Background.** While modularizing the B-5 engine for Study 2 (`src/des_evaluator.py`, 2026-09-26), the assistant found that B-5's service pass boarded requests only onto trips opened before the pass, so two matching requests served in the same pass while two cars were free rode separately. The M2 rule of Section 3 (and the closed-form evaluator) boards first. DES-M1 is unaffected. With `b5_compat=True` the new module reproduces B-5 exactly (800/800 toy cases); in the module's self-test (seed 424,244) the corrected rule changes 73 of 400 DES-M2 cases and 0 of 400 DES-M1 cases. No Phase 5 wave has been run under the corrected rule.
 
-**Design.** Rerun the B-5 protocol exactly (configurations 1, 7, 11; size 16; Block C candidate pools `_seed(cid, 99, 16)`; the random arm for all three and the four corners for configuration 7; 200 waves per arm; closed-form M1, M2 and DES-M1, DES-M2) with `des_makespan(..., b5_compat=False)`, writing `prototype/results/v0_5_phase5_S1-12_b5_boardfirst.json` (general rule 2; the stored B-5 output is not touched). The output records the SHA-256 of this registration, of the stored B-5 output, and the code tree hash. The closed-form side uses the current simulator.
+**Design.** Rerun the B-5 protocol exactly (configurations 1, 7, 11; size 16; Block C candidate pools `_seed(cid, 99, 16)`; the random arm for all three and the four corners for configuration 7; 200 waves per arm; closed-form M1, M2 and DES-M1, DES-M2) with `des_makespan(..., b5_compat=False)`, writing `prototype/results/v0_5_phase5_S1-12_b5_boardfirst.json` (general rule 2; the stored B-5 output is not touched). The output records the SHA-256 of this registration, of the stored B-5 output, and the code tree hash. The closed-form side uses the current simulator. Because the stored B-5 closed-form values predate the 2026-09-11 tie-break fix, the rerun changes two things at once. The reproduction pass that the script runs first on the random arm with `b5_compat=True` must reproduce the stored B-5 DES-M2 mean of each configuration to within 1e-6, otherwise the script stops and prints both means; its rows are kept, and their Spearman rho (M1 and M2) against the current closed-form values is reported as a tie-break-only column beside the stored and the `b5_compat=False` columns, so the boarding-rule effect is read as the difference between the last two. The DES ordering rate and the configuration 7 DES decomposition involve no closed-form value and are reported once. No additional DES runs are needed.
 
-**Reporting rule (locked before running).** Identical to S1-9: the B-5 verdict of record stays (Spearman gate not met; DES ordering 0.98 to 1.00; "faithful ordinal proxy" not supported). The rerun values (Spearman ρ per configuration, DES ordering rate, mean DES-M2 against closed-form M2, the configuration 7 DES decomposition) are reported beside the stored ones; if the gate outcome would differ, the main text says so next to the verdict.
+**Reporting rule (locked before running).** Identical to S1-9: the B-5 verdict of record stays (Spearman gate not met; DES ordering 0.98 to 1.00; "faithful ordinal proxy" not supported). The rerun values (Spearman ρ per configuration, with the tie-break-only column `rho_M1_tiebreak_only` and `rho_M2_tiebreak_only` from the `b5_compat=True` pass beside the `b5_compat=False` values, DES ordering rate, mean DES-M2 against closed-form M2, the configuration 7 DES decomposition) are reported beside the stored ones; if the gate outcome would differ, the main text says so next to the verdict.
 
 ---
@@ -111,5 +111,5 @@
 Author: ____________________  Date: ____________
 ```
-To sign: in one edit, tick the S1-11 box below, set `author_signoff` to "SIGNED (<name>, <date>)", and replace the `status` line; then run `make_manifest.py SIGNED`. The file's SHA-256 is recorded in `MANIFEST_SIGNED.json` and on OSF, never in this file, and the file is not edited afterwards.
+To sign: in one edit, tick the S1-11 box below, set `author_signoff` to "SIGNED (<name>, <date>)", and replace the `status` line; then Run, from the repository root, `python "revision_2026-09-26_ijpr/archive_package/make_manifest.py" SIGNED`; then open `MANIFEST_SIGNED.md` and confirm that the signoff column of every registration starts with SIGNED or ACKNOWLEDGED (the guard does not recognise curly quotes). The file's SHA-256 is recorded in `MANIFEST_SIGNED.json` and on OSF, never in this file, and the file is not edited afterwards.
 ```
 S1-11 included (D-D1 signed):  [ ] yes  [ ] no
```

## AMEND-2026-09-26-S1C_execution_note_B4_B6.md

```diff
--- before
+++ after
@@ -3,5 +3,5 @@
 parent: "revision_2026-07-08/amendments/AMEND-2026-07-08-B_deferred_experiments.md (SIGNED 2026-07-08)"
 date: 2026-09-26
-status: "DRAFT note; adds no design, gate, or reporting rule. NOT signed. Nothing executed."
+status: "DRAFT note; adds no gate or reporting rule; fixes the execution details that AMEND-B left open (item 2). NOT signed. Nothing executed."
 author_signoff: "PENDING (acknowledgement only; the designs and gates were signed on 2026-07-08)"
 ---
@@ -10,9 +10,9 @@
 
 ## 中文摘要
-B-4（换向惩罚、异构容量、服务噪声三项稳健性）与 B-6(ii)（候选池与订单池规模敏感性）在 2026-07-08 已登记签字，但还没有运行，也没有脚本。本说明只记录：按原文执行，不增加、不修改任何设计或门槛；代码按原文规格新写；B-6(i) 三分位方案维持 B-13 的降级（修订轮可选）。
+B-4（换向惩罚、异构容量、服务噪声三项稳健性）与 B-6(ii)（候选池与订单池规模敏感性）在 2026-07-08 已登记签字，但还没有运行，也没有脚本。本说明只记录：按原文执行，不增加任何门槛，只固定 AMEND-B 未写明的执行细节（第2项）；代码按原文规格新写；B-6(i) 三分位方案维持 B-13 的降级（修订轮可选）。
 
 ## What this note fixes
-1. **Items.** S1-4 = AMEND-B B-4 exactly as registered (6 Block C configurations; direction-switch penalty 3 s; heterogeneous per-elevator capacities; service-time noise σ ∈ {0.2, 0.5}; per-wave ordering rate and Hedge/DRO agreement per configuration; the D2-a-style gate, ≥ 90% average and ≥ 80% worst cell within each variant). S1-5 = AMEND-B B-6(ii) exactly as registered (Block A on configurations 1 and 7 with candidate pools of 1,500, 3,000, 6,000 and order pools of 300, 600, 1,200; descriptive; pool-robustness claimed only if corner identities are stable in at least 5 of 6 settings).
-2. **Unspecified details, fixed now before running.** The heterogeneous-capacity variant uses capacities (1, 3) for E = 2 (the only E in the Block C configurations), with the smaller capacity on the first elevator. This keeps the total capacity of the homogeneous (2, 2) baseline, mirroring the prototype-scale "spread, same total" setting [1, 2, 3] of `experiments_B1_heterogeneous_pool.py`; a mix such as (2, 3) was rejected because it would also add capacity. Seeds follow the Block C convention `_seed(cid, 99, 16)` for B-4 and the Block A convention for B-6(ii); the order pool for B-6(ii) at size P uses `generate_pool(demand, F, P, seed = SEED_BASE + cid)`. Simulator: current production code at the G0 freeze.
+1. **Items.** S1-4 = AMEND-B B-4 exactly as registered (6 Block C configurations; direction-switch penalty 3 s; heterogeneous per-elevator capacities; service-time noise σ ∈ {0.2, 0.5}; per-wave ordering rate and Hedge/DRO agreement per configuration; the D2-a-style gate, ≥ 90% average and ≥ 80% worst cell within each variant). S1-5 = AMEND-B B-6(ii) exactly as registered (Block A on configurations 1 and 7 with candidate pools of 1,500, 3,000, 6,000 and order pools of 300, 600, 1,200; descriptive; pool-robustness claimed only if corner identities are stable in >= 5/6 of tested settings; item 2 fixes the tested unit as the (cell, setting) pair, 27 of 32).
+2. **Unspecified details, fixed now before running.** The heterogeneous-capacity variant uses capacities (1, 3) for E = 2 (the only E in the Block C configurations), with the smaller capacity on the first elevator. This keeps the total capacity of the homogeneous (2, 2) baseline, mirroring the prototype-scale "spread, same total" setting [1, 2, 3] of `experiments_B1_heterogeneous_pool.py`; a mix such as (2, 3) was rejected because it would also add capacity. Seeds follow the Block C convention `_seed(cid, 99, 16)` for B-4 and the Block A convention for B-6(ii); the order pool for B-6(ii) at size P uses `generate_pool(demand, F, P, seed = SEED_BASE + cid)`. Simulator: current production code at the code tree hash recorded in `MANIFEST_SIGNED.json`.
    - **M1 in the B-4 variants.** The direction-switch and heterogeneous-capacity models exist only for co-occupancy (M2), so in those two variants M1 is the standard throughput abstraction (E·c = 4 single-rider slots, the same total as (1, 3) and (2, 2)); the variant measures whether the ordering survives a more realistic M2. In the service-noise variants both evaluators carry the same σ.
    - **Common random numbers.** In the service-noise variants the M1 and M2 runs of a wave use the same noise seed (both draw two factors per order in the same FIFO order), so the per-wave comparison isolates the elevator model.
@@ -24,4 +24,6 @@
 Item 2 fixes details that AMEND-B left open (the heterogeneous capacity pair, the seeds, M1 in the B-4 variants, common random numbers, and the B-6(ii) settings and stability rule). They are the natural choices, but they are new decisions: please confirm or change them before signing. The B-6(ii) choice matters most: the registered text lists the two pool sizes without saying whether they are crossed, paired, or varied one at a time; the one-at-a-time reading was chosen because it separates the two factors.
 
+To acknowledge: in one edit, fill the line below, set `author_signoff` to "ACKNOWLEDGED (<name>, <date>)", and replace the `status` line; then run, from the repository root, `python "revision_2026-09-26_ijpr/archive_package/make_manifest.py" SIGNED`; then open `MANIFEST_SIGNED.md` and confirm that the signoff column of every registration starts with SIGNED or ACKNOWLEDGED (the guard does not recognise curly quotes).
+
 ```
 Author acknowledgement: ____________________  Date: ____________
```

## experiments_phase6.py

```diff
--- before
+++ after
@@ -205,4 +205,14 @@
 def _n_tied(values, target: float) -> int:
     return int(np.sum(np.abs(np.asarray(values, dtype=float) - target) <= 1e-9))
+
+
+def _first_k_distinct_scanned(order, sig_ids, k: int) -> Tuple[List[int], int]:
+    """first_k_distinct plus the number of positions of `order` walked to
+    reach k distinct signatures (the candidates scanned of protocol §5.5);
+    the whole order counts when it holds fewer than k distinct signatures."""
+    short = first_k_distinct(order, sig_ids, k)
+    if len(short) < k:
+        return short, int(len(order))
+    return short, int(np.flatnonzero(np.asarray(order) == short[-1])[0]) + 1
 
 
@@ -257,4 +267,5 @@
     orders_by_key = {"M2": ranked(M2, ties), "max": ranked(key_max, ties)}
     shortlists: Dict[Tuple[str, str], Dict[int, List[int]]] = {}
+    scanned: Dict[Tuple[str, str], Dict[int, int]] = {}    # candidates scanned
     for key, order in orders_by_key.items():
         for name, mask in masks.items():
@@ -262,9 +273,12 @@
                 continue
             o = order[mask[order]]
-            shortlists[(key, name)] = {k: first_k_distinct(o, sig, k)
-                                       for k in k_grid}
+            sl = {k: _first_k_distinct_scanned(o, sig, k) for k in k_grid}
+            shortlists[(key, name)] = {k: short for k, (short, _) in sl.items()}
+            scanned[(key, name)] = {k: c for k, (_, c) in sl.items()}
     perm_R = list(Rpos)
     random.Random(cfg.seed6(base, cid, cfg.STREAM["r_verify"], n)).shuffle(perm_R)
-    rverify_short = {k: first_k_distinct(perm_R, sig, k) for k in k_grid}
+    rv = {k: _first_k_distinct_scanned(perm_R, sig, k) for k in k_grid}
+    rverify_short = {k: short for k, (short, _) in rv.items()}
+    rverify_scanned = {k: c for k, (_, c) in rv.items()}
 
     # ---- phase 3: DES-M1 and DES-M2 (full, or the §14 subset) --------------
@@ -418,5 +432,5 @@
     tol_R = max(cfg.REGRET_TOL_REL, cfg.REGRET_TOL_ABS / opt_R)
 
-    def released(short, order_values):
+    def released(short, order_values, n_scanned):
         for g in short:
             single(g)                                    # DES for every entry
@@ -425,4 +439,5 @@
         return {"DES-M2": float(D2[g]), "M2": float(M2[g]), "pos": int(g),
                 "source": str(source[g]), "k_actual": len(short),
+                "n_scanned": int(n_scanned),
                 "regret": float((D2[g] - opt_G) / opt_G),
                 "regret_R": float((D2[g] - opt_R) / opt_R),
@@ -441,7 +456,8 @@
         vals = M2 if key == "M2" else key_max
         label = name if key == "M2" else f"{name}_maxkey"
-        gsv_res[label] = {str(k): released(within_subset(s), vals)
+        gsv_res[label] = {str(k): released(within_subset(s), vals,
+                                           scanned[(key, name)][k])
                           for k, s in sl.items()}
-    rverify = {str(k): released(within_subset(s), M2)
+    rverify = {str(k): released(within_subset(s), M2, rverify_scanned[k])
                for k, s in rverify_short.items()}
 
@@ -627,4 +643,5 @@
     epoch, prev_c, stopped = 0.0, 0.0, None
     for s in range(1, steps + 1):
+        screen = None                     # GSV arm: k verified, candidates scanned
         seed = (cfg.seed6(base, cid, cfg.STREAM["warm_start"] + s, n)
                 + 1000 * cfg.WARM_ARM_INDEX[arm] + 100 * j)
@@ -668,5 +685,7 @@
             sig_id: Dict[tuple, int] = {}
             sids = [sig_id.setdefault(signature(pool, ix), len(sig_id)) for ix in Gs]
-            short = first_k_distinct(ranked(keyv, ties), sids, cfg.GSV_HEADLINE_K)
+            short, n_scanned = _first_k_distinct_scanned(ranked(keyv, ties), sids,
+                                                         cfg.GSV_HEADLINE_K)
+            screen = {"k_actual": len(short), "n_scanned": n_scanned}
             d2 = {g: after(Gs[g], "DES-M2") for g in short}
             pick = Gs[min(d2, key=lambda g: (d2[g], ties[g]))]
@@ -685,5 +704,5 @@
         c_m2 = ev(orders, "M2")
         log.append({"step": s, "epoch": epoch, "C_DES-M2": c_des, "C_M2": c_m2,
-                    "increment_DES-M2": c_des - prev_c})
+                    "increment_DES-M2": c_des - prev_c, "screen": screen})
         prev_c = c_des
         rel = set(pick)
```

## analysis_phase6.py

```diff
--- before
+++ after
@@ -21,4 +21,5 @@
 import numpy as np
 
+from src import experiments_phase6 as _ep
 from src import phase6_config as cfg
 from src.experiments_phase6 import RESULTS, _write_json, provenance
@@ -199,67 +200,84 @@
         return float(np.mean([ca[k] < cb[k] for k in common]))
 
-    s2 = share_lower(lambda d: gsv20(d, key_label),
-                     lambda d: d["arms"]["P8-verify"]["DES-M2"])
-    s2p = share_lower(lambda d: gsv20(d, key_label),
-                      lambda d: d["arms"]["P7-matched"]["DES-M2"], ties_count=True)
-    rob = {}
-    for k in ROBUST_KEYS:
-        r2 = share_lower(lambda d, k=k: d["robust"][rob_label][k],
-                         lambda d, k=k: d["robust"]["P8-verify"][k])
-        r2p = share_lower(lambda d, k=k: d["robust"][rob_label][k],
-                          lambda d, k=k: d["robust"]["P7-matched"][k], ties_count=True)
-        rob[k] = {"G2_share": r2, "G2_tier": _tier(r2, G["G2"]["upper"], G["G2"]["middle"]),
-                  "G2p_share": r2p,
-                  "G2p_tier": _tier(r2p, G["G2p"]["upper"], G["G2p"]["middle"])}
-    t2 = _tier(s2, G["G2"]["upper"], G["G2"]["middle"])
-    t2p = _tier(s2p, G["G2p"]["upper"], G["G2p"]["middle"])
-    out["G2"] = {"share": s2, "tier": t2, "descriptive_vs_P8_best": share_lower(
-        lambda d: gsv20(d, key_label),
-        lambda d: min(d["arms"]["P8-200"]["DES-M2"], d["arms"]["P8-1"]["DES-M2"]))}
-    out["G2p"] = {"share": s2p, "tier": t2p}
-    out["execution_robustness"] = {
-        "by_evaluator": rob,
-        "G2_lower_elsewhere": any(rank[v["G2_tier"]] < rank[t2] for v in rob.values()
-                                  if v["G2_tier"] and t2),
-        "G2p_lower_elsewhere": any(rank[v["G2p_tier"]] < rank[t2p] for v in rob.values()
-                                   if v["G2p_tier"] and t2p)}
-
-    # inputs to the C3 wording rule (STORY_CONTRACT §8): generator ablations
-    sfx = "" if upper4 else "_maxkey"                  # headline key
-
-    def abl(d, label):
-        lab = label if label == "R" else label + sfx
-        return d["gsv"][lab][head(d)]["DES-M2"] if lab in d["gsv"] else None
-
-    out["C3_wording_inputs"] = {
-        "share_GSV20_released_from_P11": float(np.mean(
-            [d["gsv"][key_label][head(d)]["source"] == "P11" for d in D])),
-        "share_GSV20_released_from_P10": float(np.mean(
-            [d["gsv"][key_label][head(d)]["source"] == "P10" for d in D])),
-        "gain_adding_P11_to_R": mean_cells(
-            lambda d: red(abl(d, "R"), abl(d, "R+P11"))),
-        "gain_adding_P10_to_R": mean_cells(
-            lambda d: red(abl(d, "R"), abl(d, "R+P10"))),
-        "note": "relative DES-M2 reduction of GSV(20) when P11 (or P10) "
-                "candidates are added to R, mean over cells; headline screening key"}
-
-    # G3 (k* under the headline key; tolerance max{2 %, 4 s / optimum})
-    kk = "M2" if upper4 else "max"
-    ck, ckr = defaultdict(list), defaultdict(list)
-    for d in D:
-        ck[(d["config_id"], d["size"])].append(d["k_star"][kk])
-        ckr[(d["config_id"], d["size"])].append(d["k_star"][f"{kk}_vs_R_opt"])
-    med_k = {c: float(np.median([x if x is not None else np.inf for x in v]))
-             for c, v in ck.items()}
-    sh20 = float(np.mean([v <= G["G3"]["upper_k"] for v in med_k.values()]))
-    sh50 = float(np.mean([v <= G["G3"]["middle_k"] for v in med_k.values()]))
-    t3 = ("upper" if sh20 >= G["G3"]["share"] else
-          "middle" if sh50 >= G["G3"]["share"] else "lower")
-    out["G3"] = {"share_k20": sh20, "share_k50": sh50, "tier": t3,
-                 "median_k_star_by_cell": {f"{c[0]}_{c[1]}": v for c, v in med_k.items()},
-                 "companion_k_star_vs_R_opt": {
-                     f"{c[0]}_{c[1]}": float(np.median([x if x is not None else np.inf
-                                                        for x in v]))
-                     for c, v in ckr.items()}}
+    def gates_under_key(key_label, rob_label, sfx, kk, key_name):
+        """G2, G2', the §7.3 execution-robustness companions, the C3 wording
+        inputs and G3 under one screening key (GSV label, robustness label,
+        ablation label suffix, k_star key). Called for the headline key and,
+        when that key is max{M1, M2}, again for the M2 key (§5.5: the M2-key
+        results are reported beside it)."""
+        res: Dict[str, dict] = {}
+        s2 = share_lower(lambda d: gsv20(d, key_label),
+                         lambda d: d["arms"]["P8-verify"]["DES-M2"])
+        s2p = share_lower(lambda d: gsv20(d, key_label),
+                          lambda d: d["arms"]["P7-matched"]["DES-M2"], ties_count=True)
+        rob = {}
+        for k in ROBUST_KEYS:
+            r2 = share_lower(lambda d, k=k: d["robust"][rob_label][k],
+                             lambda d, k=k: d["robust"]["P8-verify"][k])
+            r2p = share_lower(lambda d, k=k: d["robust"][rob_label][k],
+                              lambda d, k=k: d["robust"]["P7-matched"][k], ties_count=True)
+            rob[k] = {"G2_share": r2, "G2_tier": _tier(r2, G["G2"]["upper"], G["G2"]["middle"]),
+                      "G2p_share": r2p,
+                      "G2p_tier": _tier(r2p, G["G2p"]["upper"], G["G2p"]["middle"])}
+        t2 = _tier(s2, G["G2"]["upper"], G["G2"]["middle"])
+        t2p = _tier(s2p, G["G2p"]["upper"], G["G2p"]["middle"])
+        res["G2"] = {"share": s2, "tier": t2, "descriptive_vs_P8_best": share_lower(
+            lambda d: gsv20(d, key_label),
+            lambda d: min(d["arms"]["P8-200"]["DES-M2"], d["arms"]["P8-1"]["DES-M2"]))}
+        res["G2p"] = {"share": s2p, "tier": t2p}
+        res["execution_robustness"] = {
+            "by_evaluator": rob,
+            "G2_lower_elsewhere": any(rank[v["G2_tier"]] < rank[t2] for v in rob.values()
+                                      if v["G2_tier"] and t2),
+            "G2p_lower_elsewhere": any(rank[v["G2p_tier"]] < rank[t2p] for v in rob.values()
+                                       if v["G2p_tier"] and t2p)}
+
+        # inputs to the C3 wording rule (STORY_CONTRACT §8): generator ablations
+        def abl(d, label):
+            lab = label if label == "R" else label + sfx
+            return d["gsv"][lab][head(d)]["DES-M2"] if lab in d["gsv"] else None
+
+        res["C3_wording_inputs"] = {
+            "share_GSV20_released_from_P11": float(np.mean(
+                [d["gsv"][key_label][head(d)]["source"] == "P11" for d in D])),
+            "share_GSV20_released_from_P10": float(np.mean(
+                [d["gsv"][key_label][head(d)]["source"] == "P10" for d in D])),
+            "gain_adding_P11_to_R": mean_cells(
+                lambda d: red(abl(d, "R"), abl(d, "R+P11"))),
+            "gain_adding_P10_to_R": mean_cells(
+                lambda d: red(abl(d, "R"), abl(d, "R+P10"))),
+            "note": "relative DES-M2 reduction of GSV(20) when P11 (or P10) "
+                    "candidates are added to R, mean over cells; screening key "
+                    + key_name}
+
+        # G3 (k* under the given key; tolerance max{2 %, 1 s / optimum}, protocol
+        # §7.1; values computed in experiments_phase6.py from
+        # phase6_config.REGRET_TOL_*)
+        ck, ckr = defaultdict(list), defaultdict(list)
+        for d in D:
+            ck[(d["config_id"], d["size"])].append(d["k_star"][kk])
+            ckr[(d["config_id"], d["size"])].append(d["k_star"][f"{kk}_vs_R_opt"])
+        med_k = {c: float(np.median([x if x is not None else np.inf for x in v]))
+                 for c, v in ck.items()}
+        sh20 = float(np.mean([v <= G["G3"]["upper_k"] for v in med_k.values()]))
+        sh50 = float(np.mean([v <= G["G3"]["middle_k"] for v in med_k.values()]))
+        t3 = ("upper" if sh20 >= G["G3"]["share"] else
+              "middle" if sh50 >= G["G3"]["share"] else "lower")
+        res["G3"] = {"share_k20": sh20, "share_k50": sh50, "tier": t3,
+                     "median_k_star_by_cell": {f"{c[0]}_{c[1]}": v for c, v in med_k.items()},
+                     "companion_k_star_vs_R_opt": {
+                         f"{c[0]}_{c[1]}": float(np.median([x if x is not None else np.inf
+                                                            for x in v]))
+                         for c, v in ckr.items()}}
+        return res
+
+    out.update(gates_under_key(key_label, rob_label, "" if upper4 else "_maxkey",
+                               "M2" if upper4 else "max",
+                               out["headline_screening_key"]))
+    # §5.5 (pre-commitment D-F): when the headline key is max{M1, M2}, the same
+    # single-wave quantities under the M2 key are reported beside it
+    out["companion_M2_key"] = (None if upper4 else
+                               {"key": "M2", **gates_under_key("G", "GSV20", "",
+                                                               "M2", "M2")})
 
     # G5 (warm start)
@@ -370,5 +388,8 @@
     ap.add_argument("--allow-code-change", metavar="LOG_REFERENCE")
     args = ap.parse_args(argv)
-    require_l2(args.selftest, allow_code_change=args.allow_code_change)
+    # the deviation-log reference given with --allow-code-change is stored in
+    # the gates output too (protocol §12 item 7: recorded in every output)
+    _ep.CODE_CHANGE_REF = require_l2(args.selftest,
+                                     allow_code_change=args.allow_code_change)
     base = scratch_dir() if args.selftest else RESULTS
     tag = "selftest_" if args.selftest else ""
```

## experiments_S1_enumeration.py

```diff
--- before
+++ after
@@ -578,9 +578,9 @@
     # log median makespan and on GAP" does not say which (model, size) slice
     # feeds this table (both S1-2's 18 existing configs and S1-11's 36 new
-    # ones supply pools at BOTH sizes {8,30}). Implemented literally by
-    # reporting the main effects and the F x demand interaction table
-    # SEPARATELY for size 8 and size 30 (model fixed at M2/batched, the only
-    # model S1-11 builds pools for), rather than picking one size or
-    # pooling both sizes together, neither of which the registration states.
+    # ones supply pools under both seed models at BOTH sizes {8,30}).
+    # Implemented literally by reporting the main effects and the F x demand
+    # interaction table SEPARATELY for each (model, size) slice, M1 and M2
+    # crossed with n in {8, 30}, rather than picking one slice or pooling
+    # slices together, neither of which the registration states.
     main_effects_by_size = {}
     for key in per_config_summary:
@@ -611,15 +611,13 @@
                                   for k, v in per_config_summary.items()},
            "main_effects_by_size": main_effects_by_size,
-           "d_d1_signoff_caveat": (
-               "S1-11 is registered '[NS; only if D-D1 is signed]' with its "
-               "own sign-off checkbox ('S1-11 included (D-D1 signed)') inside "
-               "AMEND-2026-09-26-S1B_new_simulations.md's body. "
-               "registration_guard.require_signed('S1B') only reads the "
-               "file's YAML front-matter `author_signoff` field; it has no "
-               "mechanism to read that body checkbox. This script therefore "
-               "enforces the guard key it was told to use (S1B) but CANNOT "
-               "mechanically verify the separate D-D1 condition -- the "
-               "author must confirm the checkbox by hand before treating "
-               "this output as authorized, even after S1B is signed.")}
+           "d_d1_signoff_note": (
+               "S1-11 is registered '[NS; only if D-D1 is signed]'. In real "
+               "mode it runs only if the 'S1-11 included (D-D1 signed)' line "
+               "in AMEND-2026-09-26-S1B_new_simulations.md is ticked '[x] yes'; "
+               "this is enforced mechanically by "
+               "registration_guard.require_checkbox('S1B', 'S1-11 included', "
+               "'yes') in main(), in addition to require_signed('S1B'). "
+               "Self-test runs skip both guards and write only to the "
+               "scratch directory.")}
 
 
```

## analysis_S1_displays.py

```diff
--- before
+++ after
@@ -121,25 +121,64 @@
 EXPECTED_OPS = {"fifo", "cluster"}
 EXPECTED_ARMS = {"random", "phi_corner"}
+STORED_MV_TOL = 1e-9
+
+
+def _stored_mv_check(gain_rows: list, stored_per_cell: list,
+                     tol: float = STORED_MV_TOL) -> dict:
+    """S1-7 Quantities: the stored MV values serve only as a check. Compares
+    the recomputed median_fifo, median_cluster and dispatch_gain of every
+    (configuration, size, arm) with the stored per-cell median_fifo,
+    median_cluster and MV of `v0_5_phase5_supp.json` (Supp1_H1_at_scale)."""
+    stored = {(int(r["config_id"]), int(r["size"]), str(r["arm"]).lower()): r
+              for r in stored_per_cell}
+    pairs = (("median_fifo", "median_fifo"), ("median_cluster", "median_cluster"),
+             ("dispatch_gain", "MV"))
+    n_compared, max_abs_diff, mismatches, missing = 0, 0.0, [], []
+    for row in gain_rows:
+        key = (row["config_id"], row["size"], row["arm"])
+        if key not in stored:
+            missing.append(list(key))
+            continue
+        n_compared += 1
+        for mine, theirs in pairs:
+            diff = abs(float(row[mine]) - float(stored[key][theirs]))
+            max_abs_diff = max(max_abs_diff, diff)
+            if diff > tol:
+                mismatches.append({"config_id": key[0], "size": key[1],
+                                   "arm": key[2], "quantity": mine,
+                                   "recomputed": float(row[mine]),
+                                   "stored": float(stored[key][theirs]),
+                                   "abs_diff": diff})
+    return {"n_stored_cells": len(stored), "n_compared": n_compared,
+            "n_recomputed_not_in_stored": len(missing),
+            "recomputed_not_in_stored": missing,
+            "max_abs_diff": max_abs_diff, "tolerance": tol,
+            "all_agree": bool(n_compared == len(stored) and not mismatches
+                              and not missing),
+            "mismatches": mismatches}
 
 
 def run_s1_7(selftest: bool) -> dict:
+    stored_per_cell = None
     if selftest:
         df = _fabricate_supp1()
         supp_json_hash = "n/a (selftest: fabricated in-memory)"
+        stored_check = {"status": "n/a (selftest: fabricated in-memory)"}
     else:
         df = pd.read_csv(RAW_DIR / "mvs_v0_5_supp1_h1scale.csv")
         supp_json_path = RESULTS_DIR / "v0_5_phase5_supp.json"
-        # REGISTRATION NOTE (analysis_S1_displays.py, run_s1_7): S1-7 lists
-        # `v0_5_phase5_supp.json` among its Inputs (for the "already stored
-        # as MV" dispatch-gain figure). Absolute Rule 1 tonight forbids
-        # loading values out of ANY stored result file, and this script's
-        # real-mode path is written to run correctly after sign-off, not
-        # tonight -- but to avoid depending on an internal JSON schema this
-        # session never inspected, every S1-7 quantity below (including the
-        # dispatch gain) is recomputed directly from the raw CSV instead of
-        # parsed out of that JSON. The JSON is only hashed, for the audit
-        # trail the output format requires.
+        # S1-7 Quantities: "Every quantity is computed from the raw CSV; the
+        # stored MV values of the JSON serve only as a check." Every S1-7
+        # quantity below is recomputed from the raw CSV; the stored per-cell
+        # values of Supp1_H1_at_scale.per_cell are then compared with the
+        # recomputed dispatch-gain rows (stored_MV_check, _stored_mv_check)
+        # and the JSON is hashed for the audit trail.
         supp_json_hash = (_sha256_file(supp_json_path)
                           if supp_json_path.exists() else None)
+        if supp_json_path.exists():
+            with open(supp_json_path, encoding="utf-8") as f:
+                stored_per_cell = json.load(f)["Supp1_H1_at_scale"]["per_cell"]
+        else:
+            stored_check = {"status": "n/a (v0_5_phase5_supp.json not found)"}
 
     ops_vals = set(df["ops_policy"].astype(str).str.lower().unique())
@@ -212,6 +251,9 @@
                         "dispatch_gain": (float(med_fifo) - float(med_cluster))
                                         / float(med_fifo)})
-
-    return {"supp_json_sha256": supp_json_hash, "per_cell": cell_rows,
+    if stored_per_cell is not None:
+        stored_check = _stored_mv_check(gain_rows, stored_per_cell)
+
+    return {"supp_json_sha256": supp_json_hash, "stored_MV_check": stored_check,
+           "per_cell": cell_rows,
            "aggregates": aggregates, "wording_rule_outcome": wording,
            "n_cells_A_cluster_positive": f"{n_pos_cluster}/{n_cells_cluster}",
@@ -310,4 +352,11 @@
                               ignore_index=True)
         result["facet_n_with_S1-3_extension"] = _facet_stats(combined_n, "size")
+        # S1A TH-2 Display: the E and F facets are built on the merged rows
+        # once S1-3 has run (Block C alone has E = 2 and F in {3, 5}); the
+        # Block C-only facets above stay as companions.
+        cols = ["n_elevators", "F", "B"]
+        combined_ef = pd.concat([primary[cols], s1_3[cols]], ignore_index=True)
+        result["facet_E_with_S1-3_extension"] = _facet_stats(combined_ef, "n_elevators")
+        result["facet_F_with_S1-3_extension"] = _facet_stats(combined_ef, "F")
     return result, primary, secondary, supp2
 
@@ -320,6 +369,10 @@
         import matplotlib.pyplot as plt
         plt.rcParams["font.family"] = "Times New Roman"
-        facets = [("facet_E", "elevators E"), ("facet_F", "floors F"),
-                 ("facet_c_supp2", "capacity c")]
+        merged = "facet_E_with_S1-3_extension" in result   # S1-3 rows available
+        facets = [("facet_E_with_S1-3_extension" if merged else "facet_E",
+                   "elevators E" + (" (with S1-3)" if merged else " (Block C)")),
+                  ("facet_F_with_S1-3_extension" if merged else "facet_F",
+                   "floors F" + (" (with S1-3)" if merged else " (Block C)")),
+                  ("facet_c_supp2", "capacity c")]
         fig, axes = plt.subplots(1, len(facets), figsize=(4 * len(facets), 3.2))
         if len(facets) == 1:
```

## experiments_S1_b5_rerun.py（第二轮，助手直接修改；此文件在第一轮备份之外，差异按编辑内容列出）

```diff
     for cid in (1, 7, 11):
         waves = draw_waves(configs[cid], n_per_arm, cand_n)
-        if stored is not None:              # reproduction check of the draws
-            chk = evaluate(configs[cid], waves["random"], b5_compat=True)
+        # Reproduction pass under the old boarding rule (S1B, S1-12 Design):
+        # its rows are kept, and their Spearman rho against the current
+        # closed-form values is the tie-break-only column, so the boarding
+        # effect is read as the difference to the b5_compat=False rho.
+        chk = evaluate(configs[cid], waves["random"], b5_compat=True)
+        if stored is not None:              # reproduction check of the draws
             mean_old = float(np.mean([r["des_M2"] for r in chk]))
 ...
         per_config[cid] = summarise(configs[cid], arm_rows)
+        col = {k: np.array([r[k] for r in chk]) for k in chk[0]}
+        per_config[cid]["rho_M1_tiebreak_only"] = float(
+            spearmanr(col["cf_M1"], col["des_M1"]).statistic)
+        per_config[cid]["rho_M2_tiebreak_only"] = float(
+            spearmanr(col["cf_M2"], col["des_M2"]).statistic)
+        per_config[cid]["des_mean_M2_b5_rule"] = float(col["des_M2"].mean())
```

## amendments/README.md（不签字，属于上传包；第二轮）

```diff
-A one-line pointer at the end of the preregistration's §9 is optional after signing.
+The preregistration stays byte-identical and no pointer is appended to it; the pointer to the 2026-09-26 registrations goes into the manuscript's registration appendix (decision D-I as signed).
```
