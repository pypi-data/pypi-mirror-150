# SPDX-License-Identifier: 0BSD
# Copyright 2019 Alexander Kozhevnikov <mentalisttraceur@gmail.com>

"""Context managers for controlling exception chaining.

Provides a different way of controling exception chaining
(the implicit ``__context__`` and explicit ``__cause__``)
beyond just ``raise ... from ...``.
"""

__version__ = '1.0.9'
__all__ = ('context', 'cause', 'suppress_context')


class _ExceptionContext(object):
    """Context manager that sets an attribute on exceptions raised in it."""

    def __init__(self, attribute, value):
        self._attribute = attribute
        self._value = value

    def __repr__(self):
        return self._attribute[2:-2] + '(' + repr(self._value) + ')'

    def __enter__(self):
        return None

    def __exit__(self, exception_type, exception, traceback):
        if exception is not None:
            try:
                setattr(exception, self._attribute, self._value)
            except AttributeError:
                pass
        return False


def context(context):
    """Create context manager that sets ``__context__`` on exceptions.

    Arguments:
        context: The exception to set as the context of exceptions
            raised inside this context manager.

    Returns:
        ContextManager: The manager to be used in a ``with`` statement.
    """
    return _ExceptionContext('__context__', context)


def cause(cause):
    """Create context manager that sets ``__cause__`` on exceptions.

    Arguments:
        cause: The exception to set as the cause of exceptions
            raised inside this context manager.

    Returns:
        ContextManager: The manager to be used in a ``with`` statement.
    """
    return _ExceptionContext('__cause__', cause)


def suppress_context(suppress):
    """Create context manager that sets ``__suppress_context__`` on exceptions.

    Arguments:
        suppress (bool): Whether to suppress context printing
            on exceptions raised within this context manager.

    Returns:
        ContextManager: The manager to be used in a ``with`` statement.
    """
    return _ExceptionContext('__suppress_context__', suppress)
