.PHONY: help clean clean-build clean-pyc clean-test clean-venvs lint test flake8-check pylint-check {%- if cookiecutter.sphinx_docs == 'y' %} docs{% endif %} spellcheck {%- if cookiecutter.use_black == 'y' %} black-check black{% endif %} {%- if cookiecutter.use_isort == 'y' %} isort-check isort{% endif %} coverage test-upload upload  {%- if cookiecutter.use_pre_commit == 'y' %} pre-commit-hooks {% endif %} release dist dist-check install uninstall develop develop-test develop-docs {%- if cookiecutter.use_notebooks == 'y' %} notebooks jupyter-notebook jupyter-lab{% endif %}
.DEFAULT_GOAL := help

{%- if cookiecutter.environment_manager == 'conda' %}
CONDA_PACKAGES = {{ cookiecutter.conda_packages }}
{%- endif %}
TESTENV =
#TESTENV = MATPLOTLIBRC=tests
TESTOPTIONS = --doctest-modules --cov={{ cookiecutter.project_slug }}{% if cookiecutter.sphinx_docs == 'y' %}{% if cookiecutter.use_notebooks == 'y' %} --nbval --sanitize-with docs/nbval_sanitize.cfg{% endif %}{% endif %}
TESTS = src tests{% if cookiecutter.sphinx_docs == 'y' %} docs/*.rst{% if cookiecutter.use_notebooks == 'y' %} docs/*.ipynb{% endif %}{% endif %}
{% if cookiecutter.use_black == 'y' %}
BLACKOPTIONS = {% if cookiecutter.allow_single_quote_strings == 'y' %}--skip-string-normalization {% endif %}--line-length {{ cookiecutter.linelength }}
{%- endif %}
{%-if cookiecutter.support_py37 == 'y' %}
LATESTVENV = .venv/py37
  {%- set latest_venv = '.venv/py37' -%}
  {%- set latest_test_target = 'test37' -%}
{%elif cookiecutter.support_py36 == 'y' %}
LATESTVENV = .venv/py36
  {%- set latest_venv = '.venv/py36' -%}
  {%- set latest_test_target = 'test36' -%}
{% elif cookiecutter.support_py35 == 'y' %}
LATESTVENV = .venv/py35
  {%- set latest_venv = '.venv/py35' -%}
  {%- set latest_test_target = 'test35' -%}
{% else %}
LATESTVENV = .venv/py34
  {%- set latest_venv = '.venv/py34' -%}
  {%- set latest_test_target = 'test34' -%}
{% endif %}

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

clean: clean-build clean-pyc clean-test clean-venvs ## remove all build, test, coverage, and Python artifacts, as well as environments
	{% if cookiecutter.sphinx_docs == 'y' %}$(MAKE) -C docs clean{% else %}@echo "Done cleaning"{% endif %}

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	rm -fr src/*.egg-info
	rm -fr pip-wheel-metadata/
	find tests src -name '*.egg-info' -exec rm -fr {} +
	find tests src -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find tests src -name '*.pyc' -exec rm -f {} +
	find tests src -name '*.pyo' -exec rm -f {} +
	find tests src -name '*~' -exec rm -f {} +
	find tests src -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -f .coverage
	rm -fr htmlcov/

clean-venvs: ## remove testing/build environments
	rm -fr .tox
	rm -fr .venv

flake8-check: $(LATESTVENV)/bin/python ## check style with flake8
	$(LATESTVENV)/bin/python -m flake8 src tests

pylint-check: $(LATESTVENV)/bin/python ## check style with pylint
	$(LATESTVENV)/bin/python -m pylint -j 0 src

{% if cookiecutter.environment_manager == 'conda' %}
test: {%-if cookiecutter.support_py34 == 'y' %} test34{% endif %} {%- if cookiecutter.support_py35 == 'y' %} test35{% endif %} {%- if cookiecutter.support_py36 == 'y' %} test36{% endif %} {%- if cookiecutter.support_py37 == 'y' %} test37{% endif %} ## run tests on every supported Python version

.venv/py34/bin/py.test:
	@conda create -y -m -p .venv/py34 python=3.4 $(CONDA_PACKAGES)
	@.venv/py34/bin/python -m pip install -e .[dev]
{%- if cookiecutter.use_pre_commit == 'y' and latest_venv == '.venv/py34' %}
	@{{ latest_venv }}/bin/python scripts/install-pre-commit.py
{%- endif %}

test34: .venv/py34/bin/py.test ## run tests for Python 3.4
	$(TESTENV) $< -v $(TESTOPTIONS) $(TESTS)

.venv/py35/bin/py.test:
	@conda create -y -m -p .venv/py35 python=3.5 $(CONDA_PACKAGES)
	@.venv/py35/bin/python -m pip install -e .[dev]
{%- if cookiecutter.use_pre_commit == 'y' and latest_venv == '.venv/py35' %}
	@{{ latest_venv }}/bin/python scripts/install-pre-commit.py
{%- endif %}

test35: .venv/py35/bin/py.test ## run tests for Python 3.5
	$(TESTENV) $< -v $(TESTOPTIONS) $(TESTS)

.venv/py36/bin/py.test:
	@conda create -y -m -p .venv/py36 python=3.6 $(CONDA_PACKAGES)
	@.venv/py36/bin/python -m pip install -e .[dev]
{%- if cookiecutter.use_pre_commit == 'y' and latest_venv == '.venv/py36' %}
	@{{ latest_venv }}/bin/python scripts/install-pre-commit.py
{%- endif %}

test36: .venv/py36/bin/py.test{% if latest_test_target == 'test36' %}{% if cookiecutter.use_isort == 'y' %} isort-check{% endif %}{% if cookiecutter.use_black == 'y' %} black-check{% endif %}{% endif %} ## run tests for Python 3.6
	$(TESTENV) $< -v $(TESTOPTIONS) $(TESTS)

.venv/py37/bin/py.test:
	@conda create -y -m -p .venv/py37 python=3.7 $(CONDA_PACKAGES)
	@.venv/py37/bin/python -m pip install -e .[dev]
{%- if cookiecutter.use_pre_commit == 'y' and latest_venv == '.venv/py37' %}
	@{{ latest_venv }}/bin/python scripts/install-pre-commit.py
{%- endif %}

test37: .venv/py37/bin/py.test {% if latest_test_target == 'test37' %}{% if cookiecutter.use_isort == 'y' %} isort-check{% endif %}{% if cookiecutter.use_black == 'y' %} black-check{% endif %}{% endif %} ## run tests for Python 3.7
	$(TESTENV) $< -v $(TESTOPTIONS) $(TESTS)

$(LATESTVENV)/bin/python: $(LATESTVENV)/bin/py.test


{%- if cookiecutter.use_pre_commit == 'y' %}
pre-commit-hooks: $(LATESTVENV)/bin/py.test  ## install pre-commit hooks
{%- endif %}

{% if cookiecutter.sphinx_docs == 'y' %}
$(LATESTVENV)/bin/sphinx-build: $(LATESTVENV)/bin/py.test

docs: $(LATESTVENV)/bin/sphinx-build ## generate Sphinx HTML documentation, including API docs
	$(MAKE) -C docs SPHINXBUILD=../$(LATESTVENV)/bin/sphinx-build clean
{%- if cookiecutter.better_apidoc == 'n' %}
	@./$(LATESTVENV)/bin/sphinx-apidoc --separate -o docs/API/ src/{{ cookiecutter.project_slug }}
	@rm -f docs/API/modules.rst
{%-endif %}
	$(MAKE) -C docs SPHINXBUILD=../$(LATESTVENV)/bin/sphinx-build html
	@echo "open docs/_build/html/index.html"

spellcheck: $(LATESTVENV)/bin/sphinx-build ## check spelling in docs
	@$(LATESTVENV)/bin/python -m pip install sphinxcontrib-spelling
	SPELLCHECK=en_US $(MAKE) -C docs SPHINXBUILD=../$(LATESTVENV)/bin/sphinx-build spelling

{%-endif -%}
{%endif %}

{% if cookiecutter.use_black == 'y' %}
black-check: $(LATESTVENV)/bin/python  ## Check all src and test files for compliance to 'black' code style
	$(LATESTVENV)/bin/black $(BLACKOPTIONS) --diff --check src tests

black: $(LATESTVENV)/bin/python  ## Apply 'black' code style to all src and test files
	$(LATESTVENV)/bin/black $(BLACKOPTIONS) src tests

{% endif %}
{% if cookiecutter.use_isort == 'y' %}
isort-check: $(LATESTVENV)/bin/python  ## Check all src and test files for correctly sorted imports
	$(LATESTVENV)/bin/isort --recursive --check-only src tests

isort: $(LATESTVENV)/bin/python  ## Sort imports in all src and test files
	$(LATESTVENV)/bin/isort --recursive src tests

{% endif %}
coverage: {{ latest_test_target }}  ## generate coverage report in ./htmlcov
	$(LATESTVENV)/bin/coverage html
	@echo "open htmlcov/index.html"

test-upload: $(LATESTVENV)/bin/python clean-build clean-pyc dist ## package and upload a release to test.pypi.org
	$(LATESTVENV)/bin/twine check dist/*
	$(LATESTVENV)/bin/twine upload --repository-url https://test.pypi.org/legacy/ dist/*

{% if cookiecutter.on_pypi == 'y' %}
upload: $(LATESTVENV)/bin/python clean-build clean-pyc dist ## package and upload a release to pypi.org
	$(LATESTVENV)/bin/twine check dist/*
	$(LATESTVENV)/bin/twine upload dist/*

{% if cookiecutter.use_git_flow == 'n' %}
release: clean $(LATESTVENV)/bin/python ## Create a new version, package and upload it
	$(LATESTVENV)/bin/python ./scripts/release.py
{%endif %}
{%endif %}

dist: $(LATESTVENV)/bin/python clean-build clean-pyc ## builds source and wheel package
	@$< setup.py sdist
	@$< setup.py bdist_wheel
	ls -l dist

dist-check: $(LATESTVENV)/bin/python  ## Check all dist files for correctness
	$(LATESTVENV)/bin/twine check dist/*

install: clean-build clean-pyc ## install the package to the active Python's site-packages
	pip install .

uninstall:  ## uninstall the package from the active Python's site-packages
	pip uninstall {{ cookiecutter.project_slug }}

develop: clean-build clean-pyc ## install the package to the active Python's site-packages, in develop mode
	pip install -e .

develop-test: develop ## run tests within the active Python environment
	$(TESTENV) py.test -v $(TESTOPTIONS) $(TESTS)

{% if cookiecutter.sphinx_docs == 'y' %}
develop-docs: develop  ## generate Sphinx HTML documentation, including API docs, within the active Python environment
	$(MAKE) -C docs clean
{%- if cookiecutter.better_apidoc == 'n' %}
	@sphinx-apidoc --separate -o docs/API/ src/{{ cookiecutter.project_slug }}
	@rm -f docs/API/modules.rst
{%-endif %}
	$(MAKE) -C docs html
	@echo "open docs/_build/html/index.html"

{%- if cookiecutter.use_notebooks == 'y' %}
$(LATESTVENV)/bin/jupyter: $(LATESTVENV)/bin/py.test

# How to execute notebook files
%.ipynb.log: %.ipynb $(LATESTVENV)/bin/jupyter
	@echo ""
	@$(LATESTVENV)/bin/jupyter nbconvert --to notebook --execute --inplace --allow-errors --ExecutePreprocessor.kernel_name='python3' --config=/dev/null $< 2>&1 | tee $@

NOTEBOOKFILES = $(shell find docs/ -iname '*.ipynb'  -maxdepth 1)
NOTEBOOKLOGS = $(patsubst %.ipynb,%.ipynb.log,$(NOTEBOOKFILES))

notebooks: $(NOTEBOOKLOGS)  ## re-evaluate the notebooks
	@echo ""
	@echo "All notebook are now up to date; the were executed using the python3 kernel"
	@$(LATESTVENV)/bin/jupyter kernelspec list | grep python3

jupyter-notebook: $(LATESTVENV)/bin/jupyter  ## run a notebook server for editing the examples
	$(LATESTVENV)/bin/jupyter notebook --config=/dev/null

jupyter-lab: $(LATESTVENV)/bin/jupyter  ## run a jupyterlab server for editing the examples
	@$(LATESTVENV)/bin/python -m pip install jupyterlab
	$(LATESTVENV)/bin/jupyter lab --config=/dev/null
{%-endif %}
{%-endif %}
