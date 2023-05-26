.PHONY: venv setup ruff format test check clean

SHELL := /bin/bash

PYTHON_INTERPRETER := python
VENV := source .venv/bin/activate

ifeq ("$(wildcard requirements.in)","")
  PROJECT_CONFIG := pyproject.toml
else
  PROJECT_CONFIG := requirements.in
endif

venv: .venv/touchfile

.venv/touchfile: requirements.txt requirements-dev.txt
	$(VENV); pip-sync
	touch .venv/touchfile

requirements.txt: $(PROJECT_CONFIG)
	$(VENV); pip-compile --output-file=requirements.txt --resolver=backtracking $(PROJECT_CONFIG)

requirements-dev.txt: $(PROJECT_CONFIG)
	$(VENV); pip-compile --extra=dev --output-file=requirements-dev.txt --resolver=backtracking $(PROJECT_CONFIG)

setup:
	virtualenv .venv
	$(VENV); pip install pip-tools
	$(VENV); pip install --upgrade pip setuptools wheel

ruff:
	$(VENV); ruff .

format:
	$(VENV); ruff . --fix
	$(VENV); black .

test:
	$(VENV); pytest --cov=src --cov-report xml --log-level=WARNING --disable-pytest-warnings

check:
	$(VENV); ruff check .
	$(VENV); black --check .

clean:
	find . -type d -name ".ipynb_checkpoints" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf build dist