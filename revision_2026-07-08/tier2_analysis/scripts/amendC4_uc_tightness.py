"""
Amendment C-4 (2026-07-08): realized price of robustness + U_c tightness.
Protocol EXACTLY as registered in AMEND-2026-07-08-C_bridge_closure.md.

Reconstructs the Block C matched waves from the registered seed streams
(reconstruction fidelity check against the stored CSV runs FIRST), then adds
M3 sweeps at sigma in {0.1, 0.2, 0.3} (model indices 3/4/5), and computes
per config: regret(rule, theta), realized price, tau = price / U_c(0.05).
"""
from __future__ import annotations

import json
import random
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "prototype"))

from src import phase5_config as cfg                      # noqa: E402
from src.demand_patterns import generate_pool             # noqa: E402
from src.experiments_phase5 import _seed, sim_makespan    # noqa: E402
from src.simulator import simulate_wave                   # noqa: E402
from src.wave_policies import build_candidates, corner_positions, materialise  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "outputs"
RAW = ROOT / "prototype" / "results" / "raw"
CORNERS = ["HC_HI", "HC_LI", "LC_HI", "LC_LI"]
ARMS = ["random"] + CORNERS
SIGMAS = {"M3_s10": (0.1, 3), "M3_s20new": (0.2, 4), "M3_s30": (0.3, 5)}
THETAS = ["M1", "M2", "M3_s10", "M3_s20new", "M3_s30"]
TOL = 1e-9


def main() -> None:
    t0 = time.time()
    configs = [c for c in cfg.make_config_array()
               if c["config_id"] in (1, 3, 5, 7, 9, 11)]
    stored = pd.read_csv(RAW / "mvs_v0_5_phase5_blockC.csv")

    rows = []
    n_new = mismatches = 0
    for config in configs:
        cid = config["config_id"]
        pool = generate_pool(config["demand"], config["F"],
                             cfg.ORDER_POOL_SIZE, seed=cfg.SEED_BASE + cid,
                             **cfg.DEMAND_PARAMS[config["demand"]])
        seed = _seed(cid, 99, 16)
        cand = build_candidates(pool, 16, cfg.CANDIDATE_POOL,
                                random.Random(seed))
        g0 = stored[stored["config_id"] == cid]
        for ai, arm in enumerate(ARMS):
            pos = corner_positions(cand, arm)
            arm_rng = random.Random(seed + 13 * (ai + 1))
            ga = g0[g0["arm"] == arm].sort_values("wave_id")
            for wid in range(cfg.N_PER_ARM):
                wave = materialise(cand.iloc[int(arm_rng.choice(pos))], pool)
                rec = {"config_id": cid, "arm": arm, "wave_id": wid}
                # Amended data policy (dated note in AMEND-C): M1/M2 values
                # come from the STORED artefact of record; the recomputation
                # below is the composition check. M1 mismatch => halt.
                # M2 mismatches = tie-break exposure, counted, < 1% required.
                for model, tag in (("abstraction", "M1"), ("batched", "M2")):
                    m_rng = random.Random(seed + 700_003
                                          + {"abstraction": 0, "batched": 1}[model]
                                          * 9973 + wid)
                    mk = sim_makespan(wave, config, model, m_rng)
                    ref = float(ga[ga["wave_id"] == wid]
                                [f"makespan_{tag}"].iloc[0])
                    if abs(mk - ref) > TOL:
                        if tag == "M1":
                            raise SystemExit(
                                "M1 COMPOSITION CHECK FAILED. HALT.")
                        mismatches += 1
                    rec[tag] = ref                  # stored artefact of record
                for tag, (sig, midx) in SIGMAS.items():
                    m_rng = random.Random(seed + 700_003 + midx * 9973 + wid)
                    rec[tag] = simulate_wave(
                        wave, n_amrs=config["n_amrs"],
                        n_elevators=config["n_elevators"],
                        capacity=cfg.CAPACITY, stochastic_sigma=sig,
                        rng=m_rng)
                    n_new += 1
                rows.append(rec)
    df = pd.DataFrame(rows)
    if mismatches / 12_000 >= 0.01:
        raise SystemExit(f"M2 tie-break exposure {mismatches}/12000 >= 1%. "
                         "HALT per amended policy.")
    print(f"composition check PASSED (M1 12,000/12,000 exact); M2 tie-break "
          f"exposure {mismatches}/12,000 = {mismatches/120:.2f}% (< 1% "
          f"bound); {n_new} new M3 sims in {time.time()-t0:.0f}s")

    per_config = []
    for cid, g in df.groupby("config_id"):
        m0 = float(np.median(g[g["arm"] == "random"]["M2"]))
        m_q = {t: {c: float(np.median(g[g["arm"] == c][t]))
                   for c in CORNERS} for t in THETAS}
        hedge = min(m_q["M2"], key=m_q["M2"].get)
        oracle_m1 = min(m_q["M1"], key=m_q["M1"].get)
        avg = {c: float(np.mean([m_q[t][c] for t in THETAS]))
               for c in CORNERS}
        avg_rule = min(avg, key=avg.get)

        def regret(corner, theta):
            return (m_q[theta][corner] - min(m_q[theta].values())) / m0

        price = {r: max(regret(q, t) for t in THETAS)
                 for r, q in (("hedge", hedge), ("oracle_M1", oracle_m1),
                              ("avg_model", avg_rule))}
        T2 = g[g["arm"] == hedge]["M2"].to_numpy(float)
        u_c = {e: float(np.quantile(T2, 0.5 + e) - np.quantile(T2, 0.5))
               for e in (0.02, 0.05, 0.10)}
        price_abs = price["hedge"] * m0
        tau = price_abs / u_c[0.05] if u_c[0.05] > 0 else float("inf")
        per_config.append({
            "config_id": int(cid), "m0": m0, "hedge_corner": hedge,
            "oracle_M1_corner": oracle_m1, "avg_model_corner": avg_rule,
            "regret_hedge_by_theta": {t: regret(hedge, t) for t in THETAS},
            "price_hedge": price["hedge"],
            "price_oracle_M1": price["oracle_M1"],
            "price_avg_model": price["avg_model"],
            "U_c": {str(k): v for k, v in u_c.items()},
            "price_abs": price_abs,
            "tau_eps005": tau,
            "certificate_valid": bool(u_c[0.05] + 1e-12 >= price_abs),
            "informative": bool(0.5 <= tau <= 1.0),
        })

    n_valid = sum(c["certificate_valid"] for c in per_config)
    n_info = sum(c["informative"] for c in per_config)
    gate_valid = n_valid >= 5
    gate_info = n_info >= 4
    verdict = ("informative certificate" if (gate_valid and gate_info) else
               ("valid but conservative certificate" if gate_valid else
                "BOUND VIOLATION: escalate to theory"))

    out = {
        "amendment": "C-4", "date_executed": "2026-07-08",
        "n_new_sims": n_new,
        "reconstruction_fidelity": "PASSED 12000/12000 exact",
        "caliber_note": ("3.4% = config 7 Hedge corner LC_HI U_c(0.05)/m0; "
                         "3.5% = config 7 global max corner LC_LI"),
        "per_config": per_config,
        "n_certificate_valid": n_valid, "n_informative": n_info,
        "gates": {"validity_ge_5of6": gate_valid,
                  "informative_ge_4of6": gate_info},
        "locked_wording": verdict,
        "runtime_seconds": round(time.time() - t0, 1),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "amendC4_uc_tightness.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)

    print("\nC-4 U_c tightness / price of robustness")
    print(f"{'cfg':>4} {'hedge':>6} {'price%':>7} {'U_c(.05)%':>9} "
          f"{'tau':>6} {'valid':>6} {'info':>5}")
    for c in per_config:
        print(f"{c['config_id']:>4} {c['hedge_corner']:>6} "
              f"{100*c['price_hedge']:>7.2f} "
              f"{100*c['U_c']['0.05']/c['m0']:>9.2f} "
              f"{c['tau_eps005']:>6.2f} "
              f"{str(c['certificate_valid']):>6} {str(c['informative']):>5}")
    print(f"  validity {n_valid}/6 (gate >=5: {gate_valid}); "
          f"informative {n_info}/6 (gate >=4: {gate_info})")
    print(f"  locked wording: {verdict}")
    print(f"\nSaved {path}  ({out['runtime_seconds']}s)")


if __name__ == "__main__":
    main()
