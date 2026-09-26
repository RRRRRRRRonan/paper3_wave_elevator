---
title: "三条贡献 × 五条标准 全面审查（对抗验证版）"
date: 2026-08-06
method: "5 个标准视角 agent 各自横跨 C1/C2/C3 审读当前全部稿件与证据；36 条 major/critical 发现逐条交独立反驳者核实（打开引用文件、检查当前稿是否已处理、评估对 Q1 决定是否 material）；4 条被驳回、4 条降为 minor、32 条幸存。关键数字由作者助理再次亲自核对（b1_matched_assignment.json、amendF_test_retest.json、amendC4_uc_tightness.json）。"
run: "wf_39e540bf（41 agents，781 次工具调用）"
status: "决策备忘录；所列修法均不触碰冻结预注册与已锁判定"
---

# 一、判定矩阵

| 标准 | C1 问题形式化 | C2 方法论（两工具） | C3 实证诊断 |
|---|---|---|---|
| 1 创新度 / 前沿定位 | conditional | conditional | conditional |
| 2 模型正确刻画背景 | conditional | conditional | conditional |
| 3 方法合理解决问题 | conditional | conditional | conditional |
| 4 结论正确证实贡献 | **pass** | conditional | conditional |
| 5 论述链完整 | **pass** | conditional | conditional |

**总判断**：没有任何一条贡献"fail"，四要素问题类经 2024–2026 文献抢占检索仍然成立；但**没有一条贡献在五条标准上全部干净通过**。问题集中在两处"卖点超出证据"（Tool 2 的定理背书、C3 的容量占主导标题）和一批未完成的拼接/陈旧文本。所有修法都是**重新计费 + 补报告 + 完成拼接**，不需要新的大规模实验；仅两个小型注册展示可复用已有数据。

# 二、六大主题（按严重度排序）

## 主题 A（最严重）：Tool 2 的"定理保证"计费过高 —— C2

**事实**（亲自核对）：
- Prop 2 的四个前提中，(d)"无逆向重定位"在 **99.43%** 的 Block C 波次中失效（`base_rate_all_waves.repos_frac = 0.9943`）；(c) 在 12.67% 失效；(b) 自由指派下只有 57.8% 成立。四条同时成立的波次 **不足 1%**。
- 而逐波次支配却在 99.2%（自由）/ 99.67%（强制 (a)(b)）的波次成立 → 这 99.2% 是**本模拟器的经验规律**，不是 Prop 2 证出来的性质。Prop 2 证明的是"充分条件 + 恰好两条失效通道"（机制刻画），不是"规则赖以成立的保证"。
- 摘要 v1.7 与 §1 C2 的现行措辞："**Its guarantee rests on Proposition 2**"、"A dominance theorem ... **proves this simple hedge minimizes worst-case makespan**"——把 Theorem 1（在支配成立处坍缩）和 Prop 2（支配何时成立）混为一谈。

**连带三项**（发现 #13/#14/#18/#22/#27）：
- **DRO = Hedge 6/6 是一致性检查，不是证据**：在样本级一阶随机支配（门槛 D2-b）下，W1 距离恒等于均值差，argmin 代数上必然一致——与 W1 Edit 9 把 D1-c 重定性为"管道一致性检查"是同一情形。且 D2 用均值定 Hedge 角、正文用中位数：config 5 两者不一致（角间差 1.95 落在 U_c = 4.6 之内，正是 Cor 2 的刀锋区）。
- **Cor 2 的 "computable worst-case-loss bound" 措辞仍在三处**（§1 C2、W1 §4.2.3、W5 §6.1）——W10 已下令删除；U_c 界的是 M2 侧中位扰动，不是"跟随规则的最坏损失"。Cor 2 的精确条件（角间差 > max U_c）在 6 配置中仅 1 个满足，且从未设门槛。
- **Hedge 的实际价值薄且有代价**：5/6 配置三模型最优角相同（无需对冲）；唯一分歧的 config 11 中，Hedge 角在 M1 为真时 regret **2.63%**，而名义 M1 角仅 0.17%——Hedge 是"最坏水平最优"但被"最坏遗憾"支配。C-4 的这一结果在稿件里无处安放。

**修法**（全部措辞/报告层面）：
1. 摘要 + §1 C2 + §4.3：Prop 2 改计费为"机制结果：给出充分条件并证明失效只有两条通道"；Theorem 1 的表述改为"**在逐波次支配成立之处**（99.2% 的匹配波次），按最保守模型选恰好最小化最坏工期"；删除 "guarantee rests on Proposition 2"。
2. §5.3：在 99.2% 旁边并排打印前提基率 (b) 57.8% / (c) 87.3% / (d) 0.6%，明确"条件充分而远非必要；即使失效处违例也罕见"（W10 已有此读法，未落稿）。
3. D2-d 重定性为一致性检查（同 D1-c 先例，不重判 PASS）；补一行中位数 Hedge 角对照，披露 config 5。
4. 三处 U_c 措辞改为"近似支配下 M2 角中位数扰动的可计算上界"；§5.3 加一句 C-4 实付价格（5/6 为 0，config 11 为 2.63%，ε=0.10 覆盖）；§6.1 明说"对冲在 5/6 配置免费、在 1/6 配置花费 2.6%"。
5. C-4 展示加一行 minimax-regret（复用已有数据，注册为展示补充，不设门槛）。

## 主题 B：C3 的"容量占主导"标题在有保证的口径下不成立 —— C3

**事实**（亲自核对）：
- 截断 Φ-rule 份额 H_up/(H_up+M_Φ)：副本均值 0.76–0.95，18/18 > 0.5 → "约 72%"。
- **覆盖式 oracle 份额** H_up/UB（**唯一有 H_up ≥ 0 与 Theorem R 定理保证的口径**）：副本均值 **0.40–0.52，仅 4/18 > 0.5**——容量并不占主导。
- 单次运行份额的种子信度 ICC(2,1) ≈ **0.01**（覆盖式 −0.03），SEM 0.136；Amendment F 的 ICC 门槛 **FAIL**，此结果在稿件任何位置未报告；只有通过的 15/18 一致性进了摘要与 §1。
- 72% 之所以高，是因为 M_Φ 小（P5 在多数格里已找到 oracle 角）——它度量的是"P5 的脱靶相对最差角罚金很小"，与"运力锁死大头"是两种读法。
- P9（波次级线性策略）在 **7/12** 格里中位数低于 oracle 角中位数，即回收超过整个角 oracle 预算 S_or → "H_up 是任何 Φ 策略都拿不回的天花板"的表述**被自家结果反证**；M_Φ 只是"分区常数规则的遗憾"。

**修法**：
1. §1 C3 开头与摘要：删除无限定的 "capacity is the binding side"；改为**双口径并排**："截断 Φ-rule 份额约 72%；覆盖式 oracle 份额约 47%（SEM 0.14）；二元判定在 15/18 配置跨种子一致（副本均值 18/18 > 0.5，仅在 Φ-rule 口径下）"。A-R1 限定语必须同时进 §5.2 与 §6.1（现两处仍是裸 71.7%）。
2. §5.2 末加"种子级信度（Amendment F）"段：8 种子 × 18 配置，一致 15/18，ICC ≈ 0.01（FAIL，如实报），SEM 0.136，最小可检测差 0.38，50–200 波次/臂时判定一致性恢复，fig9；点名 3 个不一致配置使 15/18 可审计。
3. 全文把 "no wave-release policy on Φ can recover" 收窄为 "**no partition-constant policy on Q can recover**"，"recoverable slack" 收窄为"角常数规则在此分辨率下可回收的余量"；§5.4 报告 P9 的 R > 1 格并说明 S_or 是 Φ 波次级选择可回收量的下界。
4. C3 真正新颖的实证内容应上升为标题：分辨率/口径依赖本身（Theorem R 实证）、支配频率跨容量 2–5 稳定、战术杠杆 < 运营杠杆的诚实排序。

## 主题 C：§3 模型描述与引擎不一致 —— 横跨 C1–C3

（发现 #6–#12，反驳者全部未能驳回）
1. **T 不恒为零**：W4 说主设计 T ≡ 0，但 6 个 diurnal 配置激活了错峰放行（50 s 视窗），T 在 1/3 网格中活跃；且 "diurnal" 是误称（50 s 内的波内错峰，非日周期）。→ 改写 §3.1/§3.2，说明角分区只用 (C, I)，T 仅进入 A2 消融与 A-R1 敏感性。
2. **操作规则描述 ≠ 引擎**：§3 写"按放行顺序、电梯 FCFS"，引擎实际按采样列表顺序处理、电梯按处理顺序承诺，被指派到未放行订单的 AMR 会空等——这正是 DES 交叉验证 25–37% 悲观偏差的机制。→ 改为"按订单处理序承诺"，定义处理序为候选生成时固定的随机排列（属固定操作层，也是 Prop 2 前提 (a) 的对象），A1 补一句空等行为。
3. **单波次冷启动评估未声明**：所有 AMR/电梯空闲于 1 层、无前后波次、无积压成本——这使目标是单波次 makespan 而非吞吐量。→ 新增假设 A6 + §6.2 一句限制。
4. **§3.3 缺保真声明**：B-5 已执行且序数门槛 FAIL（ρ 0.45–0.68 < 0.9）、25–37% 系统高估，W5 limitation (1) 仍写 "pending"。→ §3.3 加两句：保守评估器、支配号与分解号可迁移、逐波次排名不可，Block B 与 P5/P6、99.2% 均限定于闭式模型类。
5. **参数无出处**（已在 04 清单第 7 条）：5 s/层、2 s 载卸、5 s 取放、c=2、σ=0.20、50 s 视窗。→ §3.3 或附录 grounding 段（公开规格来源见 real_data_assessment）。
6. **M1 不是物理安装**：M1(E, c) ≡ M1(E·c, 1)，M1/M2 之别是"容量表示方式"而非"安装类型"。→ §3.1/§4.2.1 改为"规划模型采用哪种容量表示"的不确定性；顺带这也是支配号直觉的来源。（降为 minor）
7. **发布版模拟器仍按 id(e) 破平**：B-14 修复只存在于 tier-2 脚本的 monkeypatch。→ 把 simulator.py 五处 id(e) 改为 enumerate 索引键，重跑 `python -m src.simulator`，§3.3 写入"电梯与 AMR 可用性平局按单元索引破平"，附 W10 §4 复现性说明。（降为 minor，但发布代码必须做）

## 主题 D：Theorem R 的适用范围与实验仪器不匹配 —— C2

（发现 #4/#15/#28）
- Theorem R / Cor 1 对**覆盖式**分区证明；但 72% 所在的仪器是 **FILTER_Q = 0.25 截断角（非覆盖）**，且 2×2 → 3×3 消融**不是嵌套加细**。§1 现写 "Corollary 1 applies this to the specific wave classes used in our experiments" 不成立；§5.5 A4 "confirms Corollary 1" 与 Remark R.3（非嵌套方案无序）自相矛盾；B-13 报告 3×3 在 2/12 格落在嵌套区间之外。
- **修法**：把 Theorem R 的假设改写为其证明实际使用的形式——"Q' 加细 Q 且每格的子格覆盖该格（Q 本身无需覆盖池）"，这样 Cor 1 合法覆盖截断角的**子分裂**加细；正文明说 2×2→3×3、四分位→三分位不是此类加细；A4 改写为描述性观察，Theorem R 的确认只引 W8-2 段（嵌套 2×2→4×4，12/12 + 12/12）；§1 该句改为 "applies this to the nested family validated in Section 5.2 (48/48)"。（W1 "理论声明与不声明"段把 Theorem R 也列为初等括括结果，价值在报告协议与 B-13 验证。）

## 主题 E：论述链断点与陈旧文本 —— C2/C3

（发现 #21/#23–#26/#29–#32）
1. **§4.2.1 最终版 Prop 2 文本不存在**：00_INDEX 指向的两个模块文件仍是被 X.2 证伪的三条件版 + 已退役的"唯一失效方式"句。→ 起草一份最终 §4.2.1（两通道定义、(a)–(d) 全 E 命题、必要性 X.1/X.2）与最终附录 X.4（W3-E2 去 (c*)、case B 换 Lemma 6、W10 §2 修正 1–3），两个 v1.0 模块在 INDEX 标 SUPERSEDED。
2. **§5.3 最终文本未写**：v1.0 模块仍写 "none arise from any other mechanism"；W3-E5 替换稿说分类器"未运行"（已运行）且末句被 W9 判为假。→ 按 W10 规格一次写成：99.2% [Wilson 98.9–99.4] 与 99.67% 并排、通道表 18/2/0、基率 12.67%/99.43%、W9 修正末句。
3. **§5.2 无 Amendment F 段落**（主题 B 第 2 条）。
4. **W5 §6 三处陈旧**：B-2/B-3/B-5 写作 "registered and pending"，实际均已执行且 B-5 门槛 FAIL。→ 重写 limitation (1)（B-5 结果与锁定后果）、limitation (4)（引 B-2 枚举锚点 pool optimum 38 vs P7 +47.4% 与 P8）、未来工作删去这三项。
5. **"passes every pre-registered test" 不再严格为真**：C-4 的信息量门槛 FAIL 0/6。→ 改为 "passes all four pre-registered Block C gates"，并如实报 C-4。
6. **可委托性措辞超出锁定阶梯**：§1 用 "can be recovered with existing methods"（顶格），C-1 锁定结果是 "partially recoverable"。→ "can be targeted by existing predict-then-optimize methods; an off-the-shelf SPO+ learner partially recovers it (median R = 1.00 over 7 nonzero-budget cells, 5 zero-budget cells excluded)"；Table 4 补 P8 行、P9 展示、枚举锚点。
7. §4 权威稿仍带旧编号与 "holds in 99.2% of waves"；全 E 证据栈（1,150,800 普查、E=3 切片、3× SURVIVES）只在工作笔记中。→ 执行 W10 拼接后在 §4.2.1 加一句证据。

## 主题 F：前沿定位补强 —— C1/C2

（发现 #3/#5 + minor）
1. **Bound-and-Gap 未与最近的对标物比较**：Bertsimas & Kallus (2020, *Management Science*) 的 coefficient of prescriptiveness 已用 [0,1] 比值度量协变量信息对决策的价值；EVPI/VSS 亦然。→ §2 方法流加第四句 + §4.1.3 加一条 Remark：UB/LB/GAP 与 P 的对应（无条件基准 = 随机池，oracle = q_min），并精确陈述差异——本文是中位数、分区级，且 H_up（最差角余量）在 P 中无对应物。
2. **C1 只有模拟器描述、没有形式化陈述**：§3 目标函数只写"由评估引擎给出"，无决策变量、约束或结构性质；"分开优化会丢失瓶颈交互"的耦合论断从未被检验。→ §3.1 加半页形式陈述（订单池、分派变量 x_{o,w}、波次规模/放行约束、派送映射为固定算子的两阶段目标）+ 一条结构性质（经 §2 的"退化为平面子类"论证继承单层 makespan 分批的 NP 难）；耦合论断可用已有 Supp-1 运行注册一个小展示。
3. **运营前沿 2026 新作补引**（minor）：多层 MAPF-with-elevators（arXiv 2602.20512）、WareRover（arXiv 2602.13999）、Electronics 14(5):982 多层送货机器人——均任务集外生，反而巩固四要素缺口。
4. **Theorem R 的 Blackwell 类比**（minor）：五行括括证明配 Blackwell 反而招致"太容易"的质疑；改为 EVPI/VSS 在信息细化下非负性的分位数类比，并把 Theorem R 加入"理论声明与不声明"段。

# 三、按章节的行动清单（映射到 revision_0719）

| 章节 | 必做 | 来源发现 |
|---|---|---|
| 01 Abstract | 重写 Tool 2 定理句（"在支配成立处…"）；C3 句改双口径 + 去 "binding side" | A, B |
| 02 §1 | C2 段重计费 Prop 2/Theorem 1；Cor 2 措辞；Cor 1 适用句；C3 段双口径；可委托性降一格 | A, B, D, E6 |
| 03 §2 | 加 coefficient of prescriptiveness / EVPI 定位句；2026 三篇补引 | F |
| 04 §3 | 形式化陈述 + 结构性质；T/diurnal 改写；操作规则改写；A6；保真声明；参数 grounding；M1 表示措辞；平局约定 | C, F2 |
| 05 §4 | 最终 §4.2.1 与附录 X.4 起草；Theorem R 假设重述 + Cor 1 范围；U_c 措辞；D2-d 定性；"声明与不声明"段纳入 Theorem R | A, D, E1 |
| 06 §5 | §5.2 Amendment F 段 + A-R1 限定语；§5.3 一次写成（双口径、通道表、基率、C-4 价格）；§5.4 Table 4 补 P8/P9/枚举锚点 + P9 R>1；A4 改写；B-5 范围句一致应用 | A, B, E |
| 07 §6 | limitation (1)(4)(6) 重写；未来工作删已执行项；6.1 双口径 + 对冲代价 | B, C4, E4 |
| 代码 | simulator.py 平局键改索引；重跑自检 | C7 |
| 注册展示（不设门槛，复用数据） | C-4 加 minimax-regret 行；覆盖式份额并排（amendF 已有）；耦合论断小展示（Supp-1 复用） | A5, B1, F2 |

# 四、不需要做的事

- 不需要新的大规模实验，不需要真实数据（见 real_data_assessment_2026-07-19）。
- 不触碰冻结预注册与任何已锁判定（H-D1 PARTIAL、H-D2 PASS、D2-d PASS 的重定性不是重判）。
- 不改变理论本身：Prop 2 / Theorem 1 / Theorem R / Cor 2–3 的数学都未被质疑；被质疑的是**它们被卖成什么**。

# 五、被驳回的 4 条（供参考，勿再提）

反驳者驳回了：Theorem 1 "太容易"（W1 Edit 5/8 已自评）；Prop 3 "只是定义"（W1 Edit 2 已自评）；DRO 半径任意性（Remark B.6 已辩护）；"C1 formulation 缺形式化"的一个重复提法（合并进 F2）。
