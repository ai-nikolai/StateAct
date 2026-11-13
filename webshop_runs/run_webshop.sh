#!/usr/bin/env bash
#
# Run a named WebShop experiment.
#
# The experiment table now lives in experiments/webshop.yaml and the runner in
# stateact/run_config.py; this wrapper keeps the old interface:
#
#     bash run_webshop.sh webshop_api
#     bash run_webshop.sh --list
#     bash run_webshop.sh webshop_local --dry-run
#
# NOTE (upstream quirk, preserved verbatim): the 'webshop_local' entry passes
# `--socket` with no value, because SOCKET_NAME was only ever assigned inside a
# commented-out line in the original script. Export SOCKET_NAME and pass
# --socket explicitly if you actually want the unix-socket path.

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

if [ "$#" -eq 0 ]; then
    echo "usage: $(basename "$0") <experiment> [--dry-run]" >&2
    echo "       $(basename "$0") --list" >&2
    echo >&2
    cd "${REPO_ROOT}" || exit 1
exec python3 "${REPO_ROOT}/stateact/run_config.py" webshop --list
fi

cd "${REPO_ROOT}" || exit 1
exec python3 "${REPO_ROOT}/stateact/run_config.py" webshop "$@"
