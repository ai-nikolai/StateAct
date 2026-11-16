"""Tests for stateact.backends.

Everything is mocked: no network, no GPU, no provider SDK.
"""

import json
import sys
import types
from types import SimpleNamespace

import pytest

from stateact import backends as agents


class FakeResponse:
    def __init__(self, status_code, data=None, text=None):
        self.status_code = status_code
        self._data = data
        self.text = text if text is not None else json.dumps(data or {})

    def json(self):
        if self._data is None:
            raise ValueError("not json")
        return self._data


def _install_fake_requests(monkeypatch, responses):
    module = types.ModuleType("requests")

    class RequestException(Exception):
        pass

    calls = []

    def post(url, json=None, headers=None, timeout=None):
        calls.append({"url": url, "json": json, "headers": headers, "timeout": timeout})
        result = responses.pop(0)
        if isinstance(result, Exception):
            raise result
        return result

    module.RequestException = RequestException
    module.post = post
    monkeypatch.setitem(sys.modules, "requests", module)
    monkeypatch.setattr(agents.time, "sleep", lambda _seconds: None)
    return calls, RequestException


def test_token_counts_shape():
    assert agents._token_counts() == {
        "in_token_all": 0,
        "in_token_message": 0,
        "out_token_action": 0,
    }


def test_base_agent_history_and_save(tmp_path):
    agent = agents.BaseAgent(system_name="test", save_path=str(tmp_path))
    agent.set_base_prompt_and_reset([{"role": "system", "content": "base"}])
    agent.add_to_history("hello", "user")
    agent.update_latest_history(">hello")

    assert agent.full_history[-1]["content"] == ">hello"
    assert agent.full_history[-1]["old_content"] == "hello"
    # The conversation sent to the model must see the same prefix update.
    assert agent.current_prompt[-1]["content"] == ">hello"
    assert agent.pop_from_history()["content"] == ">hello"

    agent.add_to_history("world", "assistant")
    agent.save()
    saved = json.loads(open(agent.file_name).read())
    assert saved[-1]["content"] == "world"


def test_manual_agent(monkeypatch, tmp_path):
    monkeypatch.setattr("builtins.input", lambda prompt: "go north")
    agent = agents.ManualAgent(save_path=str(tmp_path))
    action, tokens = agent.act("observation", return_token_count=True)
    assert action == "go north"
    assert tokens == agents._token_counts()
    assert agent.full_history[-1]["role"] == "assistant"


def test_url_chat_payload_and_auth(monkeypatch):
    calls, _ = _install_fake_requests(
        monkeypatch,
        [FakeResponse(200, {"choices": [{"message": {"content": "hello"}}]})],
    )

    text = agents.url_chat(
        "https://example.test/v1/chat/completions",
        "model",
        [{"role": "user", "content": "hi"}],
        temperature=0.2,
        stop="\n",
        max_tokens=12,
        api_key="secret",
    )

    assert text == "hello"
    call = calls[0]
    assert call["headers"]["Authorization"] == "Bearer secret"
    assert call["json"]["model"] == "model"
    assert call["json"]["stop"] == ["\n"]
    assert call["json"]["max_tokens"] == 12


def test_url_completion_extracts_text(monkeypatch):
    _install_fake_requests(
        monkeypatch,
        [FakeResponse(200, {"choices": [{"text": "completed"}]})],
    )
    assert agents.url_completion("http://x", "m", "prompt") == "completed"


def test_post_json_retries_then_succeeds(monkeypatch):
    calls, _ = _install_fake_requests(
        monkeypatch,
        [
            FakeResponse(429, {"error": "slow down"}),
            FakeResponse(200, {"choices": [{"message": {"content": "ok"}}]}),
        ],
    )
    data = agents._post_json("http://x", {"a": 1})
    assert data["choices"][0]["message"]["content"] == "ok"
    assert len(calls) == 2


def test_post_json_http_error(monkeypatch):
    _install_fake_requests(
        monkeypatch, [FakeResponse(400, text="bad request")]
    )
    with pytest.raises(RuntimeError, match="HTTP 400"):
        agents._post_json("http://x", {})


def test_post_json_network_error(monkeypatch):
    responses = []
    _calls, request_exception = _install_fake_requests(monkeypatch, responses)
    responses.append(request_exception("boom"))
    with pytest.raises(RuntimeError, match="failed"):
        agents._post_json("http://x", {}, max_retries=0)


def test_url_agent_act_and_history(monkeypatch, tmp_path):
    monkeypatch.setattr(
        agents,
        "_post_json",
        lambda *args, **kwargs: {"choices": [{"message": {"content": "look"}}]},
    )
    agent = agents.URLChatAgent(
        save_path=str(tmp_path), model="m", url="http://x", api_key="k"
    )
    agent.set_base_prompt_and_reset([{"role": "system", "content": "base"}])

    action, tokens = agent.act("You see a room.", return_token_count=True)
    assert action == "look"
    assert set(tokens) == {"in_token_all", "in_token_message", "out_token_action"}
    assert agent.current_prompt[-1]["content"] == "look"


def test_url_agent_single_prompt_mode(monkeypatch, tmp_path):
    monkeypatch.setattr(agents, "_post_json", lambda *args, **kwargs: {})
    agent = agents.URLChatAgent(
        save_path=str(tmp_path), model="m", url="http://x", prompt_mode="single"
    )
    agent.set_base_prompt_and_reset([
        {"role": "system", "content": "base"},
        {"role": "user", "content": "hello"},
    ])
    assert agent._payload()["messages"] == [
        {"role": "user", "content": "basehello"}
    ]


def test_url_agent_history_messages_strip_logging_fields(tmp_path):
    agent = agents.URLChatAgent(
        save_path=str(tmp_path), model="m", url="http://x",
        prompt_mode="history",
    )
    agent.set_base_prompt_and_reset([{"role": "system", "content": "base"}])
    agent.add_to_history("hello", "user", {"in_token_all": 5})

    assert agent._messages() == [
        {"role": "system", "content": "base"},
        {"role": "user", "content": "hello"},
    ]


def test_url_agent_generate_is_stateless(monkeypatch, tmp_path):
    captured = {}

    def fake_post(url, payload, headers, timeout, max_retries):
        captured.update(payload)
        return {"choices": [{"text": "done"}]}

    monkeypatch.setattr(agents, "_post_json", fake_post)
    agent = agents.URLTextAgent(save_path=str(tmp_path), model="m", url="http://x")
    assert agent.generate("prompt", stop="\n", max_tokens=5) == "done"
    assert captured == {
        "model": "m",
        "temperature": 0.0,
        "prompt": "prompt",
        "stop": ["\n"],
        "max_tokens": 5,
    }
    assert agent.current_prompt == []


def test_url_agent_requires_url(tmp_path):
    with pytest.raises(ValueError, match="needs a URL"):
        agents.URLChatAgent(save_path=str(tmp_path), model="m")


def test_sampling_agent_resamples(monkeypatch, tmp_path):
    responses = iter(["first", "second"])
    monkeypatch.setattr(
        agents,
        "_post_json",
        lambda *args, **kwargs: {
            "choices": [{"message": {"content": next(responses)}}]
        },
    )
    agent = agents.OpenAIChatTextSamplingAgent(
        save_path=str(tmp_path), model="m", url="http://x",
        resample_temperature_jump=0.5,
    )
    agent.set_base_prompt_and_reset([{"role": "system", "content": "base"}])

    assert agent.act("obs") == "first"
    agent.prepare_resample()
    assert agent.temperature == pytest.approx(0.5)
    assert agent.is_resample()
    assert agent.act("") == "second"
    assert agent.previous_samples["previous_samples"]


def _install_fake_vllm(monkeypatch):
    fake_transformers = types.ModuleType("transformers")

    class FakeTokenizer:
        @classmethod
        def from_pretrained(cls, _model):
            return cls()

        def encode(self, text):
            return text.split()

        def apply_chat_template(self, messages, **_kwargs):
            return "CHAT:" + messages[0]["content"]

    fake_transformers.AutoTokenizer = FakeTokenizer

    fake_vllm = types.ModuleType("vllm")

    class FakeLLM:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

        def generate(self, _prompts, _params):
            return [SimpleNamespace(outputs=[SimpleNamespace(text="generated")])]

    class SamplingParams:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

    fake_vllm.LLM = FakeLLM
    fake_vllm.SamplingParams = SamplingParams
    monkeypatch.setitem(sys.modules, "transformers", fake_transformers)
    monkeypatch.setitem(sys.modules, "vllm", fake_vllm)


def test_vllm_agent_is_lazy_and_works(monkeypatch, tmp_path):
    _install_fake_vllm(monkeypatch)
    agent = agents.VLLMChatAgent(
        save_path=str(tmp_path), model="fake", max_model_len=100, seed=7
    )
    assert agent.chat_model is True
    assert agent.call_model() == "generated"
    assert agent.count_tokens("one two three") == 3
    assert agent.get_sampling_params().kwargs["seed"] == 7


def test_vllm_agent_missing_dependency(tmp_path, monkeypatch):
    monkeypatch.setitem(sys.modules, "vllm", None)
    with pytest.raises(ImportError, match="vLLM"):
        agents.VLLMChatAgent(save_path=str(tmp_path), model="fake")
