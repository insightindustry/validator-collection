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
then the validator will raise a
:class:`EmptyValueError <validator_collection.errors.EmptyValueError>` exception
(which inherits from the built-in :class:`ValueError <python:ValueError>`). If
``allow_empty`` is ``True``, then an empty/falsey input value will be converted to a
:class:`None <python:None>` value.

.. caution::

  By default, ``allow_empty`` is always set to ``False``.

.. hint::

  Some validators (particularly numeric ones like
  :func:`integer <validator_collection.validators.integer>`) have additional
  options which are used to make sure the value meets criteria that you set for
  it. These options are always included as keyword arguments *after* the
  ``allow_empty`` argument, and are documented for each validator below.

When Validation Fails
------------------------

Validators raise exceptions when validation fails. All exceptions raised inherit
from built-in exceptions like :class:`ValueError <python:ValueError>`,
:class:`TypeError <python:TypeError>`, and :class:`IOError <python:IOError>`.

If the value you're validating fails its validation for some reason, the validator
may raise different exceptions depending on the reason. In most cases, this will
be a descendent of :class:`ValueError` though it can sometimes be a
:class:`TypeError`, or an :class:`IOError`, etc.

For specifics on each validator's likely exceptions and what can cause them, please
review the :doc:`Validator Reference <validators>`.

.. hint::

  While validators will always raise built-in exceptions from the standard library,
  to give you greater programmatic control over how to respond when validation
  fails, we have defined a set of custom exceptions that inherit from those
  built-ins.

  Our custom exceptions provide you with very specific, fine-grained information
  as to *why* validation for a given value failed. In general, most validators
  will raise :class:`ValueError <python:ValueError>` or
  :class:`TypeError <python:TypeError>` exceptions, and you can safely catch those
  and be fine. But if you want to handle specific types of situations with greater
  control, then you can instead catch
  :class:`EmptyValueError <validator_collection.errors.EmptyValueError>`,
  :class:`CannotCoerceError <validator_collection.errors.CannotCoerceError>`,
  :class:`MaximumValueError <validator_collection.errors.MaximumValueError>`, and the like.

  For more detailed information, please see:
  :doc:`Error Reference <errors>` and
  :doc:`Validator Reference <validators>`.

Disabling Validation
----------------------

.. caution::

  If you are disabling validators using the
  ``VALIDATORS_DISABLED`` environment variable, their related
  :doc:`checkers <checkers>` will **also** be disabled (meaning they will
  always return ``True``).

Validation can at times be an expensive (in terms of performance) operation. As
a result, there are times when you want to disable certain kinds of validation
when running in production. Using the **Validator-Collection** this is simple:

  Just add the name of the validator you want disabled to the ``VALIDATORS_DISABLED``
  environment variable, and validation will automatically be skipped.

.. caution::

  ``VALIDATORS_DISABLED`` expects a comma-separated list of values. If it isn't
  comma-separated, it won't work properly.

Here's how it works in practice. Let's say we define the following environment
variable:

.. code-block:: bash

  $ export VALIDATORS_DISABLED = "variable_name, email, ipv4"

This disables the :func:`variable_name() <validator_collection.validators.variable_name>`,
:func:`email() <validator_collection.validators.email>`, and
:func:`ipv4() <validator_collection.validators.ipv4>` validators respectively.

Now if we run:

.. code-block:: python

  from validator_collection import validators, errors

  try:
      result = validators.variable_name('this is an invalid variable name')
  except ValueError:
      # handle the error

The validator will return the ``value`` supplied to it un-changed. So that means
``result`` will be equal to ``this is an invalid variable name``.

However, if we run:

.. code-block:: python

  from validator_collection import validators, errors

  try:
      result = validators.integer('this is an invalid variable name')
  except errors.NotAnIntegerError:
      # handle the error

the validator will run and raise
:class:`NotAnIntegerError <validator_collection.errors.NotAnIntegerError>`.

We can force validators to run (even if disabled using the environment variable)
by passing a ``force_run = True`` keyword argument. For example:

.. code-block:: python

  from validator_collection import validators, errors

  try:
      result = validators.variable_name('this is an invalid variable name',
                                        force_run = True)
  except ValueError:
      # handle the error

will produce a
:class:`InvalidVariableNameError <validator_collection.errors.InvalidVariableNameError>`
(which is a type of :class:`ValueError <python:ValueError>`).
