---
title: "Pre-registered amendment B (2026-07-08): deferred new-simulation experiments"
parent: "paper_draft/phase5_scaleup_preregistration.md (LOCKED 2026-05-19)"
date: 2026-07-08
status: "DRAFTED AND DATED BEFORE ANY EXECUTION. None of the experiments below has been run as of this date; execution is deferred until compute is free (background experiments currently occupy the machine). Registering the designs now fixes hypotheses, gates, and reporting rules before any result is seen."
author_signoff: "SIGNED (Shiyue Hu, 2026-07-08). Authorization given by explicit author instruction in the 2026-07-08 working session (recorded in EXECUTION-LOG.md); countersigned by the assistant on the author's behalf. The author retains the final pre-submission read of every locked rule."
---

# Amendment B: deferred experiments (registered 2026-07-08, not yet run)

Estimated total compute: all items together are on the order of one Phase 5
run (the pre-registration's smoke-calibrated estimate for ~107k sims is
"minutes, not hours"). Item B-5 (DES cross-check) is bounded by coding time,
not runtime.

## B-1. Matched-assignment verification of Proposition 2's hypotheses

**Motivation**: Proposition 2 assumes (a) common processing order and
(b) common AMR-to-order assignment across M1/M2. The production harness
assigns each order to the earliest-free AMR (simulator.py, `min(amrs, ...)`),
so matched M1/M2 runs need not satisfy (b); the reported 99.2% therefore
conflates (b)-differences with condition-(c) violations.

**Design**: add a `simulate_wave` variant accepting a frozen order-sequence
and AMR-to-order assignment. Replay every Block C matched wave (6 configs x
5 arms x matched waves; ~18,000 replays) with the assignment recorded from
the M1 run enforced under M2.

**Addendum (2026-07-08, same day, BEFORE execution)**: the W3 theory-revision
draft constructed and numerically verified a second violation channel,
*adverse repositioning* (Example X.2: E=1, c=2, one AMR, orders (1->8) and
(8->7); C_max M1 = 103 > M2 = 68 with conditions (a), (b), (c) satisfied and
zero batching events; verified by direct simulate_wave calls 2026-07-08).
The trace classifier below must therefore distinguish THREE outcomes per
violating wave: batch-overtaking, adverse repositioning, other/unclassified.

**Pre-registered outputs and gates**:
- Report (i) the per-wave frequency with which (b) already holds under free
  assignment, (ii) the per-wave `M2 >= M1` frequency under enforced (a)+(b),
  (iii) the per-channel classification of enforced-run violations:
  batch-overtaking vs adverse repositioning vs other (trace-verified,
  extending chain_dominance_empirical_v1.0.md's classifier).
- Gate (locked): the manuscript sentence "all violations are batch-overtaking
  events" is RETIRED regardless of outcome (Example X.2 already falsifies it
  as a general claim). The replacement sentence reports the measured
  per-channel decomposition. If adverse-repositioning violations are found at
  a frequency above 0.1% of waves, the section 4 statement of Proposition 2
  must carry condition (d) prominently (not only in the appendix).
- The 99.2% headline stays as the FREE-assignment number (it describes
  practice); the enforced number is reported next to it as the
  theorem-aligned measurement.

**Second addendum (2026-07-08, registered BEFORE B-1 execution)**:
(iv) the ALL-wave base rates of the two exclusion events are counted on the
same replays (batch-overtaking events and adverse-repositioning events per
wave, over all ~6,000 Block C waves, not only violating ones), so section 4
can state how often each condition binds in the operational distribution.
(v) Instrument: the fidelity-gated mirror walk (index-stable tie-break, the
documented intent semantics; BUGREPORT-2026-07-08 applies to the stored
production values, exposure 0.27%). (vi) Enforcement direction as
registered: the M1 free run's AMR assignment is enforced on M2; the free
runs of both models are also recorded to measure how often hypothesis (b)
holds endogenously.

## B-2. Small-instance exact benchmark

**Design**: smallest grid cell (F=3, |A|=5, E=1 and E=2), wave size 8,
candidate pool restricted to 2,000 waves; exhaustive evaluation of every
candidate under deterministic M2 (the simulator is deterministic, so
enumeration IS the exact optimum over the pool); optionally CP-SAT only if
enumeration is infeasible, which is not expected.

**Pre-registered outputs**: one table positioning P5, P6, P7 against the
enumerated optimum: optimality gap of each policy per cell (percent above
enumerated best makespan). No gate; descriptive anchor. Locked wording rule:
the enumerated optimum is "the pool optimum", not "the global optimum" (the
pool is sampled, and this must be stated).

> **Dated note (2026-07-08, before execution)**: enumeration runs over the
> FULL 3,000-candidate pool (not the registered 2,000-wave restriction),
> because the stored P5/P6/P7 values were produced on the 3,000-pool and
> comparability requires the identical pool. Strictly more exhaustive; the
> pool optimum can only be lower, which makes every reported policy gap
> conservative (larger), never smaller. Cells: config 0 (E=1, Block A
> favorable-arm median as the P5 proxy, no P7 available) and config 1
> (E=2, stored Block B P5/P6 and ablation P7 medians), wave size 8, M2.

## B-3. Published-heuristic comparator P8

**Design**: adapt one published planar batching heuristic (seed/savings
lineage, Gademann-Scholz family; exact variant fixed at implementation time
and documented BEFORE running) to the shared candidate-pool protocol: P8
selects waves by the adapted savings criterion from the SAME pool as P0-P7,
Block B protocol (12 cells, same seeds).

**Pre-registered gates (locked)**: none; P8 enters the win matrix and Table 4
descriptively. Explicitly registered in advance: P8's result is reported
whether P5 beats it or not.

> **Dated note (2026-07-08, variant fixed BEFORE running, per the
> registration's own requirement)**: P8 score(W) = raw elevator travel
> minus Clarke-Wright-style batching savings plus a seed-heuristic
> destination-spread term:
> score = sum over orders |src - dst|
>         - sum over (src, dst) groups floor(n_group / 2) * |src - dst|
>         + 0.5 * (max dst - min dst).
> P8 selects the 200 lowest-scoring candidate waves per cell (ties by pool
> index). Block B protocol, policy index 9 seed streams
> (arm stream seed + 13*10, sim stream seed + 2003 + 9), model M2,
> 12 cells.

## B-4. Publication-scale robustness battery

**Design**: re-run the three strongest prototype-scale robustness checks on
the 6 Block C configs at matched-wave scale (~30-50k sims total):
(i) directional switch penalty 3s (`ElevatorPoolDirectional`),
(ii) heterogeneous per-elevator capacities (`ElevatorPoolBatchedHeterogeneous`),
(iii) service-time noise `service_sigma in {0.2, 0.5}`.

**Pre-registered outputs and gates (locked)**:
- For each variant: per-wave `M2 >= M1` dominance frequency and the Hedge/DRO
  corner agreement (D2-d analogue) per config.
- Gate: the manuscript claims "the Hedge Rule's empirical foundation is
  robust to these extensions" only if dominance frequency stays >= 90% on
  average and >= 80% worst-cell within each variant, mirroring D2-a.
  Otherwise the affected variant is reported as a boundary of validity in
  section 6 (this is an acceptable and reportable outcome).
- Scale labels: these replace, not join, the prototype-scale appendix rows;
  any prototype number retained in the appendix carries an explicit
  "prototype scale" label.

## B-5. Event-driven cross-validation of the closed-form simulator

**Design**: SimPy reimplementation of M1 and M2 (concurrent AMR processes,
elevator resources, identical 5-phase trip constants). Configs {1, 7, 11}
x 200 matched waves x {M1, M2} (~2,400 sims).

**Pre-registered outputs and gates (locked)**:
- Per-wave makespan scatter (closed-form vs DES), Spearman rho per config;
  per-wave dominance frequency under DES; sign and rough magnitude of GAP
  for config 7 under DES.
- Gate: the manuscript sentence "the closed-form accumulator is a faithful
  ordinal proxy for concurrent execution" requires Spearman rho >= 0.9 in
  every tested config AND DES dominance frequency >= 90%. If it fails, the
  limitation section states where the closed-form model diverges, and the
  affected claims are scoped to the closed-form model explicitly.

## B-6. Partition schemes beyond stored data (terciles) and candidate-pool sensitivity

**Design**: (i) tercile corner scheme on the 6 ablation configs (new arms,
~12k sims); (ii) candidate-pool sensitivity: Block A on configs {1, 7} with
CANDIDATE_POOL in {1500, 3000, 6000} and ORDER_POOL_SIZE in {300, 600, 1200}.

**Pre-registered outputs**: A-R1's capacity-share table extended with the
tercile column; GAP/H_up/M_Phi and corner identities per pool setting.
Locked rule: same decision rule as A-R1; pool-sensitivity is descriptive
(claim of pool-robustness requires corner identities stable in >= 5/6 of
tested settings).

## Execution order note

B-1 and B-4 reuse the existing driver patterns (experiments_phase5.py); B-2
and B-3 are new driver scripts around the existing simulator; B-5 is new
code. Nothing here retunes any policy, moves any pre-registered gate, or
adds a comparator after seeing its results: every gate and reporting rule
above is locked at registration time.
