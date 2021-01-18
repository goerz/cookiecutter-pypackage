#!/usr/bin/env python
"""Post-process generated project."""
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

    if '{{ cookiecutter.sphinx_docs }}' == 'n':
        remove_folder('docs')
        remove_file(os.path.join(".github", "workflows", "docs.yml"))
    if ('{{ cookiecutter.on_pypi }}' != 'y'):
        remove_file(os.path.join('scripts', 'release.py'))
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
        except CalledProcessError as exc_info:
            print(
                "ERROR: Exit code %s for command '%s'. Aborting git "
                "initialization"
                % (exc_info.returncode, " ".join(exc_info.cmd))
            )
