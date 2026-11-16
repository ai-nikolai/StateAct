"""Run a StateAct agent on one ScienceWorld task.

Install the optional dependency first:

    pip install "stateact[scienceworld]"

Start an OpenAI-compatible vLLM server, then:

    python examples/scienceworld_agent.py
"""

import os

from stateact import LLM, ScienceWorldEnv, StateActAgent, main_loop


def main():
    llm = LLM(
        os.environ.get("MODEL", "Qwen/Qwen2.5-14B-Instruct"),
        url=os.environ.get("STATEACT_LLM_URL", "http://localhost:8000/v1"),
    )
    agent = StateActAgent(
        llm=llm,
        format="string",
        prompt_order=["goal", "thought", "action"],
    )
    env = ScienceWorldEnv(
        os.environ.get("SCIENCEWORLD_TASK", "boil"),
        variation=int(os.environ.get("SCIENCEWORLD_VARIATION", "0")),
        simplification=os.environ.get("SCIENCEWORLD_SIMPLIFICATION", ""),
    )
    results = main_loop(agent, env, num_runs=1, max_steps=100, verbose=True)
    print(results)


if __name__ == "__main__":
    main()
