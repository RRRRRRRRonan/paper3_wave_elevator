"""
Amendment B-5 (2026-07-08): event-driven cross-validation of the closed-form
simulator. Protocol as registered in AMEND-2026-07-08-B_deferred_experiments.md.

A genuine discrete-event engine (heapq; no SimPy dependency): AMRs run
CONCURRENTLY, claim orders as they free up, and contend for elevators through
a FIFO-by-request-time queue. Same 5-phase trip constants as production.
Differences from the closed-form sequential accumulator (concurrent claiming,
time-ordered elevator FIFO) are exactly what the cross-check measures.

Self-tests (run first): (i) single order = closed-form exactly;
(ii) n_amrs = 1 waves = closed-form exactly (sequential degeneracy).
Gates (locked): Spearman rho >= 0.9 per config AND DES per-wave dominance
(M2 >= M1) >= 90%.
"""
from __future__ import annotations

import heapq
import json
import random
import sys
import time
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "prototype"))

from b11_conj1_search import run_mirror                   # noqa: E402
from src import phase5_config as cfg                      # noqa: E402
from src.demand_patterns import generate_pool             # noqa: E402
from src.experiments_phase5 import _seed                  # noqa: E402
from src.wave_policies import build_candidates, corner_positions, materialise  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "outputs"
SPEED, LOAD, UNLOAD, SERVICE = 5.0, 2.0, 2.0, 5.0
CAP = 2
TOL = 1e-9


def des_run(orders, n_amrs: int, E: int, model: str) -> float:
    """Event-driven concurrent simulation. orders: [(src, dst, rel)]."""
    n_units = E * CAP if model == "M1" else E
    units = [{"floor": 1, "free_at": 0.0, "busy": False}
             for _ in range(n_units)]
    ride_queue = []          # (request_time, seq, amr_id) FIFO by time
    trips = []               # active M2 trips for boarding
    amr = [{"floor": 1, "phase": None} for _ in range(n_amrs)]
    next_order = [0]         # claims strictly in wave-list order (sequencing
    finish = []              # policy held identical to the closed-form walk;
    ev = []                  # only execution dynamics differ)
    seq = 0

    def push(t, kind, payload):
        nonlocal seq
        heapq.heappush(ev, (t, seq, kind, payload))
        seq += 1

    def try_assign(t):
        """Idle AMRs claim orders in wave order, waiting for release."""
        while next_order[0] < len(orders):
            oi = next_order[0]
            idle = [a for a in range(n_amrs) if amr[a]["phase"] is None]
            if not idle:
                break
            a = idle[0]
            next_order[0] += 1
            amr[a]["phase"] = ("start", oi)
            push(max(t, orders[oi][2]), "amr_step", a)

    def request_ride(a, t):
        push(t, "ride_request", None)
        heapq.heappush(ride_queue, (t, seq, a))

    def serve_queue(t):
        """Free units take queued riders; M2 boarding on active windows."""
        # M2 boarding: queued riders matching an open window board
        if model == "M2":
            for trip in trips:
                if trip["pax"] >= CAP or t > trip["load_end"] + TOL:
                    continue
                i = 0
                while i < len(ride_queue) and trip["pax"] < CAP:
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
            free = [u for u in range(n_units)
                    if not units[u]["busy"] and units[u]["free_at"] <= t + TOL]
            if not free:
                nxt = min(u["free_at"] for u in units if u["busy"] is False
                          and u["free_at"] > t + TOL) if any(
                    not u["busy"] and u["free_at"] > t + TOL for u in units) \
                    else None
                if nxt is not None:
                    push(nxt, "wake", None)
                break
            # selection rule matches the model family: earliest free_at,
            # then index (the concurrency/queueing dynamics are what differ)
            u = min(free, key=lambda j: (units[j]["free_at"], j))
            rt, rs, ra = heapq.heappop(ride_queue)
            o, d = amr_dest(ra)
            start = max(t, rt)
            repos = abs(units[u]["floor"] - o) * SPEED
            load_end = start + repos + LOAD
            done = load_end + abs(o - d) * SPEED + UNLOAD
            units[u]["floor"] = d
            units[u]["free_at"] = done
            units[u]["busy"] = True
            push(done, "unit_free", u)
            push(done, "ride_done", ra)
            if model == "M2":
                trips.append({"src": o, "dst": d, "load_end": load_end,
                              "done": done, "pax": 1})

    def amr_dest(a):
        kind, oi = amr[a]["phase"]
        s, d, _ = orders[oi]
        return (amr[a]["floor"], s) if kind == "to_src" else (s, d)

    def amr_step(a, t):
        kind, oi = amr[a]["phase"]
        s, d, _ = orders[oi]
        if kind == "start":
            if amr[a]["floor"] != s:
                amr[a]["phase"] = ("to_src", oi)
                request_ride(a, t)
            else:
                amr[a]["phase"] = ("pickup", oi)
                push(t + SERVICE, "amr_step", a)
        elif kind == "to_src":
            amr[a]["floor"] = s
            amr[a]["phase"] = ("pickup", oi)
            push(t + SERVICE, "amr_step", a)
        elif kind == "pickup":
            if s != d:
                amr[a]["phase"] = ("to_dst", oi)
                request_ride(a, t)
            else:
                amr[a]["phase"] = ("drop", oi)
                push(t + SERVICE, "amr_step", a)
        elif kind == "to_dst":
            amr[a]["floor"] = d
            amr[a]["phase"] = ("drop", oi)
            push(t + SERVICE, "amr_step", a)
        elif kind == "drop":
            finish.append(t)
            amr[a]["phase"] = None
            try_assign(t)

    try_assign(0.0)
    guard = 0
    while ev:
        guard += 1
        if guard > 200_000:
            raise RuntimeError("DES event guard tripped")
        t, _, kind, payload = heapq.heappop(ev)
        if kind == "amr_step":
            amr_step(payload, t)
        elif kind == "ride_done":
            a = payload
            amr_step(a, t)
        elif kind == "unit_free":
            units[payload]["busy"] = False
            serve_queue(t)
        elif kind in ("ride_request", "wake"):
            serve_queue(t)
            try_assign(t)
    if len(finish) != len(orders):
        raise RuntimeError("DES did not finish all orders")
    return max(finish)


def wave_tuples(wave):
    return [(o.source_floor, o.dest_floor, o.release_time)
            for o in wave.orders]


def self_tests():
    rng = np.random.default_rng(20260708)
    pairs = [(s, d) for s in range(1, 7) for d in range(1, 7) if s != d]
    # (i) single order; (ii) single AMR sequential degeneracy
    for trial in range(400):
        n = 1 if trial < 200 else int(rng.integers(2, 5))
        n_amrs = 1
        E = int(rng.choice([1, 2]))
        orders = []
        for k in range(n):
            s, d = pairs[int(rng.integers(0, len(pairs)))]
            rel = 0.0 if k == 0 else float(rng.choice([0, 2, 5]))
            orders.append((s, d, rel))
        for model in ("M1", "M2"):
            ref, _, _ = run_mirror(orders, n_amrs, E, model, None)
            got = des_run(orders, n_amrs, E, model)
            if abs(got - ref) > TOL:
                raise SystemExit(f"DES SELF-TEST FAILED ({model}, {orders}, "
                                 f"E={E}): DES {got} vs closed-form {ref}")
    print("DES self-tests PASSED (800/800: single-order + single-AMR "
          "sequential degeneracy match closed-form exactly)")


def main() -> None:
    t0 = time.time()
    self_tests()

    configs = {c["config_id"]: c for c in cfg.make_config_array()}
    per_config = {}
    all_dom = []
    corners7 = {}
    for cid in (1, 7, 11):
        config = configs[cid]
        pool = generate_pool(config["demand"], config["F"],
                             cfg.ORDER_POOL_SIZE, seed=cfg.SEED_BASE + cid,
                             **cfg.DEMAND_PARAMS[config["demand"]])
        seed = _seed(cid, 99, 16)
        cand = build_candidates(pool, 16, cfg.CANDIDATE_POOL,
                                random.Random(seed))
        arms = (["random"] if cid != 7
                else ["random", "HC_HI", "HC_LI", "LC_HI", "LC_LI"])
        rows = {"cf_M1": [], "cf_M2": [], "des_M1": [], "des_M2": []}
        arm_store = {}
        for ai, arm in enumerate(["random", "HC_HI", "HC_LI", "LC_HI",
                                  "LC_LI"]):
            if arm not in arms:
                continue
            pos = corner_positions(cand, arm)
            arm_rng = random.Random(seed + 13 * (ai + 1))
            a_des2 = []
            for wid in range(cfg.N_PER_ARM):
                w = wave_tuples(materialise(
                    cand.iloc[int(arm_rng.choice(pos))], pool))
                cf1, _, _ = run_mirror(w, config["n_amrs"],
                                       config["n_elevators"], "M1", None)
                cf2, _, _ = run_mirror(w, config["n_amrs"],
                                       config["n_elevators"], "M2", None)
                d1 = des_run(w, config["n_amrs"], config["n_elevators"], "M1")
                d2 = des_run(w, config["n_amrs"], config["n_elevators"], "M2")
                if arm == "random":
                    rows["cf_M1"].append(cf1)
                    rows["cf_M2"].append(cf2)
                    rows["des_M1"].append(d1)
                    rows["des_M2"].append(d2)
                    all_dom.append(d2 >= d1 - TOL)
                a_des2.append((d1, d2))
            arm_store[arm] = a_des2
        rho1 = float(spearmanr(rows["cf_M1"], rows["des_M1"]).statistic)
        rho2 = float(spearmanr(rows["cf_M2"], rows["des_M2"]).statistic)
        dom = float(np.mean([d2 >= d1 - TOL
                             for d1, d2 in zip(rows["des_M1"],
                                               rows["des_M2"])]))
        per_config[cid] = {"rho_M1": rho1, "rho_M2": rho2,
                           "des_dominance": dom,
                           "cf_mean_M2": float(np.mean(rows["cf_M2"])),
                           "des_mean_M2": float(np.mean(rows["des_M2"]))}
        if cid == 7:
            m0 = float(np.median([d2 for _, d2 in arm_store["random"]]))
            m_q = {a: float(np.median([d2 for _, d2 in arm_store[a]]))
                   for a in ("HC_HI", "HC_LI", "LC_HI", "LC_LI")}
            qmax = max(m_q, key=m_q.get)
            qmin = min(m_q, key=m_q.get)
            corners7 = {"des_H_up": (m_q[qmax] - m0) / m0,
                        "des_S_or": (m0 - m_q[qmin]) / m0,
                        "des_m0": m0, "des_corner_medians": m_q,
                        "closed_form_H_up_stored": 0.157,
                        "note": "stored H_up 0.157 is config 7 batched size 8 "
                                "sub-cell; DES here is size 16 random+corner "
                                "arms, sign comparison only"}

    rho_min = min(min(v["rho_M1"], v["rho_M2"]) for v in per_config.values())
    dom_all = float(np.mean(all_dom))
    gate_rho = rho_min >= 0.9
    gate_dom = dom_all >= 0.90
    out = {
        "amendment": "B-5", "date_executed": "2026-07-08",
        "self_tests": "PASSED 800/800",
        "per_config": per_config,
        "config7_des_decomposition": corners7,
        "min_spearman_rho": rho_min,
        "des_pooled_dominance": dom_all,
        "gates": {"rho_ge_09_every_config": bool(gate_rho),
                  "des_dominance_ge_090": bool(gate_dom),
                  "faithful_ordinal_proxy": bool(gate_rho and gate_dom)},
        "runtime_seconds": round(time.time() - t0, 1),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "b5_des_crossvalidation.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)

    print("\nB-5 DES cross-validation")
    for cid, v in per_config.items():
        print(f"  cfg {cid}: rho M1 {v['rho_M1']:.3f}, M2 {v['rho_M2']:.3f}; "
              f"DES dominance {v['des_dominance']:.3f}; mean M2 closed-form "
              f"{v['cf_mean_M2']:.0f} vs DES {v['des_mean_M2']:.0f}")
    if corners7:
        print(f"  cfg 7 DES decomposition: H_up {corners7['des_H_up']:.3f}, "
              f"S_or {corners7['des_S_or']:.3f} (both positive = sign "
              "agreement with closed-form)")
    print(f"  gates: rho>=0.9 every config: {gate_rho}; DES dominance "
          f">= 0.90: {gate_dom} -> faithful ordinal proxy: "
          f"{gate_rho and gate_dom}")
    print(f"\nSaved {path}  ({out['runtime_seconds']}s)")


if __name__ == "__main__":
    main()
