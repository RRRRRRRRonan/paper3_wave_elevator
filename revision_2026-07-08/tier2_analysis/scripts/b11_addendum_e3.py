"""
Amendment B-11 ADDENDUM (2026-07-08): reproducible E = 3 corroboration slice
for the Lemma 6 all-E theorem. Protocol locked in the addendum section of
AMEND-2026-07-08-B11_conjecture1_search.md BEFORE execution.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "prototype"))

from b11_conj1_search import PAIRS, TOL, run_instance, run_mirror  # noqa: E402
from src import simulator as sim                                   # noqa: E402
from src.simulator import Order, Wave, simulate_wave               # noqa: E402

# Dated amendment note (2026-07-08): reference implementation redefined as
# production with the documented index-stable tie-break (see
# BUGREPORT-2026-07-08_tiebreak_nondeterminism.md). Harness-side monkeypatch
# only; production files untouched.


def _stable_pool_request(self, amr_current_floor, target_floor, request_time):
    slot = min(enumerate(self.slots),
               key=lambda t: (t[1].available_at, t[0]))[1]
    return slot.request(amr_current_floor, target_floor, request_time)


def _stable_batched_request(self, amr_current_floor, target_floor,
                            request_time):
    for elev in self.elevators:
        if elev.can_board(amr_current_floor, target_floor, request_time):
            return elev.board()
    elev = min(enumerate(self.elevators),
               key=lambda t: (t[1].available_at, t[0]))[1]
    return elev.dispatch(amr_current_floor, target_floor, request_time)


sim.ElevatorPool.request = _stable_pool_request
sim.ElevatorPoolBatched.request = _stable_batched_request

OUT = Path(__file__).resolve().parents[1] / "outputs"
SEED = 20260709
E, N = 3, 200_000
RELS = [0, 1, 2, 3, 5, 7, 10]


def main() -> None:
    t0 = time.time()
    rng = np.random.default_rng(SEED)

    # fidelity gate at E = 3
    print("fidelity gate: 1000 free E=3 instances vs simulate_wave ...")
    for trial in range(1000):
        n = int(rng.integers(2, 5))
        orders = []
        for k in range(n):
            s, d = PAIRS[int(rng.integers(0, len(PAIRS)))]
            rel = 0.0 if k == 0 else float(RELS[int(rng.integers(0, len(RELS)))])
            orders.append((s, d, rel))
        n_amrs = int(rng.choice([1, 2, 3, 4]))
        wave = Wave(orders=[Order(id=i, source_floor=s, dest_floor=d,
                                  release_time=r)
                            for i, (s, d, r) in enumerate(orders)],
                    release_time=0.0)
        for model, batched in (("M1", False), ("M2", True)):
            ref = simulate_wave(wave, n_amrs=n_amrs, n_elevators=E,
                                capacity=2, batched=batched)
            got, _, _ = run_mirror(orders, n_amrs, E, model, None)
            if abs(got - ref) > TOL:
                raise SystemExit(f"FIDELITY GATE FAILED trial {trial} "
                                 f"{model}: {got} vs {ref}. SLICE HALTED.")
    print("fidelity gate PASSED (2000/2000 comparisons within 1e-9)")

    n_support = n_support_viol = n_gap = n_viol_total = n_boarding = 0
    for _ in range(N):
        n = int(rng.integers(2, 5))
        orders = []
        for k in range(n):
            s, d = PAIRS[int(rng.integers(0, len(PAIRS)))]
            rel = 0.0 if k == 0 else float(RELS[int(rng.integers(0, len(RELS)))])
            orders.append((s, d, rel))
        n_amrs = int(rng.choice([1, 2, 3, 4]))
        mk1, mk2, c_ok, cstar_ok, d_ok, viol, boarding = run_instance(
            tuple(orders), n_amrs, E)
        n_viol_total += viol
        n_boarding += boarding
        if c_ok and d_ok:
            n_support += 1
            n_support_viol += viol
        if boarding and c_ok and not cstar_ok:
            n_gap += 1

    out = {
        "amendment": "B-11 addendum (E=3 slice)", "date_executed": "2026-07-08",
        "seed": SEED, "E": E, "n_instances": N,
        "fidelity_gate": "PASSED 2000/2000",
        "support_set_c_and_d": n_support,
        "violations_in_support_set": n_support_viol,
        "coverage_gap_c_holds_cstar_fails": n_gap,
        "total_violations": n_viol_total,
        "instances_with_boarding": n_boarding,
        "runtime_seconds": round(time.time() - t0, 1),
    }
    path = OUT / "b11_addendum_e3.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    print(f"\nE=3 slice: {N:,} instances ({n_boarding:,} with boarding)")
    print(f"  support set (c)+(d): {n_support:,}; violations inside: "
          f"{n_support_viol}  (locked expectation: 0)")
    print(f"  coverage gap (boarding, c holds, c* fails): {n_gap:,}")
    print(f"  total violations (conditions failing): {n_viol_total:,}")
    print(f"Saved {path}  ({out['runtime_seconds']}s)")


if __name__ == "__main__":
    main()
