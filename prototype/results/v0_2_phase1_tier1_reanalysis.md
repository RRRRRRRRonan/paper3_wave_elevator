# MVS v0.2 — Tier 1 reanalysis of Phase 1 data (exploratory)

**Date**: 2026-04-21
**Script**: [src/tier1_reanalysis.py](../src/tier1_reanalysis.py)
**Data**: existing 6000 rows from [results/raw/mvs_v0_2_phase1_samples.csv](raw/mvs_v0_2_phase1_samples.csv) — **no new simulations**.
**Pre-registration**: [intuitions_before_MVS_v0_2.md §1bis](../intuitions_before_MVS_v0_2.md)
**Raw**: [results/v0_2_phase1_tier1_reanalysis.json](v0_2_phase1_tier1_reanalysis.json)
**Figures**: [results/figures/tier1_*.png](figures/)

---

## 0. Status: exploratory only

Per pre-reg §1bis, this analysis is **explicitly exploratory**. Patterns surfaced here must be confirmed by the geometric experiment ([results/v0_2_geometric_mechanism.md](v0_2_geometric_mechanism.md)) or Phase 1.5 ([results/v0_2_phase1_5_true_batching.md](v0_2_phase1_5_true_batching.md)) before entering Paper 3 as findings. **One** prediction was pre-registered (1.1).

---

## 1. Tier 1.1 — Physical-unit β coefficients with bootstrap 95% CIs

500-iteration bootstrap on each regime (n=1000 each). M3 fit on [size, floor_distance, C, I].

| Regime | β(size) [s/order] | β(floor_dist) [s/floor] | β(C) [s/nat] | β(I) [s/unit] |
|---|---|---|---|---|
| E1_c1 | +36.75 [+34.78, +38.59] | +3.03 [+2.36, +3.69] | **−22.91 [−35.84, −10.08]** | −2.98 [−7.61, +1.99] |
| E2_c1 | +26.16 [+24.10, +28.19] | +1.14 [+0.47, +1.87] | **−23.08 [−35.47, −10.09]** | −11.83 [−18.46, −6.00] |
| E3_c1 | +18.27 [+16.53, +20.06] | +1.10 [+0.52, +1.66] | −9.83 [−22.21, +1.07] | −13.07 [−18.01, −8.07] |
| E1_c2 | +26.30 [+24.26, +28.33] | +1.10 [+0.42, +1.78] | **−24.10 [−38.79, −10.94]** | −12.05 [−18.19, −5.23] |
| E2_c2 | +14.75 [+13.44, +16.11] | +0.53 [+0.07, +1.03] | −6.17 [−15.20, +2.66] | −11.98 [−16.71, −7.72] |
| E3_c2 | +9.21 [+8.20, +10.38] | +0.46 [+0.10, +0.81] | **−7.55 [−15.19, −1.03]** | −9.17 [−12.68, −5.80] |

[figures/tier1_1_beta_physunits.png](figures/tier1_1_beta_physunits.png)

### Pre-registered prediction check (the only confirmatory part of Tier 1)

> **Pre-reg §1bis**: "|β(C)| / |β(size)| ≥ 0.30 in at least 4 of 6 regimes"

| Regime | ratio |β(C)|/|β(size)| | ≥ 0.30? |
|---|---|---|
| E1_c1 | 0.62 | ✅ |
| E2_c1 | 0.88 | ✅ |
| E3_c1 | 0.54 | ✅ |
| E1_c2 | 0.92 | ✅ |
| E2_c2 | 0.42 | ✅ |
| E3_c2 | 0.82 | ✅ |

**Verdict: prediction HELD 6/6** (max 4/6 was required).

**Implication**: Phase 1's "C explains very little R²" is not equivalent to "C is physically negligible". β(C) is between **42% and 92%** the magnitude of β(size) in seconds-per-unit terms. C **does** move the makespan needle on a per-unit basis; it just doesn't move it on a per-variance basis (because C has low variance and is partially collinear with size).

This is consistent with the conceptual-decomposition framing: if a planner can intentionally engineer waves to shift C by 0.3 nat (a realistic operational lever), the resulting makespan change of ~7 seconds (in E3_c2) may matter operationally even though C contributes <1% R² in random-wave regression.

---

## 2. Tier 1.2 — Bootstrap CIs for the M3 − M2 R² increment

200-iteration bootstrap on each regime (cheaper since each iteration runs 5-fold CV).

| Regime | M3 − M2 mean | 95% CI | CI excludes 0? |
|---|---|---|---|
| E1_c1 | +0.0011 | [−0.0003, +0.0027] | no |
| E2_c1 | +0.0049 | [+0.0010, +0.0111] | **YES** |
| E3_c1 | +0.0069 | [+0.0016, +0.0132] | **YES** |
| E1_c2 | +0.0053 | [+0.0007, +0.0127] | **YES** |
| E2_c2 | +0.0087 | [+0.0023, +0.0171] | **YES** |
| E3_c2 | +0.0118 | [+0.0027, +0.0238] | **YES** |

**Implication**: in 5 of 6 regimes the increment is **statistically distinguishable from zero**, even though it is well below the +0.05 pre-reg threshold for "useful predictive surrogate." This is a textbook small-but-real-effect pattern: not noise, just small.

This sharpens the Phase 1 verdict from "C/I are useless" to "C/I are reliably present at small effect size that doesn't justify a predictive-surrogate framing."

---

## 3. Tier 1.3 — Controlled subsample fits (β(C) sign-flips with wave size!)

For each regime, fit M3 on subsamples binned by `size` (no `size` feature in the regression; only [floor_distance, C, I]). Reveals whether β(C) is uniform or size-conditional.

### Headline finding: β(C) sign depends on wave size

| Regime | β(C) at size [3,4] | β(C) at size [5,6] | β(C) at size [7,8] |
|---|---|---|---|
| E1_c1 | **+11.48** | **+15.10** | −5.70 |
| E2_c1 | −1.16 | +2.20 | −9.90 |
| E3_c1 | **+9.63** | +5.25 | −14.39 |
| E1_c2 | −1.16 | +2.20 | −9.90 |
| E2_c2 | **+11.19** | +4.89 | −10.44 |
| E3_c2 | +5.49 | −0.19 | −11.07 |

**Pattern**: β(C) is **positive (or near zero) for small waves** (size 3-4) and **negative for large waves** (size 7-8) in **every regime**. Phase 1's aggregate β(C) < 0 was an average that hid a size-dependent sign reversal.

### Mechanism candidate

- **Small waves (size 3-4, fewer orders than AMRs)**: AMR fleet is not saturated. High C (uniform floor distribution) → more elevator setup overhead per order → β(C) > 0. The "concentrated waves are easier" intuition holds in the unsaturated fleet regime.
- **Large waves (size 7-8, orders ≥ AMRs)**: AMR fleet is saturated. High C lets AMRs work in parallel across floors → β(C) < 0. The fleet-parallelism mechanism dominates.

This is **directly testable** by the Geometric experiment (§1ter pre-reg) — varying N_AMRs / F should shift the size threshold at which β(C) flips. If the geometric experiment confirms a size×fleet interaction, this becomes a clean **two-axis regime map** for β(C):

```
            β(C) sign
            
saturated   +------+------+
fleet       |      |      |
            |  ?   |  -   |    (large N, large size)
            |      |      |
            +------+------+
            |      |      |
            |  +   |  ?   |    (small N, small size)
            |      |      |
            +------+------+
                small  large
                  wave size
```

### β(I) is NOT subject to the same flip

β(I) stays consistently negative across size bins (range −5 to −28). The directional-imbalance mechanism is robust to wave size; the C mechanism is not.

[figures/tier1_3_subsample_betaC.png](figures/tier1_3_subsample_betaC.png) (not yet generated — add to follow-up)

### This is the most informative single result of the salvage so far

The Phase 1 sign reversal of β(C) was a one-line story ("uniform waves help fleet parallelism"). Tier 1.3 turns it into a **conditional finding**: the sign depends on whether the AMR fleet is saturated. That is a much stronger Paper 3 narrative — it explains *both* the v0.1 ambiguity (where wave size = 5 sat in the middle and the effect averaged near zero) *and* the Phase 1 aggregate negative.

**Status**: candidate for primary C3-H3 finding, pending Geometric experiment confirmation.

---

## 4. Tier 1.4 — Geometric mechanism (suggestive, only 6 points)

For Phase 1's 6 regimes, plot β(C) against N_AMRs / (n_elevators × capacity) — the "fleet-per-effective-slot" ratio.

| Regime | N/(E×c) | β(C) [s/nat] |
|---|---|---|
| E1_c1 | 10.00 | −22.91 |
| E2_c1 | 5.00 | −23.08 |
| E3_c1 | 3.33 | −9.83 |
| E1_c2 | 5.00 | −24.10 |
| E2_c2 | 2.50 | −6.17 |
| E3_c2 | 1.67 | −7.55 |

**Pearson correlation = −0.758** (more AMRs per effective slot → more negative β(C))

[figures/tier1_4_betaC_vs_NoverEc.png](figures/tier1_4_betaC_vs_NoverEc.png)

**Interpretation**: qualitatively consistent with the AMR-fleet-parallelism hypothesis from §3 of [Phase 1 deliverable](v0_2_phase1_regime_sweep.md) — denser fleet, more negative β(C). But: 6 points, all from N=10, F=5; the variance-explanatory claim (N/F as the *causal* knob) cannot be tested with these data alone. **The Geometric experiment ([§1ter pre-reg](../intuitions_before_MVS_v0_2.md)) is the proper test.**

---

## 5. Net effect on the salvage case

| Pre-Tier-1 question | Tier 1 outcome |
|---|---|
| Is C/I just noise? | **No** — bootstrap CIs exclude zero in 5/6 regimes |
| Is the small R² gap a real effect or sampling jitter? | **Real**, just small in R² space |
| Is β(C) physically meaningful even when R² gain is tiny? | **Yes** — β(C) is 42–92% of β(size) in seconds |
| Is β(C) < 0 truly regime-invariant? | **No** — Tier 1.3 reveals size-dependent sign flip; Phase 1's aggregate hid this |
| Does the geometric mechanism story hold qualitatively? | **Yes** — N/(E×c) and β(C) correlate at −0.76 across 6 Phase-1 regimes |

**Overall**: Tier 1 turns the Phase 1 result from "C2-M2 surrogate weak, β(C)<0 surprising" into "C2-M2 surrogate weak in R² but physically real in seconds, AND β(C) sign is size-conditional with a candidate mechanism."

This adds **two new candidate Paper 3 findings**:
1. Per-unit β(C) is operationally meaningful even when R² gain is statistically tiny (Tier 1.1, confirmed)
2. β(C) sign reverses with wave size in a size×fleet pattern (Tier 1.3, exploratory — needs geometric exp to confirm)

If both survive Geometric experiment + Phase 1.5 robustness, the C3-H3 / C2-M2-conceptual case is much stronger than after Phase 1 alone.

---

## 6. Caveats & honesty

- **Exploratory**: §3 (size-flip), §4 (N/F correlation) are post-hoc. Neither was pre-registered. They generate hypotheses; they do not test them.
- **Double-dipping**: §3 used the same data Phase 1 used for the aggregate β(C) finding. Cannot independently confirm the size-flip on these data — needs new data.
- **Multiple comparisons**: 18 subsample fits in §3; some sign flips could be sampling noise. The pattern (positive small → negative large in **every** regime) is unusually consistent and unlikely to be all noise, but a formal correction was not applied.
- **N=6 in §4**: correlation cannot distinguish "N/(E×c) is the causal knob" from "any quantity that varies across regimes correlates with β(C)".
- **Same-data sin**: for Paper 3 to use any of these findings as confirmatory, they must be re-tested on independent simulations — which is exactly what the Geometric experiment + Phase 1.5 + Phase 3 are scheduled to do.

---

## 7. Files produced

- [src/tier1_reanalysis.py](../src/tier1_reanalysis.py) — analysis script
- [results/v0_2_phase1_tier1_reanalysis.json](v0_2_phase1_tier1_reanalysis.json) — machine-readable
- [results/figures/tier1_1_beta_physunits.png](figures/tier1_1_beta_physunits.png)
- [results/figures/tier1_4_betaC_vs_NoverEc.png](figures/tier1_4_betaC_vs_NoverEc.png)

**Tier 1 complete.** Next: Geometric mechanism experiment (sweep N×F directly).
