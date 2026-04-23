---
title: "Phase 4 H1 — Pre-registration: Tactical marginal value under strong operational layer"
parent: "Tier 1, Task A"
plan: "tier1_execution_plan.md"
models_after: "prototype/intuitions_before_MVS_v0_2.md §4bis"
date: 2026-04-22
status: "LOCKED before any simulation runs"
---

# Phase 4 H1 Pre-registration

> *This document is locked before any Phase 4 H1 simulation runs. Thresholds, handling, and narrative pivots are all fixed here. Any post-hoc deviation must be logged in §9 Surprise-log hook with explicit justification.*

---

## 1. What H1 tests and why

**The question a Q1 reviewer will ask**:
> *"Your Phase 4 v2 showed Φ-informed wave design beats random by 1.3–7.4 %. But your simulator uses a simple dispatch policy. If I put a **good** operational optimiser downstream, does the 1.3–7.4 % survive? Or does it get absorbed by smarter operations?"*

**Our answer framework**:
- Define two operational policies: **P0** (current simulator, FIFO-like) and **P1** (destination-clustered elevator batching, a concrete "strong ops" heuristic).
- Measure tactical marginal value under each.
- Compare: does the marginal value **under P1** survive the pre-registered thresholds?

**What this resolves**:
- If P1-marginal is still meaningful → *tactical layer is a genuine lever* even with better operations. C3-C gets a first-class finding.
- If P1-marginal is substantially eroded → *tactical is largely absorbed*. Narrative pivots to "tactical matters in regimes where ops cannot fully exploit wave structure" — honest, publishable, but different framing.

**What H1 does NOT test**:
- Optimal ops (no MILP). P1 is "a credibly strong heuristic", not provably optimal. This matches Wu 2024 / Keung 2023 precedent.
- Real warehouse data (L7, permanently out of scope for v0.4).

---

## 2. Design

### 2.1 Cells (same as Phase 4 v2)

- **Regimes**: E ∈ {1, 2, 3} × c = 2 → 3 regimes
- **Elevator models**: {M1 (abstraction), M2 (batched)} → 2 models
- **Cell** = (regime, model). **6 cells** total.
- **Sizes**: {4, 6, 8} within each cell.

### 2.2 Operational policies

| Name | Rule | Where to implement |
|---|---|---|
| **P0** | Current simulator — elevator serves AMRs in queue-arrival order, batches up to $c$ FIFO | Unchanged from current [simulator.py](../prototype/src/simulator.py) |
| **P1** | Destination-clustered batching — at each dispatch event, pick $c$ AMRs from the waiting queue that minimise max destination spread; dispatch 1 alone if only 1 is waiting (no artificial hold-off) | New method `.pop_cluster(c)` on `ElevatorBatched` class |

**P1 is the pre-registered "strong operational layer" heuristic.** It represents what an elevator-scheduling module with near-zero additional infrastructure cost could realistically do.

**Why P1 and not an MILP**: reviewers for C&IE accept credible heuristics; MILP introduces scaling anxieties that distract from the tactical-layer claim. Wu 2024 (Processes) used heuristic ops for the same reason.

### 2.3 Wave arms

| Name | Rule | Same as Phase 4 v2? |
|---|---|---|
| **Arm A** | Random waves (pool) | Yes |
| **Arm B** | Φ-informed corner wave: sign($\beta_C$), sign($\beta_I$) from each cell's own OLS fit picks the quartile corner | Yes |

Using identical arms as Phase 4 v2 enables side-by-side comparison and reuse of the corner-selection logic.

### 2.4 Sample size

- **200 waves per (cell, size, ops, arm)**. Matches Phase 4 v2 per-arm-sample.
- **6 cells × 3 sizes × 2 ops × 2 arms × 200 waves = 14 400 simulations**.
- Seeds: reuse Phase 4 v2 seed structure `2026 + size` for reproducibility of the Arm A / B pools; P0 vs P1 runs on identical waves (paired comparison).

### 2.5 Primary metric

For each (cell, size, ops), let $\tilde{T}^{\mathrm{ops}}_A$ and $\tilde{T}^{\mathrm{ops}}_B$ be the median makespan under arm A and B respectively.

**Marginal value under ops**:
$$\mathrm{MV}^{\mathrm{ops}}(\text{cell, size}) = \frac{\tilde{T}^{\mathrm{ops}}_A - \tilde{T}^{\mathrm{ops}}_B}{\tilde{T}^{\mathrm{ops}}_A}$$

**Absorption ratio** (diagnostic, not gate):
$$\mathrm{Abs}(\text{cell, size}) = \frac{\mathrm{MV}^{\mathrm{P0}} - \mathrm{MV}^{\mathrm{P1}}}{\mathrm{MV}^{\mathrm{P0}}}$$

Averaging across the 3 sizes per cell yields a cell-level $\mathrm{MV}^{\mathrm{P1}}$ (the threshold gate target).

---

## 3. Pre-registered thresholds

### 3.1 Primary gate — marginal value under strong ops (P1)

| Band | Criterion | Probability estimate (v1, 2026-04-22) | Probability estimate (v2, **corrected** 2026-04-22) |
|---|---|---|---|
| **Strong** | $\mathrm{MV}^{\mathrm{P1}} \ge 10\%$ in ≥ 4 / 6 cells | 20 % | **≤ 5 %** |
| **Moderate** | $\mathrm{MV}^{\mathrm{P1}} \ge 5\%$ in ≥ 4 / 6 cells | 45 % | **20–25 %** |
| **Suggestive** | $\mathrm{MV}^{\mathrm{P1}} \ge 3\%$ in ≥ 4 / 6 cells | 20 % | **30–35 %** |
| **Reject** | $\mathrm{MV}^{\mathrm{P1}} < 2\%$ in ≥ 4 / 6 cells | 15 % | **30–40 %** |

**Basis for corrected (v2) probability estimates**:
- Phase 4 v2 Option 1 cell-average MV under P0: `[+2.3, +1.3, +2.1, +5.4, +7.4, +5.5]` %. Count at each threshold (P0 baseline): **3/6 at ≥ 3 %**, **3/6 at ≥ 5 %**, **0/6 at ≥ 10 %**.
- P1 = destination-clustered batching. Mechanism: P1 reduces per-trip vertical travel more on Arm A (scattered destinations) than Arm B (already concentrated). Therefore $\mathrm{MV}^{\mathrm{P1}} < \mathrm{MV}^{\mathrm{P0}}$ in expectation — P1 **shrinks** the tactical lever, does not amplify it.
- First-order magnitude: P1 likely reduces Arm A by 2–4 % and Arm B by 0.5–1.5 %, yielding a 1–3 percentage-point drop in MV.
- Cell-level projection: `[~0.5–1.5, ~0–1, ~0–1.5, ~3.5–4.5, ~5–6, ~3.5–4.5]` %. This gives ~1–3/6 cells at ≥ 3 % and ~1–2/6 at ≥ 5 %, making **Suggestive or Reject** the modal outcomes (combined ~65–75 %).
- v1 estimate (Moderate 45 %) was made before this baseline check and was wrong-directionally optimistic.

**What this changes — and does not change**:
- **Unchanged**: thresholds (§3.1 criteria column), handling (§4), stop rules, paper-level pivots for each outcome. All LOCKED as originally pre-registered.
- **Changed**: only the pre-run subjective belief about which band is most likely. Transparency here reduces the risk of post-hoc rationalisation and preserves the integrity of the pre-reg.

### 3.2 Secondary gate — absorption ratio (interpretive)

| Band | Criterion | Interpretation |
|---|---|---|
| **Robust-to-ops** | Abs < 30 % in ≥ 4 / 6 cells | Tactical is largely orthogonal to ops quality |
| **Partly-substitutable** | 30 % ≤ Abs < 60 % in ≥ 4 / 6 cells | Tactical and ops both help; partially redundant |
| **Absorbed** | Abs ≥ 60 % in ≥ 4 / 6 cells | Ops eats most tactical value |

Absorption drives the *narrative framing*, not the paper-accept/reject decision — that's entirely on §3.1.

### 3.3 Confidence (bootstrap)

- 1000-iteration bootstrap on per-cell MV using within-arm resampling (same technique as R1).
- Pre-reg: report per-cell 95 % CI on MV^P1 and flag cells where CI excludes 0.
- **Additional gate**: in ≥ 4 / 6 cells, the MV^P1 95 % CI must exclude 0. This prevents a weak "suggestive" band from sneaking through on point estimates alone.

---

## 4. Outcome handling (locked pre-run)

### 4.1 Strong

**Paper actions**:
1. Push TR-E to primary alternate (from "reach").
2. Abstract gains a bullet: "tactical wave design retains ≥ 10 % marginal value in ≥ 4/6 cells even under a destination-clustered strong-ops baseline".
3. §6.5 C3-C upgrade: "Φ captures 25–50 % of **stable-over-ops** signal" — the over-ops phrase is the key.
4. Odds update: C&IE 80 %+, IJPR 60 %, TR-E 45 %.

### 4.2 Moderate

**Paper actions**:
1. C&IE stays primary; IJPR as strong alternate.
2. Abstract: "tactical wave design retains 5–10 % marginal value in most cells under stronger operational heuristics".
3. §6.5 C3-C minor edit: keep "25–50 %" claim; add "robust to operational policy choice".
4. Odds update: C&IE 75 %, IJPR 55 %.

### 4.3 Suggestive

**Paper actions**:
1. Hold C&IE primary; downgrade IJPR to tied alternate with FSMJ.
2. Abstract: drop the marginal-value bullet; keep the GAP framework bullet.
3. §6.5 reframed: "tactical wave design adds 3–5 % marginal over strong ops — meaningful at scale, smaller than in weak-ops settings".
4. Odds update: C&IE 65 %, IJPR 40 %.

### 4.4 Reject

**Paper actions — narrative pivot (pre-written to avoid reactive framing)**:
1. **Pivot**: Paper is no longer "tactical adds value over ops". It becomes **"tactical and operational are partly substitutable levers; we map when tactical still matters even under strong ops"**.
2. C3-C is dropped. C3-A (regime sensitivity) and C3-B (β as coarse probe) remain unchanged.
3. M4 and M5 remain unchanged — they are about **intra-tactical** decomposition, not tactical-vs-operational. The Bound-and-Gap is still a diagnostic; Model-Dominance Hedge is still a design rule.
4. New §7 subsection: "Why tactical-vs-operational substitutability does not invalidate Φ".
5. Odds update: C&IE 50 %, FSMJ 80 %. **Do NOT run Tier 2**; this is the pre-registered stop signal.

**Under no REJECT path do we**:
- Re-run P1 with different rules to "find" a better marginal (= p-hacking by ops design).
- Drop cells post-hoc to reach the 4/6 gate.
- Change thresholds to claim "suggestive" (= moving goal posts).

---

## 5. Rationale: why these specific thresholds

- **10 % strong band**: matches Phase 4 v2 §4bis.1 "strong Option 1" band. Tier consistency.
- **5 % moderate band**: matches Phase 4 v2 §4bis.1 "suggestive Option 1" band.
- **3 % suggestive**: one step below the Phase 4 v2 suggestive bar, accounting for additional attenuation by P1.
- **2 % reject**: below measurement noise (Phase 4 v2 cell-level SE ~1–2 %). Below this, effectively zero.
- **4 / 6 cells**: same denominator as Phase 4 v2 gates (2 × 3 cells), so verdicts are directly comparable.

## 6. Planned analyses

1. **Table 1**: per-cell $\mathrm{MV}^{\mathrm{P0}}$, $\mathrm{MV}^{\mathrm{P1}}$, absorption, 95 % CI on both MVs. Rows = 6 cells × 3 sizes = 18; or 6 cell-averages.
2. **Figure 1**: bar chart of MV^P0 vs MV^P1 per cell, with horizontal lines at 2 %, 5 %, 10 % thresholds.
3. **Figure 2**: absorption ratio per cell, horizontal band at 30 % and 60 %.
4. **Regime × ops × arm heatmap**: median makespan grid (12 × 3 cells).

Pre-reg explicitly **disallows**:
- Subsetting to size ≥ 6 to reach a threshold (saw this rescue Phase 4 v2 Option 1 post-hoc; pre-disallowed here).
- Claiming a p-value on MV — we use bootstrap CI, not NHST.
- Aggregating across cells to boost "average MV" — cell-level gate is what matters.

## 7. Timeline

| Day | Milestone |
|---|---|
| D1 (Mon Wk 1) | Implement `.pop_cluster(c)` on `ElevatorBatched`; unit-test against hand-computed cluster-vs-FIFO scenarios |
| D2 | Add `policy: str = "fifo"` arg to `simulate_wave` routing to P0 or P1; verify $\sigma = 0$ determinism |
| D3 | Smoke-test: 3 cells × 1 size × 2 ops × 2 arms × 20 waves = 240 sims. Sanity-check directions. |
| D4 | Write [experiments_phase4_H1.py](../prototype/src/experiments_phase4_H1.py) (full 14 400 sim grid) |
| D5 | Launch full run; save raw CSV |
| D6 (Mon Wk 2) | Write [analysis_phase4_H1.py](../prototype/src/analysis_phase4_H1.py): per-cell MVs, bootstrap, absorption, plots |
| D7 | Generate figures |
| D8 | Write `results/v0_2_phase4_H1.md` deliverable |
| D9 (Wed Wk 2) | Update [outline_v0_1.md](outline_v0_1.md) §6.5, §7, abstract per outcome band |
| D10 | Odds reassessment; hand back to Tier 1 plan for stop-rule evaluation |

---

## 8. What feeds back into the paper

Depending on outcome band (§4):

- [outline_v0_1.md](outline_v0_1.md) §1 abstract: 1 bullet revision (strong/moderate), delete (suggestive), major rewrite (reject).
- §2 Introduction: surprise A (bounded value) framing stays; surprise B (sign-flip) framing stays; new surprise C = "marginal value under strong ops = X%" added.
- §5.3 M4: add "GAP is stable under strong ops" claim (strong/moderate) or drop (suggestive/reject).
- §6.5 C3-C: updated per §4 handling.
- §7 Discussion: new subsection on tactical-vs-operational substitutability (reject only).
- §8 Limitations: one line removed (L6 "Phase 4 H1 deferred" is gone regardless of outcome).

## 9. Surprise-log hook

If any of the following occurs, log to [intuitions_before_MVS_v0_2.md §7](../prototype/intuitions_before_MVS_v0_2.md) as **Surprise #14**:

- $\mathrm{MV}^{\mathrm{P1}}$ **exceeds** $\mathrm{MV}^{\mathrm{P0}}$ in any cell (would mean strong ops *amplifies* rather than absorbs tactical value — counter-intuitive but possible if P1 exposes latent wave-structure signal).
- Absorption is **negative** in any cell (same phenomenon, different metric).
- Arm B worse than Arm A under P1 in any cell (would flip sign from Phase 4 v2 Option 1 verdict; immediate diagnostic trigger).
- P1 produces makespan **identical** to P0 across all cells (means c = 2 is too tight for clustered batching to matter — would require revisiting P1 design and is itself publishable).

---

**Pre-registration locked 2026-04-22 by the author. Simulation runs commence on D1 Mon Wk 1 against the rules above.**
