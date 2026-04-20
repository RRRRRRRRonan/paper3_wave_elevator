# Paper 3: Wave Release Coordination with Vertical Resource Constraints

Last updated: 2026-04-20

---

## One-Sentence Description
（这篇论文在做什么？用一句话。）

TODO: 写一句话描述这篇论文的核心研究问题。

参考草稿:
> I study how wave composition decisions in multi-storey AMR warehouses
> should internalize downstream elevator capacity constraints.

---

## The Gap I Fill
（文献里没人做什么？三点对比即可。）

- **Wave planning literature**: 平面 + 人工拣选，不知道 AMR，不知道电梯
- **AMR scheduling literature**: 把 wave 当外生输入，不优化组装
- **ASRS / VLM literature**: 固定基础设施 + 外生需求，不涉及 wave 决策

Nobody sits at the intersection of these three.

---

## My Claim
（我会证明什么？）

TODO: 写出核心 claim。参考草稿:
> Vertical-aware wave composition reduces makespan by X% vs.
> vertical-agnostic baselines, with the largest gains in
> [high imbalance / tight capacity] regime.

---

## Success Criterion
（什么情况下算完成？）

- [ ] MILP model formalized
- [ ] Discrete-event simulation working
- [ ] Metaheuristic outperforming baseline on benchmark instances
- [ ] One case study with company data (if accessible)
- [ ] Submitted to IJPR / TR Part E / Computers & OR by Month 10

---

## Three Risks I'm Tracking

1. **Data availability**: 公司数据申请结果不确定
   - Mitigation: 准备 synthetic instance generator 作为 backup

2. **Scope creep toward Paper 2 (BCCPS)**: 容易滑到结构性理论的诱惑
   - Mitigation: 每次 review 时检查是否偏离 north star

3. **Baseline selection**: 选错 baseline 审稿人会拒
   - Mitigation: Month 2 专门研究 baseline 选择

---

## Fit in My PhD Narrative
（这篇怎么接前两篇？）

- **Paper 1**: 能量资源 operational 决策
- **Paper 2**: AMR 资源 operational 决策
- **Paper 3** (this): 垂直资源 tactical → operational 决策耦合

→ 这是"决策层级的上升"叙事的顶点。

---

## When I Feel Lost, I Re-read This File.
