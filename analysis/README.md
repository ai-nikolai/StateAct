# Analysis

One place for the ALFWorld, WebShop and TextCraft analyses. All notebooks use
[`stateact.analysis`](../stateact/analysis) and the same result format:

```text
<results_folder>/<trial>/
  summary.csv    # one row per agent/run
  episodes.csv   # one row per environment
```

## Notebooks

- [`alfworld.ipynb`](alfworld.ipynb) — episode table, env-type success, run summary.
- [`webshop.ipynb`](webshop.ipynb) — run summary and best agent per model.
- [`textcraft.ipynb`](textcraft.ipynb) — run summary.

## CLI

```bash
python -m stateact.analysis alfworld --trial-name paper_repro_14b_fixed
python -m stateact.analysis webshop  webshop_runs/results/paper_repro_14b --best
python -m stateact.analysis textcraft textcraft_runs/results/paper_repro_14b
```

## Python

```python
from stateact.analysis import load_summary, load_episodes, summarise

episodes = load_episodes("alfworld_runs/results/paper_repro_14b_fixed")
runs = load_summary("webshop_runs/results/paper_repro_14b")
summary = summarise("textcraft_runs/results/paper_repro_14b")
```

There is no legacy format loader: all current benchmark scripts write the
files above. Historical v1/v2 outputs remain available on the old branch.
