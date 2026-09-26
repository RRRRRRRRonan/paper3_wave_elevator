---
title: "archive/paper_draft 归档清单"
date: 2026-07-19
last_updated: 2026-09-26
status: "被取代的 paper_draft 文件；只存不取。2026-09-26 起原 paper_draft/archive/ 并入根目录 archive/，即本文件夹"
---

# 归档清单（archive/paper_draft）

本文件夹原为 `paper_draft/archive/`（2026-07-19 建立），2026-09-26 目录清理时整体并入根目录 `archive/`，同时收入第二批被取代的稿件。**全部为被取代的历史文件**，写作时不要从中引用数字（见 CLAUDE.md 的尺度混用警告），也不要把其中结论当作现行口径。新旧路径与 SHA-256 见根目录 `archive/CLEANUP_2026-09-26_moves.json`。

## 第一批（2026-07-19 归档，原位置 paper_draft/）

| 文件 | 归档原因 | 被谁取代 |
|---|---|---|
| `outline_v0_1.md` | 2026-04-22 脚手架，M4/M5 旧命名 | 各节 v1.0 稿 + W 层；关键词清单（§0）仍是投稿 front matter 的来源 |
| `phase4_H1_preregistration.md` | prototype 尺度预注册，已执行 | phase5 预注册（仍在 `paper_draft/` 原位，冻结）。作为诚信文档**逐字保留** |
| `tier1_execution_plan.md` | 计划已执行完毕 | `revision_2026-07-08/EXECUTION-LOG.md` |
| `pdf_revisions_optionB.md` | PDF 修订计划已执行 | `revision_2026-07-08/` 交付物 |
| `appendix_robustness.md` | 2026-04-22 六格 prototype 尺度稳健性附录 | 出版尺度稳健性：W2 + revision tier2 输出（A-R1/A-R3/C-4/B-5） |

## 第二批（2026-09-26 归档）

| 文件 | 原位置 | 归档依据 | 现行来源 |
|---|---|---|---|
| `storyline_motivation_to_contribution_v1.md` | `paper_draft/` | 主控 §1.3：以 capacity dominance 和 `U_c` 保底为主线，已被主控取代 | `revision_2026-09-02/MASTER_REVISION_BY_SECTION.md`；`revision_2026-09-26_ijpr/STORY_CONTRACT.md` |
| `manuscript/00_INDEX.md` | `paper_draft/manuscript/` | 主控 §1.2：只作 7 到 9 月进度记录，状态已过期 | 主控文件 |
| `manuscript/abstract_v1.0.md`、`introduction_v1.0.md`、`related_works_v1.0.md` | `paper_draft/manuscript/` | 主控 §1.3：`*_v1.0` 双语或旧稿，只保留 provenance | `paper_draft/manuscript/*_v1.1*` |
| `manuscript/v1.0.pdf` | `paper_draft/manuscript/` | v1.0 全文的编译 PDF（2026-06-22） | 根目录 Word 稿 |
| `manuscript/proposition2_chain_dominance_v1.0.md`、`chain_dominance_proof_v1.0.md`、`chain_dominance_empirical_v1.0.md` | `paper_draft/manuscript/` | 主控 §1.3：旧三条件、单失败通道骨架 | 命题 3（`SECTION_4_METHODOLOGY.md` §4.3）与附录 A 草稿（`revision_2026-09-26_ijpr/week3/APPENDIX_A_draft.md`） |

## 注意

1. `theorems_m4.md`、`theorems_m5.md`、`methodology_v0_2.md` **没有**归档：冻结的 `phase5_scaleup_preregistration.md` 以同目录相对链接引用它们，预注册不可编辑，故三个文件必须留在 `paper_draft/` 原位。
2. 归档文件内部的相对链接可能因移动而失效（例如指向 `../novelty_analysis_and_contribution.md`，该文件现位于 `archive/research_notes/`）。归档文件内容一律不再更新；按本清单和移动日志回溯。
3. W1 Edit 14 的术语替换清单中指向 `methodology_v0_2.md:19` 等处的修改，目标文件仍在 `paper_draft/` 原位，与本归档无关。
