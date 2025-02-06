import yaml
import csv
import os
import json
import re
import argparse
from datetime import datetime


# import alfworld
# import alfworld.agents.environment

import alfworld.agents.environment as environment
from alfworld.agents.environment import get_environment
# import alfworld.agents.modules.generic as generic

from llamp.llms.human import Human
try:
    from llamp.llms.api import (
        AnthropicChat, AnthropicText,
        CohereChat, CohereChatText, CohereText,
        OpenAIChat, OpenAIChatText, OpenAIText, OpenAIChatTextSampling,
        NvidiaChatText,
        CerebrasChatText
    )
except Exception as e:
    print(e)
    print("Did not import API based models")

try:
    from llamp.llms.local import (
        VLLMChat
    )
except Exception as e:
    print(e)
    print("Did not import local model")

from alfworld_ablation_generator import return_jsonstate_prompt, return_stringstate_prompt
from alfworld_react_prompt_utils import return_react_examples, return_agentbench_prompts, return_json_react_examples


print("Successfully imported everything.")

# Git patch commit: https://stackoverflow.com/questions/1085162/commit-only-part-of-a-files-changes-in-git
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


def transform_put_action(action):
    """ Put action grammar correction. """
    put_regex_1 = """put(?:\s\w+)(?:\s\w+)?(?:\s\d+)\son(?:\s\w+)(?:\s\w+)?(?:\s\d+)"""
    put_regex_2 = """put(?:\s\w+)(?:\s\w+)?(?:\s\d+)\sin(?:\s\w+)(?:\s\w+)?(?:\s\d+)"""
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

    #TODO: this is for AGENTBENCH, need to refactor.
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




#################################################################
#PROMPT RELATED
#################################################################

# OPENING_MARK="<<<"
OPENING_MARK=""
# CLOSING_MARK=">>>"
CLOSING_MARK=""

# HINTS=f"""
# A few hints:
# {OPENING_MARK}
# 1. When "Nothing happens." this means your action was not successful or not valid. If this happen, then try a valid action that you have not tried before.

# 2. If you repeat yourself, try a different valid action.

# 3. Visit new places to find an object.

# 4. Some actions can be only executed in specific places, such as cleaning, heating, cooling...

# 5. Be literatal.

# 6. Initially you have not visited any places and you are starting at the 'starting_location'.

# 7. Generate one JSON output only.
# {CLOSING_MARK}
# """

HINTS=""

# INSTRUCTIONS=f"""
# This is the list of all valid actions that you can use:
# {OPENING_MARK}
# - go to <dir> [example: go to table 1]
# - open <obj> [example: open door 1]
# - close <obj> [example: close door 1]
# - put <obj> in/on <obj> [example: put apple 1 in/on table 1]
# - take <obj> from <obj> [example: take apple 1 from table 1]
# - cool <obj> with <obj> [example: cool apple 1 with fridge 1]
# - heat <obj> with <obj> [example: heat apple 1 with fire 1]
# - use <obj> [example: use desklamp 1]
# {CLOSING_MARK}
# """

INSTRUCTIONS=""


BASE_PROMPT1 = "Interact with a household to solve a task."
BASE_PROMPT2 = "You will interact with the environment to solve the given task."

TASK_MESSAGE = "Here is the task."

def generate_prompt_from_example(examples, return_raw_prompt = False, number_of_examples=1, base_prompt = "", instructions = "", hints = ""):
    """ Generates prompt """
    if number_of_examples >1:
        s_string="s"
        is_are = "are"
    else:
        s_string=""
        is_are = "is"
    number_of_examples_string = str(number_of_examples)

    #in case no alternative base_prompt is provided.
    if not base_prompt:
        base_prompt = BASE_PROMPT1

    #in case no alternative instructions is provided.
    if not instructions:
        instructions = INSTRUCTIONS

    #in case no alternative hints is provided.
    if not hints:
        hints = HINTS

    task_message = TASK_MESSAGE

    #########################################
    #
    #This is the part for the raw prompt.
    #
    #########################################
    raw_prompt = f"""{base_prompt}
{instructions}

Here {is_are} {number_of_examples_string} example{s_string}:
{OPENING_MARK}
{examples}
{CLOSING_MARK}
{hints}
{task_message}

"""
    prompt = [{
                "role" : "system",
                "content" : raw_prompt
            }]

    if return_raw_prompt:
        return raw_prompt
    else:
        return prompt

# HINT1="""1. When "Nothing happens." this means your action was not successful or not valid. This can have a variety of reasons, such as not wrong format of the output, or doing something in the wrong location, or using objects that are not available.
# If this happen, then try a valid action that you have not tried before.

# 2. If you repeat yourself, try a different valid action. Re-evaluate your assumptions.

# 3. Visit new places to find an object.

# 4. Some actions can be only executed in specific places, such as cleaning, heating, cooling...

# 5. Generate just one JSON output.
# """






#################################################################
#Logging Related
#################################################################
def write_line_to_main_log_csv(name, data):
    """Writes one line of output into the main CSV"""
    with open(name, 'a', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        if type(data) == list:
            wr.writerow(data)
        elif type(data) == dict:
            data_list = [x for _,x in data.items()]
            wr.writerow(data_list)

def save_prompt_file(file_path, raw_prompt):
    """ Saves a prompt file """
    with open(file_path, "w") as file:
        file.write(raw_prompt)


def get_empty_dict_from_csv_header(header):
    """Generate empty dict from csv header"""
    out_dict = {}
    for column_name in header:
        out_dict[column_name] = ""
    return out_dict







#################################################################
#AGENT Related
#################################################################
# TODO: REFACTOR
AGENT_MODEL_MAPPING = {
    "AnthropicChat" : ["claude-2.1", "claude-3-haiku-20240307", "claude-3-sonnet-20240229"],
    "CohereChat" : ["command","command-nightly", "command-r", "command-r-plus"],
    "OpenAIChat" : ["gpt-3.5-turbo-0125", "gpt-4-turbo-preview", "gpt-3.5-turbo-0301", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-1106"],
    "AnthropicText" : ["claude-2.1", "claude-3-haiku-20240307", "claude-3-sonnet-20240229"],
    "CohereText" : ["command","command-nightly", "command-r", "command-r-plus"],
    "OpenAIText" : ["davinci-002", "gpt-3.5-turbo-instruct"],
    "CohereChatText" : ["command","command-nightly", "command-r", "command-r-plus"],
    "OpenAIChatText" : ["gpt-3.5-turbo-0125", "gpt-4-turbo-preview", "gpt-3.5-turbo-0301", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-1106", "gpt-4o-mini"],
    "OpenAIChatTextSampling" : ["gpt-3.5-turbo-0125", "gpt-4-turbo-preview","gpt-3.5-turbo-0301", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-1106"],
    "NvidiaChatText" :["mistralai/mixtral-8x22b-instruct-v0.1","meta/llama-3.1-8b-instruct","meta/llama-3.1-70b-instruct"],
    "CerebrasChatText" :["llama3.1-8b","llama3.1-70b"],
    "VLLMChat" : ["Qwen/Qwen2.5-0.5B-Instruct","Qwen/Qwen2.5-1.5B-Instruct"]
}


def get_agent_and_model(llm_type, temperature=0.0, proposed_model=""):
    """ Returns Agent, Model"""
    print(llm_type)
    print(proposed_model)
    #Standard CHAT Models
    if llm_type == "AnthropicChat":
        model = "claude-2.1"
        if proposed_model:
            if proposed_model in AGENT_MODEL_MAPPING[llm_type]:
                model = proposed_model
            else:
                print("Proposed Model is not available using default model.")
        agent = AnthropicChat(temperature=temperature, model=model)

    elif llm_type == "CohereChat":
        # model = "command"
        # model = "command-nightly"
        model = "command-r"
        if proposed_model:
            if proposed_model in AGENT_MODEL_MAPPING[llm_type]:
                model = proposed_model
            else:
                print("Proposed Model is not available using default model.")
        agent = CohereChat(temperature=temperature, model=model)

    elif llm_type=="OpenAIChat":
        model = "gpt-3.5-turbo-0125"
        # model = "gpt-4-turbo-preview"
        if proposed_model:
            if proposed_model in AGENT_MODEL_MAPPING[llm_type]:
                model = proposed_model
            else:
                print("Proposed Model is not available using default model.")
        agent = OpenAIChat(temperature=temperature, model=model)



    #TEXT BASED MODELs
    elif llm_type =="AnthropicText":
        if proposed_model:
            if proposed_model in AGENT_MODEL_MAPPING[llm_type]:
                model = proposed_model
            else:
                print("Proposed Model is not available using default model.")
        # model = "claude-1.2"
        model = "claude-2.1"
        agent = AnthropicText(temperature=temperature, model=model)

    elif llm_type=="CohereText":
        # model = "command"
        # model = "command-nightly"
        model = "command-r"
        if proposed_model:
            if proposed_model in AGENT_MODEL_MAPPING[llm_type]:
                model = proposed_model
            else:
                print("Proposed Model is not available using default model.")
        agent = CohereText(temperature=temperature, model=model)

    elif llm_type=="OpenAIText":
        model = "davinci-002"
        model = "gpt-3.5-turbo-instruct"
        if proposed_model:
            if proposed_model in AGENT_MODEL_MAPPING[llm_type]:
                model = proposed_model
            else:
                print("Proposed Model is not available using default model.")
        agent = OpenAIText(temperature=temperature, model=model)



    #CHAT MODELS used as TEXT MODELs
    elif llm_type=="CohereChatText":
        # model = "command"
        # model = "command-nightly"
        model = "command-r"
        if proposed_model:
            if proposed_model in AGENT_MODEL_MAPPING[llm_type]:
                model = proposed_model
            else:
                print("Proposed Model is not available using default model.")
        agent = CohereChatText(temperature=temperature, model=model)


    elif llm_type=="OpenAIChatText":
        model = "gpt-3.5-turbo-0125"
        # model = "gpt-4-turbo-preview"
        if proposed_model:
            if proposed_model in AGENT_MODEL_MAPPING[llm_type]:
                model = proposed_model
            else:
                print("Proposed Model is not available using default model.")
        agent = OpenAIChatText(temperature=temperature, model=model)


    elif llm_type=="OpenAIChatTextSampling":
        model = "gpt-3.5-turbo-0125"
        # model = "gpt-4-turbo-preview"
        if proposed_model:
            if proposed_model in AGENT_MODEL_MAPPING[llm_type]:
                model = proposed_model
            else:
                print("Proposed Model is not available using default model.")
        agent = OpenAIChatTextSampling(temperature=temperature, model=model)

    elif llm_type=="NvidiaChatText":
        model = "meta/llama-3.1-8b-instruct"
        # model = "meta/llama-3.1-70b-instruct"
        # model = "gpt-4-turbo-preview"
        if proposed_model:
            if proposed_model in AGENT_MODEL_MAPPING[llm_type]:
                model = proposed_model
            else:
                print("Proposed Model is not available using default model.")
        agent = NvidiaChatText(temperature=temperature, model=model)

    elif llm_type=="CerebrasChatText":
        model = "llama3.1-8b"
        if proposed_model:
            if proposed_model in AGENT_MODEL_MAPPING[llm_type]:
                model = proposed_model
            else:
                print("Proposed Model is not available using default model.")
        agent = CerebrasChatText(temperature=temperature, model=model)

    elif llm_type=="VLLMChat":
        model = "Qwen/Qwen2.5-0.5B-Instruct"
        if proposed_model:
            if proposed_model in AGENT_MODEL_MAPPING[llm_type]:
                model = proposed_model
            else:
                print("Proposed Model is not available using default model.")
        agent = VLLMChat(model=model)


    elif llm_type=="Human":
        model = "Human"
        agent = HumanAgent()

    return agent, model



#################################################################
#Display Settings
#################################################################
# TODO changre to agent type
def get_settings_string(react_prompt, agentbench_prompt, json_react_prompt, agent_type, llm_type, model, temperature, num_envs, starting_env, prompt_ids, current_trial_name, keys_to_use_string, prompt_name, version, correction):
    """ Creates a string to print to the user the current settings. """
    not_ours = react_prompt or agentbench_prompt or json_react_prompt
    num_examples = len(prompt_ids)

    display_text = ""
    display_text += f"You are going to run Alfworld Environment with the following settings:\n"
    display_text += f"   -Agent Type: {agent_type}\n"
    display_text += f"   -LLM Type: {llm_type}\n"
    display_text += f"   -Model: {model}\n"
    display_text += f"   -Temperature: {temperature}\n"
    display_text += f"   -Starting env: {starting_env}\n"
    display_text += f"   -Ending env: {starting_env+num_envs-1}\n"
    display_text += f"   -Num of envs: {num_envs}\n"
    display_text += f"   -Current Trial Name: {current_trial_name}\n"

    if not not_ours:
        display_text += f"   -Keys that will be used: {keys_to_use_string}\n"
        display_text += f"   -Number of our Prompts: {num_examples}\n"
    if react_prompt:
        display_text += f"   -Number of React Examples: {num_examples}\n"
    if agentbench_prompt:
        display_text += f"   -Prompt Version AgentBench: {version}\n"
    if json_react_prompt:
        display_text += f"   -Number JsonReAct Examples: {num_examples}\n"

    # Swap Order
    if not agentbench_prompt:
        display_text += f"   -Prompt Ids: {prompt_ids}\n"

    #Name of prompt
    display_text += f"   -The prompt will be called: {prompt_name}\n"

    #Name of prompt
    display_text += f"   -Correction will happen: {correction}\n"


    display_text += "Do you want to continue? Press 'y' to continue."

    return display_text





#################################################################
#Env Prompt Logic
#################################################################
# TODO:
# Change to Agent-type from individual prompt_flags.
def get_prompt_example(agent_type, env_type, prompt_ids, version, generate_prompt=True, keys_to_use=[], key_renaming={}):
    """ Get name of prompt and example prompts"""
    # Generate correct prompt for this environment (basically pick the right example).
    new_base_prompt = ""

    # num_examples needed for prompt_ids
    num_examples = len(prompt_ids)

    #REACT PROMPT or OUR PROMPT
    if agent_type=="react":
        if generate_prompt:
            prompt_example = return_react_examples(env_type, prompt_ids=prompt_ids)

        prompt_id_string = '_'.join([str(y) for y in prompt_ids])
        prompt_name = f"react-{prompt_id_string}"


    elif agent_type=="agentbench":
        num_examples=1
        if generate_prompt:
            prompt_example, new_base_prompt = return_agentbench_prompts(env_type, return_base=True, version=version)
        prompt_name = f"agentbench-v{version}"

    elif agent_type=="jsonreact":
        if generate_prompt:
            prompt_example = return_json_react_examples(env_type, prompt_ids=prompt_ids, version=version)
        prompt_id_string = '_'.join([str(y) for y in prompt_ids])
        prompt_name = f"jsonreact-{prompt_id_string}-v{version}"

    elif agent_type=="ours":
        if generate_prompt:
            prompt_example = return_jsonstate_prompt(env_type, prompt_ids=prompt_ids, keys_to_use=keys_to_use, key_renaming=key_renaming)
        prompt_id_string = '_'.join([str(y) for y in prompt_ids])
        # TODO: properly test key_renaming.
        keys_string = '+'.join([str(y) for y in keys_to_use])

        prompt_name = f"jsonstate-{prompt_id_string}-k-{keys_string}"

    elif agent_type=="ours-text":
        if generate_prompt:
            prompt_example = return_stringstate_prompt(env_type, prompt_ids=prompt_ids, keys_to_use=keys_to_use, key_renaming=key_renaming)
        prompt_id_string = '_'.join([str(y) for y in prompt_ids])
        # TODO: properly test key_renaming.
        keys_string = '+'.join([str(y) for y in keys_to_use])

        prompt_name = f"stringstate-{prompt_id_string}-k-{keys_string}"

    else:
        raise NotImplementedError(f"Trying to call agent_type: {agent_type}, but it doesn't exist.")

    if generate_prompt:
        return prompt_name, prompt_example, new_base_prompt, num_examples
    else:
        return prompt_name



# AGENT_MODEL_MAPPING = [
#     "AnthropicChat",
#     "CohereChat" ,
#     "OpenAIChat" ,
#     "AnthropicText" ,
#     "CohereText" ,
#     "OpenAIText" ,
#     "CohereChatText",
#     "OpenAIChatText" ,
#     "OpenAIChatTextSampling"
# ]


#################################################################
#Arg parse
#################################################################
def build_arg_parser():
    """ Returns the argument parser"""
    parser = argparse.ArgumentParser(description="Alfworld Env with various agents")
    parser.add_argument(
        "--agent",
        type=str,
        default="ours",
        choices=[
            "react",
            "jsonreact",
            "agentbench",
            "ours",
            "ours-text"
        ],
        help="The Agent / Method choice.",
    )

    parser.add_argument("--model", type=str, default="gpt-3.5-turbo-0125", help="Underlying Model to use.(Needs to align with agent, otherwise default model will be used.)")
    parser.add_argument(
        "--llm_type",
        type=str,
        default="OpenAIChatTextSampling",
        choices=[
            "AnthropicChat",
            "CohereChat" ,
            "OpenAIChat" ,
            "AnthropicText" ,
            "CohereText" ,
            "OpenAIText" ,
            "CohereChatText",
            "OpenAIChatText" ,
            "OpenAIChatTextSampling",
            "NvidiaChatText",
            "CerebrasChatText",
            "VLLMChat"
        ],
        help="The type of llamp.llms to use.",
    )

    parser.add_argument("--agent_version", type=int, default=1, help="Method Version (if applicable)")
    parser.add_argument("--temperature", type=float, default=0.0, help="Temperature")
    parser.add_argument("--num_prompts", type=int, default=2, help="Number of prompts to use (if applicable) (LEGACY)")

    parser.add_argument("--prompt_ids", nargs='+', type=int, default=[1,0], help="A list of prompt indices to use, e.g. --prompt_indices 0 1")

    # Keys for our method
    parser.add_argument("--keys_to_remove", type=str, default="[]",help="DEPRACTED => Doesn't Work anymore. Needs to be json.loads-able list of keys to remove (LEGACY).")
    parser.add_argument("--keys_to_use", type=str, help="Needs to be json.loads-able list of keys to use")
    parser.add_argument("--keys_renaming", type=str, help="Needs to be json.loads-able list of new key names.")

    # RUN / ENV:
    parser.add_argument("--trial_name", type=str, default="v3_0_eval_test", help="Underlying Model to use.(Needs to align with agent, otherwise default model will be used.)")
    parser.add_argument("--start_index", type=int, default=0, help="Starting Index to use (inclusive).")
    parser.add_argument("--end_index", type=int, default=0, help="Ending index to use (inclusive). (Overrides num_envs)")
    parser.add_argument("--num_envs", type=int,  default=1, help="Sets the num of envs to run (gets overriden by end index)")


    parser.add_argument(
        "--eval_split",
        type=str,
        default="eval_out_of_distribution",
        choices=[
            "eval_out_of_distribution",
            "eval_in_distribution"
        ],
        help="The alfworld split to use.",
    )
    parser.add_argument("--apply_correction", action="store_true", default=False, help="Whether to apply the 'Put Regex' correction")
    parser.add_argument("--resample", action="store_true", default=False, help="Whether to resample on repetition")
    parser.add_argument("--resample_temperature", type=float, default=0.1, help="Resample Temperature increase.")

    parser.add_argument("--force_run", action="store_true", default=False, help="Whether to apply the 'Put Regex' correction")

    parser.add_argument("--silent", action="store_true", default=False, help="Whether to suppress messages during the game loop.")

    return parser





#################################################################
#################################################################
#MAIN LOOP
#################################################################
#################################################################

if __name__=="__main__":

    # More things to track:
    # 1. Tokens generated / consumed (i.e. estimated price)
    # 2. Time taken


    ####################################################
    # BASIC CONFIGURATION
    ####################################################
    BASE_FOLDER = "game_logs"
    BASE_EVAL_NAME = "alfworld_eval"
    MAIN_CSV_FILE_NAME = "alfworld_results"

    TEST_ENV = False
    # TEST_ENV = True


    parser = build_arg_parser()
    args = parser.parse_args()


    #CHANGE THIS ONE
    if not TEST_ENV:
        CURRENT_TRIAL_NAME = args.trial_name
    else:
        CURRENT_TRIAL_NAME = "v3_0_eval_test"

    ###############################
# TODO:
# 1. Make end start env as option as well (not only num of envs)
# 2. Make restart from last unfinished possible
# 3. Todo (record prompts more properly [based on order of input prompts])
    # Basic Init
    if not TEST_ENV:
        start_env_idx=args.start_index
        num_envs = args.num_envs
    else:
        start_env_idx=0
        num_envs = 1

    llm_type = args.llm_type
    # llm_type = "OpenAIChatTextSampling"
    # llm_type = "Human"
    model = args.model
    # model = "gpt-3.5-turbo-0301" #Adaplanner paper GPT3.5 (released when?)
    # model = "gpt-3.5-turbo-0613" #slightly newer version than 0301 (released 13.06.2023)
    # model = "gpt-3.5-turbo-1106" #sligthly newer version than 0613 (released 11.06.2023)
# gpt-3.5-turbo-instruct
# gpt-3.5-turbo-instruct-0914
    temperature = args.temperature

    ###############################
    # Which METHOD to run (REACT, AGENTBENCH, OURS)
    AGENT_TYPE = args.agent

    REACT_PROMPT = True if AGENT_TYPE == "react" else False
    AGENTBENCH_PROMPT = True if AGENT_TYPE == "agentbench" else False
    JSON_REACT_PROMPT = True if AGENT_TYPE == "jsonreact" else False


    OUR_TEXT_PROMPTS = True if AGENT_TYPE == "ours-text" else False
    NOT_JSON_PROMPTS = REACT_PROMPT or AGENTBENCH_PROMPT or llm_type == "Human"

    # NUM_EXAMPLES = args.num_prompts
    VERSION = args.agent_version

    PROMPT_IDS = args.prompt_ids

    CORRECTION = args.apply_correction
    RESAMPLE = args.resample
    if RESAMPLE:
        RESAMPLE_TEMPERATURE = args.resample_temperature
    else:
        RESAMPLE_TEMPERATURE = None

    # OTHER
    SILENT_MODE = args.silent


    ##############################
    # This applies to our prompts
    if args.keys_to_use:
        KEYS_TO_USE = json.loads(args.keys_to_use)
    elif AGENT_TYPE == "ours":
        print("FAIL - Need to specify which keys to use with 'ours' agents.")
        exit(-1)
    else:
        KEYS_TO_USE = ""


    prompt_name2 = get_prompt_example(
        agent_type= AGENT_TYPE,
        version = VERSION,
        prompt_ids = PROMPT_IDS,
        env_type="",
        generate_prompt=False,
        keys_to_use=KEYS_TO_USE)

    ##############################
    # Checking settings with the user. User needs to type y.
    keys_to_use_string = "+".join(KEYS_TO_USE)
    settings_string = get_settings_string(
            react_prompt = REACT_PROMPT,
            agentbench_prompt = AGENTBENCH_PROMPT,
            json_react_prompt = JSON_REACT_PROMPT,
            agent_type = AGENT_TYPE,
            llm_type = llm_type,
            model = model,
            temperature = temperature,
            num_envs = num_envs,
            prompt_ids = PROMPT_IDS,
            starting_env = start_env_idx,
            current_trial_name = CURRENT_TRIAL_NAME,
            keys_to_use_string=keys_to_use_string,
            version = VERSION,
            prompt_name = prompt_name2,
            correction = CORRECTION
        )

    print(settings_string)
    if args.force_run:
        print("WARNING: Running Anyways")
    else:
        user_input = input(">")
        if not (user_input=="y"):
            print("Exiting Programme, please change the settings in: playgrounds/playground_alfworld_eval.py")
            exit(1)


    #TODO for the future
    additional_prompt_annotation = ""


    ####################################################
    # OTHER IN-BUILT CONFIG
    ####################################################
    CREATE_NEW_LOG_CSV=False

    CURRENT_TRIAL_FOLDER = BASE_EVAL_NAME+"_"+CURRENT_TRIAL_NAME
    SAVE_FOLDER = os.path.join(BASE_FOLDER,CURRENT_TRIAL_FOLDER)
    CSV_HEADER = [
        # GENERAL AGENT/ENV Settings
        "env_idx",
        "env_type",
        "agent_type",
        "llm_type",
        "model",
        "temperature",
        "prompt_name",
        # PER GAME METRICS
        "success",
        "done",
        "total_reward",
        "early_stop",
        "error",
        # PER STEP METRICS
        "num_of_steps",
        "num_nothing_happens",
        "num_repetitions",
        "num_no_command",
        "num_no_json",
        "num_correction",
        "num_resample",
        # TOKEN COUNT
        "total_prompt_token", #How many tokens the prompt is
        "total_in_token_accumulated", #Total number of in tokens accumulated
        "total_in_token_message_accumulated", #Total number of in message tokens accumulated
        "total_out_token_accumulated", #Total number of tokens of the entire history (measured at the end)
        "total_history_token",
        # VARIOUS FLAGS and ADDITIONAL DESCRIPTIONS
        "correction", #boolean flag
        "resample", #boolean flag,
        "resample_temperature",
        "keys_to_use",
        "additional_prompt_annotation",
        "trace_file",
        "prompt_file"
    ]



    #######################################################
    # LOGGING(CSV) Related
    #######################################################
    #CSV FILE Related Things
    MAIN_CSV_FILEPATH = os.path.join(SAVE_FOLDER,MAIN_CSV_FILE_NAME+".csv")

    # Writing the Header
    if not os.path.exists(SAVE_FOLDER):
        os.mkdir(SAVE_FOLDER)
    if CREATE_NEW_LOG_CSV:
        file_counter = 0
        while os.path.exists(MAIN_CSV_FILEPATH):
            MAIN_CSV_FILEPATH = os.path.join(SAVE_FOLDER,MAIN_CSV_FILE_NAME+str(file_counter)+".csv")
            file_counter+=1
        # Now that we have a new unique csv file name create it and write the header.
        write_line_to_main_log_csv(MAIN_CSV_FILEPATH, CSV_HEADER)
    else:
        if not os.path.exists(MAIN_CSV_FILEPATH): #Only write header once
            write_line_to_main_log_csv(MAIN_CSV_FILEPATH, CSV_HEADER)




    #######################################################
    # AGENT Related
    #######################################################
    agent, actual_model = get_agent_and_model(llm_type=llm_type, temperature=temperature, proposed_model=model)
    agent.update_save_path(SAVE_FOLDER)

    if RESAMPLE:
        if not agent.is_resample():
            RESAMPLE = False
            print(f"WARNING: Your llm_type:{llm_type} does not support sampling, disabling resampling.")
            print("Do you still want to continue? Press 'y' to continue.")
            user_input = input(">")
            if user_input=="y":
                pass
            else:
                exit(1)
        else:
            agent.resample_temperature_jump = RESAMPLE_TEMPERATURE

    if actual_model != model:
        print(f"WARNING: Your model:{model} is not used, instead using default model: {actual_model}")
        print("Do you still want to continue? Press 'y' to continue.")
        user_input = input(">")
        if user_input=="y":
            pass
        else:
            exit(1)


    #######################################################
    # ENV Related
    #######################################################
    # Old Stuff
    # Env Init
    # with open('playgrounds/base_config.yaml') as reader:
    #     config = yaml.safe_load(reader)

    # env = getattr(alfworld.agents.environment, config["env"]["type"])(config, train_eval=split)
    # env = env.init_env(batch_size=1)


    # NEW STUFF TODO: v0.4.1
    split = args.eval_split
    # split = "eval_in_distribution"
    # load config
    # config = generic.load_config()

    with open('base_config.yaml') as reader:
        config = yaml.safe_load(reader)
    env_type = config['env']['type'] # 'AlfredTWEnv' or 'AlfredThorEnv' or 'AlfredHybrid'

    # setup environment
    # that's how it was done previously
    # env = getattr(environment, env_type)(config, train_eval=split)
    env = get_environment(env_type)(config, train_eval=split)
    env = env.init_env(batch_size=1)



    # Skipping Envs
    for i in range(start_env_idx):
        observation, info = env.reset()
        # name = '/'.join(info['extra.gamefile'][0].split('/')[-3:-1])
        # env_type = get_env_type(name)
        # print(name)
        # print(f"Idx: {i} Env:{env_type}")

    # input(">")



    #######################################################
    # RUNNING The Trial
    #######################################################
    # Running Trial
    for env_idx in range(num_envs):


        #######################################################
        # ENV Init
        #######################################################
        # Get new environment
        observation, info = env.reset()

        observation = '\n'.join(observation[0].split('\n\n')[1:])
        name = '/'.join(info['extra.gamefile'][0].split('/')[-3:-1])

        env_type = get_env_type(name)
        # if not env_type=="clean":
        #     continue
        print(f"Starting Env with Index: {env_idx+start_env_idx} of type: {env_type}")

        if not SILENT_MODE:
            print(observation)
        observation += "\n"
        # print(info)
        # print(name)


        #######################################################
        # PROMPT Related
        #######################################################
        prompt_name, prompt_example, new_base_prompt, num_examples = get_prompt_example(
            agent_type=AGENT_TYPE,
            env_type=env_type,
            prompt_ids=PROMPT_IDS,
            version=VERSION,
            generate_prompt=True,
            keys_to_use=KEYS_TO_USE
        )

        prompt = generate_prompt_from_example(prompt_example, number_of_examples=num_examples, base_prompt=new_base_prompt)
        agent.set_base_prompt_and_reset(prompt)

        # ###
        # Save Raw Prompt
        now = datetime.now()
        prompt_save_path = os.path.join(SAVE_FOLDER, "prompt_"+now.strftime("%d_%m_%Y_%H_%M_%S")+".txt")


        raw_prompt = generate_prompt_from_example(prompt_example, return_raw_prompt=True, number_of_examples=num_examples, base_prompt=new_base_prompt)
        save_prompt_file(prompt_save_path, raw_prompt)
        total_prompt_tokens = agent.count_tokens(raw_prompt)



        # ####################################
        # SETTING the STOP Condition for AGENT
        if OUR_TEXT_PROMPTS:
            agent.stop_sequences = ["\n\n"]
            OUR_PROMPT_ADD_BRACKET_CONDITION=False
        elif NOT_JSON_PROMPTS:
            agent.stop_sequences = ["\n"]
            OUR_PROMPT_ADD_BRACKET_CONDITION=False
        else:
            agent.stop_sequences = ["}\n", "\n}"]
            OUR_PROMPT_ADD_BRACKET_CONDITION=True




        #######################################################
        # Logging Init & Initial values
        #######################################################
        logging_dict = get_empty_dict_from_csv_header(CSV_HEADER)
        # 28
        logging_dict["env_idx"]  = env_idx+start_env_idx
        logging_dict["env_type"] = env_type
        logging_dict["llm_type"] = llm_type
        logging_dict["agent_type"] = AGENT_TYPE
        logging_dict["model"] = actual_model
        logging_dict["temperature"] = temperature




        #######################################################
        # GAME VARIABLES AND SETTINGS
        #######################################################
        # FIXED VARIABLES
        LIMIT = 100
        INPUT_TOKEN = ""
        OUTPUT_TOKEN = ""

        CAPITAL = [chr(x+65) for x in range(26)]
        LOWER = [chr(x+97) for x in range(26)]

        LIMIT_CURRENT_REPETITIONS = 5 #after 5 repetitions stop current run.
        MAX_RESAMPLE = 10 #after 10 resamples the agent will continue


        # To be reset at each run.
        game_running_flag = True
        counter = 0
        error = ""
        early_stop = ""
        success = False
        logging_done = False
        total_reward = 0


        num_nothing_happens = 0
        num_repetitions = 0

        num_no_command = 0
        num_no_json = 0

        num_correction = 0

        num_resample = 0
        num_current_resample = 0

        prev_action = ""
        num_current_repetitions = 0
        total_in_token = 0
        total_out_token = 0
        total_in_message_token = 0
        total_token = 0


        # for resampling
        CURRENT_NOTHING_HAPPENS = False

        error_count = 0

        #######################################################
        # Main Game Loop
        #######################################################
        try:
            while game_running_flag:

                was_command = False
                valid_json = False
                is_nothing_happens = False

                continue_flag = False

                # #####################
                # Action related
                action, token_count_dictionary = agent.act(f"{INPUT_TOKEN}"+observation+f"{OUTPUT_TOKEN}", return_token_count=True)

                total_in_token += token_count_dictionary["in_token_all"]
                total_in_message_token += token_count_dictionary["in_token_message"]
                total_out_token += token_count_dictionary["out_token_action"]


                #########################
                # Adding early stop here, as while loop could continue for ever otherwise (in some cases).
                counter += 1
                if counter == LIMIT:
                    early_stop = f"ENV_ERROR: Reached Step Limit:{LIMIT}"
                    print("\nFalse\nFalse")
                    print("EARLY STOP: Limit")
                    break



                # ###################################
                # Per Agent Type Cleaning
                # ###################################

                #########################
                # New Flow Split by agenttype.
                action = general_action_cleaning(action) #Done
                if not SILENT_MODE:
                    print("<<< RAW ACTION >>>:"+action)


                if OUR_TEXT_PROMPTS:
                    action = our_text_action_cleaning(action) #Done

                    if AGENT_TYPE =="ours-text":
                        actual_action, was_command = get_action_stringstate(action, key="action") #TODO

                elif not NOT_JSON_PROMPTS: #i.e.: The JSON prompts
                    action = json_action_cleaning(action) #Done

                    if AGENT_TYPE == "jsonreact":
                        if is_jsonreact_thought(action, version=VERSION): #Done
                            observation = get_observation_jsonreact_thought() #Done
                            if not SILENT_MODE:
                                print("<> OBSERVATION <>:"+observation)
                            continue_flag = True

                        actual_action, was_command, valid_json = get_action_jsonreact(action, version=VERSION, key="action") #Done

                    elif AGENT_TYPE == "ours":
                        actual_action, was_command, valid_json= get_action_jsonstate(action, key="action") #Done

                elif NOT_JSON_PROMPTS:
                    action = nojson_action_cleaning(action) #Done

                    if AGENT_TYPE == "react":
                        if is_react_thought(action): #Done
                            observation = get_observation_react_thought() #Done
                            if not SILENT_MODE:
                                print("<> OBSERVATION <>:"+observation)
                            continue_flag = True

                        actual_action = action

                    elif AGENT_TYPE == "agentbench":
                        actual_action, was_command = get_action_agentbench(action) #Done
                        if not was_command:
                            if is_agentbench_thought(action): #Done
                                observation = get_observation_agentbench_thought() #Done
                                continue_flag = True
                else:
                    raise Exception("What happened there?")

                # ###################################
                # Per action logging and logic.
                # ###################################
                # Updating the agent with a cleaned action
                agent.update_latest_history(">"+action) #Adding '>' symbol back in as this is how the example prompt is presented to LLMs.
                if not SILENT_MODE:
                    print("<<< CLEANED ACTION >>>:"+action)
                    print("<<< EXTRACTED ACTION >>>:"+actual_action)

                if action == prev_action:
                    if RESAMPLE:
                        if num_current_resample < MAX_RESAMPLE:
                            num_resample += 1
                            num_current_resample += 1
                            agent.prepare_resample()
                            print(f"RESAMPLING: {num_current_resample}")
                            continue

                    num_repetitions += 1
                    num_current_repetitions +=1
                else:
                    num_current_repetitions = 0
                    num_current_resample = 0

                prev_action = action

                # TRACKING VARIOUS METRICS
                if not was_command:
                    num_no_command += 1

                if not valid_json:
                    num_no_json += 1

                if CORRECTION:
                    actual_action, correction_happened = transform_put_action(actual_action)
                    if not SILENT_MODE:
                        print(f"TRANSFORMED_ACTION:{actual_action}")
                    if correction_happened:
                        num_correction += 1

                # Breaking early in case thoughts were repeated as well.
                if num_current_repetitions == LIMIT_CURRENT_REPETITIONS:
                    early_stop = f"ENV_ERROR: Too many ({LIMIT_CURRENT_REPETITIONS}) consecutive repetitions."
                    print("\nFalse\nFalse")
                    print("EARLY STOP: Repetitions")
                    break

                if continue_flag:
                    continue



                # ###################################
                # Observation Related.
                # ###################################
                observation, reward, done, info = env.step([actual_action])
                total_reward += reward[0]


                observation, is_nothing_happens = process_ob(observation[0], track_nothing_happens=True)
                if is_nothing_happens:
                    num_nothing_happens += 1
                    CURRENT_NOTHING_HAPPENS = True
                else:
                    CURRENT_NOTHING_HAPPENS = False


                if not SILENT_MODE:
                    print("<> OBSERVATION <>:"+observation)
                    print(info["won"][0])
                    print(done[0])
                    print(reward[0])

                if done[0] or info["won"][0]:
                    if info["won"][0]:
                        success=True
                    else:
                        success=False

                    if done[0]:
                        logging_done=True
                    else:
                        logging_done=False

                    break

        except Exception as e:
            print("AN EXCEPTION OCCURED")
            print(error)
            print(e)
            error_count += 1
            error = str(e)


        finally:
            # MAIN Score Logging
            logging_dict["success"] = success
            logging_dict["done"] = logging_done
            logging_dict["total_reward"] = total_reward
            logging_dict["error"] = error
            logging_dict["early_stop"] = early_stop

            # Step logging & per step logging
            logging_dict["num_of_steps"] = counter

            logging_dict["num_nothing_happens"] = num_nothing_happens
            logging_dict["num_repetitions"] = num_repetitions
            logging_dict["num_no_command"] = num_no_command
            logging_dict["num_no_json"] = num_no_json

            # CORRECTION & per step correction logging
            logging_dict["correction"] = CORRECTION
            logging_dict["num_correction"] = num_correction

            # RESAMPLE & per step resample logging
            logging_dict["resample"] = RESAMPLE
            logging_dict["resample_temperature"] = RESAMPLE_TEMPERATURE
            logging_dict["num_resample"] = num_resample
            # Token Count
            logging_dict["total_prompt_token"] = total_prompt_tokens
            logging_dict["total_in_token_accumulated"] = total_in_token
            logging_dict["total_in_token_message_accumulated"] = total_in_message_token
            logging_dict["total_out_token_accumulated"] = total_out_token
            logging_dict["total_history_token"] = agent.count_tokens()

            # Prompt Name Logging
            logging_dict["prompt_name"] = prompt_name
            logging_dict["keys_to_use"] = KEYS_TO_USE

            #File Loggin
            logging_dict["trace_file"] = agent.file_name
            logging_dict["prompt_file"] = prompt_save_path
            logging_dict["additional_prompt_annotation"] = additional_prompt_annotation
            write_line_to_main_log_csv(MAIN_CSV_FILEPATH, logging_dict)
            print(logging_dict)
            agent.save()
