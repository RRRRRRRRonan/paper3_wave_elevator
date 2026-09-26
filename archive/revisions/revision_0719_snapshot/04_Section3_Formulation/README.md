# 04_Section3_Formulation（§3）更新清单

- 原文：`original_docx_formulation.md`（docx 中最完整的一章：Sets/Parameters/Decision variable/Assumptions/Φ/Elevator models/Objective/Constraints）。最新表述：`W4_section3_formulation.md`。
- 任务：
  1. 以 **W4 为准**逐小节对照合并：W4 是按最终术语和编号重写的全新 §3（两阶段决策架构、A1-A5、Φ=(C,I,T) 定义、{M1,M2,M3} 模型族、闭式顺序累加器声明、候选池协议、记号表）。docx 原文中与 W4 冲突的表述以 W4 为准。
  2. 保留 docx 原文中 W4 未覆盖而仍正确的细节（如具体参数记号），并检查与 W4 记号表一致。
  3. 必加句（W10 §2.4）：**"availability ties are broken by unit index"** 作为模型约定写入 §3.3。
  4. 闭式评估器段落：声明"非事件驱动"，并前引 §5 的 DES 交叉验证（保守评估器、支配与分解符号可迁移）。
  5. 电梯建模约定（loading 2s/unloading 2s、五阶段行程）与 invariants 列表保持与实现一致（对应 2026-06 的修改 9）。
  6. 图：`../figures/fig1_system_schematic.png` 放本章。
  7. **新增：参数 grounding 段落**（2026-07-19 评估结论，审稿唯一未设防侧翼）：每个物理常数引公开来源——电梯速度/容量引 KONE HD MonoSpace CSI 规格（0.51/0.76 m/s、23 m 行程 ≈ 4-8 层）与 Schindler 2600（群控至 4 梯）；5 相分解与 2 s 载卸引 Peters RTT 论文（单层飞行 4.8-7.0 s）；F/E 取值引 Quicktron 3 层案例、Prologis（3 层 3 货梯）、ATL（13 层）。措辞用 "parameters set within publicly documented ranges"，不写 "calibrated to a facility"。来源清单见 research_notes/real_data_assessment_2026-07-19.md 证据 2。

> 全局件中属于本章的修改已逐字抽取到本文件夹 `edits_from_global.md`（2026-07-19），施工时无需再翻 `00_global`；冲突仍以 W10 为准。
