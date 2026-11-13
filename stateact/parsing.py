"""Action / observation parsing for StateAct agents.

This module holds the string-level parsing helpers that extract a concrete
action from an LLM response, and the helpers that normalise environment
observations.  It is deliberately dependency-free (only the standard library)
so it can be imported and unit-tested without alfworld / vllm / llamp
installed.

The functions here were extracted verbatim from
``alfworld_runs/alfworld_run.py`` so that behaviour is bit-for-bit unchanged;
``alfworld_run.py`` re-imports them for backwards compatibility.

Each agent format has its own extractor because the paper compares several:

===============  ===========================================================
format           expected model output
===============  ===========================================================
React            ``think: ...`` then ``action: ...``
JSON ReAct       ``{"think": "...", "action": "..."}``
AgentBench       ``THOUGHT: ...`` then ``ACTION: ...``
StateAct (json)  ``{"goal": ..., "plan": ..., "action": ...}``
StateAct (text)  ``goal: ...`` / ``plan: ...`` / ``action: ...`` lines
===============  ===========================================================
"""

import json
import re

__all__ = [
    "ENV_TYPES",
    "get_env_type",
    "transform_put_action",
    "get_observation_agentbench_thought",
    "get_observation_react_thought",
    "get_observation_jsonreact_thought",
    "general_action_cleaning",
    "json_action_cleaning",
    "our_text_action_cleaning",
    "nojson_action_cleaning",
    "is_react_thought",
    "is_jsonreact_thought",
    "is_agentbench_thought",
    "get_action_jsonreact",
    "get_action_jsonstate",
    "get_action_stringstate",
    "get_action_agentbench",
    "process_action",
    "process_ob",
]


#################################################################
#GAME LOOP & ENV Related
#################################################################

ENV_TYPES = {
    'pick_and_place': 'put',
    'pick_clean_then_place': 'clean',
    'pick_heat_then_place': 'heat',
    'pick_cool_then_place': 'cool',
    'look_at_obj': 'examine',
    'pick_two_obj': 'puttwo'
}

def get_env_type(env_name):
    """ Extracts which type of env it is"""
    env_type = ""
    for key, value in ENV_TYPES.items():
        if env_name.startswith(key):
            env_type = value
    return env_type


def transform_put_action(action, transform_to_move_syntax=True):
    """ Put action grammar correction. """
    put_regex_1 = r"""put(?:\s\w+)(?:\s\w+)?(?:\s\d+)\son(?:\s\w+)(?:\s\w+)?(?:\s\d+)"""
    put_regex_2 = r"""put(?:\s\w+)(?:\s\w+)?(?:\s\d+)\sin(?:\s\w+)(?:\s\w+)?(?:\s\d+)"""
    correction_happened = False

    if action.startswith("put"):
        answer = re.match(put_regex_1,action)
        if answer:
            action = action.replace(" on "," in/on ")
            correction_happened = True
        else:
            answer = re.match(put_regex_2,action)
            if answer:
                action = action.replace(" in "," in/on ")
                correction_happened = True
    
    if transform_to_move_syntax:
        action = action.replace("put","move")
        action = action.replace("in/on", "to")
        
    return action, correction_happened



#################################################################
#PROCESSING ACTIONS & OBSERVATIONS BASED on AGENTS
#################################################################
def get_observation_agentbench_thought():
    observation = "\n"
    return observation

def get_observation_react_thought():
    observation = "OK.\n"
    return observation

def get_observation_jsonreact_thought():
    observation = "OK.\n"
    return observation



def general_action_cleaning(action):
    """ General action cleaning. """
    if action.startswith("> "):
        action = action.replace("> ","")

    if action.startswith(">"):
        action = action.replace(">","")

    return action

def json_action_cleaning(action):
    """Action Cleaning for json."""
    action = action.strip()
    if action.startswith("```json"):
        action = action.replace("```json","")

    if action.startswith("```"):
        action = action.replace("```","")

    if action.endswith("```"):
        action = action.replace("```","")

    if not action.endswith("}"):
        action+="\n}\n"

    return action


def our_text_action_cleaning(action):
    """Action cleaning for our text"""
    action = action.strip()
    action+="\n\n"
    return action


def nojson_action_cleaning(action):
    """Action cleaning for no json."""
    action = action.strip()
    action+="\n"
    return action


def is_react_thought(action):
    return action.startswith("think:")

def is_jsonreact_thought(action, version=1):
    """ Todo: version number. """
    return '"think": "' in action

def is_agentbench_thought(action):
    return "THOUGHT:" in action



def get_action_jsonreact(action, version=1, key="action"):
    """
    Extracts 'actual_action' from action.

    'key' is not used at the moment.
    """
    if version==1:
        key = "action"

    actual_action = action
    was_command = False
    valid_json = False
    try:
        data = json.loads(action.strip())
        valid_json = True
        potential_action = data.get(key)
        if potential_action:
            actual_action = potential_action
            was_command = True
    except Exception as e:
        if (f'"{key}" : "' in action):
            was_command = True
            actions = action.split(f'"{key}" : "')
            actual_action = actions[1].split('"')[0]
            print(f"Extracted Action:{actual_action}")

        elif (f'"{key}": "' in action):
            was_command = True
            actions = action.split(f'"{key}": "')
            actual_action = actions[1].split('"')[0]
            print(f"Extracted Action:{actual_action}")

        elif (f'"{key}":"' in action):
            was_command = True
            actions = action.split(f'"{key}":"')
            actual_action = actions[1].split('"')[0]
            print(f"Extracted Action:{actual_action}")

    return actual_action, was_command, valid_json



def get_action_jsonstate(action, key="action"):
    """Extracts 'actual_action' from action. """
    actual_action = action
    was_command = False
    valid_json = False
    try:
        data = json.loads(action.strip())
        valid_json = True
        potential_action = data.get(key)
        if potential_action:
            actual_action = potential_action
            was_command = True
    except Exception as e:
        if (f'"{key}" : "' in action):
            was_command = True
            actions = action.split(f'"{key}" : "')
            actual_action = actions[1].split('"')[0]
            print(f"Extracted Action:{actual_action}")

        elif (f'"{key}": "' in action):
            was_command = True
            actions = action.split(f'"{key}": "')
            actual_action = actions[1].split('"')[0]
            print(f"Extracted Action:{actual_action}")

        elif (f'"{key}":"' in action):
            was_command = True
            actions = action.split(f'"{key}":"')
            actual_action = actions[1].split('"')[0]
            print(f"Extracted Action:{actual_action}")

    return actual_action, was_command, valid_json


def get_action_stringstate(action, key="action"):
    """Extracts 'actual_action' from action. """
    actual_action = action
    was_command = False

    SEP = f"{key}: "
    if SEP in action:
        split_sys_response = action.split(SEP)
        actual_action = split_sys_response[-1]
        was_command = True

    return actual_action, was_command


def get_action_agentbench(action):
    """Extracts 'actual_action' from action. """
    actual_action = action
    was_command = False

    if "ACTION:" in action:
        actions = action.split('ACTION:')
        actual_action = actions[1]
        was_command = True
        print(f"Extracted Action:{actual_action}")

    return actual_action, was_command


def process_action(action, track_is_illegal=False):
    """Processes Action of Agent."""
    illegal_action = False

    if 'action("' in action:
        actions = action.split('action("')
        action = actions[1].split('")')[0]
        print(f"Extracted Action:{action}")

    elif ('"action" : "' in action):
        actions = action.split('"action" : "')
        action = actions[1].split('"')[0]
        print(f"Extracted Action:{action}")

    elif ('"action": "' in action):
        actions = action.split('"action": "')
        action = actions[1].split('"')[0]
        print(f"Extracted Action:{action}")

    elif ('"action":"' in action):
        actions = action.split('"action":"')
        action = actions[1].split('"')[0]
        print(f"Extracted Action:{action}")

    #NOTE: this is for AGENTBENCH, needs proper refactor (was a TODO upstream).
    elif "ACTION:" in action:
        actions = action.split('ACTION:')
        action = actions[1]
        print(f"Extracted Action:{action}")

    else:
        illegal_action = True

    if track_is_illegal:
        return action, illegal_action
    else:
        return action



def process_ob(ob, track_nothing_happens=False):
    if ob.startswith('You arrive at loc '):
        ob = ob[ob.find('. ')+2:]

    nothing_happens = False

    if ob == "Nothing happens.":
        nothing_happens = True
        # ob = "Invalid or Impossible Action. Try again."

    if not ob.endswith("\n"):
        ob += "\n"

    if track_nothing_happens:
        return ob, nothing_happens
    else:
        return ob
