"""WebShop ``scores.csv`` analysis."""

from stateact.analysis.common import require_pandas

__all__ = ["load_scores", "summarise_scores", "best_per_model", "main"]


def load_scores(path):
    """Load ``results/<run>/scores.csv`` produced by run_webshop_adapted.py."""
    return require_pandas().read_csv(path)


def summarise_scores(data, sort=True):
    """Return one row per (model, agent) with numeric score columns."""
    pd = require_pandas()
    numeric = ["avg_score", "success_rate", "failure_rate"]
    frame = data.copy()
    for column in numeric:
        if column in frame.columns:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")
    if sort:
        by = [column for column in ("model", "agent") if column in frame.columns]
        if by:
            frame = frame.sort_values(by)
    return frame.reset_index(drop=True)


def best_per_model(data):
    """Return the best agent row (by ``avg_score``) for each model."""
    frame = summarise_scores(data)
    if "avg_score" not in frame.columns:
        raise KeyError("scores.csv has no 'avg_score' column")
    index = frame.groupby("model")["avg_score"].idxmax()
    return frame.loc[index].reset_index(drop=True)


def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser(description="Summarise WebShop scores.csv")
    parser.add_argument("scores", help="Path to scores.csv")
    parser.add_argument("--best", action="store_true", help="Show best agent per model")
    args = parser.parse_args(argv)

    data = load_scores(args.scores)
    result = best_per_model(data) if args.best else summarise_scores(data)
    print(result.to_string(index=False))
    return result


if __name__ == "__main__":
    main()
