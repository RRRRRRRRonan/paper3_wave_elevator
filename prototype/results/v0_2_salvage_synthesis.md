# MVS v0.2 — Salvage synthesis (Tier 1 + Geometric + Phase 1.5)

**Date**: 2026-04-21
**Pre-registration**: [intuitions_before_MVS_v0_2.md](../intuitions_before_MVS_v0_2.md) §0bis, §1, §1bis, §1ter
**Deliverables covered**:
1. [results/v0_2_phase1_tier1_reanalysis.md](v0_2_phase1_tier1_reanalysis.md)
2. [results/v0_2_geometric_mechanism.md](v0_2_geometric_mechanism.md)
3. [results/v0_2_phase1_5_true_batching.md](v0_2_phase1_5_true_batching.md)

---

## 1. What we asked, what we got

The salvage was triggered by Phase 1's negative decision-gate outcome (max `M3 − M2` = +0.0121, threshold +0.05). Three tracks were run in parallel to see whether the negative was avoidable or informative.

| Track | Specific question | Answer |
|---|---|---|
| **Tier 1** (no new data) | Is the small M3−M2 gap just noise? Is β(C) robust? | **Real but small** (5/6 bootstrap CIs exclude 0); β(C) is 42–92% of β(size) in physical units. **Novel finding**: β(C) sign reverses within each regime across size bands (3-4 → positive, 7-8 → negative). |
| **Geometric** (pre-registered) | Does N/F ratio control β(C) sign, as Tier 1.4 suggested? | **NO.** Pearson r = −0.15 across 20 cells (threshold −0.70). The Tier-1.4 correlation was a 6-point one-axis artefact. |
| **Phase 1.5** (pre-registered) | Does true batching rescue the predictive-surrogate framing? Is the Phase 1 β(C)<0 robust? | **NO** (M3−M2 = +0.0119, effectively unchanged) and **NO** (β(C) flips sign in 2/3 c=2 regimes, bootstrap CIs straddle 0 under batching). |

Net: two failed rescues + one genuine new finding from Tier 1.3. The Phase 1 story is smaller than it looked.

---

## 2. Paper 3 contribution status (consolidated)

| Contribution | Status before salvage | Status after salvage | Reason for change |
|---|---|---|---|
| C1 problem formulation | 🟢 | 🟢 | Unaffected |
| C2-M1 three-dim feature family | 🟢 | 🟢 | Unaffected |
| **C2-M2 as predictive surrogate** | 🟡 proposed | ❌ **FINAL REJECTED** | Neither better data (Phase 1) nor better simulator (Phase 1.5) raises M3−M2 above +0.02 |
| C2-M2-conceptual (Φ as decomposition) | 🟡 implicit | 🟢 confirmed | Tier 1.1: β magnitudes are physically real (42–92% of β(size)); model-invariant |
| C2-M3 simulator methodology | 🟢 | 🟢 (strengthened) | Phase 1.5 itself is a model-comparison contribution — documents that throughput-abstraction is optimistic by ~30% of median makespan |
| C3-H1 Φ ↔ workflow mapping | 🟢 | 🟢 | Unaffected |
| C3-H2 variance-vs-mean distinction | 🟢 | 🟢 | Strengthened by Tier 1.1 (small R² effect but real per-unit) |
| **C3-H3 β(C)<0 counterintuitive finding** | 🟡 predicted + | 🔴 **model-dependent** | Phase 1.5 shows sign flip under true batching; Geometric shows no simple geometric explanation |

**Short version for abstract**: the methodology contributions (C1, C2-M1, C2-M2-conceptual, C2-M3, C3-H1, C3-H2) are intact. The one "surprising insight" contribution (C3-H3) has to be reframed as a model-dependence observation rather than a clean counterintuitive finding.

---

## 3. What survives as a Paper 3 headline

Three survivors, ranked by strength:

### 3.1 Φ is a conceptually-useful decomposition of wave structure (strong)

Evidence: Tier 1.1 physical-unit β coefficients. Under throughput-abstraction, β(C) ∈ [−24, −7] s/nat across 6 regimes with bootstrap CIs excluding zero in 4/6. Under true batching, β(C) straddles zero but remains non-trivial in magnitude. The *decomposition itself* (C, I, T as orthogonal-ish wave descriptors) is model-invariant because it's a property of the wave, not the elevator. Use Φ as a **diagnostic framework for wave design**, not as a predictive model.

### 3.2 Throughput-abstraction is optimistic — and how much matters (strong, new)

Evidence: Phase 1.5 paired comparison. True batching produces makespans 25–47 s higher (median) than the throughput-abstraction elevator on the same waves; 86–95% of individual waves are slower under batching. Pearson r ∈ [0.85, 0.93] shows **rank order is preserved** across models but **magnitude and decomposition are not**. This is a methodology contribution: if you care about β coefficients or mean makespan, the choice of elevator model matters; if you only care about comparative wave ranking, throughput-abstraction is fine.

### 3.3 β(C) sign is a probe of the fleet–elevator interaction regime (moderate, new)

Evidence: combined Tier 1.3 + Geometric + Phase 1.5. β(C) is:
- **Positive** in small-wave / batched / small-fleet regimes (batching loss dominates; concentrated waves enable parallel trips)
- **Negative** in large-wave / abstraction / large-fleet regimes (fleet parallelism dominates; spread-out waves utilise more AMRs)

This is not a clean mechanism but it is an empirical pattern. Reframe C3-H3 as: *"β(C) is a diagnostic of whether the system is batching-limited or parallelism-limited"* rather than *"concentrated waves are faster"*. More modest, but more defensible and arguably more useful.

---

## 4. What dies

- **"β(C) < 0 is a counterintuitive discovery"** — dies as a headline. It was an artefact of the throughput-abstraction × N=10 × F=5 cell we happened to sweep in Phase 1.
- **"Φ predicts makespan better than size alone"** — dies as a predictive-surrogate claim. Gap is +0.0119 R² at best under either elevator model.
- **"N/F ratio is a causal knob for β(C)"** — dies flat. Pearson −0.15 across 20 cells.

---

## 5. What to do next (post-salvage v0.2 plan)

Given the salvage outcome:

1. **Drop v0.2 Phase 4 as originally scoped.** Arm B's "good wave" criterion was defined around β(C)<0 holding robustly; it doesn't. A redesigned Phase 4 needs a new criterion (and new pre-reg).
2. **Phase 2 (T experiment)** can still run — it tests an independent hypothesis (temporal clustering → makespan) that is not entangled with the C3-H3 collapse.
3. **Phase 3 (stochastic robustness)** is lower priority now: with the main finding already known to be model-dependent, adding AMR speed noise tests a different kind of robustness that is no longer the critical path.
4. **A size × N sweep under true batching** (a "Geometric-2" experiment, §6.3 of Phase 1.5 deliverable) would be the proper test of the surviving candidate mechanism (Tier 1.3's size × fleet hypothesis). **Not in v0.2 budget**; defer to a v0.3 decision.

Recommended next concrete action: **write a Paper-3 reframing memo** that encodes §3's three survivors and §4's three deaths, so the paper's spine is rebuilt on the salvaged evidence before spending more simulation budget.

---

## 6. Files produced in the salvage

Scripts (in [src/](../src/)):
- `tier1_reanalysis.py`
- `experiments_geometry.py`
- `simulator.py` (refactor — added `ElevatorBatched`, `ElevatorPoolBatched`, `batched=` flag)
- `experiments_phase1_5.py`
- `analysis_phase1_5.py`

Deliverables (in [results/](.)):
- `v0_2_phase1_tier1_reanalysis.md` + JSON
- `v0_2_geometric_mechanism.md` + JSON
- `v0_2_phase1_5_true_batching.md` + JSON
- `v0_2_salvage_synthesis.md` (this file)

Figures (in [figures/](figures/)):
- `tier1_1_beta_physunits.png`, `tier1_4_betaC_vs_NoverEc.png`
- `geometry_heatmaps.png`, `geometry_betaC_vs_NoverF.png`
- `phase1_5_paired_makespan.png`, `phase1_5_betaC_comparison.png`

Raw data (in [raw/](raw/)):
- `mvs_v0_2_phase1_samples.csv` (6000 rows — Phase 1)
- `mvs_v0_2_geometry_samples.csv` (20000 rows — Geometric)
- `mvs_v0_2_phase1_5_batched_samples.csv` (3000 rows — Phase 1.5)

---

**Salvage complete.** Two headline findings (Surprises #11, #12) logged in [intuitions_before_MVS_v0_2.md §7](../intuitions_before_MVS_v0_2.md). Paper 3 spine needs reframing before further simulation work.
