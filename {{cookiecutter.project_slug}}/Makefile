.PHONY: clean clean-test clean-pyc clean-build clean-venvs line pep8 docs dist install develop help
.DEFAULT_GOAL := help

{%- if cookiecutter.environment_manager == 'conda' %}
CONDA_PACKAGES =  {{ cookiecutter.conda_packages }}
{%- endif %}
TESTENV =
#TESTENV = MATPLOTLIBRC=tests
TESTOPTIONS = --doctest-modules --cov={{ cookiecutter.project_slug }} {%- if cookiecutter.use_notebooks == 'y' %} --nbval --sanitize-with docs/nbval_sanitize.cfg{% endif %}
TESTS = src tests docs/*.rst {%- if cookiecutter.use_notebooks == 'y' %} docs/*.ipynb{% endif %}
{%if cookiecutter.support_py37 == 'y' %}
  {%- set latest_venv = '.venv/py37' -%}
  {%- set latest_test_target = 'test37' -%}
{%elif cookiecutter.support_py36 == 'y' %}
  {%- set latest_venv = '.venv/py36' -%}
  {%- set latest_test_target = 'test36' -%}
{% elif cookiecutter.support_py35 == 'y' %}
  {%- set latest_venv = '.venv/py35' -%}
  {%- set latest_test_target = 'test35' -%}
{% else %}
  {%- set latest_venv = '.venv/py34' -%}
  {%- set latest_test_target = 'test34' -%}
{% endif %}

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test clean-venvs ## remove all build, test, coverage, and Python artifacts, as well as environments
	$(MAKE) -C docs clean

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	rm -fr src/*.egg-info
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

lint: ## check style with flake8
	flake8 src tests

pep8: ## check style with pep8
	pep8 src tests

{% if cookiecutter.environment_manager == 'conda' %}
test: {%if cookiecutter.support_py34 == 'y' %}test34{% endif %} {% if cookiecutter.support_py35 == 'y' %}test35{% endif %} {% if cookiecutter.support_py36 == 'y' %}test36{% endif %} {% if cookiecutter.support_py37 == 'y' %}test37{% endif %} ## run tests on every Python version

.venv/py34/bin/py.test:
	@conda create -y -m -p .venv/py34 python=3.4 $(CONDA_PACKAGES)
	@.venv/py34/bin/pip install -e .[dev]

test34: .venv/py34/bin/py.test ## run tests for Python 3.4
	$(TESTENV) $< -v $(TESTOPTIONS) $(TESTS)

.venv/py35/bin/py.test:
	@conda create -y -m -p .venv/py35 python=3.5 $(CONDA_PACKAGES)
	@.venv/py35/bin/pip install -e .[dev]

test35: .venv/py35/bin/py.test ## run tests for Python 3.5
	$(TESTENV) $< -v $(TESTOPTIONS) $(TESTS)

.venv/py36/bin/py.test:
	@conda create -y -m -p .venv/py36 python=3.6 $(CONDA_PACKAGES)
	@.venv/py36/bin/pip install -e .[dev]

test36: .venv/py36/bin/py.test ## run tests for Python 3.6
	$(TESTENV) $< -v $(TESTOPTIONS) $(TESTS)

.venv/py37/bin/py.test:
	@conda create -y -m -p .venv/py37 python=3.7 $(CONDA_PACKAGES)
	@.venv/py37/bin/pip install -e .[dev]

test37: .venv/py37/bin/py.test ## run tests for Python 3.6
	$(TESTENV) $< -v $(TESTOPTIONS) $(TESTS)

{{ latest_venv }}/bin/python: {{ latest_venv }}/bin/py.test

{% if cookiecutter.sphinx_docs == 'y' %}
{{ latest_venv }}/bin/sphinx-build: {{latest_venv }}/bin/py.test

docs: {{ latest_venv }}/bin/sphinx-build ## generate Sphinx HTML documentation, including API docs
	$(MAKE) -C docs SPHINXBUILD=../{{ latest_venv }}/bin/sphinx-build clean
{%- if cookiecutter.better_apidoc == 'n' %}
	@./{{ latest_venv }}/sphinx-apidoc --separate -o docs/API/ src/{{ cookiecutter.project_slug }}
	@rm -f docs/API/modules.rst
{%-endif %}
	$(MAKE) -C docs SPHINXBUILD=../{{ latest_venv }}/bin/sphinx-build html
	@echo "open docs/_build/html/index.html"

spellcheck: {{ latest_venv }}/bin/sphinx-build ## check spelling in docs
	@{{ latest_venv }}/bin/pip install sphinxcontrib-spelling
	SPELLCHECK=en_US $(MAKE) -C docs SPHINXBUILD=../{{ latest_venv }}/bin/sphinx-build spelling

{%-endif -%}
{%endif %}

coverage: {{ latest_test_target }}  ## generate coverage report in ./htmlcov
	{{ latest_venv }}/bin/coverage html
	@echo "open htmlcov/index.html"

test-upload: {{ latest_venv }}/bin/python clean-build clean-pyc dist ## package and upload a release to test.pypi.org
	{{ latest_venv }}/bin/twine check dist/*
	{{ latest_venv }}/bin/twine upload --repository-url https://test.pypi.org/legacy/ dist/*

{% if cookiecutter.on_pypi == 'y' %}
upload: {{ latest_venv }}/bin/python clean-build clean-pyc dist ## package and upload a release to pypi.org
	{{ latest_venv }}/bin/twine check dist/*
	{{ latest_venv }}/bin/twine upload dist/*

release: clean {{ latest_venv }}/bin/python ## Create a new version, package and upload it
	@echo "Prepare a relese, then use 'make test-upload' and 'make upload'	"
{%endif %}

dist: {{ latest_venv }}/bin/python clean-build clean-pyc ## builds source and wheel package
	@$< setup.py sdist
	@$< setup.py bdist_wheel
	ls -l dist

dist-check: {{ latest_venv }}/bin/python  ## Check all dist files for correctness
	{{ latest_venv }}/bin/twine check dist/*

install: clean-build clean-pyc ## install the package to the active Python's site-packages
	pip install .

uninstall:  ## uninstall the package from the active Python's site-packages
	pip uninstall {{ cookiecutter.project_slug }}

develop: clean-build clean-pyc ## install the package to the active Python's site-packages, in develop mode
	pip install -e .

develop-test: develop ## run tests within the active Python environment
	$(TESTENV) py.test -v $(TESTOPTIONS) $(TESTS)

develop-docs: develop  ## generate Sphinx HTML documentation, including API docs, within the active Python environment
	$(MAKE) -C docs clean
{%- if cookiecutter.better_apidoc == 'n' %}
	@sphinx-apidoc --separate -o docs/API/ src/{{ cookiecutter.project_slug }}
	@rm -f docs/API/modules.rst
{%-endif %}
	$(MAKE) -C docs html
	@echo "open docs/_build/html/index.html"

{%- if cookiecutter.use_notebooks == 'y' %}
{{ latest_venv }}/bin/jupyter: {{ latest_venv }}/bin/py.test

# How to execute notebook files
%.ipynb.log: %.ipynb {{ latest_venv }}/bin/jupyter
	@echo ""
	@{{ latest_venv }}/bin/jupyter nbconvert --to notebook --execute --inplace --allow-errors --ExecutePreprocessor.kernel_name='python3' --config=/dev/null $< 2>&1 | tee $@

NOTEBOOKFILES = $(shell find docs/ -iname '*.ipynb'  -maxdepth 1)
NOTEBOOKLOGS = $(patsubst %.ipynb,%.ipynb.log,$(NOTEBOOKFILES))

notebooks: $(NOTEBOOKLOGS)  ## re-evaluate the notebooks
	@echo ""
	@echo "All notebook are now up to date; the were executed using the python3 kernel"
	@{{ latest_venv }}/bin/jupyter kernelspec list | grep python3

jupyter-notebook: {{ latest_venv }}/bin/jupyter  ## run a notebook server for editing the examples
	{{ latest_venv }}/bin/jupyter notebook --config=/dev/null

jupyter-lab: {{ latest_venv }}/bin/jupyter  ## run a jupyterlab server for editing the examples
	@{{ latest_venv }}/bin/pip install jupyterlab
	{{ latest_venv }}/bin/jupyter lab --config=/dev/null
{%-endif %}
