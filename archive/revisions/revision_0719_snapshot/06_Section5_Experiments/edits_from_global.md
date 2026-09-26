---
title: "Section 5 适用的全局修改（W1 Edits 9-13 + W6 Edits 1/2/2b/2c + 事项）"
date: 2026-07-19
source: "逐字抽取自 00_global 的 W1/W6/W10（2026-07-08 签署交付物的副本）"
note: "如与源文件或其他 W 文件冲突，以 00_global/W10_final_integration.md 为准。W1 Edit 14 的全文查找替换总表仍在 00_global（需在整份 docx 上执行）。"
---

# Edit 9: Section 5 Table 2 and surrounding prose: gate D1-c rescoped as a pipeline consistency check

## 修改前 (BEFORE)

Source: `paper_draft/section5_draft_v0_1.md`, lines 54-76.

> **Table 2. Bound-and-Gap decomposition, Block A (72 sub-cells).**
>
> | Gate | Criterion | Result |
> |---|---|---|
> | Decomposition exact | `GAP = H_up + M_Φ` | **72 / 72** |
> | Non-negativity | `H_up ≥ 0` and `M_Φ ≥ 0` | 70 / 72 |
> | SPO-regret equivalence | `M_Φ = ` SPO regret of the Φ predictor | **72 / 72** |
> | Signal resolution | 95 % bootstrap CI of `GAP` excludes 0 | 57 / 72 (79.2 %) |
>
> The framework's two structural claims hold exactly at publication scale. The
> decomposition identity `GAP = H_up + M_Φ` and the SPO-regret equivalence
> `M_Φ = ` SPO regret (Theorem 1) are satisfied in all **72 of 72** sub-cells,
> confirming the two theorems on which Tool 1 rests at publication scale, not only
> at the prototype scale on which they were derived. The decomposition's headline
> managerial reading is equally stable: the partition-intrinsic ceiling `H_up`
> accounts for **71.7 %** of the mean gap (`GAP = 0.060`; `H_up = 0.043`,
> `M_Φ = 0.017`), and this share is **71.9 %** within the subset of sub-cells whose
> gap is statistically resolved, so the capacity-side-over-policy-side reading
> does not depend on the boundary sub-cells. Non-negativity holds in 70/72; the
> two exceptions are near-degenerate sub-cells (`H_up = −0.0021` and `−0.0044`,
> each below 0.5 % of the cell scale) where the random-pool sample median
> marginally exceeds the worst-corner sample median, a finite-sample artefact that
> does not contradict the population inequality.

## 修改后 (AFTER)

**Table 2. Bound-and-Gap decomposition, Block A (72 sub-cells).**

| Gate | Criterion | Result |
|---|---|---|
| Decomposition consistency (D1-a) | `GAP = H_up + M_Φ` | **72 / 72** |
| Non-negativity (D1-b) | `H_up ≥ 0` and `M_Φ ≥ 0` | 70 / 72 |
| SPO-bridge consistency (D1-c) | pipeline's SPO-regret computation reproduces `M_Φ` | **72 / 72** |
| Signal resolution (D1-d) | 95 % bootstrap CI of `GAP` excludes 0 | 57 / 72 (79.2 %) |

The first and third gates are pipeline consistency checks, and we report them
as such. Proposition 1 and Proposition 3 are identities, so these two rows
could fail only through an implementation defect, not for a scientific reason:
both sides of each identity are computed from the same corner medians, and the
72/72 outcomes record that the publication-scale analysis pipeline evaluates
the decomposition and its predict-then-optimize bridge consistently. They
carry no evidential weight for the framework beyond that, and we do not claim
any. The decomposition's headline managerial reading is the substantive
result, and it is stable: the partition-intrinsic ceiling `H_up` accounts for
**71.7 %** of the mean gap (`GAP = 0.060`; `H_up = 0.043`, `M_Φ = 0.017`), and
this share is **71.9 %** within the subset of sub-cells whose gap is
statistically resolved, so the capacity-side-over-policy-side reading does not
depend on the boundary sub-cells. Non-negativity holds in 70/72; the two
exceptions are near-degenerate sub-cells (`H_up = −0.0021` and `−0.0044`, each
below 0.5 % of the cell scale) where the random-pool sample median marginally
exceeds the worst-corner sample median, a finite-sample artefact that does not
contradict the population inequality.

## 理由 (RATIONALE)

对应 panel_theory.json 第 1 条 fatal flaw 中关于 D1-c 的部分："其数值'验证'
是循环的：analysis_D1_spo_equivalence.py 第 143-144 行用逐字节相同的表达式
计算两侧，72/72 门槛先验不可能失败"，defense 要求 "stop presenting the 72/72
check as a verification gate (rescope D1-c as a pipeline consistency check)"。
改写保留预注册门槛及其结果（不改判、不删除，符合预注册纪律与 TERMINOLOGY
第 7 节"verdicts never re-judged"），只重述其证据地位：恒等式检查只能因实现
缺陷而失败，不为框架提供额外证据。表内补上 D1-a/b/c/d 门槛编号便于与预注册
文档对照。注意：本编辑未触及 non-negativity 段落中 "population inequality"
的表述（panel 第 5 条 flaw），该修复属另一工作包，见 Open Issues。

---

---

# Edit 10: Section 5.2 closing paragraph: no theorem-credit for identity checks

## 修改前 (BEFORE)

Source: `paper_draft/section5_draft_v0_1.md`, lines 108-113.

> The Bound-and-Gap framework is therefore a structurally exact account of the
> value of wave design, identity and SPO-regret equivalence holding in 72/72,
> whose statistical resolution is high and, where a gap is not resolved, is
> unresolved precisely because the gap is genuinely near zero. We report D1-d as
> PARTIAL, reading its resolution as power-limited specificity rather than a
> deficiency of the decomposition.

## 修改后 (AFTER)

The Bound-and-Gap framework is therefore a structurally exact account of the
value of wave design (its two identities are consistent across the pipeline in
72/72, as identities must be), whose statistical resolution is high and,
where a gap is not resolved, is unresolved precisely because the gap is
genuinely near zero. We report D1-d as PARTIAL, reading its resolution as
power-limited specificity rather than a deficiency of the decomposition.

## 理由 (RATIONALE)

与 Edit 9 同源（panel 第 1 条 flaw）：原句 "identity and SPO-regret
equivalence holding in 72/72" 把管道一致性结果当作框架的实证支撑列举。改写
以插入语自陈"恒等式必然成立"，保留 72/72 事实但不再借其加分；同时把普通散文
中的 "SPO-regret" 措辞移除（TERMINOLOGY 第 4 节：正式术语只出现在 §4 的正式
陈述中）。H-D1 PARTIAL 判定原样保留。

---

---

# Edit 11: Section 5.3 Table 3 and lead paragraph: DRO gate tied to Corollary 3 with mean-summary scope

## 修改前 (BEFORE)

Source: `paper_draft/section5_draft_v0_1.md`, lines 135-159.

> **Table 3. Model-Dominance Hedge Rule, Block C.**
>
> | Gate | Criterion | Result |
> |---|---|---|
> | Per-wave dominance | `M2 ≥ M1` per wave | 99.2 % avg, 96.0 % worst cell |
> | First-order dominance | `M1 ⪯ M2` (quantile coupling) | 24 / 24 |
> | One-sided ε-bound | `U_c(0.05) < 5 % · m_0` | 24 / 24 |
> | DRO = Hedge | `c*_DRO = c*_Hedge` per regime | 6 / 6 |
>
> All four gates pass, and the decision-level result leads: **the corner the Hedge
> Rule selects coincides with the Wasserstein-DRO optimum in all six
> configurations**, so the closed-form rule reproduces the distributionally-robust
> release decision exactly. The remaining numbers explain why this holds and bound
> what the exceptions can cost. The mechanism is per-wave chain dominance
> (Proposition 2): the *scalar, sample-path* ordering `M2 ≥ M1` holds in **99.2 %**
> of matched waves on average (96.0 % in the worst cell), while the
> *distribution-level* first-order dominance that the DRO clause invokes holds in
> all 24 cells. The residual never flips the release decision: every violating
> wave is a batch-overtaking event, the failure mode Proposition 2 isolates, and
> even in the worst cell (config 1, 96.0 % per-wave dominance, a 4 % violation
> rate) the one-sided worst-case bound is `U_c(0.05) = 0.53 %` of that cell's
> median makespan, its largest value over all 24 cells being **3.5 %** (config 7),
> comfortably inside the 5 % gate. The Model-Dominance Hedge Rule is thus
> **confirmed at publication scale**, the firmer of the paper's two empirical
> pillars.

## 修改后 (AFTER)

**Table 3. Model-Dominance Hedge Rule, Block C.**

| Gate | Criterion | Result |
|---|---|---|
| Per-wave dominance (Proposition 2) | `M2 ≥ M1` per wave | 99.2 % avg, 96.0 % worst cell |
| First-order dominance (Corollary 3 hypothesis) | `M1 ⪯ M2` (quantile coupling) | 24 / 24 |
| One-sided ε-bound (Corollary 2) | `U_c(0.05) < 5 % · m_0` | 24 / 24 |
| DRO certification (Corollary 3, mean summary) | `c*_DRO = c*_Hedge` per regime | 6 / 6 |

All four gates pass, and the decision-level result leads: **the corner the
Hedge Rule selects coincides with the corner-calibrated Wasserstein-DRO
optimum (Corollary 3, stated for the mean) in all six configurations**, so the
closed-form rule reproduces the distributionally-robust release decision
exactly. The remaining numbers explain why this holds and bound what the
exceptions can cost. The mechanism is per-wave chain dominance
(Proposition 2), the paper's substantive theoretical result: the *scalar,
sample-path* ordering `M2 ≥ M1` holds in **99.2 %** of matched waves on
average (96.0 % in the worst cell), while the *distribution-level* first-order
dominance that Corollary 3 invokes holds in all 24 cells. The residual never
flips the release decision: every violating wave is a batch-overtaking event,
the failure mode Proposition 2 isolates, and even in the worst cell (config 1,
96.0 % per-wave dominance, a 4 % violation rate) the one-sided worst-case
bound is `U_c(0.05) = 0.53 %` of that cell's median makespan, its largest
value over all 24 cells being **3.5 %** (config 7), comfortably inside the 5 %
gate. The Model-Dominance Hedge Rule is thus **confirmed at publication
scale**, the firmer of the paper's two empirical pillars.

## 理由 (RATIONALE)

配合新编号与 DRO 降级（panel 第 2、6 条 flaw）：表内每个门槛挂上其对应的
形式结果编号，DRO 行明确写出 "Corollary 3, mean summary"，落实任务第 3 点的
统计量范围声明（collapse/Corollary 2 用中位数，DRO 用均值）在 §5 侧的呼应。
门槛本身、判定（全部 PASS、H-D2 confirmed）与所有数字原样保留，不改判。

---

---

# Edit 12: Section 5.3 probe paragraph: numbering fix and release-wording fix

## 修改前 (BEFORE)

Source: `paper_draft/section5_draft_v0_1.md`, lines 161-175.

> An exploratory probe (non-gating) tests whether the corner *ranking* itself
> is invariant across `M1`/`M2`/`M3` and finds it is not: the full ranking and the
> worst corner shift across models (mean rank correlation 0.75 against `M1`). The
> best corner that the rule actually selects is far more stable, invariant in five
> of six configurations, and the Hedge corner matches the Wasserstein-DRO optimum
> in all six, so the ranking non-invariance the probe records never flips the
> release decision. The probe is **not the motivation** for the Hedge Rule. Theorem 2's collapse under chain dominance, derived from the structural
> model-uncertainty argument in §4.2, is the methodological motivation, fixed
> before any scale-up data was seen and pre-registered as a gating hypothesis.
> The probe is the *empirical confirmation* that the model-uncertainty premise
> on which §4.2 rests is non-vacuous at publication scale: because the
> wave-design corner does in fact depend on which elevator model is believed,
> a rule whose dispatch decision is robust to that choice is operationally
> relevant, not merely formally robust against a hypothetical uncertainty that
> never materialises.

## 修改后 (AFTER)

An exploratory probe (non-gating) tests whether the corner *ranking* itself
is invariant across `M1`/`M2`/`M3` and finds it is not: the full ranking and the
worst corner shift across models (mean rank correlation 0.75 against `M1`). The
best corner that the rule actually selects is far more stable, invariant in five
of six configurations, and the Hedge corner matches the Wasserstein-DRO optimum
in all six, so the ranking non-invariance the probe records never flips the
release decision. The probe is **not the motivation** for the Hedge Rule.
Theorem 1's collapse under the chain dominance of Proposition 2, derived from
the structural model-uncertainty argument in §4.2, is the methodological
motivation, fixed before any scale-up data was seen and pre-registered as a
gating hypothesis. The probe is the *empirical confirmation* that the
model-uncertainty premise on which §4.2 rests is non-vacuous at publication
scale: because the wave-design corner does in fact depend on which elevator
model is believed, a rule whose release decision is robust to that choice is
operationally relevant, not merely formally robust against a hypothetical
uncertainty that never materialises.

## 理由 (RATIONALE)

两处机械修正：(a) "Theorem 2's collapse" 按新编号改为 "Theorem 1's collapse
under the chain dominance of Proposition 2"，顺带把主定理归属再次指回
Proposition 2；(b) "dispatch decision" 是 TERMINOLOGY 第 5 节明令禁止的表述
（Hedge Rule 只放行波次，不调度 AMR），改为 "release decision"。其余内容
（探针的非门槛性质、0.75 秩相关、五/六稳定性）原样保留。

---

---

# Edit 13: Section 5.5 ablation A3: reference updated to Proposition 3

## 修改前 (BEFORE)

Source: `paper_draft/section5_draft_v0_1.md`, lines 262-265.

> **Estimator (A3).** The cell-mean GAP is in fact marginally more stable than
> the cell-median (bootstrap SD 0.015 vs 0.021). We retain the cell-median for
> consistency with the SPO-regret equivalence of Theorem 1, which is stated for
> the median, and not on robustness grounds.

## 修改后 (AFTER)

**Estimator (A3).** The cell-mean GAP is in fact marginally more stable than
the cell-median (bootstrap SD 0.015 vs 0.021). We retain the cell-median for
consistency with the SPO bridge (Proposition 3, named Theorem 1 in the
pre-registration), which is stated for the median, and not on robustness
grounds.

## 理由 (RATIONALE)

编号同步（Theorem 1 → Proposition 3）。因预注册文档（frozen，不可改）在 A3
条目中以 "Theorem 1" 指称该结果，此处保留一个括号内的对照说明，避免读者在
比对预注册文档时误以为指向新的 Theorem 1（minimax collapse）。这一句是诚实
披露而非改判：保留中位数的理由不变。

---

---

# Edit 1. Correct the simulator description in Section 5.1 ("event-driven" is factually wrong)

## 修改前 (BEFORE)

`paper_draft/section5_draft_v0_1.md`, lines 24-26:

> The event-driven simulator of Section 4 realizes the wave makespan
> `C_max(W; M)` under the three elevator models: `M1` (throughput aggregation),
> `M2` (true co-occupancy batching), and `M3` (stochastic batching).

## 修改后 (AFTER)

> The wave makespan `C_max(W; M)` is realized by the deterministic simulator of
> Section 3.3, a closed-form sequential time-accumulator rather than an
> event-driven discrete-event model: it processes the orders of a wave in
> sequence, assigns each to the earliest-available AMR, and accumulates a
> five-phase elevator-trip cost (wait, reposition, load, travel, unload) into a
> scalar makespan, so identical inputs reproduce the identical makespan (under
> `M3`, identical inputs and random seed). The simulator evaluates the three
> elevator models: `M1` (throughput abstraction), `M2` (true co-occupancy
> batching), and `M3` (stochastic batching).

## 理由 (RATIONALE)

panel_methods 致命缺陷 1 与 panel_novelty 致命缺陷 7 都指出：仿真器是闭式顺序时间累加器（simulator.py 逐单遍历、指派给最早空闲 AMR），而 5.1 节称其为 "event-driven"，在仿真类 Q1 期刊上这属于方法学误述，审稿人核对代码即可证伪。修改后如实描述机制并指向新的 3.3 节（仿真器细节小节，另一工作包交付）。顺带把 "throughput aggregation" 统一为 TERMINOLOGY 规定的规范名 "throughput abstraction"。全 paper_draft 检索确认 "event-driven" 仅另出现一次（见 Edit 1b）。

---

---

# Edit 2. Replace the "balanced fraction" sentence with the honest fractional-design disclosure

## 修改前 (BEFORE)

`paper_draft/section5_draft_v0_1.md`, lines 26-33 (continuing the same paragraph):

> The
> publication-scale grid spans a balanced one-third fraction of the
> warehouse-configuration space: floors `F ∈ {3,5,8}`, AMR fleet
> `|A| ∈ {5,15,30}`, elevators `E ∈ {1,2}`, and demand pattern ∈ {uniform,
> clustered, diurnal}. The fraction is generated by the defining relation
> `demand = (F + |A|) mod 3` crossed with both `E` levels, yielding **18
> configurations** in which every factor level is equi-represented (each `F`,
> `|A|`, and demand level appears six times).

## 修改后 (AFTER)

> The publication-scale grid is an 18-configuration one-third fraction of the
> full `3 × 3 × 2 × 3 = 54` factorial over floors `F ∈ {3,5,8}`, AMR fleet
> `|A| ∈ {5,15,30}`, elevators `E ∈ {1,2}`, and demand pattern ∈ {uniform,
> clustered, diurnal}. The fraction is generated by the defining relation
> `demand_idx = (F_idx + |A|_idx) mod 3` over the factor-level indices, crossed
> with both `E` levels. Each `F`, `|A|`, and demand level appears in six
> configurations and each `E` level in nine, so the fraction is level-balanced
> in every one-dimensional margin; it is not, however, a design from which main
> effects can be separated. The defining relation aliases the `F`, `|A|`, and
> demand main effects with one another, so none of the three is separately
> identifiable from this grid, and any marginal contrast in one of them is
> simultaneously a contrast in the other two. Per-factor summaries reported
> below are therefore descriptive of the sampled grid, not causal factor
> effects. All pre-registered gates operate on per-cell quantities and are
> unaffected by the aliasing. Table X lists the 18 configurations, their factor
> levels, and their block memberships.

(The following sentence, "The grid is organized into three blocks: ...", remains unchanged.)

## 理由 (RATIONALE)

panel_methods 致命缺陷 4：`phase5_config.py` 第 64 行的定义关系 `demand = FACTOR_DEMAND[(fi + ai) % 3]` 使 F、|A|、demand 主效应互为别名，而 5.1 节称网格 "balanced"，属于未披露的混淆，审稿人重构网格后会视为统计幼稚或有意隐瞒。修改后：保留"边际水平均衡"这一真实性质，同时明确声明主效应不可分离，并把定义关系改写为指标形式（原文 `demand = (F + |A|) mod 3` 写在原始值上，数学上也是错的）。"Table X" 指向新的实验设计表（另一工作包交付，编号待定）。CLAUDE.md 亦明确记载 "F is confounded with |A| and demand; no clean F main-effect is identifiable"。

---

---

# Edit 2b. Caveat on the per-demand GAP contrasts in Section 5.2

## 修改前 (BEFORE)

`paper_draft/section5_draft_v0_1.md`, lines 102-106:

> Non-resolution concentrates where wave
> structure is mechanistically diluted: under diurnal demand only 17/24 resolve
> (mean `GAP = 0.046`), against 20/24 under uniform (`0.052`) and 20/24 under
> clustered demand (`0.082`), where temporal spreading no longer dilutes the
> `(C, I)` signal (Figure 3).

## 修改后 (AFTER)

> Non-resolution concentrates where wave structure is mechanistically diluted:
> under diurnal demand only 17/24 sub-cells resolve (mean `GAP = 0.046`),
> against 20/24 under uniform (`0.052`) and 20/24 under clustered demand
> (`0.082`), where temporal spreading no longer dilutes the `(C, I)` signal
> (Figure 3). Because the fractional design aliases demand with `F` and `|A|`
> (Section 5.1), these per-demand contrasts describe the sampled grid and
> should not be read as pure demand-pattern effects.

## 理由 (RATIONALE)

panel_methods 致命缺陷 4 明确点名："per-demand GAP contrasts 0.082/0.052/0.046 are partially F-and-|A| contrasts"。Edit 2 的总披露之外，正文中实际给出按 demand 分组数字的这一句需要就地加注，否则披露与用法脱节。数字本身不变，仅限定其解读。

---

---

# Edit 2c. Caveat on corr(F, GAP) = -0.18 wherever it enters the manuscript

## 修改前 (BEFORE)

The sentence does not appear in `section5_draft_v0_1.md`; its source is the results report `prototype/results/v0_5_phase5.md`, lines 50-53 and 105-106 (quoted verbatim; if the Word master's Section 5 has carried it over, replace it there):

> Mean GAP = 0.0600 (H_up 0.0430 + M_Phi 0.0170). Per demand: clustered 0.082
> (D1-d 20/24), uniform 0.052 (20/24), **diurnal 0.046 (17/24)** — the
> decomposition is weakest under diurnal demand, where T dilutes the (C,I)
> signal. `corr(F, GAP) = −0.18` — a mild decline with floor count (see §7).

> - **`GAP` vs `F`**: `corr = −0.18` — a *mild* decline of GAP with floor count.
>   Weakly triggers the hook; logged as a minor effect, not a reversal.

## 修改后 (AFTER)

Manuscript-ready sentence to use wherever this statistic is reported (publication scale, Phase 5 Block A):

> Across the 72 Block A sub-cells, `corr(F, GAP) = −0.18`, a mild negative
> association between floor count and the gap. Under the one-third fraction's
> defining relation, `F` is aliased with `|A|` and demand (Section 5.1), so
> this correlation describes the grid as sampled and cannot be read as a causal
> effect of floor count; a de-aliasing fraction would be required to isolate
> it.

## 理由 (RATIONALE)

panel_methods 致命缺陷 4 点名 corr(F, GAP) = -0.18 邀请读者做设计无法识别的主效应解读。该句目前只存在于结果报告 v0_5_phase5.md（第 53、105 行）；按 W6 任务要求提供带别名警示的正文版本，防止它被原样拼进 5.1/5.2 节或 Word 母稿。注意负号使用普通连字符或 LaTeX 负号均可，不引入 em-dash。

---

---

# W1 Open Issues 中属于本章的作者事项

1. Open issue 4：粘贴前对照工件复核的数字——`U_c(0.05)` 最大 3.5%（config 7）与 0.53%（config 1，`v0_5_phase5_blockC.json`）；prototype 尺度 `U_c` 51-94 单位与 σ=0.20 单配置角翻转（`v0_2_phase4_v2_m5_delta.json`）；全局半径消融（`v0_2_D2_wasserstein_dro.json` 的 `c_star_DRO_global_radius` 字段）。
2. Open issue 6：冻结预注册以 "Theorem 1" 指称 SPO 结果——可用 §5 开头一个脚注统一对照（"pre-registration Theorem 1 = Proposition 3; Theorem 2/3 = Theorem 1 + Corollary 3"），替代 Edit 13 的括号注反复出现。
