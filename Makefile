.PHONY: clean help test
TESTOPTIONS = -v -x -s --pdb

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT


help:  ## show this help
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)


.venv/bin/cookiecutter:
	python -m venv .venv
	.venv/bin/pip install pytest-cookies ipython pdbpp black isort pre-commit flake8 pylint


clean:  ## remove testing artifacts
	@rm -rf .venv


test: .venv/bin/cookiecutter  ## run tests
	./.venv/bin/pytest $(TESTOPTIONS) -v tests
