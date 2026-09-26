---
title: "Appendix 适用的全局修改（W10 §2 表述修正 + W6 Edits 7-8）"
date: 2026-07-19
source: "逐字抽取自 00_global 的 W1/W6/W10（2026-07-08 签署交付物的副本）"
note: "如与源文件或其他 W 文件冲突，以 00_global/W10_final_integration.md 为准。W1 Edit 14 的全文查找替换总表仍在 00_global（需在整份 docx 上执行）。"
---

## 2. Presentational fixes to apply when splicing (all wording, no math)

1. Case-B corollary preamble must state its full hypotheses: "(I2) for
   prior requests, (I3) at the current step, and u >= x_(1)" (they are
   available at every application inside the induction; the standalone
   statement was under-hypothesized).
2. Lemma 6's opening adds one sentence: "Throughout, the step is taken
   inside the coupled induction: hypotheses (a) and (b) are in force and
   Lemma 3 aligns the two models' request sequences."
3. X.4.7: "monotone function of its requests' completions" becomes
   "of earlier requests' completions" (covers zero-request orders).
4. Tie-break convention: section 3.3 states "availability ties are broken
   by unit index" as the model convention; the midpoint-median caveat in
   W2 Lemma C.1 / W8 Lemma R.1 is REPLACED by the general bracketing
   proof (breaker-supplied argument: a violation forces even N with every
   cell split exactly in half, and the cell containing the largest pool
   element below the pooled median then brackets it; author to verify the
   two-paragraph argument once). The c=1 equality claim may cite
   exchangeability: robust for any label-order tie-break.

---

# 时效性说明（2026-07-19）

以下 W6 Edits 7-8 针对的 `appendix_robustness.md` 已于 2026-07-19 归档（prototype 尺度附录，被 W2 + tier2 出版尺度稳健性取代）。仅当决定复用该附录内容时才执行这两条；若不复用，可跳过。

---

# Edit 7. "vertical concentration" sweep, hit 2: appendix robustness B.5 (prototype scale)

## 修改前 (BEFORE)

`paper_draft/appendix_robustness.md`, line 183:

> **C-axis invariant, I-axis F-dependent.** All 6 (F, model) points pick the low-concentration corner (LC); the high/low imbalance preference varies with F. GAP **grows with F** (8–12 % at F=5 → 18.7 % at F=9), so the wave-structure lever becomes **more** useful in taller buildings. See [experiments_A1_floors_sweep.py](../prototype/src/experiments_A1_floors_sweep.py), [v0_2_A1_floors_sweep.json](../prototype/results/v0_2_A1_floors_sweep.json).

## 修改后 (AFTER)

> **C-axis invariant, I-axis F-dependent.** All 6 (F, model) points pick the
> low-vertical-spread corner (LC, destinations concentrated on few floors); the
> high/low imbalance preference varies with F. GAP **grows with F** (8-12% at
> F=5 to 18.7% at F=9, prototype scale), so the wave-structure lever becomes
> **more** useful in taller buildings. See
> [experiments_A1_floors_sweep.py](../prototype/src/experiments_A1_floors_sweep.py),
> [v0_2_A1_floors_sweep.json](../prototype/results/v0_2_A1_floors_sweep.json).

## 理由 (RATIONALE)

同 Edit 6 的术语规则：LC 角应写作 low vertical spread；补一个短注 "destinations concentrated on few floors" 帮读者建立正确方向感。该段数字来自 v0_2 工件，按 CLAUDE.md 的标尺规则补上 "prototype scale" 标签；顺带去掉数值区间里的 en-dash 歧义写法并将 "→" 改为 "to"（正文风格）。

---

---

# Edit 8. "vertical concentration" sweep, hit 3: appendix robustness B.8 (prototype scale)

## 修改前 (BEFORE)

`paper_draft/appendix_robustness.md`, line 230:

> **3/4 configurations preserve best corner.** Only the extreme-heterogeneity pool (ratio 4:1 between largest and smallest elevator) flips best corner from HC_HI to LC_HI — intuitively: when a single large elevator dominates, waves should be low-concentration (to spread orders across all three elevators rather than clustering on the large one). Moderate heterogeneity is robust. See [experiments_B1_heterogeneous_pool.py](../prototype/src/experiments_B1_heterogeneous_pool.py), [v0_2_B1_heterogeneous_pool.json](../prototype/results/v0_2_B1_heterogeneous_pool.json).

## 修改后 (AFTER)

> **3/4 configurations preserve the best corner (prototype scale).** Only the
> extreme-heterogeneity pool (ratio 4:1 between the largest and smallest
> elevator) flips the best corner from HC_HI to LC_HI, that is, from high to
> low vertical spread. Moderate heterogeneity is robust. See
> [experiments_B1_heterogeneous_pool.py](../prototype/src/experiments_B1_heterogeneous_pool.py),
> [v0_2_B1_heterogeneous_pool.json](../prototype/results/v0_2_B1_heterogeneous_pool.json).

## 理由 (RATIONALE)

原句的机制性括注 "(to spread orders across all three elevators rather than clustering on the large one)" 把 "low-concentration" 按 "分散" 解读，而 LC = 低 C = 低垂直分散度 = 订单集中于少数楼层，括注与角的定义方向相反，属 TERMINOLOGY 登记的语义反转事故。修改后只陈述可由数据支持的事实（最优角从高分散翻到低分散），删除方向存疑的直觉解释；正确的机制解释需作者重推后另行补写（见 open issues）。补 prototype scale 标签，去 em-dash。

---
