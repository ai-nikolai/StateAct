"""Tests for alfworld_runs/model_registry.py."""

import pytest

from stateact import backends as agents
import model_registry as llm


def test_provider_registry_is_internally_consistent():
    assert set(llm.PROVIDERS) == set(llm.AGENT_MODEL_MAPPING)
    for name, spec in llm.PROVIDERS.items():
        assert {"cls", "backend", "default_model"} <= set(spec), name
        assert spec["backend"] in {"url", "local", "manual"}
        assert spec["default_model"] in llm.AGENT_MODEL_MAPPING[name]


def test_available_providers(monkeypatch):
    monkeypatch.setattr(
        llm, "_module_available", lambda name: name == "requests"
    )
    assert llm.available_providers(verbose=False) == {
        "URL": True,
        "VLLM": False,
        "Manual": True,
    }


@pytest.mark.parametrize(
    "proposed,force_model,honor_proposed,expected",
    [
        ("", False, True, "default"),
        ("allowed", False, True, "allowed"),
        ("not-allowed", False, True, "default"),
        ("not-allowed", True, True, "not-allowed"),
        ("allowed", False, False, "default"),
    ],
)
def test_resolve_model(monkeypatch, proposed, force_model, honor_proposed, expected):
    monkeypatch.setitem(
        llm.PROVIDERS,
        "Fake",
        dict(cls=agents.URLChatAgent, backend="url",
             default_model="default", honor_proposed=honor_proposed),
    )
    monkeypatch.setitem(llm.AGENT_MODEL_MAPPING, "Fake", ["default", "allowed"])
    assert llm._resolve_model("Fake", proposed, force_model) == expected


def test_resolve_model_accepts_any_model_for_generic_url(monkeypatch):
    monkeypatch.setitem(
        llm.PROVIDERS,
        "Fake",
        dict(cls=agents.URLChatAgent, backend="url", default_model="default",
             honor_proposed=True, accept_any_model=True),
    )
    monkeypatch.setitem(llm.AGENT_MODEL_MAPPING, "Fake", ["default"])
    assert llm._resolve_model("Fake", "custom/model", False) == "custom/model"


def test_get_manual_agent():
    agent, model = llm.get_agent_and_model("Manual")
    assert isinstance(agent, agents.ManualAgent)
    assert model == "Manual"


def test_get_url_agent(monkeypatch):
    monkeypatch.setattr(llm, "_module_available", lambda name: True)
    agent, model = llm.get_agent_and_model(
        "URLChat", temperature=0.3, proposed_model="gpt-3.5-turbo-1106",
        llm_url="https://example.test/v1/chat/completions",
        llm_api_key="secret",
    )
    assert isinstance(agent, agents.URLChatAgent)
    assert model == "gpt-3.5-turbo-1106"
    assert agent.url == "https://example.test/v1/chat/completions"
    assert agent.api_key == "secret"
    assert agent.temperature == 0.3


def test_get_url_agent_requires_url(monkeypatch):
    monkeypatch.setattr(llm, "_module_available", lambda name: True)
    with pytest.raises(ValueError, match="needs a URL"):
        llm.get_agent_and_model("URLChat")


def test_get_url_agent_missing_requests(monkeypatch):
    monkeypatch.setattr(llm, "_module_available", lambda name: False)
    with pytest.raises(ImportError, match="requests"):
        llm.get_agent_and_model("URLChat", llm_url="http://x")


def test_get_local_agent_missing_backend(monkeypatch):
    monkeypatch.setattr(
        llm, "available_providers", lambda verbose=True: {"VLLM": False}
    )
    with pytest.raises(ImportError, match="vllm"):
        llm.get_agent_and_model("VLLMChat")


def test_get_agent_unknown_provider():
    with pytest.raises(ValueError, match="Unknown llm_type"):
        llm.get_agent_and_model("definitely-not-a-provider")


def test_legacy_names_are_url_backed():
    url_types = [
        "OpenAIChat", "OpenAIChatText", "OpenAIChatTextSampling", "OpenAIText",
        "AnthropicChat", "AnthropicText", "CohereChat", "CohereText",
        "CohereChatText", "NvidiaChatText", "CerebrasChatText",
    ]
    for name in url_types:
        assert llm.PROVIDERS[name]["backend"] == "url"
    assert llm.PROVIDERS["VLLMChat"]["backend"] == "local"
    assert llm.PROVIDERS["Manual"]["backend"] == "manual"
