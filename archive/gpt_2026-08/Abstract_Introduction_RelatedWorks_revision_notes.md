# 摘要、引言与相关工作：最小修改版审校（沙漏式叙事）

_本版本以“只改必要之处”为原则。除下表明确列出的句子外，原文应当原样保留；仅在文末两处明确标注的情况下提供可选整段替换。说明文字为中文，建议替换进英文论文的句子为英文。_

---

## 🧭 使用规则与审校边界

本文件中的“需改”仅限四类问题：表达存在歧义或难以理解、术语与全文不一致、结论或新颖性表述过强、以及明显破坏沙漏式叙事的重复信息。未列出的原句在语言与叙事上可以保留，不需要为“更优雅”而做同义替换。

“移动”不等同于删除内容：它表示原句可原封不动地从引言移至 Related Works 或方法部分，以减少重复和过早的技术细节。“删除”只用于与后文完全重复的章节元话语或不必要的细节。本文不核验引用文献的事实准确性；如某项文献事实有误，应另行修改。

> 📌 **与完整替换稿的关系：**两份文件采用相同的实质修改原则、术语表、结论限定和“移动”安排。完整替换稿把这些修改整合为可直接阅读和粘贴的连续文本；其中为衔接段落而作的语序调整不构成新增的研究主张或新增的必改项。若两份文字看似不同，应以本文件列出的术语、条件和结论范围为准。

> ⏱️ **时态规则：**Abstract、Introduction，以及本文自身的方法、理论与实验结果，统一使用一般现在时。Related Works 中描述具体既有研究做了什么时，使用一般过去时；领域的一般事实或当前研究状态仍可使用一般现在时。

## 🎯 最小修改下的沙漏式叙事安排

| 章节 | 保留的主线 | 最少需要的结构动作 |
|---|---|---|
| **Abstract** | 工程场景 → 波次决策 → 两项工具 → 实验证据 → 管理含义 | 只改掉绝对化、口语化和未定义术语；保留已有研究主线 |
| **Introduction** | 多层仓储背景 → 波次组成的作用 → 研究缺口 → 研究问题 → 贡献 | 将引言第 3 段中的细粒度文献比较移至 Section 2；将第 4 段的定理/模型细节移至 Section 4 |
| **Related works** | 文献地图 → 问题类文献 → 方法类文献 → 研究缺口 | 删除元叙述，压缩唯一过长的个案说明，并修正方法段的编号逻辑 |

## 🔤 必须统一的术语

以下替换只适用于原文中出现不一致表达的位置；不要求在每一次出现时机械改写。

| 概念 | 统一写法 | 仅在下列情形替换 |
|---|---|---|
| 上游决策 | **wave composition** | 不要与 wave structure、wave content 交替指称同一决策 |
| 特征描述 | **wave profile** Φ(W) | 当 wave structure 指代三维特征表示而非订单组成时 |
| 特征类别 | **wave-profile class** | 当 corner、structure 或 candidate wave 实际指一个特征类别时 |
| 下游执行机制 | **operational dispatch policy** | 当需要明确“固定的下游策略”而非泛称 dispatch 时 |
| 分解的两部分 | **structural upper bound**；**recoverable policy slack** | 不要在同一概念上混用 structural ceiling、fixed value 与 slack |
| 电梯模型 | **conservative co-occupancy batching model** | 首次使用时；不要用 true co-occupancy batching 暗示其他模型不真实 |

wave-release 只作复合形容词使用，例如 wave-release policy；名词短语写作 wave release。

## 📝 Abstract：仅修改以下句子

未出现在本节表格中的摘要句子，包括首句、介绍两项工具的句子和 106,800 次仿真的句子，可以保留原文。

| 原句 | 最小修改建议 | 修改原因（中文） |
|---|---|---|
| “Wave composition (which orders to release together) largely fixes makespan before any AMR moves but has never been treated as a decision variable coupled to shared vertical transport.” | “Before any AMR moves, wave composition (which orders to release together) shapes the elevator demand and, consequently, the makespan; to our knowledge, no formulation treats it as a decision variable coupled with shared vertical transport.” | largely fixes 将复杂的后续执行结果说成几乎完全由波次决定；has never been treated 是难以完全证明的绝对化新颖性主张。修改后保留原结论，但明确作用机制并限定证据范围，同时将本文的叙述统一为一般现在时。 |
| “We formalize this wave-release coordination problem, fix operational dispatch, and group waves by three features: vertical spread, directional imbalance, and temporal clustering.” | “We formalize this wave-release coordination problem, hold the operational dispatch policy fixed, and represent waves by three features: vertical spread, directional imbalance, and temporal clustering.” | fix operational dispatch 没有说明“固定”的对象是策略；represent waves 比 group waves 更准确，因为此处先定义的是特征表示，而非立即分组。 |
| “The Bound-and-Gap decomposition answers what wave composition is worth, splitting it into a structural ceiling no policy can recover and a recoverable slack equal to a predict-then-optimize loss that existing methods can close.” | “The Bound-and-Gap decomposition separates composition-related performance variation into a structural upper bound that a policy cannot recover at the selected representation resolution and recoverable policy slack.” | 原句同时引入价值判断、ceiling、PTO 损失和 existing methods can close 等多层信息，非本领域读者难以理解。这里仅保留分解的核心定义；PTO 等价关系应在 Section 4 说明。 |
| “A resolution theorem shows finer grouping can only raise the ceiling.” | “A resolution theorem shows that finer grouping can only increase the structural upper bound.” | 保留原定理结论，仅将含义不直观的 ceiling 与代词式表达改为已定义术语。 |
| “The Model-Dominance Hedge Rule determines which structure to release when the elevator model is unknown by selecting the one performing best under the most conservative model.” | “When the elevator model is uncertain, the Model-Dominance Hedge Rule selects the wave-profile class with the smallest makespan under the conservative co-occupancy batching model.” | which structure 与 the one 的指代不清，且“最保守模型”未被命名。修改后明确规则选择的对象、比较指标与参照模型，并与全文模型术语统一。 |
| “A dominance theorem (any elevator count, two failure channels) proves this simple hedge minimizes worst-case makespan and equals a calibrated, distributionally robust optimum.” | “Under the stated dominance conditions, the Hedge Rule minimizes worst-case makespan and coincides with a calibrated distributionally robust optimum.” | 摘要无需前置“任意电梯数量、两类失效通道”等证明条件；this simple hedge 也不如规则名称清楚。定理条件保留给方法部分。 |
| “The Hedge Rule passes every gate: dominance holds in 99.2% of matched waves in the six-configuration block, and its selection matches that optimum in all six.” | “The Hedge Rule meets all prespecified validation criteria: dominance holds in 99.2% of matched wave pairs across the six compared configurations, and its selection matches the distributionally robust optimum in all six.” | passes every gate 过于口语化；matched waves 与“成对比较”的实验单位不一致；that optimum 指代不明。同时采用本文结果叙述的一般现在时。 |
| “The decomposition identities hold exactly (72/72), with a partial resolution pass where gaps are small.” | “The decomposition identities hold exactly in all 72 cells; the resolution check is inconclusive only where the estimated gaps are small.” | partial resolution pass 没有定义，无法让读者判断其含义。替换后准确描述低效应量单元中的检验不确定性，并统一为一般现在时。 |
| “The capacity-versus-policy verdict is seed-stable, unanimous in 15/18 configurations.” | “The capacity-versus-policy conclusion is stable across random seeds and unanimous in 15 of 18 configurations.” | verdict 偏口语；seed-stable 对跨学科读者不够直接；本文的实验结论采用一般现在时。 |
| “The two tools inform operators when composing waves pays and when capacity is the lever.” | “The two tools help operators decide whether to improve wave composition or expand elevator capacity.” | composing waves pays 与 capacity is the lever 是口语化隐喻；替换后直接说清两种工程干预。 |

## 📝 Introduction：仅修改或移动以下句子

引言第 1 段无需修改。第 2 段中，除下表列出的两句外，其余句子可以保留。

### 第 2 段

| 原句 | 最小修改建议 | 修改原因（中文） |
|---|---|---|
| “This determines the difficulty of the dispatch problem before any AMR moves.” | “This shapes the difficulty of the dispatch problem before any AMR moves.” | 订单组成会显著影响调度难度，但并不单独决定后续的随机性、执行策略和资源状态；shapes 与摘要中的因果语气一致。 |
| “However, the wave layer is the cheapest place to relieve a vertical bottleneck, because re-batching already-released orders changes neither the layout nor the fleet size.” | “Because re-batching orders before release changes neither the layout nor the fleet size, wave composition can be a low-capital intervention for mitigating vertical congestion.” | cheapest 需要成本数据支撑；而 already-released orders 与波次发布前的决策时点不一致。替换后保留其低资本优势，但不做未验证的成本比较。 |
| “Its benefit is nevertheless not automatic. In some regimes, the limiting factor is elevator capacity itself; in others, better wave composition can reduce avoidable congestion. Distinguishing these cases is necessary before investing in either a new release policy or additional capacity.” | “The operational value of recomposing waves depends on the source of congestion. When elevator capacity is binding, recomposing waves has limited scope to reduce delay. When congestion stems from the pattern of elevator requests, however, a better wave composition can reduce avoidable queueing. Operators therefore need to distinguish these two regimes before choosing between a revised wave-release policy and additional elevator capacity.” | 原句中 Its benefit 的指代较弱，并且从“低资本干预”直接跳到“容量或策略”的二分，因果链不够清楚。替换后先说明价值取决于拥堵成因，再对应两类运行情形和运营决策，逻辑更连贯，也避免暗示波次组成在容量受限时完全无效。 |

### 第 3 段

| 原句/原文位置 | 最小修改建议 | 修改原因（中文） |
|---|---|---|
| “Four elements, namely wave composition, multi-story deployment, flexible AMR fleets, and shared-elevator capacity, have largely been studied in isolation.” | “Wave composition, multi-story deployment, flexible AMR fleets, and shared-elevator capacity are typically studied separately.” | 原句的 largely in isolation 过强；替换后保留研究缺口但降低绝对性。 |
| 从 “The closest precedents treat the lift as a constraint …” 至 “Each of these precedents sidesteps the coupling …” 的四句 | 将这四句**原样移动**至 Section 2 的相应文献线；不要在 Introduction 改写。 | 这些句子不是语言错误，但属于细粒度文献比较，已在 Related Works 更完整地展开。移动而非改写是实现沙漏收束的最小动作。 |
| “In the general setting we study, however, a flexible AMR fleet shares building-wide elevators and wave composition is itself a decision. The two choices then cannot be separated: the chosen wave fixes the elevator trip distribution … so optimizing wave composition and fleet dispatch in isolation loses the bottleneck interaction that matters.” | “In the setting studied here, a flexible AMR fleet shares building-wide elevators and wave composition is itself a decision. Because the chosen wave shapes the resulting elevator-trip distribution before dispatch, wave composition and fleet dispatch cannot be optimized independently.” | 原文第二句过长，包含三层括号解释，并再次使用 fixes。拆分后不改变论证，只提高可读性和术语一致性。 |
| “We therefore formalize the intersection of these four elements as the wave-release coordination problem under vertical resource constraints; Section 2 details the precedents.” | 保留原句。 | 该句有效地完成缺口到研究问题的收束；不需要为润色而改写。 |

### 第 4 段

| 原句/原文位置 | 最小修改建议 | 修改原因（中文） |
|---|---|---|
| 从 “Two structural features motivate the tools.” 至 “Corollary 2 provides a computable worst-case bound …” | 将此部分**原样移动**至 Section 4，在两个工具分别被正式定义之后；不要在 Introduction 中改写。 | 该段没有明显语言错误，但在研究问题尚未被充分吸收时，过早引入分解、候选模型、支配关系、最小最大结论和最坏情形界。这是叙事位置问题，不是同义改写的问题。 |
| “The two tools act on the same decision (which wave-structure to release): the first measures how much that choice is worth and how much of it a wave-release policy can recover, and the second uses the reference model to select the robust one.” | “The two tools act on the same decision: the first quantifies the recoverable value of wave composition, and the second selects a robust wave-profile class under model uncertainty.” | which wave-structure to release 与全文的 wave composition/wave-profile class 不一致；worth 与 the robust one 也较口语和含混。 |

### 贡献 C1–C3

其余贡献句在保留定理和实证信息方面是有效的；只修改下列确有问题的句子。特别是 C3 必须先点明其贡献是“容量—策略诊断”，再给出仿真规模和验证结果；不要以 “Third, we evaluate …” 或实验设置作为贡献段的开头。

| 原句 | 最小修改建议 | 修改原因（中文） |
|---|---|---|
| C1 中：“Its four defining elements … have been studied only in isolation, with wave content or request set fixed or transport confined to a single device or tier; our formulation models the coupling explicitly.” | “Related studies typically fix wave content or request sets, or confine transport to a single device or tier; our formulation models the coupling explicitly.” | only in isolation 属于过强的新颖性主张；同时前半句重复列举四个要素，可删去而不损失贡献定义。 |
| C2 开头只写 “We develop two analytical tools for this decision.” | “Second, we develop two complementary analytical tools for wave-release coordination. The Bound-and-Gap decomposition is diagnostic: it quantifies how much composition-related performance variation is structurally constrained and how much a better wave-release policy can recover. The Model-Dominance Hedge Rule is prescriptive: it selects a robust wave-profile class when the elevator model is uncertain.” | 仅声明“开发两项工具”无法让读者立即理解 C2 的贡献。替换后先明确两项工具分别提供诊断价值与稳健决策价值，再进入符号、定理和等价关系。 |
| C2 中：“It splits the value of wave structure, GAP, into a structural ceiling H^up that no wave-release policy on Φ can recover and a recoverable slack M_Φ …” | “It separates GAP into a structural upper bound H^up that a wave-release policy cannot recover at the selected Φ resolution and recoverable policy slack M_Φ …” | 统一 wave structure、ceiling 与 slack 的术语；补入“在所选表征分辨率下”这一关键条件，避免把不可恢复性表述为无条件结论。 |
| C2 中：“We show that M_Φ equals the predict-then-optimize decision loss … so the slack can be recovered with existing methods.” | “We show that M_Φ equals the predict-then-optimize decision loss … thereby linking the slack to existing decision-focused methods.” | can be recovered with existing methods 容易被理解为现有方法保证完全恢复余量；修改后只陈述已证明的联系，不外推方法效果。 |
| C2 中：“Under this dominance, minimax corner selection collapses to the corner optimal under true co-occupancy batching …” | “Under this dominance, the minimax wave-profile-class selection reduces to the class that is optimal under the conservative co-occupancy batching model …” | corner 与 true 均不利于非专业读者理解，且前者与正文统一术语不一致。 |
| C3 开头仅以实验设计或仿真规模引入 | “Third, we provide an empirical capacity-versus-policy diagnosis that identifies whether, in a given operating regime, a revised wave-release policy or additional elevator capacity offers the more effective intervention.” | C3 的核心贡献不是“完成了一组仿真”，而是为运营者提供容量与策略之间的诊断依据。将该价值主张前置，随后再用预注册实验和理论检验作为证据，才能保持贡献度清晰。 |
| C3 中：“In these warehouses, under the pre-registered wave grouping and the median metric, capacity is the binding side.” | “Under the pre-registered wave grouping and the median metric, elevator capacity is the binding constraint in our experiments.” | binding side 不是自然的学术表达，且 In these warehouses 容易被理解为一般性结论。修改后限定为实验发现，并保持本文结果的一般现在时。 |
| C3 中：“Its statistical test resolves a nonzero value of wave composition in 57 of the 72 cells, which we report as a partial pass.” | “Its statistical test detects a nonzero composition-related effect in 57 of the 72 cells; the remaining cells are inconclusive because the estimated effects are small.” | resolves a nonzero value 与 partial pass 不够透明。替换后明确统计含义，避免通过/失败式表述。 |
| C3 中：“Together, the tools tell an operator, regime by regime, when smarter wave composition pays and when the lever is instead more capacity or a finer grouping.” | “Together, the tools indicate, by operating regime, whether the more effective intervention is improved wave composition, additional elevator capacity, or a finer wave representation.” | pays 与 lever 口语化；finer grouping 应明确是表征分辨率，而不是随意重新分批。 |

## 📝 Related works：仅修改或移动以下句子

除下表内容外，相关工作中的文献线、引用集合和大多数比较句均可保留原文。本文不建议因“压缩”而删去正常的学术定位句。

### 段落叙事顺序与段首主旨句

为使 Related Works 的叙事可见，每段应先说明该段在论证中的功能，再用既有文献作为证据。除段首句外，保留当前段落中的文献集合和具体比较。整体顺序为：文献地图 → 三类工程决策边界 → 两类方法学基础 → 唯一研究缺口。

| 段落 | 段落功能（中文） | 建议的英文段首主旨句 |
|---|---|---|
| P1 | 区分三条运行决策文献线与两条方法学文献线，并预告后文的展开顺序。 | “Relevant literature for this study comprises three operational streams—wave composition, vertical transport, and downstream dispatch—and two methodological streams—decision loss and information refinement, and model uncertainty. The review first delineates the scope of the three operational streams and then discusses the methodological foundations for the two analytical tools used in this study.” |
| P2 | 说明波次组成已被研究，但未处理共享电梯需求。 | “First, warehouse-operations research examined wave composition as a decision problem, but did not model its consequences for shared-elevator demand in a flexible AMR fleet.” |
| P3 | 说明多层系统已建模垂直运输，但通常将需求集视为既定。 | “Second, research on multi-story robotic mobile fulfillment systems (RMFSs) and multi-tier shuttle systems modeled vertical transport, but typically treated the task set as given before operational decisions were optimized.” |
| P4 | 说明最接近的调度研究优化下游响应，而不改变上游需求。 | “Third, research closest to the present physical setting optimized elevator or robot operations under exogenous demand rather than altering that demand through wave composition.” |
| P5 | 说明 Bound-and-Gap 分解的理论来源。 | “The Bound-and-Gap decomposition draws on a methodological stream that examined decision loss and information refinement.” |
| P6 | 说明 Hedge Rule 的理论来源及其与模型不确定性的关系。 | “The Model-Dominance Hedge Rule draws on a complementary methodological stream that addressed decisions under model uncertainty.” |
| P7 | 收束为唯一缺口，并过渡到本文定位。 | “Taken together, these streams leave unresolved the upstream coupling between wave composition and shared vertical capacity.” |

### 开头段

| 原句 | 最小修改建议 | 修改原因（中文） |
|---|---|---|
| “We position the contribution in two steps: recent surveys frame the warehouse-OR landscape, then four problem-class threads … and finally three methodological threads …” | “Relevant literature for this study comprises three operational streams—wave composition, vertical transport, and downstream dispatch—and two methodological streams—decision loss and information refinement, and model uncertainty. The review first delineates the scope of the three operational streams and then discusses the methodological foundations for the two analytical tools used in this study.” | 原句只是章节写作说明；替换后按后文实际段落明确区分“三条运行决策文献线 + 两条方法学文献线”，并预告其展开顺序。 |
| “Within the scope of these surveys, we do not find wave-release coordination under shared, multi-story elevator coupling treated as a standalone problem class …” | “Across these streams, the upstream coupling between wave composition and shared, multi-story elevator capacity appears to receive limited direct attention.” | 将穷尽性的“no prior study”改为“appears to receive limited direct attention”。这保留研究缺口，但不把文献检索表述为绝对结论，语气更符合审慎的学术写作。 |

### 订单分批段

| 原句 | 最小修改建议 | 修改原因（中文） |
|---|---|---|
| “Our delta is to represent wave composition through Φ in a multi-story setting so that it shapes the elevator trip distribution; remove the multi-story dimension or the shared elevator and our problem collapses to their planar subclass.” | “The present study represents wave composition through Φ in a multi-story setting, where it shapes the elevator-trip distribution; without the multi-story dimension or shared elevators, the setting reduces to a planar subclass.” | our delta 和 collapses 偏口语或对立式；替换后仅改变措辞，不改变与平面文献的比较逻辑。 |

### 多层系统段

| 原句/原文位置 | 最小修改建议 | 修改原因（中文） |
|---|---|---|
| 从 “A recent exception to tier confinement is Wang et al. (2025) …” 开始、详述其算法的长句 | 替换为：“Wang et al. (2025) relaxed tier confinement by jointly scheduling retrieval requests, shuttles, and two shared lift types to minimize makespan. Its retrieval-request set was nevertheless exogenous, whereas our study treats wave composition as an upstream tactical decision.” | 原句几乎复述了他人的完整系统、算法和设备细节，篇幅显著失衡。两句即可说明该研究为何是最接近的例外，以及与本文的关键差异；既有研究使用一般过去时。 |
| “Our novelty is to treat the cross-tier lift coupling as something an upstream tactical decision can be managed by wave composition rather than as a contention that must be rescheduled after the request set is finalized.” | “Our contribution is to manage cross-tier lift coupling through upstream wave composition, rather than only rescheduling contention after the request set is finalized.” | 原句的 as something an … decision can be managed by 语法拗口；同时将 novelty 改为更审慎的 contribution。 |

### 电梯控制与学习方法段

| 原句/原文位置 | 最小修改建议 | 修改原因（中文） |
|---|---|---|
| “These methods learn dispatch end-to-end at the operational layer and answer a different question from ours: they expose neither the Bound-and-Gap structural-versus-recoverable split nor a training-free closed-form reference, so we regard them as complementary rather than competing.” | “These methods learned operational dispatch, whereas our framework changes the demand pattern through wave composition. The approaches are therefore complementary: they optimized the downstream response, while our decomposition evaluates the value of an upstream decision.” | 原句把本文的特殊工具作为评价其他 AI/RL 方法的标准，且信息密度过高。替换后只说明两类方法处于不同决策层级，论证更中性；对既有研究的描述使用一般过去时。 |
| 从 “Finally, a note on sign: the classic elevator round-trip-time (RTT) literature …” 至该句末尾 | 将此句**原样移动**至 Section 4 的模型假设说明处。 | 该句讨论本文支配结论为何与经典 RTT 文献符号相反，属于模型机理与假设解释，不是文献定位所必需的信息。 |

### 方法文献段

| 原句/原文位置 | 最小修改建议 | 修改原因（中文） |
|---|---|---|
| “Proposition 3 gives this loss a partition perspective …” 与 “Theorem R gives this monotonicity an exact form …” | 将这两句**原样移动**至 Section 4 的相应命题/定理介绍之后。 | 这些句子说明的是本文定理的具体形式，而非外部文献与本文的关系。移动后 Related Works 会更聚焦。 |
| “Second, Wasserstein distributionally robust optimization …” | 将开头改为：“A second methodological connection is Wasserstein distributionally robust optimization …” | 前文已经在 First 段中插入了信息细化的补充关系；使用 A second methodological connection 可避免读者误以为编号遗漏。 |
| “Third, robust scheduling under model uncertainty …” | 将开头改为：“Finally, robust scheduling under model uncertainty …” | 这样与前述 first 和 second 形成闭合结构，消除当前编号与段落组织之间的冲突。 |

## 🧩 可选的整段替换：仅用于结构重构

严格按最小修改原则时，请采用前文的逐句替换和“移动”建议；不要再同时使用本节的整段替换。以下仅为两处真正具有结构性问题的备选方案：当你希望不逐句移动原文，而是以更短、更连贯的段落完成沙漏式叙事收束时使用。

摘要不需要整体重写，使用前文的逐句替换即可。Related Works 也无需重写其文献证据和引用集合；但应采用前述七个段首主旨句，使“文献地图 → 工程决策边界 → 方法学基础 → 研究缺口”的叙事结构清晰可见。

### Introduction 第 3 段：可选整体替换

**适用情形：**你希望将当前第 3 段的文献举例全部留给 Section 2，并用一个简短段落直接完成“研究缺口”的收束。

> Existing studies address important parts of this setting. Order-batching research determines which orders are processed together, multi-story robotic fulfillment studies model vertical transport, and elevator-control studies optimize dispatch under congestion. However, these streams generally fix either the order set, wave content, or transport domain. The unresolved upstream decision is wave composition in a system where a flexible, floor-bound AMR fleet competes for shared freight elevators. Because wave composition shapes the elevator-trip distribution before dispatch begins, it cannot be optimized independently of the vertical bottleneck.

**对应中文翻译（仅供理解，不放入英文论文）：**

> 现有研究已经处理了这一场景中的若干重要部分。订单分批研究决定哪些订单被共同处理，多层机器人履约研究刻画垂直运输，电梯控制研究则在拥堵条件下优化调度。然而，这些研究通常将订单集、波次内容或运输范围中的至少一项视为既定。尚未解决的上游决策，是在柔性、受楼层限制的 AMR 车队竞争共享货运电梯的系统中进行波次组成。由于波次组成会在调度开始前塑造电梯行程分布，因此它不能与垂直瓶颈割裂开来单独优化。

### Introduction 第 4 段：可选整体替换

**适用情形：**你希望把定理条件、候选模型和技术证明全部留给 Sections 3–4，只在引言中保留研究设计与两个核心问题。

> We study wave-release coordination as a two-stage decision problem. At the tactical stage, the operator composes a wave; at the operational stage, a fixed operational dispatch policy assigns AMRs and manages elevator trips. We represent each wave by a three-feature wave profile, $\Phi(W)$: vertical spread, directional imbalance, and temporal clustering. This representation supports two tasks: quantifying the variation in makespan that a better wave-release policy can recover and selecting a wave-profile class under elevator-model uncertainty. The Bound-and-Gap decomposition addresses the first task, and the Model-Dominance Hedge Rule addresses the second. Formal definitions, assumptions, and proofs are provided in Sections 3 and 4.

**对应中文翻译（仅供理解，不放入英文论文）：**

> 本文将波次释放协调研究为一个两阶段决策问题。在战术阶段，运营者决定如何组成波次；在运营阶段，固定的运行层调度策略分配 AMR 并管理电梯行程。我们以包含三个特征的波次画像 $\Phi(W)$ 刻画每个波次：垂直跨度、方向失衡和时间聚集度。该表征支持两项任务：量化更优波次释放策略能够恢复的完工期变化，并在电梯模型不确定时选择波次画像类别。Bound-and-Gap 分解处理第一项任务，Model-Dominance Hedge Rule 处理第二项任务。形式化定义、假设和证明将在第 3 节和第 4 节给出。

## ✅ 不需要修改的内容

以下内容在当前稿中已有效承担其功能，不建议为“润色”而改变：摘要首句的物理场景设定；摘要中 “Two tools … answer two operator questions.”；摘要中的预注册仿真规模句；引言第 1 段；引言第 3 段末句；引言的章节路线图句；以及 Related Works 中大部分按问题类别排列的引文句。

也不建议把 Introduction 或 Related Works 整段改写为全新文字。上文标记的移动和少量替换，已经足以使引言收束得更快、相关工作更聚焦，同时保留原稿大部分事实、引用与论证顺序。
