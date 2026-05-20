---
title: "PDF 定稿内容修改对照 — Option B + methodology 定位（最终完整方案）"
date: 2026-05-20
purpose: "当前 PDF (Abstract/Intro/Related Works/Problem Formulation) 全部需要修改的部分，附修改前后对照。涵盖 (a) Option B 的 C3 收缩，(b) methodology 定位。"
status: "完整 —— 这是截至目前 PDF 内容的最终修改方案"
---

# PDF 定稿内容修改对照表（最终完整版）

## 适用范围

当前 PDF 定稿 = **Abstract、Introduction、Related Works、Problem Formulation**（§1–§3）。§4 Methodology、§5 不在 PDF 里（它们以 [section4_draft_v0_1.md](section4_draft_v0_1.md) / [section5_draft_v0_1.md](section5_draft_v0_1.md) 草稿存在，是*新增章节*，不属于本"PDF 修订"）。

- **需要修改**：Abstract（贡献句）、Introduction 的 C2 段、C3 段、"operational implication"句、"two tools"预告段 —— **全部在 Abstract + §1 范围内**。
- **不需要修改**：Related Works (§2) 与 Problem Formulation (§3)。

**两个驱动因素**：
- **(a) Option B** —— C3 从 3 个 managerial outcome 收缩为 2（修改 1–4）。
- **(b) methodology 定位** —— 论文目标从 Q1-application 改为 Q1-methodology；需软化 §1 残留的"which lever / regime 分类器"口径（修改 5）。

> **诚实说明**：methodology 定位的额外改动**很小** —— 只有修改 5 一处必改。原因:PDF 本来就是 methodology 语气("two analytical tools / decomposition theorem / Hedge Rule / pre-registered simulation"),且 Option B 的 C3 重写已完成大部分"去 application 化"。我上一轮说"一整批改动"是高估,据实更正。

> 注："...constitute **three contributions** of this paper"一句**不用改** —— 指 C1/C2/C3 三个 contribution,仍是三个;Option B 只把 C3 *内部*的 outcome 从 3 减到 2。

---

# 第一组：Option B 改动（C3 三 outcome → 两）

## 修改 1 — Abstract，贡献句

**原文 (PDF p.1)**：
> The framework then delivers **three managerial outcomes**: from this decomposition, **(i) a regime-level diagnostic that tells operators which lever to pull, such as wave design, additional elevator capacity, or neither**; from the hedge rule, (ii) a closed-form dispatch policy that operators apply without identifying the true elevator model online, with worst-case loss bounded against any model-specific optimum; and combining the two, **(iii) a tactical–operational substitutability map that identifies the regimes in which wave-composition redesign substitutes for capacity expansion**.

**改后**：
> The framework then delivers **two managerial outcomes**: from the decomposition, **(i) a structural account of the value of wave design, separating a partition-intrinsic upper-tail component from a component a better policy can recover**; and from the hedge rule, (ii) a closed-form dispatch policy that operators apply without identifying the true elevator model online, with worst-case loss bounded against any model-specific optimum.

**原因**：Option B 把 C3 收缩为 2 个 outcome。(i) 由"regime-level diagnostic / which lever to pull"改为中性的"结构分解"—— Supp-1 显示 Bound-and-Gap 不是一个 sharp 的 regime 分类器。(iii) substitutability map 在 publication scale 上无 regime 区分度（clustering 处处有效），删除。

---

## 修改 2 — Introduction，C2 段（一处短语）

**原文 (PDF p.3)**：
> The Bound-and-Gap framework decomposes the value of wave-structure information into two non-negative components on a structured representation Φ = (C,I,T) of wave composition, **yielding a regime-level diagnostic over wave design, elevator capacity, and a do-nothing option**.

**改后**：
> The Bound-and-Gap framework decomposes the value of wave-structure information into two non-negative components on a structured representation Φ = (C,I,T) of wave composition, **separating a partition-intrinsic upper-tail component from a recoverable policy component**.

**原因**：同修改 1 —— Bound-and-Gap 是一个*结构分解*，不是"which lever"的 regime 分类器。C2 段其余文字（Hedge Rule 部分、与 prediction-to-decision regret / robust scheduling 的对比）**不动**。

---

## 修改 3 — Introduction，C3 段（整段重写）

**原文 (PDF p.3)**：
> **Empirical insights (C3)**: **Three managerial outcomes** from the two tools translate into operational gains. **First, the Bound-and-Gap diagnostic prospectively classifies, before any policy run, the operating regimes in which destination-clustered batching outperforms first-come, first-served dispatch, turning a post hoc decomposition into a forward-looking signal of where tactical wave design will pay off.** Second, the Hedge Rule's per-wave dominance condition holds at higher elevator capacities than the low-capacity setting for which the rule was derived, extending its reach without re-derivation. **Third, combining the two tools yields a tactical-operational substitutability map that identifies, regime by regime, when wave-composition redesign substitutes for elevator-capacity expansion.**

**改后**：
> **Empirical insights (C3)**: **Two managerial outcomes** follow from the two tools, established by pre-registered publication-scale simulation. **First, structured wave-and-dispatch design delivers a broad and substantial makespan reduction: destination-clustered dispatch lowers makespan by roughly 10% across the tested warehouse configurations, and the Bound-and-Gap decomposition characterizes the structure of this value, separating the partition-intrinsic headroom from the component a better policy can recover.** Second, the Hedge Rule's per-wave dominance condition holds at elevator capacities beyond the low-capacity setting for which the rule was derived — confirmed across c ∈ {2,3,4,5} — extending the rule's reach without re-derivation.

**原因**：
- "Three" → "Two"（Option B）。
- 原 First（prospective classification / forward-looking signal）被 Supp-1 推翻：clustering 在 12/12 cell 普遍降 ~10%，不是 regime-conditional；原型的"2/6 区域条件"是 F=3 楼层太少的产物。改为"普遍 ~10% 价值 + Bound-and-Gap 刻画其结构"。
- 原 Third（substitutability map）删除。
- Second 基本保留，加"confirmed across c ∈ {2,3,4,5}"（Supp-2 已在 publication scale 确认）。

---

## 修改 4 — Introduction，C3 段后的"operational implication"句

**原文 (PDF p.3)**：
> The operational implication is that the same warehouse data that informs heuristic batching decisions can, with these tools, support **quantified diagnoses about which lever to pull and the worst-case cost**.

**改后**：
> The operational implication is that the same warehouse data that informs heuristic batching decisions can, with these tools, support **a quantified account of where structured wave design adds value and of the worst-case cost of model misspecification**.

**原因**："which lever to pull"是被 Supp-1 削弱的 regime-分类口径，改为中性、可支撑的措辞。

---

# 第二组：methodology 定位改动

## 修改 5 — Introduction，"two tools"预告段（Bound-and-Gap 句尾）

**原文 (PDF p.2)**：
> We develop two analytical tools to address these features. The first is a Bound-and-Gap framework: a decomposition theorem that splits the value of wave-structure information into two non-negative components **and, regime by regime, tells operators whether wave design or elevator capacity is the binding lever**. The second is a Model-Dominance Hedge Rule: a closed-form dispatch policy that handles uncertainty over which elevator model best describes a warehouse, telling operators which wave to release without identifying the true model online and bounding the cost of being wrong.

**改后**：
> We develop two analytical tools to address these features. The first is a Bound-and-Gap framework: a decomposition theorem that splits the value of wave-structure information into two non-negative components **— a partition-intrinsic upper-tail component and a recoverable policy component**. The second is a Model-Dominance Hedge Rule: a closed-form dispatch policy that handles uncertainty over which elevator model best describes a warehouse, telling operators which wave to release without identifying the true model online and bounding the cost of being wrong.

**原因**：methodology 定位下,论文不主张"诊断告诉运营者该拉哪个杠杆"这种 regime-分类器口径(也已被 Supp-1 削弱)。改为中性的"结构分解"描述。Hedge Rule 那一句**不动** —— 它只是描述工具输出,与 methodology 定位相容。

---

## 可选 / 建议复核（非强制）

| # | 位置 | 现状 | 建议 |
|---|---|---|---|
| O1 | Abstract | "Both tools are validated by **pre-registered simulation experiments**." | 强化为 "...by a **pre-registered, publication-scale simulation study**." —— 把"严谨度"这个 methodology 卖点显化。低风险,建议改。 |
| O2 | Intro "two structural features" 第 1 条 | "...effect on makespan that **varies systematically across regimes**" | 可略软化;非强制(motivating 的 preliminary 观察)。 |
| O3 | Intro "two structural features" 第 2 条 | "per-wave dominance... holds in **92.5–100% of waves**" | 可加"(confirmed at ≈99% at publication scale, Section 5)"。增强,非强制。 |
| O4 | C2 段 | "our rule hedges across **two** structural model classes" | Abstract 已写 {M1,M2,M3} 三模型链;"two"与之不一致,建议统一为"a chain of structural model classes"。 |
| O5 | Abstract / §1 | （无）| 可加一句明确把贡献定位为 methodological;但论文已实质是 methodology 语气,**非必须**。 |

---

## 小结

**必须改 5 处**，全部在 **Abstract + §1 Introduction**；Related Works、Problem Formulation 不动。

| 组 | 修改 | 核心 |
|---|---|---|
| Option B | 修改 1–4 | C3 三 outcome → 两；"regime 诊断 / which lever / substitutability map" → "结构分解 + 普遍 ~10% 价值" |
| methodology 定位 | 修改 5 | §1 预告段去掉"tells operators which lever is the binding lever"的 regime-分类器口径 |

加 O1（建议）、O2–O5（可选）。改动后 PDF 的 Abstract+§1 与新增的 §4（[section4_draft_v0_1.md](section4_draft_v0_1.md)）、§5（[section5_draft_v0_1.md](section5_draft_v0_1.md)）一致 —— 同走 Option B、同为 methodology 定位、同用 Phase 5 的诚实数字。

**这份文件即截至目前 PDF 内容的最终完整修改方案。**
