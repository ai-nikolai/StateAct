# v2 review and dependency audit

This note records the review of the `v2` refactor branch and the dependency
decisions behind it. It is meant to be updated as follow-up work lands.

## What v2 already does well

- `stateact/parsing.py`, `stateact/prompts.py`, `stateact/scoring.py` and
  `stateact/run_config.py` are importable without ALFWorld, vLLM or an API key.
- The named-experiment shell registries were replaced by `experiments/*.yaml`
  plus a single runner. The argv recorded in the YAML was extracted from the
  old scripts, so the interfaces of `run_alfworld_eval.sh` / `run_webshop.sh`
  are unchanged.
- The core package (`import stateact`) only uses the standard library. pandas
  and PyYAML are optional (`.[score]`, `.[yaml]`).

## Findings from the review

1. **`llamp` is an all-or-nothing import.** `llamp.llms.api` imports every
   provider module at import time, including `anthropic`, `cohere` and
   `cerebras.cloud.sdk`. If any one SDK is missing, `import llamp.llms.api`
   fails, so *all* API providers - including OpenAI - become unavailable.
   None of those SDKs are declared by `llamp` or by
   `alfworld_runs/requirements.txt`.
2. **`llamp` pins `vllm==0.6.6.post1`.** `webshop_runs/requirements.txt`
   requires `vllm>=0.7.1`, so the ALFWorld and WebShop environments cannot be
   installed together. The pins are documented as intentional, but they make
   a single reproducible environment impossible.
3. **TextCraft requirements were incomplete.** The scripts import `tqdm`,
   `tenacity`, `numpy`, `pyyaml`, `pandas` and `openai`, none of which were
   listed. Fixed in this branch.
4. **`json_action_cleaning` corrupted fenced JSON.** A fenced object such as
   ```` ```json ... ``` ```` was stripped and then had an extra `}` appended,
   so `valid_json` was reported false even for a valid object. The extractor
   recovered via the string fallback, but the metric was wrong. Fixed with a
   unit test.
5. **`--agent act` / `--agent stateact` were broken for non-Manual LLMs.**
   The ALFWorld loop only assigned `actual_action` for `ours-text`, even
   though `OUR_TEXT_PROMPTS` also covers `stateact` and `act`. Fixed.
6. **Prompt files were opened relative to the process cwd.** This worked only
   when the scripts were launched from inside `alfworld_runs/`. The path is
   now resolved relative to the module, so tests and tooling can import the
   prompt builders from the repository root.
7. **Mutable default arguments** in `stateact.prompts.get_prompt_example`
   (`keys_to_use=[]`, `key_renaming={}`) were replaced with `None` defaults.

## Dependency audit

| Dependency | Where | Needed for | Replace / action |
| --- | --- | --- | --- |
| `llamp` | `alfworld_runs/requirements.txt` | agent classes, history/save, token counts | **Replace** with an in-repo `stateact/agents.py` (see below). |
| `vllm` | all three benchmark requirements | local HuggingFace models | Keep, but move to an optional `local` extra and use one floor (`vllm>=0.7`) where possible. |
| `transformers` + `tiktoken` | pulled in by `llamp` | token counting / tokenizer | `tiktoken` stays optional (fallback to a character heuristic); `transformers` is only needed for the vLLM tokenizer. |
| `openai` / `anthropic` / `cohere` / `cerebras-cloud-sdk` | provider SDKs, currently undeclared | API agents | Explicit optional extras: `.[openai]`, `.[anthropic]`, `.[cohere]`, `.[cerebras]`. |
| `pandas` | `stateact.scoring`, notebooks | score aggregation | Already optional via `.[score]`. |
| `pyyaml` | `stateact.run_config` | experiment tables | Already optional via `.[yaml]`; make it a dependency of `.[dev]`. |
| `alfworld`, `fast-downward-textworld`, `textworld` | `alfworld_runs/requirements.txt` | benchmark environment | Keep; these are inherently heavy and benchmark-specific. |
| `textcraft` | `textcraft_runs/requirements.txt` | benchmark environment | Keep. |
| `requests`, `beautifulsoup4`, `requests_unixsocket2` | `webshop_runs/` | WebShop HTTP client | Keep; stdlib `urllib` is possible but not worth the rewrite. |

## Recommended LLamp replacement

`llamp` is ~2k lines, but StateAct only uses a small surface:

```
BaseSystem / BaseLLMSystem
  history, reset, save, update_save_path, update_latest_history,
  set_base_prompt_and_reset, count_tokens
agent classes
  act(), prepare_resample(), is_resample(), stop_sequences
```

A replacement can be ~300 lines in `stateact/agents.py`:

1. `Agent` base class with history/save/token-counting (port `BaseSystem`).
2. `ChatAgent` for OpenAI-compatible chat completions. Use it for OpenAI,
   NVIDIA and Cerebras via `base_url`, so no extra SDKs are needed beyond
   `openai` (or even stdlib `urllib`).
3. `TextAgent` for the legacy completions API (`gpt-3.5-turbo-instruct`).
4. `AnthropicAgent` (messages API) behind an `anthropic` extra.
5. `CohereAgent` behind a `cohere` extra.
6. `VLLMAgent` behind a `local` extra; import `vllm`/`transformers` lazily.
7. `ManualAgent` (input prompt).
8. `SamplingAgent` mixin implementing the resample history used by
   `OpenAIChatTextSampling`.

Import each provider lazily inside `get_agent_and_model` so a missing SDK only
disables that provider. Keep `PROVIDERS` and `AGENT_MODEL_MAPPING` as the
public compatibility surface.

Migration can be staged:

1. Add `stateact/agents.py` and a `--agent_backend {auto,llamp,native}` switch
   (default `auto`: native if available, otherwise llamp).
2. Add tests with fake SDK modules (no network/GPU) for every code path.
3. Once the ALFWorld paper results reproduce with `--agent_backend native`,
   drop `llamp` from `alfworld_runs/requirements.txt`.

Until then, document that `llamp.llms.api` needs `openai`, `anthropic`,
`cohere` and `cerebras-cloud-sdk` installed even if only one provider is used.

## CI

`.github/workflows/ci.yml` runs:

- `ruff check stateact tests`
- `compileall` over the shared package and benchmark entry points
- `pytest` on Python 3.9-3.12
- a wheel/sdist build and import check

The tests cover parsing, prompt dispatch, the experiment tables, scoring and
the provider registry. None of them need ALFWorld, vLLM, an API key or a GPU.
