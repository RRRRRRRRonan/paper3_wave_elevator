---
title: "Section 2: Related Works, v1.0 reconstruction (bilingual: Chinese then English)"
parent: "Wave Release Coordination under Vertical Resource Constraints in Multi-Story AMR Warehouses"
date: 2026-06-19
status: "v1.0 reconstruction. Four problem-class threads (P1-P4) + three methodological threads (M1 bridge, M2 bridge, M3 contrast). Mirrors Abstract/Intro positioning; terminology per paper_draft/TERMINOLOGY.md."
curation: >
  Citation curation from the related-works-curation workflow (run wf_8390048e), with an independent verification pass.
  FIXED: "Nicolas et al. 2018" -> Lenoble, Frein & Hammami (2018); Elmachtoub & Grigas 2020 -> 2022; Vera et al. 2020 -> 2021;
  elevator-RTT cited as opposite-direction CONTRAST only (not support); "Crites & Barto et al." -> "Crites & Barto"; Azadeh survey = 2019 (53(4):917-945);
  surveys 50-year framing anchored on Boysen & de Koster (2025).
  ADDED (verified-real frontier): Liu et al. (2025, C&IE); Tappia et al. (2017, TS); Chen et al. (2023, TRE); Wu et al. (2025, TRE);
  Richer, Bierlaire & Torres (2024, Springer); So, Al-Sharif & Chan (2022) + Al-Sharif et al. (2014) [RTT contrast]; Wan, Lee & Shin (2024, AEI);
  Cheng et al. (2024, ESWA); Mandi et al. (2024, JAIR); El Balghiti et al. (2023, MOR); Sadana et al. (2025, EJOR).
  DROPPED as fabricated attribution (do NOT use): "Khojasteh et al. 2023" (true authors Casella et al.); "Wang et al. 2025" (true authors Silva et al.).
  Full DOIs in references_related_works.bib (to compile).
---

# Section 2. Related Works (v1.0)

## 中文版

我们的研究位于若干成熟文献的交汇处,每一支都触及问题的一部分,却未处理其联合
形态。我们分两步定位:先用近期综述勾勒仓储运筹学的整体图景,再走过四条问题类
研究线(它们的交集定义了我们的空白),最后梳理三条方法论线(两座桥与一处对照)。
三篇综述框定图景:Boysen and de Koster (2025) 以"仓储研究五十年"的视角给出
三代分类,把机器人化配送中心列为当前一代;Boysen, de Koster and Weidinger (2019)
综述电商时代的仓储;Azadeh, De Koster and Roy (2019) 评述机器人化与自动化仓储
系统;Pardo et al. (2024) 给出订单分批问题族的最新分类。在这些综述的范围内,我们
未发现"多层、共享电梯耦合下的波次放行协调"被当作一个独立的问题类,这与我们把
本工作定位为一次形式化的判断一致。

把订单分组当作决策变量、而非仅仅是批量大小,在仓储运筹里有长久传统,但既有工作
几乎都是单层或器件层的。Gademann et al. (2001) 在并行通道仓库中以 makespan 为
目标研究波次拣选;Bozer and Kile (2008) 与 Bartholdi and Hackman (2019) 把该决策
嵌入步行拣选系统;Ardjmand et al. (2018) 以多拣货员最小化拣选 makespan(目标与
我们一致,但单层、无共享垂直资源);Rasmi et al. (2022)、Schiffer et al. (2022)、
Haouassi et al. (2022) 在电商场景下进一步扩展波次与订单行分批。AMR 辅助的变体
扩大了决策类:Scholz, Schubert and Wäscher (2017) 同时求解订单分批、批分配与拣货
员路径;Žulj et al. (2022) 将其提升到 AMR 辅助的人到货系统;Qin, Kang and Yang
(2024) 在单层多托系统中研究、并用"wave"指代处理批,找出最优波次基数。器件层面,
Lenoble, Frein and Hammami (2018) 研究多个垂直升降模块(VLM)内的订单分批,
Boysen, Fedtke and Weidinger (2018) 研究自动分拣的最小订单展开排序;两者的数学
都内生于单一器件,不推广到横跨一支 AMR 机队的多电梯共享运力。最近的 RMFS 分批
工作(如 Liu et al., 2025)同样面向单层拣选吞吐,而非垂直耦合。我们的差别是:在
多层设定下,以结构化表示表达波次构成,使其塑造电梯的垂直行程分布;去掉多层、或
去掉共享电梯,我们的问题就退化为它们的平面子类。

多层机器人移动履行系统(RMFS)与分层穿梭系统让垂直运输显式出现,但通常通过把
穿梭车或料箱限制在单层、或把电梯当作外生队列来解耦各层,且任务集给定。Wu et al.
(2024) 研究四向穿梭系统的入库作业调度;Tadumadze et al. (2023) 研究多层 RMFS 的
订单与料箱到工作站分配;Lamballais, Roy and De Koster (2017) 给出 RMFS 性能的
排队估计。在分层存取系统(SBS/RS)一侧,Tappia et al. (2017) 给出含升降机的多层
紧凑存储的经典排队模型,Chen et al. (2023) 研究双升降机下的检索请求调度以最小化
makespan(这是与我们最接近的已发表类比,但属操作层、任务集给定、且为 SBS/RS 而非
楼面 AMR);更新的整合式工作(Wu et al., 2025)仍是单层内的拣选与补货联合优化。
我们的差别是:把跨层的电梯耦合视为一个上游战术决策(波次构成)可以管理的对象,
而非靠分层解耦来回避。

最接近物理设定的先例把电梯当作争用约束,但波次内容固定。Chakravarty et al. (2025)
用布尔可满足性为 AMR 机队求可证最优的升降调度,其任务集是外生的;Tsai et al.
(2025) 优化智能楼宇的电梯待命策略;Richer, Bierlaire and Torres (2024) 以运筹
框架研究目的地控制下的静态电梯派梯。这些工作在给定到达过程下优化派梯,而我们
优化生成该到达过程的波次。一条平行的研究线通过学习而非形式优化来控制仓库机队:
Crites and Barto (1998) 奠定了电梯群控的强化学习处理,这一线延续至今(交通模式
感知的深度强化学习派梯,Wan, Lee and Shin, 2024;RMFS 批量订单调度的深度强化
学习,Cheng et al., 2024;多机器人任务分配,Ma et al., 2025、Dhanaraj et al.,
2025、Wen and Ma, 2024;以及 AMR 机队强化学习综述,Wesselhöft et al., 2022)。
这些方法在操作层端到端地学习派梯,回答的是与我们不同的问题:它们既不暴露
Bound-and-Gap 那种"结构性与可回收"的分解,也不提供无需训练数据的闭式参照,
因此我们视其为互补而非竞争。最后须指出一处符号上的对照:经典的电梯往返时间
(RTT)文献表明,把同目的地乘客成批运送会减少停靠与往返时间(Al-Sharif et al.,
2014;So, Al-Sharif and Chan, 2022),即按个体建模会高估行程时间;而我们的链支配
方向相反(真实共占批处理弱慢于吞吐抽象)。其符号来源于我们设定下的两条假设,
详见第 4 节。

三条方法论线为我们的两个工具提供根基,前两条经第 4 节的精确等价与之相连,第三条
则是一处结构性对照。第一,预测到决策的遗憾文献界定了当一个学习到的预测器驱动
下游优化器时的损失(Elmachtoub and Grigas, 2022;Vera et al., 2021;Chenreddy
and Delage, 2023);决策聚焦学习的近期综述(Mandi et al., 2024)与预测后优化框架的
泛化界(El Balghiti et al., 2023)进一步刻画了这一损失的可学习性。定理 1 给这一
损失一个分区视角:我们分解中的策略可回收余量恰好等于分区常数预测器的 SPO 损失,
因此既有的决策聚焦方法可将其回收;这是以决策损失、而非已退役的"用结构化表示
预测 makespan"的代理来陈述的。第二,Wasserstein 分布鲁棒优化在以运输距离为半径
的模糊球内对最坏分布对冲,通常重写为凸规划(Mohajerin Esfahani and Kuhn, 2018;
Blanchet and Murthy, 2019;Gao and Kleywegt, 2023;其根基见 Delage and Ye, 2010
与 Bertsimas et al., 2011);Sadana et al. (2025) 的情境优化综述把这两座桥统一在
同一文献框架内。定理 2 与命题 2 表明,我们在 {M1, M2, M3} 上的极小极大波次角
选择与该 Wasserstein-DRO 最优解一致,并在条件链支配下坍缩为一条闭式规则。第三,
模型不确定性下的鲁棒调度(Lu and Shen, 2021;Wiesemann et al., 2013)在单一约定
模型类内对参数变动对冲;我们的电梯建模不确定性在结构上不同(吞吐抽象与真实共占
批处理是定性不同的模型,而非同一族的参数化),Model-Dominance Hedge Rule 处理的
正是这种结构性的模型类不确定性。

综合来看,这四条问题类研究线各自聚焦于波次与电梯耦合的一个侧面;本文把波次构成、
多层部署、灵活 AMR 机队与共享电梯运力的四向交互整合为单一决策问题。前两条方法论
线提供了我们的等价定理所扩展的框架,第三条则把这两个工具与一种竞争性视角区分开。

---

## English version

Our work sits at the intersection of several established bodies of literature,
each touching a part of the problem without addressing its joint form. We
position the contribution in two steps: recent surveys frame the warehouse-OR
landscape, then four problem-class threads whose intersection defines our gap,
and finally three methodological threads (two bridges and one contrast). Three
surveys frame the landscape: Boysen and de Koster (2025) give a fifty-year,
three-generation classification that places robotized distribution centers as
the current generation; Boysen, de Koster and Weidinger (2019) survey
warehousing in the e-commerce era; Azadeh, De Koster and Roy (2019) review
robotized and automated warehouse systems; and Pardo et al. (2024) provide the
most recent taxonomy of the order-batching family. Within the scope of these
surveys we do not find wave-release coordination under shared, multi-story
elevator coupling treated as a standalone problem class, consistent with our
positioning this work as a formalization step.

Treating the composition of an order batch as a decision variable, not merely
its size, has a long tradition in warehouse OR, but almost entirely in planar or
device-level settings. Gademann et al. (2001) study wave picking with a makespan
objective in parallel-aisle warehouses; Bozer and Kile (2008) and the canonical
treatment of Bartholdi and Hackman (2019) embed the decision in walk-and-pick
systems; Ardjmand et al. (2018) minimize order-picking makespan with multiple
pickers (our objective, but single-floor and without a shared vertical
resource); and Rasmi et al. (2022), Schiffer et al. (2022) and Haouassi et al.
(2022) extend wave and order-line batching in e-commerce settings. AMR-assisted
variants enlarge the decision class: Scholz, Schubert and Wäscher (2017) jointly
solve order batching, batch assignment and picker routing; Žulj et al. (2022)
lift it to AMR-assisted picker-to-parts systems; and Qin, Kang and Yang (2024)
study a single-layer multi-tote system, use the word "wave" for processing
batches, and identify an optimal wave cardinality. At the device level, Lenoble,
Frein and Hammami (2018) study order batching across several vertical lift
modules, and Boysen, Fedtke and Weidinger (2018) the minimum order-spread
sequencing problem in automated sorting; the mathematics in both is internal to
a single device and does not generalize to multi-elevator capacity shared across
a horizontal AMR fleet. Recent RMFS batching work (e.g., Liu et al., 2025)
likewise targets single-tier picking throughput rather than vertical coupling.
Our delta is to represent wave composition through Φ in a multi-story setting so
that it shapes the elevator trip distribution; remove the multi-story dimension
or the shared elevator and our problem collapses to their planar subclass.

Multi-story Robotic Mobile Fulfillment Systems (RMFS) and tier-captive shuttle
systems make vertical transport explicit, but typically decouple tiers by
confining shuttles or pods to a tier, or by modeling the lift as an exogenous
queue, with the task set given. Wu et al. (2024) schedule inbound jobs in a
four-way shuttle system; Tadumadze et al. (2023) assign orders and pods to
picking stations in a multi-level RMFS; Lamballais, Roy and De Koster (2017)
give queueing estimates of RMFS performance. On the shuttle-based
storage-and-retrieval (SBS/RS) side, Tappia et al. (2017) provide the canonical
queueing model of multi-tier compact storage with lifts, and Chen et al. (2023)
schedule retrieval requests under two lifts to minimize makespan (the closest
published analogue to ours, but operational, with the task set given, and for
SBS/RS rather than floor-bound AMRs); more recent integrated work (Wu et al.,
2025) still optimizes picking and replenishment within a single tier. Our delta
is to treat the cross-tier lift coupling as something an upstream tactical
decision, wave composition, can manage, rather than decoupling the tiers to
avoid it.

The precedents closest to our physical setting treat the elevator as a contended
constraint under fixed wave content. Chakravarty et al. (2025) compute provably
optimal lift schedules for AMR fleets via Boolean satisfiability, with an
exogenous task set; Tsai et al. (2025) optimize elevator standby strategies in
smart buildings; and Richer, Bierlaire and Torres (2024) give an OR treatment of
static elevator dispatching under destination control. These works optimize lift
dispatch given an arrival process; we optimize the wave that generates it. A
parallel line controls warehouse fleets through learning rather than formal
optimization: Crites and Barto (1998) established the reinforcement-learning
treatment of elevator group control, and the line continues today
(traffic-pattern-aware deep RL dispatching, Wan, Lee and Shin, 2024; deep RL for
batch-order scheduling in RMFS, Cheng et al., 2024; multi-robot task allocation,
Ma et al., 2025, Dhanaraj et al., 2025, Wen and Ma, 2024; and an RL-for-AMR
-fleets survey, Wesselhöft et al., 2022). These methods learn dispatch
end-to-end at the operational layer and answer a different question from ours:
they expose neither the Bound-and-Gap structural-versus-recoverable split nor a
training-free closed-form reference, so we regard them as complementary rather
than competing. Finally, a note on sign: the classic elevator round-trip-time
(RTT) literature shows that batching same-destination passengers reduces stops
and round-trip time (Al-Sharif et al., 2014; So, Al-Sharif and Chan, 2022), that
is, an individual-rider model overstates travel time, whereas our chain
dominance runs the opposite way (true co-occupancy batching is weakly slower
than the throughput abstraction); the sign follows from two assumptions of our
setting, detailed in Section 4.

Three methodological threads ground our two tools; the first two are connected to
them by precise equivalences in Section 4, the third by a structural contrast.
First, the prediction-to-decision regret literature bounds the loss when a
learned predictor drives a downstream optimizer (Elmachtoub and Grigas, 2022;
Vera et al., 2021; Chenreddy and Delage, 2023), with recent decision-focused
-learning surveys (Mandi et al., 2024) and predict-then-optimize generalization
bounds (El Balghiti et al., 2023) characterizing the learnability of that loss.
Theorem 1 gives this loss a partition perspective: the policy slack `M_Φ` of our
decomposition equals the SPO loss of a partition-constant predictor, so existing
decision-focused methods recover it, stated as a decision loss rather than as the
retired Φ-predicts-makespan surrogate. Second, Wasserstein distributionally
-robust optimization hedges against the worst-case distribution within a
transport-distance ambiguity ball, typically reformulated as a convex program
(Mohajerin Esfahani and Kuhn, 2018; Blanchet and Murthy, 2019; Gao and
Kleywegt, 2023; with foundations in Delage and Ye, 2010, and Bertsimas et al.,
2011); the contextual-optimization survey of Sadana et al. (2025) unifies both
bridges within one literature. Theorem 2 and Proposition 2 show that our minimax
wave-corner selection over {M1, M2, M3} coincides with this Wasserstein-DRO
optimum and collapses to a closed-form rule under conditional chain dominance.
Third, robust scheduling under model uncertainty (Lu and Shen, 2021; Wiesemann
et al., 2013) hedges parametric variation within a single agreed model class;
our elevator-modeling uncertainty is structurally different (throughput
aggregation and true co-occupancy batching are qualitatively distinct models,
not parameterizations of one family), and the Model-Dominance Hedge Rule
addresses exactly this structural model-class uncertainty.

Collectively, the four problem-class threads each focus on a different facet of
the wave-elevator coupling; this paper integrates the four-way interaction of
wave composition, multi-story deployment, flexible AMR fleets and shared elevator
capacity into a single decision problem. The first two methodological threads
provide the frameworks our equivalence theorems extend, and the third positions
the tools against a competing approach.
