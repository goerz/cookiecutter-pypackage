Contributing
============

{% set github_project_root =  "https://github.com/" ~ cookiecutter.github_username  ~ "/" ~ cookiecutter.project_slug  %}
Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.

Code of Conduct
---------------

Everyone interacting in the {{ cookiecutter.project_name }} project's code base, issue tracker, and any communication channels is expected to follow the [PyPA Code of Conduct](https://www.pypa.io/en/latest/code-of-conduct/).

Report Bugs and Submit Feedback
-------------------------------

Report bugs and propose features by filing an issue at <{{ github_project_root }}/issues>.

When reporting a bug, please include:

-   Your operating system name and version.
-   Any details about your local setup that might be helpful in troubleshooting.
-   Detailed steps to reproduce the bug, ideally a minimal but complete script or notebook.
-   All error messages in full, as plain text. If the output is long, attach it as a file.

When proposing a feature, explain how it would work and keep the scope as narrow as possible. Remember that this is a volunteer-driven project.

Get Started!
------------

The project uses [uv](https://docs.astral.sh/uv/) to manage the development environment and [`make`](https://www.gnu.org/software/make/) as a task runner. uv downloads and manages the required Python interpreters for you, so these two tools are all you need to install.

Follow [Aaron Meurer's Git Workflow Notes](https://www.asmeurer.com/git-workflow/) (with `{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}` instead of `sympy/sympy`). In short:

1.  Fork the repo on GitHub to your personal account and add your fork as a remote.
2.  Pull in the latest changes from the `{{ cookiecutter.main_branch }}` branch.
3.  Create a topic branch, make your changes, and commit them (testing locally).
4.  Push the topic branch to *your* fork and open a pull request against the base `{{ cookiecutter.main_branch }}` branch.

In your checkout, run `make develop` to create a virtual environment with all development dependencies and an editable install of the package. Run `make help` to see all available targets.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1.  The pull request should include tests.
2.  If the pull request adds functionality, the docs should be updated.
3.  Check <{{ github_project_root }}/actions> and make sure that the tests pass for all supported Python versions.

Branching Model
---------------

For developers with direct access to the repository, {{ cookiecutter.project_name }} uses a simple branching model where all development happens directly on the `{{ cookiecutter.main_branch }}` branch. Releases are tags on `{{ cookiecutter.main_branch }}`. Every commit on `{{ cookiecutter.main_branch }}` *should* pass all tests and be well-documented, so that `git bisect` remains effective.

For any non-trivial issue, work on a topic branch instead. To create one that addresses issue #1:

~~~ shell
git checkout -b 1-title-of-issue
git push -u origin 1-title-of-issue
~~~

Commit early and often on topic branches; they carry no restrictions and you are welcome to rewrite history by force-pushing. Before merging, clean up the commit history:

-   Use `git commit --amend` to fold work into your previous commit and to fix commit messages. This is the ideal way to make frequent snapshots without leaving behind meaningless commits like "fix typos".
-   Squash related commits together, e.g. `git rebase -i HEAD~4`. See the ["Rewriting History" chapter of Pro Git](https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History).
-   The `--fixup` flag for `git commit` marks a commit to be squashed into an earlier one with `git rebase --autosquash`.
-   If significant work lands on `{{ cookiecutter.main_branch }}` while you work, periodically rebase onto it (`git rebase {{ cookiecutter.main_branch }}`) rather than merging it in. See [Merging vs. Rebasing](https://www.atlassian.com/git/tutorials/merging-vs-rebasing).

If you collaborate with others on a topic branch, coordinate before rewriting history.

When the issue is fixed, merge the topic branch back with an explicit merge commit and delete it:

~~~ shell
git checkout {{ cookiecutter.main_branch }}
git merge --no-ff 1-title-of-issue
git push origin {{ cookiecutter.main_branch }}
git push --delete origin 1-title-of-issue
git branch -D 1-title-of-issue
~~~

The `--no-ff` option is critical, so that an explicit merge commit is created (especially if you rebased). Summarize the branch's changes in that commit message.

Commit Message Guidelines
-------------------------

Write commit messages according to this template:

~~~ none
Short (50 chars or less) summary ("subject line")

More detailed explanatory text. Wrap it to 72 characters. The blank
line separating the summary from the body is critical (unless you omit
the body entirely).

Write your subject line in the imperative: "Fix bug" and not "Fixed
bug" or "Fixes bug." A properly formed subject line should always be
able to complete the sentence "If applied, this commit will <subject>".

- Bullet points are okay, too, with a hanging indent.
~~~

Reference any issue being addressed as e.g. "#1". If the commit closes an issue, state `Closes #1` on the last line so that GitHub closes it automatically. See [Closing issues using keywords](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue).

Testing
-------

{{ cookiecutter.project_name }} includes a full test suite using [pytest](https://docs.pytest.org/en/latest/). We strive for a [test coverage](https://codecov.io/gh/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}) above 90%.

From a checkout of the repository, run

~~~ console
make test
~~~

to run the entire suite. By default, uv selects the highest supported Python; use e.g. `make PYTHON=3.13 test` to run on a specific interpreter, or `make test-lowest` to test against the lowest supported Python and dependency versions.

Tests live in the `tests` subfolder, in files named `test_*.py` containing functions named `test_*`. In addition, [doctests](https://docs.python.org/3/library/doctest.html) in docstrings and in the documentation source files are collected and run.

Code Style
----------

All code must be compatible with [PEP 8](https://peps.python.org/pep-0008/), with a line length limit of {{ cookiecutter.linelength }} characters (exceptions are permissible where they significantly improve readability). Beyond that, the project uses the [Black code style](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html) and sorts imports with [isort](https://pycqa.github.io/isort/) per the configuration in `pyproject.toml`.

-   `make black` / `make isort` reformat the code in place; `make black-check` / `make isort-check` only report deviations.
-   The style is enforced by the test suite and by [pre-commit](https://pre-commit.com) git hooks that block non-conforming commits. Install them with `make pre-commit`.
-   `make flake8` and `make pylint` provide additional, non-mandatory guidance on possible improvements.
{% if cookiecutter.sphinx_docs == 'y' %}
Write Documentation
-------------------

More documentation is always welcome, whether in the official docs, in docstrings, or elsewhere on the web. The documentation is built with [Sphinx](https://www.sphinx-doc.org/){% if cookiecutter.markdown_docs == 'y' %} from [MyST Markdown](https://myst-parser.readthedocs.io/) sources (`.md`){% else %} from [reStructuredText](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html) sources (`.rst`){% endif %}. Both prose and docstrings may include [math in LaTeX syntax](https://www.sphinx-doc.org/en/master/usage/extensions/math.html). Aim to structure the documentation along the [four Diátaxis categories](https://diataxis.fr): tutorials, how-to guides, reference/API, and explanations.

Every public function or class needs a [docstring](https://peps.python.org/pep-0257/), and every public name must be listed in its module's `__all__` (or in `__private__`), because the API page is generated automatically from `__all__`.
{% if cookiecutter.markdown_docs == 'y' %}The API page is built by [sphinx-autodoc2](https://sphinx-autodoc2.readthedocs.io/).
{% if cookiecutter.markdown_docstrings == 'y' %}Write docstrings in MyST Markdown, matching the prose sources.{% else %}Write docstrings in plain reStructuredText, using field lists (`:param:`, `:returns:`, `:rtype:`) to document arguments and return values. Note that Napoleon/Google-style sections are *not* available on this path.{% endif %}{% else %}The API page is built with `sphinx.ext.autodoc`/`autosummary`. Write docstrings in the ["Google style"](https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html) supported by the [Napoleon extension](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html).{% endif %}

Document module variables and class attributes with an inline docstring immediately after the definition. Describe instance attributes and `__init__` arguments in the class docstring; the `__init__` method itself should have no docstring.

Build the documentation locally with

~~~ console
make docs
~~~
{% endif %}
Changelog
---------

User-facing changes are tracked in [`CHANGELOG.md`]({{ github_project_root }}/blob/{{ cookiecutter.main_branch }}/CHANGELOG.md), which follows the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format. Whenever you make a user-facing change — in a pull request or a direct commit, add a bullet under the `## [Unreleased]` heading at the top of the file, with an inline category prefix (`Added:`, `Changed:`, `Deprecated:`, `Removed:`, `Fixed:`, or `Security:`):

~~~ markdown
## [Unreleased]

* Added: `frobnicate` function [[#12]]
* Fixed: crash when reading an empty input file [[#15], [#16]]
~~~

Link the relevant issue and pull request with a reference-style label `[[#N]]` (listing the issue before the pull request that closes it). You only need to write the `[[#N]]` marker in the bullet; run `make changelog` to fill in the matching link definition at the bottom of the file (it queries the GitHub API to record whether `#N` is an issue or a pull request, so it needs network access). Skip changelog entries for changes that are not user-facing: CI, dependency bumps, formatting, typo fixes, and internal-only refactoring (a leading underscore, e.g. `_helper`, marks a name as internal).

Validate the file with:

~~~ console
make check-changelog   # verify every reference has a link definition (no network)
make changelog         # additionally add any missing [#N] link definitions
~~~

`make check-changelog` runs as part of `make lint` and in CI. It is purely textual and makes no network calls; it does not verify that the links actually resolve or that the issue-vs-pull-request category is correct, so double-check those manually.

{% if cookiecutter.on_pypi == 'y' %}You never edit the release headings or version links by hand: `make release` transforms the changelog automatically. For the release commit it renames `## [Unreleased]` to `## [vX.Y.Z] - YYYY-MM-DD` and updates the version links at the bottom (pointing `[Unreleased]` at `…/compare/vX.Y.Z..HEAD` and adding `[vX.Y.Z]: …/releases/tag/vX.Y.Z`), opening the file in your editor first so you can review and refine the release notes. The tagged release commit therefore contains no `## [Unreleased]` section; a fresh empty one is added back in the immediately following `+dev` version-bump commit that opens the next development cycle. The signed git tag and the GitHub release for the version reuse that section's notes verbatim, so the release notes never have to be retyped.{% else %}When cutting a release, rename `## [Unreleased]` to `## [vX.Y.Z] - YYYY-MM-DD` and update the version links at the bottom of the file (point `[Unreleased]` at `…/compare/vX.Y.Z..HEAD` and add `[vX.Y.Z]: …/releases/tag/vX.Y.Z`). The tagged release commit should contain no `## [Unreleased]` section; add a fresh empty one back in the commit that opens the next development cycle.{% endif %}

Versioning
----------

Releases follow [Semantic Versioning](https://semver.org) and version numbers must be compatible with [PEP 440](https://peps.python.org/pep-0440/): `major.minor.patch`, e.g. `0.1.0` for the first release and `1.0.0` for the first *stable* release. Pre-releases (`1.0.0-rc1`, `1.0.0-dev1`) and, sparingly, post-releases for metadata/documentation fixes (`1.0.0.post1`) are permitted.

The current version is exposed as the `__version__` attribute of the `{{ cookiecutter.project_slug }}` package. Between releases, `__version__` on `{{ cookiecutter.main_branch }}` carries a `+dev` local-version suffix (["local version identifier"](https://peps.python.org/pep-0440/#local-version-identifiers)){% if cookiecutter.on_pypi == 'y' %}; this suffix must never appear in a release published to [PyPI](https://pypi.org){% endif %}.

{% if cookiecutter.on_pypi == 'y' %}Cut a release with

~~~ shell
make release
~~~

which applies the conventions above automatically. Releases are tagged in git using the version string prefixed with "v" (e.g. `v1.0.0`), which publishes them at <{{ github_project_root }}/releases>.{% else %}Tag releases in git using the version string prefixed with "v" (e.g. `v1.0.0`), which publishes them at <{{ github_project_root }}/releases>.{% endif %}
