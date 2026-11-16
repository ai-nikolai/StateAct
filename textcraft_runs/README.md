# Textcraft Environment:

## To get started
1. Install 
```bash
pip3 install -r requirements.txt
```

2. Run:
```bash
python3 run_textcraft_adapt.py --llm_type LOCAL --model_local Qwen/Qwen2.5-3B-Instruct
```

Paper Table 2 reproduction (normal StateAct, no ADaPT):

```bash
python3 run_textcraft_adapt.py \
    --llm_type LOCAL \
    --model_local Qwen/Qwen2.5-14B-Instruct \
    --agent_type stateact \
    --num_games 100 \
    --max_depth 1 \
    --max_model_len 16000 \
    --seed -1 \
    --results_folder results/paper_repro_14b
```

Expected: **0.37** success rate (paper Table 2, Qwen-14B). The seed-42 run
measured 0.41 (41/100); the no-seed rerun is in progress. Use `--max_depth 3`
for the ADaPT test-time-scaling experiments.

For an API / URL model (no OpenAI SDK needed):

```bash
python3 run_textcraft_adapt.py \
    --llm_type GPT \
    --llm_url "https://api.example.com/v1/completions" \
    --llm_api_key_env "MY_API_KEY" \
    --agent_type stateact
```


## Results

Runs write the shared StateAct result files into `--results_folder`:

```text
summary.csv    # one row per agent/run
episodes.csv   # one row per environment
ADaPT_*.json   # per-run traces
```

---
**Acknowledgements:**

TextCraft Environment Packaged:

- [Pypi] https://pypi.org/project/textcraft/ (`pip install textcraft`)
- [Github] https://github.com/ai-nikolai/textcraft 

Papers where Textcraft is used:

- ADaPT Paper: https://arxiv.org/abs/2311.05772
- Thread Paper: https://arxiv.org/abs/2405.17402v1



