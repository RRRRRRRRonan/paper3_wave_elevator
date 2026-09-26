---
title: "Paper 3 master revision by section"
date: 2026-09-02
last_updated: 2026-09-26
status: "ACTIVE MASTER REVISION CONTROL — 单一施工入口（2026-09-26 起叠加 §00 IJPR v2 覆盖层；覆盖层为草案，待作者审阅；原文件备份于 revision_2026-09-26_ijpr/backups/）"
scope: "折叠旧版本，统一 2026-09-02 审查、现有修改文件、理论工作包、实验结果与逐章重写顺序"
supersedes_for_action: "archive/paper_draft/manuscript/00_INDEX.md；archive/revisions/revision_0719_snapshot 中各 README（原 revision_0719）的旧施工结论；W10 中被 2026-08-06/09-02 审查推翻的叙事裁定"
preserves_as_evidence: "冻结预注册、签署修正案、EXECUTION-LOG、原始 JSON/CSV、证明工作包与旧稿审计轨迹"
---

# 2026-09-02 最新统一 Revision：按章节施工

## 00. IJPR v2 覆盖层（2026-09-26，草案，待作者审阅签字）

**来源：** 作者 2026-09-26 决定不投 EJOR、目标 IJPR（退路 C&IE），论文改为决策辅助型，"两个研究、三步流程"。完整计划与证据见 `revision_2026-09-24/readiness_assessment_CIE_IJPR_2026-09-26.md` 第二部分 v2；落地文件见 `revision_2026-09-26_ijpr/`。本覆盖层与该文件夹里的 `01_DECISIONS_TO_SIGN.md`、`STORY_CONTRACT.md` 一同在作者签字后生效。

### 00.1 仍然有效、覆盖层不改的条款

§0.2 审计事实、§0.3 证据标签、§1.4 冲突裁决、§2.4 禁用表述、§3.2 摘要禁用词、§5 相关工作的来源要求、§6 至 §9 各章对研究一内容的全部要求、§10 附录对证明与完整结果的要求、§13 交叉一致性门槛。冻结的 Phase 5 预注册与 2026-07-08 六份修正案不变。

### 00.2 被取代的条款

| 原条款 | 取代为 |
|---|---|
| §0.1 第 3 条（C3 = empirical boundary） | C3 = 生成、筛选、验证（GSV）释放流程与保真阶梯；原 C3 的边界内容并入研究一与 §5.5 |
| §2.1 建议标题 | `STORY_CONTRACT.md` §2 的三个候选，研究二出结果后定（D-E） |
| §2.2 三条贡献 | `STORY_CONTRACT.md` §3（C1 问题与基准；C2 电梯模型风险；C3 GSV 流程） |
| §2.3 研究问题 | `STORY_CONTRACT.md` §4（RQ1 集合与顺序；RQ2 评估器选择与保守性；RQ3 流程价值、短名单、诊断边界） |
| §4.2 引言骨架中的 C1 到 C3 英文 | `STORY_CONTRACT.md` §3 |
| §8、§9 的章节顺序 | §5 = 5.1 设计与登记层级；5.2 研究一；5.3 研究二；5.4 文献校准案例；5.5 有效性边界。§6 = 逐 RQ 三段 + 释放流程操作段 + 局限 + 未来工作。§8、§9 对研究一数字与措辞的要求原样保留，放入 5.2 与 5.5 |
| §3.3 Highlights 的候选主题 | 计划 v2 第二部分 §10 的五条亮点草案 |

### 00.3 数字口径更正（不改审计事实，只补口径）

- §0.2 与 §8.5 的"闭式 evaluator 约高估 makespan 25%–37%"用任一分母都不能从 `b5_des_crossvalidation.json` 复算：按闭式值为分母是 22.8% / 25.1% / 37.3%（配置 1 / 7 / 11），按 DES 值为分母是 29.5% / 33.5% / 59.5%。正文必须写明分母；建议写"DES makespans are 22.8% to 37.3% lower than the closed-form values"。
- §8.2 第 3 条"非负 70/72，说明两个近零有限样本例外"与 §7.2 第 3 点矛盾：角类族不覆盖候选池时 H_up 在精确枚举下也可为负。按 §7.2 写，D1-b 报告为"前提被 §4 证明有误的未达门槛"。
- 事后审计数字（聚类 bootstrap 的 D1-d 52 到 55/72、逐波次抽象偏差中位数 41%、Φ 角类在 FIFO 与聚类派发下的 7.47% / 7.12%、Hedge 选择频率 0.43 到 0.94）只用于决定登记什么，不得进入正文；进入正文的数字必须来自已签字登记后的运行。

### 00.4 两个研究与登记文件

| 研究 | 内容 | 登记文件 |
|---|---|---|
| 研究一 | Phase 5 预注册诊断（锁定判定原样报告）+ 2026-09-26 登记的重分析：S1-1 聚类 bootstrap、S1-2 全池枚举、S1-3 Block C 扩展、S1-6 Hedge 后悔与稳定性展示、S1-7 Supp-1 耦合展示、S1-8 最优波次位置、S1-9 破平修复重跑的报告规则、S1-11 互补分数（可选，D-D）、S1-12 用修正后的 DES-M2 登梯规则重跑 B-5（B-5 旧判定保留，新数并列）、TH-2 抽象偏差展示；S1-4、S1-5 按 AMEND-2026-07-08-B 原登记执行 | `revision_2026-09-26_ijpr/amendments/` |
| 研究二 | 第六阶段方法研究：集合对序列分解、序列杠杆（P10，含只分组的 P10g 对照）、GSV 主实验（P11、筛选、DES 验证；对照含同预算局部搜索 P7-matched 与生成器消融）、筛选后悔、保真阶梯、热启动、文献校准案例、运行时间。DES-M2 采用与闭式 M2 一致的"先登梯"规则（2026-09-26 修正 B-5 的同轮登梯遗漏，见协议 §3.5）。审查后新增：G2 对照 P8-verify(20)（同 DES 预算）、所有短名单按序列签名去重、§7.3 执行稳健性（带噪声 DES 与 B-5 语义）、G5(b) 保留比例；L2 内容移到 `paper_draft/phase6_protocol_L2_addendum.md`。评估文件第二部分 §4 的协议大纲（门槛、对照、单位）与协议不一致之处，一律以协议为准 | `paper_draft/phase6_method_study_protocol.md` |

### 00.5 理论编号的目标方案（TH-8，作者确认后在 §4 重写时生效）

| 内容 | 当前 §4 md | IJPR 目标 | 生效条件 |
|---|---|---|---|
| 诊断恒等式 | Proposition 1 | Proposition 1 | 无 |
| 类别动作 SPO 损失解释 | Proposition 2 | Remark 1 | 无 |
| 嵌套覆盖分区细化（含原 Corollary 1） | Theorem 1、Corollary 1 | Proposition 2 | 无 |
| 全 E 条件性样本路径排序 | Proposition 3 | Theorem 1 | 附录 A 组装完成且作者逐行通读（TH-1）；2026-09-27 已满足，已改名 |
| 条件性 minimax 归约（类别层）与候选层筛选保证 | Theorem 2 | Corollary 1（a）类别层、（b）候选层 | 无 |
| 超额损失与中点分位数界 | Corollary 2 | Corollary 2（主文只留一句边界） | 无 |
| 模型校准的均值 DRO 比较 | Corollary 3 | Remark 2（一句，指向 Fu, Li and Zhang 2024） | 无 |
| 有限评估器族扩展 | Corollary 4 | 删除 | 无 |

在 TH-1 完成前，排序结果继续称 Proposition 3，正文不得称其为定理。

**决定（2026-09-26，作者授权助手决定："帮我进行这四点的抉择，然后完成这四点"）：采用上表，按以下细则执行。**
1. 推论 1 含两部分：(a) 类别层（原 Theorem 2，式 (49)）；(b) 候选层（原 §4.5.2 的 "Candidate-level reduction"，式 (50)）。两部分都放在 §4.4.1；§4.5.2 只引用推论 1(b)，是 GSV 筛选步骤的保证（TH-3）。
2. 推论 2 保留其陈述与证明（超额损失与排序余量，原式 (50) 至 (52)）。原式 (53) 至 (55) 的中点分位数界（即 U_c 证书）从 §4 删去，只在 §5.5 以一句边界陈述出现，完整推导放附录（TH-5；STORY_CONTRACT §3 "The U_c certificate appears once, as a boundary statement in §5.5"）。
3. 注 2 是 §4.4.2 末的一句话：在式 (47) 的排序下，以 M1 类别分布为中心、半径取到 M2 类别分布的 Wasserstein 球上的最坏类别均值等于 M2 类别均值，并指向 Fu, Li and Zhang (2024)（MSOM 26(5): 1962–1977，DOI 10.1287/msom.2023.0159，已由 Crossref 核对）。原式 (56)、(57) 与 Mohajerin Esfahani and Kuhn (2018) 的引用随之离开 §4（TH-4）。
4. 推论 4（原式 (58)）删除。
5. 图 5 不进入 IJPR 稿：它的三块内容中，DRO 与模型族扩展已降级或删除。图 4 以现有 v1 插入，与已在 Word 中的图 2、图 3 同一版本；三张图在图件统一重绘时按 W-10（Times New Roman、15 cm、矢量 PDF 与 600 dpi PNG）一起处理。
6. 新编号下 §4 的公式为：(47) 类别层随机排序；(48) 记号；(49) 推论 1(a)；(50) 推论 1(b)；(51) 至 (53) 推论 2；(54) 至 (57) §4.5 的 GSV 式；§4.6 没有公式。
7. 命题 3 仍称 Proposition 3，直到 `revision_2026-09-26_ijpr/MATH_VERIFICATION_LOG.md` 第 4 至 12 行由作者本人签完；这一步不能代签。2026-09-27：作者报告已逐行读完附录 A、全部通过，并指示助手录入第 4 至 12 行；自此改称 Theorem 1（Word 版 §4 以修订模式修改）。

### 00.6 IJPR 施工阶段（接在 §12 之后执行；详细清单见计划 v2 第二部分）

- [x] 第 1 周：签署 D-A 到 D-M；故事契约；本覆盖层；术语表与 CLAUDE.md；研究一登记文件；第六阶段协议（设计与门槛）；OSF 登记包。（2026-09-26 已签字；OSF 登记 kps2c，禁运；见 EXECUTION-LOG 第 50 至 52 条）
- [x] 第 2 周：研究一重分析脚本与研究二代码（P10、P11、DES 模块、热启动、GSV 驱动、案例生成器骨架）及测试。（2026-09-26 完成；完备性审计见 EXECUTION-LOG 第 59 条）
- [x] 第 2 到 3 周：签字后运行研究一重分析。（2026-09-26 运行并补齐，EXECUTION-LOG 第 53 至 58 条；结果见 `revision_2026-09-26_ijpr/study1_run_2026-09-26/STUDY1_RESULTS_SUMMARY.md`）
- [x] 第 3 到 4 周：附录 A 组装与作者通读（TH-1）；补完 Word 版 §4 并新增 4.5 GSV。（2026-09-26：附录 A 已组装并经独立审查；Word 版 §4 已按上面 §00.5 的决定以修订模式补完 4.3.2 至 4.6。2026-09-27：作者报告已逐行读完附录 A，核验记录第 4 至 12 行已按其指示录入，命题 3 改称定理 1；附录 A 的 Word 版为 `revision_2026-09-26_ijpr/week3/Appendix_A_2026-09-27.docx`。仍待作者在 Word 中接受修订；EXECUTION-LOG 第 62 条）
- [ ] 第 4 周：P11 按预先写定的训练池规则调参，结果写进单独签字的 L2 附录（`paper_draft/phase6_protocol_L2_addendum.md`；协议本身签字后不改）；然后才生成测试池种子。（2026-09-27：G0 第 1 至 7 项通过；训练池调参完成，选 (α, β, γ) = (1, 1, 0.5)，主研究预计 2.6 小时、不启用子集模式；案例数据下载并通过 §11.2 检查；案例四个时间参数的范围与来源已查证；L2 已于 2026-09-27 按作者指示签字并由 `MANIFEST_SIGNED_L2` 钉住（提交 b1eaff7）；只差作者提交 kps2c 的 OSF 更新（`archive_package/osf_update_2026-09-27_L2/`），之后才生成测试池；EXECUTION-LOG 第 62 至 64 条）
- [ ] 第 5 到 7 周：运行研究二；分析；图表。
- [ ] 第 8 到 10 周：冻结数据哈希；写 §5、§6 与附录。
- [ ] 第 11 到 12 周：写 §2（定位表）、§1、摘要、亮点；定题。
- [ ] 第 13 到 16 周：一致性检查、模拟审稿、组稿、投稿包与缓冲。

## 0. 本文件如何使用

本文件是本轮论文修改的唯一主动施工入口。它把散落在根目录 DOCX、`paper_draft/manuscript`、`revision_2026-07-08`、两份贡献审查、实验输出以及已归档的 `archive/revisions/revision_0719_snapshot` 中的有效修改折叠到一套逐章规则中。后续修改应先更新本文件中的裁定，再落到正文；旧文件继续保留作溯源，不删除、不回写、不再直接拼接。

本文件不是投稿正文，而是“章节蓝图 + 冲突裁决 + 完成门槛”。最终正文仍应以完整段落写作。这里允许使用表格和清单，因为它承担施工控制功能。

正文语言约定（2026-09-11）：论文全文统一采用陈述句，英文与对应中文保持一致。符号定义、方法步骤、命题条件和证明以明确主语陈述，不使用 “Let / Fix / Suppose / Define / Draw” 等祈使结构；条件通过条件句表达，其量词、适用范围与数学含义保持不变。Section 4 已完成本轮全文语言统一，后续章节沿用这一约定。

### 0.1 本轮采用的关键假设

在没有新增容量反事实实验之前，采用风险最低的路线：

1. **C1 锁定为固定运营评估器下的单波候选选择/benchmark**，不再称完整 rolling-horizon two-stage scheduler。
2. **C2 以条件性 sample-path dominance 及两类失败机制为理论主轴**；恒等分解、SPO bridge、minimax collapse、Theorem R 和 DRO relation 按真实强度计费。
3. **C3 改为 empirical boundary and measurement sensitivity**，不再称 capacity-versus-policy diagnosis，也不再给出“buy capacity”建议。
4. 若以后坚持恢复原 C3，必须另开实验修正案，做同订单、同 wave、同随机数下改变 `E/c/fleet` 的 matched counterfactual，并与重新优化 wave policy 的收益进行同尺度比较。在该实验完成前，正文不得预支容量结论。

### 0.2 不可被本文件改写的审计事实

- H-D1 = **PARTIAL**：signal-resolution 57/72，预注册门槛 58/72。
- H-D2 = **PASS under its four preregistered Block-C gates**：matched-wave dominance 平均 99.2%，worst cell 96%，24/24 cell FOSD，6/6 minimax/DRO selection match。
- Prop. 2 的联合充分条件在不足 1% waves 上成立；99.2% 是闭式模拟器中的经验规律，不是 Prop. 2 的命中率或定理验证。
- 预注册 `Phi`-rule 口径约 72%，covering 口径约 47%；二者都是 partition/instrument-relative 读数，均不是容量效应。
- test–retest 连续份额信度失败：`Phi` share ICC 约 0.01，covering share ICC 约 −0.03；15/18 只支持二元 verdict 的一致性。
- DES 交叉验证未达到排序保真门槛：Spearman `rho` 约 0.45–0.68；闭式 evaluator 约高估 makespan 25%–37%。dominance 符号大体保留，但逐 wave 排序不能外推。
- operational clustered dispatch 平均改善约 10.2%，大于 mean tactical GAP 约 6.0%。
- 生产模拟器的 `id(e)` tie-break 缺陷已于 2026-09-11 修复（索引稳定破平 `simulator._earliest_unit`）。B-14 生产侧再生 [QA]：Block C 与 smoke 的全部预注册门槛判定不变；M1 逐行相同，M2 0.55%、M3 0.67% 的 Block C 行值随平局顺序改变；Block A/B 未在修复后重跑，其存量数值仍带 B-14 前的平局暴露。记录见 `qa_2026-09-11/QA_2026-09-11_tiebreak_fix_candidate_id.md`。
- Block A 的角点臂为有限候选池中的有放回抽样，200 行并非 200 个独立 wave；现有行级区间存在伪重复风险。2026-09-11 起 Block A/B/C 存量行已通过种子回放补齐 `candidate_id`（`results/raw/*_candidate_ids.csv`，逐行对齐经再仿真验证），聚类/去重重分析尚未执行。

### 0.3 证据等级标签

全文每张表和每个结果段应标记证据来源，避免把主预注册、后续修正和 QA 混为一层：

| 标签 | 含义 | 能否改变原主判定 |
|---|---|---|
| `[PR-C]` | 2026-05-19 主预注册确认性：Block A/H-D1、Block C/H-D2、Block B/H-Policy | 按冻结门槛给原判定 |
| `[PR-E]` | 主预注册探索性 H-D3 | 不能包装成确认性 |
| `[AM1]` | 5 月 19 日主分析前追加的 P7 与 A1–A4 | 不改变主 gate |
| `[AM2]` | 主分析后、补充实验运行前注册的 Supp-1/2 | 前瞻性补充，不是原主检验 |
| `[RA]` | 7 月 8 日 Amendment A 对既有数据的重分析 | 只作敏感性/呈现，不回溯重判 |
| `[NS]` | B/B11/B13/C/F 等运行前注册的新仿真/检验 | 可有自身 gate，但不是主预注册 |
| `[EXP]` | 无 gate 的描述性或探索性结果 | 只支持假设生成/边界描述 |
| `[QA]` | bug 修复、等价重跑、代码审计 | 不能包装成新的确认性证据 |

原始 gate 必须保留原判定；后续 dependence-robust 或 tie-break QA 若产生不同数字，应与原判定并列，不可无痕替换。

---

## 1. 版本折叠与来源优先级

### 1.1 当前有效来源

| 用途 | 首选来源 | 使用方式 |
|---|---|---|
| 最新贡献裁定 | `research_notes/contribution_review_continuation_2026-09-02.md` | 本轮声明、范围和证据强度的最高优先级 |
| 前沿定位 | `sources/frontier_novelty_audit_2026-09-02.md` | §1–§2 的 2025–2026 文献入口；提交前继续系统检索 |
| 当前 Abstract/§1 文本底稿 | `paper_draft/manuscript/abstract_v1.1_250w.md`；`introduction_v1.1.md` | 只作句子底稿；其中 capacity、first-ever 和“largely fixes”叙事仍须按本文件重写 |
| §2 底稿 | `paper_draft/manuscript/related_works_v1.1.md` | 保留已核验的分类与引用，加入 2026 前沿和 prescriptiveness/VSS/EVPI 比较 |
| §3 当前正文 | `F:/Paper 3/Problem formulation.docx`（2026-09-25 定稿；中英对照见 `revision_2026-09-24/section3_bilingual_2026-09-24.md`）。2026-09-26 更正：`SECTION_3_MODEL_FORMULATION.md` 已被该 docx 取代，只作历史（已折叠至 `archive/revision_2026-09-02/`） | 定稿；IJPR 版只需补计划 v2 的 W-1 两句与一句候选池扩充说明（见 STORY_CONTRACT.md §9） |
| §3 历史结构源 | `revision_2026-07-08/tier1_manuscript/W4_section3_formulation.md` | 仅用于追溯实现描述和候选池协议；其中旧时间、FIFO、多波与统计量表述不再取用 |
| §4 当前正文 | `revision_2026-09-02/SECTION_4_METHODOLOGY.md` | 2026-09-11 中英逐段重构稿；新旧理论编号见本文件 §7.5；正文完成不代表附录、代码和重算完成 |
| §4 理论证据 | W1、W2、W3、W8、W9、W10；尤其 W9 Lemma 6 与 W8 Theorem R | 不能机械拼接；按本文件的理论层级重新写一份自洽正文 |
| §5 数值事实 | `prototype/results`、`revision_2026-07-08/tier2_analysis/outputs`、`EXECUTION-LOG.md` | JSON/CSV 优先于旧表格和旧叙事；先修复统计单位和 tie-break 再冻结最终数字 |
| §6 结构参考 | `revision_2026-07-08/tier1_manuscript/W5_section6_discussion.md` | 仅借用 discussion 结构；capacity/buy-capacity 与 pending 状态全部作废 |
| 附录证明 | W2、W3-E2、W8、W9、两个反例模块 | 按主文最终编号组装并人工通读，不直接沿用旧 proof skeleton 的单通道表述 |
| 当前 Word | 根目录 `Wave Release Coordination under Vertical Resource Constraints in Multi.docx` | 仅用于取回仍正确的 §2/§3参数细节和格式；不是最新事实源 |

### 1.2 部分保留、折叠后不再单独施工

- 原 `revision_0719` 已于 2026-09-03 整体移至 `archive/revisions/revision_0719_snapshot`，仅作可恢复的历史章节快照；后续施工不得从该目录取稿。
- 重复性审计显示该快照共 67 个文件，其中 40 个是与 `paper_draft/manuscript` 或 `revision_2026-07-08` 逐字节相同的 SHA-256 副本；其余 27 个均为 README、`edits_from_global`、`original_docx_*` 或 PDF/包装溯源件，没有独有科学结果。
- 快照中的同名 W 文件以 `revision_2026-07-08/tier1_manuscript` 为权威副本；`archive/revisions/revision_0719_snapshot/*/edits_from_global.md` 仅保留审计轨迹，其有效修改已进入本文件，不再逐条执行，以免把旧 capacity 叙事一并带回。
- `archive/paper_draft/manuscript/00_INDEX.md` 只保留为 7–9 月进度记录。它关于“§2 已全部应用”“Prop. 2 已升级”“W5 即全文”的状态已经过期。
- `paper_draft/TERMINOLOGY.md` 的名称规则仍可参考，但第 4、7 节将 `H_up` 定义为 capacity-side、将 C3 固定为 capacity diagnosis 的内容已被本文件覆盖。
- T1–T6 与 fig1–fig10 的活跃素材入口分别统一为 `revision_2026-07-08/tables` 和 `revision_2026-07-08/figures`；归档快照中的副本不再使用。标题、算法名称、统计单位和 capacity 解读必须先更新。

### 1.3 完全过时，只存不取

- 2026-09-26 目录清理：本节与 §1.2 所列过时文件已全部移入根目录 `archive/`，下列路径已同步更新；新旧路径与 SHA-256 见 `archive/MANIFEST.md` 和 `archive/CLEANUP_2026-09-26_moves.json`。

- `archive/paper_draft/manuscript/*_v1.0.md`：双语或旧稿，只保留 provenance。
- `archive/paper_draft/manuscript/proposition2_chain_dominance_v1.0.md`、`chain_dominance_proof_v1.0.md`、`chain_dominance_empirical_v1.0.md`：旧三条件/单失败通道骨架，退出活跃写作链。
- `archive/paper_draft/`（原 `paper_draft/archive/`）：prototype 尺度、M4/M5 旧命名或已经执行完毕的计划。
- 根目录 `archive/superseded/`：旧 Section 4、旧示意图。
- `archive/gpt_2026-08/Abstract_Introduction_RelatedWorks_*`：语言编辑产物，没有吸收本轮理论、测量和 C3 裁定。
- `archive/research_notes/00_north_star.md`、`02_open_questions.md`、`03_decisions.md`、`novelty_analysis_and_contribution.md`、`paper_sections_documentation.md`：早期 MILP/SimPy/ALNS 或 prototype 路线，仅作研究历史。
- `archive/paper_draft/storyline_motivation_to_contribution_v1.md`：以 capacity dominance 和 `U_c` 保底为主线，已被本文件取代。
- `section4_draft_v0_1.md` 与 `section5_draft_v0_1.md` 中的旧结论段：可借结构，不可逐字取用。
- W5 中的 capacity-bound、buy capacity、B-2/B-3/B-5 pending/future 段落：全部作废。

### 1.4 发生冲突时如何裁决

1. **冻结规则：** 主预注册 > 签署修正案 > 后续正文或 README。
2. **数字与执行状态：** 原始 JSON/CSV > 对应分析脚本 > `EXECUTION-LOG.md` > 表图 > README/叙述稿。
3. **数学内容：** W8/W9/W2 > W10 的组装说明 > W1/W3/旧 §4/旧 Prop. 2。
4. **声明范围与创新计费：** 2026-09-02 续审 > 2026-08-06 审查 > 七月 W10 叙事 > 当前正文旧句。
5. **当前文字底稿：** 9 月 Abstract/Introduction > 8 月 Related Works > 8 月 DOCX > v1.0 文件；但较新文字也必须服从更高层的证据与声明裁定。
6. **术语表：** `TERMINOLOGY.md` 只裁决名称和写作风格，不能覆盖后续审查对科学含义的修正。
7. **修改时间：** mtime 只在同一血统、同一角色的文件间作次级判据；复制时间较新不代表科学内容更新。

若综述文件与原始结果冲突，不得挑选更符合叙事的版本，必须回到 raw output，登记冲突后重新生成表文。

---

## 2. 全文统一主线

### 2.1 建议标题

> **2026-09-26：§2.1 至 §2.3 已被 §00.2 取代（IJPR v2）。以下原文保留作溯源。**

首选标题：

> **Diagnosing and Hedging Wave-Composition Decisions under Elevator-Model Uncertainty in Multi-Story AMR Warehouses**

该标题主动避免把研究写成完整多波 scheduler，也不预支 capacity-investment 结论。若保留现题，正文必须在 §1 第一处明确“coordination”仅指给定候选池和固定运营规则下的 single-wave composition decision。

### 2.2 三条贡献的最终版本

**C1 — Scoped problem and benchmark.** 形式化一个固定 operational evaluator 下、共享楼宇货梯约束的 single-wave candidate-selection problem，并给出可复现的合成 benchmark。贡献不包括跨波覆盖、rolling horizon、实时 AMR dispatch 或容量投资优化。

**C2 — Dominance mechanism and robust class selection.** 对 throughput abstraction 与 true co-occupancy batching 的 sample-path ordering 给出全 `E` 的条件性充分条件和两类失败机制，并在该 ordering 成立时推出 minimax wave-class selection。Bound-and-Gap、SPO bridge、nested refinement 和 corner-calibrated DRO 是诊断或解释属性，不单独冒充主要创新定理。

**C3 — Empirical boundary and measurement sensitivity.** 在预注册合成网格中量化 ordering 的经验强度、Hedge 的实际代价、coarse class rule 与启发式/搜索基线的差距，以及 partition、seed、重复抽样和 DES fidelity 对结论的影响。贡献结论是“何时可相信该诊断”，不是“何时购买容量”。

### 2.3 研究问题

- **RQ1:** 在固定 operational evaluator 和给定候选池下，wave composition 的可观测结构对 makespan 有多大关联，其 partition-relative headroom 与 class-selection miss 如何分解？
- **RQ2:** 在什么可验证条件下，throughput abstraction 与 true co-occupancy batching 形成 per-wave ordering；当 ordering 成立或近似成立时，如何进行保守的 wave-class selection？
- **RQ3:** 上述诊断和选择对 partition、metric、seed、policy class、抽样单位以及并发 DES evaluator 有多敏感？

### 2.4 全文禁用或限制的表述

| 原表述 | 新规则 |
|---|---|
| `elevator capacity is the primary bottleneck` | 仅可写为研究设定/假设，或“elevator contention is the focal vertical constraint”；不得写为已由本文普遍证实的事实 |
| `wave composition largely fixes makespan before any AMR moves` | 改为“wave composition shapes the downstream request mix under a fixed operational rule”；必须同时承认 dispatch 10.2% 结果 |
| `never been treated` / `studied only in isolation` | 改为 scoped gap，并逐项对比 2025–2026 邻近研究 |
| `two-stage scheduler` | 若不建立跨波变量与 rolling dynamics，改为“single-wave selection problem evaluated under a fixed operational rule” |
| `H_up = capacity-side/structural ceiling` | 改为“partition-relative upper-tail headroom”；公式中没有容量反事实 |
| `no policy can recover H_up` | 最多写“not represented by the specified partition-constant corner rule”；P9 已反证更广义说法 |
| `72% means capacity dominates policy` | 删除；72% 与 covering 47% 只作为两种 measurement readings 并列报告 |
| `identities validated in 72/72` | 改为“identity/pipeline checks held in 72/72”；不作为外部科学验证 |
| `Prop. 2 explains 99.2%` | 删除；分开报告充分条件覆盖率与经验 ordering 频率 |
| `DRO matched 6/6 validates robustness` | 改为“the corner-calibrated analytical equivalence was reproduced in 6/6 configurations” |
| `U_c is a worst-case rule-loss bound` | 改为“M2-side corner-median perturbation bound”；M1 regret 另报 C-4 |
| `P6 = SPO-Tree` | 改为普通 squared-error decision-tree comparator，除非重新实现真正 decision-focused tree |
| `P7 = optimum` | 改为 40-iteration local-search reference；精确最优只对枚举池使用 `pool optimum` |
| `event-driven simulator` | 主 evaluator 固定称“closed-form sequential time-accumulator”；DES 只指 B-5 交叉验证器 |

---

## 3. Front matter 如何进行

### 3.1 Title

先在单波 scope 固定后定题。标题不得同时使用“coordination/scheduler”和“capacity-versus-policy”，除非对应模型与实验都真正实现。完成标准是标题中的每个动作词都能在 §3 找到决策变量，在 §4 找到方法，在 §5 找到直接证据。

### 3.2 Abstract

**起点：** `paper_draft/manuscript/abstract_v1.1_250w.md` 的正文只作语言底稿。它虽已将 dominance 改为条件句、将 ceiling 缩小到 group-level，但仍包含 `primary bottleneck`、`largely fixes`、`never been treated`、capacity-versus-policy verdict 和 capacity lever，因此必须再重写。

**建议的六句逻辑：**

1. 场景与精确限制：多层 AMR 仓库中的 shared-elevator contention，且本文研究固定 operational rule 下的 single-wave composition。
2. 文献缺口：相邻研究分别覆盖 multi-story routing、fixed-request lift scheduling 或 planar joint scheduling，但未直接研究本文这个特定交叉点。
3. C1：定义 benchmark、候选池、三类 elevator evaluators 和 primary median metric。
4. C2：先写条件性 ordering 机制，再写 ordering 成立时的 conservative class selection；Bound-and-Gap 只称 diagnostic decomposition。
5. C3 结果：H-D1 PARTIAL 57/72；经验 dominance 99.2% 且 H-D2 四门 PASS；同时说明 DES 排序保真不足或 measurement sensitivity，至少保留一个关键边界结果。
6. 结论：这些工具用于评估 coarse wave classes 和 model risk，不给出容量投资因果建议。

**可保留数字：** 106,800 model evaluations（必须在 §5.1 定义 count）、57/72 PARTIAL、99.2% matched-wave ordering、96% worst cell、6/6 analytical selection match。若 250 词无法容纳限制，优先删 72/72 identity 和 6/6，而不是删模型范围或 DES/measurement 边界。

**不得出现：** 72% capacity share、buy capacity、first-ever、所有政策不可恢复、Prop. 2 无条件保证、`U_c` downside guarantee。

**完成门槛：** 250 词以内、无引用、无 em dash；与最终 §3 的 scope、§4 的条件、§5 的统计单位和 §6 的结论逐字对齐；全文完成后最后写并重新批准。

### 3.3 Highlights 与 Keywords

Highlights 在正文冻结后重写为 3–5 条、每条不超过 C&IE 要求的 85 个字符。不得使用 capacity dominance。候选主题依次为 single-wave benchmark、全 `E` 条件 ordering、两失败机制、预注册 empirical strength、DES/measurement boundary。Keywords 建议使用 multi-story warehouse、autonomous mobile robots、wave composition、shared elevators、model uncertainty、distributionally robust optimization；若 DRO 降得更低，可用 simulation-based optimization 替换。

---

## 4. Section 1 Introduction 如何进行

**起点：** 采用 `paper_draft/manuscript/introduction_v1.1.md` 的段落节奏，不直接保留其 C3 标题与容量结论。

### 4.1 段落顺序

1. **运营背景。** 描述土地受限和多层仓库，但将 elevator bottleneck 写为 focal setting，而非无来源的普遍转移规律。
2. **上游决策。** 说明 wave composition 改变 OD、方向和到达结构；同时明确运营层固定，本文不求联合最优。
3. **邻近研究。** 引入 MAPF-E、WareRover、multi-story parcel grouping、tier-to-tier shuttle/lift 和 planar joint RMFS；用“缺少同一特定组合”建立狭义缺口。
4. **问题范围。** 定义 single-wave candidate selection、候选池、fixed operational evaluator；说明不研究跨波覆盖、订单延期和容量投资。
5. **三个 RQ。** 按本文件 §2.3 顺序提出，使 §5 一一回答。
6. **方法概览。** 先介绍 partition-relative diagnostic，再介绍 conditional dominance 与 conservative class selection；避免先给管理答案再找方法。
7. **三条贡献。** 使用本文件 §2.2 的版本。每条只包含一个主动作和一个证据对象。
8. **结果与边界预告。** 并列 H-D1 PARTIAL、H-D2 scoped PASS、measurement/DES boundary；不要把失败项藏到 Discussion。
9. **文章结构。** 只承诺实际存在的 §2–§6 和 Appendix。

### 4.2 C1–C3 在引言中的建议英文骨架

> **C1 — Problem and benchmark.** We formulate a single-wave candidate-selection problem for a multi-story AMR warehouse in which a fixed operational rule routes released orders through shared freight elevators, and we provide a reproducible synthetic benchmark spanning three elevator evaluators.

> **C2 — Conditional model ordering and robust class selection.** We characterize sufficient conditions and two failure channels for a sample-path ordering between the throughput abstraction and true co-occupancy batching. Wherever the ordering holds, conservative minimax selection reduces to the class preferred by the dominant evaluator; the accompanying decomposition and refinement results diagnose what the chosen partition represents.

> **C3 — Empirical strength and validity boundaries.** A preregistered computational study measures how often the ordering holds, the price of the resulting hedge, and how the diagnostics change with partition, policy class, repeated sampling, and an event-driven cross-validation model.

这三段是内容骨架，不是已经批准的最终英文；应在 §3–§6 完成后统一语言。

### 4.3 完成门槛

- 每个 novelty 句都有 §2 的最近邻证据；
- 每个贡献句都有对应 RQ、方法、结果和限制；
- 删除 `only in isolation`、`capacity side dominates` 和任何“完整两阶段 scheduler”暗示；
- operational dispatch 10.2% 结果与“固定运营层”的选择不矛盾；
- 不在引言中用 identity 通过率冒充 empirical validation。

---

## 5. Section 2 Related Works 如何进行

**起点：** `paper_draft/manuscript/related_works_v1.1.md`。保留已经核验的文献分组，但按“决策层 + 物理系统 + 方法基线”重新组织，避免列举式综述。

### 5.1 建议小节

1. **2.1 Wave, order batching, and integrated RMFS decisions.** 从传统 batching 到 2026 joint order allocation/rack/robot scheduling；说明这些工作多为 planar、parts-to-picker 或给定 wave。
2. **2.2 Multi-story robot and lift/elevator coordination.** 纳入 2025 graph-based multi-story parcel grouping/elevator selection、2025 tier-to-tier lift scheduling、2026 MAPF-E；精确说明它们与共享楼宇货梯、上游单波 composition 的差异。
3. **2.3 Coupling high- and low-level warehouse decisions.** 纳入 WareRover 等联合 OS–MAPF 工作，主动承认“上下层耦合”本身不是本文首创；本文差异是 evaluator、垂直资源和决策对象的特定组合。
4. **2.4 Prescriptive value and partition diagnostics.** 比较 coefficient of prescriptiveness、adjusted/expected coefficients、VSS、EVPI、SPO loss、partition refinement。说明 `M_Phi` bridge 是解释连接，不是新的学习算法。
5. **2.5 Robust optimization under model uncertainty.** 比较一般 Wasserstein DRO、stochastic-dominance DRO 闭式解与 model-class uncertainty；将 corner-calibrated relation定位为 warehouse-specific certification。
6. **2.6 Positioning matrix.** 用一张表比较 decision variable、multi-story、shared lift/elevator、flexible AMR、fixed vs endogenous request set、method、validation data。表格最后一行才给本文 scoped delta。

### 5.2 必加前沿来源

完整检索入口见 `sources/frontier_novelty_audit_2026-09-02.md`。至少核验并讨论：

- He et al. (2026), MAPF with Elevators；
- Xu et al. (2026), WareRover；
- Kim et al. (2025), multi-story path planning with parcel grouping/elevator selection；
- Ren et al. (2025), integrated tier-to-tier shuttle/lift scheduling；
- Wang et al. (2025), heterogeneous lifts；
- Xue and Wang (2026), joint order allocation/rack/robot scheduling；
- Bertsimas and Kallus (2020), coefficient of prescriptiveness；
- Jiang, Tian, and Wang (2026), updated prescriptiveness coefficients；
- Song and Luedtke (2015), partition refinement；
- Kuhn, Shafiee, and Wiesemann (2025), DRO survey；
- Fu, Li, and Zhang (2024), closed-form DRO under stochastic dominance。

### 5.3 完成门槛

- 禁止用“没有任何研究”证明 novelty；
- 每个最近邻必须写出“相同点—不同决策层—剩余缺口”；
- 加入 prescriptiveness、VSS/EVPI，不只比较 SPO；
- 引文全部来自原始论文/出版社并进入统一 BibTeX；
- `existing methods can recover it` 降为 `can target the decision loss`，除非本文直接证明可回收性。

---

## 6. Section 3 Problem Formulation 如何进行

**当前正文（2026-09-26 更正）：** `Problem formulation.docx`（2026-09-25 定稿；中英对照见 `revision_2026-09-24/section3_bilingual_2026-09-24.md`）。原 2026-09-10 版正文草稿 `SECTION_3_MODEL_FORMULATION.md` 已折叠至 `archive/revision_2026-09-02/`，只作历史；下述五节结构与 32 个编号公式同样适用于定稿。当前五节为：3.1 Problem setting and assumptions；3.2 Notation and decision variables；3.3 Candidate waves and structural classes；3.4 Objective functions；3.5 Constraints and their explanation。目标函数集中在 3.4；3.5.1 集中表达约束，3.5.2 集中解释约束。采用“英文段落 + 紧随中文译文”，三张表保留双语定义，32 个编号公式各保留单份。延续用户确认的 EJOR 叙事方向、漏斗式、一段一职和避免防御性写作要求。本次仅同步主控目录记录，未改动 Section 3 正文。

该稿保留以下目标语义：`W` 为固定规模订单集合，`pi(W)=sort(r_o, order_id)` 为跨模型统一的规范顺序，主 evaluator 为 serial resource-reservation map，类级主 estimand 为 median makespan。新增的文字澄清包括预约状态与实时状态的区别、角点类别族非空条件、中位数并列约定以及订单归属变量的联动性质。该稿仍是 Phase 1 代码修复和后续重算的模型合同，不表示生产源码已对齐；本次未修改 `Problem formulation.docx`、生产代码或实验结果。

**以下 6.1–6.6 保留为内容核查要点，不再作为正文目录。** 其中实验样本规模、具体参数取值和统计单位安排到 §5；模型实体与公式以五节正文为准。旧稿中的 `f0=1`、每层运行 5 秒、装卸各 2 秒、取货/交付各 5 秒、`sigma=0.20` 和 `alpha=0.25` 已从模型正文移出，作为 §5.1 的参数迁移记录保留，后续按配置和冻结协议核对，不能据此重新设定实验。重构前快照位于 `archive/codex_review/2026-09-07/SECTION_3_before_restructure.md`，仅用于恢复和审计，不是新的 revision 入口。

**历史起点：** W4 的物理流程和记号表 + 根 DOCX 中仍正确的参数定义。现有 W4 仍把 `H_up` 叫 capacity-side、把 P6/P7 命名过强，并且没有解决单波/多波与统计量冲突，因此不能整段复制。

### 6.1 3.1 Scope and decision problem

明确给定 warehouse configuration、订单候选池 `O`、固定波规模 `n`、固定 operational rule 和 evaluator `M`。主决策为选择 `W subset O` 且 `|W|=n`，或从预生成候选集 `C_n` 选择一个 wave。不要同时保留自由的 `W_min/W_max` 和单波 makespan 最小化，否则会机械偏向最小波。

若采用候选集表述，应明确本文研究的是：

> `min_{W in C_n} s(C_max(W; M))`

其中 `s` 的主口径必须与实验一致。建议把 primary estimand 固定为 median makespan；均值只用于 DRO 推导时单独标记。不要在式 (1) 写 expectation、§4–§5 却使用 median。

删除跨所有 `W_omega` 的覆盖约束、下一波等待、全订单调度等内容，除非正式引入 `x_{o,omega}`、波序、释放时间、截止期和跨波状态。

### 6.2 3.2 Physical system and assumptions

给出 AMR、楼层、订单 OD、共享电梯、服务阶段和固定 dispatch rule。必须明确：

- “floor-confined”究竟指 AMR 固定楼层、还是可以随货梯跨层；若有交接，定义交接；若 AMR 可乘梯，停止称其 floor-confined。
- 所有 AMR/elevator 从 floor 1 冷启动是单波实验假设 A6，不是一般仓库状态。
- 波间无 carry-over、backlog 和 overlap；这就是外推边界。
- 主 evaluator 顺序处理订单，不是 arrival-event FCFS；未来订单不能被描述成真实事件队列。
- availability tie 必须由显式 unit index 打破，且代码先修复后正文才能写“reproducible”。

### 6.3 3.3 Wave representation and partition

保留 `C`、`I`、`T` 的概念，但诚实处理三个构念问题：

- `C` 是 floor-endpoint entropy，不是物理 vertical distance；`{1,2}` 与 `{1,10}` 可有同样 entropy。应称 endpoint dispersion descriptor，并在限制中说明距离信息丢失。
- `I` 只对 cross-floor traffic 定义；无 cross-floor orders 时的零值规则必须一致。
- `T = sigma_r/mu_r` 的实现是 release-time CV；small CV 对应更紧密，而不是 high T 对应 tight burst。若主设计 `r_o=0`，则 `T` 在主分析中休眠。

建议把主预注册分区明写为 `(C,I)` 2×2，`T` 只在 staggered/nested sensitivity 中进入。这样既不伪称三维 `Phi` 全部驱动主结果，也能保留 `Phi=(C,I,T)` 作为扩展描述符。

数据生成的名称也必须与代码一致：`clustered` 是把约 80% 概率放在约 20% 的可行 `(source,destination)` 对上，不是“20% floors”；现名 `diurnal` 实际是 50 秒单波窗口内、约 70% 到达集中在约 30% 峰窗的 synthetic peaked/staggered arrivals，不应暗示真实日周期。

### 6.4 3.4 Elevator evaluators

- M1：`E*c` independent single-rider slots，是 throughput abstraction，不是物理安装了 `E*c` 台电梯。
- M2：`E` cars with same-OD co-occupancy batching。
- M3：M2 加 phase-level lognormal noise；不能进入 M1–M2 exact chain dominance。

逐步说明 reposition、load、travel、unload、AMR service clocks 和 makespan。给每个物理常数公开规格、文献范围或 sensitivity grounding，只能写“within publicly documented ranges”，不能写“calibrated to a facility”。

### 6.5 3.5 Candidate pool and policy classes

说明 600-order pool、3,000 candidate waves、训练样本、角点抽样和评估臂。保存并公开 `candidate_id`。准确命名：

- P5 = OLS-sign corner rule；
- P6 = squared-error decision-tree comparator；
- P7 = 40-iteration local-search reference；
- P8 = published/savings-style heuristic；
- P9 = wave-level SPO+ policy；
- pool optimum 只指枚举候选池中的最优 wave。

必须交代从“选 corner”到“选具体 wave”的 within-class rule，否则 Hedge 只解决 class selection，不解决 wave construction。

### 6.6 3.6 Statistical unit and validity boundary

提前声明订单池、候选 wave、抽样 wave、seed、configuration 和 model evaluation 的层级。重复抽到同一 `candidate_id` 不得作为独立 wave。说明闭式 evaluator 是主模型类，DES 是 cross-validation，不是已证明等价的真实系统。

### 6.7 本章完成门槛

- 单波或多波只保留一种问题；
- 主统计量统一；
- 时间顺序与 `T` 实现一致；
- M1/M2/M3 与代码逐行核对；
- tie-break 修复落到 production source；
- 候选类到具体 wave 的选择可执行；
- 图 1 仅显示实际模型，不暗示未实现的 rolling coordination。

---

## 7. Section 4 Methodology 如何进行

**当前正文草稿（2026-09-11，方法优先布局）：** [SECTION_4_METHODOLOGY.md](<F:/Paper 3/revision_2026-09-02/SECTION_4_METHODOLOGY.md>)。采用逐段中英文对照，公式从（33）续至（58）。本次按用户反馈重写方法总述，将核心选择与实施流程提前；现有理论结果和展示公式的数学内容均保留。生产代码对齐、数值重算和最终附录组装仍是独立任务，不能据此标为完成。

正文顺序调整为“鲁棒类别选择流程 → 类别绩效诊断 → 对应请求的条件性排序 → 鲁棒选择的性质”。总述第一段交代输入、双评估器评价、最大类别中位数最小化和固定类内释放；第二段交代诊断与排序分析的支持作用。流程先说明一般 minimax 如何执行，再在后文分析何时可简化。

第 4.2 节的诊断以既定规则的所选类别为输入，UB/LB/GAP/H_up/M_Phi 不进入核心选择目标。q_Phi、精确鲁棒决策 q*、基于估计的决策 q_hat，以及性质分析中的 q_H 各自明确，不能串成未经证明的“诊断结果产生 Hedge”流程。仅在真正覆盖分区的段落使用 partition-relative。

### 7.1 4.1 Robust class-selection procedure

4.1.1 给出候选评价与类别得分：相同订单数据、规范序列和初始状态下配对评价候选；确定性有限池精确枚举时，每个候选保留一个等权结果，重复值不去重；抽样时跨评估器使用同一候选抽样，并用帽号区分估计得分。常规评价不额外强制相同 AMR 分配，该条件仍属于后文排序命题。

4.1.2 在任何命题和证明之前给出一般类级 minimax 与波次释放：精确得分使用 Section 3 式（15）的 q*，估计得分使用当前式（35）的 q_hat；固定类别标签顺序处理并列，然后分别按 nu_q* 或 nu_qhat 抽取具体波次。M3 与直接候选基准保留为单独评价，不进入主确定性类别目标。

总体中位数与样本中位数的区别、M3 联合结果分布、重复间及候选与噪声之间的独立性均保留。若总体中位数区间非唯一，普通样本中位数不自动一致估计其中点；确定性有限候选池优先精确枚举，抽样统计的推断条件仍需 Section 5 单独核查。

### 7.2 4.2 Class-relative performance diagnosis

固定配置、波次规模和评估器后，以 `b_q = mu_qm^(0.5)` 表示类别中位数，以整个候选池的均匀分布定义 `b_0`；使用 `b` 避免把中位数记号与评估器索引 `m` 混在一起。定义 `q_min`、`q_max` 和外部给定的描述指标规则所选类别 `q_Phi`，再定义 UB、LB、GAP、H_up 和 M_Phi。

- UB 是 normalized class spread；LB 是 selected-class normalized gain，不能将名称直接当成完整调度问题的优化上下界。
- `H_up = (b_max-b_0)/b_0` 是 class-family-relative upper-tail headroom；`M_Phi = (b_qPhi-b_min)/b_0` 是 class-selection miss。
- 命题 1 是代数恒等式。`UB >= 0`、`0 <= M_Phi <= UB` 成立；H_up、LB、GAP 一般均可能为负。角点族不保证覆盖全部候选且可能重叠，因此即使精确枚举，H_up 也不自动非负；不能只归因为有限样本噪声。
- 命题 2 的 SPO 解释以类别标签为动作，以相同类别成本向量定义所选动作与最优动作。由于当前类别可能重叠，统一称 class-action loss，不直接称具有唯一波次归属的 partition-constant predictor；训练保证与 P9 结果仍需单独论证。
- 定理 1 仅比较同一基础分布、同一评价机制下的嵌套、互斥、覆盖分区 P/P'。正文已给出兼容 midpoint median 的混合夹逼证明。推论 1 是该覆盖分区序列的性质，不再称当前 truncated corner family 的实现特例。
- 细化只保证 H_up、oracle gain 和 UB 不减；M_Phi、GAP 或两类份额均无无条件单调性。精确样本核查需要划分同一组带权结果样本。

实验化时仍须在 Section 5 写明 q_Phi 的具体拟合、零系数/并列与空类别处理规则，以及样本分割和重复方案。当前诊断是对该给定规则的评价，不替代或改变 4.1 的鲁棒选择规则。

### 7.3 4.3 Conditional ordering of the deterministic evaluators

新命题 3 对应旧工作包的 Prop. 2，是 C2 的主理论。保留全 E、全整数 c 的条件（a）—（d）：相同订单序列、相同 AMR 分配、无批次超越、无不利调位。规范排序仅保证（a），不能自动保证（b）；（d）中的楼层是所选资源在其记录的下一可用时刻对应的保存楼层。

正文给出 W3/W9 归纳的两段证明思路，含 case B 的最新行程计数机制，并保留 X1（26 对 24）与 X2（103 对 68）的完整参数和解释。最终 Appendix A 仍需组装 Lemma 3–6 和完整归纳。两类反转通道仅在请求序列和 AMR 分配已对齐时构成穷尽分类；它们不能被称为每个有序波次必须满足的必要条件。

从逐候选排序转到类别排序时，使用同一类内释放分布，且明确要求类别支持集中的每个候选满足充分条件，或另外直接检查类别分布/中位数排序。经验排序频率、充分条件满足率和类别中位数排序分别记录。

### 7.4 4.4 Properties of robust class selection

新定理 2 对应旧 Theorem 1。若每个可选类别的 M2 中位数均不低于 M1，则两模型 median-minimax 最优类别集合等于 M2 中位数最优类别集合；具体波次继续由 Section 3 式（12）的固定类内抽样规则产生。

推论 2 使用 `a_q = mu_qM1^(0.5)`、`b_q = mu_qM2^(0.5)`、`e_q = [a_q-b_q]_+` 和 `V_q = b_q+e_q`，先精确界定保守选择相对于 median-minimax 最优值的超额损失，再引入 M2 类别排序间隔 Delta_H。`Delta_H > e_qH` 是唯一选择保持不变的充分条件；M1-specific regret 不属于此界。

旧单一 lower inverse-CDF 的 U_q 不适用于目前的 midpoint median。新版式（53）—（55）分别定义下、上分位数端点，以两端点均值构建 U_q^mid。违反概率前提是同一候选耦合下、逐类别的概率界，而不是把总体经验比例直接当作所有类别的精确界。旧 U_q 数值需重查，不能沿用旧公式声称通过。

推论 3 单独陈述 mean-based、class-specific、model-calibrated Wasserstein 关系。固定中心 P_q1，半径为两模型的 W1 距离；在 FOSD 下，P_q2 本身达到最坏均值上界。该关系比较均值最优类别，不声称等于主 median 最优类别，也不声称完成外部数据校准。

推论 4 用 `M^+` 表示扩展评估器族，避免占用 Section 3 已表示候选数的 K。要求统一的最大中位数成员；否则保留逐类别上包络。M3 的纳入需要另行检查其类别得分。

### 7.5 新旧理论编号对照

> **2026-09-26：IJPR 版的目标编号见 §00.5；在 §4 按 IJPR 重写前，下表仍是当前 §4 md 的有效编号。**

理论编号保持首次重构时的对应关系，当前只将实施流程提前；命题与定理的相对出现顺序不变。初稿公式（56）—（58）移为当前（33）—（35），初稿（33）—（55）顺移为当前（36）—（58），公式数学内容不变。后续施工采用下表正文编号。历史工作包、日志与旧结果标签不回写；本文件其他章节引用历史 Prop. 2 / Prop. 3 / Theorem R 时，按此表解释。

| 理论内容 | 新 Section 4 编号 | 旧工作包编号 |
|---|---|---|
| 诊断恒等式 | Proposition 1 | Proposition 1 |
| 类别动作 SPO 损失解释 | Proposition 2 | Proposition 3 |
| 嵌套覆盖分区细化 | Theorem 1 | Theorem R |
| 覆盖分区诊断分辨率 | Corollary 1 | Corollary 1（适用范围已修正） |
| 全 E 条件性样本路径排序 | Proposition 3 | Proposition 2 |
| 条件性 minimax 简化 | Theorem 2 | Theorem 1 |
| 超额损失、排序间隔与中点分位数界 | Corollary 2 及式（53）—（55） | Corollary 2（公式已修正） |
| 模型校准的均值 DRO 比较 | Corollary 3 | Corollary 3 |
| 有限评估器族条件扩展 | Corollary 4 | Corollary 4 |

Lemma 3–6 的历史标签保留供 Appendix A 组装；正文仅给出其依赖的证明思路，不把附录组装标为已完成。

### 7.6 本章完成门槛

- 已有：方法优先的中英文重构正文、两段方法总述、前置的选择与释放流程、与 Section 3 的记号衔接、式（33）—（58）、完整主命题条件、两组手算反例与理论交叉核查。
- 待完成：Appendix A 完整证明组装；附录中 midpoint quantile 修正与统计推断条件同步；作者对命题假设和证明人工通读。
- 待对齐：生产代码与模型合同、q_Phi 的实际规则、旧统计结果和修复后重算、后续章节中的新理论编号。
- 全文继续区分 identity、loss interpretation、conditional theorem 和 empirical regularity；保持 median/mean、M1/M2/M3、类别/候选基准各自的范围。

---

## 8. Section 5 Experiments and Results 如何进行

> **2026-09-26：IJPR 版 §5 的结构见 §00.2（5.1 设计与登记层级；5.2 研究一；5.3 研究二；5.4 案例；5.5 边界）。本章对研究一数字、措辞与完成门槛的要求全部保留，分别落在 5.1、5.2、5.5。**

### 8.1 5.1 Design, preregistration, and reproducibility

先准确列出代码中的因子：`F={3,5,8}`、`|A|={5,15,30}`、`E={1,2}`、三类 demand、wave sizes，以及 18 个 fractional configurations。说明 `F`、`|A|` 与 demand 的构造别名关系，因此不能识别干净的主效应。

区分三种计数：candidate waves、matched-wave rows、model evaluations。摘要的 106,800 只能在这里给出可复算公式后继续使用。修正 T1 中 `{5,10,20}` 与代码 `{5,15,30}` 的冲突。

将主研究、原始预注册、签署修正案和事后探索分层列出。已经执行的 B-2/B-3/B-5 不得再写 pending。AI 辅助脚本/对抗验证按照期刊政策如实披露，但科学判断和最终数学复核由作者承担。

实验设计表增加“证据标签”列，按本文件 §0.3 使用 `[PR-C]`、`[PR-E]`、`[AM1]`、`[AM2]`、`[RA]`、`[NS]`、`[EXP]`、`[QA]`。

生产 `id(e)` tie-break 先修成 explicit index。随后至少重跑受影响的 Block C/关键表，保存旧/新哈希与 gate-equivalence。没有完成前不得称精确可复现。

### 8.2 5.2 RQ1: Partition-relative diagnostic results

报告顺序：

1. mean `GAP = 0.060`、`H_up = 0.043`、`M_Phi = 0.017`，并换算为约 6.0、4.3、1.7 个 baseline-makespan percentage points；
2. Prop. 1/Prop. 3 pipeline checks 72/72；
3. 非负 70/72，说明两个近零有限样本例外；
4. signal-resolution 57/72 vs 58/72，判定 PARTIAL；
5. 预注册 `Phi`-rule share 约 72% 与 covering share 约 47% 并列；禁止给容量标签；
6. Theorem R 的 nested/covering validation 48/48；
7. test–retest：15/18 二元 verdict 一致，但 ICC 失败；numeric share 不稳定。

现有行级 bootstrap 必须在保存 `candidate_id` 后重做。建议按 seed/config/order-pool cluster bootstrap，或以多个独立 order pools 建立 hierarchical model。修正前，CI 只标 preliminary。

将 `[RA]` OOS 结果作为敏感性而非新主判定：单次分析中 `M_Phi` 从约 0.0170 降至 0.0142，`H_up` 从约 0.0430 降至 0.0339，train/test `q_min` 在 17/72 cells 翻转且 9/72 `M_Phi_oos` 为负。后续若保留 OOS 卖点，应做多 split/nested OOS，并在每个 split 重新拟合 `q_Phi`。

### 8.3 5.3 RQ2: Dominance mechanism and Hedge result

并列报告：

- 自由实践口径 empirical ordering 99.2%，worst cell 96%；
- theorem-aligned enforced-hypotheses 口径 99.67%；
- 条件基率与联合覆盖率，明确不足 1%；
- 违例通道 18 batch overtaking、2 reverse repositioning、0 other（与最终日志核对后冻结）；
- 24/24 FOSD、6/6 collapse/DRO match，称 preregistered internal/model-class evidence；
- Hedge 实付代价：5/6 配置为 0，config 11 为 2.63%；C-4 informativeness 0/6 FAIL 必须报告。

不要把“条件罕见但 ordering 常见”写成定理被验证。正确结论是：充分条件解释可证明子集及失败机制，而广泛 ordering 是该 evaluator family 中的经验规律。

### 8.4 5.4 RQ3: Policy-class and benchmark comparisons

重新命名 P5/P6/P7，并加入 P8/P9：

- P5 相对 P0/P1/P6 的胜率可报，但对 P7 为 0/12、约高 46%；
- P8 grand mean 约 288.4，胜 P0–P4 12/12、胜 P5 10/12、胜 P6 11/12、负 P7 0/12；
- P9 的 median recovery `R=1.00` 按锁定规则写 partial recovery，并披露零预算排除；
- config 1、size 8 的 pool optimum 38，P7 +47.4%，P5 +147%，只作一个可枚举锚点，不能外推全网格。

P9 在 7/12 cell 超过 coarse corner oracle 是重要边界证据：`H_up` 只限制指定 partition-constant class，不限制一般 wave-level policy。

### 8.5 5.5 Robustness and model validity

将以下内容集中，不散落在 Discussion：

- OOS `M_Phi` 收缩约 16.6%；
- `c={2,3,4,5}` sweep 只支持 ordering 的容量范围扩展，不是容量收益实验；
- M3 只用于 stochastic robustness，不进入 exact deterministic chain；
- operational clustered dispatch 平均改善 10.2%、12/12 超过 1%，说明运营层不是无关常数；
- DES dominance 98%–100%，但 rank `rho=0.45–0.68` 且 makespan 高估 25%–37%，因此 class/wave ranking 限于闭式 evaluator；
- partition 与 metric 双口径、ICC 和 pseudo-replication 共同构成 measurement boundary。

B-5 使用的是项目内 `heapq` DES cross-check，不得在正文写成 SimPy 实施，除非代码确实迁移并重跑。

### 8.6 表图安排

| 展示项 | 章节 | 修改要求 |
|---|---|---|
| Fig. 1 system schematic | §3 | 与 single-wave、固定运营层一致 |
| Fig. 2 Hedge schematic | §4 | 明示 conditional ordering；输出 class 而非具体 dispatch |
| Fig. 3 GAP by demand | §5.2 | 说明 fractional-design aliasing，不估 demand 独立效应 |
| Fig. 5 decomposition | §5.2 | 删除 capacity-side 配色/标签，改 upper-tail vs class miss |
| Fig. 8 resolution | §5.2 | 只画 nested/covering comparisons |
| Fig. 9 reliability | §5.2 | 突出 ICC FAIL 与 verdict/numeric 区别 |
| Fig. 4/6 policy comparisons | §5.4 | 更新 P5/P6/P7 名称并纳入 P8/P9 |
| Fig. 10 DES | §5.5 | 同时显示 sign survival 与 rank failure |
| Fig. 7 managerial workflow | §6 | 删除 buy-capacity 分支；改为“需要单独 capacity study” |

### 8.7 本章完成门槛

- 所有数字能从 JSON/CSV 一键复算；
- 统计单位、重复 wave 和共享订单池被正确建模；
- 预注册、修正案、探索分析有显式标签；
- H-D1/H-D2 结论不互相借势；
- 负结果与正结果同等可见；
- 结果节不再解释容量投资或现实因果。

---

## 9. Section 6 Discussion and Conclusion 如何进行

> **2026-09-26：IJPR 版 §6 按 STORY_CONTRACT.md 的 RQ1 至 RQ3 各写一段，另加释放流程的操作段（步骤、输入、耗时、短名单大小、何时启用 max{M1, M2} 筛选）。本章对局限、未来工作与禁用表述的要求保留。**

**起点：** W5 仅保留组织形式，不保留其 capacity-bound 结论。

### 9.1 6.1 回答 RQ1

说明 coarse partition 能把 wave-structure variation分成 upper-tail headroom 与 selected-class miss，但分解是 partition-relative。6% 是本合成网格中的平均量，不是一般仓库常数；72%/47% 的差异说明结论取决于 instrument。

### 9.2 6.2 回答 RQ2

讨论 conditional sample-path result 的理论意义：它识别可证明的 ordering 机制和两类失败通道。经验 ordering 远比充分条件覆盖面广，说明仍有未被定理刻画的机制空间。Hedge 的实际代价在 5/6 为零、一个配置为 2.63%，但证书保守且不能自动迁移到 DES 排序。

### 9.3 6.3 回答 RQ3 与实践含义

实践建议只能是分阶段诊断：先验证本地 evaluator 与 ordering，再评估 coarse class 是否有信息，最后才选择 wave class。若管理问题是“改 policy 还是买 capacity”，本文结果只能触发一个独立的 matched capacity study，不能直接回答投资方向。

operational dispatch 10.2% 大于 tactical GAP 6.0%，应被解释为 scope boundary：本文隔离上游决策以研究其机制，并不意味着运营层可忽略。

### 9.4 6.4 Limitations

至少完整披露：

1. synthetic data，无现场校准；
2. single-wave cold start，无跨波状态/积压；
3. closed-form sequential evaluator，DES rank fidelity FAIL；
4. fractional design 主效应混淆；
5. partition/metric/seed sensitivity 与 ICC FAIL；
6. 有放回抽样和共享 order pool 的统计依赖；
7. M1 是 throughput abstraction，不是物理设备模型；
8. policy contest 只覆盖有限 class/size/configuration；
9. DRO ambiguity radius 为 candidate-model calibrated；
10. 无 capacity investment variable、成本或反事实。

### 9.5 6.5 Future work

按限制一一对应：rolling multi-wave DES、真实 trace calibration、匹配容量干预、改进 descriptor（含距离与动态拥堵）、独立 order pools/层级统计、联合 upstream–operational optimization。已完成的 B-2/B-3/B-5 不得再列为 future work。

### 9.6 6.6 Conclusion

结论只重复三个有证据的动作：提出 scoped benchmark；给出 conditional ordering mechanism 和 conservative class selection；用预注册实验揭示其经验强度与 validity boundaries。最后一句不得落到 capacity purchase，应落到“诊断结论必须与 partition、policy class 和 evaluator fidelity 一起报告”。

全文总判定不能写成笼统的“all gates passed”。需分别汇报：H-D1 `[PR-C]` PARTIAL；H-D2 `[PR-C]` PASS；H-Policy `[PR-C]` PARTIAL；H-D3 `[PR-E]` model-sensitive；Amendment F `[NS]` reliability composite FAIL；C-4 `[NS]` informativeness FAIL；B-5 `[NS]` ordinal-fidelity FAIL。

### 9.7 本章完成门槛

- 每段明确回答一个 RQ；
- 不从 association/partition statistic 跳到 capacity causality；
- 所有正面发现紧邻一个适用边界；
- future work 不包含已完成事项；
- Conclusion 与 Abstract 使用同一三贡献版本。

---

## 10. Appendix 如何进行

### Appendix A — Full proof of conditional dominance

以 W3-E2/W9 的最终归纳为主，含 Lemma 3–6、case F/B、条件 `(a)–(d)`、全 `E`、X.1/X.2。删除旧 E=1+Conjecture 版本和单一失败通道叙事。作者必须对 W9 §5.2、case-B 前提和 midpoint/median bracketing 做人工通读。

### Appendix B — Diagnostic and partition mathematics

给出新 Proposition 1/Proposition 2 的完整但简短推导、新 Theorem 1 与 covering/nested definitions（旧编号分别为 Prop. 1/Prop. 3/Theorem R）。显式区分 truncated corner instrument 与 covering partitions，不让非嵌套 2×2→3×3 进入 theorem validation。midpoint-median 混合夹逼证明以新 Section 4.2.3 为准，不再使用仅证明 lower-median 情形的旧版本。

### Appendix C — DRO certification and perturbation bounds

保留 W2 的可用数学，但分开 mean-based Wasserstein relation、median-based `U_c`、M1-side empirical regret。写明 common radius 与 corner-specific radius的差别，避免将模型内校准说成外部 robustness。

### Appendix D — Experimental protocol and statistics

包含 configuration 生成关系、seed、order/candidate pool、抽样层级、`candidate_id`、cluster bootstrap/hierarchical analysis、OOS split、门槛定义和多重比较处理。

### Appendix E — Complete results and negative findings

放 72-cell 表、P0–P9、pool optimum、C-4、partition sensitivity、ICC、DES、tie-break old/new equivalence。所有结果按 preregistered/amendment/exploratory 标记。

### Appendix F — Reproducibility and integrity

列代码版本、环境、命令、输入/输出哈希、tie-break 修复、已知 bug、数据字典、匿名仓库结构、AI assistance disclosure。冻结的预注册和签署修正案保持原样，仅链接，不修改。

### 附录完成门槛

主文每个 theorem/corollary 均有唯一 proof pointer；所有表格数字有 machine-readable source；附录不得成为隐藏关键失败结果的地点，DES/ICC/H-D1 PARTIAL 必须先在主文出现。

---

## 11. References 与投稿配套如何进行

### 11.1 References

合并 `references_chain_dominance.bib` 与 `references_related_works.bib`，去重后统一 author-year。完成既有 DOI/作者核验，并加入本轮 2025–2026 前沿来源。对每条 citation 做两向检查：正文出现则 BibTeX 必有；BibTeX 被列入最终库则正文或附录应实际引用。

### 11.2 Submission back matter

准备匿名正文、title page、funding、COI、CRediT、data/code availability、AI disclosure、highlights 与 keywords。图表应以数据生成脚本重导出，核对分辨率和可访问配色。图形摘要在正文主线冻结后制作，不要以旧 capacity-versus-policy 流程为蓝本。

### 11.3 最终 DOCX

只有当 §1–§6 和 Appendix 的 Markdown 主稿均通过本文件完成门槛后，才生成新的完整 DOCX。根目录现有 DOCX 保留原名作历史基准，新文件建议命名：

`Wave_Release_Coordination_revision_2026-09-02.docx`

生成后检查标题层级、目录、公式、交叉引用、图表、参考文献、页码、匿名化和 Word 编码。不得把 frontmatter 中的内部 change log 写进投稿正文。

---

## 12. 实际施工顺序

### Phase 1 — 先修定义和代码

- [ ] 冻结 single-wave scope 与 primary median metric。
- [x] 修复 production simulator 的 `id(e)` tie-break。（2026-09-11 完成，见 `qa_2026-09-11/`）
- [ ] 修正 `T` 方向、release chronology 和 M1 物理解释。
- [x] 保存 `candidate_id` 与 order-pool/seed 层级。（2026-09-11：harness 新增 `candidate_id`/`cand_seed` 列；存量 Block A/B/C 由种子回放补齐 sidecar）
- [ ] 修正 T1 因子水平与 106,800 count 定义。

### Phase 2 — 重算受影响统计

- [ ] 重跑/核对 tie-break 影响并记录 old/new 哈希。（2026-09-11：Block C + smoke 已完成并记录哈希；Block A/B 是否在修复后全量重跑待作者决定，见 QA 记录）
- [ ] 做 cluster bootstrap 或 hierarchical reanalysis。
- [ ] 冻结双口径、ICC、P8/P9、C-4、DES 和 OOS 数字。
- [ ] 若门槛判定改变，按原预注册规则报告，不保留旧判定以迎合叙事。

### Phase 3 — 先写 Methods/Results

- [ ] 完成 §3 单波模型。
- [ ] 完成 §4 理论层级和附录证明。
- [ ] 按 RQ1–RQ3 完成 §5；同步重做表图标签。

### Phase 4 — 再写 Discussion/Related Works/Introduction

- [ ] 以最终结果重写 §6。
- [ ] 完成 §2 前沿定位表。
- [ ] 用最终 scope 和贡献重写 §1。

### Phase 5 — 最后写 Abstract 与投稿文件

- [ ] Abstract ≤250 words。
- [ ] Highlights、keywords、graphical abstract、back matter。
- [ ] 组装并验证完整 DOCX。

### Phase 6 — IJPR 版（2026-09-26 起）

见 §00.6 的逐周清单。Phase 1 至 Phase 5 中尚未勾选的项目并入对应周次执行。

---

## 13. 全文交叉一致性门槛

| 检查项 | 通过条件 |
|---|---|
| 问题对象 | Title、Abstract、§1、§3、§6 均称 single-wave candidate/class selection，或全部完成多波模型后再统一升级 |
| 贡献 | 全文只使用本文件 §2.2 的 C1–C3 结构 |
| `H_up` | 全文无 capacity-side、buy capacity 或 general policy-unrecoverable 解释 |
| `Phi` | 主 2×2 `(C,I)` 与扩展 `T` 的角色一致，不声称三维特征 fully captures system |
| 模型族 | exact ordering 仅 M1/M2；M3 单独作为 stochastic robustness |
| 统计量 | median 为主；mean-based DRO 单独标记，二者不互换 |
| 模拟器 | closed-form 主 evaluator 与 event-driven DES cross-check 名称不混 |
| 样本量 | 106,800 的 counting unit 可从表/代码复算 |
| 统计独立性 | 重复 candidate 和共享 order pool 在区间估计中被聚类处理 |
| H-D1/H-D2 | PARTIAL 与 scoped PASS 分开报告，不用一个结果为另一个背书 |
| 外部效度 | 所有实践结论带 synthetic、single-wave、fixed-evaluator、DES-rank boundary |
| 前沿性 | 无 `never/only/first` 无证据绝对句；最近邻比较更新至 2026-09-02 |
| 文档完整性 | Word 含 Abstract、§1–§6、Appendix、References、表图与 back matter；无内部 change log |

---

## 14. 本轮折叠后的唯一结论

现有项目不是缺少材料，而是材料来自不同时间点、对相同指标赋予了不同含义。最危险的旧含义是把 `H_up` 当成容量效应；最危险的旧范围是把单波候选选择称作完整 two-stage scheduler；最危险的旧证据语言是把恒等式、模型内校准和行级重复样本当成外部验证。

本轮 revision 的中心任务因此不是继续增加卖点，而是完成三次对齐：§3 的决策对象与代码对齐，§4 的理论强度与假设对齐，§5–§6 的结论与真正 estimand 对齐。完成这些对齐后，论文仍可保留一个有辨识度的狭义问题贡献、一个以 conditional dominance 为核心的方法贡献，以及一个将 measurement/model boundary 正面化的实证贡献。
