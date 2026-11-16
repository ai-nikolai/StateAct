"""Tests for the ScienceWorld env wrapper (no JVM required)."""

from stateact import ScienceWorldEnv
from stateact.main_loop import main_loop


class FakeScienceWorld:
    def __init__(self, final_score=10, final_done=False):
        self.final_score = final_score
        self.final_done = final_done
        self.loaded = None
        self.closed = False

    def load(self, task_name, variation, simplification):
        self.loaded = (task_name, variation, simplification)

    def reset(self):
        return "You are in a lab.", {"score": 0}

    def step(self, action):
        return "You see a thermometer.", 10, self.final_done, {
            "score": self.final_score,
        }

    def close(self):
        self.closed = True


def test_scienceworld_wrapper():
    raw = FakeScienceWorld()
    env = ScienceWorldEnv(
        "boil", variation=2, simplification="easy", env=raw
    )

    assert raw.loaded == ("boil", 2, "easy")
    observation = env.reset()
    assert observation == "You are in a lab."
    assert env.done is False
    assert env.score == 0

    observation = env.step("look around")
    assert observation == "You see a thermometer."
    assert env.reward == 10.0
    assert env.score == 10
    assert env.success is False

    env.close()
    assert raw.closed is True


def test_scienceworld_success_and_main_loop():
    raw = FakeScienceWorld(final_score=100, final_done=True)
    env = ScienceWorldEnv(env=raw)

    class Agent:
        def run_step(self, observation):
            return "look around", ""

        def reset(self):
            pass

    results = main_loop(Agent(), env, num_runs=1)
    assert results[0]["success"] is True
    assert env.score == 100
