*******************************************
Contributing to the Validator Collection
*******************************************

.. note::

  As a general rule of thumb, the **Validator Collection** applies
  :pep:`PEP 8 <8>` styling, with some important differences.

.. include:: _unit_tests_code_coverage.rst

.. sidebar:: What makes an API idiomatic?

  One of my favorite ways of thinking about idiomatic design comes from a `talk
  given by Luciano Ramalho at Pycon 2016`_ where he listed traits of a Pythonic
  API as being:

  * don't force [the user] to write boilerplate code
  * provide ready to use functions and objects
  * don't force [the user] to subclass unless there's a *very good* reason
  * include the batteries: make easy tasks easy
  * are simple to use but not simplistic: make hard tasks possible
  * leverage the Python data model to:

    * provide objects that behave as you expect
    * avoid boilerplate through introspection (reflection) and metaprogramming.


.. contents:: Contents:
  :local:
  :depth: 3

Design Philosophy
====================

The **Validator Collection** is meant to be a "beautiful" and "usable" library.
That means that it should offer an idiomatic API that:

* works out of the box as intended,
* minimizes "bootstrapping" to produce meaningful output, and
* does not force users to understand how it does what it does.

In other words:

.. pull-quote::

  Users should simply be able to drive the car without looking at the engine.

Style Guide
================

Basic Conventions
-------------------

* Do not terminate lines with semicolons.
* Line length should have a maximum of *approximately* 90 characters. If in doubt,
  make a longer line or break the line between clear concepts.
* Each class should be contained in its own file.
* If a file runs longer than 2,000 lines...it should probably be refactored and
  split.
* All imports should occur at the top of the file.

* Do not use single-line conditions:

  .. code-block:: python

    # GOOD
    if x:
      do_something()

    # BAD
    if x: do_something()

* When testing if an object has a value, be sure to use ``if x is None:`` or
  ``if x is not None``. Do **not** confuse this with ``if x:`` and ``if not x:``.
* Use the ``if x:`` construction for testing truthiness, and ``if not x:`` for
  testing falsiness. This is **different** from testing:

    * ``if x is True:``
    * ``if x is False:``
    * ``if x is None:``

* As of right now, because we feel that it negatively impacts readability and is
  less-widely used in the community, we are **not** using type annotations.

Naming Conventions
--------------------

* ``variable_name`` and not ``variableName`` or ``VariableName``. Should be a
  noun that describes what information is contained in the variable. If a ``bool``,
  preface with ``is_`` or ``has_`` or similar question-word that can be answered
  with a yes-or-no.
* ``function_name`` and not ``function_name`` or ``functionName``. Should be an
  imperative that describes what the function does (e.g. ``get_next_page``).
* ``CONSTANT_NAME`` and not ``constant_name`` or ``ConstantName``.
* ``ClassName`` and not ``class_name`` or ``Class_Name``.

Design Conventions
-------------------

* Functions at the module level can only be aware of objects either at a higher
  scope or singletons (which effectively have a higher scope).
* Functions and methods can use **one** positional argument (other than ``self``
  or ``cls``) without a default value. Any other arguments must be keyword
  arguments with default value given.

  .. code-block:: python

    def do_some_function(argument):
      # rest of function...

    def do_some_function(first_arg,
                         second_arg = None,
                         third_arg = True):
      # rest of function ...

* Functions and methods that accept values should start by validating their
  input, throwing exceptions as appropriate.
* When defining a class, define all attributes in ``__init__``.
* When defining a class, start by defining its attributes and methods as private
  using a single-underscore prefix. Then, only once they're implemented, decide
  if they should be public.
* Don't be afraid of the private attribute/public property/public setter pattern:

  .. code-block:: python

    class SomeClass(object):
      def __init__(*args, **kwargs):
        self._private_attribute = None

      @property
      def private_attribute(self):
        # custom logic which  may override the default return

        return self._private_attribute

      @setter.private_attribute
      def private_attribute(self, value):
        # custom logic that creates modified_value

        self._private_attribute = modified_value

* Separate a function or method's final (or default) ``return`` from the rest of
  the code with a blank line (except for single-line functions/methods).

Documentation Conventions
----------------------------

We are very big believers in documentation (maybe you can tell). To document
the **Validator Collection** we rely on several tools:

`Sphinx`_
^^^^^^^^^^^

`Sphinx`_ is used to organize the library's documentation into this lovely
readable format (which will also be published to `ReadTheDocs`_). This
documentation is written in `reStructuredText`_ files which are stored in
``<project>/docs``.

.. tip::
  As a general rule of thumb, we try to apply the `ReadTheDocs`_ own
  `Documentation Style Guide`_ to our `RST <reStructuredText>`_ documentation.

.. hint::

  To build the HTML documentation locally:

  #. In a terminal, navigate to ``<project>/docs``.
  #. Execute ``make html``.

  When built locally, the HTML output of the documentation will be available at
  ``./docs/_build/index.html``.

Docstrings
^^^^^^^^^^^
* Docstrings are used to document the actual source code itself. When
  writing docstrings we adhere to the conventions outlined in :pep:`257`.

.. _dependencies:

Dependencies
==============

.. include:: _dependencies.rst

.. _preparing-development-environment:

Preparing Your Development Environment
=========================================

In order to prepare your local development environment, you should:

#. Fork the `Git repository <https://github.com/insightindustry/validator-collection>`_.
#. Clone your forked repository.
#. Set up a virtual environment (optional).
#. Install dependencies:

  .. code-block:: bash

    validator-collection/ $ pip install -r requirements.txt

And you should be good to go!

Ideas and Feature Requests
============================

Check for open `issues <https://github.com/insightindustry/validator-collection/issues>`_
or create a new issue to start a discussion around a bug or feature idea.

Testing
=========

If you've added a new feature, we recommend you:

  * create local unit tests to verify that your feature works as expected, and
  * run local unit tests before you submit the pull request to make sure nothing
    else got broken by accident.

.. seealso::

  For more information about the **Validator Collection** testing approach please
  see: :doc:`Testing the Validator Collection <testing>`

Submitting Pull Requests
===========================

After you have made changes that you think are ready to be included in the main
library, submit a pull request on Github and one of our developers will review
your changes. If they're ready (meaning they're well documented, pass unit tests,
etc.) then they'll be merged back into the main repository and slated for inclusion
in the next release.

Building Documentation
=========================

In order to build documentation locally, you can do so from the command line using:

.. code-block:: bash

  validator-collection/ $ cd docs
  validator-collection/docs $ make html

When the build process has finished, the HTML documentation will be locally
available at:

.. code-block:: bash

  validator-collection/docs/_build/html/index.html

.. note::

  Built documentation (the HTML) is **not** included in the project's Git
  repository. If you need local documentation, you'll need to build it.

Contributors
================

Thanks to everyone who helps make the **Validator Collection** useful:

.. include:: _contributors.rst

References
=============

.. target-notes::

.. _`Sphinx`: http://sphinx-doc.org
.. _`ReadTheDocs`: https://readthedocs.org
.. _`reStructuredText`: http://www.sphinx-doc.org/en/stable/rest.html
.. _`Documentation Style Guide`: http://documentation-style-guide-sphinx.readthedocs.io/en/latest/style-guide.html
.. _`talk given by Luciano Ramalho at PyCon 2016`: https://www.youtube.com/watch?v=k55d3ZUF3ZQ
.. _`Python 2.7`: https://www.python.org/downloads/
