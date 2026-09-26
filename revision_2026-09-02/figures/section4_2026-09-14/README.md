# Section 4 figures / 方法章节图组

本图组依据当前 Section 4 MD 绘制，沿用 Fig. 1 的白底、低饱和蓝灰—青绿—琥珀配色、深色轮廓和无衬线标签。图号暂接续 Fig. 1，完整稿合并时统一核对。图片已嵌入 [SECTION_4_METHODOLOGY.md](<F:/Paper 3/revision_2026-09-02/SECTION_4_METHODOLOGY.md>)，并配有英文图注与逐段中文翻译。Word 文件未改动。

## Figures and placement

| Figure | Function | Placement |
| --- | --- | --- |
| Fig. 2 | 主选择流程与支持模块 | Section 4 总述之后 |
| Fig. 3 | 类别诊断分解与覆盖分区细化 | 4.2 末尾 |
| Fig. 4 | 评估器排序条件及两种反例 | 4.3 末尾 |
| Fig. 5 | 简化、稳定性与独立扩展 | 4.4 末尾 |

## Fig. 2 — Methodology overview

![Robust class selection and supporting analysis](<F:/Paper 3/revision_2026-09-02/figures/section4_2026-09-14/fig2_methodology_overview_v1.png>)

主流程依次进行配对评价、逐模型类别中位数计算、最坏模型得分比较和类内抽样释放。底部支持模块按输入来源连接，位置不表示章节执行顺序。M3 保持为独立评价。

## Fig. 3 — Class-relative diagnosis

![Signed diagnostic decomposition and nested covering partitions](<F:/Paper 3/revision_2026-09-02/figures/section4_2026-09-14/fig3_class_diagnosis_v1.png>)

图中将候选池参照置于类别区间之外的独立框中，避免暗示类别中位数必然夹住候选池中位数。覆盖分区具有独立分面，不与角点类别族混同。

## Fig. 4 — Ordering mechanisms

![Conditional evaluator ordering with shared-trip and repositioning examples](<F:/Paper 3/revision_2026-09-02/figures/section4_2026-09-14/fig4_ordering_mechanisms_v1.png>)

充分条件采用单向蕴含。两个反例保留正文中的精确事件时刻，分别得到 26 对 24 秒和 103 对 68 秒。面板 (c) 明示水平间距为示意布局，不作为按比例读取持续时间的坐标图。

## Fig. 5 — Robust decision properties

![Median minimax reduction, stability certificate, and complementary mean analysis](<F:/Paper 3/revision_2026-09-02/figures/section4_2026-09-14/fig5_robust_selection_properties_v1.png>)

稳定性充分条件不满足时，流程回到完整鲁棒得分比较。均值的 Wasserstein 解释与中位数选择分开；图注明确给出其随机排序方向，并定义图内的简写。

## Resolution and production notes

| File | Pixels | Effective dpi at 170 mm width | Width at 300 dpi |
| --- | --- | ---: | ---: |
| fig2_methodology_overview_v1.png | 1672 × 941 | 249.8 | 141.6 mm |
| fig3_class_diagnosis_v1.png | 1983 × 793 | 296.3 | 167.9 mm |
| fig4_ordering_mechanisms_v1.png | 1672 × 941 | 249.8 | 141.6 mm |
| fig5_robust_selection_properties_v1.png | 1672 × 941 | 249.8 | 141.6 mm |

These are raster PNG manuscript illustrations, not editable vector artwork. The image tool returned the dimensions above despite larger dimensions requested in the prompts. Merely changing DPI metadata or upscaling would not add original detail. At the final manuscript width, small mathematical subscripts and panel notes require a print-size check. A vector production pass or higher-resolution source would be appropriate if the submission requires 300 dpi or more at full 170 mm width. No journal-specific submission compliance is claimed here.

## Verification and change record

- All four selected images were inspected visually for mathematical labels, arrows, and panel correspondence.
- Figures 2 and 3 received an independent image-to-caption check; Fig. 5 received an independent mathematical-logic check.
- The two counterexample makespans were recomputed from the stated service times and matched 26/24 and 103/68 seconds.
- All four MD image paths exist. Equation tags remain 33–58, with no additions, removals, or renumbering.
- The old processing-sequence notation was synchronized to the current candidate-specific π^k in the paired condition, makespan comparison, explanation, and example setup. No theorem or decision rule was changed.
- Original Word documents, Fig. 1, production simulation code, and experimental results were not modified.
- Colors are supplemented by text, panel boundaries, and line styles. Specified dark-text/pale-fill contrast ratios exceed 10:1. This is a palette-specification calculation, not a pixel-level accessibility certification; no automated colorblind or grayscale PASS is claimed.

The editable conceptual structures and palette are in [FIGURE_DESIGN.md](<F:/Paper 3/revision_2026-09-02/figures/section4_2026-09-14/FIGURE_DESIGN.md>). The exact initial prompts and correction prompts used with the built-in image tool are in [GENERATION_PROMPTS.md](<F:/Paper 3/revision_2026-09-02/figures/section4_2026-09-14/GENERATION_PROMPTS.md>).
