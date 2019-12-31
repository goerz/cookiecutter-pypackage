.PHONY: help clean clean-build clean-pyc clean-test clean-venv flake8-check pylint-check test test35 test36 test37 test38 coverage dist dist-check
	
.DEFAULT_GOAL := help

TOXOPTIONS ?=
TOXINI ?= tox.ini
TOX = tox -c $(TOXINI) $(TOXOPTIONS)

# empty TESTS delegates to TOXINI
TESTS ?=

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

bootstrap: ## verify that tox is available and pre-commit hooks are active
	python scripts/bootstrap.py

clean: ## remove all build, test, and coverage artifacts, as well as tox environments
	python scripts/clean.py all

clean-build: ## remove build artifacts
	python scripts/clean.py build

clean-tests: ## remove test and coverage artifacts
	python scripts/clean.py tests

clean-venv: ## remove tox virtual environments
	python scripts/clean.py venv

flake8-check: bootstrap ## check style with flake8
	$(TOX) -e run-flake8

pylint-check: bootstrap ## check style with pylint
	$(TOX) -e run-pylint


test: bootstrap ## run tests for all supported Python versions
	$(TOX) -e py37-test -- $(TESTS)

test35: bootstrap ## run tests for Python 3.5
	$(TOX) -e py35-test -- $(TESTS)

test36: bootstrap ## run tests for Python 3.6
	$(TOX) -e py36-test -- $(TESTS)

test37: bootstrap ## run tests for Python 3.7
	$(TOX) -e py37-test -- $(TESTS)

test38: bootstrap ## run tests for Python 3.8
	$(TOX) -e py38-test -- $(TESTS)

test39: bootstrap ## run tests for Python 3.9
	$(TOX) -e py39-test -- $(TESTS)

coverage: test37  ## generate coverage report in ./htmlcov
	$(TOX) -e coverage
	@echo "open htmlcov/index.html"

dist: bootstrap ## builds source and wheel package
	$(TOX) -e run-cmd -- python setup.py sdist
	$(TOX) -e run-cmd -- python setup.py bdist_wheel
	ls -l dist

dist-check: bootstrap ## Check all dist files for correctness
	$(TOX) -e run-cmd -- twine check dist/*

# How to execute notebook files
%.ipynb.log: %.ipynb
	@echo ""
	$(TOX) -e run-cmd -- jupyter nbconvert --to notebook --execute --inplace --allow-errors --ExecutePreprocessor.kernel_name='python3'  --ExecutePreprocessor.timeout=-1 --config=/dev/null $< 2>&1 | tee $@
