# Paper 3: Minimal Viable Simulation (MVS) Prototype Plan

**Placement**: `F:/paper3_wave_elevator/prototype/MVS_prototype_plan.md`
**Status**: v0.1 blueprint — by Claude, 2026-04-20
**Purpose**: 让你在**3-5 天内**写出一个最小可运行的仿真，用来验证三维特征假设是否有经验基础

---

## 1. 为什么要先做 MVS 而不是先写建模论文？

简单事实：**你 Paper 3 的核心假设是"三维特征 $(C, I, T)$ 能预测 wave makespan"——这是一个经验假设，光靠思考无法证实**。

三个风险：
- 风险 A：三维特征可能预测力不足 → 你的 surrogate model 基础崩塌
- 风险 B：三维特征可能被一维主导 → 你的 "three-dimensional" novelty 就弱了
- 风险 C：真实现象可能和你的直觉完全不一样

**MVS 的目的是用 1 周时间把这三个风险暴露出来**。如果假设成立，你就有了 empirical backing 去说服导师和 reviewer；如果不成立，你就要调整或放弃这个方向——**越早知道越好**。

---

## 2. MVS 的最小 scope

### 2.1 物理系统（故意做得很小）

| 参数 | 值 | 理由 |
|---|---|---|
| 楼层数 F | **3** | 最小可 "跨层" 的数字 |
| AMR 数 N | **5** | 能观察到 congestion 的最小数 |
| Elevator 数 E | **1** | 最极端的 bottleneck，便于观察 |
| Elevator capacity | **1 AMR/ride** | 和 Chakravarty 2025 保持可比 |
| 单层电梯时间 | **5 秒**（确定性）| 简单 |
| Loading（AMR 上电梯）| **2 秒** | 固定 |
| Unloading（AMR 下电梯）| **2 秒** | 固定 |
| Pickup / Dropoff 服务时间 | **5 秒** 各 | AMR 在 source/dest 层的操作 |
| 电梯换向 | **0 秒**（简化）| v0.1 先不考虑 |

**电梯一次 `request()` 服务 = 5 步**：`wait` + `reposition`（空驶到 AMR 层）+ `loading`(2s) + `travel`（载 AMR 到 target）+ `unloading`(2s)。详见 [simulator.md](simulator.md)。

**关键**：所有参数都是**确定性的**。Stochastic 扩展留到 v0.2。

### 2.2 Order 模型

- 每个 order 有：`source_floor`, `destination_floor`, `release_time`
- Source 和 destination 至少有一个 ≠ 1（楼）
- 每班次 20-30 个 orders（足够多以观察 wave 效应，足够少以快速仿真）

### 2.3 Wave 模型

- 一个 wave 是 `{list of order IDs}` + `release_timestamp`
- 一个班次分 3-5 个 waves
- Wave 的 composition 和 release 时间是**你要研究的决策变量**

### 2.4 仿真内核（discrete-event simulation）

- 事件类型：AMR arrives at elevator, elevator arrives at floor, AMR completes order
- 每个 AMR 遵循简单策略：收到 order 后走最短路径（FCFS 规则处理 elevator 争用）
- 输出：makespan、每个 wave 的完成时间

---

## 3. 三步实验设计

### Step 1: 随机生成 1000 个 wave composition

- 固定 30 个 orders 的池
- 随机从池中抽 waves（不同 composition、不同 release time）
- 跑仿真，记录每个 wave 的 makespan
- **输出**：1000 个 `(wave_composition, release_time, makespan)` 样本

### Step 2: 为每个 wave 计算三维特征

对每个 wave $w$：

**垂直集中度 $C(w)$**（用 entropy）：
```
p_i = (wave 内 source 或 dest 为楼层 i 的 orders 数) / (wave 总 orders 数)
C(w) = - Σ p_i · log(p_i)     # Shannon entropy
```
高 $C$ = 楼层分布均匀；低 $C$ = 集中在少数楼层。

**方向不平衡 $I(w)$**：
```
N_up = wave 内"向上"的 orders 数（dest floor > source floor）
N_down = wave 内"向下"的 orders 数
I(w) = |N_up - N_down| / (N_up + N_down)
```
高 $I$ = 方向极端不平衡（全向上或全向下）；低 $I$ = 平衡。

**时间集聚 $T(w)$**：
```
如果 wave 所有 orders 同时释放（v0.1 的假设）：T(w) = 0
如果 staggered 释放：T(w) = σ(release_times) / mean(release_times)
```
v0.1 先假设 $T(w) = 0$（所有 wave 内 orders 同时释放），专注 $C$ 和 $I$。

### Step 3: 拟合 surrogate model

```
Baseline 0 (常数): Φ_0(w) = mean(makespan)
Baseline 1 (线性): Φ_1(w) = a0 + a1·|w|    # 只用 wave size
Baseline 2 (travel dist): Φ_2(w) = Φ_1 + a2·total_travel_distance
My method: Φ_my(w) = Φ_2 + a3·C(w) + a4·I(w)   # 加入 vertical features
```

**关键 metric**：
- $R^2$（解释方差比例）
- RMSE
- 交叉验证

**决定性问题**：$\Phi_{my}$ 的 $R^2$ 相比 $\Phi_2$ 提升了多少？

### Step 4: 解读结果

| $R^2$ 提升 | 解读 | 行动 |
|---|---|---|
| > 20% | **三维特征有强预测力** | Paper 3 方向稳，继续推进 |
| 10-20% | 有价值但不决定性 | 需要更精细的特征；$T$ 维度可能补救 |
| 5-10% | **警告**：改善不显著 | 重新思考 surrogate 设计 |
| < 5% | **红灯**：假设可能有误 | 重新考虑 Paper 3 方向 |

---

## 4. 预期产出

**5 天后，你应该有**：

1. `mvs_simulation.py` — 仿真主程序（~400 行 Python）
2. `mvs_features.py` — 三维特征计算（~100 行）
3. `mvs_analysis.ipynb` — Jupyter notebook，展示拟合结果和图
4. `mvs_results_v0_1.md` — 结论总结，$R^2$ 数字，可视化

**然后你可以拿着这份结果去见导师**。$R^2$ 数字比任何口头论证都有说服力。

---

## 5. 最简 Python 骨架（你可以复制开始）

### 5.1 `mvs_simulation.py`

```python
"""
MVS: Minimal Viable Simulation for Paper 3
3 floors, 5 AMRs, 1 elevator, deterministic.
"""
import heapq
import random
from dataclasses import dataclass, field
from typing import List

@dataclass
class Order:
    id: int
    source_floor: int  # 1-3
    dest_floor: int    # 1-3
    release_time: float

@dataclass
class Wave:
    orders: List[Order]
    release_time: float

@dataclass
class AMR:
    id: int
    current_floor: int
    current_time: float
    status: str = 'idle'  # 'idle', 'moving', 'waiting_elevator', 'in_elevator'

class ElevatorResource:
    """Single elevator, FCFS, serves 1 AMR at a time.

    Per-request timing (5 phases):
      (a) wait       — 电梯和 AMR 较晚到达一方等另一方
      (b) reposition — 电梯空驶到 AMR 所在层
      (c) loading    — AMR 上电梯（固定 2s）
      (d) travel     — 电梯载 AMR 到 target floor
      (e) unloading  — AMR 下电梯（固定 2s）
    """
    def __init__(self, speed_per_floor=5.0, load_time=2.0, unload_time=2.0):
        self.current_floor = 1
        self.available_at = 0.0
        self.speed = speed_per_floor
        self.load_time = load_time
        self.unload_time = unload_time

    def request(self, amr_current_floor, target_floor, request_time):
        # 返回 AMR 下电梯（完成电梯段）的时刻
        wait_start = max(request_time, self.available_at)
        reposition_time = abs(self.current_floor - amr_current_floor) * self.speed
        loading_end = wait_start + reposition_time + self.load_time
        travel_time = abs(amr_current_floor - target_floor) * self.speed
        arrive_at_target = loading_end + travel_time
        unloading_end = arrive_at_target + self.unload_time

        self.current_floor = target_floor
        self.available_at = unloading_end
        return unloading_end

def simulate_wave(wave: Wave, n_amrs: int = 5, service_time: float = 5.0):
    """
    Simulate one wave. Returns wave completion time (makespan).
    Simplification: AMRs are assigned to orders greedily, FCFS elevator.
    v0.1: same-floor AMR-to-source transitions are free (no intra-floor aisle move).
    """
    elevator = ElevatorResource()
    amrs = [AMR(id=i, current_floor=1, current_time=wave.release_time)
            for i in range(n_amrs)]
    order_finish_times = []

    for order in wave.orders:
        # Phase 1: 选最早空闲的 AMR（平局取 id 最小）
        amr = min(amrs, key=lambda a: (a.current_time, a.id))
        t = amr.current_time

        # Phase 2: AMR 移到 source_floor（只有跨层才用电梯）
        if amr.current_floor != order.source_floor:
            t = elevator.request(amr.current_floor, order.source_floor, t)
            amr.current_floor = order.source_floor

        # Phase 3: pickup
        t += service_time

        # Phase 4: AMR 送到 dest_floor（只有跨层才用电梯）
        if order.source_floor != order.dest_floor:
            t = elevator.request(order.source_floor, order.dest_floor, t)
            amr.current_floor = order.dest_floor

        # Phase 5: dropoff
        t += service_time

        amr.current_time = t
        order_finish_times.append(t)

    return max(order_finish_times) - wave.release_time  # makespan

def generate_random_wave(order_pool: List[Order], wave_size: int, 
                         release_time: float) -> Wave:
    sampled = random.sample(order_pool, wave_size)
    return Wave(orders=sampled, release_time=release_time)
```

### 5.2 `mvs_features.py`

```python
"""Three-dimensional vertical features."""
import math
from collections import Counter

def vertical_concentration(wave) -> float:
    """Shannon entropy over floor distribution (source + dest)."""
    floors = []
    for o in wave.orders:
        floors.extend([o.source_floor, o.dest_floor])
    counts = Counter(floors)
    total = sum(counts.values())
    entropy = -sum((c/total) * math.log(c/total + 1e-9) 
                   for c in counts.values())
    return entropy

def directional_imbalance(wave) -> float:
    """|N_up - N_down| / (N_up + N_down)."""
    n_up = sum(1 for o in wave.orders if o.dest_floor > o.source_floor)
    n_down = sum(1 for o in wave.orders if o.dest_floor < o.source_floor)
    if n_up + n_down == 0:
        return 0.0
    return abs(n_up - n_down) / (n_up + n_down)

def temporal_clustering(wave) -> float:
    """v0.1: all orders released at wave.release_time, so T = 0."""
    return 0.0

def wave_size(wave) -> int:
    return len(wave.orders)

def total_cross_floor_moves(wave) -> int:
    """Baseline feature: how many orders cross floors."""
    return sum(1 for o in wave.orders if o.source_floor != o.dest_floor)
```

### 5.3 `mvs_analysis.ipynb`（主要步骤）

```python
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt

# 1. 生成 1000 个 wave samples
results = []
for i in range(1000):
    wave_size = random.randint(3, 8)
    wave = generate_random_wave(order_pool, wave_size, release_time=0.0)
    makespan = simulate_wave(wave)
    results.append({
        'wave_id': i,
        'size': wave_size,
        'cross_floor': total_cross_floor_moves(wave),
        'C': vertical_concentration(wave),
        'I': directional_imbalance(wave),
        'T': temporal_clustering(wave),
        'makespan': makespan,
    })

df = pd.DataFrame(results)

# 2. 基线模型（只用 size 和 cross_floor）
X_base = df[['size', 'cross_floor']]
y = df['makespan']
m_base = LinearRegression().fit(X_base, y)
r2_base = cross_val_score(m_base, X_base, y, cv=5, scoring='r2').mean()

# 3. 加入 vertical features
X_my = df[['size', 'cross_floor', 'C', 'I']]
m_my = LinearRegression().fit(X_my, y)
r2_my = cross_val_score(m_my, X_my, y, cv=5, scoring='r2').mean()

# 4. 核心判断
improvement = r2_my - r2_base
print(f"Baseline R² = {r2_base:.3f}")
print(f"My method R² = {r2_my:.3f}")
print(f"Improvement = {improvement:.3f}")

# 可视化
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
axes[0].scatter(df['C'], df['makespan'], alpha=0.3)
axes[0].set_xlabel('Vertical Concentration C')
axes[0].set_ylabel('Makespan')
axes[1].scatter(df['I'], df['makespan'], alpha=0.3)
axes[1].set_xlabel('Directional Imbalance I')
axes[2].scatter(df['cross_floor'], df['makespan'], alpha=0.3)
axes[2].set_xlabel('Cross-Floor Moves')
plt.tight_layout()
plt.savefig('mvs_feature_plots.png')
```

---

## 6. 5 天时间表

| 天 | 任务 | 产出 |
|---|---|---|
| Day 1 | 写仿真内核 (mvs_simulation.py) + 跑通单个 wave | 能跑 1 个 wave，输出 makespan |
| Day 2 | 写特征计算 + 生成 1000 samples | `results.csv` |
| Day 3 | 拟合 baseline 和 my method + R² 比较 | 核心数字出来 |
| Day 4 | 可视化 + sanity checks + 边界情况 | 图和 notebook |
| Day 5 | 写 `mvs_results_v0_1.md` 结论总结 | 可以给导师看的 1-2 页报告 |

---

## 7. 避坑清单

### 7.1 不要在 v0.1 做的事

- ❌ 不要做 stochastic 建模 — 留到 v0.2
- ❌ 不要做 multi-elevator — v0.2
- ❌ 不要做复杂的 fleet 路径规划 — 用最简 FCFS
- ❌ 不要做 ALNS 或 metaheuristic — 先验证 surrogate，再做优化
- ❌ 不要做 GUI 或可视化动画 — 浪费时间
- ❌ 不要追求 "真实" 参数 — 只求有 congestion 现象

### 7.2 容易陷入的 trap

- **Trap 1**：代码写得太通用。你写的是 prototype，不是 production system，**越丑越好**
- **Trap 2**：花时间调超参。Linear regression 就够了，不用 XGBoost
- **Trap 3**：被 R² 数字绑架。R² = 0.6 就已经足够说事——不要执着于 0.95
- **Trap 4**：数据太少。1000 samples 是最低限度——如果时间允许跑 5000 更稳

---

## 8. MVS 结果如何影响 Paper 3

**场景 A：R² 提升 > 20%（最好情况）**
- $C$ 和 $I$ 是有力的预测因子
- 你可以直接写进 Paper 3 Section 4：*"preliminary analysis on a 3-floor, 5-AMR, 1-elevator minimal model shows that adding vertical concentration and directional imbalance features improves makespan prediction R² from X to Y"*
- 继续推进 v0.2（引入 $T$、stochastic、multi-elevator）

**场景 B：R² 提升 10-20%（小中之间）**
- 有贡献但不惊艳
- 考虑：是否需要引入非线性特征（$C \times I$、$C^2$）？
- 考虑：$T$（时间集聚）在 v0.2 里能否补足 gap？
- 继续推进但警觉

**场景 C：R² 提升 < 10%（红灯）**
- 你的三维特征假设可能有误
- **不要隐瞒这个结果**——告诉导师
- 可能需要重新思考 feature engineering：
  - 也许不是 Shannon entropy 而是 Gini coefficient
  - 也许需要建模 elevator-specific 而非 global 特征
  - 也许问题的本质不在 wave composition 而在别处
- **这不是研究失败——这是研究必要的调整**

---

## 9. MVS 之后的 Stage 2 规划

一旦 MVS 确认三维特征有预测力，v0.2 应扩展：

**v0.2 (Week 3-4)**：
- 引入多 elevator（E=2 或 3）
- 引入 elevator capacity > 1
- 引入时间集聚 $T$（staggered wave release）
- 放大到 5 层 × 20 AMR × 50 订单
- 与 Chakravarty-style operational baseline 对比

**v0.3 (Month 2)**：
- 引入 stochastic service time
- 实现 ALNS / tabu search 上层优化
- 和 Wu 2024 的 DELO-GA 对比

**v1.0 (Month 3-4)**：
- 工业规模 instance（100-500 订单）
- Case study with company data（如果能拿到）
- 完整的 Paper 3 实验

---

## 10. 最后一句

**记住：MVS 的目的不是做好看的结果，而是快速检验假设**。

如果 R² 提升很大 → 你有理由继续。
如果 R² 提升一般 → 你有理由调整。
如果 R² 提升为零 → 你省了 6 个月。

**这 5 天时间是你整个 Paper 3 里性价比最高的 5 天**。

---

## 11. Log of revisions

- **v0.1 (2026-04-20)**: Initial draft by Claude
- **v0.2 (pending)**: Refined after I actually run the MVS and see results

---

**End of MVS Plan v0.1**