# Revision package 2026-07-08 (Tier 1 + Tier 2)

按 2026-07-07 多智能体审稿意见执行的第一、二档修订：全部为**写作/编辑 + 已有数据的重分析**，
未运行任何新的批量仿真（仅有的例外：两次毫秒级的单波次 `simulate_wave` 反例验证调用，见 W3）。

**诚信链条**：`amendments/` 两份文书先写好并标注日期，之后才运行 `tier2_analysis/` 的分析；
所有锁定判定规则在看到结果前定死；预注册判定（H-D1 PARTIAL 57/72、H-D2 PASS、Policy-Partial）
一律不重判。两份 amendment 的 `author_signoff` 均为 **PENDING**，作者签字前其结论不得进正文。

---

## 今天产生的三个最重要事实

1. **A-R1 锁定规则触发**：容量主导（"capacity-bound > policy-bound"）在 oracle 口径
   `H_up/UB` 下不是方案稳定的（2×2 方案 2/6 配置、3×3 4/6、含 T 的 2×2×2 5/6）。
   按锁定规则，稿件所有 "~72%" 表述必须条件化：72% 是 **Φ-rule 口径、2×2 分区、72 子格网格**
   上的测量值，不是普适性质。相关句子的替换措辞见 W5/W7 文件头的 integration_note。
2. **W3 发现并验证了第二条支配失效渠道**（adverse repositioning，Example X.2：
   条件 (a)(b)(c) 全满足、零批处理事件，仍有 M1 = 103 > M2 = 68；已由模拟器数值验证）。
   现有命题 2 表述**被证伪**，必须加入条件 (d)；"所有违例都是 batch-overtaking" 一句按
   Amendment B-1 的锁定规则**退役**。这不影响 99.2% 的实证测量本身（测量不分机制）。
3. **OOS 检查是正面证据**：M_Φ 样本内高估仅 16.6%（低于 25% 重要性门槛），容量份额
   样本内 0.717 vs 样本外 0.705，结论不变。D1-d 的 BH-FDR 敏感性反而升到 62/72。

---

## 目录

### amendments/（先于分析写好、日期锁定）
| 文件 | 内容 |
|---|---|
| `AMEND-2026-07-08-A_reanalysis.md` | 重分析修正案（A-R1 分区敏感性、A-R2 统计强化、A-R3 OOS、A-R4 呈现层），含锁定判定规则与执行日志（A-R1 规则触发的事实记录） |
| `AMEND-2026-07-08-B_deferred_experiments.md` | 6 项延期实验的预注册（B-1 matched-assignment + 三通道违例分类器、B-2 小实例精确基准、B-3 已发表启发式 P8、B-4 出版尺度鲁棒性、B-5 DES 交叉验证、B-6 tercile + 候选池敏感性），门槛全部先行锁定，**未执行**，等机器空闲 |

### tier1_manuscript/（修改前/修改后对照稿，全部待作者审定）
| 文件 | 内容 | 最要紧的 open issue |
|---|---|---|
| `W1_theory_repackaging.md` | 14 处编辑：定理 1 降级为 Prop 3（定义性桥梁）、定理重编号方案（Thm 1 = minimax collapse 限 {M1,M2} + 完整短证明、Cor 3 = DRO certification、Cor 4 = K 模型推广）、D1-c 改标 pipeline 一致性检查、"theory does/does not claim" 段、全文查找替换表 | Prop 3 出现在 Prop 2 之前的编号瑕疵；两条 1-D 事实的引用出处需核对 |
| `W2_appendix_dro_and_hup.md` | 附录 B（DRO certification 完整数学：Lemma B.1/B.2 + Prop B.3 + 半径辩护 + 全局半径失效备注）；附录 C（覆盖分区 mixture-quantile 引理）；§4.1.1 "by construction" 修正；M4.2 假不等式替换 | Lemma B.1 等号情形、B.2 attainment 需人工核对；"24 cells FOSD" 的出处与尺度需作者确认 |
| `W3_prop2_induction.md` | X.4 归纳完整草稿（需新条件 (d) 与 E≥2 下的强化条件 (c*)）；Example X.1（26 vs 24，验证✓）与 X.2（103 vs 68，验证✓，**证伪现有命题 2**）；+0 fallback 文本 | 归纳数学需作者逐步验证；决策：发 (a)(b)(c*)(d) 一般定理还是 E=1 命题 + Conjecture 1 |
| `W4_section3_formulation.md` | 全新 §3（~1650 词）：问题陈述、Φ 精确定义（C = vertical spread）、M1/M2/M3、closed-form sequential time-accumulator 正确描述、假设 A1-A5、候选池协议、完整符号表 | ρ_c 定义需对定理 2 全文核对；corner 记号 q vs c 与容量 c 冲突待统一 |
| `W5_section6_discussion.md` | 全新 §6（~1400 词）：容量-策略诊断、config-7 工作示例、8 条 limitations（引用 amendments）、结论与 future work | 文件头 integration_note：72% 句必须按 A-R1 结果条件化；U_c 3.4% vs 3.5% 口径需统一 |
| `W6_small_edits.md` | 13 处小修：event-driven 误述、"balanced" 网格 → 混叠披露、摘要 DRO/99.2% 范围限定（中英双语）、"by construction" 一句、"vertical concentration" 全量清点处置表 | Word 母稿（docx/pdf）无法 grep，需手工搜同样错误 |
| `W7_relatedworks_contributions.md` | Wang, Tao & Yang (2025, C&IE) 插入与差异化、tier-confinement 句软化（中英）、新 BibTeX（DOI 待确认）、~350 词出版尺度贡献段（替换 §11.2 旧段与 Introduction 现段） | 文件头 integration_note：C3 的 72% 句加限定；Wang 2025 书目信息需到 Elsevier 核实；Introduction 中文段未同步 |

### tier2_analysis/
- `scripts/ar1_partition_sensitivity.py` → `outputs/ar1_partition_sensitivity.json`
- `scripts/ar2_stats_hardening.py` → `outputs/ar2_stats_hardening.json`
- `scripts/ar3_oos_corner_selection.py` → `outputs/ar3_oos_corner_selection.json`
- `scripts/ar4_build_tables.py` → `../tables/T1..T6`（从库存 JSON + 上述输出渲染）

复现：任意目录 `python <script>.py`（脚本内用绝对路径解析仓库位置）；种子 20260708。

### tables/（可直接进稿的 markdown 表）
| 表 | 内容 |
|---|---|
| `T1_experiment_design.md` | 18 配置因子水平 + 定义关系与**混叠披露** + 各 Block 仿真数对账（72,000+16,800+18,000 = 106,800） |
| `T2_main_results_18.md` | 主文 18 行：绝对 m_0 区间 + GAP/H_up/M_Φ + 容量份额 + resolved 计数 |
| `T2b_appendix_72subcells.md` | 附录 72 行全表（绝对 m_0、CI、resolved） |
| `T3_blockC_D2.md` | 24 (config, corner) 支配频率 + Wilson CI + FOSD + U_c(0.05)；池化 99.21% [98.92%, 99.42%] |
| `T4_policy_contest.md` | 完整 8 策略对比（补全 P2/P3/P4）：grand mean、含平局的胜负矩阵、关键对比 Wilson CI、P2 正面回应段 |
| `T5_partition_sensitivity.md` | A-R1 结果 + 锁定规则触发结论（headline 条件化措辞） |
| `T6_stats_and_oos.md` | A-R2/A-R3 汇总（BH 62/72、ρ CI、OOS 收缩） |

### figures/（300 dpi PNG + 生成脚本 `make_figures.py`，Okabe-Ito 色盲安全色系）
| 图 | 内容 |
|---|---|
| `fig1_system_schematic.png` | 双面板：物理系统（多层楼 + 楼层受限 AMR + 共享电梯 + 5 阶段行程）+ 两阶段决策架构 |
| `fig2_hedge_rule_schematic_v2.png` | Hedge 示意图重制：wave-release 措辞（替换违规的 "dispatch"）、作用域 {M1,M2} + M3 走 ε 界、无 em-dash |
| `fig3_gap_by_demand.png` | GAP×72 子格按 demand 分面（预注册呈现方式），实心/空心 = resolved/未 resolved，标题含混叠免责 |
| `fig4_p5_vs_p6_signed_diff.png` | P5−P6 逐格有符号差值图（替换原不可读散点图），蓝/红/灰 = P5 优/P6 优/平局 |
| `fig5_decomposition_stacked.png` | 18 配置 H_up/M_Φ 堆叠图（视觉承载容量-策略分解，标注口径条件） |
| `fig6_policy_relative_distributions.png` | 8 策略相对 P0 的 12 格分布（箱线 + 散点，P5/P7 高亮） |
| `fig7_decision_workflow.png` | practitioner 决策流程图（config-7 工作数字，两工具分工） |

---

## 作者待办（按优先级）

1. **验证 W3 的数学**：X.2 已数值验证成立，命题 2 必须加条件 (d)。决定走一般定理（需逐步验证归纳）还是 +0 fallback。这是全包里唯一"改变论文声明"的项。
2. **签字两份 amendment**（signoff PENDING → signed），A-R1 的 headline 条件化措辞随之进正文（W5/W7 文件头有现成替换句）。
3. 按 W1 的查找替换表统一定理编号；核对 W2 标注的引用出处与 "24 cells" 尺度。
4. 核对 Wang, Tao & Yang (2025) 书目信息（Elsevier PII S0360835225007053）；精读 Boysen & de Koster (2025) 关掉 stub（新增文献均不在本包范围内）。
5. 手工搜索 Word 母稿中 "event-driven" / "balanced" / 未限定 DRO 句（W6 open issue 1）。
6. 机器空闲后按 Amendment B 顺序执行 B-1 → B-5（合计约一次 Phase 5 的计算量）。

生成记录：审稿 workflow wf_9413dd5f-659（2026-07-07）；写作 workflow wf_0ec4ba43-676 +
整合与全部分析（2026-07-08）。审稿明细存于会话 scratchpad（panel_*.json / readers_*.json）。
