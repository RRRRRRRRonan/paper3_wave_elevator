---
title: "签字前审查（2026-09-26）：六份待签登记文件"
date: 2026-09-26
method: "多代理审查：6 个独立审查员各查一个维度（文件间一致性、协议对代码、研究一登记对脚本与存档、诚信与披露、签字机制对守卫、清理后的路径与事实引用）；每条发现由 3 个反驳者从事实、重要性、修法三个角度核实（轻微项 1 个）；再由 1 个查漏代理通读六份文件并同样核实。共 96 个代理，全部只读。原始输出：presign_audit_2026-09-26_raw.json（44 条确认、5 条被驳回）。"
status: "审查结论。作者于同日授权全部修改（D-M 保留选项 (a) 并加传播条款）；A1 到 A7 与 B1 到 B14 已全部应用，另按核实代理的二轮意见补了 15 处；全部差异见 presign_fix_diffs_2026-09-26.md，日志见 EXECUTION-LOG 第 49 条"
---

# 签字前审查结论

**结论：六份文件没有阻断性问题，但按现状签字会锁定 7 处实质缺陷（矛盾、不实或可能为假的锁定语句），另有约 20 处小问题一签就改不了。全部是几句话的文字修正，加 3 处代码修正，都在草稿状态下可改。建议先改再签。**

审查员核对了：六份文件互相之间；协议 §4、§5、§7、§9、§11 至 §14 对 phase6_config / phase6_policies / experiments_phase6 / analysis_phase6 / des_evaluator；S1-1 至 S1-12 对各脚本与 prototype/results 存档；守卫解析（模拟签字后 front matter 均可被识别，make_manifest DRAFT 可运行，0 缺失）；清理后的路径。以下按"必须先改"与"建议一并改"分列，编号后括号内为原始发现号。

## A. 必须先改（7 项）

| # | 文件 | 问题 | 改法 |
|---|---|---|---|
| A1 | 决定单 D-M；协议 §7.1、§16 | D-M 允许选 G3 容差 (a) 2% 或改任何门槛数值，但协议 §7.1 写死了 (b) max{2%, 1 s/最优值}，代码 `phase6_config.REGRET_TOL_ABS = 1.0` 也是 (b)。若签 (a) 而不改协议，两份签字件互相矛盾，守卫只核哈希发现不了，代码会按 (b) 跑。（1、4、6、16） | D-M 推荐行后加一句：若选 (a) 或改任何门槛数值，须在同一次签字编辑里同步改协议 §7.1/§7.2 和 `phase6_config.py`（GATES、REGRET_TOL_ABS），签字时两文件必须一致。协议 §16 加对应一句。若你直接签 (b)，现状本身一致。 |
| A2 | 决定单 D-I | I1 一边写"预注册一字不改、哈希可验证"，一边写"签字后可在预注册 §9 末尾追加一行指针（可选）"。追加会使 OSF 上钉住的哈希失配。（2、7） | 删去括号内那句；指针写进稿件的登记附录。 |
| A3 | 协议 §2 | "看过玩具结果后改过的定义"清单漏了一项：G2′ 平局算持平（第二轮审查后改，见 EXECUTION-LOG 第 31 条），且这一项使 G2′ 变松，而此前已见过玩具的 G2′ 上档标签。（5） | 在该行清单中加入 "G2′ ties counted as matches (looser; second review)"。 |
| A4 | 故事契约 C2 | 约束性措辞 "identify the only two reversal mechanisms" 没有对齐前提；方法节和 TERMINOLOGY §7 都只在"序列与 AMR 分配对齐"下证明穷尽。（9） | 改为 "identify the two reversal mechanisms, which are exhaustive under aligned sequences and AMR assignments"，中文同步。 |
| A5 | S1C | 同一文件两种说法：第 1 条 "stable in at least 5 of 6 settings"，第 2 条与代码 "至少 32 对中的 27 对（5/6）稳定"；front matter 说 "adds no design, gate, or reporting rule"，但第 2 条明确新定了细节。（10） | 第 1 条改成与第 2 条和代码一致；status 改为 "adds no gate; fixes the execution details that AMEND-B left open (item 2)"。 |
| A6 | 协议 §7.2 G3 下档 | 锁定句 "closed-form screening is not a reliable pre-filter at shortlist sizes up to 100" 可能为假：下档的定义是"中位 k* ≤ 50 的格子不足 80%"，此时 k* ≤ 100 仍可能在 80% 以上格子成立。（40） | 改为与定义一致的句子，如 "a shortlist of 50 does not suffice in at least 20% of cells"。 |
| A7 | S1A S1-6 | 措辞规则没说 "not stable"/"near tie" 按均值口径还是中位数口径判定；代码两种口径都算，可能不一致。（38） | 写明按中位数口径（第 3 节的决策统计量）判定，均值口径并列报告。 |

## B. 建议一并改（签后就改不了）

- B1 S1C 缺 front matter 签法说明；作者只填正文的 acknowledgement 行则守卫仍拦。加一句 "To acknowledge: set author_signoff to ACKNOWLEDGED (<name>, <date>) and replace the status line"。（3、8、22）
- B2 故事契约 §10 同样缺 front matter 签法说明。（11、34）
- B3 四处 "在仓库根目录运行 make_manifest.py SIGNED" 改为完整命令 `python "revision_2026-09-26_ijpr/archive_package/make_manifest.py" SIGNED`，并加一句：运行后打开 MANIFEST_SIGNED.md，确认每行 signoff 栏以 SIGNED/ACKNOWLEDGED 开头（守卫不认中文弯引号）。（33、37）
- B4 协议 §16 "OSF identifier recorded in the manifest" 不准确：清单没有该字段，且在上传前生成。改为哈希记在清单与 OSF，OSF 编号记在 L2 附录与稿件。（32）
- B5 决定单 D-A：预注册第 213 行只有 "prototype-regime diagnostic"，"partition-relative" 出自主控，不能归到该行。（15、36）
- B6 决定单 D-M (a)："在 8 单波次上最优值约 40 到 60 秒" 无尺度标签且与来源不符；改为 "发表规模 B-2 的两格 8 单最优值为 70 与 38 秒"。（30）
- B7 协议 §2 三个文件名补路径 `revision_2026-07-08/tier2_analysis/outputs/`。（35）
- B8 故事契约 §8 补三条预先规则：案例未做（D-K）时 C3 去掉 "and on a literature-calibrated case"；执行稳健性 "the lower one" 改为 "§7.3 各评估器中最低的档位；G1 按配对的 σ = 0 子样本"；情景 C 下题目不从 §2 三个候选里选。（12、27、28、42）
- B9 RQ 表补 S1-4、S1-6（RQ2）、S1-7、S1-9、S1-11（RQ1）、S2-9（RQ3）；协议 §1 的 RQ 措辞注明以契约为准。（13、44）
- B10 S1B 总则与 S1C "as of the G0 code freeze" 改为 "the code tree hash recorded in MANIFEST_SIGNED.json"（研究一在第 4 周冻结前就要跑）。（14）
- B11 协议 §14 注明 des_subset_mode 空白视为 no；§4 注明空角类的决策不进入 P5 比较；§4 的锚点与预算说明在 max{M1,M2} 键下的读法。（19、21、41）
- B12 S1A：TH-2 输出名作为总则的例外；TH-2 分面改为可得数据（E、F 只取 Block C 与 S1-3 实际覆盖的取值）；TH-2 主句 x 写明取哪些行（Block C 规模 16、按候选去重后的五臂合并）；S1-7 去掉"存档 MV 值作为核对"或改代码实现核对；S1-6 披露写明第六个配置的非正式稳定性未计算。（23、24、25、29、39）
- B13 S1B：S1-12 写明 b5_compat=True 的复现检查隔离了破平修复的影响；S1-2 的 "Corollary 1" 注明所用编号版本。（31、43）
- B14 代码（签字前改，L2 前不受哈希约束）：driver 输出扫描候选数；analysis 把 --allow-code-change 的引用写入 gates.json；max 键下同时输出 M2 键的 companion；S1-11 输出里过期的"守卫读不到勾选框"注释；analysis_phase6 里描述第 2 稿容差的过期注释。（17、18、20、26、16）

## C. 被驳回的发现（5 条，不需处理）

原始 JSON 的 `refuted` 列表；均为审查员误读或已在文件内处理。

## D. 通过的检查（摘录）

六份文件互引的章节均存在；守卫可识别模拟签字后的 front matter（含中文姓名与括号）；`make_manifest.py DRAFT` 在清理后可运行、0 缺失；S1-11 勾选框的标记串与 `require_checkbox` 一致；协议 §5.1 P10、§5.3 P11 规则与 phase6_policies 一致；种子公式、流号、池规模、输出文件名与代码一致；S1-1 至 S1-12 的输入存档均存在；无条目要求改冻结预注册；无禁用表述；情景表 A/B/C 覆盖全部组合。
