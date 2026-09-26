# Report of the helper agent that wrote the Study 1 scripts (2026-09-26)

Helper: a Sonnet subagent, instructed not to read stored result values, not to use registered seeds, to write self-test outputs only to scratch, and to create six new files only. Its report is condensed below; the assistant's corrections follow.

## What it created
`analysis_S1_cluster_bootstrap.py` (S1-1), `experiments_S1_enumeration.py` (S1-2, S1-8, S1-11), `experiments_S1_blockC_ext.py` (S1-3), `analysis_S1_displays.py` (S1-6, S1-7, TH-2), `experiments_S1_tiebreak_regen.py` (S1-9), `experiments_S1_B4_B6.py` (S1-4, S1-5). Each stopped at the guard without `--selftest` and completed with `--selftest` (toy seeds or fabricated inputs, outputs in scratch). `python -m src.simulator` still passed. It reported that nothing under `prototype/results/` was read, loaded, or modified, and that no git write command was run.

## Ambiguities it flagged (REGISTRATION NOTEs)
1. S1-1 seed range i = 1..9 versus "10 seeds" (implemented i = 0..9).
2. S1-1 Block B differences: per cell or pooled (implemented per cell, independent resampling).
3. S1-1 Block C cluster key collapses to (configuration, arm).
4. S1-2 covering-partition M_Φ(P) not defined for n × n grids (implemented an extreme-bin generalization).
5. S1-2 stored favourable corner exists only under the pool's own model.
6. S1-2 Block C has no stored favourable corner.
7. S1-11 main-effects slice unspecified (implemented per size, M2 only).
8. S1-7 recomputed from the raw CSV instead of reading the JSON.
9. S1-7 wording rule's "under both aggregates" is ill-defined.
10. B-4 M1 for the directional and heterogeneous variants (standard M1).
11. B-6(ii) crossed or paired settings (implemented paired, configurations pooled).

## What it could not implement
P8 and P9 gaps in S1-2 (it did not find the stored values); the S1-11 D-D1 condition (the guard read only front matter); a Block C regeneration check; multiprocessing; the TH-2 size facet before S1-3 has run.

## Assistant's corrections (2026-09-26, before any real run)
- S1-9 now calls the stored analysis code with redirected paths and a hash check, instead of a re-implementation.
- S1-2: Block A regeneration check joins by `row_index` (the helper used the DataFrame index); stored P8 and P9 medians read from the 2026-07-08 outputs; Block C exact regeneration check against the tie-break-fixed CSV that stops on any mismatch; minimax corner also on means; covering partitions report S_or, UB, and H_up/UB (as A-R1) and include a 3 × 3 grid.
- S1-8 also reports the share inside the stored corner.
- S1-11 builds both seed-model pool families (as registered) and requires the D-D1 box (new `require_checkbox`).
- S1-5 rewritten one factor at a time, each configuration against its own default (the helper had pooled configurations 1 and 7 and taken the modal corner).
- S1-4 service-noise variants use common random numbers for M1 and M2.
- S1-7 wording flag follows the clarified rule.
- Registrations S1A, S1B, and the S1C execution note were clarified on every flagged point.
The helper's original versions of the three rewritten scripts are kept in `helper_reports/helper_original_scripts/` for comparison.
