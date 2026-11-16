"""Model selection for StateAct.

There are only two backends:

* ``local`` - a HuggingFace model served by vLLM (``VLLMChat``).
* ``url`` - any OpenAI-compatible chat/completions endpoint (``URLChat``,
  ``URLText``, plus the legacy provider names below).
* ``manual`` - human input.

No provider SDK is imported. The legacy ``--llm_type`` names are kept as
aliases so existing experiment YAML and command lines keep working; they only
change the default URL, API-key environment variable and prompt layout.
"""

import importlib.util

from stateact import backends as agents

__all__ = [
    "AGENT_MODEL_MAPPING",
    "PROVIDERS",
    "available_providers",
    "get_agent_and_model",
]

# Models accepted per --llm_type. A proposed model outside the list falls back
# to the default unless --force_model is passed.
AGENT_MODEL_MAPPING = {
    "URLChat": [
        "gpt-3.5-turbo-0125",
        "gpt-3.5-turbo-1106",
        "gpt-4o-mini",
    ],
    "URLText": ["gpt-3.5-turbo-instruct", "davinci-002"],
    "AnthropicChat": ["claude-2.1", "claude-3-haiku-20240307", "claude-3-sonnet-20240229"],
    "AnthropicText": ["claude-2.1", "claude-3-haiku-20240307", "claude-3-sonnet-20240229"],
    "CohereChat": ["command", "command-nightly", "command-r", "command-r-plus"],
    "CohereText": ["command", "command-nightly", "command-r", "command-r-plus"],
    "CohereChatText": ["command", "command-nightly", "command-r", "command-r-plus"],
    "OpenAIChat": [
        "gpt-3.5-turbo-0125",
        "gpt-4-turbo-preview",
        "gpt-3.5-turbo-0301",
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-1106",
    ],
    "OpenAIChatText": [
        "gpt-3.5-turbo-0125",
        "gpt-4-turbo-preview",
        "gpt-3.5-turbo-0301",
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-1106",
        "gpt-4o-mini",
    ],
    "OpenAIText": ["davinci-002", "gpt-3.5-turbo-instruct"],
    "OpenAIChatTextSampling": [
        "gpt-3.5-turbo-0125",
        "gpt-4-turbo-preview",
        "gpt-3.5-turbo-0301",
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-1106",
    ],
    "NvidiaChatText": [
        "mistralai/mixtral-8x22b-instruct-v0.1",
        "meta/llama-3.1-8b-instruct",
        "meta/llama-3.1-70b-instruct",
    ],
    "CerebrasChatText": ["llama3.1-8b", "llama3.1-70b"],
    "VLLMChat": [
        "Qwen/Qwen2.5-0.5B-Instruct",
        "Qwen/Qwen2.5-1.5B-Instruct",
        "Qwen/Qwen2.5-3B-Instruct",
        "Qwen/Qwen2.5-7B-Instruct",
        "Qwen/Qwen2.5-14B-Instruct",
    ],
    "Manual": ["Manual"],
}

# Each row is one ``--llm_type``. ``cls`` is instantiated in
# :func:`get_agent_and_model`; ``backend`` drives the availability check.
PROVIDERS = {
    "URLChat": dict(
        cls=agents.URLChatAgent, backend="url",
        default_model="gpt-3.5-turbo-0125", honor_proposed=True,
        accept_any_model=True),
    "URLText": dict(
        cls=agents.URLTextAgent, backend="url",
        default_model="gpt-3.5-turbo-instruct", honor_proposed=True,
        accept_any_model=True),
    "OpenAIChat": dict(
        cls=agents.OpenAIChatAgent, backend="url",
        default_model="gpt-3.5-turbo-0125", honor_proposed=True),
    "OpenAIChatText": dict(
        cls=agents.OpenAIChatTextAgent, backend="url",
        default_model="gpt-3.5-turbo-0125", honor_proposed=True),
    "OpenAIChatTextSampling": dict(
        cls=agents.OpenAIChatTextSamplingAgent, backend="url",
        default_model="gpt-3.5-turbo-0125", honor_proposed=True),
    "OpenAIText": dict(
        cls=agents.OpenAITextAgent, backend="url",
        default_model="gpt-3.5-turbo-instruct", honor_proposed=True),
    "AnthropicChat": dict(
        cls=agents.AnthropicChatAgent, backend="url",
        default_model="claude-2.1", honor_proposed=True),
    "AnthropicText": dict(
        cls=agents.AnthropicTextAgent, backend="url",
        default_model="claude-2.1", honor_proposed=False),
    "CohereChat": dict(
        cls=agents.CohereChatAgent, backend="url",
        default_model="command-r", honor_proposed=True),
    "CohereText": dict(
        cls=agents.CohereTextAgent, backend="url",
        default_model="command-r", honor_proposed=True),
    "CohereChatText": dict(
        cls=agents.CohereChatTextAgent, backend="url",
        default_model="command-r", honor_proposed=True),
    "NvidiaChatText": dict(
        cls=agents.NvidiaChatTextAgent, backend="url",
        default_model="meta/llama-3.1-8b-instruct", honor_proposed=True),
    "CerebrasChatText": dict(
        cls=agents.CerebrasChatTextAgent, backend="url",
        default_model="llama3.1-8b", honor_proposed=True),
    "VLLMChat": dict(
        cls=agents.VLLMChatAgent, backend="local",
        default_model="Qwen/Qwen2.5-0.5B-Instruct", honor_proposed=True),
    "Manual": dict(
        cls=agents.ManualAgent, backend="manual",
        default_model="Manual", honor_proposed=False),
}


def _module_available(name):
    try:
        return importlib.util.find_spec(name) is not None
    except (ImportError, ValueError):
        return False


def available_providers(verbose=True):
    """Return ``{"URL": bool, "VLLM": bool, "Manual": True}``.

    URL models need ``requests``; local models need ``vllm`` and
    ``transformers``. Neither is required for the rest of the package.
    """
    report = {
        "URL": _module_available("requests"),
        "VLLM": _module_available("vllm") and _module_available("transformers"),
        "Manual": True,
    }
    if verbose:
        print("Model backends available:")
        for name, ok in report.items():
            print(f"  {name}: {ok}")
    return report


def _resolve_model(llm_type, proposed_model, force_model):
    """Pick the model for ``llm_type``, warning like the original did."""
    spec = PROVIDERS[llm_type]
    model = spec["default_model"]

    if not proposed_model or not spec["honor_proposed"]:
        return model

    # Generic URL agents accept any model name (the endpoint defines what is
    # valid); the legacy provider aliases keep the historical allow-list.
    if spec.get("accept_any_model") or proposed_model in AGENT_MODEL_MAPPING[llm_type]:
        return proposed_model

    print("WARNING: Proposed Model is not in LIST!!!")
    if force_model:
        print("WARNING: Using your model in anycase.")
        return proposed_model
    return model


def get_agent_and_model(llm_type, temperature=0.0, proposed_model="",
                        force_model=False, llm_url=None, llm_api_key=None,
                        llm_api_key_env=None, **kwargs):
    """Return ``(agent, model)`` for ``--llm_type``.

    ``llm_url`` / ``llm_api_key`` / ``llm_api_key_env`` override the defaults
    for URL-backed agents, which makes arbitrary OpenAI-compatible endpoints
    usable without adding a provider. Unknown types raise ``ValueError``.
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
    backend = spec["backend"]

    if backend == "manual":
        return spec["cls"](), model

    if backend == "local":
        if not available_providers(verbose=False)["VLLM"]:
            raise ImportError(
                "llm_type 'VLLMChat' needs vllm and transformers "
                "(pip install -r alfworld_runs/requirements.txt)."
            )
        return spec["cls"](model=model, **kwargs), model

    if not _module_available("requests"):
        raise ImportError(
            "URL-based models need the 'requests' package "
            "(pip install requests)."
        )

    url = llm_url or kwargs.pop("url", None)
    api_key = llm_api_key or kwargs.pop("api_key", None)
    api_key_env = llm_api_key_env or kwargs.pop("api_key_env", None)
    agent = spec["cls"](
        temperature=temperature,
        model=model,
        url=url,
        api_key=api_key,
        api_key_env=api_key_env,
        **kwargs,
    )
    return agent, model
