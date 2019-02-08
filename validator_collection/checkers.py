# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

# pylint: disable=W0703

import io
import sys

import validator_collection.validators as validators
from validator_collection._compat import integer_types, basestring
from validator_collection._decorators import disable_checker_on_env

# pylint: disable=W0613
## CORE

@disable_checker_on_env
def is_type(obj,
            type_,
            **kwargs):
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

    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator

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


@disable_checker_on_env
def are_equivalent(*args, **kwargs):
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

    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator

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


@disable_checker_on_env
def are_dicts_equivalent(*args, **kwargs):
    """Indicate if :ref:`dicts <python:dict>` passed to this function have identical
    keys and values.

    :param args: One or more values, passed as positional arguments.

    :returns: ``True`` if ``args`` have identical keys/values, and ``False`` if not.
    :rtype: :class:`bool <python:bool>`

    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator

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
                return False

            if not are_equivalent(item[key], first_item[key]):
                return False

        for key in first_item:
            if key not in item:
                return False

            if not are_equivalent(first_item[key], item[key]):
                return False

    return True


@disable_checker_on_env
def is_between(value,
               minimum = None,
               maximum = None,
               **kwargs):
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
      :obj:`None <python:None>`

    :param maximum: If supplied, will return ``True`` if ``value`` is less than or
      equal to this value.
    :type maximum: anything that supports comparison operators /
      :obj:`None <python:None>`

    :returns: ``True`` if ``value`` is greater than or equal to a supplied ``minimum``
      and less than or equal to a supplied ``maximum``. Otherwise, returns ``False``.
    :rtype: :class:`bool <python:bool>`


    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator
    :raises NotImplemented: if ``value``, ``minimum``, or ``maximum`` do not
      support comparison operators
    :raises ValueError: if both ``minimum`` and ``maximum`` are
      :obj:`None <python:None>`
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


@disable_checker_on_env
def has_length(value,
               minimum = None,
               maximum = None,
               **kwargs):
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


    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator
    :raises TypeError: if ``value`` does not support length evaluation
    :raises ValueError: if both ``minimum`` and ``maximum`` are
      :obj:`None <python:None>`
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


@disable_checker_on_env
def is_dict(value, **kwargs):
    """Indicate whether ``value`` is a valid :class:`dict <python:dict>`

    .. note::

      This will return ``True`` even if ``value`` is an empty
      :class:`dict <python:dict>`.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`

    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator

    """
    if isinstance(value, dict):
        return True

    try:
        value = validators.dict(value, **kwargs)
    except SyntaxError as error:
        raise error
    except Exception:
        return False

    return True


@disable_checker_on_env
def is_json(value,
            schema = None,
            json_serializer = None,
            **kwargs):
    """Indicate whether ``value`` is a valid JSON object.

    .. note::

      ``schema`` supports JSON Schema Drafts 3 - 7. Unless the JSON Schema indicates the
      meta-schema using a ``$schema`` property, the schema will be assumed to conform to
      Draft 7.

    :param value: The value to evaluate.

    :param schema: An optional JSON schema against which ``value`` will be validated.
    :type schema: :class:`dict <python:dict>` / :class:`str <python:str>` /
      :obj:`None <python:None>`

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`

    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator

    """
    try:
        value = validators.json(value,
                                schema = schema,
                                json_serializer = json_serializer,
                                **kwargs)
    except SyntaxError as error:
        raise error
    except Exception:
        return False

    return True


@disable_checker_on_env
def is_string(value,
              coerce_value = False,
              minimum_length = None,
              maximum_length = None,
              whitespace_padding = False,
              **kwargs):
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

    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator

    """
    if value is None:
        return False

    minimum_length = validators.integer(minimum_length, allow_empty = True, **kwargs)
    maximum_length = validators.integer(maximum_length, allow_empty = True, **kwargs)

    if isinstance(value, basestring) and not value:
        if minimum_length and minimum_length > 0 and not whitespace_padding:
            return False

        return True

    try:
        value = validators.string(value,
                                  coerce_value = coerce_value,
                                  minimum_length = minimum_length,
                                  maximum_length = maximum_length,
                                  whitespace_padding = whitespace_padding,
                                  **kwargs)
    except SyntaxError as error:
        raise error
    except Exception:
        return False

    return True


@disable_checker_on_env
def is_iterable(obj,
                forbid_literals = (str, bytes),
                minimum_length = None,
                maximum_length = None,
                **kwargs):
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

    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator

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
                                  maximum_length = maximum_length,
                                  **kwargs)
    except SyntaxError as error:
        raise error
    except Exception:
        return False

    return True


@disable_checker_on_env
def is_not_empty(value, **kwargs):
    """Indicate whether ``value`` is empty.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is empty, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`

    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator

    """
    try:
        value = validators.not_empty(value, **kwargs)
    except SyntaxError as error:
        raise error
    except Exception:
        return False

    return True


@disable_checker_on_env
def is_none(value, allow_empty = False, **kwargs):
    """Indicate whether ``value`` is :obj:`None <python:None>`.

    :param value: The value to evaluate.

    :param allow_empty: If ``True``, accepts falsey values as equivalent to
      :obj:`None <python:None>`. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :returns: ``True`` if ``value`` is :obj:`None <python:None>`, ``False``
      if it is not.
    :rtype: :class:`bool <python:bool>`

    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator

    """
    try:
        validators.none(value, allow_empty = allow_empty, **kwargs)
    except SyntaxError as error:
        raise error
    except Exception:
        return False

    return True


@disable_checker_on_env
def is_variable_name(value, **kwargs):
    """Indicate whether ``value`` is a valid Python variable name.

    .. caution::

      This function does **NOT** check whether the variable exists. It only
      checks that the ``value`` would work as a Python variable (or class, or
      function, etc.) name.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`

    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator

    """
    try:
        validators.variable_name(value, **kwargs)
    except SyntaxError as error:
        raise error
    except Exception:
        return False

    return True


@disable_checker_on_env
def is_callable(value, **kwargs):
    """Indicate whether ``value`` is callable (like a function, method, or class).

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`

    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator

    """
    return hasattr(value, '__call__')


@disable_checker_on_env
def is_uuid(value, **kwargs):
    """Indicate whether ``value`` contains a :class:`UUID <python:uuid.UUID>`

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`

    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator

    """
    try:
        validators.uuid(value, **kwargs)
    except SyntaxError as error:
        raise error
    except Exception:
        return False

    return True


## DATE / TIME

@disable_checker_on_env
def is_date(value,
            minimum = None,
            maximum = None,
            coerce_value = False,
            **kwargs):
    """Indicate whether ``value`` is a :class:`date <python:datetime.date>`.

    :param value: The value to evaluate.

    :param minimum: If supplied, will make sure that ``value`` is on or after
      this value.
    :type minimum: :class:`datetime <python:datetime.datetime>` /
      :class:`date <python:datetime.date>` / compliant :class:`str <python:str>`
      / :obj:`None <python:None>`

    :param maximum: If supplied, will make sure that ``value`` is on or before this
      value.
    :type maximum: :class:`datetime <python:datetime.datetime>` /
      :class:`date <python:datetime.date>` / compliant :class:`str <python:str>`
      / :obj:`None <python:None>`

    :param coerce_value: If ``True``, will return ``True`` if ``value`` can be
      coerced to a :class:`date <python:datetime.date>`. If ``False``,
      will only return ``True`` if ``value`` is a date value only. Defaults to
      ``False``.
    :type coerce_value: :class:`bool <python:bool>`

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`

    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator

    """
    try:
        value = validators.date(value,
                                minimum = minimum,
                                maximum = maximum,
                                coerce_value = coerce_value,
                                **kwargs)
    except SyntaxError as error:
        raise error
    except Exception:
        return False

    return True


@disable_checker_on_env
def is_datetime(value,
                minimum = None,
                maximum = None,
                coerce_value = False,
                **kwargs):
    """Indicate whether ``value`` is a :class:`datetime <python:datetime.datetime>`.

    :param value: The value to evaluate.

    :param minimum: If supplied, will make sure that ``value`` is on or after
      this value.
    :type minimum: :class:`datetime <python:datetime.datetime>` /
      :class:`date <python:datetime.date>` / compliant :class:`str <python:str>`
      / :obj:`None <python:None>`

    :param maximum: If supplied, will make sure that ``value`` is on or before this
      value.
    :type maximum: :class:`datetime <python:datetime.datetime>` /
      :class:`date <python:datetime.date>` / compliant :class:`str <python:str>`
      / :obj:`None <python:None>`

    :param coerce_value: If ``True``, will return ``True`` if ``value`` can be
      coerced to a :class:`datetime <python:datetime.datetime>`. If ``False``,
      will only return ``True`` if ``value`` is a complete timestamp. Defaults to
      ``False``.
    :type coerce_value: :class:`bool <python:bool>`

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`

    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator

    """
    try:
        value = validators.datetime(value,
                                    minimum = minimum,
                                    maximum = maximum,
                                    coerce_value = coerce_value,
                                    **kwargs)
    except SyntaxError as error:
        raise error
    except Exception:
        return False

    return True


@disable_checker_on_env
def is_time(value,
            minimum = None,
            maximum = None,
            coerce_value = False,
            **kwargs):
    """Indicate whether ``value`` is a :class:`time <python:datetime.time>`.

    :param value: The value to evaluate.

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

    :param coerce_value: If ``True``, will return ``True`` if ``value`` can be
      coerced to a :class:`time <python:datetime.time>`. If ``False``,
      will only return ``True`` if ``value`` is a valid time. Defaults to
      ``False``.
    :type coerce_value: :class:`bool <python:bool>`

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`

    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator

    """
    try:
        value = validators.time(value,
                                minimum = minimum,
                                maximum = maximum,
                                coerce_value = coerce_value,
                                **kwargs)
    except SyntaxError as error:
        raise error
    except Exception:
        return False

    return True


@disable_checker_on_env
def is_timezone(value,
                positive = True,
                **kwargs):
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

    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator

    """
    try:
        value = validators.timezone(value,
                                    positive = positive,
                                    **kwargs)
    except SyntaxError as error:
        raise error
    except Exception:
        return False

    return True


## NUMBERS

@disable_checker_on_env
def is_numeric(value,
               minimum = None,
               maximum = None,
               **kwargs):
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

    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator

    """
    try:
        value = validators.numeric(value,
                                   minimum = minimum,
                                   maximum = maximum,
                                   **kwargs)
    except SyntaxError as error:
        raise error
    except Exception:
        return False

    return True


@disable_checker_on_env
def is_integer(value,
               coerce_value = False,
               minimum = None,
               maximum = None,
               base = 10,
               **kwargs):
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

    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator

    """
    try:
        value = validators.integer(value,
                                   coerce_value = coerce_value,
                                   minimum = minimum,
                                   maximum = maximum,
                                   base = base,
                                   **kwargs)
    except SyntaxError as error:
        raise error
    except Exception:
        return False

    return True


@disable_checker_on_env
def is_float(value,
             minimum = None,
             maximum = None,
             **kwargs):
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

    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator

    """
    try:
        value = validators.float(value,
                                 minimum = minimum,
                                 maximum = maximum,
                                 **kwargs)
    except SyntaxError as error:
        raise error
    except Exception:
        return False

    return True


@disable_checker_on_env
def is_fraction(value,
                minimum = None,
                maximum = None,
                **kwargs):
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

    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator

    """
    try:
        value = validators.fraction(value,
                                    minimum = minimum,
                                    maximum = maximum,
                                    **kwargs)
    except SyntaxError as error:
        raise error
    except Exception:
        return False

    return True


@disable_checker_on_env
def is_decimal(value,
               minimum = None,
               maximum = None,
               **kwargs):
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

    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator

    """
    try:
        value = validators.decimal(value,
                                   minimum = minimum,
                                   maximum = maximum,
                                   **kwargs)
    except SyntaxError as error:
        raise error
    except Exception:
        return False

    return True


## FILE-RELATED

@disable_checker_on_env
def is_bytesIO(value, **kwargs):
    """Indicate whether ``value`` is a :class:`BytesIO <python:io.BytesIO>` object.

    .. note::

      This checker will return ``True`` even if ``value`` is empty, so long as
      its type is a :class:`BytesIO <python:io.BytesIO>`.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`

    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator

    """
    return isinstance(value, io.BytesIO)


@disable_checker_on_env
def is_stringIO(value, **kwargs):
    """Indicate whether ``value`` is a :class:`StringIO <python:io.StringIO>` object.

    .. note::

      This checker will return ``True`` even if ``value`` is empty, so long as
      its type is a :class:`String <python:io.StringIO>`.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`

    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator

    """
    return isinstance(value, io.StringIO)


@disable_checker_on_env
def is_pathlike(value, **kwargs):
    """Indicate whether ``value`` is a path-like object.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`

    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator

    """
    try:
        value = validators.path(value, **kwargs)
    except SyntaxError as error:
        raise error
    except Exception:
        return False

    return True


@disable_checker_on_env
def is_on_filesystem(value, **kwargs):
    """Indicate whether ``value`` is a file or directory that exists on the local
    filesystem.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`

    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator

    """
    try:
        value = validators.path_exists(value, **kwargs)
    except SyntaxError as error:
        raise error
    except Exception:
        return False

    return True


@disable_checker_on_env
def is_file(value, **kwargs):
    """Indicate whether ``value`` is a file that exists on the local filesystem.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`

    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator

    """
    try:
        value = validators.file_exists(value, **kwargs)
    except SyntaxError as error:
        raise error
    except Exception:
        return False

    return True


@disable_checker_on_env
def is_directory(value, **kwargs):
    """Indicate whether ``value`` is a directory that exists on the local filesystem.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`

    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator

    """
    try:
        value = validators.directory_exists(value, **kwargs)
    except SyntaxError as error:
        raise error
    except Exception:
        return False

    return True


@disable_checker_on_env
def is_readable(value, **kwargs):
    """Indicate whether ``value`` is a readable file.

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

    :param value: The value to evaluate.
    :type value: Path-like object

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`

    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator

    """
    try:
        validators.readable(value, **kwargs)
    except SyntaxError as error:
        raise error
    except Exception:
        return False

    return True


@disable_checker_on_env
def is_writeable(value,
                 **kwargs):
    """Indicate whether ``value`` is a writeable file.

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

    :param value: The value to evaluate.
    :type value: Path-like object

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`

    :raises NotImplementedError: if called on a Windows system
    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator

    """
    if sys.platform in ['win32', 'cygwin']:
        raise NotImplementedError('not supported on Windows')

    try:
        validators.writeable(value,
                             allow_empty = False,
                             **kwargs)
    except SyntaxError as error:
        raise error
    except Exception:
        return False

    return True

@disable_checker_on_env
def is_executable(value,
                  **kwargs):
    """Indicate whether ``value`` is an executable file.

    .. caution::

      This validator does **NOT** work correctly on a Windows file system. This
      is due to the vagaries of how Windows manages its file system and the
      various ways in which it can manage file permission.

      If called on a Windows file system, this validator will raise
      :class:`NotImplementedError() <python:NotImplementedError>`.

    .. caution::

      **Use of this validator is an anti-pattern and should be used with caution.**

      Validating the writability of a file *before* attempting to execute it
      exposes your code to a bug called
      `TOCTOU <https://en.wikipedia.org/wiki/Time_of_check_to_time_of_use>`_.

      This particular class of bug can expose your code to **security vulnerabilities**
      and so this validator should only be used if you are an advanced user.

      A better pattern to use when writing to file is to apply the principle of
      EAFP ("easier to ask forgiveness than permission"), and simply attempt to
      execute the file using a ``try ... except`` block.

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

    :param value: The value to evaluate.
    :type value: Path-like object

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`

    :raises NotImplementedError: if called on a Windows system
    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator

    """
    if sys.platform in ['win32', 'cygwin']:
        raise NotImplementedError('not supported on Windows')

    try:
        validators.executable(value,
                              **kwargs)
    except SyntaxError as error:
        raise error
    except Exception:
        return False

    return True


## INTERNET-RELATED

@disable_checker_on_env
def is_email(value, **kwargs):
    """Indicate whether ``value`` is an email address.

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

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`

    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator

    """
    try:
        value = validators.email(value, **kwargs)
    except SyntaxError as error:
        raise error
    except Exception:
        return False

    return True


@disable_checker_on_env
def is_url(value, **kwargs):
    """Indicate whether ``value`` is a URL.

    .. note::

      URL validation is...complicated. The methodology that we have
      adopted here is *generally* compliant with
      `RFC 1738 <https://tools.ietf.org/html/rfc1738>`_,
      `RFC 6761 <https://tools.ietf.org/html/rfc6761>`_,
      `RFC 2181 <https://tools.ietf.org/html/rfc2181>`_  and uses a combination of
      string parsing and regular expressions,

      This approach ensures more complete coverage for unusual edge cases, while
      still letting us use regular expressions that perform quickly.

    :param value: The value to evaluate.

    :param allow_special_ips: If ``True``, will succeed when validating special IP
      addresses, such as loopback IPs like ``127.0.0.1`` or ``0.0.0.0``. If ``False``,
      will fail if ``value`` is a special IP address. Defaults to ``False``.
    :type allow_special_ips: :class:`bool <python:bool>`

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`

    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator

    """
    try:
        value = validators.url(value, **kwargs)
    except SyntaxError as error:
        raise error
    except Exception:
        return False

    return True


@disable_checker_on_env
def is_domain(value, **kwargs):
    """Indicate whether ``value`` is a valid domain.

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

    :param value: The value to evaluate.

    :param allow_ips: If ``True``, will succeed when validating IP addresses,
      If ``False``, will fail if ``value`` is an IP address. Defaults to ``False``.
    :type allow_ips: :class:`bool <python:bool>`

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`

    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator

    """
    try:
        value = validators.domain(value, **kwargs)
    except SyntaxError as error:
        raise error
    except Exception:
        return False

    return True


@disable_checker_on_env
def is_ip_address(value, **kwargs):
    """Indicate whether ``value`` is a valid IP address (version 4 or version 6).

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`

    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator

    """
    try:
        value = validators.ip_address(value, **kwargs)
    except SyntaxError as error:
        raise error
    except Exception:
        return False

    return True


@disable_checker_on_env
def is_ipv4(value, **kwargs):
    """Indicate whether ``value`` is a valid IP version 4 address.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`

    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator

    """
    try:
        value = validators.ipv4(value, **kwargs)
    except SyntaxError as error:
        raise error
    except Exception:
        return False

    return True


@disable_checker_on_env
def is_ipv6(value, **kwargs):
    """Indicate whether ``value`` is a valid IP version 6 address.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`

    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator
    """
    try:
        value = validators.ipv6(value, **kwargs)
    except SyntaxError as error:
        raise error
    except Exception:
        return False

    return True


@disable_checker_on_env
def is_mac_address(value, **kwargs):
    """Indicate whether ``value`` is a valid MAC address.

    :param value: The value to evaluate.

    :returns: ``True`` if ``value`` is valid, ``False`` if it is not.
    :rtype: :class:`bool <python:bool>`

    :raises SyntaxError: if ``kwargs`` contains duplicate keyword parameters or duplicates
      keyword parameters passed to the underlying validator
    """
    try:
        value = validators.mac_address(value, **kwargs)
    except SyntaxError as error:
        raise error
    except Exception:
        return False

    return True
