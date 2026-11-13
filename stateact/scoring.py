"""Reading and aggregating the per-run result logs.

``alfworld_runs/get_score.py`` used to hold this logic inline; it is now a thin
CLI over this module so that the WebShop / TextCraft analysis notebooks can
reuse the same aggregation instead of re-implementing it.

pandas is imported lazily so that ``import stateact.scoring`` (and the
dependency-free parts of this package) keep working in a minimal environment.
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

# Defaults match the layout alfworld_run.py writes:
#   game_logs/alfworld_eval_<trial_name>/alfworld_results.csv
DEFAULT_BASE_FOLDER = "game_logs"
DEFAULT_EVAL_NAME = "alfworld_eval"
DEFAULT_CSV_NAME = "alfworld_results.csv"
SUCCESS_COLUMN = "success"


def results_path(trial_name, base_folder=DEFAULT_BASE_FOLDER,
                 eval_name=DEFAULT_EVAL_NAME, csv_name=DEFAULT_CSV_NAME):
    """Return the path of the results CSV for ``trial_name``."""
    import os

    return os.path.join(base_folder, f"{eval_name}_{trial_name}", csv_name)


def load_results(trial_name, base_folder=DEFAULT_BASE_FOLDER,
                 eval_name=DEFAULT_EVAL_NAME, csv_name=DEFAULT_CSV_NAME):
    """Load the ``alfworld_results.csv`` for a trial as a DataFrame."""
    import pandas as pd

    return pd.read_csv(results_path(trial_name, base_folder, eval_name, csv_name))


def score_dataframe(df, success_column=SUCCESS_COLUMN):
    """Aggregate a results DataFrame into ``{score, num_items, num_successful}``.

    ``score`` is the mean of the success column cast to int, i.e. the overall
    success rate reported in the paper.
    """
    df = df.astype({success_column: int})
    return {
        "score": df[success_column].mean(),
        "num_items": df[success_column].count(),
        "num_successful": df[success_column].sum(),
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
