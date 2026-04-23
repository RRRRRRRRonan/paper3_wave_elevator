"""
MVS v0.2 — Geometric mechanism experiment.

Pre-registered in intuitions_before_MVS_v0_2.md §1ter.

Tests the AMR-fleet-parallelism hypothesis: does the ratio R = N_AMRs / F
control the sign of beta(C)?

Sweep:
  N_AMRs in {3, 5, 10, 15, 20}    F in {3, 5, 7, 10}    -> 20 cells
Fixed regime: E = 2, capacity = 2 (throughput abstraction),
              wave size range 3-8, pool_size = max(20, 6*F).

Output:
  results/raw/mvs_v0_2_geometry_samples.csv  (20000 rows)
  results/v0_2_geometric_mechanism.json
"""
from __future__ import annotations

import json
import random
import time
from pathlib import Path
from typing import List, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

from src.features import compute_all_features
from src.simulator import Order, Wave, simulate_wave

N_AMRS_GRID = [3, 5, 10, 15, 20]
F_GRID = [3, 5, 7, 10]
N_SAMPLES = 1000
N_ELEVATORS = 2
CAPACITY = 2
WAVE_SIZE_MIN = 3
WAVE_SIZE_MAX = 8
RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RAW_DIR = RESULTS_DIR / "raw"
FIG_DIR = RESULTS_DIR / "figures"


def build_pool_for_F(pool_size: int, n_floors: int, seed: int) -> List[Order]:
    """Build pool excluding (1, 1) trivial orders, on F floors."""
    rng = random.Random(seed)
    orders: List[Order] = []
    i = 0
    while len(orders) < pool_size:
        src = rng.randint(1, n_floors)
        dst = rng.randint(1, n_floors)
        if not (src == 1 and dst == 1):
            orders.append(Order(id=i, source_floor=src, dest_floor=dst))
            i += 1
    return orders


def run_cell(n_amrs: int, n_floors: int, n_samples: int, seed: int) -> pd.DataFrame:
    pool_size = max(20, 6 * n_floors)
    pool = build_pool_for_F(pool_size, n_floors, seed=seed + 1)
    rng = random.Random(seed)
    rows = []
    for wave_id in range(n_samples):
        size = rng.randint(WAVE_SIZE_MIN, WAVE_SIZE_MAX)
        sampled = rng.sample(pool, size)
        wave = Wave(orders=sampled, release_time=0.0)
        makespan = simulate_wave(
            wave,
            n_amrs=n_amrs,
            n_elevators=N_ELEVATORS,
            capacity=CAPACITY,
        )
        feats = compute_all_features(wave)
        rows.append({
            "n_amrs": n_amrs, "n_floors": n_floors,
            "wave_id": wave_id, **feats, "makespan": makespan,
        })
    return pd.DataFrame(rows)


def fit_betas(df: pd.DataFrame) -> dict:
    feats = ["size", "floor_distance", "C", "I"]
    lr = LinearRegression().fit(df[feats], df["makespan"])
    r2 = lr.score(df[feats], df["makespan"])
    return {
        "betas": {f: float(c) for f, c in zip(feats, lr.coef_)},
        "r2_in_sample": float(r2),
    }


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    print("Geometric mechanism experiment")
    print(f"  N_AMRs in {N_AMRS_GRID}")
    print(f"  F in {F_GRID}")
    print(f"  Cells: {len(N_AMRS_GRID) * len(F_GRID)}, samples each: {N_SAMPLES}")
    print(f"  Fixed: E={N_ELEVATORS}, capacity={CAPACITY} (throughput, no batching)")
    print("=" * 84)
    print(f"{'cell':>10s} {'N':>4s} {'F':>4s} {'N/F':>6s} {'R2':>7s} "
          f"{'b(size)':>10s} {'b(fd)':>10s} {'b(C)':>10s} {'b(I)':>10s} {'time':>7s}")
    print("=" * 84)

    all_dfs = []
    by_cell = {}
    t0 = time.time()
    for n_amrs in N_AMRS_GRID:
        for n_floors in F_GRID:
            t_cell = time.time()
            seed = 100000 + n_amrs * 100 + n_floors
            df = run_cell(n_amrs, n_floors, N_SAMPLES, seed=seed)
            all_dfs.append(df)
            res = fit_betas(df)
            cell_key = f"N{n_amrs}_F{n_floors}"
            by_cell[cell_key] = {
                "n_amrs": n_amrs, "n_floors": n_floors,
                "n_over_f": n_amrs / n_floors,
                "betas": res["betas"], "r2_in_sample": res["r2_in_sample"],
                "makespan_mean": float(df["makespan"].mean()),
                "makespan_std": float(df["makespan"].std()),
            }
            elapsed = time.time() - t_cell
            b = res["betas"]
            print(f"{cell_key:>10s} {n_amrs:>4d} {n_floors:>4d} "
                  f"{n_amrs/n_floors:>6.2f} {res['r2_in_sample']:>7.3f} "
                  f"{b['size']:>+10.2f} {b['floor_distance']:>+10.2f} "
                  f"{b['C']:>+10.2f} {b['I']:>+10.2f} {elapsed:>6.2f}s")
    total = time.time() - t0
    print("=" * 84)
    print(f"Total runtime: {total:.1f}s")

    combined = pd.concat(all_dfs, ignore_index=True)
    out_csv = RAW_DIR / "mvs_v0_2_geometry_samples.csv"
    combined.to_csv(out_csv, index=False)
    print(f"Saved {len(combined)} rows to {out_csv}")

    # ---- Pre-registered prediction checks ----
    print()
    print("=" * 84)
    print("Pre-registered prediction checks (intuitions_before_MVS_v0_2.md §1ter)")
    print("=" * 84)

    # 1ter.1: monotone decreasing in R; positive at R<=0.5, negative at R>=2
    cells = list(by_cell.values())
    rs = np.array([c["n_over_f"] for c in cells])
    bcs = np.array([c["betas"]["C"] for c in cells])
    bis = np.array([c["betas"]["I"] for c in cells])
    pearson_C = float(np.corrcoef(rs, bcs)[0, 1])
    print(f"\n1ter.1  Pearson corr(N/F, b(C)) = {pearson_C:+.3f}")
    print(f"        b(C) at R<=0.5: " +
          ", ".join(f"{c['betas']['C']:+.1f}" for c in cells if c["n_over_f"] <= 0.5))
    print(f"        b(C) at R>=2.0: " +
          ", ".join(f"{c['betas']['C']:+.1f}" for c in cells if c["n_over_f"] >= 2.0))

    # 1ter.2: where does b(C) cross zero?
    sorted_cells = sorted(cells, key=lambda c: c["n_over_f"])
    crossing_R = None
    for i in range(len(sorted_cells) - 1):
        if sorted_cells[i]["betas"]["C"] * sorted_cells[i+1]["betas"]["C"] < 0:
            r1, r2 = sorted_cells[i]["n_over_f"], sorted_cells[i+1]["n_over_f"]
            b1, b2 = sorted_cells[i]["betas"]["C"], sorted_cells[i+1]["betas"]["C"]
            crossing_R = float(r1 - b1 * (r2 - r1) / (b2 - b1))
            print(f"\n1ter.2  b(C) zero-crossing estimated at R = {crossing_R:.2f}")
            print(f"        (between {sorted_cells[i]} and {sorted_cells[i+1]})")
            break
    if crossing_R is None:
        print(f"\n1ter.2  b(C) does not cross zero in the swept R range "
              f"(min b(C)={bcs.min():+.1f}, max b(C)={bcs.max():+.1f})")

    # Decision gate
    if abs(pearson_C) >= 0.7:
        verdict = "MECHANISM_CONFIRMED"
        verdict_text = (
            f"Pearson |corr| = {abs(pearson_C):.2f} >= 0.7 across 20 cells. "
            f"AMR-fleet-parallelism hypothesis SUPPORTED. "
            f"C3-H3 has its first quantitative mechanism."
        )
    elif abs(pearson_C) >= 0.4:
        verdict = "MECHANISM_SUGGESTIVE"
        verdict_text = (
            f"Pearson |corr| = {abs(pearson_C):.2f} in [0.4, 0.7). "
            f"Direction consistent with hypothesis but magnitude weaker than required. "
            f"Treat as suggestive; needs Phase 3 (stochastic) confirmation."
        )
    else:
        verdict = "MECHANISM_REJECTED"
        verdict_text = (
            f"Pearson |corr| = {abs(pearson_C):.2f} < 0.4. "
            f"AMR-fleet-parallelism hypothesis NOT supported. "
            f"b(C) sign-reversal in Phase 1 remains unexplained."
        )
    print(f"\nDECISION GATE: {verdict}")
    print(verdict_text)

    # ---- Heatmap of b(C) over (N, F) grid ----
    grid_C = np.zeros((len(N_AMRS_GRID), len(F_GRID)))
    grid_I = np.zeros((len(N_AMRS_GRID), len(F_GRID)))
    for i, n_amrs in enumerate(N_AMRS_GRID):
        for j, n_floors in enumerate(F_GRID):
            cell = by_cell[f"N{n_amrs}_F{n_floors}"]
            grid_C[i, j] = cell["betas"]["C"]
            grid_I[i, j] = cell["betas"]["I"]

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    for ax, grid, title, name in [
        (axes[0], grid_C, "b(C) [s/nat]", "betaC"),
        (axes[1], grid_I, "b(I) [s/unit]", "betaI"),
    ]:
        max_abs = max(abs(grid.min()), abs(grid.max()))
        im = ax.imshow(grid, cmap="RdBu_r", aspect="auto", origin="lower",
                       vmin=-max_abs, vmax=+max_abs)
        ax.set_xticks(range(len(F_GRID)))
        ax.set_xticklabels([f"F={f}" for f in F_GRID])
        ax.set_yticks(range(len(N_AMRS_GRID)))
        ax.set_yticklabels([f"N={n}" for n in N_AMRS_GRID])
        ax.set_title(title)
        for i in range(len(N_AMRS_GRID)):
            for j in range(len(F_GRID)):
                v = grid[i, j]
                ax.text(j, i, f"{v:+.1f}", ha="center", va="center",
                        color="white" if abs(v) > max_abs/2 else "black",
                        fontsize=9)
        plt.colorbar(im, ax=ax)
    plt.suptitle("Geometric experiment: b(C) and b(I) over (N_AMRs, F) grid "
                 f"(E={N_ELEVATORS}, c={CAPACITY})")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "geometry_heatmaps.png", dpi=120)
    plt.close()

    # b(C) vs N/F scatter
    fig, ax = plt.subplots(figsize=(8, 5))
    for cell in cells:
        ax.scatter(cell["n_over_f"], cell["betas"]["C"], s=60,
                   c=[cell["n_amrs"]], cmap="viridis", vmin=3, vmax=20)
        ax.annotate(f"N={cell['n_amrs']},F={cell['n_floors']}",
                    (cell["n_over_f"], cell["betas"]["C"]),
                    fontsize=7, xytext=(4, 4), textcoords="offset points")
    ax.axhline(0, color="grey", lw=0.5)
    ax.set_xlabel("N_AMRs / F")
    ax.set_ylabel("b(C) [s/nat]")
    ax.set_title(f"b(C) vs N/F  (Pearson r = {pearson_C:+.3f})  "
                 f"  E={N_ELEVATORS}, c={CAPACITY}")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "geometry_betaC_vs_NoverF.png", dpi=120)
    plt.close()

    out = {
        "by_cell": by_cell,
        "pre_reg_check": {
            "pearson_corr_NF_betaC": pearson_C,
            "pearson_corr_NF_betaI": float(np.corrcoef(rs, bis)[0, 1]),
            "betaC_zero_crossing_R": crossing_R,
            "verdict": verdict,
            "verdict_text": verdict_text,
        },
        "config": {
            "n_elevators": N_ELEVATORS, "capacity": CAPACITY,
            "n_samples_per_cell": N_SAMPLES,
            "wave_size_range": [WAVE_SIZE_MIN, WAVE_SIZE_MAX],
        },
    }
    out_json = RESULTS_DIR / "v0_2_geometric_mechanism.json"
    with out_json.open("w") as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved JSON to {out_json}")
    print(f"Saved figures to {FIG_DIR}")


if __name__ == "__main__":
    main()
