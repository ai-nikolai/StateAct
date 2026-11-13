# v2 review and dependency audit

This note records the review of the `v2` refactor branch and the dependency
decisions behind it. It is meant to be updated as follow-up work lands.

## Follow-up work landed in this branch

- `llamp` and every provider SDK were removed from the shared code.
  `stateact/agents.py` now has exactly three backends: local vLLM, one
  `requests`-based URL backend for OpenAI-compatible endpoints, and Manual.
- The legacy `--llm_type` names remain as aliases, so existing experiment
  tables and command lines keep working.
- `stateact/analysis/` was added with notebook-compatible ALFWorld helpers and
  small WebShop/TextCraft loaders.
- `scripts/pbs/` holds A100 jobs for ALFWorld and WebShop, with
  `scripts/submit_pbs.sh` as the submission helper.
- The ALFWorld dependency is isolated in `stateact/envs/alfworld.py`
  (reset/step/skip). `base_config.yaml` only contains the keys `AlfredTWEnv`
  reads, and the benchmark is pinned to `alfworld==0.4.2`,
  `textworld==1.7.0`, `fast-downward-textworld==20.6.4` (verified).
- CI now covers agents (mocked HTTP, fake vLLM), analysis and the experiment
  tables: 166 tests, no network/GPU/API key.

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

1. **`llamp` was an all-or-nothing import.** `llamp.llms.api` imported every
   provider module at import time, including `anthropic`, `cohere` and
   `cerebras.cloud.sdk`. If any one SDK was missing, importing the package
   failed, so *all* API providers - including OpenAI - became unavailable.
   None of those SDKs were declared by `llamp` or by
   `alfworld_runs/requirements.txt`. Removed in this branch.
2. **`llamp` pinned `vllm==0.6.6.post1`.** `webshop_runs/requirements.txt`
   requires `vllm>=0.7.1`, so the ALFWorld and WebShop environments could not
   be installed together. Removing `llamp` removes the forced pin.
3. **TextCraft requirements were incomplete.** The scripts import `tqdm`,
   `tenacity`, `numpy`, `pyyaml`, `pandas` and `openai`; the first five are now
   listed and the OpenAI SDK is no longer needed (URL backend).
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
8. **Two recorded experiments were already broken upstream.** ALFWorld
   `eval_mix` contained `--trial_namen`, and WebShop `webshop_local` passed
   `--socket` with no value (argparse rejects both). The experiment tables now
   record `--trial_name` and `./tmp/webshop.sock`; tests guard against either
   regression. The old shell scripts were left alone because v2 is a refactor
   branch, but the same fixes apply there.

## Dependency audit

| Dependency | Where | Needed for | Status |
| --- | --- | --- | --- |
| `llamp` | was in `alfworld_runs/requirements.txt` | agent classes, history/save, token counts | **Removed**; replaced by `stateact/agents.py`. |
| `vllm` | benchmark requirements | local HuggingFace models | Kept; optional `.[local]` extra, lazy import. |
| `transformers` | vLLM tokenizer | local models | Kept; optional `.[local]` extra. |
| `tiktoken` | token logging for API models | exact token counts | Optional; falls back to `len(text) // 4`. |
| `openai` / `anthropic` / `cohere` / `cerebras-cloud-sdk` | were used by `llamp` | API agents | **Removed.** All API calls go through `requests`. |
| `pandas` | `stateact.analysis`, scoring | result analysis | Optional via `.[score]` / `.[dev]`. |
| `pyyaml` | `stateact.run_config` | experiment tables | Optional via `.[yaml]`. |
| `alfworld`, `fast-downward-textworld`, `textworld` | `alfworld_runs/requirements.txt` | benchmark environment | Kept; inherently benchmark-specific. |
| `textcraft` | `textcraft_runs/requirements.txt` | benchmark environment | Kept. |
| `requests`, `beautifulsoup4`, `requests_unixsocket2` | `stateact.agents`, `webshop_runs/` | URL models + WebShop client | Kept. |

## LLamp replacement (implemented)

`stateact/agents.py` keeps only the surface StateAct uses:

```
BaseAgent / BaseLLMAgent
  history, reset, save, update_save_path, update_latest_history,
  set_base_prompt_and_reset, count_tokens, act()
URLAgent
  one requests.post helper, chat or legacy completions layout
VLLMChatAgent
  lazy vllm + transformers, sampling params, tokenizer-based counts
ManualAgent
  input() for debugging
```

The legacy provider names are thin `URLAgent` subclasses that only set a
default endpoint and key environment variable. OpenAI, Anthropic, Cohere,
NVIDIA and Cerebras all expose OpenAI-compatible endpoints; the exact same
`url_chat` / `url_completion` functions are also used by the WebShop and
TextCraft scripts, so no SDK is needed anywhere.

A custom endpoint can be used without touching the registry:

```bash
python3 alfworld_run.py --agent stateact --llm_type URLChat \
    --model my-model \
    --llm_url http://localhost:8000/v1/chat/completions \
    --llm_api_key_env MY_API_KEY_ENV \
    ...
```

Token counts match the previous code when `tiktoken` is installed; without it
the character-based fallback is used for logging only. The resampling path
(`OpenAIChatTextSampling`) and prompt assembly are unchanged.

## CI

`.github/workflows/ci.yml` runs:

- `ruff check stateact tests`
- `compileall` over the shared package and benchmark entry points
- `pytest` on Python 3.9-3.12
- a wheel/sdist build and import check

The 166 tests cover parsing, prompt dispatch, the experiment tables, scoring,
the URL/HTTP agent (mocked), the vLLM agent (fake modules), the analysis
helpers and the model registry. None of them need ALFWorld, vLLM, an API key
or a GPU.

## Cluster jobs

`scripts/pbs/` contains A100 jobs for ALFWorld (Qwen2.5-7B-Instruct) and
WebShop (Qwen2.5-3B-Instruct). `scripts/submit_pbs.sh` forwards `-v`
overrides to qsub and writes logs under `logs/pbs/`. The WebShop job starts
the existing `webshop.simg` with `--writable-tmpfs`, waits for its unix
socket, and cleans everything up on exit.
