"""StateAct — state tracking and reasoning for acting and planning with LLMs.

Reference implementation for https://arxiv.org/abs/2410.02810

This package factors out the parts of the original per-environment scripts
that are shared between ALFWorld, WebShop and TextCraft:

:mod:`stateact.parsing`
    Extraction of an action from a raw LLM response, plus observation
    normalisation.  Standard library only.
:mod:`stateact.llm`
    Optional-import handling for the provider SDKs and construction of the
    ``llamp`` agent for a given ``--llm_type``.
:mod:`stateact.prompts`
    Few-shot prompt assembly and the ``--agent`` -> prompt-builder dispatch.
:mod:`stateact.scoring`
    Reading and aggregating the ``*_results.csv`` logs.
:mod:`stateact.run_config`
    Config-driven runner for the named experiments that used to live in
    ~1000-line ``if [ $1 == "name" ]`` shell scripts.

The original scripts under ``alfworld_runs/``, ``webshop_runs/`` and
``textcraft_runs/`` remain the entry points and keep working unchanged::

    python3 alfworld_runs/alfworld_run.py --help

Because those scripts are run directly (not as modules), the repository root
is not automatically on ``sys.path``.  Every entry point therefore calls
:func:`add_repo_root_to_path` before importing anything from this package.
"""

__version__ = "2.0.0"

__all__ = ["add_repo_root_to_path", "__version__"]


def add_repo_root_to_path():
    """Put the repository root on ``sys.path`` so ``import stateact`` works.

    The experiment scripts are executed as plain files (``python3
    alfworld_runs/alfworld_run.py``), which makes ``sys.path[0]`` the
    *sub-directory* holding the script.  This inserts the repository root so
    that ``stateact`` is importable both when the package is installed and
    when it is merely checked out.

    Returns the repository root path that was (or already is) importable.
    """
    import os
    import sys

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)
    return repo_root
