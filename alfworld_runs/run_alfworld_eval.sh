

if [ $1 == "test" ]; then
    python3 alfworld_run.py \
        --agent "react" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-0125" \
        --trial_name "v4_1_2_test" \
        --start_index 0 \
        --num_envs 1 \
        # --end_index \

fi;


if [ $1 == "test_ours" ]; then
    keys_to_use='["goal","thought","locations_visited","current_location","current_inventory","action"]'
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_0_1_test" \
        --start_index 0 \
        --num_envs 1 \
        --prompt_ids 0 1 \
        --keys_to_use $keys_to_use
        # --end_index \

fi;

if [ $1 == "test_ours_local" ]; then
    keys_to_use='["goal","thought","locations_visited","current_location","current_inventory","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "VLLMChat" \
        --model "Qwen/Qwen2.5-1.5B-Instruct" \
        --trial_name "v5_test_local" \
        --start_index 0 \
        --num_envs 1 \
        --prompt_ids 0 1 \
        --keys_to_use $keys_to_use
        # --end_index \

fi;


if [ $1 == "cerebras_test" ]; then
keys_to_use='["goal","current_location","current_inventory","thought","action"]'
python3 alfworld_run.py \
--agent "ours-text" \
--llm_type "CerebrasChatText" \
--model "llama3.1-70b" \
--trial_name "v4_1_6_test" \
--start_index 0 \
--num_envs 1 \
--keys_to_use $keys_to_use \
--prompt_ids 1 0 \
--apply_correction \
--force_run
# --end_index \
fi;

if [ $1 == "cerebras_main" ]; then
keys_to_use='["goal","current_location","current_inventory","thought","action"]'
python3 alfworld_run.py \
--agent "ours-text" \
--llm_type "CerebrasChatText" \
--model "llama3.1-70b" \
--trial_name "v4_1_9_cerebras" \
--start_index 0 \
--num_envs 134 \
--keys_to_use $keys_to_use \
--prompt_ids 1 0 \
--apply_correction \
--force_run
# --end_index \

python3 alfworld_run.py \
    --agent "react" \
    --llm_type "CerebrasChatText" \
    --model "llama3.1-70b" \
    --trial_name "v4_1_9_cerebras" \
    --start_index 0 \
    --num_envs 134 \
    --prompt_ids 1 0 \
    --apply_correction \
    --force_run
    # --end_index \
fi;


if [ $1 == "cerebras_test2" ]; then
    python3 alfworld_run.py \
        --agent "react" \
        --llm_type "CerebrasChatText" \
        --model "llama3.1-8b" \
        --trial_name "v4_1_6_test" \
        --start_index 0 \
        --num_envs 1 \
        --prompt_ids 1 0 \
        --apply_correction \
        --force_run
        # --end_index \
fi;



if [ $1 == "camera_ready_test" ]; then
    keys_to_use='["goal","current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "NvidiaChatText" \
        --model "mistralai/mixtral-8x22b-instruct-v0.1" \
        --trial_name "v4_1_6_test" \
        --start_index 0 \
        --num_envs 1 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --apply_correction \
        --force_run
        # --end_index \

    # python3 alfworld_run.py \
    #     --agent "react" \
    #     --llm_type "OpenAIChatText" \
    #     --model "gpt-4o-mini" \
    #     --trial_name "v4_1_6_test" \
    #     --start_index 0 \
    #     --num_envs 1 \
    #     --prompt_ids 1 0 \
    #     --apply_correction \
    #     --force_run
    #     # --end_index \

    # keys_to_use='["goal","current_location","current_inventory","thought","action"]'
    # python3 alfworld_run.py \
    #     --agent "ours-text" \
    #     --llm_type "OpenAIChatText" \
    #     --model "gpt-4o-mini" \
    #     --trial_name "v4_1_6_test" \
    #     --start_index 0 \
    #     --num_envs 1 \
    #     --keys_to_use $keys_to_use \
    #     --prompt_ids 1 0 \
    #     --apply_correction \
    #     --force_run
    #     # --end_index \


    # python3 alfworld_run.py \
    #     --agent "react" \
    #     --llm_type "CohereChatText" \
    #     --model "command-r-plus" \
    #     --trial_name "v4_1_6_test" \
    #     --start_index 0 \
    #     --num_envs 1 \
    #     --prompt_ids 1 0 \
    #     --apply_correction \
    #     --force_run
    #     # --end_index \

    # keys_to_use='["goal","current_location","current_inventory","thought","action"]'
    # python3 alfworld_run.py \
    #     --agent "ours-text" \
    #     --llm_type "CohereChatText" \
    #     --model "command-r-plus" \
    #     --trial_name "v4_1_6_test" \
    #     --start_index 0 \
    #     --num_envs 1 \
    #     --keys_to_use $keys_to_use \
    #     --prompt_ids 1 0 \
    #     --apply_correction \
    #     --force_run
    #     # --end_index \

fi;

if [ $1 == "camera_ready_cohere" ]; then
    python3 alfworld_run.py \
        --agent "react" \
        --llm_type "CohereChatText" \
        --model "command-r-plus" \
        --trial_name "v4_1_6_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --prompt_ids 1 0 \
        --apply_correction \
        --force_run
        # --end_index \

    keys_to_use='["goal","current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "CohereChatText" \
        --model "command-r-plus" \
        --trial_name "v4_1_6_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --apply_correction \
        --force_run
        # --end_index \


fi;


if [ $1 == "camera_ready_nvidia" ]; then
    # python3 alfworld_run.py \
    #     --agent "react" \
    #     --llm_type "NvidiaChatText" \
    #     --model "mistralai/mixtral-8x22b-instruct-v0.1" \
    #     --trial_name "v4_1_9_eval_correction" \
    #     --start_index 0 \
    #     --num_envs 135 \
    #     --prompt_ids 1 0 \
    #     --apply_correction \
    #     --force_run
    #     # --end_index \

    keys_to_use='["goal","current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "NvidiaChatText" \
        --model "mistralai/mixtral-8x22b-instruct-v0.1" \
        --trial_name "v4_1_9_eval_correction" \
        --start_index 113 \
        --num_envs 22 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --apply_correction \
        --force_run
        # --end_index \

fi;

if [ $1 == "camera_ready_gpt4o" ]; then
    python3 alfworld_run.py \
        --agent "react" \
        --llm_type "OpenAIChatText" \
        --model "gpt-4o-mini" \
        --trial_name "v4_1_7_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --prompt_ids 1 0 \
        --apply_correction \
        --force_run
        # --end_index \

    keys_to_use='["goal","current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatText" \
        --model "gpt-4o-mini" \
        --trial_name "v4_1_7_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --apply_correction \
        --force_run
        # --end_index \


fi;

if [ $1 == "test_ours_instruct" ]; then
    keys_to_use='["goal","current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIText" \
        --model "gpt-3.5-turbo-instruct" \
        --trial_name "v4_1_5_test" \
        --start_index 0 \
        --num_envs 1 \
        --prompt_ids 0 1 \
        --keys_to_use $keys_to_use
        # --end_index \

fi;


if [ $1 == "test_ours_resample" ]; then
    keys_to_use='["goal","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatTextSampling" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_test" \
        --start_index 0 \
        --num_envs 10 \
        --keys_to_use $keys_to_use \
        --prompt_ids 0 1 \
        --resample \
        --force_run
        # --end_index \

fi;


if [ $1 == "test_ours_full" ]; then
    keys_to_use='["goal","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatTextSampling" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_test" \
        --start_index 0 \
        --num_envs 1 \
        --keys_to_use $keys_to_use \
        --prompt_ids 0 1 \
        --apply_correction \
        --resample \
        --force_run
        # --end_index \

fi;



if [ $1 == "test_all" ]; then
    keys_to_use='["goal","thought","locations_visited","action"]'
    echo "=============================="
    echo "Running react with turbo-0125"
    python3 alfworld_run.py \
        --agent "react" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-0125" \
        --trial_name "v4_1_2_test" \
        --start_index 0 \
        --num_envs 1 \
        --prompt_ids 2 0 1 \
        --force_run
        # --end_index \

    echo "=============================="
    echo "Running ours with turbo-0125"
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-0125" \
        --trial_name "v4_1_2_test" \
        --start_index 0 \
        --num_envs 1 \
        --keys_to_use $keys_to_use \
        --force_run
        # --end_index \

    echo "=============================="
    echo "Running agentbench with turbo-0125"
    python3 alfworld_run.py \
        --agent "agentbench" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-0125" \
        --trial_name "v4_1_2_test" \
        --start_index 0 \
        --num_envs 1 \
        --force_run
        # --end_index \

    echo "=============================="
    echo "Running jsonreact with turbo-0125, version 2"
    python3 alfworld_run.py \
        --agent "jsonreact" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-0125" \
        --trial_name "v4_1_2_test" \
        --start_index 0 \
        --num_envs 1 \
        --agent_version 1 \
        --force_run
        # --end_index \

    echo "=============================="
    echo "Running react with turbo-0125, with sampling llm"
    python3 alfworld_run.py \
        --agent "react" \
        --llm_type "OpenAIChatTextSampling" \
        --model "gpt-3.5-turbo-0125" \
        --trial_name "v4_1_2_test" \
        --start_index 0 \
        --num_envs 1 \
        --force_run
        # --end_index \

    echo "=============================="
    echo "Running react with turbo-0125, with instruct llm"
    python3 alfworld_run.py \
        --agent "react" \
        --llm_type "OpenAIText" \
        --model "gpt-3.5-turbo-instruct" \
        --trial_name "v4_1_2_test" \
        --start_index 0 \
        --num_envs 1 \
        --force_run
        # --end_index \

    echo "=============================="
    echo "Running react with turbo-0125 with command-r-plus"
    python3 alfworld_run.py \
        --agent "react" \
        --llm_type "CohereChat" \
        --model "command-r-plus" \
        --trial_name "v4_1_2_test" \
        --start_index 0 \
        --num_envs 1 \
        --force_run
        # --end_index \

fi;


if [ $1 == "test_cohere_text" ]; then

    echo "=============================="
    echo "Running react with command-r-plus"
    python3 alfworld_run.py \
        --agent "react" \
        --llm_type "CohereChatText" \
        --model "command-r-plus" \
        --trial_name "v4_1_2_test" \
        --start_index 0 \
        --num_envs 1 \
        --force_run
        # --end_index \
fi;


if [ $1 == "test_cohere_chat" ]; then

    echo "=============================="
    echo "Running react with command-r-plus"
    python3 alfworld_run.py \
        --agent "react" \
        --llm_type "CohereChat" \
        --model "command-r-plus" \
        --trial_name "v4_1_2_test" \
        --start_index 0 \
        --num_envs 1 \
        --force_run
        # --end_index \

fi;

if [ $1 == "eval_mix" ]; then
    keys_to_use='["thought","action"]'
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    keys_to_use='["thought","action"]'
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --apply_correction \
        --force_run
        # --end_index \

    python3 alfworld_run.py \
        --agent "jsonreact" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --prompt_ids 1 0 \
        --apply_correction \
        --force_run

    python3 alfworld_run.py \
        --agent "react" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --prompt_ids 1 0 \
        --apply_correction \
        --force_run
        # --end_index \

    keys_to_use='["plan","action"]'
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    keys_to_use='["goal","action"]'
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    keys_to_use='["locations_visited","current_location","current_inventory","action"]'
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    keys_to_use='["goal","plan","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    keys_to_use='["goal","plan","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --apply_correction \
        --force_run
        # --end_index \

    keys_to_use='["goal","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --apply_correction \
        --force_run
        # --end_index \

    keys_to_use='["goal","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatTextSampling" \
        --model "gpt-3.5-turbo-1106" \
        --trial_namen "v4_1_2_eval_resample" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run \
        --resample \
        # --end_index \

    keys_to_use='["goal","locations_visited","current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run \
        --apply_correction \
        # --end_index \

    keys_to_use='["goal","locations_visited","current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatTextSampling" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval_resample" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run \
        --resample \
        # --end_index \

    keys_to_use='["goal","locations_visited","current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatTextSampling" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval_correction_resample" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run \
        --apply_correction \
        --resample \
        # --end_index \



    keys_to_use='["goal","current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatTextSampling" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval_resample" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run \
        --resample \
        # --end_index \

    keys_to_use='["goal","current_inventory","current_location","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatTextSampling" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval_resample" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run \
        --resample \
        # --end_index \

    keys_to_use='["goal","current_location","locations_visited","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run \
        # --end_index \
fi;


if [ $1 == "eval_remaining" ]; then

    python3 alfworld_run.py \
        --agent "react" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-0125" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    python3 alfworld_run.py \
        --agent "react" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-0125" \
        --trial_name "v4_1_2_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --prompt_ids 1 0 \
        --apply_correction \
        --force_run
        # --end_index \


    keys_to_use='["goal","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    keys_to_use='["goal","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    keys_to_use='["goal","locations_visited","current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    keys_to_use='["goal","current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \




    keys_to_use='["thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-0125" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    keys_to_use='["goal","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-0125" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    keys_to_use='["goal","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-0125" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    keys_to_use='["goal","locations_visited","current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-0125" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    keys_to_use='["goal","current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-0125" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \



    keys_to_use='["thought","action"]'
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-0125" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    keys_to_use='["thought","action"]'
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-0125" \
        --trial_name "v4_1_2_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run \
        --apply_correction
        # --end_index \

    keys_to_use='["goal","current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-0125" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \


    keys_to_use='["goal","current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-0125" \
        --trial_name "v4_1_2_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run \
        --apply_correction
        # --end_index \


    keys_to_use='["thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-0125" \
        --trial_name "v4_1_2_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run \
        --apply_correction
        # --end_index \

    keys_to_use='["goal","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-0125" \
        --trial_name "v4_1_2_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run \
        --apply_correction
        # --end_index \

    keys_to_use='["goal","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-0125" \
        --trial_name "v4_1_2_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run \
        --apply_correction
        # --end_index \

    keys_to_use='["goal","locations_visited","current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-0125" \
        --trial_name "v4_1_2_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run \
        --apply_correction
        # --end_index \

    keys_to_use='["goal","current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-0125" \
        --trial_name "v4_1_2_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run \
        --apply_correction
        # --end_index \





    keys_to_use='["goal","current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatTextSampling" \
        --model "gpt-3.5-turbo-0125" \
        --trial_name "v4_1_2_eval_resample" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --resample \
        --force_run
        # --end_index \


    keys_to_use='["goal","current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatTextSampling" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval_resample" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --resample \
        --force_run
        # --end_index \



    keys_to_use='["goal","current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatTextSampling" \
        --model "gpt-3.5-turbo-0125" \
        --trial_name "v4_1_2_eval_correction_resample" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --resample \
        --apply_correction \
        --force_run
        # --end_index \

    keys_to_use='["goal","current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatTextSampling" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval_correction_resample" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --resample \
        --apply_correction \
        --force_run
        # --end_index \

    keys_to_use='["goal","current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatTextSampling" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval_resample" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --resample \
        --force_run
        # --end_index \

    keys_to_use='["goal","current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatTextSampling" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval_correction_resample" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --resample \
        --apply_correction \
        --force_run
        # --end_index \

    keys_to_use='["goal","current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatTextSampling" \
        --model "gpt-3.5-turbo-0125" \
        --trial_name "v4_1_2_eval_correction_resample" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --resample \
        --apply_correction \
        --force_run
        # --end_index \

    python3 alfworld_run.py \
        --agent "react" \
        --llm_type "OpenAIChatTextSampling" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval_resample" \
        --start_index 0 \
        --num_envs 135 \
        --prompt_ids 1 0 \
        --resample \
        --force_run
        # --end_index \

    python3 alfworld_run.py \
        --agent "react" \
        --llm_type "OpenAIChatTextSampling" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval_correction_resample" \
        --start_index 0 \
        --num_envs 135 \
        --prompt_ids 1 0 \
        --force_run \
        --apply_correction \
        --resample \
        # --end_index \

    python3 alfworld_run.py \
        --agent "react" \
        --llm_type "OpenAIChatTextSampling" \
        --model "gpt-3.5-turbo-0125" \
        --trial_name "v4_1_2_eval_resample" \
        --start_index 0 \
        --num_envs 135 \
        --prompt_ids 1 0 \
        --resample \
        --force_run
        # --end_index \

    python3 alfworld_run.py \
        --agent "react" \
        --llm_type "OpenAIChatTextSampling" \
        --model "gpt-3.5-turbo-0125" \
        --trial_name "v4_1_2_eval_correction_resample" \
        --start_index 0 \
        --num_envs 135 \
        --prompt_ids 1 0 \
        --force_run \
        --apply_correction \
        --resample \
        # --end_index \
fi;



if [ $1 == "test_ours_text" ]; then
    keys_to_use='["goal","current_location","locations_visited","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_test" \
        --start_index 0 \
        --num_envs 1 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run \
        # --end_index \
fi;


if [ $1 == "eval_ours_text" ]; then
    keys_to_use='["thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run \
        # --end_index \

fi;

if [ $1 == "eval_react1" ]; then
    python3 alfworld_run.py \
        --agent "react" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

fi;



if [ $1 == "eval_additional_1106" ]; then
    python3 alfworld_run.py \
        --agent "react" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --prompt_ids 1 0 \
        --force_run \
        --apply_correction
        # --end_index \

    keys_to_use='["goal","current_location","current_inventory","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    keys_to_use='["current_location","current_inventory","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    keys_to_use='["current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    keys_to_use='["goal","current_location","current_inventory","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run \
        --apply_correction
        # --end_index \

    keys_to_use='["current_location","current_inventory","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run \
        --apply_correction
        # --end_index \

    keys_to_use='["current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run \
        --apply_correction
        # --end_index \

    keys_to_use='["goal","current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    keys_to_use='["goal","current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run \
        --apply_correction
        # --end_index \

    # keys_to_use='["goal","action"]'
    # python3 alfworld_run.py \
    #     --agent "ours" \
    #     --llm_type "OpenAIChatText" \
    #     --model "gpt-3.5-turbo-1106" \
    #     --trial_name "v4_1_2_eval" \
    #     --start_index 0 \
    #     --num_envs 135 \
    #     --keys_to_use $keys_to_use \
    #     --prompt_ids 1 0 \
    #     --force_run
    #     # --end_index \

    # keys_to_use='["goal","action"]'
    # python3 alfworld_run.py \
    #     --agent "ours" \
    #     --llm_type "OpenAIChatText" \
    #     --model "gpt-3.5-turbo-1106" \
    #     --trial_name "v4_1_2_eval_correction" \
    #     --start_index 0 \
    #     --num_envs 135 \
    #     --keys_to_use $keys_to_use \
    #     --prompt_ids 1 0 \
    #     --force_run \
    #     --apply_correction
    #     # --end_index \
fi;

if [ $1 == "eval_instruct" ]; then

    keys_to_use='["goal","current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIText" \
        --model "gpt-3.5-turbo-instruct" \
        --trial_name "v4_1_5_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run \
        --apply_correction
        # --end_index \


    python3 alfworld_run.py \
        --agent "react" \
        --llm_type "OpenAIText" \
        --model "gpt-3.5-turbo-instruct" \
        --trial_name "v4_1_5_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --prompt_ids 1 0 \
        --force_run \
        --apply_correction
        # --end_index \
fi;

if [ $1 == "eval_instruct_extra" ]; then

    # keys_to_use='["goal","current_location","current_inventory","thought","action"]'
    # python3 alfworld_run.py \
    #     --agent "ours-text" \
    #     --llm_type "OpenAIText" \
    #     --model "gpt-3.5-turbo-instruct" \
    #     --trial_name "v4_1_5_eval_correction" \
    #     --start_index 0 \
    #     --num_envs 135 \
    #     --keys_to_use $keys_to_use \
    #     --prompt_ids 1 0 \
    #     --force_run \
    #     --apply_correction
    #     # --end_index \


    python3 alfworld_run.py \
        --agent "react" \
        --llm_type "OpenAIText" \
        --model "gpt-3.5-turbo-instruct" \
        --trial_name "v4_1_5_eval" \
        --start_index 0 \
        --num_envs 135 \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \
fi;


if [ $1 == "eval_instruct_additional" ]; then

    keys_to_use='["goal","current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIText" \
        --model "gpt-3.5-turbo-instruct" \
        --trial_name "v4_1_5_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \


    # python3 alfworld_run.py \
    #     --agent "react" \
    #     --llm_type "OpenAIText" \
    #     --model "gpt-3.5-turbo-instruct" \
    #     --trial_name "v4_1_5_eval" \
    #     --start_index 0 \
    #     --num_envs 135 \
    #     --prompt_ids 1 0 \
    #     --force_run
    #     # --end_index \
fi;

if [ $1 == "eval_extra_1106" ]; then

    keys_to_use='["thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run \
        --apply_correction
        # --end_index \

    keys_to_use='["goal","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run \
        --apply_correction
        # --end_index \

    keys_to_use='["thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    keys_to_use='["goal","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    keys_to_use='["goal","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    keys_to_use='["goal","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run \
        --apply_correction
        # --end_index \
fi;



# #######################################
# Extra interest
if [ $1 == "eval_extra" ]; then

    keys_to_use='["goal","current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run \
        --apply_correction
        # --end_index \

    keys_to_use='["thought","action"]'
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run \
        --apply_correction
        # --end_index \


    keys_to_use='["goal","current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    keys_to_use='["thought","action"]'
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \


    keys_to_use='["goal","current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatTextSampling" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval_correction_resample" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run \
        --apply_correction \
        --resample
        # --end_index \

    # python3 alfworld_run.py \
    #     --agent "react" \
    #     --llm_type "OpenAIText" \
    #     --model "davinci-002" \
    #     --trial_name "v4_1_2_eval_correction" \
    #     --start_index 0 \
    #     --num_envs 135 \
    #     --prompt_ids 1 0 \
    #     --force_run \
    #     --apply_correction
    #     # --end_index \

    # python3 alfworld_run.py \
    #     --agent "react" \
    #     --llm_type "OpenAIText" \
    #     --model "davinci-002" \
    #     --trial_name "v4_1_2_eval" \
    #     --start_index 0 \
    #     --num_envs 135 \
    #     --prompt_ids 1 0 \
    #     --force_run
    #     # --end_index \

    # python3 alfworld_run.py \
    #     --agent "react" \
    #     --llm_type "OpenAIChatText" \
    #     --model "gpt-3.5-turbo-0301" \
    #     --trial_name "v4_1_2_eval" \
    #     --start_index 0 \
    #     --num_envs 135 \
    #     --prompt_ids 1 0 \
    #     --force_run
    #     # --end_index \


    # python3 alfworld_run.py \
    #     --agent "react" \
    #     --llm_type "OpenAIChatText" \
    #     --model "gpt-3.5-turbo-0301" \
    #     --trial_name "v4_1_2_eval_correction" \
    #     --start_index 0 \
    #     --num_envs 135 \
    #     --prompt_ids 1 0 \
    #     --force_run \
    #     --apply_correction
    #     # --end_index \


    # keys_to_use='["goal","current_location","current_inventory","thought","action"]'
    # python3 alfworld_run.py \
    #     --agent "ours-text" \
    #     --llm_type "OpenAIChatTextSampling" \
    #     --model "gpt-3.5-turbo-1106" \
    #     --trial_name "v4_1_2_eval_resample" \
    #     --start_index 0 \
    #     --num_envs 135 \
    #     --keys_to_use $keys_to_use \
    #     --prompt_ids 1 0 \
    #     --force_run \
    #     --resample
    #     # --end_index \

    # python3 alfworld_run.py \
    #     --agent "react" \
    #     --llm_type "OpenAIChatTextSampling" \
    #     --model "gpt-3.5-turbo-1106" \
    #     --trial_name "v4_1_2_eval_resample" \
    #     --start_index 0 \
    #     --num_envs 135 \
    #     --prompt_ids 1 0 \
    #     --force_run \
    #     --resample
    #     # --end_index \


    # python3 alfworld_run.py \
    #     --agent "react" \
    #     --llm_type "OpenAIChatTextSampling" \
    #     --model "gpt-3.5-turbo-1106" \
    #     --trial_name "v4_1_2_eval_resample_correction" \
    #     --start_index 0 \
    #     --num_envs 135 \
    #     --prompt_ids 1 0 \
    #     --force_run \
    #     --apply_correction \
    #     --resample
    #     # --end_index \

fi;

# #######################################
# davinci EVALUATION
if [ $1 == "test_davinci_002" ]; then
    python3 alfworld_run.py \
        --agent "react" \
        --llm_type "OpenAIText" \
        --model "davinci-002" \
        --trial_name "v4_1_2_test" \
        --start_index 0 \
        --num_envs 1 \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \
fi;

# #######################################
# davinci EVALUATION
# if [ $1 == "eval_react_davinci_002" ]; then

#     python3 alfworld_run.py \
#         --agent "react" \
#         --llm_type "OpenAIText" \
#         --model "davinci-002" \
#         --trial_name "v4_1_2_eval_correction" \
#         --start_index 0 \
#         --num_envs 135 \
#         --prompt_ids 1 0 \
#         --force_run \
#         --apply_correction
#         # --end_index \

#     python3 alfworld_run.py \
#         --agent "react" \
#         --llm_type "OpenAIText" \
#         --model "davinci-002" \
#         --trial_name "v4_1_2_eval" \
#         --start_index 0 \
#         --num_envs 135 \
#         --prompt_ids 1 0 \
#         --force_run
#         # --end_index \

# fi;

# #######################################
# 0125 EVALUATION
if [ $1 == "eval_additional_0125" ]; then
    python3 alfworld_run.py \
        --agent "react" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-0125" \
        --trial_name "v4_1_3_eval" \
        --start_index 0 \
        --num_envs 135 \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    python3 alfworld_run.py \
        --agent "react" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-0125" \
        --trial_name "v4_1_3_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --prompt_ids 1 0 \
        --force_run \
        --apply_correction
        # --end_index \


    # keys_to_use='["goal","action"]'
    # python3 alfworld_run.py \
    #     --agent "ours-text" \
    #     --llm_type "OpenAIChatText" \
    #     --model "gpt-3.5-turbo-0125" \
    #     --trial_name "v4_1_3_eval_correction" \
    #     --start_index 0 \
    #     --num_envs 135 \
    #     --keys_to_use $keys_to_use \
    #     --prompt_ids 1 0 \
    #     --force_run \
    #     --apply_correction
    #     # --end_index \


    # keys_to_use='["thought","action"]'
    # python3 alfworld_run.py \
    #     --agent "ours-text" \
    #     --llm_type "OpenAIChatText" \
    #     --model "gpt-3.5-turbo-0125" \
    #     --trial_name "v4_1_3_eval_correction" \
    #     --start_index 0 \
    #     --num_envs 135 \
    #     --keys_to_use $keys_to_use \
    #     --prompt_ids 1 0 \
    #     --force_run \
    #     --apply_correction
    #     # --end_index \

    keys_to_use='["goal","current_location","current_inventory","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-0125" \
        --trial_name "v4_1_3_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run \
        --apply_correction
        # --end_index \

    # keys_to_use='["current_location","current_inventory","action"]'
    # python3 alfworld_run.py \
    #     --agent "ours-text" \
    #     --llm_type "OpenAIChatText" \
    #     --model "gpt-3.5-turbo-0125" \
    #     --trial_name "v4_1_3_eval_correction" \
    #     --start_index 0 \
    #     --num_envs 135 \
    #     --keys_to_use $keys_to_use \
    #     --prompt_ids 1 0 \
    #     --force_run \
    #     --apply_correction
    #     # --end_index \

    # keys_to_use='["current_location","current_inventory","thought","action"]'
    # python3 alfworld_run.py \
    #     --agent "ours-text" \
    #     --llm_type "OpenAIChatText" \
    #     --model "gpt-3.5-turbo-0125" \
    #     --trial_name "v4_1_3_eval_correction" \
    #     --start_index 0 \
    #     --num_envs 135 \
    #     --keys_to_use $keys_to_use \
    #     --prompt_ids 1 0 \
    #     --force_run \
    #     --apply_correction
    #     # --end_index \

    keys_to_use='["goal","current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-0125" \
        --trial_name "v4_1_3_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run \
        --apply_correction
        # --end_index \


    # keys_to_use='["goal","thought","action"]'
    # python3 alfworld_run.py \
    #     --agent "ours-text" \
    #     --llm_type "OpenAIChatText" \
    #     --model "gpt-3.5-turbo-0125" \
    #     --trial_name "v4_1_3_eval_correction" \
    #     --start_index 0 \
    #     --num_envs 135 \
    #     --keys_to_use $keys_to_use \
    #     --prompt_ids 1 0 \
    #     --force_run \
    #     --apply_correction
    #     # --end_index \





    keys_to_use='["goal","current_location","current_inventory","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-0125" \
        --trial_name "v4_1_3_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    # keys_to_use='["current_location","current_inventory","action"]'
    # python3 alfworld_run.py \
    #     --agent "ours-text" \
    #     --llm_type "OpenAIChatText" \
    #     --model "gpt-3.5-turbo-0125" \
    #     --trial_name "v4_1_3_eval" \
    #     --start_index 0 \
    #     --num_envs 135 \
    #     --keys_to_use $keys_to_use \
    #     --prompt_ids 1 0 \
    #     --force_run
    #     # --end_index \

    # keys_to_use='["current_location","current_inventory","thought","action"]'
    # python3 alfworld_run.py \
    #     --agent "ours-text" \
    #     --llm_type "OpenAIChatText" \
    #     --model "gpt-3.5-turbo-0125" \
    #     --trial_name "v4_1_2_eval" \
    #     --start_index 0 \
    #     --num_envs 135 \
    #     --keys_to_use $keys_to_use \
    #     --prompt_ids 1 0 \
    #     --force_run
    #     # --end_index \

    keys_to_use='["goal","current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-0125" \
        --trial_name "v4_1_3_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    # keys_to_use='["goal","action"]'
    # python3 alfworld_run.py \
    #     --agent "ours-text" \
    #     --llm_type "OpenAIChatText" \
    #     --model "gpt-3.5-turbo-0125" \
    #     --trial_name "v4_1_3_eval" \
    #     --start_index 0 \
    #     --num_envs 135 \
    #     --keys_to_use $keys_to_use \
    #     --prompt_ids 1 0 \
    #     --force_run
    #     # --end_index \

    # keys_to_use='["thought","action"]'
    # python3 alfworld_run.py \
    #     --agent "ours-text" \
    #     --llm_type "OpenAIChatText" \
    #     --model "gpt-3.5-turbo-0125" \
    #     --trial_name "v4_1_3_eval" \
    #     --start_index 0 \
    #     --num_envs 135 \
    #     --keys_to_use $keys_to_use \
    #     --prompt_ids 1 0 \
    #     --force_run
    #     # --end_index \

    # keys_to_use='["goal","thought","action"]'
    # python3 alfworld_run.py \
    #     --agent "ours-text" \
    #     --llm_type "OpenAIChatText" \
    #     --model "gpt-3.5-turbo-0125" \
    #     --trial_name "v4_1_3_eval" \
    #     --start_index 0 \
    #     --num_envs 135 \
    #     --keys_to_use $keys_to_use \
    #     --prompt_ids 1 0 \
    #     --force_run
    #     # --end_index \

fi;


# # #######################################
# # GPT-4o EVALUATION
# if [ $1 == "eval_additional_gpt-4o" ]; then
#     python3 alfworld_run.py \
#         --agent "react" \
#         --llm_type "OpenAIChatText" \
#         --model "gpt-4o" \
#         --trial_name "v4_1_4_eval" \
#         --start_index 0 \
#         --num_envs 135 \
#         --prompt_ids 1 0 \
#         --force_run
#         # --end_index \

#     python3 alfworld_run.py \
#         --agent "react" \
#         --llm_type "OpenAIChatText" \
#         --model "gpt-4o" \
#         --trial_name "v4_1_4_eval_correction" \
#         --start_index 0 \
#         --num_envs 135 \
#         --prompt_ids 1 0 \
#         --force_run \
#         --apply_correction
#         # --end_index \

# fi;




# #######################################
# Action Only evaluation
if [ $1 == "action_only_eval" ]; then
    keys_to_use='["action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run \
        --apply_correction
        # --end_index \

    keys_to_use='["action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \


    # keys_to_use='["action"]'
    # python3 alfworld_run.py \
    #     --agent "ours-text" \
    #     --llm_type "OpenAIChatText" \
    #     --model "gpt-3.5-turbo-0125" \
    #     --trial_name "v4_1_5_eval_correction" \
    #     --start_index 0 \
    #     --num_envs 135 \
    #     --keys_to_use $keys_to_use \
    #     --prompt_ids 1 0 \
    #     --force_run \
    #     --apply_correction
    #     # --end_index \

    # keys_to_use='["action"]'
    # python3 alfworld_run.py \
    #     --agent "ours-text" \
    #     --llm_type "OpenAIChatText" \
    #     --model "gpt-3.5-turbo-0125" \
    #     --trial_name "v4_1_5_eval" \
    #     --start_index 0 \
    #     --num_envs 135 \
    #     --keys_to_use $keys_to_use \
    #     --prompt_ids 1 0 \
    #     --force_run
    #     # --end_index \

    # keys_to_use='["action"]'
    # python3 alfworld_run.py \
    #     --agent "ours-text" \
    #     --llm_type "OpenAIChatText" \
    #     --model "gpt-3.5-turbo-0301" \
    #     --trial_name "v4_1_5_eval_correction" \
    #     --start_index 0 \
    #     --num_envs 135 \
    #     --keys_to_use $keys_to_use \
    #     --prompt_ids 1 0 \
    #     --force_run \
    #     --apply_correction
    #     # --end_index \

    # keys_to_use='["action"]'
    # python3 alfworld_run.py \
    #     --agent "ours-text" \
    #     --llm_type "OpenAIChatText" \
    #     --model "gpt-3.5-turbo-0301" \
    #     --trial_name "v4_1_5_eval" \
    #     --start_index 0 \
    #     --num_envs 135 \
    #     --keys_to_use $keys_to_use \
    #     --prompt_ids 1 0 \
    #     --force_run
    #     # --end_index \
fi;

# #######################################
# COHERE EVALUATION
if [ $1 == "eval_cohere_full" ]; then
    python3 alfworld_run.py \
        --agent "react" \
        --llm_type "CohereChatText" \
        --model "command-r-plus" \
        --trial_name "v4_1_4_eval" \
        --start_index 0 \
        --num_envs 135 \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    python3 alfworld_run.py \
        --agent "react" \
        --llm_type "CohereChatText" \
        --model "command-r-plus" \
        --trial_name "v4_1_4_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --prompt_ids 1 0 \
        --force_run \
        --apply_correction
        # --end_index \

    keys_to_use='["goal","current_location","current_inventory","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "CohereChatText" \
        --model "command-r-plus" \
        --trial_name "v4_1_4_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    keys_to_use='["current_location","current_inventory","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "CohereChatText" \
        --model "command-r-plus" \
        --trial_name "v4_1_4_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    keys_to_use='["current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "CohereChatText" \
        --model "command-r-plus" \
        --trial_name "v4_1_4_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    keys_to_use='["goal","current_location","current_inventory","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "CohereChatText" \
        --model "command-r-plus" \
        --trial_name "v4_1_4_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run \
        --apply_correction
        # --end_index \

    keys_to_use='["current_location","current_inventory","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "CohereChatText" \
        --model "command-r-plus" \
        --trial_name "v4_1_4_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run \
        --apply_correction
        # --end_index \

    keys_to_use='["current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "CohereChatText" \
        --model "command-r-plus" \
        --trial_name "v4_1_4_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run \
        --apply_correction
        # --end_index \

    keys_to_use='["goal","current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "CohereChatText" \
        --model "command-r-plus" \
        --trial_name "v4_1_4_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    keys_to_use='["goal","current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "CohereChatText" \
        --model "command-r-plus" \
        --trial_name "v4_1_4_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run \
        --apply_correction
        # --end_index \


    keys_to_use='["goal","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "CohereChatText" \
        --model "command-r-plus" \
        --trial_name "v4_1_4_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    keys_to_use='["goal","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "CohereChatText" \
        --model "command-r-plus" \
        --trial_name "v4_1_4_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run \
        --apply_correction
        # --end_index \


    keys_to_use='["thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "CohereChatText" \
        --model "command-r-plus" \
        --trial_name "v4_1_4_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    keys_to_use='["thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "CohereChatText" \
        --model "command-r-plus" \
        --trial_name "v4_1_4_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run \
        --apply_correction
        # --end_index \

    keys_to_use='["goal","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "CohereChatText" \
        --model "command-r-plus" \
        --trial_name "v4_1_4_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    keys_to_use='["goal","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours-text" \
        --llm_type "CohereChatText" \
        --model "command-r-plus" \
        --trial_name "v4_1_4_eval_correction" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run \
        --apply_correction
        # --end_index \

fi;

    # keys_to_use='["goal","locations_visited","current_location","current_inventory","action"]'
    # python3 alfworld_run.py \
    #     --agent "ours-text" \
    #     --llm_type "OpenAIChatText" \
    #     --model "gpt-3.5-turbo-1106" \
    #     --trial_name "v4_1_2_eval" \
    #     --start_index 0 \
    #     --num_envs 135 \
    #     --keys_to_use $keys_to_use \
    #     --prompt_ids 1 0 \
    #     --force_run
    #     # --end_index \


if [ $1 == "eval_full" ]; then
    python3 alfworld_run.py \
        --agent "react" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-0301" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --prompt_ids 1 0 \
        --apply_correction \
        --force_run
        # --end_index \

    python3 alfworld_run.py \
        --agent "react" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --prompt_ids 1 0 \
        --apply_correction \
        --force_run
        # --end_index \

    python3 alfworld_run.py \
        --agent "jsonreact" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --prompt_ids 1 0 \
        --force_run
        # --apply_correction
        # --end_index \

    keys_to_use='["goal","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    keys_to_use='["goal","plan","action"]'
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    keys_to_use='["goal","thought","locations_visited","current_location","current_inventory","action"]'
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    keys_to_use='["goal","plan","locations_visited","current_location","current_inventory","action"]'
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \


    keys_to_use='["goal","locations_visited","current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    keys_to_use='["goal","locations_visited","current_location","current_inventory","plan","action"]'
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    keys_to_use='["goal","current_inventory","current_location","locations_visited","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

    keys_to_use='["goal","current_location","current_inventory","thought","action"]'
    python3 alfworld_run.py \
        --agent "ours" \
        --llm_type "OpenAIChatText" \
        --model "gpt-3.5-turbo-1106" \
        --trial_name "v4_1_2_eval" \
        --start_index 0 \
        --num_envs 135 \
        --keys_to_use $keys_to_use \
        --prompt_ids 1 0 \
        --force_run
        # --end_index \

fi;
