A :term:`checker` is what it sounds like: It checks that an input value
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

Disabling Checking
----------------------

.. caution::

  If you are disabling validators using the
  ``VALIDATORS_DISABLED`` environment variable, their related checkers will
  **also** be disabled. This means they will always return ``True`` unless you
  call them using ``force_run = True``.

Checking can at times be an expensive (in terms of performance) operation. As
a result, there are times when you want to disable certain kinds of checking
when running in production. Using the **Validator-Collection** this is simple:

  Just add the name of the checker you want disabled to the ``CHECKERS_DISABLED``
  environment variable, and validation will automatically be skipped.

.. caution::

  ``CHECKERS_DISABLED`` expects a comma-separated list of values. If it isn't
  comma-separated, it won't work properly.

Here's how it works in practice. Let's say we define the following environment
variable:

.. code-block:: bash

  $ export CHECKERS_DISABLED = "is_variable_name, is_email, is_ipv4"

This disables the :func:`is_variable_name() <validator_collection.checkers.is_variable_name>`,
:func:`is_email() <validator_collection.checkers.is_email>`, and
:func:`is_ipv4() <validator_collection.checkers.is_ipv4>` validators respectively.

Now if we run:

.. code-block:: python

  from validator_collection import checkers, errors

  result = checkers.is_variable_name('this is an invalid variable name')
  # result will be True

The checker will return ``True``.

However, if we run:

.. code-block:: python

  from validator_collection import checkers

  result = validators.is_integer('this is an invalid variable name')
  # result will be False

the checker will return ``False``

We can force checkers to run (even if disabled using the environment variable)
by passing a ``force_run = True`` keyword argument. For example:

.. code-block:: python

  from validator_collection import checkers, errors

  result = checkers.is_variable_name('this is an invalid variable name',
                                     force_run = True)
  # result will be False

will return ``False``.
