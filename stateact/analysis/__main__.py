"""CLI: ``python -m stateact.analysis <alfworld|webshop|textcraft> ...``."""

import argparse

from stateact import results
from stateact.analysis import summarise, to_frame


def _print(frame):
    print(frame.to_string(index=False))
    return frame


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Analyse StateAct results (unified summary.csv format)."
    )
    subparsers = parser.add_subparsers(dest="benchmark", required=True)

    alfworld = subparsers.add_parser("alfworld", help="ALFWorld summary")
    alfworld.add_argument("--trial-name", required=True)
    alfworld.add_argument("--base-folder", default="alfworld_runs/results")

    webshop = subparsers.add_parser("webshop", help="WebShop summary")
    webshop.add_argument("run", help="Run directory containing summary.csv")
    webshop.add_argument("--best", action="store_true", help="Best agent per model")

    textcraft = subparsers.add_parser("textcraft", help="TextCraft summary")
    textcraft.add_argument("run", help="Run directory containing summary.csv")

    args = parser.parse_args(argv)

    if args.benchmark == "alfworld":
        rows = results.load_run(
            "alfworld", args.trial_name, results_folder=args.base_folder
        )
        return _print(to_frame(rows))

    frame = summarise(args.run)
    if args.benchmark == "webshop" and args.best and not frame.empty:
        index = frame.groupby("model")["score"].idxmax()
        frame = frame.loc[index].reset_index(drop=True)
    return _print(frame)


if __name__ == "__main__":
    main()
