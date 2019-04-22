#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
import sys

from setuptools import setup, find_packages


def get_version(filename):
    """Extract the package version"""
    with open(filename) as in_fh:
        for line in in_fh:
            if line.startswith('__version__'):
                return line.split('=')[1].strip()[1:-1]
    raise ValueError("Cannot extract version from %s" % filename)


with open('README.rst') as readme_file:
    readme = readme_file.read()

try:
    with open('HISTORY.rst') as history_file:
        history = history_file.read()
except OSError:
    history = ''

requirements = []

dev_requirements = [
{%- if cookiecutter.better_apidoc == 'y' %}
    'better-apidoc'
{% endif %}
    'coverage',
    'flake8',
    'gitpython',
    'pep8',
    'pylint',
    'pytest',
    'pytest-cov',
    'pytest-xdist',
    'sphinx',
    'sphinx-autobuild',
    'sphinx-autodoc-typehints',
    'sphinx_rtd_theme',
    'twine',
    'wheel',
{%- if cookiecutter.use_notebooks == 'y' %}
    'jupyter',
    'nbval',
    'nbsphinx',
    'watermark',
{% endif %}
]
{% if cookiecutter.use_black == 'y' %}
if sys.version_info >= (3, 6):
    dev_requirements.append('black')
{% endif %}

version = get_version('./src/{{ cookiecutter.project_slug }}/__init__.py')


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
{%- if cookiecutter.support_py34 == 'y' %}
        'Programming Language :: Python :: 3.4',
{%- endif %}
{%- if cookiecutter.support_py35 == 'y' %}
        'Programming Language :: Python :: 3.5',
{%- endif %}
{%- if cookiecutter.support_py36 == 'y' %}
        'Programming Language :: Python :: 3.6',
{%- endif %}
{%- if cookiecutter.support_py37 == 'y' %}
        'Programming Language :: Python :: 3.7',
{%- endif %}
    ],
    description=(
        "{{ cookiecutter.project_short_description }}"
    ),
    python_requires='>={%if cookiecutter.support_py34 == 'y' %}3.4{% elif cookiecutter.support_py35 == 'y' %}3.5{% elif cookiecutter.support_py36 == 'y' %}3.6{% elif cookiecutter.support_py37 == 'y' %}3.7{% else %}3{% endif %}',
    install_requires=requirements,
    extras_require={
        'dev': dev_requirements,
    },
{%- if cookiecutter.open_source_license in license_classifiers %}
    license="{{ cookiecutter.open_source_license }}",
{%- endif %}
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='{{ cookiecutter.project_slug }}',
    name='{{ cookiecutter.project_slug }}',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    url='https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}',
    version=version,
    zip_safe=False,
)
