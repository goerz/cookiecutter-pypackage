# Makefile for python_boilerplate development, built around uv.
#
# Run `make help` for an overview of the available targets.

.PHONY: help develop test test-lowest coverage coverage-xml \
        black black-check isort isort-check flake8 pylint lint pre-commit \
        check-changelog changelog \
        dist dist-check \
        upgrade clean distclean

.DEFAULT_GOAL := help

# Python version for the development environment. Override on the command line,
# e.g. `make PYTHON=3.11 test`. uv downloads the interpreter if it is missing.
# If unset, uv picks the highest Python compatible with requires-python.
ifdef PYTHON
  PYTHON_ARG := --python $(PYTHON)
endif

# Dependency resolution strategy. Use `make test-lowest` to verify the project
# against the lowest declared dependency versions.
RESOLUTION ?= highest

# All development tooling lives in dependency groups (see pyproject.toml).
# `uv run` transparently creates and syncs the environment before running, and
# installs this project *editable*, so every target below picks up uncommitted
# source changes immediately, with no rebuild or reinstall step.
UV := uv run $(PYTHON_ARG) --resolution $(RESOLUTION) --all-groups

# Locations passed to the linters and formatters.
SOURCES ?= src tests

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
    match = re.match(r'^([a-z0-9A-Z_-]+):.*?## (.*)$$', line)
    if match:
        target, help = match.groups()
        print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:  ## show this help
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

develop:  ## create or sync the development environment
	uv sync $(PYTHON_ARG) --resolution $(RESOLUTION) --all-groups

test:  ## run the test suite
	$(UV) pytest -vvv --doctest-modules --doctest-glob="*.rst" --doctest-glob="*.md" --cov=python_boilerplate --durations=10 -x -s src tests README.md CONTRIBUTING.md

test-lowest:  ## run the test suite against the lowest supported Python and dependencies
	$(MAKE) PYTHON=3.10 RESOLUTION=lowest-direct test

coverage:  ## generate coverage report in ./htmlcov
	$(UV) pytest --cov=python_boilerplate --cov-report=term --cov-report=html src tests
	@echo "open htmlcov/index.html"

coverage-xml:  ## convert .coverage data to coverage.xml (for CI upload)
	$(UV) coverage xml

black:  ## apply 'black' code style to all src and test files
	$(UV) black $(SOURCES)

black-check:  ## check all src and test files for compliance to 'black' code style
	$(UV) black --check --diff $(SOURCES)

isort:  ## sort imports in all src and test files
	$(UV) isort $(SOURCES)

isort-check:  ## check all src and test files for correctly sorted imports
	$(UV) isort --check-only --diff $(SOURCES)

flake8:  ## check style with flake8
	$(UV) flake8 $(SOURCES)

pylint:  ## check the code with pylint
	$(UV) pylint src

lint: black-check isort-check flake8 pylint check-changelog  ## run all linters

check-changelog:  ## validate the reference links in CHANGELOG.md (no network)
	python scripts/check_changelog.py

changelog:  ## validate CHANGELOG.md and add any missing issue/PR link targets
	python scripts/check_changelog.py --fix

pre-commit:  ## install the pre-commit git hooks
	$(UV) pre-commit install

dist:  ## build a source distribution and wheel into ./dist
	uv build
	ls -l dist

dist-check: dist  ## check all dist files for correctness
	uvx twine check dist/*

upgrade:  ## upgrade locked dependency versions to the latest compatible release
	uv lock --upgrade

clean:  ## remove build, test, and documentation artifacts
	rm -rf build dist .eggs *.egg-info
	rm -rf .pytest_cache .coverage htmlcov .mypy_cache .ruff_cache
	rm -rf docs/_build
	find . -type d -name __pycache__ -exec rm -rf {} +

distclean: clean  ## remove all generated files, including the .venv environments
	rm -rf .venv uv.lock
