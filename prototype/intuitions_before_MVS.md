# My Intuitions Before MVS v0.1 (Pre-registration document)

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

C = Shannon entropy over 楼层分布
高C = 楼层分布均匀（订单涉及 1、2、3 楼都有）
低C = 楼层分布集中（订单都在某 1-2 个楼层之间）

极端 A（低 C）：所有订单都在 1 楼 ↔ 3 楼之间
5 个订单：(1→3), (1→3), (3→1), (1→3), (3→1)
电梯只需要在 1 和 3 之间来回
2 楼完全不用停

极端 B（高 C）：订单分布在所有楼层之间
5 个订单：(1→2), (2→3), (1→3), (3→2), (2→1)
电梯要在 1、2、3 所有楼层都停
路径更碎片化

两个对抗的物理效应
效应 1（支持低 C 更快）：
低 C 时电梯路径"规律化"——像一条固定路线的班车
减少启停次数（电梯加减速是 dead time）
直觉：专线比杂线快

效应 2（支持高 C 更快）：
低 C 时所有 AMR 都在 1 楼和 3 楼"打架"——AMR 间争用加剧
低 C 意味着电梯总是"全楼层长距离跑"
高 C 时"顺路"机会多——电梯 1→2 的途中可以捎带 1→3 的需求
直觉：分散开反而不挤

**My prediction (choose one)**:

- [ ] Sign is **POSITIVE** (higher $C$ → larger makespan)
      - Reasoning: _______________________________________________
- [ ] Sign is **NEGATIVE** (higher $C$ → smaller makespan)  
      - Reasoning: _______________________________________________
- [√] **Ambiguous** (could go either way)
      - Competing effects: _______________________________________________

Two competing effects: (1) low C concentrates elevator traffic into predictable routes, reducing start-stop overhead; (2) low C concentrates AMR contention on few floors, increasing inter-AMR competition. Without simulation evidence, I cannot predict which dominates.

**My confidence (1-5)**: 2 

---

### 1.2 Directional Imbalance $I$

**Definition**: $|N_{up} - N_{down}| / (N_{up} + N_{down})$. High $I$ = most orders go same direction; Low $I$ = balanced up/down.

效应 1（支持高 I 更慢）——"空驶返程成本"
极端 A 里电梯把 AMR 送到 3 楼后，要空驶回到 1 楼接下一台 AMR
每一次电梯服务 = 有效行程（载人）+ 空驶（无载）
全向上时，空驶比例 50%
平衡时（有人上有人下），理论上电梯可以顺路带另一个方向的 AMR，空驶比例下降
这是电梯调度领域的经典结论（up-peak vs interfloor traffic）

效应 2（支持高 I 更快）——"同向顺路机会"
极端 A 里电梯上行时可以"捎带"——1→3 的途中经过 2 楼，可以顺便放下 1→2 的 AMR
平衡情况下，上行 AMR 不能和下行 AMR 共用一次电梯行程
但这个效应的前提是 elevator capacity > 1——你 v0.1 的 capacity = 1，这个效应被完全抹掉

效应 3（支持高 I 更慢）——"资源争用极值"
全向上时，所有 AMR 都在 1 楼排队等电梯
平衡时，AMR 分散在不同楼层——"排队压力"被稀释
对单电梯 FCFS 来说，队列越长 AMR 平均等待时间越长

**My prediction (choose one)**:

- [√] Sign is **POSITIVE** (higher $I$ → larger makespan)
      - Reasoning: Two effects both predict positive sign in v0.1 scope: (1) empty-return overhead—when all AMRs go one direction, elevator must empty-travel back to pick up the next, increasing dead time; (2) queue contention at the common boarding floor. The counter-effect of 'same-direction capacity sharing' is neutralized because v0.1 uses elevator capacity=1.
- [ ] Sign is **NEGATIVE** (higher $I$ → smaller makespan)
      - Reasoning: _______________________________________________
- [ ] **Ambiguous**
      - Competing effects: _______________________________________________

**My confidence (1-5)**: 3-4

---

### 1.3 Temporal Clustering $T$

**Definition (adopted convention)**: 
$T$ measures how concentrated the release times of orders within a wave are. I adopt the convention:

- **High $T$** = orders released in a concentrated time window (e.g., all released simultaneously or within a very short burst)
- **Low $T$** = orders released spread out over a longer time window (staggered release)

Mathematically, this can be operationalized as an inverse-dispersion measure, e.g.:
$T = 1 / (1 + \sigma_{release}/\mu_{release})$ 
or 
$T = n / (t_{\max} - t_{\min} + \epsilon)$

The exact formula will be finalized in v0.2. This naming convention is consistent with standard usage of "temporal clustering" in queueing and operations literature, where clustering implies concentration.

**Note on v0.1**: In v0.1 MVS, all orders within a wave share the same `release_time`, so $T$ takes a degenerate constant value (saturated high, or undefined under some formulations). This feature's predictive power **cannot be empirically tested in v0.1** — the prediction below is for v0.2.

**My prediction for v0.2**:

- [x] Sign is **POSITIVE** (higher $T$ → larger makespan)
      - Reasoning: Under the adopted convention where high $T$ means concentrated release, two physical effects predict a positive sign: 
        (1) **Concurrent demand burst**: when many orders are released simultaneously, AMRs converge on the single elevator at nearly the same time, producing a queue buildup whose length grows non-linearly with arrival rate concentration (standard queueing-theoretic result);
        (2) **Peak load stress**: the single elevator's throughput capacity is a hard upper bound; concentrated release pushes demand above this bound temporarily, forcing waiting times that spread release cannot incur.
      The counter-effect is that concentrated release gives the fleet scheduler a larger *batching optimization space* (it sees many orders at once and can match AMRs to orders optimally). However, in v0.1 and likely v0.2 early iterations, the scheduler uses a simple greedy rule that does not exploit batching information. This neutralizes the counter-effect.

**My confidence (1-5)**: 3

Reasoning for confidence level: The physical direction is consistent with queueing theory, but (a) I cannot verify in v0.1, (b) the effect magnitude depends heavily on how staggered the "spread" release is in v0.2 (few seconds vs. minutes), and (c) if v0.2 introduces a more sophisticated scheduler, the batching-space counter-effect may revive.

---

### 1.4 Cross-Floor Count (baseline feature)

**Definition**: Number of orders in the wave that require floor-crossing 
(source_floor ≠ dest_floor).

**My prediction**:

- [x] Sign is **POSITIVE** (more cross-floor → larger makespan)
- [ ] Sign is **NEGATIVE** (counterintuitive)
- [ ] **Ambiguous**

**My reasoning**: 
Cross-floor orders are the only orders that consume elevator capacity. Each cross-floor 
order requires up to 2 elevator trips (AMR to source, then AMR+order to destination), 
while same-floor orders only incur pickup + dropoff service time. Under v0.1 parameters 
(service_time = 5s per pickup/dropoff, elevator trip ≈ 14s), cross-floor orders are 
approximately 2-3× longer than same-floor orders, AND they compete for the shared 
elevator bottleneck. Both effects point strongly positive.

**My confidence (1-5)**: 5

Reasoning for high confidence: The simulator mechanics make this prediction near-mathematically 
necessary. The only way to flip this sign would be a pathological parameter regime 
(e.g., same-floor service time > cross-floor elevator time), which does not hold in v0.1.

---

## 2. Magnitude Ranking

**Honest disclosure**: At the time of writing this pre-registration, I do not yet have strong intuition about the relative magnitude of feature effects on makespan. I have not operated a multi-storey AMR system at this scale, and my confidence on individual feature signs (§1) was mostly low-to-medium. Rather than fabricate a ranking I cannot defend, I record here my *weak prior* and commit to comparing it against the observed data.

**Weak prior ranking for v0.1**:

| Rank | Feature | Reasoning |
|---|---|---|
| 1 (likely most important) | cross_floor_count | Mechanically necessary in the simulator: cross-floor orders are the only ones that consume elevator capacity. Each such order adds ~14–20s of elevator time, vs. ~10s total for same-floor orders. |
| 2 | $I$ | Under v0.1 (single elevator, capacity=1, FCFS scheduling), directional imbalance is expected to matter via empty-return overhead and queue concentration at common boarding floors. |
| 3 | $C$ | Competing effects (routing regularity vs. AMR contention on concentrated floors) leave me unable to predict the direction, let alone the magnitude. |
| 4 (zero variance) | $T$ | By v0.1 construction, all orders within a wave share release_time. $T$ has zero variance across samples and therefore zero predictive power in v0.1. Ranking position here is by definition, not prediction. |

**Note on wave size**: Wave size is not a candidate in this ranking (per the original document template), but it is expected to rival cross_floor_count as a primary predictor, with strong correlation between the two. The Risk B ablation analysis will disentangle their independent contributions.

**My confidence in this ranking**: 2 out of 5

**What I expect to learn from MVS v0.1**:
- Whether the vertical features ($C$, $I$) reach comparable magnitude to the baseline feature (cross_floor_count) under v0.1's extreme-bottleneck scope (1 elevator)
- Whether $C$ and $I$ dominate or are dominated by baselines, which will inform whether my research framing (three-dimensional vertical decomposition) needs adjustment for v0.2
- Whether there are interaction effects (e.g., $C \times I$) I did not anticipate

**Potential swap I'm most uncertain about**: Ranks 2 and 3 ($I$ vs $C$). I leaned $I$ higher because its effect mechanism (empty-return + queue concentration) is clearer to me than $C$'s mechanism. But if the simulator reveals that concentrated floor distribution causes AMR contention effects I underestimated, $C$ could outrank $I$.


---

## 3. R² Predictions

I predict the following cross-validated R² values (before running the simulation):

| Model | My predicted R² |
|---|---|
| M0 (constant) | 0.00 (by definition) |
| M1 (wave size only) | 0.4 |
| M2 (size + cross_floor) | 0.6 |
| M3 (size + cross_floor + $C$, $I$) | 0.68 |

**My predicted incremental gain from M2 → M3**: +0.08

**Interpretation of my prediction**:

- [ ] I expect M3 - M2 ≥ 0.15 → three-dim features have strong predictive power (risk A not present)
- [x] I expect M3 - M2 to be 0.05-0.15 → moderate predictive power
- [ ] I expect M3 - M2 < 0.05 → weak predictive power (risk A present)

---

## 4. Ablation Predictions

If I drop each feature from the full model, how much will R² drop?

| Drop which feature | My predicted R² drop |
|---|---|
| Drop $C$ | 0.03 | (weakest: ambiguous sign, rank 3)
| Drop $I$ | 0.05 | (moderate: positive sign, rank 2)
| Drop cross_floor_count | 0.18 | (strongest: baseline dominant, rank 1)

**My prediction (choose one)**:

- [ ] All three drops are similar (within 2×) → three features are balanced (risk B absent)
- [x] One feature dominates (drops ≥ 3× others) → risk B present
- [x] Specifically, I expect **this feature to dominate**: cross_floor_count

---

## 5. Extreme Scenario Predictions

### Scenario A: "Concentrated wave"
All 5 orders go from floor 1 to floor 3 (same direction, same source, same destination).
5 AMR 都在 1 楼，t=0 开始
电梯在 1 楼，空闲
每次电梯行程 1→3 需要：loading(2) + travel(10) + unloading(2) = 14 秒
每个 order 额外 pickup(5) + dropoff(5) = 10 秒
单个 order 完整耗时 = 14 + 10 = 24 秒
电梯一次一个，AMR 必须排队
**My predicted makespan**: 130 seconds

### Scenario B: "Uniform wave"
5 orders distributed as: (1→2), (1→3), (2→1), (2→3), (3→1) — mixed directions and floors.

**My predicted makespan**: 180 seconds

### Scenario C: "Counterbalanced wave"
5 orders: (1→3), (1→3), (1→3), (3→1), (3→1) — 3 up, 2 down.

**My predicted makespan**: 170 seconds

### Which is largest? Which is smallest?

**My prediction**:
- Largest makespan: [ ] A  [x] B  [ ] C
- Smallest makespan: [x] A  [ ] B  [ ] C

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

- [x] Not editing any prediction in this document after starting simulation
- [x] If data contradicts a prediction, recording it in `mvs_results_v0_1.md` as "Surprise #N"
- [x] Treating any contradiction as a **finding**, not an error in the simulator
- [x] (Only after ruling out simulator bugs via sanity checks)

**Signed**: shiyuehu (shiyuehu828@gmail.com)
**Date**: 2026-04-21

---

## 8. Post-MVS Addendum

**Filled 2026-04-21 after running `src/experiments.py` (n=1000 waves, seed=2026).**
**Raw data**: `prototype/results/raw/mvs_v0_1_samples.csv`

---

### 8.1 Predictions that held

| Source | Prediction | Actual | Verdict |
|---|---|---|---|
| §1.4 | `cross_floor` has POSITIVE sign (confidence 5) | `corr(cross_floor, makespan) = +0.824` | ✅ Sign correct, direction strongly confirmed |
| §1.2 | `I` has POSITIVE sign | I coefficient sign positive in M3 linear fit | ✅ Sign correct |
| §2 | `cross_floor` is rank-1 in ablation | Ablation drops confirm `cross_floor > I > C` in order | ✅ Order correct |
| §4 | "One feature dominates" (ablation) | `cross_floor` drop = -0.037, vs `C` drop ≈ 0 | ✅ Structurally confirmed |
| §5 Smallest | Scenario A smallest makespan | A=120s < B=137s, C=148s | ✅ Correct |
| §1.3 | T has zero variance in v0.1 | `var(T) = 0.000` exactly | ✅ By construction |

---

### 8.2 Predictions that failed (magnitude or sign)

| Source | Predicted | Actual | Gap |
|---|---|---|---|
| §3 | M1 (size) R² = **0.40** | **0.752** | +0.35 (underpredicted by 88%) |
| §3 | M2 R² = **0.60** | **0.808** | +0.21 |
| §3 | M3 R² = **0.68** | **0.816** | +0.14 |
| §3 | M2 − M1 = **+0.20** | **+0.056** | 3.5× overpredicted |
| §3 | M3 − M2 = **+0.08** (moderate band) | **+0.008** (**red-flag zone**) | 10× overpredicted — decision gate triggered |
| §4 | Drop cross_floor → −0.18 R² | **−0.037** | 5× overpredicted |
| §4 | Drop I → −0.05 R² | **−0.008** | 6× overpredicted |
| §4 | Drop C → −0.03 R² | **+0.001** (sign flipped) | C is statistically noise in v0.1 |
| §5 Scenario A | 130s | **120s** | −10s (−8%) |
| §5 Scenario B | 180s | **137s** | −43s (−24%) |
| §5 Scenario C | 170s | **148s** | −22s (−13%) |
| §5 Largest | B | **C** (148 > 137) | **Ranking inverted** |

---

### 8.3 Surprises (predictions that were dramatically off)

**Surprise #1 — v0.1 is far more predictable than intuition suggested**
- `size` alone gives R² = 0.752 (predicted 0.40)
- Mechanism: deterministic times × single saturated bottleneck ≈ "make-span ≈ k · size + const" in the queue-dominated regime
- Implication: the "ceiling" R² for v0.1 is very high, leaving tiny room for three-dim features to add value

**Surprise #2 — M3 − M2 = +0.008 is inside the "red flag" zone**
- Predicted +0.08 (moderate band 0.05–0.15); actual +0.008
- Linear additive C/I on top of (size, cross_floor) contributes essentially nothing in v0.1
- This does NOT falsify Paper 3 broadly; it scopes the Φ claim to "not sufficient in single-bottleneck regime under linear form"

**Surprise #3 — Scenario ranking inverted: C > B, not B > C**
- Pre-registered prediction: Largest = B (uniform)
- Actual: C = 148s > B = 137s
- Mechanism revealed: "low C" (§1.1 effect 1 "班车化") is dominated by per-trip travel distance — every trip in C goes 1↔3 (max distance), while B has short (1↔2, 2↔3) hops
- **This is itself a candidate C3-H3 insight**: concentrated vertical demand is slower, not faster, in single-bottleneck deterministic regime

**Surprise #4 — baseline collinearity**
- `cross_floor` and `size` are highly correlated (corr ≈ 0.78 by construction, since ~78% of random orders are cross-floor)
- This makes the plan's "baseline M2 = size + cross_floor" **poorly specified** — M2 is barely distinguishable from M1
- **Lesson for v0.2**: baseline must be genuinely orthogonal (e.g., total Manhattan distance weighted, or unique-floor count)

**Surprise #5 — §1.1 effect 2 was incoherent with v0.1 scope**
- The "high C 顺路机会多" effect required `capacity > 1`, which v0.1 does not have
- The pre-reg noted this for I (§1.2 effect 2) but missed the symmetric point for C
- Honest assessment: the ambiguity in my §1.1 prediction was partly artificial — in v0.1 regime, effect 1 ("班车化") had no competitor, but it was still dominated by travel distance (Surprise #3)

---

### 8.4 Implications for Paper 3's Insight novelty

Mapping v0.1 results to `novelty_analysis_and_contribution.md §8` counterfactual scenarios:

| Paper 3 claim | v0.1 impact | Status |
|---|---|---|
| **C1** Problem formulation | Not tested (Type A) | ✅ Unaffected |
| **C2-M1** Two-stage architecture | Not tested (Type A) | ✅ Unaffected |
| **C2-M2** Three-dim structured Φ | Linear version weakened in v0.1 regime | ⚠️ Must be rescoped to "regime-dependent" or "non-linear" (see v0.2 plan) |
| **C2-M3** Φ beats ML baselines | Untested | 🔲 Pending |
| **C3-H1** Marginal value of tactical layer | Untested (no operational baseline in v0.1) | 🔲 Pending (v0.2 Phase 4) |
| **C3-H2** Regime-dependence | Indirectly **supported** (Surprise #1+#2 together imply "single-bottleneck = no signal", opening the regime question) | 🟡 Promising |
| **C3-H3** Counterintuitive optima | Candidate insight from Surprise #3 | 🟡 Promising |

**Net effect on Paper 3**: v0.1 triggered Counterfactual Scenario A partially — Φ's linear-predictor framing needs revision. All other contributions are untouched or indirectly strengthened. The path forward is [MVS_v0_2_plan.md](MVS_v0_2_plan.md), which is explicitly designed to test whether Φ has predictive power in regimes v0.1 could not probe (multi-elevator, capacity>1, staggered release, non-linear models).

---

### 8.5 Commitment compliance check

Per §7 commitment, I confirm:
- ✅ No predictions in §1–§6 were edited after the simulation ran
- ✅ All contradictions are recorded here as Surprises, not as edits upstream
- ✅ Sanity checks were performed (3 hand-computed scenarios: A=120, B=137, C=148 all exactly matched simulator output), ruling out simulator bugs as an explanation for the surprises
- ✅ Surprise #3 (scenario ordering) is treated as a finding and carried forward as candidate C3-H3 material

---

## 9. Revision Log

- **v0.1 (2026-04-21, pre-run)**: Initial predictions written and signed before MVS code was run
- **v0.2 (2026-04-21, post-run)**: Post-MVS addendum added (§8 filled; §1–§7 unchanged)

---

**End of pre-registration document**