import os
import json
import re
import random


from prompts.alfworld_prompts_utils_v4_clean_base import clean_v4_base_0, clean_v4_base_1, clean_v4_base_2
from prompts.alfworld_prompts_utils_v4_cool_base import cool_v4_base_0, cool_v4_base_1, cool_v4_base_2
from prompts.alfworld_prompts_utils_v4_examine_base import examine_v4_base_0, examine_v4_base_1, examine_v4_base_2
from prompts.alfworld_prompts_utils_v4_heat_base import heat_v4_base_0, heat_v4_base_1, heat_v4_base_2
from prompts.alfworld_prompts_utils_v4_put_base import put_v4_base_0, put_v4_base_1, put_v4_base_2
from prompts.alfworld_prompts_utils_v4_puttwo_base import puttwo_v4_base_0, puttwo_v4_base_1, puttwo_v4_base_2

from alfworld_react_prompt_utils import return_react_examples, return_agentbench_prompts, return_json_react_examples


ENV_TO_EXAMPLE_MAPPING_0 = {
    "clean" : clean_v4_base_0,
    "cool"  : cool_v4_base_0,
    "examine"   : examine_v4_base_0,
    "heat"  : heat_v4_base_0,
    "put"   : put_v4_base_0,
    "puttwo"    : puttwo_v4_base_0
}

ENV_TO_EXAMPLE_MAPPING_1 = {
    "clean" : clean_v4_base_1,
    "cool"  : cool_v4_base_1,
    "examine"   : examine_v4_base_1,
    "heat"  : heat_v4_base_1,
    "put"   : put_v4_base_1,
    "puttwo"    : puttwo_v4_base_1
}

ENV_TO_EXAMPLE_MAPPING_2 = {
    "clean" : clean_v4_base_2,
    "cool"  : cool_v4_base_2,
    "examine"   : examine_v4_base_2,
    "heat"  : heat_v4_base_2,
    "put"   : put_v4_base_2,
    "puttwo"    : puttwo_v4_base_2
}

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


def remove_keys(base_prompt, keys_to_remove=[]):
    """Removes keys from the prompt and returns a base prompt."""
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


def restructure_prompt(base_prompt, keys_to_use=[], key_renaming={}):
    """
    restructures the prompt:
        - according to the order present in keys.
        - NOTE: it will only keep the keys present in keys
        - NOTE: if keys is empty it will throw an error.

    if key_renaming is also present it renames the keys:
        key_renaming = {original_name : new_name}
        - NOTE: you need to make sure the names don't have conflicts.
    """
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

def return_jsonstate_prompt(env_type, prompt_ids=[1,0], keys_to_use=["thought","action"], key_renaming={}):
    """ 
    Returns our prompt based on prompt_ids and keys_to_use. 

    TODO: add key_renaming.
    """
    prompt_mappings = [ENV_TO_EXAMPLE_MAPPING_0, ENV_TO_EXAMPLE_MAPPING_1, ENV_TO_EXAMPLE_MAPPING_2]

    prompt_example = ""
    for idx, example_idx in enumerate(prompt_ids):
        if idx>0:
            prompt_example += "\n\n"

        base_prompt = prompt_mappings[example_idx][env_type]
        updated_base_prompt = restructure_prompt(base_prompt, keys_to_use, key_renaming)
        prompt_example += transform_baseprompt_into_jsonstate_string(updated_base_prompt) 

    return prompt_example


def return_stringstate_prompt(env_type, prompt_ids=[1,0], keys_to_use=["thought","action"], key_renaming={}):
    """ 
    Returns our prompt based on prompt_ids and keys_to_use. 

    TODO: add key_renaming.
    """
    prompt_mappings = [ENV_TO_EXAMPLE_MAPPING_0, ENV_TO_EXAMPLE_MAPPING_1, ENV_TO_EXAMPLE_MAPPING_2]

    prompt_example = ""
    for idx, example_idx in enumerate(prompt_ids):
        if idx>0:
            prompt_example += "\n\n"

        base_prompt = prompt_mappings[example_idx][env_type]
        updated_base_prompt = restructure_prompt(base_prompt, keys_to_use, key_renaming)
        prompt_example += transform_baseprompt_into_stringstate_string(updated_base_prompt) 

    return prompt_example



def get_string_difference(string1, string2):
    """ Gets you the string difference """

    out_string = ""
    if len(string1) > len(string2):
        longer_string = string1
        shorter_string = string2
        longer_str = "1"
    elif len(string1) < len(string2):
        longer_string = string2
        shorter_string = string1
        longer_str = "2"

    else:
        longer_string = string1
        shorter_string = string2   
        same_length = True
        longer_str = "Same"


    for idx, char in enumerate(longer_string):
        if idx < len(shorter_string):
            if not char == shorter_string[idx]:
                out_string += f"Char different at: {idx}, s1:{char} s2:{shorter_string[idx]}\n"
        else:
            out_string += f"The {longer_str} is longer: len1:{len(string1)}, len2:{len(string2)}\n"

    return out_string
    # return None


def verify_react_and_ours(our_prompt, react_prompt):
    """ 
    Assumes that our prompts are a: 
        - list of Observation, Sys Response, 
        - where sys response is a json with various keys

    Assumes that react prompts are the "version1" variant:
        - a list of Observation, sys response
        - where sys response contains either the "think" or "action" key.
    """
    all_true = True
    thinking_count = 0

    for idx, observation in enumerate(our_prompt):

        if idx % 2 ==0:
            react_observation = react_prompt[idx+thinking_count*2]
            assertion1 = observation == react_observation
            if not assertion1:
                difference = get_string_difference(observation, react_observation)
            assert assertion1, f"\n===\nEnv Obs do not allign:\nidx:{idx}\n---\nobs:\n{observation}\n---\nreact:\n{react_observation}\n---\ndifference:\n{difference}"

        else:
            react_thought = ""
            our_state = json.loads(observation)
            react_state = json.loads(react_prompt[idx+thinking_count*2])
            while react_state.get("think"):
                react_thought += react_state["think"]+" "
                thinking_count += 1
                react_state = json.loads(react_prompt[idx+thinking_count*2])

            assertion2 = our_state["thought"] == react_thought.strip()
            if not assertion2:
                difference = get_string_difference(our_state["thought"], react_thought.strip())
            assert assertion2, f'\n===\nThoughts do not allign:\nidx:{idx}\n---\nobs:\n{our_state["thought"]}\n---\nreact:\n{react_thought.strip()}\n---\ndifference:\n{difference}'
            
            assertion3 = our_state["action"] == react_state["action"]
            if not assertion3:
                difference = get_string_difference(our_state["action"], react_state["action"])
            assert assertion3, f'\n===\nActions do not allign:\nidx:{idx}\n---\nobs:\n{our_state["action"]}\n---\nreact:\n{react_state["action"]}\n---\ndifference:\n{difference}'

    return all_true


def extract_react_command_and_arguments(action_string):
    """ 
    Extracts the react command and arguments 
    
    WARNGING: 
        At the moment:
        Only extract commands that change the state, otherwise returns None.

    Regex Builder: https://regex101.com/r/BK3La8/1
    """
    # State changing regex expressions.
    put_regex = """put\s(\w+(?:\s\w+)?\s\d+)\sin\/on\s(\w+(?:\s\w+)?\s\d+)"""
    goto_regex = """go\sto\s(\w+(?:\s\w+)?\s\d+)"""
    take_regex = """take\s(\w+(?:\s\w+)?\s\d+)\sfrom\s(\w+(?:\s\w+)?\s\d+)"""
    
    # #Commands that do not change the state
    # TODO they need to be update to extract arguments correctly.
    # open_regex = """open(?:\s\w+)(?:\s\w+)?(?:\s\d+)"""    
    # cool_regex = """cool(?:\s\w+)(?:\s\w+)?(?:\s\d+)\swith(?:\s\w+)(?:\s\w+)?(?:\s\d+)"""
    # clean_regex = """clean(?:\s\w+)(?:\s\w+)?(?:\s\d+)\swith(?:\s\w+)(?:\s\w+)?(?:\s\d+)"""
    # use_regex = """use(?:\s\w+)(?:\s\w+)?(?:\s\d+)"""
    # heat_regex = """heat(?:\s\w+)(?:\s\w+)?(?:\s\d+)\swith(?:\s\w+)(?:\s\w+)?(?:\s\d+)"""
    # examine_regex = """examine(?:\s\w+)(?:\s\w+)?(?:\s\d+)"""
    # close_regex = """close(?:\s\w+)(?:\s\w+)?(?:\s\d+)"""
    # look_regex = """look"""

    # changing_regexes = [put_regex, goto_regex, take_regex]

    answer = re.match(put_regex,action_string)
    if answer: #Put case
        put_object = answer.group(1)
        put_place = answer.group(2)
        return "put", put_object, put_place

    answer = re.match(goto_regex,action_string)
    if answer: #Put case
        goto_place = answer.group(1)
        return "goto", goto_place, None  

    answer = re.match(take_regex,action_string)
    if answer: #Put case
        take_object = answer.group(1)
        take_place = answer.group(2)
        return "take", take_object, take_place

    # Otherwise return nothing (as it's not changing the state)
    return None, None, None


def update_reference_state_with_action(reference_state, action_string):
    """ Update the reference state with a given command. """
    command, arg1, arg2 = extract_react_command_and_arguments(action_string)

    if command == "goto":
        reference_state["current_location"] = arg1
        reference_state["locations_visited"].append(arg1)
    
    if command == "put":
        # TODO check one actually carries this object.
        reference_state["current_inventory"] = ""

    if command == "take":
        # TODO check one can actually take this object. (harder)
        reference_state["current_inventory"] = arg1


def verify_state_tracking(our_prompt):
    """ 
    Assumes that our prompts are a: 
        - list of Observation, Sys Response, 
        - where sys response is a json with various keys
    """
    reference_state = {
        "locations_visited": [],
        "current_location": "starting location",
        "current_inventory": ""
    }
    keys_to_check = ["current_location","locations_visited","current_inventory"]    
   
    for idx, response in enumerate(our_prompt):
        if idx % 2 == 1:
            our_state = json.loads(response)
            # try:
            for key in keys_to_check:
                assert reference_state[key] == our_state[key],f"States are not the same for: {key} at idx:{idx}\nOurs:\n{our_state[key]}\nTheirs:\n{reference_state[key]}"
            # except AssertionError as e:
            #     print("="*8)
            #     print(f"IDX:{idx} Failed")
            #     print(e)
            
            our_action = our_state["action"]
            update_reference_state_with_action(reference_state, our_action)


if __name__=="__main__":

    all_keys = ["prompt", "goal", "plan", "locations_visited", "current_inventory", "current_location", "current_objective", "thought", "action"]

    # base_prompt = clean_v4_base_1
    error_flag = False
    alignment_error_flag = False
    state_error_flag = False
    key_error_flag = False
    key_renaming_error_flag = False
    return_jsonstate_error_flag = False

    env_mappings = [ENV_TO_EXAMPLE_MAPPING_0, ENV_TO_EXAMPLE_MAPPING_1, ENV_TO_EXAMPLE_MAPPING_2]

    env_types = ["clean","cool","examine","heat","put","puttwo"]
    
    key_renaming_none = {}   
    key_renaming = {
        "prompt": "task_description",
        # "goal": "goal",
        "plan": "global_thought",
        "locations_visited": "places_visited",
        # "current_inventory": "",
        "current_location": "current_place",
        "current_objective": "summary_thought",
        "thought": "thinking",
        "action": "act"
    }

    for env_type in env_types:
        for env_idx,env_mapping in enumerate(env_mappings):
            base_prompt = env_mapping[env_type]
            try:
                base_prompt = remove_keys(base_prompt, keys_to_remove=["prompt","current_objective","non-existant-key"])
                result = transform_baseprompt_into_jsonstate_string(base_prompt)


                try:
                    random_key_orders = random.sample(all_keys,len(all_keys))
                    base_prompt2 = env_mapping[env_type]

                    new_prompt = restructure_prompt(base_prompt2, keys_to_use = random_key_orders, key_renaming = key_renaming_none)
                    result_none = transform_baseprompt_into_jsonstate_string(new_prompt)

                    new_prompt = restructure_prompt(base_prompt2, keys_to_use = random_key_orders, key_renaming = key_renaming)
                    result = transform_baseprompt_into_jsonstate_string(new_prompt)
                    
                    try:
                        assert result_none != result, "Results should be different, as keys are renamed."
                    except AssertionError as e:
                        print("\n======")
                        print(f"{env_idx} - KeyRenaming Error")
                        print(env_type)
                        print(e)  
                        key_renaming_error_flag = True                          
                    
                    try:
                        available_prompt_index = random.sample(list({0,1,2} - {env_idx}),2)

                        result2 = return_jsonstate_prompt(env_type, prompt_ids=[available_prompt_index[0],env_idx], keys_to_use=random_key_orders, key_renaming = key_renaming)
                        result3 = return_jsonstate_prompt(env_type, prompt_ids=[env_idx], keys_to_use=random_key_orders, key_renaming = key_renaming)
                        result4 = return_jsonstate_prompt(env_type, prompt_ids=[available_prompt_index[0]], keys_to_use=random_key_orders, key_renaming = key_renaming)
                        result5 = return_jsonstate_prompt(env_type, prompt_ids=[available_prompt_index[1]], keys_to_use=random_key_orders, key_renaming = key_renaming)

                        diff = get_string_difference(result,result3)
                        assert result==result3, f"JSONSTATE PROMPTS ARE OFF:\n---\n{diff}"
                        assert (result3==result2[len(result4)+2:]) and (result4==result2[:len(result4)]), "Composite JSONSTATE is not working."
                        assert not (result5 in result2) , "Composite JSONSTATE part 2 is not working."

                    except AssertionError as e:
                        print("\n======")
                        print(f"{env_idx} - JsonState Error")
                        print(env_type)
                        print(e)  
                        return_jsonstate_error_flag = True   


                except KeyError as e:
                    print("\n======")
                    print(f"{env_idx} - KeyError")
                    print(env_type)
                    print(e)  
                    key_error_flag = True                     

                try:
                    verify_state_tracking(base_prompt)
                except AssertionError as e:
                    print("\n======")
                    print(f"{env_idx} - StateTrackingError")
                    print(env_type)
                    print(e)  
                    state_error_flag = True 

                try:
                    react_list = return_json_react_examples(env_type, prompt_ids=[env_idx], think_key="think", action_key="action", return_list=True)  
                    success = verify_react_and_ours(base_prompt, react_list[0])
                        
                except AssertionError as e:
                    print("\n======")
                    print(f"{env_idx} - AlignmentError")
                    print(env_type)
                    print(e)                
                    alignment_error_flag=True

            except Exception as e:
                print("======")
                print(f"{env_idx} - Error")
                print(env_type)
                print(e)
                error_flag=True

    failing_test_cases = ""
    if not error_flag:
        print("All prompts in correct format and generate correct strings.")
        failing_test_cases += "error_flag+"

    if not alignment_error_flag:
        print("All Prompts align with React")
        failing_test_cases += "alignment_error_flag+"    

    if not state_error_flag:
        print("All States tracked correctly")
        failing_test_cases += "state_error_flag+"    

    if not key_error_flag:
        print("All Keys are correct")
        failing_test_cases += "key_error_flag+"    

    if not key_renaming_error_flag:
        print("All Key Renaming has worked.")
        failing_test_cases += "key_renaming_error_flag+"    

    if not return_jsonstate_error_flag:
        print("All json states generated correctly.")
        failing_test_cases += "return_jsonstate_error_flag+"    

    error_present = any([error_flag, alignment_error_flag, state_error_flag, key_error_flag, key_renaming_error_flag, return_jsonstate_error_flag])
    if not error_present:
        print("==")
        print("SUCCESS - ALL Manual TESTS PASSED")
    else:
        print("==")
        print(f"FAIL - Cases Failed:{failing_test_cases}")


    example = return_stringstate_prompt("puttwo", keys_to_use=all_keys)
    print(example)

    # #########################
    # Manual test prompt "restructure"
    # #########################
    # env_type = "cool"
    # base_prompt = ENV_TO_EXAMPLE_MAPPING_0[env_type]
    # no_prompt_keys = ["prompt", "goal", "locations_visited", "current_inventory", "current_location", "plan", "current_objective", "thought", "action"]  
    # keys_renamed = {
    #     "prompt": "task_description",
    #     # "goal": "goal",
    #     "plan": "global_thought",
    #     "locations_visited": "locations_visited",
    #     # "current_inventory": "",
    #     "current_location": "current_place",
    #     "current_objective": "summary_thought",
    #     "thought": "thinking",
    #     "action": "act"
    # }

    # new_prompt = restructure_prompt(base_prompt, keys_to_use = no_prompt_keys, key_renaming = keys_renamed)
    # result = transform_baseprompt_into_jsonstate_string(new_prompt)

    # print(result)    



    # print(result)

    # 0 - cool
    # 2 - heat

# """The fridge 1 is closed.""",

    # #########################
    # TO DEBUG SPECIFIC ENVS:
    # #########################

    # env_type = "cool"
    # example_index = 0
    # react_example = return_react_examples(env_type, num=1,  first_id=example_index)
    # # react_example = return_json_react_examples(env_type, num=1, first_id=example_index, version=2, think_key="think", action_key="action")  
    # print("=-"*10)
    # print(react_example)
    # if example_index==0:
    #     base_prompt = ENV_TO_EXAMPLE_MAPPING_0[env_type]
    # elif example_index==1:
    #     base_prompt = ENV_TO_EXAMPLE_MAPPING_1[env_type]
    # elif example_index==2: 
    #     base_prompt = ENV_TO_EXAMPLE_MAPPING_2[env_type]

    # print("++++")
    # base_prompt = remove_keys(base_prompt, keys=["prompt","current_objective","goal","plan","locations_visited","current_inventory","current_location"])
    # result = transform_baseprompt_into_jsonstate_string(base_prompt)
    # print(result)

# EOF

