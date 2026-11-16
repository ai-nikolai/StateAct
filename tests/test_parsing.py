"""Unit tests for stateact.parsing (standard library only)."""

import pytest

from stateact import parsing


@pytest.mark.parametrize(
    "name,expected",
    [
        ("pick_and_place_something", "put"),
        ("pick_clean_then_place_in_recep", "clean"),
        ("pick_heat_then_place_in_recep", "heat"),
        ("pick_cool_then_place_in_recep", "cool"),
        ("look_at_obj_in_light", "examine"),
        ("pick_two_obj_and_place", "puttwo"),
        ("totally_unknown_task", ""),
    ],
)
def test_get_env_type(name, expected):
    assert parsing.get_env_type(name) == expected


@pytest.mark.parametrize(
    "action,expected_action,expected_corrected",
    [
        ("put apple 1 on table 1", "move apple 1 to table 1", True),
        ("put apple 1 in fridge 1", "move apple 1 to fridge 1", True),
        ("put apple in fridge 1", "move apple in fridge 1", False),
        ("go north", "go north", False),
    ],
)
def test_transform_put_action(action, expected_action, expected_corrected):
    transformed, corrected = parsing.transform_put_action(action)
    assert transformed == expected_action
    assert corrected is expected_corrected


def test_transform_put_action_can_keep_put_syntax():
    transformed, corrected = parsing.transform_put_action(
        "put apple 1 on table 1", transform_to_move_syntax=False
    )
    assert transformed == "put apple 1 in/on table 1"
    assert corrected is True


@pytest.mark.parametrize(
    "function,expected",
    [
        (parsing.get_observation_agentbench_thought, "\n"),
        (parsing.get_observation_react_thought, "OK.\n"),
        (parsing.get_observation_jsonreact_thought, "OK.\n"),
    ],
)
def test_thought_observations(function, expected):
    assert function() == expected


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("> go north", "go north"),
        (">go north", "go north"),
        ("go north", "go north"),
    ],
)
def test_general_action_cleaning(raw, expected):
    assert parsing.general_action_cleaning(raw) == expected


@pytest.mark.parametrize(
    "raw,expected",
    [
        ('{"action": "go north"}', '{"action": "go north"}'),
        ('```json\n{"action": "go north"}\n```', '{"action": "go north"}'),
        ('```\n{"action": "go north"}\n```', '{"action": "go north"}'),
    ],
)
def test_json_action_cleaning_removes_only_the_fence(raw, expected):
    assert parsing.json_action_cleaning(raw) == expected


def test_json_action_cleaning_appends_closing_brace_to_truncated_json():
    assert parsing.json_action_cleaning('{"action": "go north"').rstrip().endswith("}")


@pytest.mark.parametrize("text", ["think: I should look", "think:I should look"])
def test_is_react_thought(text):
    assert parsing.is_react_thought(text)


def test_is_react_thought_false():
    assert not parsing.is_react_thought("action: look")


def test_is_jsonreact_thought():
    assert parsing.is_jsonreact_thought('{"think": "look"}')
    assert not parsing.is_jsonreact_thought('{"action": "look"}')


def test_is_agentbench_thought():
    assert parsing.is_agentbench_thought("THOUGHT: look")
    assert not parsing.is_agentbench_thought("ACTION: look")


def test_get_action_jsonreact_valid_json():
    action, was_command, valid_json = parsing.get_action_jsonreact(
        '{"think": "reason", "action": "go north"}'
    )
    assert (action, was_command, valid_json) == ("go north", True, True)


@pytest.mark.parametrize(
    "raw",
    [
        '"action" : "go north"',
        '"action": "go north"',
        '"action":"go north"',
    ],
)
def test_get_action_jsonreact_recovers_from_malformed_json(raw):
    action, was_command, valid_json = parsing.get_action_jsonreact(raw)
    assert (action, was_command, valid_json) == ("go north", True, False)


def test_get_action_jsonreact_version_one_always_uses_action_key():
    action, was_command, valid_json = parsing.get_action_jsonreact(
        '{"think": "reason", "action": "look"}', version=1, key="think"
    )
    assert action == "look"
    assert was_command is True
    assert valid_json is True


def test_get_action_jsonstate_matches_jsonreact():
    raw = '{"goal": "g", "action": "look"}'
    assert parsing.get_action_jsonstate(raw) == parsing.get_action_jsonreact(raw)


def test_get_action_jsonstate_without_action():
    assert parsing.get_action_jsonstate("just text") == ("just text", False, False)


def test_get_action_stringstate():
    action, was_command = parsing.get_action_stringstate("goal: g\nplan: p\naction: go north")
    assert action == "go north"
    assert was_command is True


def test_get_action_stringstate_without_action():
    assert parsing.get_action_stringstate("goal: g") == ("goal: g", False)


def test_get_action_agentbench():
    action, was_command = parsing.get_action_agentbench("THOUGHT: hmm\nACTION: look")
    assert action == " look"
    assert was_command is True


def test_get_action_agentbench_without_action():
    assert parsing.get_action_agentbench("THOUGHT: hmm") == ("THOUGHT: hmm", False)


@pytest.mark.parametrize(
    "raw,expected",
    [
        ('action("go north")', "go north"),
        ('{"action" : "go north"}', "go north"),
        ('{"action": "go north"}', "go north"),
        ('{"action":"go north"}', "go north"),
        ("ACTION: look", " look"),
    ],
)
def test_process_action(raw, expected):
    assert parsing.process_action(raw) == expected


def test_process_action_illegal_flag():
    raw = "no command here"
    action, illegal = parsing.process_action(raw, track_is_illegal=True)
    assert action == raw
    assert illegal is True


def test_process_ob_strips_arrival_prefix():
    assert parsing.process_ob("You arrive at loc 3. You see a table.") == "You see a table.\n"


def test_process_ob_adds_newline():
    assert parsing.process_ob("You are in the kitchen.") == "You are in the kitchen.\n"


def test_process_ob_tracks_nothing_happens():
    observation, nothing_happens = parsing.process_ob(
        "Nothing happens.", track_nothing_happens=True
    )
    assert observation == "Nothing happens.\n"
    assert nothing_happens is True
