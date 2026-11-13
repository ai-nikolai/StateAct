"""ALFWorld result-log analysis.

The function names and return shapes match the helpers in
``alfworld_runs/analysis_alfworld_eval_notebook.ipynb``. They are kept
compatible on purpose so the notebook only needs an import change:

    from stateact.analysis.alfworld import load_data, analyse_data_old

The only behavioural change is that the hard-coded ``/135`` denominator is now
a ``num_envs`` argument (default 135), so smaller runs can be analysed too.
"""

import os

from stateact.analysis.common import require_pandas

__all__ = [
    "get_data_file_path",
    "convert_string_to_bool",
    "convert_string_to_bool_int",
    "convert_bool_string_to_bool_int",
    "load_data",
    "analyse_data_basic",
    "analyse_data_old",
    "analyse_data_new",
    "no_groupby_analyse_data",
    "create_pivot",
    "summarise_trial",
    "main",
]

DEFAULT_BASE_FOLDER = "game_logs"
DEFAULT_TRIAL_BASE_NAME = "alfworld_eval_"
DEFAULT_CSV_NAME = "alfworld_results.csv"
DEFAULT_NUM_ENVS = 135


def get_data_file_path(current_trial_name="v5_eval", base_folder=DEFAULT_BASE_FOLDER,
                       trial_base_name=DEFAULT_TRIAL_BASE_NAME,
                       csv_file_name=DEFAULT_CSV_NAME):
    """Return the CSV path for a trial (notebook-compatible name)."""
    return os.path.join(
        base_folder, trial_base_name + current_trial_name, csv_file_name
    )


def convert_string_to_bool(in_string):
    """Non-empty string -> True (notebook-compatible)."""
    return bool(in_string)


def convert_string_to_bool_int(in_string):
    """Non-empty string -> 1 (notebook-compatible)."""
    return 1 if in_string else 0


def convert_bool_string_to_bool_int(in_string):
    """Convert the several boolean spellings found in old CSVs to 0/1."""
    if in_string in ("(False,)", "False", "0", "", None):
        return 0
    if in_string in ("(True,)", "True", "1"):
        return 1
    raise ValueError(f"Not a boolean string: {in_string!r}")


def load_data(trial_name, base_folder=DEFAULT_BASE_FOLDER,
              trial_base_name=DEFAULT_TRIAL_BASE_NAME,
              csv_file_name=DEFAULT_CSV_NAME):
    """Load ``alfworld_results.csv`` for a trial.

    ``trial_name`` may also be a direct path to a CSV.
    """
    pd = require_pandas()
    path = trial_name if str(trial_name).endswith(".csv") else get_data_file_path(
        trial_name, base_folder, trial_base_name, csv_file_name
    )
    return pd.read_csv(
        path,
        quoting=1,
        index_col=False,
        converters={
            "early_stop": convert_string_to_bool_int,
            "error": convert_string_to_bool_int,
        },
    )


def _aggregate(input_data, groupby, header_order, num_envs):
    """Sum the numeric columns, add ``total`` / ``success_percentage``."""
    grouped = input_data.groupby(groupby)
    out = grouped.sum(numeric_only=True).reset_index()

    totals = grouped["success"].count().rename("total").reset_index()
    out = out.merge(totals, on=groupby, how="left")
    out["success_percentage"] = out["success"] / num_envs * 100

    # Historical columns first, then any extra numeric columns (tokens, etc.).
    columns = [column for column in header_order if column in out.columns]
    columns += [column for column in out.columns if column not in columns]
    return out[columns]


def analyse_data_basic(input_data, num_envs=DEFAULT_NUM_ENVS):
    """Legacy grouping by the keys removed/used.

    Old logs have ``keys_removed``; current logs record ``keys_to_use``.
    """
    key_column = "keys_removed"
    if key_column not in input_data.columns:
        key_column = "keys_to_use"
    if key_column not in input_data.columns:
        raise KeyError(
            "analyse_data_basic needs a 'keys_removed' or 'keys_to_use' column"
        )

    out = _aggregate(
        input_data,
        ["model", key_column],
        ["model", key_column, "env_idx", "success", "done", "early_stop",
         "error", "num_of_steps"],
        num_envs,
    )
    out2 = out[[key_column, "model", "success_percentage", "done"]]
    return out.groupby(key_column), out2


def analyse_data_old(input_data, num_envs=DEFAULT_NUM_ENVS):
    """Group by model / prompt_name / correction (main notebook helper)."""
    out = _aggregate(
        input_data,
        ["model", "prompt_name", "correction"],
        ["model", "prompt_name", "correction", "env_idx", "success", "done",
         "early_stop", "error", "num_of_steps"],
        num_envs,
    )
    out2 = out[["prompt_name", "model", "success_percentage", "done"]]
    return out.groupby("prompt_name"), out2


def analyse_data_new(input_data, num_envs=DEFAULT_NUM_ENVS):
    """Group by model / prompt_name / correction / resample."""
    out = _aggregate(
        input_data,
        ["model", "prompt_name", "correction", "resample"],
        ["model", "prompt_name", "correction", "resample", "env_idx", "success",
         "done", "early_stop", "error", "num_of_steps", "num_nothing_happens",
         "num_repetitions", "num_no_command", "total_in_token_accumulated",
         "total_out_token_accumulated", "num_correction"],
        num_envs,
    )
    out2 = out[["prompt_name", "model", "success_percentage", "done"]]
    return out.groupby("prompt_name"), out2


def no_groupby_analyse_data(input_data, num_envs=DEFAULT_NUM_ENVS):
    """Detailed table without collapsing away prompt/correction/resample."""
    return _aggregate(
        input_data,
        ["model", "prompt_name", "correction", "resample"],
        ["model", "prompt_name", "correction", "resample", "env_idx", "success",
         "done", "early_stop", "error", "num_of_steps"],
        num_envs,
    )


def create_pivot(in_data, variable="success", aggregation_function="sum"):
    """Pivot ``variable`` by model/prompt_name (rows) and env_type (columns)."""
    pd = require_pandas()
    if "env_type" not in in_data.columns:
        raise KeyError("create_pivot needs an 'env_type' column")

    pivot = pd.pivot_table(
        in_data,
        index=["model", "prompt_name"],
        columns=["env_type"],
        aggfunc={variable: aggregation_function},
    )
    if isinstance(pivot.columns, pd.MultiIndex):
        pivot.columns = pivot.columns.droplevel(0)
    pivot.columns.name = None
    return pivot.reset_index()


def summarise_trial(trial_name, base_folder=DEFAULT_BASE_FOLDER,
                    trial_base_name=DEFAULT_TRIAL_BASE_NAME,
                    csv_file_name=DEFAULT_CSV_NAME):
    """Return the same ``{score, num_items, num_successful}`` as scoring.py."""
    from stateact import scoring

    return scoring.score_dataframe(
        load_data(trial_name, base_folder, trial_base_name, csv_file_name)
    )


def main(argv=None):
    """CLI: ``python -m stateact.analysis.alfworld --trial-name ...``."""
    import argparse

    from stateact import scoring

    parser = argparse.ArgumentParser(description="Summarise one ALFWorld trial.")
    parser.add_argument("--trial-name", required=True)
    parser.add_argument("--base-folder", default=DEFAULT_BASE_FOLDER)
    parser.add_argument("--trial-base-name", default=DEFAULT_TRIAL_BASE_NAME)
    parser.add_argument("--csv-name", default=DEFAULT_CSV_NAME)
    args = parser.parse_args(argv)

    result = summarise_trial(
        args.trial_name, args.base_folder, args.trial_base_name, args.csv_name
    )
    print(scoring.format_score(result))
    return result


if __name__ == "__main__":
    main()
