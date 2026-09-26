# 03 Decisions Log

所有我已经做的决定 + 为什么。

每个决定必须包含:
- **When**: 什么时候决定
- **What**: 决定了什么
- **Why**: 原因
- **Revisit If**: 什么触发条件下应该重新评估

**原则**: 过去的自己做的决定, 未来的自己会忘记原因然后纠结。
写下 Why 是对未来自己最大的善意。

---

## [2026-04-20] Paper 3 topic: Wave × Elevator

- **What**: Paper 3 做 wave release coordination with vertical resource constraints
- **Why**:
  - 方法论门槛在现有技能框架内 (PDPTW + metaheuristic + 仿真)
  - Framing 原创, 交通社群潮汐车道不直接覆盖
  - 有工业背景支持, 数据路径清晰
- **Rejected alternative**: BCCPS/Framing B (结构性理论)
  - 原因: MDP 结构性分析需要 18-24 个月积累, 单人攻坚风险大
  - 保留为 Paper 4 或 postdoc 方向
- **Revisit if**:
  - 找到合适 co-author 且导师明确支持
  - 时间预算允许一年零产出

## [2026-04-20] PhD Narrative: "决策层级上升"

- **What**: 三篇论文按决策层级构建统一叙事
  - Paper 1 = operational (energy)
  - Paper 2 = operational (fleet)
  - Paper 3 = tactical + operational (wave + fleet + elevator)
- **Why**: 能自然串联三篇, 展示方法论成熟度递进
- **Rejected alternative**: "平面→立体" 叙事
  - 原因: 把 novelty 锚定在"多层"这个物理特征上, 弱化了真正的贡献
- **Revisit if**: 导师或委员会明确反对这个 framing

## [2026-04-20] 工具链选择

- **Language**: Python
- **MILP Solver**: Pyomo + Gurobi (学术版)
- **Simulation**: SimPy
- **Metaheuristic**: 先 ALNS (已熟悉)
- **Visualization**: matplotlib + seaborn
- **Why**: 全部在现有技能栈, 学习曲线短
- **Revisit if**: 数据规模超出 Gurobi 学术版限制 (2000+ variables)

## [2026-04-20] 与 Paper 1, Paper 2 的接口

- **What**: Paper 3 不显式包含充电约束 (Paper 1) 和经典任务分配 (Paper 2)
- **Why**: 避免 scope creep, 让 Paper 3 focus 锐利
- **How to connect**: 在博士论文 Chapter 1 做 unified framing,
  而不是在 Paper 3 本身承担连接责任
- **Revisit if**: 审稿人要求 Paper 3 显式与 Paper 1/2 对比

---

## 新增决定 (写在这下面)
