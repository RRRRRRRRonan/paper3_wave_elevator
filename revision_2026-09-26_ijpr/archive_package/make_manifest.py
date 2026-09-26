"""
Hash manifest for the 2026-09-26 registration package (IJPR revision).

Computes SHA-256, size, and modification time for every registration
document, the frozen Phase 5 materials, the stored Phase 5 artefacts that the
Study 1 re-analyses read, and the prototype source tree; records the git HEAD
and each file's git state. Writes MANIFEST_<label>.json and MANIFEST_<label>.md
next to this script. Standard library only; reads files, never modifies them.

Usage (from the repository root or anywhere):
    python "revision_2026-09-26_ijpr/archive_package/make_manifest.py" DRAFT
    python "revision_2026-09-26_ijpr/archive_package/make_manifest.py" SIGNED
    python "revision_2026-09-26_ijpr/archive_package/make_manifest.py" SIGNED_L2

SIGNED is written once, after the author has signed the L1 registrations; it
pins the bytes that src/registration_guard.py checks before any registered
run. SIGNED_L2 is written once, after the Stage L2 addendum is signed. A signed
manifest is never overwritten silently: re-running a SIGNED* label stops unless
--supersede is given, in which case the previous manifest is kept under a
timestamped name so the re-pinning stays visible. Upload the signed manifests
with the package (decision D-J).
"""
from __future__ import annotations

import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]                      # F:/Paper 3
sys.path.insert(0, str(ROOT / "prototype"))
# one definition of the hashes for the guard, the outputs, and the manifests
from src.registration_guard import (code_tree_sha256, front_matter_field,  # noqa: E402
                                    sha256_file)

GROUPS = {
    "registrations_2026-09-26": [
        "paper_draft/phase6_method_study_protocol.md",
        "revision_2026-09-26_ijpr/amendments/AMEND-2026-09-26-S1A_reanalyses.md",
        "revision_2026-09-26_ijpr/amendments/AMEND-2026-09-26-S1B_new_simulations.md",
        "revision_2026-09-26_ijpr/amendments/AMEND-2026-09-26-S1C_execution_note_B4_B6.md",
        "revision_2026-09-26_ijpr/amendments/AMEND-2026-09-26-S1D_execution_deviation.md",
        "revision_2026-09-26_ijpr/helper_reports/S1D_equivalence_2026-09-26.md",
        "revision_2026-09-26_ijpr/amendments/README.md",
        "paper_draft/phase6_protocol_L2_addendum.md",
        "revision_2026-09-26_ijpr/01_DECISIONS_TO_SIGN.md",
        "prototype/requirements.txt",
        "revision_2026-09-26_ijpr/STORY_CONTRACT.md",
    ],
    "frozen_phase5": [
        "paper_draft/phase5_scaleup_preregistration.md",
        "paper_draft/theorems_m4.md",
        "paper_draft/theorems_m5.md",
        "paper_draft/methodology_v0_2.md",
        "prototype/results/configs_v0_5.json",
    ],
    "signed_amendments_2026-07-08": sorted(
        str(p.relative_to(ROOT)).replace("\\", "/")
        for p in (ROOT / "revision_2026-07-08" / "amendments").glob("*.md")),
    "stored_phase5_artefacts": [],      # filled below: the files pinned at signing
    "study1_outputs_2026-09-26": [],    # filled below: written by the registered run
    "code_prototype_src": sorted(
        str(p.relative_to(ROOT)).replace("\\", "/")
        for p in (ROOT / "prototype" / "src").glob("*.py")),
}

# Result files: the stored Phase 5 artefacts are the ones the first signed
# manifest (2026-09-26T06:48:53Z, pin 3ef64f08) listed under
# "stored_phase5_artefacts"; every later file matching the same patterns is an
# output of the registered Study 1 run of 2026-09-26 (or of its completion
# modules) and is listed under its own group so that the two are not confused.
_FIRST_SIGNED = HERE / "MANIFEST_SIGNED_superseded_20260926T074123Z.json"
_first_stored = (set(k for k, v in json.loads(_FIRST_SIGNED.read_text("utf-8"))["files"].items()
                     if v["group"] == "stored_phase5_artefacts")
                 if _FIRST_SIGNED.exists() else None)
for _rel in sorted(str(p.relative_to(ROOT)).replace("\\", "/")
                   for pat in ("prototype/results/v0_5_phase5_*.json",
                               "prototype/results/raw/mvs_v0_5_*.csv")
                   for p in ROOT.glob(pat)):
    if _first_stored is None or _rel in _first_stored:
        GROUPS["stored_phase5_artefacts"].append(_rel)
    else:
        GROUPS["study1_outputs_2026-09-26"].append(_rel)


def git(*args: str) -> str:
    try:
        out = subprocess.run(["git", "-C", str(ROOT), *args],
                             capture_output=True, text=True, check=False)
        return out.stdout.strip()
    except OSError:
        return ""


def git_state(rel: str) -> str:
    tracked = subprocess.run(["git", "-C", str(ROOT), "ls-files",
                              "--error-unmatch", rel],
                             capture_output=True, text=True).returncode == 0
    if not tracked:
        return "untracked"
    return "modified" if git("status", "--porcelain", "--", rel) else "clean"


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    label = args[0] if args else "DRAFT"
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    target = HERE / f"MANIFEST_{label}.json"
    if label.startswith("SIGNED") and target.exists():
        if "--supersede" not in sys.argv:
            raise SystemExit(f"{target.name} exists; a signed manifest is not "
                             "overwritten. Use --supersede to keep the old one "
                             "under a timestamped name and write a new one.")
        stamp = now.replace(":", "").replace("-", "")
        for ext in (".json", ".md"):
            old = HERE / f"MANIFEST_{label}{ext}"
            if old.exists():
                old.rename(HERE / f"MANIFEST_{label}_superseded_{stamp}{ext}")
    entries, missing = {}, []
    for group, files in GROUPS.items():
        for rel in files:
            p = ROOT / rel
            if not p.exists():
                missing.append(rel)
                continue
            st = p.stat()
            entries[rel] = {
                "group": group, "sha256": sha256_file(p), "bytes": st.st_size,
                "signoff": (front_matter_field(p, "author_signoff")
                            if p.suffix == ".md" else ""),
                "mtime_utc": dt.datetime.fromtimestamp(
                    st.st_mtime, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "git": git_state(rel),
            }
    tree = code_tree_sha256()
    manifest = {
        "label": label, "generated_utc": now,
        "git_head": git("rev-parse", "HEAD"),
        "code_tree_sha256": tree,
        "n_files": len(entries), "missing": missing, "files": entries,
    }
    out_json = HERE / f"MANIFEST_{label}.json"
    out_json.write_text(json.dumps(manifest, indent=1), encoding="utf-8")

    lines = [f"# Manifest ({label})", "",
             f"- generated (UTC): {now}",
             f"- git HEAD: `{manifest['git_head']}`",
             f"- code tree SHA-256 (prototype/src/*.py): `{tree}`",
             f"- files: {len(entries)}; missing: {len(missing)}", ""]
    for group in GROUPS:
        lines += [f"## {group}", "", "| file | SHA-256 (LF-normalized) | sign-off | git | mtime (UTC) |",
                  "|---|---|---|---|---|"]
        for rel, e in entries.items():
            if e["group"] == group:
                lines.append(f"| `{rel}` | `{e['sha256']}` | {e['signoff'] or '-'} | "
                             f"{e['git']} | {e['mtime_utc']} |")
        lines.append("")
    if missing:
        lines += ["## Missing", ""] + [f"- `{m}`" for m in missing]
    (HERE / f"MANIFEST_{label}.md").write_text("\n".join(lines) + "\n",
                                                encoding="utf-8")
    print(f"wrote {out_json.name} and MANIFEST_{label}.md: {len(entries)} files, "
          f"{len(missing)} missing, code tree {tree[:12]}")


if __name__ == "__main__":
    main()
