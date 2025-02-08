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
python3 WebShop_adapted.py \
    --llm_type LOCAL \
    --socket ./tmp/webshop.sock \
    --model_local "Qwen/Qwen2.5-0.5B-Instruct" \
    --start 0 \
    --num_env 30 \
    --agent react
```


## In case you need to run it on an HPC cluster (e.g. PBS or SLURM) and you don't have access to docker
See `hpc_scripts/README.md` for more details on how to run using Singularity.

