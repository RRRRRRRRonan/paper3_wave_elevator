§4 Methodology

   开篇散文 (修辞升级版，预告 general framework + 两个 equivalence)

   §4.1 Bound-and-Gap framework
      
      §4.1.1 General decomposition
         - Setup (feature-agnostic)
         - Proposition 1: GAP = H_up + M_xi (修辞升级)
         - Proof
      
      §4.1.2 Equivalence to SPO regret on partitions (D1 NEW)
         - Setup: SPO loss restricted to partition-constant predictors
         - Theorem 1: M_xi = SPO regret on the partition-constant predictor class
         - Proof
         - Discussion: 把你的 framework 定位为 SPO 文献的 partition perspective
      
      §4.1.3 Application to wave-elevator coupling
         - Theorem 2 (was Theorem 1): Application of Proposition 1 to Φ
         - Corollary (Refinement monotonicity)
         - Operational interpretation
   
   §4.2 Model-Dominance Hedge Rule
      
      §4.2.1 Chain dominance setup
         - K-model family M = {M_1, M_2, M_3}
         - Chain dominance condition
      
      §4.2.2 Equivalence to Wasserstein DRO under dominance (D2 NEW)
         - Setup: Wasserstein DRO problem on the family
         - Theorem 3: Under chain dominance, Wasserstein DRO solution = Hedge Rule solution
         - Proof
         - Discussion: 把你的 Hedge Rule 定位为 DRO 文献的 dominance special case
      
      §4.2.3 Generalized Hedge Rule
         - Theorem 4 (was Theorem 2): K-model Hedge Rule closed-form
         - Corollary (2-model special case)
         - Corollary (ε-bound for relaxed dominance)
         - Operational interpretation
   
   §4.3 Connection to Section 5