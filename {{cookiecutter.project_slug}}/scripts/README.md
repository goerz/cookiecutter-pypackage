This directory contains scripts aiding in standard development tasks (usually via the Makefile):

{% if cookiecutter.on_pypi == 'y' -%}
- `release.py` — used by `make release` to publish a new version of the package.
{% endif -%}
- `check_changelog.py` — used by `make check-changelog` / `make changelog` to validate (and optionally fill in the reference links of) `CHANGELOG.md`.
