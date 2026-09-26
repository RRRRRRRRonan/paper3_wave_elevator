import pathlib

p = pathlib.Path(r"F:/Paper 3/revision_2026-09-24/section3_finalization_EJOR_edits_2026-09-24.md")
t = p.read_text(encoding="utf-8")
R = []
# ---------- summary ----------
R.append(("**结论：修改 6 项必改后即可定稿。** 其余 28 项为 EJOR 风格与表述准确性的建议，不改变任何公式、编号或结构，可按需取舍。",
          "**结论：修改 6 项必改后即可定稿。** 其余 27 项为 EJOR 风格与表述准确性的建议（另撤回 1 项），不改变任何公式、编号或结构，可按需取舍。"))
R.append(("| 建议·EJOR 风格 | R-01、R-03、R-05、R-06、R-08 至 R-11、R-16 至 R-20、R-22 至 R-24、R-28、R-29、R-31 | 简洁性、句式、标题、术语一致 |",
          "| 建议·EJOR 风格 | R-01、R-03、R-05、R-06、R-08 至 R-11、R-16 至 R-20、R-23、R-24、R-28、R-29、R-31 | 简洁性、句式、术语一致 |\n| 撤回 | R-22 | 3.5 标题保持现状 |"))
R.append(("另：`references_chain_dominance.bib` 中 `so2019calculation` 的 DOI 写作 10.1016/j.jobe.2018.12.018，Crossref 记录为 **10.1016/j.jobe.2019.01.013**（Journal of Building Engineering 22, 549–561），需一并更正。",
          "另：`references_chain_dominance.bib` 中 `so2019calculation` 的 DOI 写作 10.1016/j.jobe.2018.12.018，该号属于另一篇论文；Crossref 记录为 **10.1016/j.jobe.2019.01.013**（Journal of Building Engineering 22, 549–561），需一并更正。根目录全文 docx 的旧 §3（A5 段）有同样的错误归属，不要再复用该段。\n\n"
          "**与 §4 的依赖**：§3 有两处指向 §4 的内容，即 3.4.2 的 \"complementary distributional analysis in Section 4\"（均值型 Wasserstein 比较）和鲁棒选择在评估器有序时的简化结论。二者都在 SECTION_4_METHODOLOGY.md 的 4.4 中，而 Methodology.docx 目前止于 4.3.2。按计划 v0.2 的 S4-2 补齐 4.4 后，这些引用才在 docx 层面成立；§3 本身不需要为此改动。"))
# ---------- R-02 ----------
R.append(("(b) Reservation of one order under the true co-occupancy batching evaluator $M_2$ (Section 3.5.1): the clock of the assigned AMR (availability, readiness, start, pickup, and delivery), the waiting time, and the four phases of the loaded elevator trip (repositioning, loading, travel, and unloading). A request with the same origin and destination floors can join the trip until loading ends at $L_e$. Durations are illustrative.",
          "(b) Reservation of one order under the true co-occupancy batching evaluator $M_2$ (Section 3.5.1). The panel shows the clock of the assigned AMR (availability, readiness, start, pickup, and delivery), the waiting time, and the four phases of the loaded elevator trip (repositioning, loading, travel, and unloading). A request with the same origin and destination floors can join the trip while capacity remains, until loading ends at $L_e$. Durations are illustrative."))
R.append(("(b) 在真实同乘批处理评估器 $M_2$（第 3.5.1 节）下单个订单的预约：被指派 AMR 的时钟（可用、就绪、开始、取货与交付）、等待时间，以及载货电梯行程的四个阶段（空驶调位、装载、运行与卸载）。起点和终点楼层相同的请求可在装载于 $L_e$ 结束之前加入该行程。图中时长仅作示意。",
          "(b) 真实同乘批处理评估器 $M_2$（第 3.5.1 节）下单个订单的预约。图中给出被指派 AMR 的时钟（可用、就绪、开始、取货与交付）、等待时间，以及载货电梯行程的四个阶段（空驶调位、装载、运行与卸载）。起点和终点楼层相同的请求，在容量未满时可于装载在 $L_e$ 结束之前加入该行程。图中时长仅作示意。"))
# ---------- R-03 (both occurrences of the inserted sentence) ----------
R.append(("Formulating the decision over classes ties the release choice to interpretable properties of a wave and gives a release pattern that applies to any candidate pool.",
          "Formulating the decision over classes ties the release choice to interpretable properties of a wave. Because the classes are defined by quantiles within the pool, the same class definitions apply to any pool in which every class is nonempty.", 2))
R.append(("> 插入句：以类别为决策层次，使释放选择对应于波次的可解释性质，并形成一种可用于任意候选池的释放模式。",
          "> 插入句：以类别为决策层次，使释放选择对应于波次的可解释性质。由于类别由池内分位数定义，只要每个类别都非空，同一组类别定义即可用于任意候选池。"))
R.append(("新理由只依赖定义：类别由 $C$、$I$ 两个可解释指标的池内分位数定义，因而对任何候选池都有意义；池内最优只属于一个池。",
          "新理由只依赖定义：类别由 $C$、$I$ 两个可解释指标的池内分位数定义，因而对任何各类别均非空的候选池都有意义（3.3.3 要求每个类别非空）；池内最优只属于一个池。"))
# ---------- R-09 ----------
R.append(("> Given its order set, every permutation of a candidate is equally likely under the generation procedure. Because each candidate keeps its recorded sequence under every evaluator, evaluator comparisons for the same candidate are not affected by sequencing.",
          "> Under the generation procedure, the recorded sequence $\\pi^k$ is equally likely to be any permutation of the order set $W^k$. Because each candidate keeps its recorded sequence under every evaluator, differences between evaluators on the same candidate do not arise from resequencing."))
R.append(("> 在订单集合给定的条件下，候选生成过程使该候选的每一种排列等可能出现。由于每个候选在所有评估器下保持同一记录序列，同一候选在不同评估器之间的比较不受排序影响。",
          "> 在候选生成过程中，记录序列 $\\pi^k$ 等可能地取订单集合 $W^k$ 的任一排列。由于每个候选在所有评估器下保持同一记录序列，同一候选在不同评估器之间的差异并非来自序列的重排。"))
R.append(("中的 selected 易与决策层的\"选择\"混淆。\n",
          "中的 selected 易与决策层的\"选择\"混淆。注意：同一序列仍会影响两个评估器各自的完工时间及其差值（能否同乘取决于请求顺序），所以只能说差异不来自重排，不能说不受排序影响。\n"))
# ---------- R-13 ----------
R.append(("With the mean ready-time offset $\\bar r_W=|W|^{-1}\\sum_{o\\in W}r_o$, $T$ is the coefficient of variation of the offsets:",
          "The mean ready-time offset is $\\bar r_W=|W|^{-1}\\sum_{o\\in W}r_o$, and $T$ is the coefficient of variation of the offsets:"))
R.append(("记平均就绪时间偏移为 $\\bar r_W=|W|^{-1}\\sum_{o\\in W}r_o$，$T$ 定义为各偏移量的变异系数：",
          "平均就绪时间偏移为 $\\bar r_W=|W|^{-1}\\sum_{o\\in W}r_o$，$T$ 为各偏移量的变异系数："))
# ---------- R-14 ----------
R.append(("the first letter records the tail of $C$ and the second the tail of $I$; Section 5 writes the same labels as HC-HI, HC-LI, LC-HI, and LC-LI when it reports per-class results. The candidate-index supports are",
          "the first letter records the tail of $C$ and the second the tail of $I$. Section 5 writes these labels as HC-HI, HC-LI, LC-HI, and LC-LI, respectively. The candidate-index supports are"))
R.append(("第二个字母表示 $I$ 所处的尾部；第 5 节报告各类别结果时，将这些标签依次写作 HC-HI、HC-LI、LC-HI 和 LC-LI。",
          "第二个字母表示 $I$ 所处的尾部。第 5 节将这些标签依次写作 HC-HI、HC-LI、LC-HI 和 LC-LI。"))
R.append(("的对应关系也不清楚。\n",
          "的对应关系也不清楚。第 5 节现有底稿与结果表写作 HC_HI 或 HC·HI，定稿时须统一为 HC-HI（记入 §5 交接）。\n"))
# ---------- R-15 ----------
R.append(("The fraction differs when $C$ and $I$ are dependent or take few distinct values, because the inclusive thresholds in Equation (10) assign every candidate tied at a threshold to the tail set.",
          "The fraction can differ when $C$ and $I$ are dependent. It can also differ when a descriptor takes few distinct values, because the inclusive thresholds in Equation (10) assign every candidate tied at a threshold to the tail set."))
R.append(("若 $C$ 与 $I$ 相关，或描述指标的取值很少，这一比例会发生变化，因为式 (10) 的阈值包含等号，恰好落在阈值上的候选都被划入尾部集合。",
          "若 $C$ 与 $I$ 相关，这一比例可能偏离该值。当某一描述指标的取值很少时，比例同样可能偏离，因为式 (10) 的阈值包含等号，恰好落在阈值上的候选都被划入尾部集合。"))
# ---------- R-19 ----------
R.append(("> This mean is used only in the complementary distributional analysis of Section 4 and its numerical assessment in Section 5; the class-selection objective uses the median.",
          "> This mean enters the complementary distributional analysis of Section 4 and its numerical assessment in Section 5; the class-selection objective uses the median."))
R.append(("> 该均值只用于第 4 节的补充分布分析及其在第 5 节的数值评估；类别选择目标使用中位数。",
          "> 该均值用于第 4 节的补充分布分析及其在第 5 节的数值评估；类别选择目标使用中位数。"))
R.append(("\"The performance of a class is the median makespan\" 重复。\n",
          "\"The performance of a class is the median makespan\" 重复。不写 \"only\"，因为第 5 节还会报告策略层面的均值。本句所指的补充分布分析在 SECTION_4_METHODOLOGY.md 的 4.4.3，尚未并入 Methodology.docx（原句同样依赖这一点，见第 1 节\"与 §4 的依赖\"）。\n"))
# ---------- R-20 ----------
R.append(("> Its two members represent two hypotheses on how elevator capacity acts, as parallel single-request slots under $M_1$ or as shared trips under $M_2$; the robust selection hedges against this structural uncertainty, and Section 4 characterizes the ordering of the two evaluators.",
          "> Its two members represent two hypotheses on how elevator capacity acts: as parallel single-request slots under $M_1$ or as shared trips under $M_2$. The robust selection hedges against this structural uncertainty, and Section 4.3 gives sufficient conditions under which the two evaluators are ordered."))
R.append(("在 $M_2$ 下表现为共享行程；鲁棒选择针对的正是这一结构性不确定性，第 4 节刻画两个评估器之间的排序关系。",
          "在 $M_2$ 下表现为共享行程。鲁棒选择针对的正是这一结构性不确定性，第 4.3 节给出两个评估器有序的充分条件。"))
R.append(("主语错位，移到 $\\mathcal M_D$ 的句子中。\n",
          "主语错位，移到 $\\mathcal M_D$ 的句子中；\"characterizes\" 也言过其实，Methodology.docx 的 4.3 只给出排序的充分条件与反转机制。\n"))
# ---------- R-23 ----------
R.append(("and the request times they generate need not increase along the sequence; Fig. 1(b) illustrates the reservation of one order.",
          "and the request times they generate need not increase along the sequence. Fig. 1(b) illustrates the reservation of one order."))
R.append(("其生成的请求时刻也不必沿序列递增；图 1(b) 展示了单个订单的预约过程。",
          "其生成的请求时刻也不必沿序列递增。图 1(b) 展示了单个订单的预约过程。"))
# ---------- R-25 ----------
R.append(("> Recent multi-robot lift scheduling makes the same single-rider assumption, with each lift serving one robot at a time (Chakravarty et al., 2025).",
          "> Each slot carries one request per trip, the single-rider assumption that Chakravarty et al. (2025) adopt for multi-robot lift scheduling, in which each lift serves one robot at a time."))
R.append(("> 近期的多机器人电梯调度研究采用同样的单乘假设，即每台电梯一次只服务一台机器人（Chakravarty et al., 2025）。",
          "> 每个槽位每趟行程只载一个请求，这与 Chakravarty et al. (2025) 在多机器人电梯调度中采用的单乘假设相同，即每台电梯一次只服务一台机器人。"))
R.append(("若不需要文献锚点，也可直接删除此句。",
          "改写后只把\"单乘\"归于该文，不暗示该文用并行槽位表示容量（该文的电梯容量为 1）。若不需要文献锚点，也可直接删除此句。"))
# ---------- R-26 ----------
R.append(("> The joining request shares the trip's stored completion time, and the car's other reservation quantities remain unchanged. A request may also join",
          "> The joining request shares the trip's stored completion time; apart from the occupancy update in Equation (26), the car's reservation record is unchanged. A request may also join"))
R.append(("加入的请求共享该行程已存的完成时刻，轿厢的其他预约量保持不变。请求也可以加入",
          "加入的请求共享该行程已存的完成时刻；除式 (26) 中的占用数更新外，轿厢的预约记录保持不变。请求也可以加入"))
# ---------- R-27 ----------
R.append(("> $M_2$ shares a trip only among requests with the same origin and destination, a restricted form of the destination-based grouping used in destination group control, where requests from a common origin are assigned to cars according to their destinations until the car capacity is reached (So and Al-Sharif, 2019).",
          "> $M_2$ shares a trip only among requests with the same origin and destination. This is a restricted form of the destination-based grouping of destination group control, in which requests from a common origin are assigned to cars by destination until the car capacity is reached (So and Al-Sharif, 2019)."))
R.append(("> $M_2$ 只在起点和终点都相同的请求之间共享行程，这是目的地群控中按目的地编组的一种受限形式；在目的地群控中，来自同一起点的请求按其目的地分配到轿厢，直至达到轿厢容量（So and Al-Sharif, 2019）。",
          "> $M_2$ 只在起点和终点都相同的请求之间共享行程。这是目的地群控按目的地编组的一种受限形式；在目的地群控中，来自同一起点的请求按目的地分配到轿厢，直至达到轿厢容量（So and Al-Sharif, 2019）。"))
R.append(("需同时把 bib 中该条目的 DOI 更正为 10.1016/j.jobe.2019.01.013。",
          "需同时把 bib 中该条目的 DOI 更正为 10.1016/j.jobe.2019.01.013。Word 中原句的 $M_2$ 公式对象与 \"follows\" 之间没有空格，查找时请搜 \"follows the explicit co-occupancy convention\"。"))
# ---------- R-28 ----------
R.append(("do not overlap, because a new trip begins its empty repositioning at $\\max\\{t,B_e\\}\\ge B_e$, where $B_e$ is the completion time of the previous trip on that car.",
          "do not overlap. Each new trip begins its empty repositioning at $\\max\\{t,B_e\\}\\ge B_e$, where $B_e$ is the completion time of the previous trip on that car ($B_v$ for a slot under $M_1$)."))
R.append(("上预约的行程互不重叠，因为新行程的空驶调位开始于 $\\max\\{t,B_e\\}\\ge B_e$，其中 $B_e$ 为该轿厢上一趟行程的完成时刻。",
          "上预约的行程互不重叠。每趟新行程的空驶调位开始于 $\\max\\{t,B_e\\}\\ge B_e$，其中 $B_e$ 为该轿厢上一趟行程的完成时刻（在 $M_1$ 下为槽位的 $B_v$）。"))
# ---------- R-29 ----------
R.append(("and is not reordered by readiness: an order that is not yet eligible holds",
          "and is not reordered by readiness. An order that is not yet eligible holds"))
R.append(("不会按就绪时间重新排序：尚未具备处理资格的订单", "不会按就绪时间重新排序。尚未具备处理资格的订单"))
# ---------- R-32 ----------
R.append(("> Only the four elevator trip phases carry multipliers. Waiting times change only through the perturbed availability times of the cars, and pickup and drop-off durations remain fixed.",
          "> Only the four elevator trip phases carry multipliers. Waiting times carry none and change only as a consequence of the perturbed durations of earlier trips, while pickup and drop-off durations remain fixed."))
R.append(("> 只有电梯行程的四个阶段带有乘子。等待时间只通过轿厢可用时刻的扰动而变化，取货与卸货时长保持不变。",
          "> 只有电梯行程的四个阶段带有乘子。等待时间本身不带乘子，只因此前行程时长的扰动而间接变化；取货与卸货时长保持不变。"))
R.append(("没有说明扰动作用于哪些时长；与代码一致：噪声只在新行程派车时施加于四个阶段，服务时长不扰动。",
          "没有说明扰动作用于哪些时长。等待时间 $\\max\\{t,B_e\\}-t$ 中的请求时刻 $t$ 与可用时刻 $B_e$ 都会因此前行程的扰动而变化，登乘判断也以扰动后的 $L_e$ 为准。与代码一致：噪声只在新行程派车时施加于四个阶段，服务时长不扰动。"))

for item in R:
    old, new = item[0], item[1]
    cnt = item[2] if len(item) > 2 else 1
    n = t.count(old)
    assert n == cnt, f"expected {cnt}, found {n}: {old[:80]}"
    t = t.replace(old, new)

# ---------- R-22 withdrawn: replace the whole block ----------
start = t.index("#### R-22｜建议·风格｜3.5 各级标题")
end = t.index("#### R-23｜")
t = t[:start] + (
    "#### R-22｜撤回｜3.5 各级标题\n\n"
    "原建议把 3.5、3.5.1、3.5.2 分别改为 \"Operational evaluation and constraints\"、\"Reservation rules and constraints\"、\"Interpretation\"。"
    "撤回理由：EJOR 写作规范的模型模板本身把这一部分称为 \"Constraints\"，主控 §6 也按现标题记录了你确认的结构，现标题可以保留。"
    "若仍想改名，须同步主控，且 3.5.2 宜用 \"Interpretation of the rules\"，不要单用 \"Interpretation\"。\n\n"
) + t[end:]
p.write_text(t, encoding="utf-8")
print("applied", len(R), "replacements + R-22 withdrawal")
