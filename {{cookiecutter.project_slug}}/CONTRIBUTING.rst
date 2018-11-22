.. highlight:: shell

{%if cookiecutter.support_py36 == 'y' %}
  {%- set latest_venv = '.venv/py36' -%}
  {%- set latest_test_target = 'test36' -%}
{% elif cookiecutter.support_py35 == 'y' %}
  {%- set latest_venv = '.venv/py35' -%}
  {%- set latest_test_target = 'test35' -%}
{% else %}
  {%- set latest_venv = '.venv/py34' -%}
  {%- set latest_test_target = 'test34' -%}
{% endif -%}

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

Report Bugs
-----------

Report bugs at https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.


Submit Feedback
---------------

The best way to send feedback is to file an issue at https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)


Fix Bugs / Implement Features
-----------------------------

Look through the GitHub issues for bugs or feature requests. Anybody is welcome to submit a pull request for open issues.


Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
{%- if cookiecutter.travisci == 'y' %}
3. Check https://travis-ci.org/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/pull_requests
   and make sure that the tests pass for all supported Python versions.
{%endif %}


Get Started!
------------

Ready to contribute? Follow `Aaron Meurer's Git Workflow Notes`_ (with ``{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}`` instead of ``sympy/sympy``)

In short,

1. Clone the repository from ``git@github.com:{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.git``
2. Fork the repo on GitHub to your personal account.
3. Add your fork as a remote.
4. Pull in the latest changes from the {% if cookiecutter.use_git_flow == 'y' %}develop{% else %}master{% endif %} branch.
5. Create a topic branch
6. Make your changes and commit them (testing locally)
7. Push changes to the topic branch on *your* remote
8. Make a pull request against the base {% if cookiecutter.use_git_flow == 'y' %}develop{% else %}master{% endif %} branch through the Github website of your fork.

The project contains a ``Makefile`` to help with development tasts. In your checked-out clone, do

.. code-block:: console

    $ make help

to see the available make targets.

{% if cookiecutter.environment_manager == 'conda' %}
It is strongly recommended that you use the conda_ package manager. The
``Makefile`` relies on conda to create local testing and documentation building
environements (``make test`` and ``make docs``).

Alternatively, you may  use ``make develop-test`` and ``make develop-docs`` to
run the tests or generate the documentation within your active Python
environment. You will have to ensure that all the necessary dependencies are
installed. Also, you will not be able to test the package against all supported
Python versions.

{%- if cookiecutter.travisci == 'y' %}
You still can (and should) look at https://travis-ci.org/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/ to check that your commits pass all tests.
{%endif %}

.. _conda: https://conda.io/docs/
{%endif %}

{% if cookiecutter.use_git_flow == 'y' %}
Branching Model
---------------

{{ cookiecutter.project_name }} uses the `git-flow`_ branching model. That is, the ``develop`` branch takes the role of ``master`` in the `Git Workflow Notes`_.

In order to create topic branches with ``git flow``, after cloning the  ``{{ cookiecutter.project_slug }}`` repository, you should initialize it as follows:

.. code-block:: console

    $ git checkout master
    $ git flow init
    $ git checkout develop

.. _git-flow: https://github.com/nvie/gitflow#git-flow
.. _Git Workflow Notes: https://www.asmeurer.com/git-workflow/
{% endif -%}
.. _Aaron Meurer's Git Workflow Notes:  https://www.asmeurer.com/git-workflow/

Testing
-------

{{ cookiecutter.project_name }} includes a full test-suite using pytest_.
{%- if cookiecutter.coveralls == 'y' %}
We strive for a `test coverage`_ above 90%.
{%endif %}

From a checkout of the ``{{ cookiecutter.project_slug }}`` repository {%- if cookiecutter.environment_manager == 'conda' -%}, assuming conda_ is installed,{%endif %} you can use

.. code-block:: console

    $ make test

to run the entire test suite.

The tests are organized in the ``tests`` subfolder. It includes python scripts
whose name start with ``test_``, which contain functions whose names also start
with ``test_``. Any such functions in any such files are picked up by `pytest`_
for testing. In addition, doctests_ from any docstring or any documentation
file (``*.rst``) are picked up (by the `pytest doctest plugin`_).

{% if cookiecutter.coveralls == 'y' %}
.. _test coverage: https://coveralls.io/github/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}?branch={%- if cookiecutter.use_git_flow == 'y' -%}develop{%- else -%}master{%- endif -%}
{%endif%}
.. _pytest: https://docs.pytest.org/en/latest/
.. _doctests: https://docs.python.org/3.7/library/doctest.html
.. _pytest doctest plugin: https://docs.pytest.org/en/latest/doctest.html
.. _nbval plugin: https://nbval.readthedocs.io/en/latest/


{%- if cookiecutter.sphinx_docs == 'y' %}
.. _write-documentation:

Write Documentation
-------------------

{{ cookiecutter.project_name }} could always use more documentation, whether
as part of the official docs, in docstrings, or even on the web in blog posts,
articles, and such.

The package documentation is generated with Sphinx_, the
documentation (and docstrings) are formatted using the
`Restructured Text markup language`_ (file extension ``rst``).
See also the `Matplotlib Sphinx Sheet sheet`_ for some helpful tips.

Each function or class must have a docstring_; this docstring must
be written in the `"Google Style" format`_ (as implemented by
Sphinx' `napoleon extension`_).

At any point, from a checkout of the ``{{ cookiecutter.project_slug }}`` repository (and
assuming you have conda_ installed), you may run

.. code-block:: console

    $ make docs

to generate the documentation locally.

.. _Sphinx: http://www.sphinx-doc.org/en/master/
.. _Restructured Text markup language: http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
.. _docstring: https://www.python.org/dev/peps/pep-0257/
.. _"Google Style" format: http://www.sphinx-doc.org/en/master/usage/extensions/example_google.html#example-google
.. _napoleon extension: http://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
.. _mathematical formulas in LaTeX syntax: http://www.sphinx-doc.org/en/1.6/ext/math.html
.. _mathjax: http://www.sphinx-doc.org/en/master/usage/extensions/math.html#module-sphinx.ext.mathjax
.. _BibTeX: https://sphinxcontrib-bibtex.readthedocs.io/en/latest/
.. _Matplotlib Sphinx Sheet sheet: https://matplotlib.org/sampledoc/cheatsheet.html
{% endif %}


Developers' How-Tos
-------------------

The following assumes your current working directory is a checkout of
``{{ cookiecutter.project_slug }}``, and that you have successfully run ``make test`` (which creates
some local virtual environments that development relies on).

.. _how-to-work-on-a-topic-branch:

How to work on a topic branch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When working on an non-trivial issue, it is recommended to create a topic
branch, instead of pushing to ``master``.

To create a branch named ``issue18``::

    $ git branch issue18
    $ git checkout issue18

You can then make commits, and push them to Github to trigger Continuous Integration testing::

    $ git push origin issue18

It is ok to force-push on an issue branch

When you are done (the issue has been fixed), finish up by merging the topic
branch back into ``master``::

    $ git checkout master
    $ git merge --no-ff issue18

The ``--no-ff`` option is critical, so that an explicit merge commit is created.
Summarize the changes of the branch relative to ``master`` in the commit
message.

Then, you can push master and delete the topic branch both locally and on Github::

    $ git push origin master
    $ git push --delete origin issue18
    $ git branch -D issue18


Commit Message Guidelines
~~~~~~~~~~~~~~~~~~~~~~~~~

Write commit messages according to this template::

    Short (50 chars or less) summary

    More detailed explanatory text. Wrap it to 72 characters. The blank
    line separating the summary from the body is critical (unless you omit
    the body entirely).

    Write your commit message in the imperative: "Fix bug" and not "Fixed
    bug" or "Fixes bug." This convention matches up with commit messages
    generated by commands like git merge and git revert.

    Further paragraphs come after blank lines.

    - Bullet points are okay, too.
    - Typically a hyphen or asterisk is used for the bullet, followed by a
      single space. Use a hanging indent.

A properly formed git commit subject line should always be able to complete the
sentence "If applied, this commit will <your subject line here>".


How to reference a Github issue in a commit message
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Simply put e.g. ``#14`` anywhere in your commit message, and Github will
automatically link to your commit on the page for issue number 14.

You may also use something like ``Closes #14`` as the last line of your
commit message to automatically close the issue.
See `Closing issues using keywords`_ for details.

How to run a subset of tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To run e.g. only the tests defined in ``tests/test_{{ cookiecutter.project_slug }}.py``, use::

    $ ./.venv/py36/bin/pytest tests/test_{{ cookiecutter.project_slug }}.py

See the `pytest test selection docs`_ for details.

How to run only as single test
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Decorate the test with e.g. ``@pytest.mark.xxx``, and then run, e.g::

    $ ./{{ latest_venv }}/bin/pytest -m xxx tests/

See the `pytest documentation on markers`_ for details.

How to run only the doctests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run the following::

$ ./{{ latest_venv }}/bin/pytest --doctest-modules src

How to go into an interactive debugger
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Optionally, install the `pdbpp` package into the testing environment, for a
better experience::

    $ ./{{ latest_venv }}/bin/python -m pip install pdbpp

Then:

- before the line where you went to enter the debugger, insert a line::

    from IPython.terminal.debugger import set_trace; set_trace() # DEBUG

- Run ``pytest`` with the option ``-s``, e.g.::

    $ ./{{ latest_venv }}/bin/pytest -m xxx -s tests/

You may also see the `pytest documentation on automatic debugging`_.

.. _Jupyter’s Common Configuration system: https://jupyter-notebook.readthedocs.io/en/stable/config_overview.html#jupyter-s-common-configuration-system
.. _Closing issues using keywords: https://help.github.com/articles/closing-issues-using-keywords/
.. _pytest test selection docs: https://docs.pytest.org/en/latest/usage.html#specifying-tests-selecting-tests
.. _pytest documentation on markers: https://docs.pytest.org/en/latest/example/markers.html
.. _pytest documentation on automatic debugging: https://docs.pytest.org/en/latest/usage.html#dropping-to-pdb-python-debugger-on-failures
.. _test-driven development: https://en.wikipedia.org/wiki/Test-driven_development
.. _pytest documentation on skip and xfail: https://docs.pytest.org/en/latest/skipping.html
.. _documentation of the nbval pluging on skipping and exceptions: https://nbval.readthedocs.io/en/latest/#Skipping-specific-cells
