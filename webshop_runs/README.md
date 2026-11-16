# Webshop Environment

## Running the environment

```bash
docker run --rm -p 3000:3000 ainikolai/webshop:latest "0.0.0.0"
```

```bash
mkdir tmp
docker run --rm -v ./tmp:/tmp ainikolai/webshop:latest "unix:///tmp/webshop.sock"
```

## Running the experiments
1. Installing Requirements
```bash
pip3 install -r requirements.txt
```

Note: If you are running docker in sudo mode and you are using the unix socket version (webshop.sock) you have to run python file in sudo mode as well (to allow for the python script to access the socket.)

Note: Optionally, if running local (gated) LLM you might have to login into Huggingface. To do this run: `huggingface-cli login --token $HF_API_KEY`

2. running webshop
```bash
python3 Webshop_adapted.py
```

```bash
python3 run_webshop_adapted.py \
    --llm_type LOCAL \
    --socket ./tmp/webshop.sock \
    --model_local "Qwen/Qwen2.5-0.5B-Instruct" \
    --start 0 \
    --num_envs 30 \
    --agent react
```

Paper Table 2 reproduction (StateAct, Qwen-14B):

```bash
python3 run_webshop_adapted.py \
    --llm_type LOCAL \
    --socket ./tmp/webshop.sock \
    --model_local Qwen/Qwen2.5-14B-Instruct \
    --agent stateact2 \
    --start 0 \
    --num_envs 100 \
    --max_model_len 16000 \
    --seed -1 \
    --results_folder results/paper_repro_14b
```

Expected: **0.33** success rate (paper Table 2, Qwen-14B).
The no-seed reproduction measured **0.34** (34/100); seed 42 gave 0.29.

API / URL models use the same `requests` backend as ALFWorld (no OpenAI or
Anthropic SDK needed):

```bash
python3 run_webshop_adapted.py \
    --llm_type CHAT \
    --agent stateact \
    --llm_url "https://api.example.com/v1/chat/completions" \
    --llm_api_key_env "MY_API_KEY" \
    --socket ./tmp/webshop.sock \
    --start 0 --num_envs 30
```


## Results

Runs write the shared StateAct result files into the folder passed as
`--results_folder` (default `results/stateact_local/`):

```text
summary.csv    # one row per agent/run
episodes.csv   # one row per environment
```

## In case you need to run it on an HPC cluster (e.g. PBS or SLURM) and you don't have access to docker

The ready-to-use A100 jobs and Singularity instructions are in
[`../scripts/README.md`](../scripts/README.md).

