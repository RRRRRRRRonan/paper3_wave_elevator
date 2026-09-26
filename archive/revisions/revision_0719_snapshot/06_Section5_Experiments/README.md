# 06_Section5_Experiments（§5）更新清单

- docx 中无本章原文，为新写入。最新稿：`section5_draft_v0_1.md` + `chain_dominance_empirical_v1.0.md`（§5.3 模块）。表：`tables/T1-T6`。
- W10 §4 的改写清单：
  1. **§5.1** 设计与诚信：预注册声明、别名混淆披露（F 与 |A|、demand 混淆，无 F 主效应）；**复现性声明**：id(e) 平局 bug、暴露度 0.27%（存档 Block C M2 值）/ 5.11%（请求面临后果性平局）、B-14 index-stable 修复、四个 D2 门槛判定不变（0.9925 vs 0.9921）、发布修复版模拟器；**AI 研究过程披露**（对抗验证 agent、分析脚本；Elsevier 要求写入方法节）。
  2. **§5.2** Bound-and-Gap 验证：主结果 T2/T2b；**分辨率曲线**（Theorem R 验证 48/48，fig8）；**测量误差**（AMEND-F：SEM 0.136、判定 15/18 一致、波次预算 fig9）；份额一律带分辨率与口径限定语。**新增（2026-07-31）：首次报数处加换算锚句**——"GAP itself averages about 6% of baseline makespan, so the ceiling and the slack correspond to roughly 4.3 and 1.7 percentage points of makespan respectively."（防"72% 的分母是工期"误读；数字来源 GAP=0.060、H_up=0.043、M_Φ=0.017，v0_5 Block A）。
  3. **§5.3 重写**：自由口径 99.2%（实践）与强制口径 99.67%（定理对齐）并排；通道表 18 超越 + 2 逆向重定位 + 0 其他；基率 12.67% / 99.43%，读法"条件远非必要；即使失效处违例也罕见"；不写排他性句子。
  4. **§5.4**：Table 4 全量（含 **P8** 行：均值 288.4，胜 P0-P4 12/12、P5 10/12、P6 11/12，负 P7 0/12，解读 = savings 启发式靠喂饱共占通道取胜，反证核心机制）；**P9** exhibit（SPO+ 中位回收 R=1.00，按锁定阶梯写 "partially recoverable"，披露零预算剔除）；**枚举锚点**（pool optimum 38，P7 +47.4%，P5 +147%，config 1/size 8，措辞用 "pool optimum"）。
  5. **§5.5** 消融与稳健性：分区敏感性（A-R1 触发 → 结论条件化）、OOS（M_Φ 收缩 16.6%）、c 扫掠、M3。
  6. **新增 DES 小节**（或附录）：支配在并发下 98-100% 成立；闭式保守 25-37%；逐波次排名 ρ 0.45-0.68 → 波次级选择限定于闭式模型类；fig10。
- 图：fig3、fig4（平局灰色）、fig5、fig6、fig9、fig10。

> 全局件中属于本章的修改已逐字抽取到本文件夹 `edits_from_global.md`（2026-07-19），施工时无需再翻 `00_global`；冲突仍以 W10 为准。
