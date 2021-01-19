#!/usr/bin/env python
"""The setup script."""
import sys

from setuptools import find_packages, setup


def get_version(filename):
    """Extract the package version"""
    with open(filename, encoding='utf8') as in_fh:
        for line in in_fh:
            if line.startswith('__version__'):
                return line.split('=')[1].strip()[1:-1]
    raise ValueError("Cannot extract version from %s" % filename)


with open('README.md', encoding='utf8') as readme_file:
    README = readme_file.read()

try:
    with open('HISTORY.md', encoding='utf8') as history_file:
        HISTORY = history_file.read()
except OSError:
    HISTORY = ''

# requirements for use
requirements = []

# requirements for development (testing, generating docs)
dev_requirements = [
    'better-apidoc',
    'coverage',
    'coveralls',
{%- if cookiecutter.sphinx_docs %}
    'doctr-versions-menu',
{%- endif %}
    'flake8',
    'gitpython',
    'isort',
    'ipython',
    'pre-commit',
    'pdbpp',
    'pylint',
    'pytest',
    'pytest-cov',
    'pytest-xdist',
{%- if cookiecutter.sphinx_docs %}
    'm2r',
    'recommonmark',
    'sphinx',
    'sphinx-autobuild',
    'sphinx-copybutton',
    'sphinx-autodoc-typehints',
    'sphinx_rtd_theme',
{%- endif %}
    'twine',
    'wheel',
]
if sys.version_info >= (3, 6):
    dev_requirements.append('black')

VERSION = get_version('./src/{{ cookiecutter.project_slug }}/__init__.py')


{%- set license_classifiers = {
    'MIT license': 'License :: OSI Approved :: MIT License',
    'BSD license': 'License :: OSI Approved :: BSD License',
    'ISC license': 'License :: OSI Approved :: ISC License (ISCL)',
    'Apache Software License 2.0': 'License :: OSI Approved :: Apache Software License',
    'GNU General Public License v3': 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
} %}

setup(
    author="{{ cookiecutter.full_name.replace('\"', '\\\"') }}",
    author_email='{{ cookiecutter.email }}',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
{%- if cookiecutter.open_source_license in license_classifiers %}
        '{{ license_classifiers[cookiecutter.open_source_license] }}',
{%- endif %}
        'Natural Language :: English',
{%- if cookiecutter.support_py36 == 'y' %}
        'Programming Language :: Python :: 3.6',
{%- endif %}
{%- if cookiecutter.support_py37 == 'y' %}
        'Programming Language :: Python :: 3.7',
{%- endif %}
{%- if cookiecutter.support_py38 == 'y' %}
        'Programming Language :: Python :: 3.8',
{%- endif %}
{%- if cookiecutter.support_py38 == 'y' %}
        'Programming Language :: Python :: 3.9',
{%- endif %}
        'Natural Language :: English',
    ],
    description=(
        "{{ cookiecutter.project_short_description }}"
    ),
    python_requires='>={% if cookiecutter.support_py36 == 'y' %}3.6{% elif cookiecutter.support_py37 == 'y' %}3.7{% elif cookiecutter.support_py38 == 'y' %}3.8{% elif cookiecutter.support_py39 == 'y' %}3.9{% else %}3{% endif %}',
    install_requires=requirements,
    extras_require={'dev': dev_requirements},
{%- if cookiecutter.open_source_license in license_classifiers %}
    license="{{ cookiecutter.open_source_license }}",
{%- endif %}
    long_description=README + '\n\n' + HISTORY,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='{{ cookiecutter.project_slug }}',
    name='{{ cookiecutter.project_slug }}',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    url='https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}',
    version=VERSION,
    zip_safe=False,
)
