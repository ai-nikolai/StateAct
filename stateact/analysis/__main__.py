"""CLI: ``python -m stateact.analysis <alfworld|webshop|textcraft> ...``."""

import argparse

from stateact.analysis import alfworld, textcraft, webshop


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Analyse StateAct benchmark result logs."
    )
    subparsers = parser.add_subparsers(dest="benchmark", required=True)

    alfworld_parser = subparsers.add_parser("alfworld", help="ALFWorld results CSV")
    alfworld_parser.add_argument("--trial-name", required=True)
    alfworld_parser.add_argument("--base-folder", default=alfworld.DEFAULT_BASE_FOLDER)
    alfworld_parser.add_argument("--trial-base-name",
                                 default=alfworld.DEFAULT_TRIAL_BASE_NAME)
    alfworld_parser.add_argument("--csv-name", default=alfworld.DEFAULT_CSV_NAME)

    webshop_parser = subparsers.add_parser("webshop", help="WebShop scores.csv")
    webshop_parser.add_argument("scores")
    webshop_parser.add_argument("--best", action="store_true")

    textcraft_parser = subparsers.add_parser("textcraft", help="TextCraft results.csv")
    textcraft_parser.add_argument("results")

    args = parser.parse_args(argv)

    if args.benchmark == "alfworld":
        return alfworld.main([
            "--trial-name", args.trial_name,
            "--base-folder", args.base_folder,
            "--trial-base-name", args.trial_base_name,
            "--csv-name", args.csv_name,
        ])
    if args.benchmark == "webshop":
        extra = ["--best"] if args.best else []
        return webshop.main([args.scores, *extra])
    return textcraft.main([args.results])


if __name__ == "__main__":
    main()
