"""Tests for the notebook-compatible analysis subpackage."""

import pytest

from stateact.analysis import alfworld, textcraft, webshop
from stateact.analysis.common import clean_model_string

pd = pytest.importorskip("pandas")

ALFWORLD_CSV = """model,prompt_name,correction,resample,env_idx,env_type,success,done,early_stop,error,num_of_steps,num_nothing_happens,num_repetitions,num_no_command,total_in_token_accumulated,total_out_token_accumulated,num_correction,keys_removed
m1,p1,False,False,0,put,1,True,,,5,1,0,0,100,20,0,all
m1,p1,False,False,1,put,0,True,,,7,2,1,0,110,21,0,all
m2,p1,False,False,0,put,1,True,ENV_ERROR,,6,0,0,0,90,10,0,all
m2,p1,False,False,1,put,1,True,,,8,0,0,0,95,11,0,all
"""


@pytest.fixture
def alfworld_csv(tmp_path):
    path = tmp_path / "results.csv"
    path.write_text(ALFWORLD_CSV)
    return path


@pytest.fixture
def alfworld_frame(alfworld_csv):
    return alfworld.load_data(str(alfworld_csv))


def test_get_data_file_path():
    assert alfworld.get_data_file_path("demo") == "results/demo/episodes.csv"


@pytest.mark.parametrize("value,expected", [("", 0), ("x", 1), ("False", 1)])
def test_string_to_bool_int(value, expected):
    assert alfworld.convert_string_to_bool_int(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [("", 0), ("False", 0), ("(False,)", 0), ("True", 1), ("(True,)", 1),
     ("0", 0), ("1", 1)],
)
def test_bool_string_to_bool_int(value, expected):
    assert alfworld.convert_bool_string_to_bool_int(value) == expected


def test_load_data_converts_boolean_columns(alfworld_frame):
    assert list(alfworld_frame["early_stop"]) == [0, 0, 1, 0]
    assert list(alfworld_frame["error"]) == [0, 0, 0, 0]


def test_analyse_data_old(alfworld_frame):
    grouped, summary = alfworld.analyse_data_old(alfworld_frame, num_envs=2)
    assert summary["prompt_name"].tolist() == ["p1", "p1"]
    assert summary["model"].tolist() == ["m1", "m2"]
    assert summary["success_percentage"].tolist() == [50.0, 100.0]
    assert len(grouped.head()) == 2


def test_analyse_data_new_and_no_groupby(alfworld_frame):
    _grouped, summary = alfworld.analyse_data_new(alfworld_frame, num_envs=2)
    assert summary["success_percentage"].tolist() == [50.0, 100.0]

    detailed = alfworld.no_groupby_analyse_data(alfworld_frame, num_envs=2)
    assert {"model", "prompt_name", "success_percentage"} <= set(detailed.columns)


def test_analyse_data_basic(alfworld_frame):
    grouped, summary = alfworld.analyse_data_basic(alfworld_frame, num_envs=2)
    assert {"keys_removed", "model", "success_percentage", "done"} == set(
        summary.columns
    )
    assert len(grouped.head()) == 2


def test_analyse_data_basic_falls_back_to_keys_to_use(alfworld_frame):
    frame = alfworld_frame.drop(columns=["keys_removed"]).assign(keys_to_use="all")
    _grouped, summary = alfworld.analyse_data_basic(frame, num_envs=2)
    assert "keys_to_use" in summary.columns


def test_create_pivot(alfworld_frame):
    pivot = alfworld.create_pivot(alfworld_frame)
    assert {"model", "prompt_name", "put"} == set(pivot.columns)
    assert pivot["put"].tolist() == [1, 2]


def test_create_pivot_requires_env_type(tmp_path):
    with pytest.raises(KeyError):
        alfworld.create_pivot(pd.DataFrame({"model": ["m"], "prompt_name": ["p"]}))


def test_summarise_trial(tmp_path):
    trial_dir = tmp_path / "game_logs" / "alfworld_eval_demo"
    trial_dir.mkdir(parents=True)
    (trial_dir / "alfworld_results.csv").write_text(ALFWORLD_CSV)

    result = alfworld.summarise_trial(
        "demo", base_folder=str(tmp_path / "game_logs")
    )
    assert result["score"] == pytest.approx(0.75)
    assert result["num_items"] == 4
    assert result["num_successful"] == 3


def test_webshop_analysis(tmp_path):
    path = tmp_path / "scores.csv"
    path.write_text(
        "agent,date,model,avg_score,success_rate,failure_rate\n"
        "act,2026-01-01,m1,0.5,0.5,0.5\n"
        "react,2026-01-01,m1,0.7,0.7,0.3\n"
        "act,2026-01-01,m2,0.6,0.6,0.4\n"
    )
    frame = webshop.load_scores(path)
    summary = webshop.summarise_scores(frame)
    assert list(summary["model"]) == ["m1", "m1", "m2"]
    best = webshop.best_per_model(frame)
    assert best["agent"].tolist() == ["react", "act"]
    assert best["avg_score"].tolist() == [0.7, 0.6]


def test_textcraft_analysis(tmp_path):
    path = tmp_path / "results.csv"
    path.write_text(
        "agent,date,model,rate,total_count,average_depth,max_depth\n"
        "react,2026-01-01,m1,0.5,10,1.2,2\n"
        "react,2026-01-02,m1,0.7,10,1.4,2\n"
        "act,2026-01-01,m2,0.6,10,1.1,2\n"
    )
    summary = textcraft.summarise_results(textcraft.load_results(path))
    assert summary["model"].tolist() == ["m1", "m2"]
    assert summary["rate"].tolist() == pytest.approx([0.6, 0.6])
    assert summary["runs"].tolist() == [2, 1]


def test_clean_model_string():
    assert clean_model_string("Qwen/Qwen2.5-7B-Instruct") == (
        "qwen_qwen2-5-7b-instruct"
    )
