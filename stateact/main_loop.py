"""Run an agent against a :class:`stateact.envs.BaseEnv`."""

__all__ = ["main_loop"]


def _success(env, total_reward):
    info = getattr(env, "info", None) or {}
    if isinstance(info, dict):
        won = info.get("won", info.get("success"))
        if isinstance(won, (list, tuple)):
            won = won[0] if won else False
        if won is not None:
            return bool(won)
    return total_reward >= 1.0


def main_loop(agent, env, num_runs=1, max_steps=50, preserve_context=False,
              verbose=False):
    """Run ``agent`` on ``env`` for ``num_runs`` episodes.

    Parameters
    ----------
    agent:
        Any object with ``run_step(observation) -> (action, state)`` and
        ``reset()``.
    env:
        A :class:`stateact.envs.BaseEnv` (``reset``, ``step``, ``done``,
        ``reward``, ``info``).
    num_runs:
        Number of episodes. Each episode resets the environment.
    preserve_context:
        When true, the agent is not reset between episodes. This is what
        Reflexion uses to carry reflections forward.
    """
    results = []
    for run in range(num_runs):
        if not preserve_context:
            agent.reset()
        observation = env.reset()
        total_reward = 0.0
        done = False
        steps = 0
        last_action = ""

        while not done and steps < max_steps:
            action, _state = agent.run_step(observation)
            last_action = action
            observation = env.step(action)
            total_reward += float(getattr(env, "reward", 0.0) or 0.0)
            done = bool(getattr(env, "done", False))
            steps += 1
            if verbose:
                print(
                    f"[run {run} step {steps}] action={action!r} "
                    f"reward={getattr(env, 'reward', 0.0)} done={done}"
                )

        success = _success(env, total_reward)
        record = {
            "run": run,
            "success": success,
            "reward": total_reward,
            "steps": steps,
            "done": done,
            "last_action": last_action,
        }
        results.append(record)

        if hasattr(agent, "finish_episode"):
            agent.finish_episode(
                observation=observation,
                action=last_action,
                reward=total_reward,
                done=done,
                info=getattr(env, "info", None),
                success=success,
            )

    return results
