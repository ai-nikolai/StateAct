"""Unit tests for stateact.prompts."""

import pytest

from stateact import prompts


@pytest.mark.parametrize(
    "agent_type,prompt_ids,keys,version,expected",
    [
        ("react", [1, 0], [], 1, "react-1_0"),
        ("agentbench", [1, 0], [], 2, "agentbench-v2"),
        ("jsonreact", [1, 0], [], 3, "jsonreact-1_0-v3"),
        ("ours", [1, 0], ["goal", "action"], 1, "jsonstate-1_0-k-goal+action"),
        ("ours-text", [1, 0], ["goal", "action"], 1, "stringstate-1_0-k-goal+action"),
        ("stateact", [1, 0], ["goal", "action"], 1, "stringstate-1_0-k-goal+action"),
        ("act", [1, 0], ["goal", "action"], 1, "act-1_0"),
    ],
)
def test_prompt_name_for(agent_type, prompt_ids, keys, version, expected):
    assert prompts.prompt_name_for(agent_type, prompt_ids, keys, version) == expected


def test_prompt_name_for_rejects_unknown_agent():
    with pytest.raises(NotImplementedError):
        prompts.prompt_name_for("does-not-exist", [1], [], 1)


def test_generate_prompt_from_example_defaults():
    prompt = prompts.generate_prompt_from_example("EXAMPLES", number_of_examples=2)
    assert isinstance(prompt, list)
    assert prompt[0]["role"] == "system"
    content = prompt[0]["content"]
    assert prompts.BASE_PROMPT1 in content
    assert "Here are 2 examples:" in content
    assert "EXAMPLES" in content
    assert content.rstrip().endswith(prompts.TASK_MESSAGE)


def test_generate_prompt_from_example_singular_and_overrides():
    raw = prompts.generate_prompt_from_example(
        "EXAMPLES",
        return_raw_prompt=True,
        number_of_examples=1,
        base_prompt="BASE",
        instructions="INSTRUCTIONS",
        hints="HINTS",
    )
    assert "BASE" in raw
    assert "INSTRUCTIONS" in raw
    assert "Here is 1 example:" in raw
    assert "HINTS" in raw


def test_save_prompt_file(tmp_path):
    path = tmp_path / "prompt.txt"
    prompts.save_prompt_file(str(path), "hello")
    assert path.read_text() == "hello"


def _stub_builders(calls):
    def react(env_type, prompt_ids):
        calls.append(("react", env_type, prompt_ids))
        return "react-examples"

    def jsonreact(env_type, prompt_ids, version):
        calls.append(("jsonreact", env_type, prompt_ids, version))
        return "jsonreact-examples"

    def agentbench(env_type, return_base, version):
        calls.append(("agentbench", env_type, return_base, version))
        return "agentbench-examples", "agentbench-base"

    def stateact(env_type, prompt_ids, keys_to_use, key_renaming):
        calls.append(("stateact", env_type, prompt_ids, list(keys_to_use), dict(key_renaming)))
        return "stateact-examples"

    return {
        "react": react,
        "jsonreact": jsonreact,
        "agentbench": agentbench,
        "ours": stateact,
        "stateact": stateact,
    }


@pytest.mark.parametrize(
    "agent_type,expected_examples",
    [
        ("react", "react-examples"),
        ("jsonreact", "jsonreact-examples"),
        ("agentbench", "agentbench-examples"),
        ("ours", "stateact-examples"),
        ("ours-text", "stateact-examples"),
        ("stateact", "stateact-examples"),
        ("act", "stateact-examples"),
    ],
)
def test_get_prompt_example_dispatches_via_injected_builders(agent_type, expected_examples):
    calls = []
    name, example, base, number = prompts.get_prompt_example(
        agent_type,
        "clean",
        [1, 0],
        version=1,
        keys_to_use=["goal", "action"],
        key_renaming={"goal": "task"},
        builders=_stub_builders(calls),
    )
    assert isinstance(name, str)
    assert example == expected_examples
    # AgentBench always uses a single example; every other agent honours the
    # length of prompt_ids.
    assert number == (1 if agent_type == "agentbench" else 2)
    assert calls


def test_get_prompt_example_agentbench_forces_one_example():
    calls = []
    _name, _example, base, number = prompts.get_prompt_example(
        "agentbench",
        "clean",
        [1, 0],
        version=2,
        builders=_stub_builders(calls),
    )
    assert base == "agentbench-base"
    assert number == 1


def test_get_prompt_example_name_only_does_not_need_builders():
    name = prompts.get_prompt_example(
        "stateact", "clean", [1, 0], version=1, generate_prompt=False,
        keys_to_use=["action"],
    )
    assert name == "stringstate-1_0-k-action"


def test_get_prompt_example_rejects_unknown_agent():
    with pytest.raises(NotImplementedError):
        prompts.get_prompt_example("unknown", "clean", [1], 1, builders={})


def test_get_prompt_example_does_not_share_mutable_defaults():
    calls = []
    builders = _stub_builders(calls)
    prompts.get_prompt_example("stateact", "clean", [1], 1, builders=builders)
    prompts.get_prompt_example("stateact", "clean", [1], 1, builders=builders)
    first = calls[0][3]
    second = calls[1][3]
    assert first == [] and second == []


@pytest.mark.parametrize("env_type", sorted(prompts.BASE_EXAMPLE_MODULES))
def test_load_base_example_variants(env_type):
    variants = prompts.load_base_example_variants(env_type)
    assert len(variants) == 3
    assert all(isinstance(variant, list) for variant in variants)
    assert all(variants)


def test_load_base_example_variants_rejects_unknown_env():
    with pytest.raises(KeyError):
        prompts.load_base_example_variants("unknown-env")


def test_default_alfworld_builders():
    builders = prompts.default_alfworld_builders()
    for key in ("react", "jsonreact", "agentbench", "ours", "ours-text", "stateact"):
        assert callable(builders[key])


def test_default_alfworld_builders_end_to_end():
    name, example, base, number = prompts.get_prompt_example(
        "stateact",
        "clean",
        [1, 0],
        version=1,
        keys_to_use=["thought", "action"],
    )
    assert name == "stringstate-1_0-k-thought+action"
    assert isinstance(example, str) and example
    assert base == ""
    assert number == 2
