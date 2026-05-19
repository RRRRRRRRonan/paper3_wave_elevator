"""
MVS v0.5 — demand-pattern generators for the Phase 5 publication-scale grid.

The Section 5 scale-up adds a demand-pattern axis to the warehouse
configuration (pre-registration `phase5_scaleup_preregistration.md` §2.1).
Each generator returns an *order pool* — a list of `simulator.Order` — from
which the experiment harness samples waves. The three patterns differ in the
spatial law over (source, dest) floor pairs and, for `diurnal`, in the
temporal law over order release times:

  uniform   — (s, d) uniform over feasible floor pairs; all release_time = 0.
              Generalises experiments.build_order_pool to arbitrary F.
  clustered — `hot_fraction` of (s, d) pairs are "hot" and carry `hot_mass`
              of the orders; the rest spread over cold pairs. Models
              warehouses with dominant origin-destination lanes.
  diurnal   — spatial law uniform; release_time follows a peak / off-peak
              profile over [0, time_horizon], activating the T dimension of
              Phi = (C, I, T).

Degenerate parameters reduce clustered/diurnal to the uniform law — see
`_test_degenerate`.

Feasibility rule (from scope_rational.md, preserved from
experiments.build_order_pool): the trivial (1, 1) order is excluded;
same-floor orders on floors >= 2 are kept (the AMR still needs the elevator
to reach that floor).

Run the self-tests with:  python -m src.demand_patterns
"""
from __future__ import annotations

import random
from typing import Callable, Dict, List

from src.simulator import Order

# Diurnal default horizon. Kept on the scale of a few wave-makespans so the
# release-time span feeds the T feature without swamping the elevator signal.
# Tuned 120 -> 50 after the W4 smoke (diurnal +40.7 % makespan inflation at
# 120 was swamping the C/I decomposition signal); a pre-reg §7 calibration item.
DEFAULT_TIME_HORIZON = 50.0


def _feasible_pairs(F: int) -> List[tuple]:
    """All (src, dst) floor pairs over 1..F, excluding the trivial (1, 1)."""
    return [(s, d) for s in range(1, F + 1) for d in range(1, F + 1)
            if not (s == 1 and d == 1)]


def generate_uniform(F: int, pool_size: int, seed: int = 42) -> List[Order]:
    """(s, d) uniform over feasible pairs; release_time = 0 for all orders."""
    rng = random.Random(seed)
    pairs = _feasible_pairs(F)
    return [Order(id=i, source_floor=s, dest_floor=d)
            for i, (s, d) in enumerate(rng.choices(pairs, k=pool_size))]


def generate_clustered(F: int, pool_size: int, seed: int = 42,
                       hot_fraction: float = 0.2,
                       hot_mass: float = 0.8) -> List[Order]:
    """`hot_mass` of orders drawn from `hot_fraction` of the (s, d) pairs.

    `hot_fraction = 1.0` empties the cold set and reproduces `generate_uniform`'s
    law (every pair becomes hot, drawn uniformly).
    """
    rng = random.Random(seed)
    pairs = _feasible_pairs(F)
    n_hot = max(1, min(len(pairs), round(hot_fraction * len(pairs))))
    rng.shuffle(pairs)
    hot, cold = pairs[:n_hot], pairs[n_hot:]
    orders = []
    for i in range(pool_size):
        if cold and rng.random() >= hot_mass:
            s, d = rng.choice(cold)
        else:
            s, d = rng.choice(hot)
        orders.append(Order(id=i, source_floor=s, dest_floor=d))
    return orders


def generate_diurnal(F: int, pool_size: int, seed: int = 42,
                     time_horizon: float = DEFAULT_TIME_HORIZON,
                     peak_window: float = 0.3,
                     peak_share: float = 0.7) -> List[Order]:
    """Uniform spatial law; release_time concentrated in a peak window.

    `peak_share` of orders release within a window of width
    `peak_window * time_horizon`; the rest spread uniformly over [0, H].
    `peak_window = 1.0` makes the peak window the whole horizon and reproduces
    a flat (uniform-in-time) release law.
    """
    rng = random.Random(seed)
    pairs = _feasible_pairs(F)
    H = time_horizon
    win = min(peak_window, 1.0) * H
    peak_start = rng.uniform(0.0, max(0.0, H - win))
    orders = []
    for i in range(pool_size):
        s, d = rng.choice(pairs)
        if rng.random() < peak_share:
            rt = rng.uniform(peak_start, peak_start + win)
        else:
            rt = rng.uniform(0.0, H)
        orders.append(Order(id=i, source_floor=s, dest_floor=d,
                            release_time=rt))
    return orders


PATTERNS: Dict[str, Callable[..., List[Order]]] = {
    "uniform": generate_uniform,
    "clustered": generate_clustered,
    "diurnal": generate_diurnal,
}


def generate_pool(pattern: str, F: int, pool_size: int, seed: int = 42,
                  **kwargs) -> List[Order]:
    """Dispatch to a named pattern generator (harness entry point)."""
    if pattern not in PATTERNS:
        raise ValueError(f"unknown demand pattern: {pattern!r} "
                         f"(known: {sorted(PATTERNS)})")
    return PATTERNS[pattern](F, pool_size, seed=seed, **kwargs)


# --------------------------------------------------------------------------
# Self-tests (house style: _test_* functions, run from __main__).
# --------------------------------------------------------------------------

def _assert_valid_pool(orders: List[Order], F: int, pool_size: int) -> None:
    assert len(orders) == pool_size, f"pool size {len(orders)} != {pool_size}"
    for o in orders:
        assert 1 <= o.source_floor <= F, f"src {o.source_floor} out of 1..{F}"
        assert 1 <= o.dest_floor <= F, f"dst {o.dest_floor} out of 1..{F}"
        assert not (o.source_floor == 1 and o.dest_floor == 1), "trivial (1,1)"


def _test_uniform() -> None:
    for F in (3, 5, 8):
        pool = generate_uniform(F, 2000, seed=1)
        _assert_valid_pool(pool, F, 2000)
        assert all(o.release_time == 0.0 for o in pool), "uniform: rt must be 0"
    # determinism
    a = generate_uniform(5, 100, seed=7)
    b = generate_uniform(5, 100, seed=7)
    assert [(o.source_floor, o.dest_floor) for o in a] == \
           [(o.source_floor, o.dest_floor) for o in b], "seed not reproducible"
    print("  [OK] uniform: valid pools for F in {3,5,8}, rt=0, reproducible")


def _test_clustered() -> None:
    F, N = 5, 4000
    pool = generate_clustered(F, N, seed=2, hot_fraction=0.2, hot_mass=0.8)
    _assert_valid_pool(pool, F, N)
    # concentration: the top-20 % most-used pairs should carry a clear majority
    from collections import Counter
    freq = Counter((o.source_floor, o.dest_floor) for o in pool)
    n_pairs = len(_feasible_pairs(F))
    n_hot = max(1, round(0.2 * n_pairs))
    top_mass = sum(c for _, c in freq.most_common(n_hot)) / N
    assert top_mass >= 0.65, f"clustered not concentrated: top mass {top_mass:.3f}"
    print(f"  [OK] clustered: top-{n_hot} pairs carry {top_mass:.2f} of mass")


def _test_diurnal() -> None:
    F, N, H = 5, 4000, DEFAULT_TIME_HORIZON
    pool = generate_diurnal(F, N, seed=3, time_horizon=H,
                            peak_window=0.3, peak_share=0.7)
    _assert_valid_pool(pool, F, N)
    rts = sorted(o.release_time for o in pool)
    assert rts[0] >= 0.0 and rts[-1] <= H + 1e-9, "release_time out of [0,H]"
    # a window of width 0.3*H must hold a clear majority of releases
    win = 0.3 * H
    best = 0
    j = 0
    for i in range(N):
        while rts[j] - rts[i] <= win and j < N - 1:
            j += 1
        best = max(best, j - i)
    assert best / N >= 0.6, f"diurnal peak too weak: densest window {best/N:.3f}"
    print(f"  [OK] diurnal: densest 0.3*H window holds {best/N:.2f} of releases")


def _test_degenerate() -> None:
    # clustered with hot_fraction=1.0 -> every pair hot -> ~uniform spread
    F, N = 5, 6000
    pool = generate_clustered(F, N, seed=4, hot_fraction=1.0, hot_mass=0.8)
    from collections import Counter
    freq = Counter((o.source_floor, o.dest_floor) for o in pool)
    n_pairs = len(_feasible_pairs(F))
    spread = max(freq.values()) / (N / n_pairs)
    assert spread < 1.6, f"hot_fraction=1.0 should be ~uniform: spread {spread:.2f}"
    # diurnal with peak_window=1.0 -> flat release law over [0,H]
    H = DEFAULT_TIME_HORIZON
    pool = generate_diurnal(F, N, seed=5, time_horizon=H, peak_window=1.0)
    rts = sorted(o.release_time for o in pool)
    # split [0,H] into 4 quartile bins; counts should be roughly equal
    bins = [0, 0, 0, 0]
    for t in rts:
        bins[min(3, int(t / H * 4))] += 1
    assert max(bins) / min(bins) < 1.5, f"peak_window=1.0 not flat: {bins}"
    print("  [OK] degenerate: hot_fraction=1.0 ~uniform; peak_window=1.0 ~flat")


def _test_features_integration() -> None:
    """A wave drawn from each pool yields finite C, I, T; diurnal activates T."""
    from src.features import compute_all_features
    from src.simulator import Wave
    rng = random.Random(11)
    uni = generate_uniform(5, 500, seed=11)
    diu = generate_diurnal(5, 500, seed=11)
    w_uni = Wave(orders=rng.sample(uni, 8))
    w_diu = Wave(orders=rng.sample(diu, 8))
    f_uni = compute_all_features(w_uni)
    f_diu = compute_all_features(w_diu)
    assert f_uni["T"] == 0.0, f"uniform wave T should be 0, got {f_uni['T']}"
    assert f_diu["T"] > 0.0, f"diurnal wave T should be > 0, got {f_diu['T']}"
    for f in (f_uni, f_diu):
        assert f["C"] >= 0.0 and 0.0 <= f["I"] <= 1.0, f"bad features {f}"
    print(f"  [OK] features integration: uniform T={f_uni['T']:.3f}, "
          f"diurnal T={f_diu['T']:.3f}")


if __name__ == "__main__":
    _test_uniform()
    _test_clustered()
    _test_diurnal()
    _test_degenerate()
    _test_features_integration()
    print("demand_patterns.py: all self-tests passed.")
