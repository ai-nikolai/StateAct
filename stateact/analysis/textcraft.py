"""TextCraft ``results.csv`` / JSON analysis."""

import json

from stateact.analysis.common import require_pandas

__all__ = ["load_results", "load_result_json", "summarise_results", "main"]


def load_results(path):
    """Load the ``results.csv`` appended by run_textcraft_adapt.py."""
    return require_pandas().read_csv(path)


def load_result_json(path):
    """Load one of the per-run ``ADaPT_*.json`` result files."""
    with open(path) as handle:
        return json.load(handle)


def summarise_results(data):
    """Aggregate repeated runs by (model, agent), averaging the rate."""
    pd = require_pandas()
    frame = data.copy()
    for column in ("rate", "total_count", "average_depth", "max_depth"):
        if column in frame.columns:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")

    group_columns = [column for column in ("model", "agent") if column in frame.columns]
    if not group_columns:
        return frame.reset_index(drop=True)

    aggregation = {
        column: "mean"
        for column in ("rate", "total_count", "average_depth", "max_depth")
        if column in frame.columns
    }
    if "date" in frame.columns:
        aggregation["date"] = "count"
    out = frame.groupby(group_columns).agg(aggregation).reset_index()
    if "date" in out.columns:
        out = out.rename(columns={"date": "runs"})
    return out


def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser(description="Summarise TextCraft results.csv")
    parser.add_argument("results", help="Path to results.csv")
    args = parser.parse_args(argv)

    result = summarise_results(load_results(args.results))
    print(result.to_string(index=False))
    return result


if __name__ == "__main__":
    main()
