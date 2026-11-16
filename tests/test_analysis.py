"""Tests for the unified analysis API."""

import pytest

from stateact import results
from stateact.analysis import (
    load_episodes,
    load_summary,
    require_pandas,
    summarise,
    to_frame,
)
from stateact.analysis.__main__ import main

pd = pytest.importorskip("pandas")


def _make_run(tmp_path, benchmark, trial, agent="stateact", model="m"):
    logger = results.RunLogger(
        benchmark, agent=agent, model=model, trial=trial,
        results_folder=str(tmp_path), num_envs=2,
    )
    logger.log_episode(
        env_idx=0, env_type="put", success=True, done=True, reward=1,
        steps=4, details={"prompt_name": "p1", "keys_to_use": ["goal", "action"]},
    )
    logger.log_episode(
        env_idx=1, env_type="clean", success=False, done=True, reward=0,
        steps=6, early_stop="ENV_ERROR: Repetitions",
    )
    logger.finish()
    return tmp_path / trial


def test_load_episodes_returns_dataframe(tmp_path):
    run = _make_run(tmp_path, "alfworld", "demo")
    frame = load_episodes(run)

    assert isinstance(frame, pd.DataFrame)
    assert len(frame) == 2
    assert frame["success"].tolist() == [1, 0]
    assert frame["prompt_name"].iloc[0] == "p1"
    assert isinstance(frame["keys_to_use"].iloc[0], str)


def test_load_summary_returns_dataframe(tmp_path):
    run = _make_run(tmp_path, "webshop", "demo", agent="act")
    frame = load_summary(run)

    assert len(frame) == 1
    assert frame["benchmark"].iloc[0] == "webshop"
    assert frame["agent"].iloc[0] == "act"
    assert frame["num_envs"].iloc[0] == 2
    assert frame["score"].iloc[0] == pytest.approx(0.5)


def test_summarise_accepts_path_and_dataframe(tmp_path):
    run = _make_run(tmp_path, "textcraft", "demo", agent="react")
    from_path = summarise(run)
    from_frame = summarise(from_path)
    assert from_path.equals(from_frame)


def test_to_frame_and_require_pandas():
    frame = to_frame([{"a": 1}, {"a": 2}])
    assert frame["a"].tolist() == [1, 2]
    assert require_pandas() is pd


def test_cli_alfworld(tmp_path, capsys):
    _make_run(tmp_path, "alfworld", "demo")
    main([
        "alfworld", "--trial-name", "demo", "--base-folder", str(tmp_path),
    ])
    assert "0.5" in capsys.readouterr().out


def test_cli_webshop_best(tmp_path, capsys):
    _make_run(tmp_path, "webshop", "demo", agent="act")
    main(["webshop", str(tmp_path / "demo"), "--best"])
    assert "act" in capsys.readouterr().out
