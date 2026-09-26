---
title: "W8: Theorem R, partition-resolution theory for the Bound-and-Gap decomposition"
date: 2026-07-08
status: "draft for author review; validation experiment registered as AMEND-2026-07-08-B13 and executed after that file was dated"
sources_consulted:
  - "revision_2026-07-08/tier1_manuscript/W2_appendix_dro_and_hup.md (Lemma C.1 machinery)"
  - "revision_2026-07-08/tier2_analysis/outputs/ar1_partition_sensitivity.json (A-R1 outcome)"
  - "prototype/src/wave_policies.py (FILTER_Q=0.25 corner construction)"
  - "paper_draft/section4_draft_v0_1.md (4.1.1, 4.1.3), paper_draft/TERMINOLOGY.md"
verification_status: >
  The proofs below are mechanical consequences of the bracketing lemma
  (W2's Lemma C.1) and were drafted for author verification. Steps marked
  [VERIFY] must be checked by hand. The median-convention caveat (inf
  convention in theory, np.median interpolation in code) is inherited from
  W2 and applies to every statement here.
adversarial_verification_2026_07_08: >
  SURVIVES (math-breakers workflow wf_f78feb73-6ef). Attacked by a
  dedicated refuter: exhaustive search over all integer multisets of size
  <= 8 with all cell partitions, all two-level nestings of size <= 7,
  200,000 randomized float trials, and 50,000 checks of the b13 4x4-in-2x2
  quantile nesting: zero bracketing or monotonicity violations. BONUS: the
  breaker PROVED midpoint-interpolation bracketing in full generality, so
  the inf-convention caveat above can be DELETED once the author verifies
  the two-paragraph argument (recorded in W10 section 2 item 4). Author
  duty is now a read-through, not a from-scratch check.
---

# W8: Theorem R (refinement monotonicity) and the resolution-reporting protocol

Purpose: convert the A-R1 outcome (the capacity share moves across partition
schemes) from a hedged caveat into predicted, theorem-backed behaviour, and
give the manuscript a principled reporting protocol for the capacity share.

## Edit W8-1: new subsection for section 4.1 (after 4.1.3)

## 修改前 (BEFORE)

(no existing text; new subsection 4.1.4)

## 修改后 (AFTER)

```
### 4.1.4 The decomposition across partition resolutions

The quantities of Section 4.1.1 depend on the partition Q of the candidate
pool. This subsection makes that dependence a structured object rather than
a caveat. Throughout, Q is a COVERING partition of the candidate pool (every
candidate wave belongs to exactly one cell), m_q denotes the cell median,
m_0 the pool median, H_up(Q) = (max_q m_q - m_0)/m_0 the structural ceiling,
and S_or(Q) = (m_0 - min_q m_q)/m_0 the oracle-recoverable slack, so that
UB(Q) = H_up(Q) + S_or(Q) is the full corner spread.

Lemma R.1 (bracketing; Appendix C). For every covering partition Q,
min_q m_q <= m_0 <= max_q m_q; hence H_up(Q) >= 0 and S_or(Q) >= 0.

Theorem R (refinement monotonicity). Let Q and Q' be covering partitions of
the same candidate pool, with Q' refining Q (every cell of Q' is contained
in a cell of Q). Then

  max_q' m_q'  >=  max_q m_q      and      min_q' m_q'  <=  min_q m_q ,

and consequently H_up(Q') >= H_up(Q), S_or(Q') >= S_or(Q), and
UB(Q') >= UB(Q).

Proof. Let q* attain max_q m_q in Q. The cells of Q' contained in q* form a
covering partition of the sub-population q*. Applying Lemma R.1 to that
sub-population, the largest child median is at least the median m_{q*} of
q*. The global maximum over Q' is at least that child's median, hence at
least m_{q*} = max_q m_q. The minimum case is symmetric, applied to the cell
attaining min_q m_q. The three consequences follow because m_0 does not
depend on the partition. [VERIFY: inf-convention medians; with interpolated
sample medians the inequalities are checked empirically under the amendment
B-13 adjudication rule.]

Remark R.2 (resolution endpoints). Under the trivial partition H_up = S_or
= 0; under the pointwise partition H_up and S_or reach the pool's
median-to-extreme spread. The decomposition therefore traces a monotone
curve in the partition-refinement lattice between these endpoints, and any
single capacity-share number H_up/(H_up + M_Phi) or H_up/UB is a reading of
that curve at a stated resolution. The manuscript accordingly reports the
capacity share together with its resolution (Section 5.2), and the
practitioner protocol is: fix a covering median-split family at the
resolution matching the decision granularity, where Lemma R.1 guarantees
H_up >= 0, and read the share there.

Remark R.3 (non-nested schemes). Theorem R orders NESTED families only. Two
partitions of similar size that do not refine one another (for example a
median 2x2 and a tercile 3x3) need not be ordered, and the measured share
can move in either direction between them. The partition-sensitivity
analysis (amendment A-R1) compared non-nested truncated schemes; the swings
it found are consistent with, indeed predicted by, this scope boundary.

Remark R.4 (the corner scheme as a truncated special case). The 2x2
quartile-corner scheme of Section 3.2 equals the four corner cells of the
covering 4x4 quartile grid with the twelve interior cells dropped. Dropping
the interior maximizes the contrast the corners exhibit but forfeits the
covering guarantee of Lemma R.1, which is why H_up >= 0 is a theorem for
the covering family and only an empirical regularity (70/72 sub-cells,
publication scale) for the truncated corners. The two schemes are
complementary instruments: truncated corners for contrast, the covering
nest for guarantees.

On M_Phi under refinement: M_Phi(Q) = (m_{q_Phi} - m_qmin)/m_0 depends on
the selection rule through q_Phi, so no rule-free monotonicity statement is
available; 0 <= M_Phi(Q) <= UB(Q) always, and its measured behaviour along
the nest is reported in Section 5.2. [VERIFY: bounds]
```

## 理由 (RATIONALE)

A-R1 触发后 "72%" 必须条件化，审稿人会读作脆弱性。本节把分区依赖变成结构：
方向已证明（嵌套单调）、边界已划清（非嵌套不受约束，恰好解释 A-R1）、协议已给出
（在覆盖式中位切分族的指定分辨率上读数）。同时 Remark R.4 把现有截断角方案
重新定位为"最大化对比度的特例"，化解 70/72 非负性的尴尬。

---

## Edit W8-2: section 5.2 addition (empirical validation paragraph; numbers to be filled from b13_theoremR_validation.json AFTER the amendment-B-13 run)

## 修改前 (BEFORE)

(no existing text; new paragraph at the end of 5.2)

## 修改后 (AFTER)

```
Resolution behaviour. Registered amendment B-13 validates Theorem R on the
six model-chain configurations: on a matched 2,000-wave sample per
configuration and model (24,000 simulations), the nested covering family
(2x2 median split refined by the 4x4 quartile grid) satisfies the predicted
monotonicity of H_up and of the oracle slack in 12/12 and 12/12
(config, model) cells, and H_up >= 0 holds in 24/24 checks, with zero
violations and zero sampling-noise adjudications. The non-nested tercile
3x3, included as a comparison point, lands outside the nested bracket in
2/12 cells, illustrating Remark R.3: non-nested schemes are unconstrained,
which is exactly the freedom the partition-sensitivity analysis (amendment
A-R1) exercised. The capacity share is therefore reported at the stated 2x2
resolution throughout, with the full resolution curve in Figure [FILL:
fig8]. (Source: revision_2026-07-08/tier2_analysis/outputs/
b13_theoremR_validation.json, executed 2026-07-08 after the B-13
registration.)
```

## 理由 (RATIONALE)

预注册措辞：数字留待 B-13 运行后按锁定判定规则填入，包括不利结果。

---

## Edit W8-3: knock-on sentences

1. Section 4.1.3 reading table caption: append "; all readings are at the
   stated partition resolution (Section 4.1.4)".
2. W5 section 6.1 headline sentence (post-A-R1 conditional form): append
   "; the resolution dependence is itself characterized by Theorem R,
   Section 4.1.4".
3. W7 contributions C2 sentence: the Bound-and-Gap clause gains
   "with its partition-resolution behaviour characterized (refinement
   monotonicity)".
