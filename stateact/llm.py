"""Provider imports and ``llamp`` agent construction.

The original ``alfworld_run.py`` had six near-identical ``try/except`` blocks
(one per provider) and a ~170 line ``if/elif`` chain in ``get_agent_and_model``
where twelve branches repeated the same "is the proposed model in the allowed
list?" logic.

This module replaces both with:

* :func:`optional_import` - one helper for "import if the SDK is installed".
* :data:`PROVIDERS` - a table describing, per ``--llm_type``: where the class
  lives, its default model, whether it accepts ``temperature``, and which
  models are allowed.
* :func:`get_agent_and_model` - behaviourally identical to the original,
  driven by that table.

Installing every SDK is *not* required: a provider whose SDK is missing is
simply reported as unavailable, exactly as before.
"""

import importlib

__all__ = [
    "AGENT_MODEL_MAPPING",
    "PROVIDERS",
    "optional_import",
    "available_providers",
    "get_agent_and_model",
]


def optional_import(module_name, attributes):
    """Import ``attributes`` from ``module_name`` if the SDK is installed.

    Returns ``(objects, available)`` where ``objects`` is a dict mapping each
    requested attribute name to the imported object (empty when unavailable).
    Never raises: mirrors the original per-provider ``try/except`` blocks so a
    missing SDK degrades to "provider unavailable" rather than a crash.
    """
    try:
        module = importlib.import_module(module_name)
    except Exception as exc:  # noqa: BLE001 - deliberately broad, SDKs vary
        print(exc)
        return {}, False

    objects = {}
    try:
        for attribute in attributes:
            objects[attribute] = getattr(module, attribute)
    except AttributeError as exc:
        print(exc)
        return {}, False

    return objects, True


# Models that the original code accepts for each --llm_type. Kept verbatim so
# that "proposed model not in list" warnings behave exactly as before.
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
    "VLLMChat" : [
        "Qwen/Qwen2.5-0.5B-Instruct",
        "Qwen/Qwen2.5-1.5B-Instruct", 
        "Qwen/Qwen2.5-14B-Instruct",
    ],
    "Manual" : ["Manual"],
}


# One row per --llm_type. Field meanings:
#   module            : importable module holding the class
#   cls               : class name inside that module
#   default_model     : model used when none (or a disallowed one) is proposed
#   pass_temperature  : whether the constructor takes temperature=...
#   pass_model        : whether the constructor accepts model=...
#   honor_proposed    : whether a proposed model overrides default_model.
#                       NOTE: "AnthropicText" is False because the original
#                       code assigned model = "claude-2.1" *after* the
#                       proposed-model check, silently ignoring the proposal.
#                       Preserved as-is so the refactor changes no behaviour;
#                       see the report / ALFWorld README for the caveat.
PROVIDERS = {
    "AnthropicChat": dict(
        module="llamp.llms.api", cls="AnthropicChat",
        default_model="claude-2.1", pass_temperature=True, honor_proposed=True),
    "CohereChat": dict(
        module="llamp.llms.api", cls="CohereChat",
        default_model="command-r", pass_temperature=True, honor_proposed=True),
    "OpenAIChat": dict(
        module="llamp.llms.api", cls="OpenAIChat",
        default_model="gpt-3.5-turbo-0125", pass_temperature=True, honor_proposed=True),
    "AnthropicText": dict(
        module="llamp.llms.api", cls="AnthropicText",
        default_model="claude-2.1", pass_temperature=True, honor_proposed=False),
    "CohereText": dict(
        module="llamp.llms.api", cls="CohereText",
        default_model="command-r", pass_temperature=True, honor_proposed=True),
    "OpenAIText": dict(
        module="llamp.llms.api", cls="OpenAIText",
        default_model="gpt-3.5-turbo-instruct", pass_temperature=True, honor_proposed=True),
    "CohereChatText": dict(
        module="llamp.llms.api", cls="CohereChatText",
        default_model="command-r", pass_temperature=True, honor_proposed=True),
    "OpenAIChatText": dict(
        module="llamp.llms.api", cls="OpenAIChatText",
        default_model="gpt-3.5-turbo-0125", pass_temperature=True, honor_proposed=True),
    "OpenAIChatTextSampling": dict(
        module="llamp.llms.api", cls="OpenAIChatTextSampling",
        default_model="gpt-3.5-turbo-0125", pass_temperature=True, honor_proposed=True),
    "NvidiaChatText": dict(
        module="llamp.llms.api", cls="NvidiaChatText",
        default_model="meta/llama-3.1-8b-instruct", pass_temperature=True, honor_proposed=True),
    "CerebrasChatText": dict(
        module="llamp.llms.api", cls="CerebrasChatText",
        default_model="llama3.1-8b", pass_temperature=True, honor_proposed=True),
    "VLLMChat": dict(
        module="llamp.llms.local", cls="VLLMChat",
        default_model="Qwen/Qwen2.5-0.5B-Instruct", pass_temperature=False, honor_proposed=True),
    "Manual": dict(
        module="llamp.llms", cls="Manual",
        default_model="Manual", pass_temperature=False, honor_proposed=False,
        pass_model=False),
}


# The import blocks in the original file reported availability in this order.
_AVAILABILITY_REPORT = [
    ("OpenAI", "llamp.llms.api", ("OpenAIChat", "OpenAIChatText", "OpenAIText", "OpenAIChatTextSampling")),
    ("Anthropic", "llamp.llms.api", ("AnthropicChat", "AnthropicText")),
    ("Cohere", "llamp.llms.api", ("CohereChat", "CohereChatText", "CohereText")),
    ("Nvidia", "llamp.llms.api", ("NvidiaChatText",)),
    ("Cerebras", "llamp.llms.api", ("CerebrasChatText",)),
    ("VLLM", "llamp.llms.local", ("VLLMChat",)),
]


def available_providers(verbose=True):
    """Probe which provider SDKs can be imported.

    Returns a dict like ``{"OpenAI": True, "VLLM": False, ...}`` and, when
    ``verbose``, prints the same summary the original import block printed.
    """
    report = {}
    for label, module_name, attributes in _AVAILABILITY_REPORT:
        _objects, available = optional_import(module_name, attributes)
        report[label] = available

    if verbose:
        print("End of imports. Imported:")
        for label in ("OpenAI", "Anthropic", "Cohere", "Nvidia", "Cerebras", "VLLM"):
            print(f"{label}: {report[label]}")

    return report


def _resolve_model(llm_type, proposed_model, force_model):
    """Pick the model for ``llm_type``, warning like the original did."""
    spec = PROVIDERS[llm_type]
    model = spec["default_model"]

    if not proposed_model or not spec["honor_proposed"]:
        return model

    if proposed_model in AGENT_MODEL_MAPPING[llm_type]:
        return proposed_model

    print("WARNING: Proposed Model is not in LIST!!!")
    if force_model:
        print("WARNING: Using your model in anycase.")
        return proposed_model
    return model


def get_agent_and_model(llm_type, temperature=0.0, proposed_model="", force_model=False, **kwargs):
    """Return ``(agent, model)`` for the given ``--llm_type``.

    Same contract and defaults as the original ``alfworld_run.py`` function:
    unknown ``llm_type`` raises ``ValueError`` (the original raised
    ``UnboundLocalError`` because no branch matched).
    """
    print(llm_type)
    print(proposed_model)

    if llm_type not in PROVIDERS:
        raise ValueError(
            f"Unknown llm_type: {llm_type!r}. "
            f"Expected one of: {sorted(PROVIDERS)}"
        )

    spec = PROVIDERS[llm_type]
    model = _resolve_model(llm_type, proposed_model, force_model)

    objects, available = optional_import(spec["module"], (spec["cls"],))
    if not available:
        raise ImportError(
            f"llm_type {llm_type!r} needs {spec['module']}.{spec['cls']}, "
            f"which could not be imported. Install that provider's SDK "
            f"(see the relevant *_runs/requirements.txt)."
        )

    agent_class = objects[spec["cls"]]
    if spec.get("pass_model", True) is False:
        # Manual takes no arguments at all.
        agent = agent_class()
    elif spec["pass_temperature"]:
        agent = agent_class(temperature=temperature, model=model)
    else:
        # VLLMChat takes no temperature, but does take the vLLM kwargs
        # (max_model_len, quantization, gpus, seed, ...).
        agent = agent_class(model=model, **kwargs)

    return agent, model
