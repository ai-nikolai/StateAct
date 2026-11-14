"""Reading and aggregating the per-run result logs.

``alfworld_runs/get_score.py`` used to hold this logic inline; it is now a thin
CLI over this module so that the WebShop / TextCraft analysis notebooks can
reuse the same aggregation instead of re-implementing it.

pandas is used when available, but a standard-library ``csv`` fallback keeps
``get_score.py`` working in the benchmark environments (which do not install
pandas).
"""

__all__ = [
    "results_path",
    "load_results",
    "score_dataframe",
    "format_score",
    "score_trial",
    "summarise_rewards",
    "main",
]

# Unified layout written by alfworld_run.py:
#   results/<trial_name>/episodes.csv
# The legacy layout is still recognised:
#   game_logs/alfworld_eval_<trial_name>/alfworld_results.csv
DEFAULT_BASE_FOLDER = "results"
DEFAULT_EVAL_NAME = ""
DEFAULT_CSV_NAME = "episodes.csv"
SUCCESS_COLUMN = "success"


def results_path(trial_name, base_folder=DEFAULT_BASE_FOLDER,
                 eval_name=DEFAULT_EVAL_NAME, csv_name=DEFAULT_CSV_NAME):
    """Return the results CSV for ``trial_name`` (new layout, then legacy)."""
    import os

    folder = f"{eval_name}_{trial_name}" if eval_name else trial_name
    path = os.path.join(base_folder, folder, csv_name)
    if os.path.exists(path):
        return path

    for legacy in (
        os.path.join(base_folder, f"alfworld_eval_{trial_name}",
                     "alfworld_results.csv"),
        os.path.join("game_logs", f"alfworld_eval_{trial_name}",
                     "alfworld_results.csv"),
    ):
        if os.path.exists(legacy):
            return legacy
    return path


def _read_csv_rows(path):
    """Read a results CSV as a list of dicts (stdlib fallback)."""
    import csv

    with open(path, newline="") as handle:
        return list(csv.DictReader(handle))


def _to_success(value):
    """Parse the boolean spellings written by ALFWorld into 0/1."""
    if isinstance(value, bool):
        return int(value)
    text = str(value).strip().lower()
    if text in ("1", "true", "yes"):
        return 1
    if text in ("0", "false", "no", ""):
        return 0
    return int(float(value))


def load_results(trial_name, base_folder=DEFAULT_BASE_FOLDER,
                 eval_name=DEFAULT_EVAL_NAME, csv_name=DEFAULT_CSV_NAME):
    """Load the ``alfworld_results.csv`` for a trial.

    Returns a pandas DataFrame when pandas is installed, otherwise a list of
    row dicts. Both are accepted by :func:`score_dataframe`.
    """
    path = results_path(trial_name, base_folder, eval_name, csv_name)
    try:
        import pandas as pd
    except ImportError:
        return _read_csv_rows(path)
    return pd.read_csv(path)


def score_dataframe(df, success_column=SUCCESS_COLUMN):
    """Aggregate a results DataFrame (or row list) into score metrics.

    ``score`` is the mean of the success column cast to int, i.e. the overall
    success rate reported in the paper.
    """
    if hasattr(df, "astype") and hasattr(df, "columns"):
        column = df.astype({success_column: int})[success_column]
        return {
            "score": column.mean(),
            "num_items": column.count(),
            "num_successful": column.sum(),
        }

    values = [_to_success(row[success_column]) for row in df]
    total = len(values)
    successful = sum(values)
    return {
        "score": successful / total if total else 0.0,
        "num_items": total,
        "num_successful": successful,
    }


def format_score(result):
    """Render a :func:`score_dataframe` result the way get_score.py printed it."""
    return (
        f"Overall (mean) Score: {result['score']:.6f} "
        f"with {result['num_successful']} successful envs "
        f"and a total of {result['num_items']} envs."
    )


def score_trial(trial_name, **kwargs):
    """Load and score one trial, returning the :func:`score_dataframe` dict."""
    return score_dataframe(load_results(trial_name, **kwargs))


def summarise_rewards(rewards):
    """Aggregate a plain list of 0/1 rewards (WebShop / TextCraft style).

    Returns ``{score, num_items, num_successful}`` so notebooks written against
    the ALFWorld CSV helper can share the same reporting code.
    """
    items = [int(r) for r in rewards]
    if not items:
        return {"score": 0.0, "num_items": 0, "num_successful": 0}
    return {
        "score": sum(items) / len(items),
        "num_items": len(items),
        "num_successful": sum(items),
    }


def main(argv=None):
    """CLI: ``python -m stateact.scoring --trial_name <name>``."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Report the overall success rate for an ALFWorld trial.")
    parser.add_argument("--trial_name", required=True, help="Name of the trial")
    parser.add_argument("--base_folder", default=DEFAULT_BASE_FOLDER,
                        help=f"Folder holding the logs (default: {DEFAULT_BASE_FOLDER})")
    parser.add_argument("--eval_name", default=DEFAULT_EVAL_NAME,
                        help=f"Eval prefix (default: {DEFAULT_EVAL_NAME})")
    args = parser.parse_args(argv)

    result = score_trial(args.trial_name, base_folder=args.base_folder,
                         eval_name=args.eval_name)
    print(format_score(result))
    return result


if __name__ == "__main__":
    main()
