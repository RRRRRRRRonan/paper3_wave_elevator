"""
Amendment B-11 (2026-07-08): certified instance search for Conjecture 1.

Protocol EXACTLY as registered in AMEND-2026-07-08-B11_conjecture1_search.md
(locked before execution). Mirror implementation of simulate_wave's fifo walk
with event logging; fidelity gate vs src.simulator.simulate_wave runs FIRST
and halts the census on any mismatch.
"""
from __future__ import annotations

import json
import sys
import time
from itertools import product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "prototype"))

from src.simulator import Order, Wave, simulate_wave   # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "outputs"
SEED = 20260708
SPEED, LOAD, UNLOAD, SERVICE = 5.0, 2.0, 2.0, 5.0
CAP = 2
TOL = 1e-9
FLOORS = 6
PAIRS = [(s, d) for s in range(1, FLOORS + 1)
         for d in range(1, FLOORS + 1) if s != d]


# --------------------------------------------------------------------------
# Mirror simulator with event logging (fifo walk, deterministic M1/M2)
# --------------------------------------------------------------------------

def run_mirror(orders, n_amrs: int, E: int, model: str, assignment=None):
    """orders: list of (src, dst, rel). Returns (makespan, assignment, reqlog).

    reqlog entries: dict(origin, target, D, fresh, repos, y1, car, trip).
    M1: every request fresh on the earliest slot (E*CAP slots).
    M2: board first-fit else dispatch earliest elevator (ElevatorPoolBatched).
    """
    if model == "M1":
        units = [[1, 0.0] for _ in range(E * CAP)]        # floor, avail
    else:
        # floor, avail, trip_src, trip_dst, load_end, completion, pax, trip_id
        units = [[1, 0.0, None, None, None, None, 0, -1] for _ in range(E)]

    amrs = [[1, 0.0] for _ in range(n_amrs)]              # floor, time
    used_assignment = []
    reqlog = []

    def m1_request(o, tgt, t):
        i = min(range(len(units)), key=lambda j: (units[j][1], j))
        u = units[i]
        repos = abs(u[0] - o)
        wait = max(t, u[1])
        done = wait + repos * SPEED + LOAD + abs(o - tgt) * SPEED + UNLOAD
        u[0], u[1] = tgt, done
        reqlog.append({"origin": o, "target": tgt, "D": done, "fresh": True,
                       "repos": repos, "y1": None, "car": i, "trip": None})
        return done

    def m2_request(o, tgt, t):
        y1 = min(u[1] for u in units)
        for i, u in enumerate(units):
            if (u[2] == o and u[3] == tgt and u[6] < CAP and u[4] is not None
                    and t <= u[4]):
                u[6] += 1
                reqlog.append({"origin": o, "target": tgt, "D": u[5],
                               "fresh": False, "repos": None, "y1": y1,
                               "car": i, "trip": u[7]})
                return u[5]
        i = min(range(len(units)), key=lambda j: (units[j][1], j))
        u = units[i]
        repos = abs(u[0] - o)
        wait = max(t, u[1])
        load_end = wait + repos * SPEED + LOAD
        done = load_end + abs(o - tgt) * SPEED + UNLOAD
        u[7] += 1
        u[0], u[1], u[2], u[3], u[4], u[5], u[6] = tgt, done, o, tgt, load_end, done, 1
        reqlog.append({"origin": o, "target": tgt, "D": done, "fresh": True,
                       "repos": repos, "y1": y1, "car": i, "trip": u[7]})
        return done

    req = m1_request if model == "M1" else m2_request
    finish = []
    for k, (s, d, rel) in enumerate(orders):
        if assignment is None:
            ai = min(range(n_amrs), key=lambda j: (amrs[j][1], j))
        else:
            ai = assignment[k]
        used_assignment.append(ai)
        a = amrs[ai]
        t = max(a[1], float(rel))
        if a[0] != s:
            t = req(a[0], s, t)
            a[0] = s
        t += SERVICE
        if s != d:
            t = req(s, d, t)
            a[0] = d
        t += SERVICE
        a[1] = t
        finish.append(t)
    return max(finish), used_assignment, reqlog


# --------------------------------------------------------------------------
# Classifiers (per amendment B-11)
# --------------------------------------------------------------------------

def classify(log1, log2, mk1, mk2):
    assert len(log1) == len(log2), "request-sequence mismatch (Lemma 3!)"
    for r1, r2 in zip(log1, log2):
        assert r1["origin"] == r2["origin"] and r1["target"] == r2["target"], \
            "request floor mismatch (Lemma 3!)"
    # (c): per M2 multi-member trip, T >= D_M1(member)
    groups = {}
    for idx, r2 in enumerate(log2):
        groups.setdefault((r2["car"], r2["trip"]), []).append(idx)
    c_ok, boarding = True, False
    for members in groups.values():
        if len(members) >= 2:
            boarding = True
            T = log2[members[0]]["D"]
            if any(log1[i]["D"] > T + TOL for i in members):
                c_ok = False
    # (c*): boarded requests need D_M1 <= y1
    cstar_ok = all(log1[i]["D"] <= log2[i]["y1"] + TOL
                   for i, r2 in enumerate(log2) if not r2["fresh"]) and c_ok
    # (d): fresh-in-both requests need repos_M1 <= repos_M2
    d_ok = all(log1[i]["repos"] <= r2["repos"] + TOL
               for i, r2 in enumerate(log2) if r2["fresh"])
    viol = mk1 > mk2 + TOL
    return c_ok, cstar_ok, d_ok, viol, boarding


def run_instance(orders, n_amrs, E):
    mk2, assign, log2 = run_mirror(orders, n_amrs, E, "M2", None)
    mk1, _, log1 = run_mirror(orders, n_amrs, E, "M1", assign)
    return (mk1, mk2) + classify(log1, log2, mk1, mk2)


# --------------------------------------------------------------------------
# Fidelity gate (locked: runs first, halts on mismatch)
# --------------------------------------------------------------------------

def fidelity_gate(rng) -> None:
    print("fidelity gate: 2000 free-assignment instances vs simulate_wave ...")
    for trial in range(2000):
        n = int(rng.integers(2, 5))
        orders = [(int(rng.integers(1, FLOORS + 1)),) for _ in range(n)]
        orders = []
        for k in range(n):
            s, d = PAIRS[int(rng.integers(0, len(PAIRS)))]
            rel = 0.0 if k == 0 else float(rng.choice([0, 1, 2, 3, 5, 7, 10]))
            orders.append((s, d, rel))
        n_amrs = int(rng.choice([1, 2, 3, 4]))
        E = int(rng.choice([1, 2]))
        wave = Wave(orders=[Order(id=i, source_floor=s, dest_floor=d,
                                  release_time=r)
                            for i, (s, d, r) in enumerate(orders)],
                    release_time=0.0)
        for model, batched in (("M1", False), ("M2", True)):
            ref = simulate_wave(wave, n_amrs=n_amrs, n_elevators=E,
                                capacity=CAP, batched=batched)
            got, _, _ = run_mirror(orders, n_amrs, E, model, None)
            if abs(got - ref) > TOL:
                raise SystemExit(
                    f"FIDELITY GATE FAILED trial {trial} model {model}: "
                    f"mirror {got} vs simulate_wave {ref} on {orders}, "
                    f"n_amrs={n_amrs}, E={E}. CENSUS HALTED per amendment.")
    print("fidelity gate PASSED (4000/4000 comparisons within 1e-9)")


# --------------------------------------------------------------------------
# Census
# --------------------------------------------------------------------------

def main() -> None:
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    fidelity_gate(rng)

    census = {}
    witnesses = {"E1_cd_viol": None, "E2_cd_viol": None, "E2_cstar_d_viol": None}
    n_done = 0

    def record(orders, n_amrs, E):
        nonlocal n_done
        mk1, mk2, c_ok, cstar_ok, d_ok, viol, boarding = run_instance(
            list(orders), n_amrs, E)
        key = (E, len(orders), c_ok, cstar_ok, d_ok, viol, boarding)
        census[key] = census.get(key, 0) + 1
        if viol:
            wit = {"orders": [list(o) for o in orders], "n_amrs": n_amrs,
                   "E": E, "mk_M1": mk1, "mk_M2": mk2,
                   "c": c_ok, "c_star": cstar_ok, "d": d_ok,
                   "boarding": boarding}
            if E == 1 and c_ok and d_ok:
                witnesses["E1_cd_viol"] = witnesses["E1_cd_viol"] or wit
            if E == 2 and c_ok and d_ok:
                w0 = witnesses["E2_cd_viol"]
                if w0 is None or (len(orders), mk2) < (len(w0["orders"]),
                                                       w0["mk_M2"]):
                    witnesses["E2_cd_viol"] = wit
            if E == 2 and cstar_ok and d_ok:
                witnesses["E2_cstar_d_viol"] = witnesses["E2_cstar_d_viol"] or wit
        n_done += 1
        if n_done % 250_000 == 0:
            print(f"  {n_done:,} instances, {time.time()-t0:.0f}s")

    # Class W2: exhaustive
    for (p1, p2) in product(PAIRS, PAIRS):
        for r2 in (0, 1, 2, 3, 4, 5, 7, 10):
            for n_amrs in (1, 2):
                for E in (1, 2):
                    record(((p1[0], p1[1], 0.0), (p2[0], p2[1], float(r2))),
                           n_amrs, E)
    print(f"class W2 done: {n_done:,} instances, {time.time()-t0:.0f}s")

    # Class W3: exhaustive
    for (p1, p2, p3) in product(PAIRS, PAIRS, PAIRS):
        for (r2, r3) in product((0, 2, 5), (0, 2, 5)):
            for n_amrs in (1, 3):
                for E in (1, 2):
                    record(((p1[0], p1[1], 0.0), (p2[0], p2[1], float(r2)),
                            (p3[0], p3[1], float(r3))), n_amrs, E)
    print(f"class W3 done: {n_done:,} instances, {time.time()-t0:.0f}s")

    # Class W4: seeded sample
    rels = [0, 1, 2, 3, 5, 7, 10]
    for _ in range(150_000):
        orders = []
        for k in range(4):
            s, d = PAIRS[int(rng.integers(0, len(PAIRS)))]
            rel = 0.0 if k == 0 else float(rels[int(rng.integers(0, len(rels)))])
            orders.append((s, d, rel))
        record(tuple(orders), int(rng.choice([1, 2, 4])),
               int(rng.choice([1, 2])))
    print(f"class W4 done: {n_done:,} instances, {time.time()-t0:.0f}s")

    # ---- verdicts per locked reporting rules -------------------------------
    def total(pred):
        return sum(v for k, v in census.items() if pred(k))

    e1_selftest = total(lambda k: k[0] == 1 and k[2] and k[4] and k[5])
    e2_cd = total(lambda k: k[0] == 2 and k[2] and k[4] and k[5])
    e2_cstar = total(lambda k: k[0] == 2 and k[3] and k[4] and k[5])
    any_viol = total(lambda k: k[5])
    n_boarding = total(lambda k: k[6])

    out = {
        "amendment": "B-11", "date_executed": "2026-07-08", "seed": SEED,
        "n_instances": n_done,
        "fidelity_gate": "PASSED 4000/4000",
        "census": [{"E": k[0], "wave": k[1], "c": k[2], "c_star": k[3],
                    "d": k[4], "violation": k[5], "boarding": k[6],
                    "count": v} for k, v in sorted(census.items())],
        "rule1_E1_selftest_violations": e1_selftest,
        "rule2_E2_c_d_violations": e2_cd,
        "rule3_E2_cstar_d_violations": e2_cstar,
        "total_violations": any_viol,
        "instances_with_boarding": n_boarding,
        "witnesses": witnesses,
        "runtime_seconds": round(time.time() - t0, 1),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "b11_conj1_census.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)

    print("\nB-11 census results")
    print(f"  instances: {n_done:,}  (boarding occurred in {n_boarding:,})")
    print(f"  total dominance violations: {any_viol:,}")
    print(f"  rule 1 E=1 self-test [(c)+(d) hold, violation]: {e1_selftest} "
          f"(must be 0)")
    print(f"  rule 2 E=2 [(c)+(d) hold, violation]:  {e2_cd}")
    print(f"  rule 3 E=2 [(c*)+(d) hold, violation]: {e2_cstar}")
    for name, wit in witnesses.items():
        if wit:
            print(f"  witness {name}: orders={wit['orders']} "
                  f"n_amrs={wit['n_amrs']} E={wit['E']} "
                  f"M1={wit['mk_M1']} M2={wit['mk_M2']}")
    print(f"\nSaved {path}  ({out['runtime_seconds']}s)")


if __name__ == "__main__":
    main()
