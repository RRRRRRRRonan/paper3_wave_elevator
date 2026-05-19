"""
MVS v0.5 Phase 5 — tunable parameters and the warehouse-config array.

EVERYTHING the Phase 5 grid depends on lives here as an editable parameter;
nothing downstream is hard-coded. The config array is REGENERATED from these
values by `make_config_array()` on every run — it is a draft artefact, freely
tunable up to the smoke calibration and the pre-registration §10 author
sign-off, which is where the design is locked for the confirmatory full run.

Locking before the smoke would be premature; tuning after the full run would
be p-hacking. The window in between — W3 (harness) through W4 (smoke) — is the
legitimate tuning phase. Edit any value here and re-run; nothing is frozen.
"""
from __future__ import annotations

# ---- Warehouse-configuration factors (pre-reg §2.1) ----------------------
FACTOR_F = [3, 5, 8]            # floors
FACTOR_A = [5, 15, 30]          # AMRs
FACTOR_E = [1, 2]               # elevators
FACTOR_DEMAND = ["uniform", "clustered", "diurnal"]

CAPACITY = 2                    # elevator capacity (c = 2 throughout, as Phase 4)

# ---- Demand-pattern parameters (tunable; diurnal horizon is a smoke item) -
DEMAND_PARAMS = {
    "uniform": {},
    "clustered": {"hot_fraction": 0.2, "hot_mass": 0.8},
    "diurnal": {"time_horizon": 50.0, "peak_window": 0.3, "peak_share": 0.7},
}

# ---- Sampling ------------------------------------------------------------
ORDER_POOL_SIZE = 600           # orders per warehouse config
CANDIDATE_POOL = 3000           # random candidate waves per (config, size)
N_PER_ARM = 200                 # waves simulated per arm / policy
TRAIN_SAMPLE = 200              # candidate waves simulated to fit beta / SPO-tree
SEED_BASE = 20260519

# ---- Block definitions (pre-reg §2.2) ------------------------------------
BLOCK_A = {"models": ["abstraction", "batched"], "sizes": [8, 30],
           "arms": ["random", "HC_HI", "HC_LI", "LC_HI", "LC_LI"]}
BLOCK_B = {"model": "batched", "sizes": [8, 30], "n_configs": 6}
BLOCK_C = {"models": ["abstraction", "batched", "M3_s20"], "sizes": [16],
           "arms": ["random", "HC_HI", "HC_LI", "LC_HI", "LC_LI"],
           "n_configs": 6}
M3_SIGMA = 0.20

# ---- Smoke slice (pre-reg §7; ~1/60 scale) -------------------------------
SMOKE = {"n_configs": 3, "models": ["abstraction", "batched"], "size": 8,
         "n_per_arm": 20, "candidate_pool": 300, "train_sample": 60}


def make_config_array():
    """Generate the 18-config 1/3 fraction (regenerable, never frozen here).

    1/3 fraction of the 3x3x2x3 = 54 full grid via the defining relation
    demand_idx = (F_idx + A_idx) mod 3, crossed with both E levels:
    9 (F, A, demand) combos x 2 E levels = 18 configs. Every factor level is
    balanced (F / A / demand each appear 6x, E appears 9x).
    """
    configs = []
    cid = 0
    for fi, F in enumerate(FACTOR_F):
        for ai, A in enumerate(FACTOR_A):
            demand = FACTOR_DEMAND[(fi + ai) % 3]
            for E in FACTOR_E:
                configs.append({"config_id": cid, "F": F, "n_amrs": A,
                                "n_elevators": E, "demand": demand})
                cid += 1
    return configs


def e2_subset(configs):
    """The E = 2 configs (Blocks B and C draw their subsets from these)."""
    return [c for c in configs if c["n_elevators"] == 2]
