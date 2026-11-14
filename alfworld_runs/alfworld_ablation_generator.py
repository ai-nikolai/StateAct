import os
import sys
import json

# Make the repository root importable: this module is imported by scripts that
# are executed as plain files from inside alfworld_runs/.
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

# The six per-task base-example modules are described by a single registry in
# stateact.prompts, replacing the six explicit imports and the three
# hand-written ENV_TO_EXAMPLE_MAPPING_* tables that used to be here. The
# prompt *content* is untouched - only the wiring is generated.
from stateact.prompts import BASE_EXAMPLE_MODULES, load_base_example_variants


_BASE_EXAMPLE_VARIANTS = {
    env_type: load_base_example_variants(env_type) for env_type in BASE_EXAMPLE_MODULES
}

ENV_TO_EXAMPLE_MAPPING_0 = {k: v[0] for k, v in _BASE_EXAMPLE_VARIANTS.items()}
ENV_TO_EXAMPLE_MAPPING_1 = {k: v[1] for k, v in _BASE_EXAMPLE_VARIANTS.items()}
ENV_TO_EXAMPLE_MAPPING_2 = {k: v[2] for k, v in _BASE_EXAMPLE_VARIANTS.items()}

def transform_baseprompt_into_jsonstate_string(base_prompt, system_prefix="", agent_prefix=">"):
    """ Generate simple prompt based on the base."""
    base_prompt = remove_keys(base_prompt)
    prompt=""
    for idx, component in enumerate(base_prompt):
        if idx % 2 == 0:
            prefix = system_prefix
        else:
            prefix = agent_prefix
        
        prompt+=prefix + component + '\n\n'

    return prompt


def transform_baseprompt_into_stringstate_string(base_prompt, system_prefix="", agent_prefix=">"):
    """ Generate simple prompt based on the base."""
    base_prompt = remove_keys(base_prompt)
    prompt=""
    for idx, component in enumerate(base_prompt):
        output = ""    
        if idx % 2 == 0:
            prefix = system_prefix
            output = component
        else:
            prefix = agent_prefix
            data = json.loads(component)
            for key,value in data.items():
                if not value:
                    value = "None"
                elif type(value) == list:
                    value = ", ".join(value)

                if "_" in key:
                    key = key.replace("_"," ")
                output += f'{key}: {value}\n'
            output = output[:-1]

        
        prompt+=prefix + output + '\n\n'

    return prompt


def remove_keys(base_prompt, keys_to_remove=None):
    """Removes keys from the prompt and returns a base prompt."""
    keys_to_remove = keys_to_remove or []
    out_list = []
    for idx, component in enumerate(base_prompt):
        if idx % 2 == 1:
            try:
                data = json.loads(component)
                if keys_to_remove:
                    for key in keys_to_remove:
                        data.pop(key, None)
                component = json.dumps(data,indent=2)
            except Exception as e:
                print(idx)
                raise e
        
        out_list.append(component)
    return out_list


def restructure_prompt(base_prompt, keys_to_use=None, key_renaming=None):
    """
    restructures the prompt:
        - according to the order present in keys.
        - NOTE: it will only keep the keys present in keys
        - NOTE: if keys is empty it will throw an error.

    if key_renaming is also present it renames the keys:
        key_renaming = {original_name : new_name}
        - NOTE: you need to make sure the names don't have conflicts.
    """
    key_renaming = key_renaming or {}
    if not keys_to_use:
        raise Exception("You need to specify the keys to use in the resulting prompt.")

    # TODO WRITE THE CORRECT FUNCTION BELOW.
    out_list = []
    for idx, component in enumerate(base_prompt):
        if idx % 2 == 1:
            try:
                new_state = {}
                current_state = json.loads(component)
                for key in keys_to_use:
                    try:
                        value = current_state[key]
                    except KeyError as e:
                        raise KeyError(f"Idx:{idx}\nKey:{key}\n---\nState:\n{current_state}\n---\nComponent:\n{component}")

                    if key_renaming:
                        if key_renaming.get(key):
                            new_state[key_renaming[key]] = current_state[key]
                        else:
                            new_state[key] = current_state[key]
                    else:
                        new_state[key] = current_state[key]

                component = json.dumps(new_state,indent=2)
            except Exception as e:
                print(idx)
                raise e
        
        out_list.append(component)
    return out_list

def return_jsonstate_prompt(env_type, prompt_ids=None, keys_to_use=None, key_renaming=None):
    """Returns our prompt based on prompt_ids and keys_to_use."""
    prompt_ids = prompt_ids or [1, 0]
    keys_to_use = keys_to_use or ["thought", "action"]
    prompt_mappings = [ENV_TO_EXAMPLE_MAPPING_0, ENV_TO_EXAMPLE_MAPPING_1, ENV_TO_EXAMPLE_MAPPING_2]

    prompt_example = ""
    for idx, example_idx in enumerate(prompt_ids):
        if idx>0:
            prompt_example += "\n\n"

        base_prompt = prompt_mappings[example_idx][env_type]
        updated_base_prompt = restructure_prompt(base_prompt, keys_to_use, key_renaming)
        prompt_example += transform_baseprompt_into_jsonstate_string(updated_base_prompt) 

    return prompt_example


def return_stringstate_prompt(env_type, prompt_ids=None, keys_to_use=None, key_renaming=None):
    """Returns our prompt based on prompt_ids and keys_to_use."""
    prompt_ids = prompt_ids or [1, 0]
    keys_to_use = keys_to_use or ["thought", "action"]
    prompt_mappings = [ENV_TO_EXAMPLE_MAPPING_0, ENV_TO_EXAMPLE_MAPPING_1, ENV_TO_EXAMPLE_MAPPING_2]

    prompt_example = ""
    for idx, example_idx in enumerate(prompt_ids):
        if idx>0:
            prompt_example += "\n\n"

        base_prompt = prompt_mappings[example_idx][env_type]
        updated_base_prompt = restructure_prompt(base_prompt, keys_to_use, key_renaming)
        prompt_example += transform_baseprompt_into_stringstate_string(updated_base_prompt) 

    return prompt_example
