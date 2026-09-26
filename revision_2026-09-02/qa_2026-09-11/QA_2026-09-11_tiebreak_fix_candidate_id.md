# QA 记录 2026-09-11：tie-break 生产修复、空角类报错、[RA] median 敏感性、candidate_id 补齐

证据标签：本记录内所有内容为 `[QA]`（bug 修复、等价重跑、代码审计）或 `[RA]`（对既有数据的重分析）。按 `MASTER_REVISION_BY_SECTION.md` §0.3，二者都不能改变 2026-05-19 主预注册的任何门槛判定；本记录也没有改变任何判定。

授权范围：作者于 2026-09-11 要求执行代码动作 1、2、3、5（生产模拟器 tie-break 修复并重跑 Block C 与 smoke；空角类回退改报错；Block C 分析并列报告 median 口径 Hedge 选角；保存 `candidate_id`）。未触及 `Problem formulation.docx`、`SECTION_3_MODEL_FORMULATION.md` 或任何论文正文。未执行 git 提交。

## 1. 代码改动

| 文件 | 改动 | 自检 |
|---|---|---|
| `prototype/src/simulator.py` | 新增 `_earliest_unit(units)`：按 `(available_at, 列表索引)` 取最早可用单元；替换原 `min(..., key=(e.available_at, id(e)))` 的 5 处（`ElevatorPool.request` 的 slot 选择，以及 Batched / StochasticBatched / Directional / BatchedHeterogeneous 四个池的 dispatch 车选择）。模块 docstring 加注日期与 bug report 引用。 | `python -m src.simulator`：全部手算目标与回归子测试 `[OK]` |
| `prototype/src/wave_policies.py` | `corner_positions`：空角类由"静默回退到全池"改为 `ValueError`。 | `python -m src.wave_policies`：全部 `[OK]`。全尺度 72 个 Block A cell、6 个 Block C cell 与 smoke 的 24 个角类 cell（大小 15 至 49）均非空，报错分支从未触发。 |
| `prototype/src/experiments_phase5.py` | Block A / B / C 三个 runner 的每一行新增 `candidate_id`（被抽候选在候选池中的行位置，等于池内 `wave_id`）与 `cand_seed`（候选池生成种子）。仅追加列，seed 流与仿真语义不变。 | 由 §2 的再生对比验证：规定列对齐、数值仅在平局位置变化 |
| `prototype/src/experiments_phase5_supp.py` | Supp-1 / Supp-2 runner 同样新增两列。 | 未重跑（Supp 结果不在本次范围） |
| `prototype/src/analysis_phase5_blockC.py` | (a) 可选命令行参数 `[csv_path] [out_json]`，默认仍为预注册 CSV/JSON，使再生结果可并列分析而不覆盖存量；(b) 新增 `[RA]` 块：按类 median 重算 Hedge 选角，与预注册的 mean 口径 D2-d 并列输出（JSON 键 `RA_median_hedge_sensitivity`）；(c) `generated` 改为运行日期，新增 `source_csv`、`analysis_note`。门槛逻辑一字未动。 | 在存量 CSV 上重跑后，`H_D2` 与 `H_D3_exploratory` 两棵子树与 git HEAD 版本逐项相同 |

`prototype/results/v0_5_phase5_blockC.json` 因此被重新生成：判定内容与原文件相同，仅新增上述三个键。原文件可由 git HEAD 取回。

## 2. B-14 生产侧再生（`regen_blockC_smoke_tiebreakfix.py`）

再生对象与 2026-07-08 登记的 B-14 范围一致：Block C（6 个 E=2 配置、size 16、五臂、M1/M2/M3 同波次）与预注册 §7 smoke 切片。种子流与 2026-05-19 相同，唯一差别是修复后的 tie-break。存量文件未覆盖：Block C 再生写入 `results/raw/mvs_v0_5_phase5_blockC_tiebreakfix.csv` 与 `results/v0_5_phase5_blockC_tiebreakfix.json`；smoke 再生写入本目录 `smoke_tiebreakfix/`。

### 2.1 逐行对比（同一 config、arm、wave_id）

| Block C 列 | 行数 | 变化行 | 占比 | 差值范围 | 变化行按 config |
|---|---|---|---|---|---|
| makespan_M1 | 6000 | 0 | 0 | 无 | 无 |
| makespan_M2 | 6000 | 33 | 0.55% | −100.0 至 +43.0 | 1: 19，5: 8，7: 6 |
| makespan_M3_s20 | 6000 | 40 | 0.67% | −70.9 至 +21.6 | 1: 19，3: 3，5: 7，7: 10，9: 1 |

M1 逐行相同，与 2026-07-08 bug report 的 C-4 重建检查（M1 12,000/12,000 复现、M2 约 0.27% 敏感）方向一致；本次 M2 敏感比例略高于当时估计（0.55% 对 0.27%），说明存量运行时的堆顺序在不同 wave 间并不一致。

### 2.2 预注册门槛并列

| 项目 | 存量（2026-05-19） | 修复后 | 判定变化 |
|---|---|---|---|
| D2-a 逐波 M2 ≥ M1 平均 | 0.9921 | 0.9925 | 否（与 B-14 harness 侧结果完全一致） |
| D2-a 最差 cell | 0.960 | 0.960 | 否 |
| D2-b FOSD cell 数 | 24/24 | 24/24 | 否 |
| D2-c U_c < 5% m0 cell 数 | 24/24 | 24/24 | 否 |
| D2-d Hedge = DRO（mean） | 6/6 | 6/6 | 否 |
| H-D2 判定 | PASS | PASS | 否 |
| mean 口径 Hedge 选角（config 1/3/5/7/9/11） | LC_HI, LC_HI, HC_LI, LC_HI, HC_HI, LC_LI | 同左 | 否 |
| H-D3（探索性）qmax / qmin 不变配置数 | 2/6，5/6 | 2/6，5/6 | 否 |
| H-D3 平均 Spearman rho | 0.750 | 0.767 | 否（分支仍为 model-sensitive） |
| [RA] median 口径 Hedge 与 mean 口径一致 | 5/6 | 5/6 | 否 |

### 2.3 smoke 切片

| 项目 | 结果 |
|---|---|
| Block A 切片（600 行） | 键列对齐；0 行 makespan 变化；`favorable_corner` 逐 cell 相同 |
| Block B 切片（420 行） | 键列对齐；4 行变化（0.95%，差值 −24.9 至 +1.0） |
| S1 至 S4 与 PROCEED 判定 | 与存量 `v0_5_phase5_smoke_verdict.json` 逐叶相同（排除日期字段后差异为 0） |

### 2.4 运行时间与哈希

| 项目 | 值 |
|---|---|
| Block C 再生用时 | 1.7 s（18,000 次仿真） |
| smoke 再生用时 | 0.3 s |
| `simulator.py` 修复前（git HEAD）sha256 前 16 位 | 7ccd2a27a64b2809 |
| `simulator.py` 修复后 | afecac238c330a55 |
| Block C 存量 CSV | a48215591c8b7ae5 |
| Block C 修复后 CSV | 3097715b6d9c4cd4 |
| smoke A 存量 / 再生 | d888fe061f294db5 / a0cd5aa9f90ac0ad（再生文件多两列，数值全同） |
| smoke B 存量 / 再生 | a53c2466d8088d5f / f10d20dc5feda4ac |

完整对比 JSON：`b14_production_equivalence.json`。

## 3. [RA] median 口径 Hedge 敏感性

预注册 D2-d 在 `analysis_phase5_blockC.py` 中以类均值计算（DRO 侧本身是均值型）；预注册原文只写 `c*_DRO == c*_Hedge`，未指定统计量。§3 现稿以类 median 为决策统计量，故并列重算：

| config | Hedge(mean) = DRO | Hedge(median) | median 口径最优与次优差距 |
|---|---|---|---|
| 1 | LC_HI | LC_HI | 2.29% |
| 3 | LC_HI | LC_HI | 5.59% |
| 5 | HC_LI | HC_HI | 0.96% |
| 7 | LC_HI | LC_HI | 1.04% |
| 9 | HC_HI | HC_HI | 0.84% |
| 11 | LC_LI | LC_LI | 0.14% |

存量与修复后数据给出相同的表。用法约束：

- 预注册 D2-d 继续以 mean 口径、`[PR-C]` 标签报告 6/6；本表以 `[RA]` 标签并列报告 5/6，config 5 在 1% 边际内翻转。
- 这是续审 4.2.3 所要求的"U_c 需加角点排序 margin 条件才能推出选择不变"的实证例子，可作为 §5 中 Cor. 2 边界条件的展示。
- 预注册修正案 A3 禁止以"median 更稳健"为由辩护中位数，只能以 Theorem 1 一致性辩护；统计量的选择不得因本表而改变。

## 4. candidate_id 补齐（`reconstruct_candidate_ids.py`）

存量 2026-05-19 的 Block A/B/C CSV 不含候选索引。由于每次抽样都来自 `experiments_phase5._seed` 的登记种子流，回放抽样 RNG 即可无仿真地恢复每一行的候选索引。输出 sidecar（`row_index` 为存量 CSV 中的 0 基行号）：

- `results/raw/mvs_v0_5_phase5_blockA_candidate_ids.csv`（72,000 行）
- `results/raw/mvs_v0_5_phase5_blockB_candidate_ids.csv`（16,800 行；附 `favorable_corner_stored` 与重拟合 `favorable_corner_refit`）
- `results/raw/mvs_v0_5_phase5_blockC_candidate_ids.csv`（6,000 行）

对齐验证：按 sidecar 重建 wave，在修复后的模拟器上再仿真，与存量 makespan 比较；残余不一致再以"反向索引破平"再仿真一次。E=2 时一个 wave 内的堆顺序只能是正向或反向，因此若不一致完全由反向破平复现，则它是已知的平局效应而非对齐错误。

| Block | 再仿真行数 | 不一致 | 反向破平完全复现 | 说明 |
|---|---|---|---|---|
| A（M1，每 arm-cell 3 行） | 540 | 0 | 不适用 | M1 逐行相同 |
| A（M2，每 arm-cell 3 行，两组抽样） | 540 + 540 | 1 + 0 | 1/1 | 平局效应 |
| B（M2，每 policy-cell 10 行） | 840 | 9 | 9/9 | 平局效应；重拟合的 favourable corner 与存量 84/84 相同；P6 的重拟合树复现全部抽查行 |
| C（M1，每 arm-cell 3 行） | 90 | 0 | 不适用 | |
| C（M2，每 arm-cell 5 行） | 150 | 4 | 4/4 | 平局效应，集中于 config 1 |

每 200 行 cell 的唯一候选数：Block A 78 至 200（含 random 臂）、Block B 124 至 198、Block C 116 至 198。续审 4.2.7 所述"每个 200 行 cell 只有约 78 至 169 个唯一 wave"得到复核。

完整验证 JSON：`candidate_id_reconstruction_check.json`。

## 5. 未做与待作者决定

1. **Block A/B 是否在修复后全量重跑。** 成本只有数秒，但不在 B-14 登记范围内，且 H-D1 现为 57/72 对门槛 58/72，任何一个 cell 的变化都会改变判定。若要做，应先以日期化说明把 B-14 扩展到 Block A/B，并事先写明"无论结果如何，稿件采用修复后数字并并列报告旧判定"，再运行。本次未运行。
2. **稿件 Block C 数字的口径。** B-14 的锁定规则是"稿件采用修复后模拟器的数字并加日期化说明"。建议 §5 的 Block C 数字切换到 `_tiebreakfix` 工件（D2-a 平均 0.9925、H-D3 rho 0.767），存量工件保留为溯源。
3. **聚类 / 去重重分析（Phase 2）。** `candidate_id` 已就位，行级 bootstrap 的重做尚未执行。
4. **§5 披露文字。** 需写入：tie-break 缺陷与修复日期、Block C 的 0.55% / 0.67% 暴露、Block A/B 的状态、median 口径 5/6 的并列报告。

## 6. 本次新增或修改的文件

- 修改：`prototype/src/simulator.py`、`wave_policies.py`、`experiments_phase5.py`、`experiments_phase5_supp.py`、`analysis_phase5_blockC.py`；`prototype/results/v0_5_phase5_blockC.json`（判定不变，新增 RA 键）；`MASTER_REVISION_BY_SECTION.md` §0.2 两条审计事实与 §12 Phase 1/2 三个清单项。
- 新增：`prototype/results/raw/mvs_v0_5_phase5_blockC_tiebreakfix.csv`、`prototype/results/v0_5_phase5_blockC_tiebreakfix.json`、三个 `*_candidate_ids.csv`；本目录下两个脚本、两个验证 JSON、`smoke_tiebreakfix/`。
