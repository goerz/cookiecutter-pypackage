cookiecutter-pypackage
======================

[![Tests](https://github.com/goerz/cookiecutter-pypackage/workflows/Tests/badge.svg)](https://github.com/goerz/cookiecutter-pypackage/actions?query=workflow%3ATests)

A [cookiecutter][] template for a Python 3 package.

[cookiecutter]: https://github.com/audreyr/cookiecutter


Features
--------


* Python 3 only.
* The actual package code is in a `src` directory. See <https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure> for the reasoning behind this.
* Testing with [pytest](https://docs.pytest.org)
* Use [tox](https://tox.readthedocs.io/) for development tasks and for testing against multiple versions of Python
* Makefile wrapping around `tox` for convenience on Unix. Run `make help` inside the generated project for details.
* Keep imports sorted with [`isort`](https://github.com/timothycrosley/isort#readme)
* [Black code style](https://github.com/ambv/black#readme)
* Enforce code style with [pre-commit](https://pre-commit.com) git hooks
* Testing on [Github Actions][]
* Use [Codecov](http://codecov.io) for coverage tracking
* Optional Sphinx documentation, built and deployed by [Github Actions][] to [Github Pages][]
* Optional use of the [better_apidoc](https://github.com/goerz/better-apidoc) tool for generating API documentation with templates.
* Versions menu in online documentation with [Doctr Versions Menu][]
* Upload to [PyPI](https://pypi.org) through `make release`
* Github templates for bug reports
* Interactive post-setup script for initializing git

This template does not support hosting the documentation on [ReadTheDocs](https://readthedocs.org) (RTD), despite the immense popularity of that service. I find that RTD has quite a few hoops to jump to get all but the most straightforward documentations to build. On top of that, I find the injections of advertisements into the documentation ([ethical](https://docs.readthedocs.io/en/stable/advertising/ethical-advertising.html) or not) completely unacceptable. Both of these problems are easily solved by hosting the documentation on [Github Pages][], and the "extra features" of RTD (the version menu) is supplied by [Doctr Versions Menu][].

[Github Actions]: https://github.com/features/actions
[Github Pages]: https://pages.github.com
[Doctr Versions Menu]: https://github.com/goerz/doctr_versions_menu


Usage
-----

First, make sure to have `cookiecutter` installed:

    pip install cookiecutter

Then, create a new project with

    cookiecutter gh:goerz/cookiecutter-pypackage

Follow the prompts. You can also pass values for variables on the command line, e.g.

    cookiecutter gh:goerz/cookiecutter-pypackage  --no-input interactive_postsetup=no project_name="My Project"


Variables
---------

* `full_name`: Full author name, will show up in README, in the module, and on PyPI
* `email` Author email address
* `github_username` Username (or organization name) on github
* `project_name`: The name of the package on PyPI, also the name of the folder that will be generated
* `project_slug`: The name of the repository as it appears in Github URLs
* `project_short_description`: (Short) description to appear as the doc-string of the module, in the documentation of the console script, in the README, and on PyPI
* `version`: Initial version of the package
* `open_source_license`: The license under which the code will be available .
* `linelength`: The allowed line length of code lines (for `black` formatting). PEP 8 requires 79 characters. This is not a hard limit; code may extend beyond the `linelength` if this increases readability.
* `on_pypi`: Whether the package will be uploaded to the Python Package Index
* `sphinx_docs`: Whether the package will use Sphinx to generate its documentation
* `better_apidoc`: Whether to use <https://github.com/goerz/better-apidoc> for generating the package API for Sphinx.
* `support_py36`: Does the package support Python 3.6?
* `support_py37`: Does the package support Python 3.7?
* `support_py38`: Does the package support Python 3.8?
* `support_py39`: Does the package support Python 3.9?
* `main_python`: The version of Python to use for development tasks like building the documentation
* `main_branch`: The name of the main development branch
* `interactive_postsetup`: Whether to run the interactive post-setup script, which will e.g. set up git for the project


Post-Setup
----------

After you generate a new project from the cookiecutter template, you should do the following:

*   Declare dependencies in `setup.py`, both for installation and development (testing).  There are no additional [pip requirement files](https://pip.pypa.io/en/stable/user_guide/#requirements-files) (These are for app deployment, not for packages!).

*   If you didn't do so during project creation, initialize git and push the project to Github

*   Create a `gh-pages` branch and push it to Github.

*   If using better-apidoc, review the custom RTD templates in `docs/_templates`.

*   Review the classifiers in `setup.py`. The full list of PyPI classifiers can be found [here](https://pypi.python.org/pypi?:action=list_classifiers).

*   If the package should be registered on PyPI, upload it. You can do this with `make release`.

*   Make sure to tag releases on Github (using a leading `v` in the tag name, e.g. `v0.1.0`)

*   Activate branch protection for the main branch, to prohibit history rewriting.

The [Wiki][] describes additional best practices.

[Wiki]: https://github.com/goerz/cookiecutter-pypackage/wiki
