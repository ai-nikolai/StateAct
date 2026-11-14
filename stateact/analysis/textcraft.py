"""TextCraft analysis (thin wrapper over :mod:`stateact.analysis.core`)."""

import json

from stateact.analysis.core import load_summary, summarise

__all__ = ["load_results", "load_result_json", "summarise_results", "main"]


def load_results(path):
    """Load a unified ``summary.csv`` or a legacy TextCraft ``results.csv``."""
    frame = load_summary(path, benchmark="textcraft")
    if "rate" not in frame.columns and "score" in frame.columns:
        frame["rate"] = frame["score"]
    return frame


def load_result_json(path):
    """Load one of the per-run ``ADaPT_*.json`` trace files."""
    with open(path) as handle:
        return json.load(handle)


def summarise_results(data):
    """Aggregate repeated runs, keeping the historical ``rate``/``runs`` names."""
    frame = summarise(data, benchmark="textcraft", sort=False)
    if {"model", "agent"} <= set(frame.columns):
        grouped = frame.groupby(["model", "agent"])
        out = grouped.agg({
            "score": "mean",
            "success_rate": "mean",
            "failure_rate": "mean",
            "num_envs": "sum",
        }).reset_index()
        out["rate"] = out["score"]
        out["runs"] = grouped.size().values
        return out
    return frame


def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser(description="Summarise TextCraft results")
    parser.add_argument("results", help="Path to summary.csv / results.csv")
    args = parser.parse_args(argv)

    result = summarise_results(load_results(args.results))
    print(result.to_string(index=False))
    return result


if __name__ == "__main__":
    main()
