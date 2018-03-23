Welcome to {{ cookiecutter.project_name }}'s documentation!
==========={%- for _ in cookiecutter.project_name -%}={%- endfor -%}=================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   readme
   contributing
   {% if cookiecutter.create_author_file == 'y' -%}authors
   {% endif -%}history


API
===

.. toctree::
   :maxdepth: 1

   API of the {{ cookiecutter.project_name }} package <API/{{ cookiecutter.project_slug }}>

Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
