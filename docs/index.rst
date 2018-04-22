.. Validator Collection documentation master file, created by
   sphinx-quickstart on Sat Apr 14 11:13:03 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

####################################################
Validator Collection
####################################################

**Python library of 60+ commonly-used validator functions**

.. |strong| raw:: html

  <strong>

.. |/strong| raw:: html

  </strong>

.. sidebar:: Version Compatability

  The **Validator Collection** is designed to be compatible with Python 2.7 and
  Python 3.4 or higher.

.. include:: _unit_tests_code_coverage.rst

.. toctree::
  :hidden:
  :maxdepth: 2
  :caption: Contents:

  Home <self>
  Validator Reference <validators>
  Checker Reference <checkers>
  Error Reference <errors>
  Contributor Guide <contributing>
  Testing Reference <testing>
  Release History <history>
  Glossary <glossary>

The **Validator Collection** is a Python library that provides more than 60
functions that can be used to validate the type and contents of an input value.

Each function has a consistent syntax for easy use, and has been tested on
Python 2.7, 3.4, 3.5, and 3.6.

For a list of validators available, please see the lists below.

.. contents::
  :depth: 3
  :backlinks: entry

***************
Installation
***************

To install the **Validator Collection**, just execute:

.. code:: bash

  $ pip install validator-collection

Dependencies
==============

.. include:: _dependencies.rst

***********************************
Available Validators and Checkers
***********************************

.. tabs::

  .. tab:: Validators

    .. include:: _validator_list.rst

  .. tab:: Checkers

    .. include:: _checker_list.rst


************************************
Hello, World and Standard Usage
************************************

All validator functions have a consistent syntax so that using them is pretty
much identical. Here's how it works:

.. code-block:: python

  from validator_collection import validators, checkers, errors

  email_address = validators.email('test@domain.dev')
  # The value of email_address will now be "test@domain.dev"

  email_address = validators.email('this-is-an-invalid-email')
  # Will raise a ValueError

  try:
      email_address = validators.email(None)
      # Will raise an EmptyValueError
  except errors.EmptyValueError:
      # Handling logic goes here
  except errors.InvalidEmailError:
      # More handlign logic goes here

  email_address = validators.email(None, allow_empty = True)
  # The value of email_address will now be None

  email_address = validators.email('', allow_empty = True)
  # The value of email_address will now be None

  is_email_address = checkers.is_email('test@domain.dev')
  # The value of is_email_address will now be True

  is_email_address = checkers.is_email('this-is-an-invalid-email')
  # The value of is_email_address will now be False

  is_email_address = checkers.is_email(None)
  # The value of is_email_address will now be False

Pretty simple, right? Let's break it down just in case: Each validator comes in
two flavors: a :term:`validator` and a :term:`checker`.

.. _validators-explained:

Using Validators
==================

.. include:: _using_validators.rst

.. _checkers-explained:

Using Checkers
================

.. include:: _using_checkers.rst

.. _best-practices:

*****************
Best Practices
*****************

:ref:`Checkers <checkers-explained>` and :ref:`Validators <validators-explained>`
are designed to be used together. You can think of them as a way to quickly and
easily verify that a value contains the information you expect, and then make
sure that value is in the form your code needs it in.

There are two fundamental patterns that we find work well in practice.

Defensive Approach: Check, then Convert if Necessary
=======================================================

We find this pattern is best used when we don't have any certainty over a given
value might contain. It's fundamentally defensive in nature, and applies the
following logic:

#. Check whether ``value`` contains the information we need it to or can be
   converted to the form we need it in.
#. If ``value`` does not contain what we need but *can* be converted to what
   we need, do the conversion.
#. If ``value`` does not contain what we need but *cannot* be converted to what
   we need, raise an error (or handle it however it needs to be handled).

We tend to use this where we're first receiving data from outside of our control,
so when we get data from a user, from the internet, from a third-party API, etc.

Here's a quick example of how that might look in code:

.. code-block:: python

  from validator_collection import checkers, validators

  def some_function(value):
      # Check whether value contains a whole number.
      is_valid = checkers.is_integer(value,
                                     coerce_value = False)

      # If the value does not contain a whole number, maybe it contains a
      # numeric value that can be rounded up to a whole number.
      if not is_valid and checkers.is_integer(value, coerce_value = True):
          # If the value can be rounded up to a whole number, then do so:
          value = validators.integer(value, coerce_value = True)
      elif not is_valid:
          # Since the value does not contain a whole number and cannot be converted to
          # one, this is where your code to handle that error goes.
          raise ValueError('something went wrong!')

      return value

  value = some_function(3.14)
  # value will now be 4

  new_value = some_function('not-a-number')
  # will raise ValueError

Let's break down what this code does. First, we define ``some_function()`` which
takes a value. This function uses the
:func:`is_integer() <validator_collection.checkers.is_integer>`
checker to see if ``value`` contains a whole number, regardless of its type.

If it doesn't contain a whole number, maybe it contains a numeric value that can
be rounded up to a whole number? It again uses the
:func:`is_integer() <validator_collection.checkers.is_integer>` to check if that's
possible. If it is, then it calls the
:func:`integer() <validator_collection.validators.integer>` validator to coerce
``value`` to a whole number.

If it can't coerce ``value`` to a whole number? It raises a
:class:`ValueError <python:ValueError>`.


Confident Approach: try ... except
=====================================

Sometimes, we'll have more confidence in the values that we can expect to work
with. This means that we might expect ``value`` to *generally* have the kind of
data we need to work with. This means that situations where ``value`` doesn't
contain what we need will truly be exceptional situations, and can be handled
accordingly.

In this situation, a good approach is to apply the following logic:

#. Skip a :term:`checker` entirely, and just wrap the validator in a
   ``try...except`` block.

We tend to use this in situations where we're working with data that our own
code has produced (meaning we know - generally - what we can expect, unless
something went seriously wrong).

Here's an example:

.. code-block:: python

  from validator_collection import validators, errors

  def some_function(value):
      try:
          email_address = validators.email(value, allow_empty = False)
      except errors.InvalidEmailError as error:
          # handle the error here
      except ValueError as error:
          # handle other ValueErrors here

      # do something with your new email address value

      return email_address

  email = some_function('email@domain.com')
  # This will return the email address.

  email = some_function('not-a-valid-email')
  # This will raise a ValueError that some_function() will handle.

  email = some_function(None)
  # This will raise a ValueError that some_function() will handle.

So what's this code do? It's pretty straightforward. ``some_function()`` expects
to receive a ``value`` that contains an email address. We expect that ``value``
will *typically* be an email address, and not something weird (like a number or
something). So we just try the validator - and if validation fails, we handle
the error appropriately.

*********************
Questions and Issues
*********************

You can ask questions and report issues on the project's
`Github Issues Page <https://github.com/insightindustry/validator-collection/issues>`_

*********************
Contributing
*********************

We welcome contributions and pull requests! For more information, please see the
:doc:`Contributor Guide <contributing>`

*********************
Testing
*********************

We use `TravisCI <http://travisci.org>`_ for our build automation and
`ReadTheDocs <https://readthedocs.org>`_ for our documentation.

Detailed information about our test suite and how to run tests locally can be
found in our :doc:`Testing Reference <testing>`.

**********************
License
**********************

The **Validator Collection** is made available on a **MIT License**.

********************
Indices and tables
********************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
