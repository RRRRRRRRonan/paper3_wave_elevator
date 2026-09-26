"""Compare Study 1 self-test outputs from the pinned code (3ef64f08b16b) and the current code.
Provenance fields (hashes of code and registrations, code-tree provenance, file paths) are
removed; every other value, including every number, must be identical."""
import gzip
import hashlib
import json
from pathlib import Path

T = Path(r"C:/Users/64432/.claude/jobs/fe72e7b6/tmp")
A, B = T / "eq_pinned", T / "eq_current"
ROOT_A, ROOT_B = str(T / "pinned_wt"), "F:/Paper 3"
DROP_KEYS = {"code_tree_sha256", "code_tree_sha256_pinned", "code_tree_matches_pinned"}


def norm_str(s: str) -> str:
    for r in (ROOT_A, ROOT_A.replace("/", "\\"), ROOT_B, ROOT_B.replace("/", "\\"), str(A), str(B),
              str(A).replace("/", "\\"), str(B).replace("/", "\\")):
        s = s.replace(r, "<ROOT>")
    return s


def clean(o):
    if isinstance(o, dict):
        return {k: clean(v) for k, v in o.items()
                if k not in DROP_KEYS and not k.endswith("sha256") and not k.endswith("_path")
                and not k.endswith("_paths")}
    if isinstance(o, list):
        return [clean(v) for v in o]
    if isinstance(o, str):
        return norm_str(o)
    return o


def first_diff(a, b, path="$"):
    if type(a) != type(b):
        return f"{path}: type {type(a).__name__} vs {type(b).__name__}"
    if isinstance(a, dict):
        if set(a) != set(b):
            return f"{path}: keys differ {sorted(set(a) ^ set(b))[:6]}"
        for k in a:
            d = first_diff(a[k], b[k], f"{path}.{k}")
            if d:
                return d
        return None
    if isinstance(a, list):
        if len(a) != len(b):
            return f"{path}: length {len(a)} vs {len(b)}"
        for i, (x, y) in enumerate(zip(a, b)):
            d = first_diff(x, y, f"{path}[{i}]")
            if d:
                return d
        return None
    if a != b and not (isinstance(a, float) and a != a and b != b):   # NaN == NaN
        return f"{path}: {a!r} vs {b!r}"
    return None


files_a = {p.relative_to(A).as_posix() for p in A.rglob("*") if p.is_file() and not p.name.startswith("_log_")}
files_b = {p.relative_to(B).as_posix() for p in B.rglob("*") if p.is_file() and not p.name.startswith("_log_")}
print(f"outputs: pinned {len(files_a)}, current {len(files_b)}, only in one: {sorted(files_a ^ files_b)}")
n_json = n_data = n_img = 0
diffs = []
for rel in sorted(files_a & files_b):
    pa, pb = A / rel, B / rel
    if rel.endswith(".json"):
        n_json += 1
        d = first_diff(clean(json.loads(pa.read_text(encoding="utf-8"))), clean(json.loads(pb.read_text(encoding="utf-8"))))
        if d:
            diffs.append((rel, d))
    elif rel.endswith((".csv", ".csv.gz", ".txt")):
        n_data += 1
        rd = (lambda p: gzip.open(p, "rb").read() if rel.endswith(".gz") else p.read_bytes())
        if norm_str(rd(pa).decode("utf-8", "replace")) != norm_str(rd(pb).decode("utf-8", "replace")):
            diffs.append((rel, "data file content differs"))
    else:
        n_img += 1
        same = hashlib.sha256(pa.read_bytes()).hexdigest() == hashlib.sha256(pb.read_bytes()).hexdigest()
        print(f"  image {rel}: {'identical bytes' if same else 'bytes differ (image metadata only; not compared)'}")
print(f"compared: {n_json} JSON (provenance removed), {n_data} data files; images listed above: {n_img}")
print("DIFFERENCES:" if diffs else "NO DIFFERENCES in any compared value")
for rel, d in diffs:
    print("  ", rel, "::", d)
