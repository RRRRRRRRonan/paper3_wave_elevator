# Paper 3: Wave × Elevator — Research Workspace

**PhD Paper 3 工作目录**
**Started: 2026-04-20**

---

## 目录结构

```
paper3_wave_elevator/
├── 00_north_star.md        ← 研究方向锚点 (frequently revisited)
├── 01_reading_log.md       ← 论文阅读笔记
├── 02_open_questions.md    ← 待解决的问题
├── 03_decisions.md         ← 已做的决定 + 原因
├── papers/                 ← 下载的 PDF 文献
└── README.md               ← 本文件
```

---

## 使用约定

### 每周必做
- **周一**: 打开 `00_north_star.md`, 回顾本周方向
- **周五**: 更新 `02_open_questions.md` 和 `03_decisions.md`, 做 20 分钟自我 review

### 每读完一篇论文
- 在 `01_reading_log.md` 写一页笔记 (按模板)
- PDF 按命名规范放进 `papers/`

### 每做一个决定
- **立刻**写进 `03_decisions.md`, 不要依赖记忆
- 必须写 Why 和 Revisit If

### 遇到不确定的问题
- **立刻**写进 `02_open_questions.md`, 不要试图当场想清楚
- 带时间戳, 让未来的自己知道这是什么时候的困惑

---

## 版本控制建议

强烈建议用 Git (本地或 GitHub private repo):

```bash
cd F:\paper3_wave_elevator
git init
git add .
git commit -m "Day 1: initial setup"
```

原因: 6 个月后你会想看"当时我怎么想的", commit 历史是最好的记忆。

---

## 未来会添加的子目录

随研究推进自然添加:

```
paper3_wave_elevator/
├── src/                    ← code (Month 1 末开始)
├── data/                   ← 数据 EDA (数据到手后)
├── experiments/            ← 实验结果 (Month 2-3)
├── drafts/                 ← 论文草稿 (Month 6+)
└── figures/                ← 可视化图表
```

---

## 相关文档

- 周计划文档: `Paper1_3Month_Weekly_Plan.docx` (在 Claude 对话中下载)
- PhD narrative: "决策层级上升" (见 03_decisions.md)
