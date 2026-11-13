# StateAct Paper

This is the **OFFICIAL** implementation of the stateact paper:
[https://arxiv.org/abs/2410.02810]

---
## Getting started
Look in the "*_runs" sub-folders for **Detailed READMEs** for the invididual environments:

Environments for StateAct:
1. [Alfworld](/alfworld_runs)
2. [Webshop](/webshop_runs)
3. [Textcraft](/textcraft_runs)

For the shared library:

```bash
pip install -e ".[dev]"   # core package + pytest / ruff / pandas / pyyaml
pytest
ruff check stateact tests
```

---

## Repository layout (v2)

The `v2` branch factors the code shared by the three benchmarks into a small,
dependency-free package; the original benchmark scripts remain the entry
points and keep working unchanged.

```
stateact/
  parsing.py      # action extraction + observation normalisation (stdlib only)
  prompts.py      # few-shot prompt assembly and --agent dispatch
  llm.py          # provider registry + llamp agent construction
  scoring.py      # aggregate *_results.csv logs
  run_config.py   # runs named experiments from experiments/*.yaml
experiments/
  alfworld.yaml   # replaces the ~1000-line if/elif shell registry
  webshop.yaml
alfworld_runs/    # ALFWorld entry point + paper prompt artefacts
webshop_runs/     # WebShop entry point + vendored environment client
textcraft_runs/   # TextCraft entry points
tests/            # unit tests for stateact (no benchmark install needed)
```

Named experiments can be listed or dry-run without installing ALFWorld,
WebShop or TextCraft:

```bash
python stateact/run_config.py alfworld --list
python stateact/run_config.py alfworld eval_mix --dry-run
bash alfworld_runs/run_alfworld_eval.sh eval_mix   # old interface, still works
```

CI (`.github/workflows/ci.yml`) runs the test suite on Python 3.9-3.12,
lints the shared package, byte-compiles the benchmark entry points, and builds
the wheel. See [`docs/v2-review.md`](docs/v2-review.md) for the v2 review,
the dependency audit and the proposed `llamp` replacement.



---
## Results:
![Results](images/results.png)

## Reference:
Please cite StateAct:
```bibtex
@article{rozanov2024stateactstatetrackingreasoning,
      title={StateAct: State Tracking and Reasoning for Acting and Planning with Large Language Models}, 
      author={Nikolai Rozanov and Marek Rei},
      year={2024},
      eprint={2410.02810},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2410.02810}, 
}
```

## Known Follow-on Work / Usage:
- https://github.com/Humaid-Ibrahim/msc-ai-individual-project-agentic-ai-learning

---
(C) - Nikolai Rozanov 2024-Present
