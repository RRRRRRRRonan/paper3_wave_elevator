---
title: "Phase 6 protocol, Stage L2 addendum (P11 weights, case parameters, code freeze)"
parent: "paper_draft/phase6_method_study_protocol.md (L1; its bytes are frozen at signature and pinned in revision_2026-09-26_ijpr/archive_package/MANIFEST_SIGNED.json)"
date: ""
status: "TEMPLATE. Filled in week 4 after the Stage L2 tuning on training pools, before any test pool exists."
author_signoff: "PENDING"
protocol_L1_sha256: ""
osf_registration_id: ""
code_tree_sha256: ""
p11_weights: ""
des_subset_mode: ""
case_included: ""
case_speed_per_floor: ""
case_load_time: ""
case_unload_time: ""
case_service_time: ""
case_speed_per_floor_range: ""
case_load_time_range: ""
case_unload_time_range: ""
case_service_time_range: ""
---

# Stage L2 addendum to the Phase 6 protocol

## 中文说明
这个文件替代原来写在协议末尾的 Appendix L2。协议（L1）签字后一个字节都不再改；OSF 编号、调参结果、案例参数、代码哈希都写在这里，并单独签字。`src/registration_guard.py` 会检查：协议与本文件都已签字、都与签字清单里的哈希一致、本文件里的 `protocol_L1_sha256` 等于协议当前的哈希。代码从本文件读取 P11 权重和案例参数，所以调参之后不需要改代码，L2 记录的代码哈希就是调参时实际运行的代码。

## How to fill it in (week 4)
1. Run `python -m src.experiments_phase6 tune` (training pools only; also writes the runtime projection of §14).
2. Copy into the front matter: `p11_weights` as "alpha, beta, gamma" (the selected triple), `des_subset_mode` (yes only if the runtime projection exceeds 48 hours), `case_included` (yes if decision D-K is signed and the data file passed the §11.2 checks, otherwise no), the four `case_*` midpoints and the four `case_*_range` values as "low, high" with their sources in the table below (only if `case_included` is yes), `code_tree_sha256` from the tuning output's `code_tree_sha256` field, `protocol_L1_sha256` from `MANIFEST_SIGNED.json`, `osf_registration_id` from the OSF registration of L1, and `date`.
3. Record below: the G0 checks, the 27 tuning scores (or a pointer to `v0_6_phase6_L2_tuning.json` with its SHA-256), and the case parameter sources.
4. Set `author_signoff: "SIGNED (<name>, <date>)"`, then run `python "revision_2026-09-26_ijpr/archive_package/make_manifest.py" SIGNED_L2`, and register this file on OSF as an update of the L1 registration.
5. Only then generate test pools (`main`, `warmstart`, `runtime`, `case`).

## Record

```
G0 checks 1 to 7 (protocol §12): pass / fail, with log reference:
Tuning output file and SHA-256:
Selected (alpha, beta, gamma):
Runtime projection from the training pool (hours); set des_subset_mode above to yes if it exceeds 48 hours, otherwise no:
Case parameter table (value, documented range, source) or "case dropped (D-K)":
  travel time per floor:
  loading time:
  unloading time:
  AMR service time:
Confirmation that no test-pool seed has been used before this date:
```
