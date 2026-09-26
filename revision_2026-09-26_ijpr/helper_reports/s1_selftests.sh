#!/usr/bin/env bash
# Run the eleven Study 1 self-tests (toy seeds, scratch output) from the repo given as $1 into scratch $2.
REPO="$1"; SCR="$2"
cd "$REPO/prototype" || exit 1
export PAPER3_SCRATCH="$SCR" PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
rm -rf "$SCR"; mkdir -p "$SCR"
fail=0
for args in "analysis_S1_cluster_bootstrap" "analysis_S1_displays s1-6" "analysis_S1_displays s1-7" \
            "experiments_S1_enumeration s1-2" "experiments_S1_enumeration s1-8" "experiments_S1_enumeration s1-11" \
            "experiments_S1_blockC_ext" "analysis_S1_displays th-2" "experiments_S1_tiebreak_regen" \
            "experiments_S1_b5_rerun" "experiments_S1_B4_B6"; do
  set -- $args
  if python -m "src.$1" ${2:+$2} --selftest > "$SCR/_log_${1}_${2:-x}.txt" 2>&1; then echo "PASS $args"; else echo "FAIL $args"; fail=1; fi
done
exit $fail
