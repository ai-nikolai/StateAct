PYTHON ?= python3

.PHONY: help test lint compile build smoke

help:
	@echo "make test     - run the unit tests"
	@echo "make lint     - ruff + shell syntax checks"
	@echo "make compile  - byte-compile every entry point"
	@echo "make build    - build the wheel and sdist"
	@echo "make smoke    - list/dry-run the experiment tables"

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m ruff check stateact tests
	bash -n scripts/submit_pbs.sh scripts/pbs/*.pbs

compile:
	$(PYTHON) -m compileall -q stateact alfworld_runs webshop_runs textcraft_runs

build:
	$(PYTHON) -m build

smoke:
	$(PYTHON) stateact/run_config.py alfworld --list
	$(PYTHON) stateact/run_config.py webshop --list
	$(PYTHON) stateact/run_config.py alfworld test --dry-run
