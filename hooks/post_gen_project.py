#!/usr/bin/env python
import os
import shutil
from subprocess import call, check_call, check_output, CalledProcessError

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def remove_folder(folderpath):
    shutil.rmtree(
        os.path.join(PROJECT_DIRECTORY, folderpath), ignore_errors=True)


if __name__ == '__main__':

    if '{{ cookiecutter.create_author_file }}' != 'y':
        remove_file('AUTHORS.rst')
        remove_file('docs/authors.rst')

    if '{{ cookiecutter.sphinx_docs }}' != 'y':
        remove_folder('docs')
        remove_file('readthedocs.yml')
    else:
        if '{{ cookiecutter.readthedocs }}' != 'y':
            remove_file('readthedocs.yml')
            remove_file(os.path.join('docs', 'rtd_environment.yml'))
    if '{{ cookiecutter.travisci }}' != 'y':
        remove_file('.travis.yml')
    if '{{ cookiecutter.appveyor }}' != 'y':
        remove_file('.appveyor.yml')

    if '{{ cookiecutter.interactive_postsetup }}' == 'y':
        try:
            response = input(
                "Do you want to initialize the project with git? [yes]/no ")
            if not response.lower().strip().startswith('n'):
                if not shutil.which('git'):
                    response = input(
                        "You do not have git installed. Please install it now "
                        "and press Enter to continue.")
                if '{{ cookiecutter.use_git_flow }}' == 'y':
                    print(
                        "During the project setup, you indicated that you "
                        "want to use the git-flow branching model. This will "
                        "now be set up.")
                    print("Checking the git flow version...")
                    ret = call(['git', 'flow', 'version'])
                    if ret != 0:
                        response = input(
                            "You do not have 'git flow' installed. Please "
                            "install it now and press Enter to continue.")
                    check_call(['git', 'init'])
                    check_call([
                        'git', 'commit', '--allow-empty', '-m',
                        "git-flow initialization"])
                    check_call(['git', 'flow', 'init'])
                    print("Done initializing git-flow. A commit was created:")
                    check_call(['git', 'log'])
                else:
                    check_call(['git', 'init'])
                git_remote = (
                    'git@github.com:{{ cookiecutter.github_username }}/'
                    '{{ cookiecutter.project_slug }}.git')
                response = input(
                    "Do you want add '%s' as the git remote? "
                    "[yes]/no/<remote url> " % git_remote)
                if response.lower().strip().startswith('n'):
                    git_remote = ''
                else:
                    valid_remote = (
                        response.startswith("git") or
                        response.startswith("https://"))
                    if valid_remote:
                        git_remote = response
                    check_call(['git', 'remote', 'add', 'origin', git_remote])
                    response = input(
                        "Please make sure that %s is set up on github at this "
                        "time. Press enter to continue." % git_remote)
                response = input(
                    "Do you want to create a commit for the project skeleton? "
                    "yes/[no] ")
                if response.lower().strip().startswith('y'):
                    check_call(['git', 'add', '.'])
                    check_call(['git', 'commit', '-m', 'project skeleton'])
                    check_call(['git', 'log'])
                    response = input(
                        "Do you want to push to 'origin'? [yes]/no ")
                    if not response.lower().strip().startswith('n'):
                        check_call(['git', 'push', 'origin', '--all'])
        except CalledProcessError as exc_info:
            print(
                "ERROR: Exit code %s for command '%s'. Aborting git "
                "initialization"
                % (exc_info.returncode, " ".join(exc_info.cmd)))
