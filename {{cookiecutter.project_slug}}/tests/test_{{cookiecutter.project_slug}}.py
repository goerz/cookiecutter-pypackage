"""Tests for `{{ cookiecutter.project_slug }}` package."""

import pytest
from pkg_resources import parse_version

import {{ cookiecutter.project_slug }}


def test_valid_version():
    """Check that the package defines a valid ``__version__``."""
    v_curr = parse_version({{ cookiecutter.project_slug }}.__version__)
    v_orig = parse_version("{{ cookiecutter.version }}")
    assert v_curr >= v_orig
