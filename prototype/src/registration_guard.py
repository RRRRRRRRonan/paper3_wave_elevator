"""
Registration guard (2026-09-26): refuse to run a registered analysis before
its registrations are signed, and whenever their signed bytes have changed.

Every Study 1 and Study 2 script calls `require_signed(<key>)` (or
`require_bundle`) before it touches a registered seed, pool, or stored
artefact. The guard stops unless, for each registration,
  1. its YAML front matter reads `author_signoff: "SIGNED ..."` (the S1C
     and S1D execution notes may read "ACKNOWLEDGED ..."; every Study 1 key
     also requires S1D, see ALSO_REQUIRES),
  2. the signed manifest (revision_2026-09-26_ijpr/archive_package/
     MANIFEST_SIGNED.json, written by make_manifest.py after signing) lists
     it with the file's current hash, and
  3. no superseded signed manifest lists a different hash for a version
     that was already signed (an edit after signing cannot be re-pinned).
Study 2 runs on test pools also need the Stage L2 addendum to be signed and
pinned in MANIFEST_SIGNED_L2.json, to name the protocol's L1 hash, and to name
the code tree hash of the code that runs (`require_l2`); a code change after
L2 needs an explicit, logged override.

Hashes are taken over line-ending-normalized bytes (CRLF read as LF), so a
checkout with other line endings gives the same values.

Self-test mode (`--selftest` in the drivers) skips the checks but must use
toy seeds (`TOY_SEED_BASE`) and write only to the scratch directory
(`scratch_dir()`), never to prototype/results.

Run the guard's own tests with:  python -m src.registration_guard
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path
from typing import Dict, Iterable, Optional

REPO = Path(__file__).resolve().parents[2]
MANIFEST_DIR = REPO / "revision_2026-09-26_ijpr" / "archive_package"

REGISTRATIONS: Dict[str, Path] = {
    "phase6": REPO / "paper_draft" / "phase6_method_study_protocol.md",
    "phase6_L2": REPO / "paper_draft" / "phase6_protocol_L2_addendum.md",
    "S1A": REPO / "revision_2026-09-26_ijpr" / "amendments"
           / "AMEND-2026-09-26-S1A_reanalyses.md",
    "S1B": REPO / "revision_2026-09-26_ijpr" / "amendments"
           / "AMEND-2026-09-26-S1B_new_simulations.md",
    "S1C": REPO / "revision_2026-09-26_ijpr" / "amendments"
           / "AMEND-2026-09-26-S1C_execution_note_B4_B6.md",
    "S1D": REPO / "revision_2026-09-26_ijpr" / "amendments"
           / "AMEND-2026-09-26-S1D_execution_deviation.md",
    "decisions": REPO / "revision_2026-09-26_ijpr" / "01_DECISIONS_TO_SIGN.md",
    "story": REPO / "revision_2026-09-26_ijpr" / "STORY_CONTRACT.md",
}
STUDY2_L1 = ("phase6", "decisions", "story")
ACKNOWLEDGEABLE = {"S1C", "S1D"}
# Execution notes that every real Study 1 run also needs (S1D: the code
# changed after signing, so no Study 1 result runs before S1D is pinned).
ALSO_REQUIRES: Dict[str, tuple] = {"S1A": ("S1D",), "S1B": ("S1D",), "S1C": ("S1D",)}

# Toy seeds for self-tests: far below every registered seed range
# (registered bases are >= 20,260,519).
TOY_SEED_BASE = 424_242


class RegistrationNotSigned(SystemExit):
    """Raised (as a SystemExit) when a registration check fails."""


def sha256_file(path: Path) -> str:
    """SHA-256 of the file's bytes with CRLF normalized to LF."""
    return hashlib.sha256(Path(path).read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def rel_to_repo(path: Path) -> str:
    try:
        return Path(path).resolve().relative_to(REPO).as_posix()
    except ValueError:
        return Path(path).as_posix()


def code_tree_sha256(src_dir: Path = REPO / "prototype" / "src") -> str:
    """The one code-tree hash used everywhere (outputs, L2, manifests)."""
    files = sorted(Path(src_dir).glob("*.py"), key=lambda p: p.name)
    return hashlib.sha256("".join(f"{rel_to_repo(p)}\n{sha256_file(p)}\n"
                                  for p in files).encode()).hexdigest()


def code_provenance(manifest_dir: Path = MANIFEST_DIR) -> dict:
    """Code-tree hash of the code that runs, next to the hash pinned in
    MANIFEST_SIGNED.json (S1B general rule 1; deviation note S1D)."""
    current = code_tree_sha256()
    pinned = None
    mf = Path(manifest_dir) / "MANIFEST_SIGNED.json"
    if mf.exists():
        pinned = json.loads(mf.read_text(encoding="utf-8")).get("code_tree_sha256")
    return {"code_tree_sha256": current, "code_tree_sha256_pinned": pinned,
            "code_tree_matches_pinned": (current == pinned) if pinned else None}


def _path(key_or_path) -> Path:
    return Path(REGISTRATIONS.get(key_or_path, key_or_path))


def front_matter_field(path: Path, field: str) -> str:
    """A YAML front-matter field as a plain string ('' if absent); a trailing
    '# comment' is ignored."""
    text = Path(path).read_text(encoding="utf-8")
    m = re.match(r"^---\s*\r?\n(.*?)\r?\n---\s*\r?\n", text, flags=re.S)
    if not m:
        return ""
    for line in m.group(1).splitlines():
        if line.startswith(f"{field}:"):
            v = line.split(":", 1)[1].strip()
            if v[:1] in ('"', "'"):
                q = v[0]
                end = v.find(q, 1)
                return v[1:end] if end > 0 else v[1:]
            return v.split(" #", 1)[0].strip()
    return ""


def signoff_status(key_or_path) -> str:
    return front_matter_field(_path(key_or_path), "author_signoff")


def is_signed(key_or_path) -> bool:
    s = signoff_status(key_or_path).upper()
    return s.startswith("SIGNED") or (key_or_path in ACKNOWLEDGEABLE
                                       and s.startswith("ACKNOWLEDGED"))


def _manifest(label: str, manifest_dir: Path) -> Optional[dict]:
    m = Path(manifest_dir) / f"MANIFEST_{label}.json"
    return json.loads(m.read_text(encoding="utf-8")) if m.exists() else None


def pinned_sha256(path: Path, label: str = "SIGNED",
                  manifest_dir: Path = MANIFEST_DIR) -> Optional[str]:
    """SHA-256 recorded for `path` in MANIFEST_<label>.json (None if absent)."""
    data = _manifest(label, manifest_dir)
    entry = (data or {}).get("files", {}).get(rel_to_repo(path))
    return entry["sha256"] if entry else None


def repinned_after_signing(path: Path, label: str = "SIGNED",
                           manifest_dir: Path = MANIFEST_DIR) -> bool:
    """True if a superseded signed manifest recorded a SIGNED version of this
    file with a hash different from the current pin."""
    current = pinned_sha256(path, label, manifest_dir)
    for old in sorted(Path(manifest_dir).glob(f"MANIFEST_{label}_superseded_*.json")):
        entry = json.loads(old.read_text(encoding="utf-8")).get("files", {}).get(
            rel_to_repo(path))
        if (entry and str(entry.get("signoff", "")).upper().startswith(("SIGNED", "ACKNOWLEDGED"))
                and entry["sha256"] != current):
            return True
    return False


def require_signed(key_or_path, selftest: bool = False, label: str = "SIGNED",
                   manifest_dir: Path = MANIFEST_DIR) -> None:
    """Stop unless the registration is signed and unchanged since signing."""
    if selftest:
        return
    path = _path(key_or_path)
    if not path.exists():
        raise RegistrationNotSigned(f"REGISTRATION GUARD: {path.name} does not exist.")
    if not is_signed(key_or_path):
        raise RegistrationNotSigned(
            f"REGISTRATION GUARD: {path.name} is not signed "
            f"(author_signoff = {signoff_status(path)!r}). Registered analyses "
            "may run only after sign-off. Use --selftest for a toy run into "
            "the scratch directory.")
    pinned = pinned_sha256(path, label, manifest_dir)
    if pinned is None:
        raise RegistrationNotSigned(
            f"REGISTRATION GUARD: {path.name} is signed but not pinned in "
            f"MANIFEST_{label}.json. Run revision_2026-09-26_ijpr/"
            f"archive_package/make_manifest.py {label} after signing.")
    if sha256_file(path) != pinned:
        raise RegistrationNotSigned(
            f"REGISTRATION GUARD: {path.name} changed after signing (its "
            f"SHA-256 differs from MANIFEST_{label}.json). Restore the signed "
            "version or register a dated amendment in a new file.")
    if repinned_after_signing(path, label, manifest_dir):
        raise RegistrationNotSigned(
            f"REGISTRATION GUARD: {path.name} was re-pinned after it had been "
            "signed (a superseded manifest shows a different signed version). "
            "Edits after signing go into a dated amendment, not into the "
            "signed file.")
    for dep in ALSO_REQUIRES.get(key_or_path, ()) if isinstance(key_or_path, str) else ():
        require_signed(dep, selftest, label, manifest_dir)


def require_bundle(keys: Iterable[str], selftest: bool = False,
                   manifest_dir: Path = MANIFEST_DIR) -> None:
    for k in keys:
        require_signed(k, selftest, manifest_dir=manifest_dir)


def checkbox_ticked(key_or_path, marker: str, option: str = "yes") -> bool:
    """True if a checkbox line containing `marker` has "[x] <option>" ticked.
    Only lines that carry a box ("[") count, so a status line or a sentence
    that merely mentions the marker (as the signed S1B status line does)
    is skipped."""
    for line in _path(key_or_path).read_text(encoding="utf-8").splitlines():
        if marker in line and "[" in line:
            return re.search(r"\[[xX]\]\s*" + re.escape(option), line) is not None
    return False


def require_checkbox(key_or_path, marker: str, option: str = "yes",
                     selftest: bool = False) -> None:
    """Stop unless a body checkbox of a registration is ticked (e.g. the
    'S1-11 included (D-D1 signed)' line of AMEND-2026-09-26-S1B)."""
    if selftest:
        return
    if not checkbox_ticked(key_or_path, marker, option):
        raise RegistrationNotSigned(
            f"REGISTRATION GUARD: the checkbox {marker!r} is not ticked "
            f"'[x] {option}' in {_path(key_or_path).name}.")


def require_l2(selftest: bool = False, manifest_dir: Path = MANIFEST_DIR,
               allow_code_change: Optional[str] = None,
               src_dir: Path = REPO / "prototype" / "src") -> Optional[str]:
    """Stop unless L1 (protocol, decisions, story), the L2 addendum, the L1
    hash named in L2, and the code tree hash named in L2 all check out.

    A code change after L2 stops the run unless `allow_code_change` gives a
    reference to a dated deviation-log entry; the reference is returned so
    that the caller records it in every output."""
    if selftest:
        return None
    require_bundle(STUDY2_L1, manifest_dir=manifest_dir)
    require_signed("phase6_L2", label="SIGNED_L2", manifest_dir=manifest_dir)
    l2 = REGISTRATIONS["phase6_L2"]
    if front_matter_field(l2, "protocol_L1_sha256") != sha256_file(REGISTRATIONS["phase6"]):
        raise RegistrationNotSigned(
            "REGISTRATION GUARD: the L2 addendum's protocol_L1_sha256 does not "
            "match the signed protocol. No test pool may be generated.")
    named = front_matter_field(l2, "code_tree_sha256")
    if not named:
        raise RegistrationNotSigned("REGISTRATION GUARD: code_tree_sha256 is "
                                    "empty in the L2 addendum.")
    if named != code_tree_sha256(src_dir) and not allow_code_change:
        raise RegistrationNotSigned(
            "REGISTRATION GUARD: the code differs from the code frozen in L2. "
            "Log the change in EXECUTION-LOG.md and rerun with "
            "--allow-code-change '<log entry reference>'.")
    return allow_code_change


def scratch_dir() -> Path:
    """Output directory for self-test runs (never prototype/results)."""
    d = Path(os.environ.get("PAPER3_SCRATCH",
                            REPO / "prototype" / "scratch_selftest"))
    d.mkdir(parents=True, exist_ok=True)
    return d


# --------------------------------------------------------------------------
# Self-tests
# --------------------------------------------------------------------------

def _write_manifest(dir_: Path, label: str, files: Dict[Path, str],
                    signoff: str = "SIGNED (T, 2026-10-01)") -> None:
    rel = {rel_to_repo(p): {"sha256": h, "signoff": signoff}
           for p, h in files.items()}
    (dir_ / f"MANIFEST_{label}.json").write_text(json.dumps({"files": rel}),
                                                 encoding="utf-8")


def _test_parser_and_pinning(tmp: Path) -> None:
    signed = tmp / "signed.md"
    signed.write_text('---\ntitle: "x"\nauthor_signoff: "SIGNED (A, 2026-10-01)"\n'
                      "p11_weights: 2, 1, 0.5   # a comment\n---\nbody\n",
                      encoding="utf-8")
    pending = tmp / "pending.md"
    pending.write_text('---\ntitle: "x"\nauthor_signoff: "PENDING"\n---\n'
                       "author_signoff: SIGNED (in the body, must be ignored)\n",
                       encoding="utf-8")
    nofm = tmp / "nofm.md"
    nofm.write_text("author_signoff: SIGNED\n", encoding="utf-8")
    assert is_signed(signed)
    assert front_matter_field(signed, "p11_weights") == "2, 1, 0.5"
    assert not is_signed(pending), "body text must not count as front matter"
    assert not is_signed(nofm), "a file without front matter is never signed"
    lf_bytes = signed.read_bytes().replace(b"\r\n", b"\n")
    lf, crlf = tmp / "lf.md", tmp / "crlf.md"
    lf.write_bytes(lf_bytes)
    crlf.write_bytes(lf_bytes.replace(b"\n", b"\r\n"))
    assert sha256_file(crlf) == sha256_file(lf) == sha256_file(signed), \
        "hash must ignore CRLF"
    assert front_matter_field(crlf, "author_signoff").startswith("SIGNED")

    def stops(fn, *a, **k):
        try:
            fn(*a, **k)
        except RegistrationNotSigned:
            return True
        return False

    assert stops(require_signed, signed, manifest_dir=tmp), "unpinned must stop"
    _write_manifest(tmp, "SIGNED", {signed: sha256_file(signed)})
    require_signed(signed, manifest_dir=tmp)                 # pinned and unchanged
    original = signed.read_text(encoding="utf-8")
    signed.write_text(original + "edit\n", encoding="utf-8")
    assert stops(require_signed, signed, manifest_dir=tmp), "edit must stop"
    # re-pinning the edit: the old signed manifest is superseded -> still stops
    (tmp / "MANIFEST_SIGNED.json").rename(tmp / "MANIFEST_SIGNED_superseded_1.json")
    _write_manifest(tmp, "SIGNED", {signed: sha256_file(signed)})
    assert stops(require_signed, signed, manifest_dir=tmp), "re-pin must stop"
    # a file that was PENDING in the superseded manifest may be signed later
    later = tmp / "later.md"
    later.write_text('---\nauthor_signoff: "PENDING"\n---\n', encoding="utf-8")
    old = json.loads((tmp / "MANIFEST_SIGNED_superseded_1.json").read_text())
    old["files"][rel_to_repo(later)] = {"sha256": sha256_file(later),
                                        "signoff": "PENDING"}
    (tmp / "MANIFEST_SIGNED_superseded_1.json").write_text(json.dumps(old))
    later.write_text('---\nauthor_signoff: "SIGNED (A, 2026-10-02)"\n---\n',
                     encoding="utf-8")
    _write_manifest(tmp, "SIGNED", {later: sha256_file(later)})
    require_signed(later, manifest_dir=tmp)                  # staggered signing ok
    for p in (pending, nofm):
        assert stops(require_signed, p, manifest_dir=tmp)
    require_signed(pending, selftest=True)                   # self-test bypass
    box = tmp / "box.md"
    box.write_text("status: \"SIGNED; S1-11 included (D-D1 signed).\"\n"   # marker without a box: skipped
                   "S1-11 included (D-D1 signed):  [x] yes  [ ] no\n"
                   "Other item:  [ ] yes  [x] no\n", encoding="utf-8")
    assert checkbox_ticked(box, "S1-11 included")
    assert not checkbox_ticked(box, "S1-11 included", "no")
    assert not checkbox_ticked(box, "Other item")
    assert stops(require_checkbox, box, "Other item")
    # a Study 1 key also needs its execution note (S1D) to be signed and pinned
    main_reg, note = tmp / "s1x.md", tmp / "s1d.md"
    main_reg.write_text('---\nauthor_signoff: "SIGNED (A, 2026-10-03)"\n---\n', encoding="utf-8")
    note.write_text('---\nauthor_signoff: "PENDING"\n---\n', encoding="utf-8")
    saved = dict(REGISTRATIONS), dict(ALSO_REQUIRES)
    ACKNOWLEDGEABLE.add("S1X_NOTE")
    try:
        REGISTRATIONS.update({"S1X": main_reg, "S1X_NOTE": note})
        ALSO_REQUIRES["S1X"] = ("S1X_NOTE",)
        _write_manifest(tmp, "SIGNED", {main_reg: sha256_file(main_reg), note: sha256_file(note)})
        assert stops(require_signed, "S1X", manifest_dir=tmp), "pending note must stop"
        REGISTRATIONS["S1X_NOTE"] = tmp / "missing.md"
        assert stops(require_signed, "S1X", manifest_dir=tmp), "missing note must stop"
        REGISTRATIONS["S1X_NOTE"] = note
        note.write_text('---\nauthor_signoff: "ACKNOWLEDGED (A, 2026-10-03)"\n---\n', encoding="utf-8")
        _write_manifest(tmp, "SIGNED", {main_reg: sha256_file(main_reg), note: sha256_file(note)})
        require_signed("S1X", manifest_dir=tmp)              # both pinned: runs
        require_signed(main_reg, manifest_dir=tmp)            # by path: no dependency lookup
    finally:
        REGISTRATIONS.clear(); REGISTRATIONS.update(saved[0])
        ALSO_REQUIRES.clear(); ALSO_REQUIRES.update(saved[1])
        ACKNOWLEDGEABLE.discard("S1X_NOTE")
    print("  [OK] guard: front matter (quotes, comments, CRLF), pinned hash "
          "(unpinned, unchanged, edited, re-pinned, staggered signing), "
          "self-test bypass, body checkbox, execution-note dependency")


def _report_current() -> None:
    for key, path in REGISTRATIONS.items():
        if not path.exists():
            print(f"  {key:9s} {path.name}: (file missing)")
            continue
        pin = pinned_sha256(path, "SIGNED_L2" if key == "phase6_L2" else "SIGNED")
        print(f"  {key:9s} {path.name}: author_signoff = {signoff_status(key)!r}; "
              f"pinned = {'yes' if pin else 'no'}")
    print(f"  code tree: {code_tree_sha256()[:16]}")


if __name__ == "__main__":
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        _test_parser_and_pinning(Path(td))
    print("Current registration state:")
    _report_current()
