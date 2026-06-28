# Welcome to {{ cookiecutter.project_name }}'s documentation!

{% set github_project_root =  "https://github.com/" ~ cookiecutter.github_username  ~ "/" ~ cookiecutter.project_slug -%}
```{only} html
[![Source code on Github](https://img.shields.io/badge/{{ cookiecutter.github_username | replace("-","--") | replace("_", "__") }}-{{ cookiecutter.project_slug | replace("-","--") | replace("_", "__") }}-blue.svg?logo=github)]({{ github_project_root }})
{%- if cookiecutter.on_pypi == 'y' %}
[![PyPI](https://img.shields.io/pypi/v/{{ cookiecutter.project_slug }})](https://pypi.python.org/pypi/{{ cookiecutter.project_slug }})
[![Documentation](https://img.shields.io/badge/docs-gh--pages-blue.svg)](https://{{ cookiecutter.github_username }}.github.io/{{ cookiecutter.project_slug }}/)
[![Docs]({{ github_project_root }}/actions/workflows/docs.yml/badge.svg?branch={{ cookiecutter.main_branch }})]({{ github_project_root }}/actions?query=workflow%3ADocs)
{%- endif %}
[![Tests]({{ github_project_root }}/actions/workflows/test.yml/badge.svg?branch={{ cookiecutter.main_branch }})]({{ github_project_root }}/actions?query=workflow%3ATests)
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
```

```{toctree}
:maxdepth: 2
:caption: Getting Started

Installation & Usage <readme>
```

```{toctree}
:maxdepth: 2
:caption: API Reference
:glob:

apidocs/{{ cookiecutter.project_slug }}/*
```

```{toctree}
:maxdepth: 2
:caption: Development

contributing
authors
changelog
```

## Indices

* {ref}`genindex`
* {ref}`modindex`
