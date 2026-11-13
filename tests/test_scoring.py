"""Tests for stateact.scoring."""

import pytest

from stateact import scoring

pd = pytest.importorskip("pandas")


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


def test_format_score_matches_historical_output():
    result = {"score": 0.8059701492537313, "num_successful": 108, "num_items": 134}
    assert scoring.format_score(result) == (
        "Overall (mean) Score: 0.805970 with 108 successful envs "
        "and a total of 134 envs."
    )


@pytest.mark.parametrize(
    "rewards,expected_score,expected_successful",
    [
        ([1, 0, 0, 1], 0.5, 2),
        ([1, 1, 1], 1.0, 3),
        ([], 0.0, 0),
    ],
)
def test_summarise_rewards(rewards, expected_score, expected_successful):
    result = scoring.summarise_rewards(rewards)
    assert result["score"] == pytest.approx(expected_score)
    assert result["num_items"] == len(rewards)
    assert result["num_successful"] == expected_successful


def test_results_path():
    assert scoring.results_path("demo") == "game_logs/alfworld_eval_demo/alfworld_results.csv"


def test_score_trial_reads_real_csv(tmp_path):
    trial_dir = tmp_path / "game_logs" / "alfworld_eval_demo"
    trial_dir.mkdir(parents=True)
    (trial_dir / "alfworld_results.csv").write_text("success\n1\n0\n1\n")

    result = scoring.score_trial("demo", base_folder=str(tmp_path / "game_logs"))
    assert result["score"] == pytest.approx(2 / 3)
    assert result["num_items"] == 3
    assert result["num_successful"] == 2


def test_main_prints_score(tmp_path, capsys):
    trial_dir = tmp_path / "game_logs" / "alfworld_eval_demo"
    trial_dir.mkdir(parents=True)
    (trial_dir / "alfworld_results.csv").write_text("success\n1\n1\n")

    result = scoring.main(
        ["--trial_name", "demo", "--base_folder", str(tmp_path / "game_logs")]
    )
    assert result["score"] == pytest.approx(1.0)
    assert "Overall (mean) Score: 1.000000" in capsys.readouterr().out
