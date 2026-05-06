---
title: "Wave Release Coordination under Vertical Resource Constraints in Multi-Story AMR Warehouses"
section: "§2. Related Work prose draft v0.1"
date: 2026-05-06
status: "First prose pass; absorbs the detailed thread-by-thread positioning previously deferred from §1 Introduction"
---

# §2. Related Work *(target ~800 words; current ≈ 920)*

The relevant literature falls into two strands: (i) operations research on warehouse problems that share part of our setting (multi-story deployment, AMR fleets, lift coupling, or wave-scale grouping decisions), and (ii) methodological tools that bear on our analytical apparatus (robust scheduling under structural model uncertainty, and prediction-to-decision regret bounds). We organize the first strand into four problem-class threads and survey the second more briefly. Two recent surveys place this work in context: [Boysen and de Koster, 2025] provides a fifty-year retrospective of warehousing OR organized across three generations of distribution-center architecture, and [Boysen, Schneider, and Žulj, 2025] reviews fleet coordination problems for electric vehicles in facility logistics, including AMR fleets.

## §2.1 Device-level order batching in vertical lift modules

The work of [Lenoble, Frein, and Hammami, 2018] is closest to our framing in name (it studies "order batching" with a "vertical" element) but most distant in physical scale. They formulate order batching in an automated warehouse equipped with one to four vertical lift modules (VLMs); each VLM is a single mechanical device with a tray that travels vertically. Their decision is which item-orders to retrieve in a single tray-load, with the objective of minimizing total completion time, validated on real data from two firms. The mathematics is internal to each device: a VLM is a piece of equipment, not a building. Our setting differs at every scale of this comparison: the "vertical resource" we study is a freight elevator carrying AMRs across building floors, the wave we release is a fleet-level co-occupation window, and the coupling we treat (multi-elevator capacity shared across a horizontal AMR fleet) does not arise inside a single VLM.

## §2.2 Multi-agent robot–lift scheduling with fixed task sets

[Chakravarty, Grey, Muthugala, and Elara, 2025] address the operational scheduling of AMR fleets coordinating with shared lifts in hotel and hospital deployments. Using Boolean satisfiability (SAT) solvers with anytime constraint-programming techniques, they compute provably optimal lift schedules and report up to 4.34 times speedup over a baseline. The decision space they address is downstream of ours: their SAT formulation takes a list of robot–task assignments as exogenous input and finds the time-optimal lift schedule for delivering them. Our problem is upstream of theirs: we treat the *selection* of which orders enter the system together (wave composition) as a tactical decision variable, with the operational AMR–elevator dispatch then taking that wave as input. The scaling profile also differs: their SAT approach caps practically at small fleets (around thirty agents per scenario), whereas we target hundreds of orders per wave through a heuristic-friendly two-stage decomposition.

## §2.3 Multi-story scheduling with tier-captive transport

A growing literature studies multi-story warehouses where each tier has its own dedicated vehicles. [Wu et al., 2024] address inbound job scheduling in four-way shuttle systems, formulating a flexible flow-shop problem and proposing a double-encoded genetic algorithm with embedded simulated annealing; their DELO-GA solves 100-job instances in under 100 seconds with sub-1% optimality gap. [Keung, Lee, and Ji, 2023] study order and pod assignment in multi-level robotic mobile fulfillment systems (RMFS). Both adopt a *tier-captive* transport model: each shuttle is bound to a specific layer, and inter-layer transport happens via dedicated lift–shuttle handover, rather than via a fleet of horizontally flexible robots queueing at shared elevators. The bottleneck topology this produces is fundamentally different from ours: in tier-captive systems, a layer-bound shuttle's queue depends only on its own layer's demand, whereas in our setting AMRs from any floor compete concurrently for elevator service. This concurrency is what makes wave composition (which floors and which directions to release together) the binding tactical lever in our problem class but not in theirs.

## §2.4 Order-grouping as a decision variable in planar picker-to-parts systems

The work most directly relevant to our tactical layer treats order grouping itself as a decision variable, in planar (single-floor) settings without vertical resource coupling. [Scholz, Schubert, and Wäscher, 2017] formulate the *Joint Order Batching, Assignment and Sequencing, and Picker Routing Problem* (JOBASRP) for multi-picker manual warehouses with due-date objectives, demonstrating through variable neighborhood descent that the holistic joint solution outperforms sequential decomposition by up to 84% in total tardiness. [Žulj, Salewski, Goeke, and Schneider, 2022] extend this line to AMR-assisted picker-to-parts systems, where robots transport totes between human pickers and a depot, and develop a hybrid ALNS-tabu heuristic for the joint batching and sequencing problem. [Qin, Kang, and Yang, 2024] study order fulfillment in multi-tote storage and retrieval (MTSR) AMR systems and notably *use the term "wave"* for processing batches, identifying through an item-popularity-driven adaptive large neighborhood search an empirical optimum near 100 orders per wave in their single-layer setting. This last finding deserves careful framing: Qin's "wave" is a *cardinality* parameter (how many orders to process together), not a *composition* decision (which orders to bundle on structured features). Our work extends this single-floor decision class to the multi-story setting, where shared elevator capacity introduces a vertical-resource coupling that none of these planar precedents addresses.

## §2.5 Methodological context

Two analytical lines bear on our methodology. First, robust scheduling under model uncertainty [Wiesemann, Kuhn, and Rustem, 2013; Lu and Shen, 2021] handles parametric variation within a known model class (for example, an MDP with uncertain transition probabilities, or a robust OM problem with a known objective form and an uncertain demand parameter). Our elevator-modeling uncertainty is structurally different: throughput-aggregation and true-co-occupancy-batching are *qualitatively distinct* models of how elevators serve fleets, not two parameterizations of the same model family. The Hedge Rule we derive collapses this *structural* model-class disagreement into a single closed-form decision under a per-wave dominance condition. Second, the prediction-to-decision regret literature [Elmachtoub and Grigas, 2022; Vera, Banerjee, and Gurvich, 2021] bounds algorithmic loss when a learned predictor is plugged into a downstream optimiser. Our Bound-and-Gap framework studies a complementary post-hoc quantity: the *information gap* between an oracle on a structured feature partition and a $\Phi$-informed policy on the same partition.

## §2.6 Synthesis

None of the threads above treats the four problem-defining elements (wave composition as a tactical decision variable, multi-story deployment, flexible AMR fleets, and shared-elevator capacity coupling) as one coupled system. Order-grouping work [Scholz et al., 2017; Žulj et al., 2022; Qin et al., 2024] addresses wave grouping but in planar settings without elevator coupling. Multi-story scheduling work [Wu et al., 2024; Keung et al., 2023] addresses vertical structure but with tier-captive rather than flexible transport. Multi-agent robot–lift work [Chakravarty et al., 2025] addresses the AMR–elevator coupling but with task selection treated as exogenous. Device-level VLM batching [Lenoble et al., 2018] and the methodological literature [Wiesemann et al., 2013; Lu and Shen, 2021; Elmachtoub and Grigas, 2022; Vera et al., 2021] each touch a piece of the technical apparatus but leave the joint problem class open. We formalize that joint class in §3 and develop our analytical tools in §4.

---

## References

All DOIs below are verified and resolve to the publisher's record at the time of writing (2026-05-06).

Boysen, N., & de Koster, R. (2025). 50 years of warehousing research: An operations research perspective. *European Journal of Operational Research*, 320(3), 449–464. https://doi.org/10.1016/j.ejor.2024.03.026

Boysen, N., Schneider, M., & Žulj, I. (2025). Energy management for electric vehicles in facility logistics: A survey from an operational research perspective. *European Journal of Operational Research* (Invited Review, in press). https://doi.org/10.1016/j.ejor.2025.12.031

Chakravarty, A., Grey, M. X., Muthugala, M. A. V. J., & Elara, R. M. (2025). Toward optimal multi-agent robot and lift schedules via Boolean satisfiability. *Mathematics*, 13(18), 3031. https://doi.org/10.3390/math13183031

Elmachtoub, A. N., & Grigas, P. (2022). Smart "Predict, then Optimize". *Management Science*, 68(1), 9–26. https://doi.org/10.1287/mnsc.2020.3922

Keung, K. L., Lee, C. K. M., & Ji, P. (2023). Assigning orders and pods to picking stations in a multi-level robotic mobile fulfillment system. *Flexible Services and Manufacturing Journal*. https://doi.org/10.1007/s10696-023-09491-0

Lenoble, N., Frein, Y., & Hammami, R. (2018). Order batching in an automated warehouse with several vertical lift modules: Optimization and experiments with real data. *European Journal of Operational Research*, 267(3), 958–976. https://doi.org/10.1016/j.ejor.2017.12.037

Lu, M., & Shen, Z.-J. M. (2021). A review of robust operations management under model uncertainty. *Production and Operations Management*, 30(6), 1927–1943. https://doi.org/10.1111/poms.13239

Qin, Z., Kang, Y., & Yang, P. (2024). Making better order fulfillment in multi-tote storage and retrieval autonomous mobile robot systems. *Transportation Research Part E: Logistics and Transportation Review*, 192, 103752. https://doi.org/10.1016/j.tre.2024.103752

Scholz, A., Schubert, D., & Wäscher, G. (2017). Order picking with multiple pickers and due dates: Simultaneous solution of Order Batching, Batch Assignment and Sequencing, and Picker Routing Problems. *European Journal of Operational Research*, 263(2), 461–478. https://doi.org/10.1016/j.ejor.2017.04.038

Vera, A., Banerjee, S., & Gurvich, I. (2021). Online allocation and pricing: Constant regret via Bellman inequalities. *Operations Research*, 69(3), 821–840. https://doi.org/10.1287/opre.2020.2061

Wiesemann, W., Kuhn, D., & Rustem, B. (2013). Robust Markov decision processes. *Mathematics of Operations Research*, 38(1), 153–183. https://doi.org/10.1287/moor.1120.0566

Wu, Z., Zhang, Y., Li, L., Zhang, Z., Zhao, B., Zhang, Y., & He, X. (2024). Research on inbound jobs' scheduling in four-way-shuttle-based storage system. *Processes*, 12(1), 223. https://doi.org/10.3390/pr12010223

Žulj, I., Salewski, H., Goeke, D., & Schneider, M. (2022). Order batching and batch sequencing in an AMR-assisted picker-to-parts system. *European Journal of Operational Research*, 298(1), 182–201. https://doi.org/10.1016/j.ejor.2021.05.033
