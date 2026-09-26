# 第 4 周工作记录（2026-09-27）

签 L2 附录前要看的东西都在这里；每项的来龙去脉见 `../EXECUTION-LOG.md` 第 62 条。

| 路径 | 内容 |
|---|---|
| `g0_2026-09-27/` | 协议 §12 的 G0 第 1 至 7 项：`simulator.log`、`des_evaluator.log`、`phase6_policies.log`；各驱动 `--selftest` 的日志（`selftest_*.log`）；`g0_item6_guard_check.py/.json/.log`（真实模式在守卫处停下的检查：所有抽池、评估、写文件的函数都先换成会报错的替身；另在临时文件上检查 `require_l2` 的 9 种情形）；`code_tree_before_g0.txt` |
| `stage_L2_tune_2026-09-27/` | 训练池调参的真实运行：`tune.log`、开始与结束时刻（UTC）、运行时的代码树哈希、运行前后 `prototype/results/` 的文件清单（只多出 `v0_6_phase6_L2_tuning.json`） |
| `case_data_check_2026-09-27.json` | UCI Online Retail II 的 §11.2 检查：清洗后 1,003,212 行，588 个合格日（每日至少 600 行），各项检查通过；两个工作表在 2010-12-01 至 12-09 重叠 22,523 行且完全相同，去重规则保留第一份 |
| `case_parameters_2026-09-27/` | 案例四个时间参数的查证记录：工作流完整结果（97 条证据及逐条复核结论、两份综合、裁判表）、写进 L2 的取值、`README.md`（与裁判表的一处差异及理由、签字前待你决定的点） |
| `checks/` | 以上检查用的脚本副本；另有研究一脚本注释修正（`fix_s1_docstrings.py` 与记录）和附录 A 的 Word 组装脚本 |

数据文件本身不进仓库，来源、许可与 SHA-256 见 `prototype/data/README.md`。
