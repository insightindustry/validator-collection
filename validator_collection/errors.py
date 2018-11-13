# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member class documentation is automatically incorporated
# there as needed.

class EmptyValueError(ValueError):
    """Exception raised when an empty value is detected, but the validator does
    not allow for empty values.

    .. note::

      While in general, an "empty" value means a value that is falsey, for
      certain specific validators "empty" means explicitly
      :obj:`None <python:None>`.

      Please see: :doc:`Validator Reference <validators>`.

    **INHERITS FROM:** :class:`ValueError <python:ValueError>`

    """
    pass

class NotNoneError(ValueError):
    """Exception raised when a value of :obj:`None <python:None>` is expected,
    but a different empty value was detected.

    **INHERITS FROM:** :class:`ValueError <python:ValueError>`

    """
    pass


class InvalidVariableNameError(ValueError):
    """Exception raised when a value is not a valid Python variable name.

    **INHERITS FROM:** :class:`ValueError <python:ValueError>`

    """
    pass

class NotADictError(ValueError):
    """Exception raised when a value is not a :class:`dict <python:dict>`.

    **INHERITS FROM:** :class:`ValueError <python:ValueError>`

    """
    pass

class NotJSONError(ValueError):
    """Exception raised when a value cannot be serialized/de-serialized to a JSON object.

    **INHERITS FROM:** :class:`ValueError <python:ValueError>`

    """
    pass

class NotJSONSchemaError(ValueError):
    """Exception raised when a schema supplied is not a valid JSON Schema.

    **INHERITS FROM:** :class:`ValueError <python:ValueError>`

    """
    pass

class JSONValidationError(ValueError):
    """Exception raised when a value fails validation against a JSON Schema.

    **INHERITS FROM:** :class:`ValueError <python:ValueError>`

    """
    pass

class InvalidEmailError(ValueError):
    """Exception raised when an email fails validation.

    **INHERITS FROM:** :class:`ValueError <python:ValueError>`

    """
    pass

class InvalidURLError(ValueError):
    """Exception raised when a URL fails validation.

    **INHERITS FROM:** :class:`ValueError <python:ValueError>`

    """
    pass

class InvalidDomainError(ValueError):
    """Exception raised when a domain fails validation.

    **INHERITS FROM:** :class:`ValueError <python:ValueError>`

    """
    pass

class SlashInDomainError(InvalidDomainError):
    """Exception raised when a domain value contains a slash or backslash.

    **INHERITS FROM:** :class:`ValueError <python:ValueError>` ->
    :class:`InvalidDomainError`

    """
    pass

class AtInDomainError(InvalidDomainError):
    """Exception raised when a domain value contains an ``@`` symbol.

    **INHERITS FROM:** :class:`ValueError <python:ValueError>` ->
    :class:`InvalidDomainError`

    """
    pass

class ColonInDomainError(InvalidDomainError):
    """Exception raised when a domain value contains a colon (``:``).

    **INHERITS FROM:** :class:`ValueError <python:ValueError>` ->
    :class:`InvalidDomainError`

    """
    pass

class WhitespaceInDomainError(InvalidDomainError):
    """Exception raised when a domain value contains whitespace.

    **INHERITS FROM:** :class:`ValueError <python:ValueError>` ->
    :class:`InvalidDomainError`

    """
    pass

class InvalidIPAddressError(ValueError):
    """Exception raised when a value is not a valid IP address.

    **INHERITS FROM:** :class:`ValueError <python:ValueError>`

    """
    pass

class InvalidMACAddressError(ValueError):
    """Exception raised when a value is not a valid MAC address.

    **INHERITS FROM:** :class:`ValueError <python:ValueError>`

    """
    pass


class CannotCoerceError(TypeError):
    """Exception raised when a value cannot be coerced to an expected type.

    **INHERITS FROM:** :class:`TypeError <python:TypeError>`

    """
    pass

class NotAnIterableError(CannotCoerceError):
    """Exception raised when a value is not an iterable.

    **INHERITS FROM:** :class:`TypeError <python:TypeError>` -> :class:`CannotCoerceError <validator_collection.errors.CannotCoerceError>`

    """
    pass


class MaximumLengthError(ValueError):
    """Exception raised when a value exceeds a maximum allowed length.

    **INHERITS FROM:** :class:`ValueError <python:ValueError>`

    """
    pass

class MinimumLengthError(ValueError):
    """Exception raised when a value has a lower length than the minimum allowed.

    **INHERITS FROM:** :class:`ValueError <python:ValueError>`

    """
    pass

class MaximumValueError(ValueError):
    """Exception raised when a value exceeds a maximum allowed value.

    **INHERITS FROM:** :class:`ValueError <python:ValueError>`

    """
    pass

class MinimumValueError(ValueError):
    """Exception raised when a value has a lower or earlier value than the minimum
    allowed.

    **INHERITS FROM:** :class:`ValueError <python:ValueError>`

    """
    pass

class NotAnIntegerError(ValueError):
    """Exception raised when a value is not being coerced and is not an integer type.

    **INHERITS FROM:** :class:`ValueError <python:ValueError>`

    """
    pass

class NegativeOffsetMismatchError(ValueError):
    """Exception raised when a negative offset is expected, but the value indicates
    a positive offset.

    **INHERITS FROM:** :class:`ValueError <python:ValueError>`

    """
    pass

class PositiveOffsetMismatchError(ValueError):
    """Exception raised when a positive offset is expected, but the value indicates
    a negative offset.

    **INHERITS FROM:** :class:`ValueError <python:ValueError>`

    """
    pass

class UTCOffsetError(ValueError):
    """Exception raised when the UTC offset exceeds +/- 24 hours.

    **INHERITS FROM:** :class:`ValueError <python:ValueError>`

    """
    pass

class ValidatorUsageError(ValueError):
    """Exception raised when the validator was used incorrectly.

    **INHERITS FROM:** :class:`ValueError <python:ValueError>`

    """
    pass

class CoercionFunctionEmptyError(ValidatorUsageError):
    """Exception raised when a coercion function was empty.

    **INHERITS FROM:** :class:`ValueError <python:ValueError>` ->
    :class:`ValidatorUsageError`

    """
    pass

class CoercionFunctionError(ValueError):
    """Exception raised when a Coercion Function produces an
    :class:`Exception <python:Exception>`.

    **INHERITS FROM:** :class:`ValueError <python:ValueError>`

    """
    pass

class NotCallableError(ValueError):
    """Exception raised when a given value is not callable.

    **INHERITS FROM:** :class:`ValueError <python:ValueError>`

    """
    pass

class NotBytesIOError(ValueError):
    """Exception raised when a given value is not a
    :class:`BytesIO <python:io.BytesIO>` object.

    **INHERITS FROM:** :class:`ValueError <python:ValueError>`

    """
    pass

class NotStringIOError(ValueError):
    """Exception raised when a given value is not a
    :class:`StringIO <python:io.StringIO>` object.

    **INHERITS FROM:** :class:`ValueError <python:ValueError>`

    """
    pass


class NotPathlikeError(ValueError):
    """Exception raised when a given value is not a path-like object.

    **INHERITS FROM:** :class:`ValueError <python:ValueError>`

    """
    pass


class PathExistsError(IOError):
    """Exception raised when a path does not exist.

    **INHERITS FROM:** :class:`IOError <python:IOError>`

    """
    pass

class NotAFileError(IOError):
    """Exception raised when a path is not a file.

    **INHERITS FROM:** :class:`IOError <python:IOError>`

    """
    pass

class NotADirectoryError(IOError):
    """Exception raised when a path is not a directory.

    **INHERITS FROM:** :class:`IOError <python:IOError>`

    """
    pass


class NotReadableError(IOError):
    """Exception raised when a path is not readable.

    **INHERITS FROM:** :class:`IOError <python:IOError>`
    """
    pass

class NotWriteableError(IOError):
    """Exception raised when a path is not writeable.

    **INHERITS FROM:** :class:`IOError <python:IOError>`
    """
    pass

class NotExecutableError(IOError):
    """Exception raised when a path is not executable.

    **INHERITS FROM:** :class:`IOError <python:IOError>`
    """
    pass
