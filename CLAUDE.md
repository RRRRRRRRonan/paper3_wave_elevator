# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is a **PhD research workspace**, not a software product. It contains the simulation code, experimental results, and manuscript for **Paper 3** (working title "Wave Release Coordination under Vertical Resource Constraints in Multi-Story AMR Warehouses"; title candidates in `revision_2026-09-26_ijpr/STORY_CONTRACT.md` §2). Since 2026-09-26 the target is the *International Journal of Production Research* (IJPR) as a **decision-aid paper** with two studies, with *Computers & Industrial Engineering* as the fallback. The deliverable is a paper; the code exists to produce the figures and tables that the paper's claims rest on.

Two consequences shape almost every task here:
- **Scientific integrity is a first-class constraint.** The publication-scale experiment is **pre-registered** (`paper_draft/phase5_scaleup_preregistration.md`, locked and author-signed 2026-05-19). Do not change locked parameters, gates, or verdicts after sign-off; do not add a competitive baseline after seeing results; do not retune to clear a gate. These are "p-hacking" moves the project explicitly forbids. New analyses enter as clearly-labelled pre-registered *amendments*, before results are seen.
- **Study 1 versus Study 2.** Study 1 = the Phase 5 preregistered diagnostics plus registered re-analyses (`revision_2026-09-26_ijpr/amendments/`). Study 2 = the Phase 6 method study (`paper_draft/phase6_method_study_protocol.md`). Registration documents are drafts until their frontmatter reads `author_signoff: "SIGNED ..."`; the Study 1 re-analysis and Study 2 drivers call `src/registration_guard.py` and refuse to run before sign-off or after any edit of the signed bytes (hashes pinned in `revision_2026-09-26_ijpr/archive_package/MANIFEST_SIGNED.json`; Study 2 test pools also need the signed L2 addendum `paper_draft/phase6_protocol_L2_addendum.md`). **As of 2026-09-26 the six L1 registrations are SIGNED and pinned: never edit them (write a dated amendment instead), and never invoke a Study 1 script or `experiments_phase6` without `--selftest` unless the author has asked for that run, because they now execute for real and write into `prototype/results/`.** Never generate Study 2 test-pool seeds or run Study 2 on test pools before the protocol is signed; code tests use hand-built instances or explicitly non-registered toy seeds and write only to scratch directories. Since 2026-09-27 the Stage L2 addendum is also SIGNED (pinned in `MANIFEST_SIGNED_L2.json`; P11 weights, case parameters, code tree); Study 2 test pools are generated only after its OSF update of kps2c is registered and only when the author asks for the Study 2 run, and any change to `prototype/src/` after that needs a logged `--allow-code-change` reference.
- **The work spans several scales.** A small **prototype scale** (the older 6-cell `E∈{1,2,3}×c2` regime grid, "M4/M5" naming, Phase 4 v2), the **publication scale** (the Phase 5 18-config grid, 106,800 model evaluations), the **Study 2 scale** (`v0_6_phase6_*`), and the **calibrated case** (`v0_6_case_*`, config_id ≥ 100). Never present numbers from different scales side by side without labelling which is which — this is a recurring correctness hazard.

## Layout

- `revision_2026-09-02/MASTER_REVISION_BY_SECTION.md` — **the single active manuscript revision-control entry**. Start here for all manuscript work. Since 2026-09-26 its §00 (IJPR v2 overlay) supersedes the old title, contribution, and research-question rulings; §0.2 audit facts, §0.3 evidence tags, and §2.4 forbidden phrases stay in force.
- `revision_2026-09-26_ijpr/` — IJPR working folder: `00_REVIEW_GUIDE.md`, `01_DECISIONS_TO_SIGN.md`, `STORY_CONTRACT.md` (the only valid contribution and RQ wording), `EXECUTION-LOG.md`, Study 1 registrations in `amendments/`, the OSF archive package, backups of files edited on 2026-09-26, and `to_sign_copies/` (read-only copies of the files to sign, for reading only; signatures go on the originals, which are the only files the guard reads). The full IJPR plan and its evidence are in `revision_2026-09-24/readiness_assessment_CIE_IJPR_2026-09-26.md` (Part 2 v2).
- `prototype/src/` — all Python: the simulator, features, policies, and the `experiments_*.py` / `analysis_*.py` scripts.
- `prototype/results/` — JSON result artefacts (`v0_5_phase5_*.json` are the publication-scale ones) and `results/figures/` PNGs.
- Current manuscript sources: §3 is `Problem formulation.docx` (root; bilingual mirror `revision_2026-09-24/section3_bilingual_2026-09-24.md`), §4 is `revision_2026-09-02/SECTION_4_METHODOLOGY.md` and `Methodology.docx` (root), and the Abstract, §1, and §2 bases are in `paper_draft/manuscript/`; the root `Wave Release Coordination ... Multi.docx` is kept only for retrieving still-valid details (master §1.1).
- `paper_draft/` — references, registrations, and frozen protocol materials:
  - `paper_draft/manuscript/` — the sentence-level bases for the Abstract, §1, and §2 (`*_v1.1*`), the §4/§5 v0.1 drafts (structure only, master §1.3), and both `.bib` files.
  - `paper_draft/` root keeps: `TERMINOLOGY.md`, the frozen `phase5_scaleup_preregistration.md`, the Study 2 registration `phase6_method_study_protocol.md` with `phase6_protocol_L2_addendum.md`, `heft_additions_v0_1.md`, and `theorems_m4.md` / `theorems_m5.md` / `methodology_v0_2.md` — the last three are prototype-era but MUST stay in place because the frozen pre-registration links to them by relative path. For the same reason `prototype/intuitions_before_MVS_v0_2.md` and the two files it links (`prototype/intuitions_before_MVS.md`, `prototype/MVS_v0_2_plan.md`) stay in `prototype/`.
- `revision_2026-07-08/` — the signed 2026-07-08 revision deliverable (W1-W10 manuscript layer, six signed amendments, tables T1-T6, figures fig1-fig10, EXECUTION-LOG). Audit trail; keep intact, do not move files out of it.
- `papers/` — cited PDFs and their reading logs.
- `research_notes/` — contribution-positioning documents (`contribution_review_continuation_2026-09-02.md`, as incorporated into the active master, is the latest contribution ruling), the reading-log index, the real-data assessment, and the plain-language background note `问题背景通俗解读.md`.
- `sources/` — the frontier literature audit and the reference checks cited by the master.
- Root `archive/` — **the single place for superseded material**: store, never use as a current source, never quote numbers from it. It holds the revision snapshots (`revisions/`), superseded root files (`superseded/`), the former `paper_draft/archive/` including the prototype-scale phase4 pre-registration (`paper_draft/`), superseded manuscript versions and `00_INDEX.md` (`paper_draft/manuscript/`), early research notes (`research_notes/`), prototype-era planning notes (`prototype/`), Codex review snapshots (`codex_review/`), GPT language-editing products (`gpt_2026-08/`), the superseded Section 3 md and the old Fig. 1 design (`revision_2026-09-02/`), and the Section 3 finalization working files (`revision_2026-09-24/`). Index: `archive/MANIFEST.md`; move log with hashes for the 2026-09-26 clean-up: `archive/CLEANUP_2026-09-26_moves.json`. Put newly superseded files there, not into new per-folder archives.

## Commands

Python deps: `pip install -r prototype/requirements.txt` (numpy, pandas, scikit-learn, matplotlib, seaborn).

**All scripts run as modules from the `prototype/` directory** (imports are absolute, e.g. `from src.simulator import simulate_wave`). Running a file by path will fail the imports.

```bash
cd prototype

# Run the simulator's built-in test/sanity suite (hand-computed makespan targets,
# regime monotonicity, batching semantics, pop_cluster, gap-fix backward-compat):
python -m src.simulator

# Most modules have a self-test / smoke under __main__ — run one directly:
python -m src.features
python -m src.wave_policies

# Phase 5 experiment driver takes a mode argument (default "smoke"):
python -m src.experiments_phase5 smoke   # ~1/60-scale gate run
python -m src.experiments_phase5 full    # full publication-scale grid (long)

# Experiment -> analysis is a two-step pipeline: experiments_*.py writes a
# results/*.json, then the matching analysis_*.py reads it and emits a verdict JSON.
python -m src.experiments_phase5_supp
python -m src.analysis_phase5_supp

# Regenerate the methodology schematic figures:
python -m src.figure_methodology_schematics
```

There is **no pytest suite, linter, or build step.** "Tests" are the `_test_*` / `_sanity_check` functions invoked under each module's `if __name__ == "__main__"`. To check a single behavior, call its function in a one-off `python -c` or temporarily narrow the `__main__` block — but the canonical correctness gate is `python -m src.simulator` passing all hand-computed targets.

## Core architecture

**Two-layer decision problem (the paper's central object).** A warehouse management system makes a *tactical* decision — **wave composition**, i.e. which orders to release together and in which processing sequence (the fixed FIFO dispatch rule processes orders in release sequence) — and a *fleet scheduler* makes the *operational* decision of dispatching AMRs that must contend for shared freight elevators (the focal vertical constraint). Paper 3 studies the **tactical** layer and deliberately **holds the dispatch rule fixed**. (Any future RL/AI-agent work belongs in the operational layer as a *separate* paper — see `memory` and `paper_draft/heft_additions_v0_1.md`; it must not be bolted into this manuscript.)

**The simulator (`src/simulator.py`) is a closed-form, sequential time-accumulator, NOT an event-driven concurrent model.** `simulate_wave(...)` walks the wave's orders one at a time, assigning each to the earliest-free AMR and accumulating a 5-phase elevator-trip cost (wait → reposition → load 2s → travel → unload 2s). It returns a scalar makespan. There is **no `step`/`reset`/`observation`/`reward` API** — an RL environment would be a from-scratch rewrite, not an adaptation. Determinism: same inputs → same makespan, so unit tests assert exact hand-computed values.

**The three elevator models are the heart of the paper's robustness story:**
- `ElevatorPool` — **M1, throughput abstraction**: capacity `c` modelled as `c` parallel slots; the bottleneck-relief effect without real batching (`batched=False`).
- `ElevatorPoolBatched` — **M2, true co-occupancy batching**: a request matching an in-progress trip's `(src, dst)` boards it within the loading window (`batched=True`).
- `ElevatorPoolStochasticBatched` — **M3**: M2 with lognormal per-phase noise (`stochastic_sigma>0`, requires an `rng`).
- Plus extension models for appendix robustness studies: `ElevatorPoolDirectional` (direction-switch penalty), `ElevatorPoolBatchedHeterogeneous` (mixed per-elevator capacities). These reproduce the baseline exactly at their zero/identity parameter settings (verified by `_test_backward_compat`).

`simulate_wave`'s flags (`batched`, `stochastic_sigma`, `directional`, `heterogeneous_capacities`, `service_sigma`, `policy`) select among these; several combinations are mutually exclusive and raise `ValueError`. Defaults reproduce the v0.2 baseline.

**The feature representation Φ = (C, I, T)** (`src/features.py`): endpoint dispersion `C` (Shannon entropy over the endpoint floor distribution — *high C = floors spread out*, note the direction; plain prose "vertical spread"), directional imbalance `I`, ready-time dispersion `T` (CV of per-order ready-time offsets; **0 unless a wave is generated with staggered `release_time`s**; not used in the corner classes). Φ is positioned as a *structured decomposition*, **not** a predictive surrogate — that predictive claim was tested and retired. Do not reintroduce "Φ predicts makespan" language.

**Contributions (IJPR version; wording only from `revision_2026-09-26_ijpr/STORY_CONTRACT.md` §3):**
- **C1 problem and benchmark** — single-wave candidate selection under shared elevators with a fixed dispatch rule.
- **C2 elevator-model risk** — the conditional sample-path ordering M1 ≤ M2 (Theorem 1 of the manuscript since 2026-09-27, after the author's verification of Appendix A; still Proposition 3 in `SECTION_4_METHODOLOGY.md` and in the signed registrations), its two reversal channels (batch overtaking, adverse repositioning), the abstraction bias, and the resulting conservative screening. The **Hedge Rule** (minimax class selection collapses to the M2-best class when class medians are ordered) is a corollary. DRO is a one-sentence remark; `U_c` is a one-sentence boundary (valid 5/6, informative 0/6), never a worst-case guarantee.
- **C3 generate, screen, and verify (GSV) release procedure** — Study 2's method, evaluated along the fidelity ladder M1 → M2 → DES.
- **Bound-and-Gap** (`GAP = H_up + M_Φ`) is a *partition-relative* diagnostic: `H_up` is upper-tail headroom (not capacity-side; P9 beats the corner oracle in 7/12 cells), `M_Φ` is the class-selection miss. Its H_up share reads about 72% under the preregistered Φ rule and about 47% under the covering partition, with test–retest ICC ≈ 0.01; report both readings together and never call either a capacity share. The retired headline "capacity-bound > policy-bound" must not reappear.

**Wave-release policies (`src/wave_policies.py` and `revision_2026-07-08/tier2_analysis/scripts/`)** are *selection rules over a shared candidate pool* (`P0` random … `P5` Φ-corner rule, `P6` squared-error decision-tree comparator, `P7` 40-iteration local-search reference, `P8` savings-style heuristic, `P9` wave-level SPO+; Study 2 adds `P10` sequence-aware re-ordering and `P11` co-ride-aware constructive generator in `src/phase6_policies.py`, and the event-driven evaluator in `src/des_evaluator.py`). Keeping every policy on one candidate pool is what makes the contest fair (pre-reg §3.4). Operational dispatch within a wave is a separate `policy="fifo"|"cluster"` flag on `simulate_wave`; `fifo` is the fixed rule, `cluster` is the Supp-1 boundary check.

**Experiment → results → analysis pipeline.** `experiments_*.py` scripts simulate and dump a `results/*.json`; the matching `analysis_*.py` reads that JSON and computes gates/verdicts into another JSON. `phase5_config.py` holds every tunable knob and regenerates the 18-config grid via `make_config_array()` (a 1/3 fraction of the 3×3×2×3 factorial, `demand = (F+|A|) mod 3` crossed with both `E` levels — so **F is confounded with |A| and demand; no clean F main-effect is identifiable from this grid**).

## Naming / scale conventions to respect

- **Canonical terminology note: `paper_draft/TERMINOLOGY.md`** is the single source of truth for all naming (contribution labels, M1/M2/M3 and DES, the Φ axes, GAP/H_up/M_Φ, release policy versus dispatch rule, Study 2 terms, scale labels, the no-em-dash and Chinese-symbol-free writing rules, and a pre-finalize checklist). Consult it before writing manuscript prose; update it when a naming decision is made. Forbidden phrases: master §2.4 plus STORY_CONTRACT.md §7.
- Old → current: `M4` → Bound-and-Gap, `M5` → Hedge Rule, `M1/M2` → throughput-abstraction / true-batching, "chain dominance" → evaluator ordering, "temporal clustering" → ready-time dispersion. Prototype docs use the old names; the manuscript uses the new ones.
- `prototype/results/v0_5_phase5_*.json` = publication scale. Earlier `v0_2_*` artefacts = prototype scale. `v0_6_phase6_*` = Study 2; `v0_6_case_*` = calibrated case; re-analyses and extensions of Study 1 write `v0_5_phase5_S1-<item>_*` files (S1-9 writes `*_tiebreakfix`) and never overwrite the stored Phase 5 files.
- The pre-registration document is frozen. Treat `paper_draft/phase5_scaleup_preregistration.md` as read-only unless explicitly adding a dated, pre-results amendment; since 2026-09-26 new registrations are separate files (see `revision_2026-09-26_ijpr/amendments/` and `paper_draft/phase6_method_study_protocol.md`).
