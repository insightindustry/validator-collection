# -*- coding: utf-8 -*-

"""
*******************
tests.conftest
*******************

Utility functions that are used to configure Py.Test context.

"""

import os
import pytest


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
