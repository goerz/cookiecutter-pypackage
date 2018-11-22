cookiecutter-pypackage3
=======================

A [cookiecutter][] template for a Python 3 package.

[cookiecutter]: https://github.com/audreyr/cookiecutter


Features
--------


* Python 3 only. Although it would be straightforward to also add Python 2 support to your package by hand.
* The actual package code is in a `src` directory. See <https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure> for the reasoning behind this.
* [Travis CI](https://travis-ci.org) and [AppVeyor](http://appveyor.com) support.
* Sphinx/Read-the-docs support. This includes optional use of the [better_apidoc](https://github.com/goerz/better-apidoc) tool for generating API documentation with templates.
* Support for Jupyter Notebooks in the Sphinx documentation ([nbsphinx](https://nbsphinx.readthedocs.io/en/latest/)). This includes validation of notebooks as tests through the [nbval plugin](https://nbval.readthedocs.io/en/latest/).
* Mandatory testing with [pytest](https://docs.pytest.org)
* Environment management through [`conda`](https://conda.io/docs/)
* Development tasks are organized in a Makefile. Run `make help` inside the generated project for details.
* Support for [Coveralls](http://coveralls.io)
* Upload to [PyPI](https://pypi.org) through `make release`
* Github templates for bug reports
* Support for git-flow branching model
* Interactive post-setup script for initializing git


Usage
-----

First, make sure to have `cookiecutter` installed:

    pip install cookiecutter

Then, create a new project with

    cookiecutter gh:goerz/cookiecutter-pypackage3

Follow the prompts.


Variables
---------

* `full_name`: Full author name, will show up in README, in the module, and on PyPI
* `email` Author email address
* `github_username` Username on github
* `project_name`: The name of the package on PyPI, also the name of the folder that will be generated
* `project_short_description`: (Short) description to appear as the doc-string of the module, in the documentation of the console script, in the README, and on PyPI
* `version`: Initial version of the package
* `create_author_file`: Whether to create AUTHORS.rst
* `open_source_license`: The license under which the code will be available (choice of MIT, GPL, or Public Domain)
* `environment_manager`: The system for managing virtual environments. Currently, only `conda` is supported.
* `conda_packages`: If using `conda` as an environment manager, which packages to install from the conda repository (i.e., not through pip). If you package extensively uses the Python scientific stack, and virtual environments are managed through conda, you might consider using the anaconda meta package, and set `anaconda pytest-cov pytest-xdist coverage sphinx_rtd_theme flake8`.
* `on_pypi`: Whether the package will be uploaded to the Python Package Index
* `travisci`: Whether Travis will be used as a Continuous Integration testing service
* `appveyor`: Whether AppVeyor will be used as a Continuous Integration testing service for Windows
* `coveralls`: Whether to upload coverage data to <http://coveralls.io>. This only work if `travisci` is used.
* `sphinx_docs`: Whether the package will use Sphinx to generate its documentation
* `use_notebooks`: Whether Jupyter notebooks will be included in the Sphinx documentation, and validated through pytest. This is not compatible with `support_py34`.
* `better_apidoc`: Whether to use <https://github.com/goerz/better-apidoc> for generating the package API for Sphinx.
* `readthedocs`: Whether the Sphinx-documentation will be hosted on <https://readthedocs.org>
* `support_py34`: Does the package support Python 3.4?
* `support_py35`: Does the package support Python 3.5?
* `support_py36`: Does the package support Python 3.6?
* `support_py36`: Does the package support Python 3.7? Remember to check any conda-forge packages that you might depend on to support Python 3.7 before enabling this.
* `use_git_flow`: Whether the project uses the [git-flow branching model](https://github.com/nvie/gitflow#git-flow)
* `interactive_postsetup`: Whether to run the interactive post-setup script, which will e.g. set up git for the project


Post-Setup
----------

After you generate a new project from the cookiecutter template, you should do the following:

*   Declare dependencies in `setup.py`, both for installation and development (testing).  There are no additional [pip requirement files](https://pip.pypa.io/en/stable/user_guide/#requirements-files) (I find them unnecessary).

*   If you are using `conda` as an `environment_manager`, you may list any dependency that you know has a conda package in `CONDA_PACKAGES` in `Makefile`. Also, if you are using Travis CI (`use_travis`), you should add the same packages in the `install` section of `.travis.yml`. Any dependencies not installed as conda packages will still automatically be installed via `pip`, so the use of conda packages is optional. However, if you do use conda packages, you must manually ensure that the list of conda packages in the various locations (`Makefile`, `.travis.yml`) stays in sync. Note that conda can be extremely slow, so it recommended to only install the base Python via conda, and other dependencies via pip, if possible.

*   If you are using ReadTheDocs (RTD) with conda to host your documentation, you will have to specify the build environment for the documentation in `docs/rtd_environment.yml`.  Packages that are available through conda can be listed directly, other packages must be listed in a pip section. For example,

        channels:
          - defaults
        dependencies:
          - python=3.6
          - anaconda
          - pip:
              - better-apidoc
              - trajectorydata
              - git+https://github.com/mabuchilab/QNET.git@develop#egg=QNET-2.0.0-dev

    In general, RTD needs only a minimal number of dependencies (*not* everything required to run the tests). Specifically, you must not include any `sphinx-*` dependencies in `docs/rtd_environment.yml` -- these are installed automatically by the RTD build process. RTD will not take into account dependencies listed in `setup.py`

*   Review the custom RTD templates in `docs/_templates`

*   If you didn't do so during project creation, initialize git and push the project to Github

*   If you are using the git-flow branching model, you *must* configure this on Github. Go to the "Settings" for the project, then "Branches", and switch the "Default branch" from "master", to "develop". You may consider protecting the master branch.

*   Activate Travis CI. The easiest way to do this is to click on the `build|unknown` badge in the README on Github

*   Activate AppVeyor. The easiest way to do this is to click on the `appveyor|no id` badge in the README on Github. You must update the badge svg in `README.rst` and `docs/index.rst`.

*   Activate ReadTheDocs. Log in to <https://readthedocs.org/dashboard/>, and click the "Import a Project" button. You shouldn't have to do any configuration, as everything is set up through the `readthedocs.yml` and `docs/rtd_environment.yml` files.

*   Activate Coveralls. Log in to <https://coveralls.io>, and click on "Add Repo". Not that coverage data is only uploaded if all tests pass successfully!

*   Review the classifiers in `setup.py`. The full list of PyPI classifiers can be found [here](https://pypi.python.org/pypi?:action=list_classifiers).

*   If the package should be registered on PyPI, upload it. You can do this with `make release`. It is *strongly* recommended that you first try `make test-release` to upload the package to `test.pypi.org`.

*   Make sure to tag releases on Github
