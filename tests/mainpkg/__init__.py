"""Top-level package."""

__version__ = '0.1.0-dev'

__all__ = ['func', 'PROJECT_CONST']
__private__ = []
__known_refs__ = {'PROJECT_CONST': ':obj:`~.subpkg.submod.PROJECT_CONST`'}

from .subpkg.submod import PROJECT_CONST


def func(a):
    """This is a function that just returns `a`."""
    return a
