"""
Event-driven evaluator (DES-M1, DES-M2) for Study 2 (Phase 6 protocol §3.5).

Modularised from the Amendment B-5 engine
(revision_2026-07-08/tier2_analysis/scripts/b5_des_crossvalidation.py):
AMRs run concurrently, claim orders in wave-list order (waiting for each
order's ready time), and contend for elevator units through a queue ordered
by request time. M1 = E*c single-rider units (throughput abstraction);
M2 = E cars of capacity c with co-occupancy boarding: a request whose
(source, destination) matches an open trip boards it while the loading
window is open. Deterministic: same inputs, same makespan.

Two queue semantics (flag `b5_compat`):
  * default (False): every queued request, taken in FIFO order by
    (request time, arrival order), first tries to board an open matching
    trip, including a trip dispatched earlier in the same service pass, and
    only then takes the earliest-free unit. This is the M2 rule of Section 3
    and of the closed-form ElevatorPoolBatched ("board if possible, else
    dispatch").
  * b5_compat=True: the exact B-5 engine. Its service pass boards only onto
    trips that were open before the pass and scans the heap in array order,
    so two matching requests served in the same pass while two units are
    free ride separately. Kept to reproduce the B-5 numbers; see
    _test_semantics_difference for a hand-computed case where the two
    semantics differ (makespan 24 versus 43).

Phase constants are parameters with the production defaults (5 s per floor,
2 s load, 2 s unload, 5 s AMR service, initial floor 1).

Run the self-tests with:  python -m src.des_evaluator
"""
from __future__ import annotations

import heapq
from typing import List, Sequence, Tuple, Union

from src.simulator import Order, Wave

TOL = 1e-9
OrderTuple = Tuple[int, int, float]


def wave_to_tuples(wave: Union[Wave, Sequence]) -> List[OrderTuple]:
    """Orders as (source, destination, ready offset) relative to the wave release."""
    if isinstance(wave, Wave):
        return [(o.source_floor, o.dest_floor, float(o.release_time))
                for o in wave.orders]
    return [(int(s), int(d), float(r)) for s, d, r in wave]


def des_makespan(wave: Union[Wave, Sequence[OrderTuple]], n_amrs: int,
                 n_elevators: int, capacity: int = 2, model: str = "M2",
                 speed_per_floor: float = 5.0, load_time: float = 2.0,
                 unload_time: float = 2.0, service_time: float = 5.0,
                 initial_floor: int = 1, b5_compat: bool = False,
                 noise_sigma: float = 0.0, noise_seed: int | None = None) -> float:
    """Makespan of one wave under DES-M1 or DES-M2 (time from wave release).

    noise_sigma > 0 (execution-robustness check, protocol §7.3): every AMR
    service duration and every elevator phase (repositioning travel, load,
    loaded travel, unload) is multiplied by an independent mean-one lognormal
    factor exp(sigma*Z - sigma^2/2), drawn in event order from
    random.Random(noise_seed). noise_sigma = 0 draws nothing and reproduces
    the deterministic evaluator exactly.
    """
    if model not in ("M1", "M2"):
        raise ValueError(f"model must be 'M1' or 'M2', got {model!r}")
    orders = wave_to_tuples(wave)
    if not orders:
        return 0.0
    if noise_sigma > 0:
        import math
        import random as _random
        _nrng = _random.Random(noise_seed)

        def f() -> float:
            return math.exp(noise_sigma * _nrng.gauss(0.0, 1.0)
                            - 0.5 * noise_sigma ** 2)
    else:
        def f() -> float:
            return 1.0
    cap = int(capacity)
    n_units = n_elevators * cap if model == "M1" else n_elevators
    units = [{"floor": initial_floor, "free_at": 0.0, "busy": False}
             for _ in range(n_units)]
    ride_queue: list = []          # (request_time, seq, amr)
    trips: list = []               # M2 trips: src, dst, load_end, done, pax
    amr = [{"floor": initial_floor, "phase": None} for _ in range(n_amrs)]
    next_order = [0]
    finish: List[float] = []
    ev: list = []
    seq = 0

    def push(t, kind, payload):
        nonlocal seq
        heapq.heappush(ev, (t, seq, kind, payload))
        seq += 1

    def try_assign(t):
        while next_order[0] < len(orders):
            idle = [a for a in range(n_amrs) if amr[a]["phase"] is None]
            if not idle:
                break
            a = idle[0]
            oi = next_order[0]
            next_order[0] += 1
            amr[a]["phase"] = ("start", oi)
            push(max(t, orders[oi][2]), "amr_step", a)

    def request_ride(a, t):
        push(t, "ride_request", None)
        heapq.heappush(ride_queue, (t, seq, a))

    def amr_dest(a):
        kind, oi = amr[a]["phase"]
        s, d, _ = orders[oi]
        return (amr[a]["floor"], s) if kind == "to_src" else (s, d)

    def dispatch(u, rt, ra, t):
        o, d = amr_dest(ra)
        start = max(t, rt)
        repos = abs(units[u]["floor"] - o) * speed_per_floor * f()
        load_end = start + repos + load_time * f()
        done = (load_end + abs(o - d) * speed_per_floor * f()
                + unload_time * f())
        units[u]["floor"] = d
        units[u]["free_at"] = done
        units[u]["busy"] = True
        push(done, "unit_free", u)
        push(done, "ride_done", ra)
        if model == "M2":
            trips.append({"src": o, "dst": d, "load_end": load_end,
                          "done": done, "pax": 1})

    def free_units(t):
        return [u for u in range(n_units)
                if not units[u]["busy"] and units[u]["free_at"] <= t + TOL]

    def serve_queue(t):
        if b5_compat:
            serve_queue_b5(t)
            return
        pending = sorted(ride_queue)
        ride_queue.clear()
        for rt, rs, ra in pending:
            if model == "M2":
                o, d = amr_dest(ra)
                trip = next((tr for tr in trips
                             if tr["pax"] < cap and tr["src"] == o
                             and tr["dst"] == d
                             and t <= tr["load_end"] + TOL
                             and rt <= tr["load_end"] + TOL), None)
                if trip is not None:
                    trip["pax"] += 1
                    push(trip["done"], "ride_done", ra)
                    continue
            free = free_units(t)
            if free:
                u = min(free, key=lambda j: (units[j]["free_at"], j))
                dispatch(u, rt, ra, t)
            else:
                heapq.heappush(ride_queue, (rt, rs, ra))

    def serve_queue_b5(t):
        # Verbatim B-5 semantics (see module docstring).
        if model == "M2":
            for trip in trips:
                if trip["pax"] >= cap or t > trip["load_end"] + TOL:
                    continue
                i = 0
                while i < len(ride_queue) and trip["pax"] < cap:
                    rt, rs, ra = ride_queue[i]
                    o, d = amr_dest(ra)
                    if (rt <= trip["load_end"] + TOL and o == trip["src"]
                            and d == trip["dst"]):
                        ride_queue.pop(i)
                        heapq.heapify(ride_queue)
                        trip["pax"] += 1
                        push(trip["done"], "ride_done", ra)
                    else:
                        i += 1
        while ride_queue:
            free = free_units(t)
            if not free:
                later = [u["free_at"] for u in units
                         if not u["busy"] and u["free_at"] > t + TOL]
                if later:
                    push(min(later), "wake", None)
                break
            u = min(free, key=lambda j: (units[j]["free_at"], j))
            rt, rs, ra = heapq.heappop(ride_queue)
            dispatch(u, rt, ra, t)

    def amr_step(a, t):
        kind, oi = amr[a]["phase"]
        s, d, _ = orders[oi]
        if kind == "start":
            if amr[a]["floor"] != s:
                amr[a]["phase"] = ("to_src", oi)
                request_ride(a, t)
            else:
                amr[a]["phase"] = ("pickup", oi)
                push(t + service_time * f(), "amr_step", a)
        elif kind == "to_src":
            amr[a]["floor"] = s
            amr[a]["phase"] = ("pickup", oi)
            push(t + service_time * f(), "amr_step", a)
        elif kind == "pickup":
            if s != d:
                amr[a]["phase"] = ("to_dst", oi)
                request_ride(a, t)
            else:
                amr[a]["phase"] = ("drop", oi)
                push(t + service_time * f(), "amr_step", a)
        elif kind == "to_dst":
            amr[a]["floor"] = d
            amr[a]["phase"] = ("drop", oi)
            push(t + service_time * f(), "amr_step", a)
        elif kind == "drop":
            finish.append(t)
            amr[a]["phase"] = None
            try_assign(t)

    try_assign(0.0)
    guard, limit = 0, max(200_000, 200 * len(orders))
    while ev:
        guard += 1
        if guard > limit:
            raise RuntimeError("DES event guard tripped")
        t, _, kind, payload = heapq.heappop(ev)
        if kind in ("amr_step", "ride_done"):
            amr_step(payload, t)
        elif kind == "unit_free":
            units[payload]["busy"] = False
            serve_queue(t)
        elif kind in ("ride_request", "wake"):
            serve_queue(t)
            try_assign(t)
    if len(finish) != len(orders):
        raise RuntimeError("DES did not finish all orders")
    return max(finish)


# --------------------------------------------------------------------------
# Self-tests (house style: _test_* functions, run from __main__).
# --------------------------------------------------------------------------

def _closed_form(orders, n_amrs, E, c, model, **timing):
    from src.simulator import simulate_wave
    wave = Wave(orders=[Order(id=i, source_floor=s, dest_floor=d,
                              release_time=r)
                        for i, (s, d, r) in enumerate(orders)])
    return simulate_wave(wave, n_amrs=n_amrs, n_elevators=E, capacity=c,
                         batched=(model == "M2"), **timing)


def _toy_orders(rng, n, F, stagger):
    out = []
    for k in range(n):
        s, d = rng.randint(1, F), rng.randint(1, F)
        r = float(rng.choice([0, 2, 5, 9.5])) if (stagger and k) else 0.0
        out.append((s, d, r))
    return out


def _test_single_order() -> None:
    import random
    rng = random.Random(424_242)
    n = 0
    for _ in range(300):
        o = _toy_orders(rng, 1, rng.choice([3, 5, 8]), False)
        o = [(o[0][0], o[0][1], float(rng.choice([0, 3, 7.5])))]
        for E in (1, 2):
            for c in (1, 2, 3):
                for model in ("M1", "M2"):
                    for compat in (False, True):
                        got = des_makespan(o, 3, E, c, model, b5_compat=compat)
                        ref = _closed_form(o, 3, E, c, model)
                        assert abs(got - ref) < 1e-9, (o, E, c, model, got, ref)
                        n += 1
    print(f"  [OK] single order = closed form exactly ({n} cases)")


def _test_single_amr() -> None:
    import random
    rng = random.Random(424_243)
    n = 0
    for _ in range(300):
        orders = _toy_orders(rng, rng.randint(2, 9), rng.choice([3, 5, 8]),
                             rng.random() < 0.5)
        for E in (1, 2):
            for c in (1, 2):
                for model in ("M1", "M2"):
                    for compat in (False, True):
                        got = des_makespan(orders, 1, E, c, model,
                                           b5_compat=compat)
                        ref = _closed_form(orders, 1, E, c, model)
                        assert abs(got - ref) < 1e-9, (orders, E, c, model,
                                                       compat, got, ref)
                        n += 1
    print(f"  [OK] single-AMR waves (with ready times) = closed form exactly "
          f"({n} cases)")


def _test_hand_computed() -> None:
    # (a) two AMRs share one M2 car: both request (1->3) at t = 5
    o = [(1, 3, 0.0), (1, 3, 0.0)]
    assert des_makespan(o, 2, 2, 2, "M2") == 24.0
    # (b) a ready time delays a claim (M1, one single-rider unit):
    #     AMR0: 5 + 2 + 5 + 2 + 5 = 19; AMR1 waits to 10, requests at 15,
    #     unit at floor 2 free at 14: 15 + 5 + 2 = 22, + 5 + 2 = 29, + 5 = 34
    o = [(1, 2, 0.0), (1, 2, 10.0)]
    assert des_makespan(o, 2, 1, 1, "M1") == 34.0
    assert _closed_form(o, 2, 1, 1, "M1") == 34.0
    # (c) M1 slots serve in parallel: E = 1, c = 2 gives two single-rider units
    o = [(1, 3, 0.0), (1, 3, 0.0)]
    assert des_makespan(o, 2, 1, 2, "M1") == 24.0
    # (d) timing parameters: speed 3, load 1, unload 1, service 4
    o = [(1, 3, 0.0)]
    assert des_makespan(o, 1, 1, 2, "M2", speed_per_floor=3.0, load_time=1.0,
                        unload_time=1.0, service_time=4.0) == 4 + 1 + 6 + 1 + 4
    # (e) same-floor order on floor 2: reposition ride 1 -> 2 (2 + 5 + 2 = 9),
    #     pickup 5, no loaded ride, drop 5: 19
    assert des_makespan([(2, 2, 0.0)], 1, 1, 2, "M2") == 19.0
    assert _closed_form([(2, 2, 0.0)], 1, 1, 2, "M2") == 19.0
    print("  [OK] hand-computed multi-AMR, ready-time, M1-slot, timing and "
          "same-floor cases")


def _test_semantics_difference() -> None:
    """3 AMRs; orders (1->3), (1->3), (1->2); E = 2, c = 2, M2.

    Board-first (default and closed form): the second (1->3) request boards
    car 0; car 1 serves (1->2): 5 + 2 + 5 + 2 + 5 = 19; the (1->3) pair ends
    at 24. B-5: the two (1->3) requests take both cars; (1->2) waits for car 0
    (free at 19 on floor 3): 19 + 10 + 2 + 5 + 2 + 5 = 43.
    """
    o = [(1, 3, 0.0), (1, 3, 0.0), (1, 2, 0.0)]
    assert des_makespan(o, 3, 2, 2, "M2") == 24.0
    assert _closed_form(o, 3, 2, 2, "M2") == 24.0
    assert des_makespan(o, 3, 2, 2, "M2", b5_compat=True) == 43.0
    print("  [OK] board-first semantics: 24 (= closed form); B-5 semantics: 43")


def _test_b5_reproduction() -> None:
    """b5_compat=True reproduces the stored B-5 engine exactly on toy waves."""
    import random
    import sys
    from pathlib import Path
    scripts = (Path(__file__).resolve().parents[2] / "revision_2026-07-08"
               / "tier2_analysis" / "scripts")
    if not (scripts / "b5_des_crossvalidation.py").exists():
        raise AssertionError("B-5 script not found: reproduction test cannot run")
    sys.path.insert(0, str(scripts))
    try:
        from b5_des_crossvalidation import des_run as b5_des_run
    except Exception as exc:                      # scipy missing, etc.
        raise AssertionError(f"B-5 import failed ({exc}): reproduction test cannot run")
    rng = random.Random(424_244)
    n = 0
    diff = {"M1": 0, "M2": 0}
    for _ in range(400):
        orders = _toy_orders(rng, rng.randint(1, 16), rng.choice([3, 5, 8]),
                             rng.random() < 0.4)
        A, E = rng.choice([1, 2, 3, 5, 8]), rng.choice([1, 2])
        for model in ("M1", "M2"):
            ref = b5_des_run(orders, A, E, model)
            got = des_makespan(orders, A, E, 2, model, b5_compat=True)
            assert abs(got - ref) < 1e-9, (orders, A, E, model, got, ref)
            diff[model] += des_makespan(orders, A, E, 2, model) != ref
            n += 1
    assert diff["M1"] == 0, "the boarding rule must not change DES-M1"
    print(f"  [OK] b5_compat reproduces B-5 exactly ({n} cases); the default "
          f"(board-first) rule changes {diff['M2']} of 400 DES-M2 cases and "
          f"0 of 400 DES-M1 cases (seed 424,244)")


def _test_noise() -> None:
    """sigma = 0 is the deterministic evaluator; sigma > 0 is reproducible
    given the seed, varies across seeds, and is centred near the
    deterministic value for small sigma."""
    import random
    import statistics
    rng = random.Random(424_246)
    for _ in range(50):
        orders = _toy_orders(rng, rng.randint(1, 16), rng.choice([3, 5, 8]),
                             rng.random() < 0.4)
        for model in ("M1", "M2"):
            base = des_makespan(orders, 4, 2, 2, model)
            assert des_makespan(orders, 4, 2, 2, model, noise_sigma=0.0,
                                noise_seed=7) == base
            a = des_makespan(orders, 4, 2, 2, model, noise_sigma=0.2, noise_seed=7)
            b = des_makespan(orders, 4, 2, 2, model, noise_sigma=0.2, noise_seed=7)
            assert a == b, "noise not reproducible"
    orders = _toy_orders(random.Random(5), 16, 5, False)
    base = des_makespan(orders, 5, 2, 2, "M2")
    vals = [des_makespan(orders, 5, 2, 2, "M2", noise_sigma=0.05, noise_seed=k)
            for k in range(200)]
    assert len(set(vals)) > 1, "noise has no effect"
    assert abs(statistics.mean(vals) - base) / base < 0.05, "noise not centred"
    print("  [OK] phase noise: sigma 0 = deterministic; reproducible by seed; "
          "centred near the deterministic value")


def _test_determinism_and_ordering() -> None:
    import random
    rng = random.Random(424_245)
    for _ in range(100):
        orders = _toy_orders(rng, rng.randint(2, 20), rng.choice([3, 5, 8]),
                             rng.random() < 0.4)
        a = des_makespan(orders, 5, 2, 2, "M2")
        assert a == des_makespan(list(orders), 5, 2, 2, "M2")
    print("  [OK] deterministic")


if __name__ == "__main__":
    _test_single_order()
    _test_single_amr()
    _test_hand_computed()
    _test_semantics_difference()
    _test_b5_reproduction()
    _test_noise()
    _test_determinism_and_ordering()
