"""Test the project template

Running the test suite requires Python >= 3.6, although the cookiecutter
template itself also works with older versions of Python 3
"""
import contextlib
import io
import os
import pprint
import re
import shutil
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


def merge_folders(root_src_dir, root_dst_dir):
    """Merge `root_src_dir` into `root_dst_dir`."""
    for src_dir, __, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.copy(src_file, dst_dir)


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


def check_git_hooks(project):
    """Check that pre-commits are installed."""
    assert project.join('.git', 'hooks', 'pre-commit').isfile()


def check_committing_code(project):
    """Check that we can add code and commit it."""
    merge_folders(
        str(Path(__file__).parent / 'mainpkg'),
        str(project.join('src', 'python_boilerplate')),
    )
    cmds = (
        ['git', 'add', '.'],
        ['git', 'commit', '-m', 'Add some code'],
        ['git', 'log'],
    )
    for cmd in cmds:
        _run = check_call(cmd)
        _run(project)
    assert project.join(
        'src', 'python_boilerplate', 'subpkg', 'submod.py'
    ).isfile()


def check_call(cmd, in_stdout=None):
    """Check that the given `cmd` passes without error.

    The `cmd` (list of arguments) is run with the project folder as the working
    directory.
    """

    def _check_call(project):
        """Check `cmd` run inside of `project`."""
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
        assert result.returncode == 0
        if in_stdout is not None:
            assert in_stdout in result.stdout

    _check_call.__display_name__ = "check_call(%s)" % repr(cmd)

    return _check_call


def check_default_files(project):
    """Check the list of files for the default settings

    This check must run before any 'make test' or 'make docs'
    """
    expected_files = [
        '.appveyor.yml',
        '.editorconfig',
        '.gitignore',
        '.pre-commit-config.yaml',
        '.pylintrc',
        '.travis.yml',
        'AUTHORS.rst',
        'CONTRIBUTING.rst',
        'HISTORY.rst',
        'LICENSE',
        'Makefile',
        'MANIFEST.in',
        'README.rst',
        'setup.cfg',
        'setup.py',
        'tox.ini',
        '.github/ISSUE_TEMPLATE.md',
        '.travis/doctr_build.sh',
        '.travis/doctr_post_process.py',
        '.travis/versions.py',
        'docs/authors.rst',
        'docs/build_pdf.py',
        'docs/conf.py',
        'docs/conftest.py',
        'docs/contributing.rst',
        'docs/history.rst',
        'docs/index.rst',
        'docs/readme.rst',
        'docs/spelling_wordlist.txt',
        'docs/_extensions/dollarmath.py',
        'docs/_static/mycss.css',
        'docs/_static/version-menu.js',
        'docs/_templates/breadcrumbs.html',
        'docs/_templates/layout.html',
        'docs/_templates/module.rst',
        'docs/_templates/package.rst',
        'docs/API/.gitignore',
        'scripts/bootstrap.py',
        'scripts/clean.py',
        'scripts/pre-commit.py',
        'scripts/README.md',
        'scripts/release.py',
        'src/conftest.py',
        'src/python_boilerplate/__init__.py',
        'tests/test_python_boilerplate.py',
    ]
    assert files_match_expected(str(project), expected_files)


def check_notebook_files(project):
    """Check the list of files for the default settings

    This check must run before any 'make test' or 'make docs'
    """
    expected_files = [
        '.appveyor.yml',
        '.editorconfig',
        '.gitignore',
        '.pre-commit-config.yaml',
        '.pylintrc',
        '.travis.yml',
        'AUTHORS.rst',
        'CONTRIBUTING.rst',
        'HISTORY.rst',
        'LICENSE',
        'Makefile',
        'MANIFEST.in',
        'README.rst',
        'setup.cfg',
        'setup.py',
        'tox.ini',
        '.github/ISSUE_TEMPLATE.md',
        '.travis/doctr_build.sh',
        '.travis/doctr_post_process.py',
        '.travis/versions.py',
        'binder/environment.yml',
        'docs/authors.rst',
        'docs/build_pdf.py',
        'docs/conf.py',
        'docs/conftest.py',
        'docs/contributing.rst',
        'docs/history.rst',
        'docs/index.rst',
        'docs/nbval_sanitize.cfg',
        'docs/readme.rst',
        'docs/spelling_wordlist.txt',
        'docs/tutorial.ipynb',
        'docs/_extensions/dollarmath.py',
        'docs/_static/mycss.css',
        'docs/_static/version-menu.js',
        'docs/_templates/breadcrumbs.html',
        'docs/_templates/layout.html',
        'docs/_templates/module.rst',
        'docs/_templates/package.rst',
        'docs/API/.gitignore',
        'scripts/bootstrap.py',
        'scripts/clean.py',
        'scripts/pre-commit.py',
        'scripts/README.md',
        'scripts/release.py',
        'src/conftest.py',
        'src/python_boilerplate/__init__.py',
        'tests/test_python_boilerplate.py',
    ]
    assert files_match_expected(str(project), expected_files)


def check_rtd_files(project):
    """Check the list of files for the default settings

    This check must run before any 'make test' or 'make docs'
    """
    expected_files = [
        '.appveyor.yml',
        '.editorconfig',
        '.gitignore',
        '.pre-commit-config.yaml',
        '.pylintrc',
        '.readthedocs.yml',
        '.travis.yml',
        'AUTHORS.rst',
        'CONTRIBUTING.rst',
        'HISTORY.rst',
        'LICENSE',
        'Makefile',
        'MANIFEST.in',
        'README.rst',
        'setup.cfg',
        'setup.py',
        'tox.ini',
        '.github/ISSUE_TEMPLATE.md',
        'docs/authors.rst',
        'docs/build_pdf.py',
        'docs/conf.py',
        'docs/conftest.py',
        'docs/contributing.rst',
        'docs/history.rst',
        'docs/index.rst',
        'docs/readme.rst',
        'docs/spelling_wordlist.txt',
        'docs/_extensions/dollarmath.py',
        'docs/_static/mycss.css',
        'docs/_static/version-alert.js',
        'docs/_templates/breadcrumbs.html',
        'docs/_templates/layout.html',
        'docs/_templates/module.rst',
        'docs/_templates/package.rst',
        'docs/API/.gitignore',
        'scripts/bootstrap.py',
        'scripts/clean.py',
        'scripts/pre-commit.py',
        'scripts/README.md',
        'scripts/release.py',
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
        '.gitignore',
        '.pylintrc',
        'CONTRIBUTING.rst',
        'HISTORY.rst',
        'LICENSE',
        'Makefile',
        'MANIFEST.in',
        'README.rst',
        'setup.cfg',
        'setup.py',
        'tox.ini',
        '.github/ISSUE_TEMPLATE.md',
        'scripts/bootstrap.py',
        'scripts/clean.py',
        'scripts/README.md',
        'src/conftest.py',
        'src/python_boilerplate/__init__.py',
        'tests/test_python_boilerplate.py',
    ]
    assert files_match_expected(str(project), expected_files)


def check_xfail(check):
    """Decoractor for a check that is expected to fail."""

    def check_not(project):
        """Check the `check` fails."""
        stdout = io.StringIO()
        try:
            with contextlib.redirect_stdout(stdout):
                check(project)
        except AssertionError:
            pass
        else:
            raise AssertionError("%s passed unexpectedly" % check.__name__)

    check_not.__display_name__ = "check_xfail(%s)" % check.__name__

    return check_not


def check_make_test(project):
    """Check that 'make test' exits with no error"""
    res = make(project, 'test')
    assert res.returncode == 0


def check_make_clean(project):
    """Check that 'make clean' exits with no error"""
    res = make(project, 'clean')
    assert res.returncode == 0


def check_make_docs(project):
    """Check that 'make docs' exits with no error"""
    res = make(project, 'docs')
    assert res.returncode == 0


def check_make_docs_pdf(project):
    """Check that 'make docs-pdf' exits with no error"""
    res = make(project, 'docs-pdf')
    assert res.returncode == 0


def check_build_artifacts(project):
    """Check that the doctr_build script produces expected artifacts."""
    cmd = ['sh', '.travis/doctr_build.sh']
    env = os.environ.copy()
    env_keys = list(env.keys())
    for key in env_keys:
        if key.startswith('TRAVIS'):
            del env[key]
    env['TRAVIS_TAG'] = 'v1.0.0'
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
        cwd=str(project),
        timeout=600,
        check=False,
        universal_newlines=True,
        env=env,
    )
    if result.returncode != 0:
        print("\n'%s' STDOUT:\n%s" % (" ".join(cmd), result.stdout))
        print("\n'%s' STDERR:\n%s" % (" ".join(cmd), result.stderr))
    assert result.returncode == 0
    filenames = [
        'python_boilerplate-v1.0.0.epub',
        'python_boilerplate-v1.0.0.pdf',
        'python_boilerplate-v1.0.0.zip',
    ]
    for filename in filenames:
        assert project.join('docs', '_build', 'artifacts', filename).isfile()


def check_api_files(project):
    """Check that files generated by better_apidoc exist."""
    assert project.join(
        'docs',
        '_build',
        'html',
        'API',
        'python_boilerplate.subpkg.submod.html',
    ).isfile()


def check_dist(project):
    """Check that we can make a well-formed sdist and wheel"""
    res = make(project, 'dist', 'dist-check')
    assert res.returncode == 0
    assert len(list(Path(project.join('dist')).glob('*.whl'))) == 1
    assert len(list(Path(project.join('dist')).glob('*.tar.gz'))) == 1


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
        help                 show this help
        bootstrap            verify that tox is available and pre-commit hooks are active
        clean                remove all build, docs, test, and coverage artifacts, as well as tox environments
        clean-build          remove build artifacts
        clean-tests          remove test and coverage artifacts
        clean-venv           remove tox virtual environments
        clean-docs           remove documentation artifacts
        flake8-check         check style with flake8
        pylint-check         check style with pylint
        test                 run tests for all supported Python versions
        test35               run tests for Python 3.5
        test36               run tests for Python 3.6
        test37               run tests for Python 3.7
        test38               run tests for Python 3.8
        test39               run tests for Python 3.9
        docs                 generate Sphinx HTML documentation, including API docs
        docs-pdf             generate Sphinx PDF documentation, via latex
        black-check          Check all src and test files for complience to "black" code style
        black                Apply 'black' code style to all src and test files
        isort-check          Check all src and test files for correctly sorted imports
        isort                Sort imports in all src and test files
        coverage             generate coverage report in ./htmlcov
        test-upload          package and upload a release to test.pypi.org
        upload               package and upload a release to pypi.org
        release              Create a new version, package and upload it
        dist                 builds source and wheel package
        dist-check           Check all dist files for correctness
        '''
    ).strip()
    assert stdout == expected


def check_notebook_make_help(project):
    """Check that we have the expected make targets in the default
    configuration with notebooks enabled."""
    res = make(project, 'help')
    stdout = res.stdout
    # some versions of make print additional information that we need to strip
    stdout = re.sub(r'make.*: Entering directory.*\n', '', stdout)
    stdout = re.sub(r'make.*: Leaving directory.*', '', stdout)
    stdout = stdout.strip()
    expected = dedent(
        r'''
        help                 show this help
        bootstrap            verify that tox is available and pre-commit hooks are active
        clean                remove all build, docs, test, and coverage artifacts, as well as tox environments
        clean-build          remove build artifacts
        clean-tests          remove test and coverage artifacts
        clean-venv           remove tox virtual environments
        clean-docs           remove documentation artifacts
        flake8-check         check style with flake8
        pylint-check         check style with pylint
        test                 run tests for all supported Python versions
        test35               run tests for Python 3.5
        test36               run tests for Python 3.6
        test37               run tests for Python 3.7
        test38               run tests for Python 3.8
        test39               run tests for Python 3.9
        docs                 generate Sphinx HTML documentation, including API docs
        docs-pdf             generate Sphinx PDF documentation, via latex
        black-check          Check all src and test files for complience to "black" code style
        black                Apply 'black' code style to all src and test files
        isort-check          Check all src and test files for correctly sorted imports
        isort                Sort imports in all src and test files
        coverage             generate coverage report in ./htmlcov
        test-upload          package and upload a release to test.pypi.org
        upload               package and upload a release to pypi.org
        release              Create a new version, package and upload it
        dist                 builds source and wheel package
        dist-check           Check all dist files for correctness
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
        help                 show this help
        bootstrap            verify that tox is available and pre-commit hooks are active
        clean                remove all build, test, and coverage artifacts, as well as tox environments
        clean-build          remove build artifacts
        clean-tests          remove test and coverage artifacts
        clean-venv           remove tox virtual environments
        flake8-check         check style with flake8
        pylint-check         check style with pylint
        test                 run tests for all supported Python versions
        test35               run tests for Python 3.5
        test36               run tests for Python 3.6
        test37               run tests for Python 3.7
        test38               run tests for Python 3.8
        test39               run tests for Python 3.9
        coverage             generate coverage report in ./htmlcov
        dist                 builds source and wheel package
        dist-check           Check all dist files for correctness
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


def check_isort_ok(project):
    """Check that the entire project passes inspection with black.

    The documentation conf.py is excluded.
    """
    cmd = [
        'isort',
        '--recursive',
        '--check-only',
        '--diff',
        '--verbose',
        '--skip',
        'docs/conf.py',
        '.',
    ]
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


def check_only_py38_venv(project):
    """Check that only the .tox/py37 venv-folder exists

    Must follow `check_make_test`.
    """
    assert not project.join('.tox', 'py34').exists()
    assert not project.join('.tox', 'py35').exists()
    assert not project.join('.tox', 'py36').exists()
    assert not project.join('.tox', 'py37').exists()
    assert project.join('.tox', 'py38').isdir()
    assert not project.join('.tox', 'py39').exists()


def check_defaults_venvs(project):
    """Check that the .tox folder of the default configuration exist

    Must follow `check_make_test`.
    """
    assert not project.join('.tox', 'py34').exists()
    assert not project.join('.tox', 'py35').exists()
    assert project.join('.tox', 'py36').isdir()
    assert project.join('.tox', 'py37').isdir()
    assert project.join('.tox', 'py38').isdir()
    assert not project.join('.tox', 'py39').exists()


# fmt: off
CONFIGURATIONS = [
    (
        'default',
        {
            'interactive_postsetup': 'n'
        },
        [
            check_isort_ok,
            check_black_ok,
            check_default_make_help,
            check_default_files,
            check_make_test,
            check_dist,
            check_defaults_venvs,
            check_xfail(check_default_files),
            check_make_clean,
            check_default_files,
            check_call(['git', 'init']),
            check_call(['git', 'add', '.']),
            check_call(['git', 'commit', '-m', 'Initial commit']),
            check_call(['git', 'log'], in_stdout='Initial commit'),
            check_make_docs,
            check_git_hooks,  # should have been created by "make docs"
            check_committing_code,
            check_make_docs,
            check_make_docs_pdf,
            check_api_files,
        ],
    ),
    (
        'artifacts',
        {
            'interactive_postsetup': 'n',
            'travis_texlive': 'y'
        },
        [
            check_call(['git', 'init']),
            check_call(['git', 'add', '.']),
            check_call(['git', 'commit', '-m', 'Initial commit']),
            check_call(['git', 'log'], in_stdout='Initial commit'),
            check_committing_code,
            check_build_artifacts,
            check_api_files,
        ],
    ),
    (
        'notebooks',
        {
            'interactive_postsetup': 'n',
            'use_notebooks': 'y'

        },
        [
            check_notebook_make_help,
            check_notebook_files,
            check_make_test,
            check_make_docs,
        ],
    ),
    (
        'rtd',
        {
            'docshosting': 'ReadTheDocs',
            'interactive_postsetup': 'n'
        },
        [
            check_default_make_help,
            check_rtd_files,
        ],
    ),
    (
        'minimal',
        {
            "create_author_file": "n",
            "use_isort": "n",
            "use_black": "n",
            "use_pre_commit": "n",
            "on_pypi": "n",
            "travisci": "n",
            "appveyor": "n",
            "coverage": "None",
            "sphinx_docs": "n",
            "use_notebooks": "n",
            "better_apidoc": "n",
            "docshosting": "None",
            "support_py35": "n",
            "support_py36": "n",
            "support_py37": "y",
            "support_py38": "n",
            "support_py39": "n",
            "use_git_flow": "n",
            "interactive_postsetup": "n",
        },
        [
            check_black_ok,
            check_minimal_files,
            check_make_test,
            check_minimal_make_help,
            check_dist,
        ],
    ),
    (
        'only_latest',
        {
            "support_py35": "n",
            "support_py36": "n",
            "support_py37": "n",
            "support_py38": "y",
            "support_py39": "n",
            "use_notebooks": "n",
            "interactive_postsetup": 'n',
        },
        [
            check_make_test,
            check_make_docs,
            check_only_py38_venv
        ],
    ),
    (
        'custom_metadata',
        {
            "full_name": "The Architect",
            "email": "architect@mail.michaelgoerz.net",
            "github_username": "qucontrol",
            "project_name": "My-Py-Package",
            "project_slug": "mypypackage",
            "project_short_description": (
                "This project is generated with custom metadata"
            ),
            "version": "1.0.0-dev",
            "interactive_postsetup": 'n',
        },
        [
            check_custom_metadata
        ],
    ),
]
# fmt: on


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
    if result.exception is not None:
        print(str(result.exception))
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.isdir()
    print("")
    print("Created %s" % result.project)
    for checker in checkers:
        display_name = getattr(checker, '__display_name__', checker.__name__)
        print("   %s..." % display_name)
        checker(result.project)
