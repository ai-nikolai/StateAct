#!/usr/bin/env bash
#
# Run a named ALFWorld experiment.
#
# This used to be ~1000 lines of repeated
#     if [ $1 == "name" ]; then python3 alfworld_run.py ... ; fi;
# blocks. The experiment table now lives in experiments/alfworld.yaml and the
# runner in stateact/run_config.py; this wrapper keeps the old interface so
# every documented command still works:
#
#     bash run_alfworld_eval.sh eval_mix
#     bash run_alfworld_eval.sh --list
#     bash run_alfworld_eval.sh eval_mix --dry-run
#
# The argv each experiment passes to alfworld_run.py is unchanged (it was
# extracted mechanically from the old script).

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

if [ "$#" -eq 0 ]; then
    echo "usage: $(basename "$0") <experiment> [--dry-run]" >&2
    echo "       $(basename "$0") --list" >&2
    echo >&2
    cd "${REPO_ROOT}" || exit 1
exec python3 "${REPO_ROOT}/stateact/run_config.py" alfworld --list
fi

cd "${REPO_ROOT}" || exit 1
exec python3 "${REPO_ROOT}/stateact/run_config.py" alfworld "$@"
