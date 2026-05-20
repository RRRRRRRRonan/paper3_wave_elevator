---
title: "PDF 定稿内容修改对照 — Option B + methodology 定位 + §3-实现对齐 + §2-bridges 深化（最终完整方案）"
date: 2026-05-20
purpose: "当前 PDF (Abstract/§1/§2/§3) 全部需要修改的部分，附修改前后对照。涵盖 (a) Option B 的 C3 收缩，(b) methodology 定位，(c) §3 与代码实现的 4 处对齐，(d) §2 把 D1/D2 显化为 bridge 并补 Wasserstein-DRO 文献根基。"
status: "完整 —— 这是截至目前 PDF 内容的最终修改方案"
---

# PDF 定稿内容修改对照表（最终完整版）

## 适用范围

当前 PDF 定稿 = **Abstract、Introduction、Related Works、Problem Formulation**（§1–§3）。§4 Methodology、§5 不在 PDF 里（它们以 [section4_draft_v0_1.md](section4_draft_v0_1.md) / [section5_draft_v0_1.md](section5_draft_v0_1.md) 草稿存在，是*新增章节*，不属于本"PDF 修订"）。

- **需要修改**：Abstract（贡献句）；§1 的 C2 段 / C3 段 / "operational implication"句 / "two tools"预告段；**§2 的 methodology 段**（整段重写为 3 条 bridge/contrast 线）；§3 的 4 处与实现对齐。
- **不需要修改**：§2 的*问题类*线(4 条 thread)和 §3 的其余部分。

**四个驱动因素**：
- **(a) Option B** —— C3 从 3 个 outcome 收缩为 2（修改 1–4）。
- **(b) methodology 定位** —— 软化 §1 残留的"which lever / regime 分类器"口径（修改 5）。
- **(c) §3 与实现对齐** —— C 公式与语义反向、I 分母、d_o 同层、运营调度仅写 FIFO 等 4 处（修改 6–9）。
- **(d) §2 把 D1/D2 显化为 bridge** —— §2 现在把 SPO/robust scheduling 写成"我们 *differ*",但 §4 prove "we *equal* them (在条件下)";不修就 §4 与 §2 自相矛盾(修改 10)。

> 注："...constitute **three contributions** of this paper"一句**不用改** —— 指 C1/C2/C3,仍是三个。

---

# 第一组：Option B 改动（C3 三 outcome → 两）

## 修改 1 — Abstract，贡献句

**原文 (PDF p.1)**：
> The framework then delivers **three managerial outcomes**: from this decomposition, **(i) a regime-level diagnostic that tells operators which lever to pull, such as wave design, additional elevator capacity, or neither**; from the hedge rule, (ii) a closed-form dispatch policy that operators apply without identifying the true elevator model online, with worst-case loss bounded against any model-specific optimum; and combining the two, **(iii) a tactical–operational substitutability map that identifies the regimes in which wave-composition redesign substitutes for capacity expansion**.

**改后**：
> The framework then delivers **two managerial outcomes**: from the decomposition, **(i) a structural account of the value of wave design, separating a partition-intrinsic upper-tail component from a component a better policy can recover**; and from the hedge rule, (ii) a closed-form dispatch policy that operators apply without identifying the true elevator model online, with worst-case loss bounded against any model-specific optimum.

**原因**：Option B 把 C3 收缩为 2 个 outcome;(i) 由"which lever to pull"改为中性"结构分解"(Supp-1 显示 Bound-and-Gap 不是 sharp 的 regime 分类器);(iii) substitutability map 在 publication scale 上无 regime 区分度,删除。

---

## 修改 2 — Introduction，C2 段（一处短语）

**原文 (PDF p.3)**：
> The Bound-and-Gap framework decomposes the value of wave-structure information into two non-negative components on a structured representation Φ = (C,I,T) of wave composition, **yielding a regime-level diagnostic over wave design, elevator capacity, and a do-nothing option**.

**改后**：
> The Bound-and-Gap framework decomposes the value of wave-structure information into two non-negative components on a structured representation Φ = (C,I,T) of wave composition, **separating a partition-intrinsic upper-tail component from a recoverable policy component**.

**原因**：同修改 1 —— Bound-and-Gap 是结构分解,不是"which lever"的 regime 分类器。C2 段其余文字不动。

---

## 修改 3 — Introduction，C3 段（整段重写）

**原文 (PDF p.3)**：
> **Empirical insights (C3)**: **Three managerial outcomes** from the two tools translate into operational gains. **First, the Bound-and-Gap diagnostic prospectively classifies, before any policy run, the operating regimes in which destination-clustered batching outperforms first-come, first-served dispatch, turning a post hoc decomposition into a forward-looking signal of where tactical wave design will pay off.** Second, the Hedge Rule's per-wave dominance condition holds at higher elevator capacities than the low-capacity setting for which the rule was derived, extending its reach without re-derivation. **Third, combining the two tools yields a tactical-operational substitutability map that identifies, regime by regime, when wave-composition redesign substitutes for elevator-capacity expansion.**

**改后**：
> **Empirical insights (C3)**: **Two managerial outcomes** follow from the two tools, established by pre-registered publication-scale simulation. **First, structured wave-and-dispatch design delivers a broad and substantial makespan reduction: destination-clustered dispatch lowers makespan by roughly 10% across the tested warehouse configurations, and the Bound-and-Gap decomposition characterizes the structure of this value, separating the partition-intrinsic headroom from the component a better policy can recover.** Second, the Hedge Rule's per-wave dominance condition holds at elevator capacities beyond the low-capacity setting for which the rule was derived — confirmed across c ∈ {2,3,4,5} — extending the rule's reach without re-derivation.

**原因**："Three"→"Two"(Option B);原 First 被 Supp-1 推翻(clustering 12/12 普遍降 ~10%,不是 regime-conditional;原型 2/6 是 F=3 假象),改写;原 Third(substitutability map)删除;Second 保留,加"confirmed across c ∈ {2,3,4,5}"(Supp-2)。

---

## 修改 4 — Introduction，C3 段后的"operational implication"句

**原文 (PDF p.3)**：
> The operational implication is that the same warehouse data that informs heuristic batching decisions can, with these tools, support **quantified diagnoses about which lever to pull and the worst-case cost**.

**改后**：
> The operational implication is that the same warehouse data that informs heuristic batching decisions can, with these tools, support **a quantified account of where structured wave design adds value and of the worst-case cost of model misspecification**.

**原因**:"which lever to pull"已被 Supp-1 削弱,改为中性可支撑措辞。

---

# 第二组：methodology 定位改动

## 修改 5 — Introduction，"two tools"预告段（Bound-and-Gap 句尾）

**原文 (PDF p.2)**：
> We develop two analytical tools to address these features. The first is a Bound-and-Gap framework: a decomposition theorem that splits the value of wave-structure information into two non-negative components **and, regime by regime, tells operators whether wave design or elevator capacity is the binding lever**. The second is a Model-Dominance Hedge Rule: ...

**改后**：
> We develop two analytical tools to address these features. The first is a Bound-and-Gap framework: a decomposition theorem that splits the value of wave-structure information into two non-negative components **— a partition-intrinsic upper-tail component and a recoverable policy component**. The second is a Model-Dominance Hedge Rule: ...

**原因**:去掉 regime-分类器口径;Hedge Rule 那一句不动。

---

# 第三组：§3 与代码实现对齐

> 与 Option B / methodology 平行的实现一致性修补;reviewer 查代码就能发现。

## 修改 6 — §3 结构化特征 C(W) 定义（**严重性最高:语义反向**）

**原文 (PDF p.7)**：
> **Vertical concentration C(W) ∈ [0, 1]**: It shows how tight orders share destination floors. C(W) = 1 − H_dst(W)/log₂ F, H_dst(W) = − ∑_{f∈F} p_f(W) log₂ p_f(W), where p_f(W) = |{o∈W: d_o=f}|/|W| ... **C = 1 when all orders share one floor; C = 0 when destinations spread uniformly.**

**改后**：
> **Vertical activity diversity C(W) ≥ 0**: Shannon entropy (natural logarithm) of the empirical floor distribution taken over the *union of source and destination floors* of orders in W. With p_f(W) = (|{o ∈ W : s_o = f}| + |{o ∈ W : d_o = f}|) / (2|W|), define C(W) = −∑_{f∈F} p_f(W) ln p_f(W) (with 0 ln 0 = 0). **High C indicates orders span many floors (vertical activity is diversified); low C indicates concentration on few floors.** We treat C as a conceptual measure of vertical activity rather than a normalized [0,1] index.

**原因**:与 `features.py:vertical_concentration` 对齐:源+目的合并、自然对数、不归一化,**语义反向**(高 C = 多样,不是集中)。所有 Phase 5 数据都按实现的 C 算出;§3 必须对齐。**变量名从"Vertical concentration"改为"Vertical activity diversity"**;corner 标签 HC/LC 含义统一为"high/low 多样性"。

---

## 修改 7 — §3 结构化特征 I(W) 定义

**原文 (PDF p.7)**：
> Directional imbalance I(W) ∈ [0, 1]: ... I(W) = ||W↑| − |W↓|| **/ |W|**, ... (each order is one or the other, **since d_o ≠ s_o**) ...

**改后**：
> Directional imbalance I(W) ∈ [0, 1]: It shows how one-directional the wave's cross-floor vertical traffic is, computed over the cross-floor portion of W. With W↑ = {o ∈ W : d_o > s_o} and W↓ = {o ∈ W : d_o < s_o} (same-floor orders are excluded from both sets), I(W) = ||W↑| − |W↓|| **/ (|W↑| + |W↓|)** when |W↑|+|W↓| > 0, and I(W) = 0 otherwise.

**原因**:与 `features.py:directional_imbalance` 对齐 —— 分母 |W↑|+|W↓|,剔除同层订单;并处理 n_up+n_down=0 边界。

---

## 修改 8 — §3 订单属性 d_o 的可行性

**原文 (PDF p.6 Order attributes)**：
> d_o ∈ ℱ, **d_o ≠ s_o**: destination floor of order o

**改后**：
> d_o ∈ ℱ: destination floor of order o. The trivial floor-1 same-floor pair (s_o, d_o) = (1, 1) is excluded from O; same-floor orders on floors ≥ 2 remain in O because the assigned AMR still requires the elevator to reach that floor.

**原因**:与 `experiments.build_order_pool` / `demand_patterns._feasible_pairs` 对齐(F=3 时约 25% 是同层)。

---

## 修改 9 — §3 运营调度策略（两处:两层架构段 + 假设 A3）

**原文 1 (PDF p.6,两层架构段)**：
> ...decisions we delegate to a deterministic dispatch policy (**capacity-bounded FIFO boarding** under elevator model M ∈ M)...

**改后 1**：
> ...decisions we delegate to a deterministic dispatch policy drawn from a small set — **capacity-bounded FIFO boarding and destination-clustered batching, both under elevator model M ∈ M**. The comparison between these dispatch policies is one of the empirical questions of Section 5...

**原文 2 (PDF p.7, Assumption A3)**：
> **Capacity-bounded FIFO boarding.** AMRs join the elevator queue in arrival order and board up to c at a time under elevator model M.

**改后 2**：
> **Capacity-bounded deterministic boarding.** AMRs board the elevator up to c at a time according to a chosen deterministic policy — either FIFO (queue arrival order) or destination-clustered (selecting the c pending orders that minimize destination spread within the batch) — under elevator model M.

**原因**:与 `simulate_wave` 的 `policy ∈ {"fifo","cluster"}` 和 §5 C3-① 头条数字(cluster 降 makespan ~10%)对齐。原 §3 钉死 FIFO,与 §5 直接矛盾。

---

# 第四组：§2 methodology 段深化（把 D1/D2 显化为 bridge）

> 当前 §2 把 SPO / robust scheduling 写成"我们 *differ*",但 §4 prove "we *equal* them"。不修则 §4 与 §2 自相矛盾,reviewer 必问。同时把 Wasserstein-DRO 文献根基显化(D2 的方法论依托)。

## 修改 10 — §2 整段重写（PDF p.4–5 倒数第二段:"Two methodological threads..."）

**原文 (PDF p.4–5)**：
> Two methodological threads inform our analytical apparatus, each addressing a distinct gap. The prediction-to-decision regret literature (Elmachtoub & Grigas, 2020; Vera et al., 2020) bounds algorithmic loss when a learned predictor drives a downstream optimizer; these bounds are training-time and pre-commitment, describing a specific algorithm's regret rather than the post-hoc gap between an oracle on a structured feature partition and a feature-informed policy on the same partition. Our Bound-and-Gap framework formalizes that post-hoc information value as a non-negative decomposition into a partition-intrinsic upper-tail term (H_up) and a Φ-policy slack term (M_Φ). Robust scheduling under model uncertainty (Lu & Shen, 2021; Wiesemann et al., 2013) hedges against parametric variation within a known model class. The framework presupposes a single, agreed-upon family of models with an unknown parameter. Our elevator-modeling uncertainty is structurally different: throughput aggregation and true co-occupancy batching are qualitatively distinct models, not parameterizations of the same family. Our Model-Dominance Hedge Rule collapses this structural model-class disagreement into a single closed-form decision under a per-wave dominance condition, with a worst-case loss bound that requires no online model selection.

**改后（整段替换,~300 词）**：
> Three methodological threads inform our analytical apparatus; the first two are connected to our tools by precise equivalences proven in Section 4, the third by a structural contrast.
>
> First, the **prediction-to-decision regret** literature (Elmachtoub & Grigas, 2020; Vera et al., 2020; Chenreddy & Delage, 2023) bounds the algorithmic loss when a learned predictor drives a downstream optimizer. Theorem 1 (Section 4.1.2) gives this regret a *partition perspective*: the policy-slack component M_Φ of our decomposition equals the Smart-Predict-then-Optimize regret of the partition-constant predictor class, so the literature's training-time regret object and our post-hoc, structured-feature decomposition refer to the same underlying quantity on a finite partition. Our contribution is the decomposition itself, which separates this SPO regret from an independent partition-intrinsic headroom term H_up.
>
> Second, **Wasserstein distributionally robust optimization** (Esfahani & Kuhn, 2018; Blanchet & Murthy, 2019; Gao & Kleywegt, 2023) hedges decisions against worst-case distributions within a transport-distance ambiguity ball of a nominal model, typically reformulated as a convex program. Theorem 2 (Section 4.2.2) shows that under a chain of per-wave stochastic dominance conditions, our minimax wave-corner selection over {M_1, M_2, M_3} coincides with the Wasserstein-DRO solution at the appropriate ambiguity radius, collapsing the convex DRO program into a closed-form one-line rule. Our contribution is the dominance-conditional collapse, exploiting an empirically verified structural property to replace optimization with identification.
>
> Third, **robust scheduling under model uncertainty** (Lu & Shen, 2021; Wiesemann et al., 2013) hedges against parametric variation within a single agreed-upon model class. Our elevator-modeling uncertainty is structurally different: throughput aggregation and true co-occupancy batching are qualitatively distinct models, not parameterizations of one family. The Model-Dominance Hedge Rule addresses this *structural* model-class disagreement rather than parametric uncertainty within a class.

**原因**:
- (i) 把 §2 的 methodology 线从 2 条扩到 3 条;前两条由"contrast"改写为"bridge"(D1/D2 在 §4 prove equivalence,§2 必须呼应);
- (ii) **新增 Wasserstein-DRO 整条线** —— 这是 D2 主张坍缩等价的文献根基,原 §2 完全没引;
- (iii) 第三条(robust scheduling)保留 contrast(它对的是参数不确定,我们对的是结构性模型类不确定 —— 这条对比仍然成立)。

### 修改 10 需要新增的 4 篇引用(我已核对存在性 + 主要出版信息)

| # | 引用 | 真实出处 | 验证用 DOI / arXiv |
|---|---|---|---|
| R1 | **Esfahani, P. M., & Kuhn, D. (2018).** Data-driven distributionally robust optimization using the Wasserstein metric: performance guarantees and tractable reformulations. *Mathematical Programming*, 171(1), 115–166. | Math. Prog. 2018,171 卷 1 期 | DOI: `10.1007/s10107-017-1172-1` |
| R2 | **Blanchet, J., & Murthy, K. (2019).** Quantifying distributional model risk via optimal transport. *Mathematics of Operations Research*, 44(2), 565–600. | MOR 2019,44 卷 2 期 | DOI: `10.1287/moor.2018.0936` |
| R3 | **Gao, R., & Kleywegt, A. J. (2023).** Distributionally robust stochastic optimization with Wasserstein distance. *Mathematics of Operations Research*, 48(2), 603–655. | MOR 2023,48 卷 2 期 | DOI: `10.1287/moor.2022.1275`(arXiv 原文:1604.02199) |
| R4 | **Chenreddy, A., & Delage, E. (2023).** End-to-end conditional robust optimization. | arXiv 预印本 | arXiv: `2305.19225` |

**核验提醒**:这 4 篇我都核过存在性 + 期刊卷期。**落进 BibTeX 前请你最终再用 DOI / arXiv 号核一遍页码与作者顺序**(尤其 R3 published in MOR 印刷年份是 2023,在线发表更早)。

---

## 可选 / 建议复核

| # | 位置 | 现状 | 建议 |
|---|---|---|---|
| O1 | Abstract | "pre-registered simulation experiments" | 强化为 "**pre-registered, publication-scale simulation study**" —— methodology 严谨度卖点显化。建议改。 |
| O2 | Intro "two structural features"第 1 条 | "varies systematically across regimes" | 可略软化;非强制。 |
| O3 | Intro "two structural features"第 2 条 | "92.5–100% of waves" | 加"(confirmed at ≈99% at publication scale, Section 5)"。 |
| O4 | C2 段 | "hedges across **two** structural model classes" | 与 abstract {M1,M2,M3} 三模型链不一致,改为 "a chain of structural model classes"。 |
| O5 | Abstract / §1 | (无) | 可加一句明确"methodological contribution",但论文实质已是 methodology 语气,**非必须**。 |

### 引用年份核验(待你确认原意)

| V# | 位置 | PDF 当前年份 | 实际出版 | 说明 |
|---|---|---|---|---|
| V1 | §2 prediction-to-decision regret | **Elmachtoub & Grigas, 2020** | **Management Science 68(1), 9–26, 2022** | PDF "2020" 可能是 arXiv 年份(arXiv:1710.08005);若引正式期刊版,应改为 2022 |
| V2 | §2 同上 | **Vera et al., 2020** | **Operations Research 69(3), 821–840, 2021** | PDF "2020" 可能是 arXiv 年份;正式版 2021 |
| V3 | §2 surveys | **Boysen et al., 2017**("50 years of warehousing research") | **Boysen & de Koster (2025).** *European Journal of Operational Research*, 320(3), 449–464 | PDF "2017" 与"50 years of evolution"叙述对应的应是 Boysen & de Koster (2025) —— **疑年份错** |

修改 10 的英文新段我已经用 PDF 当前的"2020"(Elmachtoub、Vera)以保持文中*暂时一致*;若你决定改用正式版年份,需要在 §2 全文统一改。

---

## 小结

**必须改 10 处**,四组:

| 组 | 修改 | 位置 | 核心 |
|---|---|---|---|
| 第一组 Option B | 1–4 | Abstract + §1 | C3 三 outcome → 两;"regime 诊断 / which lever / substitutability map" → "结构分解 + 普遍 ~10% 价值" |
| 第二组 methodology 定位 | 5 | §1 | 去掉"binding lever"的 regime-分类器口径 |
| 第三组 §3-实现对齐 | 6–9 | §3 | C 公式与语义对齐;I 分母对齐;允许同层订单(除 (1,1));调度策略含 FIFO + cluster |
| 第四组 §2-bridges 深化 | 10 | §2 | methodology 段从 2 条 contrast 扩为 3 条(2 bridge + 1 contrast);把 D1/D2 显化;新增 4 篇引用(Esfahani & Kuhn 2018、Blanchet & Murthy 2019、Gao & Kleywegt 2023、Chenreddy & Delage 2023) |

加 O1–O5 可选;V1–V3 年份核验。

改后 PDF 的 Abstract+§1+§2+§3 与新增的 §4([section4_draft_v0_1.md](section4_draft_v0_1.md))、§5([section5_draft_v0_1.md](section5_draft_v0_1.md))**全面贯通** —— 同走 Option B、同为 methodology 定位、同用 Phase 5 诚实数字、§3 对齐代码、§2 把 D1/D2 显化为 bridge。

**这份文件即截至目前 PDF 内容的最终完整修改方案。**
