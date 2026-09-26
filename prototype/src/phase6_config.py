"""
Phase 6 (Study 2) knobs, as fixed by paper_draft/phase6_method_study_protocol.md.

Everything here mirrors a numbered clause of the protocol; a change here is a
protocol deviation and must be logged in revision_2026-09-26_ijpr/EXECUTION-LOG.md
before any Study 2 result exists. The Phase 5 grid (configs 0-17) is reused
unchanged from src/phase5_config.py. The Stage L2 values (P11 weights, case
timing) are read from the signed L2 addendum, never edited into this file, so
the code that ran the tuning is the code that runs the study.
"""
from __future__ import annotations

from src import phase5_config as p5
from src.registration_guard import REGISTRATIONS, front_matter_field

# ---- §3.1 configurations ----------------------------------------------------
CONFIGS = p5.make_config_array()                  # the 18 Phase 5 configurations
CAPACITY = 2
DEMAND_PARAMS = p5.DEMAND_PARAMS
ORDER_POOL_SIZE = 600

# Calibrated case (§11; only if decision D-K is signed). The timing entries are
# filled from Appendix L2; None means "production defaults" and marks the case
# as not yet parameterised.
CASE_CONFIGS = [
    {"config_id": 100, "F": 3, "n_amrs": 30, "n_elevators": 2,
     "demand": "case_online_retail"},
    {"config_id": 101, "F": 3, "n_amrs": 30, "n_elevators": 3,
     "demand": "case_online_retail"},
]
def _l2_float(field: str):
    v = front_matter_field(REGISTRATIONS["phase6_L2"], field)
    return float(v) if v else None


def case_timing() -> dict:
    """Case phase times from the L2 addendum (None = not yet fixed)."""
    return {k: _l2_float(f"case_{k}") for k in
            ("speed_per_floor", "load_time", "unload_time", "service_time")}


def case_included() -> bool:
    """§11: the calibrated case runs only if the L2 addendum says yes."""
    return front_matter_field(REGISTRATIONS["phase6_L2"], "case_included").lower() == "yes"


def case_timing_ranges() -> dict:
    """(low, high) per case parameter from the L2 addendum (None if empty)."""
    out = {}
    for k in ("speed_per_floor", "load_time", "unload_time", "service_time"):
        v = front_matter_field(REGISTRATIONS["phase6_L2"], f"case_{k}_range")
        for ch in "()[]":
            v = v.replace(ch, "")
        vals = [float(x) for x in v.split(",") if x.strip()]
        out[k] = tuple(vals) if len(vals) == 2 else None
    return out


def p11_weights():
    """(alpha, beta, gamma) from the L2 addendum, or None before Stage L2.
    Accepts "2, 1, 0.5", "(2, 1, 0.5)", or "[2.0, 1.0, 0.5]"."""
    v = front_matter_field(REGISTRATIONS["phase6_L2"], "p11_weights")
    if not v:
        return None
    for ch in "()[]":
        v = v.replace(ch, "")
    w = tuple(float(x) for x in v.split(",") if x.strip())
    if len(w) != 3:
        raise ValueError(f"p11_weights in the L2 addendum must have 3 values: {v!r}")
    return w


def des_subset_mode() -> bool:
    """§14: the subset mode is decided in the L2 record, not on the command line."""
    v = front_matter_field(REGISTRATIONS["phase6_L2"], "des_subset_mode").lower()
    if v not in ("", "yes", "no"):
        raise ValueError(f"des_subset_mode in the L2 addendum must be yes or no: {v!r}")
    return v == "yes"
CASE_OUTBOUND_SHARE = 0.8
CASE_READY_HORIZON = 50.0                         # sensitivity run only

# ---- §3.2 pools and seeds ---------------------------------------------------
TEST_POOL_BASES = [20260900 + p for p in range(1, 9)]       # S_p, p = 1..8
TRAIN_POOL_BASES = [20260950 + t for t in range(1, 3)]      # S_t, t = 1, 2
BOOTSTRAP_SEED = 20260926

STREAM = {"robust_subsample": 87, "order_pool": 89, "random_candidates": 90,
          "seqvar_draw": 91, "permutations": 92, "p11": 93,
          "training_sample": 94, "p7": 95, "r_verify": 96,
          "des_subset": 97, "ties": 98, "noise": 99, "warm_start": 100}


def seed6(base: int, config_id: int, stream: int, size: int) -> int:
    """The Phase 5 `_seed` mixing formula with a Phase 6 base (§3.2)."""
    s = base + config_id * 100_003 + (stream + 1) * 37 + (size + 1) * 37 ** 2
    return s % (2 ** 31)


# ---- §3.3 to §3.4 candidate sets -------------------------------------------
SIZES = [8, 16, 30]
K_RANDOM = 3000                                   # |R|
K_P11 = 200                                       # K'
TRAIN_SAMPLE = 200                                # P5 / P9 training draws

# ---- §4 arms ----------------------------------------------------------------
P8_K = 200
P8_VERIFY_K = 20                                  # P8-verify(20), G2 comparator
P9_HYPER = {"k_train": 13, "step": 0.05, "iters": 300, "k_deploy": 200}
P7_RUNS = 8
P7_ITER = 40
P7_MATCHED_BUDGET = 6200                          # = |G| M2 evaluations
P7_MATCHED_VERIFY = 20
GSV_K = [1, 5, 10, 20, 50, 100, 6200]           # distinct signatures (§5.5)
GSV_HEADLINE_K = 20
REGRET_TOL_REL = 0.02                             # G3: max{2 %, 1 s / optimum} (protocol §7.1)
REGRET_TOL_ABS = 1.0                              # draft 2 used 4.0; see protocol §2

# ---- §7.3 execution robustness ---------------------------------------------
ROBUST_SIGMAS = [0.1, 0.2]
ROBUST_REPS = 20
ROBUST_SUBSAMPLE = 50                             # P0 and P0+P10 subsample

# ---- §5.4 P11 tuning grid (Stage L2) ----------------------------------------
P11_GRID = {"alpha": [1.0, 2.0, 4.0], "beta": [0.5, 1.0, 2.0],
            "gamma": [0.0, 0.5, 1.0]}
P11_TUNE_QUANTILE = 0.10                          # numpy default (linear) interpolation

# ---- §6 set versus sequence -------------------------------------------------
SEQVAR_CANDIDATES = 200
SEQVAR_PERMUTATIONS = 20

# ---- §7 gates (locked wording tiers; thresholds only) ----------------------
GATES = {
    "G1": {"upper": 0.075, "middle": 0.025, "sign": 0.75},
    "G2": {"upper": 0.75, "middle": 0.50},
    "G2p": {"upper": 0.50, "middle": 0.25},
    "G3": {"regret": 0.02, "upper_k": 20, "middle_k": 50, "share": 0.80},
    "G4": {"upper": 0.95, "middle": 0.80},
    "G5": {"ordering": 0.95, "retention": 0.80},
    "G6": {"upper": 0.5, "middle": 0.2},
    "G8": {"upper": 0.75, "middle": 0.50},
}

# ---- §9 warm start ----------------------------------------------------------
WARM_SIZE = 16
WARM_STEPS = 5
WARM_REPLICATES = {"P0": 3, "P5": 3, "GSV": 1}
WARM_ARM_INDEX = {"P0": 0, "P5": 1, "GSV": 2}
WARM_G5A_SAMPLE = 300
WARM_VARIANT_B_FRACTION = 0.5

# ---- §10 runtime ------------------------------------------------------------
RUNTIME_CONFIGS = [1, 7, 17]
RUNTIME_K = [1000, 3000, 10000]
RUNTIME_SIZES = [8, 16, 30, 60]

# ---- §14 contingency ------------------------------------------------------
DES_SUBSET_TOP = 500
DES_SUBSET_RANDOM = 500                           # stream 97
RUNTIME_LIMIT_HOURS = 48
PROJECTION_CONFIG = 17                            # largest configuration (F 8, 30 AMRs)
