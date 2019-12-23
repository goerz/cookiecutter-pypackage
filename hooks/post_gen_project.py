#!/usr/bin/env python
import os
import shutil
from subprocess import call, check_call, CalledProcessError

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def remove_folder(folderpath):
    shutil.rmtree(
        os.path.join(PROJECT_DIRECTORY, folderpath), ignore_errors=True
    )


if __name__ == '__main__':

    if '{{ cookiecutter.create_author_file }}' != 'y':
        remove_file('AUTHORS.rst')
        remove_file('docs/authors.rst')
    if '{{ cookiecutter.sphinx_docs }}' == 'y':
        if '{{ cookiecutter.docshosting }}' != 'ReadTheDocs':
            remove_file('.readthedocs.yml')
            remove_file(os.path.join('docs', '_static', 'version-alert.js'))
        if '{{ cookiecutter.docshosting }}' != 'Doctr':
            remove_file(os.path.join('docs', '_static', 'version-menu.js'))
        if '{{ cookiecutter.use_notebooks }}' != 'y':
            remove_file(os.path.join('docs', 'nbval_sanitize.cfg'))
            remove_file(os.path.join('docs', 'tutorial.ipynb'))
            remove_folder('binder')
    else:
        remove_folder('docs')
        remove_folder('binder')
        remove_file('.readthedocs.yml')
    if '{{ cookiecutter.travisci }}' != 'y':
        remove_file('.travis.yml')
        remove_folder('.travis')
    else:
        if '{{ cookiecutter.travis_texlive }}' != 'y':
            remove_folder(os.path.join('.travis', 'texlive'))
        if '{{ cookiecutter.docshosting }}' != 'Doctr':
            remove_file(os.path.join('.travis', 'doctr_post_process.py'))
            remove_file(os.path.join('.travis', 'versions.py'))
            remove_file(os.path.join('.travis', 'doctr_build.sh'))
    if '{{ cookiecutter.appveyor }}' != 'y':
        remove_file('.appveyor.yml')
    if (
        '{{ cookiecutter.use_git_flow }}' == 'y'
        or '{{ cookiecutter.on_pypi }}' != 'y'
    ):
        remove_file(os.path.join('scripts', 'release.py'))
        if len(os.listdir('scripts')) == 0:
            remove_folder('scripts')
    if '{{ cookiecutter.use_pre_commit }}' != 'y':
        remove_file('.pre-commit-config.yaml')
        remove_file(os.path.join('scripts', 'pre-commit.py'))
        if len(os.listdir('scripts')) == 0:
            remove_folder('scripts')
    if '{{ cookiecutter.interactive_postsetup }}' == 'y':
        try:
            response = input(
                "Do you want to initialize the project with git? [yes]/no "
            )
            if not response.lower().strip().startswith('n'):
                if not shutil.which('git'):
                    response = input(
                        "You do not have git installed. Please install it now "
                        "and press Enter to continue."
                    )
                if '{{ cookiecutter.use_git_flow }}' == 'y':
                    print(
                        "During the project setup, you indicated that you "
                        "want to use the git-flow branching model. This will "
                        "now be set up."
                    )
                    print("Checking the git flow version...")
                    ret = call(['git', 'flow', 'version'])
                    if ret != 0:
                        response = input(
                            "You do not have 'git flow' installed. Please "
                            "install it now and press Enter to continue."
                        )
                    check_call(['git', 'init'])
                    check_call(
                        [
                            'git',
                            'commit',
                            '--allow-empty',
                            '-m',
                            "git-flow initialization",
                        ]
                    )
                    check_call(['git', 'flow', 'init'])
                    print("Done initializing git-flow. A commit was created:")
                    check_call(['git', 'log'])
                else:
                    check_call(['git', 'init'])
                git_remote = (
                    'git@github.com:{{ cookiecutter.github_username }}/'
                    '{{ cookiecutter.project_slug }}.git'
                )
                response = input(
                    "Do you want add '%s' as the git remote? "
                    "[yes]/no/<remote url> " % git_remote
                )
                if response.lower().strip().startswith('n'):
                    git_remote = ''
                else:
                    valid_remote = response.startswith(
                        "git"
                    ) or response.startswith("https://")
                    if valid_remote:
                        git_remote = response
                    check_call(['git', 'remote', 'add', 'origin', git_remote])
                    response = input(
                        "Please make sure that %s is set up on github at this "
                        "time. Press enter to continue." % git_remote
                    )
                response = input(
                    "Do you want to create a commit for the project skeleton? "
                    "[yes]/no "
                )
                if not response.lower().strip().startswith('n'):
                    check_call(['git', 'add', '.'])
                    check_call(['git', 'commit', '-m', 'Initial commit'])
                    check_call(['git', 'log'])
                    response = input(
                        "Do you want to push to 'origin'? [yes]/no "
                    )
                    if not response.lower().strip().startswith('n'):
                        check_call(['git', 'push', 'origin', '--all'])
                if '{{ cookiecutter.docshosting }}' == "Doctr":
                    response = input(
                        "Do you want to initialize Doctr at this time? "
                        "[yes]/no "
                    )
                    if not response.lower().strip().startswith('n'):
                        cmd = [
                            'tox',
                            '-e',
                            'run-cmd',
                            '--',
                            'doctr',
                            'configure',
                            '--no-upload-key',
                            '--no-authenticate',
                            '--key-path',
                            'docs/doctr_deploy_key',
                        ]
                        check_call(cmd)
        except CalledProcessError as exc_info:
            print(
                "ERROR: Exit code %s for command '%s'. Aborting git "
                "initialization"
                % (exc_info.returncode, " ".join(exc_info.cmd))
            )
