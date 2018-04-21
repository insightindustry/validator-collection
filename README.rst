

======================
Validator Collection
======================

**Python library of 60+ commonly-used validator functions**

.. list-table::
  :widths: 10 90
  :header-rows: 1

  * - Branch
    - Unit Tests
  * - `latest <https://github.com/insightindustry/validator-collection/tree/master>`_
    -
      .. image:: https://travis-ci.org/insightindustry/validator-collection.svg?branch=master
         :target: https://travis-ci.org/insightindustry/validator-collection
         :alt: Build Status (Travis CI)

      .. image:: https://codecov.io/gh/insightindustry/validator-collection/branch/master/graph/badge.svg
         :target: https://codecov.io/gh/insightindustry/validator-collection
         :alt: Code Coverage Status (Codecov)

      .. image:: https://readthedocs.org/projects/validator-collection/badge/?version=latest
         :target: http://validator-collection.readthedocs.io/en/latest/?badge=latest
         :alt: Documentation Status (ReadTheDocs)

  * - `v. 1.0.0 <https://github.com/insightindustry/validator-collection/tree/v1-0-0>`_
    -
     .. image:: https://travis-ci.org/insightindustry/validator-collection.svg?branch=v1-0-0
        :target: https://travis-ci.org/insightindustry/validator-collection
        :alt: Build Status (Travis CI)

     .. image:: https://codecov.io/gh/insightindustry/validator-collection/branch/v1-0-0/graph/badge.svg
        :target: https://codecov.io/gh/insightindustry/validator-collection
        :alt: Code Coverage Status (Codecov)

     .. image:: https://readthedocs.org/projects/validator-collection/badge/?version=v1-0-0
        :target: http://validator-collection.readthedocs.io/en/latest/?badge=v1-0-0
        :alt: Documentation Status (ReadTheDocs)

  * - `develop <https://github.com/insightindustry/validator-collection/tree/develop>`_
    -
      .. image:: https://travis-ci.org/insightindustry/validator-collection.svg?branch=develop
         :target: https://travis-ci.org/insightindustry/validator-collection
         :alt: Build Status (Travis CI)

      .. image:: https://codecov.io/gh/insightindustry/validator-collection/branch/develop/graph/badge.svg
         :target: https://codecov.io/gh/insightindustry/validator-collection
         :alt: Code Coverage Status (Codecov)

      .. image:: https://readthedocs.org/projects/validator-collection/badge/?version=develop
         :target: http://validator-collection.readthedocs.io/en/latest/?badge=develop
         :alt: Documentation Status (ReadTheDocs)



The **Validator Collection** is a Python library that provides more than 60
functions that can be used to validate the type and contents of an input value.

Each function has a consistent syntax for easy use, and has been tested on
Python 2.7, 3.4, 3.5, and 3.6.

For a list of validators available, please see the lists below.

**COMPLETE DOCUMENTATION ON READTHEDOCS:** http://validator-collection.readthedocs.io/en/latest

------

.. contents:: Contents
  :local:
  :depth: 3
  :backlinks: entry

--------

***************
Installation
***************

To install the **Validator Collection**, just execute:

.. code:: bash

  $ pip install validator-collection

**Dependencies:**

.. list-table::
  :widths: 50 50
  :header-rows: 1

  * - Python 3.x
    - Python 2.7
  * - None. Uses the standard library.
    - The `regex <https://pypi.python.org/pypi/regex>`_ drop-in replacement for
      Python's (buggy) standard ``re`` module.

      Conditional dependencies will be automatically installed if you are
      installing to Python 2.x.

-------

***********************************
Available Validators and Checkers
***********************************

Validators
=============

**SEE:** `Validator Reference <http://validator-collection.readthedocs.io/en/latest/validators.html>`_

.. list-table::
  :widths: 30 30 30 30 30
  :header-rows: 1

  * - Core
    - Date/Time
    - Numbers
    - File-related
    - Internet-related
  * - ``dict``
    - ``date``
    - ``numeric``
    - ``bytesIO``
    - ``email``
  * - ``string``
    - ``datetime``
    - ``integer``
    - ``stringIO``
    - ``url``
  * - ``iterable``
    - ``time``
    - ``float``
    - ``path``
    - ``domain``
  * - ``none``
    - ``timezone``
    - ``fraction``
    - ``path_exists``
    - ``ip_address``
  * - ``not_empty``
    -
    - ``decimal``
    - ``file_exists``
    - ``ipv4``
  * - ``uuid``
    -
    -
    - ``directory_exists``
    - ``ipv6``
  * - ``variable_name``
    -
    -
    -
    - ``mac_address``

Checkers
==========

**SEE:** `Checker Reference <http://validator-collection.readthedocs.io/en/latest/checkers.html>`_

.. list-table::
  :widths: 30 30 30 30 30
  :header-rows: 1

  * - Core
    - Date/Time
    - Numbers
    - File-related
    - Internet-related
  * - ``is_type``
    - ``is_date``
    - ``is_numeric``
    - ``is_bytesIO``
    - ``is_email``
  * - ``is_between``
    - ``is_datetime``
    - ``is_integer``
    - ``is_stringIO``
    - ``is_url``
  * - ``has_length``
    - ``is_time``
    - ``is_float``
    - ``is_pathlike``
    - ``is_domain``
  * - ``are_equivalent``
    - ``is_timezone``
    - ``is_fraction``
    - ``is_on_filesystem``
    - ``is_ip_address``
  * - ``are_dicts_equivalent``
    -
    - ``is_decimal``
    - ``is_file``
    - ``is_ipv4``
  * - ``is_dict``
    -
    -
    - ``is_directory``
    - ``is_ipv6``
  * - ``is_string``
    -
    -
    -
    - ``is_mac_address``
  * - ``is_iterable``
    -
    -
    -
    -
  * - ``is_not_empty``
    -
    -
    -
    -
  * - ``is_none``
    -
    -
    -
    -
  * - ``is_callable``
    -
    -
    -
    -
  * - ``is_uuid``
    -
    -
    -
    -
  * - ``is_variable_name``
    -
    -
    -
    -

-----

************************************
Hello, World and Standard Usage
************************************

All validator functions have a consistent syntax so that using them is pretty
much identical. Here's how it works:

.. code-block:: python

  from validator_collection import validators, checkers

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
two flavors: a validator and a checker.

.. _validators-explained:

Using Validators
==================

**SEE:** `Validator Reference <http://validator-collection.readthedocs.io/en/latest/validators.html>`_

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
then the validator will raise a ``ValueError`` exception. If ``allow_empty``
is ``True``, then an empty/falsey input value will be converted to a ``None``
value.

**CAUTION:** By default, ``allow_empty`` is always set to ``False``.

If the value you're validating fails its validation for some reason, the validator
may raise different exceptions depending on the reason. In most cases, this will
be a ``ValueError`` though it can sometimes be a ``TypeError``, or an
``AttributeError``, etc. For specifics on each validator's likely exceptions
and what can cause them, please review the `Validator Reference <http://validator-collection.readthedocs.io/en/latest/validators.html>`_.

**HINT:** Some validators (particularly numeric ones like ``integer``) have additional
options which are used to make sure the value meets criteria that you set for
it. These options are always included as keyword arguments *after* the
``allow_empty`` argument, and are documented for each validator below.

.. _checkers-explained:

Using Checkers
================

Please see the `Checker Reference <http://validator-collection.readthedocs.io/en/latest/checkers.html>`_

Likewise, a checker is what it sounds like: It checks that an input value
is what you expect it to be, and tells you ``True``/``False`` whether it is or not.

**IMPORTANT:** Checkers do *not* verify or convert object types. You can think of a checker as
a tool that tells you whether its corresponding `validator <#using-validators>`_
would fail. See `Best Practices <#best-practices>`_ for tips and tricks on
using the two together.

Each checker is expressed as the name of the thing being validated, prefixed by
``is_``. So the checker for an email address is ``is_email()`` and the checker
for an integer is ``is_integer()``.

Checkers take the input value you want to check as their first (and often only)
positional argumet. If the input value validates, they will return ``True``. Unlike
`validators <#using-validators>`_, checkers will not raise an exception if
validation fails. They will instead return ``False``.

**HINT:** If you need to know *why* a given value failed to validate, use the validator
instead.

**HINT:** Some checkers (particularly numeric ones like ``is_integer()``) have additional
options which are used to make sure the value meets criteria that you set for
it. These options are always *optional* and are included as keyword arguments
*after* the input value argument. For details, please see the
`Checker Reference <http://validator-collection.readthedocs.io/en/latest/checkers.html>`_.

.. _best-practices:

------

*****************
Best Practices
*****************

`Checkers <#using-checkers>`_ and `Validators <#using-validators>`_
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
``is_integer()``
checker to see if ``value`` contains a whole number, regardless of its type.

If it doesn't contain a whole number, maybe it contains a numeric value that can
be rounded up to a whole number? It again uses the
``is_integer()`` to check if that's
possible. If it is, then it calls the
``integer()`` validator to coerce
``value`` to a whole number.

If it can't coerce ``value`` to a whole number? It raises a ``ValueError``.


Confident Approach: try ... except
=====================================

Sometimes, we'll have more confidence in the values that we can expect to work
with. This means that we might expect ``value`` to *generally* have the kind of
data we need to work with. This means that situations where ``value`` doesn't
contain what we need will truly be exceptional situations, and can be handled
accordingly.

In this situation, a good approach is to apply the following logic:

#. Skip a checker entirely, and just wrap the validator in a
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

----------

*********************
Questions and Issues
*********************

You can ask questions and report issues on the project's
`Github Issues Page <https://github.com/insightindustry/validator-collection/issues>`_

*********************
Contributing
*********************

We welcome contributions and pull requests! For more information, please see the
`Contributor Guide <http://validator-collection.readthedocs.io/en/latest/contributing.html>`_

*********************
Testing
*********************

We use `TravisCI <http://travisci.org>`_ for our build automation and
`ReadTheDocs <https://readthedocs.org>`_ for our documentation.

Detailed information about our test suite and how to run tests locally can be
found in our `Testing Reference <http://validator-collection.readthedocs.io/en/latest/testing.html>`_.

**********************
License
**********************

The **Validator Collection** is made available on a **MIT License**.
