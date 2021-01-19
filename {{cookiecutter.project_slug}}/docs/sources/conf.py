# -*- coding: utf-8 -*-
import datetime
import os
import sys
from pathlib import Path

import git
from m2r import MdInclude

import {{ cookiecutter.project_slug }}


DOCS_SOURCES = Path(__file__).parent
ROOT = DOCS_SOURCES / '..' / '..'  # project root

sys.path.insert(0, os.path.abspath('_extensions'))

# -- Generate API documentation ------------------------------------------------


{%- if cookiecutter.better_apidoc == 'y' %}
def run_apidoc(app):
    """Generage API documentation"""
    import better_apidoc

    better_apidoc.APP = app
    better_apidoc.main(
        [
            'better-apidoc',
            '-t',
            str(DOCS_SOURCES / '_templates'),
            '--force',
            '--no-toc',
            '--separate',
            '-o',
            str(DOCS_SOURCES / 'API'),
            os.path.join(ROOT / 'src' / '{{ cookiecutter.project_slug }}'),
        ]
    )
{%- endif %}


# -- General configuration -----------------------------------------------------

# Report broken links as warnings
nitpicky = True
nitpick_ignore = [('py:class', 'callable')]

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosummary',
    'sphinx.ext.extlinks',
    'sphinx.ext.ifconfig',
    'sphinx.ext.todo',
    'sphinx.ext.inheritance_diagram',
    'sphinx_copybutton',
    'dollarmath',
    'sphinx_autodoc_typehints',
{%- if cookiecutter.sphinx_docs == 'y' %}
    'doctr_versions_menu',
{%- endif %}
]

if os.getenv('SPELLCHECK'):
    extensions.append('sphinxcontrib.spelling')
    spelling_show_suggestions = True
    spelling_lang = os.getenv('SPELLCHECK')
    spelling_word_list_filename = 'spelling_wordlist.txt'
    spelling_ignore_pypi_package_names = True

intersphinx_mapping = {
    'python': ('https://docs.python.org/{{ cookiecutter.main_python }}', None),
    'sympy': ('https://docs.sympy.org/latest/', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/reference/', None),
    'numpy': ('https://docs.scipy.org/doc/numpy/', None),
    'matplotlib': ('https://matplotlib.org/', None),
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

source_suffix = '.rst'
master_doc = 'index'
project = {{ '{0!r}'.format(cookiecutter.project_name) }}
year = str(datetime.datetime.now().year)
author = {{ '{0!r}'.format(cookiecutter.full_name) }}
copyright = '{0}, {1}'.format(year, author)
version = {{ cookiecutter.project_slug }}.__version__
release = version
git_tag = "v%s" % version
if version.endswith('dev'):
    try:
        last_commit = str(git.Repo(ROOT).head.commit)[:7]
        release = "%s (%s)" % (version, last_commit)
        git_tag = str(git.Repo(ROOT).head.commit)
    except git.exc.InvalidGitRepositoryError:
        git_tag = "master"
numfig = True

pygments_style = 'friendly'
extlinks = {
    'issue': ('https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/issues/%s', '#'),
    'pr': ('https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/pull/%s', 'PR #'),
}

# autodoc settings
autoclass_content = 'both'
autodoc_member_order = 'bysource'
autodoc_mock_imports = []  # e.g.: 'numpy', 'scipy', ...


html_last_updated_fmt = '%b %d, %Y'
html_split_index = False
html_sidebars = {'**': ['searchbox.html', 'globaltoc.html', 'sourcelink.html']}
html_short_title = '%s-%s' % (project, version)

{% raw %}
# Mathjax settings
mathjax_path = (
    'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.6/MathJax.js'
)
mathjax_config = {
    'extensions': ['tex2jax.js'],
    'jax': ['input/TeX', 'output/SVG'],
    'TeX': {
        'extensions': ["AMSmath.js", "AMSsymbols.js"],
        'Macros': {
            'Re': ['{\\operatorname{Re}}', 0],
            'Im': ['{\\operatorname{Im}}', 0],
            'Real': ['{\\mathbb{R}}', 0],
            'Complex': ['{\\mathbb{C}}', 0],
            'Integer': ['{\\mathbb{N}}', 0],
        },
    },
}
{% endraw %}

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# -- Monkeypatch for instance attribs (sphinx bug #2044) -----------------------

from sphinx.ext.autodoc import (
    ClassLevelDocumenter,
    InstanceAttributeDocumenter,
)


def iad_add_directive_header(self, sig):
    ClassLevelDocumenter.add_directive_header(self, sig)


InstanceAttributeDocumenter.add_directive_header = iad_add_directive_header

# -- Options for HTML output ---------------------------------------------------

# on_rtd is whether we are on readthedocs.org, this line of code grabbed from
# docs.readthedocs.org
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
if not on_rtd:  # only import and set the theme if we're building docs locally
    import sphinx_rtd_theme

    html_theme = "sphinx_rtd_theme"
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
# html_theme = 'sphinxdoc'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    'collapse_navigation': True,
    'display_version': True,
    'navigation_depth': 4,
}

# Add any paths that contain custom themes here, relative to this directory.
# html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
# html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
# html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
# html_favicon = 'favicon.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# JavaScript filenames, relative to html_static_path
html_js_files = []

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
# html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
# html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
# html_additional_pages = {}

# If false, no module index is generated.
# html_domain_indices = True

# If false, no index is generated.
# html_use_index = True

# If true, the index is split into individual pages for each letter.
# html_split_index = False

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = False

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
# html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
# html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = None

nbsphinx_prolog = r"""
{%- raw %}
{% set docname = env.doc2path(env.docname, base='docs') %}
{%- endraw %}

.. only:: html

    .. role:: raw-html(raw)
        :format: html

    :raw-html:`<a href="http://nbviewer.jupyter.org/github/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/blob/<<GIT_TAG>>/{%- raw -%}{{ docname }}{%- endraw -%}" target="_blank"><img alt="Render on nbviewer" src="https://img.shields.io/badge/render%20on-nbviewer-orange.svg" style="vertical-align:text-bottom"></a>&nbsp;<a href="https://mybinder.org/v2/gh/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/<<GIT_TAG>>?filepath={%- raw -%}{{ docname }}{%- endraw -%}}" target="_blank"><img alt="Launch Binder" src="https://mybinder.org/badge_logo.svg" style="vertical-align:text-bottom"></a>`
""".replace(
    '<<GIT_TAG>>', git_tag
)

# -- Options for LaTeX output -------------------------------------------------

# latex_engine = 'lualatex'
latex_elements = {
    'preamble': r'''
\usepackage[titles]{tocloft}
\cftsetpnumwidth {1.25cm}\cftsetrmarg{1.5cm}
\setlength{\cftchapnumwidth}{0.75cm}
\setlength{\cftsecindent}{\cftchapnumwidth}
\setlength{\cftsecnumwidth}{1.25cm}
\usepackage{emptypage}
''',
    'fncychap': r'\usepackage[Bjornstrup]{fncychap}',
    'printindex': r'\footnotesize\raggedright\printindex',
    'babel': '',
}
latex_show_urls = 'no'

# -----------------------------------------------------------------------------

{%- if cookiecutter.better_apidoc == 'y' %}


def setup(app):
    app.connect('builder-inited', run_apidoc)
    # from m2r to make `mdinclude` work
    app.add_config_value('no_underscore_emphasis', False, 'env')
    app.add_config_value('m2r_parse_relative_links', False, 'env')
    app.add_config_value('m2r_anonymous_references', False, 'env')
    app.add_config_value('m2r_disable_inline_math', False, 'env')
    app.add_directive('mdinclude', MdInclude)

{%- endif %}
