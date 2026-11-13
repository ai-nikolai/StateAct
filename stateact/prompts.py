"""Few-shot prompt assembly and the ``--agent`` -> prompt-builder dispatch.

Extracted from ``alfworld_runs/alfworld_run.py`` (the format constants,
``generate_prompt_from_example``, ``save_prompt_file``, ``get_prompt_example``)
and from ``alfworld_runs/alfworld_ablation_generator.py`` (the six base-example
imports and the three ``ENV_TO_EXAMPLE_MAPPING_*`` tables that differed only by
which variant index they selected).

Design note
-----------
The few-shot *content* stays exactly where it was: the modules under
``alfworld_runs/prompts/`` are the paper artifacts and are not rewritten here.
What this module removes is the duplication around them: one registry
(:data:`BASE_EXAMPLE_MODULES`) replaces six hard-coded imports and three
near-identical dicts, and the builders are resolved lazily so that
``import stateact.prompts`` works without the ``alfworld_runs`` directory on
``sys.path``.
"""

import importlib

__all__ = [
    "BASE_PROMPT1",
    "BASE_PROMPT2",
    "TASK_MESSAGE",
    "OPENING_MARK",
    "CLOSING_MARK",
    "HINTS",
    "INSTRUCTIONS",
    "BASE_EXAMPLE_MODULES",
    "AGENT_TYPES",
    "generate_prompt_from_example",
    "save_prompt_file",
    "load_base_example_variants",
    "prompt_name_for",
    "default_alfworld_builders",
    "get_prompt_example",
]


#################################################################
#Prompt format constants
#################################################################

BASE_PROMPT1 = "Interact with a household to solve a task."
BASE_PROMPT2 = "You will interact with the environment to solve the given task."

TASK_MESSAGE = "Here is the task."

OPENING_MARK = ""
CLOSING_MARK = ""
HINTS = ""
INSTRUCTIONS = ""


#################################################################
#Few-shot example registry (ALFWorld task types)
#################################################################

# env_type -> (module holding the base examples, variable prefix).
# The modules define `{prefix}_v4_base_0`, `{prefix}_v4_base_1` and
# `{prefix}_v4_base_2`; which one is used is the `--prompt_ids` argument.
BASE_EXAMPLE_MODULES = {
    "clean":   ("prompts.alfworld_prompts_utils_v4_clean_base",   "clean"),
    "cool":    ("prompts.alfworld_prompts_utils_v4_cool_base",    "cool"),
    "examine": ("prompts.alfworld_prompts_utils_v4_examine_base", "examine"),
    "heat":    ("prompts.alfworld_prompts_utils_v4_heat_base",    "heat"),
    "put":     ("prompts.alfworld_prompts_utils_v4_put_base",     "put"),
    "puttwo":  ("prompts.alfworld_prompts_utils_v4_puttwo_base",  "puttwo"),
}

# The agent types the dispatch below understands (also the --agent choices).
AGENT_TYPES = ("react", "jsonreact", "agentbench", "ours", "ours-text", "stateact", "act")


def load_base_example_variants(env_type):
    """Return the three base-example variants for ``env_type`` as a list.

    ``[variants[0], variants[1], variants[2]]`` is exactly what the three
    ``ENV_TO_EXAMPLE_MAPPING_*`` dicts in the ablation generator held, but
    derived from a single table instead of six imports plus three literals.
    """
    try:
        module_name, prefix = BASE_EXAMPLE_MODULES[env_type]
    except KeyError:
        raise KeyError(
            f"Unknown env_type {env_type!r}; expected one of "
            f"{sorted(BASE_EXAMPLE_MODULES)}"
        ) from None

    module = importlib.import_module(module_name)
    return [getattr(module, f"{prefix}_v4_base_{index}") for index in (0, 1, 2)]


#################################################################
#Generic prompt assembly
#################################################################

def generate_prompt_from_example(examples, return_raw_prompt=False, number_of_examples=1,
                                 base_prompt="", instructions="", hints=""):
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


def save_prompt_file(file_path, raw_prompt):
    """ Saves a prompt file """
    with open(file_path, "w") as file:
        file.write(raw_prompt)


#################################################################
#Prompt naming + dispatch
#################################################################

def prompt_name_for(agent_type, prompt_ids, keys_to_use=(), version=1):
    """Return the ``--trial_name``-style prompt identifier for a config.

    Mirrors the naming in the original ``get_prompt_example``, e.g.
    ``stringstate-1_0-k-goal+thought+action``.
    """
    prompt_id_string = '_'.join([str(y) for y in prompt_ids])

    if agent_type == "react":
        return f"react-{prompt_id_string}"
    if agent_type == "agentbench":
        return f"agentbench-v{version}"
    if agent_type == "jsonreact":
        return f"jsonreact-{prompt_id_string}-v{version}"

    keys_to_use = list(keys_to_use)
    if agent_type == "act":
        keys_to_use = ["action"]
        return f"act-{prompt_id_string}"

    keys_string = '+'.join([str(y) for y in keys_to_use])
    if agent_type == "ours":
        return f"jsonstate-{prompt_id_string}-k-{keys_string}"
    if agent_type in ("ours-text", "stateact"):
        return f"stringstate-{prompt_id_string}-k-{keys_string}"

    raise NotImplementedError(f"Trying to call agent_type: {agent_type}, but it doesn't exist.")


def default_alfworld_builders():
    """Resolve the ALFWorld prompt builders.

    These live in ``alfworld_runs/`` as top-level modules (not a package), so
    this import only works when that directory is on ``sys.path`` - which it is
    when the entry points are run as scripts, the documented way.
    """
    try:
        ablation = importlib.import_module("alfworld_ablation_generator")
        react_utils = importlib.import_module("alfworld_react_prompt_utils")
    except ImportError as exc:
        raise ImportError(
            "The ALFWorld prompt builders could not be imported. Run the entry "
            "points from inside alfworld_runs/ (e.g. "
            "`cd alfworld_runs && python3 alfworld_run.py ...`), or pass "
            "`builders=` explicitly."
        ) from exc

    return {
        "react": react_utils.return_react_examples,
        "jsonreact": react_utils.return_json_react_examples,
        "agentbench": react_utils.return_agentbench_prompts,
        "ours": ablation.return_jsonstate_prompt,
        "ours-text": ablation.return_stringstate_prompt,
        "stateact": ablation.return_stringstate_prompt,
    }


def get_prompt_example(agent_type, env_type, prompt_ids, version, generate_prompt=True,
                       keys_to_use=[], key_renaming={}, builders=None):
    """ Get name of prompt and example prompts.

    ``builders`` maps agent_type -> builder callable; it defaults to the
    ALFWorld builders (see :func:`default_alfworld_builders`) and can be
    injected so that other environments/tests can reuse the dispatch.
    """
    if agent_type not in AGENT_TYPES:
        raise NotImplementedError(f"Trying to call agent_type: {agent_type}, but it doesn't exist.")

    new_base_prompt = ""
    num_examples = len(prompt_ids)
    prompt_name = prompt_name_for(agent_type, prompt_ids, keys_to_use, version)

    prompt_example = ""
    if generate_prompt:
        if builders is None:
            builders = default_alfworld_builders()

        if agent_type == "react":
            prompt_example = builders["react"](env_type, prompt_ids=prompt_ids)

        elif agent_type == "agentbench":
            num_examples = 1
            prompt_example, new_base_prompt = builders["agentbench"](
                env_type, return_base=True, version=version)

        elif agent_type == "jsonreact":
            prompt_example = builders["jsonreact"](
                env_type, prompt_ids=prompt_ids, version=version)

        elif agent_type == "ours":
            prompt_example = builders["ours"](
                env_type, prompt_ids=prompt_ids, keys_to_use=keys_to_use,
                key_renaming=key_renaming)

        elif agent_type in ("ours-text", "stateact"):
            prompt_example = builders["stateact"](
                env_type, prompt_ids=prompt_ids, keys_to_use=keys_to_use,
                key_renaming=key_renaming)

        elif agent_type == "act":
            # "act" is StateAct with only the action key.
            prompt_example = builders["stateact"](
                env_type, prompt_ids=prompt_ids, keys_to_use=["action"],
                key_renaming=key_renaming)

    if generate_prompt:
        return prompt_name, prompt_example, new_base_prompt, num_examples
    else:
        return prompt_name
