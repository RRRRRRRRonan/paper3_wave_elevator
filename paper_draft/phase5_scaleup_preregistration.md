---
title: "Phase 5 — Pre-registration: publication-scale validation of §4 + §5"
parent: "Section 4 + Section 5 revision plan (D1/D2/D3 extension)"
plan: "tier1_execution_plan.md (successor)"
date: 2026-05-19
status: "LOCKED — author signed §10 (2026-05-19) after the §7 smoke passed"
---

# Phase 5 Pre-registration — publication-scale validation

> *Stage-gate discipline: this document fixes the design, gates, and stop
> rules. A 1/60-scale smoke test (§7) runs first; the full ~107k-sim grid is
> launched ONLY if the smoke gate passes and the author signs §10. Any
> post-hoc deviation is logged in §9.*

---

## 1. Why Phase 5 exists

Phase 4 v2 / H1 established the Bound-and-Gap framework and the Hedge Rule at
**prototype scale**: 3 regimes, fixed `F = 3`, fixed `|A| = 5`, sizes 4–8, 2
policies, uniform demand — 18 sub-cells. A Q1 *application-track* reviewer
will not accept a tactical-design claim validated on a single floor count and
a single demand process.

Phase 5 scales the validation to **publication scale** and, in doing so,
re-tests the three methodology extensions on a grid wide enough to be
credible:

- **D1** — SPO-regret equivalence of the policy-miss term `M_Phi`
  ([analysis_D1_spo_equivalence.py](../prototype/src/analysis_D1_spo_equivalence.py)).
- **D2** — Wasserstein-DRO / Hedge-Rule equivalence under chain dominance
  ([analysis_D2_wasserstein_dro.py](../prototype/src/analysis_D2_wasserstein_dro.py)).
- **D3** — *status change, see §1.1*.

### 1.1 D3 status — original claim withdrawn

The originally proposed D3 ("`H_up` is monotone along the model chain
`M_1 <= M_2 <= M_3`") **failed its smoke check 0/3** and the failure is
mechanistic, not a sample-size artefact: `H_up = (m_qmax - m_0)/m_0` is a
ratio whose numerator and denominator are inflated together by stochastic
dominance, so it is not order-preserving. The salvage search
([analysis_D3_chain_invariance.py](../prototype/src/analysis_D3_chain_invariance.py),
[v0_2_D3_chain_invariance.json](../prototype/results/v0_2_D3_chain_invariance.json))
tested seven candidate chain objects; **none holds in 3/3 regimes** at
prototype scale — but the corner-identity / ranking objects are confounded by
small-sample noise (raw corner spreads of 4–15 wave-time units against a
median makespan of 100–240, with 200-wave median SE ≈ 3–4 units).

**Decision**: D3 is *not* shipped as a theorem. The salvage data already
carries a usable result of the *opposite* sign — the corner ranking is
**model-dependent** (M2's co-occupancy physics reorders M1's corners, beyond
what small-sample noise explains). Model-sensitivity is itself an M4↔M5
coupling statement: *because* the Bound-and-Gap corner depends on which
elevator model is believed, the Model-Dominance Hedge Rule (M5) is
**necessary, not optional**. The corner-invariance question is therefore
demoted to an **exploratory (non-gating) hypothesis H-D3** (§3.3), re-tested
at scale where the noise floor is resolved. Both outcomes are usable: if H-D3
holds it returns as an *empirical* "model-robust diagnostic" result; if it
fails it confirms the model-sensitivity reading that motivates M5. Neither is
a proof, and §4 ships **D1 + D2 only** regardless.

---

## 2. Design

### 2.1 Warehouse-configuration factors

| Factor | Levels | Note |
|---|---|---|
| `F` floors | 3, 5, 8 | new — was fixed at 3 |
| `|A|` AMRs | 5, 15, 30 | new — was fixed at 5 |
| `E` elevators | 1, 2 | as Phase 4 |
| demand pattern | uniform, clustered, diurnal | new — `demand_patterns.py` |

Full factorial = 3·3·2·3 = 54 configurations. Phase 5 uses a **balanced 1/3
fraction = 18 configurations** via the defining relation
`demand_idx = (F_idx + |A|_idx) mod 3` crossed with both `E` levels; every
factor level is equi-represented (F / |A| / demand each 6×, E 9×). The array
is regenerated from `phase5_config.make_config_array()` into
`prototype/results/configs_v0_5.json` on every run; it stays tunable up to the
§10 sign-off, which locks it as the design object.

### 2.2 Three experiment blocks

| Block | Purpose | Grid | Sims |
|---|---|---|---|
| **A — decomposition** | D1 + D2 core; 72 sub-cells | 18 configs × {M1,M2} × {8,30} sizes × 5 arms × 200 waves | 72 000 |
| **B — policy comparison** | P0–P6, the 7-policy contest | 6 configs × {8,30} sizes × 7 policies × 200 waves | 16 800 |
| **C — model chain** | D2 ε-bound + H-D3 exploratory | 6 configs × {M1,M2,M3} matched-wave × size 16 × 5 arms × 200 waves | 18 000 |

**Total = 106 800 simulations.** "Sub-cell" (the unit of every gate below) =
one `(config, model, size)` triple; Block A has **72 sub-cells**, the
publication-scale replacement for the prototype's 18. Block B has no separate
arm axis — the seven wave-composition policies *are* the wave-design choice
(P5 = the Φ-corner), so they replace the arm dimension. Block C simulates each
drawn wave under all three models (matched-wave) so per-wave dominance is
measurable.

Block B's 6 configs and Block C's 6 configs are the first six `E = 2` rows of
the 18-config array (where policy and co-occupancy effects are visible).

### 2.3 Arms (Blocks A & C — same corner scheme as Phase 4 v2)

`random` (pool) + 4 quartile corners `{HC_HI, HC_LI, LC_HI, LC_LI}` on
`Phi = (C, I)`. Blocks A and C use these 5 arms; Block B has no arm axis — its
7 policies are themselves the wave-design choice (see §2.2 / §2.4).

### 2.4 The seven policies (Block B)

The seven P0–P6 are *wave-composition* policies (which orders to release
together), distinct from the Phase 4 H1 operational dispatch policies; Phase 5
holds operational dispatch fixed. Each policy selects waves from a shared
candidate pool, so the contest is fair. All seven are implemented in
`wave_policies.py` (single flat module with a `POLICIES` registry).

| Id | Wave-composition rule |
|---|---|
| P0 | random sample (baseline) |
| P1 | destination-clustered — low destination spread |
| P2 | cardinality-only — low cross-floor count |
| P3 | direction-balanced — low directional imbalance `I` |
| P4 | temporal-clustered — low temporal CV `T` |
| P5 | Φ-informed — the Φ-favourable (C, I) corner (this paper's method) |
| P6 | SPO-Tree — lowest cell-mean predicted makespan |

P6 is the load-bearing contrast: a partition-constant predictor fitted with
the SPO-Tree *cell-mean* rule, against which P5's cell-median Φ rule must be
shown to differ (D1 §4.1.2 discussion).

### 2.5 Sample size & seeds

200 waves per `(sub-cell, arm)` (Blocks A/C) or `(config, size, policy)`
(Block B). Seeds are deterministic per cell (no `hash()` of strings — see
`experiments_phase5._seed`), so every run is reproducible. Within a Block B
`(config, size)` all 7 policies select from one shared candidate pool; in
Block C all 3 models simulate the same drawn waves (matched-wave).

---

## 3. Pre-registered hypotheses and gates

All gates evaluate over Block A's 72 sub-cells unless stated. `m_0` is the
random-pool median makespan of the sub-cell.

### 3.1 H-D1 — decomposition holds at scale (confirmatory)

| Gate | Criterion |
|---|---|
| D1-a | `GAP = H_up + M_Phi` exact (< 1e-9) in **72/72** |
| D1-b | `H_up >= 0` and `M_Phi >= 0` in **72/72** |
| D1-c | `M_Phi == SPO_regret(Phi)` exact in **72/72** |
| D1-d | 95 % bootstrap CI on `GAP` excludes 0 in **≥ 58/72 (≥ 80 %)** |

D1-a/b/c are algebraic and expected to pass trivially; **D1-d is the real
test** — it asks whether the decomposition still resolves signal once `F` and
`|A|` vary.

### 3.2 H-D2 — chain dominance and ε-bound (confirmatory)

| Gate | Criterion |
|---|---|
| D2-a | per-wave `M2 >= M1` ≥ 90 % averaged over Block C cells; ≥ 80 % worst cell |
| D2-b | FOSD `M1 <= M2` (quantile coupling) in ≥ 90 % of Block C cells |
| D2-c | one-sided `U_c(0.05) < 5 % · m_0` in ≥ 80 % of Block C cells |
| D2-d | DRO worst case == Hedge value, and `c*_DRO == c*_Hedge`, per regime |

### 3.3 H-D3 — corner-invariance (EXPLORATORY, non-gating)

Re-test on Block C (`M1, M2, M3`, size 16, 6 configs):

| Probe | Reported metric |
|---|---|
| worst/best corner identity invariant across M1/M2/M3 | fraction of configs |
| corner-ranking Spearman ρ vs M1 | mean ρ, with bootstrap CI |

**H-D3 does not gate the paper.** Pre-committed reading — both branches yield
a usable §5 result, decided before the scale-up data is seen:
- **invariant** — corner identity invariant in ≥ 90 % of configs **and** mean
  ρ ≥ 0.8 with bootstrap CI excluding 0 → empirical "model-robust diagnostic"
  subsection in §5.
- **sensitive** (the mechanistically more likely branch) — confirms a
  **model-sensitive** diagnostic, written up as the motivating observation
  for the Hedge Rule (M5): the wave-design corner depends on the believed
  elevator model, so M5's model-robust selection is necessary. This is a §5
  coupling result, **not** a §6 limitation.

No theorem is claimed in either branch; §4 ships D1 + D2 only.

### 3.4 H-Policy — the 7-policy contest (confirmatory, Block B)

Let a sub-cell "favour P5" if P5's Φ-informed median makespan is strictly
below the comparator's.

| Band | Criterion |
|---|---|
| Policy-Strong | P5 beats P0 in ≥ 90 %, beats P1 in ≥ 60 %, beats P6 in ≥ 50 % |
| Policy-Partial | P5 beats P0 in ≥ 75 %, beats P1 in ≥ 50 % |
| Policy-Weak | P5 fails to beat P0 in ≥ 75 % of cells |

The **P5-vs-P6** comparison is the D1 differentiator: it tests whether the
cell-median Φ rule actually outperforms the SPO-Tree cell-mean rule on the
heavy-tailed simulator makespan.

---

## 4. Outcome handling (locked pre-run)

| Outcome | Paper action |
|---|---|
| **H-D1 pass + H-D2 pass + Policy-Strong** | §4 ships D1+D2 as scaled-and-confirmed; §5 reports the 72-sub-cell grid as the primary validation table; acceptance estimate moves toward the upper band. |
| **H-D1 pass + H-D2 pass + Policy-Partial** | Same §4; §5 reports P5's advantage as regime-conditional (mirrors the H1 PARTIAL re-interpretation). |
| **H-D1-d fails (< 80 %)** | The decomposition does not resolve signal at scale → honest §8 limitation: "Bound-and-Gap is a prototype-regime diagnostic"; D1 stays (it is algebraic) but the empirical-utility claim is softened. |
| **Policy-Weak** | P5 does not beat a naive baseline at scale → narrative pivot, pre-written: the contribution is the *diagnostic decomposition*, not a competitive policy. Do not re-tune P5 to rescue the gate. |
| **H-D3 invariant branch** | "model-robust diagnostic" empirical subsection in §5. |
| **H-D3 sensitive branch** | model-sensitivity confirmed → written as the §5 motivation for M5, **not** a §6 limitation. |

**Disallowed under every outcome**: dropping configs to reach a gate;
re-running with new policy rules to "find" a win; switching `M_Phi` back to
cell-mean to flatter P5 vs P6; moving the 80 % / 90 % bars.

---

## 5. Simulator extensions (built — W1–W3, before this sign-off)

No core rewrite. `simulator.py` already parameterises `F`, `|A|`, `E`, wave
size. Two additions, both built and unit-tested before this sign-off:

1. **`demand_patterns.py`** — `generate_uniform`, `generate_clustered`
   (20 % hot (s,d) pairs carry 80 % mass), `generate_diurnal` (peak/off-peak
   release times; `time_horizon = 50 s`, smoke-calibrated down from 120 s).
   Degenerate parameters reduce clustered / diurnal to uniform.
2. **`wave_policies.py`** — P0–P6 as one flat module with a `POLICIES`
   registry and shared candidate-pool / corner / predictor-fit helpers.

Folder layout stays **flat** under `prototype/src/` with the established
`analysis_*` / `experiments_*` naming plus `demand_patterns.py`,
`wave_policies.py`, `phase5_config.py`, `experiments_phase5.py` — no
sub-package, to avoid breaking the relative-path links already in
[theorems_m4.md](theorems_m4.md), [theorems_m5.md](theorems_m5.md) and
[methodology_v0_2.md](methodology_v0_2.md).

---

## 6. Planned analyses

1. **Table 1** — 72-sub-cell Block A decomposition: `H_up`, `M_Phi`, `GAP`,
   95 % CI, SPO-regret check. Reuses [analysis_D1_spo_equivalence.py](../prototype/src/analysis_D1_spo_equivalence.py)
   with the wider CSV.
2. **Table 2** — Block C chain: per-wave dominance, `U_c(0.05)`, DRO==Hedge.
3. **Table 3** — Block B 7-policy contest: win-fraction matrix P0–P6.
4. **Figure 1** — `GAP` vs `(F, |A|)` heatmap, faceted by demand pattern.
5. **Figure 2** — P5-vs-P6 paired makespan scatter (the D1 differentiator).

## 7. Smoke test — the stage-gate (runs FIRST)

**1/60-scale slice ≈ 1 020 sims**: 3 configs (one per demand pattern) ×
{M1,M2} × size 8 × 5 arms × 20 waves (Block A slice, 600) + 3 configs × 7
policies × size 8 × 20 waves (Block B slice, 420).

**Smoke gate — PROCEED only if all hold:**

| Check | Pass condition |
|---|---|
| S1 decomposition non-degenerate | `GAP > 0` in ≥ 2/3 smoke configs |
| S2 dominance direction | median(batched) ≥ median(abstraction) in ≥ 80 % of (config, arm) cells (distributional proxy; the per-wave gate D2-a runs on matched-wave Block C) |
| S3 policy direction | P5 median makespan ≤ P0 median in ≥ 2/3 configs |
| S4 demand patterns bite | clustered or diurnal differs from uniform median makespan by ≥ 3 % |

If **any** of S1–S4 fails → **STOP at the smoke**. This is a legitimate
pre-reg pivot, not a suppressed result: revise the failing component
(decomposition partition, policy spec, or demand generator) and re-smoke
before the full run. Do not launch the 107k-sim grid on a failed smoke.

## 8. Stop rules

1. Smoke gate fails (§7) → stop, revise, re-smoke. Do not launch full run.
2. Smoke passes + author signs §10 → launch Block A, then B, then C.
3. Full run, H-D1-d fails → §4.3 outcome handling; **do not** add cells to rescue.
4. Full run, Policy-Weak → narrative pivot (§4); **do not** re-tune P5.
5. Wall-clock: if the full run exceeds 2× its estimated runtime, checkpoint
   and analyse Block A alone — it carries the D1/D2 confirmatory load.

## 9. Surprise-log hook

Log to [intuitions_before_MVS_v0_2.md](../prototype/intuitions_before_MVS_v0_2.md)
if: `GAP` decreases with `F` (more floors, less wave signal — counter-intuitive);
P6 (SPO-Tree cell-mean) beats P5 (cell-median) in ≥ 50 % of cells (would
invalidate the D1 §4.1.2 cell-median argument); diurnal demand inverts the
corner ranking vs uniform.

## 9.1 Amendment 1 — ablations + P7 optimization baseline (2026-05-19)

Logged the same day as the §10 sign-off, **before the W6 confirmatory
analysis**. The author requested a strengthened design after signing; because
no confirmatory result had yet been computed, this is legitimate design
strengthening, not goalpost-moving. The amendment **adds** analyses and
**touches none of the locked H-D1 / H-D2 / H-Policy gates or thresholds**.

**Added.** (a) **P7** — a local-search wave-composition optimizer
([experiments_phase5_ablation.py](../prototype/src/experiments_phase5_ablation.py),
modest 40-iteration budget), the "how close to optimal" reference the
feature-based policies P0–P6 lacked. (b) **Four ablations A1–A4**
([analysis_phase5_ablation.py](../prototype/src/analysis_phase5_ablation.py) →
[v0_5_phase5_ablation.json](../prototype/results/v0_5_phase5_ablation.json)).
The originally-listed fifth ablation (β-sign corner vs OLS-argmin corner)
collapses — for a linear OLS fit the two pick the same corner identically, and
the β-sign-vs-nonlinear-predictor question is already the P5-vs-P6 contest.

**Findings — recorded before W6, reported as-is (favourable or not):**

| # | Ablation | Result |
|---|---|---|
| A1 | Φ=(C,I) vs C-only / I-only | mean makespan reduction 3.7 % / 2.7 % / 1.1 %; (C,I) beats *both* singles in only 39/72 cells → **C is the dominant feature, I a weak secondary**; (C,I) is best on average, not universally. |
| A2 | T dimension: 2×2 (C,I) vs 2×2×2 (C,I,T) | T adds corner leverage in 1/6 configs (1/2 diurnal) → **T is a weak lever**, marginal even under diurnal demand. |
| A3 | estimator: cell-median vs cell-mean GAP | cell-mean GAP is the **more** stable estimator (bootstrap SD 0.015 vs 0.021, 71/72 cells). The cell-median's robustness rationale proposed for §4 is **not supported**; the median is retained only for consistency with Theorem 1 (the SPO-regret equivalence is stated for it). The planned "median is consistent and robust" sentence must NOT be used; justify the median by Theorem-1 consistency instead. |
| A4 | granularity: 2×2 vs 3×3 (C,I) | 3×3 raises UB in 6/6 configs (mean UB 0.086 → 0.128) → **confirms Corollary M4.4** (refinement monotonicity) at publication scale. |

**P7 reference.** P5 (Φ-informed) sits **46.4 % above** the P7 local-search
optimum and captures only **19.0 %** of the P0→P7 improvement gap. P5 beats the
naive P0 but is far from optimal — consistent with the paper's framing that the
contribution is the **diagnostic decomposition**, not P5 as a competitive
policy (the §4 "Policy-Weak" handling row anticipates exactly this).

**Consequences.** A3 forbids the planned median-robustness sentence (use
Theorem-1 consistency instead). P7 and A1/A2 inform — but do not change — the
W6 H-Policy interpretation. The §3 gates and §4 outcome rules stand exactly as
signed in §10.

## 9.2 Amendment 2 — supplementary publication-scale experiments for C3 (2026-05-19)

Logged after the W6 confirmatory analysis. C3's three managerial outcomes
(the regime diagnostic, the Hedge Rule's reach beyond `c = 2`, the
substitutability map) were demonstrated at **prototype scale** (Phase 4:
`F = 3`, `|A| = 5`). To match the publication-scale validation of C2
(Blocks A/C), two supplementary experiments are pre-registered here and run
against the gates below. They are **new experiments**, not re-runs of any
locked H-D1/H-D2/H-Policy gate; design and gates are fixed in this subsection
**before** the supplementary run, and results are reported as-is.

**Supp-1 — H1 at publication scale (C3-1, C3-3).** Operational dispatch P0
(FIFO) vs P1 (destination-clustered) across the 6 `E = 2` configs × {8, 30}
sizes × {random, Φ-corner} arms × M2 (batched) × 200 matched waves. Marginal
value `MV = (median T_P0 − median T_P1) / median T_P0`.
- **Supp1-a**: `Pearson(H_up, MV) < 0` on the Φ-corner arm — high
  partition-headroom configs benefit more from clustering (replicates the
  prototype −0.67).
- **Supp1-b**: `MV` is regime-conditional — `MV > 1 %` in a strict subset of
  cells and ≈ 0 elsewhere, not uniform.

**Supp-2 — capacity sweep (C3-2).** Matched-wave M1/M2 across the 6 `E = 2`
configs × `c ∈ {2,3,4,5}` × 5 corner arms × size 16 × 200 waves.
- **Supp2-a**: per-wave `M2 ≥ M1` ≥ 90 % averaged and ≥ 80 % worst cell, at
  **each** `c ∈ {3,4,5}` (the capacities beyond the `c = 2` derivation).

**Honest pre-statement.** These supplements give C3 publication-scale
evidence; they do **not** guarantee a stronger C3 — the prototype H1 was
regime-conditional (2/6), and a regime-conditional result at scale is the
expected and acceptable outcome. Whatever the gates return is reported.

**§9.2-R Results** ([v0_5_phase5_supp.json](../prototype/results/v0_5_phase5_supp.json),
run 2026-05-19 against the gates above).

*Supp-2 (C3-2) — PASS.* Per-wave `M2 ≥ M1` is ≥ 99.7 % averaged and ≥ 98 %
worst-cell at **every** `c ∈ {2,3,4,5}`. Supp2-a met: the Hedge Rule's
chain-dominance condition holds at capacities beyond its `c = 2` derivation —
**confirmed at publication scale**. C3-2 stands as stated.

*Supp-1 (C3-1, C3-3) — PARTIAL, with a paradigm correction.* Supp1-a met
weakly (`Pearson(H_up, MV) = −0.11`); Supp1-b **fails** — destination-clustered
dispatch lowers makespan by `MV > 1 %` in **12/12** cells (mean
`MV = +10.2 %`), not in a regime-conditional subset. Honest reading: **at
publication scale, destination-clustered dispatch delivers a broad ~10 %
makespan reduction; it is not regime-conditional.** The prototype H1's
regime-conditionality (2/6 cells, `Pearson = −0.67`) was a small-floor-count
(`F = 3`) artefact — with `F ∈ {3,5,8}` there is enough destination spread for
clustering to help everywhere. **Consequence**: C3-1 ("prospectively
classifies which regimes benefit") and C3-3 ("regime-conditional
substitutability map") do **not** replicate at scale and must be reframed; the
broad +10 % value is itself a stronger result for "structured dispatch has
value." C2-M4's diagnostic remains valid as a *structural decomposition*
(H_up vs M_Φ) but not as a sharp *regime classifier*. Logged here before §5 is
drafted.

## 10. Author sign-off

```
Design (§2) reviewed and locked:            [x]  shiyuehu      date 2026-05-19
Gates (§3) and stop rules (§8) accepted:     [x]  shiyuehu      date 2026-05-19
configs_v0_5.json frozen:                    [x]  shiyuehu      date 2026-05-19
Smoke gate (§7) verdict:        PASS         [x]  shiyuehu      date 2026-05-19
Full-run authorisation:                      [x]  shiyuehu      date 2026-05-19
```

*Signed by the lead author (shiyuehu) on 2026-05-19, recorded by the assistant
per the author's explicit instruction. Smoke verdict:
[v0_5_phase5_smoke_verdict.json](../prototype/results/v0_5_phase5_smoke_verdict.json)
— PROCEED, S1–S4 all pass. From this point the design is frozen; any deviation
is logged in §9.*

---

## Appendix — workflow & status

| Step | Output | Status |
|---|---|---|
| W1 | `demand_patterns.py` + unit tests | done |
| W2 | `wave_policies.py` P0–P6 + self-tests | done |
| W3 | `experiments_phase5.py` + `phase5_config.py` + draft `configs_v0_5.json` | done |
| W4 | smoke run (§7) + smoke verdict report | done — PROCEED |
| **GATE** | **author signs §10** | **done 2026-05-19** |
| W5 | full run, ~107k sims (smoke-calibrated estimate: minutes, not hours) | authorised |
| W6 | Tables 1–3, Figures 1–2, `v0_5_phase5.md` deliverable | pending |

`§4` code is **already done**: D1/D2 verified ([v0_2_D1_spo_equivalence.json](../prototype/results/v0_2_D1_spo_equivalence.json),
[v0_2_D2_wasserstein_dro.json](../prototype/results/v0_2_D2_wasserstein_dro.json));
the cell-median estimator the audit flagged was already in place. Phase 5 is
the §5 scale-up plus the SPO-Tree baseline that D1's discussion needs.

---

**Pre-registration LOCKED 2026-05-19 — author signed §10 after the §7 smoke
passed (PROCEED). The full run is hereby authorised; it precedes any §5 table
in the paper. Post-hoc deviations from this point are logged in §9.**
