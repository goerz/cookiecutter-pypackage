# {{ cookiecutter.project_name }}
{% set github_project_root =  "https://github.com/" ~ cookiecutter.github_username  ~ "/" ~ cookiecutter.project_slug  %}
[![Source code on Github](https://img.shields.io/badge/{{ cookiecutter.github_username | replace("-","--") | replace("_", "__") }}-{{ cookiecutter.project_slug | replace("-","--") | replace("_", "__") }}-blue.svg?logo=github)][Github]
{%- if cookiecutter.on_pypi == 'y' %}
[![PyPI](https://img.shields.io/pypi/v/{{ cookiecutter.project_slug }}.svg)](https://pypi.python.org/pypi/{{ cookiecutter.project_slug }})
{%- else %}
<!--Not on PyPI-->
{%- endif %}
{%- if cookiecutter.sphinx_docs == 'y' %}
[![Documentation](https://img.shields.io/badge/docs-gh--pages-blue.svg)][docs]
[![Docs]({{ github_project_root }}/workflows/Docs/badge.svg?branch={{ cookiecutter.main_branch }})]({{ github_project_root }}/actions?query=workflow%3ADocs)
{%- else %}
<!--No online documentation-->
<!--No documentation workflow-->
{%- endif %}
[![Tests]({{ github_project_root }}/workflows/Tests/badge.svg?branch={{ cookiecutter.main_branch }})]({{ github_project_root }}/actions?query=workflow%3ATests)
[![Coverage](https://codecov.io/gh/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/branch/{{ cookiecutter.main_branch }}/graph/badge.svg)](https://codecov.io/gh/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }})
{%- if cookiecutter.open_source_license == 'MIT license' %}
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
{%- elif cookiecutter.open_source_license == 'BSD license' %}
[![BSD License](https://img.shields.io/badge/License-BSD-green.svg)](https://opensource.org/licenses/BSD-3-Clause)
{%- elif cookiecutter.open_source_license == 'ISC license' %}
[![ISC License](https://img.shields.io/badge/License-ISC-green.svg)](https://opensource.org/licenses/ISC)
{%- elif cookiecutter.open_source_license == 'Apache Software License 2.0' %}
[![Apache 2.0 License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](https://opensource.org/licenses/Apache-2.0)
{%- elif cookiecutter.open_source_license == 'GNU General Public License v3' %}
[![GPL v3 License](https://img.shields.io/badge/License-GPL%20v3-green.svg)](https://www.gnu.org/licenses/gpl-3.0)
{%- endif %}

{{ cookiecutter.project_short_description }}

Development of {{ cookiecutter.project_name }} happens on [Github][].
{% if cookiecutter.sphinx_docs == 'y' %}
You can read the full documentation [online][docs].

[docs]: https://{{ cookiecutter.github_username }}.github.io/{{ cookiecutter.project_slug }}/
{% endif %}

## Installation

{%- if cookiecutter.on_pypi == 'y' %}
To install the latest released version of {{ cookiecutter.project_name }}, run this command in your terminal:

```
pip install {{ cookiecutter.project_slug }}
```

This is the preferred method to install {{ cookiecutter.project_name }}, as it will always install the most recent stable release.

If you don't have [pip](https://pip.pypa.io) installed, the [Python installation guide](http://docs.python-guide.org/en/latest/starting/installation/), respectively the [Python Packaging User Guide](https://packaging.python.org/tutorials/installing-packages/) can guide you through the process.
{%endif %}

To install the latest development version of {{ cookiecutter.project_name }} from [Github][].

```
pip install git+https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.git@{{ cookiecutter.main_branch }} }}#egg={{ cookiecutter.project_slug }}
```

{% if cookiecutter.on_pypi == 'n' %}

**Note: ** {{ cookiecutter.project_name }} is currently not released on the [Python Package Index](https://pypi.org), so you will not be able to install it with `pip install <package name>`.

{%-endif%}

## Usage

To use {{ cookiecutter.project_name }} in a Python project:

``` python
import {{ cookiecutter.project_slug }}
```

[Github]: {{ github_project_root }}
