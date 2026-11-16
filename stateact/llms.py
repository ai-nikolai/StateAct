"""Minimal OpenAI-compatible model client.

There is one provider path: an HTTP endpoint returning the OpenAI
chat/completions or completions shape. Point it at a local vLLM server or a
remote API; the client only needs ``requests``.

    llm = LLM("Qwen/Qwen2.5-14B-Instruct",
              url="http://localhost:8000/v1",
              api_key_env="OPENAI_API_KEY")
    text = llm("You are in a room. What do you do?")
"""

import os

from stateact.backends import url_chat, url_completion

__all__ = ["LLM", "url_chat", "url_completion"]


class LLM:
    """Call an OpenAI-compatible endpoint.

    ``url`` may be a base URL (``http://host:8000/v1``) or a full endpoint
    (``.../v1/chat/completions``). ``mode`` selects chat or legacy completion
    when the URL is a base.
    """

    def __init__(self, model, url=None, api_key=None, api_key_env=None,
                 mode="chat", temperature=0.0, max_tokens=1000, stop=None,
                 timeout=60, max_retries=4):
        self.model = model
        self.url = url or os.environ.get("STATEACT_LLM_URL")
        if not self.url:
            raise ValueError(
                "LLM needs a url=... or STATEACT_LLM_URL "
                "(either a local vLLM server or a remote OpenAI-compatible API)."
            )
        self.api_key = api_key
        self.api_key_env = api_key_env
        self.mode = mode
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.stop = stop
        self.timeout = timeout
        self.max_retries = max_retries

    @classmethod
    def from_env(cls, model, **kwargs):
        """Build from ``STATEACT_LLM_*`` environment variables."""
        kwargs.setdefault("url", os.environ.get("STATEACT_LLM_URL"))
        kwargs.setdefault("api_key", os.environ.get("STATEACT_LLM_API_KEY"))
        kwargs.setdefault("api_key_env", os.environ.get("STATEACT_LLM_API_KEY_ENV"))
        kwargs.setdefault("mode", os.environ.get("STATEACT_LLM_MODE", "chat"))
        return cls(model=model, **kwargs)

    def _endpoint(self, mode):
        url = self.url.rstrip("/")
        if url.endswith("/chat/completions") or url.endswith("/completions"):
            return url
        suffix = "/chat/completions" if mode == "chat" else "/completions"
        return url + suffix

    def _kwargs(self, stop, max_tokens, temperature, **overrides):
        return {
            "temperature": self.temperature if temperature is None else temperature,
            "stop": self.stop if stop is None else stop,
            "max_tokens": self.max_tokens if max_tokens is None else max_tokens,
            "api_key": self.api_key,
            "api_key_env": self.api_key_env,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
            **overrides,
        }

    def chat(self, messages, stop=None, max_tokens=None, temperature=None, **kwargs):
        return url_chat(
            self._endpoint("chat"),
            self.model,
            messages,
            **self._kwargs(stop, max_tokens, temperature, **kwargs),
        )

    def complete(self, prompt, stop=None, max_tokens=None, temperature=None, **kwargs):
        return url_completion(
            self._endpoint("completion"),
            self.model,
            prompt,
            **self._kwargs(stop, max_tokens, temperature, **kwargs),
        )

    def __call__(self, prompt, stop=None, mode=None):
        mode = mode or self.mode
        if mode == "chat":
            return self.chat([{"role": "user", "content": prompt}], stop=stop)
        return self.complete(prompt, stop=stop)
