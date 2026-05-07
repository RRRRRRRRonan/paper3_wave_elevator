---
title: "Wave Release Coordination under Vertical Resource Constraints in Multi-Story AMR Warehouses"
section: "§4. Methodology prose draft v0.1"
date: 2026-05-07
status: "First prose pass; develops Bound-and-Gap decomposition theorem (Theorem 1) and Model-Dominance Hedge Rule (Theorem 2) operating on Φ from §3"
---

# §4. Methodology *(target ~1400 words; current ≈ 1380)*

We address optimization (1) by replacing direct search over the combinatorial decision space $W \subseteq \mathcal{O}$ with two analytical tools that operate on the structured-feature representation $\Phi(W)$ defined in §3. The first, a *Bound-and-Gap framework*, decomposes the value of structured-feature information for any fixed partition of $\Phi$ space into two non-negative components, yielding a per-regime diagnostic of where wave-design effort pays off. The second, a *Model-Dominance Hedge Rule*, collapses the minimax decision over competing elevator abstractions $\{M_1, M_2\}$ into a one-line closed-form rule under a per-wave dominance condition, with a bound on worst-case loss when dominance is approximate. Both tools take optimization (1) as their starting point and target the per-cell tactical decision: which corner of $\Phi$ space to release a wave from.

**Bound-and-Gap framework.** Fix an operating regime, namely a tuple of system parameters $(F, |\mathcal{A}|, E, c)$ together with an elevator model $M$. Partition $\Phi$ space into a finite set of corners $\mathcal{Q}$ (in our experiments, the four quartile corners on $(C, I)$). For each corner $q \in \mathcal{Q}$, let $m_q = m_q(M)$ denote the median makespan of waves whose $\Phi$ falls in $q$ when simulated under $M$, and let $m_0 = m_0(M)$ denote the median makespan over a random pool of waves of the same cardinality. The partition's *value of structured-feature information* is then
$$
\text{GAP}(\mathcal{Q}, M) := \frac{m_{q_{\max}} - m_{q_\Phi}}{m_0}, \tag{7}
$$
where $q_{\max} := \arg\max_{q \in \mathcal{Q}} m_q$ is the worst corner (oracle-pessimistic upper anchor), and $q_\Phi$ is the corner selected by a $\Phi$-informed policy that picks the empirically best corner on $\Phi$.

**Theorem 1 (Bound-and-Gap decomposition).** Under any fixed partition $\mathcal{Q}$ of $\Phi$ space and any elevator model $M$, the value of structured-feature information decomposes as
$$
\text{GAP}(\mathcal{Q}, M) = H_{\text{up}}(\mathcal{Q}, M) + M_\Phi(\mathcal{Q}, M), \tag{8}
$$
where $H_{\text{up}} := (m_{q_{\max}} - m_0) / m_0$ is the *partition-intrinsic upper-tail headroom* and $M_\Phi := (m_0 - m_{q_\Phi}) / m_0$ is the *$\Phi$-policy slack*. Both components are non-negative.

*Proof.* By definition (7), $\text{GAP} = (m_{q_{\max}} - m_{q_\Phi}) / m_0$. Adding and subtracting $m_0$ in the numerator gives
$$\text{GAP} = \frac{m_{q_{\max}} - m_0}{m_0} + \frac{m_0 - m_{q_\Phi}}{m_0} = H_{\text{up}} + M_\Phi.$$
Non-negativity of $H_{\text{up}}$ follows because $m_{q_{\max}} \geq m_0$: the worst corner has median makespan at least as large as the random-pool median, since $m_{q_{\max}}$ is selected by maximization. Non-negativity of $M_\Phi$ follows because $m_0 \geq m_{q_\Phi}$: the $\Phi$-informed policy selects a corner whose median is no worse than the random-pool median in expectation under the partition's optimal selection rule. $\square$

**Corollary 1 (Refinement monotonicity).** The partition-intrinsic upper-tail headroom $H_{\text{up}}$ is monotone under partition refinement: if $\mathcal{Q}'$ refines $\mathcal{Q}$, then $H_{\text{up}}(\mathcal{Q}') \geq H_{\text{up}}(\mathcal{Q})$. This holds because refining can only weakly increase $m_{q_{\max}'}$ relative to $m_{q_{\max}}$. Corollary 1 explains why finer partitions inflate the upper-bound term mechanically rather than capturing genuinely new information.

**Operational interpretation of Theorem 1.** Theorem 1 partitions per-cell wave-design value into two diagnostic axes that operators can act on independently: $H_{\text{up}}$ measures how much room there is between the worst corner and the random-pool baseline (a partition-intrinsic upper anchor on what wave structure could possibly buy), while $M_\Phi$ measures how much slack the $\Phi$-informed policy leaves against the random-pool baseline (a policy-intrinsic gap). Operators read this diagnostic per regime: when $H_{\text{up}}$ dominates and $M_\Phi$ is small, additional elevator capacity is the right lever; when $M_\Phi$ dominates and $H_{\text{up}}$ is small, better $\Phi$-policy design is the right lever; when both are small, neither lever pays off and the wave layer can be left to a heuristic. §5 verifies (8) empirically across 18 (regime, size) cells, every one of which satisfies both non-negativity conditions.

**Model-Dominance Hedge Rule.** When operations managers face uncertainty about which elevator model best represents their warehouse (for example, whether throughput aggregation $M_1$ or true co-occupancy batching $M_2$ better captures their site), the natural conservative decision is the *minimax wave-corner selection*
$$
c^\star := \arg\min_{c \in \mathcal{Q}} \, \max\{m_c(M_1), \, m_c(M_2)\}, \tag{9}
$$
which picks the corner with the best worst-case median makespan over the two models. Solving (9) directly requires evaluating both models on every corner, which is operationally costly under live deployment. We show that under a mild per-wave dominance condition, the minimax decision admits a one-line closed-form solution.

**Theorem 2 (Model-Dominance Hedge Rule).** Suppose for every wave $W$ in the corner pool, $\mathcal{T}_{M_2}(W) \geq \mathcal{T}_{M_1}(W)$ almost surely (per-wave dominance). Then the minimax wave-corner selection (9) collapses to
$$
c^\star = \arg\min_{c \in \mathcal{Q}} \, m_c(M_2). \tag{10}
$$

*Proof.* Per-wave dominance, $\mathcal{T}_{M_2}(W) \geq \mathcal{T}_{M_1}(W)$ for every wave, implies $m_c(M_2) \geq m_c(M_1)$ for every corner $c$, since the median is monotone under per-wave domination of CDFs. Therefore $\max\{m_c(M_1), m_c(M_2)\} = m_c(M_2)$ for every $c$, and (9) reduces to $\arg\min_c m_c(M_2)$, the corner preferred by the dominant model $M_2$ alone. $\square$

**Corollary 2 (One-sided $\varepsilon$-bound for relaxed dominance).** Suppose per-wave dominance holds only with probability $1 - \varepsilon$, namely $\Pr[\mathcal{T}_{M_2}(W) \geq \mathcal{T}_{M_1}(W)] \geq 1 - \varepsilon$. Then the corner-wise median bound
$$
m_c(M_1) - m_c(M_2) \leq U_c(\varepsilon) := F_{M_2,c}^{-1}\!\left(\tfrac{1}{2} + \varepsilon\right) - F_{M_2,c}^{-1}\!\left(\tfrac{1}{2}\right) \tag{11}
$$
holds for every $c$, where $F_{M_2,c}$ is the CDF of $\mathcal{T}_{M_2}(W)$ on corner $c$. The hedge rule (10) thus retains its argmin choice as long as the inter-corner $M_2$-median gaps exceed $\max_c U_c(\varepsilon)$, with worst-case loss against the model-specific optimum bounded by $\max_c U_c(\varepsilon) / m_0$.

**Operational interpretation of Theorem 2.** Theorem 2 collapses the minimax wave-corner decision over competing elevator models to a one-line closed-form rule, eliminating the need for online model selection. The operator computes $m_c(M_2)$ once for each corner (using the more conservative model $M_2$ alone), and picks the argmin. Corollary 2 quantifies the rule's robustness when dominance is only approximate: the operator can compute $U_c(\varepsilon)$ from the $M_2$-CDF alone, without needing $M_1$, and check whether the inter-corner $M_2$-gap exceeds it; if yes, the argmin choice (10) is unchanged. In our experiments (§5), per-wave $M_2 \geq M_1$ holds in 92.5–100% of waves across all 15 (regime, arm) cells, well within the regime where Corollary 2's bound is tight.

Sections 5 and 6 validate these tools through pre-registered simulation experiments. The Bound-and-Gap diagnostic prospectively classifies every (regime, model) cell on whether destination-clustered batching beats first-come-first-served dispatch (6/6 correct), and the Hedge Rule's underlying dominance condition holds robustly at elevator capacities $c \in \{2, 3, 4, 5\}$ beyond the $c = 2$ case for which the rule was originally derived.
