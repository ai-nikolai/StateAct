# Cluster run scripts

This directory holds the PBS (PBS Professional) jobs for the local A100 queue
(`hx`). The jobs use the two backends from `stateact.agents`:

- **ALFWorld**: local vLLM model, no API key.
- **WebShop**: local vLLM model + the existing `webshop_runs/webshop.simg`
  behind a unix socket.

## Quick start

From the repository root:

```bash
# ALFWorld, Qwen2.5-7B-Instruct, 134 environments
bash scripts/submit_pbs.sh alfworld

# WebShop, Qwen2.5-3B-Instruct, 100 environments
bash scripts/submit_pbs.sh webshop

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
```

Use one `-v` flag with a comma-separated list (qsub replaces the list when
given twice). Other qsub options work as usual, e.g.
`-l walltime=00:30:00` or `-q hx`.

| Variable | Default | Used by |
| --- | --- | --- |
| `MODEL` | ALFWorld: `Qwen/Qwen2.5-7B-Instruct`; WebShop: `Qwen/Qwen2.5-3B-Instruct` | both |
| `NUM_ENVS` | ALFWorld: 134; WebShop: 100 | both |
| `START_INDEX` | 0 | ALFWorld |
| `SEED` | 42 | both |
| `AGENT` | `stateact` | both |
| `MAX_MODEL_LEN` | 16000 (ALFWorld), 6400 (WebShop) | both |
| `TRIAL_NAME` | timestamped | ALFWorld |
| `RESULTS_FOLDER` | `results/stateact_local` | WebShop |
| `CONDA_ENV` | `env_alfworld` / `env_webshop` | both |
| `WEBSHOP_SIMG` | `webshop_runs/webshop.simg` | WebShop |

The scripts activate conda through `~/miniconda3/etc/profile.d/conda.sh` and
use `nvidia-smi`/one A100 from the `hx` queue. Both models fit comfortably in
a single A100 at the default context lengths; reduce `MAX_MODEL_LEN` if the
queue gives you a smaller GPU.

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

- WebShop needs the container image at `webshop_runs/webshop.simg` and the
  launcher at `~/z_scripts/example_run_webshop.sh`. The job starts the server
  with `--writable-tmpfs`, waits for the unix socket, runs the experiment, and
  cleans both up on exit.
- ALFWorld needs the ALFWorld data (`alfworld-download`) and
  `alfworld_runs/base_config.yaml`; both are already assumed by the existing
  README.
- The API/URL backend is not used by these jobs. It can be selected from the
  command line with `--llm_type URLChat --llm_url ...`.
