---
title: "Execution note (2026-09-26): running the registered AMEND-B items B-4 and B-6(ii) as Study 1 items S1-4 and S1-5"
parent: "revision_2026-07-08/amendments/AMEND-2026-07-08-B_deferred_experiments.md (SIGNED 2026-07-08)"
date: 2026-09-26
status: "DRAFT note; adds no design, gate, or reporting rule. NOT signed. Nothing executed."
author_signoff: "PENDING (acknowledgement only; the designs and gates were signed on 2026-07-08)"
---

# Execution note: B-4 and B-6(ii)

## 中文摘要
B-4（换向惩罚、异构容量、服务噪声三项稳健性）与 B-6(ii)（候选池与订单池规模敏感性）在 2026-07-08 已登记签字，但还没有运行，也没有脚本。本说明只记录：按原文执行，不增加、不修改任何设计或门槛；代码按原文规格新写；B-6(i) 三分位方案维持 B-13 的降级（修订轮可选）。

## What this note fixes
1. **Items.** S1-4 = AMEND-B B-4 exactly as registered (6 Block C configurations; direction-switch penalty 3 s; heterogeneous per-elevator capacities; service-time noise σ ∈ {0.2, 0.5}; per-wave ordering rate and Hedge/DRO agreement per configuration; the D2-a-style gate, ≥ 90% average and ≥ 80% worst cell within each variant). S1-5 = AMEND-B B-6(ii) exactly as registered (Block A on configurations 1 and 7 with candidate pools of 1,500, 3,000, 6,000 and order pools of 300, 600, 1,200; descriptive; pool-robustness claimed only if corner identities are stable in at least 5 of 6 settings).
2. **Unspecified details, fixed now before running.** The heterogeneous-capacity variant uses capacities (1, 3) for E = 2 (the only E in the Block C configurations), with the smaller capacity on the first elevator. This keeps the total capacity of the homogeneous (2, 2) baseline, mirroring the prototype-scale "spread, same total" setting [1, 2, 3] of `experiments_B1_heterogeneous_pool.py`; a mix such as (2, 3) was rejected because it would also add capacity. Seeds follow the Block C convention `_seed(cid, 99, 16)` for B-4 and the Block A convention for B-6(ii); the order pool for B-6(ii) at size P uses `generate_pool(demand, F, P, seed = SEED_BASE + cid)`. Simulator: current production code at the G0 freeze.
   - **M1 in the B-4 variants.** The direction-switch and heterogeneous-capacity models exist only for co-occupancy (M2), so in those two variants M1 is the standard throughput abstraction (E·c = 4 single-rider slots, the same total as (1, 3) and (2, 2)); the variant measures whether the ordering survives a more realistic M2. In the service-noise variants both evaluators carry the same σ.
   - **Common random numbers.** In the service-noise variants the M1 and M2 runs of a wave use the same noise seed (both draw two factors per order in the same FIFO order), so the per-wave comparison isolates the elevator model.
   - **B-6(ii) settings and stability.** One factor at a time around the Phase 5 default (candidate pool 3,000, order pool 600): candidate pool 1,500 and 6,000 at order pool 600; order pool 300 and 1,200 at candidate pool 3,000. Each (configuration, model, size) cell of configurations 1 and 7 is compared with its own default setting, recomputed in the same run: 8 cells × 4 settings = 32 tested pairs. A pair is stable when the favourable corner, q_max, and q_min all equal the default's. Pool-robustness is claimed only if at least 5/6 of the 32 pairs (27) are stable; per-identity shares are reported.
3. **Not run.** B-6(i) (tercile corners) stays optional for a revision round, as downgraded by B-13.
4. **Reporting.** As in AMEND-B: B-4 variants that miss the gate are reported as boundaries of validity in §5.5 and §6. Outputs: `results/v0_5_phase5_S1-4_B4.json`, `results/v0_5_phase5_S1-5_B6ii.json`.

## Question for the author
Item 2 fixes details that AMEND-B left open (the heterogeneous capacity pair, the seeds, M1 in the B-4 variants, common random numbers, and the B-6(ii) settings and stability rule). They are the natural choices, but they are new decisions: please confirm or change them before signing. The B-6(ii) choice matters most: the registered text lists the two pool sizes without saying whether they are crossed, paired, or varied one at a time; the one-at-a-time reading was chosen because it separates the two factors.

```
Author acknowledgement: ____________________  Date: ____________
```
