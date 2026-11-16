"""Smoke tests for the package entry points."""

import sys
from pathlib import Path

import stateact


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_version_is_set():
    assert stateact.__version__


def test_add_repo_root_to_path():
    path = stateact.add_repo_root_to_path()
    assert path == str(REPO_ROOT)
    assert path in sys.path
    # Calling it twice must not duplicate the entry.
    assert stateact.add_repo_root_to_path() == path
    assert sys.path.count(path) == 1


def test_public_modules_import_without_benchmark_dependencies():
    import stateact.backends
    import stateact.analysis
    import stateact.envs
    import stateact.parsing
    import stateact.run_config
    import stateact.scoring

    assert stateact.parsing.__name__ == "stateact.parsing"
    assert stateact.backends.__name__ == "stateact.backends"
    assert stateact.analysis.__name__ == "stateact.analysis"
    assert stateact.envs.__name__ == "stateact.envs"
    assert stateact.run_config.__name__ == "stateact.run_config"
    assert stateact.scoring.__name__ == "stateact.scoring"


def test_public_agent_library_api():
    import stateact

    assert stateact.BaseAgent
    assert stateact.ReActAgent
    assert stateact.AgentBenchAgent
    assert stateact.StateActAgent
    assert stateact.ReflexionAgent
    assert stateact.AdaptAgent
    assert stateact.BaseEnv
    assert stateact.AlfworldEnv
    assert stateact.TextcraftEnv
    assert stateact.WebshopEnv
    assert stateact.LLM
    assert stateact.main_loop
