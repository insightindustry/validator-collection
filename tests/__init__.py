# -*- coding: utf-8 -*-

"""
************************
Testing Philosophy
************************

.. note::

  Unit tests for the **PDF Layer Extractor** are written using `pytest`_ and
  a comprehensive set of test automation are provided by `tox`_.

There are many schools of thought when it comes to test design. When building
the **Validator Collection**, we decided to focus on practicality. That means:

  * **DRY is good, KISS is better.** To avoid repetition, our test suite makes
    extensive use of fixtures, parametrization, and decorator-driven behavior.
    This minimizes the number of test functions that are nearly-identical.
    However, there are certain elements of code that are repeated in almost all test
    functions, as doing so will make future readability and maintenance of the
    test suite easier.
  * **Coverage matters...kind of.** We have documented the primary intended
    behavior of every function in the **Validator Collection** library, and the
    most-likely failure modes that can be expected.  At the time of writing, we
    have about 80% code coverage. Yes, yes: We know that is less than 100%. But
    there are edge cases which are almost impossible to bring about, based on
    confluences of factors in the wide world. Our goal is to test the key
    functionality, and as bugs are uncovered to add to the test functions as
    necessary.

************************
Test Organization
************************

Each individual test module (e.g. ``test_validators.py``) corresponds to a
conceptual grouping of functionality. For example:

* ``test_validators.py`` tests validator functions found in
  ``validator_collection/_validators.py``

Certain test modules are tightly coupled, as the behavior in one test module may
have implications on the execution of tests in another. These test modules use
a numbering convention to ensure that they are executed in their required order,
so that ``test_1_NAME.py`` is always executed before
``test_2_NAME.py``.

**************************************
Configuring & Running Tests
**************************************

Installing with the Test Suite
=================================

.. tabs::

  ..tab:: Installing via pip

    .. code-block:: bash

      $ pip install validator-collection[tests]

  .. tab:: From Local Development Environment

    .. seealso::

      When you
      :ref:`create a local development environment <preparing-development-environment>`,
      all dependencies for running and extending the test suite are installed.

Command-line Options
=====================

The test suite exposes a number of command-line options that are used to configure
the context in which the **Validator Collection** is to be tested. These options are:

.. todo::

  Update the CLI options.


* CLI OPTIONS GO HERE

In order for a test function to accept these options, they should have an argument
whose name matches the command-line option minus the ``--`` prefix, with ``-``
replaced by ``_``. Thus: ``--keep-db`` becomes ``keep_db``. Options that
are IDs should then receive a suffix of ``_id``.

.. tip::

  For a full list of the CLI options available, try:

  .. code-block:: bash

    validator-collection $ cd tests/
    validator-collection/tests/ $ pytest --help

Configuration File
===================

Because it can be tedious to constantly type or copy/paste lots of options into
your terminal to run tests, we have prepared a ``pytest.ini`` file in the
``tests/`` directory that will automatically apply default CLI options when you
run the test suite.

Of course, you can override any of these default CLI options using the command
line directly.

Running Tests
==============

.. tabs::

  .. tab:: Using ``pytest.ini``

    To run the entire test suite:

    .. code-block:: bash

      tests/ $ pytest

    To run a specific test module:

    .. code-block:: bash

      tests/ $ pytest tests/test_module.py

    To run a specific test function::

    .. code-block: bash

      tests/ $ pytest tests/test_module.py -k 'test_my_test_function'

*****************
Skipping Tests
*****************

.. todo::

  Update skipping logic

Tests that rely on command-line options will be skipped if those command-line
options are not supplied. To ensure that a test gets skipped correctly, you can
decorate the test with the following::

    @pytest.mark.            # Skips if keep_db is falsey

*******************
Incremental Tests
*******************

A variety of test functions are designed to test related functionality. As a
result, they are designed to execute incrementally. In order to execute tests
incrementally, they need to be defined as methods within a class that you decorate
with the ``@pytest.mark.incremental`` decorator as shown below::

    @pytest.mark.incremental
    class TestIncremental(object):
        def test_function1(self):
            pass
        def test_modification(self):
            assert 0
        def test_modification2(self):
            pass

This class will execute the ``TestIncremental.test_function1()`` test, execute and
fail on the ``TestIncremental.test_modification()`` test, and automatically fail
``TestIncremental.test_modification2()`` because of the ``.test_modification()``
failure.

To pass state between incremental tests, add a ``state`` argument to their method
definitions. For example::

    @pytest.mark.incremental
    class TestIncremental(object):
        def test_function(self, state):
            state.is_logged_in = True
            assert state.is_logged_in = True
        def test_modification1(self, state):
            assert state.is_logged_in is True
            state.is_logged_in = False
            assert state.is_logged_in is False
        def test_modification2(self, state):
            assert state.is_logged_in is True

Given the example above, the third test (``test_modification2``) will fail because
``test_modification`` updated the value of ``state.is_logged_in``.

.. note::

  ``state`` is instantiated at the level of the entire test session (one run of
  the test suite). As a result, it can be affected by tests in other test modules.

.. target-notes::

.. _`pytest`: https://docs.pytest.org/en/latest/
.. _`mocks`: https://en.wikipedia.org/wiki/Mock_object
.. _`stubs`: https://en.wikipedia.org/wiki/Test_stub
"""
