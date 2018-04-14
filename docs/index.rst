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
  Contributing <contributing>
  Testing Reference <testing>
  Glossary <glossary>

The **Validator Collection** is a Python library that provides more than 50
validator functions that can be used to validate the type and contents of an
input value. Each function has a consistent syntax for easy use, and has been
tested on Python 2.7, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, and 3.6.

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

************************************
Hello, World and Standard Usage
************************************

All validator functions have a consistent syntax so that using them is pretty
much identical. Here's how it works:

.. code-block:: python

  import validator_collection as validators

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

  is_email_address = validators.is_email('test@domain.dev')
  # The value of is_email_address will now be True

  is_email_address = validators.is_email('this-is-an-invalid-email')
  # The value of is_email_address will now be False

  is_email_address = validators.is_email(None)
  # The value of is_email_address will now be False

Pretty simple, right? Let's break it down just in case: Each validator comes in
two flavors: a :term:`validator` and a :term:`checker`.

.. _validators-explained:

Using Validators
==================
A validator does what it says on the tin: It validates that an input value is
what you think it should be, and returns its valid form.

Each validator is expressed as the name of the thing being validated, for example
``email()``.

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
is ``True``, however, an empty/falsey input value will be convertd to a ``None``
value.

.. caution::

  By default, ``allow_empty`` is always set to ``False``.

If the value you're validating fails its validation for some reason, the validator
may raise different exceptions depending on the reason. Sometimes it'll be an
:class:`TypeError`, other times an :class:`AttributeError`, etc. For specifics
on each validator's exceptions and what can cause them, please take a look at the
validator's documentation below.

.. hint::

  Some validators (particularly numeric ones like :ref:`integer <validators.integer>`)
  have additional options which are used to make sure the value meets criteria that
  you set for it. These options are always included as keyword arguments *after*
  the ``allow_empty`` argument, and are documented for each validator below.

.. _checkers-explained:

Using Checkers
================

Likewise, a :term:`checker` is what it sounds like: It checks that an input value
is what you expect it to be, and tells you ``True``/``False`` whether it is or not.

Each checker is expressed as the name of the thing being validated, prefixed by
``is_``. So the checker for an email address is ``is_email()`` and the checker
for an integer is ``is_integer()``.

Checkers take the input value you want to check as their first (and often only)
positional argumet. If the input value validates, they will return ``True``. Unlike
:ref:`validators <validators-explained>`, checkers will not raise an exception if
validation fails. They will instead return ``False``.

.. hint::

  If you need to know *why* a given value failed to validate, use the validator
  instead.

.. hint::

  Some checkers (particularly numeric ones like :ref:`is_integer <_checkers.is_integer>`)
  have additional options which are used to make sure the value meets criteria that
  you set for it. These options are always *optional* and are included as keyword
  arguments *after* the input value argument. They are documented for each checker below.


*********************
Validator Reference
*********************

Validators
============

.. automodule:: validator_collection._validators
  :members:

Checkers
==========

.. automodule:: validator_collection._checkers
  :members:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
