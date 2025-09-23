# Alfworld Environment

## Getting started
1. Installation of requirements. (Footnote 1)
<!-- Note the CMAKE line is important for `fast-downward-textworld`. (Footnote 1) -->
```bash
pip3 install -r pip3 install -r requirements.txt
```

2. Downloading Alfworld Data
```bash
alfworld-download
```

3. (**Full version** (to reproduce results)) Running alfworld locally: (tested on A100)
```bash
mkdir game_logs
keys_to_use='["goal","locations_visited","current_location","current_inventory","thought","action"]'
python3 alfworld_run.py \
   --agent "ours-text" \
   --llm_type "VLLMChat" \
   --model Qwen/Qwen2.5-14B-Instruct \
   --keys_to_use $keys_to_use \
   --trial_name "baseline_14B" \
   --start_index 0 \
   --num_envs 134 \
   --prompt_ids 1 0 \
   --apply_correction \
   --force_run \
   --force_model \
   --max_model_len 16000 \
   --seed 42
```

4. To get overall quick scores:
```bash
python3 get_score.py --trial_name "baseline_14B"
```

**Expected Result:**
```
Overall (mean) Score: 0.805970 with 108 successful env and a total of 134 envs.
```

---

## More Options:
5. Running Alfworld with different settings (see in `run_alfworld_eval.sh`). E.g.:
```bash
mkdir game_logs #unless you have the folder already
./run_alworld_eval.sh test_ours_local
```

6. To interact with Alfworld by Manually typing (i.e. as a Human):
```bash
python3 alfworld_run.py \
    --agent "react" \
    --llm_type "Manual" \
    --trial_name "reproduce" \
    --start_index 0 \
    --num_envs 1 \
    --force_run
    # --end_index \
```

7. In depth analysis happens in the `analysis_alfworld_eval_notebook.ipynb`


8. To run `ReAct` baseline:
```bash
python3 alfworld_run.py \
   --agent "react" \
   --llm_type "VLLMChat" \
   --model Qwen/Qwen2.5-14B-Instruct \
   --trial_name "baseline_react_14B" \
   --start_index 0 \
   --num_envs 134 \
   --prompt_ids 1 0 \
   --apply_correction \
   --force_run \
   --force_model \
   --max_model_len 16000 \
   --seed 42
```

<!-- **Expected Result:** -->
<!-- python3 get_score.py --trial_name "baseline_react_14B"
 -->
<!-- ```

``` -->



---
## Footnotes: 
Footnote 1: Before `fast-downward-textworld==20.6.3` (Apr 25) the classical installation breaks the installation (you will need the commented CMAKE Var), like this:
```bash
export CMAKE_POLICY_VERSION_MINIMUM=3.5 
pip3 install -r pip3 install -r requirements.txt
```

## OTHER NOTES: 

### What to use in the State?
- Note for Alfworld: For 7B or 14B models it is imortant to use `locations_visited` to get the full performance.

- Note for Webshop: Across models and agents, using `thoughts` made performance worse on Webshop.

### Blackwell GPUs not working: at the moment it seems for Blackwell GPUs the above won't work. (as of 23.09.2025)
Here is a potential fix (not verified) to install vllm: https://discuss.vllm.ai/t/vllm-on-rtx5090-working-gpu-setup-with-torch-2-9-0-cu128/1492 


---
## Other issues:
There was an issue with reproducibility: https://github.com/ai-nikolai/StateAct/issues/3 
However it was resolved, the above README instruction 3 should give you the right results.