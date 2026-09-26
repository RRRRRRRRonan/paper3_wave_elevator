---
title: "达标评估与修改方案：方案 A（不投 EJOR，目标 IJPR，底线 C&IE）"
date: 2026-09-26
basis: "2026-09-25 多代理评估（工作流 wf_6e7d903d-05b：4 个取证代理、4 个维度评审、1 个模拟审稿人、1 个事实核查代理；114 条引用事实中 110 条与原始文件一致、3 条已更正、1 条无法核实）。原始证据来源：prototype/results/v0_5_phase5_*.json、revision_2026-07-08/tier2_analysis/outputs/*.json、revision_2026-09-02/MASTER_REVISION_BY_SECTION.md、paper_draft/phase5_scaleup_preregistration.md、paper_draft/manuscript/*、Problem formulation.docx（2026-09-25）、Methodology.docx（2026-09-17）、papers/ 及联网检索。"
scope: "第一部分是评估记录；第二部分是按创新性、贡献度、故事完整度、实验设计复杂性四个维度组织的修改方案。方案分两档：C&IE 基线包（必做）和 IJPR 增项包。"
numbering: "定理编号以 revision_2026-09-02/SECTION_4_METHODOLOGY.md 为准：Proposition 3 = 条件性样本路径排序（M1 与 M2），Theorem 2 = 条件性 minimax 归约（Hedge Rule）。主控文件与旧稿仍用 Prop. 2 称呼排序结果，引用时请注意。"
scale: "本文件所有数字均为发表规模（Phase 5，18 配置），除非标注 [B-11 小实例] 或 [原型规模]。证据标签按主控 §0.3：[PR-C] [PR-E] [AM1] [AM2] [RA] [NS] [EXP] [QA]。"
---

# 达标评估与修改方案（2026-09-26）

**"方案 A"的定义（本文件采用作者 2026-09-25 的口径）：** 不投 EJOR，改投次一级的期刊。首选 IJPR（International Journal of Production Research），底线 C&IE（Computers & Industrial Engineering）。研究笔记 `contribution_review_continuation_2026-09-02.md` §5.3 里另有一个也叫"路线 A"的方案（保留"容量 vs 策略"结论，需新做匹配干预实验），与本文件无关，只在第一部分 §6 说明它需要什么。

---

# 第一部分 评估

## 0. 评估方法与可信度

- 四个取证代理分别整理：贡献定位与故事链、实验结果、实验设计与理论、文献前沿与期刊标准。合计 175 条证据，每条带文件行号或 JSON 键路径。
- 四个评审代理分别对一个维度给出 steelman（最强的支持理由）、attack（最强的反对理由）、C&IE 与 IJPR 两档判定、1 到 5 分评分（3 分为及格线）、以及不违反预注册的补救措施。
- 一个"审稿人 2"代理模拟 C&IE 初审和全文评审。
- 一个事实核查代理逐条核对评审引用的 114 条事实。结果：110 条与原始文件一致；3 条更正（见 §5）；1 条无法核实（Kim et al. 2025 全文 403）。
- 所有代理只读，未修改任何文件。

## 1. 总判定

| 维度 | 对 C&IE | 对 IJPR | 评分（3 = 及格线） | 一句话 |
|---|---|---|---|---|
| 创新性 | 边缘 | 不足 | 2.5 | 问题交叉点没有找到重复；方法上只有 Proposition 3 有深度；三篇直接先行工作未引 |
| 贡献度 | 边缘 | 不足 | 2.5 | 去掉已废止的容量结论后，只剩一个机制结果（仍是证明梗概）和一份诚实的边界研究；"两个可用工具"的卖点被自家预注册证据否定 |
| 故事完整度 | **不足** | 不足 | 2 | 只有 §3 按现行口径写好；Word 版 §4 缺 Hedge Rule；§5、§6、附录 A 没有符合口径的文本；摘要和引言仍讲已废止的故事 |
| 实验设计复杂性 | 边缘 | 不足 | 3 | 治理与验证层高于 C&IE 常态；核心设计比"106,800 次仿真"单薄：18 个混杂配置，关键块只覆盖 6 个，闭式评估器排序保真不达标，伪重复未处理 |

**模拟审稿（C&IE）：** 初审退稿风险中等（若摘要、引言不改则高）；评审后最可能的结果是"拒稿后重投"。完成第二部分的 C&IE 基线包后，可进入大修。

**对两档期刊的总体判断：**
- C&IE：可以冲，但必须先完成基线包；论文形态是"界定清楚的基准问题 + 机制定理 + 诚实的有效性边界"的洞察型论文。
- IJPR：目前四个维度都不足。IJPR 的范围明确要求"convincing scientific results with clear, real-life applications as well as fundamental techniques"（见 §2）。本文没有真实应用锚点、没有有竞争力的决策方法、理论只有一个未完成的命题。要达到 IJPR，需要第二部分的增项包，其中两项（决策方法、文献校准案例）结果未知。

## 2. 两个期刊的标准与同类论文形态

**C&IE 范围（Elsevier 官方文字，经检索确认）：** 发表"the development of new computerized methodologies for solving industrial engineering problems, as well as the applications of those methodologies"；应用类论文"are welcome, as long as they satisfy the criteria of originality in the choice of the problem and the tools utilized to solve it, generality of the approach for applicability to other problems, and significance of the results produced"。
- 同类论文形态（垂直运输、多层仓库方向）：多为"MIP 模型 + 精确算法或元启发式 + 合成算例"，例如 Wang et al. 2025（C&IE 210:111559，异构升降机联合调度，MIP + 逻辑 Benders + ALNS&TS）、Ren et al. 2025（C&IE 204:111095，层间四向穿梭车与升降机集成调度）。
- 仿真型洞察论文也有先例（Winkelhaus et al. 2022，C&IE 167:107981；2026 年一篇 DES + 深度学习的 RMFS 车队规模论文）。
- 纯合成算例在 C&IE 是常态（项目自己的评估 `research_notes/real_data_assessment_2026-07-19.md:5,10,14`）。

**IJPR 范围（Taylor & Francis 官方文字，经检索确认）：** "the journal publishes convincing scientific results with clear, real-life applications as well as fundamental techniques developed in computer, decision and mathematical sciences to solve complex decision problems that arise in design, measurement, management and control of production and logistics systems"。
- 同类论文形态：IJPR 63(1) 2025（多层穿梭车 AMR 订单排序、料箱调度与路径：MILP + 两阶段 VNS，代码公开）；IJPR 64(6) 2026（混合多深位 RMFS 调度）；IJPR 64(5) 2026（波次拣选下的货架重定位）；IJPR 64(14) 2026（料箱配送）；以及 SBS/RS 穿梭车与升降机一脉（53(19) 2015；57(4) 2019；58(16) 2020）。全部是优化模型或解析模型论文，没有"只做仿真诊断"的先例。

**由此得出的两档标准：**

| 要素 | C&IE 及格 | IJPR 及格 |
|---|---|---|
| 问题 | 选题有原创性，界定清楚 | 同左，且能对应到明确的生产或物流决策 |
| 方法 | 可以是诊断工具或分析框架，但要有一个非平凡的结果 | 需要一个能用的决策方法，并与合理基线比较 |
| 理论 | 一个完整证明的非平凡结果即可 | 同左，最好能解释经验现象 |
| 实验 | 合成算例可以；预注册是加分 | 合成算例可以，但要有参数依据或校准案例；覆盖要完整 |
| 应用 | "welcome"，非必需 | "clear, real-life applications"是明文要求 |

## 3. 逐维度评估

### 3.1 创新性：边缘（C&IE）/ 不足（IJPR）

**支持的证据**

| 事实 | 出处 |
|---|---|
| 界定后的问题交叉点在 2021–2026 文献里没有找到重复：单波次组成决策 + 楼层受限的柔性 AMR 车队 + 共享楼宇货梯争用 + 电梯模型不确定 | sources/frontier_novelty_audit_2026-09-02.md:62-66 |
| 最接近的工作都把任务集当作给定：Chakravarty 2025（SAT 电梯调度，任务外生，≤35 个体）；He et al. 2026（MAPF with Elevators，起终点预先指定）；Wang 2025、Ren 2025（C&IE，检索集给定）；Zhen 2023（AOR）。Tadumadze 2023 让各层隔离。Han 2025、Kim 2025 对配送任务分组，但电梯只算固定等待成本，无多机器人争用 | papers/reading_log_chakravarty2025.md:16-22；https://arxiv.org/html/2602.20512v2；https://pmc.ncbi.nlm.nih.gov/articles/PMC11946681；https://doi.org/10.3390/electronics14050982 |
| 建模上把 M1、M2 当作两个竞争性假说而非同一族的参数化，并把这种模型不确定带进战术决策 | Problem formulation.docx 3.4.2（"two hypotheses on how elevator capacity acts"） |
| Proposition 3 是非循环的实质结果：对任意 E ≥ 1、c ≥ 1，在条件 (a)–(d) 下给出 M1 ≤ M2 的逐样本路径排序；两个精确反例分离出仅有的两种反转机制（共享行程超车 26 对 24 秒；不利空驶 103 对 68 秒），并在生产模拟器上复现 | SECTION_4_METHODOLOGY.md:229-300；plan_section3_section4_v0_2.md:21 |
| 结论方向与电梯工程"拼梯缩短往返时间"的传统直觉相反，是可迁移的建模教训 | related_works_v1.1.md:124-130；blockC.json#H_D2.perwave_avg = 0.99208 [PR-C] |
| 在对齐指派的前提下，两种失效通道是完备的：115 万小实例普查在 (c)+(d) 下 0 次违例 [B-11 小实例，NS]；对齐指派后 20 次违例全部落入两个通道（18 超车、2 空驶）[NS] | b11_conj1_census.json；b1_matched_assignment.json#violation_channels |
| 一个少见的方法论洞察：粗分区的价值分解依赖测量口径（72% 对 47%），重测不可靠（ICC 0.009 / −0.029） | amendF_test_retest.json [NS]；ar1_partition_sensitivity.json [RA] |

**削弱的证据**

| 事实 | 出处 |
|---|---|
| 除 Proposition 3 外，理论都是恒等式或一行推导：Prop 1（差距分解）和 Prop 2（SPO 等价）证明各一行；Theorem 2（Hedge Rule）是"a ≤ b 时 max{a, b} = b"，证明两句；Corollary 3 是"一阶随机占优下 W1 等于均值差" | SECTION_4_METHODOLOGY.md:122-170, 343-353, 461-478 |
| Hedge Rule 在结构上就是 Fan, Hong & Zhang (2020, Management Science 66(1):190-208) "Distributionally Robust Selection of the Best" 的两模型特例；项目未引任何 ranking-and-selection 文献，而 related works 声称模型类不确定"structurally different" | 全库检索 0 命中；related_works_v1.1.md:157-162 |
| 三篇直接先行工作未引：Gallien & Weber (2010, MSOM 12(4):642-662)"To Wave or Not to Wave?"（面对共享下游瓶颈的波次释放，用真实数据）；RAWSim-O (2017)（已指出电梯是多层 RMFS 瓶颈，需要任务分配来缓解）；Fan-Hong-Zhang 2020 | 项目自写文件 0 命中（Gallien & Weber 仅出现在 papers/50 years of warehousing research.pdf 的参考文献里） |
| 主控要求的 9 篇前沿邻居一篇都不在 bib 里：He 2026、Xu 2026 WareRover、Kim 2025、Ren 2025、Xue & Wang 2026、Bertsimas & Kallus 2020、Jiang 2026、Kuhn 2025、Fu 2024；也没有与 coefficient of prescriptiveness、VSS、EVPI 的比较 | references_related_works.bib（52 条，无上述任何键）；MASTER:238-261 |
| "上下层耦合"本身已不新：WareRover（Xu et al. 2026）、SOAR（Tang et al. 2026，Geekplus 实机部署） | https://arxiv.org/abs/2602.13999；https://arxiv.org/abs/2605.03842 |
| Proposition 3 仍标"Proof sketch"，附录 A 未组装；其联合充分条件只覆盖不到 1% 的波次（条件 (d) 仅在约 0.6% 的波次成立，(b) 在自由指派下 57.8%），所以 99.2% 的排序频率不是定理解释的 | SECTION_4_METHODOLOGY.md:276；b1_matched_assignment.json#base_rate_all_waves.repos_frac = 0.9943, #hyp_b_free_frac = 0.578 [NS] |
| 排序在很大程度上是结构性的：逐波次 (M2 − M1)/M1 的中位数为 41%，M1 表现为乐观的松弛，所以高频率在审稿人看来是意料之中 | 对 raw/mvs_v0_5_phase5_blockC_tiebreakfix.csv 的只读重算 [EXP，未登记] |
| 决策层面的新意薄：Hedge 只在 1/6 个配置改变决策；证书 0/6 有信息量；4/6 个配置的类别差距 ≤ 1.04% | amendC4_uc_tightness.json [NS]；blockC.json#RA_median_hedge_sensitivity [RA] |
| 策略层面没有新方法：Φ 角类规则 P5（303.6）不如只按订单数选的 P2（299.2）；被无仿真的节约法 P8 在 10/12 格击败；对局部搜索 P7 0/12 | blockB.json [PR-C]；b2_b3_benchmarks.json#B3 [NS] |
| 现稿的优先权表述会被上述文献直接反驳："has never been treated"、"studied only in isolation"、"integrates the four-way interaction ... into a single decision problem" | abstract_v1.1_250w.md:49；introduction_v1.1.md:189；related_works_v1.1.md:164-167 |

**结论：** 创新性真实但窄。C&IE 认可"选题原创性"，所以作为界定清楚的交叉点问题 + 一个机制定理，可达边缘及格；IJPR 期望方法层面的新东西，现在没有。

### 3.2 贡献度：边缘（C&IE）/ 不足（IJPR）

**支持的证据**

| 事实 | 出处 |
|---|---|
| C1 至 C3 的现行口径内部自洽，且已按证据诚实定价：C1 界定清楚的基准问题；C2 条件性排序机制 + 稳健类别选择（Bound-and-Gap、SPO、细化、DRO 降为支撑性质）；C3 经验边界与测量敏感性 | MASTER:127-131 |
| H-D2 是唯一稳固的预注册支柱：逐波次 M2 ≥ M1 平均 99.21%，最差格 96%，24/24 FOSD，24/24 U_c，6/6 collapse，判定 PASS；修复破平后 99.25%、判定不变；c = 2..5 均 ≥ 99.75%；DES 下符号保留（0.98–1.00） | blockC.json#H_D2 [PR-C]；blockC_tiebreakfix.json [QA]；supp.json#Supp2 [AM2]；b5_des_crossvalidation.json#des_pooled_dominance [NS] |
| Hedge 在 5/6 个配置代价为 0 | amendC4_uc_tightness.json#per_config[*].price_hedge [NS] |
| 战术杠杆存在且不被更好的调度吸收：P5 在 10/12 格胜过随机；Block A 中 Φ 类平均改善 3.7%；事后重算 Supp-1 数据，Φ 角类相对随机的优势在 FIFO 下 7.47%、在聚类调度下 7.12%（各 10/12 格为正；按总平均算为 4.86% / 4.25%） | blockB.json [PR-C]；ablation.json#A1_feature = 0.0372 [AM1]；supp.json#Supp1.per_cell 的重算 [EXP，未登记] |
| 负结果和部分通过的结果都如实保留，没有调参 | MASTER:32-40；prereg:208-218 |

**削弱的证据**

| 事实 | 出处 |
|---|---|
| 计划 v0.2 的卖点"两个简单可用的诊断工具"被锁定证据否定：D1-d 57/72 未达 58 的门槛，预注册第 213 行规定此时必须写"Bound-and-Gap is a prototype-regime diagnostic"并弱化实用性表述 | blockA.json#gates [PR-C]；prereg:213 |
| §4 的 markdown 和 Word 版都没有出现"Hedge"或"Bound-and-Gap"这两个词（以 robust class selection、q_H 等名称出现） | SECTION_4_METHODOLOGY.md 检索 0 命中 |
| 唯一的实质定理未完成，且解释机制而非频率 | SECTION_4_METHODOLOGY.md:276；MASTER:34, 417 |
| Hedge 在唯一起作用的配置 11 里，按 M1 计的代价是 2.63%，而 M1 名义最优角类只有 0.17%；证书在那里无效，且 6/6 无信息量 | amendC4_uc_tightness.json#per_config[5] [NS] |
| 方法输出的类别选择脆弱：中位数口径下与第二名的差距 2.29% / 5.59% / 0.96% / 1.04% / 0.84% / 0.14%；中位数与均值口径在配置 5 不一致；候选聚类 bootstrap 的选择稳定性在 5/6 个配置为 0.43–0.78 | blockC.json#RA_median_hedge_sensitivity [RA]；对 tiebreakfix.csv 的重算 [EXP，未登记] |
| 类别排序不能迁移到并发评估器：DES Spearman ρ 最低 0.449，门槛 0.9，faithful_ordinal_proxy = false | b5_des_crossvalidation.json#gates [NS] |
| 战术杠杆小于运营杠杆：聚类调度平均改善 10.2%（12/12 格 > 1%），高于 Block A 的平均 GAP 6.0%，也高于同 12 格上 P5 的 7.2% | supp.json#Supp1 [AM2]；blockA.json#mean_GAP [PR-C] |
| 现稿的贡献陈述仍写着已废止的结论："(C3) Empirical capacity-versus-policy diagnosis ... the capacity side dominates, with about 72%"，"when the lever is instead more capacity" | introduction_v1.1.md:221-228, 250-251 |

**结论：** 剥离容量结论后，贡献 = 一个机制结果 + 一个几乎不改变决策的稳健规则 + 一份边界研究。C&IE 可作为洞察论文勉强及格，前提是不再卖"两个工具"；IJPR 需要一个能用的决策方法，现在没有。

### 3.3 故事完整度：不足（两档）

**设计层面是自洽的：** 主控给出一条主线（C1–C3、RQ1–RQ3、逐节完成门槛，MASTER:127-137, 425-564, 657-673）；每个环节都有来源；负结果在新的 C3（"什么时候可以信任这个诊断"）里讲得通；§5 需要的每个数字都已在 JSON 里，缺的是写作而不是新实验。

**但稿件层面这条主线不存在：**

| 部分 | 现状 | 出处 |
|---|---|---|
| 摘要 | v1.8 一段里至少 7 处已废止表述："primary bottleneck"、"largely fixes makespan"、"never been treated"、"structural ceiling ... cannot recover"、"capacity-versus-policy verdict is seed-stable"、"when capacity is the lever"；没有研究问题；缺主控要求的 DES / 测量边界句 | abstract_v1.1_250w.md:49；MASTER:170-181 |
| §1 引言 | C3 标题为"Empirical capacity-versus-policy diagnosis"，写"the capacity side dominates, with about 72%"；"two-stage scheduler"；"studied only in isolation"；承诺"Section 4 develops the two tools"，而 §4 并没有；用旧定理编号；无 RQ | introduction_v1.1.md:120-167, 185, 189, 221-254 |
| §2 相关工作 | 缺主控要求的全部 9 篇前沿文献；缺 prescriptiveness / VSS / EVPI 比较；保留"integrates the four-way interaction"；无定位对照表 | related_works_v1.1.md:122, 139-142, 157-167；MASTER:238-261 |
| §3 | 接近定稿，32 个公式与代码逐项一致；但没有 RQ，且有 10 处指向尚不存在的 §5 | pf_0925_recheck_placeholders.md（"Section 5"10 次，"RQ"0 次） |
| §4 | markdown 完整到式 (58)；Word 版停在 4.3.2，缺式 (47)、Fig. 4 和整个 4.4（Theorem 2、Corollary 2–4、Fig. 5）；Proposition 3 仍为证明梗概，附录 A 未组装 | plan_section3_section4_v0_2.md:20；SECTION_4_METHODOLOGY.md:276 |
| §5 | 只有 2026 年 5 月的草稿，至少违反 10 条口径："event-driven simulator"、"72/72 confirming the two theorems"、"71.7% capacity-side reading"、"every violating wave is a batch-overtaking event"（已废止：18 超车 + 2 空驶）、"81% residual outside any corner rule's reach"（被 P9 反驳）、把负的 H_up 说成有限样本假象（与 §4 矛盾） | section5_draft_v0_1.md:24, 63-76, 152-158, 222-229；MASTER:369 |
| §6 | 只有 W5：§6.1 标题"a capacity-versus-policy diagnosis"，结尾"direct the remaining effort at the capacity side"，把已执行且失败的 B-5 列为未来工作 | W5_section6_discussion.md:56, 122-126 |
| 附录 A | 未组装 | MASTER:417, 572 |
| 项目指引文件 | CLAUDE.md:76 与 TERMINOLOGY.md:39, 48, 52 仍写"capacity-bound > policy-bound"、"~72% (capacity-side dominant)"、"T = temporal clustering"，后续写作有被重新污染的风险 | 直接核对 |

**卖点三处不一致：** 计划 v0.2 卖"两个可用工具"；主控把 Bound-and-Gap 降为支撑性质；预注册的 H-D1 结果规则要求称之为"prototype-regime diagnostic"。

**即使重写后，最弱的一环仍是"证据到管理含义"：** 决策对象是闭式评估器下的类别排序，通常是接近平局（4/6 个配置差距 ≤ 1.04%），很少改变决策（1/6），排序不能迁移到 DES，而且被论文固定不动的运营层杠杆（10.2%）盖过。确认性结果的正负比例是 2 项 PASS（H-D2、Supp-2）对 7 项 PARTIAL 或 FAIL（H-D1、H-Policy、H-D3 model-sensitive、F、C-4、B-5、Supp-1）。若不给每个边界结果配一条可执行的报告规则，C3 会读成失败清单。

**结论：** 目前 2 分。评审估计：仅靠写作和带标签的重新呈现（不做新的确认性实验），C&IE 可升到约 3.5 分；IJPR 仍偏弱。

### 3.4 实验设计复杂性：边缘（C&IE）/ 不足（IJPR）

**高于 C&IE 常态的部分**

| 事实 | 出处 |
|---|---|
| 锁定的预注册含数值门槛（如 D1-d ≥ 58/72），不利结果照实报告：H-D1 PARTIAL、H-Policy Partial、B-5 排序门槛 FAIL、C-4 信息量 0/6 FAIL、F 信度 FAIL | prereg:150-157；blockA.json#gates；MASTER:32-40 |
| 三块设计有配对核心：Block A 分解（18 × 2 模型 × 2 规模 × 5 臂 × 200 = 72,000）；Block B 共享 3000 候选池上的 7 策略竞赛（16,800）；Block C 同一批波次在 M1/M2/M3 下配对评价（6,000 × 3 = 18,000） | phase5_config.py:31-44；experiments_phase5.py:274-292 |
| 验证层：事件驱动 DES 交叉验证；8 次重复的重测信度（18 配置）；样本外角类选择；115 万小实例认证普查；两个精确反例；破平修复后的 Block C 再生（判定不变） | b5、amendF、ar3、b11、b14 各 JSON |
| 基线梯度从朴素到强：P0–P4 简单规则、P6 决策树、P7 局部搜索、P8 节约法、P9 SPO+，外加池内最优锚点 | wave_policies.py:117-265；b2_b3_benchmarks.json；amendC1_p9_spoplus.json |
| 补充因子：容量扫描 c = 2..5（PASS）、运营调度杠杆（Supp-1） | supp.json [AM2] |
| 统计加固：Wilson 区间、336 个 Mann-Whitney 检验的 BH 校正、格中位数 Wilcoxon | ar2_stats_hardening.json [RA] |

**比"106,800 次仿真"单薄的部分**

| 事实 | 出处 |
|---|---|
| 规模便宜且混杂：全部是闭式串行计算，预注册自估"minutes, not hours"；3000 候选 × 2 模型 0.8 秒。18 个配置是 1/3 部分因子，demand = (F + \|A\|) mod 3，F、\|A\|、需求模式互相混杂，任何主效应都不可识别 | prereg:412；plan v0.2:24；phase5_config.py:52-69 |
| 承担贡献的块最薄：Block B、C 和两个补充实验都只用配置 {1,3,5,7,9,11}，全是 E = 2、F ∈ {3,5}，没有 F = 8，没有单电梯；Block C 只用 n = 16。H-Policy 建立在 12 格上，H-D2 与 Hedge 建立在 24 格上 | experiments_phase5.py:280-282；phase5_config.py:42 |
| 评估器效度：主评估器是顺序时间累加器（主控禁止称 event-driven）；登记的排序保真门槛 FAIL（ρ 最低 0.449；M2 侧 0.449 / 0.671 / 0.500）；DES 只查了 3 个配置，且用的是自研 heapq 实现而非登记的 SimPy；闭式模型高估 M2 均值，按闭式值算 22.8% / 25.1% / 37.3%，主控写的"25%–37%"与 JSON 不完全一致 | simulator.py:555-674；b5_des_crossvalidation.json#per_config；AMEND-B:134；EXECUTION-LOG.md:294 |
| 伪重复：角类臂每 200 行平均只有 134.7 个不同候选（最少 78）；bootstrap 按行重抽；聚类重分析未做。D1-d 的第 58 格 bootstrap 下界恰为 0.0，只因规则要求严格 > 0 而失败；16/72 格下界在 ±0.005 内。仅换 bootstrap 种子，行级结果在 56–58/72 之间；候选聚类 bootstrap 给出 52–55/72 | raw/*_candidate_ids.csv 计数 [QA]；analysis_phase5_blockA.py:55-63, 75；只读重算 [EXP，未登记] |
| 每个配置只有一个订单池，所有臂、模型、规模共用；池间方差只在修正案 F 里测过，而那里显示份额极不稳定 | experiments_phase5.py:113-116；amendF [NS] |
| 8 个确认性门槛里有 3 个是代码里的恒等式：D1-a、D1-c（与 M_Φ 同一表达式）、D2-d（FOSD 成立时 max(mean T1, mean T2) 恒等于 mean T1 + W1） | analysis_phase5_blockA.py:34, 53；analysis_phase5_blockC.py:77-78 |
| 推荐规则没有有竞争力或精确的对照：池内最优只算了 2 格（配置 1、n = 8 的最优为 38，P7 高 47.4%，P5 高 147%） | b2_b3_benchmarks.json#B2 [NS] |
| 已登记但未执行：B-4 稳健性电池（换向惩罚、异构容量、服务噪声）、B-6(ii) 池规模敏感性；Block A/B 修复破平后未重跑 | AMEND-B:112-158；W10:146；MASTER:39 |
| 数据纯合成，没有参数依据段落（γ = 5 秒/层、装卸 2 秒、c = 2 固定）；C&IE 可接受，IJPR 偏弱 | phase5_config.py:23；real_data_assessment:20-28 |
| 预注册无法对外验证：预注册文件与 Block A 结果 JSON 首次进入 git 是同一个提交（2c47cc5，2026-05-20 00:29 +0900），没有 OSF/Zenodo 时间戳 | git log |
| 报告不一致：T1 表列 \|A\| ∈ {5,10,20}，代码是 {5,15,30} | T1_experiment_design.md:3 vs phase5_config.py:18 |

**结论：** 作为洞察论文，C&IE 可以接受（前提是诚实界定）；IJPR 需要真实性依据、完整覆盖和并发评估器下的决策验证。

## 4. 模拟审稿人（C&IE）的主要意见

初审风险中等；若摘要和引言不改，风险高。四个推高因素：
1. 首页自相矛盾：摘要、引言的容量结论会被 §5 自己的 ICC、72% 对 47%、P9 结果反驳。
2. 没有算法：P5 被无仿真的 P8 在 10/12 格击败，比 40 次迭代的局部搜索高 46.4%。
3. 漏引同刊 2025 年的邻居 Ren 2025（Wang 2025 已在 related_works_v1.1.md:92-105 讨论，但未进定位表）和三篇先行工作。
4. Word 版 §4 不完整；主定理以"Proof sketch"交稿。

评审后的 14 条主要意见浓缩为：

| # | 意见 | 关键证据 |
|---|---|---|
| 1 | 卖点冲突：计划卖"两个工具"，主控降级 Bound-and-Gap，预注册要求"prototype-regime diagnostic"；必须选一种口径贯穿全文 | plan v0.2:13；MASTER:129；prereg:213 |
| 2 | 理论定价高于深度；唯一非平凡结果在稿件里没有证明 | SECTION_4:122-135, 158-169, 276, 343-353 |
| 3 | Prop 3 解释机制不解释频率，而频率本身在意料之中（中位数 41% 的结构差距） | b1 JSON；只读重算 |
| 4 | Hedge 很少起作用、常是统计平局、两个通过的门槛弱于表面：D2-d 由 D2-b 蕴含；D2-c 的 U_c 是 M2 分布的局部离散度而非损失界 | analysis_phase5_blockC.py:69, 77-78；amendC4 |
| 5 | 决策对象过不了评估器保真检验；至少要报告配置 1、7、11 下 Hedge 类与 M2 最优类在 DES 下是否一致 | b5 JSON |
| 6 | 实际意义与竞争力：P5 对 P0 经 BH 校正后不显著（p = 0.033）；P2 对 P5 p = 0.79；必须把 P8、P9、P7 放进主策略表 | ar2_stats_hardening.json [RA] |
| 7 | Bound-and-Gap 不是可靠的定量诊断："ceiling"读法已被内部 P9 反驳（7/12 格超过角类最优） | amendF、ar1、ar3、amendC1 |
| 8 | 统计单位与 H-D1 的刀锋判定：必须先登记再做聚类重分析，并列报告 | MASTER:39-40, 633 |
| 9 | 设计覆盖比宣传的窄：§5.1 必须说明混杂、6/18 覆盖、106,800 的定义、未执行的登记检验 | prereg:76-92, 412 |
| 10 | 文献定位不新且漏先行工作 | 见 §3.1 |
| 11 | 故事内部不一致（见 §3.3） | |
| 12 | 预注册无法对外验证，事后层次大：需要一张表列出每个假设、门槛、标签、判定、日期 | git log；MASTER:42-60 |
| 13 | 外部效度与参数依据：加公开规格依据段落；不得声称"calibrated to a facility" | real_data_assessment:20-30, 53-57 |

**进入大修的最低包（MR-1 至 MR-8）和进入接收的加项（ACCEPT-1 至 3）已并入第二部分。**

## 5. 事实核查中的更正与系统性偏差

三条更正：
1. "Gallien & Weber 在整个工作区 0 次提及"不准确：它出现在 papers/50 years of warehousing research.pdf 的参考文献里。准确说法是"在项目自写的稿件、bib、docx 和笔记里 0 次提及"。
2. 聚类 bootstrap 的 D1-d 区间应为 52–55/72（3 个种子），不是 52–54；行级 bootstrap 换 10 个种子为 56–58/72。两者都未登记，不得作为结果引用。
3. 同上，标签正确（未登记，使用前须登记），数值只近似复现。

评审引用中的系统性偏差（写 §5 时要避免）：
- 定理编号在不同文件间漂移（排序结果在 §4 md 是 Proposition 3，在主控和旧稿是 Prop. 2；SPO 等价在旧稿是 Theorem 1）。引用时须注明所依据的文件。
- 事后 [EXP] 数字未附度量定义和种子：7.47% / 7.12% 是各格比值的平均，总平均口径为 4.86% / 4.25%。
- b1 的 repos_frac 0.9943 是条件 (d) 被违反的基率，不是"联合充分条件的覆盖率"；dominance_enforced_frac 0.9967 是强制指派下的排序频率。
- 子集范围未标注：Block B、C 只用 6 个配置；B-5 只用 3 个；B-11 普查是小实例（波次规模 2–4），既不属于原型网格也不属于发表网格。
- Block A/B 的数字（D1-d 57/72、Block B 均值）在破平修复前生成，未重跑。
- RA_median_hedge_sensitivity 是 2026-09-11 加入的，而主控 §0.3 把 [RA] 定义为 2026-07-08 的修正案 A；72% 是 [RA]（ar1），47% 与两个 ICC 是 [NS]（amendF），标签应逐数拆分。
- 主控的 DES 高估"25%–37%"用任一分母都对不上：按闭式值 22.8–37.3%，按 DES 值 29.5–59.5%。

## 6. 关于另一条"路线 A"（容量对策略）

研究笔记 §5.3 的"路线 A"要保留"容量 vs 策略"结论。现有数据完全不支持：E = 1 与 E = 2 的配置用不同订单池（pool seed = SEED_BASE + config_id），Supp-2 每个 c 抽不同波次，模拟器只输出标量完工时间，没有等待、利用率、队长指标。要走这条路需要新登记一个匹配干预实验（同订单、同波次、同就绪时间、同噪声、同种子下改变 E、c 或车队），定义 Δcap 与 Δpolicy 于同一基线和统计量，报告聚类置信区间、异质性、DES 复核，并按成本归一化。算力不是障碍（0.8 秒 / 3000 候选 × 2 模型），登记与成本模型才是。本文件不推荐现在做；见第二部分 E-12（可选）。

---

# 第二部分 修改方案（目标 IJPR，底线 C&IE）

## 0. 总体策略

**两档打包：**
- **C&IE 基线包**：第一部分 §4 的 MR-1 至 MR-8 加上不违反预注册的低成本重分析。以写作为主，几乎不需要新的确认性实验。做完后可投 C&IE，预期进入大修。
- **IJPR 增项包**：在基线包之上补齐 IJPR 明文要求的两样东西，即真实应用锚点和能用的决策方法，并把理论与覆盖补到 IJPR 同类论文的水平。其中两项的结果事先不知道，必须先登记门槛再运行，失败也要报告。

**先拍板的五个决定（D-A 至 D-E）：**

| 编号 | 决定 | 推荐 | 影响 |
|---|---|---|---|
| D-A | 贡献口径 | 放弃"两个简单可用的诊断工具"。改为：C1 基准问题；C2 以 Proposition 3（升为定理后）为核心的条件性排序机制 + 由它推出的保守类别选择；C3 经验边界与测量敏感性。Bound-and-Gap 按预注册第 213 行写成"partition-relative, prototype-regime diagnostic" | 摘要、§1、§4 标题、§6；plan v0.2 §0 L13、TERMINOLOGY.md、CLAUDE.md 同步 |
| D-B | 是否为 IJPR 增加一个决策方法 | 见 C-6"筛选加验证"提案。这是本文件新提出的方案，此前任何评审或想法清单里都没有；结果未知；需登记 | 决定论文形态是"洞察论文"还是"决策辅助论文" |
| D-C | 是否做文献校准案例 | IJPR 必做；C&IE 可选。按 real_data_assessment 的可选项执行 | §5 新增子节；第三尺度标签 |
| D-D | 是否补齐完整因子设计 | IJPR 建议做（补跑另外 36 个配置，登记为 [NS] 描述性扩展） | 主效应可识别 |
| D-E | 题目 | 主控建议的"Diagnosing and Hedging Wave-Composition Decisions under Elevator-Model Uncertainty in Multi-Story AMR Warehouses"；若加 C-6 方法，题目需相应体现"screen-and-verify" | 全文 |

**不可逾越的红线（预注册纪律）：**
1. 已锁定的判定（H-D1 PARTIAL 57/72、H-D2 PASS、H-Policy Partial、H-D3 model-sensitive、C-4 FAIL、B-5 FAIL、F FAIL）不得改写；任何新数字与原判定并列报告。
2. 新分析一律先登记（日期化修正案，门槛与措辞阶梯在运行前锁定），再运行，再报告；标签按主控 §0.3。
3. 不得事后向已锁定的 H-Policy 竞赛加入新基线；新方法或新对照进入新的 [NS] 研究，有自己的门槛。
4. 不得重调 P5、不得改 make_config_array() 的 18 个配置、不得把 [EXP] 事后计算写成确认性证据。
5. 不得把本文件里的审计数字（52–55/72、56–58/72、41%、7.47%、0.43–0.78）直接写进稿件；它们只说明"该登记做什么"。

## 1. 创新性

| 编号 | 档位 | 动作 | 回应的问题 | 进入方式 | 工作量 |
|---|---|---|---|---|---|
| N-1 | C&IE | 重写摘要、§1、亮点里的新意表述，只保留三条：界定清楚的单波次组成问题与基准（C1）；Proposition 3 作为理论核心（任意 E、c 的条件性排序、与 RTT 直觉相反的符号、对齐指派下完备的两种反转通道）；经验边界结果（C3）。删除"never treated"、"only in isolation"、"integrates the four-way interaction" | §3.1 削弱证据末行；R2 意见 10、11 | 写作 | 2 天 |
| N-2 | C&IE | §2 加定位对照表。列：决策层；波次或请求集是否内生；是否有多机器人电梯争用；是否柔性楼层受限车队；是否考虑电梯模型不确定；理论类型；验证数据。行：Gallien & Weber 2010、RAWSim-O 2017、Han 2025、Kim 2025、Chakravarty 2025、He 2026、Wang 2025、Ren 2025、Zhen 2023、Tadumadze 2023、Qin 2024、Xue & Wang 2026、Xu 2026、Tang 2026。最后一行才是本文 | 三篇先行工作与 9 篇前沿邻居缺失 | 写作 + 补 bib | 3 天 |
| N-3 | C&IE | 把 Hedge 明确定位为 Fan, Hong & Zhang (2020) 稳健最优选择的两模型特例，并说明本文的新意在于"排序前提在仓库电梯场景下可证"（Proposition 3），不在 minimax 归约本身；把 Bound-and-Gap 与 Bertsimas & Kallus 2020 的 coefficient of prescriptiveness、Jiang 2026、VSS、EVPI 比较；把 Corollary 3 与 Fu et al. 2024 的占优下闭式 DRO 比较 | 审稿人"这是已知技术"的攻击 | 写作 | 2 天 |
| N-4 | C&IE | 组装附录 A（Lemma 3–6、情形 F/B、全 E 归纳，约 400 行），作者通读并承担数学责任，然后按计划 v0.2 D-3 把 Proposition 3 升为 Theorem。用 B-11 普查（(c)+(d) 下 1,150,800 实例 0 违例）和 B-1 通道拆分（18/2/0）作为"机制完备"证据，标 [NS]，不得写成频率解释 | 唯一非平凡结果仍是梗概 | 写作 + 数学核验 | 1–2 周 |
| N-5 | IJPR | 登记并运行 Proposition 3 的"必要性侧"描述性分析：逐波次量化条件 (d) 被违反时距离产生反转还差多少（余量分布），或检验一个覆盖大多数波次的较弱聚合充分条件。目标是把"充分条件覆盖 < 1%，排序却成立 99.2%"这一落差从"未解释"变成"部分解释"。若能得到概率型或余量型的排序陈述（把中位数 41% 的结构差距与观测频率联系起来），C2 的理论深度会实质提高 | R2 意见 3；ACCEPT-1 | [NS] 修正案，先登记；数学部分是新工作 | 2–4 周，结果未知 |
| N-6 | IJPR | 把测量口径依赖（72% 对 47%；ICC 0.009 / −0.029；样本外收缩 16.6% / 21.2%）写成对"结构价值诊断"这一类方法的可迁移警示，并与 prescriptiveness 系数对照 | 把负结果变成可识别的洞察 | 写作 | 2 天 |
| N-7 | IJPR | 若采纳 C-6，把"闭式筛选 + DES 验证"作为方法层面的新意点：便宜评估器负责在数千候选里筛，昂贵评估器只验证短名单，而 Proposition 3 保证用 M2 筛是保守的 | R2"没有算法" | 见 C-6 | 见 C-6 |

## 2. 贡献度

| 编号 | 档位 | 动作 | 回应的问题 | 进入方式 | 工作量 |
|---|---|---|---|---|---|
| C-1 | C&IE | 执行 D-A：摘要、§1、亮点严格按 MASTER:127-131 的 C1–C3 写；C2 以 Theorem（原 Proposition 3）开头，Theorem 2 改称推论级归约；Bound-and-Gap 在引入处即注明预注册第 213 行的弱化表述；删除 introduction_v1.1.md:221-251 与 abstract:49 的容量语句；同步修改 CLAUDE.md:76、TERMINOLOGY.md:39, 48, 52、plan v0.2:13 | 卖点冲突；已废止结论 | 写作 | 3 天 |
| C-2 | C&IE | 登记一个 [RA] 呈现修正案（只用已有数据，无门槛），然后在 C-4 显示表里加一行 minimax-regret：公开报告 minimax-makespan 与 minimax-regret 的选择在 5/6 个配置一致，只在配置 11 分歧（2.63% 对 0.17%）；每个 Hedge 选择旁给出与第二名的差距和候选聚类 bootstrap 的选择频率 | Hedge 的决策价值被质疑 | [RA]，先登记 | 3 天 |
| C-3 | C&IE | 登记 Supp-1 的"耦合显示"为 [EXP] 描述性呈现（明确非确认性）：Φ 角类相对随机的优势在 FIFO 下与聚类调度下的数值，各格为正的个数，附单种子、200 波次、E = 2、F ∈ {3,5} 的限定，并同时给出两种度量口径（各格比值平均与总平均）。用它回答"运营杠杆 10.2% 大于战术杠杆，为什么还研究战术层"：两个杠杆大致可叠加 | 故事最弱一环 | [EXP]，先登记 | 2 天 |
| C-4 | C&IE | 登记并运行 candidate_id 聚类（或去重）bootstrap，覆盖 Block A/B/C 的全部区间；与预注册的 57/72 并列报告，判定不变；§5.1 把分析单位改称"unique candidate waves"，并把 106,800 定义为模型评估次数。事先写好 Block A/B 破平修复重跑的新旧并列报告规则 | 伪重复；刀锋判定 | [RA]/[QA]，先登记 | 3 天；算力分钟级 |
| C-5 | C&IE | 代码、池种子、candidate_id 边车文件、冻结的预注册及其提交哈希发布到 Zenodo，并如实说明锁定是内部的（同一提交） | C1 作为可复现基准的可信度 | 归档 | 1 天 |
| C-6 | IJPR | **决策方法提案："筛选加验证"（screen-and-verify）的波次组成方法。** 本文件新提出，需作者拍板（D-B）。第一阶段：用闭式评估器在 M2 下评价全部 K = 3000 个候选（0.8 秒），取前 k 名；按 Theorem 2 的逻辑，在排序成立时候选层面的 minimax 选择就是 M2 池内最优，所以用 M2 筛是保守的。第二阶段：用事件驱动 DES 评价这 k 个候选，释放其中 DES 最优者。研究问题：短名单要多大，便宜筛选才能找回 DES 池内最优；筛选后悔（DES 下所选候选相对 DES 池内最优的差距）随 k 如何变化；用 M1 筛与用 M2 筛的差别。对照：随机、P7、P8、P9、闭式池内最优、DES 池内最优。评价范围：至少 Block C 的 6 个配置，最好 18 个（B-5 的 JSON 记录 runtime_seconds = 0.7，对应 3 个配置 × 200 个配对波次，所以全池 DES 在算力上可行）。门槛与措辞阶梯在运行前锁定，例如"k ≤ 20 时在 ≥ 5/6 配置找回 DES 最优"为通过；失败则报告为方法的有效性边界 | R2"没有算法"、"排序不迁移到 DES"；IJPR 的"决策方法"要求 | [NS] 修正案，先登记；不进入 H-Policy 的锁定判定；池内最优从 §3.4.3 的基准升为方法的一部分需在 C1 口径里说明 | 2–3 周；算力分钟级；结果未知 |
| C-7 | IJPR | 执行 N-5 的理论加强。若成功，C2 从"机制 + 归约"升为"机制 + 频率解释 + 归约" | 理论深度 | 同 N-5 | 同 N-5 |
| C-8 | IJPR | 若 C-6 成功，§6 的管理含义改为三段可执行建议：用 M2 筛、用 DES 验证短名单、粗类别诊断只用于解释；若 C-6 失败，管理含义保持 C&IE 版本（见 S-6），并把失败作为"闭式筛选的边界"报告 | 证据到含义 | 写作 | 3 天 |

## 3. 故事完整度

| 编号 | 档位 | 动作 | 回应的问题 | 工作量 |
|---|---|---|---|---|
| S-1 | C&IE | 先冻结一页"故事契约"：一种口径（D-A）、三个 RQ（MASTER:135-137）、每节的完成门槛、题目（D-E）。传播到 plan v0.2 §0、主控 §2.2、TERMINOLOGY.md、CLAUDE.md。主控 §6 的 §3 指针改为 Problem formulation.docx，§7.5 编号表按 D-3 更新，删去 Corollary 4，L23 的"覆盖分区证据为无"改为引用 B-13 的 48/48 并说明中位数约定差异 | 三处口径冲突；指引文件污染；来源漂移 | 1 天 |
| S-2 | C&IE | 补完 Word 版 §4：4.3.2 结尾、式 (47)、Fig. 4、整个 4.4（三段式 Theorem 2 与 Corollary 2–3）；把 Hedge Rule 和 Bound-and-Gap 的名字放进 §4 标题；组装附录 A（N-4） | §4 缺方法；两个工具名在 §4 里为 0 次 | 1–2 周（与 N-4 合并） |
| S-3 | C&IE | §5 从 JSON 重新写，按 RQ1–RQ3 顺序，加证据标签列。必须包含：106,800 = 72,000 + 16,800 + 18,000 的定义；混杂说明；Block B/C 只覆盖 6/18 配置；H-D1 PARTIAL 57/72；D1-b 70/72 作为"前提被 §4 证明有误"的未达门槛（H_up 对非覆盖角类族可为负）；H-D2 PASS，并把 D2-c、D2-d 写成 FOSD 蕴含的一致性检查；H-Policy Partial 并把 P8、P9、B-2 池内最优锚点（38；P7 +47.4%；P5 +147%）放进主策略表；ICC FAIL；72% 与 47% 并列；样本外收缩；DES 符号保留但排序 FAIL，高估幅度写明分母；C-4 代价与证书无信息量；充分条件 < 1% 对 99.2% 频率；聚类 bootstrap 结果并列；一张列出全部假设、门槛、标签、判定、日期的总表。一句话都不从 section5_draft_v0_1.md 复制 | §5 不存在 | 2 周 |
| S-4 | C&IE | §1 写出 RQ1–RQ3；§2 按主控 §5.1 的六个小节重组，以 N-2 的定位表收尾；摘要最后写，按主控 L170-177 的六句逻辑，250 词内，不含 72% 份额、buy capacity、first-ever、无条件保证、U_c 下行保证 | 首页自相矛盾 | 1 周 |
| S-5 | C&IE | §6 全新写（只借 W5 的结构）：逐 RQ 一段；每个边界结果配一条可执行的报告规则：(i) 对冲前先验证本地评估器的排序；(ii) 任何类别选择都要报告差距与选择稳定性；(iii) H_up 不作容量解读，容量问题须另做匹配研究；把 10.2% 对 6.0% 写成范围边界；B-5 从未来工作里删掉（已执行） | §6 不存在 | 1 周 |
| S-6 | C&IE | 修小的悬空点：题目决定；DES 高估幅度用 JSON 可复算的分母；T1 的 \|A\| 层次改为 {5,15,30}；U_c 的定义按 analysis_phase5_blockC.py:69 写成"M2 分布的局部离散度"，旧值按主控 L390 重算；定理编号全文统一 | 悬空表述 | 2 天 |
| S-7 | IJPR | 若采纳 C-6，故事主线改为"决策辅助"：动机（共享货梯争用）→ 缺口（组成决策 + 模型不确定）→ 方法（M2 筛选 + DES 验证，含 Theorem 保守性保证）→ 诊断（Bound-and-Gap 解释为什么粗类别不够）→ 边界（ICC、分区、保真）→ 校准案例（S-8）。C1–C3 相应改写为 C1 问题与基准、C2 保证与方法、C3 边界与案例 | IJPR 的"决策问题"框架 | 与 C-6 同步 |
| S-8 | IJPR | 加"文献校准案例"子节（E-9 的结果）：用公开规格与公开订单数据驱动 1–2 个第三尺度配置，走同一管线加 DES；措辞只能是"parameters set within publicly documented ranges"，不得写"calibrated to a facility" | IJPR 的"real-life applications" | 1 周 |
| S-9 | IJPR | 摘要与 §1 用生产研究的语言：明确决策者是谁（WMS 的波次释放），决策频率，可交付物（一个筛选加验证流程 + 一个诊断协议），以及在什么条件下不适用 | IJPR 初审对"纯 OR、无生产研究框架"的过滤 | 与 S-4 同步 |

## 4. 实验设计复杂性

| 编号 | 档位 | 动作 | 回应的问题 | 进入方式 | 工作量 |
|---|---|---|---|---|---|
| E-1 | C&IE | 聚类 bootstrap（同 C-4） | 伪重复 | [RA]，先登记 | 3 天 |
| E-2 | C&IE | 登记并运行 Block C 的扩展：把 M1/M2/M3 配对评价（沿用 D2-a/b 的门槛定义、Hedge 代价、第二名差距、聚类 bootstrap 选择频率）扩到未覆盖的 12 个配置（全部 E = 1 与 F = 8）以及 n ∈ {8, 30}。声明不能改变锁定的 H-D2 判定 | 关键证据只覆盖 E = 2、F ≤ 5、n = 16 | [NS]，先登记 | 算力分钟级；分析 3 天 |
| E-3 | C&IE | 执行已登记的 B-4 稳健性电池（换向惩罚、异构容量、服务噪声）与 B-6(ii) 池规模敏感性，门槛按 AMEND-2026-07-08-B 原文；失败按锁定规则报告为有效性边界。或在附录 F 明确撤回并给理由 | "已登记未执行"的可见缺口 | 已登记 | 算力分钟级；分析 3 天 |
| E-4 | C&IE | 登记并运行全池枚举（计划 v0.2 §4 的修正案 3）：36 个池的精确类别中位数与精确池内最优；报告 P5/P7/P8 在 12 格（而非 2 格）上的最优性差距。作为描述性锚点，不作竞争策略，不改门槛 | 缺精确对照 | [NS]，先登记 | 算力约 30 秒；分析 2 天 |
| E-5 | C&IE | §5.1 诚实呈现设计：因子覆盖矩阵（混杂关系；哪个块覆盖哪些配置）；把恒等式检查（D1-a、D1-c、D2-d、B-13）与经验门槛分开列 | "夸大严谨"的攻击 | 写作 | 1 天 |
| E-6 | C&IE | 写参数依据段落与表：γ（5 秒/层）、装卸 2 秒、c、E 对应到公开货梯规格（KONE HD MonoSpace CSI、Schindler 2600、Peters RTT 论文的逐相位分解），按 real_data_assessment:22-28 的清单 | 参数无出处 | 写作 | 2 天 |
| E-7 | C&IE | 预注册与提交哈希归档到 OSF/Zenodo，并声明锁定是内部的；行文改称"locked analysis plan with dated amendments" | 预注册不可验证 | 归档 | 1 天 |
| E-8 | IJPR | 登记 DES 作为决策对象的协同评估器：在全部 18 个配置（至少 Block C 的 6 个）上用 DES 评价角类臂，报告类别排序一致性、DES 下的 Hedge 类、闭式所选类是否落在 DES 第二名差距之内；与 C-6 的 DES 验证共用一次运行；把 B-5 用 heapq 而非 SimPy 的偏离写进附录 F | 排序保真 FAIL 只查了 3 个配置 | [NS]，先登记 | 算力分钟级；分析 1 周 |
| E-9 | IJPR | 登记"文献校准案例"修正案：KONE/Peters 相位时间 + 公开订单集（JD MSOM 2020、Instacart 2017 或 UCI Online Retail II）驱动的楼层需求与就绪时间 + 一个公开的多层机器人仓锚点（如 3 层设施）。1–2 个配置（config_id ≥ 100，结果文件用独立前缀），跑既有管线加 DES。第三尺度标签登记进 TERMINOLOGY.md | IJPR 的真实应用要求 | 修正案，先登记 | 数天；算力分钟级 |
| E-10 | IJPR | 登记多池重复：Block B 与 Block C 在每个配置上用 5–8 个独立订单池（复用修正案 F 的种子）重跑，报告配置级均值 ± 池间标准差（P5 对 P0/P2/P8 的增益、Hedge 代价、C-6 的筛选后悔） | 单池依赖 | [NS]，先登记 | 算力分钟级；分析 3 天 |
| E-11 | IJPR | 登记互补分数：补跑 3 × 3 × 2 × 3 全因子中剩余的 36 个配置（另外两个 1/3 分数），作为描述性扩展，使 F、\|A\|、需求模式的主效应可估计。锁定判定只基于原 18 个配置 | 主效应不可识别 | [NS]，先登记 | 算力分钟级；分析 1 周 |
| E-12 | 可选 | 匹配容量干预实验（第一部分 §6）。只有在想恢复"容量 vs 策略"结论时才做；需要给模拟器加等待、利用率、队长输出，并有成本模型。不建议在本轮做 | 另一条路线 A | [NS]，先登记 | 3–4 周 |

## 5. 执行顺序与依赖

```
阶段 0（1–2 天）  S-1 故事契约；D-A 至 D-E 拍板；所有待登记修正案一次性写好并签日期
阶段 1（1 周）    先登记再运行的重分析与扩展：C-4/E-1、C-2、C-3、E-2、E-3、E-4
                  （算力总计分钟级；结果并列报告，不改判定）
阶段 2（1–2 周）  N-4 附录 A + Prop 3 升定理；S-2 补完 Word 版 §4
阶段 3（2 周）    S-3 写 §5；S-5 写 §6；E-5、E-6、S-6
阶段 4（1 周）    S-4 写 §1、§2（含 N-2、N-3）、摘要、亮点；C-5、E-7 归档
                  ── 到此为 C&IE 基线包，约 6–8 周 ──
阶段 5（并行 2–4 周）IJPR 增项：C-6 筛选加验证（含 E-8 的 DES 协同评估）；E-9 校准案例；
                  E-10 多池重复；E-11 互补分数；N-5/C-7 理论加强
阶段 6（1–2 周）  按增项结果改写 S-7、S-8、S-9、C-8；全文再次一致性检查
                  ── 到此为 IJPR 增项包，在基线包之上再加约 4–8 周 ──
```

依赖关系：
- S-3（§5）依赖阶段 1 的全部结果，因为 H-D1 处在一格之差的门槛上，数字必须先定型再写。
- S-4（§1、§2、摘要）必须最后写。
- C-6、E-8 共用一次 DES 运行；E-10 的多池重复若做，C-6 的筛选后悔也应在多池上报告。
- N-5 是纯数学加实验的探索，与写作并行，失败不影响基线包。

## 6. 预期效果（诚实估计）

| 维度 | 现状 | 完成 C&IE 基线包后 | 再完成 IJPR 增项包后 |
|---|---|---|---|
| 创新性 | 2.5 | 3（定位准确，Prop 3 成为完整定理） | 3.5（若 C-6 或 N-5 成功）；否则 3 |
| 贡献度 | 2.5 | 3（口径统一，Hedge 与边界结果定价诚实） | 3.5–4（若 C-6 成功，有了能用的方法）；C-6 失败则 3 |
| 故事完整度 | 2 | 3.5（全文按一条主线写完） | 4（决策辅助主线 + 案例） |
| 实验设计 | 3 | 3.5（覆盖补齐、伪重复处理、依据段落） | 4（DES 协同评估、多池、全因子、校准案例） |
| C&IE | 拒稿后重投 | 大修，可望接收 | 接收概率更高 |
| IJPR | 不足 | 仍偏弱（缺方法与应用锚点） | 有机会，但取决于 C-6 与 E-9 的结果 |

**判断依据：** IJPR 同类论文都有一个优化或解析方法，且范围明文要求真实应用。基线包不提供这两样，所以基线包做完后 IJPR 仍不足。增项包里 C-6 与 E-9 直接对应这两项要求；两者结果事先未知，这是 IJPR 路线的主要风险。

## 7. 作者需要拍板的清单

1. D-A：是否放弃"两个工具"的口径，改按 MASTER C1–C3。
2. D-B：是否登记并运行 C-6"筛选加验证"方法。若否，IJPR 路线基本不成立，建议直接以 C&IE 为目标。
3. D-C：是否做 E-9 文献校准案例。
4. D-D：是否补跑互补分数（E-11）。
5. D-E：题目。
6. 阶段 1 的修正案清单是否一次性签署（C-2、C-3、C-4/E-1、E-2、E-3、E-4）。
7. N-5 的理论探索是否立项（结果未知，不影响基线包）。

## 8. 来源

- 期刊范围：[IJPR aims and scope](https://www.tandfonline.com/journals/tprs20/about-this-journal)；[C&IE journal page](https://www.sciencedirect.com/journal/computers-and-industrial-engineering)。
- 先行工作与前沿邻居：[Gallien & Weber 2010, MSOM](https://pubsonline.informs.org/doi/abs/10.1287/msom.1100.0291)；[Fan, Hong & Zhang 2020, Management Science](https://pubsonline.informs.org/doi/10.1287/mnsc.2018.3213)；[RAWSim-O 2017](https://arxiv.org/html/1710.04726)；[Wang et al. 2025, C&IE 210:111559](https://www.sciencedirect.com/science/article/abs/pii/S0360835225007053)；[Ren et al. 2025, C&IE 204:111095](https://www.sciencedirect.com/science/article/abs/pii/S0360835225002414)；[He et al. 2026, MAPF with Elevators](https://arxiv.org/html/2602.20512v2)；[Han et al. 2025, Sensors](https://pmc.ncbi.nlm.nih.gov/articles/PMC11946681)；[Kim et al. 2025, Electronics](https://doi.org/10.3390/electronics14050982)；[Zhen et al. 2023, Annals of OR](https://dblp.org/rec/journals/anor/ZhenWLTY23.html)；[Xu et al. 2026, WareRover](https://arxiv.org/abs/2602.13999)；[Tang et al. 2026, SOAR](https://arxiv.org/abs/2605.03842)；[Tadumadze et al. 2023, FSMJ](https://link.springer.com/article/10.1007/s10696-023-09491-0)。
- IJPR 同类论文：[IJPR 63(1) 2025](https://www.tandfonline.com/doi/abs/10.1080/00207543.2024.2361436)；[IJPR 64(6) 2026](https://www.tandfonline.com/doi/abs/10.1080/00207543.2025.2609978)；[IJPR 64(5) 2026](https://www.tandfonline.com/doi/full/10.1080/00207543.2025.2609176)；[IJPR 64(14) 2026](https://www.tandfonline.com/doi/full/10.1080/00207543.2026.2616669)。
- C&IE 仿真型先例：[Winkelhaus et al. 2022, C&IE 167](https://www.sciencedirect.com/science/article/pii/S0360835222000511)；[2026 DES + 深度学习 RMFS 车队规模论文](https://www.sciencedirect.com/science/article/abs/pii/S0360835226001117)。
- 预注册在仿真研究中的价值：[Pawel et al., arXiv 2203.13076](https://arxiv.org/pdf/2203.13076)；[COS simulation-studies preregistration template](https://www.cos.io/blog/introducing-the-simulation-studies-preregistration-template)。
- 项目内部：MASTER_REVISION_BY_SECTION.md（§0.1–0.3、§2.2–2.4、§5、§8、§9）；phase5_scaleup_preregistration.md（§3、§4 第 213 行、§9）；contribution_review_2026-08-06.md；contribution_review_continuation_2026-09-02.md；real_data_assessment_2026-07-19.md；CONTRIBUTION-IDEAS-2026-07-08.md；plan_section3_section4_v0_2.md。
- 本次评估的原始输出：工作流 wf_6e7d903d-05b 的 journal.jsonl（C:\Users\64432\.claude\projects\F--Paper-3\44566305-b1de-4f16-8662-87a70f46d90f\subagents\workflows\wf_6e7d903d-05b\）。
