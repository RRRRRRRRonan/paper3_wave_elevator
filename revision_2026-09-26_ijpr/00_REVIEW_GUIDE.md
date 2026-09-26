---
title: "审阅指南：2026-09-26 自动工作（第 1 周 + 第 2 周 + 独立审查 + 第 3 周不依赖签字的部分）"
date: 2026-09-26
status: "Weeks 1 and 2 FINAL; week 3 added the same day (section W3 below); nothing here is signed"
---

# 审阅指南

## 签字状态（2026-09-26，最新）

六份登记文件已按你的明确授权签字（签字字段注明"作者在 2026-09-26 会话中明确授权，助手据此录入"），`make_manifest.py SIGNED` 已生成签字清单（113 个文件，代码树 3ef64f08b16b）。守卫对研究一的三份登记和研究二的 L1 三份全部放行，L2 附录仍未签、研究二测试池仍被拦下。**从现在起研究一的登记脚本会真正运行、写入 `prototype/results/`，只在你决定开跑时调用。** 签字件此后一个字节都不能改。

第一周剩下的一步是你本人的操作：按 `archive_package/README_OSF.md` 上传 OSF（选禁运；上传集可直接用 `to_sign_copies/now/` 加 `MANIFEST_SIGNED.md`），把 OSF 编号记到稿件的登记附录（不要写进签字件）。之后按本文件第 7 节的顺序运行研究一；研究二第 4 周先 `tune`（只用训练池）再填签 L2 附录。

## W3. 第 3 周新增

你选的三项都做完了：附录 A 草稿、§4.5 GSV 正文与算法框（已按你的授权以**修订模式**写进 `Methodology.docx`）、案例数据加载器。签字仍未进行，所以研究一、研究二的登记运行仍全部被守卫拦下（已重新逐个验证 18/18）。

| 顺序 | 文件 | 你要做什么 | 预计时间 |
|---|---|---|---|
| W3-1 | `Methodology.docx`（文末 §4.5，修订模式） | 在 Word"审阅"窗格逐段接受或拒绝；8 条批注说明了每处待办。五个公式是黄色占位符，需要你用 MathType 建立；行内符号是普通格式文字，不是 MathType。修订者显示为你的 Word 用户名"诗月 胡"（Word 忽略了自动化设置的用户名），批注里写明是助手插入的 | 30 分钟 |
| W3-2 | `revision_2026-09-26_ijpr/week3/SECTION_4_5_GSV_draft.md` | §4.5 的中英对照源稿与作者说明 1 到 6。重点看**符号**：扩充候选池 𝒦⁺ = 𝒦 ∪ 𝒦^seq ∪ 𝒦^con、筛选键 ψ_k、短名单 𝒦^V（规模 K_V）、释放候选 k†、筛选遗憾 Reg(K_V)、K_V^⋆、事件驱动评估器 M₂^DES。已对照**定稿第 3 节**（`Problem formulation.docx` 的双语镜像）和现行第 4 节核对，避开了已用符号（第 3 节表 3.3 与式 (32) 的选项集合 𝒮、𝒢_τ、s_o、r_o、ρ_q、Δ_H 等；上标 C 容易被读成补集）。协议、代码和 TERMINOLOGY 里仍叫 k 与 r(k)，TERMINOLOGY 已加对照行 | 20 分钟 |
| W3-3 | `revision_2026-09-26_ijpr/week3/APPENDIX_A_draft.md` | **逐行通读**命题 3 的完整证明（引理 A.1 到 A.5、推论 A.1、情形 F/B、全 E 归纳、c = 1、两个反例的完整时间线），读一项就在 `MATH_VERIFICATION_LOG.md` 对应行签一项（文末"审阅说明"第 1 条有对照表：第 4 到 11 行）。第 4 到 12 行都签完后，命题 3 才能改名为定理 1。已请一位独立审查员专门尝试推翻这份草稿：证明主链（引理 A.1 到 A.5、推论 A.1、归纳各步、c = 1）成立；主链之外的 2 处错句、2 处缺口已改正，均不涉及证明步骤（审阅说明第 7 条） | 2 到 3 小时 |
| W3-4 | 同上，文末"审阅说明"第 2 到 4 条 | 三个小决定：① 可选的注 A.2 与引理 A.4(ii)（更强条件下的短证明）保留还是删掉；② 是否在 §4.3.1 命题 3 的式 (46) 后加一句"等价地，当 (a)(b) 成立时，式 (46) 任一不等式反转都要求 (c) 或 (d) 失效"（TH-1 要求）；③ 第 3 节的 D_e（轿厢行程完成时刻）与第 4 节的 D_1(ϱ)、D_2(ϱ) 共用字母 D，是否改名 | 10 分钟 |
| W3-5 | `prototype/src/case_online_retail.py` 与 `experiments_phase6.py case` | 只在合成数据上自测过，没有读取任何真实数据。真跑需要：D-K 选"做案例"、L2 附录填 `case_included: yes` 与四个时间参数的中值和范围、提供 Online Retail II 文件路径 | 以后 |

**目录清理（2026-09-26，应你的要求）。** 过时材料已全部折叠到根目录 `archive/`（全仓库唯一归档处，原 `paper_draft/archive/` 也并入其中）。依据是主控 §1.1 至 §1.3 已判定过时的文件，加上已执行的计划、被取代的版本、工作文件夹和审查快照。共移动 145 个文件，每个文件移动前后哈希一致；删除的只有 Word 残留临时文件、`.pyc` 缓存和空目录。现行文档中的路径已同步更新（改前均有备份）。总索引在 `archive/MANIFEST.md`，逐文件新旧路径在 `archive/CLEANUP_2026-09-26_moves.json`，想恢复任何文件按其中的路径移回即可。根目录 `README.md` 已按现状重写。**清理中发现一处实质问题并已改正**：我第 3 周核对符号时用的是已被 `Problem formulation.docx` 取代的旧第 3 节 md。定稿第 3 节用 𝒮 表示选项集合，所以 §4.5 的短名单已改为 𝒦^V，Word 修订已重做；附录 A 的例子改为直接给出记录序列，证明本身不受影响（见 EXECUTION-LOG 第 42 条）。

第 3 周的其他事实：
1. **Word 只改了 `Methodology.docx`**，改前备份在 `backups/Methodology.docx.orig_2026-09-26`（哈希已记入 `SHA256_before_edits.txt`）。插入后逐段核对：原有 60 段的文字、格式和全部 157 个 MathType 对象与备份一致，差异只有 Word 保存时自动做的规范化。想整体撤销，把备份复制回去即可。
2. **§4.3.2 后半段（式 (47) 起）和 §4.4 没有写进 Word**，因为它们取决于主控 §00.5 的编号决定（定理 2 改推论 1、推论 3 降为注、推论 4 删除）；Word 里留了黄色占位段和批注。§4.5 的公式编号等它们插入后再定。
3. **附录 A 没有写进 Word**：要等你读完并签数学核验记录。两个反例今天又用第 3 节的式 (18) 到 (29) 手算、并用模拟器各跑一次核对：26 对 24、103 对 68，与 7 月一致。
4. 你的 Word 里一直开着 `Problem formulation.docx`（自 9 月 24 日），自动化用的是另一个 Word 实例，没有碰那个窗口。
5. 第 3 周的逐条记录在 `EXECUTION-LOG.md` 第 33 条起。

## 0. 一句话

夜里按你的指示做完了第 1 周（登记文件、故事契约、决定单、术语、主控、OSF 包）和第 2 周（研究二代码、DES 模块、守卫、研究一脚本），又请了两轮独立审查，并在签字前把审查发现的问题全部改掉。全部是**草案**：没有替你签字，没有在任何登记的数据或种子上运行分析，没有上传，没有 git 提交，Word 稿没动。所有登记脚本在你签字前都会被守卫拦下（已逐个验证）；签字后如果文件再被改动一个字节，守卫也会拦下。

## 1. 需要你拍板或签字的（按建议的审阅顺序）

| 顺序 | 文件 | 你要做什么 | 预计时间 |
|---|---|---|---|
| 1 | `revision_2026-09-26_ijpr/01_DECISIONS_TO_SIGN.md` | D-A 到 D-M 逐条写"同意推荐"或改选项，文末签字。重点：D-H（协议现在就锁门槛）、D-K（案例；就绪时间主分析取 0）、D-L（P9 去留）、D-M（门槛数值；**G3 容差要在 2% 与 max{2%, 1 秒} 之间二选一**） | 30 分钟 |
| 2 | `revision_2026-09-26_ijpr/STORY_CONTRACT.md`（已加中文译文，以英文为准） | 通读 C1 到 C3、RQ；重点看 §8：结局表现在是穷尽的（方法强弱 × G1 档位 → A/B/C），加上 C2、C3 的措辞规则。C1 已按你的决定改为 "We construct a reproducible synthetic benchmark"（构建），与 D-J 的 J4（代码按请求提供）一致；签字 | 30 分钟 |
| 3 | `paper_draft/phase6_method_study_protocol.md`（研究二协议，第 3 稿） | 见第 2 节；签 §16（L1） | 1.5 到 2 小时 |
| 4 | `revision_2026-09-26_ijpr/amendments/AMEND-2026-09-26-S1A_reanalyses.md` | 研究一重分析（S1-1、S1-6、S1-7、TH-2）；重点看 S1-1 新写的"两个估计对象"；签字 | 20 分钟 |
| 5 | `.../AMEND-2026-09-26-S1B_new_simulations.md` | 研究一新仿真（S1-2、S1-3、S1-8、S1-9、S1-11、S1-12）；签字，并在文末勾选 S1-11 是否做（取决于 D-D） | 20 分钟 |
| 6 | `.../AMEND-2026-09-26-S1C_execution_note_B4_B6.md` | B-4、B-6(ii) 是 7 月已签的设计；这里补了原文没写的细节（异构容量、M1 定义、共同随机数、B-6(ii) 一次只变一个因素），确认或改后签收 | 10 分钟 |
| 7 | `paper_draft/phase6_protocol_L2_addendum.md` | 现在不用填；第 4 周调参后填写并单独签字 | 以后 |
| 8 | `revision_2026-09-26_ijpr/MATH_VERIFICATION_LOG.md` | 第 3 到 4 周读附录 A 时逐行填写（TH-1） | 以后 |

**签字前审查（2026-09-26，你审过副本之后）：** 96 个代理的审查没有发现阻断项，但确认了 7 处实质缺陷和约 20 处小问题（`helper_reports/presign_audit_2026-09-26.md`）。你授权全部修改后已改完，核实代理的二轮意见也已处理；测试 26/26 通过，守卫 18/18 拦下。**六份文件相对于你审过的版本的全部差异集中在 `helper_reports/presign_fix_diffs_2026-09-26.md`，签字前请只复核这一份。** 两处请你特别确认：(1) S1A 的 S1-6 里，非正式稳定性的记录现在同时引用了就绪评估（5/6 个配置 0.43 到 0.78）和主控（六个配置 0.43 到 0.94），若你记得第六个配置的值实际未算，请改回；(2) D-M 若选 (a) 或改任何门槛数值，须按新加的传播条款同步改协议 §7.1/§7.2 和 `phase6_config.py`。

待签文件的只读副本集中放在 `revision_2026-09-26_ijpr/to_sign_copies/`（已按修正后的原件刷新）（`now/` 六份、`later/` 两份，`00_README.md` 列出每份对应的原件路径），方便阅读和打印；**签字一律签在上表的原件上**，守卫只认原件。

签字方法：每个文件在**同一次编辑**里完成三件事：填写/勾选内容，把 front matter 的 `author_signoff` 改成 `"SIGNED (你的名字, 日期)"`（S1C 也可写 `ACKNOWLEDGED`），把 `status` 行改成已签字的说明。全部签完后在仓库根目录运行 `python "revision_2026-09-26_ijpr/archive_package/make_manifest.py" SIGNED`，再上传 OSF。**生成签字清单之后，这些文件一个字节都不要再改**：守卫会拦下，改完重新登记也会被识别；如需改动，写一份带日期的新修正案。可以分几次签（先签研究一，后签研究二），每次签完用 `--supersede` 重新生成清单即可，已签文件不变就不受影响。

## 2. 协议第 3 稿里请重点看的地方

1. **§2 事先已知结果的披露。** Phase 5 各块、P7/P8/P9、Supp-1 的 10.2%、B-5 DES、9 月 25 日的非正式审计数字，以及今晚代码自测和两位审查员玩具检查里看到的数字（例如玩具 P11 候选 147/160 满足 M1 ≤ M2、第 1 稿的玩具门槛档位、玩具规模下的最优值 38 到 111 秒）。**注意：看过玩具结果之后，G2 的对照、G5(b)、G3 容差这三处门槛定义都改过**，触发原因是两轮审查而不是玩具数值；§2 逐条列明。第 1 稿里"门槛没有因此改动"的说法不准确，已更正。
2. **§3.5 DES-M2 的登梯规则（重要）。** B-5 的事件仿真在同一服务轮里不让第二个同路线请求搭上刚派出的车，与第 3 节和闭式 M2 不一致（手算：43 秒对 24 秒；模块自测里 400 个 DES-M2 案例中 73 个结果不同，DES-M1 不受影响）。研究二一律用修正后的规则；研究一登记了 S1-12 用新规则重跑 B-5，旧判定保留、新数并列。
3. **§4 对照组（审查后改动最大）。** G2 现在和 P8-verify(20) 比（P8 前 20 名、同样经 P10 重排、同样 20 次 DES 验证），因为原来和"零评估的 P8"比几乎必胜，不算检验；G2′ 和同预算局部搜索 P7-matched 比，它现在也能用 P10 重排；所有短名单都按"序列签名"去重（审查员发现 M2 前 20 名里有时只有 9 到 15 个不同的波次）。
4. **§7.3 执行稳健性（新增）。** DES-M2 既挑选又打分，所以把释放出的波次再用"带相位噪声的 DES"（σ = 0.1、0.2，各 20 次重复）和"B-5 语义"重新评价；若这些评价下 G2、G2′ 的档位更低，正文并列两个档位，摘要用较低者。
5. **§7 其他门槛。** G1 措辞不再和闭式调度收益比较；G3 容差：第 1 稿 2%（短波次上约 1 秒，几乎要求精确最优），第 2 稿 max{2%, 4 秒}（第二轮审查发现相当于 3.6% 到 10.5%，过松），第 3 稿 max{2%, 1 秒}，由你在 2% 与 max{2%, 1 秒} 之间选定；G2′ 平局算"持平"；G5(b) 改为"热启动下保留了多少单波优势"（中位数 ≥ 0.8）；G8 措辞改为"选评估器的最优候选"。
6. **§9 热启动** 在 G4 之后运行，使用 G4 决定的筛选键；G5(a) 从随机候选里抽样。
7. **§11 案例** 登记了数据清洗规则（去掉取消单、非商品编码、非正数量等）；仍取决于 D-K。
8. **§14 运行时间预估** 在第 4 周用训练池做；超过 48 小时才启用"子集模式"（已实现，流 97）。
9. **§16 与 L2 附录。** 协议签字后一字不改；哈希记在签字清单和 OSF 上；OSF 编号、P11 权重、案例参数、代码哈希都写在单独的 L2 附录里并单独签字。

## 3. 夜里发现、你需要知道的事实

1. **注册历史的诚实表述**（`archive_package/README_OSF.md` §3）：Phase 5 预注册第一次进 git 是 `2c47cc5`（5 月 20 日 00:29），与 Phase 5 结果同一次提交；预注册文件最后修改时间（5 月 19 日 23:19）晚于原始结果文件（20:28）。仓库本身无法证明锁定设计早于结果；论文应称其为"内部锁定、有签字记录的预注册"，不要声称有外部时间戳。7 月 8 日的六份修正案从未进 git。今天这批登记若在运行前上传 OSF，将是本项目第一批有外部时间戳的登记。
2. **Phase 5 的 D1-d 计数依赖 bootstrap 种子**：非正式看过行级 bootstrap 换种子时在 56 到 58/72 之间，58 正好是门槛。锁定判定（57/72，PARTIAL）不变，S1-1 会把种子范围登记后并列报告。
3. **未提交的代码。** `simulator.py`（9 月 11 日破平修复 + 今晚的可选相位时间参数与测试）、`wave_policies.py`（空角类报错）、`experiments_phase5*.py`（候选编号）都未提交；哈希清单记录了当前代码树。
4. **研究一脚本由辅助代理（Sonnet）编写，我逐个核查后改了 8 处**（`helper_reports/S1_scripts_helper_report_2026-09-26.md`），原始版本保存在 `helper_reports/helper_original_scripts/`。
5. **两轮独立审查**：报告与逐条回应在 `helper_reports/independent_review_2026-09-26.md`（含第二轮）；EXECUTION-LOG 第 19 到 31 条是对应的改动记录。第二轮没有发现阻断性问题。

## 4. 改动过的已有文件（都有备份和差异文件）

| 文件 | 改了什么 | 备份与差异 |
|---|---|---|
| `CLAUDE.md` | IJPR 目标、两个研究、守卫与哈希锁、命名 | `backups/CLAUDE.md.orig_2026-09-26`、`.diff` |
| `paper_draft/TERMINOLOGY.md` | IJPR 版改写；GSV 定义含 P10(R)；P7-matched、P8-verify、P10g、序列签名、执行稳健性 | `backups/TERMINOLOGY.md.orig_2026-09-26`、`.diff` |
| `revision_2026-09-02/MASTER_REVISION_BY_SECTION.md` | 新 §00 覆盖层与指针 | `backups/MASTER_REVISION_BY_SECTION.md.orig_2026-09-26`、`.diff` |
| `prototype/src/simulator.py` | 可选参数 `speed_per_floor`、`load_time`、`unload_time` 和两个测试；默认不传，结果逐值不变（快照 43,200 个值 + 2,100 次随机调用核对） | `backups/simulator.py.orig_2026-09-26`、`.diff` |
| `prototype/requirements.txt` | 加了 `scipy>=1.14`（分析要用，原来漏列） | `backups/requirements.txt.orig_2026-09-26`、`.diff` |
| `Methodology.docx` | 第 3 周：文末以修订模式插入 §4.5 与 8 条批注 | `backups/Methodology.docx.orig_2026-09-26` |
| `revision_2026-09-24/readiness_assessment_CIE_IJPR_2026-09-26.md`、`section3_bilingual_2026-09-24.md`，`revision_2026-09-02/SECTION_4_METHODOLOGY.md` 与 `figures/section4_2026-09-14/FIGURE_DESIGN.md`，`paper_draft/manuscript/*_v1.1*.md` 三份 | 目录清理：只改了指向已归档文件的路径（每份 1 到 2 处） | 各自的 `.orig_2026-09-26` 与 `.diff` |
| `README.md`（根目录） | 目录清理：旧版（四月模板）归档为 `archive/superseded/README_2026-09-03.md`，重写为现状说明 | 旧版即归档件 |

回退：把 `backups/` 里对应的 `.orig_2026-09-26` 文件复制回原位置（`SHA256_before_edits.txt` 有改前哈希）。`wave_policies.py` 备份了但没有改。

## 5. 新建的文件

- 文档：`00_REVIEW_GUIDE.md`（本文件）、`01_DECISIONS_TO_SIGN.md`、`STORY_CONTRACT.md`、`EXECUTION-LOG.md`、`MATH_VERIFICATION_LOG.md`、`amendments/`（S1A、S1B、S1C、README）、`archive_package/`（README_OSF、make_manifest.py、MANIFEST_DRAFT）、`helper_reports/`（两份报告、协议第 1 稿、辅助代理原始脚本）、`paper_draft/phase6_method_study_protocol.md`、`paper_draft/phase6_protocol_L2_addendum.md`。
- 代码（`prototype/src/`）：`registration_guard.py`、`des_evaluator.py`、`phase6_config.py`、`phase6_policies.py`、`experiments_phase6.py`、`analysis_phase6.py`、`experiments_S1_b5_rerun.py`、`analysis_S1_cluster_bootstrap.py`、`experiments_S1_enumeration.py`、`experiments_S1_blockC_ext.py`、`analysis_S1_displays.py`、`experiments_S1_tiebreak_regen.py`、`experiments_S1_B4_B6.py`。

## 6. 没有做的事

- 没有签字、没有上传 OSF 或 Zenodo、没有 git 提交或推送。
- 没有运行任何登记的分析，没有生成研究二的训练池或测试池，没有在存档结果上计算任何新统计量；`prototype/results/` 和 `revision_2026-07-08/tier2_analysis/outputs/` 下没有新文件（已多次核对）。
- 第 1、2 周没有改 Word 稿；第 3 周按你的授权只以修订模式改了 `Methodology.docx`（见 W3 节）。`Problem formulation.docx` 那句"Section 5 also evaluates pools augmented with constructed and re-sequenced candidates (Study 2)."仍未改，待你授权。
- 案例数据加载器、附录 A 草稿已在第 3 周完成（见 W3 节）；附录 A 写进 Word、§4.3.2 后半段与 §4.4 写进 Word、以及依赖签字的正文改写仍未做。

## 7. 签字以后的执行顺序

在仓库根目录：
1. `python "revision_2026-09-26_ijpr/archive_package/make_manifest.py" SIGNED`，然后上传 OSF（`README_OSF.md` §4）。

在 `prototype/` 目录：
2. 研究一（任意顺序，每条几分钟到一小时）：
   - `python -m src.analysis_S1_cluster_bootstrap`
   - `python -m src.analysis_S1_displays s1-6`、`s1-7`
   - `python -m src.experiments_S1_enumeration s1-2`、`s1-8`（`s1-11` 需先勾选）
   - `python -m src.experiments_S1_blockC_ext`，然后 `python -m src.analysis_S1_displays th-2`
   - `python -m src.experiments_S1_tiebreak_regen`、`python -m src.experiments_S1_b5_rerun`
   - `python -m src.experiments_S1_B4_B6`
3. 研究二第 4 周：`python -m src.experiments_phase6 tune`（只用训练池，同时给出运行时间预估）→ 填写并签 L2 附录（含 `des_subset_mode`、代码哈希）→ 在仓库根目录运行 `make_manifest.py SIGNED_L2` → `main`（按配置分块保存，中断后重跑会跳过已完成的配置，全部完成后自动合并；也可 `merge`）→ `python -m src.analysis_phase6`（得到 G4 与筛选键）→ `warmstart`、`runtime` → 再运行一次 `analysis_phase6`。若 L2 之后必须改代码，先在 EXECUTION-LOG 记一条，再加 `--allow-code-change "<那一条>"`。
