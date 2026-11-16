"""StateAct ``BaseEnv`` wrapper for ScienceWorld.

ScienceWorld is an optional dependency (it runs a JVM simulator):

    pip install stateact[scienceworld]
    # or: pip install scienceworld

Example::

    env = ScienceWorldEnv("boil", variation=0, simplification="easy")
    observation = env.reset()
    while not env.done:
        observation = env.step("look around")
"""

from stateact.envs.base import BaseEnv

__all__ = ["ScienceWorldEnv"]


class ScienceWorldEnv(BaseEnv):
    """Wrap ``scienceworld.ScienceWorldEnv`` with the StateAct env interface."""

    def __init__(self, task_name=None, variation=0, simplification="",
                 env_step_limit=100, env=None, **kwargs):
        super().__init__()
        if env is None:
            try:
                from scienceworld import ScienceWorldEnv as _ScienceWorldEnv
            except ImportError as exc:  # pragma: no cover - env dependent
                raise ImportError(
                    "ScienceWorldEnv needs the scienceworld package "
                    "(pip install stateact[scienceworld])."
                ) from exc
            env = _ScienceWorldEnv(
                taskName=task_name,
                envStepLimit=env_step_limit,
                **kwargs,
            )
        self.env = env
        self.task_name = task_name
        self.variation = variation
        self.simplification = simplification
        self.score = 0
        self.success = False
        if task_name:
            self.load(task_name, variation, simplification)

    def load(self, task_name, variation=0, simplification=""):
        self.env.load(task_name, variation, simplification)
        self.task_name = task_name
        self.variation = variation
        self.simplification = simplification

    def reset(self, task_name=None, variation=0, simplification=""):
        if task_name:
            self.load(task_name, variation, simplification)
        observation, info = self.env.reset()
        self.reward = 0.0
        self.done = False
        self.info = info or {}
        self.score = int(self.info.get("score", 0))
        self.success = self.score >= 100
        return observation

    def step(self, action):
        observation, reward, done, info = self.env.step(action)
        self.reward = float(reward)
        self.done = bool(done)
        self.info = info or {}
        self.score = int(self.info.get("score", 0))
        self.success = self.score >= 100
        return observation

    def close(self):
        if hasattr(self.env, "close"):
            self.env.close()
