# Reading Log: Boysen & de Koster (2025)

**Full citation**: Boysen, N., & de Koster, R. (2025). 50 years of warehousing research — An operations research perspective. *European Journal of Operational Research*, 320(3), 449–464. DOI: 10.1016/j.ejor.2024.03.026. **Open Access** (Creative Commons).

**Placement**: `F:\paper3_wave_elevator\papers\reading_log_boysen_dekoster_2025.md`
**Read date**: 2026-04-24（stub drafted by Claude，**PDF 仍未在 papers/ 目录内 — 精读 pending**）
**Relevance rating for Paper 3**: ⭐⭐⭐⭐⭐（authoritative positioning anchor; Q1 审稿人大概率引用）
**Status**: **STUB — PDF 未到位，精读 pending**

> ⚠ **2026-04-24 更新**：用户尝试 download 此 PDF，但实际保存到 `papers/` 里的文件是 **Boysen, Schneider & Žulj (2025) "Energy management..."** —— 是**另一篇综述**。详见 [reading_log_boysen_schneider_zulj_2025.md](reading_log_boysen_schneider_zulj_2025.md)。
>
> **当前 Paper 3 §1.2 已按 lean-intro 原则移除对此篇的 hook**（不依赖此 anchor）。用户完成下载后，精读本篇 + 按下面 §6.1 三情形定稿 §3 Related Work 的 anchor wording 即可。

---

## ⚠ 为什么这份 log 是 stub

两件事必须用户精读后才能定稿：

1. **情形 A/B/C 判定**（见 §6.1）：综述是否提到 multi-storey AMR wave composition 作为 open agenda？这决定 §1.2 和 §3 Related Work 里引用这篇的 positioning wording。本 stub 为三种情形都准备了候选 wording，用户精读后勾选即可。
2. **§4.3 的具体引用页码/章节**：综述里如果有讨论"robotized DC"或"future research"的具体段落，需要页码定位。

精读推荐路径：先读 Abstract + §1 + 最后一个"research agenda"或"outlook"章节；次读三代分类的定义；其余略读即可。**预计 2–3 小时**。

---

## 1. Problem

**他们在做什么？**

50 年仓储 OR 综述。把仓储系统的演化拆为**三代**（从公开 abstract 与作者此前工作推断，精读后校对）：

- **第一代 (basic systems)**：传统 man-on-board AS/RS、公共仓库，结构固定，OR 问题偏 storage assignment + routing
- **第二代 (extended system setups)**：mini-load / SBS-RS / 多设备集成；引入并行 setup、batching
- **第三代 (state-of-the-art robotized distribution centers)**：RMFS / G2P / AMR fleets / robot-arm pick

**他们解决什么问题？** 不是新建模型；他们**整理 OR 视角的文献脉络**，并给出 future warehousing generations 的 research agenda。

**为什么重要？** *EJOR* 是 warehousing OR 的权威期刊，两位作者（Boysen 与 de Koster）在 warehousing/distribution OR 方向的综述被引量领先。对 Paper 3，这**不是一篇可以忽略的文献** — 它是 positioning 的权威锚点，审稿人几乎必然引用它。

---

## 2. Method

综述性论文，method 即文献组织方法：

- 三代分类框架（来自 abstract：basic → extended → robotized）
- 每代内按 OR 问题类（storage assignment / order picking / job scheduling / layout）组织
- 最终给出 research agenda，指向 "future warehousing generations"

精读时请确认：三代的具体分界线（按时间？按 enabling technology？按 OR problem class？）以及 research agenda 是**总结式**还是**processive（明确 open problem 列表）**。

---

## 3. Result

综述无独立 "result"。需要精读后回答三个具体问题：

- **Q1**：三代分类的具体定义是什么？（引用页码）
- **Q2**：robotized DC（第三代）讨论是否包含 multi-storey deployment？有无 elevator / vertical coupling？
- **Q3**：research agenda 列出的 open problems 是什么？"wave composition"、"multi-storey AMR"、"elevator-fleet coupling" 有无被点名？

---

## 4. Relevance to my Paper 3

### 4.1 Positioning 功能（不是方法借鉴）

这篇**不提供方法借鉴** — 它是综述，不建模。它的功能是：

- 给 Paper 3 一个 **authoritative reference** 来挂接"为什么 multi-storey AMR warehousing 是一个 research class 而不是 ad-hoc 场景"
- 让 §1.2 / §3 Related Work 能引用**warehousing OR 领域权威**的 classification

### 4.2 不引用的代价

如果 Paper 3 不引用 Boysen & de Koster 2025，审稿人**几乎肯定**会提："你们为什么不参考最近 EJOR 的仓储综述？"这对 C&IE / TRE / EJOR 都是负分。

---

## 5. What I can borrow

**Classification language**：如果综述用了"three generations"分类，Paper 3 可以在 §1.2 或 §4.1 里借用这个语言，把自己定位在第三代（robotized DC）内一个具体的、尚未成熟的子类上（multi-storey AMR）。

**Taxonomy hook**：如果综述把 warehousing 研究分成 layout / storage / picking / scheduling 几大块，Paper 3 的 wave-release coordination 应定位为 "picking + scheduling 的耦合子类"。

---

## 6. What I must differentiate from

### 6.1 必须写进 Paper 3 Introduction 的 wording（**精读后从以下三选一**）

**情形 A — 综述 explicitly flags multi-storey AMR wave composition 作为 open agenda**：

> "Boysen and de Koster (2025) explicitly identify multi-storey AMR warehousing with wave-scale tactical coordination as an open research agenda for future warehousing generations. This paper provides the first systematic treatment."

**情形 B — 综述 mentions multi-storey / AMR generally but not wave composition specifically**：

> "Boysen and de Koster (2025) position robotized distribution centers as the state-of-the-art warehousing generation and flag deployment-scale coordination problems in AMR fleets as an open direction. This paper addresses one such problem: tactical wave release under shared elevator capacity."

**情形 C — 综述 does not mention multi-storey AMR at all**：

> "The recent *EJOR* survey by Boysen and de Koster (2025) covers 50 years of warehousing OR research through the robotized-DC generation. Multi-storey AMR deployments as an independent research class have emerged only in 2024–2025 (see Wang 2025; Yang 2025 *TRE*; Qin, Kang, Yang 2024 *TRE*), post-dating the survey's coverage. This paper is among the first to treat the associated tactical wave-composition problem."

**Action**: 用户精读后在此文件 §9 revision log 里记录选定的情形 + 对应 wording。Paper draft `§1.2` 的挂接句以对应版本为准。

### 6.2 审稿人质疑的预案

**Q**: "Boysen & de Koster 2025 综述里既然没提到 multi-storey AMR wave composition，是不是说明这个问题不重要？"

**A**（**情形 C 下使用，情形 A/B 不需要这条**）：综述发表于 2025 年，覆盖 2024 年前的文献。Multi-storey AMR warehousing 作为**独立 research class** 是 2024–2025 才成型的（cite Wang 2025, Yang 2025 *TRE*, Qin et al. 2024 *TRE*）。Paper 3 是这个新兴 class 里**第一次系统处理 wave composition 作为 tactical decision variable** 的工作。综述未覆盖反映的是 problem class 刚浮现的事实。

**Q**: "你这篇是不是只是综述 research agenda 里的一个数据点？"

**A**: 不。Paper 3 提供的是 *framework*（Bound-and-Gap + Hedge Rule），不只是一个 case study。即使把场景换成 multi-tier shuttle 或 multi-floor RMFS，framework 仍可迁移。综述 flag 的 direction 是 problem class；Paper 3 提供的是 domain 内的 theoretical + empirical apparatus。

---

## 7. Open questions about their work

1. Three-generation taxonomy 的确切定义（需精读 §1 或 §2）
2. Research agenda 的具体措辞 — 是否点名 "multi-storey" / "vertical coupling" / "wave-release"
3. Future generation 指向是否主要是 AI / autonomy / sustainability，还是结构（如 multi-storey）？
4. 对 2024 年文献的覆盖深度 — 是否已包括 Qin 2024 *TRE*、Yang 2025 *TRE*

---

## 8. Key takeaways

- ⭐ **权威锚点，不可绕过** — 即使综述未点名 Paper 3 的具体问题，也必须引用并 position。
- 精读优先级：**Abstract → Conclusion / Research Agenda → Three-Generation 定义** → 其余略读。
- §6.1 wording 必须**精读完成后**才能写进 paper 正文；在此之前 paper §1.2 / §3 引用这篇时请用**中性占位句**（"a recent EJOR survey traces warehousing evolution across three generations"），避免 overclaim。

---

## 9. Log of revisions

- **v0.1 (2026-04-24)**: Stub by Claude，bibliography + open-access 状态 verified via WebSearch；§4/§5/§6.1/§7 标为 TODO。
- **v0.2 (pending, user)**: 精读后选定 §6.1 情形 A/B/C，定稿 wording；回填 §3 具体 finding。

---

**End of Boysen & de Koster 2025 reading log v0.1 (stub)**
