---
title: "W2: Appendix formal mathematics: Wasserstein-DRO certification of the Hedge Rule, and the H_up non-negativity repair"
date: 2026-07-08
sources_consulted:
  - "paper_draft/theorems_m4.md (Corollary M4.2 and proof)"
  - "paper_draft/theorems_m5.md (Proposition M5.1, Corollary M5.2)"
  - "paper_draft/section4_draft_v0_1.md (4.1.1, 4.2.2)"
  - "paper_draft/section5_draft_v0_1.md (D1 gate table, lines 55-76)"
  - "prototype/src/analysis_D2_wasserstein_dro.py (docstring derivation, global-radius ablation)"
  - "prototype/results/v0_2_D2_wasserstein_dro.json (prototype-scale verification summary)"
  - "prototype/src/wave_policies.py (FILTER_Q = 0.25 quartile-corner construction, lines 44, 88-105)"
  - "scratchpad/panel_theory.json (fatal flaws 2 and 5; required_additions 1 and 6)"
  - "paper_draft/TERMINOLOGY.md, CLAUDE.md"
status: "draft for author review"
---

# W2. Appendix formal mathematics

本文档提供两组稿件级修订材料。第一组是审稿组指出"承诺了但不存在"的附录数学: Theorem 2 第二子句 (DRO 等价) 的完整附录推导, 目前该推导只存在于 `analysis_D2_wasserstein_dro.py` 的 docstring 中。第二组修复 H_up 非负性的表述链: 正确的混合分位数引理 (覆盖性划分下的总体级结论), §4.1.1 中 "by construction" 的删除与改写, 以及 theorems_m4.md 中 Corollary M4.2 错误中间步骤的替换。所有 AFTER 文本为可直接进稿的英文, 无 em-dash。

Numbering convention used below: the new DRO material is **Appendix B** (assuming the chain-dominance proof of Proposition 2 is Appendix A); the new mixture-quantile lemma is **Appendix C**. If the author's appendix lettering differs, renumber consistently (see open issues).

---

# EDIT 1. New appendix subsection: Wasserstein-DRO certification of the Hedge Rule

## 修改前 (BEFORE)

(no existing text; new section)

The manuscript currently promises this proof without providing it: `paper_draft/section4_draft_v0_1.md`, §4.2.2, lines 179-185, ends the Theorem 2 proof sketch with "(full proof in Appendix)", but `paper_draft/Appendix/` contains only the chain-dominance material. The only written derivation lives in the docstring of `prototype/src/analysis_D2_wasserstein_dro.py` (lines 9-37).

## 修改后 (AFTER)

> **Placement:** new appendix section, after the chain-dominance proof appendix. All notation as in Sections 3 and 4.

### Appendix B. Wasserstein-DRO certification of the Hedge Rule

This appendix proves the second clause of Theorem 2: with the operator's nominal model taken to be the throughput abstraction M1 and model ambiguity per corner captured by a 1-Wasserstein ball whose radius is calibrated to the corner-conditional model discrepancy, the distributionally robust corner selection coincides with the Hedge corner. The result is a certification rather than an independent theorem: once the two elementary one-dimensional facts below are in place, the equivalence follows in six lines from chain dominance. We state it for the mean summary; see Remark B.5 for the scope.

**B.1 Setup.** Fix a corner $c \in \mathcal{Q}$. Each wave $W$ in corner $c$ is evaluated under both elevator models on matched inputs, and we write $P_1^c$ and $P_2^c$ for the corner-conditional distributions of $C_{\max}(W; M1)$ and $C_{\max}(W; M2)$, $W \in c$; in the numerical verification these are the empirical distributions of the paired makespan samples. Both are probability measures on $\mathbb{R}$ with finite first moments. Write $F_k^c$ for the cumulative distribution function of $P_k^c$ and $E_k^c[T]$ for its mean.

For probability measures $P, Q$ on $\mathbb{R}$ with finite first moments, the 1-Wasserstein distance is
$$W_1(P, Q) \;=\; \inf_{\pi \in \Pi(P, Q)} \mathbb{E}_{(X, Y) \sim \pi} |X - Y|,$$
where $\Pi(P, Q)$ is the set of couplings of $P$ and $Q$. On the real line it admits the closed forms (Vallender, 1974)
$$W_1(P, Q) \;=\; \int_{\mathbb{R}} |F_P(t) - F_Q(t)|\, dt \;=\; \int_0^1 |F_P^{-1}(u) - F_Q^{-1}(u)|\, du .$$

Model uncertainty in corner $c$ is captured by the ambiguity ball centred at the nominal corner-conditional distribution,
$$\mathcal{B}_{\rho_c}(P_1^c) \;=\; \bigl\{\, Q \text{ on } \mathbb{R} \;:\; W_1(Q, P_1^c) \le \rho_c \,\bigr\}, \qquad \rho_c \;=\; W_1(P_1^c, P_2^c).$$
By construction $P_2^c \in \mathcal{B}_{\rho_c}(P_1^c)$, and $\rho_c$ is the smallest radius for which this containment holds: per corner, the ambiguity set is the minimal set that honestly contains the rival model (Remark B.6). The distributionally robust corner selection is
$$c^\star_{\mathrm{DRO}} \;=\; \operatorname*{argmin}_{c \in \mathcal{Q}} \; \sup_{Q \in \mathcal{B}_{\rho_c}(P_1^c)} \mathbb{E}_Q[T].$$

**B.2 Two one-dimensional facts.**

**Lemma B.1 (integrated CDF gap; equality with the mean gap under dominance).** *For $P, Q$ on $\mathbb{R}$ with finite first moments,*
$$W_1(P, Q) \;=\; \int |F_P - F_Q|\, dt \;\ge\; \bigl|\, \mathbb{E}_Q[T] - \mathbb{E}_P[T] \,\bigr|,$$
*with equality if and only if $F_P - F_Q$ has a single sign almost everywhere, that is, if and only if one of $P, Q$ first-order stochastically dominates the other.*

*Proof.* The integral formula is Vallender's (1974) identity. For the mean gap, $\mathbb{E}_P[T] = \int_0^\infty (1 - F_P(t))\, dt - \int_{-\infty}^0 F_P(t)\, dt$ and likewise for $Q$, so
$$\mathbb{E}_Q[T] - \mathbb{E}_P[T] \;=\; \int_{\mathbb{R}} \bigl(F_P(t) - F_Q(t)\bigr)\, dt .$$
Comparing with $W_1 = \int |F_P - F_Q|\, dt$, the triangle inequality for integrals gives the stated inequality, with equality if and only if the integrand $F_P - F_Q$ keeps one sign almost everywhere. A single sign of $F_P - F_Q$ is precisely first-order stochastic dominance of one distribution over the other (Shaked and Shanthikumar, 2007, Section 1.A). $\blacksquare$

**Lemma B.2 (worst case of the identity objective over a $W_1$ ball).** *For any $P$ on $\mathbb{R}$ with finite first moment and any $\rho \ge 0$,*
$$\sup_{Q :\, W_1(Q, P) \le \rho} \mathbb{E}_Q[T] \;=\; \mathbb{E}_P[T] + \rho,$$
*and the supremum is attained by the translate $Q^\ast = \mathrm{law}(X + \rho)$, $X \sim P$.*

*Proof.* Upper bound: for any admissible $Q$ and any coupling $\pi$ of $(P, Q)$, $\mathbb{E}_Q[T] - \mathbb{E}_P[T] = \mathbb{E}_\pi[Y - X] \le \mathbb{E}_\pi|Y - X|$; taking the infimum over couplings gives $\mathbb{E}_Q[T] - \mathbb{E}_P[T] \le W_1(P, Q) \le \rho$. This is the Kantorovich-Rubinstein bound applied to the 1-Lipschitz function $f(t) = t$ (Villani, 2009, Chapter 5). Attainment: the translate $Q^\ast$ satisfies $W_1(Q^\ast, P) = \rho$ (couple $X$ with $X + \rho$; no coupling can do better since means differ by $\rho$) and $\mathbb{E}_{Q^\ast}[T] = \mathbb{E}_P[T] + \rho$. $\blacksquare$

Lemma B.2 is the specialization, to a scalar random cost and the identity (1-Lipschitz) objective, of the general Wasserstein-DRO duality of Mohajerin Esfahani and Kuhn (2018); see also Blanchet and Murthy (2019) for the general strong-duality and attainment theory. We state and prove the scalar case directly because nothing beyond it is used.

**B.3 The certification.**

**Proposition B.3 (DRO certification of the Hedge corner; mean summary).** *Suppose that in every corner $c \in \mathcal{Q}$ the corner-conditional distributions satisfy first-order stochastic dominance,*
$$F_1^c(t) \;\ge\; F_2^c(t) \quad \text{for all } t \in \mathbb{R} \qquad (\text{M2 stochastically larger}). \tag{FOSD}$$
*Then, with the corner-calibrated radii $\rho_c = W_1(P_1^c, P_2^c)$,*
$$\operatorname*{argmin}_{c \in \mathcal{Q}} \; \max_{k \in \{1, 2\}} E_k^c[T] \;=\; \operatorname*{argmin}_{c \in \mathcal{Q}} \; \sup_{Q \in \mathcal{B}_{\rho_c}(P_1^c)} \mathbb{E}_Q[T],$$
*and both sides equal the M2-optimal corner $\operatorname{argmin}_c E_2^c[T]$: the Hedge corner is exactly the Wasserstein-DRO optimum.*

*Proof.* Fix $c \in \mathcal{Q}$. Then:

1. (FOSD) implies $E_2^c[T] \ge E_1^c[T]$, hence $\max_k E_k^c[T] = E_2^c[T]$ (the Hedge value in corner $c$).
2. $E_2^c[T] = E_1^c[T] + \bigl(E_2^c[T] - E_1^c[T]\bigr)$.
3. Under (FOSD) the equality case of Lemma B.1 gives $E_2^c[T] - E_1^c[T] = W_1(P_1^c, P_2^c)$.
4. By definition of the radius, $W_1(P_1^c, P_2^c) = \rho_c$.
5. Lemma B.2 gives $E_1^c[T] + \rho_c = \sup_{Q \in \mathcal{B}_{\rho_c}(P_1^c)} \mathbb{E}_Q[T]$ (the DRO worst case in corner $c$).
6. Chaining 1 through 5: the Hedge value and the DRO worst case coincide corner by corner, so their argmins over $c$ coincide, and by step 1 both equal $\operatorname{argmin}_c E_2^c[T]$. $\blacksquare$

**Remark B.4 (the hypothesis, and what verifies it).** The load-bearing hypothesis is distribution-level first-order stochastic dominance per corner. This is weaker than the per-wave sample-path ordering of Proposition 2: almost-sure dominance on matched waves implies (FOSD), but the converse fails, and (FOSD) can survive a small mass of per-wave violations. It is (FOSD), not the per-wave ordering, that the equality case of Lemma B.1 requires. Empirically, on the matched-wave data (prototype scale, `v0_2_D2_wasserstein_dro.json`), (FOSD) holds at every coupled quantile in 12 of 12 (regime, corner) cells, the per-corner value identity DRO worst case $=$ Hedge value holds to float tolerance in 12 of 12, and the corner selections coincide in 3 of 3 regimes.

**Remark B.5 (mean versus median scope).** Proposition B.3 is a statement about the mean summary: Lemma B.2's closed form is specific to expectations of Lipschitz objectives, and step 3 uses the mean-gap form of $W_1$. By contrast, the collapse clause of Theorem 2 and the $\varepsilon$-bound of Corollary 2 are stated for the median (indeed for any monotone summary). The two clauses therefore certify the same corner through different summary statistics, and each result's summary statistic is stated explicitly in the text.

**Remark B.6 (why the radius must be corner-calibrated).** A single global radius (for instance $\rho = \max_c \rho_c$, or any corner-independent value) destroys the equivalence: the supremum then adds the same constant to every corner's nominal mean, so the DRO argmin reduces to $\operatorname{argmin}_c E_1^c[T]$, the nominal-model corner, which differs from the Hedge corner whenever M1 and M2 rank corners differently. The per-corner radius $\rho_c = W_1(P_1^c, P_2^c)$ is therefore load-bearing, and it is not a free tuning parameter: it is the smallest radius whose corner-$c$ ball contains the rival model, that is, the minimal ambiguity set that honestly represents the model family in each corner. Any larger radius preserves the containment but weakens the certificate; any smaller radius excludes M2 and the hedge no longer covers the family. The global-radius ablation in the verification script (`analysis_D2_wasserstein_dro.py`) documents this failure mode explicitly, and we report it as evidence that the calibration is necessary rather than convenient.

**Remark B.7 (when dominance fails).** If (FOSD) fails in some corner, Lemma B.1 yields the strict inequality $W_1 > |E_2^c - E_1^c|$ and the DRO worst case strictly overshoots the Hedge value by the dominance-violation mass $\delta_c := W_1(P_1^c, P_2^c) - (E_2^c[T] - E_1^c[T]) \ge 0$. The corner selection still survives whenever $\max_c \delta_c$ is smaller than the minimal inter-corner gap in the Hedge values, a sufficient condition parallel to Corollary 2. The chain-broken control (M2 versus the stochastic extension M3 at $\sigma = 0.20$, prototype scale) illustrates both halves: the value identity breaks in 12 of 12 (regime, corner) cells, while the corner argmin survives in 2 of 3 regimes (`v0_2_D2_wasserstein_dro.json`), exactly the knife-edge behaviour the sufficient condition describes.

**References cited here.** Blanchet, J., Murthy, K., 2019. Quantifying distributional model risk via optimal transport. Mathematics of Operations Research 44 (2), 565--600. Mohajerin Esfahani, P., Kuhn, D., 2018. Data-driven distributionally robust optimization using the Wasserstein metric: performance guarantees and tractable reformulations. Mathematical Programming 171, 115--166. Shaked, M., Shanthikumar, J.G., 2007. Stochastic Orders. Springer, New York. Vallender, S.S., 1974. Calculation of the Wasserstein distance between probability distributions on the line. Theory of Probability and Its Applications 18 (4), 784--786. Villani, C., 2009. Optimal Transport: Old and New. Springer, Berlin.

## 理由 (RATIONALE)

对应 panel_theory.json 第 2 条 CRITICAL 缺陷与 required_additions 第 1 条: §4.2.2 承诺 "full proof in Appendix" 但附录不存在, DRO 推导只在代码 docstring 里。本节按审稿组建议的 Path A 把结果定位为 "certification" 而非独立定理, 把两个一维事实 (W1 的 CDF 积分表示及 FOSD 下等于均值差; W1 球上 1-Lipschitz 期望的最坏情形 = 名义值 + 半径) 正式陈述并给出自含证明, 引用 Mohajerin Esfahani & Kuhn (2018) 与 Blanchet & Murthy (2019) 说明其为一般对偶的特例。半径逐角标定的辩护 (最小诚实模糊集) 与全局半径消融 (Remark B.6) 把审稿组认定的 "reverse-engineered" 弱点转为公开陈述的必要条件; Remark B.5 修复 mean-vs-median 口径不一致; 所有经验数字标注 prototype scale。

---

# EDIT 2. Section 4.2.2: align the proof sketch with Appendix B (mean scope, radius calibration, honest pointer)

## 修改前 (BEFORE)

Source: `f:\Paper 3\paper_draft\section4_draft_v0_1.md`, §4.2.2, approx. lines 178-185:

```
*Proof sketch.* Monotonicity of `s` carries the per-wave dominance to the
conditional statistics, so `max_M s[·|c] = s[C_max(·; M2)|c]` for every
corner, and the outer `argmin` reduces accordingly. For the second clause, the
Wasserstein-1 distance between the nominal and dominant models equals their
mean gap exactly under dominance, so the worst case over the ambiguity ball is
attained at the dominant model; the two `argmin`s therefore agree (full proof
in Appendix). ∎
```

## 修改后 (AFTER)

*Proof sketch.* Monotonicity of `s` carries the per-wave dominance to the
conditional statistics, so `max_M s[·|c] = s[C_max(·; M2)|c]` for every
corner, and the outer `argmin` reduces accordingly. The second clause is a
distributionally robust certification stated for the mean summary: centre a
Wasserstein-1 ball at the nominal model `M1` in each corner and calibrate its
radius to the corner-conditional model discrepancy, `ρ_c = W₁(M1, M2 | c)`,
the smallest radius whose ball contains the rival model. Under first-order
stochastic dominance `W₁` equals the mean gap exactly, so the worst case over
the ball is attained at the dominant model and the DRO `argmin` coincides with
the Hedge `argmin`. The collapse clause holds for any monotone summary; the
DRO clause is specific to the mean (Appendix B, Proposition B.3, together with
the two supporting one-dimensional lemmas and the radius-calibration remark). ∎

## 理由 (RATIONALE)

配合 EDIT 1: 正文的 proof sketch 必须与新附录的实际口径一致。原文未说明 DRO 子句只对均值统计量成立 (panel_theory.json 缺陷 2 明确点名 mean-vs-median 不匹配), 也未说明半径是逐角标定且是包含对手模型的最小半径。修改后 "full proof in Appendix" 的承诺指向真实存在的 Appendix B, 并预先声明口径, 避免审稿人发现正文与附录不符。改动刻意最小化, 不触碰 Theorem 2 本体的重述 (那属于另一任务的范围)。

---

# EDIT 3. New appendix subsection: the mixture-quantile lemma behind H_up ≥ 0

## 修改前 (BEFORE)

(no existing text; new section)

The manuscript currently asserts the property without a correct proof anywhere in the workspace: §4.1.1 says "by construction" (see EDIT 4), and the only written argument, `theorems_m4.md` Corollary M4.2, uses a false intermediate step (see EDIT 5).

## 修改后 (AFTER)

> **Placement:** new appendix section (Appendix C), referenced from §4.1.1 and §5.

### Appendix C. Non-negativity of the structural ceiling: scope and proof

The policy component satisfies $M_\Phi \ge 0$ unconditionally, by definition of the minimizing corner. The structural ceiling $H_{\mathrm{up}} = (m_{q_{\max}} - m_0) / m_0$ compares a corner median with the pooled median, and its sign is a statement about the partition scheme. The following lemma gives the population-level guarantee and delimits its scope.

**Lemma C.1 (mixture-quantile bracketing).** *Let $\{\mathcal{W}_q\}_{q \in \mathcal{Q}}$ be a finite partition of the candidate pool $\mathcal{W}$ whose corners cover the pool, with weights $w_q = \mathbb{P}(W \in \mathcal{W}_q) > 0$ summing to one. Let $F_q$ be the corner-conditional makespan distribution functions, $F_0 = \sum_q w_q F_q$ the pooled distribution function, and let $m_q = \inf\{t : F_q(t) \ge 1/2\}$ and $m_0 = \inf\{t : F_0(t) \ge 1/2\}$ be the corresponding medians. Then*
$$\min_q m_q \;\le\; m_0 \;\le\; \max_q m_q .$$
*In particular $m_{q_{\max}} \ge m_0$, so $H_{\mathrm{up}} \ge 0$, for any covering partition.*

*Proof.* Write $m^\ast = \max_q m_q$. Each $F_q$ is right-continuous and non-decreasing, so $F_q(m_q) \ge 1/2$ and hence $F_q(m^\ast) \ge F_q(m_q) \ge 1/2$ for every $q$. Because the corners cover the pool, the pooled distribution is the mixture $F_0 = \sum_q w_q F_q$, so $F_0(m^\ast) = \sum_q w_q F_q(m^\ast) \ge 1/2$, which gives $m_0 \le m^\ast$. For the lower bracket, write $m_\ast = \min_q m_q$ and take any $t < m_\ast$. Since $t < m_q$ for every $q$, the definition of $m_q$ as an infimum forces $F_q(t) < 1/2$ for every $q$, hence $F_0(t) = \sum_q w_q F_q(t) < 1/2$, which gives $m_0 \ge m_\ast$. $\blacksquare$

**Remark C.2 (covering versus truncated corners).** Lemma C.1 is a statement about mixtures: the pooled distribution function is a weighted average of the corner distribution functions only when every wave in the pool belongs to some corner. The corner scheme implemented in the experiments is deliberately not of this type. The four corners are the intersections of top and bottom 25 percent quantile bins on the two axes of the representation, `C` (vertical spread) and `I` (directional imbalance) (`FILTER_Q = 0.25` in `wave_policies.py`): each corner is an extreme region of the `(C, I)` plane, and the union of the four corners excludes the middle of both marginals, hence covers only a fraction of the pool. This truncation is what gives the corners their contrast, and its price is that no mixture identity links $F_0$ to the corner distributions, so $H_{\mathrm{up}} \ge 0$ is not a theorem for the implemented scheme. It is instead an empirical regularity: at publication scale it holds in 70 of 72 sub-cells, and the two exceptions are near-degenerate ($H_{\mathrm{up}} = -0.0021$ and $-0.0044$, each below 0.5 percent of the cell scale and within bootstrap noise of zero). The population guarantee of Lemma C.1 applies verbatim to covering variants of the scheme, for instance the $2 \times 2$ median-split partition of the `(C, I)` plane.

## 理由 (RATIONALE)

对应 panel_theory.json 第 5 条 MAJOR 缺陷与 required_additions 第 6 条 (Option 1, clean): 给出正确的总体级引理及其完整证明 (混合 CDF 的分位数夹逼), 并明确该保证只适用于覆盖性划分; 实现中的角是截断的四分位交集 (非覆盖), 对它 H_up ≥ 0 只是经验规律 (publication scale 70/72, 两个例外在自助噪声范围内)。这同时为 §5 现有的 "does not contradict the population inequality" 一句提供了此前不存在的、被正式陈述并证明的那条总体不等式。C 轴按 TERMINOLOGY 规则称 vertical spread。

---

# EDIT 4. Section 4.1.1: remove "by construction" and state the correct scope

## 修改前 (BEFORE)

Source: `f:\Paper 3\paper_draft\section4_draft_v0_1.md`, §4.1.1, approx. lines 52-59:

```
Because `m_q_max ≥ m_0` and `m_q_Φ ≥ m_q_min` by construction, **both
components are non-negative**: `GAP ≥ 0`, and it is strictly positive whenever
the partition is non-degenerate. The two components have distinct readings.
`H_up` is the *partition-intrinsic upper-tail headroom*, the relative makespan
penalty of the worst corner, structural and present even when `Φ` selects
perfectly. `M_Φ` is the *Φ-policy miss*, the relative cost of `Φ` choosing
its corner rather than the oracle-best one, a residual that better feature
engineering can recover (Figure 1).
```

## 修改后 (AFTER)

The two components are non-negative in different senses. `M_Φ ≥ 0` holds by
definition: `q_min` minimizes the corner medians, so `m_q_Φ ≥ m_q_min` for
whichever corner `Φ` selects. `H_up ≥ 0` holds at the population level
whenever the corners cover the candidate pool: the pooled distribution
function is then a mixture of the corner distribution functions, and a
mixture-quantile argument brackets the pooled median between the extreme
corner medians, `min_q m_q ≤ m_0 ≤ max_q m_q` (Lemma C.1, Appendix C). The
corners implemented in Section 5 are truncated quartile bins, the top and
bottom 25 percent intersections on `C` and `I`, which do not cover the pool;
for that scheme `H_up ≥ 0` is an empirical regularity rather than a
guarantee, and Section 5 reports it as such (70 of 72 sub-cells at
publication scale, with two near-degenerate exceptions within bootstrap noise
of zero). With the same qualification, `GAP ≥ 0`, strictly so whenever the
partition is non-degenerate. The two components have distinct readings.
`H_up` is the *partition-intrinsic upper-tail headroom*, the relative makespan
penalty of the worst corner, structural and present even when `Φ` selects
perfectly. `M_Φ` is the *Φ-policy miss*, the relative cost of `Φ` choosing
its corner rather than the oracle-best one, a residual that better feature
engineering can recover (Figure 1).

## 理由 (RATIONALE)

对应 panel_theory.json 第 5 条缺陷: 原文 "by construction" 对 H_up 是错误断言, 且与论文自己的 Table 2 (70/72, 两个负值) 同页矛盾。修改后区分两种非负性来源: M_Φ 确为定义所致; H_up 的保证是总体级且仅限覆盖性划分 (指向新 Lemma C.1), 实现中的截断四分位角只有经验规律并预告 §5 的 70/72。这消除了正文与结果表的自相矛盾, 并把 "GAP 严格为正" 的断言限定在同一口径下。段落其余部分逐字保留。

---

# EDIT 5. theorems_m4.md: replace Corollary M4.2's false intermediate step

## 修改前 (BEFORE)

Source: `f:\Paper 3\paper_draft\theorems_m4.md`, §3, approx. lines 41-48:

```
**Corollary M4.2.** *Each component of the GAP decomposition is individually non-negative, yielding two free lower bounds:*

- (M4.2a) $\; \mathrm{GAP} \;\ge\; H_{\mathrm{up}} \;\ge\; 0$, *with equality iff* $m_{q_\Phi} = m_{q_{\min}}$ *(Φ picks the oracle-best corner)*.
- (M4.2b) $\; \mathrm{GAP} \;\ge\; M_\Phi \;\ge\; 0$, *with equality iff* $m_{q_{\max}} = m_0$ *(no corner is worse than random)*.

**Proof.** $H_{\mathrm{up}} \ge 0$ follows from $m_{q_{\max}} = \max_q m_q \ge \operatorname{median}_q(m_q) \ge m_0$ (the random pool's median is bounded above by the worst-corner median since the max dominates any centrepiece). $M_\Phi \ge 0$ from $m_{q_\Phi} \ge m_{q_{\min}} = \min_q m_q$. The equality conditions follow directly from the definitions. $\blacksquare$

**Consequence for empirical practice**: *$\mathrm{GAP} > 0$ whenever the partition is non-degenerate (at least one corner worse than random) or Φ misses the oracle-best corner.* This explains the R1 finding that the GAP bootstrap CI excludes 0 in 6/6 cells: both components are strictly positive in every cell.
```

## 修改后 (AFTER)

**Corollary M4.2 (non-negativity; covering partitions).** *Suppose the corners of $\mathcal{Q}$ cover the candidate pool, and let $m_0$ be the pooled median. Then each component of the GAP decomposition is non-negative, yielding two free lower bounds:*

- (M4.2a) $\; \mathrm{GAP} \;\ge\; H_{\mathrm{up}} \;\ge\; 0$, *with* $\mathrm{GAP} = H_{\mathrm{up}}$ *iff* $m_{q_\Phi} = m_{q_{\min}}$ *(Φ picks the oracle-best corner)*.
- (M4.2b) $\; \mathrm{GAP} \;\ge\; M_\Phi \;\ge\; 0$, *with* $\mathrm{GAP} = M_\Phi$ *iff* $m_{q_{\max}} = m_0$ *(no corner is worse than random)*.

**Proof.** $M_\Phi \ge 0$ is definitional: $m_{q_\Phi} \ge \min_q m_q = m_{q_{\min}}$. For $H_{\mathrm{up}} \ge 0$, write $w_q > 0$ for the corner weights; because the corners cover the pool, the pooled distribution function is the mixture $F_0 = \sum_q w_q F_q$. With $m^\ast := \max_q m_q$, right-continuity and monotonicity of each $F_q$ give $F_q(m^\ast) \ge F_q(m_q) \ge 1/2$ for every $q$, hence $F_0(m^\ast) \ge 1/2$ and therefore $m_0 \le m^\ast = m_{q_{\max}}$. (Symmetrically, $F_q(t) < 1/2$ for every $q$ and every $t < \min_q m_q$, so $m_0 \ge m_{q_{\min}}$: the pooled median is bracketed by the extreme corner medians.) The equality conditions follow from Proposition M4.1. $\blacksquare$

**Correction note (2026-07-08).** The v0.1 proof used the intermediate step $\max_q m_q \ge \operatorname{median}_q(m_q) \ge m_0$, which is false in general: the unweighted median of the corner medians does not bound the pooled median (corner weights are unequal), and for non-covering corner schemes no mixture identity relates $F_0$ to the $F_q$ at all. The bracketing proof above replaces it and makes the covering hypothesis explicit.

**Scope remark (truncated corners as implemented).** The corners implemented in Phase 4 v2 and Phase 5 are NOT covering: they are the top/bottom-25% quartile-intersection bins on $(C, I)$ (`FILTER_Q = 0.25` in `wave_policies.py`), which exclude the middle of both marginals. For this truncated scheme Corollary M4.2a does not apply and $H_{\mathrm{up}} \ge 0$ is an empirical regularity, not a corollary: it holds in 18/18 sub-cells at prototype scale and in 70/72 sub-cells at publication scale, the two publication-scale exceptions being near-degenerate ($H_{\mathrm{up}} = -0.0021$ and $-0.0044$, each below 0.5% of the cell scale and within bootstrap noise of zero). The population guarantee applies verbatim to covering variants such as the $2 \times 2$ median-split partition.

**Consequence for empirical practice**: *for covering partitions, $\mathrm{GAP} > 0$ whenever the partition is non-degenerate (at least one corner worse than random) or Φ misses the oracle-best corner; for the implemented truncated corners the same reading holds up to the finite-sample caveat above.* This is consistent with the R1 finding (prototype scale) that the GAP bootstrap CI excludes 0 in 6/6 cells, and with the publication-scale gate table (exact decomposition 72/72; non-negativity 70/72).

## 理由 (RATIONALE)

对应 panel_theory.json 第 5 条缺陷中被逐字点名的错误步骤 (theorems_m4.md 第 46 行 "max_q m_q >= median_q(m_q) >= m_0"): 第二个不等号在一般情形不成立, 且实现中的角是非覆盖的截断桶, 混合论证根本不适用。替换为带覆盖性假设的正确夹逼证明, 加入 Correction note 说明错误所在 (内部定理文档, 保留修正痕迹有助于诚实追溯), 并用 Scope remark 把实现方案的 70/72 经验规律与总体保证分开, 数字均标注 scale。Consequence 段同步改写, 避免再从错误引理推出 "both components strictly positive in every cell" 这种被数据反驳的话。

---

# EDIT 6. Section 5: point the "population inequality" sentence at the lemma that now exists

## 修改前 (BEFORE)

Source: `f:\Paper 3\paper_draft\section5_draft_v0_1.md`, approx. lines 72-76:

```
Non-negativity holds in 70/72; the
two exceptions are near-degenerate sub-cells (`H_up = −0.0021` and `−0.0044`,
each below 0.5 % of the cell scale) where the random-pool sample median
marginally exceeds the worst-corner sample median, a finite-sample artefact that
does not contradict the population inequality.
```

## 修改后 (AFTER)

Non-negativity holds in 70/72; the two exceptions are near-degenerate
sub-cells (`H_up = −0.0021` and `−0.0044`, each below 0.5 % of the cell scale)
where the random-pool sample median marginally exceeds the worst-corner sample
median. This is the behaviour anticipated in Section 4.1.1 for the truncated
quartile corners: the population guarantee `min_q m_q ≤ m_0 ≤ max_q m_q`
(Lemma C.1, Appendix C) applies to covering partitions, whereas the
implemented corners are top and bottom quartile intersections for which
`H_up ≥ 0` is an empirical regularity; both deviations are within bootstrap
noise of zero.

## 理由 (RATIONALE)

对应 panel_theory.json 第 5 条缺陷的收尾: 原句 "does not contradict the population inequality" 援引一条当时任何文档都未陈述或证明的不等式。EDIT 3 落地 Lemma C.1 之后, 此句改为准确表述: 总体保证存在但只适用于覆盖性划分, 实现方案是截断角, 70/72 是经验规律的正常表现而非需要辩解的反常。与 EDIT 4 的 §4.1.1 新表述互相呼应, 三处 (正文 §4、附录 C、结果 §5) 口径一致。

---

## 汇总: 与审稿意见的对应关系

| Edit | audit finding (panel_theory.json) | 性质 |
|---|---|---|
| 1 | fatal flaw 2 (CRITICAL), required_additions 1 | 新附录 B: DRO certification 完整数学 |
| 2 | fatal flaw 2 (mean-vs-median; "full proof in Appendix" 落空) | §4.2.2 sketch 对齐 |
| 3 | fatal flaw 5 (MAJOR), required_additions 6 | 新附录 C: 混合分位数引理 |
| 4 | fatal flaw 5 ("by construction" 断言) | §4.1.1 改写 |
| 5 | fatal flaw 5 (false step, theorems_m4.md:46) | Corollary M4.2 修正 |
| 6 | fatal flaw 5 ("population inequality" 无出处) | §5 句子对齐 |
