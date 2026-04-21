"""
MVS v0.1 simulator.

Implements the deterministic elevator semantics defined in
F:/paper3_wave_elevator/prototype/simulator.md — one single-capacity elevator,
FCFS, 5-phase per-request timing: wait -> reposition -> load(2s) -> travel -> unload(2s).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List


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


class ElevatorResource:
    """Single elevator, capacity=1, FCFS."""

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


def simulate_wave(
    wave: Wave,
    n_amrs: int = 5,
    service_time: float = 5.0,
    initial_amr_floor: int = 1,
) -> float:
    """Simulate one wave and return makespan (wave completion - release_time)."""
    elevator = ElevatorResource()
    amrs = [
        AMR(id=i, current_floor=initial_amr_floor, current_time=wave.release_time)
        for i in range(n_amrs)
    ]
    order_finish_times: List[float] = []

    for order in wave.orders:
        amr = min(amrs, key=lambda a: (a.current_time, a.id))
        t = amr.current_time

        if amr.current_floor != order.source_floor:
            t = elevator.request(amr.current_floor, order.source_floor, t)
            amr.current_floor = order.source_floor

        t += service_time

        if order.source_floor != order.dest_floor:
            t = elevator.request(order.source_floor, order.dest_floor, t)
            amr.current_floor = order.dest_floor

        t += service_time

        amr.current_time = t
        order_finish_times.append(t)

    return max(order_finish_times) - wave.release_time


def _build_wave(pairs: List[tuple]) -> Wave:
    orders = [Order(id=i, source_floor=s, dest_floor=d) for i, (s, d) in enumerate(pairs)]
    return Wave(orders=orders, release_time=0.0)


def _sanity_check() -> None:
    """Hand-computed makespan targets per intuitions_before_MVS §5 + plan-review audit."""
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
    print("Sanity check: hand-computed vs simulator makespan")
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


if __name__ == "__main__":
    _test_single_order()
    _sanity_check()
