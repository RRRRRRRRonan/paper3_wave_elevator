"""
Study 2 (Phase 6) release procedures, as specified in
paper_draft/phase6_method_study_protocol.md.

  P10   sequence-aware re-ordering (§5.1): co-ride blocks, readiness, chaining
  P10g  grouping-only re-ordering (§5.1 step 6), for the chaining increment
  P11   co-ride-aware constructive generator (§5.3)
  P8    savings-style score (verbatim formula of AMEND-B B-3)
  P9    linear SPO+ bottom-k predictor (verbatim AMEND-C C-1 fit)
  P7    budgeted multi-start local search (P7-matched, §4), same move as
        wave_policies.optimize_wave_localsearch
  GSV   screen-then-verify selection with the §3.2 tie rule
  warm start: concatenation of released waves with absolute ready offsets (§9)

A candidate is a tuple of order-pool indices in processing sequence; P10 and
P10g return a permutation of positions that is applied to that tuple.
The Phase 5 modules are not modified.

Run the self-tests with:  python -m src.phase6_policies
"""
from __future__ import annotations

import random
from collections import Counter
from typing import Callable, Dict, List, Optional, Sequence, Tuple

import numpy as np

from src.simulator import Order, Wave, simulate_wave

OrderTuple = Tuple[int, int, float]


# --------------------------------------------------------------------------
# Order access helpers
# --------------------------------------------------------------------------

def tuples_of(pool: Sequence[Order], idxs: Sequence[int]) -> List[OrderTuple]:
    return [(pool[i].source_floor, pool[i].dest_floor,
             float(pool[i].release_time)) for i in idxs]


def wave_of(orders: Sequence[OrderTuple]) -> Wave:
    return Wave(orders=[Order(id=k, source_floor=s, dest_floor=d,
                              release_time=r)
                        for k, (s, d, r) in enumerate(orders)],
                release_time=0.0)


def apply_perm(idxs: Sequence[int], perm: Sequence[int]) -> Tuple[int, ...]:
    return tuple(idxs[p] for p in perm)


# --------------------------------------------------------------------------
# P10 / P10g
# --------------------------------------------------------------------------

def _blocks(orders: Sequence[OrderTuple], capacity: int):
    groups: Dict[Tuple[int, int], List[int]] = {}
    same: List[int] = []
    for pos, (s, d, _r) in enumerate(orders):
        if s == d:
            same.append(pos)
        else:
            groups.setdefault((s, d), []).append(pos)
    blocks = []
    for (s, d), members in groups.items():
        members = sorted(members, key=lambda p: (orders[p][2], p))
        for i in range(0, len(members), capacity):
            b = members[i:i + capacity]
            blocks.append({"s": s, "d": d, "members": b, "first": min(b),
                           "ready": max(orders[p][2] for p in b)})
    return blocks, same


def p10_permutation(orders: Sequence[OrderTuple], capacity: int = 2,
                    initial_floor: int = 1) -> List[int]:
    """P10 sequence-aware re-ordering (protocol §5.1 steps 1 to 5)."""
    blocks, same = _blocks(orders, capacity)
    placed, cur = [], initial_floor
    for level in sorted({b["ready"] for b in blocks}):
        rem = [b for b in blocks if b["ready"] == level]
        while rem:
            b = min(rem, key=lambda b: (abs(b["s"] - cur), -len(b["members"]),
                                        (b["s"], b["d"]), b["first"]))
            rem.remove(b)
            placed.append(b)
            cur = b["d"]
    attach: Dict[int, List[int]] = {j: [] for j in range(len(placed))}
    tail: List[int] = []
    for p in sorted(same, key=lambda p: (orders[p][2], p)):
        f, r = orders[p][0], orders[p][2]
        j = next((j for j, b in enumerate(placed)
                  if b["d"] == f and b["ready"] <= r), None)
        (attach[j] if j is not None else tail).append(p)
    perm: List[int] = []
    for j, b in enumerate(placed):
        perm += b["members"] + attach[j]
    return perm + tail


def p10g_permutation(orders: Sequence[OrderTuple], capacity: int = 2) -> List[int]:
    """P10g: co-ride blocks ordered by (ready time, first position); same-floor
    orders keep their positions (protocol §5.1 step 6)."""
    blocks, _ = _blocks(orders, capacity)
    blocks.sort(key=lambda b: (b["ready"], b["first"]))
    cross_seq = iter([p for b in blocks for p in b["members"]])
    return [pos if s == d else next(cross_seq)
            for pos, (s, d, _r) in enumerate(orders)]


# --------------------------------------------------------------------------
# P11 constructive generator
# --------------------------------------------------------------------------

def p11_construct(src: np.ndarray, dst: np.ndarray, size: int, capacity: int,
                  alpha: float, beta: float, gamma: float,
                  rng: random.Random) -> List[int]:
    """One P11 order set in construction order (protocol §5.3 steps 1 to 2).

    `src`, `dst` are the source and destination floors of the order pool.
    The caller applies P10 to the result (step 3).
    """
    src = np.asarray(src, dtype=int)
    dst = np.asarray(dst, dtype=int)
    n_pool = len(src)
    if size > n_pool:
        raise ValueError("size exceeds the order pool")
    n_fl = int(max(src.max(), dst.max())) + 1
    cross = src != dst
    cross_idx = np.flatnonzero(cross)
    if len(cross_idx) == 0:
        raise ValueError("P11 needs at least one cross-floor order")
    chosen = np.zeros(n_pool, dtype=bool)
    count = np.zeros((n_fl, n_fl), dtype=int)
    is_dest = np.zeros(n_fl, dtype=bool)
    is_src = np.zeros(n_fl, dtype=bool)
    endp = np.zeros(n_fl, dtype=bool)

    def add(i: int) -> None:
        chosen[i] = True
        count[src[i], dst[i]] += 1
        is_dest[dst[i]] = True
        is_src[src[i]] = True
        endp[src[i]] = True
        endp[dst[i]] = True

    first = int(cross_idx[rng.randrange(len(cross_idx))])
    seq = [first]
    add(first)
    while len(seq) < size:
        pair = cross & (count[src, dst] % capacity != 0)
        chain = is_dest[src] | is_src[dst]
        new_floors = ((~endp[src]).astype(int)
                      + ((~endp[dst]) & (dst != src)).astype(int))
        score = alpha * pair + beta * chain - gamma * new_floors
        score = np.where(chosen, -np.inf, score)
        best = score.max()
        ties = np.flatnonzero(np.abs(score - best) <= 1e-12)
        pick = int(ties[rng.randrange(len(ties))])
        seq.append(pick)
        add(pick)
    return seq


# --------------------------------------------------------------------------
# P8 and P9 (verbatim definitions from the 2026-07-08 amendments)
# --------------------------------------------------------------------------

def p8_score(orders: Sequence[OrderTuple]) -> float:
    """AMEND-B B-3 savings-style score (b2_b3_benchmarks.run_b3.p8_score)."""
    travel = sum(abs(s - d) for s, d, _ in orders)
    groups = Counter((s, d) for s, d, _ in orders)
    savings = sum((n // 2) * abs(s - d) for (s, d), n in groups.items())
    dsts = [d for _, d, _ in orders]
    return travel - savings + 0.5 * (max(dsts) - min(dsts))


def spo_plus_fit(X: np.ndarray, c: np.ndarray, k_train: int = 13,
                 step: float = 0.05, iters: int = 300) -> np.ndarray:
    """AMEND-C C-1 linear SPO+ subgradient fit (amendC1_p9_spoplus.spo_plus_fit)."""
    n, p = X.shape
    beta = np.zeros(p)

    def zstar(cost):
        sel = np.zeros(n)
        sel[np.argsort(cost, kind="stable")[:k_train]] = 1.0
        return sel

    z_c = zstar(c)
    for _ in range(iters):
        c_hat = X @ beta
        g_vec = zstar(2 * c_hat - c) - z_c
        beta += step * (X.T @ g_vec)
    return beta


def p9_predictions(features: np.ndarray, train_idx: Sequence[int],
                   c_train: Sequence[float], hyper: dict) -> np.ndarray:
    """Standardize (C, I, T) over the candidate pool, fit SPO+ on the training
    draws, return predicted costs for every candidate (AMEND-C C-1)."""
    feats = np.asarray(features, dtype=float)
    mu, sd = feats.mean(axis=0), feats.std(axis=0)
    sd[sd == 0] = 1.0
    X = (feats - mu) / sd
    beta = spo_plus_fit(X[list(train_idx)], np.asarray(c_train, dtype=float),
                        hyper["k_train"], hyper["step"], hyper["iters"])
    return X @ beta


# --------------------------------------------------------------------------
# Rankings, GSV, local search
# --------------------------------------------------------------------------

def tie_ranks(n: int, rng: random.Random) -> np.ndarray:
    """Rank of each candidate in a fixed uniformly random permutation (§3.2 ties)."""
    perm = list(range(n))
    rng.shuffle(perm)
    rank = np.empty(n, dtype=int)
    rank[perm] = np.arange(n)
    return rank


def ranked(values: Sequence[float], ties: np.ndarray) -> np.ndarray:
    """Candidate positions sorted by value, ties by the fixed permutation."""
    return np.lexsort((ties, np.asarray(values, dtype=float)))


def gsv_select(screen: Sequence[float], verify: Callable[[int], float], k: int,
               ties: np.ndarray, pool_mask: Optional[np.ndarray] = None
               ) -> Tuple[int, float, List[int]]:
    """Screen by `screen`, verify the top k with `verify`, return
    (released position, its verified value, shortlist)."""
    order = ranked(screen, ties)
    if pool_mask is not None:
        order = order[pool_mask[order]]
    short = [int(i) for i in order[:k]]
    vals = [verify(i) for i in short]
    best = min(range(len(short)), key=lambda j: (vals[j], ties[short[j]]))
    return short[best], vals[best], short


def local_search_budgeted(n_pool: int, size: int,
                          eval_fn: Callable[[Tuple[int, ...]], float],
                          rng: random.Random, budget: int, n_iter: int = 40,
                          end_hook: Optional[Callable] = None):
    """Multi-start local search with a total evaluation budget (P7-matched).

    Each run is wave_policies.optimize_wave_localsearch (same rng call order);
    runs repeat until `budget` evaluations are spent, the last run truncated.
    `end_hook(idxs) -> (value, idxs2)`, if given, is called once after each
    completed run while budget remains (e.g. the M2 value of the end point's
    P10 re-ordering); each call counts as one evaluation.
    Returns ([(value, idxs), ...] end points, evaluations spent, hook results),
    the hook results in the same discovery order.
    """
    ends, extras, spent = [], [], 0
    while spent < budget:
        idx = rng.sample(range(n_pool), size)
        best = eval_fn(tuple(idx))
        spent += 1
        in_set = set(idx)
        for _ in range(n_iter):
            if spent >= budget:
                break
            out_i = rng.randrange(n_pool)
            if out_i in in_set:
                continue
            drop = rng.randrange(size)
            trial = list(idx)
            trial[drop] = out_i
            mk = eval_fn(tuple(trial))
            spent += 1
            if mk < best:
                best, idx = mk, trial
                in_set = set(trial)
        ends.append((best, tuple(idx)))
        if end_hook is not None and spent < budget:
            extras.append(end_hook(tuple(idx)))
            spent += 1
    return ends, spent, extras


def signature(pool: Sequence[Order], idxs: Sequence[int]) -> Tuple[OrderTuple, ...]:
    """What every evaluator sees: the ordered (source, destination, ready)
    list. Candidates with equal signatures have equal values everywhere."""
    return tuple(tuples_of(pool, idxs))


def first_k_distinct(order: Sequence[int], sig_ids: Sequence[int],
                     k: int) -> List[int]:
    """The first k positions of `order` with distinct signature ids."""
    seen, out = set(), []
    for g in order:
        sid = sig_ids[g]
        if sid in seen:
            continue
        seen.add(sid)
        out.append(int(g))
        if len(out) == k:
            break
    return out


# --------------------------------------------------------------------------
# Warm start (§9)
# --------------------------------------------------------------------------

def concat_chain(pool: Sequence[Order], chain: Sequence[Sequence[int]],
                 epochs: Sequence[float]) -> List[OrderTuple]:
    """Released waves in release order, ready offsets made absolute."""
    out: List[OrderTuple] = []
    for idxs, e in zip(chain, epochs):
        out += [(s, d, e + r) for s, d, r in tuples_of(pool, idxs)]
    return out


# --------------------------------------------------------------------------
# Self-tests
# --------------------------------------------------------------------------

def _toy(rng, n, F, stagger):
    return [(rng.randint(1, F), rng.randint(1, F),
             float(rng.choice([0, 3, 8.5])) if stagger else 0.0)
            for _ in range(n)]


def _test_p10_hand() -> None:
    o = [(1, 3, 0.0), (2, 1, 0.0), (1, 3, 0.0), (3, 2, 0.0), (2, 2, 0.0),
         (1, 3, 0.0)]
    # blocks (1,3):[0,2],[5]; (2,1):[1]; (3,2):[3]; chain from 1:
    # [0,2] -> 3; [3] -> 2; [1] -> 1; [5] -> 3; same-floor 4 after block [3]
    assert p10_permutation(o) == [0, 2, 3, 4, 1, 5], p10_permutation(o)
    # readiness first: the (2,1) block is ready at 0, the (1,3) pair at 4
    o = [(1, 3, 4.0), (1, 3, 0.0), (2, 1, 0.0)]
    assert p10_permutation(o) == [2, 1, 0], p10_permutation(o)
    # P10g: blocks by (ready, first position); same-floor positions kept
    o = [(2, 2, 0.0), (1, 3, 0.0), (3, 1, 0.0), (1, 3, 0.0)]
    assert p10g_permutation(o) == [0, 1, 3, 2], p10g_permutation(o)
    print("  [OK] P10 / P10g hand-built cases")


def _test_p10_properties() -> None:
    rng = random.Random(424_300)
    for _ in range(2000):
        o = _toy(rng, rng.randint(1, 30), rng.choice([3, 5, 8]),
                 rng.random() < 0.5)
        perm = p10_permutation(o)
        assert sorted(perm) == list(range(len(o))), "not a permutation"
        o2 = [o[p] for p in perm]
        assert p10_permutation(o2) == list(range(len(o))), "not idempotent"
        g = p10g_permutation(o)
        assert sorted(g) == list(range(len(o)))
        # same (s, d) orders that share a block are adjacent in the output
        pos = {p: k for k, p in enumerate(perm)}
        blocks, _ = _blocks(o, 2)
        for b in blocks:
            ks = sorted(pos[p] for p in b["members"])
            assert ks[-1] - ks[0] == len(ks) - 1, "block split"
    print("  [OK] P10: permutation, idempotent, blocks contiguous (2,000 toy "
          "waves with and without ready times); P10g permutation")


def _test_p11() -> None:
    rng = random.Random(424_301)
    src = np.array([rng.randint(1, 5) for _ in range(600)])
    dst = np.array([rng.randint(1, 5) for _ in range(600)])
    for size in (8, 16, 30):
        s1 = p11_construct(src, dst, size, 2, 2.0, 1.0, 0.5, random.Random(7))
        s2 = p11_construct(src, dst, size, 2, 2.0, 1.0, 0.5, random.Random(7))
        assert s1 == s2, "not deterministic"
        assert len(set(s1)) == size and src[s1[0]] != dst[s1[0]]
    # pure pairing weight: every cross-floor (s, d) count ends even when the
    # pool allows it (alpha only, size even)
    seq = p11_construct(src, dst, 16, 2, 1.0, 0.0, 0.0, random.Random(3))
    cnt = Counter((int(src[i]), int(dst[i])) for i in seq
                  if src[i] != dst[i])
    odd = sum(v % 2 for v in cnt.values())
    assert odd <= 1, f"pairing weight left {odd} open pairs"
    print("  [OK] P11: distinct orders, cross-floor seed, deterministic, "
          "pairing weight closes co-ride pairs")


def _test_p8_p9() -> None:
    o = [(1, 3, 0.0), (1, 3, 0.0), (2, 5, 0.0)]
    # travel 2+2+3 = 7; savings 1*2 = 2; dest spread 5-3 = 2 -> 7 - 2 + 1 = 6
    assert p8_score(o) == 6.0
    import sys
    from pathlib import Path
    scripts = (Path(__file__).resolve().parents[2] / "revision_2026-07-08"
               / "tier2_analysis" / "scripts")
    sys.path.insert(0, str(scripts))
    try:
        from amendC1_p9_spoplus import spo_plus_fit as original
    except Exception as exc:
        raise AssertionError(f"P9 equality test cannot run ({exc})")
    rng = np.random.default_rng(424_302)
    for _ in range(20):
        X = rng.normal(size=(200, 3))
        c = X @ rng.normal(size=3) + rng.normal(size=200)
        assert np.array_equal(spo_plus_fit(X, c), original(X, c))
    print("  [OK] P8 hand case; P9 fit identical to the AMEND-C code (20 draws)")


def _test_local_search() -> None:
    from src.wave_policies import optimize_wave_localsearch
    rng = random.Random(424_303)
    pool = [Order(i, rng.randint(1, 5), rng.randint(1, 5)) for i in range(120)]

    def ev(idxs):
        return simulate_wave(Wave([pool[i] for i in idxs]), n_amrs=3,
                             n_elevators=2, capacity=2, batched=True)

    def sim_fn(w):
        return simulate_wave(w, n_amrs=3, n_elevators=2, capacity=2,
                             batched=True)

    ref = optimize_wave_localsearch(pool, 8, sim_fn, random.Random(11), 40)
    ends, spent, _ = local_search_budgeted(len(pool), 8, ev, random.Random(11),
                                           budget=10_000, n_iter=40)
    assert ends[0] == ref, (ends[0], ref)
    ends, spent, _ = local_search_budgeted(len(pool), 8, ev, random.Random(12),
                                           budget=333, n_iter=40)
    assert spent == 333
    # with the P10 hook: same first end point, one extra evaluation per run,
    # budget still exact
    def hook(ix):
        ix2 = apply_perm(ix, p10_permutation(tuples_of(pool, ix)))
        return ev(ix2), ix2
    ends2, spent2, extras = local_search_budgeted(
        len(pool), 8, ev, random.Random(11), budget=500, n_iter=40, end_hook=hook)
    assert ends2[0] == ref and spent2 == 500
    assert len(extras) in (len(ends2), len(ends2) - 1)
    print("  [OK] budgeted local search: first run = optimize_wave_localsearch; "
          "budget exact, also with the P10 end-point hook")


def _test_concat_and_gsv() -> None:
    from src.des_evaluator import des_makespan
    rng = random.Random(424_304)
    pool = [Order(i, rng.randint(1, 5), rng.randint(1, 5),
                  float(rng.choice([0, 4]))) for i in range(60)]
    idxs = rng.sample(range(60), 16)
    one = concat_chain(pool, [idxs], [0.0])
    w = Wave([pool[i] for i in idxs])
    assert simulate_wave(wave_of(one), n_amrs=4, n_elevators=2, capacity=2,
                         batched=True) == simulate_wave(
        w, n_amrs=4, n_elevators=2, capacity=2, batched=True)
    assert des_makespan(one, 4, 2, 2, "M2") == des_makespan(w, 4, 2, 2, "M2")
    two = concat_chain(pool, [idxs, idxs[::-1]], [0.0, 100.0])
    assert all(r >= 100.0 for _, _, r in two[16:])
    # GSV: verify picks the best of the shortlist; ties by permutation
    screen = [5, 1, 1, 3, 2]
    ties = np.array([4, 1, 0, 3, 2])
    order = ranked(screen, ties)
    assert list(order) == [2, 1, 4, 3, 0]
    pos, val, short = gsv_select(screen, lambda i: [9, 7, 7, 1, 8][i], 3, ties)
    assert short == [2, 1, 4] and pos == 2 and val == 7
    assert first_k_distinct([4, 2, 0, 1, 3], [0, 1, 1, 0, 2], 2) == [4, 2]
    assert first_k_distinct([4, 2, 0, 1, 3], [0, 1, 1, 0, 2], 9) == [4, 2, 0]
    same = signature(pool, idxs)
    assert same == tuple(tuples_of(pool, idxs))
    print("  [OK] one-wave chain = single wave (closed form and DES); "
          "ranking, GSV tie rule, distinct-signature selection")


if __name__ == "__main__":
    _test_p10_hand()
    _test_p10_properties()
    _test_p11()
    _test_p8_p9()
    _test_local_search()
    _test_concat_and_gsv()
