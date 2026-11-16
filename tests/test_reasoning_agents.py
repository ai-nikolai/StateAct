"""Tests for the reasoning agents and main loop."""

import pytest

from stateact import agents
from stateact.envs import BaseEnv
from stateact.main_loop import main_loop


class FakeLLM:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.prompts = []

    def __call__(self, prompt, stop=None):
        self.prompts.append(prompt)
        return next(self.responses)


def test_react_agent_auto_ok_turn():
    llm = FakeLLM(["think: I should look around", "action: go north"])
    agent = agents.ReActAgent(llm=llm, max_turns=2)

    action, state = agent.run_step("You are in a room.")

    assert action == "go north"
    assert state == {"thought": "I should look around"}
    assert any(entry["role"] == "user" and entry["content"] == "OK."
               for entry in agent.history)
    assert "OK." in llm.prompts[1]


def test_react_agent_bare_action():
    agent = agents.ReActAgent(llm=FakeLLM(["look"]))
    assert agent.run_step("obs")[0] == "look"


def test_agentbench_agent():
    agent = agents.AgentBenchAgent(
        llm=FakeLLM(["THOUGHT: check the room\nACTION: look"])
    )
    action, state = agent.run_step("obs")
    assert action == "look"
    assert state == {"thought": "check the room"}


def test_stateact_string_agent():
    agent = agents.StateActAgent(
        llm=FakeLLM([
            "goal: find an apple\n"
            "current_location: kitchen\n"
            "thought: look in the fridge\n"
            "action: go to fridge 1"
        ]),
        format="string",
        prompt_order=["goal", "current_location", "thought", "action"],
    )
    action, state = agent.run_step("obs")
    assert action == "go to fridge 1"
    assert state["goal"] == "find an apple"
    assert state["current_location"] == "kitchen"
    assert state["thought"] == "look in the fridge"


def test_stateact_json_agent():
    agent = agents.StateActAgent(
        llm=FakeLLM([
            '```json\n{"goal": "find an apple", '
            '"thought": "check fridge", "action": "look"}\n```'
        ]),
        format="json",
        prompt_order=["goal", "thought", "action"],
    )
    action, state = agent.run_step("obs")
    assert action == "look"
    assert state == {"goal": "find an apple", "thought": "check fridge"}


def test_stateact_format_examples():
    agent = agents.StateActAgent(
        llm=FakeLLM(["goal: g\nthought: t\naction: a"]),
        format="string",
        prompt_order=["goal", "thought", "action"],
        example_trajectories=[
            {"goal": "g", "thought": "t", "action": "a"}
        ],
    )
    prompt = agent.build_prompt()
    assert "goal: g" in prompt
    assert "thought: t" in prompt


def test_agent_raises_without_action():
    agent = agents.ReActAgent(
        llm=FakeLLM(["think: still thinking", "think: again"]),
        max_turns=2,
    )
    with pytest.raises(RuntimeError, match="did not produce an action"):
        agent.run_step("obs")


class RecordingAgent:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.observations = []
        self.reset_count = 0
        self.finish_count = 0

    def run_step(self, observation):
        self.observations.append(observation)
        response = next(self.responses, ("look", ""))
        if isinstance(response, Exception):
            raise response
        return response

    def reset(self):
        self.reset_count += 1

    def finish_episode(self, **kwargs):
        self.finish_count += 1


def test_reflexion_adds_reflections_to_observation():
    base = RecordingAgent([("look", "")])
    agent = agents.ReflexionAgent(base, llm=FakeLLM(["be more careful"]))
    agent.reflect("failed obs", "bad action", reward=0)
    agent.run_step("next obs")
    assert "Reflections from previous attempts" in base.observations[0]
    assert "be more careful" in base.observations[0]


def test_reflexion_finish_episode():
    base = RecordingAgent([])
    agent = agents.ReflexionAgent(base, llm=FakeLLM(["reflection"]))
    agent.finish_episode(reward=0, success=False)
    assert agent.reflections == ["reflection"]
    agent.finish_episode(reward=1, success=True)
    assert agent.reflections == ["reflection"]


def test_adapt_retries_with_plan():
    class FailingAgent:
        def __init__(self):
            self.calls = 0
            self.observations = []

        def run_step(self, observation):
            self.observations.append(observation)
            self.calls += 1
            if self.calls == 1:
                raise RuntimeError("no action")
            return "look", ""

        def reset(self):
            pass

    base = FailingAgent()
    agent = agents.AdaptAgent(base, llm=FakeLLM(["1. inspect"]), max_depth=1)
    action, state = agent.run_step("obs")
    assert action == "look"
    assert state == ""
    assert "Suggested plan" in base.observations[1]


class FakeEnv(BaseEnv):
    def __init__(self):
        super().__init__()
        self.steps = 0
        self.reset_count = 0

    def reset(self):
        self.reset_count += 1
        self.steps = 0
        self.done = False
        self.reward = 0.0
        self.info = {}
        return "start"

    def step(self, action):
        self.steps += 1
        self.reward = 1.0 if self.steps == 2 else 0.0
        self.done = self.steps >= 2
        return f"step-{self.steps}"


def test_main_loop_runs_episodes():
    agent = RecordingAgent([("a", ""), ("b", ""), ("c", ""), ("d", "")])
    env = FakeEnv()
    results = main_loop(agent, env, num_runs=2, max_steps=10)

    assert len(results) == 2
    assert all(result["steps"] == 2 for result in results)
    assert all(result["success"] for result in results)
    assert agent.reset_count == 2
    assert agent.finish_count == 2


def test_main_loop_preserve_context():
    agent = RecordingAgent([("a", "")])
    env = FakeEnv()
    main_loop(agent, env, num_runs=1, preserve_context=True)
    assert agent.reset_count == 0
