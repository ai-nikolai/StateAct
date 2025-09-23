# Alfworld Environment

## Getting started
1. Installation of requirements
```bash
pip3 install -r requirements.txt
```

2. Downloading Alfworld Data
```bash
alfworld-download
```

3. (Quick Version) Running Alfworld locally
```bash
mkdir game_logs #this is required for alfworld llm to run at the moment (needs to be fixed later)
./run_alworld_eval.sh test_ours_local
```

4. (Full version) Running alfworld locally:
```bash
mkdir game_logs
keys_to_use='["goal","current_location","current_inventory","thought","action"]'
python3 alfworld_run.py \
    --agent "ours-text" \
    --llm_type "VLLMChat" \
    --model "Qwen/Qwen2.5-14B-Instruct" \
    --trial_name "v5_test_local" \
    --start_index 0 \
    --num_envs 1 \
    --prompt_ids 0 1 \
    --keys_to_use $keys_to_use \
    --force_run \
    --force_model \
    --max_model_len 16000
    # --end_index \
```

## NOTE: at the moment it seems for Blackwell GPUs the above won't work.
Here is a potential fix (not verified): https://discuss.vllm.ai/t/vllm-on-rtx5090-working-gpu-setup-with-torch-2-9-0-cu128/1492 