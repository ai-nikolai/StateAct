"""Tests for the unified result format."""

import csv
import json

from stateact import results


def _read(path):
    with open(path, newline="") as handle:
        return list(csv.DictReader(handle))


def test_run_logger_writes_unified_files(tmp_path):
    logger = results.RunLogger(
        "alfworld", agent="stateact", model="m", trial="demo",
        results_folder=str(tmp_path), split="eval", num_envs=2,
    )
    logger.log_episode(
        env_idx=0, env_type="put", success=True, done=True, reward=1.0,
        steps=5, details={"num_repetitions": 1},
    )
    logger.log_episode(
        env_idx=1, env_type="clean", success=False, done=False, reward=0.0,
        steps=7, early_stop="ENV_ERROR: Repetitions",
    )
    summary = logger.finish()

    episodes = _read(tmp_path / "demo" / "episodes.csv")
    assert len(episodes) == 2
    assert list(episodes[0]) == results.EPISODE_FIELDS
    assert episodes[0]["success"] == "1"
    assert episodes[1]["early_stop"].startswith("ENV_ERROR")

    summaries = _read(tmp_path / "demo" / "summary.csv")
    assert len(summaries) == 1
    assert list(summaries[0]) == results.SUMMARY_FIELDS
    assert float(summaries[0]["score"]) == 0.5
    assert float(summaries[0]["avg_steps"]) == 6.0
    assert summary["run_id"]


def test_load_episodes_flattens_details(tmp_path):
    logger = results.RunLogger(
        "alfworld", agent="stateact", model="m", trial="demo",
        results_folder=str(tmp_path),
    )
    logger.log_episode(
        env_idx=3, success=True, done=True, reward=1.0, steps=4,
        details={"prompt_name": "stringstate", "num_repetitions": 2},
    )
    logger.finish()

    rows = results.load_episodes(tmp_path / "demo", benchmark="alfworld")
    assert rows[0]["prompt_name"] == "stringstate"
    assert rows[0]["num_repetitions"] == 2
    assert rows[0]["steps"] == 4
    assert json.loads(rows[0]["details"])["prompt_name"] == "stringstate"


def test_load_summary_new_run(tmp_path):
    logger = results.RunLogger(
        "webshop", agent="act", model="m", trial="demo",
        results_folder=str(tmp_path), num_envs=2,
    )
    logger.log_episode(env_idx=0, success=True, reward=0.5, steps=10)
    logger.log_episode(env_idx=1, success=False, reward=0.0, steps=12)
    logger.finish(score=0.25, success_rate=0.5, failure_rate=0.0)

    rows = results.load_summary(tmp_path / "demo", benchmark="webshop")
    assert len(rows) == 1
    assert rows[0]["benchmark"] == "webshop"
    assert rows[0]["score"] == 0.25
    assert rows[0]["success_rate"] == 0.5
    assert rows[0]["num_envs"] == 2


def test_load_webshop_legacy_scores(tmp_path):
    path = tmp_path / "scores.csv"
    path.write_text(
        "agent,date,model,avg_score,success_rate,failure_rate\n"
        "act,2026-01-01,m1,0.5,0.4,0.1\n"
    )
    rows = results.load_summary(path, benchmark="webshop")
    assert rows[0]["score"] == 0.5
    assert rows[0]["success_rate"] == 0.4
    assert rows[0]["failure_rate"] == 0.1


def test_load_textcraft_legacy_results(tmp_path):
    path = tmp_path / "results.csv"
    path.write_text(
        "agent,date,model,rate,total_count,average_depth,max_depth\n"
        "react,2026-01-01,m1,0.6,100,1.5,3\n"
    )
    rows = results.load_summary(path, benchmark="textcraft")
    assert rows[0]["score"] == 0.6
    assert rows[0]["success_rate"] == 0.6
    assert rows[0]["num_envs"] == 100
    assert rows[0]["average_depth"] == "1.5"


def test_load_alfworld_legacy_episodes_as_summary(tmp_path):
    path = tmp_path / "alfworld_results.csv"
    path.write_text(
        "env_idx,env_type,success,done,total_reward,num_of_steps,error,early_stop\n"
        '0,put,True,True,1,5,,\n'
        '1,clean,False,True,0,7,,\n'
    )
    rows = results.load_summary(path, benchmark="alfworld")
    assert rows[0]["num_envs"] == 2
    assert rows[0]["score"] == 0.5
    assert rows[0]["avg_steps"] == 6.0
