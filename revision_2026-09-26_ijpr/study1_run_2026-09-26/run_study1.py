"""Study 1 registered run (author's instruction of 2026-09-26: "帮我开始跑study 1").

Runs the eleven Study 1 commands in the registered order, from prototype/, with the
registered defaults (no override flags). Stops at the first failure. Before and after,
hashes every file under prototype/results/ so that new and changed files are listed and
no stored Phase 5 file can change unnoticed. One log file per command in this folder.
"""
import datetime as dt
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROTO = HERE.parents[1] / "prototype"
RESULTS = PROTO / "results"
STEPS = [
    ["analysis_S1_cluster_bootstrap"],
    ["analysis_S1_displays", "s1-6"],
    ["analysis_S1_displays", "s1-7"],
    ["experiments_S1_enumeration", "s1-2"],
    ["experiments_S1_enumeration", "s1-8"],
    ["experiments_S1_enumeration", "s1-11"],
    ["experiments_S1_blockC_ext"],
    ["analysis_S1_displays", "th-2"],
    ["experiments_S1_tiebreak_regen"],
    ["experiments_S1_b5_rerun"],
    ["experiments_S1_B4_B6"],
]


def now():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def snapshot():
    return {p.relative_to(RESULTS).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(RESULTS.rglob("*")) if p.is_file()}


def main():
    start_at = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    state_path = HERE / "run_state.json"
    state = json.loads(state_path.read_text(encoding="utf-8")) if start_at and state_path.exists() else {
        "started_utc": now(), "results_before": snapshot(), "steps": []}
    state_path.write_text(json.dumps(state, indent=1), encoding="utf-8")
    for i, step in enumerate(STEPS):
        if i < start_at:
            continue
        name = "_".join(step)
        log = HERE / f"{i + 1:02d}_{name}.log"
        t0, started = time.time(), now()
        print(f"START {i + 1}/{len(STEPS)} {' '.join(step)} at {started}", flush=True)
        with open(log, "w", encoding="utf-8") as fh:
            rc = subprocess.run([sys.executable, "-u", "-m", f"src.{step[0]}", *step[1:]], cwd=PROTO,
                                stdout=fh, stderr=subprocess.STDOUT,
                                env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8",
                                     "PYTHONDONTWRITEBYTECODE": "1"}).returncode
        secs = round(time.time() - t0, 1)
        state["steps"].append({"step": i + 1, "command": " ".join(step), "started_utc": started,
                               "seconds": secs, "exit_code": rc, "log": log.name})
        state_path.write_text(json.dumps(state, indent=1), encoding="utf-8")
        print(f"{'DONE' if rc == 0 else 'FAILED'} {i + 1}/{len(STEPS)} {' '.join(step)} "
              f"exit={rc} in {secs}s", flush=True)
        if rc != 0:
            break
    after = snapshot()
    before = state["results_before"]
    state["finished_utc"] = now()
    state["new_files"] = sorted(k for k in after if k not in before)
    state["changed_files"] = sorted(k for k in after if k in before and after[k] != before[k])
    state["removed_files"] = sorted(k for k in before if k not in after)
    state["results_after"] = after
    state_path.write_text(json.dumps(state, indent=1), encoding="utf-8")
    print(f"RUN END new={len(state['new_files'])} changed={state['changed_files']} "
          f"removed={state['removed_files']}", flush=True)


if __name__ == "__main__":
    main()
