> 提取说明：本文件由 `Wave Release Coordination under Vertical Resource Constraints in Multi.docx` 自动提取（2026-07-19），仅用于修订对照。Word 公式（OMML）被压平成行内文本，格式细节以 docx 为准。


## Problem Formulation

We consider a multi-story fulfillment warehouse with F floors connected by E shared freight elevators. A fleet of ∣A∣ floor-bound autonomous mobile robots (AMRs) handle horizontal travel on each floor; floor-to-floor transfers go through the elevators, with each elevator carrying at most c AMRs per trip. Orders arrive over a planning horizon, each with a known source floor, destination floor, and release time. A wave is a subset of orders released into the system simultaneously at the start of a release window of length Δ. The system performance metric is the wave makespan: the time at which the last order in the wave is delivered, given a fixed operational dispatch policy.

This setting decomposes naturally into two coupled decision layers. The tactical layer chooses which orders to bundle into a wave W, namely the wave composition decision; this is the focus of our analysis. The operational layer determines, given W, which AMR serves which order, which AMRs board each elevator trip, and in what order. We delegate these decisions to a deterministic dispatch policy, defaulting to capacity-bounded FIFO boarding under the elevator model M∈M, with full simulator details given in Section 4. We model only the wave-composition decision as a formal variable; downstream AMR-elevator execution is a simulator-realized policy. This simplification is deliberate: the wave-elevator coupling is fully captured by Φ(W) at the partition resolution on which our analytical tools operate; finer partitions reveal additional structure within Φ-cells, a property formalized as the refinement monotonicity result of Corollary 1 in Section 4. Operational lift scheduling is well studied (Chakravarty et al., 2025); the upstream wave layer that prior work treats as exogenous is formalized in this paper.

### Sets and indexes

O: set of all orders over the planning horizon, indexed by o.

F={1, 2, .., F}: set of floors, indexed by f.

A: AMR fleet, indexed by a.

E: set of elevators, indexed by e.

Wω: sequence of waves over the planning horizon, indexed by ω.

M=M1, M2, M3: elevator-model set, indexed by m.

### Parameters

All parameters below are deterministic under elevator models M1 and M2. Under M3, the timing primitives (τs, τe, τd) become lognormally perturbed with scale σ{M3}∈{0.10, 0.20}. Numerical values are reported in Section 5.

Warehouse and fleet:

F∈Z≥2: number of floors

A: AMR fleet size

E: number of elevators

c∈Z≥1: per-trip elevator capacity

Timing primitives:

τs∈R>0: per-event AMR service time at pickup or dropoff

τe∈R>0: per-floor elevator travel time

τd∈R>0: elevator dwell time per stop

Operator-set release controls:

Wmin, Wmax∈Z≥1: wave cardinality bounds

τω∈R>0: release window start of wave ω

∆∈R>0: release window length

Order attributes (input data):

so∈F: source floor of order o

do∈F: destination floor of order o (same-floor orders with do=so are admissible; they contribute no elevator demand and are excluded from the IW computation)

ro∈R≥0: release time of order o

### Decision variable

The model has a single decision variable, the tactical wave composition.

xo∈0, 1, ∀o∈O: wave-inclusion indicator, with xo=1 if order o is released in the current wave.

The wave composition is the induced set W={o∈O: xo=1}.

### Assumptions

The formulation rests on five assumptions, each stated explicitly, so the scope of validity is identifiable.

A1. Single-order AMR carriage. Each AMR transports at most one order at a time. This aligns with industry practice for parcel-scale fulfillment and rules out multi-tote AMR variants(Qin et al., 2024).

A2. Source-before-destination sequencing. For each served order o, the assigned AMR visits the source floor so before the destination floor do.

A3. Capacity-bounded FIFO boarding. AMRs join the elevator queue in arrival order and board up to c at a time under the elevator model M.

A4. Intra-floor travel collapsed into service time. AMR horizontal travel within a floor is summarized by the per-event service time τs, with no explicit congestion or routing on the floor.

A5. Elevator model is a fixed property of the warehouse, unknown to the operator at decision time. The elevator model M∈M is a structural property of the physical elevator subsystem (its boarding logic and trip-time aggregation), exogenous to the wave-composition decision. Because the warehouse OR literature uses both throughput-aggregation (Bartholdi & Hackman, 2019) and co-occupancy batching (Chakravarty et al., 2025), we do not commit to a single convention.

### Structured-feature representation

We summarize each candidate wave by a three-dimensional fingerprint ΦW=(CW, IW, T(W)), a function of the decision {xo}, on which the analytical tools of Section 4 operate. The three axes each capture a distinct physical mechanism of vertical resource stress.

Vertical activity diversity CW≥0. Shannon entropy (natural logarithm) of the empirical floor distribution taken over the union of source and destination floors of orders in W. With pfW=o∈W:so=f+o∈W:do=f2W, we define CW=-f∈FpfWlnpf(W), with 0ln0=0. High C indicates that orders span many floors (diversified vertical activity); low C indicates concentration on a few floors.

Directional imbalance I(W)∈[0, 1]: It measures how one-directional the cross-floor traffic is. With W↑=o∈W:do>so and W↓=o∈W:do<so (same-floor orders excluded from both), IW=W↑-W↓W↑+W↓ when W↑+W↓>0, and IW=0 otherwise.

Temporal clustering T(W)≥0: It is the coefficient of variation of per-order release times, measured relative to the wave’s release-window start. TW=σr(W)μr(W). High T means orders arrive in tight bursts; low T means they spread evenly across the window.

The three axes capture conceptually distinct mechanisms: multi-floor spread, up-versus-down asymmetry, and temporal bunching, each with a clear physical meaning. We treat Φ as a conceptual decomposition rather than a predictive surrogate.

### Elevator models

The dispatch policy is realized through a simulator under one of three elevator models:

M1(throughput aggregation): Each elevator is modeled as a server with a per-AMR throughput rate that incorporates batched-trip efficiency into a single multiplier.

M2(true co-occupancy batching): At each elevator, the next c AMRs in the queue board together and ride as a unit, with realistic per-trip capacity, dwell time, and direction handling.

M3 (stochastic batching): It extends M2 with lognormal noise on per-trip duration at scale σM3, used for robustness sensitivity.

M1 and M2 are both well-attested in the warehouse OR literature; the structural disagreement between throughput aggregation and explicit co-occupancy is the methodological gap our Hedge Rule resolves.

### Objective function

The objective function minimizes the expected wave makespan under the chosen elevator model:

minW⊆OE[Cmax(W;M, ξ)]

(1)

where CmaxW;M, ξ≔maxo∈Wtodeliver(W;M, ξ) is the wave makespan, todeliver(W;M, ξ) is the simulator-realized delivery time of order o under elevator model M, and ξ denotes a realization of the operational randomness in the dispatch simulator. Under M1 and M2, ξ is degenerate and (1) reduces to the deterministic makespan CmaxW;M; under M3, ξ equals the lognormal perturbations on (τs, τe, τd) at scale σ{M3} and the expectation is non-degenerate. The expectation in (1) is taken over ξ. We adopt the makespan rather than the average delivery time because wave throughput in multi-story fulfillment is gated by the slowest order: the next wave cannot release until elevator capacity is freed by the current wave's completion.

### Constraints

The wave composition W is subject to two classes of constraints:

Wmin≤W≤Wmax

(2)

ro∈τω, τω+∆, ∀o∈W

(3)

ω1[o∈Wω]=1, ∀o∈O

(4)

xo∈0, 1, ∀o∈O

(5)

Constraints (2)-(5) define the wave-composition decision space: cardinality bounds, temporal feasibility, exactly-one-wave-per-order, and the binary inclusion indicator. The elevator capacity bound (naboarde, t≤c) and the AMR fleet limit A are not formal optimization constraints at the wave-composition stage. They are invariants enforced by the operational simulator under the dispatch policy of Assumptions A1–A3, where the wave makespan Cmax(W;M) is realized. The capacity bound enters the formulation through its effect on Cmax (a wave with composition incompatible with c manifests as a higher Cmax(W;M) rather than as infeasibility), making it natural to absorb into the objective rather than to state as a constraint. We solve (1)-(5) one wave at a time: at each release window, the decision is over orders not yet released, so (4) is automatically satisfied. The decision object in the rest of the paper is therefore a single wave's inclusion vector.

Equations (1)-(5), together with Assumptions A1-A5, define the wave release coordination problem under vertical resource constraints. This minimal formulation is deliberate: the wave-elevator coupling is fully captured by ΦW=(CW, IW, T(W)) at the partition resolution on which our analytical tools operate. Operational lift scheduling is well studied (Chakravarty et al., 2025); the upstream wave layer, which prior work treats as exogenous, is formalized in this paper. Direct solution by enumeration over {xo}o is intractable in any case (combinatorial |O|, simulator-realized objective), so Section 4’s tools are how the formulation becomes operational.

Ardjmand, E., Shakeri, H., Singh, M., & Sanei Bajgiran, O. (2018). Minimizing order picking makespan with multiple pickers in a wave picking warehouse. International Journal of Production Economics, 206, 169–183. https://doi.org/10.1016/j.ijpe.2018.10.001

Azadeh, K., De Koster, R., & Roy, D. (2019). Robotized and automated warehouse systems: Review and recent developments. In Transportation Science (Vol. 53, Number 4, pp. 917–945). INFORMS Inst.for Operations Res.and the Management Sciences. https://doi.org/10.1287/trsc.2018.0873

Azadeh, K., Roy, D., & De Koster, R. (2019). Design, modeling, and analysis of vertical robotic storage and retrieval systems. Transportation Science, 53(5), 1213–1234. https://doi.org/10.1287/trsc.2018.0883

Bartholdi, J. J., & Hackman, S. T. (2019). Warehouse & Distribution Science. www.warehouse-science.com

Bertsimas, D., Brown, D. B., & Caramanis, C. (2011). Theory and applications of robust optimization. In SIAM Review (Vol. 53, Number 3, pp. 464–501). https://doi.org/10.1137/080734510

Blanchet, J., & Murthy, K. (2019). Quantifying Distributional Model Risk via Optimal Transport MATHEMATICS OF OPERATIONS RESEARCH Quantifying Distributional Model Risk via Optimal Transport. Source: Mathematics of Operations Research, 44(2), 565–600. https://doi.org/10.2307/27287849

Boysen, N., de Koster, R., & Weidinger, F. (2019). Warehousing in the e-commerce era: A survey. In European Journal of Operational Research (Vol. 277, Number 2, pp. 396–411). Elsevier B.V. https://doi.org/10.1016/j.ejor.2018.08.023

Boysen, N., Fedtke, S., & Weidinger, F. (2018). Optimizing automated sorting in warehouses: The minimum order spread sequencing problem. European Journal of Operational Research, 270(1), 386–400. https://doi.org/10.1016/j.ejor.2018.03.026

Bozer, Y. A., & Kile, J. W. (2008). Order batching in walk-and-pick order picking systems. International Journal of Production Research, 46(7), 1887–1909. https://doi.org/10.1080/00207540600920850

Chakravarty, A., Grey, M. X., Muthugala, M. A. V. J., & Elara, R. M. (2025). Toward Optimal Multi-Agent Robot and Lift Schedules via Boolean Satisfiability. Mathematics, 13(18). https://doi.org/10.3390/math13183031

Chenreddy, A., & Delage, E. (2024). End-to-end Conditional Robust Optimization. http://arxiv.org/abs/2403.04670

Crites, R. H., Barto, A. G., Huhns, M., & Weiss, G. (1998). Elevator Group Control Using Multiple Reinforcement Learning Agents (Vol. 33).

Delage, E., & Ye, Y. (2010). Accessibility support: If you experience accessibility issues with this file, report them here Distributionally Robust Optimization Under Moment Uncertainty with Application to Data-Driven Problems. Operations Research, 62(6), 1358–1376. https://www.jstor.org/stable/40792682

Dhanaraj, N., Nemlekar, H., Nikolaidis, S., & Gupta, S. K. (2025). Proactive Contingency-Aware Task Allocation and Scheduling in Multi-Robot Multi-Human Cells via Hindsight Optimization. IEEE Transactions on Automation Science and Engineering, 22, 13046–13060. https://doi.org/10.1109/TASE.2025.3546281

Elmachtoub, A. N., & Grigas, P. (2020). Smart “Predict, then Optimize.” http://arxiv.org/abs/1710.08005

Gademann, A. J. R. M. noud, Van Den Berg, J. P., & Van Der Hoff, H. H. (2001). An order batching algorithm for wave picking in a parallel-aisle warehouse. IIE Transactions (Institute of Industrial Engineers), 33(5), 385–398. https://doi.org/10.1080/07408170108936837

Gao, R., & Kleywegt, A. (2023). Distributionally Robust Stochastic Optimization with Wasserstein Distance. Mathematics of Operations Research, 48(2), 603–655. https://doi.org/10.1287/moor.2022.1275

Haouassi, M., Kergosien, Y., Mendoza, J. E., & Rousseau, L. M. (2022). The integrated orderline batching, batch scheduling, and picker routing problem with multiple pickers: the benefits of splitting customer orders. Flexible Services and Manufacturing Journal, 34(3), 614–645. https://doi.org/10.1007/s10696-021-09425-8

Lu, M., & Shen, Z. J. M. (2021). A Review of Robust Operations Management under Model Uncertainty. Production and Operations Management, 30(6), 1927–1943. https://doi.org/10.1111/poms.13239

Ma, S., Ruan, J., Du, Y., Bucknall, R., & Liu, Y. (2025). An End-To-End Deep Reinforcement Learning Based Modular Task Allocation Framework for Autonomous Mobile Systems. IEEE Transactions on Automation Science and Engineering, 22, 1519–1533. https://doi.org/10.1109/TASE.2024.3367237

Mohajerin Esfahani, P., & Kuhn, D. (2018). Data-driven distributionally robust optimization using the Wasserstein metric: performance guarantees and tractable reformulations. Mathematical Programming, 171(1–2), 115–166. https://doi.org/10.1007/s10107-017-1172-1

Nicolas, L., Yannick, F., & Ramzi, H. (2018). Order batching in an automated warehouse with several vertical lift modules: Optimization and experiments with real data. European Journal of Operational Research, 267(3), 958–976. https://doi.org/10.1016/j.ejor.2017.12.037

Pardo, Gil-Borrás, Alonso-Ayuso, & Duarte. (2024). Order batching problems: Taxonomy and literature review. European Journal of Operational Research, 313(1), 1–24. https://doi.org/10.13039/501100011033

Qin, Z., Kang, Y., & Yang, P. (2024). Making better order fulfillment in multi-tote storage and retrieval autonomous mobile robot systems. Transportation Research Part E: Logistics and Transportation Review, 192. https://doi.org/10.1016/j.tre.2024.103752

Rasmi, S. A. B., Wang, Y., & Charkhgard, H. (2022). Wave order picking under the mixed-shelves storage strategy: A solution method and advantages. Computers and Operations Research, 137. https://doi.org/10.1016/j.cor.2021.105556

Schiffer, M., Boysen, N., Klein, P. S., Laporte, G., & Pavone, M. (2022). Optimal Picking Policies in E-Commerce Warehouses. Management Science, 68(10), 7497–7517. https://doi.org/10.1287/mnsc.2021.4275

Scholz, A., Schubert, D., & Wäscher, G. (2017). Order picking with multiple pickers and due dates – Simultaneous solution of Order Batching, Batch Assignment and Sequencing, and Picker Routing Problems. European Journal of Operational Research, 263(2), 461–478. https://doi.org/10.1016/j.ejor.2017.04.038

Tadumadze, G., Wenzel, J., Emde, S., Weidinger, F., & Elbert, R. (2023). Assigning orders and pods to picking stations in a multi-level robotic mobile fulfillment system. Flexible Services and Manufacturing Journal, 35(4), 1038–1075. https://doi.org/10.1007/s10696-023-09491-0

Tsai, I. N., Wu, Y. X., Huang, Y. H., Chen, Y. C., & Ding, J. J. (2025). Optimization of Elevator Standby Scheduling Strategy in Smart Buildings. Applied System Innovation, 8(5). https://doi.org/10.3390/asi8050132

Vera, A., Banerjee, S., & Gurvich, I. (2020). Online Allocation and Pricing: Constant Regret via Bellman Inequalities. http://arxiv.org/abs/1906.06361

Wen, C., & Ma, H. (2024). An indicator-based evolutionary algorithm with adaptive archive update cycle for multi-objective multi-robot task allocation. Neurocomputing, 593. https://doi.org/10.1016/j.neucom.2024.127836

Wesselhöft, M., Hinckeldeyn, J., & Kreutzfeldt, J. (2022). Controlling Fleets of Autonomous Mobile Robots with Reinforcement Learning: A Brief Survey. Robotics, 11(5). https://doi.org/10.3390/robotics11050085

Wiesemann, W., Kuhn, D., & Rustem, B. (2013). Robust markov decision processes. Mathematics of Operations Research, 38(1), 153–183. https://doi.org/10.1287/moor.1120.0566

Wu, J., Yang, Z., Zhen, L., Li, W., & Ren, Y. (2025). Joint optimization of order picking and replenishment in robotic mobile fulfillment systems. Transportation Research Part E: Logistics and Transportation Review, 194. https://doi.org/10.1016/j.tre.2024.103930

Wu, Z., Zhang, Y., Li, L., Zhang, Z., Zhao, B., Zhang, Y., & He, X. (2024). Research on Inbound Jobs’ Scheduling in Four-Way-Shuttle-Based Storage System. Processes, 12(1). https://doi.org/10.3390/pr12010223

Žulj, I., Salewski, H., Goeke, D., & Schneider, M. (2022). Order batching and batch sequencing in an AMR-assisted picker-to-parts system. European Journal of Operational Research, 298(1), 182–201. https://doi.org/10.1016/j.ejor.2021.05.033
