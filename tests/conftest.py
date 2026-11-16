"""Shared test configuration.

The benchmark entry points are plain scripts (``python3 alfworld_runs/alfworld_run.py``),
so they put their own directory on ``sys.path``.  Tests run from the repository
root instead, so add both the root (for ``stateact``) and ``alfworld_runs`` (for
the prompt artefacts) explicitly.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ALFWORLD_DIR = REPO_ROOT / "alfworld_runs"

for path in (str(REPO_ROOT), str(ALFWORLD_DIR)):
    if path not in sys.path:
        sys.path.insert(0, path)
