import json
import os

# Resolve the prompt files relative to this module, not the process cwd.  The
# scripts are documented to be run from inside alfworld_runs/, but the shared
# alfworld_runs.prompt_builders dispatcher and the test-suite import this module from the
# repository root as well.
BASE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts")

react_prompt_file_name = "alfworld_react_prompts_original_v3_corrected.json"
react_prompt_file = os.path.join(BASE_FOLDER, react_prompt_file_name)
with open(react_prompt_file, "r") as file:
    original_react_prompts = json.load(file)



agentbench_prompt_file_name = "agentbench_prompts_v1_plan_first.json"
agentbench_prompt_file = os.path.join(BASE_FOLDER,agentbench_prompt_file_name)
with open(agentbench_prompt_file, "r") as file:
    original_agentbench_prompts_v1 = json.load(file)

agentbench_prompt_file_name = "agentbench_prompts_v2_react.json"
agentbench_prompt_file = os.path.join(BASE_FOLDER,agentbench_prompt_file_name)
with open(agentbench_prompt_file, "r") as file:
    original_agentbench_prompts_v2 = json.load(file)


def return_react_examples(env_type, prompt_ids=None):
    """Given the env type return a react example."""
    index_list = prompt_ids or [1, 0]
    target_trace = ""
    for example_idx in range(len(index_list)):
        if example_idx>0:
            target_trace+="\n\n"
        target_trace += original_react_prompts[f"react_{env_type}_{index_list[example_idx]}"]
  
    return target_trace


def extract_command_and_format(command, version=1, think_key="think", action_key="action"):
    """Sub func to extract commands.
    Documentation on double {{, }} for f-strings 
    https://stackoverflow.com/questions/5466451/how-do-i-escape-curly-brace-characters-in-a-string-while-using-format-or
    """
    thinking = False
    if "think:" in command:
        sys_think = command.split("\n")[0].split("think:")[1].strip()
        sys_act = ""
        thinking = True
    else:
        sys_act = command.split("\n")[0].strip()
        sys_think = ""

    if version==1:
        if thinking:
            sys_response = f'{{\n"{think_key}": "{sys_think}"\n}}' 
        else:
            sys_response = f'{{\n"{action_key}": "{sys_act}"\n}}'

    elif version==2:
        sys_response = f'{{\n"{think_key}": "{sys_think}",\n"{action_key}": "{sys_act}"\n}}' 

    elif version==3:
        if thinking:
            sys_response = f'{{\n"response": "think: {sys_think}"\n}}' 
        else:
            sys_response = f'{{\n"response": "{sys_act}"\n}}'

    else:
        raise NotImplementedError(f"No other versions available for jsonreact at the moment. You tried version: {version}")

    env_observation = command.split("\n")[1]

    return sys_response, env_observation


def return_json_react_examples(env_type, prompt_ids=None, version=1, think_key="think", action_key="action", return_list=False):
    """Given the env type return a json react example."""
    prompt_ids = prompt_ids or [1, 0]
    target_trace = ""
    if return_list:
        target_trace_list = []

    index_list = prompt_ids

    for example_idx in range(len(index_list)):
        if example_idx>0:
            target_trace+="\n\n"
        
        string_trace = original_react_prompts[f"react_{env_type}_{index_list[example_idx]}"]

        commands = string_trace.split(">")

        if return_list:
            # Need to append a list to have one list per example
            target_trace_list.append( [commands[0].strip()] )

        for idx,command in enumerate(commands[1:]):
            sys_response, env_observation = extract_command_and_format(command, version, think_key, action_key)
            commands[idx+1] = sys_response+"\n\n"+env_observation+"\n\n"
            if return_list:
                target_trace_list[example_idx].append(sys_response)
                target_trace_list[example_idx].append(env_observation)

        target_trace += ">".join(commands)

    if return_list:
        return target_trace_list

    return target_trace


def return_agentbench_prompts(env_type, return_base=True, version=2):
    """ Returns Agentbench Prompt"""
    if version == 1:
        original_agentbench_prompts = original_agentbench_prompts_v1
    elif version == 2:
        original_agentbench_prompts = original_agentbench_prompts_v2
    else:
        raise NotImplementedError(f"Wrong version number for Agentbench prompt. You tried version: {version}")
    
    prompt_example = "".join(original_agentbench_prompts[env_type])
    if return_base:
        base_prompt = original_agentbench_prompts["base_prompt"]
        return prompt_example, base_prompt
    else:
        return prompt_example
