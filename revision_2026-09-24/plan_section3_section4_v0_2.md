---
title: "路线 A 修改计划 v0.2 — Section 3 与 Section 4"
date: 2026-09-24
status: "计划稿 v0.2，替代 v0.1。v0.1 的 §3 条目（S3-01 到 S3-11）与 §4 重写基于过时底稿（根目录全文 docx 的旧 §3、2026-06-23 的 §4 草稿），不再执行；v0.1 中正确的理论诊断与两条 regret 界在本稿中保留并落到现行文本上。"
basis: "§3 基准：F:/Paper 3/Problem formulation.docx（2026-09-14 17:19，11 页，238 个公式对象）。§4 基准：F:/Paper 3/Methodology.docx（2026-09-17 21:42，7 页，157 个公式对象，公式 (33) 到 (46)）。§4 的 markdown 源：revision_2026-09-02/SECTION_4_METHODOLOGY.md（2026-09-14，公式 (33) 到 (58)）。主控：revision_2026-09-02/MASTER_REVISION_BY_SECTION.md §7.5 编号表、§0.3 证据标签。代码：prototype/src。QA：revision_2026-09-02/qa_2026-09-11/。"
scope: "只覆盖 §3、§4 及其直接依赖（一份 [NS] 枚举再分析、术语表、主控编号表）。Abstract/§1/§2/§5 的连带修改只记录在 §5 传播清单。"
---

# 路线 A 修改计划 v0.2：Section 3 + Section 4

## 0. 路线 A、本轮核查结论与 v0.1 的处置

**路线 A 的定位**：新问题框架 + 预注册大规模仿真 + 两个简单可用的诊断工具，属洞察型论文，目标 C&IE 首选、IJPR 备选。三条硬约束不变：理论陈述与证明强度相称；§3 每条运营规则能指到 `simulator.py` 的代码行；预注册结果不被替换，新分析以带标签的修正案并列进入。

**2026-09-24 核查结论**

| 项目 | 结论 | 证据 |
|---|---|---|
| §3 docx | 可定稿。9 月 14 日 17:19 版相对 12 日 22:29 版改动了 3.1 第 2 段、3.2.2、3.2.3（改用 $\pi^k$ 与 $(W^k,\pi^k)$ 记号）、式 (13)(16)、3.4.2 的均值句、3.5.1 的 lexargmin 定义、3.5.2 的 $M_2$ 解释段；全部与代码一致。只有一处回退：3.2.3 的 $\mathcal J_n=1,\ldots,n$ 再次丢失花括号 | PDF 第 3 页裁剪 |
| §4 docx | 不完整。转录到 4.3.2 的第二个反例为止；缺 4.3.2 的末两段与式 (47)、Fig. 4、整个 4.4（式 (48) 到 (58)、Theorem 2、Corollary 2 到 4、Fig. 5）。Hedge Rule 目前不在 §4 里 | docx 60 段，md 对应内容在第 306 到 505 行 |
| §4 反例 | 4.3.2 两个实例用生产模拟器复算：X1 得 $M_1=26$、$M_2=24$；X2 得 $M_1=103$、$M_2=68$，与正文逐位一致 | `simulate_wave` 直接调用 |
| v0.1 的 regret 界 | 在 Block C 六个配置上全部成立；$R_1$ 实现值 5 个为 0、config 11 为 $m_0$ 的 2.6%，界 $\Delta_{12}(q_1^\star)$ 为 $m_0$ 的 20.6% 到 32.5%；$R_3$ 实现值不超过 0.5%，界 $2\delta_3$ 为 2.9% 到 5.1% | 存量与 tie-break 修复后数据一致 |
| 覆盖分区（Theorem 1）的实证 | 目前没有。旧消融 A4 的 2×2 到 3×3 不嵌套 | 主控 §7.2 |
| 重跑成本 | 最重 setting 的 3000 候选 × 2 模型用 0.8 秒；36 个 setting 全池枚举约半分钟。v0.1 的"1 到 1.5 周机时"不成立 | 实测 |
| 四分位极角 cell 与角类的关系 | 只在"并列值划到低侧"约定下近似相等：36 个候选池中恰好落在 $Q_{0.75}(I)$ 的候选中位数占 5.9%，最多 19.5% | 实测 |

**v0.1 的处置**

| v0.1 内容 | 处置 |
|---|---|
| S3-01 到 S3-11 | 作废（针对旧 §3；定稿 §3 已无这些问题） |
| §4 重写（Prop 1 混合证明、Cor 1 嵌套、DRO 降为 Remark、Cor 2 在 $F_2^{-1}(1/2+\varepsilon)$ 取值） | 现行 md 已含等价内容（式 (42) 的中点约定夹逼、Theorem 1 嵌套、Corollary 3 只作均值比较、式 (53) 到 (55) 的端点分位数），不再重写 |
| Theorem 1 的 regret 界 (ii)(iii) | 采纳，并入本稿 S4-2 的 Theorem 2 |
| 主分区改为 2×2 中位数分区并重跑、旧结果入附录 | 不采纳：违反主控 §0.3。改为 [NS] 全池枚举再分析并列报告 |
| 撤销 D2-d 作为 gate | 不采纳：已通过的 gate 按主控 §2.4 措辞保留 |
| lower median 约定 | 不采纳：§3 3.4.2 与 §4 式 (42) 均已按中点约定完成 |
| T 改为 $\sigma_r/\Delta$ 并改名 | 见 D-2，推荐不改代码，只统一名称 |
| "cell" 替换 "class"、"setting" 替换 "sub-cell" | 前者不采纳（现行 §4 已用 class 指角类族、cell 指覆盖分区），后者采纳 |
| M1/M2 的文献锚点、相关系数句 | 采纳（S3-7；相关系数入 §5） |

---

## 1. 先拍板的决定（D-1 到 D-6）

| # | 决定 | 推荐 | 备选 | 影响 |
|---|---|---|---|---|
| D-1 | 分区方案 | 角类（§3.3.3 的 $\alpha$ 尾部交集）保持为预注册主方案；覆盖分区只用于 Theorem 1 与 Corollary 1 的实证，以 [NS] 全池枚举再分析并列报告（见 §4） | v0.1 方案：换主方案并重跑 | §5、预注册修正案 |
| D-2 | $T$ 的定义与名称 | 定义保留式 (8) 的变异系数；名称统一为 **ready-time dispersion**（§3 已用此词，方向正确：高 $T$ = 分散），TERMINOLOGY 中 "temporal clustering" 行改名；不改 `features.py` | 采纳 $\sigma_r/\Delta$：需新增 `temporal_dispersion`、改式 (8)、A2 消融按 [RA] 重算 | TERMINOLOGY、Abstract/§1 的轴名 |
| D-3 | §4 结果编号与强度 | Proposition 1（恒等式）、Proposition 2（class-action loss）、Theorem 1（嵌套覆盖分区细化，证明完整）、Corollary 1、Proposition 3（条件性排序，标 Proof sketch，附录 A 组装完成前不升格）、**Theorem 2 改为三段式 Hedge Rule**：(i) 有序时的简化 (49)，(ii) 有序时 $M_1$ 专属 regret 界，(iii) 任意评估器的 regret 界；Corollary 2（超额损失与 $U_q^{\mathrm{mid}}$）、Corollary 3（均值 Wasserstein 比较）保留；Corollary 4 并入 Theorem 2(iii) 后删除 | 若附录 A 先完成，则 Proposition 3 升为 Theorem 2、Hedge Rule 为 Theorem 3 | §4；主控 §7.5 |
| D-4 | 术语 | 角类族用 **class**，覆盖分区单元用 **cell**，实验单元用 **setting**（= configuration × evaluator × wave size，替换 "sub-cell"）；"corner class" 只在 §3.3.3 定义处出现 | 全文 "corner" 改 "cell" | TERMINOLOGY、§5 |
| D-5 | 统计约定 | 中点中位数不变。[NS] 枚举后，$M_1$、$M_2$ 的类中位数、池中位数与池最优在池内精确；$M_3$ 继续用 Block C 抽样估计 | 无 | §4.1.1、§5.1 |
| D-6 | D2-d | 保留为 [PR-C] gate，措辞用主控 §2.4："the corner-calibrated analytical equivalence was reproduced in 6/6 configurations"；Corollary 3 已说明半径逐类校准 | 撤销 | §5.3 |

---

## 2. §3 修改清单（基准：Problem formulation.docx 2026-09-14 17:19）

编号 S3-n。均为小项，不改变结构与公式编号。英文为可粘贴文本。

### S3-1 3.2.3 的 $\mathcal J_n$ 花括号（回退项）
- **位置**：3.2.3 第 1 段，式 (1) 之前。
- **现文**：The index $j\in\mathcal J_n=1,\ldots,n$ denotes a position in the sequence:
- **改后**：The index $j\in\mathcal J_n=\{1,\ldots,n\}$ denotes a position in the sequence:
- **原因**：9 月 12 日 22:29 版已修，14 日重写该句时 MathType 对象丢了花括号；式 (13)、(31) 把 $\mathcal J_n$ 当集合用。

### S3-2 表 3.2 的 $r_o$ 名称
- **现文**：$r_o\ge0$ | order-ready offset relative to $t_W$
- **改后**：$r_o\ge0$ | ready-time offset relative to $t_W$
- **原因**：A3、3.3.2 与式 (8) 的解释都用 "ready-time offset"。

### S3-3 表 3.3 标题句点
- **现文**：Table 3.3. Variables in the class and candidate formulations.
- **改后**：Table 3.3. Variables in the class and candidate formulations
- **原因**：与表 3.1、3.2 一致。

### S3-4 $T$ 的名称与在本节的角色（D-2）
- **位置 1**：3.3.2，式 (7) 之后。
- **现文**：Ready-time dispersion measures how order eligibility is spread within the wave.
- **改后**：The ready-time dispersion $T$ measures how order eligibility is spread within the wave.
- **位置 2**：3.3.3 首句。
- **现文**：The class construction uses the lower and upper tails of $C$ and $I$; $T$ records temporal variation separately.
- **改后**：The class construction uses the lower and upper tails of $C$ and $I$; $T$ records temporal variation separately and does not enter the corner classes or the selection problems of this section. It is retained in Equation (9) as a descriptor of the released wave under staggered ready times and is used only in the sensitivity analyses of Section 5.
- **原因**：审稿人会问为什么 $\Phi$ 的第三维在本节没有用处；同时给 $T$ 一个与方向一致的固定名称。

### S3-5 3.3.3 分位数约定
- **现文**：… let $Q_u(X)$ denote its empirical $u$-quantile over the candidate pool, computed by linear interpolation between order statistics.
- **改后**：… let $Q_u(X)$ denote its empirical $u$-quantile over the candidate pool, computed by linear interpolation between the adjacent order statistics at position $1+(K-1)u$ (the type 7 definition of Hyndman and Fan, 1996).
- **原因**：`np.quantile` 默认即 type 7；不写明则复现者可能取到不同的类边界。

### S3-6 式 (31) 的分页
- **现文**：引导句 "Resource conditions. The reservation rules enforce the following conditions, which are the feasibility requirements of the wave-level schedule:" 在第 9 页末，式 (31) 在第 10 页顶。
- **改后**：给引导段设"与下段同页"（Keep with next）。

### S3-7 3.5.1 的文献锚点（可选）
- **位置 1**：Throughput abstraction $M_1$ 段末，"…and in whether requests share a trip." 之后。
- **补句**：$M_1$ is the throughput-aggregation convention of Bartholdi and Hackman (2019).
- **位置 2**：True co-occupancy batching $M_2$ 段，"…uses a separate trip." 之后。
- **补句**：$M_2$ follows the explicit co-occupancy convention used for shared lifts and vehicles (Tadumadze et al., 2023; Chakravarty et al., 2025).
- **原因**：定稿 §3 目前没有任何文献锚点，A6 的"两种表示并存"需要出处。三条引用须先在 bib 中核对（v0.1 §6 已记录 Tadumadze 2023a/b 需合并）。

### S3-8 与 §4、§5 的接口（不改 §3 正文，记录依赖）
- 3.1 第 2 段 "a finite-pool benchmark whose exact value is obtained by evaluating all candidates under the specified evaluator"：[NS] 枚举完成后对全部 36 个 setting 成立；完成前只有 B-2 的 config 1、size 8 一个锚点。
- 3.3.1 "Section 5 states, for each experimental block, whether the pool is shared across evaluators"：§5.1 须写出 Block A 按 (config, model, size) 建池、Block C 与 [NS] 枚举按 (config, size) 建池。
- 3.3.3 "Section 5 reports the realized class sizes and overlaps"：§5 须给出角类占池比例（Block A 2.9% 到 15.0%，Block C 4.9% 到 14.7%，重叠 0）。
- 3.4.2 的均值句：D2-d 用均值计算、median 口径 5/6 一致、config 5 在 0.96% 边际内翻转，这三条披露落在 §5.3。

**§3 验收**：S3-1 到 S3-6 完成后 §3 定稿；S3-7 视 bib 核对结果决定；S3-8 是 §5 的义务。

---

## 3. §4 修改清单（基准：Methodology.docx 2026-09-17 21:42）

编号 S4-n。docx 现有内容（4.1 到 4.3.2 第二个反例）保留；以下先补全，再修正。所有新增公式的 LaTeX 以 md 为源，md 同步更新（主控 §1.1 规定 md 为 §4 当前正文）。

### S4-1 补齐 4.3.2 的末两段、式 (47) 与 Fig. 4
- **位置**：第二个反例 "…the reversal arises from the unfavorable repositioning distance in (d)." 之后。
- **来源**：md 第 306 到 319 行。补入两段：(a) "The examples show why (c) and (d) enter the sufficient conditions in Proposition 3. …"；(b) "For a class $q$, the same draw $\kappa\sim\nu_q$ is evaluated under both deterministic evaluators. If conditions (a)–(d) of Proposition 3 hold for every candidate in $\mathcal K_q$, then $Y_{\kappa M_1}\le Y_{\kappa M_2}$ almost surely. …" 及
$$F_{q1}(t)\ge F_{q2}(t)\ \text{for all } t,\qquad \mu^{0.5}_{qM_1}\le\mu^{0.5}_{qM_2}. \tag{47}$$
- 插入 Fig. 4（`revision_2026-09-02/figures/section4_2026-09-14/fig4_ordering_mechanisms_v1.png`）及 md 第 319 行的图注。
- **原因**：没有 (47)，4.4 的前提（类中位数有序）与 4.3 的逐波排序之间没有桥。

### S4-2 新增 4.4 Properties of robust class selection（含加强后的 Theorem 2）
来源为 md 4.4.1 到 4.4.3（第 323 到 505 行），按 D-3 调整。新的公式编号如下：(48) 记号；(49) 简化；(50) 新增 regret 界；(51) 到 (53) 对应 md 的 (50) 到 (52)；(54) 到 (56) 对应 md 的 (53) 到 (55)；(57) 到 (58) 对应 md 的 (56) 到 (57)；md 的 (58)（Corollary 4）删除。总编号仍为 (33) 到 (58)。

**4.4.1 的记号（md 式 (48)，保留）**
$$a_q=\mu^{0.5}_{qM_1},\qquad b_q=\mu^{0.5}_{qM_2},\qquad V_q=\max\{a_q,b_q\},\qquad q_H\in\arg\min_{q\in\mathcal Q}b_q. \tag{48}$$
补一句记号：Let $q_1\in\arg\min_{q\in\mathcal Q}a_q$ denote an $M_1$-optimal class and $\Delta_q:=b_q-a_q$ the evaluator gap of class $q$.

**Theorem 2（替换 md 的 Theorem 2，可粘贴）**

> **Theorem 2 (Model-Dominance Hedge Rule).** Let $R_1(q_H):=a_{q_H}-a_{q_1}$ denote the regret of the conservative choice when $M_1$ is the evaluator in force.
> (i) *Reduction.* If $a_q\le b_q$ for every $q\in\mathcal Q$, then $V_q=b_q$ for every class and
> $$\arg\min_{q\in\mathcal Q}\max\{a_q,b_q\}=\arg\min_{q\in\mathcal Q}b_q. \tag{49}$$
> (ii) *Regret under ordering.* Under the same premise, $0\le R_1(q_H)\le b_{q_H}-a_{q_1}\le\Delta_{q_1}$.
> (iii) *Regret under an arbitrary evaluator.* Let $m'$ be any evaluator with class medians $v_q$ defined by Equation (14), let $q'\in\arg\min_q v_q$, and let $\delta':=\max_{q\in\mathcal Q}|v_q-b_q|$. Then, without any ordering assumption,
> $$0\le v_{q_H}-v_{q'}\le 2\delta'. \tag{50}$$
> In particular, for $m'=M_3$ the regret of releasing from $q_H$ is at most $2\delta_3$, with $\delta_3$ the largest class-wise discrepancy between the $M_3$ and $M_2$ medians.
>
> **Proof.** (i) The premise gives $V_q=b_q$ for every selectable class; minimizing identical class scores yields the same optimal set. (ii) $a_{q_H}\le b_{q_H}\le b_{q_1}=a_{q_1}+\Delta_{q_1}$: the first inequality is the premise at $q_H$, the second is the $M_2$-optimality of $q_H$. Subtracting $a_{q_1}$ gives both bounds. (iii) Write $v_{q_H}-v_{q'}=(v_{q_H}-b_{q_H})+(b_{q_H}-b_{q'})+(b_{q'}-v_{q'})$. The middle term is at most zero by the $M_2$-optimality of $q_H$; each outer term is at most $\delta'$. $\square$

> 解释段（放在证明后）：Part (i) is the reduction used by the procedure of Section 4.1: under class-median ordering the robust decision is the $M_2$-optimal class, whatever the evaluator in force. Parts (ii) and (iii) price the decision. Under ordering the price is confined to the single class $q_1$ and is computable from the two deterministic class medians; without ordering, the generic bound (50) applies with $\delta'$ the largest class-wise discrepancy from $M_2$. Section 5 reports both bounds relative to the pool median $b_0$, together with the realized regrets.

- **保留**：md 4.4.1 中 "Equation (47) supplies one sufficient route to the premise …" 一段及其后关于估计目标的一段。
- **删除**：md 4.4.2 末段 "Evaluator-specific regret, such as $R_1(q_H)=a_{q_H}-\min_q a_q$, makes a different comparison and is evaluated separately." 改为 "Evaluator-specific regret is bounded in Theorem 2(ii)–(iii)."
- **4.4.2 Corollary 2**：按 md 保留，式 (50) 到 (55) 改号为 (51) 到 (56)；证明与 $U_q^{\mathrm{mid}}$ 定义不变。
- **4.4.3 Corollary 3**：按 md 保留，式 (56)、(57) 改号为 (57)、(58)；紧接的解释段保留 "This relation concerns the mean-based counterpart …" 一句。
- **Corollary 4 删除**：其内容（有限评估器族的简化）已被 Theorem 2(iii) 覆盖且不需要"同一评估器在每个类都最大"的前提；md 中 "Including $M_3$ in this extension requires its own median comparisons" 一句随之删除。
- **Fig. 5**：插入 `fig5_robust_selection_properties_v1.png`；图注 (c) 改为 "(c) The mean-based Wasserstein equality requires $F_{q1}(t)\ge F_{q2}(t)$ for all $t$ and every class; the regret bounds of Theorem 2 need no ordering for part (iii)." 图中 panel (c) 若印有 "finite-family median extension" 字样，需重生成。

**Theorem 2 的数值（写入 §5.3，此处备查，Block C，size 16，六个 E=2 配置）**

| config | $q_1$ | $q_H$ | $R_1/b_0$ | $\Delta_{q_1}/b_0$ | $R_3/b_0$ | $2\delta_3/b_0$ |
|---|---|---|---|---|---|---|
| 1 | LC_HI | LC_HI | 0 | 26.8% | 0 | 2.9% |
| 3 | LC_HI | LC_HI | 0 | 20.6% | 0 | 4.1% |
| 5 | HC_HI | HC_HI | 0 | 22.4% | 0 | 5.1% |
| 7 | LC_HI | LC_HI | 0 | 25.6% | 0 | 4.8% |
| 9 | HC_HI | HC_HI | 0 | 32.5% | 0 | 4.0% |
| 11 | HC_LI | LC_LI | 2.6% | 32.0% | 0.5% | 4.3% |

读法：(iii) 的界紧到可作 §5 的 worst-case 数字；(ii) 的界比实现值大一个量级，只能作为保守界报告，不能写成"worst-case loss"头条。

### S4-3 式 (36) 与 §3 的重复定义
- **现文**：$\nu_0(k)=1/K,\ b_0=\mathrm{Med}_{\kappa\sim\nu_0,\xi}Y_{\kappa m}(\xi),\ b_q=\mu^{0.5}_{qm}$ (36)，正文 "This pool distribution is denoted by $\nu_0$".
- **改后**：正文改为 "The reference choice draws uniformly from the entire candidate pool, with the distribution $\nu_0$ of Section 3.3.3"; 式 (36) 只保留 $b_0$ 与 $b_q$ 两个定义。
- **原因**：一处定义（AGENT.md 第 4 条）；$\nu_0$ 已在 §3.3.3 定义。

### S4-4 $q_\Phi$ 段与 §3 的矛盾
- **现文**（4.2.1）：Its fitting procedure, treatment of tied scores, and handling of empty corner supports form part of that rule.
- **改后**：Its fitting procedure and treatment of tied scores form part of that rule.
- **原因**：§3.3.3 要求 $\mathcal K_q\neq\varnothing$ 对每个 $q$ 成立，代码遇空类报错（2026-09-11 QA），不存在"空类处理"。

### S4-5 引用格式
- **现文**（4.2.2）：(Adam N. Elmachtoub & Paul Grigas, 2021)
- **改后**：(Elmachtoub and Grigas, 2022)
- **原因**：TERMINOLOGY 规定用期刊年份（Management Science 68(1), 2022）；Word 引文源需改为姓氏格式。

### S4-6 4.1.1 的"精确"与 Phase 5 的抽样
- **现文**：For each class and evaluator, the deterministic median is obtained exactly from one equally weighted outcome per candidate in its support, retaining repeated outcome values:
- **改后**：For each class and evaluator, the deterministic median is obtained exactly by evaluating every candidate in the class support once, with one equally weighted outcome per candidate and repeated outcome values retained:
- **补句**（式 (34) 之后 "Section 5 specifies the sampling sizes and uncertainty analysis." 改为）：Section 5 states, for each result, whether class scores come from complete enumeration or from Equation (34), and gives the sampling sizes and uncertainty analysis for the latter.
- **原因**：预注册 Block A/C 用式 (34) 的 200 次有放回抽样；[NS] 枚举后 $M_1$、$M_2$ 的分数按式 (33) 精确。两种口径都会出现在 §5，须在 §4 先说清。

### S4-7 Proposition 3 的标签与附录
- 保留 "Proposition" 与 "Proof sketch"。附录 A（Lemma 3 到 6 的归纳）组装并经作者通读前不升格；升格后按 D-3 备选方案重编号。
- 两个反例已用生产模拟器复算一致（26/24；103/68），在 §5.1 的复现性说明中记一句 "the two instances of Section 4.3.2 are reproduced by the released simulator".

### S4-8 新增 4.5 What Section 5 tests（约 150 词）
> Section 5 evaluates the results of this section as follows. For Proposition 1, the identity $\mathrm{GAP}=H_{\mathrm{up}}+M_\Phi$ and the bounds in Equation (40) are reported as checks; the pre-registered gate is signal resolution, whether the bootstrap interval of $\mathrm{GAP}$ excludes zero. For Theorem 1 and Corollary 1, the nested $2\times2$ and $4\times4$ covering partitions of the enumerated candidate pools are compared. For Proposition 3, the frequency of conditions (a)–(d) and the frequency of the ordering in Equation (46) are reported separately. For Theorem 2, the class-median ordering of Equation (47), the coincidence of the robust and $M_2$-optimal classes, and the realized regrets against the bounds of parts (ii) and (iii) are reported. For Corollary 2, $U_q^{\mathrm{mid}}$ is compared with the ranking margin. For Corollary 3, the mean-based coincidence is reported as an analytical consistency check. Pre-registered results, registered amendments, and re-analyses are labeled as such.

### S4-9 其他核对项（无需改动，记录）
- 式 (33) 到 (46) 的 LaTeX 与 md 一致；§4 用的 $\mathcal K_q$、$\nu_q$、$Y_{km}$、$\mu^{0.5}_{qm}$、$\mathcal M_D$、$W^k$、$\pi^k$、$q^\star$ 与定稿 §3 一致。
- 4.1.2 "A fixed class-label order resolves ties" 与 `analysis_phase5_blockC.py` 的 `min(cmap, …)`（按 HH、HL、LH、LL 顺序）一致。
- 式 (38)、(39) 与 `analysis_phase5_blockA.py` 的 `decompose` 逐项一致。
- 禁用表述扫描：无 "closed-form"、"chain"、"capacity-side"、"two-stage"、"event-driven"（主评估器）、破折号；拼写为美式。

**§4 验收**：S4-1、S4-2 完成后 §4 才包含 C2 的全部内容；S4-3 到 S4-6 为一致性修正；S4-7 是附录门槛；S4-8 是与 §5 的交接。

---

## 4. [NS] 修正案：全池枚举再分析（不重跑预注册块）

**目的**：给 Theorem 1、Corollary 1 提供嵌套覆盖分区的实证；把 $M_1$、$M_2$ 下的类中位数、池中位数、池最优 (17)、角类规模与重叠从"抽样估计"变为"池内精确"；计算 Theorem 2 的界。全部是对既有候选池的枚举，不改变任何预注册结果。

**登记文本草稿（追加为预注册 §9.3，运行前 commit）**

> ## 9.3 Amendment 3 — complete enumeration of the candidate pools (2026-09-24)
> **Trigger.** A theorem audit found that the refinement result of Section 4.2.3 requires nested, disjoint, covering partitions, whereas the pre-registered ablation A4 compared a $2\times2$ and a $3\times3$ partition that are not nested. The same audit noted that the deterministic class medians of Equation (33) can be computed exactly because the closed-form evaluators evaluate a 3,000-candidate pool in under one second.
> **Changes.** (a) For every pre-registered (configuration, wave size) pool, all candidates are evaluated once under $M_1$ and $M_2$ from the registered seeds. (b) Exact class medians, pool median, pool optimum, corner-class sizes and overlaps, and the signed components of Proposition 1 are reported beside the pre-registered sampled values. (c) The nested $2\times2$ (median split) and $4\times4$ (quartile split) covering partitions of $(C,I)$ are built on the same enumerated pools with ties assigned to the lower cell; Theorem 1 and Corollary 1 are checked on them. (d) The bounds of Theorem 2(ii)–(iii) and Corollary 2 are computed for the six Block C configurations, with $M_3$ medians taken from the pre-registered Block C sample.
> **Gates.** None. All pre-registered gates and verdicts (H-D1 PARTIAL, H-D2 PASS, H-Policy) are unchanged and remain the confirmatory results. This amendment is labeled [NS] and was written before the enumeration was run.

**代码**

| # | 文件 | 内容 |
|---|---|---|
| E-1 | `prototype/src/experiments_v0_6_enumerate_pool.py` | 对 36 个 (config, size) 池按注册种子重建候选，逐候选评估 $M_1$、$M_2$；输出每行 candidate_id、C、I、T、两模型 makespan |
| E-2 | `prototype/src/partition.py` | `grid_partition(cand, axes=("C","I"), cuts)`：切点在同一池上算一次并冻结；并列值划到低侧；返回 cell 标签 |
| E-3 | `prototype/src/analysis_v0_6_enumeration.py` | 精确 $b_q$、$b_0$、(17)、角类规模与重叠、Proposition 1 各项；2×2 与 4×4 的 Theorem 1 检查；Theorem 2 与 Corollary 2 的界 |

**不做**：不新增基线；不改 $T$ 的代码；不改中位数约定；不重跑 Block A/B/C。

---

## 5. 传播清单（下一轮执行，本轮只记录）

| 位置 | 内容 | 触发 |
|---|---|---|
| TERMINOLOGY.md | 新增 "setting = configuration × evaluator × wave size（替换 sub-cell）"；"T = ready-time dispersion（CV；高 T = 分散）" 替换 "temporal clustering"；注明 class（角类族）与 cell（覆盖分区）的区分 | D-2、D-4 |
| 主控 §7.5 | Theorem 2 内容改为三段式；Corollary 4 删除；式 (48) 到 (58) 的新对应 | D-3 |
| 主控 §6 | §3 节结构改为定稿的 3.1 到 3.5 | 已定稿的 §3 |
| Abstract、§1 C2 段 | "temporal clustering" 改名；C2 的措辞改为 "a conditional evaluator-ordering proposition and a hedge theorem with computable regret bounds" | D-2、D-3 |
| §5.1 | 各结果的口径标签（枚举 / 式 (34) 抽样）；候选池是否跨评估器共享；两个反例的复现句 | S4-6、S4-7 |
| §5.2 | 角类规模与重叠；Proposition 1 的精确值并列 | S3-8、§4 |
| §5.3 | Theorem 2 的界与实现 regret（上表）；D2-d 用均值、median 口径 5/6、config 5 翻转 | S4-2、D-6 |
| §5.5 | Theorem 1 的嵌套 2×2 到 4×4 检查替换旧 A4 的读法 | §4 |
| SECTION_4_METHODOLOGY.md | 与 docx 同步 S4-1 到 S4-8 | 主控 §1.1 |

---

## 6. 验收清单

**§3**
- [ ] S3-1 花括号已恢复；S3-2、S3-3 名称与标题一致；S3-4 的 $T$ 名称与角色句已加；S3-5 分位数约定已注明；S3-6 式 (31) 与引导句同页。
- [ ] S3-7 的三条引用在 bib 中核对后再加。

**§4**
- [ ] 4.3.2 含式 (47) 与 Fig. 4；4.4 含式 (48) 到 (58)、Theorem 2（三段）、Corollary 2、Corollary 3、Fig. 5；无 Corollary 4。
- [ ] 式 (36) 不再重定义 $\nu_0$；$q_\Phi$ 段无 "empty corner supports"；引用为 (Elmachtoub and Grigas, 2022)。
- [ ] 4.1.1 区分枚举与抽样；4.5 与 §5 的 gate 一一对应。
- [ ] Proposition 3 仍标 Proof sketch，附录 A 组装为独立门槛。
- [ ] md 与 docx 同步。

**流程**
- [ ] 预注册 §9.3 在 E-1 运行前提交并 commit；枚举结果以 [NS] 标签与 [PR-C] 结果并列，不替换任何判定。
