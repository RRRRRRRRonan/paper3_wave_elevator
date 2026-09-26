# Bug report (2026-07-08): heap-dependent tie-breaking in the elevator pools

**Severity**: latent nondeterminism in the production simulator; affects
exact reproducibility of every artifact produced with it. Does not by
itself invalidate any stored result (each run is internally consistent),
but the manuscript's determinism/reproducibility statement must be scoped,
and the code must be fixed for release.

## Defect

`prototype/src/simulator.py`:

- line 135 (`ElevatorPool.request`):
  `slot = min(self.slots, key=lambda e: (e.available_at, id(e)))`
- line 375 (`ElevatorPoolBatched.request`):
  `elev = min(self.elevators, key=lambda e: (e.available_at, id(e)))`

The comment at line 134 states the INTENT: "ties broken by slot order
(stable)". `id(e)` is the CPython memory address, which follows allocation
order only on a clean heap; after heap churn, object ids need not be in
list order, so the argmin among availability-tied units becomes
heap-state-dependent. Ties among units standing on DIFFERENT floors then
change repositioning legs and hence makespans. (AMR selection is safe: it
keys on the explicit integer `a.id`.)

## Reproduction (2026-07-08, this machine, Python 3.12)

Wave: orders (2->4, rel 0), (2->4, rel 5), (2->6, rel 1); n_amrs = 4,
E = 3, c = 2, batched M2. In one process:

- 20 fresh `simulate_wave` calls: all return 43.0.
- allocate and free 10,000 objects, then 20 fresh calls: returns BOTH
  43.0 and 48.0 across calls.

Discovered by the B-11 addendum fidelity gate (mirror with index
tie-break vs production), which halted the E = 3 slice per its locked
rule. The B-11 main census gate (E in {1,2}) had passed 4000/4000 in its
process, i.e. production behaved index-like there.

## Impact assessment

1. Stored Phase 5 artifacts (v0_5_*) were generated in single long-running
   processes; within each run the tie policy was whatever the heap gave.
   Aggregate statistics (medians over hundreds of waves, gate verdicts)
   are robust to rare tie flips, but exact per-wave values may not
   reproduce across environments.
2. The theory is unaffected: Proposition 2 / Lemma 6 arguments are
   tie-break agnostic (any fixed tie-break among availability-tied units
   satisfies the argmin property used in the proofs).
3. `python -m src.simulator`'s hand-computed test targets pass on fresh
   interpreters (clean heap) and did not catch this.

## Fix (proposed, NOT applied to production in this revision)

Replace both keys with index-stable selection, e.g.
`min(enumerate(self.slots), key=lambda t: (t[1].available_at, t[0]))[1]`,
matching the documented intent and the AMR rule's pattern. Applying the
fix changes behavior only at heap-reordered ties, but to keep the stored
artifacts' provenance honest the fix must ship WITH a regeneration
equivalence check, registered below, not as a silent patch.

## Registered follow-up (B-14, dated 2026-07-08, execution deferred)

B-14: apply the index-stable tie-break on a branch; re-run Block C and the
Block A smoke slice under the fixed simulator; locked reporting: (i) all
pre-registered gate VERDICTS must be recomputed and reported side by side
(expectation: unchanged; any flip is reported and the manuscript uses the
fixed-simulator numbers with a dated note); (ii) the per-wave tie-incidence
rate (requests whose argmin faced an availability tie among units on
different floors) is measured and reported as the exposure statistic.
Until B-14 runs, the manuscript's reproducibility statement says:
"deterministic given the platform's allocation behavior; an index-stable
tie-break and regeneration check are registered".

## Measured exposure (2026-07-08, C-4 reconstruction check)

First quantitative exposure measurement on REAL stored data: reconstructing
all 12,000 Block C (config, arm, wave) M1/M2 values from the registered
seed streams in fresh processes reproduces M1 exactly (12,000/12,000, twice)
while M2 mismatches 30 (run 1) and 32 (run 2) of 12,000, i.e. **~0.27% of
stored Block C M2 values are tie-sensitive**, concentrated in configs 1, 7,
5 (E = 2), with per-wave differences from -100 to +38 time units, two-sided.
Corner medians over 200 waves are insensitive (the C-4 analysis proceeded
under the amended stored-artefact data policy). M1's immunity in this data
is consistent with its 4 co-located slots rarely reaching equal-availability
different-floor states at these configs, while M2's 2 batching cars reach
them regularly. This number is the prior estimate for B-14's exposure
statistic.

## Immediate handling in this revision package

The B-11 addendum's fidelity reference is redefined (dated note in the
amendment) as production-with-index-tie-break (one-line monkeypatch in the
harness only), i.e. the documented intent. The main census conclusions
stand as registered (its gate passed in-process; its harness is the
deterministic intent-conformant implementation).
