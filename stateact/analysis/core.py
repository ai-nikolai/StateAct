"""Unified analysis entry points for all benchmarks.

Everything is built on :mod:`stateact.results`, so ALFWorld, WebShop and
TextCraft are read through the same ``summary.csv`` / ``episodes.csv`` schemas.
pandas is imported lazily because the benchmark environments do not install it.
"""

from stateact import results

__all__ = ["require_pandas", "to_frame", "load_summary", "load_episodes", "summarise"]


def require_pandas():
    import pandas as pd

    return pd


def to_frame(rows):
    return require_pandas().DataFrame(rows)


def load_summary(path_or_dir):
    """Load ``summary.csv`` as a DataFrame."""
    return to_frame(results.load_summary(path_or_dir))


def load_episodes(path_or_dir):
    """Load ``episodes.csv`` as a DataFrame."""
    return to_frame(results.load_episodes(path_or_dir))


def summarise(path_or_data, sort=True):
    """Return one clean row per run, sorted by model/agent when available.

    ``path_or_data`` may be a path, a row list, or an existing DataFrame.
    """
    if hasattr(path_or_data, "columns"):
        frame = path_or_data.copy()
    elif isinstance(path_or_data, (list, tuple)):
        frame = to_frame(path_or_data)
    else:
        frame = load_summary(path_or_data)

    if sort:
        columns = [c for c in ("model", "agent", "trial") if c in frame.columns]
        if columns:
            frame = frame.sort_values(columns)
    return frame.reset_index(drop=True)
