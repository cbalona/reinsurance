.PHONY: clean venv lint format sync
SHELL := pwsh.exe

PYTHON_INTERPRETER := python
VENV := .venv/Scripts/activate

ifeq ("$(wildcard requirements.in)","")
  PROJECT_CONFIG := pyproject.toml
else
  PROJECT_CONFIG := requirements.in
endif

venv: .venv/touchfile

.venv/touchfile: requirements.txt requirements-dev.txt
	$(VENV) ; pip-sync
	python -m pip install -e ".[dev]"
	echo $null > .venv/touchfile

requirements.txt: $(PROJECT_CONFIG)
	$(VENV) ; pip-compile --output-file=requirements.txt --resolver=backtracking $(PROJECT_CONFIG)

requirements-dev.txt: $(PROJECT_CONFIG)
	$(VENV) ; pip-compile --extra=dev --output-file=requirements-dev.txt --resolver=backtracking $(PROJECT_CONFIG)


#################################################################################
# HOUSEKEEPING                                                                  #
#################################################################################
# Lint using ruff
ruff:
	ruff .

## Format files using black
format:
	ruff . --fix
	black .

# Run tests
test:
	pytest --cov=src --cov-report xml --log-level=WARNING --disable-pytest-warnings

# Run checks (ruff + test)
check:
	ruff check .
	black --check .

clean:
	Remove-Item -Recurse -Force .ipynb_checkpoints
	Get-ChildItem -Directory -Recurse -Filter .ipynb_checkpoints | ForEach-Object { if (Test-Path $_.FullName) { Remove-Item -Recurse -Force $_.FullName } }
	Remove-Item -Recurse -Force .pytest_cache
	Get-ChildItem -Directory -Recurse -Filter .pytest_cache | ForEach-Object { if (Test-Path $_.FullName) { Remove-Item -Recurse -Force $_.FullName } }
	Remove-Item -Recurse -Force __pycache__
	Get-ChildItem -Directory -Recurse -Filter __pycache__ | ForEach-Object { if (Test-Path $_.FullName) { Remove-Item -Recurse -Force $_.FullName } }
	Remove-Item -Recurse -Force build
	Remove-Item -Recurse -Force dist