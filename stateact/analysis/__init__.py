"""Analysis helpers for the unified result format.

Every benchmark writes the same files::

    <results_folder>/<trial>/summary.csv
    <results_folder>/<trial>/episodes.csv

Use :func:`load_summary`, :func:`load_episodes` or :func:`summarise` for all
three benchmarks. The notebooks under the repository's ``analysis/`` folder
use the same functions.
"""

from stateact.analysis.core import (
    load_episodes,
    load_summary,
    require_pandas,
    summarise,
    to_frame,
)

__all__ = [
    "load_episodes",
    "load_summary",
    "require_pandas",
    "summarise",
    "to_frame",
]
