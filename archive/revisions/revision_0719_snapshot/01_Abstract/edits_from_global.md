---
title: "Abstract 适用的全局修改（W6 Edits 3-4 + W1 Edit 14 摘要行）"
date: 2026-07-19
source: "逐字抽取自 00_global 的 W1/W6/W10（2026-07-08 签署交付物的副本）"
note: "如与源文件或其他 W 文件冲突，以 00_global/W10_final_integration.md 为准。W1 Edit 14 的全文查找替换总表仍在 00_global（需在整份 docx 上执行）。"
---

# Edit 3. Scope the Abstract's Hedge Rule claims (English paragraph)

## 修改前 (BEFORE)

`paper_draft/Abstract/abstract_v1.0.md`, lines 72-76 (third English paragraph, first sentence):

> A pre-registered study of 106,800 simulations reports each tool's outcome as it stands, and the two differ: the
> Hedge Rule passes every gate (per-wave dominance 99.2%, matching the
> distributionally-robust optimum), while the Bound-and-Gap identities hold
> exactly (72/72) and its resolution gate, met in 79% (a partial pass), fails only
> where the gap is genuinely small.

## 修改后 (AFTER)

> A pre-registered study of 106,800 simulations reports each tool's outcome as
> it stands, and the two differ: the Hedge Rule passes every gate (per-wave
> dominance holding in 99.2% of matched waves across the six-configuration
> model-chain block, and the wave-structure it selects matching the
> distributionally-robust optimum in all six configurations tested), while the
> Bound-and-Gap identities hold exactly (72/72) and its resolution gate, met in
> 79% (a partial pass), fails only where the gap is genuinely small.

## 理由 (RATIONALE)

panel_novelty 致命缺陷 7："the abstract says the DRO match holds 'in every configuration' when Block C covers 6 of 18 configs"。DRO-Hedge 一致性（6/6）与逐波次支配序（99.2%）都只在 Block C 的六配置模型链区块上测得，摘要不加限定会被 Table 3 直接证伪。修改后两个数字均标注其实际覆盖范围，验证结论本身（PASS）不变、不重判。

---

---

# Edit 4. Scope the Abstract's Hedge Rule claims (Chinese paragraph, symbol-free)

## 修改前 (BEFORE)

`paper_draft/Abstract/abstract_v1.0.md`, lines 81-84 (third Chinese paragraph, first sentence):

> 一项预注册研究（共 106,800 次仿真）如实报告两个工具各自的结论，两者并不相同：Hedge Rule 通过全部门槛
> （逐波次支配序 99.2%，且与分布鲁棒最优解一致），而 Bound-and-Gap 的恒等关系精确
> 成立（72/72），其分辨门槛在 79% 达到（部分通过），未达到之处恰是波次设计价值本就
> 很小的子单元。

## 修改后 (AFTER)

> 一项预注册研究（共 106,800 次仿真）如实报告两个工具各自的结论，两者并不相同：
> Hedge Rule 通过全部门槛（在六配置模型链区块中，99.2% 的匹配波次满足逐波次支配序；
> 其选出的波次结构在受测的全部六个配置中与分布鲁棒最优解一致），而 Bound-and-Gap
> 的恒等关系精确成立（72/72），其分辨门槛在 79% 达到（部分通过），未达到之处恰是
> 波次设计价值本就很小的子单元。

## 理由 (RATIONALE)

与 Edit 3 对应的中文段同步限定（TERMINOLOGY 第 9 节要求双语段落同改）。中文版保持无数学符号（不出现模型代号或希腊字母），"六配置模型链区块" 与 "受测的全部六个配置" 分别限定 99.2% 与 DRO 一致性两个数字的范围。

---

---

# 本章适用的 W1 Edit 14 查找替换行（Abstract 部分）

| 位置 | 现文 | 替换为 |
|---|---|---|
| abstract_v1.0.md : 10 (YAML note) | `the formal term "SPO regret" stays in the Theorem 1 statement in section 4` | `... stays in the Proposition 3 statement in section 4` |
| abstract_v1.0.md : 54-55 (正文) | `Under a conditional dominance result that we establish, this simplest rule is provably the distributionally-robust optimum.` | `Under a conditional dominance result that we establish, this simplest rule is provably the robust choice: it is exactly minimax over the candidate models and matches a calibrated distributionally-robust optimum.` |
| abstract_v1.0.md : 65-66 (中文段) | `……这条最简单的规则可被证明就是分布鲁棒意义下的最优解。` | `……这条最简单的规则可被证明是稳健的选择：它恰是候选模型之间的极小极大解，并与一个经过校准的分布鲁棒最优解一致。` |
