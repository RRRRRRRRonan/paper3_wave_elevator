# MVS v0.2 Phase 1 — Regime Sweep

**Date**: 2026-04-21
**Scripts**: [src/experiments_v0_2.py](../src/experiments_v0_2.py), [src/analysis_phase1.py](../src/analysis_phase1.py)
**Data**: 6000 rows = 6 regimes × 1000 paired waves
  Same wave content across regimes (only `n_elevators`, `capacity` vary).
**Raw**: [results/raw/mvs_v0_2_phase1_samples.csv](raw/mvs_v0_2_phase1_samples.csv)
**JSON**: [results/v0_2_phase1_regime_sweep.json](v0_2_phase1_regime_sweep.json)
**Figures**: [results/figures/](figures/)

---

## 1. Decision gate outcome

| Metric | Value | Threshold | Verdict |
|---|---|---|---|
| Max(M3 − M2) across 6 regimes | **+0.0121** (at E3_c2) | ≥ 0.05 → pass | ❌ **REJECTED** |
| Max(M3 − M2) | +0.0121 | ≥ 0.02 → ambiguous | ❌ Below ambiguous |

**H_v2.1 (C/I emerges when bottleneck relieved)** is **not supported** at the threshold the plan committed to.

**However**: the gap **grows monotonically** with bottleneck relief — from +0.0012 in v0.1-equivalent regime to +0.0121 in the most relieved regime — a **10× increase**. The mechanism predicted by H_v2.1 is qualitatively visible; the magnitude is just well under the threshold for "Φ is a useful predictive surrogate."

This triggers the planned **Scenario A rescue** path (see [novelty_analysis_and_contribution.md §8](../../novelty_analysis_and_contribution.md#L408)): Φ remains valid as a **conceptual decomposition** but the "predictive surrogate" framing of C2-M2 must be retired.

---

## 2. Per-regime model ladder (5-fold CV, shuffled, seed=42)

Baseline change vs v0.1: replaced `cross_floor` with `floor_distance = Σ |src − dst|` (Manhattan-weighted) — Phase 0 flagged the original baseline as collinear with `size`. The decollinearisation only partially worked (see §6.2).

| Regime | r²_M1 (size) | r²_M2 (size+fd) | r²_M3 (+C+I) | r²_M3+ (+6 inter.) | **M3 − M2** | M3 − M2_cross | M3+ − M3 |
|---|---|---|---|---|---|---|---|
| E1_c1 (v0.1-like) | 0.886 | 0.897 | 0.898 | 0.898 | **+0.0012** | +0.0046 | −0.0004 |
| E2_c1 | 0.743 | 0.746 | 0.751 | 0.756 | **+0.0051** | −0.0035 | +0.0043 |
| E3_c1 | 0.712 | 0.717 | 0.724 | 0.729 | **+0.0074** | −0.0120 | +0.0052 |
| E1_c2 | 0.743 | 0.746 | 0.751 | 0.756 | **+0.0051** | −0.0035 | +0.0043 |
| E2_c2 | 0.671 | 0.673 | 0.681 | 0.685 | **+0.0083** | −0.0115 | +0.0044 |
| **E3_c2** | **0.584** | **0.588** | **0.600** | **0.613** | **+0.0121** | +0.0020 | +0.0135 |

Heatmaps: [figures/phase1_heatmap_M3_minus_M2.png](figures/phase1_heatmap_M3_minus_M2.png)

**Pattern**: clean monotone ordering — the more the bottleneck is relieved, the larger the C+I increment, and the smaller the size-dominated baseline R². E1_c2 and E2_c1 are exactly equal (a known artefact of the throughput-abstraction model of capacity — see §6.1).

---

## 3. M3 coefficients per regime

| Regime | β(size) | β(floor_dist) | **β(C)** | **β(I)** |
|---|---|---|---|---|
| E1_c1 | +36.76 | +3.04 | **−22.77** | −2.92 |
| E2_c1 | +26.24 | +1.11 | **−23.99** | −12.04 |
| E3_c1 | +18.26 | +1.11 | −9.77 | −13.02 |
| E1_c2 | +26.24 | +1.11 | −23.99 | −12.04 |
| E2_c2 | +14.71 | +0.54 | −5.78 | −11.81 |
| E3_c2 | +9.17 | +0.46 | −7.60 | −9.18 |

**Direction surprise (vs pre-registration §1.3)**:
- Pre-reg predicted **β(C) > 0** ("concentrated waves cluster on bottleneck → longer makespan"). Observed **β(C) < 0** in every regime.
- Pre-reg predicted **β(I) > 0** ("imbalanced waves underutilise return trips"). Observed **β(I) < 0** in every regime.

C is Shannon entropy of source+dest floor distribution: high C = floors used uniformly; low C = orders concentrated on few floors. The negative sign says **uniform-floor waves complete faster than concentrated waves** — opposite of the pre-reg intuition.

A plausible mechanism: with N=10 AMRs and F=5 floors, AMR positions also distribute. A wave whose orders span all floors lets every AMR participate in parallel; a wave concentrated on floors {1,2} forces a few AMRs to do all the work while others sit idle. The bottleneck **inside the AMR fleet** dominates the bottleneck **at the elevator** here.

The I sign reversal is even cleaner: a fully one-directional wave (I=1) just runs the elevator one direction and is straightforward; a balanced wave (I=0) creates more route conflicts. v0.1 hinted at this in scenario C ("counterbalanced 3up/2down" took 148s vs scenario A's 120s for fully concentrated 1→3).

---

## 4. Interpretation

### 4.1 What Phase 1 ruled out

- **The "C/I are invisible only because of v0.1's tight regime" hypothesis** is now testable and **partially refuted**. C/I do not reach the +0.05 threshold in any of the 6 regimes tested.
- **The non-decollinearised baseline (size + cross_floor) is misleading**. Comparing M3 against `size + cross_floor` (M2_cross column) gives **negative** increments in 4 regimes — i.e., the v0.1-style baseline was actually overfitting to noise that C+I help suppress. This validates Phase 0's call to switch to `floor_distance`.

### 4.2 What Phase 1 confirmed (qualitatively)

- **Bottleneck relief shifts variance from queuing to spatial structure.** Baseline R² drops from 0.90 (E1_c1) to 0.59 (E3_c2): once the elevator is no longer the bottleneck, `size` alone explains a lot less, and **the residual variance is increasingly captured by C and I** (10× growth in increment). This is the H_v2.1 mechanism — at the wrong magnitude.
- **Interactions matter slightly more in relieved regimes.** M3+ − M3 grows from −0.0004 to +0.0135. Phase 0 (on v0.1 data) saw zero interaction signal; here at E3_c2 the interactions add another ~1.4 pp.

### 4.3 What Phase 1 surfaced as new

- **Sign reversals on β(C) and β(I)** — pre-registered predictions were wrong. This is the most informative single finding of v0.2 so far.
- **The "more parallelism → more spatial signal" trend is monotone and clean** — even though it never crosses the threshold, the heatmap shape is a publishable insight on its own (regime-dependence of feature informativeness).

---

## 5. Consequences for Paper 3 contributions

| Claim | Pre-Phase 1 status | Post-Phase 1 status |
|---|---|---|
| **C1** problem novelty | safe (Type A) | unchanged |
| **C2-M1** two-stage architecture | safe (Type A) | unchanged |
| **C2-M2** Φ as **predictive surrogate** | testable; needed +0.05 in some regime | **DOWNGRADED** — best evidence is +0.012, not predictive in the surrogate-modelling sense |
| **C2-M2-conceptual** Φ as **conceptual decomposition** | implicit fallback | **PROMOTED** to primary framing — C/I/T as interpretable axes, not as ML feature replacements |
| **C2-M3** Φ beats ML | needed v0.3 to test | now lower priority — predictive surrogate framing weakened |
| **C3-H1** tactical marginal value | Phase 4 | unchanged |
| **C3-H2** regime-dependent | Phase 1 should *find* the regime | **partially supported in unexpected sense**: the *informativeness* of C/I is regime-dependent (monotone), but the magnitudes are uniformly small. This is a regime-dependence finding, just not the one we predicted. |
| **C3-H3** counterintuitive optima | not yet | the **β(C) < 0, β(I) < 0** finding is itself counterintuitive — could feed C3-H3 |

**Net**: Phase 1 weakens the strong "Φ is the right surrogate" framing but strengthens the conceptual-decomposition framing and provides **one publishable surprise** (sign reversal of β(C), β(I) — direct contradiction of the standard "concentrated waves are bad" intuition).

---

## 6. Caveats & limitations

### 6.1 Throughput-abstraction model of capacity

Capacity > 1 is implemented as "an elevator with capacity c behaves like c independent serving slots" rather than true co-occupancy batching (where multiple passengers share a single trip if same source). Consequence: **E=2, c=1 and E=1, c=2 give identical results** (both = 2 slots), as visible in the table. This is a **deliberate simplification** for Phase 1 to avoid an event-driven scheduler refactor; the cost is that the capacity axis under-tests "co-occupancy reduces stops" — a mechanism that could plausibly favour high-C waves (concentrated → easier to batch).

**If the true batching semantics were implemented**, β(C) might flip back positive in capacity > 1 regimes (concentrated waves → more batching opportunity → faster). This is the single most important Phase 1 caveat. v0.3 (or a Phase 1.5 follow-up) should re-test E1_c2 and E2_c2 with true-batching semantics before Paper 3 commits to the β(C) < 0 finding.

### 6.2 Baseline collinearity only partially resolved

Even with `floor_distance` replacing `cross_floor`, `corr(size, floor_distance) = 0.83` in this sample (vs 0.97 for `cross_floor`). Reason: the order pool excludes only (1,1), so ~83% of pool orders are cross-floor and almost every wave's `floor_distance` scales near-linearly with `size`. To truly orthogonalise we'd need to oversample same-floor orders or stratify wave generation by `floor_distance / size` — defer to Phase 2 if needed.

### 6.3 Single wave-content set across regimes

Same 1000 wave specs are reused in all 6 regimes (paired design — strengthens within-wave comparison). But this means the wave-level C, I distributions are identical across regimes; we test how *a fixed wave distribution* performs under different infrastructures, not how *adversarially-chosen waves per regime* would perform. The latter is Phase 4.

### 6.4 No stochasticity

All service times deterministic. Phase 3 will check robustness.

---

## 7. Decision: what does Paper 3 do now?

Per plan §9 v0.2-D scenario, the planned response to "all regimes < threshold" is **Scenario A rescue**. Concretely:

1. **Stop pursuing C2-M2-as-predictive-surrogate.** No more model bake-offs; no more "Φ outperforms ML baseline" framing.
2. **Reframe C2-M2 as Φ-as-decomposition.** The three axes are *interpretable structural features* of waves, not necessarily *predictive features for a regression*. Their value is in **giving a planner human-readable handles** for wave shape, not in replacing learned models.
3. **Pivot the empirical case for Paper 3** toward C3-H1 (Phase 4) — does using Φ to construct waves yield better operational outcomes than random waves? This is a tactical-value claim, not a predictive-modelling claim, and is far less affected by Phase 1's negative result.
4. **Lift the sign-reversal finding to a first-class result.** β(C) < 0 and β(I) < 0 contradict the standard wave-design intuition. If robust under Phase 3 (stochastic) and Phase 1.5 (true batching), this is a genuine novel insight (probably C3-H3 territory).
5. **Skip Phase 2 (temporal clustering) until pre-registration v0.2 is updated.** Pre-reg §1.3 made a directional prediction for T; Phases 0 and 1 already invalidated the directional predictions for C and I. Don't run Phase 2 against an outdated prior — re-pre-register first.

---

## 8. Cost

| Item | Time |
|---|---|
| Code changes (simulator pool, features, experiments, analysis) | ~30 min |
| 6 × 1000 simulations | 0.1 s |
| 5-fold CV across 6 regimes × 5 models | < 5 s |
| Plot generation | < 2 s |
| **Total compute** | **~10 s** |
| Decision value | **high** — definitively closes the "regime relief saves Φ-as-surrogate" question |

---

## 9. Files produced

- [src/experiments_v0_2.py](../src/experiments_v0_2.py) — regime-sweep runner
- [src/analysis_phase1.py](../src/analysis_phase1.py) — per-regime model ladder + heatmap
- [results/raw/mvs_v0_2_phase1_samples.csv](raw/mvs_v0_2_phase1_samples.csv) — 6000 rows
- [results/v0_2_phase1_regime_sweep.json](v0_2_phase1_regime_sweep.json) — machine-readable
- [results/figures/phase1_heatmap_M3_minus_M2.png](figures/phase1_heatmap_M3_minus_M2.png)
- [results/figures/phase1_heatmap_r2_M3.png](figures/phase1_heatmap_r2_M3.png)
- [results/figures/phase1_heatmap_M3_minus_M2cross.png](figures/phase1_heatmap_M3_minus_M2cross.png)

**Phase 1 complete.** Recommended next step: pause to update [intuitions_before_MVS.md §8](../intuitions_before_MVS.md) and decide between (a) Phase 1.5 true-batching follow-up, (b) Phase 4 (tactical), (c) re-pre-register v0.2 then Phase 2.
