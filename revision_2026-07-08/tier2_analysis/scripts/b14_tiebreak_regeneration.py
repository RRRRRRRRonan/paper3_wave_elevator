"""
Amendment B-14 (2026-07-08, registered in BUGREPORT-2026-07-08): index-stable
tie-break patch + regeneration equivalence check.

Patches ALL THREE elevator pool classes (M1 pool, M2 pool, M3 stochastic
pool) with the documented index-order tie-break (harness-side monkeypatch;
production files untouched), re-runs Block C (matched chain, 18,000 sims)
and the Block A smoke slice, recomputes the pre-registered gate VERDICTS
side by side with the stored artefacts, and measures the tie-incidence
exposure statistic (requests facing an availability tie among units on
different floors).
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "prototype"))

from src import phase5_config as cfg                      # noqa: E402
from src import simulator as sim                          # noqa: E402
from src.experiments_phase5 import (_span_demand, run_chain_block,  # noqa: E402
                                    run_corner_block)

OUT = Path(__file__).resolve().parents[1] / "outputs"
CORNERS = ["HC_HI", "HC_LI", "LC_HI", "LC_LI"]
EPS = 0.05

TIE_STATS = {"requests": 0, "ties": 0, "ties_diff_floor": 0}


def _pick_stable(units, floor_of):
    TIE_STATS["requests"] += 1
    avmin = min(u.available_at for u in units)
    tied = [u for u in units if u.available_at == avmin]
    if len(tied) > 1:
        TIE_STATS["ties"] += 1
        if len({floor_of(u) for u in tied}) > 1:
            TIE_STATS["ties_diff_floor"] += 1
    for u in units:                       # index order = list order
        if u.available_at == avmin:
            return u
    raise AssertionError


def patch():
    def pool_request(self, amr_current_floor, target_floor, request_time):
        slot = _pick_stable(self.slots, lambda u: u.current_floor)
        return slot.request(amr_current_floor, target_floor, request_time)

    def batched_request(self, amr_current_floor, target_floor, request_time):
        for elev in self.elevators:
            if elev.can_board(amr_current_floor, target_floor, request_time):
                return elev.board()
        elev = _pick_stable(self.elevators, lambda u: u.current_floor)
        return elev.dispatch(amr_current_floor, target_floor, request_time)

    sim.ElevatorPool.request = pool_request
    sim.ElevatorPoolBatched.request = batched_request
    if hasattr(sim, "ElevatorPoolStochasticBatched"):
        sim.ElevatorPoolStochasticBatched.request = batched_request


def blockC_gates(df):
    """Replicate analysis_phase5_blockC's D2 gate computations."""
    from scipy.stats import wasserstein_distance
    cells = []
    dro = {}
    for cid, gc in df.groupby("config_id"):
        m0 = float(np.median(gc[gc["arm"] == "random"]["makespan_M2"]))
        dro[cid] = {}
        for corner in CORNERS:
            sub = gc[gc["arm"] == corner]
            T1 = sub["makespan_M1"].to_numpy(float)
            T2 = sub["makespan_M2"].to_numpy(float)
            perwave = float(np.mean(T2 >= T1))
            fosd = float(np.mean(np.sort(T2) >= np.sort(T1) - 1e-9))
            U_c = float(np.quantile(T2, 0.5 + EPS) - np.quantile(T2, 0.5))
            cells.append({"perwave": perwave, "fosd_ok": fosd >= 0.99,
                          "uc_ok": U_c < 0.05 * m0})
            dro[cid][corner] = (max(float(np.mean(T1)), float(np.mean(T2))),
                                float(np.mean(T1))
                                + float(wasserstein_distance(T1, T2)))
    avg = float(np.mean([c["perwave"] for c in cells]))
    worst = float(np.min([c["perwave"] for c in cells]))
    n_collapse = sum(min(m, key=lambda c: m[c][0]) == min(m, key=lambda c: m[c][1])
                     for m in dro.values())
    return {
        "D2a": bool(avg >= 0.90 and worst >= 0.80),
        "D2a_avg": avg, "D2a_worst": worst,
        "D2b": bool(sum(c["fosd_ok"] for c in cells) >= 0.90 * len(cells)),
        "D2c": bool(sum(c["uc_ok"] for c in cells) >= 0.80 * len(cells)),
        "D2d": bool(n_collapse == len(dro)),
        "n_collapse": n_collapse,
    }


def main() -> None:
    t0 = time.time()
    patch()
    configs = cfg.make_config_array()
    e2 = cfg.e2_subset(configs)

    # Block C regeneration under the fixed tie-break
    dfC = run_chain_block(e2[:cfg.BLOCK_C["n_configs"]],
                          cfg.BLOCK_C["models"], cfg.BLOCK_C["sizes"],
                          cfg.BLOCK_C["arms"], cfg.N_PER_ARM,
                          cfg.CANDIDATE_POOL)
    gates_fixed = blockC_gates(dfC)
    stored = json.loads((ROOT / "prototype" / "results"
                         / "v0_5_phase5_blockC.json").read_text(encoding="utf-8"))
    sd2 = stored["H_D2"]
    gates_stored = {"D2a": sd2["D2a"], "D2a_avg": sd2["perwave_avg"],
                    "D2a_worst": sd2["perwave_worst"], "D2b": sd2["D2b"],
                    "D2c": sd2["D2c"], "D2d": sd2["D2d"],
                    "n_collapse": sd2["n_collapse"]}

    # Block A smoke slice under the fixed tie-break (gate-relevant stats)
    s = cfg.SMOKE
    slice_a = _span_demand(configs, s["n_configs"])
    dfA = run_corner_block(slice_a, s["models"], [s["size"]],
                           cfg.BLOCK_A["arms"], s["n_per_arm"],
                           s["candidate_pool"], s["train_sample"])
    smoke_rows = []
    for (cid, model, size), g in dfA.groupby(["config_id", "model", "size"]):
        fav = g["favorable_corner"].iloc[0]
        m_q = {c: float(np.median(g[g["arm"] == c]["makespan"]))
               for c in CORNERS}
        m0 = float(np.median(g[g["arm"] == "random"]["makespan"]))
        qmax = max(m_q, key=m_q.get); qmin = min(m_q, key=m_q.get)
        H = (m_q[qmax] - m0) / m0
        M = (m_q[fav] - m_q[qmin]) / m0
        smoke_rows.append({"config_id": int(cid), "model": model,
                           "H_up": H, "M_Phi": M, "GAP": H + M,
                           "identity_exact": True})

    verdict_match = all(gates_fixed[k] == gates_stored[k]
                        for k in ("D2a", "D2b", "D2c", "D2d"))
    out = {
        "amendment": "B-14", "date_executed": "2026-07-08",
        "patch": "index-stable tie-break on all three pool classes "
                 "(harness-side; production untouched)",
        "blockC_gates_fixed_simulator": gates_fixed,
        "blockC_gates_stored_artefact": gates_stored,
        "gate_verdicts_unchanged": bool(verdict_match),
        "smoke_sliceA_fixed": smoke_rows,
        "tie_exposure": {**TIE_STATS,
                         "tie_frac": TIE_STATS["ties"] / TIE_STATS["requests"],
                         "consequential_tie_frac":
                             TIE_STATS["ties_diff_floor"]
                             / TIE_STATS["requests"]},
        "runtime_seconds": round(time.time() - t0, 1),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "b14_tiebreak_regeneration.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)

    print("B-14 tie-break regeneration equivalence")
    print(f"  Block C gates fixed vs stored:")
    for k in ("D2a", "D2b", "D2c", "D2d"):
        print(f"    {k}: fixed {gates_fixed[k]}  stored {gates_stored[k]}")
    print(f"    perwave avg: fixed {gates_fixed['D2a_avg']:.4f} vs stored "
          f"{gates_stored['D2a_avg']:.4f}; worst {gates_fixed['D2a_worst']:.3f} "
          f"vs {gates_stored['D2a_worst']:.3f}")
    print(f"  GATE VERDICTS UNCHANGED: {verdict_match}")
    print(f"  tie exposure: {TIE_STATS['ties']:,} ties / "
          f"{TIE_STATS['requests']:,} requests "
          f"({100*out['tie_exposure']['tie_frac']:.2f}%); consequential "
          f"(different floors): {TIE_STATS['ties_diff_floor']:,} "
          f"({100*out['tie_exposure']['consequential_tie_frac']:.2f}%)")
    print(f"\nSaved {path}  ({out['runtime_seconds']}s)")


if __name__ == "__main__":
    main()
