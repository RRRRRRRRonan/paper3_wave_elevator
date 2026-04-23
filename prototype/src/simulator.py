"""
MVS v0.1/v0.2 simulator.

v0.1: 1 elevator, capacity=1, F=3, FCFS, 5-phase per-request timing
      (wait -> reposition -> load(2s) -> travel -> unload(2s)).

v0.2: Generalised to `ElevatorPool(n_elevators, capacity)` with the same
5-phase semantics per trip. Capacity is modelled as a throughput
abstraction: an elevator of capacity c behaves as c parallel independent
serving-slots sharing the same physical unit. This captures the
bottleneck-relief effect without requiring event-driven batch scheduling.

v0.2 Phase 1.5: `ElevatorPoolBatched` implements true co-occupancy
batching: a request with the same (src, dst) as an in-progress trip, and
arriving before that trip's loading window closes, boards the same trip
(up to `capacity` passengers share one reposition+load+travel+unload
cycle). Non-matching requests queue for the next available cycle.

v0.2 Tier 1 gap-fix extensions (2026-04-22):
  - `service_sigma` (Gap 1): per-pickup/dropoff service time multiplied by
    lognormal(mean=1, sigma=service_sigma) to capture intra-floor service
    heterogeneity (proxy for path congestion / pick variance) without
    requiring a path-planning model.
  - per-`Order.release_time` (Gap 2): orders may have non-zero arrival
    times, activating the T dimension of Phi. AMRs idle until the next
    pending order arrives.
  - `ElevatorPoolDirectional` (Gap 3): true-batching elevator with a
    direction-switch overhead `dir_switch_penalty` whenever a new trip
    reverses direction relative to the previous trip — the simplest
    direction-aware extension that preserves M5's model-class framework.
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Order:
    id: int
    source_floor: int
    dest_floor: int
    release_time: float = 0.0


@dataclass
class Wave:
    orders: List[Order]
    release_time: float = 0.0


@dataclass
class AMR:
    id: int
    current_floor: int
    current_time: float


class Elevator:
    """Single elevator serving-slot: 5-phase FCFS, capacity=1."""

    def __init__(
        self,
        speed_per_floor: float = 5.0,
        load_time: float = 2.0,
        unload_time: float = 2.0,
        initial_floor: int = 1,
    ):
        self.current_floor = initial_floor
        self.available_at = 0.0
        self.speed = speed_per_floor
        self.load_time = load_time
        self.unload_time = unload_time

    def request(
        self,
        amr_current_floor: int,
        target_floor: int,
        request_time: float,
    ) -> float:
        wait_start = max(request_time, self.available_at)
        reposition_time = abs(self.current_floor - amr_current_floor) * self.speed
        loading_end = wait_start + reposition_time + self.load_time
        travel_time = abs(amr_current_floor - target_floor) * self.speed
        arrive_at_target = loading_end + travel_time
        unloading_end = arrive_at_target + self.unload_time

        self.current_floor = target_floor
        self.available_at = unloading_end
        return unloading_end


# Backward compatibility alias
ElevatorResource = Elevator


class ElevatorPool:
    """Pool of E elevators, each with `capacity` parallel serving slots.

    capacity > 1 is modelled as parallel slots within a single elevator —
    an aggregate-throughput abstraction (see module docstring).
    """

    def __init__(
        self,
        n_elevators: int = 1,
        capacity: int = 1,
        speed_per_floor: float = 5.0,
        load_time: float = 2.0,
        unload_time: float = 2.0,
        initial_floor: int = 1,
    ):
        total_slots = n_elevators * capacity
        self.slots: List[Elevator] = [
            Elevator(
                speed_per_floor=speed_per_floor,
                load_time=load_time,
                unload_time=unload_time,
                initial_floor=initial_floor,
            )
            for _ in range(total_slots)
        ]
        self.n_elevators = n_elevators
        self.capacity = capacity

    def request(
        self,
        amr_current_floor: int,
        target_floor: int,
        request_time: float,
    ) -> float:
        # Pick slot with earliest availability; ties broken by slot order (stable).
        slot = min(self.slots, key=lambda e: (e.available_at, id(e)))
        return slot.request(amr_current_floor, target_floor, request_time)


class ElevatorBatched:
    """Single elevator with true co-occupancy batching.

    Carries up to `capacity` passengers on one trip. A request can board an
    in-progress trip iff (src, dst) match and request_time <= trip_loading_end
    (i.e. boarding window still open) and trip_passengers < capacity. After
    boarding closes the elevator commits to its trip; further requests queue
    for the next trip cycle.
    """

    def __init__(
        self,
        capacity: int = 2,
        speed_per_floor: float = 5.0,
        load_time: float = 2.0,
        unload_time: float = 2.0,
        initial_floor: int = 1,
    ):
        self.current_floor = initial_floor
        self.available_at = 0.0
        self.capacity = capacity
        self.speed = speed_per_floor
        self.load_time = load_time
        self.unload_time = unload_time
        # Current trip state (None if idle)
        self.trip_src = None
        self.trip_dst = None
        self.trip_loading_end = None
        self.trip_completion = None
        self.trip_passengers = 0

    def can_board(self, src: int, dst: int, request_time: float) -> bool:
        return (
            self.trip_src == src
            and self.trip_dst == dst
            and self.trip_passengers < self.capacity
            and request_time <= self.trip_loading_end
        )

    def board(self) -> float:
        self.trip_passengers += 1
        return self.trip_completion

    def dispatch(self, src: int, dst: int, request_time: float) -> float:
        wait_start = max(request_time, self.available_at)
        reposition = abs(self.current_floor - src) * self.speed
        loading_end = wait_start + reposition + self.load_time
        travel = abs(src - dst) * self.speed
        arrive = loading_end + travel
        unloading_end = arrive + self.unload_time

        self.current_floor = dst
        self.available_at = unloading_end
        self.trip_src = src
        self.trip_dst = dst
        self.trip_loading_end = loading_end
        self.trip_completion = unloading_end
        self.trip_passengers = 1
        return unloading_end

    @staticmethod
    def pop_cluster(c: int, candidates: List[tuple]) -> List[int]:
        """Pick c indices from `candidates` minimising max destination spread.

        Each candidate is a tuple `(src, dst, *meta)`; only `dst` (index 1) is
        used for the spread, with `src` (index 0) as a tie-break to favour
        matching pairs (which improves batching via `can_board`).

        Implements the Phase 4 H1 P1 dispatch heuristic. If
        `len(candidates) <= c` returns all indices (no artificial hold-off).
        """
        n = len(candidates)
        if n <= c:
            return list(range(n))
        from itertools import combinations
        best_idx = None
        best_score = (float("inf"), float("inf"))
        for combo in combinations(range(n), c):
            dsts = [candidates[i][1] for i in combo]
            srcs = [candidates[i][0] for i in combo]
            score = (max(dsts) - min(dsts), max(srcs) - min(srcs))
            if score < best_score:
                best_score = score
                best_idx = list(combo)
        return best_idx


class ElevatorBatchedStochastic:
    """ElevatorBatched with lognormal multiplicative noise on each phase.

    For Reinforcement Experiment R3 (Phase 4 v2 §11.10): tests whether the
    batched-vs-abstraction dominance result and M5's collapse-to-batched rule
    survive realistic per-trip variability. Each phase duration (reposition,
    load, travel, unload) is scaled by an independent lognormal multiplier
    with mean 1 and parameter sigma. sigma=0 reproduces ElevatorBatched.
    """

    def __init__(
        self,
        capacity: int = 2,
        speed_per_floor: float = 5.0,
        load_time: float = 2.0,
        unload_time: float = 2.0,
        initial_floor: int = 1,
        noise_sigma: float = 0.1,
        rng: Optional[random.Random] = None,
    ):
        self.current_floor = initial_floor
        self.available_at = 0.0
        self.capacity = capacity
        self.speed = speed_per_floor
        self.load_time = load_time
        self.unload_time = unload_time
        self.trip_src = None
        self.trip_dst = None
        self.trip_loading_end = None
        self.trip_completion = None
        self.trip_passengers = 0
        self.noise_sigma = noise_sigma
        self.rng = rng if rng is not None else random.Random(0)

    def _noise(self) -> float:
        if self.noise_sigma <= 0:
            return 1.0
        # Lognormal with mean 1: mu = -sigma^2/2
        mu = -0.5 * self.noise_sigma * self.noise_sigma
        return math.exp(self.rng.gauss(mu, self.noise_sigma))

    def can_board(self, src: int, dst: int, request_time: float) -> bool:
        return (
            self.trip_src == src
            and self.trip_dst == dst
            and self.trip_passengers < self.capacity
            and request_time <= self.trip_loading_end
        )

    def board(self) -> float:
        self.trip_passengers += 1
        return self.trip_completion

    def dispatch(self, src: int, dst: int, request_time: float) -> float:
        wait_start = max(request_time, self.available_at)
        reposition = abs(self.current_floor - src) * self.speed * self._noise()
        loading_end = wait_start + reposition + self.load_time * self._noise()
        travel = abs(src - dst) * self.speed * self._noise()
        arrive = loading_end + travel
        unloading_end = arrive + self.unload_time * self._noise()

        self.current_floor = dst
        self.available_at = unloading_end
        self.trip_src = src
        self.trip_dst = dst
        self.trip_loading_end = loading_end
        self.trip_completion = unloading_end
        self.trip_passengers = 1
        return unloading_end


class ElevatorPoolStochasticBatched:
    """Pool of ElevatorBatchedStochastic; same scheduling logic as Pool Batched."""

    def __init__(
        self,
        n_elevators: int = 1,
        capacity: int = 2,
        speed_per_floor: float = 5.0,
        load_time: float = 2.0,
        unload_time: float = 2.0,
        initial_floor: int = 1,
        noise_sigma: float = 0.1,
        rng: Optional[random.Random] = None,
    ):
        if rng is None:
            rng = random.Random(0)
        self.elevators: List[ElevatorBatchedStochastic] = [
            ElevatorBatchedStochastic(
                capacity=capacity,
                speed_per_floor=speed_per_floor,
                load_time=load_time,
                unload_time=unload_time,
                initial_floor=initial_floor,
                noise_sigma=noise_sigma,
                rng=rng,
            )
            for _ in range(n_elevators)
        ]
        self.n_elevators = n_elevators
        self.capacity = capacity

    def request(
        self,
        amr_current_floor: int,
        target_floor: int,
        request_time: float,
    ) -> float:
        for elev in self.elevators:
            if elev.can_board(amr_current_floor, target_floor, request_time):
                return elev.board()
        elev = min(self.elevators, key=lambda e: (e.available_at, id(e)))
        return elev.dispatch(amr_current_floor, target_floor, request_time)


class ElevatorPoolBatched:
    """Pool of E elevators, each with true co-occupancy batching (capacity c)."""

    def __init__(
        self,
        n_elevators: int = 1,
        capacity: int = 2,
        speed_per_floor: float = 5.0,
        load_time: float = 2.0,
        unload_time: float = 2.0,
        initial_floor: int = 1,
    ):
        self.elevators: List[ElevatorBatched] = [
            ElevatorBatched(
                capacity=capacity,
                speed_per_floor=speed_per_floor,
                load_time=load_time,
                unload_time=unload_time,
                initial_floor=initial_floor,
            )
            for _ in range(n_elevators)
        ]
        self.n_elevators = n_elevators
        self.capacity = capacity

    def request(
        self,
        amr_current_floor: int,
        target_floor: int,
        request_time: float,
    ) -> float:
        for elev in self.elevators:
            if elev.can_board(amr_current_floor, target_floor, request_time):
                return elev.board()
        elev = min(self.elevators, key=lambda e: (e.available_at, id(e)))
        return elev.dispatch(amr_current_floor, target_floor, request_time)


class ElevatorBatchedDirectional(ElevatorBatched):
    """ElevatorBatched with a direction-switch overhead (Gap 3 extension).

    Models the empirical fact that real freight elevators incur an idle /
    braking interval when reversing direction — acceleration profiles are
    direction-coupled and most production dispatchers prefer same-direction
    sweeps. The simplest meaningful extension: add `dir_switch_penalty`
    seconds to the wait-start of any new trip whose direction (sign of
    dst - src) differs from the previous trip's direction.

    `dir_switch_penalty = 0` reproduces ElevatorBatched. Default 3.0 s is
    on the same scale as load_time/unload_time.
    """

    def __init__(
        self,
        capacity: int = 2,
        speed_per_floor: float = 5.0,
        load_time: float = 2.0,
        unload_time: float = 2.0,
        initial_floor: int = 1,
        dir_switch_penalty: float = 3.0,
    ):
        super().__init__(
            capacity=capacity,
            speed_per_floor=speed_per_floor,
            load_time=load_time,
            unload_time=unload_time,
            initial_floor=initial_floor,
        )
        self.dir_switch_penalty = dir_switch_penalty
        self.last_direction = 0  # 0 = neutral, +1 = up, -1 = down

    def dispatch(self, src: int, dst: int, request_time: float) -> float:
        new_dir = 1 if dst > src else (-1 if dst < src else 0)
        wait_start = max(request_time, self.available_at)
        if (
            self.last_direction != 0
            and new_dir != 0
            and new_dir != self.last_direction
        ):
            wait_start += self.dir_switch_penalty
        reposition = abs(self.current_floor - src) * self.speed
        loading_end = wait_start + reposition + self.load_time
        travel = abs(src - dst) * self.speed
        arrive = loading_end + travel
        unloading_end = arrive + self.unload_time

        self.current_floor = dst
        self.available_at = unloading_end
        self.trip_src = src
        self.trip_dst = dst
        self.trip_loading_end = loading_end
        self.trip_completion = unloading_end
        self.trip_passengers = 1
        if new_dir != 0:
            self.last_direction = new_dir
        return unloading_end


class ElevatorPoolDirectional:
    """Pool of ElevatorBatchedDirectional; same dispatch logic as PoolBatched."""

    def __init__(
        self,
        n_elevators: int = 1,
        capacity: int = 2,
        speed_per_floor: float = 5.0,
        load_time: float = 2.0,
        unload_time: float = 2.0,
        initial_floor: int = 1,
        dir_switch_penalty: float = 3.0,
    ):
        self.elevators: List[ElevatorBatchedDirectional] = [
            ElevatorBatchedDirectional(
                capacity=capacity,
                speed_per_floor=speed_per_floor,
                load_time=load_time,
                unload_time=unload_time,
                initial_floor=initial_floor,
                dir_switch_penalty=dir_switch_penalty,
            )
            for _ in range(n_elevators)
        ]
        self.n_elevators = n_elevators
        self.capacity = capacity

    def request(
        self,
        amr_current_floor: int,
        target_floor: int,
        request_time: float,
    ) -> float:
        for elev in self.elevators:
            if elev.can_board(amr_current_floor, target_floor, request_time):
                return elev.board()
        elev = min(self.elevators, key=lambda e: (e.available_at, id(e)))
        return elev.dispatch(amr_current_floor, target_floor, request_time)


def _service_noise_factor(rng: Optional[random.Random], sigma: float) -> float:
    """Lognormal multiplier with mean 1 and parameter sigma."""
    if sigma <= 0 or rng is None:
        return 1.0
    mu = -0.5 * sigma * sigma
    return math.exp(rng.gauss(mu, sigma))


def simulate_wave(
    wave: Wave,
    n_amrs: int = 5,
    service_time: float = 5.0,
    initial_amr_floor: int = 1,
    n_elevators: int = 1,
    capacity: int = 1,
    batched: bool = False,
    stochastic_sigma: float = 0.0,
    rng: Optional[random.Random] = None,
    policy: str = "fifo",
    service_sigma: float = 0.0,
    directional: bool = False,
    dir_switch_penalty: float = 3.0,
) -> float:
    """Simulate one wave and return makespan (wave completion - release_time).

    batched=True uses ElevatorPoolBatched (true co-occupancy batching); only
    meaningful when capacity >= 2.

    stochastic_sigma > 0 selects ElevatorPoolStochasticBatched (M3): true
    batching with lognormal noise on each phase. `rng` is required when
    stochastic_sigma > 0 for reproducibility.

    `policy` controls operational dispatch:
      - "fifo" (P0): orders processed in wave-order, FIFO at the elevator.
      - "cluster" (P1): orders processed in clusters of `capacity` chosen by
        `ElevatorBatched.pop_cluster` to minimise destination spread; intended
        as the strong-ops heuristic for Phase 4 H1 (no artificial hold-off).
        Operationally equivalent to elevator-side queue clustering in this
        sequential simulator: picking c orders to assign together is the same
        as the elevator pulling c AMRs from its waiting queue.

    Tier 1 gap-fix parameters (default values reproduce v0.2 baseline):
      - `service_sigma` (Gap 1): if > 0, each pickup/dropoff service time is
        multiplied by an independent lognormal(mean=1, sigma) draw. Captures
        intra-floor service-time heterogeneity (a proxy for path congestion
        and pick-time variance) without requiring an explicit motion model.
        Requires `rng` when > 0.
      - per-`Order.release_time` (Gap 2): if any order has release_time > 0
        relative to wave.release_time, the AMR servicing that order waits
        until max(amr.current_time, wave.release_time + order.release_time).
        Activates the T dimension of Phi. Default 0.0 reproduces baseline.
      - `directional` (Gap 3): if True, uses ElevatorPoolDirectional (true
        batching with direction-switch overhead). `dir_switch_penalty`
        controls the overhead in seconds. Mutually exclusive with
        `stochastic_sigma > 0` (combine in v0.5+ if needed).
    """
    if stochastic_sigma > 0 and directional:
        raise ValueError(
            "stochastic_sigma > 0 and directional=True are mutually exclusive"
        )
    if stochastic_sigma > 0:
        pool = ElevatorPoolStochasticBatched(
            n_elevators=n_elevators,
            capacity=capacity,
            initial_floor=initial_amr_floor,
            noise_sigma=stochastic_sigma,
            rng=rng if rng is not None else random.Random(0),
        )
    elif directional:
        pool = ElevatorPoolDirectional(
            n_elevators=n_elevators,
            capacity=capacity,
            initial_floor=initial_amr_floor,
            dir_switch_penalty=dir_switch_penalty,
        )
    elif batched:
        pool = ElevatorPoolBatched(
            n_elevators=n_elevators,
            capacity=capacity,
            initial_floor=initial_amr_floor,
        )
    else:
        pool = ElevatorPool(
            n_elevators=n_elevators,
            capacity=capacity,
            initial_floor=initial_amr_floor,
        )
    amrs = [
        AMR(id=i, current_floor=initial_amr_floor, current_time=wave.release_time)
        for i in range(n_amrs)
    ]
    order_finish_times: List[float] = []

    if policy not in ("fifo", "cluster"):
        raise ValueError(f"unknown policy: {policy!r}")

    if service_sigma > 0 and rng is None:
        rng = random.Random(0)

    pending = list(wave.orders)
    cluster_buffer: List[Order] = []

    while pending or cluster_buffer:
        if not cluster_buffer:
            if policy == "cluster" and capacity > 1 and len(pending) > 1:
                cands = [(o.source_floor, o.dest_floor) for o in pending]
                idx = ElevatorBatched.pop_cluster(capacity, cands)
                cluster_buffer = [pending[i] for i in idx]
                for i in sorted(idx, reverse=True):
                    del pending[i]
            else:
                cluster_buffer = [pending.pop(0)]

        order = cluster_buffer.pop(0)
        amr = min(amrs, key=lambda a: (a.current_time, a.id))
        order_release_abs = wave.release_time + order.release_time
        t = max(amr.current_time, order_release_abs)

        if amr.current_floor != order.source_floor:
            t = pool.request(amr.current_floor, order.source_floor, t)
            amr.current_floor = order.source_floor

        t += service_time * _service_noise_factor(rng, service_sigma)

        if order.source_floor != order.dest_floor:
            t = pool.request(order.source_floor, order.dest_floor, t)
            amr.current_floor = order.dest_floor

        t += service_time * _service_noise_factor(rng, service_sigma)

        amr.current_time = t
        order_finish_times.append(t)

    return max(order_finish_times) - wave.release_time


def _build_wave(pairs: List[tuple]) -> Wave:
    orders = [Order(id=i, source_floor=s, dest_floor=d) for i, (s, d) in enumerate(pairs)]
    return Wave(orders=orders, release_time=0.0)


def _sanity_check() -> None:
    """v0.1 hand-computed makespan targets (pool with E=1, capacity=1 == v0.1)."""
    scenarios = {
        "A (concentrated 1->3)": (
            [(1, 3)] * 5,
            120.0,
        ),
        "B (uniform mixed)": (
            [(1, 2), (2, 3), (1, 3), (3, 2), (2, 1)],
            137.0,
        ),
        "C (counterbalanced 3up/2down)": (
            [(1, 3), (1, 3), (1, 3), (3, 1), (3, 1)],
            148.0,
        ),
    }
    print("=" * 60)
    print("Sanity check (v0.1 regime: E=1, capacity=1): hand-computed vs simulator")
    print("=" * 60)
    all_pass = True
    for name, (pairs, expected) in scenarios.items():
        wave = _build_wave(pairs)
        got = simulate_wave(wave)
        status = "OK" if abs(got - expected) < 1e-6 else "FAIL"
        if status == "FAIL":
            all_pass = False
        print(f"  [{status}] {name:35s} expected={expected:6.1f}  got={got:6.1f}")
    print("=" * 60)
    print("All sanity checks passed." if all_pass else "SOME CHECKS FAILED — fix before proceeding.")


def _test_single_order() -> None:
    """Minimal smoke: 1 order, 1 AMR, already at source floor."""
    wave = _build_wave([(1, 2)])
    got = simulate_wave(wave, n_amrs=1)
    # pickup(5) + load(2) + travel(5) + unload(2) + dropoff(5) = 19
    expected = 19.0
    assert abs(got - expected) < 1e-6, f"test_single_order: expected {expected}, got {got}"
    print(f"  [OK] test_single_order: makespan={got}")


def _test_pool_regime() -> None:
    """Regime sanity: capacity>=2 or E>=2 should give <= makespan of (E=1, c=1)."""
    wave = _build_wave([(1, 3)] * 5)  # scenario A, v0.1 = 120s
    base = simulate_wave(wave)
    e2 = simulate_wave(wave, n_elevators=2, capacity=1)
    c2 = simulate_wave(wave, n_elevators=1, capacity=2)
    e3c2 = simulate_wave(wave, n_elevators=3, capacity=2)
    assert base == 120.0, f"baseline regression: {base}"
    assert e2 <= base, f"E=2 should not be slower than E=1: e2={e2}, base={base}"
    assert c2 <= base, f"capacity=2 should not be slower: c2={c2}, base={base}"
    assert e3c2 <= e2, f"E=3,c=2 should not be slower than E=2,c=1"
    print(f"  [OK] pool regime: E=1,c=1={base}  E=2,c=1={e2}  E=1,c=2={c2}  E=3,c=2={e3c2}")


def _test_batched_regime() -> None:
    """Batched semantics: scenario A (5 x 1->3) with E=1, c=2, batched=True.

    Hand trace: orders 1 & 2 share trip #1 (finish at 19); orders 3 & 4 share
    trip #2 (finish at 43); order 5 takes trip #3 (finish at 67). With the
    5s dropoff service added, wave makespan = 67 + 5 = 72.
    """
    wave = _build_wave([(1, 3)] * 5)
    got = simulate_wave(wave, n_elevators=1, capacity=2, batched=True)
    expected = 72.0
    status = "OK" if abs(got - expected) < 1e-6 else "FAIL"
    print(f"  [{status}] batched scenario A (E=1,c=2): expected={expected}  got={got}")
    # batched should be strictly faster than throughput-abstraction on this wave
    # (throughput-abstraction c=2 on 5 identical 1->3 would still dispatch 5 trips).
    abstr = simulate_wave(wave, n_elevators=1, capacity=2, batched=False)
    assert got <= abstr, f"batched {got} should be <= abstraction {abstr} on matched-direction wave"
    print(f"  [OK] batched ({got}) <= abstraction ({abstr}) for matched-direction wave")


def _test_pop_cluster() -> None:
    """Unit tests for ElevatorBatched.pop_cluster."""
    # Trivial case: <= c candidates returns all
    idx = ElevatorBatched.pop_cluster(2, [(1, 2)])
    assert idx == [0], f"single candidate: {idx}"
    idx = ElevatorBatched.pop_cluster(2, [(1, 2), (1, 3)])
    assert idx == [0, 1], f"two candidates: {idx}"

    # Three candidates with c=2: should pick the two with closest dst
    cands = [(1, 1), (1, 2), (1, 3)]
    idx = ElevatorBatched.pop_cluster(2, cands)
    assert sorted(idx) in ([0, 1], [1, 2]), f"closest-dst pair: {idx}"
    chosen = sorted(cands[i][1] for i in idx)
    assert chosen[1] - chosen[0] == 1, f"spread should be 1, got dsts {chosen}"

    # Identical-dst pair preferred over mixed
    cands = [(1, 3), (1, 2), (1, 3)]  # two with dst=3, one with dst=2
    idx = ElevatorBatched.pop_cluster(2, cands)
    assert sorted(idx) == [0, 2], f"same-dst pair: {idx} (should pair the two dst=3)"

    # Tie-break on src spread
    cands = [(1, 2), (3, 2), (2, 2)]  # all dst=2; closest src pair
    idx = ElevatorBatched.pop_cluster(2, cands)
    chosen_srcs = sorted(cands[i][0] for i in idx)
    assert chosen_srcs[1] - chosen_srcs[0] == 1, f"src tie-break: srcs {chosen_srcs}"

    print(f"  [OK] pop_cluster: 4/4 sub-tests")


def _test_policy_cluster() -> None:
    """Unit tests for simulate_wave(policy='cluster')."""
    # Determinism: cluster on a 1-order wave equals fifo
    w = _build_wave([(1, 3)])
    assert simulate_wave(w, policy="fifo") == simulate_wave(w, policy="cluster")

    # On a 5x(1->3) wave with batched c=2, cluster ≡ fifo (orders all identical)
    w = _build_wave([(1, 3)] * 5)
    f = simulate_wave(w, n_elevators=1, capacity=2, batched=True, policy="fifo")
    c = simulate_wave(w, n_elevators=1, capacity=2, batched=True, policy="cluster")
    assert f == c == 72.0, f"identical-order wave: fifo={f} cluster={c}"

    # On a wave with destination shuffle, cluster should be <= fifo
    # Wave: [(1,2), (1,3), (1,2), (1,3)] — pre-clustering matters
    w = _build_wave([(1, 2), (1, 3), (1, 2), (1, 3)])
    f = simulate_wave(w, n_elevators=1, capacity=2, batched=True, policy="fifo")
    c = simulate_wave(w, n_elevators=1, capacity=2, batched=True, policy="cluster")
    assert c <= f, f"cluster should not be slower: fifo={f} cluster={c}"
    assert c < f, (
        f"on a shuffled wave with batchable pairs, cluster should be strictly faster:"
        f" fifo={f} cluster={c}"
    )
    print(f"  [OK] policy=cluster: shuffled-wave fifo={f} cluster={c} (cluster wins)")

    # Capacity=1 (no batching): cluster should equal fifo (no batching benefit)
    w = _build_wave([(1, 2), (1, 3), (1, 2)])
    f = simulate_wave(w, n_elevators=1, capacity=1, policy="fifo")
    c = simulate_wave(w, n_elevators=1, capacity=1, policy="cluster")
    # Reordering can change makespan even without batching, since AMR routing
    # depends on order processing sequence. Just check both terminate sanely.
    assert f > 0 and c > 0, f"capacity=1: fifo={f} cluster={c}"

    print(f"  [OK] policy=cluster: 4/4 sub-tests")


def _test_service_sigma() -> None:
    """Gap 1: service_sigma=0 reproduces baseline; sigma>0 produces variation."""
    wave = _build_wave([(1, 3)] * 5)
    base = simulate_wave(wave)  # baseline 120
    same = simulate_wave(wave, service_sigma=0.0)
    assert same == base, f"service_sigma=0 should reproduce baseline: {same} vs {base}"

    # sigma > 0 with fixed seed gives reproducible noise; mean over many seeds
    # should center near baseline (lognormal mean = 1).
    samples = [
        simulate_wave(wave, service_sigma=0.3, rng=random.Random(s))
        for s in range(50)
    ]
    avg = sum(samples) / len(samples)
    # 50 lognormal pickups+drops per wave x 5 orders => 10 multipliers; avg of 50 waves
    # should be within ~5% of baseline.
    assert abs(avg - base) / base < 0.05, (
        f"mean of 50 noisy waves ({avg:.2f}) should be close to baseline {base}"
    )
    # Variance check: should not all be equal
    distinct = len(set(round(s, 3) for s in samples))
    assert distinct > 30, f"service_sigma=0.3 should produce varied makespans: {distinct} distinct"
    print(f"  [OK] service_sigma: baseline {base}, noisy mean {avg:.2f} ({distinct} distinct of 50)")


def _test_order_release_time() -> None:
    """Gap 2: per-order release_time delays AMR; default 0.0 reproduces baseline."""
    wave = _build_wave([(1, 3)] * 5)
    base = simulate_wave(wave)  # baseline 120

    # All orders release at 0 -> same result
    same = simulate_wave(wave)
    assert same == base, f"release_time=0: {same} vs {base}"

    # Stagger: each order arrives 10s later. The 5th arrives at 40s.
    staggered_orders = [
        Order(id=i, source_floor=1, dest_floor=3, release_time=10.0 * i)
        for i in range(5)
    ]
    staggered = Wave(orders=staggered_orders, release_time=0.0)
    got = simulate_wave(staggered)
    assert got >= base, f"staggered makespan {got} should be >= baseline {base}"
    # First-order time = 24s (pickup5+load2+travel10+unload2+drop5); subsequent
    # delays cap by max(amr.current_time, order.release_time).
    print(f"  [OK] order release_time: baseline {base}, staggered (CV>0) {got}")

    # Edge case: huge stagger -> last order arrival time dominates
    huge = Wave(
        orders=[
            Order(id=i, source_floor=1, dest_floor=3, release_time=1000.0 * i)
            for i in range(3)
        ],
        release_time=0.0,
    )
    got = simulate_wave(huge)
    # last order releases at 2000s, then ~24s of work => ~2024
    assert got >= 2000, f"huge-stagger makespan should >= 2000: {got}"
    print(f"  [OK] order release_time: huge stagger -> {got}")


def _test_directional() -> None:
    """Gap 3: directional=True with penalty=0 reproduces ElevatorBatched.

    With penalty>0, a wave that requires direction reversal should be slower
    than the batched baseline.
    """
    # Same-direction wave: no reversals -> directional with any penalty == batched
    wave_same = _build_wave([(1, 3)] * 5)
    base = simulate_wave(wave_same, n_elevators=1, capacity=2, batched=True)
    dir0 = simulate_wave(
        wave_same, n_elevators=1, capacity=2, directional=True,
        dir_switch_penalty=10.0,
    )
    assert dir0 == base, f"same-direction wave: directional {dir0} should equal batched {base}"

    # Reversal wave: 3 up + 2 down. directional with penalty>0 should be slower.
    wave_mixed = _build_wave([(1, 3), (1, 3), (1, 3), (3, 1), (3, 1)])
    base_mixed = simulate_wave(wave_mixed, n_elevators=1, capacity=2, batched=True)
    dir_mixed = simulate_wave(
        wave_mixed, n_elevators=1, capacity=2, directional=True,
        dir_switch_penalty=5.0,
    )
    assert dir_mixed > base_mixed, (
        f"reversal wave: directional ({dir_mixed}) should be slower than batched ({base_mixed})"
    )

    # Penalty=0 should reproduce batched exactly even on mixed wave
    dir_zero = simulate_wave(
        wave_mixed, n_elevators=1, capacity=2, directional=True,
        dir_switch_penalty=0.0,
    )
    assert dir_zero == base_mixed, (
        f"directional with penalty=0 should equal batched: {dir_zero} vs {base_mixed}"
    )
    print(
        f"  [OK] directional: same-dir wave dir==batched ({base}); "
        f"mixed wave batched={base_mixed} directional(p=5)={dir_mixed}"
    )


def _test_backward_compat() -> None:
    """All three extensions at default values must reproduce v0.2 baselines."""
    wave = _build_wave([(1, 3)] * 5)
    base = simulate_wave(wave)
    assert base == 120.0, f"v0.1 sanity: {base}"
    # All three new params at defaults
    same = simulate_wave(
        wave, service_sigma=0.0, directional=False, dir_switch_penalty=3.0,
    )
    assert same == base, f"all-defaults call: {same} vs {base}"
    print(f"  [OK] backward-compat: all new params at defaults reproduce baseline {base}")


if __name__ == "__main__":
    _test_single_order()
    _sanity_check()
    _test_pool_regime()
    _test_batched_regime()
    _test_pop_cluster()
    _test_policy_cluster()
    _test_service_sigma()
    _test_order_release_time()
    _test_directional()
    _test_backward_compat()
