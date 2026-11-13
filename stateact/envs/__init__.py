"""Optional environment adapters.

The core package has no benchmark dependencies. Importing a module here does
*not* import the benchmark; the heavy import happens inside the constructor.
"""

from stateact.envs.alfworld import AlfworldEnv

__all__ = ["AlfworldEnv"]
