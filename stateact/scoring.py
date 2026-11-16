"""Score one ALFWorld run from ``results/<trial>/episodes.csv``.

The scoring code is standard-library friendly so it works in ``env_alfworld``,
which does not install pandas.
"""

from stateact import results

__all__ = [
    "results_path",
    "load_results",
    "score_dataframe",
    "format_score",
    "score_trial",
    "summarise_rewards",
    "main",
]

DEFAULT_BASE_FOLDER = "results"
SUCCESS_COLUMN = "success"


def results_path(trial_name, base_folder=DEFAULT_BASE_FOLDER):
    """Return ``<base_folder>/<trial>/episodes.csv``."""
    return results.episodes_path(trial_name, base_folder)


def load_results(trial_name, base_folder=DEFAULT_BASE_FOLDER):
    """Load the per-episode rows for a trial."""
    return results.load_episodes(results_path(trial_name, base_folder))


def _to_success(value):
    if isinstance(value, bool):
        return int(value)
    text = str(value).strip().lower()
    if text in ("1", "true", "yes"):
        return 1
    if text in ("0", "false", "no", ""):
        return 0
    return int(float(value))


def score_dataframe(df, success_column=SUCCESS_COLUMN):
    """Aggregate a DataFrame or a row list into score metrics."""
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
    return (
        f"Overall (mean) Score: {result['score']:.6f} "
        f"with {result['num_successful']} successful envs "
        f"and a total of {result['num_items']} envs."
    )


def score_trial(trial_name, **kwargs):
    return score_dataframe(load_results(trial_name, **kwargs))


def summarise_rewards(rewards):
    """Aggregate a plain list of 0/1 rewards."""
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
        description="Report the overall success rate for an ALFWorld trial."
    )
    parser.add_argument("--trial_name", required=True, help="Name of the trial")
    parser.add_argument(
        "--base_folder", default=DEFAULT_BASE_FOLDER,
        help=f"Folder holding the runs (default: {DEFAULT_BASE_FOLDER})",
    )
    args = parser.parse_args(argv)

    result = score_trial(args.trial_name, base_folder=args.base_folder)
    print(format_score(result))
    return result


if __name__ == "__main__":
    main()
