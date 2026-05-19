---
title: "Phase 5 — publication-scale validation: results (W6 deliverable)"
parent: "phase5_scaleup_preregistration.md (LOCKED 2026-05-19)"
date: 2026-05-19
status: "W6 complete — gate verdicts below; pre-reg §4 outcome determined"
---

# Phase 5 Results — publication-scale validation

Analysis of the 106,800-simulation Phase 5 grid (Blocks A/B/C) plus the §9.1
ablation amendment, against the gates locked in
[phase5_scaleup_preregistration.md](../../paper_draft/phase5_scaleup_preregistration.md)
§3. No new simulations — pure reanalysis of the W5 raw CSVs.

## 1. Gate verdict summary

| Hypothesis | Gate result | Verdict |
|---|---|---|
| **H-D1** decomposition | D1-a 72/72, D1-b 70/72, D1-c 72/72, **D1-d 57/72** (bar ≥ 58) | **PARTIAL** |
| **H-D2** chain / DRO | D2-a ✓ (0.992 avg, 0.960 worst), D2-b 24/24, D2-c 24/24, D2-d 6/6 | **PASS** |
| **H-D3** corner-invariance (exploratory) | qmax inv 2/6, qmin inv 5/6, mean ρ = 0.75 | **model-sensitive** branch |
| **H-Policy** 7-policy contest | P5 beats P0 0.83 / P1 0.83 / P6 0.67; 46.4 % above P7 | **Policy-Partial** |

## 2. Pre-registered §4 outcome determination

H-D1 is **not** a pass: D1-d resolves the GAP signal (95 % CI excludes 0) in
**57/72 sub-cells = 79.2 %**, missing the pre-registered ≥ 80 % (≥ 58/72) bar
**by one cell**. Per pre-reg §4, the **"H-D1-d fails (< 80 %)"** row fires:

> *honest §8 limitation: "Bound-and-Gap is a prototype-regime diagnostic"; D1
> stays (it is algebraic) but the empirical-utility claim is softened.*

This is reported as a near-miss (one cell) **factually**, but the verdict is a
fail of D1-d — the pre-registered bar was 58 and is not moved (pre-reg §8
stop-rule 3; §10 sign-off). Combined with **Policy-Partial**, the paper-level
outcome is: D1/D2 ship as **theorems** (algebraically exact at scale), D2 also
**empirically confirmed**, D1's empirical signal-resolution **regime-dependent
and softened**, P5 a **modest diagnostic-driven heuristic, not a champion
policy**.

## 3. Table 1 — Block A decomposition (H-D1), 72 sub-cells

| Gate | Result | Note |
|---|---|---|
| D1-a `GAP = H_up + M_Phi` exact | **72/72** | the decomposition algebra holds exactly at scale |
| D1-b `H_up ≥ 0, M_Phi ≥ 0` | **70/72** | 2 near-degenerate sub-cells have `H_up ≈ −ε`: the random-pool *sample* median marginally exceeds the worst-corner sample median. `M_Phi ≥ 0` always (q_min is the argmin). The population inequality (Corollary M4.2) is **not** violated — finite-sample noise. |
| D1-c `M_Phi == SPO_regret(Φ)` exact | **72/72** | Theorem 1 (D1) — the SPO-regret equivalence holds exactly across the whole grid |
| D1-d GAP 95 % bootstrap CI excludes 0 | **57/72 (79.2 %)** | bar ≥ 58/72; **misses by one cell** |

Mean GAP = 0.0600 (H_up 0.0430 + M_Phi 0.0170). Per demand: clustered 0.082
(D1-d 20/24), uniform 0.052 (20/24), **diurnal 0.046 (17/24)** — the
decomposition is weakest under diurnal demand, where T dilutes the (C,I)
signal. `corr(F, GAP) = −0.18` — a mild decline with floor count (see §7).

## 4. Table 2 — Block C model chain (H-D2 + H-D3), matched-wave

**H-D2 — PASS (clean).**

| Gate | Result |
|---|---|
| D2-a per-wave `M2 ≥ M1` | 0.992 average over 24 cells, 0.960 worst cell — clears ≥ 90 % / ≥ 80 % |
| D2-b FOSD `M1 ≤ M2` | 24/24 cells |
| D2-c one-sided `U_c(0.05) < 5 % · m_0` | 24/24 cells |
| D2-d `c*_DRO == c*_Hedge` | 6/6 configs — Wasserstein-DRO reproduces the Hedge Rule |

The Model-Dominance Hedge Rule and the chain-dominance condition it rests on
are **confirmed at publication scale**. D2 is the firmer of the two pillars.

**H-D3 — exploratory, "model-sensitive" branch.** Worst-corner identity is
invariant across M1/M2/M3 in only 2/6 configs; best-corner in 5/6; mean
corner-ranking Spearman ρ = 0.75 (< 0.8 threshold). Per pre-reg §3.3 the
**model-sensitive** branch fires: the wave-design corner depends on the
believed elevator model → written up as the §5 *motivation* for the Hedge Rule
(M5), not a §6 limitation. No theorem claimed.

## 5. Table 3 — Block B 7-policy contest (H-Policy), 12 cells

P5 win-fractions: vs P0 **0.83**, vs P1 **0.83**, vs P6 **0.67**, vs P7
**0.00**. Band = **Policy-Partial** (≥ 75 % vs P0 and ≥ 50 % vs P1; below the
≥ 90 % Policy-Strong bar).

- **P5 vs P6** (the D1 differentiator): P5 wins 0.67 — the cell-median Φ rule
  beats the SPO-Tree cell-mean predictor in two-thirds of cells. P6 beats P5
  in 0.33 — below the §9 surprise threshold of 0.50, so the D1 §4.1.2
  cell-median argument is **not** invalidated.
- **P5 vs P7**: P5 never beats the local-search optimizer and sits **46.4 %
  above** it. P5 is a cheap, no-simulation feature heuristic — far from
  optimal, modestly better than naive/heuristic baselines.
- Surprise: **P2 (cardinality-only)** is the strongest of the simple
  heuristics — it beats P5 in 0.42 of cells. Low cross-floor count is a potent
  lever; the paper should report this honestly.

## 6. Ablations (pre-reg §9.1 amendment)

| # | Finding |
|---|---|
| A1 feature | (C,I) mean reduction 3.7 % > C-only 2.7 % > I-only 1.1 %; (C,I) beats both singles in 39/72 cells — **C dominant, I weak secondary**. |
| A2 T dimension | T adds corner leverage in 1/6 configs — **weak lever**. |
| A3 estimator | cell-**mean** GAP is marginally more stable (boot SD 0.015 vs 0.021); the cell-median is kept for **Theorem-1 consistency**, not robustness. |
| A4 granularity | 3×3 raises UB in 6/6 configs — **confirms Corollary M4.4** at scale. |
| P7 reference | P5 captures **19.0 %** of the P0→P7 improvement gap. |

## 7. Surprise-log (pre-reg §9)

- **`GAP` vs `F`**: `corr = −0.18` — a *mild* decline of GAP with floor count.
  Weakly triggers the hook; logged as a minor effect, not a reversal.
- **P6 beats P5 ≥ 50 %**: NOT triggered (P6 wins 0.33) — the cell-median
  argument survives.
- **diurnal corner ranking**: subsumed by the H-D3 model-sensitive finding —
  corner ranking is model-dependent generally; diurnal is the weakest regime
  for the (C,I) decomposition (Table 1).

## 8. Figures

- [phase5_fig1_gap_landscape.png](figures/phase5_fig1_gap_landscape.png) —
  GAP across the 72 sub-cells vs F and vs |A|, coloured by demand.
- [phase5_fig2_p5_vs_p6.png](figures/phase5_fig2_p5_vs_p6.png) — P5-vs-P6
  paired median makespan (the D1 differentiator).

## 9. What feeds into the paper

- **§4 methodology** — ships **D1 + D2 as theorems** (algebraically exact at
  scale: D1-a/c 72/72). The cell-median is justified by Theorem-1 consistency,
  **not** robustness (A3). D3 is not a theorem.
- **§5 results** — D2 reported as **confirmed at publication scale** (the
  firm pillar). D1's decomposition reported with the honest D1-d figure
  (resolves signal in 79 % of sub-cells, regime-dependent, weakest under
  diurnal). H-D3 model-sensitivity becomes the §5 *motivation* for M5. The
  7-policy contest + P7 reference: P5 a modest diagnostic-driven heuristic.
- **§6 / §8 limitations** — the pre-registered "Bound-and-Gap is a
  prototype-regime diagnostic" softening; P5 is 46 % above a local-search
  optimum; C carries most of the Φ signal (I, T marginal).
- **Framing** — the contribution is the **theoretically-grounded diagnostic
  decomposition** (D1) and the **confirmed Hedge Rule** (D2), honestly
  ablated. Not a competitive wave-design policy.

## 10. Honest assessment

D2 is solid and confirmed. D1's theorems are exact; its empirical
signal-resolution misses the pre-set bar by one sub-cell and is
regime-dependent. The 7-policy contest puts P5 ahead of naive and heuristic
baselines but far from a search optimum. None of this is a triumph; none of it
is a collapse. The pre-registration (§10, locked before W5; §9.1 amendment
before W6) is what lets every number above be reported as-is — the partial
results are honest regime-conditional findings, not a fishing residue.

---

**W6 complete 2026-05-19. Phase 5 closed. Verdicts: H-D1 PARTIAL (D1-d 57/72),
H-D2 PASS, H-D3 model-sensitive, H-Policy Partial. Pre-reg §4 outcome:
"H-D1-d fails" + "Policy-Partial" rows.**
