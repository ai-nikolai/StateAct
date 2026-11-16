"""Config-driven runner for the named experiments.

Historically each benchmark had a long shell script of the form::

    if [ $1 == "eval_mix" ]; then
        python3 alfworld_run.py --agent ours --llm_type OpenAIChatText ... \\
        ...
    fi;

with ~1000 lines of that for ALFWorld and a smaller copy for WebShop. This
module replaces the repetition with a table (``experiments/*.yaml``) and a
single runner.

The tables were generated mechanically from the original shell scripts, so the
argv for every experiment is byte-for-byte what the shell used to execute. The
shell scripts remain as thin wrappers with the same interface:

    bash alfworld_runs/run_alfworld_eval.sh eval_mix
    python3 stateact/run_config.py alfworld eval_mix --dry-run

Commands are executed with an argv list (never through a shell), so a recorded
argument such as ``["goal","thought","action"]`` reaches the program intact.
"""

import argparse
import os
import shlex
import subprocess
import sys

__all__ = [
    "EXPERIMENTS_DIR",
    "load_suite",
    "list_experiments",
    "commands_for",
    "format_command",
    "run_experiment",
    "main",
]

EXPERIMENTS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "experiments")


def _load_yaml(path):
    try:
        import yaml
    except ImportError as exc:  # pragma: no cover - depends on environment
        raise ImportError(
            "Reading the experiment tables needs PyYAML (pip install pyyaml)."
        ) from exc

    with open(path, "r") as handle:
        return yaml.safe_load(handle)


def load_suite(suite, experiments_dir=EXPERIMENTS_DIR):
    """Load the YAML table for ``suite`` (e.g. ``"alfworld"``).

    Returns the parsed dict with keys ``suite``, ``runner_dir``, ``python`` and
    ``experiments``.
    """
    path = suite
    if not os.path.isfile(path):
        path = os.path.join(experiments_dir, f"{suite}.yaml")
    if not os.path.isfile(path):
        raise FileNotFoundError(
            f"No experiment table for {suite!r} (looked for {path})."
        )
    return _load_yaml(path)


def list_experiments(config):
    """Return the experiment names in the order they appear in the table."""
    return list(config["experiments"].keys())


def commands_for(config, name):
    """Return the list of ``{"script", "args"}`` commands for one experiment."""
    experiments = config["experiments"]
    if name not in experiments:
        raise KeyError(
            f"Unknown experiment {name!r}. Available: {', '.join(experiments)}"
        )
    return experiments[name]


def format_command(python, script, args):
    """Render one command as a copy-pasteable shell string (for display only)."""
    return " ".join(shlex.quote(part) for part in [python, script, *args])


def run_experiment(config, name, dry_run=False, python=None, cwd=None):
    """Run (or with ``dry_run``, just print) every command of one experiment.

    Mirrors the original shell behaviour in that a failing command does not stop
    the remaining ones - the old scripts had no ``set -e`` - but the failures are
    collected and the caller is told via the return value.

    Returns a list of ``(command_string, returncode_or_None)``; ``None`` marks a
    command that was not run (dry run).
    """
    commands = commands_for(config, name)
    python = python or config.get("python", "python3")
    runner_dir = cwd or config.get("runner_dir") or "."

    if not os.path.isdir(runner_dir):
        raise NotADirectoryError(
            f"runner_dir {runner_dir!r} for suite {config.get('suite')!r} does not exist. "
            f"Run from the repository root, or pass --cwd."
        )

    results = []
    for index, command in enumerate(commands, start=1):
        script, args = command["script"], list(command.get("args") or [])
        rendered = format_command(python, script, args)
        prefix = f"[{index}/{len(commands)}]"
        if dry_run:
            print(f"{prefix} {rendered}")
            results.append((rendered, None))
            continue

        print(f"{prefix} {rendered}", flush=True)
        completed = subprocess.run([python, script, *args], cwd=runner_dir)
        results.append((rendered, completed.returncode))
        if completed.returncode != 0:
            print(f"{prefix} EXIT {completed.returncode}", file=sys.stderr, flush=True)

    return results


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Run a named experiment from experiments/<suite>.yaml.",
        epilog="Examples:  run_config.py alfworld --list\n"
               "           run_config.py alfworld eval_mix --dry-run\n"
               "           run_config.py alfworld test_ours")
    parser.add_argument("suite", help="Experiment suite, e.g. alfworld or webshop")
    parser.add_argument("experiment", nargs="?",
                        help="Experiment name (omit with --list)")
    parser.add_argument("--list", action="store_true", help="List experiments and exit")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print the commands without running them")
    parser.add_argument("--python", default=None,
                        help="Interpreter to use (default: the table's `python`, i.e. python3)")
    parser.add_argument("--cwd", default=None,
                        help="Override the table's runner_dir")
    parser.add_argument("--experiments-dir", default=EXPERIMENTS_DIR,
                        help="Directory holding the YAML tables")
    args = parser.parse_args(argv)

    try:
        config = load_suite(args.suite, experiments_dir=args.experiments_dir)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        available = sorted(
            name[:-5] for name in os.listdir(args.experiments_dir)
            if name.endswith(".yaml")) if os.path.isdir(args.experiments_dir) else []
        if available:
            print(f"available suites: {', '.join(available)}", file=sys.stderr)
        return 2

    if args.list or not args.experiment:
        names = list_experiments(config)
        print(f"{config.get('suite', args.suite)}: {len(names)} experiments "
              f"(runner_dir={config.get('runner_dir')})")
        for name in names:
            print(f"  {name:32s} {len(commands_for(config, name))} command(s)")
        if not args.experiment and not args.list:
            print("\nPass an experiment name to run one; --dry-run to only print.")
        return 0

    try:
        results = run_experiment(config, args.experiment, dry_run=args.dry_run,
                                 python=args.python, cwd=args.cwd)
    except KeyError as exc:
        # Unknown experiment name: the message already lists what is available.
        print(f"error: {exc.args[0] if exc.args else exc}", file=sys.stderr)
        return 2
    except (FileNotFoundError, NotADirectoryError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.dry_run:
        return 0

    failures = [(cmd, rc) for cmd, rc in results if rc not in (0, None)]
    if failures:
        print(f"\n{len(failures)} of {len(results)} command(s) failed:", file=sys.stderr)
        for cmd, rc in failures:
            print(f"  exit {rc}: {cmd}", file=sys.stderr)
        return 1
    print(f"\nAll {len(results)} command(s) succeeded.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
