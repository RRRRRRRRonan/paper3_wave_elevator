"""
MVS v0.5 — wave-design (composition) policies P0-P6 for the Phase 5 grid.

Each policy is a *selection rule* over a shared candidate pool of random
waves: given a DataFrame of candidate waves with precomputed descriptors, the
rule returns k row positions, which the harness materialises and simulates.
Operating all seven policies on one candidate pool keeps the contest fair
(pre-registration `phase5_scaleup_preregistration.md` §3.4) and mirrors the
Phase 4 v2 quartile-corner methodology.

Naming note: these P0-P6 are *wave-composition* policies (which orders to
release together), distinct from the Phase 4 H1 operational dispatch policies
(fifo / cluster). Phase 5 holds operational dispatch fixed; the tactical
wave-design layer is the variable under test.

  P0 random            — uniform sample (baseline)
  P1 dest_cluster      — waves of low destination spread
  P2 cardinality       — waves of low cross-floor count (short trips)
  P3 dir_balanced      — waves of low directional imbalance I
  P4 temporal          — waves of low temporal CV T
  P5 phi               — waves in the Phi-favourable (C, I) corner   [this paper]
  P6 spo_tree          — waves of lowest SPO-Tree cell-mean predicted makespan

P5 vs P6 is the D1 differentiator (methodology §4.1.2): P5 selects by the Phi
cell-median corner rule; P6 by an SPO-Tree cell-MEAN predictor — the SPO-Tree
literature's assumption. Each policy restricts to its favourable subset and
samples k waves from it; P0's favourable subset is the whole pool.

Run the self-tests with:  python -m src.wave_policies
"""
from __future__ import annotations

import random
from typing import Callable, Dict, List, Optional, Sequence

import numpy as np
import pandas as pd

from src.features import compute_all_features
from src.simulator import Order, Wave

# Favourable-subset quantile for the structured filter policies (matches the
# Phase 4 v2 top/bottom-25 % corner cut).
FILTER_Q = 0.25
DESC_COLS = ["size", "cross_floor", "floor_distance", "C", "I", "T",
             "dest_spread"]


# --------------------------------------------------------------------------
# Candidate-pool construction
# --------------------------------------------------------------------------

def describe_wave(wave: Wave) -> dict:
    """Phi features (C, I, T) plus the descriptors the policies filter on."""
    f = compute_all_features(wave)
    dests = [o.dest_floor for o in wave.orders]
    f["dest_spread"] = (max(dests) - min(dests)) if dests else 0
    return f


def build_candidates(pool: List[Order], size: int, n: int,
                     rng: random.Random) -> pd.DataFrame:
    """Generate `n` random waves of fixed `size` with descriptors + order idxs.

    Generalises experiments_phase4_v2.build_candidate_waves with the T and
    dest_spread descriptors the Phase 5 policies need.
    """
    rows = []
    for k in range(n):
        idxs = rng.sample(range(len(pool)), size)
        wave = Wave(orders=[pool[i] for i in idxs], release_time=0.0)
        rows.append({"wave_id": k, **describe_wave(wave), "idxs": tuple(idxs)})
    return pd.DataFrame(rows).reset_index(drop=True)


def materialise(cand_row, pool: List[Order]) -> Wave:
    """Rebuild a Wave from a candidate row's stored order indices."""
    return Wave(orders=[pool[i] for i in cand_row["idxs"]], release_time=0.0)


# --------------------------------------------------------------------------
# Corner arms — the decomposition partition shared by Blocks A / C and P5
# --------------------------------------------------------------------------

CORNER_ARMS = ["random", "HC_HI", "HC_LI", "LC_HI", "LC_LI"]


def corner_positions(cand: pd.DataFrame, arm: str,
                     q: float = FILTER_Q) -> np.ndarray:
    """Row positions for a decomposition corner arm (Phase 4 v2 quartile scheme).

    'random' is the whole candidate pool; the four corners are the C/I
    quartile-intersection bins (HC = high-C top quartile, LI = low-I bottom
    quartile, etc.).
    """
    if arm == "random":
        return np.arange(len(cand))
    c_high, i_high = arm.startswith("HC"), arm.endswith("HI")
    C, I = cand["C"].to_numpy(), cand["I"].to_numpy()
    c_cut = np.quantile(C, 1.0 - q if c_high else q)
    i_cut = np.quantile(I, 1.0 - q if i_high else q)
    c_mask = C >= c_cut if c_high else C <= c_cut
    i_mask = I >= i_cut if i_high else I <= i_cut
    pos = np.where(c_mask & i_mask)[0]
    return pos if len(pos) else np.arange(len(cand))


def favorable_label(beta: dict) -> str:
    """The Phi-favourable corner label from OLS beta signs (Phase 4 v2 rule)."""
    return (("HC" if beta["beta_C"] < 0 else "LC") + "_"
            + ("HI" if beta["beta_I"] < 0 else "LI"))


# --------------------------------------------------------------------------
# Predictor fits used by P5 / P6 (called by the harness after a training pass)
# --------------------------------------------------------------------------

def fit_phi_beta(cand: pd.DataFrame, makespans: Sequence[float]) -> dict:
    """OLS of makespan on (1, C, I); returns the (beta_C, beta_I) signs P5 needs."""
    X = np.column_stack([np.ones(len(cand)), cand["C"].to_numpy(),
                         cand["I"].to_numpy()])
    coef, *_ = np.linalg.lstsq(X, np.asarray(makespans, dtype=float),
                               rcond=None)
    return {"beta_C": float(coef[1]), "beta_I": float(coef[2])}


def fit_spo_tree(cand: pd.DataFrame, makespans: Sequence[float],
                 feature_cols: Sequence[str] = ("C", "I"),
                 max_depth: int = 3, seed: int = 0):
    """SPO-Tree cell-average predictor: a depth-limited regression tree.

    A DecisionTreeRegressor with squared-error splits predicts each leaf's
    *mean* training makespan — exactly the SPO-Tree cell-average rule, the
    contrast against P5's Phi cell-median selection.
    """
    from sklearn.tree import DecisionTreeRegressor
    tree = DecisionTreeRegressor(max_depth=max_depth, random_state=seed)
    tree.fit(cand[list(feature_cols)].to_numpy(),
             np.asarray(makespans, dtype=float))
    return tree


# --------------------------------------------------------------------------
# The seven selection rules — uniform signature (cand, k, rng, ctx) -> [int]
# --------------------------------------------------------------------------

def _sample(positions: np.ndarray, k: int, rng: random.Random) -> List[int]:
    """Draw k row positions with replacement (empty -> caller's fallback)."""
    return [int(rng.choice(positions)) for _ in range(k)]


def _select_low(cand: pd.DataFrame, col: str, k: int, rng: random.Random,
                q: float = FILTER_Q) -> List[int]:
    """Sample k waves from the favourable (lowest-`col`) quantile subset."""
    vals = cand[col].to_numpy()
    cut = np.quantile(vals, q)
    pos = np.where(vals <= cut)[0]
    if len(pos) == 0:
        pos = np.arange(len(cand))
    return _sample(pos, k, rng)


def select_random(cand, k, rng, ctx=None) -> List[int]:           # P0
    return _sample(np.arange(len(cand)), k, rng)


def select_dest_cluster(cand, k, rng, ctx=None) -> List[int]:     # P1
    return _select_low(cand, "dest_spread", k, rng)


def select_cardinality(cand, k, rng, ctx=None) -> List[int]:      # P2
    return _select_low(cand, "cross_floor", k, rng)


def select_dir_balanced(cand, k, rng, ctx=None) -> List[int]:     # P3
    return _select_low(cand, "I", k, rng)


def select_temporal(cand, k, rng, ctx=None) -> List[int]:         # P4
    return _select_low(cand, "T", k, rng)


def select_phi(cand, k, rng, ctx) -> List[int]:                   # P5
    """Phi-favourable (C, I) corner: sign(beta) picks the quartile corner."""
    return _sample(corner_positions(cand, favorable_label(ctx)), k, rng)


def select_spo_tree(cand, k, rng, ctx) -> List[int]:              # P6
    """Lowest SPO-Tree-predicted-makespan quartile."""
    tree = ctx["spo_tree"]
    cols = list(ctx.get("feature_cols", ("C", "I")))
    pred = tree.predict(cand[cols].to_numpy())
    cut = np.quantile(pred, FILTER_Q)
    pos = np.where(pred <= cut)[0]
    if len(pos) == 0:
        pos = np.arange(len(cand))
    return _sample(pos, k, rng)


POLICIES: Dict[str, Callable] = {
    "P0_random": select_random,
    "P1_dest_cluster": select_dest_cluster,
    "P2_cardinality": select_cardinality,
    "P3_dir_balanced": select_dir_balanced,
    "P4_temporal": select_temporal,
    "P5_phi": select_phi,
    "P6_spo_tree": select_spo_tree,
}

# Policies that need a fitted predictor in ctx (the harness supplies it).
NEEDS_CTX = {"P5_phi": "beta", "P6_spo_tree": "spo_tree"}


def select(policy: str, cand: pd.DataFrame, k: int, rng: random.Random,
           ctx: Optional[dict] = None) -> List[int]:
    """Registry entry point: dispatch to a named policy's selection rule."""
    if policy not in POLICIES:
        raise ValueError(f"unknown policy {policy!r} (known: {sorted(POLICIES)})")
    return POLICIES[policy](cand, k, rng, ctx)


# --------------------------------------------------------------------------
# P7 — optimization reference (local search over wave compositions)
# --------------------------------------------------------------------------

def optimize_wave_localsearch(pool: List[Order], size: int, sim_fn,
                              rng: random.Random, n_iter: int = 40):
    """P7 reference optimizer: local search over wave compositions.

    Starts from a random size-`size` wave and repeatedly swaps one in-wave
    order for one out-of-wave order, keeping a swap iff it lowers the simulated
    makespan. Unlike P0-P6 (feature-based selection, no simulator access), P7
    queries `sim_fn` during the search, so it is a near-best-achievable
    *reference* — the "how close to optimal" yardstick the deployable policies
    are measured against, not itself a deployable policy. `n_iter` is
    deliberately modest: a credible practical local optimum, not a proven
    global one (the paper reports it as such).

    Returns (best_makespan, best_order_index_tuple).
    """
    idx = rng.sample(range(len(pool)), size)
    best = sim_fn(Wave(orders=[pool[i] for i in idx], release_time=0.0))
    in_set = set(idx)
    for _ in range(n_iter):
        out_i = rng.randrange(len(pool))
        if out_i in in_set:
            continue
        drop = rng.randrange(size)
        trial = list(idx)
        trial[drop] = out_i
        cand_mk = sim_fn(Wave(orders=[pool[i] for i in trial],
                              release_time=0.0))
        if cand_mk < best:
            best, idx = cand_mk, trial
            in_set = set(trial)
    return best, tuple(idx)


# --------------------------------------------------------------------------
# Self-tests (house style: _test_* functions, run from __main__).
# --------------------------------------------------------------------------

def _candidate_fixture(pattern: str = "uniform", F: int = 5, size: int = 8,
                       n: int = 2500, seed: int = 1) -> pd.DataFrame:
    from src.demand_patterns import generate_pool
    pool = generate_pool(pattern, F, pool_size=600, seed=seed)
    return build_candidates(pool, size, n, random.Random(seed + 1))


def _test_candidates() -> None:
    cand = _candidate_fixture()
    assert len(cand) == 2500
    for col in DESC_COLS + ["idxs"]:
        assert col in cand.columns, f"missing descriptor column {col}"
    assert (cand["size"] == 8).all(), "fixed-size waves expected"
    assert (cand["dest_spread"] >= 0).all()
    print(f"  [OK] build_candidates: 2500 waves, descriptors {DESC_COLS}")


def _test_filter_directions() -> None:
    """Each structured filter policy must shift its target feature downward."""
    rng = random.Random(7)
    cand = _candidate_fixture()
    base = cand.iloc[select_random(cand, 600, random.Random(7))]
    for policy, col in [(select_dest_cluster, "dest_spread"),
                        (select_cardinality, "cross_floor"),
                        (select_dir_balanced, "I")]:
        sel = cand.iloc[policy(cand, 600, random.Random(7))]
        assert sel[col].mean() < base[col].mean(), (
            f"{policy.__name__}: mean {col} {sel[col].mean():.3f} "
            f"not below baseline {base[col].mean():.3f}")
    # P4 needs temporal structure -> diurnal pool
    cand_d = _candidate_fixture(pattern="diurnal")
    base_d = cand_d.iloc[select_random(cand_d, 600, random.Random(7))]
    sel_d = cand_d.iloc[select_temporal(cand_d, 600, random.Random(7))]
    assert sel_d["T"].mean() < base_d["T"].mean(), "P4 did not lower T"
    print("  [OK] filter policies P1/P2/P3/P4 each lower their target feature")


def _test_phi_corner() -> None:
    cand = _candidate_fixture()
    medC, medI = cand["C"].median(), cand["I"].median()
    # beta_C < 0, beta_I < 0  ->  favourable = high C, high I
    hi = cand.iloc[select_phi(cand, 600, random.Random(3),
                              {"beta_C": -1.0, "beta_I": -1.0})]
    assert hi["C"].mean() > medC and hi["I"].mean() > medI, "HC_HI corner wrong"
    # beta_C > 0  ->  favourable = low C
    lo = cand.iloc[select_phi(cand, 600, random.Random(3),
                              {"beta_C": 1.0, "beta_I": -1.0})]
    assert lo["C"].mean() < medC, "LC corner wrong"
    print("  [OK] P5 phi: beta signs select the correct (C, I) corner")


def _test_spo_tree() -> None:
    cand = _candidate_fixture()
    # synthetic makespan increasing in C and I (no simulator needed for unit test)
    y = 100.0 + 25.0 * cand["C"].to_numpy() + 12.0 * cand["I"].to_numpy()
    beta = fit_phi_beta(cand, y)
    assert beta["beta_C"] > 0 and beta["beta_I"] > 0, f"OLS sign wrong: {beta}"
    tree = fit_spo_tree(cand, y, seed=0)
    sel = select_spo_tree(cand, 600, random.Random(5),
                          {"spo_tree": tree, "feature_cols": ("C", "I")})
    y_sel = y[np.asarray(sel)]
    assert y_sel.mean() < y.mean(), "P6 did not pick low-predicted waves"
    print(f"  [OK] P6 spo_tree: fit + select, mean makespan "
          f"{y_sel.mean():.1f} < pool {y.mean():.1f}")


def _test_registry_and_determinism() -> None:
    cand = _candidate_fixture()
    y = 100.0 + 20.0 * cand["C"].to_numpy()
    ctx = {"beta_C": -1.0, "beta_I": -1.0,
           "spo_tree": fit_spo_tree(cand, y, seed=0),
           "feature_cols": ("C", "I")}
    for name in POLICIES:
        a = select(name, cand, 200, random.Random(9), ctx)
        b = select(name, cand, 200, random.Random(9), ctx)
        assert a == b, f"{name}: not reproducible under fixed seed"
        assert len(a) == 200 and all(0 <= i < len(cand) for i in a), \
            f"{name}: invalid index set"
    print(f"  [OK] registry: all {len(POLICIES)} policies valid + reproducible")


def _test_p7() -> None:
    from src.demand_patterns import generate_uniform
    pool = generate_uniform(5, 400, seed=1)
    # synthetic objective: total floor distance (deterministic, no simulator)
    def sim_fn(w):
        return float(sum(abs(o.source_floor - o.dest_floor) for o in w.orders))
    rng = random.Random(2)
    randoms = [sim_fn(Wave(orders=[pool[i]
                                   for i in rng.sample(range(len(pool)), 8)]))
               for _ in range(30)]
    best, idx = optimize_wave_localsearch(pool, 8, sim_fn, random.Random(3),
                                          n_iter=60)
    assert len(set(idx)) == 8, "P7 produced an invalid (duplicate-order) wave"
    assert best < min(randoms), f"P7 {best} not below random min {min(randoms)}"
    print(f"  [OK] P7 localsearch: {best:.0f} < random-start min "
          f"{min(randoms):.0f}")


if __name__ == "__main__":
    _test_candidates()
    _test_filter_directions()
    _test_phi_corner()
    _test_spo_tree()
    _test_registry_and_determinism()
    _test_p7()
    print("wave_policies.py: all self-tests passed.")
