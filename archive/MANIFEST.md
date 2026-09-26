---
title: "根目录 archive 归档清单（全仓库唯一归档处）"
date: 2026-07-19
last_updated: 2026-09-26
status: "只存不取：这里的文件不是现行来源，不要从中引用数字或结论。2026-09-26 起全仓库的过时材料统一折叠到本目录"
---

# 归档清单（仓库根 archive/）

**用法。** 本目录是全仓库唯一的归档处。现行来源一律以 `revision_2026-09-02/MASTER_REVISION_BY_SECTION.md` §1.1 和 `CLAUDE.md` 的 Layout 为准。以后被取代的文件也放到这里，不要再新建各自的 archive 子目录。2026-09-26 这一批的逐文件新旧路径、git 跟踪状态和移动前后 SHA-256（逐一核对一致）记录在 `CLEANUP_2026-09-26_moves.json`；按其中的 `from`/`to` 反向移动即可恢复（被 git 跟踪的文件用 `git mv`）。

## 目录一览

| 子目录 | 内容 | 原位置 | 归档日期 | 依据 |
|---|---|---|---|---|
| `revisions/revision_0719_snapshot/` | 七月章节包装快照，67 个文件 | 根目录 `revision_0719/` | 2026-09-03 | 详见 `revisions/MANIFEST.md` |
| `superseded/` | 旧 §4 单节 Word 与 PDF、旧示意图、旧 README | 根目录 | 2026-07-19；README 为 2026-09-26 | 见下表 |
| `paper_draft/` | 原 `paper_draft/archive/` 的 5 个文件，加上 2026-09-26 归档的 storyline 与 `manuscript/` 下的旧稿 | `paper_draft/archive/`、`paper_draft/`、`paper_draft/manuscript/` | 2026-07-19 与 2026-09-26 | 详见 `paper_draft/MANIFEST.md`（主控 §1.2、§1.3） |
| `research_notes/` | `00_north_star.md`、`02_open_questions.md`、`03_decisions.md`、`novelty_analysis_and_contribution.md`、`paper_sections_documentation.md`、`formulations/problem_formulation_v0_1_DRAFT.md` | `research_notes/` | 2026-09-26 | 主控 §1.3："早期 MILP/SimPy/ALNS 或 prototype 路线，仅作研究历史"；四月的问题建模草稿已被定稿第 3 节取代 |
| `prototype/` | 四月的原型规划与说明：`MVS_prototype_plan.md`、`scope_rational.md`、`simulator.md`、`structure.md`；`results_figures/fig_section3_setting.{pdf,png}`（2026-09-11 版第 3 节图） | `prototype/`、`prototype/results/figures/` | 2026-09-26 | 计划已执行或说明已过期；第 3 节图的现行版本为 `revision_2026-09-24/fig1_section3_setting.png`。`prototype/intuitions_before_MVS_v0_2.md` 被冻结预注册直接链接，它又链接 `intuitions_before_MVS.md` 与 `MVS_v0_2_plan.md`，这三个文件因此留在 `prototype/` 原位（后两个曾被移入本目录，链接检查后当日移回，见移动日志的 `restored_after_check`） |
| `codex_review/` | Codex 审查快照 2026-09-07、09-10、09-14、09-14-finalcheck（Word 渲染页、提取文本、源 docx 快照、重构前第 3 节） | 根目录 `.codex_review/` | 2026-09-26 | 渲染核查的过程产物；主控第 334 行引用的重构前快照路径已同步更新 |
| `gpt_2026-08/` | `Abstract_Introduction_RelatedWorks_*` 两份 md 与一份 PDF | 根目录 `gpt/` | 2026-09-26 | 主控 §1.3："语言编辑产物，没有吸收本轮理论、测量和 C3 裁定" |
| `revision_2026-09-02/` | `SECTION_3_MODEL_FORMULATION.md`（2026-09-10 版第 3 节）；`figures/fig1_2026-09-14/`（旧 Fig. 1 调色设计） | `revision_2026-09-02/` | 2026-09-26 | 主控 §1.1：第 3 节现行正文为 `Problem formulation.docx`（双语镜像 `revision_2026-09-24/section3_bilingual_2026-09-24.md`）；现行 Fig. 3.1 为 `revision_2026-09-24/fig1_section3_setting.png` |
| `revision_2026-09-24/` | `_work/`（第 3 节定稿过程的渲染、裁图、差异、公式清单与一份 docx 备份）、`plan_section3_section4_v0_1.md`、`readiness_assessment_CIE_IJPR_2026-09-26_v1_CIE_baseline.md`、`section3_finalization_EJOR_edits_2026-09-24.md`、`fig1_section3_setting_v2/v3.{pdf,png}` | `revision_2026-09-24/` | 2026-09-26 | 已执行的修改清单、被 v0_2/v2 取代的计划、图的中间版本；现行文件留在 `revision_2026-09-24/` |

## superseded/ 明细

| 文件 | 原位置 | 说明 |
|---|---|---|
| `Section 4.docx` | 根目录 | 2026-05-28 的 §4 单节 Word 稿；内容已并入根目录 Word 主稿（"Wave Release Coordination ... Multi.docx"，2026-06-22） |
| `Section 4.pdf` | 根目录 | 同上的 PDF 导出（2026-05-27） |
| `fig1_bound_and_gap_framework.png` | 根目录 | 2026-05-21 方法示意图旧版；现行版本由 `python -m src.figure_methodology_schematics` 生成于 `prototype/results/figures/fig_bound_and_gap_schematic.png` |
| `fig2_model_dominance_hedge_rule.png` | 根目录 | 同上，现行版本为 `fig_hedge_rule_schematic.png` |
| `README_2026-09-03.md` | 根目录 `README.md` | 四月的工作目录模板（其中的 `00_north_star.md` 等结构早已不存在）；2026-09-26 由新的根目录 `README.md` 取代 |

## 2026-09-26 删除的内容（均无保存价值）

- `word_temp/` 整个目录：`~$ction 4.docx`、`~$ve Release ....docx`（2026-05-24 的过期 Word 锁文件）与 `~WRL0005/0444/2764/3160.tmp`（Word 保存残留）。本清单原先写明"确认 Word 主稿无异常后可整目录删除"；删除前已确认 Word 主稿可正常打开。
- `prototype/src/__pycache__/` 的 70 个 `.pyc` 字节码（运行时自动再生，`.gitignore` 早已排除；其中 54 个曾被 git 跟踪，已从索引移除）。
- 空目录：`.codex_review/2026-09-07/render/`、`.codex_review/word_20260903_phase1/`、`prototype/notebooks/`，以及移空后的 `.codex_review/`、`gpt/`、`paper_draft/archive/`、`research_notes/formulations/`、`revision_2026-09-24/_work/`、`revision_2026-09-02/figures/fig1_2026-09-14/`。

## 仍在原位、指向旧路径的历史引用（有意不改）

以下文件是带日期的历史记录或受冻结规则保护，其中提到的旧路径不作修改，按本清单回溯：冻结预注册 `paper_draft/phase5_scaleup_preregistration.md` 及其链接的 `theorems_m4.md`、`theorems_m5.md`、`prototype/intuitions_before_MVS_v0_2.md`；`revision_2026-07-08/` 全部审计文件；`research_notes/contribution_review_continuation_2026-09-02.md`（9 月 2 日裁定原文）；`revision_2026-09-02/qa_2026-09-11/` 的 QA 记录；`paper_draft/heft_additions_v0_1.md`；`papers/reading_log_lenoble2018.md`；`prototype/src/features.py`、`demand_patterns.py`、`experiments.py` 中的出处注释；已存结果 `prototype/results/*`。
