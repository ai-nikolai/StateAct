# StateAct

Official implementation of **StateAct: Enhancing LLM Base Agents via
Self-prompting and State-tracking**
[arXiv:2410.02810](https://arxiv.org/abs/2410.02810)

StateAct is a state-tracking base agent for LLM agents. This repository runs it
on three benchmarks:

- **ALFWorld** — household text environments
- **WebShop** — simulated online shopping
- **TextCraft** — text-based crafting

The current `v2` layout keeps the benchmark environments separate but shares
the agent, result format, analysis and cluster tooling.

---

## Install

Core package and development tools:

```bash
pip install -e ".[dev]"
```

Benchmark environments are installed separately because their dependencies
differ:

```bash
pip install -r alfworld_runs/requirements.txt    # env_alfworld
pip install -r webshop_runs/requirements.txt     # env_webshop
pip install -r textcraft_runs/requirements.txt   # env_textcraft
```

The core package itself has no runtime dependencies. Local models need
`vllm` + `transformers`; URL models only need `requests`.

---

## Reproduction results (paper Table 2)

Paper settings: StateAct, Qwen2.5-14B-Instruct, greedy decoding.

| Benchmark | Paper | Reproduced | Notes |
| --- | --- | --- | --- |
| ALFWorld | **0.78** | **0.776119** (104/134) | exact at paper precision |
| WebShop | **0.33** | see `scripts/pbs/webshop_a100.pbs` | `stateact2`, 100 envs |
| TextCraft | **0.37** | see `scripts/pbs/textcraft_a100.pbs` | `stateact`, depth 1, 100 games |

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
  agents.py       # local vLLM + one requests-based URL backend + manual
  llm.py          # --llm_type registry
  parsing.py      # action extraction / observation normalisation
  prompts.py      # few-shot prompt assembly
  envs/           # ALFWorld environment adapter
  results.py      # unified summary.csv / episodes.csv + RunLogger
  scoring.py      # score one run
  analysis/       # loaders for the unified format
  run_config.py   # runs experiments/*.yaml

experiments/      # named ALFWorld/WebShop experiment tables
alfworld_runs/    # ALFWorld entry point + prompt artefacts
webshop_runs/     # WebShop entry point
textcraft_runs/   # TextCraft entry point
analysis/         # unified analysis notebooks
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
