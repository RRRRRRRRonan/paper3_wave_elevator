---
title: "Execution deviation note (2026-09-26): code changes after signing, before any Study 1 run"
parent: "AMEND-2026-09-26-S1B_new_simulations.md general rule 1 (SIGNED 2026-09-26); applies to every Study 1 item of S1A, S1B, and S1C"
date: 2026-09-26
status: "ACKNOWLEDGED 2026-09-26; written after signing and before any registered Study 1 run; adds no item, gate, threshold, or reporting rule. Nothing executed as of acknowledgement."
author_signoff: "ACKNOWLEDGED (Shiyue Hu, 2026-09-26). Authorization given by explicit author instruction in the 2026-09-26 working session ('确认 S1D'), after the author's review of this note and its evidence file; the assistant entered the acknowledgement at that instruction."
---

# Execution deviation note S1D: code changes after signing

## 中文摘要
签字后、任何 Study 1 正式运行之前，代码有两处改动，因此代码树哈希不再等于签字时钉住的值（3ef64f08…）：
(1) 签字后发现的守卫缺陷修复（S1B 状态行让已勾选的 S1-11 被读成未勾选）；
(2) 按 S1B 通用规则 1 的要求，让每个 Study 1 输出同时记录运行代码的哈希和钉住的哈希。规则 1 已登记，但在签字前没有实现。
另有 (3)：守卫现在要求本说明先确认并钉住，Study 1 才能正式运行。
规则 1 只允许"不触及 Study 1 脚本所导入文件"的后续代码，而这些改动触及了 Study 1 脚本本身和它们导入的守卫，所以需要本说明。
所有设计、种子、门槛、判定规则和输出文件名都不变；模拟器与分析模块与签字版逐字节相同。
在签字版代码和当前代码上各跑一次 11 个自测，去掉来源字段后，所有输出值完全相同。
确认后，用 `make_manifest.py SIGNED --supersede` 把新代码树（cd0694e4…）连同本说明一起钉住，旧清单原样保留。

## 1. What changed after signing
The signed manifest (`archive_package/MANIFEST_SIGNED.json`, generated 2026-09-26T06:48:53Z) pins code tree `3ef64f08b16beb4ca4f5aa1130202a8d9193c8b04d4f49038de9122c79277135`. Before any registered Study 1 command was run, three changes were made to `prototype/src/`:

1. **Checkbox fix in the guard** (found at signing, EXECUTION-LOG entry 50). The S1B status line written at signing mentions "S1-11 included (D-D1 signed)". `registration_guard.checkbox_ticked` read the first line containing that marker, which was the status line, so the ticked box `[x] yes` read as unticked and S1-11 would have been refused. The function now reads only lines that carry a box. A regression case was added to the guard's self-test.
2. **Code-tree provenance in every Study 1 output.** S1B general rule 1 says that each output records the hash of the code that ran next to the pinned one. Apart from S1-12 (`experiments_S1_b5_rerun.py`), the Study 1 scripts recorded only their own file hash, because the wording was added in the second pre-signing review round and the code was not updated. A function `registration_guard.code_provenance()` now returns `code_tree_sha256`, `code_tree_sha256_pinned`, and `code_tree_matches_pinned`. Its fields are added to the metadata record of six scripts (one import line and one dictionary entry per metadata record): `analysis_S1_cluster_bootstrap.py` (two records), `analysis_S1_displays.py`, `experiments_S1_enumeration.py`, `experiments_S1_blockC_ext.py`, `experiments_S1_tiebreak_regen.py`, `experiments_S1_B4_B6.py`.
3. **This note is required before any Study 1 run.** `require_signed` for S1A, S1B, or S1C now also requires this note to be acknowledged and pinned (`ALSO_REQUIRES` in the guard). A missing registration file now stops with a guard message instead of a Python error. Both behaviours have self-test cases.

The resulting code tree is `cd0694e4fedeee112d451828d8d03adcbd36a576ecf33dbcf5988b54265dd14c`. The full diff (7 files) is in `helper_reports/S1D_equivalence_2026-09-26.md`.

## 2. Why this is a deviation
S1B general rule 1 allows a code tree later than the pinned one only if the difference "touches no file that the Study 1 scripts import". The changes touch the Study 1 scripts and `registration_guard.py`, which every Study 1 script imports. The condition is therefore not met, and the change is recorded here as a dated execution deviation, before any registered Study 1 result exists.

## 3. What does not change
- No item, design, seed, configuration, pool, gate, threshold, verdict rule, reporting rule, or output file name of S1A, S1B, or S1C changes. The six signed registration files are not edited.
- `simulator.py`, `features.py`, `wave_policies.py`, `phase5_config.py`, `des_evaluator.py`, all `analysis_phase5_*` modules, and every other file under `prototype/src/` except the seven listed are identical to the pinned tree (CRLF read as LF). In the six Study 1 scripts, only the import line and the metadata entries changed; no line that computes a result changed.
- Study 2 is not affected. Its test pools stay blocked until the L2 addendum is signed, and the L2 addendum names its own code tree at that time.

## 4. Evidence that the results are unchanged
The pinned tree was rebuilt in a separate git worktree (commit `c7a024a` without the checkbox fix), and its code-tree hash was recomputed; it equals the pinned value. The eleven Study 1 self-tests (toy seeds far below every registered seed, scratch output only) were run on the pinned tree and on the current tree. All 11 pass on both. After removing the provenance fields only, all 14 JSON outputs, all 8 CSV outputs, and the one figure are identical: 0 differing values. `python -m src.simulator` passes all hand-computed targets on the current tree. Method, commands, the verbatim comparison output, and the diff: `helper_reports/S1D_equivalence_2026-09-26.md`.

## 5. Pinning and use of results
1. After acknowledgement, `make_manifest.py SIGNED --supersede` writes a new `MANIFEST_SIGNED.json` that pins this note and the code tree `cd0694e4…`. The previous manifest is kept unchanged as `MANIFEST_SIGNED_superseded_<UTC stamp>.json`, which keeps the original pin `3ef64f08…` on record. The six signed files keep their pinned hashes, so the guard's re-pin check does not fire for them.
2. Every Study 1 output then records `code_tree_sha256` and `code_tree_sha256_pinned`. A Study 1 result is used only if the two are equal, or if any later difference meets S1B general rule 1 and is listed in EXECUTION-LOG.md before the result is used. Any other code change before Study 1 is complete needs a further dated note.
3. This note and the new manifest are added to the OSF registration as an update (J4: under embargo until acceptance). The OSF update date is the external timestamp of this note.

## Acknowledgement
To acknowledge: in one edit, fill the line below, set `author_signoff` to "ACKNOWLEDGED (<name>, <date>)", and replace the `status` line. Then run, from the repository root, `python "revision_2026-09-26_ijpr/archive_package/make_manifest.py" SIGNED --supersede`. Then open `MANIFEST_SIGNED.md` and confirm that the signoff column of all seven registrations starts with SIGNED or ACKNOWLEDGED, and that the code tree reads `cd0694e4…`.

```
Author acknowledgement: Shiyue Hu  Date: 2026-09-26
```
