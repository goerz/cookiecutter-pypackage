# Python Boilerplate

[![Source code on Github](https://img.shields.io/badge/goerz-python__boilerplate-blue.svg?logo=github)][Github]
<!--Not on PyPI-->
<!--No online documentation-->
<!--No documentation workflow-->
[![Tests](https://github.com/goerz/python_boilerplate/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/goerz/python_boilerplate/actions?query=workflow%3ATests)
[![Coverage](https://codecov.io/gh/goerz/python_boilerplate/branch/master/graph/badge.svg)](https://codecov.io/gh/goerz/python_boilerplate)
[![BSD License](https://img.shields.io/badge/License-BSD-green.svg)](https://opensource.org/licenses/BSD-3-Clause)

Python Boilerplate contains all the boilerplate you need to create a Python package.

Development of Python Boilerplate happens on [Github][].


## Installation

To install the latest development version from [Github][]:

```
pip install git+https://github.com/goerz/python_boilerplate.git@master#egg=python_boilerplate
```


**Note:** Python Boilerplate is currently not released on the [Python Package Index](https://pypi.org), so you will not be able to install it with `pip install <package name>`.

## Usage

To use Python Boilerplate in a Python project:

``` python
import python_boilerplate
```

## Development

The project uses [uv](https://docs.astral.sh/uv/) to manage the development environment and [`make`](https://www.gnu.org/software/make/) as a task runner. After cloning the repository, run

```
make develop
```

to create a virtual environment with all development dependencies. Run `make help` for an overview of available targets, and see [CONTRIBUTING.md][] for full contributing guidelines.

To set a debugger breakpoint, use Python's built-in `breakpoint()`. The development environment includes [ipdb](https://github.com/gotcha/ipdb); activate it by setting the environment variable:

```
export PYTHONBREAKPOINT=ipdb.set_trace
```

[Github]: https://github.com/goerz/python_boilerplate
[CONTRIBUTING.md]: https://github.com/goerz/python_boilerplate/blob/master/CONTRIBUTING.md
