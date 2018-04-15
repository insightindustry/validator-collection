# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

# pylint: disable=W0703

import validator_collection.validators as validators
from validator_collection._compat import integer_types


def is_uuid(value):
    """Indicate whether ``value`` is a :ref:`UUID <python:uuid.UUID>`

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :ref:`bool <python:bool>`
    """
    try:
        value = validators.uuid(value)
    except Exception:
        return False

    return True


def is_email(value):
    """Indicate whether ``value`` is an email address.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :ref:`bool <python:bool>`
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
    :rtype: :ref:`bool <python:bool>`
    """
    try:
        value = validators.email(value)
    except Exception:
        return False

    return True


def is_string(value,
              minimum_length = None,
              maximum_length = None,
              whitespace_padding = False):
    """Indicate whether ``value`` is a URL.

    :param value: The value to evaluate.

    :param minimum_length: If supplied, indicates the minimum number of characters
      needed to be valid.
    :type minimum_length: :ref:`int <python:int>`

    :param maximum_length: If supplied, indicates the minimum number of characters
      needed to be valid.
    :type maximum_length: :ref:`int <python:int>`

    :param whitespace_padding: If ``True`` and the value is below the
      ``minimum_length``, pad the value with spaces. Defaults to ``False``.
    :type whitespace_padding: :ref:`bool <python:bool>`

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :ref:`bool <python:bool>`
    """
    if value is None:
        return False

    minimum_length = validators.integer(minimum_length, allow_empty = True)
    maximum_length = validators.integer(maximum_length, allow_empty = True)

    if isinstance(value, str) and not value:
        if minimum_length and minimum_length > 0 and not whitespace_padding:
            return False

        return True

    try:
        value = validators.string(value,
                                  minimum_length = minimum_length,
                                  maximum_length = maximum_length,
                                  whitespace_padding = whitespace_padding)
    except Exception:
        return False

    return True


def is_iterable(obj,
                minimum_length = None,
                maximum_length = None):
    """Indicate whether ``obj`` is iterable.

    :param minimum_length: If supplied, indicates the minimum number of members
      needed to be valid.
    :type minimum_length: :ref:`int <python:int>`

    :param maximum_length: If supplied, indicates the minimum number of members
      needed to be valid.
    :type maximum_length: :ref:`int <python:int>`

    :returns: ``True`` if ``obj`` is a valid iterable, ``False`` if not.
    :rtype: :ref:`bool <python:bool>`
    """
    if obj is None:
        return False

    if obj == str or obj == bytes:
        return False

    try:
        obj = validators.iterable(obj,
                                  allow_empty = True,
                                  minimum_length = minimum_length,
                                  maximum_length = maximum_length)
    except Exception:
        return False

    return True


def is_datetime(value,
                minimum = None,
                maximum = None):
    """Indicate whether ``value`` is a :ref:`datetime <python:datetime.datetime>`.

    :param value: The value to evaluate.

    :param minimum: If supplied, will make sure that ``value`` is on or after this value.
    :type minimum: :ref:`datetime <python:datetime.datetime>` /
      :ref:`date <python:datetime.date>` / compliant :ref:`str <python:str>` / ``None``

    :param maximum: If supplied, will make sure that ``value`` is on or before this
      value.
    :type maximum: :ref:`datetime <python:datetime.datetime>` /
      :ref:`date <python:datetime.date>` / compliant :ref:`str <python:str>` / ``None``

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :ref:`bool <python:bool>`
    """
    try:
        value = validators.datetime(value,
                                    minimum = minimum,
                                    maximum = maximum)
    except Exception:
        return False

    return True


def is_date(value,
            minimum = None,
            maximum = None):
    """Indicate whether ``value`` is a :ref:`date <python:datetime.date>`.

    :param value: The value to evaluate.

    :param minimum: If supplied, will make sure that ``value`` is on or after this value.
    :type minimum: :ref:`datetime <python:datetime.datetime>` /
      :ref:`date <python:datetime.date>` / compliant :ref:`str <python:str>` / ``None``

    :param maximum: If supplied, will make sure that ``value`` is on or before this
      value.
    :type maximum: :ref:`datetime <python:datetime.datetime>` /
      :ref:`date <python:datetime.date>` / compliant :ref:`str <python:str>` / ``None``

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :ref:`bool <python:bool>`
    """
    try:
        value = validators.date(value,
                                minimum = minimum,
                                maximum = maximum)
    except Exception:
        return False

    return True


def is_time(value,
            minimum = None,
            maximum = None):
    """Indicate whether ``value`` is a :ref:`time <python:datetime.time>`.

    :param value: The value to evaluate.

    :param minimum: If supplied, will make sure that ``value`` is on or after this value.
    :type minimum: :ref:`datetime <python:datetime.datetime>` /
      :ref:`date <python:datetime.date>` / compliant :ref:`str <python:str>` / ``None``

    :param maximum: If supplied, will make sure that ``value`` is on or before this
      value.
    :type maximum: :ref:`datetime <python:datetime.datetime>` /
      :ref:`date <python:datetime.date>` / compliant :ref:`str <python:str>` / ``None``

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :ref:`bool <python:bool>`
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
    """Indicate whether ``value`` is a :ref:`tzinfo <python:datetime.tzinfo>`.

    :param value: The value to evaluate.

    :param positive: Indicates whether the ``value`` is positive or negative
      (only has meaning if ``value`` is a string). Defaults to ``True``.
    :type positive: :ref:`bool <python:bool>`

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :ref:`bool <python:bool>`
    """
    try:
        value = validators.timezone(value,
                                    positive = positive)
    except Exception:
        return False

    return True


def is_not_empty(value):
    """Indicate whether ``value`` is empty.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :ref:`bool <python:bool>`
    """
    try:
        value = validators.not_empty(value)
    except Exception:
        return False

    return True


def is_none(value):
    """Indicate whether ``value`` is ``None``.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is ``None``, ``False`` if it is not.
    :rtype: :ref:`bool <python:bool>`
    """
    try:
        value = validators.none(value)
    except Exception:
        return False

    return True


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
    :rtype: :ref:`bool <python:bool>`
    """
    try:
        value = validators.numeric(value,
                                   minimum = minimum,
                                   maximum = maximum)
    except Exception:
        return False

    return True


def is_decimal(value,
               minimum = None,
               maximum = None):
    """Indicate whether ``value`` is a :ref:`Decimal <python:decimal.Decimal>`.

    :param value: The value to evaluate.

    :param minimum: If supplied, will make sure that ``value`` is greater than or
      equal to this value.
    :type minimum: numeric

    :param maximum: If supplied, will make sure that ``value`` is less than or
      equal to this value.
    :type maximum: numeric

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :ref:`bool <python:bool>`
    """
    try:
        value = validators.decimal(value,
                                   minimum = minimum,
                                   maximum = maximum)
    except Exception:
        return False

    return True


def is_integer(value,
               minimum = None,
               maximum = None):
    """Indicate whether ``value`` is an :ref:`int <python:int>`.

    :param value: The value to evaluate.

    :param minimum: If supplied, will make sure that ``value`` is greater than or
      equal to this value.
    :type minimum: numeric

    :param maximum: If supplied, will make sure that ``value`` is less than or
      equal to this value.
    :type maximum: numeric

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :ref:`bool <python:bool>`
    """
    minimum = validators.numeric(minimum, allow_empty = True)
    maximum = validators.numeric(maximum, allow_empty = True)

    if value is None or not isinstance(value, integer_types):
        return False

    if value and minimum and value < minimum:
        return False
    elif value and maximum and value > maximum:
        return False

    return True


def is_float(value,
             minimum = None,
             maximum = None):
    """Indicate whether ``value`` is a :ref:`float <python:float>`.

    :param value: The value to evaluate.

    :param minimum: If supplied, will make sure that ``value`` is greater than or
      equal to this value.
    :type minimum: numeric

    :param maximum: If supplied, will make sure that ``value`` is less than or
      equal to this value.
    :type maximum: numeric

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :ref:`bool <python:bool>`
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
    """Indicate whether ``value`` is a :ref:`Fraction <python:fractions.Fraction>`.

    :param value: The value to evaluate.

    :param minimum: If supplied, will make sure that ``value`` is greater than or
      equal to this value.
    :type minimum: numeric

    :param maximum: If supplied, will make sure that ``value`` is less than or
      equal to this value.
    :type maximum: numeric

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :ref:`bool <python:bool>`
    """
    try:
        value = validators.fraction(value,
                                    minimum = minimum,
                                    maximum = maximum)
    except Exception:
        return False

    return True


def is_variable_name(value):
    """Indicate whether ``value`` is a valid Python variable name.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :ref:`bool <python:bool>`
    """
    try:
        value = validators.variable_name(value)
    except Exception:
        return False

    return True


def is_ipv4(value):
    """Indicate whether ``value`` is a valid IP version 4 address.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :ref:`bool <python:bool>`
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
    :rtype: :ref:`bool <python:bool>`
    """
    try:
        value = validators.ipv6(value)
    except Exception:
        return False

    return True


def is_ip(value):
    """Indicate whether ``value`` is a valid IP address.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :ref:`bool <python:bool>`
    """
    return is_ipv4(value) or is_ipv6(value)


def is_mac_address(value):
    """Indicate whether ``value`` is a valid MAC address.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :ref:`bool <python:bool>`
    """
    try:
        value = validators.mac_address(value)
    except Exception:
        return False

    return True


def is_dict(value):
    """Indicate whether ``value`` is a valid :ref:`dict <python:dict>`

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :ref:`bool <python:bool>`
    """
    if isinstance(value, dict):
        return True

    try:
        value = validators.dict(value)
    except Exception:
        return False

    return True


def is_stringIO(value):
    """Indicate whether ``value`` is a :ref:`StringIO <python:io.StringIO>` object.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :ref:`bool <python:bool>`
    """
    try:
        value = validators.stringIO(value)
    except Exception:
        return False

    return True


def is_bytesIO(value):
    """Indicate whether ``value`` is a :ref:`BytesIO <python:io.BytesIO>` object.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :ref:`bool <python:bool>`
    """
    try:
        value = validators.bytesIO(value)
    except Exception:
        return False

    return True


def is_pathlike(value):
    """Indicate whether ``value`` is a path-like object.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :ref:`bool <python:bool>`
    """
    try:
        value = validators.path(value)
    except Exception:
        return False

    return True


def is_on_filesystem(value):
    """Indicate whether ``value`` is a file or directory on the local filesystem.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :ref:`bool <python:bool>`
    """
    try:
        value = validators.path_exists(value)
    except Exception:
        return False

    return True


def is_file(value):
    """Indicate whether ``value`` is a file on the local filesystem.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :ref:`bool <python:bool>`
    """
    try:
        value = validators.file_exists(value)
    except Exception:
        return False

    return True


def is_directory(value):
    """Indicate whether ``value`` is a directory on the local filesystem.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :ref:`bool <python:bool>`
    """
    try:
        value = validators.directory_exists(value)
    except Exception:
        return False

    return True


def is_type(obj, type_):
    """Indicate if ``obj`` is a type in ``type_``.

    :param obj: The object whose type should be checked.
    :type obj: :ref:`object <python:object>`

    :param type_: The type(s) to check against.
    :type type_: :ref:`type <python:type>` / iterable of :ref:`type <python:type>` /
      :ref:`str <python:str>` with type name / iterable of :ref:`str <python:str>` of
      type name

    :returns: ``True`` if ``obj`` is a type in ``type_``. Otherwise, ``False``.
    :rtype: :ref:`bool <python:bool>`
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


def are_dicts_equivalent(*args):
    """Indicate if :ref:`dicts <python:dict> passed to this function have identical
    keys and values.

    :returns: ``True`` if ``args`` have identical keys/values, and ``False`` if not.
    :rtype: :ref:`bool <python:bool>`
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


def are_equivalent(*args):
    """Indicate if arguments passed to this function are equivalent.

    :returns: ``True`` if ``args`` are equivalent, and ``False`` if not.
    :rtype: :ref:`bool <python:bool>`
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
