"""Report the overall ALFWorld success rate for one trial.

Thin CLI wrapper: the scoring logic lives in ``stateact.scoring`` so the same
aggregation can be reused by the WebShop / TextCraft analysis notebooks.

Usage (from anywhere; paths are resolved relative to ``alfworld_runs/``):

    python3 alfworld_runs/get_score.py --trial_name "baseline_14B"

Expected output:

    Overall (mean) Score: 0.805970 with 108 successful envs and a total of 134 envs.
"""

import os
import sys

# Make the repository root importable: this script is executed as a plain file.
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_SCRIPT_DIR)
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from stateact.scoring import main  # noqa: E402


if __name__ == "__main__":
    # results/ and legacy game_logs/ live next to this script, so make the
    # CLI work from any working directory.
    os.chdir(_SCRIPT_DIR)
    main()
