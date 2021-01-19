Welcome to {{ cookiecutter.project_name }}'s documentation!
==========={%- for _ in cookiecutter.project_name -%}={%- endfor -%}=================

{% set github_project_root =  "https://github.com/" ~ cookiecutter.github_username  ~ "/" ~ cookiecutter.project_slug  %}
.. only:: html

   .. image:: https://img.shields.io/badge/{{ cookiecutter.github_username | replace("-","--") | replace("_", "__") }}-{{ cookiecutter.project_slug | replace("-","--") | replace("_", "__") }}-blue.svg?logo=github
      :alt: Source code on Github
      :target: {{ github_project_root }}

{%- if cookiecutter.on_pypi == 'y' %}

   .. image:: https://img.shields.io/pypi/v/{{ cookiecutter.project_slug }}.svg
      :alt: PyPI
      :target: https://pypi.python.org/pypi/{{ cookiecutter.project_slug }}

{%- endif %}

{%- if cookiecutter.on_pypi == 'y' %}

   .. image:: https://img.shields.io/badge/docs-gh--pages-blue.svg
      :alt: Documentation
      :target: https://{{ cookiecutter.github_username }}.github.io/{{ cookiecutter.project_slug }}/

   .. image:: {{ github_project_root }}/workflows/Docs/badge.svg?branch={{ cookiecutter.main_branch }}
      :alt: Docs
      :target: {{ github_project_root }}/actions?query=workflow%3ADocs

{%- endif %}

   .. image:: {{ github_project_root }}/workflows/Tests/badge.svg?branch={{ cookiecutter.main_branch }}
      :alt: Tests
      :target: {{ github_project_root }}/actions?query=workflow%3ATests

   .. image:: https://codecov.io/gh/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/branch/{{ cookiecutter.main_branch }}/graph/badge.svg
      :alt: Coverage
      :target: https://codecov.io/gh/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}

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

.. Tutorials (learning oriented):

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   Installation & Usage <readme>


.. Explanation / Discussion (understanding-oriented):

   TODO

   How-to (problem-oriented)

   TODO

.. toctree::
   :maxdepth: 2
   :caption: Development

   contributing
   authors
   history

.. Reference (information oriented):

.. toctree::
   :maxdepth: 1
   :caption: Reference

   API of the {{ cookiecutter.project_name }} package <API/{{ cookiecutter.project_slug }}>

* :ref:`modindex`
