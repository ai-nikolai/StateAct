"""Run a StateAct agent on one ALFWorld episode.

Start an OpenAI-compatible vLLM server first:

    python -m vllm.entrypoints.openai.api_server \
        --model Qwen/Qwen2.5-14B-Instruct --port 8000

Then:

    cd alfworld_runs && python ../examples/alfworld_agent.py
"""

import os

from stateact import AlfworldEnv, LLM, StateActAgent, main_loop


def main():
    llm = LLM(
        os.environ.get("MODEL", "Qwen/Qwen2.5-14B-Instruct"),
        url=os.environ.get("STATEACT_LLM_URL", "http://localhost:8000/v1"),
        api_key_env=os.environ.get("STATEACT_LLM_API_KEY_ENV"),
    )
    agent = StateActAgent(
        llm=llm,
        example_trajectories="",
        format="string",
        prompt_order=["goal", "thought", "action"],
    )
    env = AlfworldEnv(
        os.environ.get("STATEACT_ALFWORLD_SPLIT", "ood_test"),
        config_path=os.environ.get("STATEACT_ALFWORLD_CONFIG", "base_config.yaml"),
    )
    results = main_loop(agent, env, num_runs=1, max_steps=50, verbose=True)
    print(results)


if __name__ == "__main__":
    main()
