"""G0 item 6 (protocol §12), real-mode half: every Study 2 driver stops at the guard in real mode.

Run from prototype/:  python "../revision_2026-09-26_ijpr/week4/g0_2026-09-27/g0_item6_guard_check.py"

Safety net: before any real-mode call, every function of the drivers that could draw a pool, evaluate a
candidate, or write a file is replaced by a stub that raises SafetyNet. A driver that got past its guard
would therefore stop at the stub, not run. Nothing is written to prototype/results/.

Part B checks require_l2 on temporary copies (a temporary L2 file and temporary manifests, with the real
signed L1 files pinned at their real hashes): unsigned, signed but unpinned, wrong protocol hash, empty
code hash, code differing from L2 (with and without --allow-code-change), superseded manifest with a
different signed version, and the passing case. The real L2 file and manifests are only read.
This file lives outside prototype/src, so it is not part of the code tree hash."""
import json
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "prototype"))
from src import analysis_phase6 as ap6                          # noqa: E402
from src import experiments_phase6 as ep6                       # noqa: E402
from src import registration_guard as rg                        # noqa: E402


class SafetyNet(Exception):
    pass


def _stub(name):
    def f(*a, **k):
        raise SafetyNet(f"{name} reached: the guard did not stop the driver")
    return f


RISKY_EP6 = ["order_pool", "run_decision", "run_chain", "run_case", "merge_parts", "tune_instance",
             "runtime_projection", "_write_json", "_write_rows", "build_G"]
for nm in RISKY_EP6:
    setattr(ep6, nm, _stub(f"experiments_phase6.{nm}"))
for nm in ("analyse", "_write_json"):
    if hasattr(ap6, nm):
        setattr(ap6, nm, _stub(f"analysis_phase6.{nm}"))
if hasattr(ap6, "_ep"):
    for nm in RISKY_EP6:
        setattr(ap6._ep, nm, _stub(f"analysis_phase6._ep.{nm}"))

results = {}


def expect_stop(label, fn):
    try:
        fn()
    except rg.RegistrationNotSigned as e:
        results[label] = {"stopped_at_guard": True, "message": str(e)[:160]}
        return
    except SafetyNet as e:
        results[label] = {"stopped_at_guard": False, "message": str(e)}
        return
    except SystemExit as e:
        results[label] = {"stopped_at_guard": False, "message": f"other SystemExit: {e}"[:200]}
        return
    results[label] = {"stopped_at_guard": False, "message": "returned normally"}


# Part A: the real L2 addendum is unsigned now, so every L2-guarded command must stop at the guard
for cmd in ("main", "merge", "warmstart", "runtime", "case"):
    expect_stop(f"experiments_phase6 {cmd}", lambda c=cmd: ep6.main([c]))
expect_stop("experiments_phase6 case --case-data", lambda: ep6.main(
    ["case", "--case-data", str(Path(rg.REPO) / "prototype" / "data" / "online_retail_II.xlsx")]))
expect_stop("analysis_phase6", lambda: ap6.main([]))

# Part B: require_l2 on temporary copies
l1 = {k: rg.REGISTRATIONS[k] for k in rg.STUDY2_L1}
real_l2 = rg.REGISTRATIONS["phase6_L2"]
proto_sha = rg.sha256_file(rg.REGISTRATIONS["phase6"])
tree = rg.code_tree_sha256()
part_b = {}
with tempfile.TemporaryDirectory() as td:
    tmp = Path(td)
    l2 = tmp / "l2.md"
    l1_pins = {p: rg.sha256_file(p) for p in l1.values()}

    def write_l2(signoff, proto, code):
        l2.write_text(f'---\nauthor_signoff: "{signoff}"\nprotocol_L1_sha256: "{proto}"\n'
                      f'code_tree_sha256: "{code}"\n---\nbody\n', encoding="utf-8")

    def pin(label="SIGNED_L2"):
        rg._write_manifest(tmp, "SIGNED", l1_pins)
        rg._write_manifest(tmp, label, {l2: rg.sha256_file(l2)})

    def outcome(**kw):
        try:
            ref = rg.require_l2(manifest_dir=tmp, **kw)
            return f"passes (returns {ref!r})"
        except rg.RegistrationNotSigned as e:
            return "stops: " + str(e).split(".")[0][:110]

    saved = rg.REGISTRATIONS["phase6_L2"]
    rg.REGISTRATIONS["phase6_L2"] = l2
    try:
        write_l2("PENDING", proto_sha, tree); pin()
        part_b["unsigned"] = outcome()
        write_l2("SIGNED (T, 2026-10-01)", proto_sha, tree)
        rg._write_manifest(tmp, "SIGNED", l1_pins)
        (tmp / "MANIFEST_SIGNED_L2.json").unlink(missing_ok=True)
        part_b["signed, not pinned"] = outcome()
        pin()
        part_b["signed and pinned, correct hashes"] = outcome()
        write_l2("SIGNED (T, 2026-10-01)", "0" * 64, tree); pin()
        part_b["wrong protocol_L1_sha256"] = outcome()
        write_l2("SIGNED (T, 2026-10-01)", proto_sha, ""); pin()
        part_b["empty code_tree_sha256"] = outcome()
        write_l2("SIGNED (T, 2026-10-01)", proto_sha, "f" * 64); pin()
        part_b["code differs from L2"] = outcome()
        part_b["code differs, --allow-code-change given"] = outcome(allow_code_change="EXECUTION-LOG entry 99 (test)")
        write_l2("SIGNED (T, 2026-10-01)", proto_sha, tree); pin()
        l2_after = l2.read_text(encoding="utf-8")
        l2.write_text(l2_after.replace("body", "an earlier signed version"), encoding="utf-8")
        rg._write_manifest(tmp, "SIGNED_L2_superseded_1", {l2: rg.sha256_file(l2)})
        l2.write_text(l2_after, encoding="utf-8")
        part_b["superseded manifest pins a different signed version"] = outcome()
        (tmp / "MANIFEST_SIGNED_L2_superseded_1.json").unlink()
        part_b["passing case again after removing the superseded manifest"] = outcome()
    finally:
        rg.REGISTRATIONS["phase6_L2"] = saved

expected_b = {"unsigned": "stops", "signed, not pinned": "stops", "signed and pinned, correct hashes": "passes",
              "wrong protocol_L1_sha256": "stops", "empty code_tree_sha256": "stops",
              "code differs from L2": "stops", "code differs, --allow-code-change given": "passes",
              "superseded manifest pins a different signed version": "stops",
              "passing case again after removing the superseded manifest": "passes"}
ok_a = all(v["stopped_at_guard"] for v in results.values())
ok_b = all(part_b[k].startswith(v) for k, v in expected_b.items())
out = {"part_A_real_mode_stops": results, "part_B_require_l2_cases": part_b,
       "real_L2_unchanged_sha256": rg.sha256_file(real_l2), "code_tree_sha256": tree,
       "pass": ok_a and ok_b}
Path(__file__).with_name("g0_item6_guard_check.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
for k, v in results.items():
    print(f"  [{'OK' if v['stopped_at_guard'] else 'FAIL'}] {k}: {v['message'][:100]}")
for k, v in part_b.items():
    print(f"  [{'OK' if v.startswith(expected_b[k]) else 'FAIL'}] require_l2 {k}: {v}")
print("G0 item 6 (real-mode half):", "PASS" if out["pass"] else "FAIL")
