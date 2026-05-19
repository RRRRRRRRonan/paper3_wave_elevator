"""
MVS v0.2 — D3 salvage investigation.

The originally proposed D3 claim -- "H_up is monotone along the model chain
M_1 <= M_2 <= M_3" -- FAILS on the R3 matched-wave data (0/3 regimes).  The
failure is mechanistic, not a sample-size artefact: H_up = (m_qmax - m_0)/m_0
is a *ratio*, and stochastic dominance inflates the numerator and the
denominator m_0 together, so the normalised headroom is not order-preserving.

This script searches the R3 data for a chain object that IS stable, so D3 can
be reformulated around something true.  Candidate objects, per regime, under
each model M in {M_1, M_2, M_3(s10), M_3(s20)}:

  identity invariants (does the *corner* the diagnostic points at move?)
    C1  argmax-corner q_max          -- the worst corner
    C2  argmin-corner q_min          -- the oracle-best corner
    C3  full corner ranking          -- Spearman rho vs the M_1 ranking

  magnitude objects (is the *number* monotone along M_1 <= M_2?)
    C4  raw upper headroom   m_qmax - m_0          (un-normalised H_up)
    C5  raw corner spread    m_qmax - m_qmin       (un-normalised UB)
    C6  normalised spread    (m_qmax - m_qmin)/m_0 (= UB)
    C7  normalised H_up      (m_qmax - m_0)/m_0    (the known failure, for contrast)

A candidate is reported as a viable D3 object if it holds in 3/3 regimes
(identity: same corner / rho = 1 across all four models; magnitude: monotone
non-decreasing along M_1 -> M_2, the genuine dominance chain).

No simulator runs: reanalysis of mvs_v0_2_phase4_v2_m3_samples.csv.

Output:
  results/v0_2_D3_chain_invariance.json
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RAW_DIR = RESULTS_DIR / "raw"
CSV = RAW_DIR / "mvs_v0_2_phase4_v2_m3_samples.csv"

REGIMES = ["E1_c2", "E2_c2", "E3_c2"]
CORNERS = ["HC_HI", "HC_LI", "LC_HI", "LC_LI"]
MODELS = [("makespan_M1", "M1"), ("makespan_M2", "M2"),
          ("makespan_M3_s10", "M3s10"), ("makespan_M3_s20", "M3s20")]
# The genuine stochastic-dominance chain (M3 is a noisy perturbation of M2,
# so magnitude-monotonicity is only asserted along M1 -> M2).
CHAIN_MAG = ["M1", "M2"]


def cell_objects(sub: pd.DataFrame, mcol: str) -> dict:
    """Per-model decomposition objects for one (regime, model)."""
    m_q = {c: float(np.median(sub[sub["arm"] == c][mcol])) for c in CORNERS}
    m_0 = float(np.median(sub[sub["arm"] == "random"][mcol]))
    q_max = max(m_q, key=m_q.get)
    q_min = min(m_q, key=m_q.get)
    return {
        "m_q": m_q,
        "m_0": m_0,
        "q_max": q_max,
        "q_min": q_min,
        "raw_headroom": m_q[q_max] - m_0,                       # C4
        "raw_spread": m_q[q_max] - m_q[q_min],                  # C5
        "norm_spread_UB": (m_q[q_max] - m_q[q_min]) / m_0,      # C6
        "norm_H_up": (m_q[q_max] - m_0) / m_0,                  # C7
    }


def main() -> None:
    df = pd.read_csv(CSV)

    # Per (regime, model) objects.
    obj = {r: {} for r in REGIMES}
    for regime in REGIMES:
        sub = df[df["regime"] == regime]
        for mcol, mname in MODELS:
            obj[regime][mname] = cell_objects(sub, mcol)

    # ---------------------------------------------------- identity invariants
    print("=" * 100)
    print("D3 salvage -- identity invariants (does the diagnostic's corner "
          "move along the chain?)")
    print("=" * 100)
    print(f"{'regime':8s}  {'object':14s}  "
          f"{'M1':>8s} {'M2':>8s} {'M3s10':>8s} {'M3s20':>8s}  {'invariant?':>11s}")

    identity_rows = []
    for regime in REGIMES:
        for key, label in [("q_max", "C1 worst q"), ("q_min", "C2 best  q")]:
            vals = {m: obj[regime][m][key] for _, m in MODELS}
            inv = len(set(vals.values())) == 1
            print(f"{regime:8s}  {label:14s}  "
                  f"{vals['M1']:>8s} {vals['M2']:>8s} "
                  f"{vals['M3s10']:>8s} {vals['M3s20']:>8s}  "
                  f"{'YES' if inv else 'NO':>11s}")
            identity_rows.append({"regime": regime, "object": key,
                                  "values": vals, "invariant": inv})

    # Corner-ranking invariance: Spearman rho of each model's corner-median
    # vector against M1's.
    print()
    print(f"{'regime':8s}  {'corner-rank Spearman rho vs M1':32s}  "
          f"{'M2':>8s} {'M3s10':>8s} {'M3s20':>8s}  {'rho==1 all?':>12s}")
    rank_rows = []
    for regime in REGIMES:
        base = [obj[regime]["M1"]["m_q"][c] for c in CORNERS]
        rhos = {}
        for _, m in MODELS:
            if m == "M1":
                continue
            vec = [obj[regime][m]["m_q"][c] for c in CORNERS]
            rho = float(spearmanr(base, vec).statistic)
            rhos[m] = rho
        all_one = all(abs(r - 1.0) < 1e-9 for r in rhos.values())
        print(f"{regime:8s}  {'':32s}  "
              f"{rhos['M2']:>8.3f} {rhos['M3s10']:>8.3f} "
              f"{rhos['M3s20']:>8.3f}  {'YES' if all_one else 'NO':>12s}")
        rank_rows.append({"regime": regime, "spearman_vs_M1": rhos,
                          "ranking_invariant": all_one})

    # ---------------------------------------------------- magnitude monotone
    print()
    print("=" * 100)
    print("D3 salvage -- magnitude objects (monotone non-decreasing along the "
          "genuine chain M1 -> M2?)")
    print("=" * 100)
    print(f"{'regime':8s}  {'object':18s}  "
          f"{'M1':>10s} {'M2':>10s} {'M3s10':>10s} {'M3s20':>10s}  "
          f"{'M1<=M2?':>8s}")

    mag_keys = [("raw_headroom", "C4 raw headroom"),
                ("raw_spread", "C5 raw spread"),
                ("norm_spread_UB", "C6 norm spread UB"),
                ("norm_H_up", "C7 norm H_up")]
    mag_rows = []
    for regime in REGIMES:
        for key, label in mag_keys:
            vals = {m: obj[regime][m][key] for _, m in MODELS}
            mono = vals["M1"] <= vals["M2"] + 1e-9
            print(f"{regime:8s}  {label:18s}  "
                  f"{vals['M1']:>10.4f} {vals['M2']:>10.4f} "
                  f"{vals['M3s10']:>10.4f} {vals['M3s20']:>10.4f}  "
                  f"{'YES' if mono else 'NO':>8s}")
            mag_rows.append({"regime": regime, "object": key,
                             "values": vals, "monotone_M1_le_M2": mono})

    # ------------------------------------------------------------- candidate
    candidates = {
        "C1_worst_corner_identity": sum(
            1 for r in identity_rows
            if r["object"] == "q_max" and r["invariant"]),
        "C2_best_corner_identity": sum(
            1 for r in identity_rows
            if r["object"] == "q_min" and r["invariant"]),
        "C3_corner_ranking": sum(1 for r in rank_rows
                                 if r["ranking_invariant"]),
        "C4_raw_headroom_mono": sum(
            1 for r in mag_rows
            if r["object"] == "raw_headroom" and r["monotone_M1_le_M2"]),
        "C5_raw_spread_mono": sum(
            1 for r in mag_rows
            if r["object"] == "raw_spread" and r["monotone_M1_le_M2"]),
        "C6_norm_spread_UB_mono": sum(
            1 for r in mag_rows
            if r["object"] == "norm_spread_UB" and r["monotone_M1_le_M2"]),
        "C7_norm_H_up_mono": sum(
            1 for r in mag_rows
            if r["object"] == "norm_H_up" and r["monotone_M1_le_M2"]),
    }

    print()
    print("=" * 100)
    print("Candidate scoreboard (n_regimes passing / 3)")
    print("=" * 100)
    for k, v in candidates.items():
        flag = "  <-- viable D3 object" if v == 3 else ""
        print(f"  {k:30s}  {v}/3{flag}")

    viable = [k for k, v in candidates.items() if v == 3]
    print()
    if viable:
        print(f"RECOMMENDATION: reformulate D3 around {', '.join(viable)}.")
        print("These hold in 3/3 regimes -- a true coupling claim: the "
              "Bound-and-Gap corner diagnostic is invariant along the model")
        print("chain, so an operator using the simple model M_1 picks the "
              "same wave-release corner as one using M_2 or stochastic M_3.")
    else:
        print("RECOMMENDATION: no object is 3/3; D3 cannot be salvaged on R3 "
              "data -- keep methodology at D1 + D2.")

    out = {
        "generated": "2026-05-19",
        "purpose": "D3 salvage investigation: the proposed 'H_up monotone in "
                   "chain' claim fails 0/3; search for a chain object that "
                   "holds so D3 can be reformulated.",
        "source_csv": CSV.name,
        "identity_invariants": identity_rows,
        "corner_ranking": rank_rows,
        "magnitude_objects": mag_rows,
        "candidate_scoreboard": candidates,
        "viable_D3_objects": viable,
    }
    out_path = RESULTS_DIR / "v0_2_D3_chain_invariance.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved {out_path}")


if __name__ == "__main__":
    main()
