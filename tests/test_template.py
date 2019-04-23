"""Test the project template

Running the test suite requires Python >= 3.6, although the cookiecutter
template itself also works with older versions of Python 3
"""
import pprint
import re
import subprocess
from pathlib import Path
from textwrap import dedent

import pytest


def make(project, *targets):
    """Run 'make' for the given `targets in the project folder

    Return a subprocess.CompletedProcess instance, with the stdout and stderr
    of the call to ``make`` in the correspdonding attributes.
    """
    cmd = ['make'] + list(targets)
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
        cwd=str(project),
        timeout=600,
        check=False,
        universal_newlines=True,
    )
    if result.returncode != 0:
        print("\n'%s' STDOUT:\n%s" % (" ".join(cmd), result.stdout))
        print("\n'%s' STDERR:\n%s" % (" ".join(cmd), result.stderr))
    return result


def get_files(directory):
    """Return a list of file in the given directory, relative to that
    directory"""
    return list(
        str(p.relative_to(directory))
        for p in Path(directory).glob('**/*')
        if p.is_file()
    )


def files_match_expected(directory, expected):
    """Check the the files in `directory` match the list in `expected`

    The `expected` list should contain file paths relative to `directory`.
    Ordering is irrelevant.
    """
    files = get_files(directory)
    if set(files) != set(expected):
        print("\nFiles in directory %s:" % directory)
        pprint.pprint(files)
        print("\nMissing:")
        pprint.pprint(list(set(expected).difference(files)) or None)
        print("\nUnexpected:")
        pprint.pprint(list(set(files).difference(expected)) or None)
        return False
    else:
        return True


def check_default_files(project):
    """Check the list of files for the default settings

    This check must run before any 'make test' or 'make docs'
    """
    expected_files = [
        '.appveyor.yml',
        '.editorconfig',
        '.github/ISSUE_TEMPLATE.md',
        '.gitignore',
        '.pylintrc',
        '.travis.yml',
        'AUTHORS.rst',
        'CONTRIBUTING.rst',
        'HISTORY.rst',
        'LICENSE',
        'MANIFEST.in',
        'Makefile',
        'README.rst',
        'binder/environment.yml',
        'docs/API/.gitignore',
        'docs/Makefile',
        'docs/_extensions/dollarmath.py',
        'docs/_static/mycss.css',
        'docs/_templates/breadcrumbs.html',
        'docs/_templates/layout.html',
        'docs/_templates/module.rst',
        'docs/_templates/package.rst',
        'docs/authors.rst',
        'docs/conf.py',
        'docs/conftest.py',
        'docs/contributing.rst',
        'docs/history.rst',
        'docs/index.rst',
        'docs/make.bat',
        'docs/nbval_sanitize.cfg',
        'docs/readme.rst',
        'docs/rtd_environment.yml',
        'docs/spelling_wordlist.txt',
        'docs/tutorial.ipynb',
        'pyproject.toml',
        'readthedocs.yml',
        'scripts/release.py',
        'setup.cfg',
        'setup.py',
        'src/conftest.py',
        'src/python_boilerplate/__init__.py',
        'tests/test_python_boilerplate.py',
    ]
    assert files_match_expected(str(project), expected_files)


def check_minimal_files(project):
    """Check the list of files for the minimal settings

    This check must run before any 'make test' or 'make docs'
    """
    expected_files = [
        '.editorconfig',
        '.github/ISSUE_TEMPLATE.md',
        '.gitignore',
        '.pylintrc',
        'CONTRIBUTING.rst',
        'HISTORY.rst',
        'LICENSE',
        'MANIFEST.in',
        'Makefile',
        'README.rst',
        'pyproject.toml',
        'scripts/release.py',
        'setup.cfg',
        'setup.py',
        'src/conftest.py',
        'src/python_boilerplate/__init__.py',
        'tests/test_python_boilerplate.py',
    ]
    assert files_match_expected(str(project), expected_files)


def check_make_test(project):
    """Check that 'make test' exits with no error"""
    res = make(project, 'test')
    assert res.returncode == 0


def check_make_docs(project):
    """Check that 'make docs' exits with no error"""
    res = make(project, 'docs')
    assert res.returncode == 0


def check_default_make_help(project):
    """Check that we have the expected make targets in the default
    configuration"""
    res = make(project, 'help')
    stdout = res.stdout
    # some versions of make print additional information that we need to strip
    stdout = re.sub(r'make.*: Entering directory.*\n', '', stdout)
    stdout = re.sub(r'make.*: Leaving directory.*', '', stdout)
    stdout = stdout.strip()
    expected = dedent(
        r'''
        clean                remove all build, test, coverage, and Python artifacts, as well as environments
        clean-build          remove build artifacts
        clean-pyc            remove Python file artifacts
        clean-test           remove test and coverage artifacts
        clean-venvs          remove testing/build environments
        lint                 check style with flake8
        test                 run tests on every Python version
        docs                 generate Sphinx HTML documentation, including API docs
        spellcheck           check spelling in docs
        black-check          Check all src and test files for compliance to 'black' code style
        black                Apply 'black' code style to all src and test files
        isort-check          Check all src and test files for correctly sorted imports
        isort                Sort imports in all src and test files
        coverage             generate coverage report in ./htmlcov
        test-upload          package and upload a release to test.pypi.org
        upload               package and upload a release to pypi.org
        release              Create a new version, package and upload it
        dist                 builds source and wheel package
        dist-check           Check all dist files for correctness
        install              install the package to the active Python's site-packages
        uninstall            uninstall the package from the active Python's site-packages
        develop              install the package to the active Python's site-packages, in develop mode
        develop-test         run tests within the active Python environment
        develop-docs         generate Sphinx HTML documentation, including API docs, within the active Python environment
        notebooks            re-evaluate the notebooks
        jupyter-notebook     run a notebook server for editing the examples
        jupyter-lab          run a jupyterlab server for editing the examples
        '''
    ).strip()
    assert stdout == expected


def check_minimal_make_help(project):
    """Check that we have the expected make targets in the minimal
    configuration"""
    res = make(project, 'help')
    stdout = res.stdout
    # some versions of make print additional information that we need to strip
    stdout = re.sub(r'make.*: Entering directory.*\n', '', stdout)
    stdout = re.sub(r'make.*: Leaving directory.*', '', stdout)
    stdout = stdout.strip()
    expected = dedent(
        r'''
        clean                remove all build, test, coverage, and Python artifacts, as well as environments
        clean-build          remove build artifacts
        clean-pyc            remove Python file artifacts
        clean-test           remove test and coverage artifacts
        clean-venvs          remove testing/build environments
        lint                 check style with flake8
        test                 run tests on every Python version
        coverage             generate coverage report in ./htmlcov
        test-upload          package and upload a release to test.pypi.org
        dist                 builds source and wheel package
        dist-check           Check all dist files for correctness
        install              install the package to the active Python's site-packages
        uninstall            uninstall the package from the active Python's site-packages
        develop              install the package to the active Python's site-packages, in develop mode
        develop-test         run tests within the active Python environment
        '''
    ).strip()
    assert stdout == expected


def check_black_ok(project):
    """Check that the entire project passes inspection with black"""
    cmd = [
        'black',
        '--skip-string-normalization',
        '--line-length',
        '79',
        '--diff',
        '--check',
        str(project),
    ]
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
        timeout=600,
        check=False,
        universal_newlines=True,
    )
    if result.returncode != 0:
        print("\n'%s' STDOUT:\n%s" % (" ".join(cmd), result.stdout))
        print("\n'%s' STDERR:\n%s" % (" ".join(cmd), result.stderr))
    assert result.returncode == 0


def check_custom_metadata(project):
    """Check that the project was generated with the custom metadata from the
    CONFIGURATION"""
    assert project.join('src', 'mypypackage').isdir()
    with open(project.join('setup.py')) as in_fh:
        setup_py = in_fh.read()
        assert "This project is generated with custom metadata" in setup_py
        assert 'author="The Architect"' in setup_py
        assert "author_email='architect@mail.michaelgoerz.net'" in setup_py
        assert "url='https://github.com/qucontrol/mypypackage'" in setup_py
    with open(project.join('src', 'mypypackage', '__init__.py')) as in_fh:
        init_py = in_fh.read()
        assert "__version__ = '1.0.0-dev'" in init_py
        assert "My-Py-Package" in init_py


def check_only_py34_venv(project):
    """Check that only the .venv/py34 venv-folder exists

    Must follow `check_make_test`.
    """
    assert project.join('.venv', 'py34').isdir()
    assert not project.join('.venv', 'py35').exists()
    assert not project.join('.venv', 'py36').exists()
    assert not project.join('.venv', 'py37').exists()
    assert not project.join('.venv', 'py38').exists()


def check_only_py37_venv(project):
    """Check that only the .venv/py37 venv-folder exists

    Must follow `check_make_test`.
    """
    assert not project.join('.venv', 'py34').isdir()
    assert not project.join('.venv', 'py35').exists()
    assert not project.join('.venv', 'py36').exists()
    assert project.join('.venv', 'py37').exists()
    assert not project.join('.venv', 'py38').exists()


def check_defaults_venvs(project):
    """Check that the .venv folder of the default configuration exist

    Must follow `check_make_test`.
    """
    assert not project.join('.venv', 'py34').isdir()
    assert project.join('.venv', 'py35').exists()
    assert project.join('.venv', 'py36').exists()
    assert project.join('.venv', 'py37').exists()
    assert not project.join('.venv', 'py38').exists()


CONFIGURATIONS = [
    (
        'default',
        {'interactive_postsetup': 'n'},
        [
            check_black_ok,
            check_default_make_help,
            check_default_files,
            check_make_test,
            check_make_docs,
            check_defaults_venvs,
        ],
    ),
    (
        'minimal',
        {
            "create_author_file": "n",
            "use_isort": "n",
            "use_black": "n",
            "on_pypi": "n",
            "travisci": "n",
            "appveyor": "n",
            "coveralls": "n",
            "sphinx_docs": "n",
            "use_notebooks": "n",
            "better_apidoc": "n",
            "readthedocs": "n",
            "support_py34": "n",
            "support_py35": "n",
            "support_py36": "n",
            "support_py37": "y",
            "use_git_flow": "n",
            "interactive_postsetup": "n",
        },
        [
            check_black_ok,
            check_minimal_files,
            check_make_test,
            check_minimal_make_help,
        ],
    ),
    (
        'only_34',
        {
            "support_py34": "y",
            "support_py35": "n",
            "support_py36": "n",
            "support_py37": "n",
            "use_notebooks": "n",
            "interactive_postsetup": 'n',
        },
        [check_make_test, check_make_docs, check_only_py34_venv],
    ),
    (
        'only_latest',
        {
            "support_py34": "n",
            "support_py35": "n",
            "support_py36": "n",
            "support_py37": "y",
            "use_notebooks": "n",
            "interactive_postsetup": 'n',
        },
        [check_make_test, check_make_docs, check_only_py37_venv],
    ),
    (
        'custom_metadata',
        {
            "full_name": "The Architect",
            "email": "architect@mail.michaelgoerz.net",
            "github_username": "qucontrol",
            "project_name": "My-Py-Package",
            "project_slug": "mypypackage",
            "project_short_description": "This project is generated with custom metadata",
            "version": "1.0.0-dev",
            "interactive_postsetup": 'n',
        },
        [check_custom_metadata],
    ),
]


@pytest.mark.parametrize("name,context,checkers", CONFIGURATIONS)
def test_template(cookies, name, context, checkers):
    """Test one element of CONFIGURATION

    Args:
        cookies: Fixture from pytest-cookies
            (https://github.com/hackebrot/pytest-cookies)
        name (str): a string identifer for the configuration
        context (dict): values overriding the defaults in ``cookiecutter.json``
        checkers (list[callable]): list of "checker" routines that will be
            called, each routine gets the :class:`.LocalPath` to the rendered
            project folder as its input
    """
    result = cookies.bake(extra_context=context)
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.isdir()
    print("")
    print("Created %s" % result.project)
    for checker in checkers:
        print("   %s..." % checker.__name__)
        checker(result.project)


def test_no_jupyter_with_py34(cookies):
    """Test that the template won't allow Jupyter notebooks with Python 3.4"""
    context = {
        "support_py34": "y",
        "support_py35": "y",
        "support_py36": "n",
        "support_py37": "n",
        "use_notebooks": "y",
        "interactive_postsetup": 'n',
    }
    result = cookies.bake(extra_context=context)
    assert result.exit_code != 0
    assert "Hook script failed" in str(result.exception)
