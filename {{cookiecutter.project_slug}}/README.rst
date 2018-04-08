{% for _ in cookiecutter.project_name %}={% endfor %}
{{ cookiecutter.project_name }}
{% for _ in cookiecutter.project_name %}={% endfor %}

{%- if cookiecutter.on_pypi == 'y' %}
.. image:: https://img.shields.io/pypi/v/{{ cookiecutter.project_slug }}.svg
        :target: https://pypi.python.org/pypi/{{ cookiecutter.project_slug }}
{%endif %}

{%- if cookiecutter.travisci == 'y' %}
.. image:: https://img.shields.io/travis/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.svg
        :target: https://travis-ci.org/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}
{%- endif %}

{%- if cookiecutter.coveralls == 'y' %}
.. image:: https://coveralls.io/repos/github/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/badge.svg?branch={%- if cookiecutter.use_git_flow == 'y' -%}develop{%- else -%}master{%- endif -%}
        :target: https://coveralls.io/github/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}?branch={%- if cookiecutter.use_git_flow == 'y' -%}develop{%- else -%}master{%- endif -%}
{%- endif %}

{%- if cookiecutter.readthedocs == 'y' %}
.. image:: https://readthedocs.org/projects/{{ cookiecutter.project_slug | replace("_", "-") }}/badge/?version=latest
        :target: https://{{ cookiecutter.project_slug | replace("_", "-") }}.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status
{%- endif %}

{{ cookiecutter.project_short_description }}

Development of {{ cookiecutter.project_name }} happens on `Github`_.


Installation
------------

{%- if cookiecutter.on_pypi == 'y' %}
To install the latest released version of {{ cookiecutter.project_name }}, run this command in your terminal:

.. code-block:: console

    $ pip install {{ cookiecutter.project_slug }}

This is the preferred method to install {{ cookiecutter.project_name }}, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/
{%endif %}

To install the latest development version of {{ cookiecutter.project_name }} from `Github`_.

.. code-block:: console

    $ pip install git+https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.git@{%- if cookiecutter.use_git_flow == 'y' -%}develop{%- else -%}master{%- endif -%}#egg={{ cookiecutter.project_slug }}

{%- if cookiecutter.on_pypi == 'n' %}
Note that {{ cookiecutter.project_name }} is currently not released on the `Python Package Index`_, hence you will not be able to install it with ``pip install {{ cookiecutter.project_slug }}``.

.. _Python Package Index: https://pypi.org
{%endif%}

.. _Github: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}

Usage
-----

To use {{ cookiecutter.project_name }} in a project::

    import {{ cookiecutter.project_slug }}
