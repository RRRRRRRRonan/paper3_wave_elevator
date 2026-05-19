---
title: "PDF 定稿内容修改对照 — Option B (C3 收缩为 2 个 outcome) + Phase 5 结果"
date: 2026-05-19
purpose: "列出当前 PDF (Abstract/Intro/Related Works/Problem Formulation) 中所有需要修改的部分，附修改前后对照"
---

# PDF 定稿内容修改对照表

## 适用范围

当前 PDF 定稿 = **Abstract、Introduction、Related Works、Problem Formulation**（§1–§3）。

- **需要修改**：Abstract（贡献句）、Introduction 的 **C2 段一处**、**C3 段整段**、**C3 后的"operational implication"句**。
- **不需要修改**：**Related Works** 与 **Problem Formulation (§3)** —— 它们定位方法、定义问题，不含被 Phase 5 推翻的经验主张。Φ=(C,I,T) 在 §3 已声明为"conceptual decomposition rather than a predictive surrogate"，与消融发现（C 主导、I/T 弱）不冲突。

**两个驱动因素**：(a) 你选了 **Option B** —— C3 从 3 个 managerial outcome 收缩为 2；(b) **Phase 5 Supp-1** —— destination-clustered dispatch 在 publication scale 普遍降 makespan ~10%（12/12 cell），**不是** regime-conditional，因此原 C3-1 的"prospectively classifies which regimes"和 C3-3 的"substitutability map"站不住。

> 注："...constitute **three contributions** of this paper"一句**不用改** —— 它指 C1/C2/C3 三个 contribution，仍是三个；Option B 只把 C3 *内部*的 outcome 从 3 减到 2。

---

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

## 可选 / 建议复核（非强制，不属"必须改"）

| 位置 | 现状 | 建议 |
|---|---|---|
| Intro "two structural features" 第 1 条 | "wave composition has a small but real effect... that **varies systematically across regimes**" | 可略软化措辞；非强制（这是 motivating 的 preliminary sweep 观察，已声明为 preliminary）|
| Intro "two structural features" 第 2 条 | "per-wave dominance... holds in **92.5–100% of waves**" | 可加一句"(confirmed at ≈99% per-wave dominance at publication scale, Section 5)"—— 增强，非强制 |
| C2 段 | "our rule hedges across **two** structural model classes" | Abstract 已写 {M1,M2,M3} 三模型链；此处"two"与之略不一致，可统一为"a chain of structural model classes"。非 Option-B 引起，但顺手可改 |

---

## 小结

**必须改 4 处**，全部在 **Abstract + Introduction**；Related Works 与 Problem Formulation 不动。改动核心：(1) C3 三 outcome → 两 outcome；(2) "regime 诊断 / which lever / substitutability map"口径 → "结构分解 + 普遍 ~10% 价值"口径。改动后 PDF 的 §1 与即将写的 §5（见 [section5_draft_v0_1.md](section5_draft_v0_1.md)）一致。
