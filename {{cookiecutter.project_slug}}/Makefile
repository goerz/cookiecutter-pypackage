.PHONY: help clean clean-build clean-pyc clean-test clean-venv flake8-check pylint-check test test35 test36 test37 test38 {%- if cookiecutter.sphinx_docs == 'y' %} docs docs-pdf clean-docs{% endif %} {%- if cookiecutter.use_black == 'y' %} black-check black{% endif %} {%- if cookiecutter.use_isort == 'y' %} isort-check isort{% endif %} coverage {%- if cookiecutter.on_pypi == 'y' %} test-upload upload release{% endif %} dist dist-check {%- if cookiecutter.use_notebooks == 'y' %} notebooks jupyter-notebook jupyter-lab{% endif %}
	
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

clean: ## remove all build, {%- if cookiecutter.sphinx_docs == 'y' %} docs,{% endif %} test, and coverage artifacts, as well as tox environments
	python scripts/clean.py all

clean-build: ## remove build artifacts
	python scripts/clean.py build

clean-tests: ## remove test and coverage artifacts
	python scripts/clean.py tests

clean-venv: ## remove tox virtual environments
	python scripts/clean.py venv

{%- if cookiecutter.sphinx_docs == 'y' %}

clean-docs: ## remove documentation artifacts
	python scripts/clean.py docs

{%- endif %}

flake8-check: bootstrap ## check style with flake8
	$(TOX) -e run-flake8

pylint-check: bootstrap ## check style with pylint
	$(TOX) -e run-pylint

{% set testenvs = [] %}
{%- if cookiecutter.support_py35 == "y" and testenvs.append("py35-test") %}{% endif %}
{%- if cookiecutter.support_py36 == "y" and testenvs.append("py36-test") %}{% endif %}
{%- if cookiecutter.support_py37 == "y" and testenvs.append("py37-test") %}{% endif %}
{%- if cookiecutter.support_py38 == "y" and testenvs.append("py38-test") %}{% endif %}
{%- if cookiecutter.support_py39 == "y" and testenvs.append("py39-test") %}{% endif %}
test: bootstrap ## run tests for all supported Python versions
	$(TOX) -e {{ testenvs | join(",") }} -- $(TESTS)

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

{%- if cookiecutter.sphinx_docs == 'y' %}

docs: bootstrap ## generate Sphinx HTML documentation, including API docs
	$(TOX) -e docs
	@echo "open docs/_build/html/index.html"

docs-pdf: bootstrap ## generate Sphinx PDF documentation, via latex
	$(TOX) -e docs -- -b latex _build/latex
	$(TOX) -e run-cmd -- python docs/build_pdf.py docs/_build/latex/*.tex

{%- endif %}

{%- if cookiecutter.use_black == 'y' %}

black-check: bootstrap ## Check all src and test files for complience to "black" code style
	$(TOX) -e run-blackcheck

black: bootstrap ## Apply 'black' code style to all src and test files
	$(TOX) -e run-black

{%- endif %}

{%- if cookiecutter.use_isort == 'y' %}

isort-check: bootstrap ## Check all src and test files for correctly sorted imports
	$(TOX) -e run-isortcheck

isort: bootstrap ## Sort imports in all src and test files
	$(TOX) -e run-isort

{%- endif %}

coverage: test37  ## generate coverage report in ./htmlcov
	$(TOX) -e coverage
	@echo "open htmlcov/index.html"

{%- if cookiecutter.on_pypi == 'y' %}

test-upload: bootstrap clean-build dist ## package and upload a release to test.pypi.org
	$(TOX) -e run-cmd -- twine check dist/*
	$(TOX) -e run-cmd -- twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload: bootstrap clean-build dist ## package and upload a release to pypi.org
	$(TOX) -e run-cmd -- twine check dist/*
	$(TOX) -e run-cmd -- twine upload dist/*

release: bootstrap ## Create a new version, package and upload it
	python{{ cookiecutter.main_python }} -m venv .venv/release
	.venv/release/bin/python -m pip install click gitpython pytest
	.venv/release/bin/python ./scripts/release.py

{%- endif %}

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

{%- if cookiecutter.use_notebooks == 'y' %}

notebooks: docs/tutorial.ipynb.log

jupyter-notebook: bootstrap ## run a notebook server for editing the examples
	$(TOX) -e run-cmd -- jupyter notebook --config=/dev/null

jupyter-lab: bootstrap ## run a jupyterlab server for editing the examples
	$(TOX) -e run-cmd -- pip install jupyterlab
	$(TOX) -e run-cmd -- jupyter lab --config=/dev/null

{%- endif %}
