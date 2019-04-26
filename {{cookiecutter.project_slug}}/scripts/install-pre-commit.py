{%- if cookiecutter.support_py37 == 'y' -%}
  {%- set latest_venv = '.venv/py37' -%}
  {%- set latest_test_target = 'test37' -%}
{%- elif cookiecutter.support_py36 == 'y' %}
  {%- set latest_venv = '.venv/py36' -%}
  {%- set latest_test_target = 'test36' -%}
{%- elif cookiecutter.support_py35 == 'y' %}
  {%- set latest_venv = '.venv/py35' -%}
  {%- set latest_test_target = 'test35' -%}
{%- else %}
  {%- set latest_venv = '.venv/py34' -%}
  {%- set latest_test_target = 'test34' -%}
{%- endif -%}
#!/usr/bin/env python
"""Install the pre-commit hooks

This should be run from the Makefile immediately after creating {{ latest_venv }}
"""
import os


if not os.path.isdir("{{ latest_venv }}"):
    os.system("make {{ latest_venv }}/bin/python")

if os.path.isdir(".git") and not os.path.isfile(".git/hooks/pre-commit"):
    print("##################################################################")
    print("Installing pre-commit hooks")
    print("##################################################################")
    os.system("{{ latest_venv }}/bin/pre-commit install")
