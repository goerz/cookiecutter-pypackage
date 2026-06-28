.PHONY: clean help test
TESTOPTIONS = -v -x -s

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


# The test suite bakes the template (pytest-cookies) and checks the rendered
# output with black and isort. The generated projects manage their own tooling
# through uv, so only these few packages are needed here. black and isort are
# pinned so that the formatting checks are reproducible and match the versions
# used by the generated project's pre-commit hooks.
.venv/bin/cookiecutter:
	uv venv .venv
	uv pip install --python .venv/bin/python pytest-cookies "black==24.10.0" "isort==5.13.2"


clean:  ## remove testing artifacts
	rm -rf .venv


test: .venv/bin/cookiecutter  ## run tests
	PATH=$(shell pwd)/.venv/bin:$(PATH) pytest --ignore=tests/examples $(TESTOPTIONS) tests
