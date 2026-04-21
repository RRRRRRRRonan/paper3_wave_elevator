# MVS v0.2 Phase 0 — Non-linear Diagnostic

**Date**: 2026-04-21
**Script**: `src/analysis.py`
**Input**: `results/raw/mvs_v0_1_samples.csv` (1000 waves from v0.1, seed=2026)
**Raw results**: `results/v0_2_phase0_nonlinear.json`

---

## 1. Decision gate outcome

| Metric | Value | Threshold | Verdict |
|---|---|---|---|
| Best non-linear R² − M3 linear R² | **+0.0039** | ≥ 0.05 | ❌ **REJECTED** |
| Linear interaction terms gap | +0.0048 | ≥ 0.05 | ❌ REJECTED |

**H_v2.2 (non-linear reveals hidden C/I signal)** is **not supported** on v0.1 data.

---

## 2. Model comparison (5-fold CV, shuffled, seed=42)

| Model | Features | CV R² | Δ vs M3 linear |
|---|---|---|---|
| M1 linear | size | 0.7525 | −0.0641 |
| M2 linear | size + cross_floor | 0.8092 | −0.0074 |
| **M3 linear** | **+ C + I** | **0.8166** | **baseline** |
| M3+ linear | + 6 interaction terms | 0.8214 | +0.0048 |
| RF (200 trees) | base 4 | 0.8024 | **−0.0142** |
| GBM (200 trees, depth 3) | base 4 | 0.8205 | +0.0039 |
| RF + interactions | 10 features | 0.8019 | −0.0147 |
| GBM + interactions | 10 features | 0.8157 | −0.0009 |

**Observations**:
1. **Tree models essentially tie with or underperform linear regression.** RF is 1.4 pp worse, GBM is at par with M3+ linear. On genuinely non-linear data, trees should win decisively at n=1000.
2. **Adding interaction terms to linear regression gains +0.005 R²** — below noise threshold.
3. **Adding interactions to trees makes them WORSE** (−0.0005 to −0.0005) — sign that interaction features are noise or the trees already captured needed structure.

---

## 3. Permutation importance (RF, base features, 20 repeats)

| Feature | Importance | Std |
|---|---|---|
| size | **+1.123** | 0.048 |
| cross_floor | +0.208 | 0.009 |
| C | +0.112 | 0.006 |
| I | +0.098 | 0.007 |

**Interesting contrast with linear ablation**:
- Linear ablation (from §8.2 of `intuitions_before_MVS.md`): dropping C changes R² by −0.001, dropping I changes by −0.008
- Permutation importance: C ≈ 0.11, I ≈ 0.10

Why the discrepancy? **Collinearity**. Permutation importance captures "any variance this feature correlates with," while ablation measures "unique variance after others." C and I carry redundant signal with `size` and `cross_floor`, so linear ablation gives them near-zero, but trees still use them for reducing impurity.

**This is noteworthy**: trees **do see** C and I as informative, just not independently. That is information that linear regression cannot extract.

---

## 4. Linear M3+ coefficients with interactions

| Term | Coefficient |
|---|---|
| size | +11.82 |
| cross_floor | +8.27 |
| **C** | **+53.68** |
| I | +2.83 |
| C × I | +0.21 |
| I² | −5.62 |
| **C²** | **−39.92** |
| C × cross_floor | +4.91 |
| I × cross_floor | −8.73 |
| size × I | +4.05 |

**Pattern detection**:
- `C` linear (+54) + `C²` (−40) → **concave relationship**: makespan grows with C but at a diminishing rate. Mild non-linearity in C.
- `I × cross_floor` (−8.7) → small interaction: imbalance hurts less when fewer orders cross floors (obvious mechanism).
- `size × I` (+4.0) → size amplifies imbalance effect.
- `C × I` ≈ 0 → **no direct C-I interaction** (contrary to my §6.2 open question).

These signs are physically plausible but the R² improvement from all of them combined is only +0.005. In v0.1, **the total non-linear and interaction signal is ~0.5 pp of R²**, well inside noise.

---

## 5. Interpretation

### 5.1 What Phase 0 ruled out

- **Functional-form salvage**: v0.1's red flag cannot be explained away by "we used the wrong model." Both tree models and high-order linear terms give marginal (or no) improvement.
- **Hidden C-I interaction**: the `C × I` term is near zero. The Paper 3 intuition that "concentration and imbalance interact" is not visible in v0.1.

### 5.2 What Phase 0 confirmed

- **The limitation is structural, not functional.** v0.1's single-bottleneck + deterministic regime genuinely offers little room for three-dim features. Size already captures 75% of variance.
- **v0.2 Phase 1 (regime sweep) is now the decisive experiment.** If C/I don't emerge under any (E, capacity) combination, Paper 3's Φ as "predictive surrogate" is truly in trouble.

### 5.3 Minor positive signal

Trees' permutation importance (C ≈ 0.11, I ≈ 0.10) suggests C and I are **not pure noise** — they carry collinear/redundant signal with `size` and `cross_floor`. This is consistent with "the features are correct but v0.1 regime doesn't differentiate them." v0.2 should check whether de-collinearizing the baseline (replacing `cross_floor` with total Manhattan distance or unique-floor count) reveals C/I signal.

---

## 6. Consequences for v0.2 execution

| v0.2 Plan change | Before Phase 0 | After Phase 0 |
|---|---|---|
| Surrogate form in Phase 1-4 | "linear vs non-linear — decide after Phase 0" | **Stick with linear M3+** (with interaction terms). Do not spend effort on tree-model tuning. |
| Baseline in Phase 1 | `size + cross_floor` | **Replace with `size + total_floor_distance`** (decollinearize) — revealed as important by Phase 0's collinearity analysis |
| Phase 1 priority | Share with other phases | **Elevated to critical path** — this is now the only way to rescue C2-M2's "predictive surrogate" framing |
| Risk posture | Moderate | Higher — if Phase 1 also shows M3−M2 < 0.05 across all regimes, Paper 3 enters Scenario A rescue (Φ as conceptual decomposition only) |

---

## 7. Cost

- Runtime: ~20 seconds
- New data generated: **none** (pure analysis on existing v0.1 data)
- Decision value: **high** — definitively rules out "wrong model" hypothesis, which would have consumed 2-3 days of v0.2 if not ruled out early

**Phase 0 is complete.** Proceed to Phase 1 (regime sweep) with linear M3+ as the surrogate form.
