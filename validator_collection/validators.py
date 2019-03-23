# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

import decimal as decimal_
import fractions
import io
import math
import os
import uuid as uuid_
import datetime as datetime_
import string as string_
import sys

from ast import parse

import jsonschema

from validator_collection._compat import numeric_types, integer_types, datetime_types,\
    date_types, time_types, timestamp_types, tzinfo_types, POSITIVE_INFINITY, \
    NEGATIVE_INFINITY, TimeZone, json_, is_py2, is_py3, dict_, float_, basestring, re
from validator_collection._decorators import disable_on_env
from validator_collection import errors


URL_REGEX = re.compile(
    r"^"
    # protocol identifier
    r"(?:(?:https?|ftp)://)"
    # user:pass authentication
    r"(?:\S+(?::\S*)?@)?"
    r"(?:"
    # IP address exclusion
    # private & local networks
    r"(?!(?:10|127)(?:\.\d{1,3}){3})"
    r"(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})"
    r"(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})"
    # IP address dotted notation octets
    # excludes loopback network 0.0.0.0
    # excludes reserved space >= 224.0.0.0
    # excludes network & broadcast addresses
    # (first & last IP address of each class)
    r"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
    r"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}"
    r"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"
    r"|"
    r"(?:"
    r"(?:localhost|invalid|test|example)|("
    # host name
    r"(?:(?:[a-z\u00a1-\uffff0-9]-*_*)*[a-z\u00a1-\uffff0-9]+)"
    # domain name
    r"(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*"
    # TLD identifier
    r"(?:\.(?:[a-z\u00a1-\uffff]{2,}))"
    r")))"
    # port number
    r"(?::\d{2,5})?"
    # resource path
    r"(?:/\S*)?"
    r"$"
    , re.UNICODE)

URL_SPECIAL_IP_REGEX = re.compile(
    r"^"
    # protocol identifier
    r"(?:(?:https?|ftp)://)"
    # user:pass authentication
    r"(?:\S+(?::\S*)?@)?"
    r"(?:"
    # IP address dotted notation octets
    # excludes loopback network 0.0.0.0
    # excludes reserved space >= 224.0.0.0
    # excludes network & broadcast addresses
    # (first & last IP address of each class)
    r"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
    r"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}"
    r"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"
    r"|"
    # host name
    r"(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)"
    # domain name
    r"(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*"
    # TLD identifier
    r"(?:\.(?:[a-z\u00a1-\uffff]{2,}))"
    r")"
    # port number
    r"(?::\d{2,5})?"
    # resource path
    r"(?:/\S*)?"
    r"$"
    , re.UNICODE)


DOMAIN_REGEX = re.compile(
    r"\b((?=[a-z\u00a1-\uffff0-9-]{1,63}\.)(xn--)?[a-z\u00a1-\uffff0-9]+"
    r"(-[a-z\u00a1-\uffff0-9]+)*\.)+[a-z]{2,63}\b",
    re.UNICODE
)

URL_PROTOCOLS = ('http://',
                 'https://',
                 'ftp://')

SPECIAL_USE_DOMAIN_NAMES = ('localhost',
                            'invalid',
                            'test',
                            'example')

EMAIL_REGEX = re.compile(
    r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\""
    r"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")"
    r"@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])"
    r"?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}"
    r"(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:"
    r"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
)


MAC_ADDRESS_REGEX = re.compile(r'^(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$')

IPV6_REGEX = re.compile(
    '^(?:(?:[0-9A-Fa-f]{1,4}:){6}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|::(?:[0-9A-Fa-f]{1,4}:){5}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){4}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){3}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,2}[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){2}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,3}[0-9A-Fa-f]{1,4})?::[0-9A-Fa-f]{1,4}:(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,4}[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,5}[0-9A-Fa-f]{1,4})?::[0-9A-Fa-f]{1,4}|(?:(?:[0-9A-Fa-f]{1,4}:){,6}[0-9A-Fa-f]{1,4})?::)(?:%25(?:[A-Za-z0-9\\-._~]|%[0-9A-Fa-f]{2})+)?$'
)

# pylint: disable=W0613

## CORE

@disable_on_env
def uuid(value,
         allow_empty = False,
         **kwargs):
    """Validate that ``value`` is a valid :class:`UUID <python:uuid.UUID>`.

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns :obj:`None <python:None>` if
      ``value`` is empty. If ``False``, raises a
      :class:`EmptyValueError <validator_collection.errors.EmptyValueError>`
      if ``value`` is empty. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :returns: ``value`` coerced to a :class:`UUID <python:uuid.UUID>` object /
      :obj:`None <python:None>`
    :rtype: :class:`UUID <python:uuid.UUID>` / :obj:`None <python:None>`

    :raises EmptyValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    :raises CannotCoerceError: if ``value`` cannot be coerced to a
      :class:`UUID <python:uuid.UUID>`

    """
    if not value and not allow_empty:
        raise errors.EmptyValueError('value (%s) was empty' % value)
    elif not value:
        return None

    if isinstance(value, uuid_.UUID):
        return value

    try:
        value = uuid_.UUID(value)
    except ValueError:
        raise errors.CannotCoerceError('value (%s) cannot be coerced to a valid UUID')

    return value


@disable_on_env
def string(value,
           allow_empty = False,
           coerce_value = False,
           minimum_length = None,
           maximum_length = None,
           whitespace_padding = False,
           **kwargs):
    """Validate that ``value`` is a valid string.

    :param value: The value to validate.
    :type value: :class:`str <python:str>` / :obj:`None <python:None>`

    :param allow_empty: If ``True``, returns :obj:`None <python:None>` if ``value``
      is empty. If ``False``, raises a
      :class:`EmptyValueError <validator_collection.errors.EmptyValueError>` if
      ``value`` is empty. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :param coerce_value: If ``True``, will attempt to coerce ``value`` to a string if
      it is not already. If ``False``, will raise a :class:`ValueError` if ``value``
      is not a string. Defaults to ``False``.
    :type coerce_value: :class:`bool <python:bool>`

    :param minimum_length: If supplied, indicates the minimum number of characters
      needed to be valid.
    :type minimum_length: :class:`int <python:int>`

    :param maximum_length: If supplied, indicates the minimum number of characters
      needed to be valid.
    :type maximum_length: :class:`int <python:int>`

    :param whitespace_padding: If ``True`` and the value is below the
      ``minimum_length``, pad the value with spaces. Defaults to ``False``.
    :type whitespace_padding: :class:`bool <python:bool>`

    :returns: ``value`` / :obj:`None <python:None>`
    :rtype: :class:`str <python:str>` / :obj:`None <python:None>`

    :raises EmptyValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    :raises CannotCoerceError: if ``value`` is not a valid string and ``coerce_value``
      is ``False``
    :raises MinimumLengthError: if ``minimum_length`` is supplied and the length of
      ``value`` is less than ``minimum_length`` and ``whitespace_padding`` is
      ``False``
    :raises MaximumLengthError: if ``maximum_length`` is supplied and the length of
      ``value`` is more than the ``maximum_length``
    """
    if not value and not allow_empty:
        raise errors.EmptyValueError('value (%s) was empty' % value)
    elif not value:
        return None

    minimum_length = integer(minimum_length, allow_empty = True)
    maximum_length = integer(maximum_length, allow_empty = True)

    if coerce_value:
        value = str(value)
    elif not isinstance(value, basestring):
        raise errors.CannotCoerceError('value (%s) was not coerced to a string' % value)

    if value and maximum_length and len(value) > maximum_length:
        raise errors.MaximumLengthError(
            'value (%s) exceeds maximum length %s' % (value, maximum_length)
        )

    if value and minimum_length and len(value) < minimum_length:
        if whitespace_padding:
            value = value.ljust(minimum_length, ' ')
        else:
            raise errors.MinimumLengthError(
                'value (%s) is below the minimum length %s' % (value, minimum_length)
            )

    return value


@disable_on_env
def iterable(value,
             allow_empty = False,
             forbid_literals = (str, bytes),
             minimum_length = None,
             maximum_length = None,
             **kwargs):
    """Validate that ``value`` is a valid iterable.

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns :obj:`None <python:None>` if ``value``
      is empty. If ``False``, raises a
      :class:`EmptyValueError <validator_collection.errors.EmptyValueError>` if
      ``value`` is empty. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :param forbid_literals: A collection of literals that will be considered invalid
      even if they are (actually) iterable. Defaults to :class:`str <python:str>` and
      :class:`bytes <python:bytes>`.
    :type forbid_literals: iterable

    :param minimum_length: If supplied, indicates the minimum number of members
      needed to be valid.
    :type minimum_length: :class:`int <python:int>`

    :param maximum_length: If supplied, indicates the minimum number of members
      needed to be valid.
    :type maximum_length: :class:`int <python:int>`

    :returns: ``value`` / :obj:`None <python:None>`
    :rtype: iterable / :obj:`None <python:None>`

    :raises EmptyValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    :raises NotAnIterableError: if ``value`` is not a valid iterable or
      :obj:`None <python:None>`
    :raises MinimumLengthError: if ``minimum_length`` is supplied and the length of
      ``value`` is less than ``minimum_length`` and ``whitespace_padding`` is
      ``False``
    :raises MaximumLengthError: if ``maximum_length`` is supplied and the length of
      ``value`` is more than the ``maximum_length``
    """
    if not value and not allow_empty:
        raise errors.EmptyValueError('value (%s) was empty' % value)
    elif value is None:
        return None

    minimum_length = integer(minimum_length, allow_empty = True, force_run = True) # pylint: disable=E1123
    maximum_length = integer(maximum_length, allow_empty = True, force_run = True) # pylint: disable=E1123

    if isinstance(value, forbid_literals) or not hasattr(value, '__iter__'):
        raise errors.NotAnIterableError('value type (%s) not iterable' % type(value))

    if value and minimum_length is not None and len(value) < minimum_length:
        raise errors.MinimumLengthError(
            'value has fewer items than the minimum length %s' % minimum_length
        )

    if value and maximum_length is not None and len(value) > maximum_length:
        raise errors.MaximumLengthError(
            'value has more items than the maximum length %s' % maximum_length
        )

    return value


@disable_on_env
def none(value,
         allow_empty = False,
         **kwargs):
    """Validate that ``value`` is :obj:`None <python:None>`.

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns :obj:`None <python:None>` if ``value``
      is empty but **not** :obj:`None <python:None>`. If  ``False``, raises a
      :class:`NotNoneError` if ``value`` is empty but **not**
      :obj:`None <python:None>`. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :returns: :obj:`None <python:None>`

    :raises NotNoneError: if ``allow_empty`` is ``False`` and ``value`` is empty
      but **not** :obj:`None <python:None>` and

    """
    if value is not None and not value and allow_empty:
        pass
    elif (value is not None and not value) or value:
        raise errors.NotNoneError('value was not None')

    return None


@disable_on_env
def not_empty(value,
              allow_empty = False,
              **kwargs):
    """Validate that ``value`` is not empty.

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns :obj:`None <python:None>` if
      ``value`` is empty. If ``False``, raises a
      :class:`EmptyValueError <validator_collection.errors.EmptyValueError>`
      if ``value`` is empty. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :returns: ``value`` / :obj:`None <python:None>`

    :raises EmptyValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    """
    if not value and allow_empty:
        return None
    elif not value:
        raise errors.EmptyValueError('value was empty')

    return value


@disable_on_env
def variable_name(value,
                  allow_empty = False,
                  **kwargs):
    """Validate that the value is a valid Python variable name.

    .. caution::

      This function does **NOT** check whether the variable exists. It only
      checks that the ``value`` would work as a Python variable (or class, or
      function, etc.) name.

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns :obj:`None <python:None>` if
      ``value`` is empty. If ``False``, raises a
      :class:`EmptyValueError <validator_collection.errors.EmptyValueError>`
      if ``value`` is empty. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :returns: ``value`` / :obj:`None <python:None>`
    :rtype: :class:`str <python:str>` or :obj:`None <python:None>`

    :raises EmptyValueError: if ``allow_empty`` is ``False`` and ``value``
      is empty
    """
    if not value and not allow_empty:
        raise errors.EmptyValueError('value (%s) was empty' % value)
    elif not value:
        return None

    try:
        parse('%s = None' % value)
    except (SyntaxError, ValueError, TypeError):
        raise errors.InvalidVariableNameError(
            'value (%s) is not a valid variable name' % value
        )

    return value


@disable_on_env
def dict(value,
         allow_empty = False,
         json_serializer = None,
         **kwargs):
    """Validate that ``value`` is a :class:`dict <python:dict>`.

    .. hint::

      If ``value`` is a string, this validator will assume it is a JSON
      object and try to convert it into a :class:`dict <python:dict>`

      You can override the JSON serializer used by passing it to the
      ``json_serializer`` property. By default, will utilize the Python
      :class:`json <json>` encoder/decoder.

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns :obj:`None <python:None>` if
      ``value`` is empty. If ``False``, raises a
      :class:`EmptyValueError <validator_collection.errors.EmptyValueError>`
      if ``value`` is empty. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :param json_serializer: The JSON encoder/decoder to use to deserialize a
      string passed in ``value``. If not supplied, will default to the Python
      :class:`json <python:json>` encoder/decoder.
    :type json_serializer: callable

    :returns: ``value`` / :obj:`None <python:None>`
    :rtype: :class:`dict <python:dict>` / :obj:`None <python:None>`

    :raises EmptyValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    :raises CannotCoerceError: if ``value`` cannot be coerced to a
      :class:`dict <python:dict>`
    :raises NotADictError: if ``value`` is not a :class:`dict <python:dict>`

    """
    original_value = value
    if not value and not allow_empty:
        raise errors.EmptyValueError('value (%s) was empty' % value)
    elif not value:
        return None

    if json_serializer is None:
        json_serializer = json_

    if isinstance(value, str):
        try:
            value = json_serializer.loads(value)
        except Exception:
            raise errors.CannotCoerceError(
                'value (%s) cannot be coerced to a dict' % original_value
            )

        value = dict(value,
                     json_serializer = json_serializer)

    if not isinstance(value, dict_):
        raise errors.NotADictError('value (%s) is not a dict' % original_value)

    return value


@disable_on_env
def json(value,
         schema = None,
         allow_empty = False,
         json_serializer = None,
         **kwargs):
    """Validate that ``value`` conforms to the supplied JSON Schema.

    .. note::

      ``schema`` supports JSON Schema Drafts 3 - 7. Unless the JSON Schema indicates the
      meta-schema using a ``$schema`` property, the schema will be assumed to conform to
      Draft 7.

    .. hint::

      If either ``value`` or ``schema`` is a string, this validator will assume it is a
      JSON object and try to convert it into a :class:`dict <python:dict>`.

      You can override the JSON serializer used by passing it to the
      ``json_serializer`` property. By default, will utilize the Python
      :class:`json <json>` encoder/decoder.

    :param value: The value to validate.

    :param schema: An optional JSON Schema against which ``value`` will be validated.

    :param allow_empty: If ``True``, returns :obj:`None <python:None>` if
      ``value`` is empty. If ``False``, raises a
      :class:`EmptyValueError <validator_collection.errors.EmptyValueError>`
      if ``value`` is empty. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :param json_serializer: The JSON encoder/decoder to use to deserialize a
      string passed in ``value``. If not supplied, will default to the Python
      :class:`json <python:json>` encoder/decoder.
    :type json_serializer: callable

    :returns: ``value`` / :obj:`None <python:None>`
    :rtype: :class:`dict <python:dict>` / :class:`list <python:list>` of
      :class:`dict <python:dict>` / :obj:`None <python:None>`

    :raises EmptyValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    :raises CannotCoerceError: if ``value`` cannot be coerced to a
      :class:`dict <python:dict>`
    :raises NotJSONError: if ``value`` cannot be deserialized from JSON
    :raises NotJSONSchemaError: if ``schema`` is not a valid JSON Schema object
    :raises JSONValidationError: if ``value`` does not validate against the JSON Schema

    """
    original_value = value
    original_schema = schema

    if not value and not allow_empty:
        raise errors.EmptyValueError('value (%s) was empty' % value)
    elif not value:
        return None

    if not json_serializer:
        json_serializer = json_

    if isinstance(value, str):
        try:
            value = json_serializer.loads(value)
        except Exception:
            raise errors.CannotCoerceError(
                'value (%s) cannot be deserialized from JSON' % original_value
            )
    if isinstance(schema, str):
        try:
            schema = dict(schema,
                          allow_empty = allow_empty,
                          json_serializer = json_serializer,
                          **kwargs)
        except Exception:
            raise errors.CannotCoerceError(
                'schema (%s) cannot be coerced to a dict' % original_schema
            )

    if not isinstance(value, (list, dict_)):
        raise errors.NotJSONError('value (%s) is not a JSON object' % original_value)

    if original_schema and not isinstance(schema, dict_):
        raise errors.NotJSONError('schema (%s) is not a JSON object' % original_schema)

    if not schema:
        return value

    try:
        jsonschema.validate(value, schema)
    except jsonschema.exceptions.ValidationError as error:
        raise errors.JSONValidationError(error.message)
    except jsonschema.exceptions.SchemaError as error:
        raise errors.NotJSONSchemaError(error.message)

    return value


## DATE / TIME


@disable_on_env
def date(value,
         allow_empty = False,
         minimum = None,
         maximum = None,
         coerce_value = True,
         **kwargs):
    """Validate that ``value`` is a valid date.

    :param value: The value to validate.
    :type value: :class:`str <python:str>` / :class:`datetime <python:datetime.datetime>`
      / :class:`date <python:datetime.date>` / :obj:`None <python:None>`

    :param allow_empty: If ``True``, returns :obj:`None <python:None>` if
      ``value`` is empty. If ``False``, raises a
      :class:`EmptyValueError <validator_collection.errors.EmptyValueError>`
      if ``value`` is empty. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :param minimum: If supplied, will make sure that ``value`` is on or after this value.
    :type minimum: :class:`datetime <python:datetime.datetime>` /
      :class:`date <python:datetime.date>` / compliant :class:`str <python:str>`
      / :obj:`None <python:None>`

    :param maximum: If supplied, will make sure that ``value`` is on or before this
      value.
    :type maximum: :class:`datetime <python:datetime.datetime>` /
      :class:`date <python:datetime.date>` / compliant :class:`str <python:str>`
      / :obj:`None <python:None>`

    :param coerce_value: If ``True``, will attempt to coerce ``value`` to a
      :class:`date <python:datetime.date>` if it is a timestamp value. If ``False``,
      will not.
    :type coerce_value: :class:`bool <python:bool>`

    :returns: ``value`` / :obj:`None <python:None>`
    :rtype: :class:`date <python:datetime.date>` / :obj:`None <python:None>`

    :raises EmptyValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    :raises CannotCoerceError: if ``value`` cannot be coerced to a
      :class:`date <python:datetime.date>` and is not :obj:`None <python:None>`
    :raises MinimumValueError: if ``minimum`` is supplied but ``value`` occurs before
      ``minimum``
    :raises MaximumValueError: if ``maximum`` is supplied but ``value`` occurs after
      ``maximum``

    """
    # pylint: disable=too-many-branches
    if not value and not allow_empty:
        raise errors.EmptyValueError('value (%s) was empty' % value)
    elif not value:
        return None

    minimum = date(minimum, allow_empty = True, force_run = True)               # pylint: disable=E1123
    maximum = date(maximum, allow_empty = True, force_run = True)               # pylint: disable=E1123

    if not isinstance(value, date_types):
        raise errors.CannotCoerceError(
            'value (%s) must be a date object, datetime object, '
            'ISO 8601-formatted string, '
            'or POSIX timestamp, but was %s' % (value, type(value))
        )
    elif isinstance(value, datetime_.datetime) and not coerce_value:
        raise errors.CannotCoerceError(
            'value (%s) must be a date object, or '
            'ISO 8601-formatted string, '
            'but was %s' % (value, type(value))
        )
    elif isinstance(value, datetime_.datetime) and coerce_value:
        value = value.date()
    elif isinstance(value, timestamp_types) and coerce_value:
        try:
            value = datetime_.date.fromtimestamp(value)
        except ValueError:
            raise errors.CannotCoerceError(
                'value (%s) must be a date object, datetime object, '
                'ISO 8601-formatted string, '
                'or POSIX timestamp, but was %s' % (value, type(value))
            )
    elif isinstance(value, str):
        try:
            value = datetime_.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
            if coerce_value:
                value = value.date()
            else:
                raise errors.CannotCoerceError(
                    'value (%s) must be a date object, '
                    'ISO 8601-formatted string, '
                    'or POSIX timestamp, but was %s' % (value, type(value))
                )
        except ValueError:
            if len(value) > 10 and not coerce_value:
                raise errors.CannotCoerceError(
                    'value (%s) must be a date object, or '
                    'ISO 8601-formatted string, '
                    'but was %s' % (value, type(value))
                )
            if ' ' in value:
                value = value.split(' ')[0]
            if 'T' in value:
                value = value.split('T')[0]

            if len(value) != 10:
                raise errors.CannotCoerceError(
                    'value (%s) must be a date object, datetime object, '
                    'ISO 8601-formatted string, '
                    'or POSIX timestamp, but was %s' % (value, type(value))
                )
            try:
                year = int(value[:4])
                month = int(value[5:7])
                day = int(value[-2:])
                value = datetime_.date(year, month, day)
            except (ValueError, TypeError):
                raise errors.CannotCoerceError(
                    'value (%s) must be a date object, datetime object, '
                    'ISO 8601-formatted string, '
                    'or POSIX timestamp, but was %s' % (value, type(value))
                )
    elif isinstance(value, numeric_types) and not coerce_value:
        raise errors.CannotCoerceError(
            'value (%s) must be a date object, or '
            'ISO 8601-formatted string, '
            'but was %s' % (value, type(value))
        )


    if minimum and value and value < minimum:
        raise errors.MinimumValueError(
            'value (%s) is before the minimum given (%s)' % (value.isoformat(),
                                                             minimum.isoformat())
        )
    if maximum and value and value > maximum:
        raise errors.MaximumValueError(
            'value (%s) is after the maximum given (%s)' % (value.isoformat(),
                                                            maximum.isoformat())
        )

    return value


@disable_on_env
def datetime(value,
             allow_empty = False,
             minimum = None,
             maximum = None,
             coerce_value = True,
             **kwargs):
    """Validate that ``value`` is a valid datetime.

    .. caution::

      If supplying a string, the string needs to be in an ISO 8601-format to pass
      validation. If it is not in an ISO 8601-format, validation will fail.

    :param value: The value to validate.
    :type value: :class:`str <python:str>` / :class:`datetime <python:datetime.datetime>`
      / :class:`date <python:datetime.date>` / :obj:`None <python:None>`

    :param allow_empty: If ``True``, returns :obj:`None <python:None>` if
      ``value`` is empty. If ``False``, raises a
      :class:`EmptyValueError <validator_collection.errors.EmptyValueError>`
      if ``value`` is empty. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :param minimum: If supplied, will make sure that ``value`` is on or after this value.
    :type minimum: :class:`datetime <python:datetime.datetime>` /
      :class:`date <python:datetime.date>` / compliant :class:`str <python:str>` /
      :obj:`None <python:None>`

    :param maximum: If supplied, will make sure that ``value`` is on or before this
      value.
    :type maximum: :class:`datetime <python:datetime.datetime>` /
      :class:`date <python:datetime.date>` / compliant :class:`str <python:str>` /
      :obj:`None <python:None>`

    :param coerce_value: If ``True``, will coerce dates to
      :class:`datetime <python:datetime.datetime>` objects with times of 00:00:00. If ``False``, will error
      if ``value`` is not an unambiguous timestamp. Defaults to ``True``.
    :type coerce_value: :class:`bool <python:bool>`

    :returns: ``value`` / :obj:`None <python:None>`
    :rtype: :class:`datetime <python:datetime.datetime>` / :obj:`None <python:None>`

    :raises EmptyValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    :raises CannotCoerceError: if ``value`` cannot be coerced to a
      :class:`datetime <python:datetime.datetime>` value and is not
      :obj:`None <python:None>`
    :raises MinimumValueError: if ``minimum`` is supplied but ``value`` occurs
      before ``minimum``
    :raises MaximumValueError: if ``maximum`` is supplied but ``value`` occurs
      after ``minimum``

    """
    # pylint: disable=too-many-branches
    if not value and not allow_empty:
        raise errors.EmptyValueError('value (%s) was empty' % value)
    elif not value:
        return None

    minimum = datetime(minimum, allow_empty = True, force_run = True)           # pylint: disable=E1123
    maximum = datetime(maximum, allow_empty = True, force_run = True)           # pylint: disable=E1123

    if not isinstance(value, datetime_types):
        raise errors.CannotCoerceError(
            'value (%s) must be a date object, datetime object, '
            'ISO 8601-formatted string, '
            'or POSIX timestamp, but was %s' % (value,
                                                type(value))
        )
    elif isinstance(value, timestamp_types) and coerce_value:
        try:
            value = datetime_.datetime.fromtimestamp(value)
        except ValueError:
            raise errors.CannotCoerceError(
                'value (%s) must be a date object, datetime object, '
                'ISO 8601-formatted string, '
                'or POSIX timestamp, but was %s' % (value,
                                                    type(value))
            )
    elif isinstance(value, str):
        # pylint: disable=line-too-long
        try:
            if 'T' in value:
                value = datetime_.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f%z')
            else:
                value = datetime_.datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f%z')
        except ValueError:
            try:
                if 'T' in value:
                    value = datetime_.datetime.strptime(value, '%Y/%m/%dT%H:%M:%S%z')
                else:
                    value = datetime_.datetime.strptime(value, '%Y/%m/%d %H:%M:%S%z')
            except ValueError:
                try:
                    if 'T' in value:
                        value = datetime_.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S%z')
                    else:
                        value = datetime_.datetime.strptime(value, '%Y-%m-%d %H:%M:%S%z')
                except ValueError:
                    try:
                        if 'T' in value:
                            value = datetime_.datetime.strptime(value,
                                                                '%Y/%m/%dT%H:%M:%S%z')
                        else:
                            value = datetime_.datetime.strptime(value,
                                                                '%Y/%m/%d %H:%M:%S%z')
                    except ValueError:
                        try:
                            if 'T' in value:
                                value = datetime_.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                            else:
                                value = datetime_.datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')
                        except ValueError:
                            try:
                                if 'T' in value:
                                    value = datetime_.datetime.strptime(value, '%Y/%m/%dT%H:%M:%S')
                                else:
                                    value = datetime_.datetime.strptime(value, '%Y/%m/%d %H:%M:%S')
                            except ValueError:
                                try:
                                    if 'T' in value:
                                        value = datetime_.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
                                    else:
                                        value = datetime_.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                                except ValueError:
                                    try:
                                        if 'T' in value:
                                            value = datetime_.datetime.strptime(value,
                                                                                '%Y/%m/%dT%H:%M:%S')
                                        else:
                                            value = datetime_.datetime.strptime(value,
                                                                                '%Y/%m/%d %H:%M:%S')
                                    except ValueError:
                                        if coerce_value:
                                            value = date(value)
                                        else:
                                            raise errors.CannotCoerceError(
                                                'value (%s) must be a datetime object, '
                                                'ISO 8601-formatted string, '
                                                'or POSIX timestamp' % value
                                            )
    # pylint: enable=line-too-long
    elif isinstance(value, numeric_types) and not coerce_value:
        raise errors.CannotCoerceError(
            'value (%s) must be a datetime object, '
            'ISO 8601-formatted string, '
            'or POSIX timestamp' % value
        )

    if isinstance(value, datetime_.date) and not isinstance(value, datetime_.datetime):
        if coerce_value:
            value = datetime_.datetime(value.year,                                  # pylint: disable=R0204
                                       value.month,
                                       value.day,
                                       0,
                                       0,
                                       0,
                                       0)
        else:
            raise errors.CannotCoerceError(
                'value (%s) must be a datetime object, '
                'ISO 8601-formatted string, '
                'or POSIX timestamp' % value
            )


    if minimum and value and value < minimum:
        raise errors.MinimumValueError(
            'value (%s) is before the minimum given (%s)' % (value.isoformat(),
                                                             minimum.isoformat())
        )
    if maximum and value and value > maximum:
        raise errors.MaximumValueError(
            'value (%s) is after the maximum given (%s)' % (value.isoformat(),
                                                            maximum.isoformat())
        )

    return value


@disable_on_env
def time(value,
         allow_empty = False,
         minimum = None,
         maximum = None,
         coerce_value = True,
         **kwargs):
    """Validate that ``value`` is a valid :class:`time <python:datetime.time>`.

    .. caution::

      This validator will **always** return the time as timezone naive (effectively
      UTC). If ``value`` has a timezone / UTC offset applied, the validator will
      coerce the value returned back to UTC.

    :param value: The value to validate.
    :type value: :func:`datetime <validator_collection.validators.datetime>` or
      :func:`time <validator_collection.validators.time>`-compliant
      :class:`str <python:str>` / :class:`datetime <python:datetime.datetime>` /
      :class:`time <python:datetime.time> / numeric / :obj:`None <python:None>`

    :param allow_empty: If ``True``, returns :obj:`None <python:None>` if
      ``value`` is empty. If ``False``, raises a
      :class:`EmptyValueError <validator_collection.errors.EmptyValueError>`
      if ``value`` is empty. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :param minimum: If supplied, will make sure that ``value`` is on or after this value.
    :type minimum: :func:`datetime <validator_collection.validators.datetime>` or
      :func:`time <validator_collection.validators.time>`-compliant
      :class:`str <python:str>` / :class:`datetime <python:datetime.datetime>` /
      :class:`time <python:datetime.time> / numeric / :obj:`None <python:None>`

    :param maximum: If supplied, will make sure that ``value`` is on or before this
      value.
    :type maximum: :func:`datetime <validator_collection.validators.datetime>` or
      :func:`time <validator_collection.validators.time>`-compliant
      :class:`str <python:str>` / :class:`datetime <python:datetime.datetime>` /
      :class:`time <python:datetime.time> / numeric / :obj:`None <python:None>`

    :param coerce_value: If ``True``, will attempt to coerce/extract a
      :class:`time <python:datetime.time>` from ``value``. If ``False``, will only
      respect direct representations of time. Defaults to ``True``.
    :type coerce_value: :class:`bool <python:bool>`

    :returns: ``value`` in UTC time / :obj:`None <python:None>`
    :rtype: :class:`time <python:datetime.time>` / :obj:`None <python:None>`

    :raises EmptyValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    :raises CannotCoerceError: if ``value`` cannot be coerced to a
      :class:`time <python:datetime.time>` and is not :obj:`None <python:None>`
    :raises MinimumValueError: if ``minimum`` is supplied but ``value`` occurs
      before ``minimum``
    :raises MaximumValueError: if ``maximum`` is supplied but ``value`` occurs
      after ``minimum``

    """
    # pylint: disable=too-many-branches
    if not value and not allow_empty:
        if isinstance(value, datetime_.time):
            pass
        else:
            raise errors.EmptyValueError('value (%s) was empty' % value)
    elif not value:
        if not isinstance(value, datetime_.time):
            return None

    minimum = time(minimum, allow_empty = True, force_run = True)               # pylint: disable=E1123
    maximum = time(maximum, allow_empty = True, force_run = True)               # pylint: disable=E1123

    if not isinstance(value, time_types):
        raise errors.CannotCoerceError(
            'value (%s) must be a datetime object, '
            'ISO 8601-formatted string, '
            'or POSIX timestamp, but was %s' % (value,
                                                type(value))
        )
    elif isinstance(value, datetime_.datetime) and not coerce_value:
        raise errors.CannotCoerceError(
            'value (%s) must be a datetime object, '
            'ISO 8601-formatted string, '
            'or POSIX timestamp, but was %s' % (value,
                                                type(value))
        )
    elif isinstance(value, datetime_.datetime) and coerce_value:
        value = value.time()
    elif isinstance(value, timestamp_types):
        try:
            datetime_value = datetime(value, force_run = True)                  # pylint: disable=E1123
            if coerce_value:
                value = datetime_value.time()
            else:
                raise errors.CannotCoerceError(
                    'value (%s) must be a time object, '
                    'ISO 8601-formatted string, '
                    'but was %s' % (value,
                                    type(value))
                )
        except ValueError:
            raise errors.CannotCoerceError(
                'value (%s) must be a datetime object, '
                'ISO 8601-formatted string, '
                'or POSIX timestamp, but was %s' % (value,
                                                    type(value))
            )
    elif isinstance(value, basestring):
        is_value_calculated = False
        if len(value) > 10:
            try:
                datetime_value = datetime(value, force_run = True)              # pylint: disable=E1123
                if coerce_value:
                    value = datetime_value.time()
                else:
                    raise errors.CannotCoerceError(
                        'value (%s) must be a time object, '
                        'ISO 8601-formatted string, '
                        'but was %s' % (value,
                                        type(value))
                    )
                is_value_calculated = True
            except ValueError:
                pass

        if not is_value_calculated:
            try:
                if '+' in value:
                    components = value.split('+')
                    is_offset_positive = True
                elif '-' in value:
                    components = value.split('-')
                    is_offset_positive = False
                else:
                    raise ValueError()

                time_string = components[0]
                if len(components) > 1:
                    utc_offset = components[1]
                else:
                    utc_offset = None

                time_components = time_string.split(':')
                hour = int(time_components[0])
                minutes = int(time_components[1])
                seconds = time_components[2]
                if '.' in seconds:
                    second_components = seconds.split('.')
                    seconds = int(second_components[0])
                    microseconds = int(second_components[1])
                else:
                    microseconds = 0

                utc_offset = timezone(utc_offset,                               # pylint: disable=E1123
                                      allow_empty = True,
                                      positive = is_offset_positive,
                                      force_run = True)

                value = datetime_.time(hour = hour,
                                       minute = minutes,
                                       second = seconds,
                                       microsecond = microseconds,
                                       tzinfo = utc_offset)
            except (ValueError, TypeError, IndexError):
                raise errors.CannotCoerceError(
                    'value (%s) must be a datetime object, '
                    'ISO 8601-formatted string, '
                    'or POSIX timestamp, but was %s' % (value,
                                                        type(value))
                )

        if value is not None:
            value = value.replace(tzinfo = None)

    if minimum is not None and value and value < minimum:
        raise errors.MinimumValueError(
            'value (%s) is before the minimum given (%s)' % (value.isoformat(),
                                                             minimum.isoformat())
        )
    if maximum is not None and value and value > maximum:
        raise errors.MaximumValueError(
            'value (%s) is after the maximum given (%s)' % (value.isoformat(),
                                                            maximum.isoformat())
        )

    return value


@disable_on_env
def timezone(value,
             allow_empty = False,
             positive = True,
             **kwargs):
    """Validate that ``value`` is a valid :class:`tzinfo <python:datetime.tzinfo>`.

    .. caution::

      This does **not** verify whether the value is a timezone that actually
      exists, nor can it resolve timezone names (e.g. ``'Eastern'`` or ``'CET'``).

      For that kind of functionality, we recommend you utilize:
      `pytz <https://pypi.python.org/pypi/pytz>`_

    :param value: The value to validate.
    :type value: :class:`str <python:str>` / :class:`tzinfo <python:datetime.tzinfo>`
      / numeric / :obj:`None <python:None>`

    :param allow_empty: If ``True``, returns :obj:`None <python:None>` if
      ``value`` is empty. If ``False``, raises a
      :class:`EmptyValueError <validator_collection.errors.EmptyValueError>`
      if ``value`` is empty. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :param positive: Indicates whether the ``value`` is positive or negative
      (only has meaning if ``value`` is a string). Defaults to ``True``.
    :type positive: :class:`bool <python:bool>`

    :returns: ``value`` / :obj:`None <python:None>`
    :rtype: :class:`tzinfo <python:datetime.tzinfo>` / :obj:`None <python:None>`

    :raises EmptyValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    :raises CannotCoerceError: if ``value`` cannot be coerced to
      :class:`tzinfo <python:datetime.tzinfo>` and is not :obj:`None <python:None>`
    :raises PositiveOffsetMismatchError: if ``positive`` is ``True``, but the offset
      indicated by ``value`` is actually negative
    :raises NegativeOffsetMismatchError: if ``positive`` is ``False``, but the offset
      indicated by ``value`` is actually positive

    """
    # pylint: disable=too-many-branches
    original_value = value

    if not value and not allow_empty:
        raise errors.EmptyValueError('value (%s) was empty' % value)
    elif not value:
        return None

    if not isinstance(value, tzinfo_types):
        raise errors.CannotCoerceError(
            'value (%s) must be a tzinfo, '
            'UTC offset in seconds expressed as a number, '
            'UTC offset expressed as string of form +HH:MM, '
            'but was %s' % (value, type(value))
        )
    elif isinstance(value, datetime_.datetime):
        value = value.tzinfo
    elif isinstance(value, datetime_.date):
        return None
    elif isinstance(value, datetime_.time):
        return value.tzinfo
    elif isinstance(value, timestamp_types):
        return None
    elif isinstance(value, str):
        if '+' not in value and '-' not in value:
            try:
                datetime_value = datetime(value, force_run = True)              # pylint: disable=E1123
                return datetime_value.tzinfo
            except TypeError:
                raise errors.CannotCoerceError(
                    'value (%s) must be a tzinfo, '
                    'UTC offset in seconds expressed as a number, '
                    'UTC offset expressed as string of form +HH:MM, '
                    'but was %s' % (value, type(value))
                )
        elif '-' in value:
            try:
                datetime_value = datetime(value, force_run = True)              # pylint: disable=E1123
                return datetime_value.tzinfo
            except TypeError:
                pass

        if '+' in value and not positive:
            raise errors.NegativeOffsetMismatchError(
                'expected a negative UTC offset but value is positive'
            )
        elif '-' in value and positive and len(value) == 6:
            positive = False
        elif '-' in value and positive:
            raise errors.PositiveOffsetMismatchError(
                'expected a positive UTC offset but value is negative'
            )

        if '+' in value:
            value = value[value.find('+'):]
        elif '-' in value:
            value = value[value.rfind('-'):]

        value = value[1:]

        offset_components = value.split(':')
        if len(offset_components) != 2:
            raise errors.CannotCoerceError(
                'value (%s) must be a tzinfo, '
                'UTC offset in seconds expressed as a number, '
                'UTC offset expressed as string of form +HH:MM, '
                'but was %s' % (value, type(value))
            )
        hour = int(offset_components[0])
        minutes = int(offset_components[1])

        value = (hour * 60 * 60) + (minutes * 60)

        if not positive:
            value = 0 - value

    if isinstance(value, numeric_types):
        if value > 0:
            positive = True
        elif value < 0:
            positive = False
        elif value == 0:
            return None

        offset = datetime_.timedelta(seconds = value)
        if is_py2:
            value = TimeZone(offset = offset)
        elif is_py3:
            try:
                value = TimeZone(offset)
            except ValueError:
                raise errors.UTCOffsetError(
                    'value (%s) cannot exceed +/- 24h' % original_value
                )
        else:
            raise NotImplementedError()

    return value


## NUMBERS

@disable_on_env
def numeric(value,
            allow_empty = False,
            minimum = None,
            maximum = None,
            **kwargs):
    """Validate that ``value`` is a numeric value.

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns :obj:`None <python:None>` if ``value``
      is :obj:`None <python:None>`. If ``False``, raises an
      :class:`EmptyValueError <validator_collection.errors.EmptyValueError>` if
      ``value`` is :obj:`None <python:None>`.
      Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :param minimum: If supplied, will make sure that ``value`` is greater than or
      equal to this value.
    :type minimum: numeric

    :param maximum: If supplied, will make sure that ``value`` is less than or
      equal to this value.
    :type maximum: numeric

    :returns: ``value`` / :obj:`None <python:None>`

    :raises EmptyValueError: if ``value`` is :obj:`None <python:None>` and
      ``allow_empty`` is ``False``
    :raises MinimumValueError: if ``minimum`` is supplied and ``value`` is less
      than the ``minimum``
    :raises MaximumValueError: if ``maximum`` is supplied and ``value`` is more
      than the ``maximum``
    :raises CannotCoerceError: if ``value`` cannot be coerced to a numeric form

    """
    if maximum is None:
        maximum = POSITIVE_INFINITY
    else:
        maximum = numeric(maximum)
    if minimum is None:
        minimum = NEGATIVE_INFINITY
    else:
        minimum = numeric(minimum)

    if value is None and not allow_empty:
        raise errors.EmptyValueError('value (%s) was empty' % value)
    elif value is not None:
        if isinstance(value, str):
            try:
                value = float_(value)
            except (ValueError, TypeError):
                raise errors.CannotCoerceError(
                    'value (%s) cannot be coerced to a numeric form' % value
                )
        elif not isinstance(value, numeric_types):
            raise errors.CannotCoerceError(
                'value (%s) is not a numeric type, was %s' % (value,
                                                              type(value))
            )

    if value is not None and value > maximum:
        raise errors.MaximumValueError(
            'value (%s) exceeds maximum (%s)' % (value, maximum)
        )

    if value is not None and value < minimum:
        raise errors.MinimumValueError(
            'value (%s) less than minimum (%s)' % (value, minimum)
        )

    return value


@disable_on_env
def integer(value,
            allow_empty = False,
            coerce_value = False,
            minimum = None,
            maximum = None,
            base = 10,
            **kwargs):
    """Validate that ``value`` is an :class:`int <python:int>`.

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns :obj:`None <python:None>` if
      ``value`` is :obj:`None <python:None>`. If  ``False``, raises a
      :class:`EmptyValueError <validator_collection.errors.EmptyValueError>` if
      ``value`` is :obj:`None <python:None>`.
      Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :param coerce_value: If ``True``, will force any numeric ``value`` to an integer
      (always rounding up). If ``False``, will raise an error if ``value`` is numeric
      but not a whole number. Defaults to ``False``.
    :type coerce_value: :class:`bool <python:bool>`

    :param minimum: If supplied, will make sure that ``value`` is greater than or
      equal to this value.
    :type minimum: numeric

    :param maximum: If supplied, will make sure that ``value`` is less than or
      equal to this value.
    :type maximum: numeric

    :param base: Indicates the base that is used to determine the integer value.
      The allowed values are 0 and 2–36. Base-2, -8, and -16 literals can be
      optionally prefixed with ``0b/0B``, ``0o/0O/0``, or ``0x/0X``, as with
      integer literals in code. Base 0 means to interpret the string exactly as
      an integer literal, so that the actual base is 2, 8, 10, or 16. Defaults to
      ``10``.

    :returns: ``value`` / :obj:`None <python:None>`

    :raises EmptyValueError: if ``value`` is :obj:`None <python:None>` and
      ``allow_empty`` is ``False``
    :raises MinimumValueError: if ``minimum`` is supplied and ``value`` is less
      than the ``minimum``
    :raises MaximumValueError: if ``maximum`` is supplied and ``value`` is more
      than the ``maximum``
    :raises NotAnIntegerError: if ``coerce_value`` is ``False``, and ``value``
      is not an integer
    :raises CannotCoerceError: if ``value`` cannot be coerced to an
      :class:`int <python:int>`

    """
    value = numeric(value,                                                      # pylint: disable=E1123
                    allow_empty = allow_empty,
                    minimum = minimum,
                    maximum = maximum,
                    force_run = True)

    if value is not None and hasattr(value, 'is_integer'):
        if value.is_integer():
            return int(value)

    if value is not None and coerce_value:
        float_value = math.ceil(value)
        if is_py2:
            value = int(float_value)                                            # pylint: disable=R0204
        elif is_py3:
            str_value = str(float_value)
            value = int(str_value, base = base)
        else:
            raise NotImplementedError('Python %s not supported' % os.sys.version)
    elif value is not None and not isinstance(value, integer_types):
        raise errors.NotAnIntegerError('value (%s) is not an integer-type, '
                                       'is a %s'% (value, type(value))
                                      )

    return value


@disable_on_env
def float(value,
          allow_empty = False,
          minimum = None,
          maximum = None,
          **kwargs):
    """Validate that ``value`` is a :class:`float <python:float>`.

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns :obj:`None <python:None>` if
      ``value`` is :obj:`None <python:None>`. If  ``False``, raises a
      :class:`EmptyValueError <validator_collection.errors.EmptyValueError>` if
      ``value`` is :obj:`None <python:None>`. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :returns: ``value`` / :obj:`None <python:None>`
    :rtype: :class:`float <python:float>` / :obj:`None <python:None>`

    :raises EmptyValueError: if ``value`` is :obj:`None <python:None>` and
      ``allow_empty`` is ``False``
    :raises MinimumValueError: if ``minimum`` is supplied and ``value`` is less
      than the ``minimum``
    :raises MaximumValueError: if ``maximum`` is supplied and ``value`` is more
      than the ``maximum``
    :raises CannotCoerceError: if unable to coerce ``value`` to a
      :class:`float <python:float>`

    """
    try:
        value = _numeric_coercion(value,
                                  coercion_function = float_,
                                  allow_empty = allow_empty,
                                  minimum = minimum,
                                  maximum = maximum)
    except (errors.EmptyValueError,
            errors.CannotCoerceError,
            errors.MinimumValueError,
            errors.MaximumValueError) as error:
        raise error
    except Exception as error:
        raise errors.CannotCoerceError('unable to coerce value (%s) to float, '
                                       'for an unknown reason - please see '
                                       'stack trace' % value)

    return value


@disable_on_env
def fraction(value,
             allow_empty = False,
             minimum = None,
             maximum = None,
             **kwargs):
    """Validate that ``value`` is a :class:`Fraction <python:fractions.Fraction>`.

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns :obj:`None <python:None>` if ``value``
      is :obj:`None <python:None>`. If  ``False``, raises a
      :class:`EmptyValueError <validator_collection.errors.EmptyValueError>` if
      ``value`` is :obj:`None <python:None>`. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :returns: ``value`` / :obj:`None <python:None>`
    :rtype: :class:`Fraction <python:fractions.Fraction>` / :obj:`None <python:None>`

    :raises EmptyValueError: if ``value`` is :obj:`None <python:None>` and
      ``allow_empty`` is ``False``
    :raises MinimumValueError: if ``minimum`` is supplied and ``value`` is less
      than the ``minimum``
    :raises MaximumValueError: if ``maximum`` is supplied and ``value`` is more
      than the ``maximum``
    :raises CannotCoerceError: if unable to coerce ``value`` to a
      :class:`Fraction <python:fractions.Fraction>`

    """
    try:
        value = _numeric_coercion(value,
                                  coercion_function = fractions.Fraction,
                                  allow_empty = allow_empty,
                                  minimum = minimum,
                                  maximum = maximum)
    except (errors.EmptyValueError,
            errors.CannotCoerceError,
            errors.MinimumValueError,
            errors.MaximumValueError) as error:
        raise error
    except Exception as error:
        raise errors.CannotCoerceError('unable to coerce value (%s) to Fraction, '
                                       'for an unknown reason - please see '
                                       'stack trace' % value)

    return value


@disable_on_env
def decimal(value,
            allow_empty = False,
            minimum = None,
            maximum = None,
            **kwargs):
    """Validate that ``value`` is a :class:`Decimal <python:decimal.Decimal>`.

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns :obj:`None <python:None>` if ``value``
      is :obj:`None <python:None>`. If  ``False``, raises a
      :class:`EmptyValueError <validator_collection.errors.EmptyValueError>` if
      ``value`` is :obj:`None <python:None>`. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :param minimum: If supplied, will make sure that ``value`` is greater than or
      equal to this value.
    :type minimum: numeric

    :param maximum: If supplied, will make sure that ``value`` is less than or
      equal to this value.
    :type maximum: numeric

    :returns: ``value`` / :obj:`None <python:None>`
    :rtype: :class:`Decimal <python:decimal.Decimal>` / :obj:`None <python:None>`

    :raises EmptyValueError: if ``value`` is :obj:`None <python:None>` and
      ``allow_empty`` is ``False``
    :raises MinimumValueError: if ``minimum`` is supplied and ``value`` is less than the
      ``minimum``
    :raises MaximumValueError: if ``maximum`` is supplied and ``value`` is more than the
      ``maximum``
    :raises CannotCoerceError: if unable to coerce ``value`` to a
      :class:`Decimal <python:decimal.Decimal>`

    """
    if value is None and allow_empty:
        return None
    elif value is None:
        raise errors.EmptyValueError('value cannot be None')

    if isinstance(value, str):
        try:
            value = decimal_.Decimal(value.strip())
        except decimal_.InvalidOperation:
            raise errors.CannotCoerceError(
                'value (%s) cannot be converted to a Decimal' % value
            )
    elif isinstance(value, fractions.Fraction):
        try:
            value = float(value, force_run = True)                              # pylint: disable=R0204, E1123
        except ValueError:
            raise errors.CannotCoerceError(
                'value (%s) cannot be converted to a Decimal' % value
            )

    value = numeric(value,                                                      # pylint: disable=E1123
                    allow_empty = False,
                    maximum = maximum,
                    minimum = minimum,
                    force_run = True)

    if not isinstance(value, decimal_.Decimal):
        value = decimal_.Decimal(value)

    return value


def _numeric_coercion(value,
                      coercion_function = None,
                      allow_empty = False,
                      minimum = None,
                      maximum = None):
    """Validate that ``value`` is numeric and coerce using ``coercion_function``.

    :param value: The value to validate.

    :param coercion_function: The function to use to coerce ``value`` to the desired
      type.
    :type coercion_function: callable

    :param allow_empty: If ``True``, returns :obj:`None <python:None>` if
      ``value`` is :obj:`None <python:None>`. If  ``False``, raises a
      :class:`EmptyValueError <validator_collection.errors.EmptyValueError>` if
      ``value`` is :obj:`None <python:None>`. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :returns: ``value`` / :obj:`None <python:None>`
    :rtype: the type returned by ``coercion_function``

    :raises CoercionFunctionEmptyError: if ``coercion_function`` is empty
    :raises EmptyValueError: if ``value`` is :obj:`None <python:None>` and
      ``allow_empty`` is ``False``
    :raises CannotCoerceError: if ``coercion_function`` raises an
      :class:`ValueError <python:ValueError>`, :class:`TypeError <python:TypeError>`,
      :class:`AttributeError <python:AttributeError>`,
      :class:`IndexError <python:IndexError>, or
      :class:`SyntaxError <python:SyntaxError>`

    """
    if coercion_function is None:
        raise errors.CoercionFunctionEmptyError('coercion_function cannot be empty')
    elif not hasattr(coercion_function, '__call__'):
        raise errors.NotCallableError('coercion_function must be callable')

    value = numeric(value,                                                      # pylint: disable=E1123
                    allow_empty = allow_empty,
                    minimum = minimum,
                    maximum = maximum,
                    force_run = True)

    if value is not None:
        try:
            value = coercion_function(value)
        except (ValueError, TypeError, AttributeError, IndexError, SyntaxError):
            raise errors.CannotCoerceError(
                'cannot coerce value (%s) to desired type' % value
            )

    return value


## FILE-RELATED

@disable_on_env
def bytesIO(value,
            allow_empty = False,
            **kwargs):
    """Validate that ``value`` is a :class:`BytesIO <python:io.BytesIO>` object.

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns :obj:`None <python:None>` if
      ``value`` is empty. If ``False``, raises a
      :class:`EmptyValueError <validator_collection.errors.EmptyValueError>`
      if ``value`` is empty. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :returns: ``value`` / :obj:`None <python:None>`
    :rtype: :class:`BytesIO <python:io.BytesIO>` / :obj:`None <python:None>`

    :raises EmptyValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    :raises NotBytesIOError: if ``value`` is not a :class:`BytesIO <python:io.BytesIO>`
      object.
    """
    if not value and not allow_empty:
        raise errors.EmptyValueError('value (%s) was empty' % value)
    elif not value:
        return None

    if not isinstance(value, io.BytesIO):
        raise errors.NotBytesIOError('value (%s) is not a BytesIO, '
                                     'is a %s' % (value, type(value)))

    return value


@disable_on_env
def stringIO(value,
             allow_empty = False,
             **kwargs):
    """Validate that ``value`` is a :class:`StringIO <python:io.StringIO>` object.

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns :obj:`None <python:None>` if
      ``value`` is empty. If ``False``, raises a
      :class:`EmptyValueError <validator_collection.errors.EmptyValueError>`
      if ``value`` is empty. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :returns: ``value`` / :obj:`None <python:None>`
    :rtype: :class:`StringIO <python:io.StringIO>` / :obj:`None <python:None>`

    :raises EmptyValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    :raises NotStringIOError: if ``value`` is not a :class:`StringIO <python:io.StringIO>`
      object
    """
    if not value and not allow_empty:
        raise errors.EmptyValueError('value (%s) was empty' % value)
    elif not value:
        return None

    if not isinstance(value, io.StringIO):
        raise ValueError('value (%s) is not an io.StringIO object, '
                         'is a %s' % (value, type(value)))

    return value


@disable_on_env
def path(value,
         allow_empty = False,
         **kwargs):
    """Validate that ``value`` is a valid path-like object.

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns :obj:`None <python:None>` if
      ``value`` is empty. If ``False``, raises a
      :class:`EmptyValueError <validator_collection.errors.EmptyValueError>`
      if ``value`` is empty. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :returns: The path represented by ``value``.
    :rtype: Path-like object / :obj:`None <python:None>`

    :raises EmptyValueError: if ``allow_empty`` is ``False`` and ``value`` is empty
    :raises NotPathlikeError: if ``value`` is not a valid path-like object

    """
    if not value and not allow_empty:
        raise errors.EmptyValueError('value (%s) was empty' % value)
    elif not value:
        return None

    if hasattr(os, 'PathLike'):
        if not isinstance(value, (str, bytes, int, os.PathLike)):                    # pylint: disable=E1101
            raise errors.NotPathlikeError('value (%s) is path-like' % value)
    else:
        if not isinstance(value, int):
            try:
                os.path.exists(value)
            except TypeError:
                raise errors.NotPathlikeError('value (%s) is not path-like' % value)

    return value


@disable_on_env
def path_exists(value,
                allow_empty = False,
                **kwargs):
    """Validate that ``value`` is a path-like object that exists on the local
    filesystem.

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns :obj:`None <python:None>` if
      ``value`` is empty. If ``False``, raises a
      :class:`EmptyValueError <validator_collection.errors.EmptyValueError>`
      if ``value`` is empty. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :returns: The file name represented by ``value``.
    :rtype: Path-like object / :obj:`None <python:None>`

    :raises EmptyValueError: if ``allow_empty`` is ``False`` and ``value``
      is empty
    :raises NotPathlikeError: if ``value`` is not a path-like object
    :raises PathExistsError: if ``value`` does not exist

    """
    if not value and not allow_empty:
        raise errors.EmptyValueError('value (%s) was empty' % value)
    elif not value:
        return None

    value = path(value, force_run = True)                                       # pylint: disable=E1123

    if not os.path.exists(value):
        raise errors.PathExistsError('value (%s) not found' % value)

    return value


@disable_on_env
def file_exists(value,
                allow_empty = False,
                **kwargs):
    """Validate that ``value`` is a valid file that exists on the local filesystem.

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns :obj:`None <python:None>` if
      ``value`` is empty. If ``False``, raises a
      :class:`EmptyValueError <validator_collection.errors.EmptyValueError>`
      if ``value`` is empty. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :returns: The file name represented by ``value``.
    :rtype: Path-like object / :obj:`None <python:None>`

    :raises EmptyValueError: if ``allow_empty`` is ``False`` and ``value``
      is empty
    :raises NotPathlikeError: if ``value`` is not a path-like object
    :raises PathExistsError: if ``value`` does not exist on the local filesystem
    :raises NotAFileError: if ``value`` is not a valid file

    """
    if not value and not allow_empty:
        raise errors.EmptyValueError('value (%s) was empty' % value)
    elif not value:
        return None

    value = path_exists(value, force_run = True)                                # pylint: disable=E1123

    if not os.path.isfile(value):
        raise errors.NotAFileError('value (%s) is not a file')

    return value


@disable_on_env
def directory_exists(value,
                     allow_empty = False,
                     **kwargs):
    """Validate that ``value`` is a valid directory that exists on the local
    filesystem.

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns :obj:`None <python:None>` if
      ``value`` is empty. If ``False``, raises a
      :class:`EmptyValueError <validator_collection.errors.EmptyValueError>`
      if ``value`` is empty. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :returns: The file name represented by ``value``.
    :rtype: Path-like object / :obj:`None <python:None>`

    :raises EmptyValueError: if ``allow_empty`` is ``False`` and ``value``
      is empty
    :raises NotPathlikeError: if ``value`` is not a path-like object
    :raises PathExistsError: if ``value`` does not exist on the local filesystem
    :raises NotADirectoryError: if ``value`` is not a valid directory

    """
    if not value and not allow_empty:
        raise errors.EmptyValueError('value (%s) was empty' % value)
    elif not value:
        return None

    value = path_exists(value, force_run = True)                                # pylint: disable=E1123

    if not os.path.isdir(value):
        raise errors.NotADirectoryError('value (%s) is not a directory' % value)

    return value


@disable_on_env
def readable(value,
             allow_empty = False,
             **kwargs):
    """Validate that ``value`` is a path to a readable file.

    .. caution::

      **Use of this validator is an anti-pattern and should be used with caution.**

      Validating the readability of a file *before* attempting to read it
      exposes your code to a bug called
      `TOCTOU <https://en.wikipedia.org/wiki/Time_of_check_to_time_of_use>`_.

      This particular class of bug can expose your code to **security vulnerabilities**
      and so this validator should only be used if you are an advanced user.

      A better pattern to use when reading from a file is to apply the principle of
      EAFP ("easier to ask forgiveness than permission"), and simply attempt to
      write to the file using a ``try ... except`` block:

      .. code-block:: python

        try:
            with open('path/to/filename.txt', mode = 'r') as file_object:
                # read from file here
        except (OSError, IOError) as error:
            # Handle an error if unable to write.

    :param value: The path to a file on the local filesystem whose readability
      is to be validated.
    :type value: Path-like object

    :param allow_empty: If ``True``, returns :obj:`None <python:None>` if
      ``value`` is empty. If ``False``, raises a
      :class:`EmptyValueError <validator_collection.errors.EmptyValueError>`
      if ``value`` is empty. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :returns: Validated path-like object or :obj:`None <python:None>`
    :rtype: Path-like object or :obj:`None <python:None>`

    :raises EmptyValueError: if ``allow_empty`` is ``False`` and ``value``
      is empty
    :raises NotPathlikeError: if ``value`` is not a path-like object
    :raises PathExistsError: if ``value`` does not exist on the local filesystem
    :raises NotAFileError: if ``value`` is not a valid file
    :raises NotReadableError: if ``value`` cannot be opened for reading

    """
    if not value and not allow_empty:
        raise errors.EmptyValueError('value (%s) was empty' % value)
    elif not value:
        return None

    value = file_exists(value, force_run = True)                                # pylint: disable=E1123

    try:
        with open(value, mode='r'):
            pass
    except (OSError, IOError):
        raise errors.NotReadableError('file at %s could not be opened for '
                                      'reading' % value)

    return value

@disable_on_env
def writeable(value,
              allow_empty = False,
              **kwargs):
    """Validate that ``value`` is a path to a writeable file.

    .. caution::

      This validator does **NOT** work correctly on a Windows file system. This
      is due to the vagaries of how Windows manages its file system and the
      various ways in which it can manage file permission.

      If called on a Windows file system, this validator will raise
      :class:`NotImplementedError() <python:NotImplementedError>`.

    .. caution::

      **Use of this validator is an anti-pattern and should be used with caution.**

      Validating the writability of a file *before* attempting to write to it
      exposes your code to a bug called
      `TOCTOU <https://en.wikipedia.org/wiki/Time_of_check_to_time_of_use>`_.

      This particular class of bug can expose your code to **security vulnerabilities**
      and so this validator should only be used if you are an advanced user.

      A better pattern to use when writing to file is to apply the principle of
      EAFP ("easier to ask forgiveness than permission"), and simply attempt to
      write to the file using a ``try ... except`` block:

      .. code-block:: python

        try:
            with open('path/to/filename.txt', mode = 'a') as file_object:
                # write to file here
        except (OSError, IOError) as error:
            # Handle an error if unable to write.

    .. note::

      This validator relies on :func:`os.access() <python:os.access>` to check
      whether ``value`` is writeable. This function has certain limitations,
      most especially that:

      * It will **ignore** file-locking (yielding a false-positive) if the file
        is locked.
      * It focuses on *local operating system permissions*, which means if trying
        to access a path over a network you might get a false positive or false
        negative (because network paths may have more complicated authentication
        methods).

    :param value: The path to a file on the local filesystem whose writeability
      is to be validated.
    :type value: Path-like object

    :param allow_empty: If ``True``, returns :obj:`None <python:None>` if
      ``value`` is empty. If ``False``, raises a
      :class:`EmptyValueError <validator_collection.errors.EmptyValueError>`
      if ``value`` is empty. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :returns: Validated absolute path or :obj:`None <python:None>`
    :rtype: Path-like object or :obj:`None <python:None>`

    :raises EmptyValueError: if ``allow_empty`` is ``False`` and ``value``
      is empty
    :raises NotImplementedError: if used on a Windows system
    :raises NotPathlikeError: if ``value`` is not a path-like object
    :raises NotWriteableError: if ``value`` cannot be opened for writing

    """
    if not value and not allow_empty:
        raise errors.EmptyValueError('value (%s) was empty' % value)
    elif not value:
        return None

    value = path(value, force_run = True)

    if sys.platform in ['win32', 'cygwin']:
        raise NotImplementedError('not supported on Windows')

    is_valid = os.access(value, mode = os.W_OK)

    if not is_valid:
        raise errors.NotWriteableError('writing not allowed for file at %s' % value)

    return value

@disable_on_env
def executable(value,
               allow_empty = False,
               **kwargs):
    """Validate that ``value`` is a path to an executable file.

    .. caution::

      This validator does **NOT** work correctly on a Windows file system. This
      is due to the vagaries of how Windows manages its file system and the
      various ways in which it can manage file permission.

      If called on a Windows file system, this validator will raise
      :class:`NotImplementedError() <python:NotImplementedError>`.

    .. caution::

      **Use of this validator is an anti-pattern and should be used with caution.**

      Validating the executability of a file *before* attempting to execute it
      exposes your code to a bug called
      `TOCTOU <https://en.wikipedia.org/wiki/Time_of_check_to_time_of_use>`_.

      This particular class of bug can expose your code to **security vulnerabilities**
      and so this validator should only be used if you are an advanced user.

      A better pattern to use when writing to file is to apply the principle of
      EAFP ("easier to ask forgiveness than permission"), and simply attempt to
      execute the file using a ``try ... except`` block.

    .. note::

      This validator relies on :func:`os.access() <python:os.access>` to check
      whether ``value`` is executable. This function has certain limitations,
      most especially that:

      * It will **ignore** file-locking (yielding a false-positive) if the file
        is locked.
      * It focuses on *local operating system permissions*, which means if trying
        to access a path over a network you might get a false positive or false
        negative (because network paths may have more complicated authentication
        methods).

    :param value: The path to a file on the local filesystem whose writeability
      is to be validated.
    :type value: Path-like object

    :param allow_empty: If ``True``, returns :obj:`None <python:None>` if
      ``value`` is empty. If ``False``, raises a
      :class:`EmptyValueError <validator_collection.errors.EmptyValueError>`
      if ``value`` is empty. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :returns: Validated absolute path or :obj:`None <python:None>`
    :rtype: Path-like object or :obj:`None <python:None>`

    :raises EmptyValueError: if ``allow_empty`` is ``False`` and ``value``
      is empty
    :raises NotImplementedError: if used on a Windows system
    :raises NotPathlikeError: if ``value`` is not a path-like object
    :raises NotAFileError: if ``value`` does not exist on the local file system
    :raises NotExecutableError: if ``value`` cannot be executed

    """
    if not value and not allow_empty:
        raise errors.EmptyValueError('value (%s) was empty' % value)
    elif not value:
        return None

    value = file_exists(value, force_run = True)

    if sys.platform in ['win32', 'cygwin']:
        raise NotImplementedError('not supported on Windows')

    is_valid = os.access(value, mode = os.X_OK)

    if not is_valid:
        raise errors.NotExecutableError('execution not allowed for file at %s' % value)

    return value


## INTERNET-RELATED

@disable_on_env
def email(value,
          allow_empty = False,
          **kwargs):
    """Validate that ``value`` is a valid email address.

    .. note::

      Email address validation is...complicated. The methodology that we have
      adopted here is *generally* compliant with
      `RFC 5322 <https://tools.ietf.org/html/rfc5322>`_ and uses a combination of
      string parsing and regular expressions.

      String parsing in particular is used to validate certain *highly unusual*
      but still valid email patterns, including the use of escaped text and
      comments within an email address' local address (the user name part).

      This approach ensures more complete coverage for unusual edge cases, while
      still letting us use regular expressions that perform quickly.

    :param value: The value to validate.
    :type value: :class:`str <python:str>` / :obj:`None <python:None>`

    :param allow_empty: If ``True``, returns :obj:`None <python:None>` if
      ``value`` is empty. If ``False``, raises a
      :class:`EmptyValueError <validator_collection.errors.EmptyValueError>`
      if ``value`` is empty. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :returns: ``value`` / :obj:`None <python:None>`
    :rtype: :class:`str <python:str>` / :obj:`None <python:None>`

    :raises EmptyValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    :raises CannotCoerceError: if ``value`` is not a :class:`str <python:str>` or
      :obj:`None <python:None>`
    :raises InvalidEmailError: if ``value`` is not a valid email address or
      empty with ``allow_empty`` set to ``True``
    """
    # pylint: disable=too-many-branches,too-many-statements,R0914

    if not value and not allow_empty:
        raise errors.EmptyValueError('value (%s) was empty' % value)
    elif not value:
        return None

    if not isinstance(value, basestring):
        raise errors.CannotCoerceError('value must be a valid string, '
                                       'was %s' % type(value))

    if '@' not in value:
        raise errors.InvalidEmailError('value (%s) is not a valid email address' % value)
    if '(' in value and ')' in value:
        open_parentheses = value.find('(')
        close_parentheses = value.find(')') + 1

        if close_parentheses < open_parentheses:
            raise errors.InvalidEmailError('value (%s) is not a valid email '
                                           'address' % value)

        commented_value = value[open_parentheses:close_parentheses]
        value = value.replace(commented_value, '')
    elif '(' in value:
        raise errors.InvalidEmailError('value (%s) is not a valid email address' % value)
    elif ')' in value:
        raise errors.InvalidEmailError('value (%s) is not a valid email address' % value)

    if '<' in value or '>' in value:
        lt_position = value.find('<')
        gt_position = value.find('>')
        first_quote_position = -1
        second_quote_position = -1

        if lt_position >= 0:
            first_quote_position = value.find('"', 0, lt_position)
        if gt_position >= 0:
            second_quote_position = value.find('"', gt_position)

        if first_quote_position < 0 or second_quote_position < 0:
            raise errors.InvalidEmailError('value (%s) is not a valid email '
                                           'address' % value)

    at_count = value.count('@')
    if at_count > 1:
        last_at_position = 0
        last_quote_position = 0
        for x in range(0, at_count):                                            # pylint: disable=W0612
            at_position = value.find('@', last_at_position + 1)
            if at_position >= 0:
                first_quote_position = value.find('"',
                                                  last_quote_position,
                                                  at_position)
                second_quote_position = value.find('"',
                                                   first_quote_position)
                if first_quote_position < 0 or second_quote_position < 0:
                    raise errors.InvalidEmailError(
                        'value (%s) is not a valid email address' % value
                    )
            last_at_position = at_position
            last_quote_position = second_quote_position

    split_values = value.split('@')
    if len(split_values) < 2:
        raise errors.InvalidEmailError('value (%s) is not a valid email address' % value)

    local_value = ''.join(split_values[:-1])
    domain_value = split_values[-1]
    is_domain = False
    is_ip = False
    try:
        if domain_value.startswith('[') and domain_value.endswith(']'):
            domain_value = domain_value[1:-1]
        domain(domain_value)
        is_domain = True
    except ValueError:
        is_domain = False

    if not is_domain:
        try:
            ip_address(domain_value, force_run = True)                          # pylint: disable=E1123
            is_ip = True
        except ValueError:
            is_ip = False

    if not is_domain and is_ip:
        try:
            email(local_value + '@test.com', force_run = True)                  # pylint: disable=E1123
        except ValueError:
            raise errors.InvalidEmailError('value (%s) is not a valid email '
                                           'address' % value)

        return value

    if not is_domain:
        raise errors.InvalidEmailError('value (%s) is not a valid email address' % value)
    else:
        is_valid = EMAIL_REGEX.search(value)

        if not is_valid:
            raise errors.InvalidEmailError('value (%s) is not a valid email '
                                           'address' % value)

        matched_string = is_valid.group(0)
        position = value.find(matched_string)
        if position > 0:
            prefix = value[:position]
            if prefix[0] in string_.punctuation:
                raise errors.InvalidEmailError('value (%s) is not a valid email '
                                               'address' % value)
            if '..' in prefix:
                raise errors.InvalidEmailError('value (%s) is not a valid email '
                                               'address' % value)

        end_of_match = position + len(matched_string)
        suffix = value[end_of_match:]
        if suffix:
            raise errors.InvalidEmailError('value (%s) is not a valid email '
                                           'address' % value)

    return value


@disable_on_env
def url(value,
        allow_empty = False,
        allow_special_ips = False,
        **kwargs):
    """Validate that ``value`` is a valid URL.

    .. note::

      URL validation is...complicated. The methodology that we have
      adopted here is *generally* compliant with
      `RFC 1738 <https://tools.ietf.org/html/rfc1738>`_,
      `RFC 6761 <https://tools.ietf.org/html/rfc6761>`_,
      `RFC 2181 <https://tools.ietf.org/html/rfc2181>`_  and uses a combination of
      string parsing and regular expressions,

      This approach ensures more complete coverage for unusual edge cases, while
      still letting us use regular expressions that perform quickly.

    :param value: The value to validate.
    :type value: :class:`str <python:str>` / :obj:`None <python:None>`

    :param allow_empty: If ``True``, returns :obj:`None <python:None>` if
      ``value`` is empty. If ``False``, raises a
      :class:`EmptyValueError <validator_collection.errors.EmptyValueError>`
      if ``value`` is empty. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :param allow_special_ips: If ``True``, will succeed when validating special IP
      addresses, such as loopback IPs like ``127.0.0.1`` or ``0.0.0.0``. If ``False``,
      will raise a :class:`InvalidURLError` if ``value`` is a special IP address. Defaults
      to ``False``.
    :type allow_special_ips: :class:`bool <python:bool>`

    :returns: ``value`` / :obj:`None <python:None>`
    :rtype: :class:`str <python:str>` / :obj:`None <python:None>`

    :raises EmptyValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    :raises CannotCoerceError: if ``value`` is not a :class:`str <python:str>` or
      :obj:`None <python:None>`
    :raises InvalidURLError: if ``value`` is not a valid URL or
      empty with ``allow_empty`` set to ``True``

    """
    is_recursive = kwargs.pop('is_recursive', False)

    if not value and not allow_empty:
        raise errors.EmptyValueError('value (%s) was empty' % value)
    elif not value:
        return None

    if not isinstance(value, basestring):
        raise errors.CannotCoerceError('value must be a valid string, '
                                       'was %s' % type(value))

    value = value.lower()

    is_valid = False
    stripped_value = None
    for protocol in URL_PROTOCOLS:
        if protocol in value:
            stripped_value = value.replace(protocol, '')

    for special_use_domain in SPECIAL_USE_DOMAIN_NAMES:
        if special_use_domain in value:
            if stripped_value:
                try:
                    domain(stripped_value,
                           allow_empty = False,
                           is_recursive = is_recursive)
                    is_valid = True

                except (ValueError, TypeError):
                    pass

    if not is_valid and allow_special_ips:
        print('not valid and allowing special ips')
        try:
            ip_address(stripped_value, allow_empty = False)
            is_valid = True
        except (ValueError, TypeError):
            pass

    if not is_valid:
        is_valid = URL_REGEX.match(value)

    if not is_valid and allow_special_ips:
        is_valid = URL_SPECIAL_IP_REGEX.match(value)

    if not is_valid:
        raise errors.InvalidURLError('value (%s) is not a valid URL' % value)

    return value


@disable_on_env
def domain(value,
           allow_empty = False,
           allow_ips = False,
           **kwargs):
    """Validate that ``value`` is a valid domain name.

    .. caution::

      This validator does not verify that ``value`` **exists** as a domain. It
      merely verifies that its contents *might* exist as a domain.

    .. note::

      This validator checks to validate that ``value`` resembles a valid
      domain name. It is - generally - compliant with
      `RFC 1035 <https://tools.ietf.org/html/rfc1035>`_ and
      `RFC 6761 <https://tools.ietf.org/html/rfc6761>`_, however it diverges
      in a number of key ways:

        * Including authentication (e.g. ``username:password@domain.dev``) will
          fail validation.
        * Including a path (e.g. ``domain.dev/path/to/file``) will fail validation.
        * Including a port (e.g. ``domain.dev:8080``) will fail validation.

      If you are hoping to validate a more complete URL, we recommend that you
      see :func:`url <validator_collection.validators.url>`.

    .. hint::

      Leading and trailing whitespace will be automatically stripped.

    :param value: The value to validate.
    :type value: :class:`str <python:str>` / :obj:`None <python:None>`

    :param allow_empty: If ``True``, returns :obj:`None <python:None>` if
      ``value`` is empty. If ``False``, raises a
      :class:`EmptyValueError <validator_collection.errors.EmptyValueError>`
      if ``value`` is empty. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :param allow_ips: If ``True``, will succeed when validating IP addresses,
      If ``False``, will raise a :class:`InvalidDomainError` if ``value`` is an IP
      address. Defaults to ``False``.
    :type allow_ips: :class:`bool <python:bool>`

    :returns: ``value`` / :obj:`None <python:None>`
    :rtype: :class:`str <python:str>` / :obj:`None <python:None>`

    :raises EmptyValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    :raises CannotCoerceError: if ``value`` is not a :class:`str <python:str>` or
      :obj:`None <python:None>`
    :raises InvalidDomainError: if ``value`` is not a valid domain name or
      empty with ``allow_empty`` set to ``True``
    :raises SlashInDomainError: if ``value`` contains a slash or backslash
    :raises AtInDomainError: if ``value`` contains an ``@`` symbol
    :raises ColonInDomainError: if ``value`` contains a ``:`` symbol
    :raises WhitespaceInDomainError: if ``value`` contains whitespace

    """
    is_recursive = kwargs.pop('is_recursive', False)

    if not value and not allow_empty:
        raise errors.EmptyValueError('value (%s) was empty' % value)
    elif not value:
        return None

    if not isinstance(value, basestring):
        raise errors.CannotCoerceError('value must be a valid string, '
                                       'was %s' % type(value))

    if '/' in value:
        raise errors.SlashInDomainError('valid domain name cannot contain "/"')
    if '\\' in value:
        raise errors.SlashInDomainError('valid domain name cannot contain "\\"')
    if '@' in value:
        raise errors.AtInDomainError('valid domain name cannot contain "@"')
    if ':' in value:
        raise errors.ColonInDomainError('valid domain name cannot contain ":"')

    value = value.strip().lower()

    for item in string_.whitespace:
        if item in value:
            raise errors.WhitespaceInDomainError('valid domain name cannot contain '
                                                 'whitespace')

    if value in SPECIAL_USE_DOMAIN_NAMES:
        return value

    if allow_ips:
        try:
            ip_address(value, allow_empty = allow_empty)
            is_valid = True
        except (ValueError, TypeError, AttributeError):
            is_valid = False

        if is_valid:
            return value

    is_valid = DOMAIN_REGEX.match(value)

    if not is_valid and not is_recursive:
        with_prefix = 'http://' + value
        try:
            url(with_prefix, force_run = True, is_recursive = True)                                  # pylint: disable=E1123
        except ValueError:
            raise errors.InvalidDomainError('value (%s) is not a valid domain' % value)

    return value


@disable_on_env
def ip_address(value,
               allow_empty = False,
               **kwargs):
    """Validate that ``value`` is a valid IP address.

    .. note::

      First, the validator will check if the address is a valid IPv6 address.
      If that doesn't work, the validator will check if the address is a valid
      IPv4 address.

      If neither works, the validator will raise an error (as always).

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns :obj:`None <python:None>` if
      ``value`` is empty. If ``False``, raises a
      :class:`EmptyValueError <validator_collection.errors.EmptyValueError>`
      if ``value`` is empty. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :returns: ``value`` / :obj:`None <python:None>`

    :raises EmptyValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    :raises InvalidIPAddressError: if ``value`` is not a valid IP address or empty with
      ``allow_empty`` set to ``True``

    """
    if not value and not allow_empty:
        raise errors.EmptyValueError('value (%s) was empty' % value)
    elif not value:
        return None

    if is_py2 and value and isinstance(value, unicode):
        value = value.encode('utf-8')

    try:
        value = ipv6(value, force_run = True)                                   # pylint: disable=E1123
        ipv6_failed = False
    except ValueError:
        ipv6_failed = True

    if ipv6_failed:
        try:
            value = ipv4(value, force_run = True)                               # pylint: disable=E1123
        except ValueError:
            raise errors.InvalidIPAddressError('value (%s) is not a valid IPv6 or '
                                               'IPv4 address' % value)

    return value


@disable_on_env
def ipv4(value, allow_empty = False):
    """Validate that ``value`` is a valid IP version 4 address.

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns :obj:`None <python:None>` if
      ``value`` is empty. If ``False``, raises a
      :class:`EmptyValueError <validator_collection.errors.EmptyValueError>`
      if ``value`` is empty. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :returns: ``value`` / :obj:`None <python:None>`

    :raises EmptyValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    :raises InvalidIPAddressError: if ``value`` is not a valid IP version 4 address or
      empty with ``allow_empty`` set to ``True``
    """
    if not value and allow_empty is False:
        raise errors.EmptyValueError('value (%s) was empty' % value)
    elif not value:
        return None

    try:
        components = value.split('.')
    except AttributeError:
        raise errors.InvalidIPAddressError('value (%s) is not a valid ipv4' % value)

    if len(components) != 4 or not all(x.isdigit() for x in components):
        raise errors.InvalidIPAddressError('value (%s) is not a valid ipv4' % value)

    for x in components:
        try:
            x = integer(x,
                        minimum = 0,
                        maximum = 255)
        except ValueError:
            raise errors.InvalidIPAddressError('value (%s) is not a valid ipv4' % value)

    return value


@disable_on_env
def ipv6(value,
         allow_empty = False,
         **kwargs):
    """Validate that ``value`` is a valid IP address version 6.

    :param value: The value to validate.

    :param allow_empty: If ``True``, returns :obj:`None <python:None>` if
      ``value`` is empty. If ``False``, raises a
      :class:`EmptyValueError <validator_collection.errors.EmptyValueError>`
      if ``value`` is empty. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :returns: ``value`` / :obj:`None <python:None>`

    :raises EmptyValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    :raises InvalidIPAddressError: if ``value`` is not a valid IP version 6 address or
      empty with ``allow_empty`` is not set to ``True``

    """
    if not value and allow_empty is False:
        raise errors.EmptyValueError('value (%s) was empty' % value)
    elif not value:
        return None

    if not isinstance(value, str):
        raise errors.InvalidIPAddressError('value (%s) is not a valid ipv6' % value)

    value = value.lower().strip()

    is_valid = IPV6_REGEX.match(value)

    if not is_valid:
        raise errors.InvalidIPAddressError('value (%s) is not a valid ipv6' % value)

    return value


@disable_on_env
def mac_address(value,
                allow_empty = False,
                **kwargs):
    """Validate that ``value`` is a valid MAC address.

    :param value: The value to validate.
    :type value: :class:`str <python:str>` / :obj:`None <python:None>`

    :param allow_empty: If ``True``, returns :obj:`None <python:None>` if
      ``value`` is empty. If ``False``, raises a
      :class:`EmptyValueError <validator_collection.errors.EmptyValueError>`
      if ``value`` is empty. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :returns: ``value`` / :obj:`None <python:None>`
    :rtype: :class:`str <python:str>` / :obj:`None <python:None>`

    :raises EmptyValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    :raises CannotCoerceError: if ``value`` is not a valid :class:`str <python:str>`
      or string-like object
    :raises InvalidMACAddressError: if ``value`` is not a valid MAC address or empty with
      ``allow_empty`` set to ``True``

    """
    if not value and not allow_empty:
        raise errors.EmptyValueError('value (%s) was empty' % value)
    elif not value:
        return None

    if not isinstance(value, basestring):
        raise errors.CannotCoerceError('value must be a valid string, '
                                       'was %s' % type(value))

    if '-' in value:
        value = value.replace('-', ':')

    value = value.lower().strip()

    is_valid = MAC_ADDRESS_REGEX.match(value)

    if not is_valid:
        raise errors.InvalidMACAddressError('value (%s) is not a valid MAC '
                                            'address' % value)

    return value
