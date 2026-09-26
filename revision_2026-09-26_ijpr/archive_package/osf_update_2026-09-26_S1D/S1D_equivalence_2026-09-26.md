# S1D evidence: code change after signing and equivalence of results (2026-09-26)

Supports `amendments/AMEND-2026-09-26-S1D_execution_deviation.md`. Written by the assistant; read-only evidence.

## Code trees
- Pinned at signing (`archive_package/MANIFEST_SIGNED.json`, generated 2026-09-26T06:48:53Z): `3ef64f08b16beb4ca4f5aa1130202a8d9193c8b04d4f49038de9122c79277135`.
- Current (after the changes below): `cd0694e4fedeee112d451828d8d03adcbd36a576ecf33dbcf5988b54265dd14c`.
- The pinned tree was rebuilt in a separate git worktree at commit `c7a024a` with the post-signing checkbox fix taken out; its code-tree hash was recomputed and equals the pinned value.
- Hash definition: `registration_guard.code_tree_sha256` over `prototype/src/*.py`, CRLF read as LF.

## Files changed (7; 81 changed lines)
- `prototype/src/analysis_S1_cluster_bootstrap.py`
- `prototype/src/analysis_S1_displays.py`
- `prototype/src/experiments_S1_B4_B6.py`
- `prototype/src/experiments_S1_blockC_ext.py`
- `prototype/src/experiments_S1_enumeration.py`
- `prototype/src/experiments_S1_tiebreak_regen.py`
- `prototype/src/registration_guard.py`

No other file under `prototype/src/` differs. `simulator.py`, `features.py`, `wave_policies.py`, `phase5_config.py`, `des_evaluator.py`, and every `analysis_phase5_*` module are byte-identical (CRLF read as LF) to the pinned tree.

## Equivalence test
Method: the eleven Study 1 self-tests (`--selftest`: toy seeds from `TOY_SEED_BASE` = 424,242, far below every registered seed; output only to a scratch folder) were run once on the pinned tree and once on the current tree, with Python 3.12.10, numpy 2.1.2, pandas 2.2.3. The self-tests call the same computation functions as the real runs, on smaller toy inputs. Every JSON output was compared value by value after removing provenance fields only (keys ending in `sha256`, `_path`, `_paths`, and the three code-provenance keys, which exist only in the current outputs) and after replacing the two repository roots by one placeholder. CSV outputs were compared as text with the same root replacement; images by bytes. Commands: `s1_selftests.sh`, `compare_equivalence.py` (job scratch folder).

Self-tests: 11/11 pass on both trees. `python -m src.simulator` passes all hand-computed targets on the current tree. `python -m src.registration_guard` passes, including the new dependency cases.

Result (verbatim):
```
outputs: pinned 23, current 23, only in one: []
  image TH-2_abstraction_bias.png: identical bytes
compared: 14 JSON (provenance removed), 8 data files; images listed above: 1
NO DIFFERENCES in any compared value
```

Three JSON outputs carry no `code_tree_matches_pinned` field, by design: `v0_5_phase5_blockA_tiebreakfix.json` and `..._blockB_tiebreakfix.json` are written by the unchanged Phase 5 gate code that S1-9 runs, and the S1-9 comparison file written next to them carries the provenance; the S1-12 output (`experiments_S1_b5_rerun.py`) already recorded `code_tree_sha256` before signing and is unchanged.

## Full diff, pinned tree to current tree (`prototype/src/*.py`)
```diff
diff --git a/prototype/src/analysis_S1_cluster_bootstrap.py b/prototype/src/analysis_S1_cluster_bootstrap.py
index 0676b91..c56e09c 100644
--- a/prototype/src/analysis_S1_cluster_bootstrap.py
+++ b/prototype/src/analysis_S1_cluster_bootstrap.py	
@@ -38,6 +38,7 @@ import numpy as np
 import pandas as pd
 
 from src.analysis_phase5_blockA import CORNERS, decompose
+from src.registration_guard import code_provenance  # S1D: code-tree hash in every output
 from src.registration_guard import require_signed, scratch_dir
 
 RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
@@ -426,7 +427,7 @@ def run_real() -> dict:
 
     out = {
         "registration_sha256": _sha256_file(REG_PATH),
-        "code_sha256": _sha256_file(Path(__file__)),
+        "code_sha256": _sha256_file(Path(__file__)), **code_provenance(),
         "input_sha256": hashes,
         "selftest": False,
         "blockA": run_blockA(a),
@@ -569,7 +570,7 @@ def run_selftest(B: int) -> dict:
 
     return {
         "registration_sha256": _sha256_file(REG_PATH),
-        "code_sha256": _sha256_file(Path(__file__)),
+        "code_sha256": _sha256_file(Path(__file__)), **code_provenance(),
         "input_sha256": "n/a (selftest: fabricated in-memory, not read from disk)",
         "selftest": True,
         "reference_row_level_reproducibility_check": {"ref1": ref1, "ref2": ref2,
diff --git a/prototype/src/analysis_S1_displays.py b/prototype/src/analysis_S1_displays.py
index 795250e..7506c06 100644
--- a/prototype/src/analysis_S1_displays.py
+++ b/prototype/src/analysis_S1_displays.py	
@@ -38,6 +38,7 @@ from src.analysis_S1_cluster_bootstrap import _check_join
 from src.experiments_S1_blockC_ext import (_class_stat_dict,
                                            clustered_stability,
                                            hedge_and_minimax)
+from src.registration_guard import code_provenance  # S1D: code-tree hash in every output
 from src.registration_guard import require_signed, scratch_dir
 
 RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
@@ -489,7 +490,7 @@ def main() -> None:
     if args.cmd == "s1-7":
         input_paths.append(RESULTS_DIR / "v0_5_phase5_supp.json")
     meta = {"registration_sha256": _sha256_file(REG_PATH),
-           "code_sha256": _sha256_file(Path(__file__)),
+           "code_sha256": _sha256_file(Path(__file__)), **code_provenance(),
            "input_sha256": ({} if args.selftest else
                             {q.name: _sha256_file(q) for q in input_paths
                              if q.exists()}),
diff --git a/prototype/src/experiments_S1_B4_B6.py b/prototype/src/experiments_S1_B4_B6.py
index 44cb487..c2e262e 100644
--- a/prototype/src/experiments_S1_B4_B6.py
+++ b/prototype/src/experiments_S1_B4_B6.py	
@@ -54,6 +54,7 @@ from src.analysis_phase5_blockA import CORNERS, decompose
 from src.demand_patterns import generate_pool
 from src.experiments_phase5 import _config_fields, _seed, run_corner_block
 from src.experiments_S1_blockC_ext import blockC_style_unit
+from src.registration_guard import code_provenance  # S1D: code-tree hash in every output
 from src.registration_guard import TOY_SEED_BASE, require_signed, scratch_dir
 from src.simulator import simulate_wave
 from src.wave_policies import build_candidates, corner_positions, materialise
@@ -300,7 +301,7 @@ def main() -> None:
     out_dir = scratch_dir() if args.selftest else RESULTS_DIR
     meta = {"registration_sha256": _sha256_file(REG_PATH),
            "b4_b6_design_sha256": _sha256_file(B4_DESIGN_PATH),
-           "code_sha256": _sha256_file(Path(__file__)),
+           "code_sha256": _sha256_file(Path(__file__)), **code_provenance(),
            "selftest": args.selftest}
 
     s1_4_path = out_dir / "v0_5_phase5_S1-4_B4.json"
diff --git a/prototype/src/experiments_S1_blockC_ext.py b/prototype/src/experiments_S1_blockC_ext.py
index 10c89af..db9052f 100644
--- a/prototype/src/experiments_S1_blockC_ext.py
+++ b/prototype/src/experiments_S1_blockC_ext.py	
@@ -41,6 +41,7 @@ from scipy.stats import wasserstein_distance
 from src import phase5_config as cfg
 from src.analysis_phase5_blockA import CORNERS
 from src.experiments_phase5 import run_chain_block
+from src.registration_guard import code_provenance  # S1D: code-tree hash in every output
 from src.registration_guard import TOY_SEED_BASE, require_signed, scratch_dir
 
 RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
@@ -282,7 +283,7 @@ def main() -> None:
     df.to_csv(csv_path, index=False)
 
     out = {"registration_sha256": _sha256_file(REG_PATH),
-          "code_sha256": _sha256_file(Path(__file__)),
+          "code_sha256": _sha256_file(Path(__file__)), **code_provenance(),
           "selftest": args.selftest, "n_per_arm": n_per_arm, "cand_n": cand_n,
           "stability_B": stab_B, "raw_csv": str(csv_path), **summary}
     json_path = out_dir / "v0_5_phase5_S1-3_blockC_ext.json"
diff --git a/prototype/src/experiments_S1_enumeration.py b/prototype/src/experiments_S1_enumeration.py
index de57c15..307bc89 100644
--- a/prototype/src/experiments_S1_enumeration.py
+++ b/prototype/src/experiments_S1_enumeration.py	
@@ -43,6 +43,7 @@ from src import phase5_config as cfg
 from src.analysis_phase5_blockA import CORNERS, decompose
 from src.demand_patterns import generate_pool
 from src.experiments_phase5 import MODEL_IDX, MODEL_TAG, _seed, sim_makespan
+from src.registration_guard import code_provenance  # S1D: code-tree hash in every output
 from src.registration_guard import require_checkbox
 from src.registration_guard import TOY_SEED_BASE, require_signed, scratch_dir
 from src.simulator import Wave
@@ -675,7 +676,7 @@ def main() -> None:
                    + [tier2 / "b2_b3_benchmarks.json",
                       tier2 / "amendC1_p9_spoplus.json"])
     meta = {"registration_sha256": _sha256_file(REG_PATH),
-           "code_sha256": _sha256_file(Path(__file__)),
+           "code_sha256": _sha256_file(Path(__file__)), **code_provenance(),
            "input_sha256": ({} if args.selftest else
                             {q.name: _sha256_file(q) for q in input_paths
                              if q.exists()}),
diff --git a/prototype/src/experiments_S1_tiebreak_regen.py b/prototype/src/experiments_S1_tiebreak_regen.py
index af150b4..f57cd7d 100644
--- a/prototype/src/experiments_S1_tiebreak_regen.py
+++ b/prototype/src/experiments_S1_tiebreak_regen.py	
@@ -46,6 +46,7 @@ import pandas as pd
 from src import phase5_config as cfg
 from src.experiments_phase5 import run_corner_block, run_policy_block
 from src.experiments_phase5_ablation import P7_ITER, run_p7
+from src.registration_guard import code_provenance  # S1D: code-tree hash in every output
 from src.registration_guard import TOY_SEED_BASE, require_signed, scratch_dir
 
 RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
@@ -201,7 +202,7 @@ def main() -> None:
         json.dump(regen_b, f, indent=2, default=str)
 
     meta = {"registration_sha256": _sha256_file(REG_PATH),
-           "code_sha256": _sha256_file(Path(__file__)),
+           "code_sha256": _sha256_file(Path(__file__)), **code_provenance(),
            "selftest": args.selftest,
            "csv_paths": {k: str(v) for k, v in csv_paths.items()}}
     if args.selftest:
diff --git a/prototype/src/registration_guard.py b/prototype/src/registration_guard.py
index 6330465..a806ddb 100644
--- a/prototype/src/registration_guard.py
+++ b/prototype/src/registration_guard.py	
@@ -6,7 +6,8 @@ Every Study 1 and Study 2 script calls `require_signed(<key>)` (or
 `require_bundle`) before it touches a registered seed, pool, or stored
 artefact. The guard stops unless, for each registration,
   1. its YAML front matter reads `author_signoff: "SIGNED ..."` (the S1C
-     execution note may read "ACKNOWLEDGED ..."),
+     and S1D execution notes may read "ACKNOWLEDGED ..."; every Study 1 key
+     also requires S1D, see ALSO_REQUIRES),
   2. the signed manifest (revision_2026-09-26_ijpr/archive_package/
      MANIFEST_SIGNED.json, written by make_manifest.py after signing) lists
      it with the file's current hash, and
@@ -47,11 +48,16 @@ REGISTRATIONS: Dict[str, Path] = {
            / "AMEND-2026-09-26-S1B_new_simulations.md",
     "S1C": REPO / "revision_2026-09-26_ijpr" / "amendments"
            / "AMEND-2026-09-26-S1C_execution_note_B4_B6.md",
+    "S1D": REPO / "revision_2026-09-26_ijpr" / "amendments"
+           / "AMEND-2026-09-26-S1D_execution_deviation.md",
     "decisions": REPO / "revision_2026-09-26_ijpr" / "01_DECISIONS_TO_SIGN.md",
     "story": REPO / "revision_2026-09-26_ijpr" / "STORY_CONTRACT.md",
 }
 STUDY2_L1 = ("phase6", "decisions", "story")
-ACKNOWLEDGEABLE = {"S1C"}
+ACKNOWLEDGEABLE = {"S1C", "S1D"}
+# Execution notes that every real Study 1 run also needs (S1D: the code
+# changed after signing, so no Study 1 result runs before S1D is pinned).
+ALSO_REQUIRES: Dict[str, tuple] = {"S1A": ("S1D",), "S1B": ("S1D",), "S1C": ("S1D",)}
 
 # Toy seeds for self-tests: far below every registered seed range
 # (registered bases are >= 20,260,519).
@@ -81,6 +87,18 @@ def code_tree_sha256(src_dir: Path = REPO / "prototype" / "src") -> str:
                                   for p in files).encode()).hexdigest()
 
 
+def code_provenance(manifest_dir: Path = MANIFEST_DIR) -> dict:
+    """Code-tree hash of the code that runs, next to the hash pinned in
+    MANIFEST_SIGNED.json (S1B general rule 1; deviation note S1D)."""
+    current = code_tree_sha256()
+    pinned = None
+    mf = Path(manifest_dir) / "MANIFEST_SIGNED.json"
+    if mf.exists():
+        pinned = json.loads(mf.read_text(encoding="utf-8")).get("code_tree_sha256")
+    return {"code_tree_sha256": current, "code_tree_sha256_pinned": pinned,
+            "code_tree_matches_pinned": (current == pinned) if pinned else None}
+
+
 def _path(key_or_path) -> Path:
     return Path(REGISTRATIONS.get(key_or_path, key_or_path))
 
@@ -146,6 +164,8 @@ def require_signed(key_or_path, selftest: bool = False, label: str = "SIGNED",
     if selftest:
         return
     path = _path(key_or_path)
+    if not path.exists():
+        raise RegistrationNotSigned(f"REGISTRATION GUARD: {path.name} does not exist.")
     if not is_signed(key_or_path):
         raise RegistrationNotSigned(
             f"REGISTRATION GUARD: {path.name} is not signed "
@@ -169,6 +189,8 @@ def require_signed(key_or_path, selftest: bool = False, label: str = "SIGNED",
             "signed (a superseded manifest shows a different signed version). "
             "Edits after signing go into a dated amendment, not into the "
             "signed file.")
+    for dep in ALSO_REQUIRES.get(key_or_path, ()) if isinstance(key_or_path, str) else ():
+        require_signed(dep, selftest, label, manifest_dir)
 
 
 def require_bundle(keys: Iterable[str], selftest: bool = False,
@@ -178,9 +200,12 @@ def require_bundle(keys: Iterable[str], selftest: bool = False,
 
 
 def checkbox_ticked(key_or_path, marker: str, option: str = "yes") -> bool:
-    """True if the line containing `marker` has "[x] <option>" ticked."""
+    """True if a checkbox line containing `marker` has "[x] <option>" ticked.
+    Only lines that carry a box ("[") count, so a status line or a sentence
+    that merely mentions the marker (as the signed S1B status line does)
+    is skipped."""
     for line in _path(key_or_path).read_text(encoding="utf-8").splitlines():
-        if marker in line:
+        if marker in line and "[" in line:
             return re.search(r"\[[xX]\]\s*" + re.escape(option), line) is not None
     return False
 
@@ -302,14 +327,38 @@ def _test_parser_and_pinning(tmp: Path) -> None:
         assert stops(require_signed, p, manifest_dir=tmp)
     require_signed(pending, selftest=True)                   # self-test bypass
     box = tmp / "box.md"
-    box.write_text("S1-11 included (D-D1 signed):  [x] yes  [ ] no\n"
+    box.write_text("status: \"SIGNED; S1-11 included (D-D1 signed).\"\n"   # marker without a box: skipped
+                   "S1-11 included (D-D1 signed):  [x] yes  [ ] no\n"
                    "Other item:  [ ] yes  [x] no\n", encoding="utf-8")
     assert checkbox_ticked(box, "S1-11 included")
+    assert not checkbox_ticked(box, "S1-11 included", "no")
     assert not checkbox_ticked(box, "Other item")
     assert stops(require_checkbox, box, "Other item")
+    # a Study 1 key also needs its execution note (S1D) to be signed and pinned
+    main_reg, note = tmp / "s1x.md", tmp / "s1d.md"
+    main_reg.write_text('---\nauthor_signoff: "SIGNED (A, 2026-10-03)"\n---\n', encoding="utf-8")
+    note.write_text('---\nauthor_signoff: "PENDING"\n---\n', encoding="utf-8")
+    saved = dict(REGISTRATIONS), dict(ALSO_REQUIRES)
+    ACKNOWLEDGEABLE.add("S1X_NOTE")
+    try:
+        REGISTRATIONS.update({"S1X": main_reg, "S1X_NOTE": note})
+        ALSO_REQUIRES["S1X"] = ("S1X_NOTE",)
+        _write_manifest(tmp, "SIGNED", {main_reg: sha256_file(main_reg), note: sha256_file(note)})
+        assert stops(require_signed, "S1X", manifest_dir=tmp), "pending note must stop"
+        REGISTRATIONS["S1X_NOTE"] = tmp / "missing.md"
+        assert stops(require_signed, "S1X", manifest_dir=tmp), "missing note must stop"
+        REGISTRATIONS["S1X_NOTE"] = note
+        note.write_text('---\nauthor_signoff: "ACKNOWLEDGED (A, 2026-10-03)"\n---\n', encoding="utf-8")
+        _write_manifest(tmp, "SIGNED", {main_reg: sha256_file(main_reg), note: sha256_file(note)})
+        require_signed("S1X", manifest_dir=tmp)              # both pinned: runs
+        require_signed(main_reg, manifest_dir=tmp)            # by path: no dependency lookup
+    finally:
+        REGISTRATIONS.clear(); REGISTRATIONS.update(saved[0])
+        ALSO_REQUIRES.clear(); ALSO_REQUIRES.update(saved[1])
+        ACKNOWLEDGEABLE.discard("S1X_NOTE")
     print("  [OK] guard: front matter (quotes, comments, CRLF), pinned hash "
           "(unpinned, unchanged, edited, re-pinned, staggered signing), "
-          "self-test bypass, body checkbox")
+          "self-test bypass, body checkbox, execution-note dependency")
 
 
 def _report_current() -> None:
```
