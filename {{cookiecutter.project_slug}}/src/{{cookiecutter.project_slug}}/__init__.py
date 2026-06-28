"""Top-level package for {{ cookiecutter.project_name }}."""

from importlib.metadata import version


__version__ = version("{{ cookiecutter.project_slug }}")

# All members whose name does not start with an underscore must be listed
# either in __all__ or in __private__
{%- if cookiecutter.sphinx_docs == 'y' %}
__all__ = ['hello_world']
{%- else %}
__all__ = []
{%- endif %}
__private__ = []
{%- if cookiecutter.sphinx_docs == 'y' %}


def hello_world(name="World"):
{%- if cookiecutter.markdown_docs == 'y' and cookiecutter.markdown_docstrings == 'y' %}
    """Return a friendly greeting.

    This example function demonstrates how a [MyST] docstring is rendered on
    the auto-generated **API** page. Replace it with your own public API, and
    keep every public name listed in `__all__`.

    Arguments:

    - `name`: the name to greet. Defaults to `"World"`.

    Returns the greeting `"Hello, {name}!"`:

    ```python
    >>> hello_world("Alice")
    'Hello, Alice!'

    ```

    [MyST]: https://mystmd.org/guide/typography
    """
{%- elif cookiecutter.markdown_docs == 'y' %}
    """Return a friendly greeting.

    This example function demonstrates how a plain reStructuredText docstring
    is rendered on the auto-generated **API** page. Replace it with your own
    public API, and keep every public name listed in ``__all__``.

    :param name: The name to greet. Defaults to ``"World"``.
    :type name: str
    :returns: The greeting ``"Hello, {name}!"``.
    :rtype: str

    Example::

        >>> hello_world("Alice")
        'Hello, Alice!'

    """
{%- else %}
    """Return a friendly greeting.

    This example function demonstrates how a `reStructuredText`_ docstring
    with `Napoleon`_ Google-style sections is rendered on the auto-generated
    **API** page. Replace it with your own public API, and keep every public
    name listed in ``__all__``.

    Args:
        name: The name to greet. Defaults to ``"World"``.

    Returns:
        The greeting ``"Hello, {name}!"``.

    Example:
        >>> hello_world("Alice")
        'Hello, Alice!'

    .. _reStructuredText: https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
    .. _Napoleon: https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
    """
{%- endif %}
    return f"Hello, {name}!"
{%- endif %}
