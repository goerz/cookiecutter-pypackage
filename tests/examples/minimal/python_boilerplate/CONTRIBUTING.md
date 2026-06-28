Contributing
============


Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.

Code of Conduct
---------------

Everyone interacting in the Python Boilerplate project's code base, issue tracker, and any communication channels is expected to follow the [PyPA Code of Conduct](https://www.pypa.io/en/latest/code-of-conduct/).

Report Bugs and Submit Feedback
-------------------------------

Report bugs and propose features by filing an issue at <https://github.com/goerz/python_boilerplate/issues>.

When reporting a bug, please include:

-   Your operating system name and version.
-   Any details about your local setup that might be helpful in troubleshooting.
-   Detailed steps to reproduce the bug, ideally a minimal but complete script or notebook.
-   All error messages in full, as plain text. If the output is long, attach it as a file.

When proposing a feature, explain how it would work and keep the scope as narrow as possible. Remember that this is a volunteer-driven project.

Get Started!
------------

The project uses [uv](https://docs.astral.sh/uv/) to manage the development environment and [`make`](https://www.gnu.org/software/make/) as a task runner. uv downloads and manages the required Python interpreters for you, so these two tools are all you need to install.

Follow [Aaron Meurer's Git Workflow Notes](https://www.asmeurer.com/git-workflow/) (with `goerz/python_boilerplate` instead of `sympy/sympy`). In short:

1.  Fork the repo on GitHub to your personal account and add your fork as a remote.
2.  Pull in the latest changes from the `master` branch.
3.  Create a topic branch, make your changes, and commit them (testing locally).
4.  Push the topic branch to *your* fork and open a pull request against the base `master` branch.

In your checkout, run `make develop` to create a virtual environment with all development dependencies and an editable install of the package. Run `make help` to see all available targets.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1.  The pull request should include tests.
2.  If the pull request adds functionality, the docs should be updated.
3.  Check <https://github.com/goerz/python_boilerplate/actions> and make sure that the tests pass for all supported Python versions.

Branching Model
---------------

For developers with direct access to the repository, Python Boilerplate uses a simple branching model where all development happens directly on the `master` branch. Releases are tags on `master`. Every commit on `master` *should* pass all tests and be well-documented, so that `git bisect` remains effective.

For any non-trivial issue, work on a topic branch instead. To create one that addresses issue #1:

~~~ shell
git checkout -b 1-title-of-issue
git push -u origin 1-title-of-issue
~~~

Commit early and often on topic branches; they carry no restrictions and you are welcome to rewrite history by force-pushing. Before merging, clean up the commit history:

-   Use `git commit --amend` to fold work into your previous commit and to fix commit messages. This is the ideal way to make frequent snapshots without leaving behind meaningless commits like "fix typos".
-   Squash related commits together, e.g. `git rebase -i HEAD~4`. See the ["Rewriting History" chapter of Pro Git](https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History).
-   The `--fixup` flag for `git commit` marks a commit to be squashed into an earlier one with `git rebase --autosquash`.
-   If significant work lands on `master` while you work, periodically rebase onto it (`git rebase master`) rather than merging it in. See [Merging vs. Rebasing](https://www.atlassian.com/git/tutorials/merging-vs-rebasing).

If you collaborate with others on a topic branch, coordinate before rewriting history.

When the issue is fixed, merge the topic branch back with an explicit merge commit and delete it:

~~~ shell
git checkout master
git merge --no-ff 1-title-of-issue
git push origin master
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

Python Boilerplate includes a full test suite using [pytest](https://docs.pytest.org/en/latest/). We strive for a [test coverage](https://codecov.io/gh/goerz/python_boilerplate) above 90%.

From a checkout of the repository, run

~~~ console
make test
~~~

to run the entire suite. By default, uv selects the highest supported Python; use e.g. `make PYTHON=3.13 test` to run on a specific interpreter, or `make test-lowest` to test against the lowest supported Python and dependency versions.

Tests live in the `tests` subfolder, in files named `test_*.py` containing functions named `test_*`. In addition, [doctests](https://docs.python.org/3/library/doctest.html) in docstrings and in the documentation source files are collected and run.

Code Style
----------

All code must be compatible with [PEP 8](https://peps.python.org/pep-0008/), with a line length limit of 79 characters (exceptions are permissible where they significantly improve readability). Beyond that, the project uses the [Black code style](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html) and sorts imports with [isort](https://pycqa.github.io/isort/) per the configuration in `pyproject.toml`.

-   `make black` / `make isort` reformat the code in place; `make black-check` / `make isort-check` only report deviations.
-   The style is enforced by the test suite and by [pre-commit](https://pre-commit.com) git hooks that block non-conforming commits. Install them with `make pre-commit`.
-   `make flake8` and `make pylint` provide additional, non-mandatory guidance on possible improvements.

Changelog
---------

User-facing changes are tracked in [`CHANGELOG.md`](https://github.com/goerz/python_boilerplate/blob/master/CHANGELOG.md), which follows the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format. Whenever you make a user-facing change — in a pull request or a direct commit, add a bullet under the `## [Unreleased]` heading at the top of the file, with an inline category prefix (`Added:`, `Changed:`, `Deprecated:`, `Removed:`, `Fixed:`, or `Security:`):

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

When cutting a release, rename `## [Unreleased]` to `## [vX.Y.Z] - YYYY-MM-DD` and update the version links at the bottom of the file (point `[Unreleased]` at `…/compare/vX.Y.Z..HEAD` and add `[vX.Y.Z]: …/releases/tag/vX.Y.Z`). The tagged release commit should contain no `## [Unreleased]` section; add a fresh empty one back in the commit that opens the next development cycle.

Versioning
----------

Releases follow [Semantic Versioning](https://semver.org) and version numbers must be compatible with [PEP 440](https://peps.python.org/pep-0440/): `major.minor.patch`, e.g. `0.1.0` for the first release and `1.0.0` for the first *stable* release. Pre-releases (`1.0.0-rc1`, `1.0.0-dev1`) and, sparingly, post-releases for metadata/documentation fixes (`1.0.0.post1`) are permitted.

The current version is exposed as the `__version__` attribute of the `python_boilerplate` package. Between releases, `__version__` on `master` carries a `+dev` local-version suffix (["local version identifier"](https://peps.python.org/pep-0440/#local-version-identifiers)).

Tag releases in git using the version string prefixed with "v" (e.g. `v1.0.0`), which publishes them at <https://github.com/goerz/python_boilerplate/releases>.
