"""The module inside the sub-package."""

__all__ = ['x', 'PROJECT_CONST']
__private__ = ['y']


PROJECT_CONST = 2
"""An integer constant."""


def x(a):
    """Function x of `a`."""
    return a + 1


def y(a):
    """Function not exported in ``__all__``."""
    return a


def _z(a):
    """A private function."""
    return None
