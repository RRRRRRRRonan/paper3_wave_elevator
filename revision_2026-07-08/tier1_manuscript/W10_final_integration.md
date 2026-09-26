---
title: "W10: final integration, adversarial-verification outcomes, and the manuscript knock-on list"
date: 2026-07-08
status: "integration reference for applying W1-W9 to paper_draft; supersedes conflicting knock-on notes in earlier W files"
sources: "math-breakers workflow wf_f78feb73-6ef (3x SURVIVES); EXECUTION-LOG.md (all idea and B-item results); amendments A/B/B11/B13/F/C (all signed 2026-07-08)"
---

# W10: final integration

## 1. Adversarial verification outcome (the author's math checklist, discharged)

Three independent breaker agents attacked the theory with instruction to
refute, plus mechanical counterexample search (their ~1.5M instances and
200k per-step boarding checks, on top of the B-11 census's 1.35M):

| target | verdict | mathematical findings |
|---|---|---|
| Lemma 6 + case-B corollary | SURVIVES | none; bound attained with equality, never exceeded |
| Theorem R + Lemma R.1 | SURVIVES | none; midpoint-median bracketing PROVED in full generality |
| W3-E2 induction (Lemmas 3-5, cases F/B, condition (d)) | SURVIVES | none; Lemma 4's premise v >= x_(1) confirmed load-bearing and correctly discharged |

The author's remaining verification duty is a READ-THROUGH, no longer a
from-scratch check: W9 section 5.2 (Lemma 6), W8 (Theorem R), and the four
presentational fixes below.

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

## 3. Theory package: final shipping form

- Proposition 2 ships as the ALL-E theorem: (a), (b), (c), (d) imply
  per-request dominance hence chain dominance, proof = W3-E2 induction
  with case B closed by Lemma 6 (W9 section 5.2); (c*) deleted from the
  statement (survives as an optional proof-internal device).
- Necessity: Examples X.1 (26 vs 24) and X.2 (103 vs 68), both
  simulator-verified; the failure taxonomy is exactly two channels.
- Evidence stack to cite in section 4/5: B-11 census (1,150,800 instances,
  zero support-set violations, E=1 self-test clean), E=3 slice (200,000,
  zero in 34,067), B-1 operational measurement (free-(b) 57.8%, enforced
  dominance 99.67%, violations 18 overtaking + 2 repositioning + 0 other),
  adversarial per-step verification (zero invariant violations).
- Theorem R with the B-13 validation (48/48) and fig8; capacity share
  reported per resolution and metric, with amendment F's measurement error
  (SEM 0.136, verdict unanimity 15/18, wave budget fig9).

## 4. Manuscript knock-ons from today's B-items

- **Section 5.3 rewrite** (chain dominance empirics): free-assignment
  99.2% (practice) NEXT TO enforced-hypotheses 99.67% (theorem-aligned);
  channel table 18/2/0; base rates 12.67% / 99.43% with the reading
  "conditions are far from necessary; violations are rare even where they
  fail"; retire the exclusivity sentence (already locked).
- **Reproducibility statement + code release note** (section 5.1 +
  appendix): the id(e) tie-break defect, measured exposure (0.27% of
  stored Block C M2 values; 5.11% of requests face consequential ties),
  the index-stable fix, and B-14's gate-equivalence result (all four D2
  verdicts unchanged; avg 0.9925 vs 0.9921). Release the fixed simulator.
- **Table 4 extension**: P8 row (grand mean 288.4; beats P0-P4 12/12,
  P5 10/12, P6 11/12; loses to P7 0/12) with the interpretation that the
  savings heuristic wins by
  feeding the co-occupancy channel, evidence FOR the paper's central
  mechanism; P9 exhibit beside Table 4 (median recovery R = 1.00, ships
  as "partially recoverable" per the locked ladder with the zero-budget
  exclusion disclosed).
- **Enumeration anchor** (section 5.4): pool optimum 38 vs P7 +47.4%,
  P5 +147% (config 1, size 8); wording "pool optimum" as locked.
- **New DES subsection or appendix** (B-5): dominance survives concurrency
  (98-100%), decomposition signs survive (config 7 H_up 0.138 > 0);
  closed-form is a conservative evaluator (25-37% pessimistic); per-wave
  rank moderately correlated (rho 0.45-0.68) so wave-level selections are
  scoped to the closed-form model class. fig10.
- **U_c scope fix** (section 4.2 + 6): Cor 2 bounds the M2-side median
  perturbation loss; the M1-side regret of following the Hedge corner is
  a different quantity, measured by C-4 (price 0 in 5/6 configs, 2.63%
  in config 11, covered at eps = 0.10); delete every "worst-case loss at
  most U_c" gloss that equivocates the two.

## 5. Narrative upgrades (from the execution-log grand review)

1. C2 = the two tools + the all-E dominance theorem + Theorem R; formal
   inventory (FINAL SCHEME, adjudicated 2026-07-08 after the triple-check
   found this file conflicting with W1): **Prop 1** identity, **Prop 2**
   all-E conditional chain dominance under (a)(b)(c)(d) (the substantive
   result; statement upgraded per W9 Lemma 6, LABEL KEPT), **Prop 3** SPO
   bridge (demonstrated by P9), **Theorem 1** minimax collapse over
   {M1, M2}, **Theorem R** partition resolution (4.1.4), **Cor 1**
   refinement monotonicity restated as the one-line specialization of
   Theorem R for the implemented corner family (do not state the same
   monotonicity twice), **Cor 2** epsilon bound, **Cor 3** DRO
   certification, **Cor 4** K-model collapse; Lemmas 3-6 appendix-internal.
   Extra find/replace beyond W1 Edit 14: W5:60,64 "Theorem 1" -> 
   "Proposition 3" (SPO-bridge context); W7:325 "(Theorem 1; Elmachtoub
   and Grigas, 2022)" -> "(Proposition 3; ...)"; W7:330-331 "(Theorem 2;
   Mohajerin Esfahani and Kuhn, 2018)" -> "(Theorem 1 with Corollary 3;
   ...)"; plus the three W1-Edit-14 omissions already logged
   (methodology_v0_2.md:19, proposition2_chain_dominance_v1.0.md:5,10,22,
   120, TERMINOLOGY.md:51).
2. C3 headline: "the binary capacity-vs-policy verdict is seed-stable
   (unanimous in 15/18 configs; capacity-dominant in 18/18 replicate
   means) while the numeric share is a resolution- and metric-indexed
   reading with quantified measurement error" plus the per-regime
   diagnostic story.
3. Integrity as a selling point: pre-registration + locked gates + three
   self-check catches (production tie-break bug, SPO+ sign bug, exposure
   measurement) reported in section 5.1.
4. Hedge Rule: robustness empirically free in 5/6 configs; certificate
   valid-but-conservative; deployable ex ante.
5. Venue: the package now supports a TR-E/EJOR attempt; C&IE remains the
   safe main target.

## 6. Residual author to-dos (nothing else remains open from the audits)

1. Read-throughs: W9 5.2, W8, the two-paragraph midpoint-bracketing
   argument, the six signed amendments' locked rules.
2. Wang, Tao & Yang (2025) bibliographic confirmation at the publisher;
   Boysen & de Koster (2025) full read (stub closure).
3. Manual search of the Word masters for "event-driven"/"balanced"/DRO
   gloss remnants (W6 open issue 1).
4. Apply W1-W8 + this file to paper_draft. CORRECTED splice order
   (triple-check finding: W3-E4 is SUPERSEDED by Lemma 6 and must NOT be
   pasted verbatim): section 4.2.1 = W3-E4's paragraph STRUCTURE with W9
   section 7 knock-ons applied (single Proposition 2 under (a)-(d) for all
   E, Conjecture 1 paragraph deleted, both necessity examples kept), then
   W1's cross-references EXCEPT Edits 8 and 11's retired exclusivity
   sentences (replace with the two-channel wording per W10 section 4 /
   B-1), then W6/W7 line edits (W7's "Wang, Tao & Yang" citations become
   "Wang et al." per the five-author Crossref record), then the section 5
   rewrites above.
5. Optional (registered, non-gating): B-4 robustness battery, B-6(ii),
   B-7 initial-position sensitivity, A-R5 multi-split OOS, B-10.
