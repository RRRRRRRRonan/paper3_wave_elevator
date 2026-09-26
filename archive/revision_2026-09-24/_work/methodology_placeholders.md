4. Methodology

We use a simulation-based robust class-selection framework to determine the structural class from which a wave is released. Given the candidate pool and class definitions in Section 3, candidate waves are evaluated under the two deterministic elevator models using common order data and prescribed reservation rules. Each class is scored by the larger of its two median makespans. The framework selects the class with the smallest such score and implements the decision by drawing a candidate wave from its fixed within-class distribution.

Two analyses support this selection framework. A class-level diagnostic measures performance differences across the selectable classes and the loss associated with a prespecified class-selection rule. A paired analysis of elevator requests establishes sufficient conditions for ordering the two evaluators and identifies mechanisms that can reverse that ordering. When the ⟦E1⟧ median is no smaller in every selectable class, the robust decision reduces to selecting the class with the smallest ⟦E2⟧ median; departures from this ordering are assessed through class-score differences and ranking margins. Fig. 2 shows the decision flow and the supporting roles of the three analyses.

⟦FIGURE⟧

Fig. 2. Robust class selection and its supporting analyses. Common recorded order sequences support paired evaluations under ⟦E3⟧ and ⟦E4⟧. Evaluator-specific class medians enter the minimax rule, and the selected class determines the fixed distribution from which a wave is released. The diagram displays exact scores; sampled scores follow the same flow with the estimates in Equations (34)–(35). Class-relative diagnosis, conditional evaluator ordering, and decision-property analysis form supporting branches. ⟦E5⟧ assesses the selected class under phase-time variation. Solid arrows indicate the decision flow; dashed arrows indicate supporting analysis or assessment.

4.1 Robust class-selection procedure

4.1.1 Candidate evaluation and class scores

The procedure takes the candidate pool, structural classes, resource configuration, and within-class release distributions defined in Section 3 as inputs. Each candidate is evaluated under ⟦E6⟧ and ⟦E7⟧ using the same order sequence and initial state. For each class and evaluator, the deterministic median is obtained exactly from one equally weighted outcome per candidate in its support, retaining repeated outcome values:

[DISPLAY] ⟦E8⟧

When class scores are estimated by sampling, ⟦E9⟧ candidate indices ⟦E10⟧ are drawn independently, and the same draws are used across evaluators. For evaluations under ⟦E11⟧, phase-time realizations ⟦E12⟧ are independent across replications and independent of the candidate indices. The estimated class median is

[DISPLAY] ⟦E13⟧

where ⟦E14⟧ is omitted for deterministic evaluators. For ⟦E15⟧ and ⟦E16⟧, candidate sampling is the source of variation in this estimate. Under ⟦E17⟧, it also incorporates phase-time variation, matching the joint outcome distribution in Equation (14). All medians follow the midpoint convention in Section 3.4.2. Section 5 specifies the sampling sizes and uncertainty analysis.

4.1.2 Class selection and wave release

For each class, the decision rule retains the larger median across ⟦E18⟧ and selects the class with the smallest retained value. Thus, the comparison is between evaluator-specific class medians. With exact scores, the selected class is ⟦E19⟧ from Equation (15). With estimated scores, the same rule gives

[DISPLAY] ⟦E20⟧

A fixed class-label order resolves ties in either minimization. The selected class is implemented through Equation (12), with ⟦E21⟧ for the exact-score decision and ⟦E22⟧ for the estimated-score decision. The resulting wave ⟦E23⟧ is then released. This step maps the class decision to a concrete wave while preserving the specified within-class sampling rule. The resulting output comprises the selected class, its release distribution, and its evaluated makespan profile. The direct candidate benchmark in Equations (16)–(17) provides a comparison with choosing an individual wave, while ⟦E24⟧ assesses performance under phase-time variation. The same class-score data also support the performance diagnosis developed next.

4.2 Class-relative performance diagnosis

4.2.1 Reference scores and diagnostic decomposition

Alongside the robust decision, the evaluation outcomes quantify the performance differences between classes and the quality of a prespecified selection rule. For a fixed resource configuration, wave size, and evaluator ⟦E25⟧, the class medians in Equation (14) provide the comparison scores. The reference choice draws uniformly from the entire candidate pool. This pool distribution is denoted by ⟦E26⟧, while ⟦E27⟧ and ⟦E28⟧ denote the reference and class medians under the fixed evaluator:

[DISPLAY] ⟦E29⟧

For ⟦E30⟧ and ⟦E31⟧, the pool reference is computed by complete candidate enumeration or estimated using draws from ⟦E32⟧. Under ⟦E33⟧, it is estimated from joint candidate and phase-time draws following Section 4.1. All medians use the midpoint convention in Section 3.4.2. Positive service durations and a nonempty wave give ⟦E34⟧, so it can normalize comparisons across configurations. The best and worst selectable classes under this evaluator are denoted by

[DISPLAY] ⟦E35⟧

The class returned by a prespecified selection rule using the descriptors ⟦E36⟧ is denoted by ⟦E37⟧. Its fitting procedure, treatment of tied scores, and handling of empty corner supports form part of that rule. The diagnostic takes this rule’s selected class as an input and compares it with both the class oracle ⟦E38⟧ and the pool reference. Here ⟦E39⟧ identifies the class selected by the rule being assessed, whereas ⟦E40⟧ and ⟦E41⟧ identify the robust decisions defined above. The normalized class spread ⟦E42⟧, the selected class’s normalized gain ⟦E43⟧, and their difference ⟦E44⟧ are defined as

[DISPLAY] ⟦E45⟧

Proposition 1 (diagnostic identity). For any nonempty selectable class family and any selected class ⟦E46⟧, the diagnostic satisfies

[DISPLAY] ⟦E47⟧

Proof. Substituting Equation (38) gives ⟦E48⟧ in the numerator. Division by ⟦E49⟧ yields Equation (39). The two terms describe different comparisons. The class-family-relative upper-tail headroom ⟦E50⟧ locates the largest class median relative to the pool median. The class-selection miss ⟦E51⟧ measures the normalized excess median makespan of the selected class over the best class in the same family. Resource quantities and operational rules remain fixed in both comparisons. Because ⟦E52⟧,

[DISPLAY] ⟦E53⟧

The signs of the other terms depend on the reference comparison: ⟦E54⟧ exactly when ⟦E55⟧, and ⟦E56⟧ exactly when the selected class’s median is no greater than the pool median. The corner family in Section 3.3 need not cover the entire candidate pool and may have overlapping supports at tied thresholds. Its class medians therefore need not bracket ⟦E57⟧; ⟦E58⟧ and ⟦E59⟧ can be negative. These values retain the signed comparisons defined in Equations (38)–(39).

4.2.2 Class-selection loss

The selection term also has a decision-loss interpretation. In predict-then-optimize, the Smart Predict-then-Optimize (SPO) loss evaluates the cost of the decision induced by predicted coefficients, relative to an optimal decision under the true coefficients (Adam N. Elmachtoub & Paul Grigas, 2021) . Here the actions are class labels. Their cost vector is ⟦E60⟧, and a predicted class-score vector ⟦E61⟧ induces the choice ⟦E62⟧ under a fixed tie convention.

Proposition 2 (class-action loss interpretation). For the class decision induced by ⟦E63⟧, its SPO loss under ⟦E64⟧ satisfies

[DISPLAY] ⟦E65⟧

Proof. The selected action incurs cost ⟦E66⟧, and the oracle action incurs cost ⟦E67⟧. Their difference is the numerator of ⟦E68⟧. Thus, ⟦E69⟧ evaluates the quality of a class decision on a fixed class-cost vector. A learning method can target this loss through the class scores it predicts; its training and generalization properties depend on the learning procedure and data design.

4.2.3 Resolution of covering partitions

The resolution analysis uses a finite, disjoint, covering partition ⟦E70⟧ of the same candidate pool to examine how classification detail changes the observed class spread. Each cell has positive probability under ⟦E71⟧, and its outcome distribution is obtained by conditioning the same pool distribution and evaluator on that cell. Its midpoint median is denoted by ⟦E72⟧. This construction preserves the mixture relationship between the pool and its cells, giving

[DISPLAY] ⟦E73⟧

The bracketing property holds for the midpoint convention. In the proof of the upper inequality, ⟦E74⟧, and ⟦E75⟧ denotes the median interval of cell ⟦E76⟧. Every cell has cumulative probability at least one half at ⟦E77⟧. If the pool midpoint exceeded ⟦E78⟧, the pool’s cumulative probability at ⟦E79⟧ would equal one half, forcing the same equality in every positive-weight cell. Their median intervals would then have a common point, and the pool median interval would be their intersection. A cell attaining the largest lower endpoint would have a midpoint at least as large as the pool midpoint, contradicting the definition of ⟦E80⟧. Reflection of the outcome variable gives the lower inequality.

Theorem 1 (nested-partition refinement). The following result concerns finite covering partitions ⟦E81⟧ and ⟦E82⟧ of the same candidate pool, with positive-probability cells and cell distributions induced by the same base distribution and evaluator. If ⟦E83⟧ refines ⟦E84⟧, meaning that every cell of ⟦E85⟧ lies within one cell of ⟦E86⟧, then

[DISPLAY] ⟦E87⟧

Proof. The outcome distribution in a parent cell is the mixture of the distributions in its children, with weights ⟦E88⟧. Equation (42), applied within that parent, brackets its median by its smallest and largest child medians. The upper inequality for a parent attaining the largest coarse median and the lower inequality for a parent attaining the smallest coarse median establish the result.

Corollary 1 (diagnostic resolution). Along a nested sequence of such partitions, ⟦E89⟧, the oracle gain ⟦E90⟧, and ⟦E91⟧ are nonnegative and nondecreasing under refinement. This follows from Equations (42)–(43), with ⟦E92⟧ fixed. The selection term ⟦E93⟧ additionally depends on the rule’s choice at each resolution. The corner family ⟦E94⟧ and the covering partition ⟦E95⟧ answer different diagnostic questions. The former compares selected tail combinations of ⟦E96⟧ and ⟦E97⟧; the latter tracks how a complete classification resolves variation across the whole pool. Resolution comparisons use genuinely nested boundaries and consistent allocation of threshold ties. At the sample level, exact checks of Theorem 1 partition the same weighted outcome sample so that each parent distribution remains the mixture of its children. Fig. 3 separates the class-relative comparisons from the resolution analysis of covering partitions.

⟦FIGURE⟧

Fig. 3. Comparisons underlying the class-relative diagnostic. (a) Under one fixed evaluator, the best, selected, and worst class medians define the class spread and selected gain relative to the pool median ⟦E98⟧. (b) The identity ⟦E99⟧ separates the signed reference comparison from the nonnegative class-selection miss; ⟦E100⟧ is the corresponding class-action loss. (c) A separate nested, disjoint, covering partition uses the same pool distribution and evaluator, with positive cell weights. Refinement cannot shrink the range of cell medians. This partition is distinct from the corner family ⟦E101⟧.

4.3 Conditional ordering of the deterministic evaluators

4.3.1 Coupled request comparison

The relative magnitudes of the two evaluator scores determine which model sets a class's robust score. To analyze this relationship, we compare their resource reservations. The deterministic evaluators represent elevator capacity through different resource states: ⟦E102⟧ uses ⟦E103⟧ independent single-request slots, whereas ⟦E104⟧ uses ⟦E105⟧ physical cars with shared trips. Their completion times depend jointly on request timing, resource availability, and stored destination floors. We compare the evaluators on the same candidate wave using the serial reservation rules of Section 3.5. A corresponding elevator request is denoted by ⟦E106⟧, and its unloading completion time under ⟦E107⟧ by ⟦E108⟧, for ⟦E109⟧.

Proposition 3 (conditional sample-path ordering). The result applies to a candidate wave ⟦E110⟧ evaluated from the common initial state in Section 3.1, for any ⟦E111⟧ and ⟦E112⟧. Its conclusion holds when the two deterministic evaluations satisfy conditions (a)–(d).

Both evaluators process orders in the same recorded sequence ⟦E113⟧.

Each order is assigned to the same AMR in both evaluations.

No shared ⟦E114⟧ trip overtakes its corresponding ⟦E115⟧ requests. For every ⟦E116⟧ trip ⟦E117⟧ containing at least two requests, ⟦E118⟧ denotes its request group and ⟦E119⟧ its shared unloading completion time. The required relation is

[DISPLAY] ⟦E120⟧

Repositioning does not disadvantage ⟦E121⟧ on requests for which both evaluators create a new trip. For each such request with origin floor ⟦E122⟧, ⟦E123⟧ denotes the selected resource’s stored floor immediately before its state update in ⟦E124⟧. The required relation is

[DISPLAY] ⟦E125⟧

Under these conditions, every corresponding elevator request and the wave makespan satisfy

[DISPLAY] ⟦E126⟧

Conditions (a) and (b) align the sequence, origins, and destinations of elevator requests, including the AMR’s movement to an order’s pickup floor. The recorded sequence in Equation (1), shared across evaluators, supplies (a). Condition (b) is an additional property of the paired evaluations because earlier elevator completions affect subsequent earliest-available-AMR choices. In (d), the stored floor is the resource’s location at its recorded next-available time, as defined in Section 3.5. Conditions (c) and (d) are assessed on the paired reservation paths.

Proof sketch. The proof proceeds by induction over the reservation sequence. The induction maintains the completion-time ordering for previous requests and the ordering of the earliest ⟦E127⟧ resource availabilities: if ⟦E128⟧ and ⟦E129⟧ are the sorted ⟦E130⟧ and ⟦E131⟧ availability states, then ⟦E132⟧ for ⟦E133⟧. Common AMR assignments and the monotone service-time recursions give an earlier or equal request time under ⟦E134⟧. When both evaluators create a new trip, this comparison, earliest availability, and (d) order the new completion times. Replacing the smallest availability in each list preserves the required ordering. For a request joining an existing ⟦E135⟧ trip, condition (c) gives its completion-time comparison directly. The availability comparison follows from a counting argument. Any ⟦E136⟧ trip already replaced by a later reservation completed no later than the current fleet minimum; hence completions above a threshold ⟦E137⟧ can belong only to the latest trips of at most ⟦E138⟧ cars. Those trips contain at most ⟦E139⟧ requests. If the joining trip ends above that threshold, its spare place reduces the count of previous requests by one. Previous completion-time ordering transfers this count to the ⟦E140⟧ slots, preserving ⟦E141⟧ after the new slot reservation. The AMR recursions then order every order completion, including orders that inherit earlier resource delays without making a new elevator request. Taking the maximum and subtracting the common ⟦E142⟧ proves Equation (46).

4.3.2 Reversal mechanisms and class-level implications

Two small instances isolate the roles of shared trips and repositioning. Both use ⟦E143⟧, ⟦E144⟧, ⟦E145⟧, ⟦E146⟧, ⟦E147⟧, ⟦E148⟧, and ⟦E149⟧, with times measured in seconds. Both examples use the recorded processing sequence in the order described below. In the first instance, ⟦E150⟧ and ⟦E151⟧. Two orders travel from floor 1 to floor 3, with ready-time offsets 0 and 2. Their delivery requests reach the elevator at times 5 and 7. Under ⟦E152⟧, separate slots complete the trips at 19 and 21, and the wave finishes at 26. Under ⟦E153⟧, the second request joins the first trip at its loading-end time 7. Both requests finish the elevator trip at 19, giving a wave makespan of 24. Thus, a shared trip can overtake a corresponding independent-slot request, violating (c). In the second instance, ⟦E154⟧ and ⟦E155⟧. The first order travels from floor 1 to floor 8, and the second from floor 8 to floor 7; both have ready-time offset 0. The first order finishes at 49, and the second order’s elevator request is issued at 54. Under ⟦E156⟧, the earliest-available slot is the unused slot at floor 1. Its empty movement to floor 8 takes 35 seconds, producing a wave makespan of 103. Under ⟦E157⟧, the car is already at floor 8, and the wave finishes at 68. No trip is shared; the reversal arises from the unfavorable repositioning distance in (d).