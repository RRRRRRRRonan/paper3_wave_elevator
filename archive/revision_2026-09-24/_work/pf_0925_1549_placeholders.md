3 Problem formulation

3.1 Problem setting and assumptions

We consider a multi-story warehouse in which a fleet of autonomous mobile robots (AMRs) transports orders between source and destination floors. To serve an order, an AMR travels to the source floor, collects the load, and delivers it to the destination floor. A set of elevators shared by all AMRs provides the only means of changing floors, so the elevators are the vertical resource for which the AMRs compete. Orders released together form a wave, and their source floors, destination floors, and ready times determine the elevator requests generated when the wave is executed. Fig. 3.1(a) illustrates this setting.

⟦FIGURE⟧

Fig. 3.1. Problem setting and serial reservation of one order. (a) A multi-story warehouse in which an AMR fleet shares ⟦E1⟧ elevators. The decision is which ⟦E2⟧ orders from the order pool form the wave ⟦E3⟧ released at ⟦E4⟧. For each order, an AMR carries a load from its source floor to its destination floor. AMRs change floors only by elevator trips, and a car carries up to ⟦E5⟧ AMRs traveling between the same pair of floors. All AMRs and cars start on a common floor ⟦E6⟧, drawn as floor 1. Steps 1 to 4 trace order ⟦E7⟧; order ⟦E8⟧ stays on one floor, so its load needs no elevator trip. (b) Reservation of one order under the true co-occupancy batching evaluator ⟦E9⟧ (Section 3.5.1). The upper lane follows the assigned AMR, which first rides an elevator to the pickup floor if it is elsewhere; the lower lane follows the car that serves its loaded trip. Pickup and drop-off times include movement within a floor (Assumption A4). A request with the same origin and destination floors can join the trip while capacity remains, until loading ends at ⟦E10⟧. Durations are illustrative.

The warehouse management system selects, at the release epoch, a wave of fixed size n from a finite pool of K candidate waves. Resource quantities and operational rules are given, so the decision concerns which orders enter the wave. The fixed size keeps candidates comparable and rules out shortening the completion time by releasing fewer orders. The order data and the candidate pool are known at the release epoch, whereas the representation of the elevator subsystem is uncertain and is described by a family of evaluators. The main formulation selects a structural class, defined by the floor distribution and directional balance of its candidate waves, and implements that choice through a fixed within-class selection rule. Formulating the decision over classes ties the release choice to interpretable properties of a wave. Because the classes are defined by quantiles within the pool, the same class definitions apply to any pool in which every class is nonempty. Class-level performance is obtained by evaluating the candidates of each class, exactly or from a sample, and is compared across elevator representations. Direct candidate selection is specific to one pool and provides a finite-pool benchmark, whose exact value is obtained by evaluating all candidates under the specified evaluator. The decision problem is to choose the class whose median wave makespan is smallest under the least favorable evaluator; the benchmark selects, for a given evaluator, the candidate whose makespan is smallest (Section 3.4).

The formulation rests on the following assumptions.

A1 (single isolated wave): Each decision instance concerns one wave released at time ⟦E11⟧. All AMRs and elevator resources are available on a common floor ⟦E12⟧ at ⟦E13⟧, with no outstanding reservations. No other wave shares these resources, and the evaluation ends when the last selected order is delivered; backlog from earlier waves and interaction with later waves are outside the model.

A2 (single-load AMRs): An AMR carries one order at a time, and the AMR that collects an order also delivers it.

A3 (order information): Every available order has a known source floor, destination floor, and ready-time offset ⟦E14⟧; the order becomes eligible for processing at ⟦E15⟧.

A4 (intra-floor operations): Movement and handling within a floor are represented by fixed pickup and drop-off service durations; intra-floor routing and congestion are not modeled.

A5 (elevator trips): A trip serves one origin-destination pair and consists of an empty repositioning leg from the floor at which the car last became available to the request origin, loading, a loaded leg from origin to destination, and unloading; the travel time of each leg is proportional to the number of floors traversed. An AMR rides an elevator whenever a movement crosses floors.

A6 (evaluator uncertainty): The elevator subsystem is represented by one of several evaluators (Section 3.5) that differ in their representation of capacity and trip-time variability. The applicable representation is not known at the release epoch, so decisions are evaluated under more than one representation; Section 3.4 specifies which representations enter the robust selection, and which one assesses a selected class under trip-time variability.

3.2 Notation and decision variables

3.2.1 Basic indices and parameters

Tables 3.1 and 3.2 summarize the basic indices and input parameters. Candidate-wave descriptors and operational state quantities are introduced with their definitions in Sections 3.3 and 3.5.

Table 3.1. Basic indices and sets

[TABLE]

  | Symbol | Definition

  | ⟦E16⟧ | warehouse-floor index

  | ⟦E17⟧ | order index in the available order pool

  | ⟦E18⟧ | AMR index

  | ⟦E19⟧ | physical-elevator index

  | ⟦E20⟧ | candidate-wave index

  | ⟦E21⟧ | selectable structural-class label (Section 3.3.3); the reference class, labeled ⟦E22⟧, lies outside ⟦E23⟧ and serves only as a comparison baseline

  | ⟦E24⟧ | elevator-evaluator index

[/TABLE]

Table 3.2. Input parameters

[TABLE]

  | Symbol | Definition

  | ⟦E25⟧ | number of warehouse floors

  | ⟦E26⟧ | number of AMRs

  | ⟦E27⟧ | number of physical elevator cars

  | ⟦E28⟧ | maximum number of AMRs sharing one physical elevator trip

  | ⟦E29⟧ | fixed number of orders in a wave

  | ⟦E30⟧ | number of candidate waves in the finite pool

  | ⟦E31⟧ | decision and release epoch of the wave

  | ⟦E32⟧ | common initial floor of the AMRs and elevator resources

  | ⟦E33⟧ | source and destination floors of order ⟦E34⟧

  | ⟦E35⟧ | ready-time offset relative to ⟦E36⟧

  | ⟦E37⟧ | elevator travel time per traversed floor

  | ⟦E38⟧ | elevator loading and unloading durations

  | ⟦E39⟧ | AMR pickup and drop-off service durations

  | ⟦E40⟧ | tail probability for structural-class construction

  | ⟦E41⟧ | standard deviation of the logarithm of each phase multiplier under ⟦E42⟧

[/TABLE]

The resource counts, capacity, and candidate-pool size are positive integers, and ⟦E43⟧. All service durations and time offsets use the same time unit. The numerical values of the parameters in Table 3.2, the generator of the order pool ⟦E44⟧ and of the ready-time offsets, and the sample sizes used to estimate class statistics are specified in Section 5.

3.2.2 Selection variables

The class formulation chooses a class label ⟦E45⟧, and the candidate benchmark chooses a candidate index ⟦E46⟧; each decision selects one element of a finite set. Section 3.4 states the two decisions as optimization problems, and Section 3.5.1 writes both as one binary program in the variables of Table 3.3, with score coefficients supplied by the operational evaluation.

Table 3.3. Variables in the class and candidate formulations

[TABLE]

  | Variable | Domain | Definition

  | ⟦E47⟧ | {0, 1} | 1 if option ⟦E48⟧ is selected, and 0 otherwise (⟦E49⟧ for the class formulation, ⟦E50⟧ for the candidate benchmark)

  | ⟦E51⟧ | ⟦E52⟧ | auxiliary upper bound on the selected option’s scores over the evaluator family of the program

[/TABLE]

3.2.3 Evaluation notation

Each candidate wave is evaluated by reserving resources in a prescribed processing sequence. For candidate ⟦E53⟧, ⟦E54⟧ is its order set and ⟦E55⟧ is the processing sequence recorded when its orders are drawn during candidate generation (Section 3.3.1). The pair ⟦E56⟧ is fixed before evaluation and shared by all evaluators. The index ⟦E57⟧ denotes a position in the sequence:

[DISPLAY] ⟦E58⟧

Under the generation procedure, the recorded sequence ⟦E59⟧ is equally likely to be any permutation of the order set ⟦E60⟧. Because each candidate keeps its recorded sequence under every evaluator, differences between evaluators on the same candidate do not arise from resequencing. Across candidates, the sequences vary and contribute to the outcome variation within a class. All class and candidate results use the recorded sequences; Section 5 reports one alternative operational dispatch rule, which reorders the sequence, as a separately labeled robustness check.

Under ⟦E61⟧, this evaluation also incorporates variation in trip-phase durations. Each newly reserved trip receives four multipliers ⟦E62⟧ for empty repositioning, loading, loaded travel, and unloading, respectively. These multipliers are independent across phases and trips, and each multiplier Z satisfies

[DISPLAY] ⟦E63⟧

The collection of phase multipliers used in a wave evaluation is denoted by ⟦E64⟧, where ⟦E65⟧ is the realization space. The phase multipliers are independent of the within-class candidate draw ⟦E66⟧ introduced in Section 3.3.3. Given a candidate k, an evaluator m, and when ⟦E67⟧, a phase-time realization ⟦E68⟧, the operational rules determine all state quantities and order completion times. The dependence of operational states on these inputs is omitted from their notation.

3.3 Candidate waves and structural classes

3.3.1 Candidate waves

Each candidate index ⟦E69⟧ identifies an order set ⟦E70⟧ and its recorded processing sequence ⟦E71⟧. Each candidate is generated by drawing ⟦E72⟧ distinct orders uniformly at random from ⟦E73⟧, and the ⟦E74⟧ candidates are generated independently before selection. Evaluators compared on the same decision, as in the robust selection of Section 3.4.2, use the same pool; Section 5 states whether the pools of each experiment are shared across evaluators. Every candidate has the fixed size

[DISPLAY] ⟦E75⟧

3.3.2 Wave descriptors

The floor distribution of a wave is measured using both endpoints of every order. For a candidate wave ⟦E76⟧, ⟦E77⟧ denotes the proportion of its ⟦E78⟧ endpoints located on floor ⟦E79⟧:

[DISPLAY] ⟦E80⟧

where ⟦E81⟧ is the indicator function. Endpoint dispersion is represented by the entropy

[DISPLAY] ⟦E82⟧

Here ⟦E83⟧ denotes the natural logarithm. Larger C reflects greater diversity in the endpoint distribution across floor labels, arising from broader support or a more even distribution. C depends only on how endpoints are distributed over the floors, not on the distances between them; travel distances enter the evaluation through the floor differences in Equations (24), (28), and (30). Directional imbalance measures the asymmetry between upward and downward order movements. The numbers of upward and downward orders are

[DISPLAY] ⟦E84⟧

The absolute difference is normalized by the number of cross-floor orders:

[DISPLAY] ⟦E85⟧

Thus ⟦E86⟧, with zero indicating balanced cross-floor counts or the absence of cross-floor orders, and one indicating movement in only one direction. Same-floor orders do not contribute to either count. The ready-time dispersion ⟦E87⟧ measures how order eligibility is spread within the wave. The mean ready-time offset is ⟦E88⟧, and ⟦E89⟧ is the coefficient of variant of the offset:

[DISPLAY] ⟦E90⟧

Smaller T indicates more compact ready-time offsets relative to their mean. When all orders are ready at the release epoch, ⟦E91⟧. The resulting descriptor vector is

[DISPLAY] ⟦E92⟧

3.3.3 Structural classes and within-class selection

The class construction uses the lower and upper tails of C and I; T records temporal variation separately and does not enter the corner classes or the selection problems of this section. It is retained in Equation (9) as a descriptor of the released wave under staggered ready times and is used only in the sensitivity analyses of Section 5. For descriptor ⟦E93⟧, ⟦E94⟧ denotes its empirical ⟦E95⟧-quantile over the candidate pool, computed by linear interpolation between the adjacent order statistics at position ⟦E96⟧. A common tail probability ⟦E97⟧ defines four candidate-index sets:

[DISPLAY] ⟦E98⟧

A corner class consists of candidates lying in a tail region of both descriptors. In the labels ⟦E99⟧, the first letter records the tail of ⟦E100⟧ and the second the tail of ⟦E101⟧. Section 5 writes these labels as HC-HI, HC-LI, LC-HI, and LC-LI, respectively. The candidate-index supports are

[DISPLAY] ⟦E102⟧

The selectable labels form ⟦E103⟧. A class-selection instance requires ⟦E104⟧ for every ⟦E105⟧, so that the class median in Equation (14) is defined for every selectable class. For continuous and independent descriptors, each class contains approximately a fraction ⟦E106⟧ of the pool. The fraction can differ when ⟦E107⟧ and ⟦E108⟧ are dependent. It can also differ when a descriptor takes few distinct values, because the inclusive thresholds in Equation (10) assign every candidate tied at a threshold to the tail set. The classes need not cover the pool, since candidates outside the four intersections belong to no class. Conversely, when ties make the lower and upper thresholds of a descriptor coincide, a candidate can belong to more than one class. Section 5 reports the realized class sizes and overlaps.

[DISPLAY] ⟦E109⟧

Selecting class q releases the wave ⟦E110⟧ with ⟦E111⟧. The class choice thus determines the distribution of the released wave, while the within-class rule is fixed. Repeated draws from ⟦E112⟧ are independent draws with replacement from the finite set ⟦E113⟧, so the same candidate can be released, or evaluated, more than once; the candidate identity of every evaluated draw is recorded, so that repeated candidates in an evaluated sample can be identified. The unrestricted pool defines a reference class, labeled ⟦E114⟧, with ⟦E115⟧ for every ⟦E116⟧. It is not a decision option; it is the baseline against which Section 4 measures the value of class selection.

3.4 Objective functions

3.4.1 Wave completion measure

With the candidate, evaluator, and phase-time realization made explicit, ⟦E117⟧denotes the completion time of the order in position j of candidate k (Section 3.5.1). Wave makespan measures elapsed time from release until the last selected order is delivered:

[DISPLAY] ⟦E118⟧

For ⟦E119⟧ and ⟦E120⟧, the outcome is deterministic and the argument ⟦E121⟧ is omitted. Under ⟦E122⟧, Equation (13) defines the makespan for one phase-time realization.

3.4.2 Robust structural-class selection

The performance of a class is the median makespan induced by its fixed release distribution. We use the median because Section 4 states its class-level diagnosis for it and Section 5 reports it for each class, so the decision problem, the analysis, and the experiments share one estimand. When the median is non-unique, we use the midpoint of its median interval. For ⟦E123⟧ and ⟦E124⟧, the class median is defined as

[DISPLAY] ⟦E125⟧

For ⟦E126⟧ and ⟦E127⟧, variation in Equation (14) arises from the candidate draw. Under ⟦E128⟧, the distribution includes both candidate variation and phase-time noise, and the median is taken over this joint outcome distribution. When evaluators are compared, the same draw ⟦E129⟧ is evaluated under every evaluator, with the phase-time realization ⟦E130⟧ drawn independently of ⟦E131⟧. The corresponding class mean is ⟦E132⟧. This mean enters the complementary distributional analysis of Section 4 and its numerical assessment in Section 5; the class-selection objective uses the median.

Under a single evaluator ⟦E133⟧, the nominal class selection is ⟦E134⟧. The deterministic evaluator family is ⟦E135⟧. Its two members represent two hypotheses on how elevator capacity acts: as parallel single-request slots under ⟦E136⟧ or as shared trips under ⟦E137⟧. The robust selection hedges against this structural uncertainty, and Section 4.3 gives sufficient conditions under which the two evaluators are ordered. ⟦E138⟧ retains the reservation rules of ⟦E139⟧ rather than a third capacity hypothesis, and it is used to assess a selected class under trip-time variability. The robust class decision minimizes the larger of its two median makespans:

[DISPLAY] ⟦E140⟧

The class medians are not observed at the release epoch; Section 4.1 obtains them by evaluating the candidates of each class, exactly or by sampling, and applies the selection rule to the resulting scores. Section 4 also diagnoses a descriptor-based class rule that selects a label ⟦E141⟧ from the signs of a relation between makespan and ⟦E142⟧ fitted on an evaluated training sample under a given evaluator; that rule is distinct from the within-class draw of Equation (12), and its fitting sample is specified in Section 5.

3.4.3 Candidate-wave benchmarks

Direct candidate selection uses deterministic scores

[DISPLAY] ⟦E143⟧

For an evaluator ⟦E144⟧, the pool optimum ⟦E145⟧ attains the smallest score,

[DISPLAY] ⟦E146⟧

Because every selection rule of Section 3.4 releases a wave from the same pool, Equation (17) is a lower bound on the makespan attainable under evaluator ⟦E147⟧ by any such rule.

3.5 Constraints and their explanation

3.5.1 Constraint formulation

The three evaluators are serial reservation models, deterministic except for the phase multipliers of ⟦E148⟧. Orders are reserved one at a time along the processing sequence, so the evaluators do not simulate concurrent execution, and the request times they generate need not increase along the sequence. Fig. 3.1(b) illustrates the reservation of one order. Section 5 cross-validates the evaluators against an event-driven simulation that uses the same physical specification but executes trips concurrently.

Processing sequence and AMR assignment. Each order’s complete route is reserved before the next order is considered. After the first ⟦E149⟧ orders have been reserved, ⟦E150⟧ denotes the next availability time of AMR a and ⟦E151⟧ the floor at which it becomes available; initially, ⟦E152⟧ and ⟦E153⟧. For a finite index set ⟦E154⟧ and real values ⟦E155⟧, ⟦E156⟧, ⟦E157⟧ denotes the smallest index among those attaining ⟦E158⟧. This rule makes each selection in Equations (18), (23), and (27) unique. Order ⟦E159⟧ is assigned to the earliest-available AMR, with ties resolved by AMR index, and begins at

[DISPLAY] ⟦E160⟧

An elevator request specifies an origin g, a destination ⟦E161⟧, and a request time t. The elevator reservation state is denoted by ⟦E162⟧. The request updates this state and returns a completion time:

[DISPLAY] ⟦E163⟧

Within a fixed evaluation, ⟦E164⟧ denotes the returned time ⟦E165⟧, with every call replacing ⟦E166⟧ by ⟦E167⟧. The assigned AMR first reaches the order’s source and completes pickup:

[DISPLAY] ⟦E168⟧

It then reaches the destination and completes delivery:

[DISPLAY] ⟦E169⟧

After delivery, the assigned AMR becomes available at the destination:

[DISPLAY] ⟦E170⟧

For every ⟦E171⟧, ⟦E172⟧ and ⟦E173⟧.

Throughput abstraction ⟦E174⟧. Evaluator ⟦E175⟧ represents E elevators of capacity c by Ec independent single-request service slots, indexed by ⟦E176⟧. Each slot has a next availability time ⟦E177⟧ and a floor ⟦E178⟧ associated with that availability, initially ⟦E179⟧ and ⟦E180⟧. A request uses

[DISPLAY] ⟦E181⟧

Its completion time is

[DISPLAY] ⟦E182⟧

The selected slot is updated to ⟦E183⟧ and ⟦E184⟧; all other slots retain their states. The slots represent capacity as parallelism: ⟦E185⟧ cars of capacity ⟦E186⟧ under ⟦E187⟧ coincide with ⟦E188⟧ cars of unit capacity, and every request occupies a slot for a full trip. ⟦E189⟧ and ⟦E190⟧ use the same trip durations; they differ only in the number of servers that can run in parallel and in whether requests share a trip. Each slot carries one request per trip, the single-rider assumption that Chakravarty et al. (2025) adopt for multi-robot lift scheduling, in which each lift serves one robot at a time.

True co-occupancy batching ⟦E191⟧. Evaluator ⟦E192⟧ uses E physical cars, each accommodating at most c AMRs on a trip. For each car e, the evaluator stores its next availability ⟦E193⟧, associated floor ⟦E194⟧, and latest reserved trip. That trip is described by its origin-destination pair ⟦E195⟧, loading-end time ⟦E196⟧, completion time ⟦E197⟧, and reserved occupancy ⟦E198⟧. Initially, ⟦E199⟧, ⟦E200⟧, no trip pair is stored, ⟦E201⟧, and ⟦E202⟧. A request can share a stored trip when its origin and destination match those of the trip, the trip has remaining capacity, and the request time is no later than the end of loading. The boardable-car set is

[DISPLAY] ⟦E203⟧

If ⟦E204⟧, the lowest-index eligible car is selected:

[DISPLAY] ⟦E205⟧

The joining request shares the trip’s stored completion time; apart from the occupancy update in Equation (26), the car's reservation record is unchanged. A request may also join a trip that starts after its request time, in which case it waits for that trip. When ⟦E206⟧, the request creates a new trip on the earliest-available car, with equal availability resolved by car index:

[DISPLAY] ⟦E207⟧

Using the car’s pre-update state, the new loading-end and completion times are

[DISPLAY] ⟦E208⟧

The elevator returns ⟦E209⟧ and updates the car’s reservation record:

[DISPLAY] ⟦E210⟧

The new trip replaces that car’s stored trip record, and subsequent requests test Equation (25) against the latest record of each car. A stored trip serves one origin-destination pair and makes no intermediate stops; a request with a different pair, or one arriving after loading has ended, uses a separate trip. ⟦E211⟧shares a trip only among requests with the same origin and destination. This is a restricted form of the destination-based grouping of destination group control, in which requests from a common origin are assigned to cars by destination until the car capacity is reached (So et al., 2022) .

Stochastic batching ⟦E212⟧. Evaluator ⟦E213⟧ retains the car-assignment, boarding, and capacity rules of ⟦E214⟧. The loading-end and completion times of a new trip become

[DISPLAY] ⟦E215⟧

The reservation update follows Equation (29). Both a newly reserved request and a joining request return ⟦E216⟧. Requests joining the same trip share this stored completion time, with no additional phase draws.

Resource conditions. The reservation rules enforce the following conditions, which are the feasibility requirements of the wave-level schedule:

[DISPLAY] ⟦E217⟧

The first condition requires order readiness, the second requires that an AMR start its next order only after delivering the current one, and the third bounds the occupancy of a shared trip. In addition, trips reserved on the same car, or on the same slot under ⟦E218⟧, do not overlap. Each new trip begins its empty repositioning at ⟦E219⟧, where ⟦E220⟧ is the completion time of the previous trip on that car (⟦E221⟧ for a slot under ⟦E222⟧). These conditions are implied by Equations (18) to (30); the first two hold for all three evaluators, and the third for the two evaluators under which trips are shared.

Selection program. Both decisions of Section 3.4 select one option from a finite index set ⟦E223⟧ with score coefficients ⟦E224⟧: the class formulation has ⟦E225⟧, ⟦E226⟧, and evaluator family ⟦E227⟧; the pool optimum under evaluator ⟦E228⟧ has ⟦E229⟧, ⟦E230⟧, and ⟦E231⟧. With the variables of Table 3.3, the common program is

[DISPLAY] ⟦E232⟧

Equation (32) reproduces Equation (15) for ⟦E233⟧ and Equation (17) for ⟦E234⟧.

3.5.2 Explanation of constraints

Processing sequence and AMR assignment. The processing sequence is the candidate-specific permutation ⟦E235⟧ in Equation (1) and is not reordered by readiness. An order that is not yet eligible holds its assigned AMR until ⟦E236⟧, which the maximum in Equation (18) enforces together with resource availability. Equations (20) and (21) activate an elevator request only when a movement crosses floors. A same-floor order can still require an initial elevator trip if its assigned AMR is on a different floor. Pickup and drop-off advance the AMR clock by their fixed service durations, and each order updates the state of its assigned AMR, so subsequent assignments use the resulting availability times.

Throughput abstraction ⟦E237⟧. Equation (24) charges every request its waiting time and a complete trip of repositioning, loading, loaded travel, and unloading. Capacity therefore acts only through the number of slots that can serve requests at the same time, and two requests with the same origin and destination never share a trip.

True co-occupancy batching ⟦E238⟧. Trips are reserved in the order of the processing sequence, so a new trip starts only after the trips already reserved on its car have been completed, even when its request time is earlier. The boarding test in Equation (25) also takes priority over new-trip assignment in Equations (27)–(29), so an eligible shared trip is selected even when a dedicated trip on another car could finish sooner.

Stochastic batching ⟦E239⟧. Only the four elevator trip phases carry multipliers. Waiting times carry none and change only as a consequence of the perturbed durations of earlier trips, while pickup and drop-off durations remain fixed.

Resource conditions. Equation (31) collects the feasibility requirements that the reservation rules already enforce: order readiness through the maximum in Equation (18), sequential use of each AMR through the availability update in Equation (22), and trip occupancy through the boarding test in Equation (25). They are stated separately so that the wave-level schedule can be checked without re-deriving the recursions.

Selection program. The first constraint of Equation (32) selects exactly one option; the score constraints bound ⟦E240⟧ below by the selected option’s score under each evaluator in ⟦E241⟧, and minimization makes ⟦E242⟧ equal to the largest of those scores. A selected class is implemented through Equation (12); the pool optimum releases the selected candidate directly.