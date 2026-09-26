---
title: "Section 4 适用的全局修改（W1 Edits 1-8 + W6 Edits 5/5b/5c + 补充行）"
date: 2026-07-19
source: "逐字抽取自 00_global 的 W1/W6/W10（2026-07-08 签署交付物的副本）"
note: "如与源文件或其他 W 文件冲突，以 00_global/W10_final_integration.md 为准。W1 Edit 14 的全文查找替换总表仍在 00_global（需在整份 docx 上执行）。"
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

---

# Edit 5. Qualify the non-negativity claim in Section 4.1.1 ("by construction" contradicts Table 2's 70/72)

## 修改前 (BEFORE)

`paper_draft/section4_draft_v0_1.md`, lines 52-54:

> Because `m_q_max ≥ m_0` and `m_q_Φ ≥ m_q_min` by construction, **both
> components are non-negative**: `GAP ≥ 0`, and it is strictly positive whenever
> the partition is non-degenerate.

## 修改后 (AFTER)

> The two components carry different guarantees. `M_Φ ≥ 0` holds by
> construction, because `q_min` is the argmin over corners. `H_up ≥ 0` is a
> population-level property that holds for covering partitions, whose corners
> jointly exhaust the sampling pool so that the pool median cannot exceed the
> worst-corner median (Lemma A.x in the Appendix); the implemented corners are
> truncated quartile bins that retain only the extreme quartiles of `(C, I)`
> and do not cover the pool, so for them `H_up ≥ 0` is an empirical regularity
> rather than a theorem, observed in 70 of 72 sub-cells at publication scale
> with two near-degenerate exceptions (Section 5.2). `GAP ≥ 0` inherits the
> same qualification.

## 理由 (RATIONALE)

panel_novelty 致命缺陷 7：4.1.1 节断言两分量 "by construction" 非负，而 Table 2 报告 70/72、两个 H_up 为负，稿件自相矛盾，审稿人对表即可发现。数学事实是：M_Φ ≥ 0 确实按构造成立（q_min 是逐角最小者）；H_up ≥ 0 只在覆盖型划分下是总体性质，而实现中的四个角是截断的四分位桶（非覆盖），样本层面无保证。完整引理与证明是 W2 的交付物，此处只把 4.1 节这句话改诚实，"Lemma A.x" 为占位引用。

---

---

# Edit 5b. Companion fix: Section 4 opening paragraph

## 修改前 (BEFORE)

`paper_draft/section4_draft_v0_1.md`, lines 17-19:

> The first, a **Bound-and-Gap framework**,
> decomposes the value of wave-structure information into two non-negative
> components and rests on a decomposition theorem (§4.1).

## 修改后 (AFTER)

> The first, a **Bound-and-Gap framework**, decomposes the value of
> wave-structure information into two components, non-negative under the
> covering-partition qualification made precise in §4.1.1, and rests on a
> decomposition theorem (§4.1).

## 理由 (RATIONALE)

4.1.1 的限定改了之后，第 4 节导语中未加限定的 "two non-negative components" 会与之不一致，形成新的自相矛盾。一处限定、处处跟随。

---

---

# Edit 5c. Companion fix: Section 4.1.3 opening sentence

## 修改前 (BEFORE)

`paper_draft/section4_draft_v0_1.md`, lines 87-88:

> Because `H_up` and `M_Φ` are non-negative and independently interpretable,
> their pair is a structural reading of where a cell's wave-design value sits.

## 修改后 (AFTER)

> Because `H_up` and `M_Φ` are non-negative (`M_Φ` by construction, `H_up` in
> the qualified sense of §4.1.1) and independently interpretable, their pair is
> a structural reading of where a cell's wave-design value sits.

## 理由 (RATIONALE)

同 Edit 5b：4.1.3 再次无条件断言非负，需与 4.1.1 的限定保持一致。括号内区分两分量的保证强度，与 Table 2 的 70/72 完全相容。

---

---

# 本章适用的 W1 Edit 14 补充行与遗留事项

| 位置 | 现文 | 替换为 |
|---|---|---|
| section4_draft_v0_1.md : 5 (YAML) | `D1/D2 shipped as theorems` | `D1 shipped as Proposition 3 (bridge); D2 as Theorem 1 + Corollaries 3-4` |
| proposition2_chain_dominance_v1.0.md : 5, 10, 22, 120 | 旧编号残留（W1 Edit 14 三处遗漏之一，EXECUTION-LOG 记录） | 按最终方案套用（Prop 2 标签不变，涉及旧 "Theorem 1/2" 的引用改为 Prop 3 / Theorem 1 / Cor 3） |

# W1 Open Issues 中属于本章的作者事项

1. Open issue 1：Proposition 3（§4.1.2）先于 Proposition 2（§4.2.1）出现的编号顺序瑕疵——W1 建议接受，作者最终定夺。
2. Open issue 2：Corollary 3 证明的两个一维事实（W1 ≥ |均值差|、1-Lipschitz 目标的 sup = nominal + radius）与 Mohajerin Esfahani & Kuhn / Blanchet & Murthy 的归属划分，作者需通读核验一次。
3. Open issue 3：Corollary 4 的假设（逐波次 a.s. 成对支配 vs 更弱的逐角一阶随机支配均可）——确认采用哪个陈述。
