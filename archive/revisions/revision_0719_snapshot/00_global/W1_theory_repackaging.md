---
title: "W1: Theory repackaging (statement-level rewrites of Section 4's formal results)"
date: 2026-07-08
sources_consulted:
  - paper_draft/TERMINOLOGY.md
  - paper_draft/theorems_m4.md
  - paper_draft/theorems_m5.md
  - paper_draft/section4_draft_v0_1.md
  - paper_draft/section5_draft_v0_1.md
  - paper_draft/methodology_v0_2.md
  - paper_draft/Abstract/abstract_v1.0.md
  - paper_draft/Introduction/introduction_v1.0.md
  - prototype/src/analysis_D1_spo_equivalence.py
  - prototype/src/analysis_D2_wasserstein_dro.py
  - scratchpad/panel_theory.json (audit findings)
status: "draft for author review"
---

# W1 Theory repackaging

This document implements five changes motivated by the theory-panel audit
(panel_theory.json): (1) demote "Theorem 1" (the SPO identity) to a
Proposition framed as a definitional bridge, and rescope gate D1-c as a
pipeline consistency check; (2) restate the minimax collapse with honest scope
(exact over {M1, M2} only, K-model corollary added, M3 routed through the
epsilon bound); (3) downgrade the DRO clause to a Corollary with an explicit
defense of the corner-calibrated radius and an explicit summary-statistic
scope; (4) rebill Proposition 2 (conditional chain dominance) as the paper's
main theoretical result and add a "what the theory does and does not claim"
paragraph; (5) fix the Theorem-2-vs-Theorem-3 numbering inconsistency with one
final scheme and a find/replace table.

**Final numbering scheme adopted throughout this document:**

| Label | Result | Status vs current draft |
|---|---|---|
| Proposition 1 | Bound-and-Gap decomposition (GAP = H_up + M_Phi) | unchanged |
| Proposition 2 | conditional chain dominance | unchanged (heavily cross-referenced; kept for continuity) |
| Proposition 3 | SPO bridge (demoted from "Theorem 1") | demoted, reframed |
| Theorem 1 | minimax collapse over {M1, M2} (was clause 1 of "Theorem 2") | rescoped |
| Corollary 1 | refinement monotonicity | unchanged |
| Corollary 2 | one-sided epsilon bound (routes M3) | unchanged number, expanded text |
| Corollary 3 | Wasserstein-DRO certification (was clause 2 of "Theorem 2", = "Theorem 3" in methodology_v0_2.md and the D-scripts) | downgraded to Corollary |
| Corollary 4 | K-model collapse under pairwise dominance | new |

Rationale for the scheme: Proposition 2, Corollary 1, and Corollary 2 are
referenced by number in TERMINOLOGY.md, the Introduction, the section 5 draft,
the Appendix skeleton, and two splice files; renumbering them would create
cross-document churn with high error risk, so they keep their numbers. The
one cosmetic cost is that Proposition 3 appears in section 4.1.2, before
Proposition 2 in section 4.2.1; see Open Issues for the alternative swap if
the author prefers strict order-of-appearance numbering.

---

# Edit 1: Section 4 opening paragraph (rebalanced billing; dispatch-wording fix)

## 修改前 (BEFORE)

Source: `paper_draft/section4_draft_v0_1.md`, lines 13-23.

> Section 3 cast wave release coordination as a stochastic optimization whose
> objective `C_max(W; M)` is simulator-realized and whose decision space is
> combinatorial. Rather than search that space directly, we develop two
> analytical tools that operate on the structured representation `Φ(W)` and on a
> finite partition of `Φ`-space. The first, a **Bound-and-Gap framework**,
> decomposes the value of wave-structure information into two non-negative
> components and rests on a decomposition theorem (§4.1). The second, a
> **Model-Dominance Hedge Rule**, resolves uncertainty over the elevator model
> into a single closed-form dispatch decision and rests on a minimax-collapse
> theorem (§4.2). Each tool is stated as a theorem here and validated at
> publication scale in Section 5; §4.3 states the predictions that link the two.

## 修改后 (AFTER)

Section 3 cast wave release coordination as a stochastic optimization whose
objective `C_max(W; M)` is simulator-realized and whose decision space is
combinatorial. Rather than search that space directly, we develop two
analytical tools that operate on the structured representation `Φ(W)` and on a
finite partition of `Φ`-space. The first, a **Bound-and-Gap framework**,
decomposes the value of wave-structure information into two non-negative
components (§4.1). The second, a **Model-Dominance Hedge Rule**, resolves
uncertainty over the elevator model into a single closed-form wave-release
decision (§4.2). The formal backbone of the section is deliberately graded,
and we bill each result as what it is. The substantive theoretical result is
Proposition 2, a conditional sample-path dominance between the two elevator
models with an identified unique failure channel. The minimax collapse
(Theorem 1) and its distributionally-robust reading (Corollary 3) are short
consequences of that dominance. The decomposition (Proposition 1) and its
predict-then-optimize bridge (Proposition 3) are exact identities whose value
is diagnostic and positional, not derivational. §4.3 states the predictions
that link the tools to the publication-scale evaluation of Section 5 and
closes with an explicit statement of what the theory does and does not claim.

## 理由 (RATIONALE)

对应 panel_theory.json 第 6 条 fatal flaw（"collapse 子句本身只是一步观察，
实质内容全在 Proposition 2"）及其 defense（"rebalance the billing: 把
Proposition 2 作为主定理，collapse 与 DRO 读法作为其推论"）。原开篇把两个工具
都说成 "rests on a theorem"、"Each tool is stated as a theorem"，正是审稿panel
指出的 over-billing。另外原文 "closed-form dispatch decision" 违反
TERMINOLOGY.md 第 5 节规则（Hedge Rule 是放行规则，绝不能称 dispatch），一并
改为 "wave-release decision"。

---

# Edit 2: Section 4.1.2 rewritten: "Theorem 1" demoted to Proposition 3, framed as a definitional bridge

## 修改前 (BEFORE)

Source: `paper_draft/section4_draft_v0_1.md`, lines 61-83.

> ### 4.1.2 The policy component is an SPO regret
>
> The policy component admits a second reading that places the framework inside
> the predict-then-optimize literature. Treat "which corner to release a wave
> from" as a decision over `Q`; the true cost vector is `(m_q)_{q∈Q}` and the
> oracle solves `argmin_q m_q`. A *partition-constant predictor* is any cost
> vector that is constant on each corner (the natural predictor class on a
> finite partition) and its Smart-Predict-then-Optimize (SPO) loss is the
> realized-minus-oracle cost of the corner it induces.
>
> **Theorem 1 (D1: SPO-regret equivalence).** *The policy component `M_Φ`
> equals the SPO regret of the Φ-induced partition-constant predictor, namely
> `(m_q_Φ − m_q_min)/m_0`.*
>
> *Proof sketch.* The Φ-informed predictor induces the decision `q_Φ`; its SPO
> loss against the true cost vector is `m_q_Φ − m_q_min`; normalizing by `m_0`
> gives `M_Φ` directly (full statement and proof in Appendix). ∎
>
> Theorem 1 positions the Bound-and-Gap framework as the *partition perspective*
> on SPO: where the prediction-to-decision regret literature bounds an
> algorithm's loss at training time, `M_Φ` is a post-hoc information-value gap on
> a fixed partition. The cell-median is used throughout for consistency with this
> equivalence, which is stated for the median.

## 修改后 (AFTER)

### 4.1.2 A definitional bridge to predict-then-optimize

The policy component admits a second reading that places the framework inside
the predict-then-optimize literature. Treat "which corner to release a wave
from" as a decision over `Q`; the true cost vector is `(m_q)_{q∈Q}` and the
oracle solves `argmin_q m_q`. A *partition-constant predictor* is any cost
vector that is constant on each corner (the natural predictor class on a
finite partition), and its Smart-Predict-then-Optimize (SPO) loss (Elmachtoub
and Grigas, 2022) is the realized-minus-oracle cost of the corner it induces.

**Proposition 3 (SPO bridge).** *The policy component `M_Φ` equals the SPO
regret of the Φ-induced partition-constant predictor. Unfolding the SPO loss
of the predictor that induces the decision `q_Φ` against the true cost vector
`(m_q)` gives `m_q_Φ − m_q_min`; normalizing by `m_0` gives `M_Φ`.* ∎

We state this as a proposition rather than a theorem, and we are explicit
about its epistemic status: it is a definitional identity, obtained by
unfolding the SPO loss on a four-point decision space. Its value is the
connection it establishes, not the derivation it contains. The identity
certifies that `M_Φ` is not an ad hoc diagnostic: it is exactly the decision
loss studied by the predict-then-optimize literature, restricted to the
partition-constant predictor class, so the guarantees and training methods
developed for that loss apply verbatim to the component our decomposition
isolates as recoverable. Where the prediction-to-decision literature bounds an
algorithm's loss at training time, `M_Φ` reads the same object post hoc, as an
information-value gap on a fixed partition. The cell median is used throughout
for consistency with this bridge, which is stated for the median.

## 理由 (RATIONALE)

对应 panel_theory.json 第 1 条 fatal flaw（CRITICAL）："Theorem 1 是把 SPO 损失
定义在 4 角点决策空间上展开得到的恒等式，包装成定理；承诺的附录证明不存在。"
其 defense 明确要求 "Demote Theorem 1 to a Remark or Proposition explicitly
framed as a positioning identity ('the value is the bridge, not the
derivation')"。改写后：(a) 编号降为 Proposition 3；(b) 标题从断言式改为
"definitional bridge"；(c) 删除 "full statement and proof in Appendix" 这句
指向不存在证明的话（展开定义即为完整证明，随语句给出）；(d) 正文直接自陈其
恒等式身份，先发制人化解 "repackaged definition" 的审稿意见。补上 Elmachtoub
and Grigas (2022) 期刊年份引用（TERMINOLOGY 第 9 节）。

---

# Edit 3: Section 4.2.1 minimax setup: honest family scope

## 修改前 (BEFORE)

Source: `paper_draft/section4_draft_v0_1.md`, lines 119-128.

> The elevator model is exogenous to wave composition (§3, Assumption A5), but an
> operator may not know which model `M ∈ {M1, M2, M3}` describes their
> warehouse. The conservative response is the **minimax wave-corner selection**
>
> > `c* = argmin_{c∈Q} max_{M∈ℳ} s[ C_max(W; M) | W ∈ c ]`,
>
> where `s` is any monotone summary statistic of the makespan distribution
> (median, mean, or any quantile). Evaluated naively, `c*` requires the operator
> to identify the true model online. The Hedge Rule removes that requirement by
> exploiting a structural relation among the models.

## 修改后 (AFTER)

The elevator model is exogenous to wave composition (§3, Assumption A5), but
an operator may not know which model describes their warehouse. Write the
candidate family as `ℳ = {M1, M2, M3}`. Within it, the exact theory of this
section concerns the deterministic pair `{M1, M2}`: the stochastic extension
`M3` perturbs `M2` symmetrically, is not comparable to it in the dominance
order we establish, and enters the theory only through the approximation bound
of Corollary 2 (§4.2.3). The conservative response to model uncertainty is the
**minimax wave-corner selection** over a family `ℳ' ⊆ ℳ`,

> `c* = argmin_{c∈Q} max_{M∈ℳ'} s[ C_max(W; M) | W ∈ c ]`,

where `s` is a monotone summary statistic of the makespan distribution
(median, mean, or any quantile; our working statistic is the median).
Evaluated naively, `c*` requires the operator to identify the true model
online. The Hedge Rule removes that requirement by exploiting a structural
relation between the two deterministic models.

## 理由 (RATIONALE)

对应 panel_theory.json 第 6 条 fatal flaw（MAJOR）："Theorem 2 的量词范围超出
其证明：§4.2.1 把 minimax 定义在 {M1, M2, M3} 上，但 collapse 证明只覆盖
{M1, M2}；D2 脚本自己写明 M3 'is not part of the chain'。" 该 defense 要求
"Restate Theorem 2 with the correct scope... route M3 explicitly through
Corollary 2 as the eps-approximate member"。改写在 minimax 问题一出场就把
家族范围讲清楚，使后文 Theorem 1（只对 {M1, M2}）的陈述与设定一致，堵住
"定理对其量化的家族为假" 的指控。

---

# Edit 4: Section 4.2.1 closing paragraph: cross-reference fix (DRO clause becomes Corollary 3)

## 修改前 (BEFORE)

Source: `paper_draft/section4_draft_v0_1.md`, lines 154-165.

> **Why the condition is structural, not cosmetic.** Because `M1` instantiates
> `E·c` single-rider servers and `M2` only `E` batching servers, the dominance is
> a structural inequality (more independent single-rider slots weakly beat fewer
> batching servers), not a modelling identity. It therefore cannot hold
> unconditionally, and batch-overtaking is the genuine channel that breaks it.
> This is what makes the per-wave frequency reported in Section 5 a measurement,
> not a self-consistency check. We keep two statements distinct: the *scalar,
> sample-path* ordering of Proposition 2, whose frequency Section 5 reports, and
> the *distribution-level* first-order stochastic dominance `F_{M1} ≥ F_{M2}` that
> Theorem 2's distributionally-robust clause invokes; the latter holds exactly in
> all 24 cells, while `M3`'s lognormal residual is routed to Corollary 2's bound
> (§4.2.3).

## 修改后 (AFTER)

**Why the condition is structural, not cosmetic.** Because `M1` instantiates
`E·c` single-rider servers and `M2` only `E` batching servers, the dominance is
a structural inequality (more independent single-rider slots weakly beat fewer
batching servers), not a modelling identity. It therefore cannot hold
unconditionally, and batch-overtaking is the genuine channel that breaks it.
This is what makes the per-wave frequency reported in Section 5 a measurement,
not a self-consistency check. We keep two statements distinct: the *scalar,
sample-path* ordering of Proposition 2, whose frequency Section 5 reports, and
the *distribution-level* first-order stochastic dominance `F_{M1} ≥ F_{M2}`
that the distributionally-robust certification of Corollary 3 invokes
(§4.2.4); the latter holds exactly in all 24 Block C cells at publication
scale, while `M3`'s lognormal residual is routed to Corollary 2's bound
(§4.2.3).

## 理由 (RATIONALE)

配合 Edit 6/7 的重编号：原文引用 "Theorem 2's distributionally-robust clause"，
在新方案下该内容是 Corollary 3（§4.2.4）。同时按 TERMINOLOGY 第 8 节给
"all 24 cells" 补上量表标签（publication scale, Block C）。注意：panel 第 4 条
flaw（假设 (a)/(b) 在自由指派 harness 下未被强制）质疑本段 "a measurement,
not a self-consistency check" 一句；该修复属于另一个工作包（matched-assignment
重验证），此处保留原句，见 Open Issues。

---

# Edit 5: Section 4.2.2 rewritten: Theorem 1 (collapse over {M1, M2} only); DRO clause removed to Corollary 3

## 修改前 (BEFORE)

Source: `paper_draft/section4_draft_v0_1.md`, lines 167-206.

> ### 4.2.2 Collapse under chain dominance and its DRO equivalence
>
> **Theorem 2 (D2: minimax collapse and DRO equivalence).** *Under chain
> dominance, the minimax corner collapses to the corner optimal for the
> dominant model,*
>
> > `c* = argmin_{c∈Q} s[ C_max(W; M2) | W ∈ c ]`,
>
> *and this corner coincides with the solution of the Wasserstein
> distributionally-robust problem whose ambiguity ball, centred at the
> nominal model and sized to the model-discrepancy radius, contains the family.*
>
> *Proof sketch.* Monotonicity of `s` carries the per-wave dominance to the
> conditional statistics, so `max_M s[·|c] = s[C_max(·; M2)|c]` for every
> corner, and the outer `argmin` reduces accordingly. For the second clause, the
> Wasserstein-1 distance between the nominal and dominant models equals their
> mean gap exactly under dominance, so the worst case over the ambiguity ball is
> attained at the dominant model; the two `argmin`s therefore agree (full proof
> in Appendix). ∎
>
> Theorem 2 yields a **closed-form wave-release rule** (Figure 2): release waves
> from the corner that is optimal under the true-batching model `M2`, with no
> online model identification and no distributionally-robust optimization to
> solve. Where robust scheduling hedges over a parameter within one model class,
> this rule hedges across *structurally distinct* model classes by exploiting a
> verified dominance. The contribution is therefore not that robust dispatch needs
> heavy machinery, but the reverse: the simplest possible rule, hedge against the
> single most conservative model, is provably the distributionally-robust optimum,
> resting on a condition (Proposition 2) that holds in 99.2% of waves with a
> bounded, mechanistically identified residual.
>
> **Figure 2.** The Model-Dominance Hedge Rule. (a) Chain dominance of `M2`
> over `M1` in cumulative-distribution terms: `F_{M_1}(t) ≥ F_{M_2}(t)`
> pointwise, so `M2` is stochastically larger and the worst case in the
> Wasserstein-1 ball `B_ρ(M1)` of radius `ρ = W₁(M1, M2)` is attained at `M2`
> (Theorem 2's DRO clause). (b) The closed-form decision flow: verify chain
> dominance empirically, then follow the `M2`-optimal corner; no online model
> identification is required. *(Source:
> `prototype/results/figures/fig_hedge_rule_schematic.png`; generator
> `prototype/src/figure_methodology_schematics.py`.)*

## 修改后 (AFTER)

### 4.2.2 Collapse under chain dominance

**Theorem 1 (minimax collapse over {M1, M2}).** *Let `s` be any monotone
summary statistic. If chain dominance holds per wave, `C_max(W; M1) ≤
C_max(W; M2)` for every `W`, then the minimax corner over the deterministic
pair `{M1, M2}` collapses to the corner optimal for the dominant model:*

> `c* = argmin_{c∈Q} s[ C_max(W; M2) | W ∈ c ]`.

*Proof.* Per-wave dominance carries to every corner-conditional distribution,
so monotonicity of `s` gives `s[C_max(·; M1) | c] ≤ s[C_max(·; M2) | c]` for
every corner `c`. The inner maximum is therefore attained at `M2` in every
corner, and the outer `argmin` reduces to the `M2`-optimal corner. ∎

Two remarks on scope. First, the theorem is stated for the two-model family
for which it is proved. It does not quantify over `M3`: the stochastic model
breaks per-wave dominance symmetrically, and every claim involving `M3` is
routed through the approximation bound of Corollary 2 (§4.2.3); the extension
to larger families under pairwise dominance is Corollary 4 (§4.2.4). Second,
the mathematical content of the collapse is deliberately light: granted
Proposition 2's dominance, the reduction is a few lines. The substance of the
Hedge Rule is Proposition 2 itself; the collapse is the step that turns that
substance into a decision rule.

Theorem 1 yields a **closed-form wave-release rule** (Figure 2): release waves
from the corner that is optimal under the true-batching model `M2`, with no
online model identification and no robust-optimization program to solve. Where
robust scheduling hedges over a parameter within one model class, this rule
hedges across *structurally distinct* model classes by exploiting a verified
dominance. The contribution is therefore not that robust wave release needs
heavy machinery, but the reverse: the simplest possible rule, hedge against
the single most conservative model, is exactly the minimax choice over the
deterministic pair, rests on a condition (Proposition 2) that holds in 99.2%
of waves at publication scale with a bounded, mechanistically identified
residual, and additionally admits a distributionally-robust certification
(Corollary 3, §4.2.4).

**Figure 2.** The Model-Dominance Hedge Rule. (a) Chain dominance of `M2`
over `M1` in cumulative-distribution terms: `F_{M_1}(t) ≥ F_{M_2}(t)`
pointwise, so `M2` is stochastically larger and the worst case in the
Wasserstein-1 ball `B_ρc(M1)` of corner-calibrated radius `ρ_c = W₁(M1, M2 | c)`
is attained at `M2` (Corollary 3, §4.2.4). (b) The closed-form decision flow:
verify chain dominance empirically, then follow the `M2`-optimal corner; no
online model identification is required. *(Source:
`prototype/results/figures/fig_hedge_rule_schematic.png`; generator
`prototype/src/figure_methodology_schematics.py`.)*

## 理由 (RATIONALE)

对应 panel_theory.json 第 6 条 flaw（陈述范围超出证明范围：原定理量化在
{M1, M2, M3} 上而只对 {M1, M2} 成立）与第 2 条 flaw（DRO 子句按构造成立，
应降级）。改写把 collapse 单独立为 Theorem 1，明确只对 {M1, M2}，proof sketch
升级为完整（本来就只有几行）的 proof，DRO 子句整体移出到 Corollary 3（Edit 7），
并删除指向不存在附录证明的 "full proof in Appendix"。同时按 defense 要求
主动自陈 collapse 数学内容轻、实质在 Proposition 2，实现 billing 再平衡。
"robust dispatch" 改为 "robust wave release"（TERMINOLOGY 第 5 节），99.2%
标注 publication scale。图注中的 "Theorem 2's DRO clause" 同步改为
Corollary 3，半径改为 corner-calibrated 写法与 Corollary 3 一致。

---

# Edit 6: Section 4.2.3 rewritten: Corollary 2 as the explicit route for M3, with epsilon and U_c quantified

## 修改前 (BEFORE)

Source: `paper_draft/section4_draft_v0_1.md`, lines 209-218.

> Exact almost-sure dominance is a strong assumption; the stochastic model `M3`
> satisfies it only approximately. **Corollary 2 (one-sided ε-bound)** weakens
> the hypothesis to `P[ C_max(W;M2) ≥ C_max(W;M1) ] ≥ 1 − ε`. Then the
> per-corner median gap is bounded by a one-sided quantity
> `U_c(ε) = F₂⁻¹(½ + ε) − F₂⁻¹(½)`, computable from the makespan quantiles
> alone, and the collapse of Theorem 2 remains exact whenever the inter-corner
> gaps in the dominant-model ranking exceed `max_c U_c(ε)`. The worst-case loss
> from following the rule when the operator's model is in fact mis-specified is
> thus bounded by a quantity the operator can evaluate from their own data.

## 修改后 (AFTER)

Exact almost-sure dominance is a strong assumption, and the stochastic model
`M3` does not satisfy it: its lognormal per-phase noise perturbs `M2`
symmetrically, so `M3` is not a member of the dominance chain. `M3` therefore
enters the theory only through the following bound. **Corollary 2 (one-sided
ε-bound).** *Weaken the hypothesis to `P[ C_max(W; M2) ≥ C_max(W; M1) ] ≥ 1 − ε`
per corner, and let `s` be the median. Then the per-corner median gap is
bounded by the one-sided quantity `U_c(ε) = F₂⁻¹(½ + ε) − F₂⁻¹(½)`, computable
from the makespan quantiles alone, and the collapse of Theorem 1 remains exact
whenever the inter-corner gaps in the dominant-model ranking exceed
`max_c U_c(ε)`.* Corollary 2 is stated for the median, and it is the clause
through which every `M3` claim in this paper is routed. It also quantifies the
price of the approximation at both ends of the spectrum. At publication scale
the bound is small where the rule operates: `U_c(0.05)` never exceeds 3.5% of
the cell median makespan across the 24 Block C cells (Section 5.3). At
prototype scale, the chain-broken control (`M2` versus `M3` at `σ = 0.20`)
drives the violation mass to roughly `ε ≈ 0.5` and `U_c` to 51 to 94 wave-time
units, exceeding the inter-corner gaps; this is exactly the knife-edge regime
in which the corollary withholds the collapse, and one prototype configuration
does flip its selected corner there. The worst-case loss from following the
rule when the operator's model is in fact mis-specified is thus bounded by a
quantity the operator can evaluate from their own data.

## 理由 (RATIONALE)

对应 panel_theory.json 第 6 条 flaw 的 defense："route M3 explicitly through
Corollary 2 as the eps-approximate member, with the epsilon and U_c
quantified"。改写点：(a) 开头明确 M3 不在支配链内（与
analysis_D2_wasserstein_dro.py 文档字符串一致），Corollary 2 是 M3 的唯一
理论通道；(b) 引用对象从 "Theorem 2" 更新为 "Theorem 1"；(c) 把 ε 与 U_c 的
两端数值写进正文并按 TERMINOLOGY 第 8 节分别标注 publication scale（Block C
的 3.5%）与 prototype scale（σ=0.20 控制组的 51-94 单位、单配置翻转）；
(d) 明确 Corollary 2 的统计量范围是中位数（配合 Edit 7 的统计量范围声明）。

---

# Edit 7: New Section 4.2.4: Corollary 3 (DRO certification) and Corollary 4 (K-model collapse)

## 修改前 (BEFORE)

(no existing text; new section, inserted after §4.2.3 and before §4.3)

## 修改后 (AFTER)

### 4.2.4 Two consequences: a DRO certification and the K-model extension

The collapse admits a reading in the language of distributionally robust
optimization, which we state as a corollary rather than as a stand-alone
theorem because it follows from two classical one-dimensional facts once
dominance is granted.

**Corollary 3 (Wasserstein-DRO certification; mean summary).** *Take the
operator's nominal model to be `M1` and, per corner `c`, form the
Wasserstein-1 ambiguity ball `B_ρc(M1 | c)` with the corner-calibrated radius
`ρ_c = W₁(M1, M2 | c)`. If `M1 ⪯ M2` in first-order stochastic dominance per
corner, then the distributionally-robust corner for the mean makespan
objective coincides with the Hedge corner:*

> `argmin_{c∈Q} sup_{Q'∈B_ρc(M1|c)} E_{Q'}[ C_max | c ]
>  = argmin_{c∈Q} E_{M2}[ C_max | c ]`.

*Proof.* Two facts about distributions on the real line. First,
`W₁(M1, M2 | c) ≥ | E_{M2}[C_max|c] − E_{M1}[C_max|c] |`, with equality if and
only if one distribution first-order dominates the other; under the dominance
hypothesis, `ρ_c = E_{M2}[C_max|c] − E_{M1}[C_max|c]`. Second, for a
1-Lipschitz objective, the worst case over a Wasserstein-1 ball equals the
nominal value plus the radius (Mohajerin Esfahani and Kuhn, 2018; Blanchet and
Murthy, 2019), so `sup_{Q'∈B_ρc} E_{Q'}[C_max|c] = E_{M1}[C_max|c] + ρ_c =
E_{M2}[C_max|c]`. The DRO objective therefore equals the Hedge value corner by
corner, and the two `argmin`s coincide. ∎

We call this a certification, and we defend the radius choice explicitly
rather than leave it implicit. Per corner, `ρ_c` is the smallest radius for
which the ball around the nominal model contains the rival model: `B_ρc(M1|c)`
is the minimal honest ambiguity set, in the sense that any smaller ball
excludes a model the operator considers possible and any larger ball hedges
against distributions no candidate model generates. The per-corner calibration
is necessary, not cosmetic. With a single global radius `ρ`, the inflation
term is constant across corners, the DRO `argmin` degenerates to
`argmin_c E_{M1}[C_max|c]`, and the correspondence with the Hedge corner is
lost; we ran exactly this ablation (prototype scale,
`analysis_D2_wasserstein_dro.py`) and observed the degeneration, which is why
the corollary is stated for the corner-calibrated radius. Finally, the
summary-statistic scope of the formal results differs and we state it
explicitly: Theorem 1 holds for any monotone summary and is applied at the
median, Corollary 2 is stated for the median, and Corollary 3 is stated for
the mean, the statistic for which the Wasserstein-1 worst case has the closed
form used in the proof.

**Corollary 4 (K-model collapse under pairwise dominance).** *Let
`ℳ' = {M_(1), …, M_(K)}` be any finite model family containing a maximal
element `M_(K)` with `C_max(W; M_(k)) ≤ C_max(W; M_(K))` per wave for every
`k`. Then for any monotone summary `s`, the minimax corner over `ℳ'` collapses
to the `M_(K)`-optimal corner.*

*Proof.* Per-wave dominance carries to every corner-conditional distribution,
so `s[C_max(·; M_(k)) | c] ≤ s[C_max(·; M_(K)) | c]` for all `k` and every
corner `c`. The inner maximum over the family is attained at `M_(K)` in every
corner, and the `argmin` reduces exactly as in Theorem 1. ∎

Corollary 4 says the two-model statement is not an artifact of `K = 2`:
whenever the family has a most conservative member in the pairwise per-wave
dominance order, hedging against that member alone is exactly minimax over the
whole family. What it does not do is re-admit `M3`, which is not comparable to
`M2` in this order; `M3` remains routed through Corollary 2.

## 理由 (RATIONALE)

对应 panel_theory.json 第 2 条 fatal flaw（CRITICAL）的 Path A defense：
"soften the claim ... to 'admits a DRO certification: for the corner-calibrated
radius rho_c = W1(M1,M2|c), the Hedge corner is exactly the DRO optimum',
state it as a Corollary"，并要求 (a) 显式辩护半径选择（最小诚实模糊集）、
(b) 把 global-radius 消融作为"校准必要性"的证据写进正文、(c) 显式声明均值/
中位数的统计量范围、(d) 把只存在于代码 docstring 的推导提升为正文数学（两个
一维事实 + 引用 Mohajerin Esfahani & Kuhn 2018 / Blanchet & Murthy 2019）。
同时落实第 6 条 flaw 的 K-model corollary（约 5 行证明，顺带关闭
theorems_m5.md §7 的 open item "Extend to |M| > 2"）。消融数据来自 v0_2 原型
数据，已按规则标注 prototype scale。

---

# Edit 8: Section 4.3 rewritten: predictions under new numbering, plus the "what the theory does and does not claim" paragraph; footer with scale labels

## 修改前 (BEFORE)

Source: `paper_draft/section4_draft_v0_1.md`, lines 220-236.

> ## 4.3 From tools to predictions
>
> The two tools yield predictions that Section 5 tests at publication scale.
> Proposition 1 and Theorem 1 predict that `GAP = H_up + M_Φ` and `M_Φ = ` SPO
> regret hold *exactly* on every cell, a structural claim, not a statistical
> one. Corollary 1 predicts `H_up` grows under partition refinement. Theorem 2
> predicts the Wasserstein-DRO corner and the Hedge corner coincide whenever
> chain dominance holds, and Corollary 2 predicts the regimes in which the
> collapse is exact versus knife-edge. Section 5 evaluates each prediction
> against a pre-registered acceptance gate.
>
> ---
>
> *Full proofs:* `paper_draft/theorems_m4.md` (Proposition 1, Theorem 1,
> Corollary 1) and `paper_draft/theorems_m5.md` (Theorem 2, Corollary 2);
> numerical verification in `prototype/results/v0_2_D1_spo_equivalence.json`
> and `v0_2_D2_wasserstein_dro.json`.

## 修改后 (AFTER)

## 4.3 From tools to predictions, and the scope of the theory

The two tools yield predictions that Section 5 tests at publication scale, and
the predictions are of different kinds. Proposition 1 and Proposition 3 are
identities: `GAP = H_up + M_Φ` and the SPO bridge hold exactly on every cell
by construction, so Section 5 reports their 72/72 outcomes as consistency
checks on the analysis pipeline, not as empirical tests that could have failed
for scientific reasons. Corollary 1 predicts `H_up` grows under partition
refinement. Proposition 2 makes the one falsifiable structural prediction:
per-wave dominance `M2 ≥ M1` fails only through batch-overtaking, so its
per-wave frequency is a measurement and its violations must all be
batch-overtaking events. Theorem 1 predicts that wherever dominance holds the
Hedge corner is the minimax corner over `{M1, M2}`; Corollary 3 predicts that
it coincides with the corner-calibrated Wasserstein-DRO optimum for the mean;
and Corollary 2 predicts the regimes in which the collapse is exact versus
knife-edge under the stochastic model `M3`. Section 5 evaluates each
prediction against a pre-registered acceptance gate.

**What the theory does and does not claim.** We close by grading the formal
results, because they are not of one kind and we prefer to state this
ourselves. Two results are exact identities: Proposition 1 (the decomposition)
and Proposition 3 (the SPO bridge) hold by unfolding definitions, and their
value is diagnostic and positional; they give the components non-negativity,
interpretable names, and a literature in which `M_Φ` is a first-class object.
Three results are elementary consequences of a dominance hypothesis: Theorem 1,
Corollary 3, and Corollary 4 each follow in a few lines once dominance is
granted, and we present them as the operational payoff of that hypothesis, not
as independent mathematical contributions. The substantive result is
Proposition 2: a sample-path coupling argument that establishes when the
throughput abstraction is optimistic relative to true co-occupancy batching,
identifies batch-overtaking as the unique failure channel, and yields a
falsifiable prediction that Section 5 verifies at publication scale. Stated
plainly, the paper's theoretical claim is Proposition 2, together with the
observation that everything an operator needs, a closed-form robust
wave-release rule with a distributionally-robust certification and a
computable mis-specification bound, follows from it by short arguments.

---

*Full proofs and derivations:* Appendix (Proposition 2 coupling argument;
Corollary 3 derivation). Numerical verification of the identities and the DRO
certification at prototype scale (Phase 4 v2 data):
`prototype/results/v0_2_D1_spo_equivalence.json` and
`v0_2_D2_wasserstein_dro.json`. Publication-scale validation of every gated
prediction: Section 5, `prototype/results/v0_5_phase5_*.json`.

## 理由 (RATIONALE)

对应 panel_theory.json nice_to_have 第 4 条（"a short 'what the theory does
and does not claim' paragraph in §4 ... stating plainly which results are
identities, which are elementary consequences, and which is the substantive
coupling theorem"）以及 required_additions 第 8 条（§4 footer 应指向
publication-scale v0_5 工件，并逐结果声明统计量范围）。§4.3 正文同步到新编号，
并把 "预测" 分级：恒等式类预测重定性为管道一致性检查（配合 Edit 9 对 §5 的
改写），Proposition 2 升为唯一可证伪的结构性预测（billing 再平衡的落点）。
页脚将 v0_2 工件明确标注为 prototype scale，另列 v0_5 为 publication scale，
消除量表混排隐患。

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

# Edit 14: Final numbering scheme and find/replace table for every affected mention

## 修改前 (BEFORE)

(no single existing text; this edit is a cross-file consistency operation. The
inconsistency it resolves: the DRO result is "Theorem 3" in
`paper_draft/methodology_v0_2.md` line 31 and in the docstrings of
`prototype/src/analysis_D1_spo_equivalence.py` / `analysis_D2_wasserstein_dro.py`,
but "Theorem 2" (as a clause) in `paper_draft/section4_draft_v0_1.md` line 169.)

## 修改后 (AFTER)

Adopt the scheme in the header of this document (Prop 1 decomposition, Prop 2
chain dominance, Prop 3 SPO bridge, Theorem 1 minimax collapse, Cor 1
refinement, Cor 2 epsilon bound, Cor 3 DRO certification, Cor 4 K-model).
Apply the following replacements. Rows marked [done above] are fully covered
by Edits 1-13; the remaining rows are one-line mechanical replacements.

| File : line (approx.) | Current text | Replace with |
|---|---|---|
| section4_draft_v0_1.md : 5 (YAML) | `D1/D2 shipped as theorems` | `D1 shipped as Proposition 3 (bridge); D2 as Theorem 1 + Corollaries 3-4` |
| section4_draft_v0_1.md : 61-83 | `Theorem 1 (D1: SPO-regret equivalence)` and §4.1.2 | [done above, Edit 2] |
| section4_draft_v0_1.md : 119-128 | minimax over `M ∈ {M1, M2, M3}` | [done above, Edit 3] |
| section4_draft_v0_1.md : 163 | `Theorem 2's distributionally-robust clause invokes` | [done above, Edit 4] |
| section4_draft_v0_1.md : 169-185 | `Theorem 2 (D2: minimax collapse and DRO equivalence)` | [done above, Edit 5] |
| section4_draft_v0_1.md : 187 | `Theorem 2 yields a **closed-form wave-release rule**` | [done above, Edit 5: `Theorem 1 yields ...`] |
| section4_draft_v0_1.md : 202 | `(Theorem 2's DRO clause)` in Figure 2 caption | [done above, Edit 5: `(Corollary 3, §4.2.4)`] |
| section4_draft_v0_1.md : 215 | `the collapse of Theorem 2 remains exact` | [done above, Edit 6: `the collapse of Theorem 1 remains exact`] |
| section4_draft_v0_1.md : 220-236 | §4.3 and footer | [done above, Edit 8] |
| section5_draft_v0_1.md : 60 | `SPO-regret equivalence | M_Φ = SPO regret of the Φ predictor` | [done above, Edit 9] |
| section5_draft_v0_1.md : 65 | `SPO-regret equivalence ... (Theorem 1)` | [done above, Edit 9] |
| section5_draft_v0_1.md : 109 | `identity and SPO-regret equivalence holding in 72/72` | [done above, Edit 10] |
| section5_draft_v0_1.md : 142 | `DRO = Hedge | c*_DRO = c*_Hedge per regime` | [done above, Edit 11: annotated `(Corollary 3, mean summary)`] |
| section5_draft_v0_1.md : 151 | `that the DRO clause invokes` | [done above, Edit 11: `that Corollary 3 invokes`] |
| section5_draft_v0_1.md : 167 | `Theorem 2's collapse under chain dominance` | [done above, Edit 12] |
| section5_draft_v0_1.md : 264 | `the SPO-regret equivalence of Theorem 1` | [done above, Edit 13] |
| Abstract/abstract_v1.0.md : 10 (YAML changes note) | `the formal term "SPO regret" stays in the Theorem 1 statement in section 4` | `the formal term "SPO regret" stays in the Proposition 3 statement in section 4` |
| Abstract/abstract_v1.0.md : 54-55 (body) | `Under a conditional dominance result that we establish, this simplest rule is provably the distributionally-robust optimum.` | `Under a conditional dominance result that we establish, this simplest rule is provably the robust choice: it is exactly minimax over the candidate models and matches a calibrated distributionally-robust optimum.` |
| Abstract/abstract_v1.0.md : 65-66 (Chinese) | `在我们所确立的一个带条件支配性结果之下，这条最简单的规则可被证明就是分布鲁棒意义下的最优解。` | `在我们所确立的一个带条件支配性结果之下，这条最简单的规则可被证明是稳健的选择：它恰是候选模型之间的极小极大解，并与一个经过校准的分布鲁棒最优解一致。` |
| Introduction/introduction_v1.0.md : 173 | `we prove (Theorem 1) that M_Φ is exactly a predict-then-optimize decision loss` | `we identify (Proposition 3) M_Φ as exactly a predict-then-optimize decision loss` |
| Introduction/introduction_v1.0.md : 179-183 | `we prove (Theorem 2) that, under a conditional per-wave dominance result we establish (Proposition 2), this simplest rule coincides exactly with the Wasserstein distributionally-robust optimum (Mohajerin Esfahani and Kuhn, 2018) and carries a computable worst-case-loss bound.` | `we prove a conditional per-wave dominance result (Proposition 2) under which this simplest rule is exactly minimax over the deterministic model pair (Theorem 1), coincides with a corner-calibrated Wasserstein distributionally-robust optimum (Corollary 3; Mohajerin Esfahani and Kuhn, 2018), and carries a computable worst-case-loss bound (Corollary 2).` |
| methodology_v0_2.md : 14 | `Theorem 1: M_xi = SPO regret ...` | `Proposition 3 (demoted): M_xi = SPO regret ...` (outline note only) |
| methodology_v0_2.md : 31 | `Theorem 3: Under chain dominance, Wasserstein DRO solution = Hedge Rule solution` | `Corollary 3: DRO certification under the corner-calibrated radius` |
| methodology_v0_2.md : 36 | `Theorem 4 (was Theorem 2): K-model Hedge Rule closed-form` | `Theorem 1 (collapse over {M1,M2}) + Corollary 4 (K-model)` |
| analysis_D1_spo_equivalence.py : docstring lines 2-4, 28, output "theorem" field | `Theorem 1` | `Proposition 3 (SPO bridge; was Theorem 1)` (provenance comment; code behavior unchanged) |
| analysis_D2_wasserstein_dro.py : docstring lines 2-4, 27, output "theorem" field | `Theorem 3` | `Corollary 3 (DRO certification; was Theorem 3)` (provenance comment; code behavior unchanged) |
| TERMINOLOGY.md : §4 M_Φ row, §7 C2 row | `(Theorem 1)`; `three results: Prop 1, Theorem 1, Theorem 2, plus Prop 2 / Cor 1 / Cor 2` | `(Proposition 3)`; `Prop 1 / Prop 3 identities, Theorem 1 collapse, Prop 2 chain dominance (main result), Cor 1 / Cor 2 / Cor 3 / Cor 4` |
| RelatedWorks/related_works_v1.0.md : 190, 199 | `Theorem 1 gives this loss a partition perspective`; `Theorem 2 and Proposition 2 show that our minimax` | `Proposition 3 gives this loss a partition perspective`; `Theorem 1, Corollary 3, and Proposition 2 show that our minimax` |
| phase5_scaleup_preregistration.md : 316 | `Theorem 1 (the SPO-regret equivalence ...)` | DO NOT EDIT (frozen pre-registration). Handle by the parenthetical mapping note added in Edit 13. |

## 理由 (RATIONALE)

对应 panel_theory.json required_additions 第 8 条："one consistent theorem
numbering (the DRO result is 'Theorem 3' in methodology_v0_2.md and both
D-scripts, 'Theorem 2' in §4)"。方案保持 Proposition 2 / Corollary 1 /
Corollary 2 编号不变（跨文档引用最多、改动风险最高），只重排被审计点名的
两个结果（SPO 恒等式降为 Prop 3，DRO 子句降为 Cor 3），并新增 Cor 4。
预注册文档冻结不可改，用 Edit 13 的括号对照注解决历史命名衔接。D-scripts
与工作文档行属于溯源注释修改，不影响任何计算行为，但为避免下一次审计再次
发现新旧编号并存，建议作者随本轮修订一并执行（本文档不直接修改这些文件）。

---

# Open issues for the author

1. **Proposition ordering.** Under the adopted scheme, Proposition 3 (§4.1.2)
   appears in the text before Proposition 2 (§4.2.1). If strict
   order-of-appearance numbering is preferred, the alternative is to swap the
   labels (SPO bridge = Prop 2, chain dominance = Prop 3), at the cost of
   updating TERMINOLOGY.md, the Introduction, the Abstract YAML note, the
   Appendix skeleton, and both Experiments/Methodology splice files, and of
   breaking the "Proposition 2 = chain dominance" convention used in every
   working document since April. I recommend accepting the mild ordering
   blemish; the author should decide.
2. **Math steps needing human verification (Corollary 3 proof).** Please
   verify: (a) the 1-D fact `W₁ ≥ |mean gap|` with equality iff first-order
   dominance (equivalently, ordered quantile functions); (b) the closed form
   `sup` over a W1 ball of a 1-Lipschitz expectation `= nominal + radius`, and
   that the makespan objective (identity function) is 1-Lipschitz so equality
   is attained; (c) the correct attribution split between Mohajerin Esfahani &
   Kuhn (2018) and Blanchet & Murthy (2019) for the general form. The
   derivation currently lives only in the analysis_D2 docstring; the Appendix
   write-up (a separate required addition) must state both facts formally.
3. **Corollary 4 proof check.** The 5-line proof assumes per-wave (almost
   sure) pairwise dominance against the maximal model; confirm this is the
   intended hypothesis (it mirrors Proposition M5.1's condition (D)) and that
   the corollary should not instead be stated under the weaker first-order
   stochastic dominance per corner (which also suffices; the a.s. version
   implies it).
4. **Numbers to re-verify against artefacts before pasting**: `U_c(0.05)` max
   3.5 % (config 7) and 0.53 % (config 1) at publication scale
   (`v0_5_phase5_blockC.json`); prototype-scale `U_c` range 51-94 units and
   the single-configuration corner flip at `σ = 0.20`
   (`v0_2_phase4_v2_m5_delta.json`); the global-radius ablation outcome
   (`v0_2_D2_wasserstein_dro.json`, field `c_star_DRO_global_radius`).
5. **Out of W1 scope, flagged for other work packages**: (a) the H_up
   non-negativity "population inequality" sentence kept verbatim in Edit 9 is
   contested by panel flaw 5 and needs the covering-partition lemma fix;
   (b) the "a measurement, not a self-consistency check" sentence kept in
   Edit 4 is contested by panel flaw 4 pending the matched-assignment
   amendment; (c) the Proposition 2 appendix induction (panel flaw 3) and the
   promised Appendix write-ups of the Proposition 3 unfolding and Corollary 3
   derivation; (d) the out-of-sample M_Φ split with the El Balghiti et al.
   citation (panel flaw 1 defense, second half).
6. **Pre-registration cross-naming.** The frozen pre-registration refers to
   the SPO result as "Theorem 1". Edit 13 adds a parenthetical mapping; the
   author may prefer a single footnote at the start of Section 5 instead
   ("results renumbered in revision: pre-registration Theorem 1 = Proposition
   3, Theorem 2/3 = Theorem 1 + Corollary 3") to avoid repeating it.
