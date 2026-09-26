---
title: "revision_0719：逐章更新工作包"
date: 2026-07-19
base: "根目录 Word 主稿《Wave Release Coordination under Vertical Resource Constraints in Multi.docx》"
status: "分章节整理的最新修订部件；文件均为副本，原件位置见下"
---

# revision_0719 使用说明

**基稿** = 根目录 Word 主稿 docx。它目前只含 Abstract、Introduction、Related works、Problem Formulation（§3）；**§4、§5、§6、附录在 docx 中尚不存在**，属于"新写入"而非"修改"。每章文件夹里：`original_docx_*.md` = 从 docx 提取的当前原文（无原文的章没有此文件），其余 = 该章最新更新部件，`README.md` = 本章更新清单。

## 建议工作顺序

1. **先做全局**（`00_global/`）：W1 的术语/编号 find/replace 先在整份 docx 上过一遍，再逐章改，避免新旧编号混排。
2. 然后按 `01_ → 10_` 逐章进行。
3. 图表：`figures/` 有 10 张最新图和放置对照表；§5 的表在 `06_Section5_Experiments/tables/`。

## 最终编号方案（裁定于 2026-07-08，全文统一）

Prop 1（恒等分解）、Prop 2（全 E 条件链支配，(a)-(d)）、Prop 3（SPO 桥）、Theorem 1（minimax 坍缩）、Theorem R（分区分辨率，§4.1.4）、Cor 1（细化单调特例）、Cor 2（ε 界 U_c）、Cor 3（DRO 认证）、Cor 4（K 模型）；Lemma 3-6 只在附录。

## 全局硬规则

- 命名以 `paper_draft/TERMINOLOGY.md` 为唯一权威（无破折号；C 高=楼层分散；Φ 不写 "predicts"；Hedge Rule 不写 "dispatch"）。
- 禁止引用 prototype 尺度数字（6-cell、M4/M5 时代）；出版尺度 = v0_5_phase5 系列。
- 已锁判定不得重判：H-D1 PARTIAL（57/72）、H-D2 PASS。
- Wang et al. (2025) 五作者，引用格式 "Wang et al."。

## 各章一览

| 文件夹 | 论文章节 | docx 原文 | 核心部件 |
|---|---|---|---|
| 01_Abstract | Abstract | 有 | abstract_v1.0.md（需裁到 250 词） |
| 02_Section1_Introduction | §1 | 有 | introduction_v1.0.md + W7 Edit 6 |
| 03_Section2_RelatedWorks | §2 | 有 | related_works_v1.0.md + W7 |
| 04_Section3_Formulation | §3 | 有（最完整章） | W4（最新表述） |
| 05_Section4_Methodology | §4 | 有（旧 Section 4.docx，已归档件） | section4_draft + prop2 模块 + W3/W8 |
| 06_Section5_Experiments | §5 | 无 | section5_draft + §5.3 模块 + T1-T6 |
| 07_Section6_Discussion | §6 | 无 | W5 即全文 |
| 08_Appendix | 附录 | 无 | 证明模块 + W2/W9 |
| 09_References | 参考文献 | 无 | 两个 .bib + 核验清单 |
| 10_Submission_BackMatter | 投稿配套 | 无 | C&IE 合规清单 |

## 副本来源（原件勿动）

各节 md 最新稿来自 `paper_draft/manuscript/`；W1-W10、T1-T6、fig1-fig10 来自 `revision_2026-07-08/`（签署交付物，审计留痕）。**如需改部件内容，请改 `paper_draft/manuscript/` 中的原件再重新拷贝；本目录副本只作对照参考。**

## 2026-08-06 全面审查（三贡献 × 五标准）

对抗验证版审查报告：`research_notes/contribution_review_2026-08-06.md`（32 条幸存发现，六大主题，按章节的行动清单）。**施工优先级高于各章 README 中的旧任务**：主题 A（Tool 2 定理计费）与主题 B（C3 双口径标题）涉及已定稿的 Abstract v1.7 与 §1 v1.1，需要重开。
