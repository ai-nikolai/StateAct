# Cluster run scripts

This directory holds the PBS (PBS Professional) jobs for the local A100 queue
(`hx`). The jobs use the local vLLM backend from `stateact.agents`:

- **ALFWorld**: `alfworld_runs/`, 134 eval environments.
- **WebShop**: `webshop_runs/` + the existing `webshop_runs/webshop.simg`
  behind a unix socket.
- **TextCraft**: `textcraft_runs/`, stateact planning with `max_depth=3`.

## Quick start

From the repository root:

```bash
# ALFWorld, Qwen2.5-7B-Instruct, 134 environments
bash scripts/submit_pbs.sh alfworld

# WebShop, Qwen2.5-14B-Instruct, stateact2, 100 environments (paper Table 2)
bash scripts/submit_pbs.sh webshop

# TextCraft, Qwen2.5-14B-Instruct, stateact, depth 1, 100 games (paper Table 2)
bash scripts/submit_pbs.sh textcraft

# Check the command without submitting
bash scripts/submit_pbs.sh alfworld --dry-run
```

Logs are written to `logs/pbs/<benchmark>_<timestamp>.log`.

## Overrides

Any qsub `-v` variable is forwarded to the job:

```bash
bash scripts/submit_pbs.sh alfworld \
    -v "MODEL=Qwen/Qwen2.5-3B-Instruct,NUM_ENVS=20,AGENT=react"

bash scripts/submit_pbs.sh webshop \
    -v "MODEL=Qwen/Qwen2.5-7B-Instruct,AGENT=act,NUM_ENVS=30"

bash scripts/submit_pbs.sh textcraft \
    -v "MODEL=Qwen/Qwen2.5-32B-Instruct,AGENT=stateact,MAX_DEPTH=3,NUM_GAMES=100"
```

For a quick smoke test, use the smaller 3B models:

```bash
bash scripts/submit_pbs.sh webshop \
    -v "MODEL=Qwen/Qwen2.5-3B-Instruct,AGENT=stateact,NUM_ENVS=10"

bash scripts/submit_pbs.sh textcraft \
    -v "MODEL=Qwen/Qwen2.5-3B-Instruct,AGENT=stateact,MAX_DEPTH=1,NUM_GAMES=10"
```

Use one `-v` flag with a comma-separated list (qsub replaces the list when
given twice). Other qsub options work as usual, e.g.
`-l walltime=00:30:00` or `-q hx`.

| Variable | Default | Used by |
| --- | --- | --- |
| `MODEL` | ALFWorld: `Qwen/Qwen2.5-7B-Instruct`; WebShop/TextCraft: `Qwen/Qwen2.5-14B-Instruct` | all |
| `NUM_ENVS` | ALFWorld: 134; WebShop: 100 | ALFWorld, WebShop |
| `NUM_GAMES` | 100 | TextCraft |
| `START_INDEX` | 0 | ALFWorld |
| `SEED` | 42 | all |
| `AGENT` | `stateact`; WebShop paper config uses `stateact2` | all |
| `MAX_DEPTH` | 1 (paper normal); use 3 for ADaPT | TextCraft |
| `MAX_MODEL_LEN` | 16000 | all |
| `TRIAL_NAME` | timestamped | ALFWorld |
| `RESULTS_FOLDER` | `results/stateact_local` (WebShop), `results/stateact_repro` (TextCraft) | WebShop, TextCraft |
| `CONDA_ENV` | `env_alfworld` / `env_webshop` / `env_textcraft` | all |
| `WEBSHOP_SIMG` | `webshop_runs/webshop.simg` | WebShop |

The scripts activate conda through `~/miniconda3/etc/profile.d/conda.sh` and
use `nvidia-smi`/one A100 from the `hx` queue. Both models fit comfortably in
a single A100 at the default context lengths; reduce `MAX_MODEL_LEN` if the
queue gives you a smaller GPU.

## Result files

All three jobs use the shared `stateact.results` format:

```text
<results_folder>/summary.csv    # one row per agent/run
<results_folder>/episodes.csv   # one row per environment
```

ALFWorld defaults to `alfworld_runs/results/<trial>/`; WebShop writes into
`webshop_runs/<RESULTS_FOLDER>/` and TextCraft into
`textcraft_runs/<RESULTS_FOLDER>/`. Benchmark-specific fields are in the
`details` JSON column.

TextCraft also writes its per-run `ADaPT_*.json` trace next to the CSV files.

## PBS or SLURM?

This cluster runs PBS, so the checked-in scripts use `#PBS` directives and
`qsub`. If you move to SLURM, replace the header with the equivalent:

```bash
#SBATCH --job-name=stateact_alfworld_a100
#SBATCH --nodes=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=64G
#SBATCH --gres=gpu:a100:1
#SBATCH --time=08:00:00
#SBATCH --partition=hx
#SBATCH --output=logs/pbs/%x_%j.log
```

and submit with `sbatch`. The body of the jobs is scheduler-independent.

## Notes

- WebShop needs the container image at `webshop_runs/webshop.simg` (or pass
  `-v WEBSHOP_SIMG=/path/to/webshop.simg`) and the launcher at
  `~/z_scripts/example_run_webshop.sh`. The job starts the server with
  `--writable-tmpfs`, waits for the unix socket, runs the experiment, and
  cleans both up on exit.
- Both jobs force `CUDA_VISIBLE_DEVICES` to a numeric ordinal because vLLM
  0.6.x cannot parse the GPU UUIDs that PBS exports.
- ALFWorld needs the ALFWorld data (`alfworld-download`) and
  `alfworld_runs/base_config.yaml`; both are already assumed by the existing
  README.
- The API/URL backend is not used by these jobs. It can be selected from the
  command line with `--llm_type URLChat --llm_url ...`.
