---
title: "写作台索引：当前论文写作文件一览"
date: 2026-07-19
last_updated: 2026-09-03
status: "SUPERSEDED FOR ACTION — 历史进度记录，不再作为施工入口"
---

# 00_INDEX：历史写作台（已停止施工）

> **当前唯一施工入口：** `../../revision_2026-09-02/MASTER_REVISION_BY_SECTION.md`。该主控已经折叠本索引中仍有效的内容，并覆盖下表的旧状态、旧拼接顺序和旧贡献裁定。

本文件仅保留 2026-07 至 2026-09 初的章节进度轨迹。下表和后续 W1–W10 拼接顺序属于历史快照，不得直接执行；所列正文文件仍可在最新主控指定时作为句子或结构底稿。

| 论文章节 | 本文件夹最新稿 | 待应用的修订层（在 `../../revision_2026-07-08/tier1_manuscript/`） | 状态 |
|---|---|---|---|
| Abstract | `abstract_v1.1_250w.md`（正文 v1.8，249 词，2026-09-02） | 2026-08-06 审查主题 A/B 重计费：定理句改条件式（"Wherever it is slowest ..."）+ 双通道句、"passes every gate" 改四门、天花板收窄为 group-level、判定句加 instrument 限定语（详见 frontmatter 第 19 条） | **重开，待作者重新批准**（v1.7 定稿被主题 A/B 推翻）；`abstract_v1.0.md` 保留为双语工作稿 |
| §1 Introduction | `introduction_v1.1.md`（正文重开版，2026-09-02） | 2026-08-06 审查主题 A/B/D/E6：C2 重计费（删 "guarantee rests on Proposition 2"，Theorem 1 条件式，Prop 2 = 机制结果）、C3 双口径（72% Φ-rule / 47% covering）、Cor 1/Cor 2 措辞修正、可委托性降档（详见 frontmatter 第 16 条） | **重开，待作者审读**；v1.0 保留为双语工作稿 |
| §2 Related Works | `related_works_v1.1.md`（英文投稿版，2026-07-31） | 已全部应用（Wang et al. 2025 例外段、裁定编号、minimax 范围修正、Theorem R 类比 + Blackwell/Song-Luedtke） | **改写完成，待作者审读**；v1.0 保留为双语工作稿 |
| §3 Formulation | （无旧稿，全新节） | **W4** 即全文 | 直接采用 W4 |
| §4 Methodology | `section4_draft_v0_1.md` + `proposition2_chain_dominance_v1.0.md`（§4.2.1 模块） | W1（重编号）+ W3（经 W9 knock-on）+ W8（§4.1.4 Theorem R） | 按 W10 §6.4 顺序拼接；Prop 2 已升级为全 E |
| §5 Experiments | `section5_draft_v0_1.md` + `chain_dominance_empirical_v1.0.md`（§5.3 模块） | W6 + W10 §4（§5.3 重写、复现性声明、Table 4 扩展、DES 小节） | 表 T1-T6、图 fig1-fig10 在 revision 文件夹 |
| §6 Discussion | （无旧稿，全新节） | **W5** 即全文 | 直接采用 W5 |
| Appendix | `chain_dominance_proof_v1.0.md` | W2（DRO + H_up 数学）+ W3-E2/W9（归纳 + Lemma 6） | 待拼接 |
| References | `references_chain_dominance.bib`、`references_related_works.bib` | 无 | bib 文件自带提交前核验清单（DOI、Wang et al.、Boysen & de Koster） |
| 编译稿 | `v1.0.pdf` | 不含 2026-07-08 修订层 | 拼接后重新编译 |

## 拼接顺序（W10 §6.4，裁定后版本）

1. §4.2.1 用 W3-E4 的段落**结构** + W9 §7 knock-on（单一 Proposition 2、(a)-(d)、全 E；删 Conjecture 1 段；保留 X.1/X.2 两个反例）。W3-E4 原文已被 Lemma 6 取代，**不可**逐字粘贴。
2. W1 交叉引用，但 Edit 8/11 的排他性句子改用双通道表述（W10 §4 / B-1）。
3. W6/W7 行级修改（W7 的引用写作 "Wang et al." 五作者）。
4. §5 各处重写（W10 §4 清单）。
5. 编号方案以 W10 §5.1 为准：Prop 1 / Prop 2（全 E）/ Prop 3 / Theorem 1 / Theorem R / Cor 1-4。

## 不在本文件夹但写作时常用（勿移动）

- `../TERMINOLOGY.md`：命名唯一权威（无破折号规则、量表方向等），动笔前查。
- `../phase5_scaleup_preregistration.md`：**冻结**，只读。
- `../theorems_m4.md`、`../theorems_m5.md`、`../methodology_v0_2.md`：prototype 时代旧稿，但被冻结的预注册以相对链接引用，**必须留在原位**；写作时不要从中取数（prototype 尺度）。
- `../storyline_motivation_to_contribution_v1.md`：动机到贡献叙事线。
- `../heft_additions_v0_1.md`：§6 未来工作素材（RL 属于运营层、另文）。
- `../../revision_2026-07-08/`：修订交付物（W1-W10、六份签署修正案、T1-T6 表、fig1-fig10 图、EXECUTION-LOG）。审计留痕，原样保留。

## 归档位置

- `../archive/`：prototype 时代旧稿（旧 outline、phase4 预注册、执行计划等），见其 MANIFEST.md。
- 仓库根 `archive/`：过时的 Section 4.docx/pdf、旧示意图、Word 临时文件，以及原 `revision_0719/` 的完整历史快照；见 `../../archive/MANIFEST.md`。
- 仓库根 `research_notes/`：研究方向文档（north star、novelty 分析等）。
