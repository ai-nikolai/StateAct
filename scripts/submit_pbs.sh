#!/usr/bin/env bash
#
# Submit one of the A100 PBS jobs from the repository root.
#
# Usage:
#     bash scripts/submit_pbs.sh alfworld [qsub options...]
#     bash scripts/submit_pbs.sh webshop  [qsub options...]
#     bash scripts/submit_pbs.sh alfworld --dry-run
#
# Any remaining arguments are passed to qsub, so variables can be overridden:
#     bash scripts/submit_pbs.sh alfworld -v MODEL=Qwen/Qwen2.5-3B-Instruct
#     bash scripts/submit_pbs.sh webshop  -v AGENT=react -v NUM_ENVS=30
#
# Overridable variables (see the .pbs files): MODEL, NUM_ENVS, START_INDEX,
# SEED, AGENT, MAX_MODEL_LEN, TRIAL_NAME, RESULTS_FOLDER, CONDA_ENV,
# WEBSHOP_SIMG, REPO_ROOT.

set -euo pipefail

BENCHMARK="${1:-}"
if [ -z "${BENCHMARK}" ]; then
    echo "usage: $0 <alfworld|webshop> [qsub options...]" >&2
    exit 2
fi
shift

case "${BENCHMARK}" in
    alfworld|webshop) ;;
    *)
        echo "error: unknown benchmark '${BENCHMARK}' (expected alfworld or webshop)" >&2
        exit 2
        ;;
esac

DRY_RUN=0
QSUB_ARGS=()
for argument in "$@"; do
    if [ "${argument}" = "--dry-run" ]; then
        DRY_RUN=1
    else
        QSUB_ARGS+=("${argument}")
    fi
done

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PBS_FILE="${REPO_ROOT}/scripts/pbs/${BENCHMARK}_a100.pbs"
LOG_DIR="${REPO_ROOT}/logs/pbs"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
LOG_FILE="${LOG_DIR}/${BENCHMARK}_${TIMESTAMP}.log"

if [ ! -f "${PBS_FILE}" ]; then
    echo "error: PBS file not found: ${PBS_FILE}" >&2
    exit 2
fi

mkdir -p "${LOG_DIR}"

# Submit from the repository root so PBS_O_WORKDIR is the repo root; the job
# scripts use that as their default REPO_ROOT.
cd "${REPO_ROOT}"

CMD=(
    qsub
    -N "stateact_${BENCHMARK}_${TIMESTAMP}"
    -o "${LOG_FILE}"
    "${QSUB_ARGS[@]}"
    "${PBS_FILE}"
)

printf 'Submitting:'
printf ' %q' "${CMD[@]}"
printf '\n'

if [ "${DRY_RUN}" -eq 1 ]; then
    exit 0
fi

"${CMD[@]}"
