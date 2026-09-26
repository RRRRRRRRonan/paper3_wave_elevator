"""
Amendment B-1 (2026-07-08): matched-assignment verification of Proposition 2's
hypotheses on the Block C waves, with the three-channel violation classifier
and the all-wave base-rate addendum. Protocol as registered in
AMEND-2026-07-08-B_deferred_experiments.md (B-1 + both dated addenda).

Instrument: the fidelity-gated mirror walk (b11_conj1_search.run_mirror,
index-stable tie-break). Waves reconstructed from the registered seed streams
(compositions verified by C-4's M1 12,000/12,000 match).
"""
from __future__ import annotations

import json
import random
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "prototype"))

from b11_conj1_search import TOL, classify, run_mirror     # noqa: E402
from src import phase5_config as cfg                       # noqa: E402
from src.demand_patterns import generate_pool              # noqa: E402
from src.experiments_phase5 import _seed                   # noqa: E402
from src.wave_policies import build_candidates, corner_positions, materialise  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "outputs"
ARMS = ["random", "HC_HI", "HC_LI", "LC_HI", "LC_LI"]


def wave_to_tuples(wave):
    return [(o.source_floor, o.dest_floor, o.release_time)
            for o in wave.orders]


def main() -> None:
    t0 = time.time()
    configs = [c for c in cfg.make_config_array()
               if c["config_id"] in (1, 3, 5, 7, 9, 11)]

    n_waves = 0
    b_holds_free = 0
    dom_enforced = 0
    viol_rows = []
    base_rate_overtake = base_rate_repos = 0
    per_config = {}

    for config in configs:
        cid = config["config_id"]
        pool = generate_pool(config["demand"], config["F"],
                             cfg.ORDER_POOL_SIZE, seed=cfg.SEED_BASE + cid,
                             **cfg.DEMAND_PARAMS[config["demand"]])
        seed = _seed(cid, 99, 16)
        cand = build_candidates(pool, 16, cfg.CANDIDATE_POOL,
                                random.Random(seed))
        cc = {"n": 0, "b_free": 0, "dom": 0, "viol": 0}
        for ai, arm in enumerate(ARMS):
            pos = corner_positions(cand, arm)
            arm_rng = random.Random(seed + 13 * (ai + 1))
            for wid in range(cfg.N_PER_ARM):
                wave = materialise(cand.iloc[int(arm_rng.choice(pos))], pool)
                orders = wave_to_tuples(wave)
                n_amrs, E = config["n_amrs"], config["n_elevators"]

                mk1, asg1, log1 = run_mirror(orders, n_amrs, E, "M1", None)
                mk2f, asg2, _ = run_mirror(orders, n_amrs, E, "M2", None)
                if asg1 == asg2:
                    b_holds_free += 1
                    cc["b_free"] += 1
                mk2, _, log2 = run_mirror(orders, n_amrs, E, "M2", asg1)

                c_ok, cstar_ok, d_ok, viol, boarding = classify(
                    log1, log2, mk1, mk2)
                # all-wave base rates (addendum iv): overtaking event =
                # (c) violated; adverse repositioning event = (d) violated
                base_rate_overtake += (not c_ok)
                base_rate_repos += (not d_ok)
                if mk2 >= mk1 - TOL:
                    dom_enforced += 1
                    cc["dom"] += 1
                else:
                    channel = ("batch_overtaking" if not c_ok else
                               ("adverse_repositioning" if not d_ok
                                else "other"))
                    viol_rows.append({"config_id": cid, "arm": arm,
                                      "wave_id": wid, "mk_M1": mk1,
                                      "mk_M2_enforced": mk2,
                                      "channel": channel})
                    cc["viol"] += 1
                n_waves += 1
                cc["n"] += 1
        per_config[cid] = cc

    channels = {}
    for v in viol_rows:
        channels[v["channel"]] = channels.get(v["channel"], 0) + 1
    n_viol = len(viol_rows)
    pct_repos_viol = (channels.get("adverse_repositioning", 0) / n_waves
                      if n_waves else 0.0)
    gate_d_prominent = pct_repos_viol > 0.001

    out = {
        "amendment": "B-1 (+ addenda)", "date_executed": "2026-07-08",
        "instrument": "fidelity-gated mirror, index-stable tie-break",
        "n_waves": n_waves, "n_replays": n_waves * 3,
        "hyp_b_holds_free_assignment": b_holds_free,
        "hyp_b_free_frac": b_holds_free / n_waves,
        "dominance_enforced": dom_enforced,
        "dominance_enforced_frac": dom_enforced / n_waves,
        "n_violations_enforced": n_viol,
        "violation_channels": channels,
        "base_rate_all_waves": {
            "batch_overtaking_events": base_rate_overtake,
            "adverse_repositioning_events": base_rate_repos,
            "overtake_frac": base_rate_overtake / n_waves,
            "repos_frac": base_rate_repos / n_waves},
        "locked_rules": {
            "all_violations_are_overtaking_sentence": "RETIRED (per addendum)",
            "condition_d_prominent_in_section4": bool(gate_d_prominent),
        },
        "per_config": per_config,
        "violations": viol_rows[:50],
        "runtime_seconds": round(time.time() - t0, 1),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "b1_matched_assignment.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)

    print("B-1 matched-assignment verification (Block C, mirror instrument)")
    print(f"  waves: {n_waves:,} ({n_waves*3:,} mirror runs)")
    print(f"  hypothesis (b) holds under FREE assignment: "
          f"{b_holds_free:,}/{n_waves:,} = {b_holds_free/n_waves:.4f}")
    print(f"  per-wave M2 >= M1 under ENFORCED (a)+(b): "
          f"{dom_enforced:,}/{n_waves:,} = {dom_enforced/n_waves:.4f}")
    print(f"  violations: {n_viol} -> channels {channels}")
    print(f"  ALL-wave base rates: overtaking {base_rate_overtake} "
          f"({100*base_rate_overtake/n_waves:.2f}%), adverse repositioning "
          f"{base_rate_repos} ({100*base_rate_repos/n_waves:.2f}%)")
    print(f"  condition (d) prominent in section 4 (>0.1% repos violations): "
          f"{gate_d_prominent}")
    print(f"\nSaved {path}  ({out['runtime_seconds']}s)")


if __name__ == "__main__":
    main()
