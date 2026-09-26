---
title: "Pre-registered amendment A (2026-07-08): reanalysis-only additions to Phase 5"
parent: "paper_draft/phase5_scaleup_preregistration.md (LOCKED 2026-05-19)"
date: 2026-07-08
status: "DRAFTED AND DATED BEFORE EXECUTION. All analyses below operate exclusively on Phase 5 artefacts already on disk (raw CSVs under prototype/results/raw/, block JSONs under prototype/results/). No new simulations are run under this amendment."
author_signoff: "SIGNED (Shiyue Hu, 2026-07-08). Authorization given by explicit author instruction in the 2026-07-08 working session (recorded in EXECUTION-LOG.md); countersigned by the assistant on the author's behalf. The author retains the final pre-submission read of every locked rule."
scope_rule: "None of the analyses in this amendment re-judges a pre-registered gate. The Phase 5 verdicts (H-D1 PARTIAL 57/72, H-D2 PASS, H-D3 model-sensitive, H-Policy Partial) are final per pre-reg section 8 stop-rule 3 and are reported unchanged. Everything here is descriptive, sensitivity, or presentation-layer."
---

# Amendment A: reanalysis-only additions (executed 2026-07-08)

Motivation: the 2026-07-07 internal review (multi-agent audit, four referee
lenses) identified reporting gaps that a Computers and Industrial Engineering
referee would flag: the capacity-share headline lacks a partition-sensitivity
check, win fractions and dominance frequencies carry no uncertainty, the 72
simultaneous D1-d bootstrap CIs have no multiplicity treatment, the corner
selection inside M_Phi is fit and evaluated on the same sample, and Table 4
omits three of the seven pre-registered comparators. Each item below fixes one
of these by reanalysis of existing artefacts.

Common settings, locked here before execution:

- RNG seed for every new bootstrap / split in this amendment: `20260708`.
- Bootstrap replicates: 1000 (matching analysis_phase5_blockA.py).
- All decision rules below are stated BEFORE results are seen.

## A-R1. Partition-sensitivity of the capacity-share reading

**Data**: `raw/mvs_v0_5_phase5_ablation_scheme.csv` (pre-reg section 9.1 A4
amendment data; 6 configs {1,3,5,7,9,11}, size 16, model M2, schemes
`2x2_CI`, `3x3_CI`, `2x2x2_CIT`, plus the shared `random` arm) and
`raw/mvs_v0_5_phase5_blockA.csv` (72 sub-cells, scheme `2x2_CI` at sizes
{8,30}, models {M1,M2}).

**Computation**: per (config, scheme): corner medians `m_q`, pooled-random
median `m_0`, then

- `H_up = (m_qmax - m_0)/m_0` (structural ceiling; partition-intrinsic),
- `S_or = (m_0 - m_qmin)/m_0` (oracle-recoverable slack; partition-intrinsic;
  equals `M_Phi` when the wave-release rule picks the oracle corner),
- `UB = H_up + S_or`, and the **capacity share** `H_up / UB`.

The Phi-rule-based split `H_up/(H_up + M_Phi)` (the 72-sub-cell "~72%"
headline) is only defined where `favorable_corner` exists (the 2x2 scheme);
it is reported alongside for the same 6 configs for reference. Terciles and
any scheme not present in the stored CSVs are explicitly OUT OF SCOPE here
(they require new simulation; see Amendment B, item B-6).

**Locked decision rule**: the manuscript keeps the headline sentence "the
binding limitation is predominantly capacity-side" only if `H_up/UB > 0.5`
in at least 5 of 6 configs under EVERY stored scheme. Otherwise the headline
is restated as partition-conditional ("at the 2x2 resolution a practitioner
would act on") in Abstract, section 5, and section 6.

## A-R2. Statistical hardening (uncertainty and multiplicity)

**Data**: `raw/mvs_v0_5_phase5_blockB.csv` + `raw/mvs_v0_5_phase5_ablation_P7.csv`
(Block B), `raw/mvs_v0_5_phase5_blockC.csv` (Block C),
`raw/mvs_v0_5_phase5_blockA.csv` (Block A).

1. **Block B win fractions**: Wilson 95% intervals on every pairwise win
   fraction over the 12 (config, size) cells (n = 12; intervals will be wide,
   reported as such).
2. **Block B distribution tests**: per cell and policy pair, two-sided
   Mann-Whitney U on the per-sim makespan samples (policies select different
   waves, so within-cell samples are unpaired); across the family of
   (28 pairs x 12 cells) tests, Benjamini-Hochberg FDR at q = 0.05.
   Across-cell paired complement: Wilcoxon signed-rank on the 12 paired cell
   medians per policy pair, BH-corrected across the 28 pairs.
3. **Block C dominance**: Wilson 95% intervals on per-wave `M2 >= M1`
   frequency per (config, corner) cell and pooled (the 99.2% / 96.0%
   numbers).
4. **D1-d multiplicity sensitivity**: per sub-cell one-sided bootstrap
   p-value `p = (1 + #{boot GAP <= 0}) / (N_boot + 1)` with the same
   estimator as analysis_phase5_blockA.py, then BH-FDR at q = 0.05 across
   the 72 sub-cells. **The pre-registered D1-d verdict (57/72, PARTIAL) is
   not re-judged**; this analysis is reported as a sensitivity note
   ("resolved sub-cell count under BH-FDR: X/72").
5. **H-D3 rho CI**: the pre-registered bootstrap CI on mean corner-ranking
   Spearman rho (missing from the W6 artefact): resample waves within each
   (config, arm) cell, recompute corner medians, rankings, and rho; 1000
   replicates; report the 95% percentile interval.

**Locked decision rule**: none of these change any verdict. They populate
uncertainty columns in the manuscript tables and one sensitivity sentence
each in section 5.

## A-R3. Out-of-sample evaluation of the corner selection inside M_Phi

**Motivation**: in `M_Phi = (m[q_phi] - m[q_min])/m_0`, the argmin `q_min` is
fit and evaluated on the same 200-wave sample, which biases `M_Phi` upward
(winner's curse on the oracle corner). Theorem 1's bridge to
predict-then-optimize invites exactly this referee question.

**Computation**: per Block A sub-cell, split each arm's waves 50/50 with seed
20260708; determine `q_min_train` (and `q_max_train`) from training-half
corner medians; evaluate `M_Phi_oos = (m_test[q_phi] - m_test[q_min_train])/m_0_test`
and `H_up_oos = (m_test[q_max_train] - m_0_test)/m_0_test` on the held-out
half (`q_phi` = the stored `favorable_corner`, which is NOT refit, as it was
fixed ex ante). Report per sub-cell in-sample vs out-of-sample values, the
mean relative shrinkage, and the count of sub-cells where the train-selected
extreme corner is not the test argmin/argmax.

**Locked decision rule**: report both numbers regardless of direction. If
mean `M_Phi` shrinks by more than 25% relative out-of-sample, section 5 adds
the sentence "in-sample M_Phi overstates the recoverable slack; we therefore
quote the out-of-sample value alongside" and the abstract number (if any)
switches to the out-of-sample value. The GAP identity rows (D1-a/c) are
algebraic and unaffected.

## A-R4. Presentation-layer completion (no new statistics)

1. **Table 4 completed to all seven pre-registered comparators plus P7**:
   P2/P3/P4 rows added from `v0_5_phase5_blockB.json` (already computed,
   never rendered), including the adverse P2 result (P2 beats P5 in 0.42 of
   cells). One manuscript paragraph addresses it.
2. **Main results table with absolute values**: per sub-cell `m_0` (absolute
   median makespan, time units) recomputed from the Block A raw CSV alongside
   the stored GAP/H_up/M_Phi/CI; 18-row per-config summary in the main text,
   72-row version in the appendix.
3. **Experiment-design table**: the 18 configs with factor levels and the
   defining relation `demand_idx = (F_idx + A_idx) mod 3`, with an explicit
   aliasing disclosure (F, |A|, demand main effects not separately
   identifiable); block sim counts reconciling to 106,800.
4. **Figure repairs** (presentation amendment for the deviation from the
   pre-registered heatmap spec): Fig "gap landscape" re-rendered faceted by
   demand with the aliasing caveat in the caption; Fig "P5 vs P6" re-rendered
   as a signed per-cell difference plot; the Hedge Rule schematic re-worded
   from "dispatch" to wave-release terminology per TERMINOLOGY.md; new
   exhibits (system schematic, H_up/M_Phi stacked bars, seven-policy
   distribution plot, practitioner decision-workflow figure) added. No
   underlying numbers change.

## Execution log

- 2026-07-08: amendment drafted and dated. Analyses A-R1..A-R4 executed the
  same day, AFTER this file was written. Scripts and outputs live in
  `revision_2026-07-08/tier2_analysis/`; each output JSON embeds the script
  name, input file hashes are not recorded (files are git-tracked instead).
- 2026-07-08 (post-execution, factual record; rules above unchanged):
  - **A-R1: the locked decision rule FIRED.** Capacity share H_up/UB > 0.5
    in 2/6 configs (2x2_CI), 4/6 (3x3_CI), 5/6 (2x2x2_CIT). Per the locked
    rule the manuscript headline is restated as partition- and
    metric-conditional; the Phi-rule share on the 72-sub-cell grid (0.717)
    stays as a described measurement, not a universal claim.
  - A-R2: D1-d BH-FDR sensitivity resolves 62/72 (pre-reg verdict 57/72
    PARTIAL unchanged); pooled dominance 99.21% Wilson [98.92%, 99.42%],
    worst cell 96.0% [92.3%, 98.0%]; H-D3 mean rho 0.750 CI [0.517, 0.875];
    221/336 Mann-Whitney tests significant after BH.
  - A-R3: mean M_Phi shrinks 16.6% out-of-sample (H_up 21.2%); below the
    locked 25% materiality bar, so no wording change is triggered; capacity
    share stable (0.717 in-sample, 0.705 OOS).
  - A-R4: tables T1-T6 and figures 1-7 generated under
    `revision_2026-07-08/tables/` and `figures/`.
