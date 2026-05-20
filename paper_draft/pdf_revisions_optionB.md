---
title: "PDF 定稿内容修改对照 — Option B + methodology 定位 + §3-实现对齐 + §2-bridges 深化（最终完整方案 v2）"
date: 2026-05-20
purpose: "当前 PDF (Abstract/§1/§2/§3) 全部需要修改的部分，附修改前后对照。涵盖 (a) Option B 的 C3 收缩，(b) methodology 定位，(c) §3 与代码实现的 4 处对齐 + Abstract 轴名连带，(d) §2 把 D1/D2 显化为 bridge 并补 Wasserstein-DRO 文献根基。"
status: "完整 v2 —— 已修正 v1 的两处遗漏 (Abstract 轴命名、§2 开头/结尾'two threads')"
---

# PDF 定稿内容修改对照表（最终完整版 v2）

## 适用范围

当前 PDF 定稿 = **Abstract、Introduction、Related Works、Problem Formulation**（§1–§3）。§4、§5 不在 PDF（以 [section4_draft_v0_1.md](section4_draft_v0_1.md) / [section5_draft_v0_1.md](section5_draft_v0_1.md) 存在,属新增章节)。

- **需要修改**:**Abstract**(贡献句 **+ Φ 轴命名句**);§1 的 C2 段 / C3 段 / "operational implication"句 / "two tools"预告段;**§2 的 methodology 段(整段重写 + 开头/结尾的 "two threads" 措辞**同步更新**)**;§3 的 4 处与实现对齐。
- **不需要修改**:§2 的*问题类*线(4 个 problem-class threads 不动);§3 的其余部分。

**四个驱动因素**:
- **(a) Option B** —— C3 三 outcome → 两(修改 1–4)。
- **(b) methodology 定位** —— 软化 §1 残留的"binding lever"口径(修改 5)。
- **(c) §3 与实现对齐** —— C 公式与语义、I 分母、d_o 同层、调度策略 + Abstract 轴名连带(修改 6–9 + 修改 11)。
- **(d) §2 把 D1/D2 显化为 bridge** —— 否则 §4 prove "equal"、§2 写 "differ" 自相矛盾(修改 10,**含 §2 开头+结尾的 "two threads" 同步更新**)。

> 注:"...constitute **three contributions** of this paper"一句**不用改** —— 指 C1/C2/C3,仍三个。

---

# 第一组：Option B 改动（C3 三 outcome → 两）

## 修改 1 — Abstract,贡献句

**原文 (PDF p.1)**:
> The framework then delivers **three managerial outcomes**: from this decomposition, **(i) a regime-level diagnostic that tells operators which lever to pull, such as wave design, additional elevator capacity, or neither**; from the hedge rule, (ii) a closed-form dispatch policy that operators apply without identifying the true elevator model online, with worst-case loss bounded against any model-specific optimum; and combining the two, **(iii) a tactical–operational substitutability map that identifies the regimes in which wave-composition redesign substitutes for capacity expansion**.

**改后**:
> The framework then delivers **two managerial outcomes**: from the decomposition, **(i) a structural account of the value of wave design, separating a partition-intrinsic upper-tail component from a component a better policy can recover**; and from the hedge rule, (ii) a closed-form dispatch policy that operators apply without identifying the true elevator model online, with worst-case loss bounded against any model-specific optimum.

**原因**:Option B 把 C3 收缩为 2 个 outcome;(i) 由"regime 分类器"改为"结构分解";(iii) substitutability map 大规模无 regime 区分度,删除。

---

## 修改 2 — Introduction,C2 段（一处短语）

**原文 (PDF p.3)**:
> The Bound-and-Gap framework decomposes the value of wave-structure information into two non-negative components on a structured representation Φ = (C,I,T) of wave composition, **yielding a regime-level diagnostic over wave design, elevator capacity, and a do-nothing option**.

**改后**:
> The Bound-and-Gap framework decomposes the value of wave-structure information into two non-negative components on a structured representation Φ = (C,I,T) of wave composition, **separating a partition-intrinsic upper-tail component from a recoverable policy component**.

**原因**:Bound-and-Gap 是结构分解,不是 regime 分类器。C2 段其余文字不动。

---

## 修改 3 — Introduction,C3 段（整段重写）

**原文 (PDF p.3)**:
> **Empirical insights (C3)**: **Three managerial outcomes** from the two tools translate into operational gains. **First, the Bound-and-Gap diagnostic prospectively classifies, before any policy run, the operating regimes in which destination-clustered batching outperforms first-come, first-served dispatch, turning a post hoc decomposition into a forward-looking signal of where tactical wave design will pay off.** Second, the Hedge Rule's per-wave dominance condition holds at higher elevator capacities than the low-capacity setting for which the rule was derived, extending its reach without re-derivation. **Third, combining the two tools yields a tactical-operational substitutability map that identifies, regime by regime, when wave-composition redesign substitutes for elevator-capacity expansion.**

**改后**:
> **Empirical insights (C3)**: **Two managerial outcomes** follow from the two tools, established by pre-registered publication-scale simulation. **First, structured wave-and-dispatch design delivers a broad and substantial makespan reduction: destination-clustered dispatch lowers makespan by roughly 10% across the tested warehouse configurations, and the Bound-and-Gap decomposition characterizes the structure of this value, separating the partition-intrinsic headroom from the component a better policy can recover.** Second, the Hedge Rule's per-wave dominance condition holds at elevator capacities beyond the low-capacity setting for which the rule was derived — confirmed across c ∈ {2,3,4,5} — extending the rule's reach without re-derivation.

**原因**:"Three"→"Two";原 First 被 Supp-1 推翻(clustering 12/12 普遍降 ~10%,F=3 假象不复存在);原 Third 删除;Second 加"confirmed across c ∈ {2,3,4,5}"(Supp-2)。

---

## 修改 4 — Introduction,C3 段后的"operational implication"句

**原文 (PDF p.3)**:
> The operational implication is that the same warehouse data that informs heuristic batching decisions can, with these tools, support **quantified diagnoses about which lever to pull and the worst-case cost**.

**改后**:
> The operational implication is that the same warehouse data that informs heuristic batching decisions can, with these tools, support **a quantified account of where structured wave design adds value and of the worst-case cost of model misspecification**.

**原因**:"which lever to pull"已被 Supp-1 削弱,改为中性可支撑措辞。

---

# 第二组：methodology 定位改动

## 修改 5 — Introduction,"two tools"预告段（Bound-and-Gap 句尾）

**原文 (PDF p.2)**:
> We develop two analytical tools to address these features. The first is a Bound-and-Gap framework: a decomposition theorem that splits the value of wave-structure information into two non-negative components **and, regime by regime, tells operators whether wave design or elevator capacity is the binding lever**. The second is a Model-Dominance Hedge Rule: ...

**改后**:
> We develop two analytical tools to address these features. The first is a Bound-and-Gap framework: a decomposition theorem that splits the value of wave-structure information into two non-negative components **— a partition-intrinsic upper-tail component and a recoverable policy component**. The second is a Model-Dominance Hedge Rule: ...

**原因**:去掉"binding lever"的 regime-分类器口径;Hedge Rule 那一句不动。

---

# 第三组：§3 与代码实现对齐（+ Abstract 轴名连带）

## 修改 6 — §3 结构化特征 C(W) 定义（**最严重:语义反向**）

**原文 (PDF p.7)**:
> **Vertical concentration C(W) ∈ [0, 1]**: It shows how tight orders share destination floors. C(W) = 1 − H_dst(W)/log₂ F, H_dst(W) = − ∑_{f∈F} p_f(W) log₂ p_f(W), where p_f(W) = |{o∈W: d_o=f}|/|W| ... **C = 1 when all orders share one floor; C = 0 when destinations spread uniformly.**

**改后**:
> **Vertical activity diversity C(W) ≥ 0**: Shannon entropy (natural logarithm) of the empirical floor distribution taken over the *union of source and destination floors* of orders in W. With p_f(W) = (|{o ∈ W : s_o = f}| + |{o ∈ W : d_o = f}|) / (2|W|), define C(W) = −∑_{f∈F} p_f(W) ln p_f(W) (with 0 ln 0 = 0). **High C indicates orders span many floors (vertical activity is diversified); low C indicates concentration on few floors.** We treat C as a conceptual measure of vertical activity rather than a normalized [0,1] index.

**原因**:与 `features.py:vertical_concentration` 对齐:源+目的合并、自然对数、不归一化、语义反向(高 C = 多样)。**变量名从"Vertical concentration"改为"Vertical activity diversity"**。

> **符号助记说明(诚实写出)**:保留符号 C 作为变量(虽然新名称"diversity"不再以 C 起首);corner 标签 HC/LC 沿用,统一释为"高/低 C 值 = 高/低 多样性"。这是 label 级选择,不影响公式。**§4 草稿的 corner 标签也据此更新**(目前 §4 草稿只把 HC/LC 当 label,不带旧"集中"语义,所以兼容)。

---

## 修改 7 — §3 结构化特征 I(W) 定义

**原文 (PDF p.7)**:
> Directional imbalance I(W) ∈ [0, 1]: ... I(W) = ||W↑| − |W↓|| **/ |W|**, ... (each order is one or the other, **since d_o ≠ s_o**) ...

**改后**:
> Directional imbalance I(W) ∈ [0, 1]: It shows how one-directional the wave's cross-floor vertical traffic is, computed over the cross-floor portion of W. With W↑ = {o ∈ W : d_o > s_o} and W↓ = {o ∈ W : d_o < s_o} (same-floor orders are excluded from both sets), I(W) = ||W↑| − |W↓|| **/ (|W↑| + |W↓|)** when |W↑|+|W↓| > 0, and I(W) = 0 otherwise.

**原因**:与 `features.py:directional_imbalance` 对齐。

---

## 修改 8 — §3 订单属性 d_o 的可行性

**原文 (PDF p.6 Order attributes)**:
> d_o ∈ ℱ, **d_o ≠ s_o**: destination floor of order o

**改后**:
> d_o ∈ ℱ: destination floor of order o. The trivial floor-1 same-floor pair (s_o, d_o) = (1, 1) is excluded from O; same-floor orders on floors ≥ 2 remain in O because the assigned AMR still requires the elevator to reach that floor.

**原因**:与 `experiments.build_order_pool` / `demand_patterns._feasible_pairs` 对齐。

---

## 修改 9 — §3 运营调度策略（**修订:把 cluster 定位为实验处理因子,不是第二个决策变量**）

> **v2 修订**:你提的"a small set"与 §3 "single decision variable / operational layer carries no decision variables"有张力;把 cluster 定位为 §5 的*实验处理因子*,不让它升格为决策变量。

**原文 1 (PDF p.6,两层架构段)**:
> ...decisions we delegate to a deterministic dispatch policy (**capacity-bounded FIFO boarding** under elevator model M ∈ M)...

**改后 1**:
> ...decisions we delegate to a **deterministic dispatch policy, defaulting to capacity-bounded FIFO boarding under elevator model M ∈ M. Section 5 additionally evaluates a destination-clustered alternative as an experimental treatment factor (not as an additional decision variable of the formulation).**

**原文 2 (PDF p.7, Assumption A3)**:
> **Capacity-bounded FIFO boarding.** AMRs join the elevator queue in arrival order and board up to c at a time under elevator model M.

**改后 2**:
> **Capacity-bounded FIFO boarding (default).** AMRs join the elevator queue in arrival order and board up to c at a time under elevator model M. The destination-clustered alternative evaluated in Section 5 follows the same capacity bound and boarding semantics, differing only in the order in which queued AMRs board the next trip.

**原因**:与 `simulate_wave` 的 `policy ∈ {"fifo","cluster"}` 和 §5 C3-① 头条(cluster 降 ~10%)对齐,**同时保护 §3 "single decision variable"的干净叙述** —— cluster 是 §5 的处理因子,不是 §3 决策空间的扩展。

---

## 修改 11 — Abstract,Φ 轴命名句（**propagates 修改 6 to Abstract**）

> **v2 新增**:修改 6 把 §3 的 C 重命名为"Vertical activity diversity",但 Abstract 仍写"vertical concentration",会造成 Abstract 与 §3 术语不一致。

**原文 (PDF p.1)**:
> ...instantiated here on a three-dimensional Φ = (C, I, T) of wave composition, **namely vertical concentration, directional imbalance, and temporal clustering**; the theorem splits the value of wave-structure information into two non-negative components.

**改后**:
> ...instantiated here on a three-dimensional Φ = (C, I, T) of wave composition, **namely vertical activity diversity, directional imbalance, and temporal clustering**; the theorem splits the value of wave-structure information into two non-negative components.

**原因**:与修改 6 一致(Abstract 与 §3 术语统一)。

---

# 第四组：§2 methodology 段深化（把 D1/D2 显化为 bridge）

> **v2 修订**:不仅重写 §2 的 methodology 段(原修改 10),还**同步更新 §2 开头段和结尾段**对 "two methodological threads" 的引用 —— 否则中间改成 3 条线,开头说 "two threads / 1:1 对应"、结尾说 "two threads each provide tools" 会自相冲突。

## 修改 10 — §2 整段重写(三处:开头段 + methodology 段 + 结尾段)

### 修改 10a — §2 开头段（PDF p.3）

**原文**:
> We organize the relevant literature into four problem-class threads that share aspects of our physical setting and **two methodological threads** that pertain to our analytical apparatus. The four problem-class threads jointly establish the gap that motivates our problem formulation (C1), and **the two methodological threads each correspond to one of the two analytical tools we develop (C2)**. The problem-class threads are: ... The **methodological threads are prediction-to-decision regret (Elmachtoub & Grigas, 2020; Vera et al., 2020) and robust scheduling under model uncertainty (Lu & Shen, 2021; Wiesemann et al., 2013)**.

**改后**:
> We organize the relevant literature into four problem-class threads that share aspects of our physical setting and **three methodological threads** that pertain to our analytical apparatus. The four problem-class threads jointly establish the gap that motivates our problem formulation (C1); **two of the methodological threads connect to our analytical tools (C2) by equivalences proven in Section 4 (prediction-to-decision regret and Wasserstein distributionally robust optimization), and the third positions our tools by structural contrast (robust scheduling under parametric model uncertainty)**. The problem-class threads are: ... The **methodological threads are prediction-to-decision regret (Elmachtoub & Grigas, 2020; Vera et al., 2020; Chenreddy & Delage, 2023), Wasserstein distributionally robust optimization (Mohajerin Esfahani & Kuhn, 2018; Blanchet & Murthy, 2019; Gao & Kleywegt, 2023), and robust scheduling under model uncertainty (Lu & Shen, 2021; Wiesemann et al., 2013)**.

### 修改 10b — §2 中段 methodology 段（PDF p.4–5,倒数第二段）

**原文**:
> Two methodological threads inform our analytical apparatus, each addressing a distinct gap. The prediction-to-decision regret literature (Elmachtoub & Grigas, 2020; Vera et al., 2020) bounds algorithmic loss when a learned predictor drives a downstream optimizer; ... Our Bound-and-Gap framework formalizes that post-hoc information value as a non-negative decomposition into a partition-intrinsic upper-tail term (H_up) and a Φ-policy slack term (M_Φ). Robust scheduling under model uncertainty (Lu & Shen, 2021; Wiesemann et al., 2013) hedges against parametric variation within a known model class. ... Our Model-Dominance Hedge Rule collapses this structural model-class disagreement into a single closed-form decision under a per-wave dominance condition, with a worst-case loss bound that requires no online model selection.

**改后(整段替换,~300 词)**:
> Three methodological threads inform our analytical apparatus; the first two are connected to our tools by precise equivalences proven in Section 4, the third by a structural contrast.
>
> First, the **prediction-to-decision regret** literature (Elmachtoub & Grigas, 2020; Vera et al., 2020; Chenreddy & Delage, 2023) bounds the algorithmic loss when a learned predictor drives a downstream optimizer. Theorem 1 (Section 4.1.2) gives this regret a *partition perspective*: the policy-slack component M_Φ of our decomposition equals the Smart-Predict-then-Optimize regret of the partition-constant predictor class, so the literature's training-time regret object and our post-hoc, structured-feature decomposition refer to the same underlying quantity on a finite partition. Our contribution is the decomposition itself, which separates this SPO regret from an independent partition-intrinsic headroom term H_up.
>
> Second, **Wasserstein distributionally robust optimization** (Mohajerin Esfahani & Kuhn, 2018; Blanchet & Murthy, 2019; Gao & Kleywegt, 2023) hedges decisions against worst-case distributions within a transport-distance ambiguity ball of a nominal model, typically reformulated as a convex program. Theorem 2 (Section 4.2.2) shows that under a chain of per-wave stochastic dominance conditions, our minimax wave-corner selection over {M_1, M_2, M_3} coincides with the Wasserstein-DRO solution at the appropriate ambiguity radius, collapsing the convex DRO program into a closed-form one-line rule. Our contribution is the dominance-conditional collapse, exploiting an empirically verified structural property to replace optimization with identification.
>
> Third, **robust scheduling under model uncertainty** (Lu & Shen, 2021; Wiesemann et al., 2013) hedges against parametric variation within a single agreed-upon model class. Our elevator-modeling uncertainty is structurally different: throughput aggregation and true co-occupancy batching are qualitatively distinct models, not parameterizations of one family. The Model-Dominance Hedge Rule addresses this *structural* model-class disagreement rather than parametric uncertainty within a class.

### 修改 10c — §2 结尾段（PDF p.5）

**原文**:
> The four problem-class threads each address one aspect of the wave-elevator coupling, but none integrates all four; **the two methodological threads each provide tools that close a specific gap in our methodology**. The empirical findings demonstrating these contributions in action are deferred to Sections 5 and 6.

**改后**:
> The four problem-class threads each address one aspect of the wave-elevator coupling, but none integrates all four; **the three methodological threads connect to our methodology in distinct ways — two by precise equivalences proven in Section 4, the third by structural contrast in the type of uncertainty handled**. The empirical findings demonstrating these contributions in action are deferred to Sections 5 and 6.

**原因(修改 10 全部三处共同)**:
- (i) §2 从 2 条 methodology 线扩为 3 条;前两条由 contrast 改为 bridge(D1/D2 在 §4 prove equivalence,§2 必须呼应);
- (ii) **新增 Wasserstein-DRO 整条线**(D2 的方法论根基);
- (iii) 第三条(robust scheduling)保留 contrast;
- (iv) **开头段 + 结尾段对"two threads"的引用同步更新**,避免与重写后的中段冲突 —— 否则 §2 自身就自相矛盾。

### 修改 10 需要新增的 4 篇引用（已核对存在性 + 主要出版信息）

| # | 引用 | 真实出处 | 验证号 |
|---|---|---|---|
| R1 | **Mohajerin Esfahani, P., & Kuhn, D. (2018).** Data-driven distributionally robust optimization using the Wasserstein metric: performance guarantees and tractable reformulations. *Mathematical Programming*, 171(1), 115–166. | Math. Prog. 2018, 171(1) | DOI: `10.1007/s10107-017-1172-1` |
| R2 | **Blanchet, J., & Murthy, K. (2019).** Quantifying distributional model risk via optimal transport. *Mathematics of Operations Research*, 44(2), 565–600. | MOR 2019, 44(2) | DOI: `10.1287/moor.2018.0936` |
| R3 | **Gao, R., & Kleywegt, A. J. (2023).** Distributionally robust stochastic optimization with Wasserstein distance. *Mathematics of Operations Research*, 48(2), 603–655. | MOR 2023, 48(2)(arXiv 原:1604.02199) | DOI: `10.1287/moor.2022.1275` |
| R4 | **Chenreddy, A., & Delage, E. (2023).** End-to-end conditional robust optimization. | arXiv 预印本 | arXiv: `2305.19225` |

> **v2 修订**:R1 第一作者**著录为 "Mohajerin Esfahani, P."**(姓氏为 *Mohajerin Esfahani*,复合姓;此前 v1 用的 "Esfahani, P. M." 是次优写法)。最终落 BibTeX 前请用 DOI 再核一遍(尤其页码、作者顺序)。

---

## 可选 / 建议复核

| # | 位置 | 现状 | 建议 |
|---|---|---|---|
| O1 | Abstract | "pre-registered simulation experiments" | 强化为 "**pre-registered, publication-scale simulation study**"。建议改。 |
| O2 | Intro "two structural features"第 1 条 | "varies systematically across regimes" | 可略软化;非强制。 |
| O3 | Intro "two structural features"第 2 条 | "92.5–100% of waves" | 加"(confirmed at ≈99% at publication scale, Section 5)"。 |
| O4 | C2 段 | "hedges across **two** structural model classes" | 与 abstract {M1,M2,M3} 三模型链不一致,改为 "a chain of structural model classes"。 |
| O5 | Abstract / §1 | (无) | 可加一句明确"methodological contribution",非必须。 |

### 引用年份核验（**v2 建议:全文统一一种约定**）

| V# | 位置 | PDF 当前 | 实际正式版 | 说明 |
|---|---|---|---|---|
| V1 | §2 prediction-to-decision regret | Elmachtoub & Grigas, **2020** | *Mgmt Sci* 68(1), 9–26, **2022** | PDF "2020" 疑为 arXiv 年份 |
| V2 | §2 同上 | Vera et al., **2020** | *OR* 69(3), 821–840, **2021** | 同上 |
| V3 | §2 surveys | Boysen et al., **2017**("50 years of warehousing research") | Boysen & de Koster, *EJOR* 320(3), 449–464, **2025** | 与"fifty years of evolution"叙述对应应是 2025 那篇 |

**v2 修订建议:全文统一一种引用年份约定** —— 要么全用 arXiv 年份(早),要么全用正式期刊年份(晚)。我在修改 10 的英文段里**沿用 PDF 当前的"2020"**(暂保持 §2 内一致),但 V1/V2/V3 一旦你定了约定,需全文(包括修改 10 段)统一替换。建议用**正式期刊年份**(更标准、reviewer 一查 DOI 即对),即 Elmachtoub 2022、Vera 2021、Boysen 2025。

---

## 小结

**必须改 11 处**,四组:

| 组 | 修改 | 位置 | 核心 |
|---|---|---|---|
| 第一组 Option B | 1–4 | Abstract + §1 | C3 三 outcome → 两;regime-分类口径 → 结构分解 + 普遍 ~10% |
| 第二组 methodology 定位 | 5 | §1 | "binding lever"口径去掉 |
| 第三组 §3-实现对齐(+ Abstract 轴名连带) | 6–9, **11** | §3 + **Abstract** | C 公式/语义对齐(改名 diversity);I 分母;允许同层订单;调度策略含 FIFO + cluster(cluster 定位为 §5 处理因子);**Abstract 轴名同步** |
| 第四组 §2-bridges 深化 | 10(三处:**开头 + 中段 + 结尾**) | §2 | methodology 段从 2 条 contrast → 3 条(2 bridge + 1 contrast);新增 Wasserstein-DRO 整条线 + 4 篇引用;**开头/结尾 "two threads" 同步更新** |

加 O1–O5 可选;V1–V3 年份核验(建议全文统一用正式期刊年份)。

改后 PDF 的 Abstract + §1 + §2 + §3 与新增 §4 / §5 **全面贯通且 §2 内部自洽**:
- 同走 Option B;
- 同为 methodology 定位;
- 同用 Phase 5 诚实数字;
- §3 对齐代码 + Abstract 轴名同步;
- §2 把 D1/D2 显化为 bridge + 三处段落措辞自洽;
- cluster 在 §3 定位为 §5 处理因子(保护"single decision variable")。

**这份 v2 才是真正完整的最终方案。**
