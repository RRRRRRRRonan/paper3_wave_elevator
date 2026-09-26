"""Week 4, before the L2 code freeze: correct the pre-signing status text in the module docstrings of the six
Study 1 scripts (registrations signed or acknowledged on 2026-09-26; registered run the same day).
Only the module docstring changes; the check below compares each module's AST with the docstring removed."""
import ast
import hashlib
import json
from pathlib import Path

SRC = Path(r"F:/Paper 3/prototype/src")
RUN = "revision_2026-09-26_ijpr/study1_run_2026-09-26/"
REAL = "# real run: writes into prototype/results/; only at the author's request"

EDITS = {
    "experiments_S1_B4_B6.py": [
        ('Guard key: "S1C" (author_signoff of the EXECUTION NOTE is\n'
         '"PENDING (acknowledgement only; the designs and gates were signed on\n'
         '2026-07-08)" as of 2026-09-26 -- so even though B-4/B-6\'s own DESIGN was\n'
         'signed 2026-07-08, `registration_guard.require_signed("S1C")` reads the\n'
         'EXECUTION NOTE\'s own front matter, which is still PENDING, and stops. This\n'
         'is the guard key the task brief specifies for S1-4/S1-5.\n',
         'Guard key: "S1C". The designs and gates of B-4/B-6 were signed on\n'
         '2026-07-08; `registration_guard.require_signed("S1C")` reads the EXECUTION\n'
         'NOTE\'s own front matter, which was ACKNOWLEDGED on 2026-09-26, and also\n'
         'requires the S1D deviation note (acknowledged the same day).\n'),
        ('Real mode never executes tonight: `require_signed("S1C")` stops the script\n'
         'first. Self-test mode',
         'Real mode runs only after `require_signed("S1C")` passes; the registered\n'
         f'run took place on 2026-09-26 ({RUN}). Self-test mode'),
        ('  python -m src.experiments_S1_B4_B6             # stops at the guard\n',
         f'  python -m src.experiments_S1_B4_B6             {REAL}\n'),
    ],
    "experiments_S1_enumeration.py": [
        ('Guard key: "S1B" (author_signoff PENDING as of 2026-09-26).\n',
         'Guard key: "S1B" (signed 2026-09-26; the guard also requires the S1D note).\n'),
        ('procedure (S1-2\'s own Inputs name these CSVs), but real mode never executes\n'
         'tonight: `require_signed("S1B")` stops the script first, since the\n'
         'registration is unsigned. Self-test mode never reads any file under\n',
         'procedure (S1-2\'s own Inputs name these CSVs). Real mode runs only after\n'
         '`require_signed("S1B")` passes; the registered run took place on\n'
         f'2026-09-26 ({RUN}). Self-test mode never reads any file under\n'),
        ('  python -m src.experiments_S1_enumeration s1-2             # stops at guard\n',
         f'  python -m src.experiments_S1_enumeration s1-2             {REAL}\n'),
    ],
    "experiments_S1_blockC_ext.py": [
        ('Real mode never executes tonight: `require_signed("S1B")` stops the script\n'
         'first. Self-test mode',
         'Real mode runs only after `require_signed("S1B")` passes; the registered\n'
         f'run took place on 2026-09-26 ({RUN}). Self-test mode'),
        ('  python -m src.experiments_S1_blockC_ext             # stops at the guard\n',
         f'  python -m src.experiments_S1_blockC_ext             {REAL}\n'),
    ],
    "experiments_S1_tiebreak_regen.py": [
        ('("S1-9. Tie-break regeneration of Blocks A and B [QA]"). Guard key: "S1B"\n'
         '(author_signoff PENDING as of 2026-09-26).\n',
         '("S1-9. Tie-break regeneration of Blocks A and B [QA]"). Guard key: "S1B"\n'
         '(signed 2026-09-26; the guard also requires the S1D note).\n'),
        ('(phase5_config.SEED_BASE, experiments_phase5._seed) -- exactly what Absolute\n'
         'Rule 2 forbids running tonight. `require_signed("S1B", selftest=False)`\n'
         'stops the script before any of this executes; the registration is unsigned.\n',
         '(phase5_config.SEED_BASE, experiments_phase5._seed), and runs only after\n'
         '`require_signed("S1B", selftest=False)` passes; the registered run took\n'
         f'place on 2026-09-26 ({RUN}).\n'),
        ('  python -m src.experiments_S1_tiebreak_regen             # stops at guard\n',
         f'  python -m src.experiments_S1_tiebreak_regen             {REAL}\n'),
    ],
    "analysis_S1_cluster_bootstrap.py": [
        ('Guard key: "S1A" (author_signoff PENDING as of 2026-09-26 -- real mode refuses\n'
         'to run until signed; --selftest exercises the code on fabricated data only).\n',
         'Guard key: "S1A" (signed 2026-09-26; the guard also requires the S1D note;\n'
         f'registered run on 2026-09-26, {RUN};\n'
         '--selftest exercises the code on fabricated data only).\n'),
        ('  python -m src.analysis_S1_cluster_bootstrap            # stops at the guard\n',
         f'  python -m src.analysis_S1_cluster_bootstrap            {REAL}\n'),
    ],
    "analysis_S1_displays.py": [
        ('Guard key: "S1A" (author_signoff PENDING as of 2026-09-26).\n',
         'Guard key: "S1A" (signed 2026-09-26; the guard also requires the S1D note).\n'),
        ('the registration names and never executes tonight: `require_signed("S1A")`\n'
         'stops the script first. Self-test mode',
         'the registration names and runs only after `require_signed("S1A")` passes;\n'
         f'the registered run took place on 2026-09-26 ({RUN}). Self-test mode'),
        ('  python -m src.analysis_S1_displays s1-6             # stops at the guard\n',
         f'  python -m src.analysis_S1_displays s1-6             {REAL}\n'),
    ],
}


def ast_without_docstring(src: str) -> str:
    tree = ast.parse(src)
    body = tree.body
    if body and isinstance(body[0], ast.Expr) and isinstance(getattr(body[0], "value", None), ast.Constant) \
            and isinstance(body[0].value.value, str):
        tree.body = body[1:]
    return ast.dump(tree)


record = {}
for name, reps in EDITS.items():
    p = SRC / name
    raw = p.read_bytes()
    crlf = b"\r\n" in raw
    old = raw.decode("utf-8").replace("\r\n", "\n")
    new = old
    for a, b in reps:
        assert new.count(a) == 1, (name, a[:70])
        new = new.replace(a, b)
    assert ast_without_docstring(old) == ast_without_docstring(new), name
    out = (new.replace("\n", "\r\n") if crlf else new).encode("utf-8")
    p.write_bytes(out)
    record[name] = {"sha256_before": hashlib.sha256(raw).hexdigest(), "sha256_after": hashlib.sha256(out).hexdigest(),
                    "replacements": len(reps), "code_outside_docstring_unchanged": True}
    print(f"{name}: {len(reps)} replacements; AST outside the docstring unchanged")
Path(r"C:/Users/64432/.claude/jobs/fe72e7b6/tmp/s1_docstring_fix_record.json").write_text(json.dumps(record, indent=2))
