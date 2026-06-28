"""Tests for `{{ cookiecutter.project_slug }}` package."""

from packaging.version import parse as parse_version

import {{ cookiecutter.project_slug }}


def test_valid_version():
    """Check that the package defines a valid ``__version__``."""
    v_curr = parse_version({{ cookiecutter.project_slug }}.__version__)
    v_orig = parse_version("{{ cookiecutter.version }}")
    assert v_curr >= v_orig
{%- if cookiecutter.sphinx_docs == 'y' %}


def test_hello_world():
    """Check the example ``hello_world`` function."""
    assert {{ cookiecutter.project_slug }}.hello_world("Alice") == "Hello, Alice!"
{%- endif %}
