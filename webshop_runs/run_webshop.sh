
if [ $1 == "webshop_local" ]; then
    # SOCKET_NAME="./tmp/webshop.sock"
    ACTUAL_MODEL="Qwen/Qwen2.5-3B-Instruct"
    NUM_ENVS=100
    QUANTIZATION=0
    EXPERIMENT_NAME="results/v5_16K"
    MAX_MODEL_LEN=16000

    python3 run_webshop_adapted.py \
        --llm_type LOCAL \
        --socket $SOCKET_NAME \
        --model_local $ACTUAL_MODEL \
        --start 0 \
        --num_env $NUM_ENVS \
        --agent act \
        --max_model_len $MAX_MODEL_LEN \
        --quantization $QUANTIZATION \
        --results_folder $EXPERIMENT_NAME \
        --seed 42
fi;



if [ $1 == "webshop_api" ]; then
    NUM_ENVS=100
    EXPERIMENT_NAME="results/v6_api_paper"

    python3 run_webshop_adapted.py \
        --llm_type NORMAL \
        --start 0 \
        --num_env $NUM_ENVS \
        --agent act \
        --results_folder $EXPERIMENT_NAME \
        --seed 42
fi;


if [ $1 == "webshop_api_chat" ]; then
    NUM_ENVS=30
    EXPERIMENT_NAME="results/v6_api"

    python3 run_webshop_adapted.py \
        --llm_type CHAT \
        --start 0 \
        --num_env $NUM_ENVS \
        --agent ssa \
        --results_folder $EXPERIMENT_NAME \
        --seed 42
fi;

if [ $1 == "webshop_eval" ]; then
    NUM_ENVS=100
    # EXPERIMENT_NAME="results/v6_api_paper"
    EXPERIMENT_NAME="results/v6_api_paper"


    python3 run_webshop_adapted.py \
        --llm_type NORMAL \
        --start 0 \
        --num_env $NUM_ENVS \
        --agent ssa \
        --results_folder $EXPERIMENT_NAME \
        --seed 42

    python3 run_webshop_adapted.py \
        --llm_type NORMAL \
        --start 0 \
        --num_env $NUM_ENVS \
        --agent stateact-no-state \
        --results_folder $EXPERIMENT_NAME \
        --seed 42
fi;
