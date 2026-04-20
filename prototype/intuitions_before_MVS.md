# My Intuitions Before MVS v0.1 (Pre-registration document)

**Placement**: `F:\paper3_wave_elevator\prototype\intuitions_before_MVS.md`
**Purpose**: Lock in my hypotheses BEFORE running any simulation, to prevent post-hoc rationalization
**Must be completed before**: Writing any simulator code
**Signature date**: _______________

---

## Why This Document Exists

This is a **pre-registration document**. Its purpose is to record my predictions about the MVS v0.1 simulation results BEFORE I see any data.

After the simulation runs, I commit to NOT editing this document. If the data contradicts my predictions, I will record the contradiction in `mvs_results_v0_1.md` as a finding—not modify this file to match the data.

This protects against:
- Post-hoc rationalization ("I knew it all along")
- HARKing (Hypothesizing After Results are Known)
- Unconscious data dredging

It also enables a future claim of "counterintuitive finding" in Paper 3—which requires documented evidence of what my prior intuition was.

---

## 1. My Predictions About Feature Signs

For each feature, I predict the direction of its effect on `makespan` (larger or smaller), BEFORE seeing any data.

### 1.1 Vertical Concentration $C$ (Shannon entropy across floors)

**Definition**: Higher $C$ = more uniform distribution of orders across floors; Lower $C$ = concentrated on few floors.

**My prediction (choose one)**:

- [ ] Sign is **POSITIVE** (higher $C$ → larger makespan)
      - Reasoning: _______________________________________________
- [ ] Sign is **NEGATIVE** (higher $C$ → smaller makespan)  
      - Reasoning: _______________________________________________
- [ ] **Ambiguous** (could go either way)
      - Competing effects: _______________________________________________

**My confidence (1-5)**: __ 

---

### 1.2 Directional Imbalance $I$

**Definition**: $|N_{up} - N_{down}| / (N_{up} + N_{down})$. High $I$ = most orders go same direction; Low $I$ = balanced up/down.

**My prediction (choose one)**:

- [ ] Sign is **POSITIVE** (higher $I$ → larger makespan)
      - Reasoning: _______________________________________________
- [ ] Sign is **NEGATIVE** (higher $I$ → smaller makespan)
      - Reasoning: _______________________________________________
- [ ] **Ambiguous**
      - Competing effects: _______________________________________________

**My confidence (1-5)**: __

---

### 1.3 Temporal Clustering $T$

**Note**: In v0.1 MVS, $T = 0$ is fixed (all orders in a wave released simultaneously). So I cannot test this dimension empirically in v0.1. Its sign prediction is for v0.2.

**My prediction for v0.2 (choose one)**:

- [ ] Sign is **POSITIVE** (higher $T$ → larger makespan)
      - Reasoning: _______________________________________________
- [ ] Sign is **NEGATIVE** (higher $T$ → smaller makespan)
      - Reasoning: _______________________________________________
- [ ] **Ambiguous**
      - Competing effects: _______________________________________________

**My confidence (1-5)**: __

---

### 1.4 Cross-Floor Count (baseline feature)

**Definition**: Number of orders in the wave that require floor-crossing.

**My prediction (choose one)**:

- [ ] Sign is **POSITIVE** (more cross-floor → larger makespan)  ← most likely
- [ ] Sign is **NEGATIVE** (counterintuitive)
- [ ] **Ambiguous**

**My reasoning**: _______________________________________________

---

## 2. Magnitude Ranking

**Before seeing data**, I predict the RELATIVE importance of the three features.

Rank from most important (1) to least important (3) in terms of predictive power for makespan:

| Rank | Feature |
|---|---|
| 1 (most important) | [ ] $C$  [ ] $I$  [ ] $T$  [ ] cross_floor_count |
| 2 | [ ] $C$  [ ] $I$  [ ] $T$  [ ] cross_floor_count |
| 3 | [ ] $C$  [ ] $I$  [ ] $T$  [ ] cross_floor_count |

**My reasoning for this ranking**: _______________________________________________

---

## 3. R² Predictions

I predict the following cross-validated R² values (before running the simulation):

| Model | My predicted R² |
|---|---|
| M0 (constant) | 0.00 (by definition) |
| M1 (size only) | ______ |
| M2 (size + cross_floor) | ______ |
| M3 (size + cross_floor + $C$, $I$) | ______ |

**My predicted incremental gain from M2 → M3**: ______

**Interpretation of my prediction**:

- [ ] I expect M3 - M2 ≥ 0.15 → three-dim features have strong predictive power (risk A not present)
- [ ] I expect M3 - M2 to be 0.05-0.15 → moderate predictive power
- [ ] I expect M3 - M2 < 0.05 → weak predictive power (risk A present)

---

## 4. Ablation Predictions

If I drop each feature from the full model, how much will R² drop?

| Drop which feature | My predicted R² drop |
|---|---|
| Drop $C$ | ______ |
| Drop $I$ | ______ |
| Drop cross_floor_count | ______ |

**My prediction (choose one)**:

- [ ] All three drops are similar (within 2×) → three features are balanced (risk B absent)
- [ ] One feature dominates (drops ≥ 3× others) → risk B present
- [ ] Specifically, I expect **this feature to dominate**: ______

---

## 5. Extreme Scenario Predictions

### Scenario A: "Concentrated wave"
All 5 orders go from floor 1 to floor 3 (same direction, same source, same destination).

**My predicted makespan**: ______ seconds

**My reasoning**: _______________________________________________

### Scenario B: "Uniform wave"
5 orders distributed as: (1→2), (1→3), (2→1), (2→3), (3→1) — mixed directions and floors.

**My predicted makespan**: ______ seconds

**My reasoning**: _______________________________________________

### Scenario C: "Counterbalanced wave"
5 orders: (1→3), (1→3), (1→3), (3→1), (3→1) — 3 up, 2 down.

**My predicted makespan**: ______ seconds

**My reasoning**: _______________________________________________

### Which is largest? Which is smallest?

**My prediction**:
- Largest makespan: [ ] A  [ ] B  [ ] C
- Smallest makespan: [ ] A  [ ] B  [ ] C

**My reasoning**: _______________________________________________

---

## 6. Non-obvious Predictions (Bonus)

These are harder-to-predict things I'll note, to test later.

### 6.1 Is the relationship between $C$ and makespan monotonic?

- [ ] Yes, monotonic
- [ ] No, U-shaped or inverted-U
- [ ] I don't know

### 6.2 Is there an interaction effect between $C$ and $I$?

- [ ] Yes, I expect $C \times I$ to matter beyond their individual effects
- [ ] No, they are additively independent
- [ ] I don't know

### 6.3 If the data shows any of these surprises, which would surprise me most?

Rank (1 = most surprising, 4 = least surprising):
- [ ] Rank __: $C$ has OPPOSITE sign than I predicted
- [ ] Rank __: $I$ has OPPOSITE sign than I predicted
- [ ] Rank __: Concentrated wave is actually FASTER than uniform wave
- [ ] Rank __: Cross-floor count dominates, $C$ and $I$ are irrelevant

---

## 7. Commitment

I commit to:

- [ ] Not editing any prediction in this document after starting simulation
- [ ] If data contradicts a prediction, recording it in `mvs_results_v0_1.md` as "Surprise #N"
- [ ] Treating any contradiction as a **finding**, not an error in the simulator
- [ ] (Only after ruling out simulator bugs via sanity checks)

**Signed**: _______________
**Date**: _______________

---

## 8. Post-MVS Addendum (fill AFTER running simulation)

After running MVS v0.1, I will add a brief section here listing:

1. Which predictions were correct?
2. Which predictions were wrong (and by how much)?
3. Any "surprises" — predictions that were dramatically off
4. What these surprises mean for Paper 3's Insight novelty

**DO NOT fill this section before running the simulation.**

---

## 9. Revision Log

- **v0.1 (2026-04-__)**: Initial predictions written before MVS code was run
- **v0.2 (2026-04-__)**: Post-MVS addendum added (no edits to predictions)

---

**End of pre-registration document**