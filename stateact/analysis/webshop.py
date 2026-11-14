"""WebShop analysis (thin wrapper over :mod:`stateact.analysis.core`)."""

from stateact.analysis.core import load_summary, summarise

__all__ = ["load_scores", "summarise_scores", "best_per_model", "main"]


def load_scores(path):
    """Load a unified ``summary.csv`` or a legacy WebShop ``scores.csv``."""
    frame = load_summary(path, benchmark="webshop")
    if "score" in frame.columns:
        frame["avg_score"] = frame["score"].astype(float)
    return frame


def summarise_scores(data, sort=True):
    return summarise(data, benchmark="webshop", sort=sort)


def best_per_model(data):
    """Return the best agent row (by score) for each model."""
    frame = summarise_scores(data)
    if "score" not in frame.columns:
        raise KeyError("No 'score' column in WebShop results")
    index = frame.groupby("model")["score"].idxmax()
    return frame.loc[index].reset_index(drop=True)


def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser(description="Summarise WebShop results")
    parser.add_argument("scores", help="Path to summary.csv / scores.csv")
    parser.add_argument("--best", action="store_true", help="Best agent per model")
    args = parser.parse_args(argv)

    frame = load_scores(args.scores)
    result = best_per_model(frame) if args.best else summarise_scores(frame)
    print(result.to_string(index=False))
    return result


if __name__ == "__main__":
    main()
