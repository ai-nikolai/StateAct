"""StateAct ``BaseEnv`` wrapper for a WebShop client.

The WebShop server client lives in ``webshop_runs/run_webshop_adapted.py``
because it is tied to the environment image and HTTP helpers. This wrapper
adapts any client that exposes ``reset()`` and ``step(action)``.
"""

from stateact.envs.base import BaseEnv

__all__ = ["WebshopEnv"]


class WebshopEnv(BaseEnv):
    """Wrap a WebShop client object.

    ``client`` must implement ``reset()`` and ``step(action)`` returning
    ``(observation, reward, done, info)`` or ``(observation, info)`` on reset.
    """

    def __init__(self, client=None):
        super().__init__()
        if client is None:
            raise ValueError(
                "WebshopEnv needs a client. Use the client from "
                "webshop_runs/run_webshop_adapted.py, or construct "
                "WebshopEnv(client=...) after starting the WebShop server."
            )
        self.client = client

    def reset(self):
        result = self.client.reset()
        if isinstance(result, tuple) and len(result) == 2:
            observation, info = result
        else:
            observation, info = result, {}
        self.reward = 0.0
        self.done = False
        self.info = info or {}
        return observation

    def step(self, action):
        observation, reward, done, info = self.client.step(action)
        self.reward = float(reward)
        self.done = bool(done)
        self.info = info
        return observation
