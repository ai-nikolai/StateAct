"""StateAct ``BaseEnv`` wrapper for TextCraft."""

from stateact.envs.base import BaseEnv

__all__ = ["TextcraftEnv"]


class TextcraftEnv(BaseEnv):
    """Wrap ``textcraft.TextCraft`` with the StateAct env interface."""

    def __init__(self, env=None, seed=None):
        super().__init__()
        if env is None:
            try:
                from textcraft import TextCraft
            except ImportError as exc:  # pragma: no cover - env dependent
                raise ImportError(
                    "TextcraftEnv needs the textcraft package "
                    "(pip install -r textcraft_runs/requirements.txt)."
                ) from exc
            env = TextCraft()
        self.env = env
        self.seed = seed
        self.task = ""

    def reset(self, seed=None):
        seed = self.seed if seed is None else seed
        if seed is None:
            observation, info = self.env.reset()
        else:
            observation, info = self.env.reset(seed=seed)
        self.task = observation
        self.reward = 0.0
        self.done = False
        self.info = info or {}
        return observation

    def step(self, action):
        result = self.env.step(action)
        # TextCraft returns (obs, reward, done, info, extra).
        if len(result) == 5:
            observation, reward, done, info, _ = result
        else:
            observation, reward, done, info = result
        self.reward = float(reward)
        self.done = bool(done)
        self.info = info
        return observation
