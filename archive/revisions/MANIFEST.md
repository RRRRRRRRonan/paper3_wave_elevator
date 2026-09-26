---
title: "Revision 历史快照归档清单"
date: 2026-09-03
status: "ARCHIVED — 可恢复，只存不取"
---

# Revision 历史快照归档清单

## revision_0719_snapshot

- 原位置：`F:\Paper 3\revision_0719`
- 当前归档位置：`F:\Paper 3\archive\revisions\revision_0719_snapshot`
- 归档动作：整体移动；没有删除或改写快照内容。
- 完整性：67 个文件，共 4,068,145 bytes；移动前后文件数与总字节数一致。
- 折叠理由：40 个文件与 `paper_draft/manuscript` 或 `revision_2026-07-08` 的权威来源 SHA-256 完全一致；其余 27 个为 README、`edits_from_global`、`original_docx_*`、PDF 或章节包装溯源件。审计未发现独有科学结果。

## 当前唯一施工链

| 内容角色 | 活跃入口 |
|---|---|
| 全文逐章修订与冲突裁决 | `revision_2026-09-02/MASTER_REVISION_BY_SECTION.md` |
| W1–W10 理论与章节底稿 | `revision_2026-07-08/tier1_manuscript/` |
| 表格素材 | `revision_2026-07-08/tables/` |
| 图与制图脚本 | `revision_2026-07-08/figures/` |
| 当前 Abstract、Introduction、Related Works 文字底稿 | `paper_draft/manuscript/` |

归档快照只用于追溯七月章节包装过程，不再作为正文、表格、图片或结论的施工来源。快照内部的旧相对路径可能仍指向原目录结构，因此审计时应优先依据本清单回到活跃入口。

## 恢复方式

如确需恢复，可在确认根目录不存在同名 `revision_0719` 后，将整个 `revision_0719_snapshot` 移回 `F:\Paper 3\revision_0719`。该操作只是目录回移；归档过程未丢弃任何文件。
