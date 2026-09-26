# 09_References 更新清单

- `references_chain_dominance.bib` + `references_related_works.bib`，合并后统一 author-year（APA 类）样式渲染，DOI 全部保留为永久链接。
- 提交前核验（bib 文件头部自带 flag + W10 §6.2）：
  1. Chaudhry-Templeton ISBN、Sorsa 2012 数字声明 —— 逐条复核。
  2. Wang et al. (2025)：五作者（Wang, Tao, Chen, Zhu, Yang），*C&IE* 210:111559，DOI 10.1016/j.cie.2025.111559 —— 已按 Crossref 核对，出版社页面再确认一次。**2026-07-31：条目 `wang2025retrieval` 已补入 related_works.bib**（此前 W7 Edit 5 只落了正文没落 bib）；条目暂以姓氏占位，**提交前必须到出版社页面补全五位作者的名**（禁止猜名——本项目有过伪造署名教训）。
  3. 新增：Song & Luedtke (2015, SIAM J. Optim., DOI 10.1137/140967337)（Theorem R 类比）；Boysen & de Koster (2025)（通读后定引用位置）。
  3b. **2026-07-31 新增三项**（related_works_v1.1 已在正文引用，bib 需补条目）：① `blackwell1953equivalent`（Blackwell 1953, comparison of experiments）；② `song2015adaptive`（同上第 3 条，正文已落 §2）；③ **Wu 2024 四向穿梭车**——§2 同时引用 Wu et al. (2024) 与 Wu et al. (2025，Jiabin Wu），bib 目前只有 wu2025joint；需补 2024 条目，并确认两位 Wu 首字母是否相同（若同为 J.，按 APA 需全名消歧，§1 的 "J. Wu et al., 2025" 写法届时统一）。
  3d. **2026-08-06 全量核验完成（缺口清零）**：51 条 §2 文中引用逐条审计，31 条缺失条目经 5 路网络核验工作流（wf_4f2e56d7，逐条 Crossref/出版社页面确认）后全部补入 related_works.bib（现共 52 条目，无重复键）。三项连带修正：① "Chenreddy & Delage 2023" 不存在 → 文中改 "Chenreddy et al., 2022"（NeurIPS 35，三作者）；② `wu2025joint` 署名纠错（Jingwen Wu/Zhiyuan Yang/Wenxin Li/Yiran Ren，旧条目名全错）；③ 两位 Wu 消歧（Z. Wu 2024 = Zhaoyun，Processes 12(1):223 已建条 `wu2024inbound`；J. Wu 2025 = Jingwen），§2 文中已按 APA 写 "Z. Wu et al. (2024)" / "J. Wu et al. (2025)"，**§1 引言里的 "J. Wu et al., 2025" 因此确认正确、无需改**。遗留待办：新条目中带 % PROSE CAUTION / % CONFIRM 注释的逐条过一眼（Qin"single-layer"措辞、Chakravarty"provably optimal"措辞、Ma"state-of-the-art"措辞、Gademann 荷兰姓氏大小写、Bozer 全名、Wang 五作者全名、boysen2025fifty 标题、chen2023retrieval 题名、vera2021online DOI）。
  3c. **2026-07-31 缺口审计结果**：`tadumadze2023assigning`（FSMJ 35:1038-1075，DOI 10.1007/s10696-023-09491-0）此前两个 bib 均缺，已补入 related_works.bib（Springer 页面核验）；共用条目住 chain-dom bib 的有 lamballais2017estimating、so2019calculation、kuusinen2012study、santi2014quantifying——合并渲染时勿重复键。剩余唯一缺口 = Wu 2024（见 3b③）。
  4. 全部 DOI 重跑一遍有效性 + 检查 editorial notices（撤稿/更正）。
