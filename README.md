cookiecutter-pypackage
======================

[![Build Status](https://travis-ci.org/goerz/cookiecutter-pypackage.svg?branch=master)](https://travis-ci.org/goerz/cookiecutter-pypackage)

A [cookiecutter][] template for a Python 3 package, with a special focus on scientific computing.

[cookiecutter]: https://github.com/audreyr/cookiecutter


Features
--------


* Python 3 only.
* The actual package code is in a `src` directory. See <https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure> for the reasoning behind this.
* Support for [`isort`](https://github.com/timothycrosley/isort#readme)
* Support for [Black code style](https://github.com/ambv/black#readme)
* Support for [pre-commit](https://pre-commit.com) git hooks
* [Travis CI](https://travis-ci.org) and [AppVeyor](http://appveyor.com) support.
* Sphinx/Read-the-docs support. This includes optional use of the [better_apidoc](https://github.com/goerz/better-apidoc) tool for generating API documentation with templates.
* Support for Jupyter Notebooks in the Sphinx documentation ([nbsphinx](https://nbsphinx.readthedocs.io/en/latest/)). This includes validation of notebooks as tests through the [nbval plugin](https://nbval.readthedocs.io/en/latest/).
* Mandatory testing with [pytest](https://docs.pytest.org)
* Use [tox](https://tox.readthedocs.io/) for development tasks and for testing against multiple versions of Python
* Makefile wrapping around `tox` for convenience on Unix. Run `make help` inside the generated project for details.
* Support for [Coveralls](http://coveralls.io) and [Codecov](http://codecov.io)
* Upload to [PyPI](https://pypi.org) through `make release`
* Documentation hosting on [ReadTheDocs](https://readthedocs.org) (not recommended due to advertising) and [Doctr](https://drdoctr.github.io)
* "Versions menu" in Doctr-generated documentation, with downloadable documentation artifacts (zip/pdf/epub) hosted on Github or [Bintray](http://bintray.com)
* Github templates for bug reports
* Optional support for git-flow branching model
* Interactive post-setup script for initializing git


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
* `create_author_file`: Whether to create AUTHORS.rst
* `open_source_license`: The license under which the code will be available .
* `use_isort`: Whether to require that all imports are sorted according to the `isort` utility
* `use_black`: Whether the [black code formatter](https://github.com/ambv/black) should be used to enforce code styles. This enables `make black`, `make black-check`, and the underlying tox environments, as well as automatic checking of the code style on Travis.
* `use_pre_commit`: Whether to use [pre-commit](https://pre-commit.com) to manage git pre-commit hooks. A local hook for checking for trailing whitespace and DEBUG lines is always included, as well as third-party hooks for `isort` and `black` if `use_isort` and `use_black` are True.
* `linelength`: The allowed line length of code lines (for `black` formatting). PEP 8 requires 79 characters. This is not a hard limit; code may extend beyond the `linelength` if this increases readability.
* `allow_single_quote_strings`: Whether strings are allowed to be enclosed in single quotes, cf. `-S` option of `black`.
* `on_pypi`: Whether the package will be uploaded to the Python Package Index
* `travisci`: Whether Travis will be used as a Continuous Integration testing service
* `travis_texlive`: Whether texlive should be installed on Travis. This may be required for building the documentation. Required for downloadable PDF documentation through Doctr.
* `appveyor`: Whether AppVeyor will be used as a Continuous Integration testing service for Windows
* `appveyor_username`: Username on AppVeyor
* `coverage`: Which service to use for keeping track of code coverage
* `sphinx_docs`: Whether the package will use Sphinx to generate its documentation
* `use_notebooks`: Whether Jupyter notebooks will be included in the Sphinx documentation, and validated through `pytest`.
* `better_apidoc`: Whether to use <https://github.com/goerz/better-apidoc> for generating the package API for Sphinx.
* `docshosting`: Which service to use for hosting the Sphinx-generated documentation. The following choices are available:
    * Doctr: Host documentation on Github pages and use [Doctr](https://drdoctr.github.io) to build it. This gives you full control over the documentation
    * ReadTheDocs: Host documentation on the widely used [ReadTheDocs](https://readthedocs.org) website. This severely limits the documentation build process. Also, ReadTheDocs will inject advertisements into your documentation, which is really unacceptable.
* `doctr_artifact_hosting`: If `docshosting` is "Doctr", which provider to use for binary documentation artifacts (e.g. zipped-html/epub/pdf versions of the documentation linked in the "Download" menu. The following choices are available:
    * bintray: Upload artifacts to https://bintray.com/. Requires a (free) Bintray account, and manual setup of the appropriate organization/repo/package on Bintray. Recommended.
    * gh-releases: The "Releases" tab of the Github project. The only drawback of this is that it requires an OAUTH token for Github, which are notoriously wide in scope. If you choose this, you might as well use the same token for Doctr deployment (instead of the default option of using a more restricted SSH deploy key)
    * gh-pages: artifacts will be kept directly in the Github pages to which Doctr deploys. This may quickly accumulate large amounts of binary data in you git repo and blow up in size. Not recommended.
    * None: do not build any documentation artifacts: you will only have an HTML documentation
* `support_py35`: Does the package support Python 3.5?
* `support_py36`: Does the package support Python 3.6?
* `support_py37`: Does the package support Python 3.7?
* `support_py38`: Does the package support Python 3.8?
* `support_py39`: Does the package support Python 3.9?
* `main_python`: The version of Python to use for development tasks like building the documentation
* `use_git_flow`: Whether the project uses the [git-flow branching model](https://github.com/nvie/gitflow#git-flow)
* `interactive_postsetup`: Whether to run the interactive post-setup script, which will e.g. set up git for the project


Post-Setup
----------

After you generate a new project from the cookiecutter template, you should do the following:

*   Declare dependencies in `setup.py`, both for installation and development (testing).  There are no additional [pip requirement files](https://pip.pypa.io/en/stable/user_guide/#requirements-files) (These are for app deployment, not for packages!).

*   If you didn't do so during project creation, initialize git and push the project to Github

*   Activate ReadTheDocs or Doctr. For ReadTheDocs, log in to <https://readthedocs.org/dashboard/>, and click the "Import a Project" button. You shouldn't have to do any configuration, as everything is set up through the `.readthedocs.yml` file.  For Doctr, if you did not already do so during the interactive post-setup script, run `tox -e run-cmd -- doctr configure --no-upload-key --no-authenticate --key-path docs/doctr_deploy_key` and set the Doctr deploy key in the Github settings according to the instructions printed by `doctr configure`. Update your `.travis.yml` file with the encrypted deploy key, and with any deploy keys required for uploading documentation artifacts (`doctr_artifact_hosting`).

*   If using better-apidoc, review the custom RTD templates in `docs/_templates`.


*   If you are using the git-flow branching model, you *must* configure this on Github. Go to the "Settings" for the project, then "Branches", and switch the "Default branch" from "master", to "develop". You may consider protecting the master branch.

*   Activate Travis CI. The easiest way to do this is to click on the `build|unknown` badge in the README on Github

*   Activate AppVeyor. The easiest way to do this is to click on the `appveyor|no id` badge in the README on Github. You must update the badge svg in `README.rst` and `docs/index.rst`.

*   Activate Coveralls or Codecov. For Coveralls, log in to <https://coveralls.io>, and click on "Add Repo". Not that coverage data is only uploaded if all tests pass successfully!

*   Review the classifiers in `setup.py`. The full list of PyPI classifiers can be found [here](https://pypi.python.org/pypi?:action=list_classifiers).

*   If you are using [pre-commit](https://pre-commit.com), review the `.pre-commit-config.yaml` file, especially for whether you will want to use more recent `rev`s for third-party hooks.

*   If the package should be registered on PyPI, upload it. You can do this with `make release`.

*   Make sure to tag releases on Github (using a leading `v` in the tag name, e.g. `v0.1.0`)

*   Activate branch protection for the `master` branch (and `develop` branch, if using the git flow branching model), to prohibit history rewriting for these branches.
