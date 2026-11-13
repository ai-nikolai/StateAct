"""Minimal adapter for the ALFWorld TextWorld environment.

The run script only needs ``reset()`` and ``step()``. Keeping the ALFWorld
API usage here means:

* the rest of StateAct never imports ``alfworld`` / ``textworld``;
* the environment version is pinned in one place;
* the adapter is testable with a fake environment factory (no download, no
  TextWorld install).

The adapter targets ALFWorld 0.4.x with TextWorld 1.6+ / 1.7.x.
"""

from stateact.parsing import get_env_type

__all__ = ["load_config", "AlfworldEnv"]

DEFAULT_CONFIG = "base_config.yaml"
DEFAULT_SPLIT = "eval_out_of_distribution"


def load_config(path=DEFAULT_CONFIG):
    """Load an ALFWorld YAML config (kept separate so tests can use a dict)."""
    import yaml

    with open(path) as handle:
        return yaml.safe_load(handle)


class AlfworldEnv:
    """Thin ``reset``/``step`` wrapper around ``alfworld``'s Gym environment.

    Parameters
    ----------
    config_path:
        Path to the ALFWorld YAML config.
    split:
        ``train``, ``eval_in_distribution`` or ``eval_out_of_distribution``.
    batch_size:
        TextWorld batch size. StateAct always uses 1.
    env_factory:
        Optional injection point: a callable like
        ``alfworld.agents.environment.get_environment``. Tests pass a fake
        factory; production code leaves it as ``None``.
    """

    def __init__(self, config_path=DEFAULT_CONFIG, split=DEFAULT_SPLIT,
                 batch_size=1, env_factory=None, config=None):
        self.config = config if config is not None else load_config(config_path)
        self.split = split
        self.batch_size = batch_size
        self.env_type_name = self.config["env"]["type"]

        if env_factory is None:
            from alfworld.agents.environment import get_environment
            env_factory = get_environment

        env_class = env_factory(self.env_type_name)
        self.env = env_class(self.config, train_eval=split).init_env(
            batch_size=batch_size
        )
        self.env_type = ""
        self.gamefile = ""

    def reset(self):
        """Reset and return ``(observation_text, env_type)``.

        ALFWorld prepends a room-description paragraph; the old run script
        removed it, so this adapter does the same. ``env_type`` is one of
        ``put``/``clean``/``heat``/``cool``/``examine``/``puttwo``.
        """
        observation, info = self.env.reset()
        text = observation[0]
        text = "\n".join(text.split("\n\n")[1:])

        self.gamefile = info["extra.gamefile"][0]
        name = "/".join(self.gamefile.split("/")[-3:-1])
        self.env_type = get_env_type(name)
        return text, self.env_type

    def step(self, action):
        """Step with one action and return ``(observation, reward, done, info)``."""
        observation, reward, done, info = self.env.step([action])
        return observation[0], reward[0], done[0], info

    def skip(self, count):
        """Reset ``count`` episodes (the ``--start_index`` behaviour)."""
        for _ in range(count):
            self.reset()
