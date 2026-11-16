"""Base environment interface used by :func:`stateact.main_loop`."""

__all__ = ["BaseEnv"]


class BaseEnv:
    """Minimal environment contract.

    ``step`` returns the next observation and updates ``reward``, ``done`` and
    ``info`` on the environment::

        observation = env.step(action)
        while not env.done:
            ...
    """

    def __init__(self):
        self.done = False
        self.reward = 0.0
        self.info = {}

    def reset(self):
        raise NotImplementedError

    def step(self, action):
        raise NotImplementedError

    def close(self):
        pass
