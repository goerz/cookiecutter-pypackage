"""Top-level package for Python Boilerplate."""

from importlib.metadata import version


__version__ = version("python_boilerplate")

# All members whose name does not start with an underscore must be listed
# either in __all__ or in __private__
__all__ = ['hello_world']
__private__ = []


def hello_world(name="World"):
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
    return f"Hello, {name}!"
