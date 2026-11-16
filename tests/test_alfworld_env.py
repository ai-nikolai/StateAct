"""Tests for the ALFWorld environment adapter (no alfworld install needed)."""

import sys

import pytest

from stateact.envs import AlfworldAdapter, AlfworldEnv
from stateact.envs.alfworld import load_config

CONFIG = {
    "dataset": {"num_eval_games": 1},
    "env": {"type": "AlfredTWEnv"},
}


class FakeEnv:
    def __init__(self, config, train_eval):
        self.config = config
        self.train_eval = train_eval
        self.reset_count = 0
        self.last_actions = None
        self.batch_size = None

    def init_env(self, batch_size):
        self.batch_size = batch_size
        return self

    def reset(self):
        self.reset_count += 1
        observation = ["You arrive somewhere.\n\nYou see a table.\n"]
        info = {
            "extra.gamefile": [
                "/data/valid_unseen/pick_and_place_simple/trial/game.tw-pddl"
            ]
        }
        return observation, info

    def step(self, actions):
        self.last_actions = actions
        return ["You see a chair.\n"], [1.0], [False], {"won": [False]}


def fake_factory(env_type):
    assert env_type == "AlfredTWEnv"
    return FakeEnv


def test_load_config(tmp_path):
    path = tmp_path / "config.yaml"
    path.write_text("env:\n  type: AlfredTWEnv\n")
    assert load_config(path) == {"env": {"type": "AlfredTWEnv"}}


def test_reset_returns_text_and_env_type():
    env = AlfworldAdapter(config=CONFIG, split="eval_out_of_distribution",
                      env_factory=fake_factory)
    observation, env_type = env.reset()

    assert observation == "You see a table.\n"
    assert env_type == "put"
    assert env.gamefile.endswith("game.tw-pddl")
    assert env.env.batch_size == 1
    assert env.env.train_eval == "eval_out_of_distribution"


def test_step_delegates_single_action():
    env = AlfworldAdapter(config=CONFIG, env_factory=fake_factory)
    observation, reward, done, info = env.step("look")

    assert observation == "You see a chair.\n"
    assert reward == 1.0
    assert done is False
    assert info == {"won": [False]}
    assert env.env.last_actions == ["look"]


def test_skip_resets_repeatedly():
    env = AlfworldAdapter(config=CONFIG, env_factory=fake_factory)
    env.skip(3)
    assert env.env.reset_count == 3


def test_adapter_does_not_import_alfworld():
    # In CI alfworld is not installed at all, so importing this module and
    # constructing an adapter with a fake factory must not touch it.
    AlfworldAdapter(config=CONFIG, env_factory=fake_factory)
    assert "alfworld" not in sys.modules


def test_missing_config_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        AlfworldAdapter(config_path=tmp_path / "missing.yaml", env_factory=fake_factory)


class FakeAdapter:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def reset(self):
        return "You see a table.\n", "put"

    def step(self, action):
        return "You see a chair.\n", 1.0, False, {"won": [False]}


def test_base_env_wrapper():
    env = AlfworldEnv("ood_test", adapter_factory=FakeAdapter)
    observation = env.reset()
    assert observation == "You see a table.\n"
    assert env.info["env_type"] == "put"
    assert env.done is False

    observation = env.step("look")
    assert observation == "You see a chair.\n"
    assert env.reward == 1.0
    assert env.done is False
    assert env.info == {"won": [False]}
