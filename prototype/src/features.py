"""
MVS v0.1 wave-level features.

Three-dimensional vertical decomposition (C, I, T) plus baseline features.
Definitions per MVS_prototype_plan.md §5.2.
"""
from __future__ import annotations

import math
from collections import Counter

from src.simulator import Wave


def vertical_concentration(wave: Wave) -> float:
    """Shannon entropy over floor distribution (source + dest combined).

    High C => floors distributed uniformly.
    Low C  => orders concentrated on few floors.
    """
    floors = []
    for o in wave.orders:
        floors.append(o.source_floor)
        floors.append(o.dest_floor)
    if not floors:
        return 0.0
    counts = Counter(floors)
    total = sum(counts.values())
    entropy = 0.0
    for c in counts.values():
        p = c / total
        entropy -= p * math.log(p)
    return entropy


def directional_imbalance(wave: Wave) -> float:
    """|N_up - N_down| / (N_up + N_down). Same-floor orders excluded."""
    n_up = sum(1 for o in wave.orders if o.dest_floor > o.source_floor)
    n_down = sum(1 for o in wave.orders if o.dest_floor < o.source_floor)
    if n_up + n_down == 0:
        return 0.0
    return abs(n_up - n_down) / (n_up + n_down)


def temporal_clustering(wave: Wave) -> float:
    """v0.1: all orders share wave.release_time, so T is a degenerate constant.

    Returned as 0.0 to keep the feature column present; it has zero variance
    in v0.1 and therefore zero predictive power (expected).
    """
    return 0.0


def wave_size(wave: Wave) -> int:
    return len(wave.orders)


def total_cross_floor_moves(wave: Wave) -> int:
    return sum(1 for o in wave.orders if o.source_floor != o.dest_floor)


def total_floor_distance(wave: Wave) -> int:
    """Sum of |src - dst| (Manhattan distance) across all orders.

    v0.2 baseline feature replacing cross_floor. Decollinearises from `size`:
    in v0.1 cross_floor correlated 0.78 with size because any cross-floor
    order counted as 1 regardless of distance; with F=5 and distances in
    {0,1,2,3,4}, total_floor_distance is an independent magnitude signal.
    """
    return sum(abs(o.source_floor - o.dest_floor) for o in wave.orders)


def compute_all_features(wave: Wave) -> dict:
    return {
        "size": wave_size(wave),
        "cross_floor": total_cross_floor_moves(wave),
        "floor_distance": total_floor_distance(wave),
        "C": vertical_concentration(wave),
        "I": directional_imbalance(wave),
        "T": temporal_clustering(wave),
    }


def _smoke() -> None:
    from src.simulator import Order

    waves = {
        "concentrated 1<->3": Wave(
            orders=[Order(i, 1, 3) for i in range(3)] + [Order(i + 3, 3, 1) for i in range(2)]
        ),
        "uniform": Wave(
            orders=[
                Order(0, 1, 2),
                Order(1, 2, 3),
                Order(2, 1, 3),
                Order(3, 3, 2),
                Order(4, 2, 1),
            ]
        ),
        "all up (1->3)": Wave(orders=[Order(i, 1, 3) for i in range(5)]),
    }
    print(f"{'wave':25s} {'size':>5s} {'cross':>6s} {'C':>7s} {'I':>7s} {'T':>5s}")
    for name, w in waves.items():
        f = compute_all_features(w)
        print(
            f"{name:25s} {f['size']:>5d} {f['cross_floor']:>6d} "
            f"{f['C']:>7.3f} {f['I']:>7.3f} {f['T']:>5.2f}"
        )


if __name__ == "__main__":
    _smoke()
