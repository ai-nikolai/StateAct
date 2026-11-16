"""Tests for the OpenAI-compatible LLM client."""

import pytest

from stateact import llms


def test_llm_builds_chat_endpoint(monkeypatch):
    calls = []

    def fake_chat(url, model, messages, **kwargs):
        calls.append((url, model, messages, kwargs))
        return "answer"

    monkeypatch.setattr(llms, "url_chat", fake_chat)
    llm = llms.LLM("model", url="http://host:8000/v1", api_key_env="KEY")

    assert llm("hello") == "answer"
    url, model, messages, _kwargs = calls[0]
    assert url == "http://host:8000/v1/chat/completions"
    assert model == "model"
    assert messages == [{"role": "user", "content": "hello"}]


def test_llm_builds_completion_endpoint(monkeypatch):
    calls = []

    def fake_completion(url, model, prompt, **kwargs):
        calls.append((url, model, prompt, kwargs))
        return "answer"

    monkeypatch.setattr(llms, "url_completion", fake_completion)
    llm = llms.LLM("model", url="http://host/v1", mode="completion")

    assert llm("hello") == "answer"
    assert calls[0][0] == "http://host/v1/completions"


def test_llm_accepts_full_endpoint(monkeypatch):
    calls = []

    def fake_chat(url, model, messages, **kwargs):
        calls.append(url)
        return "answer"

    monkeypatch.setattr(llms, "url_chat", fake_chat)
    llm = llms.LLM("model", url="http://host/custom/chat/completions")
    llm("hello")
    assert calls == ["http://host/custom/chat/completions"]


def test_llm_from_env(monkeypatch):
    monkeypatch.setenv("STATEACT_LLM_URL", "http://host/v1")
    monkeypatch.setenv("STATEACT_LLM_API_KEY", "secret")
    monkeypatch.setenv("STATEACT_LLM_MODE", "completion")
    llm = llms.LLM.from_env("model")
    assert llm.url == "http://host/v1"
    assert llm.api_key == "secret"
    assert llm.mode == "completion"


def test_llm_requires_url(monkeypatch):
    monkeypatch.delenv("STATEACT_LLM_URL", raising=False)
    with pytest.raises(ValueError, match="STATEACT_LLM_URL"):
        llms.LLM("model")
