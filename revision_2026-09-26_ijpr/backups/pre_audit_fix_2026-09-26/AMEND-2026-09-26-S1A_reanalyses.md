---
title: "Registered re-analyses of stored Phase 5 data (2026-09-26): S1-1, S1-6, S1-7, TH-2"
parent: "paper_draft/phase5_scaleup_preregistration.md (LOCKED 2026-05-19); revision_2026-07-08/amendments/ (six signed amendments)"
date: 2026-09-26
status: "DRAFT, prepared overnight by the assistant at the author's request. NOT signed. NOTHING executed: no quantity defined below has been computed by the registered procedure. Informal audit values seen earlier are disclosed in each item."
author_signoff: "PENDING"
evidence_tags: "[RA] for S1-1, S1-6, S1-7, TH-2 (re-analysis of stored data; cannot change any locked verdict)"
---

# Registered re-analyses of stored Phase 5 data

## 中文摘要

- 本文件登记四项"只用已存数据"的重分析：S1-1 候选聚类 bootstrap；S1-6 Hedge 选择的 minimax-regret 行与稳定性；S1-7 Supp-1 耦合展示；TH-2 抽象偏差展示。
- 都是 [RA]：不改任何锁定判定（H-D1 仍为 PARTIAL，57/72；H-D2 仍为 PASS），只在旁边并列报告。
- 每项都写明了此前非正式看过的数字（例如聚类 bootstrap 52 到 55/72、稳定性 0.43 到 0.78、41%、7.47%/7.12%），审稿人能判断哪些结果事先可预见。
- 你要确认：种子与 B 值；每项的"措辞规则"；S1-1 以原始 CSV 为主、修复破平后的 CSV 为辅的安排。

## General rules for all items

1. Locked verdicts are unchanged: H-D1 PARTIAL (D1-d 57/72 against a gate of 58/72), H-D2 PASS, H-Policy and Supp verdicts as stored. Every item below is reported next to the locked result, never in place of it.
2. Inputs are the stored artefacts listed per item, read only. Stored artefacts are never overwritten; outputs go to new files named `v0_5_phase5_S1-<item>_*.json`.
3. Every output file records the SHA-256 of each input file and of this registration.
4. Informal values computed before this registration (the 2026-09-25 audit, readiness assessment Part 1) are disclosed per item. They are not results and are not quoted in the manuscript.
5. Primary data, one rule for all items: an item that re-analyses a locked verdict (S1-1, S1-6) uses the stored artefact behind that verdict as primary and the tie-break-fixed data as secondary; a display that feeds a new manuscript statement (TH-2) uses the current-simulator (tie-break-fixed) data as primary and the stored artefact as secondary. Both versions are always reported.

---

## S1-1. Candidate-clustered bootstrap for the Phase 5 intervals [RA]

**Motivation and estimand.** Corner arms draw 200 waves with replacement from a finite corner class, so the same candidate often appears several times (mean 134.7 distinct candidates per 200 rows, minimum 78; M1 and M2 are deterministic, so repeats are identical values). Two estimands must be kept apart. (i) The class median of the finite 3,000-candidate pool: the row bootstrap is the standard interval for the sampled estimate, and S1-2 replaces any interval by the exact enumerated value. (ii) The class median over the population of waves that the order pool can generate, which is what a statement about the configuration (such as D1-d, "the value of wave structure is positive") refers to: here the distinct candidate is the sampling unit, repeated draws of one candidate add no information about the population, and the row bootstrap understates the interval width. The candidate-clustered bootstrap below targets estimand (ii) and is reported as such; for estimand (i) the manuscript reports the exact S1-2 values. The re-analysis is a sensitivity analysis for estimand (ii), not a correction of the preregistered procedure.

**Inputs.** `results/raw/mvs_v0_5_phase5_blockA.csv` joined to `mvs_v0_5_phase5_blockA_candidate_ids.csv` by `row_index`; `mvs_v0_5_phase5_blockB.csv` with `mvs_v0_5_phase5_blockB_candidate_ids.csv`; `mvs_v0_5_phase5_blockC.csv` with `mvs_v0_5_phase5_blockC_candidate_ids.csv` (primary, the data behind the locked H-D2 verdict) and `mvs_v0_5_phase5_blockC_tiebreakfix.csv` (secondary, current simulator). The join is checked row by row (config, model, size, arm must agree); any mismatch stops the analysis.

**Procedure.**
- Cluster = one distinct `candidate_id` within (config, model, size, arm) for Block A, within (config, size, policy) for Block B, and within (config, arm) for Block C (size 16 throughout; the M1 and M2 values of a wave sit in one row and are resampled together).
- One bootstrap replicate: within each arm independently, draw as many clusters as the arm has, uniformly with replacement, and include every row of each drawn cluster (its multiplicity is kept). Recompute the statistic exactly as the stored analysis does (`analysis_phase5_blockA.decompose` for GAP).
- B = 2,000 replicates; percentile 95% interval; seed 20260927.
- Seed sensitivity: the same procedure with seeds 20260927 + i, i = 0, …, 9 (i = 0 is the primary seed); the range of counts over these 10 seeds is reported.
- Companion (deduplicated) analysis: each distinct candidate counted once per arm; point estimates and a row bootstrap of the deduplicated rows (same B and seed).
- Reference row: the stored row-level procedure (B = 1,000, seed 20260519) is re-run unchanged to confirm that it reproduces 57/72 exactly. If it does not, the analysis stops and the discrepancy is logged before anything else is reported. The same row-level procedure is then run with seeds 20260519 + i, i = 0, …, 9, and the range of counts is reported next to the locked 57/72 (the locked count is seed-dependent; the informal range 56 to 58/72 reaches the 58/72 gate at one seed).

**Statistics reported.**
- Block A: per sub-cell GAP interval under the clustered bootstrap; the count of sub-cells whose lower limit exceeds 0 (the D1-d statistic), with the 10-seed range; the same for the deduplicated analysis.
- Block B: clustered 95% intervals of each policy's cell median (P0 to P6) and, per cell, of the differences used by the H-Policy bands (P5 − P0, P5 − P1, P5 − P6), with the two policies resampled independently (their waves are different candidates); across cells only the mean of the per-cell differences is reported, without a pooled interval. P7 rows are independent runs and keep a row bootstrap.
- Block C: clustered intervals of the per-cell per-wave ordering rate (share of waves with M2 ≥ M1), of its average over the 24 cells, and of its worst cell.

**Reporting rule (locked).** The manuscript reports, in the Study 1 table, "D1-d: 57/72 (row-level, preregistered; verdict PARTIAL; range a to b over 10 bootstrap seeds)" and beside it "x/72 (candidate-clustered, population estimand; range c to d over 10 seeds)". The analysis unit sentence in §5.1 states that corner arms are samples with replacement, names the two estimands, and says which interval belongs to which. No sentence may describe the clustered count, or the seed range, as the verdict.

**Prior exposure.** The 2026-09-25 audit computed an informal candidate-clustered D1-d count of 52 to 55/72 over 3 seeds and a row-level range of 56 to 58/72 over 10 seeds (readiness assessment Part 1). The registered procedure above fixes the seeds, B, and the handling of multiplicity before any registered value is computed.

---

## S1-6. Minimax-regret row and stability of the Hedge corner [RA]

**Inputs.** Block C matched data (primary: stored CSV; secondary: tie-break-fixed CSV), 6 configurations (1, 3, 5, 7, 9, 11), size 16, arms HC_HI, HC_LI, LC_HI, LC_LI.

**Quantities per configuration**, each computed on class means (the preregistered D2-d basis) and on class medians (the Section 3 decision statistic):
- v_m(q) = class statistic of corner q under m ∈ {M1, M2}.
- Hedge corner = argmin_q max{v_M1(q), v_M2(q)} (as stored).
- Minimax-regret corner = argmin_q max_m (v_m(q) − min_q′ v_m(q′)) / min_q′ v_m(q′).
- Second-place margin = (second-lowest − lowest) / lowest of the Hedge criterion.
- Stability = share of clustered bootstrap replicates (the S1-1 procedure, B = 2,000, seed 20260928) in which the Hedge corner equals the full-data Hedge corner; the same for the minimax-regret corner.

**Display.** One table row per configuration: Hedge corner (mean, median), minimax-regret corner (mean, median), agreement flags, margin, stability. The Block C extension (S1-3) adds rows for the other configurations, marked as [NS] extension rows.

**Wording rule (locked).** A Hedge choice with stability below 0.80 is described as "not stable under resampling" for that configuration; a margin below 1% is described as "a near tie". The locked D2-d collapse count (6/6) is reported unchanged. Disclosure: the 0.80 threshold was set after the informal stabilities 0.43 to 0.78 (5 of 6 configurations) had been seen, so the "not stable" outcome for those configurations is foreseeable and is labelled prior-exposed in the manuscript.

**Prior exposure.** The stored [RA] median block (2026-09-11) gives median margins of 2.29%, 5.59%, 0.96%, 1.04%, 0.84%, and 0.14% and median and mean Hedge corners that disagree in one configuration (5/6 agree). The 2026-09-25 audit computed informal clustered selection stabilities of 0.43 to 0.78 in 5 of 6 configurations. The minimax-regret corner has not been computed.

---

## S1-7. Supp-1 coupling display [RA, prior-exposed]

**Inputs.** `results/raw/mvs_v0_5_supp1_h1scale.csv` (6 configurations, sizes 8 and 30, arms random and phi_corner, dispatch FIFO and cluster, 200 waves each) and `v0_5_phase5_supp.json`.

**Quantities.**
- Per cell (configuration, size) and dispatch rule r ∈ {FIFO, cluster}: class advantage A_r = (median of random − median of phi_corner) / median of random.
- Aggregates reported both ways: the mean of per-cell A_r, and the ratio of grand means (mean over cells of the random medians minus mean over cells of the phi_corner medians, divided by the former). Count of cells with A_r > 0.
- Dispatch gain per arm: (median FIFO − median cluster) / median FIFO. Every quantity is computed from the raw CSV; the stored MV values of the JSON serve only as a check.

**Wording rule (locked).** The text states both aggregates in one sentence ("x% as the mean of cell ratios, y% as the ratio of grand means") and the cell count. The class advantage is described as "persisting under clustered dispatch" only if A_cluster > 0 in at least 9 of 12 cells and both aggregates of A_cluster are positive; otherwise "not robust to the dispatch rule".

**Prior exposure.** The 2026-09-25 audit computed A_FIFO = 7.47% and A_cluster = 7.12% as means of per-cell ratios, 4.86% and 4.25% as ratios of grand means, with 10/12 positive cells each. The registered display therefore has a known outcome; it is registered to fix the definitions and the wording rule, and it is labelled prior-exposed in the manuscript.

---

## TH-2. Abstraction-bias display [RA]

**Definition.** For a wave w, abstraction bias B(w) = (M2(w) − M1(w)) / M1(w), the relative optimism of the throughput abstraction against co-occupancy.

**Inputs.**
- Block C matched rows (primary: tie-break-fixed CSV, which reflects the current simulator; secondary: stored CSV), 6 configurations, size 16, 5 arms.
- S1-3 extension rows (other configurations; sizes 8, 16, 30) once S1-3 has run; marked [NS].
- Supp-2 capacity rows (`mvs_v0_5_supp2_capacity.csv`, c ∈ {2, 3, 4, 5}, size 16) for the capacity facet. These rows carry no candidate identifiers, so the capacity facet uses rows as drawn.

**Display.** Distribution of B over waves (rows as drawn, and deduplicated by candidate where identifiers exist), faceted by E, F, n (from S1-3), and c (from Supp-2); median and interquartile range per facet; share of waves with B < 0 (reversals), cross-referenced with the B-1 channel decomposition.

**Wording rule (locked).** "In this benchmark the throughput abstraction is optimistic by a median of x% (interquartile range a% to b%)", with x from the primary Block C data at size 16. Facet medians are reported in the figure, not merged into x.

**Prior exposure.** The 2026-09-25 audit computed an informal median B of 41% on the tie-break-fixed Block C CSV. No facet has been computed.

---

## Sign-off

```
Author: ____________________  Date: ____________
```
To sign: in one edit, set `author_signoff` to "SIGNED (<name>, <date>)" and replace the `status` line; then run `make_manifest.py SIGNED`. The file's SHA-256 is recorded in `MANIFEST_SIGNED.json` and on OSF, never in this file, and the file is not edited afterwards.
