"""Tests for stateact.scoring."""

import pytest

from stateact import results, scoring

pd = pytest.importorskip("pandas")


def _make_run(base, trial="demo"):
    logger = results.RunLogger(
        "alfworld", agent="stateact", model="m", trial=trial,
        results_folder=str(base), num_envs=3,
    )
    for idx, success in enumerate([True, False, True]):
        logger.log_episode(
            env_idx=idx, success=success, done=True, reward=int(success), steps=1
        )
    logger.finish()


def test_score_dataframe():
    frame = pd.DataFrame({"success": [1, 0, 1, 1]})
    result = scoring.score_dataframe(frame)
    assert result["score"] == pytest.approx(0.75)
    assert result["num_items"] == 4
    assert result["num_successful"] == 3


def test_score_dataframe_coerces_strings():
    frame = pd.DataFrame({"success": ["1", "0", "1"]})
    result = scoring.score_dataframe(frame)
    assert result["score"] == pytest.approx(2 / 3)
    assert result["num_successful"] == 2


def test_score_dataframe_custom_column():
    frame = pd.DataFrame({"won": [1, 0]})
    result = scoring.score_dataframe(frame, success_column="won")
    assert result["score"] == pytest.approx(0.5)


def test_format_score():
    result = {"score": 0.8059701492537313, "num_successful": 108, "num_items": 134}
    assert scoring.format_score(result) == (
        "Overall (mean) Score: 0.805970 with 108 successful envs "
        "and a total of 134 envs."
    )


@pytest.mark.parametrize(
    "rewards,expected_score,expected_successful",
    [([1, 0, 0, 1], 0.5, 2), ([1, 1, 1], 1.0, 3), ([], 0.0, 0)],
)
def test_summarise_rewards(rewards, expected_score, expected_successful):
    result = scoring.summarise_rewards(rewards)
    assert result["score"] == pytest.approx(expected_score)
    assert result["num_items"] == len(rewards)
    assert result["num_successful"] == expected_successful


@pytest.mark.parametrize(
    "value,expected",
    [("True", 1), ("False", 0), ("1", 1), ("0", 0), ("true", 1), ("", 0)],
)
def test_to_success(value, expected):
    assert scoring._to_success(value) == expected


def test_score_rows_without_pandas():
    rows = [{"success": "True"}, {"success": "False"}, {"success": "1"}]
    result = scoring.score_dataframe(rows)
    assert result["score"] == pytest.approx(2 / 3)
    assert result["num_items"] == 3
    assert result["num_successful"] == 2


def test_results_path():
    assert scoring.results_path("demo") == "results/demo/episodes.csv"


def test_load_results_reads_unified_episodes(tmp_path):
    base = tmp_path / "results"
    _make_run(base)
    rows = scoring.load_results("demo", base_folder=str(base))
    assert isinstance(rows, list)
    assert len(rows) == 3
    assert sum(row["success"] for row in rows) == 2


def test_score_trial(tmp_path):
    base = tmp_path / "results"
    _make_run(base)
    result = scoring.score_trial("demo", base_folder=str(base))
    assert result["score"] == pytest.approx(2 / 3)
    assert result["num_items"] == 3
    assert result["num_successful"] == 2


def test_main_prints_score(tmp_path, capsys):
    base = tmp_path / "results"
    _make_run(base)
    result = scoring.main(
        ["--trial_name", "demo", "--base_folder", str(base)]
    )
    assert result["score"] == pytest.approx(2 / 3)
    assert "Overall (mean) Score: 0.666667" in capsys.readouterr().out
