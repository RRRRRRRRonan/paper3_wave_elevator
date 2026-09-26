# 登记文件副本（2026-09-26；now/ 已是签字后的版本，与 MANIFEST_SIGNED.json 一致）

**先读这一段。** `now/` 里现在是六份**已签字**登记文件的只读副本（2026-09-26 签字后刷新，哈希与 `archive_package/MANIFEST_SIGNED.json` 一致），可直接作为 OSF 上传集使用；`later/` 是另外两份文件（2026-09-27：L2 附录已签字；数学核验记录已录入）。原件才是守卫读取的文件，副本仅供阅读、打印和上传。登记守卫 `prototype/src/registration_guard.py` 和 `make_manifest.py` 只读取下表"原件路径"中的文件：签在副本上不起作用，登记脚本仍会被拦下，哈希清单也不会记录它。副本已设为只读，以防误签。

## 现在要签（now/）

| 顺序 | 副本 | 原件路径（在这里签） | 签字时要做的 | 复制时原件 SHA-256（前 16 位） |
|---|---|---|---|---|
| 1 | `now/01_DECISIONS_TO_SIGN.md` | `revision_2026-09-26_ijpr/01_DECISIONS_TO_SIGN.md` | D-A 到 D-M 逐条写"同意推荐"或改选项（重点 D-D、D-H、D-J 选 J4、D-K、D-L、D-M 的 G3 二选一）；文末签名与日期 | `787656291d715d88` |
| 2 | `now/STORY_CONTRACT.md` | `revision_2026-09-26_ijpr/STORY_CONTRACT.md` | 通读（中英对照，以英文为准）；文末签名与日期 | `18a76d1e96a25008` |
| 3 | `now/phase6_method_study_protocol.md` | `paper_draft/phase6_method_study_protocol.md` | §16 勾两个框（L1 设计与门槛锁定；D-K、D-L 按决定单）；签名与日期 | `a92d93c1a1cbe900` |
| 4 | `now/AMEND-2026-09-26-S1A_reanalyses.md` | `revision_2026-09-26_ijpr/amendments/AMEND-2026-09-26-S1A_reanalyses.md` | 文末签名与日期 | `00f03ff20c640f3f` |
| 5 | `now/AMEND-2026-09-26-S1B_new_simulations.md` | `revision_2026-09-26_ijpr/amendments/AMEND-2026-09-26-S1B_new_simulations.md` | 文末签名与日期；勾 "S1-11 included: yes / no"（与 D-D 一致） | `5141174f587c106f` |
| 6 | `now/AMEND-2026-09-26-S1C_execution_note_B4_B6.md` | `revision_2026-09-26_ijpr/amendments/AMEND-2026-09-26-S1C_execution_note_B4_B6.md` | 只需确认：填 "Author acknowledgement"，front matter 可写 `ACKNOWLEDGED` | `59e12d3ab5dcb833` |

## 以后再签（later/）

| 副本 | 原件路径 | 什么时候 | 复制时原件 SHA-256（前 16 位） |
|---|---|---|---|
| `later/phase6_protocol_L2_addendum.md` | `paper_draft/phase6_protocol_L2_addendum.md` | 2026-09-27 已签字（按你的指示录入），并由 `MANIFEST_SIGNED_L2.json` 钉住；副本已换成签字后的版本 | `891e727e9759de96` |
| `later/MATH_VERIFICATION_LOG.md` | `revision_2026-09-26_ijpr/MATH_VERIFICATION_LOG.md` | 2026-09-27 第 4 至 12 行已按你的指示录入，命题 3 已改名定理 1（副本已刷新）。不属于登记签字 | `45fdc54a00165ea4` |

## 签法（在原件上，每个文件一次编辑完成）

1. 填好内容、勾好框。
2. 把 front matter 的 `author_signoff` 改为 `"SIGNED (你的名字, 日期)"`（S1C 可写 `ACKNOWLEDGED (...)`）。
3. 改掉 `status` 行。

全部签完后，在仓库根目录运行 `python "revision_2026-09-26_ijpr/archive_package/make_manifest.py" SIGNED`，再按 `archive_package/README_OSF.md` 上传 OSF（选禁运）。生成签字清单后，原件一个字节都不要再改。可以分批签，每批重新生成清单时加 `--supersede`。

## 副本会过时

- 原件在签字前若再有改动，副本不会跟着变：用上表的哈希核对（`sha256sum <原件>`）。
- 签字后这些副本仍是 PENDING 版本，已经过时。届时可以删掉整个 `to_sign_copies/` 文件夹，或让助手按签字后的原件重新生成一套（例如作为 OSF 上传包，其哈希应与 `MANIFEST_SIGNED.json` 一致）。
- 副本设了只读属性；如需去掉：在 PowerShell 中运行 `Get-ChildItem "revision_2026-09-26_ijpr\to_sign_copies" -Recurse -File | ForEach-Object { $_.IsReadOnly = $false }`。

`revision_2026-09-26_ijpr/amendments/README.md` 属于上传包，但不需要签字，未复制。
