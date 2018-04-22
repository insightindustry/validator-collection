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
      :class:`None <python:None>`.

      Please see: :doc:`Validator Reference <validators>`.

    """
    pass

class NotNoneError(ValueError):
    """Exception raised when a value of :class:`None <python:None>` is expected,
    but a different empty value was detected."""
    pass


class InvalidVariableNameError(ValueError):
    """Exception raised when a value is not a valid Python variable name."""
    pass

class NotADictError(ValueError):
    """Exception raised when a value is not a :class:`dict <python:dict>`."""
    pass

class InvalidEmailError(ValueError):
    """Exception raised when an email fails validation."""
    pass

class InvalidURLError(ValueError):
    """Exception raised when a URL fails validation."""
    pass

class InvalidDomainError(ValueError):
    """Exception raised when a domain fails validation."""
    pass

class SlashInDomainError(InvalidDomainError):
    """Exception raised when a domain value contains a slash or backslash."""
    pass

class AtInDomainError(InvalidDomainError):
    """Exception raised when a domain value contains an ``@`` symbol."""
    pass

class ColonInDomainError(InvalidDomainError):
    """Exception raised when a domain value contains a colon (``:``)."""
    pass

class WhitespaceInDomainError(InvalidDomainError):
    """Exception raised when a domain value contains whitespace."""
    pass

class InvalidIPAddressError(ValueError):
    """Exception raised when a value is not a valid IP address."""
    pass

class InvalidMACAddressError(ValueError):
    """Exception raised when a value is not a valid MAC address."""
    pass


class CannotCoerceError(TypeError):
    """Exception raised when a value cannot be coerced to an expected type."""
    pass

class NotAnIterableError(TypeError):
    """Exception raised when a value is not an iterable."""
    pass


class MaximumLengthError(ValueError):
    """Exception raised when a value exceeds a maximum allowed length."""
    pass

class MinimumLengthError(ValueError):
    """Exception raised when a value has a lower length than the minimum allowed."""
    pass

class MaximumValueError(ValueError):
    """Exception raised when a value exceeds a maximum allowed value."""
    pass

class MinimumValueError(ValueError):
    """Exception raised when a value has a lower or earlier value than the minimum
    allowed."""
    pass

class NotAnIntegerError(ValueError):
    """Exception raised when a value is not being coerced and is not an integer type."""
    pass

class NegativeOffsetMismatchError(ValueError):
    """Exception raised when a negative offset is expected, but the value indicates
    a positive offset."""
    pass

class PositiveOffsetMismatchError(ValueError):
    """Exception raised when a positive offset is expected, but the value indicates
    a negative offset."""
    pass

class UTCOffsetError(ValueError):
    """Exception raised when the UTC offset exceeds +/- 24 hours."""
    pass

class ValidatorUsageError(ValueError):
    """Exception raised when the validator was used incorrectly."""
    pass

class CoercionFunctionEmptyError(ValidatorUsageError):
    """Exception raised when a coercion function was empty."""
    pass

class CoercionFunctionError(ValueError):
    """Exception raised when a Coercion Function produces an
    :class:`Exception <python:Exception>`."""
    pass

class NotCallableError(ValueError):
    """Exception raised when a given value is not callable."""
    pass

class NotBytesIOError(ValueError):
    """Exception raised when a given value is not a
    :class:`BytesIO <python:io.BytesIO>` object."""
    pass

class NotStringIOError(ValueError):
    """Exception raised when a given value is not a
    :class:`StringIO <python:io.StringIO>` object."""
    pass


class NotPathlikeError(ValueError):
    """Exception raised when a given value is not a path-like object."""
    pass


class PathExistsError(IOError):
    """Exception raised when a path does not exist."""
    pass

class NotAFileError(IOError):
    """Exception raised when a path is not a file."""
    pass

class NotADirectoryError(IOError):
    """Exception raised when a path is not a directory."""
    pass
