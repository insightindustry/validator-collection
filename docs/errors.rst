**********************************
Error Reference
**********************************

.. module:: validator_collection.errors

.. contents::
  :local:
  :depth: 3
  :backlinks: entry

----------

Handling Errors
=================

.. tip::

  By design, :term:`checkers <checker>` **never** raise exceptions. If a given
  value fails, a checker will just return ``False``.

  :term:`Validators <validator>` **always** raise exceptions when validation
  fails.

When :term:`validators <validator>` fail, they raise exceptions. There are three
ways for exceptions to provide you with information that is useful in different
circumstances:

#. **Exception Type**. The type of the exception itself (and the name of that type)
   tells you a lot about the nature of the error. On its own, this should be
   enough for you to understand "what went wrong" and "why validation failed".
   Most importantly, this is easy to catch in your code using ``try ... except``
   blocks, giving you fine-grained control over how to handle exceptional situations.
#. **Message**. Each exception is raised when a human-readable message, a brief
   string that says "this is why this exception was raised". This is primarily
   useful in debugging your code, because at run-time we don't want to parse
   strings to make control flow decisions.
#. **Stack Trace**. Each exception is raised with a stacktrace of the exceptions
   and calls that preceded it. This helps to provide the context for the error, and
   is (typically) most useful for debugging and logging purposes. In rare circumstances,
   we might want to programmatically parse this information...but that's a pretty
   rare requirement.

We have designed the exceptions raised by the **Validator-Collection** to leverage
all three of these types of information.

Validator Names/Types
-------------------------

By design, all exceptions raised by the **Validator-Collection** inherit from
the `built-in exceptions <https://docs.python.org/3.6/library/exceptions.html>`_
defined in the standard library. This makes it simple to plug the **Validator-Collection**
into existing validation code you have which already catches
:class:`ValueError <python:ValueError>`, :class:`TypeError <python:TypeError>`,
and the like.

However, because we have sub-classed the built-in exceptions, you can easily apply
more fine-grained control over your code.

For example, let us imagine a validation which will fail:

.. code-block:: python

  from validator_collection import validators

  value = validators.decimal('123.45',
                             allow_empty = False,
                             minimum = 0,
                             maximum = 100)

By design, we know that this value will fail validation. We have specified
a ``maximum`` of 100, and the value being passed in is (a string) with a value of
``123.45``. This **will** fail.

We can catch this using a standard/built-in :class:`ValueError <python:ValueError>`
like so:

.. code-block:: python

  from validator_collection import validators

  try:
      value = validators.decimal('123.45',
                                 allow_empty = False,
                                 minimum = 0,
                                 maximum = 100)
  except ValueError as error:
      # Handle the error

Looking at the documentation for
:func:`validators.decimal() <validator_collection.validators.decimal>`, we can
see that this will catch all of the following situations:

  * when an empty/false value is passed with ``allow_empty = False``,
  * when a value is less than the allowed minimum,
  * when a value is more than the allowed maximum

But maybe we want to handle each of these situations a little differently? In
that case, we can use the custom exceptions defined by the **Validator-Collection**:

.. code-block:: python

  from validator_collection import validators, errors

  try:
      value = validators.decimal('123.45',
                                 allow_empty = False,
                                 minimum = 0,
                                 maximum = 100)
  except errors.EmptyValueError as error:
      # Handle the situation where an empty value was received.
  except errors.MinimumValueError as error:
      # Handle the situation when a value is less than the allowed minimum.
  except errors.MaximumValueError as error:
      # Handle the situation when a value is more than the allowed minimum.

Both approaches will work, but one gives you a little more precise control over
how your code handles a failed validation.

.. tip::

  We **strongly** recommend that you review the exceptions raised by each of
  the :doc:`validators` you use. Each validator precisely documents
  which exceptions it raises, and each exception's documentation shows what
  built-in exceptions it inherits from.

Validator Messages
---------------------

Because the **Validator-Collection** produces exceptions which inherit from the
standard library, we leverage the same API. This means they print to standard
output with a human-readable message that provides an explanation for "what went
wrong."

Stack Traces
--------------

Because the **Validator-Collection** produces exceptions which inherit from the
standard library, it leverages the same API for handling stack trace information.
This means that it will be handled just like a normal exception in unit test
frameworks, logging solutions, and other tools that might need that information.

---------

Standard Errors
===================

EmptyValueError (from :class:`ValueError <python:ValueError>`)
-----------------------------------------------------------------

.. autoclass:: EmptyValueError

CannotCoerceError (from :class:`TypeError <python:TypeError>`)
------------------------------------------------------------------

.. autoclass:: CannotCoerceError

MinimumValueError (from :class:`ValueError <python:ValueError>`)
------------------------------------------------------------------

.. autoclass:: MinimumValueError

MaximumValueError (from :class:`ValueError <python:ValueError>`)
------------------------------------------------------------------

.. autoclass:: MaximumValueError

ValidatorUsageError (from :class:`ValueError <python:ValueError>`)
---------------------------------------------------------------------

.. autoclass:: ValidatorUsageError

CoercionFunctionEmptyError (from :class:`ValidatorUsageError`)
-----------------------------------------------------------------------------

.. autoclass:: CoercionFunctionEmptyError

CoercionFunctionError (from :class:`ValueError`)
------------------------------------------------------------------

.. autoclass:: CoercionFunctionError

---------

Core
=======

MinimumLengthError (from :class:`ValueError <python:ValueError>`)
------------------------------------------------------------------

.. autoclass:: MinimumLengthError

MaximumLengthError (from :class:`ValueError <python:ValueError>`)
------------------------------------------------------------------

.. autoclass:: MaximumLengthError

NotNoneError (from :class:`ValueError <python:ValueError>`)
------------------------------------------------------------------

.. autoclass:: NotNoneError

NotADictError (from :class:`ValueError <python:ValueError>`)
------------------------------------------------------------------

.. autoclass:: NotADictError

NotAnIterableError (from :class:`CannotCoerceError`)
------------------------------------------------------------------

.. autoclass:: NotAnIterableError

NotCallableError (from :class:`ValueError <python:ValueError>`)
------------------------------------------------------------------

.. autoclass:: NotCallableError

InvalidVariableNameError (from :class:`ValueError <python:ValueError>`)
----------------------------------------------------------------------------

.. autoclass:: InvalidVariableNameError

-----------

Date / Time
===============

UTCOffsetError (from :class:`ValueError <python:ValueError>`)
------------------------------------------------------------------

.. autoclass:: UTCOffsetError

NegativeOffsetMismatchError (from :class:`ValueError <python:ValueError>`)
----------------------------------------------------------------------------

.. autoclass:: NegativeOffsetMismatchError

PositiveOffsetMismatchError (from :class:`ValueError <python:ValueError>`)
----------------------------------------------------------------------------

.. autoclass:: PositiveOffsetMismatchError

--------

Numbers
=========

NotAnIntegerError (from :class:`ValueError <python:ValueError>`)
------------------------------------------------------------------

.. autoclass:: NotAnIntegerError

------------

File-related
===============

NotPathlikeError (from :class:`ValueError <python:ValueError>`)
------------------------------------------------------------------

.. autoclass:: NotPathlikeError

PathExistsError (from :class:`IOError <python:IOError>`)
------------------------------------------------------------------

.. autoclass:: PathExistsError

NotAFileError (from :class:`IOError <python:IOError>`)
------------------------------------------------------------------

.. autoclass:: NotAFileError

NotADirectoryError (from :class:`IOError <python:IOError>`)
------------------------------------------------------------------

.. autoclass:: NotADirectoryError

NotBytesIOError (from :class:`ValueError <python:ValueError>`)
------------------------------------------------------------------

.. autoclass:: NotBytesIOError

NotStringIOError (from :class:`ValueError <python:ValueError>`)
------------------------------------------------------------------

.. autoclass:: NotStringIOError

---------

Internet-related
===================

InvalidEmailError (from :class:`ValueError <python:ValueError>`)
------------------------------------------------------------------

.. autoclass:: InvalidEmailError

InvalidURLError (from :class:`ValueError <python:ValueError>`)
------------------------------------------------------------------

.. autoclass:: InvalidURLError

InvalidDomainError (from :class:`ValueError <python:ValueError>`)
------------------------------------------------------------------

.. autoclass:: InvalidDomainError

SlashInDomainError (from :class:`InvalidDomainError`)
------------------------------------------------------------------

.. autoclass:: SlashInDomainError

AtInDomainError (from :class:`InvalidDomainError`)
------------------------------------------------------------------

.. autoclass:: AtInDomainError

ColonInDomainError (from :class:`InvalidDomainError`)
------------------------------------------------------------------

.. autoclass:: ColonInDomainError

WhitespaceInDomainError (from :class:`InvalidDomainError`)
------------------------------------------------------------------

.. autoclass:: WhitespaceInDomainError

InvalidIPAddressError (from :class:`ValueError <python:ValueError>`)
-----------------------------------------------------------------------

.. autoclass:: InvalidIPAddressError

InvalidMACAddressError (from :class:`ValueError <python:ValueError>`)
-----------------------------------------------------------------------

.. autoclass:: InvalidMACAddressError
