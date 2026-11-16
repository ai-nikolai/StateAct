# StateAct

Official implementation of **StateAct: Enhancing LLM Base Agents via
Self-prompting and State-tracking**
[arXiv:2410.02810](https://arxiv.org/abs/2410.02810)

StateAct is a state-tracking base agent for LLM agents. This repository runs it
on three benchmarks:

- **ALFWorld** — household text environments
- **WebShop** — simulated online shopping
- **TextCraft** — text-based crafting
- **ScienceWorld** — interactive science experiments (optional wrapper)

The current `v2` layout keeps the benchmark environments separate but shares
the agent, result format, analysis and cluster tooling.

---

## Install

Agent library (includes `requests`):

```bash
pip install stateact
# optional ScienceWorld wrapper:
pip install "stateact[scienceworld]"

# from a checkout, with development tools:
pip install -e ".[dev]"
```

Benchmark environments are installed separately because their dependencies
differ:

```bash
pip install -r alfworld_runs/requirements.txt    # env_alfworld
pip install -r webshop_runs/requirements.txt     # env_webshop
pip install -r textcraft_runs/requirements.txt   # env_textcraft
```

The agent library only needs `requests`. Benchmark scripts that use an
in-process local model additionally need `vllm` + `transformers`; those stay
in the per-benchmark requirements files.

---

## Standalone agent library

`stateact` is also a small agent library that is independent of the benchmark
runners.

```python
from stateact import (
    LLM, ReActAgent, AgentBenchAgent, StateActAgent,
    ReflexionAgent, AdaptAgent,
    BaseEnv, AlfworldEnv, TextcraftEnv, ScienceWorldEnv, WebshopEnv,
    main_loop,
)

llm = LLM(
    "Qwen/Qwen2.5-14B-Instruct",
    url="http://localhost:8000/v1",   # local vLLM server or remote API
    api_key_env="OPENAI_API_KEY",     # omit for a local server
)

agent = StateActAgent(
    llm=llm,
    example_trajectories="",          # string or list of dicts
    format="string",                  # "string" or "json"
    prompt_order=["goal", "thought", "action"],
)

env = AlfworldEnv("ood_test")         # BaseEnv wrapper
results = main_loop(agent, env, num_runs=1, preserve_context=False)
```

### Agents

| Agent | Response format |
| --- | --- |
| `ReActAgent` | `think: ...` / `action: ...` (auto `OK.` turn) |
| `AgentBenchAgent` | `THOUGHT: ...` / `ACTION: ...` |
| `StateActAgent(format="string")` | key/value lines, e.g. `goal: ...` |
| `StateActAgent(format="json")` | one JSON object with the same keys |
| `ReflexionAgent(base_agent)` | base agent + reflections after failures |
| `AdaptAgent(base_agent)` | base agent + plan/decompose retry (ADaPT-style) |

Every agent implements:

```python
action, state = agent.run_step(observation)
agent.reset()
```

### Environments

`BaseEnv` defines:

```python
observation = env.reset()
observation = env.step(action)
env.done     # bool
env.reward   # float
env.info     # dict
```

Wrappers: `AlfworldEnv`, `TextcraftEnv`, `ScienceWorldEnv`, and `WebshopEnv`
(adapts a WebShop server client).

### Main loop

```python
from stateact import ScienceWorldEnv, main_loop

# ScienceWorld (optional; needs
#   pip install "stateact[scienceworld]")
sci = ScienceWorldEnv("boil", variation=0, simplification="easy")
main_loop(agent, sci, num_runs=1)

# fresh agent each episode
main_loop(agent, env, num_runs=5, preserve_context=False)

# keep agent memory/reflections (Reflexion style)
main_loop(agent, env, num_runs=5, preserve_context=True)
```

### Model providers

Only OpenAI-compatible HTTP endpoints are supported by the library:

```bash
# local vLLM server
python -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen2.5-14B-Instruct --port 8000
```

```python
llm = LLM("Qwen/Qwen2.5-14B-Instruct", url="http://localhost:8000/v1")
```

Remote APIs use the same interface; pass `api_key_env` or
`STATEACT_LLM_API_KEY`. Environment variables supported by
`LLM.from_env(...)` are `STATEACT_LLM_URL`, `STATEACT_LLM_API_KEY`,
`STATEACT_LLM_API_KEY_ENV` and `STATEACT_LLM_MODE`.

The benchmark scripts still have the older in-process `VLLMChat` backend for
exact paper reproduction; that is separate from the library's `LLM` client.

---

## Reproduction results (paper Table 2)

Paper settings: StateAct, Qwen2.5-14B-Instruct, greedy decoding.

| Benchmark | Paper | Seed 42 | No seed | Exact setting |
| --- | --- | --- | --- | --- |
| ALFWorld | **0.78** | **0.776119** (104/134) | — | `--seed 42` |
| WebShop | **0.33** | 0.29 (29/100) | **0.34** (34/100) | `--seed -1` |
| TextCraft | **0.37** | 0.41 (41/100) | **0.36** (36/100) | `--seed -1` |

Notes:

- ALFWorld matches the paper at two-decimal precision (0.78).
- WebShop no-seed and TextCraft no-seed are each within one environment of the
  paper (34 vs 33 and 36 vs 37).
- vLLM is not bit-deterministic at temperature 0; a single run can move by a
  few environments. The no-seed setting matches the original paper scripts.
- Seed-42 runs are shown for comparison and are not the paper setting.

Full ALFWorld log:

```text
Overall (mean) Score: 0.776119 with 104 successful envs and a total of 134 envs.
```

---

## Run everything on the A100 cluster (PBS)

From the repository root:

```bash
# ALFWorld paper config
bash scripts/submit_pbs.sh alfworld \
  -v "MODEL=Qwen/Qwen2.5-14B-Instruct,AGENT=ours-text,TRIAL_NAME=paper_repro_14b"

# WebShop paper config
bash scripts/submit_pbs.sh webshop \
  -v "RESULTS_FOLDER=results/paper_repro_14b,WEBSHOP_SIMG=/path/to/webshop.simg"

# TextCraft paper config
bash scripts/submit_pbs.sh textcraft \
  -v "RESULTS_FOLDER=results/paper_repro_14b"

# List / dry-run
bash scripts/submit_pbs.sh alfworld --dry-run
```

Defaults:

| Job | Model | Agent | Size |
| --- | --- | --- | --- |
| ALFWorld | Qwen2.5-7B-Instruct | `stateact` | 134 envs |
| WebShop | Qwen2.5-14B-Instruct | `stateact2` | 100 envs |
| TextCraft | Qwen2.5-14B-Instruct | `stateact` | 100 games, depth 1 |

All jobs write logs to `logs/pbs/<benchmark>_<timestamp>.log`. See
[`scripts/README.md`](scripts/README.md) for every overridable variable and the
SLURM equivalent.

---

## Run locally

### ALFWorld

```bash
cd alfworld_runs
python3 alfworld_run.py \
  --agent ours-text \
  --llm_type VLLMChat \
  --model Qwen/Qwen2.5-14B-Instruct \
  --keys_to_use '["goal","current_location","current_inventory","locations_visited","thought","action"]' \
  --trial_name paper_repro_14b \
  --start_index 0 \
  --num_envs 134 \
  --prompt_ids 1 0 \
  --apply_correction \
  --force_run --force_model \
  --max_model_len 16000 \
  --seed 42
```

Score it:

```bash
python3 get_score.py --trial_name paper_repro_14b
```

### WebShop

Start the WebShop server (see [`webshop_runs/README.md`](webshop_runs/README.md)),
then:

```bash
cd webshop_runs
python3 run_webshop_adapted.py \
  --llm_type LOCAL \
  --socket ./tmp/webshop.sock \
  --model_local Qwen/Qwen2.5-14B-Instruct \
  --agent stateact2 \
  --start 0 --num_envs 100 \
  --max_model_len 16000 \
  --seed 42 \
  --results_folder results/paper_repro_14b
```

### TextCraft

```bash
cd textcraft_runs
python3 run_textcraft_adapt.py \
  --llm_type LOCAL \
  --model_local Qwen/Qwen2.5-14B-Instruct \
  --agent_type stateact \
  --num_games 100 \
  --max_depth 1 \
  --max_model_len 16000 \
  --seed 42 \
  --results_folder results/paper_repro_14b
```

### API / URL models

No provider SDK is required. Any OpenAI-compatible endpoint works:

```bash
python3 alfworld_run.py \
  --agent stateact \
  --llm_type URLChat \
  --model my-model \
  --llm_url https://api.example.com/v1/chat/completions \
  --llm_api_key_env MY_API_KEY \
  --force_run
```

`URLChat`, `URLText`, `VLLMChat` and `Manual` are the current backends. Older
provider names are accepted as aliases in the experiment tables.

---

## Results

Every benchmark writes the same files:

```text
<results_folder>/<trial>/
  summary.csv    # one row per agent/run
  episodes.csv   # one row per environment episode
```

Common summary columns:

```text
run_id, benchmark, agent, model, trial, split, num_envs, score,
success_rate, failure_rate, avg_reward, avg_steps,
started_at, finished_at, details
```

Common episode columns:

```text
run_id, benchmark, agent, model, trial, env_idx, env_type,
success, done, reward, steps, error, early_stop, details
```

Benchmark-specific values live in the `details` JSON column. There is no
legacy result loader: the old branch contains the old formats.

---

## Analysis

Notebooks are in [`analysis/`](analysis):

- [`analysis/alfworld.ipynb`](analysis/alfworld.ipynb)
- [`analysis/webshop.ipynb`](analysis/webshop.ipynb)
- [`analysis/textcraft.ipynb`](analysis/textcraft.ipynb)

CLI:

```bash
python -m stateact.analysis alfworld --trial-name paper_repro_14b_fixed
python -m stateact.analysis webshop  webshop_runs/results/paper_repro_14b --best
python -m stateact.analysis textcraft textcraft_runs/results/paper_repro_14b
```

Python:

```python
from stateact.analysis import load_summary, load_episodes, summarise

episodes = load_episodes("alfworld_runs/results/paper_repro_14b_fixed")
runs = summarise("webshop_runs/results/paper_repro_14b")
```

---

## Repository layout

```text
stateact/
  agents.py       # ReAct, AgentBench, StateAct (string/JSON), Reflexion, ADaPT
  llms.py         # OpenAI-compatible LLM client (requests)
  backends.py     # benchmark model backends (local vLLM, URL, Manual)
  envs/           # BaseEnv + ALFWorld/TextCraft/ScienceWorld/WebShop wrappers
  main_loop.py    # run an agent on an environment
  parsing.py      # action extraction / observation normalisation
  results.py      # unified summary.csv / episodes.csv + RunLogger
  scoring.py      # score one run
  analysis/       # loaders for the unified format
  run_config.py   # runs experiments/*.yaml

alfworld_runs/    # ALFWorld entry point, prompts, model_registry, adapter
webshop_runs/     # WebShop entry point
textcraft_runs/   # TextCraft entry point
experiments/      # named ALFWorld/WebShop experiment tables
analysis/         # unified analysis notebooks
examples/         # standalone library examples
scripts/          # PBS jobs (ALFWorld, WebShop, TextCraft)
tests/            # unit tests (no benchmark install required)
```

---

## Development

```bash
make test     # pytest
make lint     # ruff + PBS syntax
make build    # wheel + sdist
make compile  # byte-compile all entry points
```

CI runs the same checks on Python 3.9–3.12.

---

## Citation

A machine-readable citation is in [`CITATION.cff`](CITATION.cff).

```bibtex
@article{rozanov2024stateactstatetrackingreasoning,
  title={StateAct: State Tracking and Reasoning for Acting and Planning with Large Language Models},
  author={Nikolai Rozanov and Marek Rei},
  year={2024},
  eprint={2410.02810},
  archivePrefix={arXiv},
  primaryClass={cs.AI},
  url={https://arxiv.org/abs/2410.02810}
}
```

---

(C) Nikolai Rozanov 2024–Present
