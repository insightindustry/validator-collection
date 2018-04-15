# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

# pylint: disable=W0703

import io

import validator_collection.validators as validators
from validator_collection._compat import integer_types, basestring


## CORE

def is_type(obj, type_):
    """Indicate if ``obj`` is a type in ``type_``.

    .. hint::

      This checker is particularly useful when you want to evaluate whether
      ``obj`` is of a particular type, but importing that type directly to use
      in :func:`isinstance() <python:isinstance>` would cause a circular import
      error.

      To use this checker in that kind of situation, you can instead pass the
      *name* of the type you want to check as a string in ``type_``. The checker
      will evaluate it and see whether ``obj`` is of a type or inherits from a
      type whose name matches the string you passed.

    :param obj: The object whose type should be checked.
    :type obj: :class:`object <python:object>`

    :param type_: The type(s) to check against.
    :type type_: :class:`type <python:type>` / iterable of :class:`type <python:type>` /
      :class:`str <python:str>` with type name / iterable of :class:`str <python:str>`
      with type name

    :returns: ``True`` if ``obj`` is a type in ``type_``. Otherwise, ``False``.
    :rtype: :class:`bool <python:bool>`

    """
    if not is_iterable(type_):
        type_ = [type_]

    return_value = False
    for check_for_type in type_:
        if isinstance(check_for_type, type):
            return_value = isinstance(obj, check_for_type)
        elif obj.__class__.__name__ == check_for_type:
            return_value = True
        else:
            return_value = _check_base_classes(obj.__class__.__bases__,
                                               check_for_type)

        if return_value is True:
            break

    return return_value


def _check_base_classes(base_classes, check_for_type):
    """Indicate whether ``check_for_type`` exists in ``base_classes``.
    """
    return_value = False
    for base in base_classes:
        if base.__name__ == check_for_type:
            return_value = True
            break
        else:
            return_value = _check_base_classes(base.__bases__, check_for_type)
            if return_value is True:
                break

    return return_value


def are_equivalent(*args):
    """Indicate if arguments passed to this function are equivalent.

    .. hint::

      This checker operates recursively on the members contained within iterables
      and :class:`dict <python:dict>` objects.

    .. caution::

      If you only pass one argument to this checker - even if it is an iterable -
      the checker will *always* return ``True``.

      To evaluate members of an iterable for equivalence, you should instead
      unpack the iterable into the function like so:

      .. code-block:: python

        obj = [1, 1, 1, 2]

        result = are_equivalent(*obj)
        # Will return ``False`` by unpacking and evaluating the iterable's members

        result = are_equivalent(obj)
        # Will always return True

    :param args: One or more values, passed as positional arguments.

    :returns: ``True`` if ``args`` are equivalent, and ``False`` if not.
    :rtype: :class:`bool <python:bool>`
    """
    if len(args) == 1:
        return True

    first_item = args[0]
    for item in args[1:]:
        if type(item) != type(first_item):                                      # pylint: disable=C0123
            return False

        if isinstance(item, dict):
            if not are_dicts_equivalent(item, first_item):
                return False
        elif hasattr(item, '__iter__') and not isinstance(item, (str, bytes, dict)):
            if len(item) != len(first_item):
                return False
            for value in item:
                if value not in first_item:
                    return False
            for value in first_item:
                if value not in item:
                    return False
        else:
            if item != first_item:
                return False

    return True


def are_dicts_equivalent(*args):
    """Indicate if :ref:`dicts <python:dict>` passed to this function have identical
    keys and values.

    :param args: One or more values, passed as positional arguments.

    :returns: ``True`` if ``args`` have identical keys/values, and ``False`` if not.
    :rtype: :class:`bool <python:bool>`
    """
    # pylint: disable=too-many-return-statements
    if not args:
        return False

    if len(args) == 1:
        return True

    if not all(is_dict(x) for x in args):
        return False

    first_item = args[0]
    for item in args[1:]:
        if len(item) != len(first_item):
            return False

        for key in item:
            if key not in first_item:
                print('key not in first item')
                return False

            if not are_equivalent(item[key], first_item[key]):
                print(item[key])
                print(first_item[key])
                return False

        for key in first_item:
            if key not in item:
                return False

            if not are_equivalent(first_item[key], item[key]):
                return False

    return True


def is_between(value,
               minimum = None,
               maximum = None):
    """Indicate whether ``value`` is greater than or equal to a supplied ``minimum``
    and/or less than or equal to ``maximum``.

    .. note::

      This function works on any ``value`` that support comparison operators,
      whether they are numbers or not. Technically, this means that ``value``,
      ``minimum``, or ``maximum`` need to implement the Python magic methods
      :func:`__lte__ <python:object.__lte__>` and :func:`__gte__ <python:object.__gte__>`.

      If ``value``, ``minimum``, or ``maximum`` do not support comparison
      operators, they will raise :class:`NotImplemented <python:NotImplemented>`.

    :param value: The ``value`` to check.
    :type value: anything that supports comparison operators

    :param minimum: If supplied, will return ``True`` if ``value`` is greater than or
      equal to this value.
    :type minimum: anything that supports comparison operators /
      :class:`None <python:None>`

    :param maximum: If supplied, will return ``True`` if ``value`` is less than or
      equal to this value.
    :type maximum: anything that supports comparison operators /
      :class:`None <python:None>`

    :returns: ``True`` if ``value`` is greater than or equal to a supplied ``minimum``
      and less than or equal to a supplied ``maximum``. Otherwise, returns ``False``.
    :rtype: :class:`bool <python:bool>`

    :raises NotImplemented: if ``value``, ``minimum``, or ``maximum`` do not
      support comparison operators
    :raises ValueError: if both ``minimum`` and ``maximum`` are
      :class:`None <python:None>`
    """
    if minimum is None and maximum is None:
        raise ValueError('minimum and maximum cannot both be None')

    if value is None:
        return False

    if minimum is not None and maximum is None:
        return value >= minimum
    elif minimum is None and maximum is not None:
        return value <= maximum
    elif minimum is not None and maximum is not None:
        return value >= minimum and value <= maximum


def has_length(value,
               minimum = None,
               maximum = None):
    """Indicate whether ``value`` has a length greater than or equal to a
    supplied ``minimum`` and/or less than or equal to ``maximum``.

    .. note::

      This function works on any ``value`` that supports the
      :func:`len() <python:len>` operation. This means that ``value`` must implement
      the :func:`__len__ <python:__len__>` magic method.

      If ``value`` does not support length evaluation, the checker will raise
      :class:`NotImplemented <python:NotImplemented>`.

    :param value: The ``value`` to check.
    :type value: anything that supports length evaluation

    :param minimum: If supplied, will return ``True`` if ``value`` is greater than or
      equal to this value.
    :type minimum: numeric

    :param maximum: If supplied, will return ``True`` if ``value`` is less than or
      equal to this value.
    :type maximum: numeric

    :returns: ``True`` if ``value`` has length greater than or equal to a
      supplied ``minimum`` and less than or equal to a supplied ``maximum``.
      Otherwise, returns ``False``.
    :rtype: :class:`bool <python:bool>`

    :raises TypeError: if ``value`` does not support length evaluation
    :raises ValueError: if both ``minimum`` and ``maximum`` are
      :class:`None <python:None>`
    """
    if minimum is None and maximum is None:
        raise ValueError('minimum and maximum cannot both be None')

    length = len(value)
    minimum = validators.numeric(minimum,
                                 allow_empty = True)
    maximum = validators.numeric(maximum,
                                 allow_empty = True)

    return is_between(length,
                      minimum = minimum,
                      maximum = maximum)


def is_dict(value):
    """Indicate whether ``value`` is a valid :class:`dict <python:dict>`

    .. note::

      This will return ``True`` even if ``value`` is an empty
      :class:`dict <python:dict>`.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`
    """
    if isinstance(value, dict):
        return True

    try:
        value = validators.dict(value)
    except Exception:
        return False

    return True


def is_string(value,
              coerce_value = False,
              minimum_length = None,
              maximum_length = None,
              whitespace_padding = False):
    """Indicate whether ``value`` is a string.

    :param value: The value to evaluate.

    :param coerce_value: If ``True``, will check whether ``value`` can be coerced
      to a string if it is not already. Defaults to ``False``.
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

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`
    """
    if value is None:
        return False

    minimum_length = validators.integer(minimum_length, allow_empty = True)
    maximum_length = validators.integer(maximum_length, allow_empty = True)

    if isinstance(value, basestring) and not value:
        if minimum_length and minimum_length > 0 and not whitespace_padding:
            return False

        return True

    try:
        value = validators.string(value,
                                  coerce_value = coerce_value,
                                  minimum_length = minimum_length,
                                  maximum_length = maximum_length,
                                  whitespace_padding = whitespace_padding)
    except Exception:
        return False

    return True


def is_iterable(obj,
                forbid_literals = (str, bytes),
                minimum_length = None,
                maximum_length = None):
    """Indicate whether ``obj`` is iterable.

    :param forbid_literals: A collection of literals that will be considered invalid
      even if they are (actually) iterable. Defaults to a :class:`tuple <python:tuple>`
      containing :class:`str <python:str>` and :class:`bytes <python:bytes>`.
    :type forbid_literals: iterable

    :param minimum_length: If supplied, indicates the minimum number of members
      needed to be valid.
    :type minimum_length: :class:`int <python:int>`

    :param maximum_length: If supplied, indicates the minimum number of members
      needed to be valid.
    :type maximum_length: :class:`int <python:int>`

    :returns: ``True`` if ``obj`` is a valid iterable, ``False`` if not.
    :rtype: :class:`bool <python:bool>`
    """
    if obj is None:
        return False

    if obj in forbid_literals:
        return False

    try:
        obj = validators.iterable(obj,
                                  allow_empty = True,
                                  forbid_literals = forbid_literals,
                                  minimum_length = minimum_length,
                                  maximum_length = maximum_length)
    except Exception:
        return False

    return True


def is_not_empty(value):
    """Indicate whether ``value`` is empty.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is empty, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`
    """
    try:
        value = validators.not_empty(value)
    except Exception:
        return False

    return True


def is_none(value, allow_empty = False):
    """Indicate whether ``value`` is :class:`None <python:None>`.

    :param value: The value to evaluate.

    :param allow_empty: If ``True``, accepts falsey values as equivalent to
      :class:`None <python:None>`. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :returns: ``True`` if ``value`` is :class:`None <python:None>`, ``False``
      if it is not.
    :rtype: :class:`bool <python:bool>`
    """
    try:
        validators.none(value, allow_empty = allow_empty)
    except Exception:
        return False

    return True


def is_variable_name(value):
    """Indicate whether ``value`` is a valid Python variable name.

    .. caution::

      This function does **NOT** check whether the variable exists. It only
      checks that the ``value`` would work as a Python variable (or class, or
      function, etc.) name.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`
    """
    try:
        validators.variable_name(value)
    except Exception:
        return False

    return True


def is_uuid(value):
    """Indicate whether ``value`` contains a :class:`UUID <python:uuid.UUID>`

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`

    """
    try:
        validators.uuid(value)
    except Exception:
        return False

    return True


## DATE / TIME

def is_date(value,
            minimum = None,
            maximum = None):
    """Indicate whether ``value`` is a :class:`date <python:datetime.date>`.

    :param value: The value to evaluate.

    :param minimum: If supplied, will make sure that ``value`` is on or after
      this value.
    :type minimum: :class:`datetime <python:datetime.datetime>` /
      :class:`date <python:datetime.date>` / compliant :class:`str <python:str>`
      / :class:`None <python:None>`

    :param maximum: If supplied, will make sure that ``value`` is on or before this
      value.
    :type maximum: :class:`datetime <python:datetime.datetime>` /
      :class:`date <python:datetime.date>` / compliant :class:`str <python:str>`
      / :class:`None <python:None>`

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`
    """
    try:
        value = validators.date(value,
                                minimum = minimum,
                                maximum = maximum)
    except Exception:
        return False

    return True


def is_datetime(value,
                minimum = None,
                maximum = None):
    """Indicate whether ``value`` is a :class:`datetime <python:datetime.datetime>`.

    :param value: The value to evaluate.

    :param minimum: If supplied, will make sure that ``value`` is on or after
      this value.
    :type minimum: :class:`datetime <python:datetime.datetime>` /
      :class:`date <python:datetime.date>` / compliant :class:`str <python:str>`
      / :class:`None <python:None>`

    :param maximum: If supplied, will make sure that ``value`` is on or before this
      value.
    :type maximum: :class:`datetime <python:datetime.datetime>` /
      :class:`date <python:datetime.date>` / compliant :class:`str <python:str>`
      / :class:`None <python:None>`

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`
    """
    try:
        value = validators.datetime(value,
                                    minimum = minimum,
                                    maximum = maximum)
    except Exception:
        return False

    return True


def is_time(value,
            minimum = None,
            maximum = None):
    """Indicate whether ``value`` is a :class:`time <python:datetime.time>`.

    :param value: The value to evaluate.

    :param minimum: If supplied, will make sure that ``value`` is on or after this value.
    :type minimum: :func:`datetime <validator_collection.validators.datetime>` or
      :func:`time <validator_collection.validators.time>`-compliant
      :class:`str <python:str>` / :class:`datetime <python:datetime.datetime>` /
      :class:`time <python:datetime.time> / numeric / :class:`None <python:None>`

    :param maximum: If supplied, will make sure that ``value`` is on or before this
      value.
    :type maximum: :func:`datetime <validator_collection.validators.datetime>` or
      :func:`time <validator_collection.validators.time>`-compliant
      :class:`str <python:str>` / :class:`datetime <python:datetime.datetime>` /
      :class:`time <python:datetime.time> / numeric / :class:`None <python:None>`

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`
    """
    try:
        value = validators.time(value,
                                minimum = minimum,
                                maximum = maximum)
    except Exception:
        return False

    return True


def is_timezone(value,
                positive = True):
    """Indicate whether ``value`` is a :class:`tzinfo <python:datetime.tzinfo>`.

    .. caution::

      This does **not** validate whether the value is a timezone that actually
      exists, nor can it resolve timzone names (e.g. ``'Eastern'`` or ``'CET'``).

      For that kind of functionality, we recommend you utilize:
      `pytz <https://pypi.python.org/pypi/pytz>`_

    :param value: The value to evaluate.

    :param positive: Indicates whether the ``value`` is positive or negative
      (only has meaning if ``value`` is a string). Defaults to ``True``.
    :type positive: :class:`bool <python:bool>`

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`
    """
    try:
        value = validators.timezone(value,
                                    positive = positive)
    except Exception:
        return False

    return True


## NUMBERS

def is_numeric(value,
               minimum = None,
               maximum = None):
    """Indicate whether ``value`` is a numeric value.

    :param value: The value to evaluate.

    :param minimum: If supplied, will make sure that ``value`` is greater than or
      equal to this value.
    :type minimum: numeric

    :param maximum: If supplied, will make sure that ``value`` is less than or
      equal to this value.
    :type maximum: numeric

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`
    """
    try:
        value = validators.numeric(value,
                                   minimum = minimum,
                                   maximum = maximum)
    except Exception:
        return False

    return True


def is_integer(value,
               coerce_value = False,
               minimum = None,
               maximum = None,
               base = 10):
    """Indicate whether ``value`` contains a whole number.

    :param value: The value to evaluate.

    :param coerce_value: If ``True``, will return ``True`` if ``value`` can be coerced
      to whole number. If ``False``, will only return ``True`` if ``value`` is already
      a whole number (regardless of type). Defaults to ``False``.
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
    :type base: :class:`int <python:int>`

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`
    """
    try:
        value = validators.integer(value,
                                   coerce_value = coerce_value,
                                   minimum = minimum,
                                   maximum = maximum,
                                   base = base)
    except Exception:
        return False

    return True


def is_float(value,
             minimum = None,
             maximum = None):
    """Indicate whether ``value`` is a :class:`float <python:float>`.

    :param value: The value to evaluate.

    :param minimum: If supplied, will make sure that ``value`` is greater than or
      equal to this value.
    :type minimum: numeric

    :param maximum: If supplied, will make sure that ``value`` is less than or
      equal to this value.
    :type maximum: numeric

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`
    """
    try:
        value = validators.float(value,
                                 minimum = minimum,
                                 maximum = maximum)
    except Exception:
        return False

    return True


def is_fraction(value,
                minimum = None,
                maximum = None):
    """Indicate whether ``value`` is a :class:`Fraction <python:fractions.Fraction>`.

    :param value: The value to evaluate.

    :param minimum: If supplied, will make sure that ``value`` is greater than or
      equal to this value.
    :type minimum: numeric

    :param maximum: If supplied, will make sure that ``value`` is less than or
      equal to this value.
    :type maximum: numeric

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`
    """
    try:
        value = validators.fraction(value,
                                    minimum = minimum,
                                    maximum = maximum)
    except Exception:
        return False

    return True


def is_decimal(value,
               minimum = None,
               maximum = None):
    """Indicate whether ``value`` contains a :class:`Decimal <python:decimal.Decimal>`.

    :param value: The value to evaluate.

    :param minimum: If supplied, will make sure that ``value`` is greater than or
      equal to this value.
    :type minimum: numeric

    :param maximum: If supplied, will make sure that ``value`` is less than or
      equal to this value.
    :type maximum: numeric

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`
    """
    try:
        value = validators.decimal(value,
                                   minimum = minimum,
                                   maximum = maximum)
    except Exception:
        return False

    return True


## FILE-RELATED

def is_bytesIO(value):
    """Indicate whether ``value`` is a :class:`BytesIO <python:io.BytesIO>` object.

    .. note::

      This checker will return ``True`` even if ``value`` is empty, so long as
      its type is a :class:`BytesIO <python:io.BytesIO>`.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`
    """
    return isinstance(value, io.BytesIO)


def is_stringIO(value):
    """Indicate whether ``value`` is a :class:`StringIO <python:io.StringIO>` object.

    .. note::

      This checker will return ``True`` even if ``value`` is empty, so long as
      its type is a :class:`String <python:io.StringIO>`.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`
    """
    return isinstance(value, io.StringIO)


def is_pathlike(value):
    """Indicate whether ``value`` is a path-like object.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`
    """
    try:
        value = validators.path(value)
    except Exception:
        return False

    return True


def is_on_filesystem(value):
    """Indicate whether ``value`` is a file or directory that exists on the local
    filesystem.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`
    """
    try:
        value = validators.path_exists(value)
    except Exception:
        return False

    return True


def is_file(value):
    """Indicate whether ``value`` is a file that exists on the local filesystem.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`
    """
    try:
        value = validators.file_exists(value)
    except Exception:
        return False

    return True


def is_directory(value):
    """Indicate whether ``value`` is a directory that exists on the local filesystem.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`
    """
    try:
        value = validators.directory_exists(value)
    except Exception:
        return False

    return True


## INTERNET-RELATED

def is_email(value):
    """Indicate whether ``value`` is an email address.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`
    """
    try:
        value = validators.email(value)
    except Exception:
        return False

    return True


def is_url(value):
    """Indicate whether ``value`` is a URL.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`
    """
    try:
        value = validators.url(value)
    except Exception:
        return False

    return True


def is_ip_address(value):
    """Indicate whether ``value`` is a valid IP address (version 4 or version 6).

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`
    """
    try:
        value = validators.ip_address(value)
    except Exception:
        return False

    return True


def is_ipv4(value):
    """Indicate whether ``value`` is a valid IP version 4 address.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`
    """
    try:
        value = validators.ipv4(value)
    except Exception:
        return False

    return True


def is_ipv6(value):
    """Indicate whether ``value`` is a valid IP version 6 address.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`
    """
    try:
        value = validators.ipv6(value)
    except Exception:
        return False

    return True


def is_mac_address(value):
    """Indicate whether ``value`` is a valid MAC address.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`
    """
    try:
        value = validators.mac_address(value)
    except Exception:
        return False

    return True
