# MVS v0.2 — Geometric mechanism experiment

**Date**: 2026-04-21
**Script**: [src/experiments_geometry.py](../src/experiments_geometry.py)
**Pre-registration**: [intuitions_before_MVS_v0_2.md §1ter](../intuitions_before_MVS_v0_2.md)
**Raw data**: [results/raw/mvs_v0_2_geometry_samples.csv](raw/mvs_v0_2_geometry_samples.csv) (20000 rows)
**JSON**: [results/v0_2_geometric_mechanism.json](v0_2_geometric_mechanism.json)
**Figures**: [results/figures/geometry_*.png](figures/)

---

## 1. Decision gate outcome

| Pre-registered metric | Value | Threshold | Verdict |
|---|---|---|---|
| Pearson \|corr(N/F, β(C))\| across 20 cells | **0.153** | ≥ 0.7 → confirmed | ❌ **MECHANISM_REJECTED** |
| Same | 0.153 | ≥ 0.4 → suggestive | ❌ Below suggestive |

**The AMR-fleet-parallelism hypothesis as formulated (β(C) sign controlled by N/F ratio) is NOT supported.**

This is **Surprise #11** against [intuitions_before_MVS_v0_2.md §1ter](../intuitions_before_MVS_v0_2.md).

---

## 2. The full grid

5 N_AMRs × 4 F values × 1000 waves each. Fixed E=2, capacity=2 (throughput, no batching).

### β(C) heatmap

[figures/geometry_heatmaps.png](figures/geometry_heatmaps.png) — left panel.

| | F=3 | F=5 | F=7 | F=10 |
|---|---|---|---|---|
| **N=3**  | +3.6 | +18.7 | +7.6 | +6.1 |
| **N=5**  | +11.6 | +14.4 | +19.5 | +2.3 |
| **N=10** | −8.2 | −3.5 | −8.9 | **+18.0** |
| **N=15** | +1.9 | −10.0 | +24.0 | +20.7 |
| **N=20** | +14.8 | +5.9 | +10.4 | −6.9 |

### β(C) vs N/F scatter

[figures/geometry_betaC_vs_NoverF.png](figures/geometry_betaC_vs_NoverF.png)

20 points, R = N/F ranges 0.30–6.67. Pearson r = **−0.153**. Visually no trend. **The pre-registered prediction was clearly wrong.**

---

## 3. Substantive findings (in order of importance)

### 3.1 N/F is the wrong knob

The pre-reg invoked Tier 1.4's −0.76 correlation between N/(E×c) and β(C) across 6 Phase-1 regimes as evidence for the mechanism. **That correlation does not generalise** when N and F vary independently. Plausible reasons:

- Tier 1.4 had N=10 and F=5 fixed; only E×c varied. The "geometric" interpretation (N/F as the knob) was over-extrapolation from a one-axis sweep.
- Effective slots E×c and floor count F have different physical meanings: slots is queueing capacity, F is spatial spread of the workload. Conflating them via "N/F" loses information.

### 3.2 β(C) IS strongly N-dependent, but non-monotone

Average β(C) by row (across F values):

| N | mean β(C) | sign |
|---|---|---|
| 3 | +9.0 | + |
| 5 | +12.0 | + |
| 10 | −0.7 | ≈ 0 |
| 15 | +9.2 | + |
| 20 | +6.3 | + |

β(C) at N=10 (Phase 1's value) is the **only** N where the average dips negative. Phase 1 took the row that happened to dip. The Phase 1 "discovery" of β(C) < 0 was real for N=10 but **does not extend to other fleet sizes**.

This is a textbook **Yule–Simpson reversal candidate**: aggregating across N (or marginal slicing) gives a different sign than within most cells.

### 3.3 The size-dependent sign flip from Tier 1.3 is the real finding

Tier 1.3 reported β(C) > 0 for size 3-4 and β(C) < 0 for size 7-8 in **every** Phase-1 regime. The Geometric experiment used wave size range 3-8, so each cell's β(C) is an average over that range. The cells with the most negative β(C) (N=10 row) are likely picking up the same large-wave saturation effect, but it's not strong enough to show up as a clean N-trend because wave-size variation within each cell dominates.

**Implication for Paper 3**: the "N/F mechanism" story is dead. The "size×fleet-saturation mechanism" is still alive (Tier 1.3 evidence), but the Geometric experiment did not test it directly because size was treated as a sample-level variable, not a swept axis.

### 3.4 β(I) is also noisy and non-systematic

β(I) ranges from −40 to +21 across the 20 cells with no apparent (N, F) pattern. Pre-reg §1ter.3 explicitly did not predict an I pattern, so this is consistent with prior — but it does mean **neither β(C) nor β(I) has a clean (N, F) explanation**.

### 3.5 R² is much lower than Phase 1's high-relief regimes

R² in-sample ranges 0.65–0.81. Phase 1's E3_c2 was 0.60, E1_c1 was 0.90. The Geometric cells sit in between — the bottleneck-relief × spatial-spread combinations don't produce more predictable systems than Phase 1, just differently structured ones. Further evidence that **R² alone is the wrong metric** for this question.

---

## 4. Updated mechanism candidates

The Geometric experiment falsified one specific hypothesis (N/F ratio controls β(C)). Two candidates remain:

### Candidate A — Wave-size relative to fleet (from Tier 1.3)

Mechanism: β(C) is positive when the wave underloads the fleet (small waves, fleet idle), negative when the wave overloads the fleet (large waves, fleet saturated). The crossover is around size ≈ 5–6 for N=10.

Test (deferred): hold N fixed, sweep wave size range systematically, refit per (N, size_band).

### Candidate B — No simple geometric mechanism exists

Possibility: β(C) is a complex function of wave content × fleet × infrastructure interactions, with no single-variable explanation. The Phase 1 sign reversal is real but **regime-specific** rather than systematic.

If this is true, Paper 3 cannot claim "we explain why concentrated waves are slower in regime X" — only "we observed concentrated waves to be slower in regime X". This is weaker but still publishable as an empirical observation.

---

## 5. Updated impact on Paper 3 contributions

| Claim | Pre-Geometric status | Post-Geometric status |
|---|---|---|
| **C3-H3** (counterintuitive: β(C) < 0 in Phase 1) | 🟢 First evidence | 🟡 Partially undercut — the effect is real for N=10 but not generalisable as "N/F mechanism" |
| **Tier 1.3 size-flip hypothesis** | 🟡 Exploratory | 🟡 **Unaffected** — Geometric experiment did not test size×fleet directly. Still the most-promising salvage hypothesis. |
| **C2-M2-conceptual** (Φ as decomposition) | ⬆ Promoted | ⬆ Still promoted (Tier 1.1 physical-units finding stands) |
| **AMR-fleet-parallelism mechanism for C3-H3** | Hypothesis | ❌ **Rejected** as N/F formulation |

---

## 6. What this changes about the salvage

- **Bad news**: C3-H3 cannot use "N/F controls β(C)" as a mechanism. The Phase 1 sign reversal is no longer cleanly explained.
- **Good news**: the size×fleet-saturation hypothesis (Tier 1.3) is the better candidate and was not tested here. A follow-up "Geometric-2" experiment that sweeps wave size range × N is the proper test.
- **Honest news**: Paper 3's Φ-as-decomposition framing still survives (Tier 1.1's physical-units finding is robust). What dies here is one specific "we have a mechanism" sub-claim. The empirical observation (Phase 1 β(C) < 0) remains, just less explainable.

**Recommendation**: do **not** spend additional simulation budget on geometric variations until Phase 1.5 (true batching) and the size×fleet follow-up are scoped. We've now invested 2 experiments testing β(C) mechanisms; further unstructured exploration risks turning v0.2 into a fishing expedition.

---

## 7. Surprise #11 entry (for [intuitions_before_MVS_v0_2.md §7](../intuitions_before_MVS_v0_2.md))

> **Surprise #11 (2026-04-21)**: The AMR-fleet-parallelism hypothesis (pre-reg §1ter.1: "β(C) monotone decreasing in N/F") is rejected at all pre-registered thresholds. Across 20 (N, F) cells with E=2, capacity=2, Pearson corr(N/F, β(C)) = −0.153 (predicted: ≤ −0.7). β(C) ranges from −10 to +24 across cells with no apparent (N, F) trend. The Phase 1 sign reversal at N=10 does not generalise as predicted. **Mechanism candidate updated**: the more promising (untested) hypothesis is now Tier 1.3's "wave size relative to fleet capacity controls β(C) sign." The N/F formulation was over-extrapolation from a 6-point one-axis correlation in Tier 1.4.

---

## 8. Files produced

- [src/experiments_geometry.py](../src/experiments_geometry.py) — sweep runner + analysis
- [results/raw/mvs_v0_2_geometry_samples.csv](raw/mvs_v0_2_geometry_samples.csv) — 20000 rows
- [results/v0_2_geometric_mechanism.json](v0_2_geometric_mechanism.json) — machine-readable
- [results/figures/geometry_heatmaps.png](figures/geometry_heatmaps.png)
- [results/figures/geometry_betaC_vs_NoverF.png](figures/geometry_betaC_vs_NoverF.png)

**Geometric experiment complete (negative result).** Next: Phase 1.5 true-batching simulator refactor.
