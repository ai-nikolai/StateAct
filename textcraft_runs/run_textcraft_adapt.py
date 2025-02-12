import json
import os
import sys
import json
import re
from tqdm import tqdm
from datetime import datetime

from tenacity import (
    retry,
    stop_after_attempt, # type: ignore
    wait_random_exponential, # type: ignore
    RetryError
)
import copy
import ast
import numpy as np
# sys.path.append("../EnvironmentWebs/environments/")
from textcraft import TextCraft

import random #for the seed
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--llm_type", type=str, default="LOCAL", choices=["GPT", "LOCAL"])
parser.add_argument("--model_local", type=str, default="Qwen/Qwen2.5-0.5B-Instruct")
parser.add_argument("--num_games", type=int, default=30)
parser.add_argument("--max_model_len", type=int, default=16000)
parser.add_argument("--gpus", type=int, default=1, help="Number of GPUs to use")
parser.add_argument("--results_folder", type=str, default="results")
parser.add_argument("--quantization", type=int, default=0, help="Whether a quantized model is being loaded.")
parser.add_argument("--max_depth", type=int, default=1, help="What depth to use for textcraft")
parser.add_argument("--seed", type=int, default=-1, help="Default seed to use for vllm, if -1 then a None / random seed will be chosen.")
parser.add_argument(
    "--agent_type", 
    type=str, 
    default="react", 
    choices=[
        "react", 
        "stateact",
        "stateact_no_thought",
        "stateact_no_state",
        "stateact_no_goal",
    ]
)

args = parser.parse_args()
# LLM_TYPE="GPT"
# LLM_TYPE="LOCAL"
LLM_TYPE=args.llm_type


# SEED = random.randint(0, 2**32 - 1) if args.seed == -1 else args.seed
SEED = None if args.seed == -1 else args.seed
print(f"The used seed: {SEED}")

AGENT_TYPE = args.agent_type

if LLM_TYPE=="GPT":
    import openai
    openai.api_key = os.environ["OPENAI_API_KEY"]
    LM = 'gpt-3.5-turbo-instruct'

elif LLM_TYPE=="LOCAL":
    LM=args.model_local
    MAX_PROMPT_LENGTH=args.max_model_len
max_runs = 40
# max_depth = 4
# num_games = 200 #originally 200
# verbose = False

# env = TextCraft(minecraft_dir="../EnvironmentWebs/environments/textcraft/")
env = TextCraft()
environment_context = '''You can perform the following actions to interact with the environment: 
- craft [target count] [target item] using [count] [item]
- get [count] [item]
- inventory
Here [count] is a place holder for number of object, and [item] is placeholder for name of object.

'''

# @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(15))
def llm(prompt, stop=["\n"], max_tokens=150, plan=False):
    if plan:
        max_tokens=800
        stop=['\n\n']
    else:
        max_tokens=150
        stop=['\n']
    if 'davinci' in LM or 'instruct' in LM:
        if plan:
            prompt= 'You are an helpful assistant helping me play a simple version of Minecraft. ' + prompt,
        else:
            prompt='You are a helpful assistant playing Minecraft\n' + environment_context + prompt,
        response = openai.Completion.create(
        model=LM,
        prompt=prompt,
        temperature=0,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=stop
        )
        return response["choices"][0]["text"]
    elif 'gpt-3.5-turbo' in LM or 'gpt-4' in LM:
        if plan:
            messages=[
                {"role": "system", "content": 'You are an helpful assistant helping me play a simple version of Minecraft.'},
                {"role": "user", "content": prompt}
            ],
        else:
            messages=[
            {"role": "system", "content": 'You are a helpful assistant playing Minecraft.' + environment_context},
            {"role": "user", "content": prompt}
            ],
        response = openai.ChatCompletion.create(
        model=LM,
        messages=messages,
        temperature=0,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=stop
        )
        choices = response["choices"]
        completion_objs = [choice.message for choice in choices]
        completions = [completion.content for completion in completion_objs]
        return completions[0]

# @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(25))
# def plan_llm(prompt, stop=["\n\n"]):
#     if 'davinci' in LM or 'turbo-instruct' in LM:
#       if isinstance(prompt, list): prompt = prompt[0]
#       response = openai.Completion.create(
#         model=LM,
#         prompt= 'You are an helpful assistant helping me play a simple version of Minecraft. ' + prompt,
#         temperature=0,
#         max_tokens=800,
#         top_p=1,
#         frequency_penalty=0.0,
#         presence_penalty=0.0,
#         # stop=stop
#       )
#       return response["choices"][0]["text"]
#     elif 'gpt-3.5-turbo' in LM or 'gpt-4' in LM:
#       if isinstance(prompt, list): prompt = prompt[0]
#       init_prmpt = 'You are an helpful assistant helping me play a simple version of Minecraft.'
#       response = openai.ChatCompletion.create(
#       model=LM,
#       messages=[
#         {"role": "system", "content": init_prmpt},
#         {"role": "user", "content": prompt}
#       ],
#       temperature=0,
#       max_tokens=800,
#       top_p=1,
#       frequency_penalty=0.0,
#       presence_penalty=0.0,
#       # stop=stop
#       )
#       choices = response["choices"]
#       completion_objs = [choice.message for choice in choices]
#       completions = [completion.content for completion in completion_objs]
#       return completions[0]


def local_llm_closure():
    from vllm import LLM, SamplingParams
    QUANTIZATION=bool(args.quantization)
    # Initialize model with HF token authentication
    if not QUANTIZATION:
        llm = LLM(
            model=LM,
            trust_remote_code=True,
            max_model_len=MAX_PROMPT_LENGTH,
            gpu_memory_utilization=0.90,
            dtype="auto",
            tensor_parallel_size=args.gpus,
            # download_dir="/tmp/model_cache", 
        )
    else:
        llm = LLM(
            model=LM,
            trust_remote_code=True,
            max_model_len=MAX_PROMPT_LENGTH,
            gpu_memory_utilization=0.95,
            dtype="auto",
            quantization="bitsandbytes", 
            load_format="bitsandbytes",
            tensor_parallel_size=args.gpus,    
            # download_dir="/tmp/model_cache", 
        )
    def llm_local(prompt, stop=None, max_tokens=150, plan=False):
        if not stop:
            if plan:
                stop=['\n\n']
            else:
                stop=['\n']  
        if plan:
            max_tokens=800
        else:
            max_tokens=150
        # Set sampling parameters
        sampling_params = SamplingParams(
            temperature=0,
            max_tokens=max_tokens,
            stop=stop,
            seed=SEED #TODO make adaptable between runs
        )
        
        # Generate completion
        outputs = llm.generate(prompt, sampling_params)
        return outputs[0].outputs[0].text
    
    return llm_local


if LLM_TYPE=="GPT":
    # plan_llm = plan_llm
    # llm = llm
    call_llm = llm
elif LLM_TYPE=="LOCAL":
    # plan_llm = local_llm_closure()
    # llm = plan_llm
    call_llm = local_llm_closure()


def parse_expression(expression):
    stack = []
    current = {}
    for token in re.findall(r'Step \d+|AND|OR|\(|\)', expression):
        if token.startswith('Step'):
            if 'steps' not in current:
                current['steps'] = []
            current['steps'].append(int(token.split()[1]))
        elif token in ('AND', 'OR'):
            current['logic'] = token
        elif token == '(':
            stack.append(current)
            current = {}
        elif token == ')':
            closed = current
            current = stack.pop()
            if 'steps' not in current:
                current['steps'] = []
            current['steps'].append(closed)
    return current

def plan_to_args(plan, keyword = 'Step', lkey = 'execution order'):
    args = []
    lines = plan.split('\n')
    for line in lines:
        if line.startswith(keyword): args.append(re.sub(r'{} \d+: '.format(keyword), '', line))
        if lkey in line.lower():
            logic = line.split(': ')[-1]
    args_lookup = {i+1: args[i] for i in range(len(args))}
    try:
        return fetch_args(args_lookup, parse_expression(logic))
    except: 
        return {'steps': args, 'logic': 'AND'}

def print_completion(completion):
    out_lines = ['\t-----']
    lines = completion.split('\n')
    lines = ['\t' + line for line in lines]
    out_lines.extend(lines)
    out_lines.append('\t-----')
    out_text = "\n".join(out_lines)
    print(out_text)
    return

def fetch_args(args_lookup, logic_exp):
    out = copy.deepcopy(logic_exp)
    assert 'steps' in logic_exp.keys()
    for s, step in enumerate(logic_exp['steps']):
        if isinstance(step, int):
            out['steps'][s] = args_lookup[step]
        elif isinstance(step, dict):
            out['steps'][s] = fetch_args(args_lookup, step)
    return out

# def textcraft_run_react(prompt, to_print=True, ob='', env=env, max_runs=40, output_term=True):
#     if isinstance(prompt, list): 
#         init_prompt = copy.copy(prompt)
#         init_prompt.append({'type': 'env', 'content': ob})
#     else:
#         init_prompt = prompt + '\n' + ob + '\n>'
#     prompt = ''
#     action_history = []
#     max_patience = 5
#     pat_ctr = 0
#     success = False
#     terminate = False
#     num_runs = 0
#     if to_print:
#         print(ob)
#         sys.stdout.flush()
#     for i in range(1, max_runs):
        
#         action = call_llm(init_prompt + prompt, stop=['\n']).strip()
#         num_runs += 1
#         action = action.lstrip('> ')
        
#         observation, reward, done, _,  info = env.step('> ' + action)

#         if action.startswith('think:'):
#             observation = 'OK.'
#             if 'task completed' in action.lower(): done = True; success = True
#             if 'task failed' in action.lower(): done = True; success = False
#         else: action_history.append(action)
#         if observation.startswith("Could not") or observation == "OK.": 
#             pat_ctr += 1
#             if pat_ctr == max_patience: terminate = True; break
#         else: pat_ctr = 0
#         if to_print:
#             print(f'Act {i}: {action}\nObs {i}: {observation}')
#             sys.stdout.flush()
#         prompt += f' {action}\n{observation}\n>'
#         if reward: success = True; terminate = False
#         if done:
#             return reward, success, terminate, prompt, action_history, num_runs
#     if not done: success = False; terminate = True
#     return 0, success, terminate,  prompt, action_history, num_runs


def clean_action(action, prompt_type="react"):
    """
    If the prompt is stateact-like.
    """
    if prompt_type=="react":
        return action
    elif "stateact" in prompt_type:
        # print(action)
        # print(action.split("action: "))
        try:
            action_split = action.split('action: ')[1]
            action_split = action_split.split('\n')[0]
            return action_split
        except Exception as e:
            print("\n\n\n\n\n\n===================\nWe are receiving a fault in the model prediction.\n\n\n\n\n")
            print(e)
            return action


def textcraft_run_adapt(prompt, to_print=True, ob='', env=env, max_runs=40, output_term=True, prompt_type="react"):
    if isinstance(prompt, list): 
        init_prompt = copy.copy(prompt)
        init_prompt.append({'type': 'env', 'content': ob})
    else:
        init_prompt = prompt + '\n' + ob + '\n>'
    prompt = ''
    action_history = []
    max_patience = 8
    pat_ctr = 0
    success = False
    terminate = False
    num_runs = 0
    if to_print:
        print(env.step('inventory'))
        print(ob)
        sys.stdout.flush()
    for i in range(1, max_runs):
        if prompt_type=="react":
            action = call_llm(init_prompt + prompt, stop=['\n']).strip()
        elif "stateact" in prompt_type:
            action = call_llm(init_prompt + prompt, stop=['\n\n']).strip()
            # print(f"=============\nWe received action: {action}")
        else:
            raise NotImplementedError(f"Prompt type {prompt_type} is not available.")

        num_runs += 1
        action = action.lstrip('> ')
        
        observation, reward, done, _,  info = env.step(action)
        
        if 'task completed' in action.lower(): done = True; success = True
        if 'task failed' in action.lower(): done = True; success = False
        if action.startswith('think'):
            observation = 'OK.'
            if 'task completed' in action.lower(): done = True; success = True
            if 'task failed' in action.lower(): done = True; success = False
        else: 
            action = clean_action(action, prompt_type=prompt_type)
            action_history.append(action)
        if "Could not" in observation or observation == "OK.": 
            pat_ctr += 1
            if pat_ctr == max_patience: terminate = True; break
        else: pat_ctr = 0
        if to_print:
            print(f'Act {i}: {action}\nObs {i}: {observation}')
            # print(pat_ctr)
            sys.stdout.flush()
        prompt += f' {action}\n{observation}\n>'
        if reward > 0: success = True; terminate = False
        if done:
            return reward, success, terminate, prompt, action_history, num_runs
    if not done: success = False; terminate = True
    return 0, success, terminate,  prompt, action_history, num_runs

plan_prompt = '''Your task is to come up with a short plan to help me accomplish my goal in a couple of steps using at most ONE of the provided crafting commands. You can take the help of crafting commands below to create new objects. 
Craft command can be understood as follows: craft [target] using [ingredients], where target is item/object generated by the craft command as output and ingredient are the inputs. You are given an agent that can "craft" or "fetch" objects.

Here is are some examples.

Crafting commands:
craft 3 dark oak sign using 6 dark oak planks, 1 stick
craft 4 dark oak planks using 1 dark oak log
craft 1 stick using 1 planks
craft 4 stick using 2 bamboo
craft 4 oak planks using 1 oak log
craft 1 dark oak fence using 2 stick, 4 dark oak planks
craft 1 warped stairs using 6 warped planks
craft 3 oak sign using 6 oak planks, 1 stick

Goal: craft dark oak sign.

# Think: My target is a dark oak sign. From the list of crafting commands, only 1 command generates my target: craft 3 dark oak sign using 6 oak planks, 1 stick. I will use this command to devise a plan. My ingredients are: 6 dark oak planks, 1 stick. I should first get all the ingredients and then use the crafting command.
Step 1: fetch 6 dark oak planks
Step 2: fetch 1 stick
# Think: Now that I have collected the input ingredients, I can craft the dark oak sign using given command.
Step 3: craft dark oak sign using 6 dark oak planks, 1 stick
# Think: To succeed, I need to perform all these steps, one after the other. So I need to use the "AND" operator.
Execution Order: (Step 1 AND Step 2 AND Step 3)

Goal: fetch 6 dark oak planks.

# Think: My target is 6 dark oak planks. From the list of crafting commands, only 1 command generates my target: craft 4 dark oak planks using 1 dark oak log. My ingredients are: 1 dark oak log. To successfully accomplish the goal, I should first get all the ingredients and then use the crafting command.
Step 1: fetch 1 dark oak log
# Think: Now that I have collected the input ingredients, I can craft dark oak planks using given command. I know that I cannot use a partial recipe.
Step 2: craft 4 dark oak planks using 1 dark oak log
# Think: This gives me 4 dark oak planks which is less than my desired 6 dark oak planks. I know that I cannot use a partial recipe. So my goal is not satisfied, I need to craft more dark oak planks by repeating Step 2 one more time.
Step 3: craft 4 dark oak planks using 1 dark oak log
# Think: To succeed, I need to perform all these steps, one after the other. So I need to use the "AND" operator.
Execution Order: (Step 1 AND Step 2 AND Step 3)

Here is a different goal with different craft commands. Your task is to come up with a short plan to help me accomplish my goal in a couple of steps using at most ONE of the provided crafting commands. You can take the help of crafting commands below to create new objects. Keep in mind that:
- It is okay to generate more target objects than your goal.
- Be very careful with the count of objects, SAME object counts mentioned in the input crafting command. 
- You cannot use a partial crafting command recipe, i.e. if the recipe generates 2 objects you CANNOT alter it to produce just 1. 
- Also, you can use ONLY 1 crafting command in your plan.
'''




# ####################################################
# STATEACT PROMPTS
# ####################################################

atomic_examples_stateact = {
'craft_with_ingredients':'''Crafting commands:
craft 3 dark oak sign using 6 dark oak planks, 1 stick
craft 4 dark oak planks using 1 dark oak log
craft 1 stick using 1 planks
craft 4 stick using 2 bamboo
craft 4 oak planks using 1 oak log
craft 1 dark oak fence using 2 stick, 4 dark oak planks
craft 1 warped stairs using 6 warped planks
craft 3 oak sign using 6 oak planks, 1 stick

Goal: craft dark oak sign

> goal: craft dark oak sign
inventory: Unknown
think: I should check if I can fetch dark oak sign directly from the environment or the inventory.
action: inventory

Inventory: [stick] (1) [dark oak planks] (6)

> goal: craft dark oak sign
inventory: 1 stick, 6 dark oak planks
think: None
action: get dark oak sign

Could not find dark oak sign

> goal: craft dark oak sign
inventory: 1 stick, 6 dark oak planks
think: I cannot get dark oak sign directly, I need to craft it. From the crafting commands, I can use: craft dark oak sign using 6 dark oak planks, 1 stick. Ingredients needed: 6 dark oak planks, 1 stick. Input assumption: I have all the neccessary ingredients in my inventory. Let me verify this first.
action: inventory

Inventory: [stick] (1) [dark oak planks] (6)

> goal: craft dark oak sign
inventory: 1 stick, 6 dark oak planks
think: I found my ingredients: 6 dark oak planks, 1 stick in my inventory. My assumption is true, I can proceed. I will use the crafting command: craft dark oak sign using 6 dark oak planks
action: craft 3 dark oak sign using 6 dark oak planks, 1 stick

Crafted 3 minecraft:dark_oak_sign

> goal: craft dark oak sign
inventory: 3 dark oak sign
think: None
action: inventory

Inventory: [dark oak sign] (3)

> goal: craft dark oak sign
inventory: 3 dark oak sign
think: I now have dark oak sign in my inventory. Task Completed!
action: None
''', 
'craft_with_ingredients_gen':'''Goal: fetch 2 dark oak logs.

> goal: fetch 2 dark oak logs
inventory: unknown
think: I should check my inventory first, to see if I already have dark oak sign. Otherwise, I will directly try to get it from the environment.
action: inventory

Inventory: [stick] (1)

> goal: fetch 2 dark oak logs
inventory: 1 stick
think: None
action: get 2 dark oak logs

Got 2 dark oak logs

> goal: fetch 2 dark oak logs
inventory: 1 stick, 2 dark oak log
think: None
action: inventory

Inventory: [dark oak log] (2) [stick] (1)

> goal: fetch 2 dark oak logs
inventory: 1 stick, 2 dark oak log
think: I have 2 dark oak logs in my inventory. Task Completed!
action: None
'''
}

stateact_trajectory = '''Goal: craft 2 oak planks

> goal: craft 2 oak planks
inventory: unknown
think: I should check if I can fetch dark oak sign directly from the environment or the inventory.
action: intentory

Inventory: [stick] (1) 

> goal: craft 2 oak planks
inventory: 1 stick
think: None
action: get 2 oak planks

Could not find 2 oak planks

> goal: craft 2 oak planks
inventory: 1 stick
think: I cannot get oak planks directly, I need to craft it. From the crafting commands, I can use: craft 4 oak planks using 1 oak log. Ingredients needed: 1 dark oak log. Input assumption: I have the ingredients needed in my inventory. Let me verify this first.
action: inventory

Inventory: [stick] (1) 

> goal: craft 2 oak planks
inventory: 1 stick
think: My assumption is false. I need to get the ingredients: 1 oak log first.
action: get 1 oak log

Got 1 oak log

> goal: craft 2 oak planks
inventory: 1 stick, 1 oak log
think: None
action: craft 4 oak planks using 1 oak log

Crafted 4 minecraft:oak_planks

> goal: craft 2 oak planks
inventory: 1 stick, 4 oak planks
think: None
action: inventory

Inventory: [stick] (1) [oak_planks] (4)

> goal: craft 2 oak planks
inventory: 1 stick, 4 oak planks
think: I now have 2 oak planks in my inventory. Task Completed!
acition: None
'''

# NO THOUGHT
atomic_examples_stateact_no_thought = {
'craft_with_ingredients':'''Crafting commands:
craft 3 dark oak sign using 6 dark oak planks, 1 stick
craft 4 dark oak planks using 1 dark oak log
craft 1 stick using 1 planks
craft 4 stick using 2 bamboo
craft 4 oak planks using 1 oak log
craft 1 dark oak fence using 2 stick, 4 dark oak planks
craft 1 warped stairs using 6 warped planks
craft 3 oak sign using 6 oak planks, 1 stick

Goal: craft dark oak sign

> goal: craft dark oak sign
inventory: Unknown
action: inventory

Inventory: [stick] (1) [dark oak planks] (6)

> goal: craft dark oak sign
inventory: 1 stick, 6 dark oak planks
action: get dark oak sign

Could not find dark oak sign

> goal: craft dark oak sign
inventory: 1 stick, 6 dark oak planks
action: inventory

Inventory: [stick] (1) [dark oak planks] (6)

> goal: craft dark oak sign
inventory: 1 stick, 6 dark oak planks
action: craft 3 dark oak sign using 6 dark oak planks, 1 stick

Crafted 3 minecraft:dark_oak_sign

> goal: craft dark oak sign
inventory: 3 dark oak sign
action: inventory

Inventory: [dark oak sign] (3)

> goal: craft dark oak sign
inventory: 3 dark oak sign
action: None
''', 
'craft_with_ingredients_gen':'''Goal: fetch 2 dark oak logs.

> goal: fetch 2 dark oak logs
inventory: unknown
action: inventory

Inventory: [stick] (1)

> goal: fetch 2 dark oak logs
inventory: 1 stick
action: get 2 dark oak logs

Got 2 dark oak logs

> goal: fetch 2 dark oak logs
inventory: 1 stick, 2 dark oak log
action: inventory

Inventory: [dark oak log] (2) [stick] (1)

> goal: fetch 2 dark oak logs
inventory: 1 stick, 2 dark oak log
action: None
'''
}

stateact_no_thought_trajectory = '''Goal: craft 2 oak planks

> goal: craft 2 oak planks
inventory: unknown
action: intentory

Inventory: [stick] (1) 

> goal: craft 2 oak planks
inventory: 1 stick
action: get 2 oak planks

Could not find 2 oak planks

> goal: craft 2 oak planks
inventory: 1 stick
action: inventory

Inventory: [stick] (1) 

> goal: craft 2 oak planks
inventory: 1 stick
action: get 1 oak log

Got 1 oak log

> goal: craft 2 oak planks
inventory: 1 stick, 1 oak log
action: craft 4 oak planks using 1 oak log

Crafted 4 minecraft:oak_planks

> goal: craft 2 oak planks
inventory: 1 stick, 4 oak planks
action: inventory

Inventory: [stick] (1) [oak_planks] (4)

> goal: craft 2 oak planks
inventory: 1 stick, 4 oak planks
acition: None
'''


# NO STATE
atomic_examples_stateact_no_state = {
'craft_with_ingredients':'''Crafting commands:
craft 3 dark oak sign using 6 dark oak planks, 1 stick
craft 4 dark oak planks using 1 dark oak log
craft 1 stick using 1 planks
craft 4 stick using 2 bamboo
craft 4 oak planks using 1 oak log
craft 1 dark oak fence using 2 stick, 4 dark oak planks
craft 1 warped stairs using 6 warped planks
craft 3 oak sign using 6 oak planks, 1 stick

Goal: craft dark oak sign

> goal: craft dark oak sign
think: I should check if I can fetch dark oak sign directly from the environment or the inventory.
action: inventory

Inventory: [stick] (1) [dark oak planks] (6)

> goal: craft dark oak sign
think: None
action: get dark oak sign

Could not find dark oak sign

> goal: craft dark oak sign
think: I cannot get dark oak sign directly, I need to craft it. From the crafting commands, I can use: craft dark oak sign using 6 dark oak planks, 1 stick. Ingredients needed: 6 dark oak planks, 1 stick. Input assumption: I have all the neccessary ingredients in my inventory. Let me verify this first.
action: inventory

Inventory: [stick] (1) [dark oak planks] (6)

> goal: craft dark oak sign
think: I found my ingredients: 6 dark oak planks, 1 stick in my inventory. My assumption is true, I can proceed. I will use the crafting command: craft dark oak sign using 6 dark oak planks
action: craft 3 dark oak sign using 6 dark oak planks, 1 stick

Crafted 3 minecraft:dark_oak_sign

> goal: craft dark oak sign
think: None
action: inventory

Inventory: [dark oak sign] (3)

> goal: craft dark oak sign
think: I now have dark oak sign in my inventory. Task Completed!
action: None
''', 
'craft_with_ingredients_gen':'''Goal: fetch 2 dark oak logs.

> goal: fetch 2 dark oak logs
think: I should check my inventory first, to see if I already have dark oak sign. Otherwise, I will directly try to get it from the environment.
action: inventory

Inventory: [stick] (1)

> goal: fetch 2 dark oak logs
think: None
action: get 2 dark oak logs

Got 2 dark oak logs

> goal: fetch 2 dark oak logs
think: None
action: inventory

Inventory: [dark oak log] (2) [stick] (1)

> goal: fetch 2 dark oak logs
think: I have 2 dark oak logs in my inventory. Task Completed!
action: None
'''
}

stateact_no_state_trajectory = '''Goal: craft 2 oak planks

> goal: craft 2 oak planks
think: I should check if I can fetch dark oak sign directly from the environment or the inventory.
action: intentory

Inventory: [stick] (1) 

> goal: craft 2 oak planks
think: None
action: get 2 oak planks

Could not find 2 oak planks

> goal: craft 2 oak planks
think: I cannot get oak planks directly, I need to craft it. From the crafting commands, I can use: craft 4 oak planks using 1 oak log. Ingredients needed: 1 dark oak log. Input assumption: I have the ingredients needed in my inventory. Let me verify this first.
action: inventory

Inventory: [stick] (1) 

> goal: craft 2 oak planks
think: My assumption is false. I need to get the ingredients: 1 oak log first.
action: get 1 oak log

Got 1 oak log

> goal: craft 2 oak planks
think: None
action: craft 4 oak planks using 1 oak log

Crafted 4 minecraft:oak_planks

> goal: craft 2 oak planks
think: None
action: inventory

Inventory: [stick] (1) [oak_planks] (4)

> goal: craft 2 oak planks
think: I now have 2 oak planks in my inventory. Task Completed!
acition: None
'''


# NO GOAL
atomic_examples_stateact_no_goal = {
'craft_with_ingredients':'''Crafting commands:
craft 3 dark oak sign using 6 dark oak planks, 1 stick
craft 4 dark oak planks using 1 dark oak log
craft 1 stick using 1 planks
craft 4 stick using 2 bamboo
craft 4 oak planks using 1 oak log
craft 1 dark oak fence using 2 stick, 4 dark oak planks
craft 1 warped stairs using 6 warped planks
craft 3 oak sign using 6 oak planks, 1 stick

Goal: craft dark oak sign

> inventory: Unknown
think: I should check if I can fetch dark oak sign directly from the environment or the inventory.
action: inventory

Inventory: [stick] (1) [dark oak planks] (6)

> inventory: 1 stick, 6 dark oak planks
think: None
action: get dark oak sign

Could not find dark oak sign

> inventory: 1 stick, 6 dark oak planks
think: I cannot get dark oak sign directly, I need to craft it. From the crafting commands, I can use: craft dark oak sign using 6 dark oak planks, 1 stick. Ingredients needed: 6 dark oak planks, 1 stick. Input assumption: I have all the neccessary ingredients in my inventory. Let me verify this first.
action: inventory

Inventory: [stick] (1) [dark oak planks] (6)

> inventory: 1 stick, 6 dark oak planks
think: I found my ingredients: 6 dark oak planks, 1 stick in my inventory. My assumption is true, I can proceed. I will use the crafting command: craft dark oak sign using 6 dark oak planks
action: craft 3 dark oak sign using 6 dark oak planks, 1 stick

Crafted 3 minecraft:dark_oak_sign

> inventory: 3 dark oak sign
think: None
action: inventory

Inventory: [dark oak sign] (3)

> inventory: 3 dark oak sign
think: I now have dark oak sign in my inventory. Task Completed!
action: None
''', 
'craft_with_ingredients_gen':'''Goal: fetch 2 dark oak logs.

> inventory: unknown
think: I should check my inventory first, to see if I already have dark oak sign. Otherwise, I will directly try to get it from the environment.
action: inventory

Inventory: [stick] (1)

> inventory: 1 stick
think: None
action: get 2 dark oak logs

Got 2 dark oak logs

> inventory: 1 stick, 2 dark oak log
think: None
action: inventory

Inventory: [dark oak log] (2) [stick] (1)

> inventory: 1 stick, 2 dark oak log
think: I have 2 dark oak logs in my inventory. Task Completed!
action: None
'''
}

stateact_no_goal_trajectory = '''Goal: craft 2 oak planks

> inventory: unknown
think: I should check if I can fetch dark oak sign directly from the environment or the inventory.
action: intentory

Inventory: [stick] (1) 

> inventory: 1 stick
think: None
action: get 2 oak planks

Could not find 2 oak planks

> inventory: 1 stick
think: I cannot get oak planks directly, I need to craft it. From the crafting commands, I can use: craft 4 oak planks using 1 oak log. Ingredients needed: 1 dark oak log. Input assumption: I have the ingredients needed in my inventory. Let me verify this first.
action: inventory

Inventory: [stick] (1) 

> inventory: 1 stick
think: My assumption is false. I need to get the ingredients: 1 oak log first.
action: get 1 oak log

Got 1 oak log

> inventory: 1 stick, 1 oak log
think: None
action: craft 4 oak planks using 1 oak log

Crafted 4 minecraft:oak_planks

> inventory: 1 stick, 4 oak planks
think: None
action: inventory

Inventory: [stick] (1) [oak_planks] (4)

> inventory: 1 stick, 4 oak planks
think: I now have 2 oak planks in my inventory. Task Completed!
acition: None
'''







# ####################################################
# NORMAL PART OF THE PROMPTS
# ####################################################
atomic_examples = {
'craft_with_ingredients':'''Crafting commands:
craft 3 dark oak sign using 6 dark oak planks, 1 stick
craft 4 dark oak planks using 1 dark oak log
craft 1 stick using 1 planks
craft 4 stick using 2 bamboo
craft 4 oak planks using 1 oak log
craft 1 dark oak fence using 2 stick, 4 dark oak planks
craft 1 warped stairs using 6 warped planks
craft 3 oak sign using 6 oak planks, 1 stick

Goal: craft dark oak sign

> think: I should check if I can fetch dark oak sign directly from the environment or the inventory.
OK.

> inventory: 
Inventory: [stick] (1) [dark oak planks] (6)

> get dark oak sign
Could not find dark oak sign

> think: I cannot get dark oak sign directly, I need to craft it. From the crafting commands, I can use: craft dark oak sign using 6 dark oak planks, 1 stick. Ingredients needed: 6 dark oak planks, 1 stick. Input assumption: I have all the neccessary ingredients in my inventory. Let me verify this first.
OK.

> inventory
Inventory: [stick] (1) [dark oak planks] (6)

> think: I found my ingredients: 6 dark oak planks, 1 stick in my inventory. My assumption is true, I can proceed. I will use the crafting command: craft dark oak sign using 6 dark oak planks
OK.

> craft 3 dark oak sign using 6 dark oak planks, 1 stick
Crafted 3 minecraft:dark_oak_sign

> inventory 
Inventory: [dark oak sign] (3)

> think: I now have dark oak sign in my inventory. Task Completed!
OK.
''', 
'craft_with_ingredients_gen':'''Goal: fetch 2 dark oak logs.

> think: I should check my inventory first, to see if I already have dark oak sign. Otherwise, I will directly try to get it from the environment.
OK.

> inventory
Inventory: [stick] (1)

> get 2 dark oak logs.
Got 2 dark oak logs

> inventory
Inventory: [dark oak log] (2) [stick] (1)

> think: I have 2 dark oak logs in my inventory. Task Completed!
OK.
'''
}

react_trajectory = '''Goal: craft 2 oak planks

> think: I should check if I can fetch dark oak sign directly from the environment or the inventory.
OK.

> inventory: 
Inventory: [stick] (1) 

> get 2 oak planks
Could not find 2 oak planks

> think: I cannot get oak planks directly, I need to craft it. From the crafting commands, I can use: craft 4 oak planks using 1 oak log. Ingredients needed: 1 dark oak log. Input assumption: I have the ingredients needed in my inventory. Let me verify this first.
OK.

> inventory
Inventory: [stick] (1) 

> think: My assumption is false. I need to get the ingredients: 1 oak log first.
OK.

> get 1 oak log
Got 1 oak log

> craft 4 oak planks using 1 oak log
Crafted 4 minecraft:oak_planks

> inventory
Inventory: [stick] (1) [oak_planks] (4)

> think: I now have 2 oak planks in my inventory. Task Completed!
OK.
'''

atomic_exec_prompt = '''You are given few useful crafting recipes to craft items in Minecraft. Crafting commands are of the format "craft [target object] using [input ingredients]". You can either "fetch" an object (ingredients) from the inventory or the environment or "craft" (target) using any of the crafting commands. You can use ONLY these crafting commands provided, do not use your own crafting commands. However, if the crafting command uses a generic ingredient like "planks", you can use special types of the same ingredient e.g. "dark oak planks" in the command instead. '''
# REACT PART
if AGENT_TYPE=="react":
    atomic_exec_prompt+="""For any other natural language or thoughts, use prefix 'think: '."""
    atomic_exec_prompt+="""\n\nHere is a demo of how to fetch and craft objects.\n\n"""
    atomic_exec_prompt +=  '\n\n'.join(atomic_examples[k] for k in atomic_examples.keys()) + '\n'
    # Pure React
    atomic_exec_prompt += 'Here is an example of a complex goal.\n\n' + react_trajectory + '\n'

elif AGENT_TYPE=="stateact":
    # STATEACT ALTERNATIVE
    atomic_exec_prompt+="""\n\nHere is a demo of how to fetch and craft objects.\n\n"""
    atomic_exec_prompt +=  '\n\n'.join(atomic_examples_stateact[k] for k in atomic_examples_stateact.keys()) + '\n'
    # Pure Stateact
    atomic_exec_prompt += 'Here is an example of a complex goal.\n\n' + stateact_trajectory + '\n'

elif AGENT_TYPE=="stateact_no_thought":
    # STATEACT ALTERNATIVE
    atomic_exec_prompt+="""\n\nHere is a demo of how to fetch and craft objects.\n\n"""
    atomic_exec_prompt +=  '\n\n'.join(atomic_examples_stateact_no_thought[k] for k in atomic_examples_stateact_no_thought.keys()) + '\n'
    # Pure Stateact
    atomic_exec_prompt += 'Here is an example of a complex goal.\n\n' + stateact_no_thought_trajectory + '\n'

elif AGENT_TYPE=="stateact_no_state":
    # STATEACT ALTERNATIVE
    atomic_exec_prompt+="""\n\nHere is a demo of how to fetch and craft objects.\n\n"""
    atomic_exec_prompt +=  '\n\n'.join(atomic_examples_stateact_no_state[k] for k in atomic_examples_stateact_no_state.keys()) + '\n'
    # Pure Stateact
    atomic_exec_prompt += 'Here is an example of a complex goal.\n\n' + stateact_no_state_trajectory + '\n'

elif AGENT_TYPE=="stateact_no_goal":
    # STATEACT ALTERNATIVE
    atomic_exec_prompt+="""\n\nHere is a demo of how to fetch and craft objects.\n\n"""
    atomic_exec_prompt +=  '\n\n'.join(atomic_examples_stateact_no_goal[k] for k in atomic_examples_stateact_no_goal.keys()) + '\n'
    # Pure Stateact
    atomic_exec_prompt += 'Here is an example of a complex goal.\n\n' + stateact_no_goal_trajectory + '\n'

atomic_exec_prompt += "Now here is a different goal. You can use these crafting commands to accomplish the goal. When you the desired item in your inventory, think: Task Completed! If you have tried your best but cannot proceed, think: task failed!\n" 


def plan_and_run(
        commands, 
        task, 
        idx, 
        env, 
        prompt, 
        past_action_checkpoint=[], 
        past_info_prop = '', 
        depth = 1, 
        num_runs = 0, 
        verbose = False, 
        comm_state = False, 
        ttype='', 
        max_depth=1,
        prompt_type="react"
    ):
    # print("===================")
    # print(f"running prompt_type:{prompt_type}")
    plan_list = []

    info_prop = past_info_prop 
    action_checkpoint = past_action_checkpoint
    running_completion = ''
    if isinstance(task, str):
        if verbose: print('Starting... ' + task, ' at depth ' + str(depth))
        custom_ob = commands + '\nGoal: ' + task + '\n'
        if len(info_prop):
            if verbose: print('Loading ...', info_prop)
            if LM in ["gpt-3.5-turbo", "gpt-4", "gpt-3.5-turbo-0301"]:
                r, succ, term, completion, act_history, num = textcraft_run_adapt(prompt, to_print=False, ob=custom_ob + '\n' +  info_prop , env=env, prompt_type=prompt_type) #'\nResume from loaded checkpoint, last finished action:\n' +

            else:
                r, succ, term, completion, act_history, num = textcraft_run_adapt(prompt, to_print=False, ob=custom_ob + '\n' +  info_prop , env=env, prompt_type=prompt_type) #'\nResume from loaded checkpoint, last finished action:\n' +
        else:
            r, succ, term, completion, act_history, num = textcraft_run_adapt(prompt, to_print=False, ob=custom_ob, env=env, prompt_type=prompt_type)
            # r, succ, term, env, trace, actions, depth, plans, num_runs
        if verbose: 
            print_completion(completion)
            print('Task ({}) Success: '.format(task), succ)
        plan_list.append(task + ' at depth ' + str(depth) + ', success: ' + str(succ))
        num_runs += num
        if succ or depth >= max_depth:
            if succ: action_checkpoint.extend(act_history)
            running_completion += completion + '\n'
            if succ:
                info_prop = '> inventory\n'
                obs, _, _, _, _ = env.step('inventory')
                info_prop += obs + '\n'
            return r, succ, term, env, running_completion, action_checkpoint, depth, plan_list, num_runs, info_prop
        
        
        plan = call_llm(plan_prompt + '\n' + custom_ob, plan=True)
        if verbose: 
            print('-----')
            print_completion(plan)
            print('-----')
        plan_steps = plan_to_args(plan)
        if verbose: print(plan_steps)
        num_runs += 1
        if len(plan_steps['steps']) == 1: 
            plan_steps = plan_steps['steps'][0]
            if type(plan_steps) == str: plan_steps={'steps':[plan_steps]}
            if 'logic' not in plan_steps.keys():
                try:
                    logic = plan_steps['logic']
                except: logic = "AND"; plan_steps['logic'] = logic
        depth += 1
    else:
        plan_steps = task
        try: logic = plan_steps['logic']
        except: logic = "AND"; plan_steps['logic'] = logic

    if verbose: print('Identified subtasks... ' + str(plan_steps['steps']) + ' at depth {}, logic: '.format(depth) + str(plan_steps['logic']))
    plan_list.append(str(plan_steps['steps']) + ' at depth ' + str(depth) + ' and logic ' + str(plan_steps['logic']))
    for sub_task in plan_steps['steps']:
        if verbose: print('At subtask: ' + str(sub_task))
        r, succ, term, env, completion, act_history, _, decomp_plans, num, info_prop = plan_and_run(commands, sub_task, idx, env, prompt, past_action_checkpoint=action_checkpoint, past_info_prop=info_prop, depth=depth, verbose=verbose, comm_state=comm_state, ttype=ttype, max_depth=max_depth, prompt_type=prompt_type) #Need to propogate info_prop here.
        plan_list.extend(decomp_plans)
        num_runs += num
        if plan_steps['logic'].lower() == 'or':
            if succ:
                if not set(act_history).issubset(action_checkpoint): action_checkpoint.extend(act_history)
                running_completion += completion + '\n'
                info_prop = '> inventory\n'
                obs, _, _, _, _ = env.step('inventory')
                info_prop += obs + '\n'
                return r, succ, term, env, running_completion, action_checkpoint, depth, plan_list, num_runs, info_prop
        # If reached here you have succeeded.
        if succ:
            if not set(act_history).issubset(action_checkpoint): action_checkpoint.extend(act_history)
            running_completion += completion + '\n'
            info_prop = '> inventory\n'
            obs, _, _, _, _ = env.step('inventory')
            info_prop += obs + '\n'
    
        if plan_steps['logic'].lower() == 'and' and not succ:
            return r, succ, term, env, running_completion, action_checkpoint, depth, plan_list, num_runs, info_prop

    return r, succ, term, env, running_completion, action_checkpoint, depth, plan_list, num_runs, info_prop\


# ##############################3
# Main PARAMETERS

max_depth=args.max_depth #for full ADAPT: max_depth =4; for REACT max_depth = 1
# AGENT="REACT"
num_games = args.num_games #originally 200
verbose = True


## Running main loop for evaluation
outputs = {}
pbar = tqdm(list(range(num_games)))
rs = []; cnts = []
depths = []
rate = 0.0
pbar.set_postfix({'success rate': rate})
env = TextCraft()

print(f"Running AGENTTYPE: {AGENT_TYPE} with depth: {max_depth}")
for idx in pbar:
    obs, info = env.reset(seed=idx)
    commands, task = obs.split('Goal: ')
    trace = []
    r, succ, term, env, trace, actions, depth, plans, num_runs, _ = plan_and_run(commands, task, idx, env, atomic_exec_prompt, past_action_checkpoint=[], comm_state=False, verbose=verbose, max_depth=max_depth, prompt_type=AGENT_TYPE)
    rs.append(r)
    cnts.append(1)
    depths.append(depth)
    rate = sum(rs)/sum(cnts)
    outputs[f'env_{idx}'] = {'problem': task, 'commands': commands, 'trace': trace, 'plans': plans, 'reward': r, 'runs': num_runs}
    pbar.set_postfix({'rate': rate})
outputs['overall'] = {'rate': sum(rs) / sum(cnts),  'count': cnts, "num_envs":sum(cnts), "depths":depths}

final_rate = sum(rs) / sum(cnts)
total_count = sum(cnts)
average_depth = sum(depths) / sum(cnts)

import string

def clean_model_string(s):
    # Convert to lowercase
    s = s.lower()
    # Replace / with _
    s = s.replace('/', '_')
    # Replace all punctuation (except _) with -
    # Create a translation table that maps all punctuation to - except _
    punct_to_dash = str.maketrans({p: '-' for p in string.punctuation if p != '_'})
    s = s.translate(punct_to_dash)
    return s

clean_model_name = clean_model_string(LM)

print(f"For model {LM}, received score: {outputs['overall']} ")
dest_file = os.path.join(
    args.results_folder,
    '{}.json'.format(f'ADaPT_{AGENT_TYPE}_{clean_model_name}_maxd{max_depth}_max_run_{max_runs}_test_num{num_games}')
)
print("===================FILE NAME")
print(dest_file)
dest_file_csv = os.path.join(
    args.results_folder,
    'results.csv'
)
os.makedirs('/'.join(dest_file.split('/')[:-1]), exist_ok=True)
t = open(dest_file, 'w+')
json.dump(outputs, t, indent=4)
t.close()

current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Check if file exists and create if not
if not os.path.exists(dest_file_csv):
    with open(dest_file_csv, 'w') as f:
        f.write("agent,date,model,rate,total_count,average_depth,max_depth\n")

with open(dest_file_csv, 'a') as f:
    f.write(f"{AGENT_TYPE},{current_date},{clean_model_name},{final_rate},{total_count},{average_depth},{max_depth}\n")
