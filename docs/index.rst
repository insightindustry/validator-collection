.. Validator Collection documentation master file, created by
   sphinx-quickstart on Sat Apr 14 11:13:03 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

####################################################
Validator Collection
####################################################

**Python library of commonly-used validator functions**

.. |strong| raw:: html

  <strong>

.. |/strong| raw:: html

  </strong>

.. sidebar:: Version Compatability

  The **Validator Collection** is designed to be compatible with Python 2.7 and
  Python 3.4 and higher.

  Most validator functions will work on earlier versions as well, however certain
  validator functions will raise a :class:`NotImplementedError` if they are
  not supported in your Python environment.

.. toctree::
  :hidden:
  :maxdepth: 2
  :caption: Contents:

  Home <self>
  Validator Reference <validators>
  Checker Reference <checkers>
  Contributing <contributing>
  Testing Reference <testing>
  Glossary <glossary>

The **Validator Collection** is a Python library that provides more than 60
functions that can be used to validate the type and contents of an input value.

Each function has a consistent syntax for easy use, and has been tested on
Python 2.7, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, and 3.6.

For a list of validators available, please see the table of contents below.

.. contents::
  :depth: 3
  :backlinks: entry

***************
Installation
***************

To install the **Validator Collection**, just execute:

.. code:: bash

  $ pip install validator-collection

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

  import validator_collection.validators as validators
  import validator_collection.checkers as checkers

  email_address = validators.email('test@domain.dev')
  # The value of email_address will now be "test@domain.dev"

  email_address = validators.email('this-is-an-invalid-email')
  # Will raise a ValueError

  email_address = validators.email(None)
  # Will raise a ValueError

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
A validator does what it says on the tin: It validates that an input value is
what you think it should be, and returns its valid form.

Each validator is expressed as the name of the thing being validated, for example
:func:`email() <validator_collection.validators.email>`.

Each validator accepts a value as its first argument, and an optional ``allow_empty``
boolean as its second argument. For example:

.. code-block:: python

  email_address = validators.email(value, allow_empty = True)

If the value you're validating validates successfully, it will be returned. If
the value you're validating needs to be coerced to a different type, the
validator will try to do that. So for example:

.. code-block:: python

  validators.integer(1)
  validators.integer('1')

will both return an ``int`` of ``1``.

If the value you're validating is empty/falsey and ``allow_empty`` is ``False``,
then the validator will raise a :class:`ValueError` exception. If ``allow_empty``
is ``True``, then an empty/falsey input value will be convertd to a :class:`None <python:None>`
value.

.. caution::

  By default, ``allow_empty`` is always set to ``False``.

If the value you're validating fails its validation for some reason, the validator
may raise different exceptions depending on the reason. In most cases, this will
be a :class:`ValueError` though it can sometimes be a :class:`TypeError`, or an
:class:`AttributeError`, etc. For specifics on each validator's likely exceptions
and what can cause them, please review the :doc:`Validator Reference <validators>`.

.. hint::

  Some validators (particularly numeric ones like
  :func:`integer <validator_collection.validators.integer>`) have additional
  options which are used to make sure the value meets criteria that you set for
  it. These options are always included as keyword arguments *after* the
  ``allow_empty`` argument, and are documented for each validator below.

.. _checkers-explained:

Using Checkers
================

Likewise, a :term:`checker` is what it sounds like: It checks that an input value
is what you expect it to be, and tells you ``True``/``False`` whether it is or not.

.. important::

  Checkers do *not* verify or convert object types. You can think of a checker as
  a tool that tells you whether its corresponding :ref:`validator <validators-explained>`
  would fail. See :ref:`Best Practices <best-practices>` for tips and tricks on
  using the two together.

Each checker is expressed as the name of the thing being validated, prefixed by
``is_``. So the checker for an email address is
:func:`is_email() <validator_collection.checkers.is_email>` and the checker
for an integer is :func:`is_integer() <validator_collection.checkers.is_integer>`.

Checkers take the input value you want to check as their first (and often only)
positional argumet. If the input value validates, they will return ``True``. Unlike
:ref:`validators <validators-explained>`, checkers will not raise an exception if
validation fails. They will instead return ``False``.

.. hint::

  If you need to know *why* a given value failed to validate, use the validator
  instead.

.. hint::

  Some checkers (particularly numeric ones like
  :func:`is_integer <validator_collection.checkers.is_integer>`) have additional
  options which are used to make sure the value meets criteria that you set for
  it. These options are always *optional* and are included as keyword arguments
  *after* the input value argument. For details, please see the
  :doc:`Checker Reference <checkers>`.

.. _best-practices:

*****************
Best Practices
*****************

:ref:`Checkers <checkers-explained>` and :ref:`Validators <validators-explained>`
are designed to be used together. You can think of them as a way to quickly and
easily verify that a value contains the information you expect, and then make
sure that value is in the form your code needs it in.

There are two fundamental patterns that we find work well in practice.

Defensive Aprpoach: Check, then Convert if Necessary
-------------------------------------------------------

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

If it can't coerce ``value`` to a whole number? It raises a :class:`ValueError`.


Confident Approach: try ... except
--------------------------------------

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

  from validator_collection import validators

  def some_function(value):
      try:
        email_address = validators.email(value, allow_empty = False)
      except ValueError:
        # handle the error here

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

********************
Indices and tables
********************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
