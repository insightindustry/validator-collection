# -*- coding: utf-8 -*-

"""
*******************
tests.conftest
*******************

Utility functions that are used to configure Py.Test context.

"""

import abc
import collections
import os

import pytest
from validator_collection._compat import is_py2

if is_py2:
    Iterable = collections.Iterable
else:
    Iterable = collections.abc.Iterable


def pytest_addoption(parser):
    """Define options that the parser looks for in the command-line.

    Pattern to use::

      parser.addoption("--cli-option",
                       action="store",
                       default=None,
                       help="cli-option: help text goes here")

    """
    # pylint: disable=unused-argument
    pass


def pytest_runtest_makereport(item, call):
    """Connect current incremental test to its preceding parent."""
    # pylint: disable=W0212
    if "incremental" in item.keywords:
        if call.excinfo is not None:
            parent = item.parent
            parent._previousfailed = item


def pytest_runtest_setup(item):
    """Fail test if preceding incremental test failed."""
    if "incremental" in item.keywords:
        previousfailed = getattr(item.parent, "_previousfailed", None)
        if previousfailed is not None:
            pytest.xfail(
                "previous test failed (%s) for reason: %s" % (previousfailed.name,
                                                              previousfailed))


class State(object):
    """Class to hold incremental test state."""
    # pylint: disable=too-few-public-methods
    pass


@pytest.fixture
def state(request):
    """Return the :class:`State` object that holds incremental test state."""
    # pylint: disable=W0108
    return request.cached_setup(
        setup = lambda: State(),
        scope = "session"
    )


def _add_metaclass(metaclass):
    """Class decorator for creating a class with a metaclass."""
    def wrapper(cls):
        """
        Decor for a metaclass.

        Args:
            cls: (todo): write your description
        """
        orig_vars = cls.__dict__.copy()
        slots = orig_vars.get('__slots__')
        if slots is not None:
            if isinstance(slots, str):
                slots = [slots]
            for slots_var in slots:
                orig_vars.pop(slots_var)
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)

        return metaclass(cls.__name__, cls.__bases__, orig_vars)

    return wrapper


@_add_metaclass(abc.ABCMeta)
class MetaClassParentType(object):
    """The parent meta class object."""
    pass

class MetaClassType(MetaClassParentType):
    """The child meta class type."""
    pass


class GetItemIterable(object):
    """A class that does not have a ``__iter__`` method, but does use
    ``__getitem__``."""

    items = (1, 2, 3, 4)

    def __getitem__(self, key):
        """
        Returns the value of a given key.

        Args:
            self: (todo): write your description
            key: (str): write your description
        """
        return self.items[key]


class IterIterable(object):
    """A class that has an ``__iter__`` method."""

    def __iter__(self):
        """
        Returns an iterator over the iterable.

        Args:
            self: (todo): write your description
        """
        return self

    def __next__(self):
        """
        Returns the next iteration.

        Args:
            self: (todo): write your description
        """
        raise StopIteration()

    def next(self):
        """
        Returns the next item

        Args:
            self: (todo): write your description
        """
        return self.__next__()

class IterableIterable(Iterable):
    """A class that inherits from ``Iterable``."""

    def __iter__(self):
        """
        Returns an iterator over the iterable.

        Args:
            self: (todo): write your description
        """
        return self

    def __next__(self):
        """
        Returns the next iteration.

        Args:
            self: (todo): write your description
        """
        raise StopIteration()

    def next(self):
        """
        Returns the next item

        Args:
            self: (todo): write your description
        """
        return self.__next__()


class FalseIterable(Iterable):
    """A class that inherits from ``Iterable``."""

    def __iter__(self):
        """
        Returns an iterable of iterable.

        Args:
            self: (todo): write your description
        """
        raise AttributeError('this simulates an AttributeError')
