# Analysis

One place for the ALFWorld, WebShop and TextCraft analyses. All notebooks use
[`stateact.analysis`](../stateact/analysis) and the shared result format:

```text
<results_folder>/<trial>/
  summary.csv    # one row per agent/run
  episodes.csv   # one row per environment
```

The loaders also read the historical files (`alfworld_results.csv`, WebShop
`scores.csv`, TextCraft `results.csv`), so old runs still work.

## Notebooks

- [`alfworld.ipynb`](alfworld.ipynb) — episode table, per-prompt summary, env-type pivot.
- [`webshop.ipynb`](webshop.ipynb) — run summary and best agent per model.
- [`textcraft.ipynb`](textcraft.ipynb) — aggregated success rate and depth.

The original paper notebooks are preserved in [`legacy/`](legacy/).

## CLI

```bash
python -m stateact.analysis alfworld --trial-name <trial> --base-folder alfworld_runs/results
python -m stateact.analysis webshop  webshop_runs/results/stateact_local --best
python -m stateact.analysis textcraft textcraft_runs/results/stateact_repro
```

## Python

```python
from stateact.analysis import load_summary, load_episodes, summarise
from stateact.analysis import alfworld

episodes = load_episodes("alfworld_runs/results/paper_repro_14b_fixed")
runs = summarise("webshop_runs/results/stateact_local")
summary = alfworld.summarise_trial("paper_repro_14b_fixed",
                                   base_folder="alfworld_runs/results")
```
