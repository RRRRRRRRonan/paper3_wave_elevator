3 Problem formulation

3.1 Problem setting and assumptions

We consider a multi-story warehouse in which autonomous mobile robots (AMRs) transport orders between source and destination floors. The elevators are shared by all AMRs and are the only means of changing floors, so they are the vertical resource for which the AMRs contend. An AMR travels to an order’s source, collects the load, and delivers it to the destination. The orders released together form a wave. Their origins, destinations, and ready times determine the vertical transport requests generated during wave execution. Fig. 1(a) sketches this setting.

⟦FIGURE⟧

Fig. 1. (a) Multi-story warehouse with an AMR fleet sharing ⟦E1⟧ elevators; a wave is a set of orders with source and destination floors, and AMRs change floors only by elevator trips; all resources start on the common floor ⟦E2⟧ at the release epoch ⟦E3⟧. (b) Serial reservation of one order ⟦E4⟧ under ⟦E5⟧: the AMR clock (available at ⟦E6⟧, ready at ⟦E7⟧, start ⟦E8⟧, pickup, delivery) and the five phases of the loaded elevator trip (wait, reposition, load, travel, unload); a request with the same origin-destination pair may join the trip until loading ends at ⟦E9⟧. Durations are illustrative.

The warehouse management system selects, at the release epoch, a wave of fixed size n from a finite pool of K candidate waves. Resource quantities and operational rules are given, so the decision concerns which orders enter the wave. The fixed size keeps candidates comparable and rules out shortening the completion time by releasing fewer orders. The order data and the candidate pool are known at the release epoch, whereas the representation of the elevator subsystem is uncertain and is described by a family of evaluators. The main formulation selects a structural class, defined by the floor distribution and directional balance of its candidate waves, and implements that choice through a fixed within-class selection rule. Class-level performance is estimated from evaluated samples and compared across elevator representations. Direct candidate selection provides a finite-pool benchmark whose exact value is obtained by evaluating all candidates under the specified evaluator. The decision problem is to choose the class whose median wave makespan is smallest under the least favorable evaluator; the benchmark selects, for a given evaluator, the candidate whose makespan is smallest (Section 3.4).

The formulation rests on the following assumptions.

A1 (single isolated wave): Each decision instance concerns one wave released at time ⟦E10⟧. All AMRs and elevator resources are available on a common floor ⟦E11⟧ at ⟦E12⟧, with no outstanding reservations. No other wave shares these resources, and the evaluation ends when the last selected order is delivered; backlog from earlier waves and interaction with later waves are outside the model.

A2 (single-load AMRs): An AMR carries one order at a time, and the AMR that collects an order also delivers it.

A3 (order information): Every available order has a known source floor, destination floor, and ready-time offset ⟦E13⟧; the order becomes eligible for processing at ⟦E14⟧.

A4 (intra-floor operations): Movement and handling within a floor are represented by fixed pickup and drop-off service durations; intra-floor routing and congestion are not modeled.

A5 (elevator trips): A trip serves one origin-destination pair and consists of an empty repositioning leg from the floor at which the car last became available to the request origin, loading, a loaded leg from origin to destination, and unloading; the travel time of each leg is proportional to the number of floors traversed. An AMR rides an elevator whenever a movement crosses floors.

A6 (evaluator uncertainty): The elevator subsystem is represented by one of several evaluators (Section 3.5) that differ in their representation of capacity and trip-time variability. The applicable representation is not known at the release epoch, so decisions are evaluated under more than one representation; Section 3.4 specifies which representations enter the robust selection, and which one assesses a selected class under trip-time variability.

3.2 Notation and decision variables

3.2.1 Basic indices and parameters

Tables 3.1 and 3.2 summarize the basic indices and input parameters. Candidate-wave descriptors and operational state quantities are introduced with their definitions in Sections 3.3 and 3.5.

Table 3.1. Basic indices and sets

[TABLE]

  | Symbol | Definition

  | ⟦E15⟧ | warehouse-floor index

  | ⟦E16⟧ | order index in the available order pool

  | ⟦E17⟧ | AMR index

  | ⟦E18⟧ | physical-elevator index

  | ⟦E19⟧ | candidate-wave index

  | ⟦E20⟧ | selectable structural-class label (Section 3.3.3); the reference class, labeled ⟦E21⟧, lies outside ⟦E22⟧ and serves only as a comparison baseline

  | ⟦E23⟧ | elevator-evaluator index

[/TABLE]

Table 3.2. Input parameters

[TABLE]

  | Symbol | Definition

  | ⟦E24⟧ | number of warehouse floors

  | ⟦E25⟧ | number of AMRs

  | ⟦E26⟧ | number of physical elevator cars

  | ⟦E27⟧ | maximum number of AMRs sharing one physical elevator trip

  | ⟦E28⟧ | fixed number of orders in a wave

  | ⟦E29⟧ | number of candidate waves in the finite pool

  | ⟦E30⟧ | decision and release epoch of the wave

  | ⟦E31⟧ | common initial floor of the AMRs and elevator resources

  | ⟦E32⟧ | source and destination floors of order ⟦E33⟧

  | ⟦E34⟧ | order-ready offset relative to ⟦E35⟧

  | ⟦E36⟧ | elevator travel time per traversed floor

  | ⟦E37⟧ | elevator loading and unloading durations

  | ⟦E38⟧ | AMR pickup and drop-off service durations

  | ⟦E39⟧ | tail probability for structural-class construction

  | ⟦E40⟧ | lognormal phase-time noise parameter under ⟦E41⟧

[/TABLE]

The resource counts, capacity, and candidate-pool size are positive integers, and ⟦E42⟧. All service durations and time offsets use the same time unit. The numerical values of the parameters in Table 3.2, the generator of the order pool ⟦E43⟧ and of the ready-time offsets, and the sample sizes used to estimate class statistics are specified in Section 5.

3.2.2 Selection variables

The decision of the class formulation is the class label ⟦E44⟧, and the decision of the candidate benchmark is the candidate index ⟦E45⟧. Both decisions select one element from a finite set. The class decision solves Equation (15), while the candidate decision attains the minimum in Equation (17). Equation (32) expresses both decisions through a common binary program using the variables in Table 3.3. Their score coefficients are supplied by the operational evaluation of Section 3.5.

Table 3.3. Variables in the class and candidate formulations.

[TABLE]

  | Variable | Domain | Definition

  | ⟦E46⟧ | {0, 1} | 1 if option ⟦E47⟧ of the index set ⟦E48⟧ is selected (⟦E49⟧ for classes, ⟦E50⟧ for candidates)

  | ⟦E51⟧ | ⟦E52⟧ | auxiliary upper bound on the selected option’s scores over the evaluator family of the program

[/TABLE]

3.2.3 Evaluation notation

Each candidate wave is evaluated by reserving resources in a prescribed processing sequence. For candidate ⟦E53⟧, ⟦E54⟧ is its order set and ⟦E55⟧ is the processing sequence recorded when its orders are drawn during candidate generation (Section 3.3.1). The pair ⟦E56⟧ is fixed before evaluation and shared by all evaluators. The index ⟦E57⟧ denotes a position in the sequence:

[DISPLAY] ⟦E58⟧

Conditional on the selected order set, each permutation is equally likely under the candidate-generation procedure. Each candidate retains its recorded sequence across evaluators, so their comparison uses the same prescribed order sequence. Variation in these recorded sequences contributes to within-class outcome variation. All class and candidate results use the recorded sequences; Section 5 reports an alternative operational dispatch rule that reorders the sequence as a separately labeled robustness check.

Under ⟦E59⟧, this evaluation also incorporates variation in trip-phase durations. Each newly reserved trip receives four multipliers ⟦E60⟧ for empty repositioning, loading, loaded travel, and unloading, respectively. These multipliers are independent across phases and trips, and each multiplier Z satisfies

[DISPLAY] ⟦E61⟧

The collection of phase multipliers used in a wave evaluation is denoted by ⟦E62⟧, where ⟦E63⟧ is the realization space. The phase-noise source is independent of the within-class candidate draw ⟦E64⟧ introduced in Section 3.3.3. Given a candidate wave k, an evaluator m, and a phase-time realization ⟦E65⟧ when ⟦E66⟧, the operational rules determine all state quantities and order completion times. The dependence of operational states on these inputs is omitted from their notation.

3.3 Candidate waves and structural classes

3.3.1 Candidate waves

Each candidate index ⟦E67⟧ identifies an unordered order set ⟦E68⟧ containing ⟦E69⟧ orders and its recorded processing sequence ⟦E70⟧. Each candidate is generated by drawing ⟦E71⟧ distinct orders uniformly at random from ⟦E72⟧, and the ⟦E73⟧ candidates are generated independently before selection. Whenever two evaluators are compared on the same decision, as in the robust selection of Section 3.4.2, the same pool is used for both; Section 5 states, for each experimental block, whether the pool is shared across evaluators. Every candidate has the fixed size

[DISPLAY] ⟦E74⟧

3.3.2 Wave descriptors

The floor distribution of a wave is measured using both endpoints of every order. For a candidate wave ⟦E75⟧, ⟦E76⟧ denotes the proportion of its ⟦E77⟧ endpoints located on floor ⟦E78⟧:

[DISPLAY] ⟦E79⟧

where ⟦E80⟧ is the indicator function. Endpoint dispersion is represented by the entropy

[DISPLAY] ⟦E81⟧

Here ⟦E82⟧ denotes the natural logarithm. Larger C reflects greater diversity in the endpoint distribution across floor labels, arising from broader support or a more even distribution. It describes how endpoints are distributed among floors; travel distances are determined by the numerical differences between the relevant floor indices. Directional imbalance measures the asymmetry between upward and downward order movements. Their counts are

[DISPLAY] ⟦E83⟧

The absolute difference is normalized by the number of cross-floor orders:

[DISPLAY] ⟦E84⟧

Thus ⟦E85⟧, with zero indicating balanced cross-floor counts or the absence of cross-floor orders, and one indicating movement in only one direction. Same-floor orders do not contribute to either count. Ready-time dispersion measures how order eligibility is spread within the wave. The mean ready-time offset is ⟦E86⟧, and its relative dispersion is defined as

[DISPLAY] ⟦E87⟧

Smaller T indicates more compact ready-time offsets relative to their mean. When all orders are ready at the release epoch, ⟦E88⟧. The resulting descriptor vector is

[DISPLAY] ⟦E89⟧

3.3.3 Structural classes and within-class selection

The class construction uses the lower and upper tails of C and I; T records temporal variation separately. For descriptor ⟦E90⟧, ⟦E91⟧ denotes its empirical ⟦E92⟧-quantile over the candidate pool, computed by linear interpolation between order statistics. A common tail probability ⟦E93⟧ defines four candidate-index sets:

[DISPLAY] ⟦E94⟧

A corner class consists of candidates lying in a tail region of both descriptors. The labels ⟦E95⟧ record the tails of ⟦E96⟧ and ⟦E97⟧, respectively (written HC-HI, HC-LI, LC-HI, LC-LI, in the same order, where Sections 4 and 5 report per-corner results), with candidate-index supports

[DISPLAY] ⟦E98⟧

The selectable labels form ⟦E99⟧, the corner labels of Equation (11). A class-selection instance requires ⟦E100⟧ for every ⟦E101⟧, so that the class median of Equation (14) is defined for every selectable class. For continuous, independent descriptors the fraction of the pool in each class is of order ⟦E102⟧; it can differ from this value when ⟦E103⟧ and ⟦E104⟧ are dependent, and also when the descriptors take few distinct values, because the inclusive thresholds in Equation (10) place every candidate tied at a threshold into the tail set. Candidates outside all four intersections remain in the candidate pool but outside the corner classes, so the classes do not cover the pool. Because the tail inequalities include their thresholds, quantile ties can produce overlapping supports, in which case a candidate belongs to more than one class; this affects the sampling distributions below but not their definitions. Section 5 reports the realized class sizes and overlaps. Each selectable class is implemented by uniform sampling over its candidate indices. The fixed within-class distribution is

[DISPLAY] ⟦E105⟧

Selecting class q therefore leads to a draw ⟦E106⟧ and the release of ⟦E107⟧. The class choice determines the distribution of the released wave, while its within-class sampling rule remains fixed. Repeated draws from ⟦E108⟧ are independent draws with replacement from the finite set ⟦E109⟧, so the same candidate can be released, or evaluated, more than once; the candidate identity of every evaluated draw is recorded, so that repeated candidates in an evaluated sample can be identified. The unrestricted pool defines a reference class, labeled ⟦E110⟧, with ⟦E111⟧ for every ⟦E112⟧. It is not a decision option; it is the baseline against which Section 4 measures the value of class selection.

3.4 Objective functions

3.4.1 Wave completion measure

Restoring the candidate, evaluator, and realization indices gives the order completion time ⟦E113⟧. Wave makespan measures elapsed time from release until the last selected order is delivered:

[DISPLAY] ⟦E114⟧

For ⟦E115⟧ and ⟦E116⟧, the outcome is deterministic and the argument ⟦E117⟧ is omitted. Under ⟦E118⟧, Equation (13) defines the makespan for one phase-time realization.

3.4.2 Robust structural-class selection

The performance of a class is the median makespan induced by its fixed release distribution. The median is the statistic for which the class-level decomposition of Section 4 is stated and the statistic that Section 5 estimates per class, so using it here keeps the decision problem, the analysis, and the experiments on one estimand. When the median is non-unique, we use the midpoint of its median interval. For ⟦E119⟧ and ⟦E120⟧, the class median is defined as

[DISPLAY] ⟦E121⟧

For ⟦E122⟧ and ⟦E123⟧, variation in Equation (14) arises from the candidate draw. Under ⟦E124⟧, the distribution includes both candidate variation and phase-time noise, and the median is taken over this joint outcome distribution. When evaluators are compared, the same draw ⟦E125⟧ is evaluated under every evaluator, with the phase-time realization ⟦E126⟧ drawn independently of ⟦E127⟧. The corresponding class mean is ⟦E128⟧. This mean is used in the complementary distributional analysis in Section 4 and its numerical assessment in Section 5. The class-selection objective in this formulation uses the median defined in Equation (14).

Under a single evaluator ⟦E129⟧, the nominal class selection is ⟦E130⟧. The deterministic evaluator family is ⟦E131⟧. Its two members are distinct hypotheses about how elevator capacity acts, parallel slots under ⟦E132⟧ versus shared trips under ⟦E133⟧, and this is the uncertainty the robust selection covers. ⟦E134⟧ retains the reservation rules of ⟦E135⟧ and adds mean-one phase multipliers (Equation (2)), so it is a perturbation of ⟦E136⟧ rather than a third capacity hypothesis; it assesses a selected class under trip-time variability, and Section 4 characterizes the ordering within ⟦E137⟧. The robust class decision minimizes the larger of its two median makespans:

[DISPLAY] ⟦E138⟧

The class medians are not observed at the release epoch; Section 5 estimates them from evaluated samples of each class, and Section 4 analyzes selection rules that act on such estimates. Section 4 also diagnoses a descriptor-based class rule that selects a label ⟦E139⟧ from the signs of a relation between makespan and ⟦E140⟧ fitted on an evaluated training sample under a given evaluator; that rule is distinct from the within-class draw of Equation (12), and its fitting sample is specified in Section 5.

3.4.3 Candidate-wave benchmarks

Direct candidate selection uses deterministic scores

[DISPLAY] ⟦E141⟧

For an evaluator ⟦E142⟧, the pool optimum ⟦E143⟧ attains the smallest score,

[DISPLAY] ⟦E144⟧

Because every selection rule of Section 3.4 releases a wave from the same pool, Equation (17) is a lower bound on the makespan attainable under evaluator ⟦E145⟧ by any such rule.

3.5 Constraints and their explanation

3.5.1 Constraint formulation

The evaluators are deterministic serial reservation models, apart from the phase noise of ⟦E146⟧: they do not simulate concurrent execution, and the request timestamps generated along the processing sequence need not be globally increasing; Fig. 1(b) illustrates the reservation of one order. Section 5 cross-validates them against an event-driven simulation that is built on the same physical specification but executes trips concurrently.

Processing sequence and AMR assignment. Each order’s complete route is reserved before the next order is considered. The quantities ⟦E147⟧ and ⟦E148⟧ denote AMR a’s next availability time and associated floor after the first ⟦E149⟧ orders have been reserved, respectively, with initial values ⟦E150⟧ and ⟦E151⟧. For a finite index set ⟦E152⟧ and real values ⟦E153⟧, ⟦E154⟧, ⟦E155⟧ denotes the smallest index among those attaining ⟦E156⟧. This rule makes each selection in Equations (18), (23), and (27) unique. Order ⟦E157⟧ is assigned to the earliest-available AMR, with ties resolved by AMR index, and begins at

[DISPLAY] ⟦E158⟧

An elevator request specifies an origin g, a destination ⟦E159⟧, and a request time t. The elevator reservation state is denoted by ⟦E160⟧. The request updates this state and returns a completion time:

[DISPLAY] ⟦E161⟧

Within a fixed evaluation, ⟦E162⟧ denotes the returned time ⟦E163⟧, with every call replacing ⟦E164⟧ by ⟦E165⟧. The assigned AMR first reaches the order’s source and completes pickup:

[DISPLAY] ⟦E166⟧

It then reaches the destination and completes delivery:

[DISPLAY] ⟦E167⟧

After delivery, the assigned AMR becomes available at the destination:

[DISPLAY] ⟦E168⟧

For every ⟦E169⟧, ⟦E170⟧ and ⟦E171⟧.

Throughput abstraction ⟦E172⟧. Evaluator ⟦E173⟧ represents E elevators of capacity c by Ec independent single-request service slots, indexed by ⟦E174⟧. Each slot has a next availability time ⟦E175⟧ and a floor ⟦E176⟧ associated with that availability, initially ⟦E177⟧ and ⟦E178⟧. A request uses

[DISPLAY] ⟦E179⟧

Its completion time is

[DISPLAY] ⟦E180⟧

The selected slot is updated to ⟦E181⟧ and ⟦E182⟧; all other slots retain their states. The slots represent capacity as parallelism: ⟦E183⟧ cars of capacity ⟦E184⟧ under ⟦E185⟧ coincide with ⟦E186⟧ cars of unit capacity, and every request occupies a slot for a full trip. ⟦E187⟧ and ⟦E188⟧ use the same trip durations; they differ only in the number of servers that can run in parallel and in whether requests share a trip.

True co-occupancy batching ⟦E189⟧. Evaluator ⟦E190⟧ uses E physical cars, each accommodating at most c AMRs on a trip. For each car e, the evaluator stores its next availability ⟦E191⟧, associated floor ⟦E192⟧, and latest reserved trip. That trip is described by its origin-destination pair ⟦E193⟧, loading-end time ⟦E194⟧, completion time ⟦E195⟧, and reserved occupancy ⟦E196⟧. Initially, ⟦E197⟧, ⟦E198⟧, no trip pair is stored, ⟦E199⟧, and ⟦E200⟧. A request can share a stored trip when its origin and destination match, capacity remains, and it is ready no later than loading ends. The boardable-car set is

[DISPLAY] ⟦E201⟧

If ⟦E202⟧, the lowest-index eligible car is selected:

[DISPLAY] ⟦E203⟧

The joining request shares the trip’s stored completion time, and its other reservation quantities remain unchanged. A joining request may have a request time earlier than the start of the stored trip; it then waits for that trip and shares its completion time. When ⟦E204⟧, the request creates a new trip on the earliest-available car, with equal availability resolved by car index:

[DISPLAY] ⟦E205⟧

Using the car’s pre-update state, the new loading-end and completion times are

[DISPLAY] ⟦E206⟧

The elevator returns ⟦E207⟧ and updates the car’s reservation record:

[DISPLAY] ⟦E208⟧

The new trip replaces that car’s stored trip record, and subsequent requests test Equation (25) against the latest record of each car. A stored trip serves one origin-destination pair and makes no intermediate stops; a request with a different pair, or one arriving after loading has ended, uses a separate trip.

Stochastic batching ⟦E209⟧. Evaluator ⟦E210⟧ retains the car-assignment, boarding, and capacity rules of ⟦E211⟧. The loading-end and completion times of a new trip become

[DISPLAY] ⟦E212⟧

The reservation update follows Equation (29). Both a newly reserved request and a joining request return ⟦E213⟧. Requests joining the same trip share this stored completion time, with no additional phase draws.

Resource conditions. The reservation rules enforce the following conditions, which are the feasibility requirements of the wave-level schedule:

[DISPLAY] ⟦E214⟧

The first condition requires order readiness, the second requires that an AMR start its next order only after delivering the current one, and the third bounds the occupancy of a shared trip. In addition, trips reserved on the same car (or slot under ⟦E215⟧) do not overlap: a new trip begins its empty repositioning no earlier than ⟦E216⟧ (formally, at ⟦E217⟧), where ⟦E218⟧ is the completion time of that car’s previous trip. These conditions are implied by Equations (18) to (30); the first two hold for all three evaluators, and the third for the two evaluators under which trips are shared.

Selection program. Both decisions of Section 3.4 select one option from a finite index set ⟦E219⟧ with score coefficients ⟦E220⟧: the class formulation has ⟦E221⟧, ⟦E222⟧, and evaluator family ⟦E223⟧; the pool optimum under evaluator ⟦E224⟧ has ⟦E225⟧, ⟦E226⟧, and ⟦E227⟧. With the variables of Table 3.3, the common program is

[DISPLAY] ⟦E228⟧

Equation (32) reproduces Equation (15) for ⟦E229⟧ and Equation (17) for ⟦E230⟧.

3.5.2 Explanation of constraints

Processing sequence and AMR assignment. The processing sequence is the candidate-specific permutation ⟦E231⟧ in Equation (1) and remains unchanged by order readiness; an order that is not yet eligible holds its assigned AMR until ⟦E232⟧, which the maximum in Equation (18) enforces together with resource availability. Equations (20) and (21) activate an elevator request only when a movement crosses floors. A same-floor order can still require an initial elevator trip if its assigned AMR is on a different floor. Pickup and drop-off advance the AMR clock by their fixed service durations, and each order updates the state of its assigned AMR, so subsequent assignments use the resulting availability times.

Throughput abstraction ⟦E233⟧. Equation (24) charges every request the full five-phase trip, so capacity acts only through the number of slots that can serve requests at the same time; two requests with the same origin and destination never share a trip.

True co-occupancy batching ⟦E234⟧. Elevator requests are processed in the prescribed reservation sequence. When the boardable-car set in Equation (25) is nonempty, the request joins the lowest-index eligible car and shares its stored completion time. Otherwise, Equations (27)–(29) reserve a new trip on the earliest-available car, with repositioning starting no earlier than that car’s recorded availability. The boarding test takes priority over new-trip assignment, so an eligible shared trip is selected even when a dedicated trip on another car could finish sooner.

Stochastic batching ⟦E235⟧. Waiting follows from resource availability, while pickup and drop-off durations remain fixed.

Resource conditions. Equation (31) collects the feasibility requirements that the reservation rules already enforce: order readiness through the maximum in Equation (18), sequential use of each AMR through the availability update in Equation (22), and trip occupancy through the boarding test in Equation (25). They are stated separately so that the wave-level schedule can be checked without re-deriving the recursions.

Selection program. The first constraint of Equation (32) selects exactly one option; the score constraints bound ⟦E236⟧ below by the selected option’s score under each evaluator in ⟦E237⟧, and minimization makes ⟦E238⟧ equal to the largest of those scores. A selected class is implemented through Equation (12); the pool optimum releases the selected candidate directly.