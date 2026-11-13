"""Tests for the YAML-backed experiment runner."""

import sys
import textwrap
from pathlib import Path

import pytest

from stateact import run_config

REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def alfworld_suite():
    return run_config.load_suite("alfworld")


@pytest.fixture(scope="module")
def webshop_suite():
    return run_config.load_suite("webshop")


def test_load_suite_from_name(alfworld_suite):
    assert alfworld_suite["suite"] == "alfworld"
    assert alfworld_suite["runner_dir"] == "alfworld_runs"
    assert alfworld_suite["python"] == "python3"


def test_load_suite_from_path(alfworld_suite):
    path = run_config.EXPERIMENTS_DIR + "/alfworld.yaml"
    assert run_config.load_suite(path)["suite"] == "alfworld"


def test_load_suite_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        run_config.load_suite("no-such-suite", experiments_dir=str(tmp_path))


@pytest.mark.parametrize("suite_name,expected_count", [("alfworld", 34), ("webshop", 4)])
def test_experiment_counts(suite_name, expected_count):
    suite = run_config.load_suite(suite_name)
    assert len(run_config.list_experiments(suite)) == expected_count


def _assert_suite_is_runnable(suite):
    runner_dir = REPO_ROOT / suite["runner_dir"]
    assert runner_dir.is_dir()
    for name in run_config.list_experiments(suite):
        commands = run_config.commands_for(suite, name)
        assert commands, f"{name} has no commands"
        for command in commands:
            assert set(command) >= {"script"}
            script = runner_dir / command["script"]
            assert script.is_file(), f"{name}: missing script {script}"
            args = command.get("args") or []
            assert all(isinstance(argument, str) for argument in args)
            assert all("\n" not in argument for argument in args)


def test_alfworld_suite_commands_are_runnable(alfworld_suite):
    _assert_suite_is_runnable(alfworld_suite)


def test_webshop_suite_commands_are_runnable(webshop_suite):
    _assert_suite_is_runnable(webshop_suite)


def test_commands_for_unknown_experiment(alfworld_suite):
    with pytest.raises(KeyError):
        run_config.commands_for(alfworld_suite, "no-such-experiment")


def test_format_command_quotes_arguments():
    rendered = run_config.format_command(
        "python3", "script.py", ["--name", "hello world", "--flag"]
    )
    assert rendered == "python3 script.py --name 'hello world' --flag"


def test_run_experiment_dry_run_does_not_execute(tmp_path, capsys):
    suite_path = tmp_path / "suite.yaml"
    suite_path.write_text(
        textwrap.dedent(
            """
            suite: demo
            runner_dir: .
            python: python3
            experiments:
              demo_exp:
                - script: demo.py
                  args: ["a b", "c"]
            """
        )
    )
    suite = run_config.load_suite(str(suite_path))
    results = run_config.run_experiment(suite, "demo_exp", dry_run=True, cwd=str(tmp_path))
    assert len(results) == 1
    command, returncode = results[0]
    assert returncode is None
    assert "'a b' c" in command
    assert not (tmp_path / "marker.txt").exists()
    assert "demo.py" in capsys.readouterr().out


def test_run_experiment_executes_and_reports_failures(tmp_path):
    (tmp_path / "ok.py").write_text("open('marker.txt', 'w').write('ran')\n")
    (tmp_path / "fail.py").write_text("raise SystemExit(3)\n")
    suite_path = tmp_path / "suite.yaml"
    suite_path.write_text(
        textwrap.dedent(
            f"""
            suite: demo
            runner_dir: {tmp_path}
            python: {sys.executable}
            experiments:
              mixed:
                - script: ok.py
                - script: fail.py
            """
        )
    )
    suite = run_config.load_suite(str(suite_path))
    results = run_config.run_experiment(suite, "mixed", cwd=str(tmp_path))
    assert [returncode for _command, returncode in results] == [0, 3]
    assert (tmp_path / "marker.txt").read_text() == "ran"


def test_main_lists_experiments(capsys):
    assert run_config.main(["alfworld", "--list"]) == 0
    output = capsys.readouterr().out
    assert "34 experiments" in output
    assert "eval_mix" in output


def test_main_unknown_suite_returns_error(capsys, tmp_path):
    assert run_config.main(["no-such-suite", "--experiments-dir", str(tmp_path)]) == 2
    assert "No experiment table" in capsys.readouterr().err


def test_main_unknown_experiment_returns_error(capsys):
    assert run_config.main(["alfworld", "no-such-experiment", "--dry-run"]) == 2
    assert "Unknown experiment" in capsys.readouterr().err


def test_main_dry_run(alfworld_suite, capsys):
    assert run_config.main([
        "alfworld", "test", "--dry-run", "--cwd", str(REPO_ROOT / "alfworld_runs"),
    ]) == 0
    captured = capsys.readouterr()
    assert "alfworld_run.py" in captured.out
    assert "All" not in captured.out
