Welcome to {{ cookiecutter.project_name }}'s documentation!
==========={%- for _ in cookiecutter.project_name -%}={%- endfor -%}=================

.. image:: https://img.shields.io/badge/github-{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}-blue.svg
   :alt: Source code on Github
   :target: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}
{%- if cookiecutter.on_pypi == 'y' %}
.. image:: https://img.shields.io/pypi/v/{{ cookiecutter.project_slug }}.svg
   :alt: {{ cookiecutter.project_name }} on the Python Package Index
   :target: https://pypi.python.org/pypi/{{ cookiecutter.project_slug }}
{%endif %}

{%- if cookiecutter.travisci == 'y' %}
.. image:: https://img.shields.io/travis/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.svg
   :alt: Travis Continuous Integration
   :target: https://travis-ci.org/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}
{%- endif %}
{%- if cookiecutter.appveyor == 'y' %}
.. image:: https://img.shields.io/badge/appveyor-no%20id-red.svg
   :alt: AppVeyor Continuous Integration
   :target: https://ci.appveyor.com/project/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}
{%- endif %}

{%- if cookiecutter.coveralls == 'y' %}
.. image:: https://img.shields.io/coveralls/github/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/{% if cookiecutter.use_git_flow == 'y' %}develop{% else %}master{% endif %}.svg
   :alt: Coveralls
   :target: https://coveralls.io/github/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}?branch={%- if cookiecutter.use_git_flow == 'y' -%}develop{%- else -%}master{%- endif -%}
{%- endif %}

{%- if cookiecutter.readthedocs == 'y' %}
.. image:: https://readthedocs.org/projects/{{ cookiecutter.project_slug | replace("_", "-") }}/badge/?version=latest
   :alt: Documentation Status
   :target: https://{{ cookiecutter.project_slug | replace("_", "-") }}.readthedocs.io/en/latest/?badge=latest
{%- endif %}

{%- if cookiecutter.open_source_license == 'MIT license' %}
.. image:: https://img.shields.io/badge/License-MIT-green.svg
   :alt: MIT License
   :target: https://opensource.org/licenses/MIT
{%- elif cookiecutter.open_source_license == 'BSD license' %}
.. image:: https://img.shields.io/badge/License-BSD-green.svg
   :alt: BSD License
   :target: https://opensource.org/licenses/BSD-3-Clause
{%- elif cookiecutter.open_source_license == 'ISC license' %}
.. image:: https://img.shields.io/badge/License-ISC-green.svg
   :alt: ISC License
   :target: https://opensource.org/licenses/ISC
{%- elif cookiecutter.open_source_license == 'Apache Software License 2.0' %}
.. image:: https://img.shields.io/badge/License-Apache%202.0-green.svg
   :alt: Apache 2.0 License
   :target: https://opensource.org/licenses/Apache-2.0
{%- elif cookiecutter.open_source_license == 'GNU General Public License v3' %}
.. image:: https://img.shields.io/badge/License-GPL%20v3-green.svg
   :alt: GPL v3 License
   :target: https://www.gnu.org/licenses/gpl-3.0
{%- endif %}

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   readme
   contributing
   {% if cookiecutter.create_author_file == 'y' -%}authors
   {% endif -%}history
   {% if cookiecutter.use_notebooks == 'y' -%}tutorial.ipynb{% endif %}


API
===

.. toctree::
   :maxdepth: 1

   API of the {{ cookiecutter.project_name }} package <API/{{ cookiecutter.project_slug }}>

Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
