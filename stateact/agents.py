"""LLM agents without provider SDKs.

StateAct needs three things from a model: a conversation history, an
``act()`` method that records the exchange, and token counts for the CSV log.
The previous implementation delegated those to the external ``llamp`` package,
which imported every provider SDK at once and pinned ``vllm==0.6.6.post1``.

This module keeps the small surface StateAct actually uses and implements only
two backends:

* :class:`VLLMChatAgent` - local models through vLLM (lazy import, optional).
* :class:`URLAgent` - any OpenAI-compatible chat/completions endpoint through
  one ``requests.post`` helper. The legacy ``--llm_type`` names (OpenAI,
  Anthropic, Cohere, NVIDIA, Cerebras) are thin subclasses that only set the
  default URL, key environment variable, and prompt layout.
* :class:`ManualAgent` - human input for debugging.

No ``openai``, ``anthropic``, ``cohere`` or ``cerebras`` SDK is imported.
"""

import copy
import json
import os
import time
from datetime import datetime

__all__ = [
    "BaseAgent",
    "BaseLLMAgent",
    "ManualAgent",
    "URLAgent",
    "URLChatAgent",
    "URLTextAgent",
    "OpenAIChatAgent",
    "OpenAIChatTextAgent",
    "OpenAIChatTextSamplingAgent",
    "OpenAITextAgent",
    "AnthropicChatAgent",
    "AnthropicTextAgent",
    "CohereChatAgent",
    "CohereTextAgent",
    "CohereChatTextAgent",
    "NvidiaChatTextAgent",
    "CerebrasChatTextAgent",
    "VLLMChatAgent",
    "url_chat",
    "url_completion",
]

RETRY_STATUS_CODES = {408, 409, 429, 500, 502, 503, 504}
DEFAULT_TIMEOUT = 60
DEFAULT_MAX_RETRIES = 4


def _as_list(value):
    if value is None:
        return None
    if isinstance(value, (list, tuple)):
        return list(value)
    return [value]


def _token_counts(in_tokens=0, message_tokens=0, out_tokens=0):
    return {
        "in_token_all": in_tokens,
        "in_token_message": message_tokens,
        "out_token_action": out_tokens,
    }


def _post_json(url, payload, headers=None, timeout=DEFAULT_TIMEOUT,
               max_retries=DEFAULT_MAX_RETRIES):
    """POST ``payload`` as JSON and return the decoded response.

    A missing/broken ``requests`` install is reported as a normal
    ``ImportError``; HTTP errors include the status and a body snippet.
    """
    try:
        import requests
    except ImportError as exc:  # pragma: no cover - depends on the environment
        raise ImportError(
            "URL-based models need the 'requests' package "
            "(pip install requests)."
        ) from exc

    last_error = None
    for attempt in range(max_retries + 1):
        try:
            response = requests.post(
                url, json=payload, headers=headers or {}, timeout=timeout
            )
        except requests.RequestException as exc:
            last_error = exc
            if attempt == max_retries:
                raise RuntimeError(f"Request to {url} failed: {exc}") from exc
            time.sleep(min(2 ** attempt, 30))
            continue

        if response.status_code in RETRY_STATUS_CODES and attempt < max_retries:
            last_error = response
            time.sleep(min(2 ** attempt, 30))
            continue

        if response.status_code >= 400:
            raise RuntimeError(
                f"{url} returned HTTP {response.status_code}: "
                f"{response.text[:500]}"
            )

        try:
            return response.json()
        except ValueError as exc:
            raise RuntimeError(
                f"{url} returned non-JSON content: {response.text[:500]}"
            ) from exc

    raise RuntimeError(f"Request to {url} failed: {last_error}")


def _extract_text(data, mode):
    """Pull the generated text out of a chat/completions response."""
    choices = data.get("choices") or []
    if choices:
        first = choices[0]
        if mode == "completion":
            text = first.get("text")
        else:
            message = first.get("message") or {}
            text = message.get("content")
            if isinstance(text, list):
                text = "".join(
                    part.get("text", "") if isinstance(part, dict) else str(part)
                    for part in text
                )
        if text is not None:
            return text

    for key in ("text", "completion", "response", "output_text"):
        if key in data:
            return data[key]

    raise RuntimeError(f"Could not find generated text in response: {data}")


def url_chat(url, model, messages, *, temperature=0.0, stop=None,
             max_tokens=1000, api_key=None, api_key_env=None, headers=None,
             timeout=DEFAULT_TIMEOUT, max_retries=DEFAULT_MAX_RETRIES, **extra):
    """Call an OpenAI-compatible ``/chat/completions`` endpoint."""
    request_headers = {"Content-Type": "application/json"}
    request_headers.update(headers or {})
    key = api_key or (os.environ.get(api_key_env) if api_key_env else None)
    if key:
        request_headers["Authorization"] = f"Bearer {key}"

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }
    if stop is not None:
        payload["stop"] = _as_list(stop)
    if max_tokens is not None:
        payload["max_tokens"] = max_tokens
    payload.update(extra)

    return _extract_text(
        _post_json(url, payload, request_headers, timeout, max_retries), "chat"
    )


def url_completion(url, model, prompt, *, temperature=0.0, stop=None,
                   max_tokens=250, api_key=None, api_key_env=None,
                   headers=None, timeout=DEFAULT_TIMEOUT,
                   max_retries=DEFAULT_MAX_RETRIES, **extra):
    """Call an OpenAI-compatible legacy ``/completions`` endpoint."""
    request_headers = {"Content-Type": "application/json"}
    request_headers.update(headers or {})
    key = api_key or (os.environ.get(api_key_env) if api_key_env else None)
    if key:
        request_headers["Authorization"] = f"Bearer {key}"

    payload = {
        "model": model,
        "prompt": prompt,
        "temperature": temperature,
    }
    if stop is not None:
        payload["stop"] = _as_list(stop)
    if max_tokens is not None:
        payload["max_tokens"] = max_tokens
    payload.update(extra)

    return _extract_text(
        _post_json(url, payload, request_headers, timeout, max_retries),
        "completion",
    )


class BaseAgent:
    """Conversation history, persistence and the ``act`` contract."""

    LOG_FILE_ENDING = ".json"

    def __init__(self, system_name="base", save_path="game_logs", **kwargs):
        self.base_prompt = []
        self.current_prompt = []
        self.full_history = []
        self.system_name = system_name
        self.save_path_base = save_path
        self.file_name = self.get_save_path()

    def call_model(self, *args, **kwargs):  # pragma: no cover - abstract
        raise NotImplementedError

    def act(self, current_observation, return_token_count=False, *args, **kwargs):
        self.add_to_history(current_observation, "user")
        action = self.call_model()
        self.add_to_history(action, "assistant")
        if return_token_count:
            return action, _token_counts()
        return action

    def reset(self, *args, **kwargs):
        self.current_prompt = copy.deepcopy(self.base_prompt)
        self.full_history = copy.deepcopy(self.current_prompt)
        self.file_name = self.get_save_path()

    def add_first_observation(self, first_obs, *args, **kwargs):
        self.add_to_history(first_obs, "user")

    def add_to_history(self, content, role, additional_data=None, *args, **kwargs):
        entry = {"role": role, "content": content}
        self.current_prompt.append(entry)

        logged = dict(entry)
        logged.update(additional_data or {})
        self.full_history.append(self._extend_memory(logged))

    def _extend_memory(self, memory):
        return memory

    def pop_from_history(self, return_full=True, *args, **kwargs):
        try:
            if return_full:
                self.current_prompt.pop()
                return self.full_history.pop()
            self.full_history.pop()
            return self.current_prompt.pop()
        except IndexError:
            return None

    def update_latest_history(self, content, key="content", old_key="old_content",
                              *args, **kwargs):
        previous = self.full_history[-1][key]
        self.full_history[-1][key] = content
        self.full_history[-1][old_key] = previous

    def _extract_prompt_from_history(self, history,
                                     keys_to_keep=("role", "content")):
        return [{key: segment.get(key) for key in keys_to_keep}
                for segment in history]

    def load_from_saved_data(self, previous_history, *args, **kwargs):
        self.reset()
        if isinstance(previous_history, list):
            self.full_history = previous_history
        elif isinstance(previous_history, str):
            with open(previous_history) as handle:
                self.full_history = json.load(handle)
        else:
            self.full_history = json.load(previous_history)
        self.current_prompt = self._extract_prompt_from_history(self.full_history)

    def set_base_prompt_and_reset(self, base_prompt, *args, **kwargs):
        self.base_prompt = base_prompt
        self.reset()

    def save(self, *args, **kwargs):
        with open(self.file_name, "w") as handle:
            json.dump(self.full_history, handle, indent=4)

    def get_file_name(self, base_name="logs", *args, **kwargs):
        now = datetime.now()
        return (f"{self.system_name}_{base_name}_"
                f"{now.strftime('%d_%m_%Y_%H_%M_%S')}{self.LOG_FILE_ENDING}")

    def get_save_path(self, save_path="", *args, **kwargs):
        if save_path:
            self.save_path_base = save_path
        os.makedirs(self.save_path_base, exist_ok=True)
        return os.path.join(self.save_path_base, self.get_file_name())

    def update_save_path(self, save_path, *args, **kwargs):
        self.save_path_base = save_path
        self.file_name = self.get_save_path(save_path)

    def count_tokens(self, *args, **kwargs):
        return 0

    def is_resample(self, *args, **kwargs):
        return False


class BaseLLMAgent(BaseAgent):
    """Adds token accounting and the prompt-based ``act`` loop."""

    def __init__(self, system_name="base_llm", save_path="game_logs",
                 temperature=0.0, **kwargs):
        super().__init__(system_name=system_name, save_path=save_path)
        self.temperature = temperature

    def _extend_memory(self, memory):
        memory.update({"temperature": self.temperature})
        return memory

    def _count_in_token(self, current_observation):
        tokens_until_now = self.count_tokens()
        message_tokens = self.count_tokens(current_observation)
        return {
            "in_token_all": tokens_until_now + message_tokens,
            "in_token_message": message_tokens,
        }

    def _count_out_token(self, action):
        return {"out_token_action": self.count_tokens(action)}

    def act(self, current_observation, temperature=None, return_token_count=False):
        additional_in = self._count_in_token(current_observation)
        self.add_to_history(current_observation, "user", additional_in)

        if self.count_tokens() != additional_in["in_token_all"]:
            print("WARNING: In Tokens need to be same length.")

        action = self.call_model(temperature)
        additional_out = self._count_out_token(action)
        action = self.post_process_model_output(action)
        self.add_to_history(action, "assistant", additional_out)

        if return_token_count:
            return action, {**additional_in, **additional_out}
        return action

    def call_model(self, temperature=None):  # pragma: no cover - abstract
        raise NotImplementedError

    def post_process_model_output(self, model_output):
        return model_output

    def generate_text_prompt(self):
        return "".join(section["content"] for section in self.current_prompt)

    def count_tokens(self, optional_text=None, model_name="gpt-3.5"):
        text = self.generate_text_prompt() if optional_text is None else optional_text
        encoder = _tiktoken_encoder(model_name)
        if encoder is not None:
            return len(encoder.encode(text))
        # Deterministic fallback when tiktoken is not installed.  It is only
        # used for logging, never for truncation.
        return max(1, len(text) // 4)


_TIKTOKEN_CACHE = {}


def _tiktoken_encoder(model_name):
    if model_name in _TIKTOKEN_CACHE:
        return _TIKTOKEN_CACHE[model_name]

    try:
        import tiktoken
    except ImportError:
        _TIKTOKEN_CACHE[model_name] = None
        return None

    short = "-".join(str(model_name).split("-")[:2])
    try:
        encoder = tiktoken.encoding_for_model(short)
    except Exception:
        try:
            encoder = tiktoken.get_encoding("cl100k_base")
        except Exception:
            encoder = None
    _TIKTOKEN_CACHE[model_name] = encoder
    return encoder


class URLAgent(BaseLLMAgent):
    """OpenAI-compatible chat/completions agent using one HTTP call."""

    default_url = None
    default_api_key_env = None
    default_mode = "chat"
    default_prompt_mode = "history"
    default_headers = None

    def __init__(self, system_name="URLChat", save_path="game_logs",
                 temperature=0.0, model="gpt-3.5-turbo-0125", url=None,
                 api_key=None, api_key_env=None, headers=None, timeout=DEFAULT_TIMEOUT,
                 max_retries=DEFAULT_MAX_RETRIES, max_tokens=1000,
                 mode=None, prompt_mode=None, **kwargs):
        super().__init__(system_name=system_name, save_path=save_path,
                         temperature=temperature)
        self.model = model
        self.url = url or self.default_url
        if not self.url:
            raise ValueError(
                f"{type(self).__name__} needs a URL (pass url=... or "
                "set --llm_url / STATEACT_LLM_URL)."
            )

        key_env = api_key_env or self.default_api_key_env
        self.api_key = api_key or (os.environ.get(key_env) if key_env else None)
        self.headers = {"Content-Type": "application/json"}
        self.headers.update(self.default_headers or {})
        self.headers.update(headers or {})
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"

        self.timeout = timeout
        self.max_retries = max_retries
        self.max_tokens = max_tokens
        self.mode = mode or self.default_mode
        self.prompt_mode = prompt_mode or self.default_prompt_mode
        self.stop_sequences = None

    def _messages(self):
        if self.prompt_mode == "single":
            return [{"role": "user", "content": self.generate_text_prompt()}]
        return self.current_prompt

    def _payload(self, prompt_text=None, stop=None, max_tokens=None, mode=None):
        mode = mode or self.mode
        payload = {
            "model": self.model,
            "temperature": self.temperature,
        }
        if mode == "completion":
            payload["prompt"] = (
                prompt_text if prompt_text is not None
                else self.generate_text_prompt()
            )
        else:
            payload["messages"] = (
                [{"role": "user", "content": prompt_text}]
                if prompt_text is not None else self._messages()
            )

        stop = self.stop_sequences if stop is None else stop
        if stop is not None:
            payload["stop"] = _as_list(stop)
        if (self.max_tokens if max_tokens is None else max_tokens) is not None:
            payload["max_tokens"] = (
                self.max_tokens if max_tokens is None else max_tokens
            )
        return payload

    def call_model(self, temperature=None):
        if temperature is not None:
            self.temperature = temperature
        data = _post_json(
            self.url, self._payload(), self.headers, self.timeout, self.max_retries
        )
        return _extract_text(data, self.mode)

    def generate(self, prompt, stop=None, max_tokens=None, mode=None):
        """Stateless single call, used by the legacy benchmark scripts."""
        payload = self._payload(
            prompt_text=prompt, stop=stop, max_tokens=max_tokens, mode=mode
        )
        data = _post_json(
            self.url, payload, self.headers, self.timeout, self.max_retries
        )
        return _extract_text(data, mode or self.mode)


class URLChatAgent(URLAgent):
    """Generic chat agent; pass any OpenAI-compatible endpoint with url=..."""


class URLTextAgent(URLAgent):
    """Generic legacy completions agent."""

    default_mode = "completion"
    default_prompt_mode = "single"

    def __init__(self, *args, **kwargs):
        # The old OpenAIText agent capped completions at 250 tokens.
        kwargs.setdefault("max_tokens", 250)
        super().__init__(*args, **kwargs)


# ---------------------------------------------------------------------------
# Legacy provider names.  They are all thin URLAgent subclasses; keeping the
# names means the existing experiment tables keep working.
# ---------------------------------------------------------------------------

class OpenAIChatAgent(URLAgent):
    default_url = "https://api.openai.com/v1/chat/completions"
    default_api_key_env = "OPENAI_API_KEY"


class OpenAIChatTextAgent(OpenAIChatAgent):
    default_prompt_mode = "single"


class OpenAIChatTextSamplingAgent(OpenAIChatTextAgent):
    """Chat agent that supports the repetition-resampling loop."""

    def __init__(self, *args, resample_temperature_jump=0.1, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_temperature = self.temperature
        self.resample_temperature_jump = resample_temperature_jump
        self.previous_samples = {}
        self.resampling = False
        self.previous_samples_key = "previous_samples"
        self.history_keys = ["role", "content", "temperature", "out_token_action"]

    def act(self, current_observation="", temperature=None, return_token_count=False):
        if not self.resampling:
            if not current_observation:
                raise ValueError("An observation is required when not resampling.")
            self.temperature = self.original_temperature
            self.previous_samples = {}
            additional_in = self._count_in_token(current_observation)
            self.add_to_history(current_observation, "user", additional_in)
        else:
            # The last history entry was popped by prepare_resample(); reuse
            # the token counts of the most recent user observation.
            previous = next(
                (entry for entry in reversed(self.full_history)
                 if "in_token_all" in entry),
                {},
            )
            additional_in = {
                "in_token_all": previous.get("in_token_all", 0),
                "in_token_message": previous.get("in_token_message", 0),
            }

        action = self.call_model(temperature)
        additional_out = self._count_out_token(action)
        action = self.post_process_model_output(action)
        self.add_to_history(action, "assistant", additional_out)
        self.resampling = False

        if self.previous_samples:
            additional_out.update(self.previous_samples)
        if return_token_count:
            return action, additional_out
        return action

    def prepare_resample(self, increase_temperature=True):
        previous = self.pop_from_history(return_full=True)
        if not previous:
            self.previous_samples = {}
            return

        turn = {key: previous.get(key) for key in self.history_keys}
        samples = previous.get(self.previous_samples_key) or []
        samples.append(turn)
        self.previous_samples = {self.previous_samples_key: samples}
        self.resampling = True
        if increase_temperature:
            self.temperature += self.resample_temperature_jump

    def is_resample(self):
        return True


class OpenAITextAgent(URLTextAgent):
    default_url = "https://api.openai.com/v1/completions"
    default_api_key_env = "OPENAI_API_KEY"


class AnthropicChatAgent(URLAgent):
    default_url = "https://api.anthropic.com/v1/chat/completions"
    default_api_key_env = "ANTHROPIC_API_KEY"
    default_headers = {"anthropic-version": "2023-06-01"}


class AnthropicTextAgent(AnthropicChatAgent):
    default_prompt_mode = "single"


class CohereChatAgent(URLAgent):
    default_url = "https://api.cohere.ai/compatibility/v1/chat/completions"
    default_api_key_env = "COHERE_API_KEY"


class CohereTextAgent(CohereChatAgent):
    default_prompt_mode = "single"


class CohereChatTextAgent(CohereChatAgent):
    default_prompt_mode = "single"


class NvidiaChatTextAgent(URLAgent):
    default_url = "https://integrate.api.nvidia.com/v1/chat/completions"
    default_api_key_env = "NVIDIA_API_KEY"
    default_prompt_mode = "single"


class CerebrasChatTextAgent(URLAgent):
    default_url = "https://api.cerebras.ai/v1/chat/completions"
    default_api_key_env = "CEREBRAS_API_KEY"
    default_prompt_mode = "single"


class VLLMChatAgent(BaseLLMAgent):
    """Local HuggingFace model served through vLLM."""

    def __init__(self, system_name="VLLMChat", save_path="game_logs",
                 temperature=0.0, model="Qwen/Qwen2.5-0.5B-Instruct",
                 tensor_parallel_size=1, max_model_len=16000,
                 quantization=False, stop_sequences=None, seed=-1, **kwargs):
        super().__init__(system_name=system_name, save_path=save_path,
                         temperature=temperature)
        try:
            from transformers import AutoTokenizer
            from vllm import LLM
        except ImportError as exc:  # pragma: no cover - depends on the environment
            raise ImportError(
                "Local models need vLLM and transformers "
                "(pip install vllm transformers)."
            ) from exc

        self.model = model
        self.max_model_len = max_model_len
        self.tensor_parallel_size = tensor_parallel_size
        self.stop_sequences = stop_sequences
        self.seed = None if seed == -1 else seed
        self.tokenizer = AutoTokenizer.from_pretrained(model)

        try:
            self.apply_chat_template("test")
            self.chat_model = True
        except Exception:
            self.chat_model = False

        llm_kwargs = dict(
            model=model,
            tensor_parallel_size=tensor_parallel_size,
            gpu_memory_utilization=0.95,
            max_model_len=max_model_len,
            dtype="auto",
        )
        if quantization:
            llm_kwargs.update(
                gpu_memory_utilization=0.90,
                quantization="bitsandbytes",
                load_format="bitsandbytes",
                enable_chunked_prefill=True,
                max_num_seqs=4,
            )
        self.llm = LLM(**llm_kwargs)

        print("=" * 20)
        print(
            f"Model loaded as: {model} with tensors: {tensor_parallel_size} "
            f"and seed: {seed}. Is quantization: {quantization}; "
            f"is chat_model: {self.chat_model}"
        )

    def apply_chat_template(self, prompt):
        messages = [{"role": "user", "content": prompt[-self.max_model_len:]}]
        return self.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )

    def get_sampling_params(self):
        from vllm import SamplingParams

        return SamplingParams(
            temperature=self.temperature,
            top_p=1.0,
            repetition_penalty=1.00,
            max_tokens=min(2000, self.max_model_len),
            stop=self.stop_sequences,
            seed=self.seed,
        )

    def call_model(self, temperature=None):
        prompt = self.generate_text_prompt()
        if self.chat_model:
            prompt = self.apply_chat_template(prompt)
        outputs = self.llm.generate([prompt], self.get_sampling_params())
        return outputs[0].outputs[0].text

    def count_tokens(self, optional_text=None, model_name=None):
        text = self.generate_text_prompt() if optional_text is None else optional_text
        return len(self.tokenizer.encode(text))


class ManualAgent(BaseAgent):
    """Human-in-the-loop agent used for debugging."""

    def __init__(self, system_name="Manual", save_path="game_logs", **kwargs):
        super().__init__(system_name=system_name, save_path=save_path)

    def call_model(self):
        return input("[[INPUT YOUR ACTION]] >>")
