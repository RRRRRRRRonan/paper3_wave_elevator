# Paper 3：多层 AMR 仓库中受垂直资源约束的波次释放协调

博士论文第三篇论文的工作目录：仿真代码、实验结果与稿件。目标期刊为 *International Journal of Production Research*（决策辅助型论文，两个研究），备选 *Computers & Industrial Engineering*。

## 从哪里开始

| 要做的事 | 入口 |
|---|---|
| 了解规则、目录与命名（也是 AI 助手的工作说明） | `CLAUDE.md`、`paper_draft/TERMINOLOGY.md` |
| 改稿件：各节现行来源、冲突裁决、禁用说法 | `revision_2026-09-02/MASTER_REVISION_BY_SECTION.md` |
| IJPR 版当前工作、待审阅与待签字事项 | `revision_2026-09-26_ijpr/00_REVIEW_GUIDE.md` |
| IJPR 修改方案与证据 | `revision_2026-09-24/readiness_assessment_CIE_IJPR_2026-09-26.md`（第二部分 v2） |

## 现行稿件来源

| 部分 | 现行来源 |
|---|---|
| Abstract、§1、§2 | `paper_draft/manuscript/abstract_v1.1_250w.md`、`introduction_v1.1.md`、`related_works_v1.1.md`（句子底稿，按主控改写） |
| §3 | `Problem formulation.docx`（双语镜像 `revision_2026-09-24/section3_bilingual_2026-09-24.md`） |
| §4 | `revision_2026-09-02/SECTION_4_METHODOLOGY.md` 与 `Methodology.docx`；§4.5 与附录 A 草稿在 `revision_2026-09-26_ijpr/week3/` |
| §5 数字 | `prototype/results/`、`revision_2026-07-08/tier2_analysis/outputs/`（注意标明尺度） |
| 全文 Word（仅取回细节） | `Wave Release Coordination under Vertical Resource Constraints in Multi.docx` |

## 目录

```
CLAUDE.md, AGENT.md, README.md      规则与入口
*.docx                              现行 Word 稿（§3、§4）与旧全文稿
paper_draft/                        术语、冻结的 Phase 5 预注册、研究二协议与 L2 附录、manuscript/ 文字底稿与 .bib
prototype/                          src/ 代码（在 prototype/ 下以 python -m src.<模块> 运行）、results/ 结果
revision_2026-07-08/                七月已签字的修订交付物（审计轨迹，保持原样）
revision_2026-09-02/                主控文件、§4 源稿、§4 配图、2026-09-11 QA
revision_2026-09-24/                IJPR 就绪评估与方案、第 3 节双语镜像与 Fig. 3.1
revision_2026-09-26_ijpr/           IJPR 工作夹：决定单、故事契约、登记修正案、执行日志、OSF 包、备份、第 3 周稿件
research_notes/                     贡献定位与裁定、阅读索引、真实数据评估、问题背景通俗解读
sources/                            前沿文献审计与引用核查
papers/                             引用文献 PDF 与阅读笔记
archive/                            全仓库唯一的归档处（过时材料，只存不取；见 archive/MANIFEST.md）
```

## 诚信规则（摘要）

Phase 5 预注册已冻结，锁定的参数、门槛与判定不得改动；新分析只能以签字前登记的修正案进入。研究一重分析与研究二的驱动脚本在登记文件签字前会被 `prototype/src/registration_guard.py` 拦下。完整规则见 `CLAUDE.md`。
