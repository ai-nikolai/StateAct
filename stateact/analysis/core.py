"""Unified analysis entry points.

Everything is built on :mod:`stateact.results`, so ALFWorld, WebShop and
TextCraft are read through the same summary/episode schemas.  pandas is
imported lazily because the benchmark environments do not install it.
"""

from stateact import results
from stateact.analysis.common import require_pandas

__all__ = ["to_frame", "load_summary", "load_episodes", "summarise"]


def to_frame(rows):
    """Convert a row list to a DataFrame (pandas is imported lazily)."""
    return require_pandas().DataFrame(rows)


def load_summary(path_or_dir, benchmark=None):
    """Load ``summary.csv`` (or a legacy scores file) as a DataFrame."""
    return to_frame(results.load_summary(path_or_dir, benchmark=benchmark))


def load_episodes(path_or_dir, benchmark=None):
    """Load ``episodes.csv`` (or a legacy ALFWorld CSV) as a DataFrame."""
    return to_frame(results.load_episodes(path_or_dir, benchmark=benchmark))


def summarise(path_or_data, benchmark=None, sort=True):
    """Return one clean row per run, sorted by model/agent when available.

    ``path_or_data`` may be a path, a row list, or an existing DataFrame.
    """
    if hasattr(path_or_data, "columns"):
        frame = path_or_data.copy()
    elif isinstance(path_or_data, (list, tuple)):
        frame = to_frame(path_or_data)
    else:
        frame = load_summary(path_or_data, benchmark=benchmark)

    if sort:
        columns = [c for c in ("model", "agent", "trial") if c in frame.columns]
        if columns:
            frame = frame.sort_values(columns)
    return frame.reset_index(drop=True)
