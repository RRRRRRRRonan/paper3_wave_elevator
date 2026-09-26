"""
Amendment F (2026-07-08): test-retest reliability + wave-budget study.
Protocol EXACTLY as registered in AMEND-2026-07-08-F_test_retest.md.

R = 8 full-pipeline replicates x 18 configs; measurands: (i) truncated-corner
Phi-rule capacity share (Block-A protocol), (ii) covering 2x2 median-split
share H_up/UB (b13-style sample). Sub-sampling N in {50,100,200}. Seeds
S_r = 20260800 + r.
"""
from __future__ import annotations

import json
import random
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "prototype"))

from src import phase5_config as cfg                      # noqa: E402
from src.demand_patterns import generate_pool             # noqa: E402
from src.experiments_phase5 import sim_makespan           # noqa: E402
from src.wave_policies import (build_candidates, corner_positions,  # noqa: E402
                               favorable_label, fit_phi_beta, materialise)

OUT = Path(__file__).resolve().parents[1] / "outputs"
CORNERS = ["HC_HI", "HC_LI", "LC_HI", "LC_LI"]
MODEL_IDX = {"abstraction": 0, "batched": 1}
R_REPS = 8
SUBN = [50, 100, 200]


def _seed(base: int, config_id: int, *parts: int) -> int:
    s = base + config_id * 100_003
    for i, p in enumerate(parts):
        s += (p + 1) * (37 ** (i + 1))
    return s % (2 ** 31)


def replicate_config(config: dict, base_seed: int):
    """One replicate of the Block-A diagnostic + covering sample for one config."""
    cid = config["config_id"]
    pool = generate_pool(config["demand"], config["F"], cfg.ORDER_POOL_SIZE,
                         seed=base_seed + cid,
                         **cfg.DEMAND_PARAMS[config["demand"]])
    shares_sub = {n: [] for n in SUBN}       # per sub-cell Phi-rule shares
    for model in ("abstraction", "batched"):
        for size in (8, 30):
            seed = _seed(base_seed, cid, MODEL_IDX[model], size)
            cand = build_candidates(pool, size, cfg.CANDIDATE_POOL,
                                    random.Random(seed))
            rng_t = random.Random(seed + 1)
            n_tr = min(cfg.TRAIN_SAMPLE, len(cand))
            sub = cand.iloc[[rng_t.randrange(len(cand))
                             for _ in range(n_tr)]].reset_index(drop=True)
            mks_t = [sim_makespan(materialise(row, pool), config, model, rng_t)
                     for _, row in sub.iterrows()]
            fav = favorable_label(fit_phi_beta(sub, mks_t))
            arm_mks = {}
            for ai, arm in enumerate(["random"] + CORNERS):
                pos = corner_positions(cand, arm)
                arm_rng = random.Random(seed + 13 * (ai + 1))
                sim_rng = random.Random(seed + 1009 + ai)
                arm_mks[arm] = [
                    sim_makespan(materialise(
                        cand.iloc[int(arm_rng.choice(pos))], pool),
                        config, model, sim_rng)
                    for _ in range(cfg.N_PER_ARM)]
            for n in SUBN:
                m_q = {c: float(np.median(arm_mks[c][:n])) for c in CORNERS}
                m0 = float(np.median(arm_mks["random"][:n]))
                qmax = max(m_q, key=m_q.get)
                qmin = min(m_q, key=m_q.get)
                H = (m_q[qmax] - m0) / m0
                M = (m_q[fav] - m_q[qmin]) / m0
                shares_sub[n].append(H / (H + M) if (H + M) > 0
                                     else float("nan"))
    phi_share = {n: float(np.nanmean(shares_sub[n])) for n in SUBN}

    # covering 2x2 median-split share (size 16, M2, 2000-wave sample)
    seed_c = _seed(base_seed, cid, 99, 16)
    cand = build_candidates(pool, 16, cfg.CANDIDATE_POOL, random.Random(seed_c))
    rng_s = np.random.default_rng(seed_c)
    idx = rng_s.choice(len(cand), size=2000, replace=False)
    C = cand["C"].to_numpy()[idx]
    I = cand["I"].to_numpy()[idx]
    mks = np.array([sim_makespan(materialise(cand.iloc[int(p)], pool), config,
                                 "batched", random.Random(seed_c + 500_000 + i))
                    for i, p in enumerate(idx)])
    lc = (C > np.median(C)).astype(int)
    li = (I > np.median(I)).astype(int)
    m0 = float(np.median(mks))
    meds = [float(np.median(mks[(lc == a) & (li == b)]))
            for a in (0, 1) for b in (0, 1) if ((lc == a) & (li == b)).any()]
    H_cov = (max(meds) - m0) / m0
    S_cov = (m0 - min(meds)) / m0
    cov_share = H_cov / (H_cov + S_cov) if (H_cov + S_cov) > 0 else float("nan")
    return phi_share, cov_share


def icc_2_1(mat: np.ndarray) -> float:
    """ICC(2,1), two-way random effects, absolute agreement. mat: n x k."""
    n, k = mat.shape
    grand = mat.mean()
    row_m = mat.mean(axis=1)
    col_m = mat.mean(axis=0)
    ms_r = k * np.sum((row_m - grand) ** 2) / (n - 1)
    ms_c = n * np.sum((col_m - grand) ** 2) / (k - 1)
    ss_e = np.sum((mat - row_m[:, None] - col_m[None, :] + grand) ** 2)
    ms_e = ss_e / ((n - 1) * (k - 1))
    return float((ms_r - ms_e) /
                 (ms_r + (k - 1) * ms_e + k * (ms_c - ms_e) / n))


def main() -> None:
    t0 = time.time()
    configs = cfg.make_config_array()
    resolved_set = [0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 13, 14, 15, 16]

    data = {}          # (config, rep) -> (phi_share_byN, cov_share)
    runtimes = []
    for r in range(1, R_REPS + 1):
        base = 20260800 + r
        tr = time.time()
        for config in configs:
            data[(config["config_id"], r)] = replicate_config(config, base)
        runtimes.append(round(time.time() - tr, 1))
        print(f"replicate {r}/8 done in {runtimes[-1]}s "
              f"(total {time.time()-t0:.0f}s)")

    cids = [c["config_id"] for c in configs]
    mat_phi = np.array([[data[(c, r)][0][200] for r in range(1, R_REPS + 1)]
                        for c in cids])
    mat_cov = np.array([[data[(c, r)][1] for r in range(1, R_REPS + 1)]
                        for c in cids])

    def stats(mat):
        icc = icc_2_1(mat)
        sd_w = float(np.mean(np.std(mat, axis=1, ddof=1)))
        sem = sd_w * np.sqrt(max(0.0, 1 - icc))
        return icc, sd_w, sem, 1.96 * np.sqrt(2) * sem

    icc_phi_all, sd_phi, sem_phi, mdd_phi = stats(mat_phi)
    icc_phi_res, _, _, _ = stats(mat_phi[[cids.index(c)
                                          for c in resolved_set]])
    icc_cov_all, sd_cov, sem_cov, mdd_cov = stats(mat_cov)

    verdicts = (mat_phi > 0.5)
    unanimous = [bool(v.all() or (~v).all()) for v in verdicts]
    n_unanimous = sum(unanimous)

    # wave budget: smallest N whose verdict matches N=200 verdict in all reps
    budget = {}
    for ci, c in enumerate(cids):
        v200 = verdicts[ci]
        n_star = None
        for n in SUBN:
            vn = np.array([data[(c, r)][0][n] > 0.5
                           for r in range(1, R_REPS + 1)])
            if (vn == v200).all():
                n_star = n
                break
        budget[c] = n_star

    gate_icc = icc_phi_res >= 0.75
    gate_unan = n_unanimous >= 15
    out = {
        "amendment": "F", "date_executed": "2026-07-08",
        "R": R_REPS, "n_configs": len(cids), "seeds": "20260801..20260808",
        "phi_share": {
            "icc_2_1_all18": icc_phi_all, "icc_2_1_resolved15": icc_phi_res,
            "within_config_sd": sd_phi, "SEM": sem_phi, "MDD95": mdd_phi,
            "per_config_mean": {c: float(mat_phi[ci].mean())
                                for ci, c in enumerate(cids)},
            "per_config_sd": {c: float(mat_phi[ci].std(ddof=1))
                              for ci, c in enumerate(cids)}},
        "covering_share": {
            "icc_2_1_all18": icc_cov_all, "within_config_sd": sd_cov,
            "SEM": sem_cov, "MDD95": mdd_cov,
            "per_config_mean": {c: float(mat_cov[ci].mean())
                                for ci, c in enumerate(cids)}},
        "verdict_unanimity": {"n_unanimous": n_unanimous,
                              "per_config": dict(zip(cids, unanimous))},
        "wave_budget_N_star": budget,
        "gates": {"icc_resolved_ge_075": bool(gate_icc),
                  "unanimity_ge_15of18": bool(gate_unan),
                  "reliable_in_resolved_regimes": bool(gate_icc and gate_unan)},
        "runtime_per_replicate_s": runtimes,
        "runtime_total_s": round(time.time() - t0, 1),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "amendF_test_retest.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)

    print("\nAmendment F results")
    print(f"  Phi-rule share ICC(2,1): all-18 {icc_phi_all:.3f}, "
          f"resolved-15 {icc_phi_res:.3f}  (gate >= 0.75: "
          f"{'PASS' if gate_icc else 'FAIL'})")
    print(f"  covering share ICC(2,1): {icc_cov_all:.3f}")
    print(f"  SEM(phi) {sem_phi:.3f}, MDD95 {mdd_phi:.3f}; "
          f"SEM(cov) {sem_cov:.3f}")
    print(f"  verdict unanimity: {n_unanimous}/18  (gate >= 15: "
          f"{'PASS' if gate_unan else 'FAIL'})")
    print(f"  gate verdict: reliable_in_resolved_regimes = "
          f"{gate_icc and gate_unan}")
    print(f"  wave budget N*: { {k: v for k, v in budget.items()} }")
    print(f"  runtime per replicate: {runtimes} s")
    print(f"\nSaved {path}  ({out['runtime_total_s']}s)")


if __name__ == "__main__":
    main()
