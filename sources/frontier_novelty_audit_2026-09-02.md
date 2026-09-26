# Frontier novelty lookup log — 2026-09-02

## Purpose

This lookup supports the continuation review of the manuscript's three claimed contributions. The search focused on (i) multi-story robot/elevator coordination, (ii) joint order scheduling and robot operations, and (iii) prescriptive-value and distributionally robust optimization methods. It is a targeted novelty audit, not a systematic review.

## Search questions used

1. What 2025–2026 work treats multi-story robot routing or scheduling with elevators/lifts?
2. What 2025–2026 work jointly optimizes order-level and robot-level warehouse decisions?
3. What established or recent metrics already quantify the value of information/policies in contextual optimization?
4. Are closed-form DRO results under stochastic dominance already part of the literature?

## Screened primary sources and relevance

### Physical/problem-class frontier

- He, Wu, Zhao, and Ren (2026), **Conflict-Based Search for Multi-Agent Path Finding with Elevators**. The paper formalizes MAPF with elevator states and cross-floor conflicts. Its agents' start/goal tasks are fixed, so it does not appear to make upstream wave composition the decision; however, it is now a mandatory comparison for any claim that multi-agent/elevator coupling is unstudied.  
  URL: https://arxiv.org/abs/2602.20512

- Xu et al. (2026), **It Takes Two to Tango: A Holistic Simulator for Joint Order Scheduling and Multi-Agent Path Finding in Robotic Warehouses** (WareRover). It directly couples high-level order scheduling with low-level congestion under dynamic streams, motion constraints, and failures. It is not visibly a multi-story shared-elevator wave model, but it makes blanket claims such as “high- and low-level choices have only been studied in isolation” unsafe.  
  URL: https://arxiv.org/abs/2602.13999

- Kim et al. (2025), **Efficient Graph-Based Multi-Story Path Planning with Optimized Elevator Selection for Indoor Delivery Robots**. It combines floor-based parcel grouping, multi-story routing, and elevator selection. The setting is not a flexible multi-AMR fulfillment fleet with shared-elevator congestion, but it is close enough that the manuscript must explain the precise difference rather than claim that parcel/wave composition and elevators have never been coupled.  
  URL: https://www.mdpi.com/2079-9292/14/5/982

- Ren et al. (2025), **Scheduling optimisation in a multi-deep tier-to-tier four-way shuttle storage and retrieval system**. It jointly treats request sequencing, equipment selection, and path planning with lifts. The request set remains operationally given, which preserves a narrower upstream-wave distinction.  
  URL: https://www.sciencedirect.com/science/article/pii/S0360835225002414

- Wang et al. (2025), **Retrieval scheduling in four-directional shuttle-based compact storage and retrieval systems with heterogeneous lifts**. It jointly schedules fixed retrieval requests, shuttles, shuttle-lifts, and bin-lifts. It is a close operational-layer comparator, not an upstream composition paper.  
  URL: https://www.sciencedirect.com/science/article/pii/S0360835225007053

- Xue and Wang (2026), **Joint optimization of order allocation, rack selection, and robot scheduling under flexible storage location**. It formulates a joint wave-completion-time problem and validates on operational data. It is planar parts-to-picker rather than multi-story/shared elevator, but it weakens any general claim that wave/order composition and robot scheduling are separated in recent work.  
  URL: https://www.sciencedirect.com/science/article/pii/S1366554526002267

- Lu et al. (2026), **Reinforcement learning for joint scheduling in robotic mobile fulfillment systems**. This is another recent integrated RMFS decision paper that should be screened before the literature review is frozen.  
  URL: https://www.sciencedirect.com/science/article/pii/S0377221726006466

- Cheng et al. (2026), **An integrated batch scheduling algorithm for order and rack sequencing with multi-visit mobile robots**. This is a recent batch/order–robot integration comparator; its physical scope differs from the manuscript's multi-story elevator setting.  
  URL: https://www.sciencedirect.com/science/article/pii/S0957417426009693

### Methodological frontier and baselines

- Bertsimas and Kallus (2020), **From Predictive to Prescriptive Analytics**. It introduces the coefficient of prescriptiveness for measuring the prescriptive content of data/policy performance. The Bound-and-Gap framework must be compared against this baseline and against classical VSS/EVPI-style information-value measures.  
  URL: https://ideas.repec.org/a/inm/ormnsc/v66y2020i3p1025-1044.html

- Jiang, Tian, and Wang (2026), **On the coefficients of prescriptiveness in contextual optimization**. This very recent paper proposes adjusted and expected coefficients, making a 2026 comparison necessary if Bound-and-Gap is sold as a new value diagnostic.  
  URL: https://aimspress.com/article/doi/10.3934/era.2026266

- Elmachtoub and Grigas, **Smart “Predict, then Optimize”**. SPO loss already measures decision error induced by predictions. In the manuscript, the claimed equality between `M_Phi` and SPO loss is largely a direct consequence of defining both with the same selected and oracle corners; it should be positioned as an interpretation, not experimentally “confirmed” theory.  
  URL: https://arxiv.org/abs/1710.08005

- Song and Luedtke (2015), **An adaptive partition-based approach for solving two-stage stochastic programs with fixed recourse**. This is the relevant partition-refinement precedent. The manuscript's refinement theorem must be limited to genuinely nested partitions.  
  URL: https://epubs.siam.org/doi/abs/10.1137/140967337

- Kuhn, Shafiee, and Wiesemann (2025), **Distributionally robust optimization**. This survey codifies the mature DRO landscape and the central role of ambiguity-set construction. A corner-specific radius calibrated from the candidate models therefore needs an operational or statistical justification; matching the calibrated worst member is not by itself strong empirical validation.  
  URL: https://www.cambridge.org/core/journals/acta-numerica/article/distributionally-robust-optimization/5B4E65E3A5A2AEF24E218A6B34E6EAA2

- Fu, Li, and Zhang (2024), **Distributionally Robust Newsvendor Under Stochastic Dominance with a Feature-Based Application**. It gives closed-form robust decisions under stochastic-dominance-related ambiguity sets. It does not pre-empt the warehouse-specific result, but it means “dominance makes DRO collapse to a closed form” is not generically novel.  
  URL: https://ideas.repec.org/a/inm/ormsom/v26y2024i5p1962-1977.html

## Novelty implication

The narrow problem gap remains plausible: upstream composition of a single wave for a flexible, floor-confined AMR fleet contending for building-level freight elevators is not directly duplicated by the screened sources. The stronger language currently used in the manuscript—“never treated,” “studied only in isolation,” or an implied first coupling of upstream and downstream decisions—is not supported after the 2025–2026 screen. The defensible claim is a scoped synthesis/benchmark at a particular decision layer, subject to a more complete systematic search.

For the methodology, novelty should be priced by theorem strength. Algebraic decompositions, a definition-level SPO equality, minimax reduction after assuming a worst model, and a model-calibrated DRO coincidence are supporting properties. The potentially distinctive piece is a correct, nontrivial sample-path characterization of when the elevator-model ordering holds and fails, plus a transparent empirical diagnostic protocol. That core is not yet integrated into the Word manuscript.
