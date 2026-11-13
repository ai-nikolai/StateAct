"""Tests for the provider registry in stateact.llm.

No provider SDK (or GPU) is needed: the tests inject a fake module into
``sys.modules`` just like a real optional dependency would be.
"""

import sys
import types

import pytest

from stateact import llm


def _install_fake_provider(monkeypatch, name="fake_provider"):
    module = types.ModuleType(name)
    created = []

    class FakeAgent:
        def __init__(self, **kwargs):
            self.kwargs = kwargs
            created.append(self)

    module.FakeAgent = FakeAgent
    monkeypatch.setitem(sys.modules, name, module)
    monkeypatch.setitem(
        llm.PROVIDERS,
        "Fake",
        dict(
            module=name,
            cls="FakeAgent",
            default_model="fake-default",
            pass_temperature=True,
            honor_proposed=True,
        ),
    )
    monkeypatch.setitem(llm.AGENT_MODEL_MAPPING, "Fake", ["fake-default", "fake-other"])
    return created


def test_provider_registry_is_internally_consistent():
    assert set(llm.PROVIDERS) == set(llm.AGENT_MODEL_MAPPING)
    for name, spec in llm.PROVIDERS.items():
        for field in ("module", "cls", "default_model"):
            assert spec.get(field), f"{name} is missing {field}"
        assert spec["default_model"] in llm.AGENT_MODEL_MAPPING[name]


def test_optional_import_success():
    objects, available = llm.optional_import("json", ("loads", "dumps"))
    assert available is True
    assert set(objects) == {"loads", "dumps"}
    assert objects["loads"] is __import__("json").loads


def test_optional_import_missing_module(capsys):
    objects, available = llm.optional_import("definitely_not_a_real_module_xyz", ("x",))
    assert objects == {}
    assert available is False
    assert capsys.readouterr().out  # the original code reported the exception


def test_optional_import_missing_attribute():
    objects, available = llm.optional_import("json", ("definitely_missing",))
    assert objects == {}
    assert available is False


def test_available_providers(monkeypatch):
    monkeypatch.setattr(
        llm,
        "optional_import",
        lambda module_name, attributes: ({}, module_name.endswith(".local")),
    )
    report = llm.available_providers(verbose=False)
    assert report == {
        "OpenAI": False,
        "Anthropic": False,
        "Cohere": False,
        "Nvidia": False,
        "Cerebras": False,
        "VLLM": True,
    }


@pytest.mark.parametrize(
    "proposed,force_model,honor_proposed,expected",
    [
        ("", False, True, "fake-default"),
        ("fake-other", False, True, "fake-other"),
        ("not-allowed", False, True, "fake-default"),
        ("not-allowed", True, True, "not-allowed"),
        ("fake-other", False, False, "fake-default"),
    ],
)
def test_resolve_model(monkeypatch, proposed, force_model, honor_proposed, expected):
    monkeypatch.setitem(
        llm.PROVIDERS,
        "Fake",
        dict(
            module="unused",
            cls="Unused",
            default_model="fake-default",
            pass_temperature=True,
            honor_proposed=honor_proposed,
        ),
    )
    monkeypatch.setitem(llm.AGENT_MODEL_MAPPING, "Fake", ["fake-default", "fake-other"])
    assert llm._resolve_model("Fake", proposed, force_model) == expected


def test_get_agent_and_model_passes_temperature_and_model(monkeypatch):
    created = _install_fake_provider(monkeypatch)
    agent, model = llm.get_agent_and_model(
        "Fake", temperature=0.3, proposed_model="fake-other"
    )
    assert model == "fake-other"
    assert agent is created[0]
    assert agent.kwargs == {"temperature": 0.3, "model": "fake-other"}


def test_get_agent_and_model_without_temperature(monkeypatch):
    created = _install_fake_provider(monkeypatch)
    monkeypatch.setitem(
        llm.PROVIDERS,
        "Fake",
        dict(
            module="fake_provider",
            cls="FakeAgent",
            default_model="fake-default",
            pass_temperature=False,
            honor_proposed=True,
        ),
    )
    agent, model = llm.get_agent_and_model(
        "Fake", max_model_len=4096, seed=1
    )
    assert model == "fake-default"
    assert agent is created[0]
    assert agent.kwargs == {"model": "fake-default", "max_model_len": 4096, "seed": 1}


def test_get_agent_and_model_manual_takes_no_arguments(monkeypatch):
    created = _install_fake_provider(monkeypatch)
    monkeypatch.setitem(
        llm.PROVIDERS,
        "Fake",
        dict(
            module="fake_provider",
            cls="FakeAgent",
            default_model="fake-default",
            pass_temperature=False,
            honor_proposed=False,
            pass_model=False,
        ),
    )
    agent, model = llm.get_agent_and_model("Fake")
    assert model == "fake-default"
    assert agent is created[0]
    assert agent.kwargs == {}


def test_get_agent_and_model_unknown_provider():
    with pytest.raises(ValueError, match="Unknown llm_type"):
        llm.get_agent_and_model("definitely-not-a-provider")


def test_get_agent_and_model_missing_sdk(monkeypatch):
    monkeypatch.setitem(
        llm.PROVIDERS,
        "Fake",
        dict(
            module="definitely_not_a_real_module_xyz",
            cls="FakeAgent",
            default_model="fake-default",
            pass_temperature=False,
            honor_proposed=True,
        ),
    )
    monkeypatch.setitem(llm.AGENT_MODEL_MAPPING, "Fake", ["fake-default"])
    with pytest.raises(ImportError, match="could not be imported"):
        llm.get_agent_and_model("Fake")
