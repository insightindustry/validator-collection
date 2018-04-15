# -*- coding: utf-8 -*-

"""
***********************************
tests.test_validators
***********************************

Tests for validators.

"""

import time as time_
import decimal
import fractions
import io
import os
import uuid
from datetime import datetime, date, time, tzinfo, timedelta

import pytest

import validator_collection.validators as validators
from validator_collection._compat import numeric_types


## CORE

@pytest.mark.parametrize('value, fails, allow_empty', [
    ({ 'key': 'value' }, False, False),
    ('{"key": "json"}', False, False),
    (['key', 'value'], True, False),
    ('[{"key": "json"}]', True, False),
    ({}, False, True),
    ({}, True, False),
    ('not-a-dict', True, False),
    ('', True, False),
    ('', False, True),
    (None, True, False),
    (None, False, True),
])
def test_dict(value, fails, allow_empty):
    """Does dict() return a correct value?"""
    if not fails:
        validated = validators.dict(value, allow_empty = allow_empty)
        if value:
            assert isinstance(validated, dict)
        else:
            assert validated is None
    else:
        with pytest.raises(ValueError):
            value = validators.dict(value, allow_empty = allow_empty)


@pytest.mark.parametrize('value, fails, allow_empty, minimum_length, maximum_length, whitespace_padding, expected_length', [
    ('test', False, False, None, None, False, 4),
    ('', False, True, None, None, False, 0),
    ('', True, False, None, None, False, 0),
    (None, False, True, None, None, False, 0),
    (None, True, False, None, None, False, 0),

    ('test', False, False, 4, None, False, 4),
    ('test', False, False, 1, None, False, 4),
    ('test', True, False, 50, None, False, 4),
    ('test', False, False, 50, None, True, 50),

    ('test', False, False, None, 5, False, 4),
    ('test', False, False, None, 4, False, 4),
    ('test', True, False, None, 3, False, 4),
])
def test_string(value,
                fails,
                allow_empty,
                minimum_length,
                maximum_length,
                whitespace_padding,
                expected_length):
    """Test the string validator."""
    if not fails:
        validated = validators.string(value,
                                      allow_empty = allow_empty,
                                      minimum_length = minimum_length,
                                      maximum_length = maximum_length,
                                      whitespace_padding = whitespace_padding)
        if value:
            assert isinstance(validated, str)
            assert len(validated) == expected_length
        else:
            assert validated is None
    else:
        with pytest.raises((ValueError, TypeError)):
            validated = validators.string(value,
                                          allow_empty = allow_empty,
                                          minimum_length = minimum_length,
                                          maximum_length = maximum_length,
                                          whitespace_padding = whitespace_padding)


@pytest.mark.parametrize('value, fails, allow_empty', [
    (uuid.uuid4(), False, False),
    ('123e4567-e89b-12d3-a456-426655440000', False, False),
    ('not-a-uuid', True, False),
    ('', True, False),
    ('', False, True),
    (None, True, False),
    (None, False, True),
])
def test_uuid(value, fails, allow_empty):
    """Does validate_uuid() return a correct value?"""
    if not fails:
        validated = validators.uuid(value, allow_empty = allow_empty)
        if value:
            assert isinstance(validated, uuid.UUID)
        else:
            assert validated is None
    else:
        with pytest.raises((ValueError, TypeError)):
            value = validators.uuid(value, allow_empty = allow_empty)


@pytest.mark.parametrize('value, fails, allow_empty, minimum_length, maximum_length', [
    (['test', 123], False, False, None, None),
    ([], False, True, None, None),
    ([], True, False, None, None),
    (None, False, True, None, None),
    (None, True, False, None, None),
    ('not-a-list', True, False, None, None),
    (set([1, 2, 3]), False, False, None, None),
    ((1, 2, 3), False, False, None, None),
    (set(), True, False, None, None),
    (set(), False, True, None, None),
    ((), True, False, None, None),
    ((), False, True, None, None),
    (123, True, False, None, None),

    (['test', 123], False, False, 1, None),
    (['test', 123], False, False, 2, None),
    (['test', 123], False, False, None, 3),
    (['test', 123], False, False, None, 2),
    (['test', 123], True, False, 3, None),
    (['test', 123], True, False, None, 1),

])
def test_iterable(value, fails, allow_empty, minimum_length, maximum_length):
    """Test the string validator."""
    if not fails:
        validated = validators.iterable(value,
                                        allow_empty = allow_empty,
                                        minimum_length = minimum_length,
                                        maximum_length = maximum_length)
        if value is not None:
            assert validated is not None
            assert hasattr(validated, '__iter__')
        else:
            assert validated is None
    else:
        with pytest.raises((ValueError, TypeError)):
            validated = validators.iterable(value,
                                            allow_empty = allow_empty,
                                            minimum_length = minimum_length,
                                            maximum_length = maximum_length)


@pytest.mark.parametrize('value, fails, allow_empty', [
    (['test', 123], False, False),
    ([], False, True),
    ([], True, False),
    (None, False, True),
    (None, True, False),
    ('', False, True),
    ('', True, False),
    ('not-a-list', False, False),
    (set([1, 2, 3]), False, False),
    ((1, 2, 3), False, False),
    (set(), True, False),
    (set(), False, True),
    ((), True, False),
    ((), False, True),
    (123, False, False)
])
def test_not_empty(value, fails, allow_empty):
    """Test the none validator."""
    if not fails:
        validated = validators.not_empty(value, allow_empty = allow_empty)
        if not value and allow_empty:
            assert validated is None
        elif value:
            assert validated is not None
    else:
        with pytest.raises((ValueError, TypeError)):
            validated = validators.not_empty(value, allow_empty = allow_empty)


@pytest.mark.parametrize('value, fails, allow_empty, coerce_value', [
    (['test', 123], False, False, True),
    ([], False, True, False),
    ([], True, False, False),
    (None, False, False, False),
    ('', False, True, False),
    ('', True, False, False),
    ('', False, False, True)
])
def test_none(value, fails, allow_empty, coerce_value):
    """Test the null validator."""
    if not fails:
        validated = validators.none(value,
                                    allow_empty = allow_empty,
                                    coerce_value = coerce_value)
        if coerce_value:
            assert validated is None
        elif allow_empty and not value:
            assert validated is None
        else:
            assert validated is None
    else:
        with pytest.raises((ValueError, TypeError)):
            validated = validators.none(value,
                                        allow_empty = allow_empty,
                                        coerce_value = coerce_value)


@pytest.mark.parametrize('value, fails, allow_empty', [
    ('my_variable', False, False),
    ('_my_variable', False, False),
    ('', True, False),
    ('my variable', True, False),
    ('123_variable', True, False),
    ('', True, False),
    ('my variable', True, False),
    ('123_variable', True, False),
    (None, True, False),
    ('', True, False),
    ('my variable', True, False),
    ('123_variable', True, False),
    (None, True, False)
])
def test_variable_name(value, fails, allow_empty):
    """Test the variable name validator."""
    if not fails:
        validated = validators.variable_name(value,
                                             allow_empty = allow_empty)
        if allow_empty and not value:
            assert validated is None
        else:
            assert validated is not None
    else:
        with pytest.raises(ValueError):
            validated = validators.variable_name(value,
                                                 allow_empty = allow_empty)



## DATE / TIME

@pytest.mark.parametrize('value, fails, allow_empty, minimum, maximum', [
    ('2018-01-01', False, False, None, None),
    ('2018/01/01', False, False, None, None),
    ('01/01/2018', True, False, None, None),
    (date(2018,1,1), False, False, None, None),
    (datetime.utcnow(), False, False, None, None),
    ('1/1/2018', True, False, None, None),
    ('1/1/18', True, False, None, None),
    (None, True, False, None, None),
    (None, False, True, None, None),
    ('', True, False, None, None),
    ('', False, True, None, None),
    ('1/46/2018', True, False, None, None),
    ('not-a-date', True, False, None, None),
    ('2018-01-01 00:00:00.00000', False, False, None, None),
    ('01/01/2018 00:00:00.00000', True, False, None, None),
    ('2018-01-46', True, False, None, None),
    ('1/46/2018', True, False, None, None),
    ('not-a-date', True, False, None, None),

    ('2018-01-01', False, False, '2017-12-01', None),
    ('2018/01/01', False, False, '2018-01-01', None),
    ('2018-01-01', True, False, '2018-02-01', None),

    ('2018/01/01', False, False, None, '2018-01-31'),
    ('2018/01/01', False, False, None, '2018-01-01'),
    ('2018/01/01', True, False, None, '2017-12-31'),

    (time_.time(), False, False, None, None),
    (datetime.utcnow().time(), True, False, None, None)
])
def test_date(value, fails, allow_empty, minimum, maximum):
    """Test the date validator."""
    if not fails:
        validated = validators.date(value,
                                    allow_empty = allow_empty,
                                    minimum = minimum,
                                    maximum = maximum)
        if value:
            assert isinstance(validated, date)
        else:
            assert validated is None
    else:
        with pytest.raises((ValueError, TypeError)):
            validated = validators.date(value,
                                        allow_empty = allow_empty,
                                        minimum = minimum,
                                        maximum = maximum)


@pytest.mark.parametrize('value, fails, allow_empty, minimum, maximum', [
    ('2018-01-01', False, False, None, None),
    ('2018/01/01', False, False, None, None),
    ('01/01/2018', True, False, None, None),
    (date(2018,1,1), False, False, None, None),
    (datetime.utcnow(), False, False, None, None),
    ('1/1/2018', True, False, None, None),
    ('1/1/18', True, False, None, None),
    (None, True, False, None, None),
    (None, False, True, None, None),
    ('', True, False, None, None),
    ('', False, True, None, None),
    ('1/46/2018', True, False, None, None),
    ('not-a-date', True, False, None, None),
    ('2018-01-01T00:00:00.00000', False, False, None, None),
    ('2018-01-01 00:00:00.00000', False, False, None, None),
    ('01/01/2018 00:00:00.00000', True, False, None, None),
    ('2018-01-46', True, False, None, None),
    ('1/46/2018', True, False, None, None),
    ('not-a-date', True, False, None, None),
    ('2018-01-01T00:00:00', False, False, None, None),

    ('2018-01-01', False, False, '2010-01-01', None),
    ('2018/01/01', False, False, '2018-01-01', None),
    ('2018/01/01', True, False, '2018-02-01', None),

    ('2018-01-01', False, False, None, '2018-02-01'),
    ('2018/01/01', False, False, None, '2018-01-01'),
    ('2018/01/01', True, False, None, '2010-01-01'),

    (time_.time(), False, False, None, None),
    (datetime.utcnow().time(), True, False, None, None),

])
def test_datetime(value, fails, allow_empty, minimum,  maximum):
    """Test the datetime validator."""
    if not fails:
        validated = validators.datetime(value,
                                        allow_empty = allow_empty,
                                        minimum = minimum,
                                        maximum = maximum)
        if value:
            assert isinstance(validated, datetime)
        else:
            assert validated is None
    else:
        with pytest.raises((ValueError, TypeError)):
            validated = validators.datetime(value,
                                            allow_empty = allow_empty,
                                            minimum = minimum,
                                            maximum = maximum)


@pytest.mark.parametrize('value, fails, allow_empty, minimum, maximum', [
    ('2018-01-01', False, False, None, None),
    ('2018/01/01', False, False, None, None),
    ('01/01/2018', True, False, None, None),
    (date(2018,1,1), True, False, None, None),
    (datetime.utcnow(), False, False, None, None),
    ('1/1/2018', True, False, None, None),
    ('1/1/18', True, False, None, None),
    (None, True, False, None, None),
    (None, False, True, None, None),
    ('', True, False, None, None),
    ('', False, True, None, None),
    ('1/46/2018', True, False, None, None),
    ('not-a-date', True, False, None, None),
    ('2018-01-01T00:00:00.00000', False, False, None, None),
    ('2018-01-01 00:00:00.00000', False, False, None, None),
    ('01/01/2018 00:00:00.00000', True, False, None, None),
    ('2018-01-46', True, False, None, None),
    ('1/46/2018', True, False, None, None),
    ('not-a-date', True, False, None, None),
    ('2018-01-01T00:00:00', False, False, None, None),

    ('2018-01-01', False, False, datetime(year = 2017,
                                          month = 1,
                                          day = 1).time(), None),
    ('2018/01/01', False, False, datetime(year = 2018,
                                          month = 1,
                                          day = 1).time(), None),
    ('2018/01/01', True, False, datetime(year = 2018,
                                         month = 2,
                                         day = 1,
                                         hour = 3).time(), None),

    ('2018-01-01', False, False, None, datetime(year = 2019,
                                                month = 1,
                                                day = 1).time()),
    ('2018/01/01', False, False, None, datetime(year = 2018,
                                                month = 1,
                                                day = 1).time()),
    ('2018/01/01T03:00:00', True, False, None, datetime(year = 2017,
                                                        month = 1,
                                                        day = 1,
                                                        hour = 0).time()),

    (time_.time(), False, False, None, None),
    (datetime.utcnow().time(), False, False, None, None),

])
def test_time(value, fails, allow_empty, minimum,  maximum):
    """Test the datetime validator."""
    if not fails:
        validated = validators.time(value,
                                    allow_empty = allow_empty,
                                    minimum = minimum,
                                    maximum = maximum)
        if value:
            assert isinstance(validated, time)
        else:
            assert validated is None
    else:
        with pytest.raises((ValueError, TypeError)):
            validated = validators.time(value,
                                        allow_empty = allow_empty,
                                        minimum = minimum,
                                        maximum = maximum)
            print(validated)


@pytest.mark.parametrize('value, fails, allow_empty', [
    ('2018-01-01', False, False),
    ('2018/01/01', False, False),
    ('01/01/2018', True, False),
    (date(2018,1,1), False, False),
    (datetime.utcnow(), False, False),
    ('1/1/2018', True, False),
    ('1/1/18', True, False),
    (None, True, False),
    (None, False, True),
    ('', True, False),
    ('', False, True),
    ('1/46/2018', True, False),
    ('not-a-date', True, False),
    ('2018-01-01T00:00:00.00000', False, False),
    ('2018-01-01 00:00:00.00000', False, False),
    ('01/01/2018 00:00:00.00000', True, False),
    ('2018-01-46', True, False),
    ('1/46/2018', True, False),
    ('not-a-date', True, False),
    ('2018-01-01T00:00:00', False, False),
    ('2018-01-01 00:00:00', False, False),

    (time_.time(), False, False),
    (datetime.utcnow().time(), False, False),

    ('2018-01-01T00:00:00.00000+05:00', False, False),
    ('2018-01-01T00:00:00.00000-05:00', False, False),
    ('2018-01-01T00:00:00.00000-48:00', False, False),
    ('01/01/2018T00:00:00.00000-48:00', True, False),
    ('2018-01-01T00:00:00+01:00', False, False),
    ('2018-01-01T00:00:00+00:00', False, False),
    ('2018-01-01T00:00:00-01:00', False, False),
    ('01/01/2018T00:00:00.00000-48:00', True, False),
    ('2018-01-01T00:00:00+48:00', False, False),


    ('+06:00', False, False),
    ('-06:00', False, False),
    ('+12:00', False, False),
    ('+1:00', False, False),
    ('+48:00', True, False),

])
def test_timezone(value, fails, allow_empty):
    """Test the tzinfo validator."""
    if not fails:
        validated = validators.timezone(value,
                                        allow_empty = allow_empty)
        if value:
            assert isinstance(validated, (tzinfo, type(None)))
        else:
            assert validated is None
    else:
        with pytest.raises(ValueError):
            value = validators.timezone(value,
                                        allow_empty = allow_empty)


## NUMBERS

@pytest.mark.parametrize('value, fails, allow_empty, minimum, maximum', [
    (1, False, False, None, None),
    (1.5, False, False, None, None),
    (0, False, False, None, None),
    (None, True, False, None, None),
    (None, False, True, None, None),
    (decimal.Decimal(1.5), False, False, None, None),
    (fractions.Fraction(1.5), False, False, None, None),

    (1, False, False, -5, None),
    (1, False, False, 1, None),
    (1, True, False, 5, None),

    (5, False, False, None, 10),
    (5, False, False, None, 5),
    (5, True, False, None, 1),

])
def test_numeric(value, fails, allow_empty, minimum, maximum):
    """Test the numeric validator."""
    if not fails:
        validated = validators.numeric(value,
                                       allow_empty = allow_empty,
                                       minimum = minimum,
                                       maximum = maximum)
        if value is not None:
            assert isinstance(validated, numeric_types)
        else:
            assert validated is None
    else:
        with pytest.raises((ValueError, TypeError)):
            validated = validators.numeric(value,
                                           allow_empty = allow_empty,
                                           minimum = minimum,
                                           maximum = maximum)


@pytest.mark.parametrize('value, fails, allow_empty, coerce_value, minimum, maximum, expects', [
    (1, False, False, False, None, None, 1),
    (1.5, True, False, False, None, None, 2),
    (1.5, False, False, True, None, None, 2),
    (0, False, False, False, None, None, 0),
    (None, True, False, False, None, None, None),
    (None, False, True, False, None, None, None),
    (decimal.Decimal(1.5), True, False, False, None, None, 2),
    (decimal.Decimal(1.5), False, False, True, None, None, 2),
    (fractions.Fraction(1.5), True, False, False, None, None, 2),
    (fractions.Fraction(1.5), False, False, True, None, None, 2),

    (1, False, False, False, -5, None, 1),
    (1, False, False, False, 1, None, 1),
    (1, True, False, False, 5, None, None),

    (5, False, False, None, False, 10, 5),
    (5, False, False, None, False, 5, 5),
    (5, True, False, None, False, 1, None),

])
def test_integer(value, fails, allow_empty, coerce_value, minimum, maximum, expects):
    """Test the numeric validator."""
    if not fails:
        validated = validators.integer(value,
                                       allow_empty = allow_empty,
                                       coerce_value = coerce_value,
                                       minimum = minimum,
                                       maximum = maximum)
        if value is not None:
            assert isinstance(validated, numeric_types)
            assert validated == expects
        else:
            assert validated is None
    else:
        with pytest.raises((ValueError, TypeError)):
            validated = validators.integer(value,
                                           allow_empty = allow_empty,
                                           coerce_value = coerce_value,
                                           minimum = minimum,
                                           maximum = maximum)


@pytest.mark.parametrize('value, fails, allow_empty, minimum, maximum', [
    (1, False, False, None, None),
    (1.5, False, False, None, None),
    (0, False, False, None, None),
    (None, True, False, None, None),
    (None, False, True, None, None),
    (decimal.Decimal(1.5), False, False, None, None),
    (fractions.Fraction(1.5), False, False, None, None),

    (1, False, False, -5, None),
    (1, False, False, 1, None),
    (1, True, False, 5, None),

    (5, False, False, None, 10),
    (5, False, False, None, 5),
    (5, True, False, None, 1),

])
def test_float(value, fails, allow_empty, minimum, maximum):
    """Test the numeric validator."""
    if not fails:
        validated = validators.float(value,
                                     allow_empty = allow_empty,
                                     minimum = minimum,
                                     maximum = maximum)
        if value is not None:
            assert isinstance(validated, float)
        else:
            assert validated is None
    else:
        with pytest.raises((ValueError, TypeError)):
            validated = validators.float(value,
                                         allow_empty = allow_empty,
                                         minimum = minimum,
                                         maximum = maximum)


@pytest.mark.parametrize('value, fails, allow_empty, minimum, maximum', [
    (1, False, False, None, None),
    (1.5, False, False, None, None),
    (0, False, False, None, None),
    (None, True, False, None, None),
    (None, False, True, None, None),
    (decimal.Decimal(1.5), False, False, None, None),
    (fractions.Fraction(1.5), False, False, None, None),

    (1, False, False, -5, None),
    (1, False, False, 1, None),
    (1, True, False, 5, None),

    (5, False, False, None, 10),
    (5, False, False, None, 5),
    (5, True, False, None, 1),

])
def test_fraction(value, fails, allow_empty, minimum, maximum):
    """Test the numeric validator."""
    if not fails:
        validated = validators.fraction(value,
                                        allow_empty = allow_empty,
                                        minimum = minimum,
                                        maximum = maximum)
        if value is not None:
            assert isinstance(validated, fractions.Fraction)
        else:
            assert validated is None
    else:
        with pytest.raises((ValueError, TypeError)):
            validated = validators.fraction(value,
                                            allow_empty = allow_empty,
                                            minimum = minimum,
                                            maximum = maximum)


@pytest.mark.parametrize('value, fails, allow_empty, minimum, maximum', [
    (1, False, False, None, None),
    (1.5, False, False, None, None),
    (0, False, False, None, None),
    (None, True, False, None, None),
    (None, False, True, None, None),
    (decimal.Decimal(1.5), False, False, None, None),
    (fractions.Fraction(1.5), False, False, None, None),

    (1, False, False, -5, None),
    (1, False, False, 1, None),
    (1, True, False, 5, None),

    (5, False, False, None, 10),
    (5, False, False, None, 5),
    (5, True, False, None, 1),

])
def test_decimal(value, fails, allow_empty, minimum, maximum):
    """Test the numeric validator."""
    if not fails:
        validated = validators.decimal(value,
                                       allow_empty = allow_empty,
                                       minimum = minimum,
                                       maximum = maximum)
        if value is not None:
            assert isinstance(validated, decimal.Decimal)
        else:
            assert validated is None
    else:
        with pytest.raises((ValueError, TypeError)):
            validated = validators.decimal(value,
                                           allow_empty = allow_empty,
                                           minimum = minimum,
                                           maximum = maximum)


## FILE-RELATED

@pytest.mark.parametrize('value, fails, allow_empty', [
    (io.BytesIO(), False, False),
    ("", True, False),
    (None, True, False),
    ("", False, True),
    (None, False, True)
])
def test_bytesIO(value, fails, allow_empty):
    """Test the bytesIO validator."""
    if not fails:
        validated = validators.bytesIO(value, allow_empty = allow_empty)
        if value:
            assert isinstance(validated, io.BytesIO)
        else:
            assert validated is None
    else:
        with pytest.raises((ValueError, TypeError)):
            validated = validators.bytesIO(value, allow_empty = allow_empty)


@pytest.mark.parametrize('value, fails, allow_empty', [
    (io.StringIO(), False, False),
    ("", True, False),
    (None, True, False),
    ("", False, True),
    (None, False, True)
])
def test_stringIO(value, fails, allow_empty):
    """Test the bytesIO validator."""
    if not fails:
        validated = validators.stringIO(value, allow_empty = allow_empty)
        if value:
            assert isinstance(validated, io.StringIO)
        else:
            assert validated is None
    else:
        with pytest.raises((ValueError, TypeError)):
            validated = validators.stringIO(value, allow_empty = allow_empty)


@pytest.mark.parametrize('value, fails, allow_empty', [
    ('/test', False, False),
    ('.', False, False),
    ('./', False, False),
    (os.path.abspath('.'), False, False),
    (123, True, False),
    ("", True, False),
    (None, True, False),
    ("", False, True),
    (None, False, True)
])
def test_path(value, fails, allow_empty):
    """Test the bytesIO validator."""
    if not fails:
        validated = validators.path(value, allow_empty = allow_empty)
        if value:
            assert validated is not None
        else:
            assert validated is None
    else:
        with pytest.raises((ValueError, TypeError)):
            validated = validators.path(value, allow_empty = allow_empty)


@pytest.mark.parametrize('value, fails, allow_empty', [
    ('/test', True, False),
    ('.', False, False),
    ('./', False, False),
    (os.path.abspath('.'), False, False),
    (123, True, False),
    ("", True, False),
    (None, True, False),
    ("", False, True),
    (None, False, True)
])
def test_path_exists(value, fails, allow_empty):
    """Test the bytesIO validator."""
    if not fails:
        validated = validators.path_exists(value, allow_empty = allow_empty)
        if value:
            assert validated is not None
        else:
            assert validated is None
    else:
        with pytest.raises((ValueError, TypeError, IOError)):
            validated = validators.path_exists(value, allow_empty = allow_empty)


@pytest.mark.parametrize('value, fails, allow_empty', [
    ('/test', True, False),
    (os.path.abspath(__file__), False, False),
    (os.path.abspath('.'), True, False),
    (123, True, False),
    ("", True, False),
    (None, True, False),
    ("", False, True),
    (None, False, True)
])
def test_file_exists(value, fails, allow_empty):
    """Test the bytesIO validator."""
    if not fails:
        validated = validators.file_exists(value, allow_empty = allow_empty)
        if value:
            assert validated is not None
        else:
            assert validated is None
    else:
        with pytest.raises((ValueError, TypeError, IOError)):
            validated = validators.file_exists(value, allow_empty = allow_empty)


@pytest.mark.parametrize('value, fails, allow_empty', [
    ('/test', True, False),
    (os.path.abspath(__file__), True, False),
    (os.path.abspath('.'), False, False),
    (os.path.dirname(os.path.abspath('.')), False, False),
    (123, True, False),
    ("", True, False),
    (None, True, False),
    ("", False, True),
    (None, False, True)
])
def test_directory_exists(value, fails, allow_empty):
    """Test the bytesIO validator."""
    if not fails:
        validated = validators.directory_exists(value, allow_empty = allow_empty)
        if value:
            assert validated is not None
        else:
            assert validated is None
    else:
        with pytest.raises((ValueError, TypeError, IOError)):
            validated = validators.directory_exists(value, allow_empty = allow_empty)


## INTERNET-RELATED

@pytest.mark.parametrize('value, fails, allow_empty', [
    ("http://foo.com/blah_blah", False, False),
    ("http://foo.com/blah_blah/", False, False),
    ("http://foo.com/blah_blah_(wikipedia)", False, False),
    ("http://foo.com/blah_blah_(wikipedia)_(again)", False, False),
    ("http://www.example.com/wpstyle/?p=364", False, False),
    ("https://www.example.com/foo/?bar=baz&inga=42&quux", False, False),
    ("http://✪df.ws/123", False, False),
    ("http://userid:password@example.com:8080", False, False),
    ("http://userid:password@example.com:8080/", False, False),
    ("http://userid@example.com", False, False),
    ("http://userid@example.com/", False, False),
    ("http://userid@example.com:8080", False, False),
    ("http://userid@example.com:8080/", False, False),
    ("http://userid:password@example.com", False, False),
    ("http://userid:password@example.com/", False, False),
    ("http://142.42.1.1/", False, False),
    ("http://142.42.1.1:8080/", False, False),
    ("http://➡.ws/䨹", False, False),
    ("http://⌘.ws", False, False),
    ("http://⌘.ws/", False, False),
    ("http://foo.com/blah_(wikipedia)#cite-1", False, False),
    ("http://foo.com/blah_(wikipedia)_blah#cite-1", False, False),
    ("http://foo.com/unicode_(✪)_in_parens", False, False),
    ("http://foo.com/(something)?after=parens", False, False),
    ("http://☺.damowmow.com/", False, False),
    ("http://code.google.com/events/#&product=browser", False, False),
    ("http://j.mp", False, False),
    ("ftp://foo.bar/baz", False, False),
    ("http://foo.bar/?q=Test%20URL-encoded%20stuff", False, False),
    ("http://مثال.إختبار", False, False),
    ("http://例子.测试", False, False),
    ("http://उदाहरण.परीक्षा", False, False),
    ("http://-.~_!$&'()*+,;=:%40:80%2f::::::@example.com", False, False),
    ("http://1337.net", False, False),
    ("http://a.b-c.de", False, False),
    ("http://a.b--c.de/", False, False),
    ("http://223.255.255.254", False, False),
    ("", True, False),
    (None, True, False),
    ("http://", True, False),
    ("http://.", True, False),
    ("http://..", True, False),
    ("http://../", True, False),
    ("http://?", True, False),
    ("http://??", True, False),
    ("http://??/", True, False),
    ("http://#", True, False),
    ("http://##", True, False),
    ("http://##/", True, False),
    ("http://foo.bar?q=Spaces should be encoded", True, False),
    ("//", True, False),
    ("//a", True, False),
    ("///a", True, False),
    ("///", True, False),
    ("http:///a", True, False),
    ("foo.com", True, False),
    ("rdar://1234", True, False),
    ("h://test", True, False),
    ("http:// shouldfail.com", True, False),
    (":// should fail", True, False),
    ("http://foo.bar/foo(bar)baz quux", True, False),
    ("ftps://foo.bar/", True, False),
    ("http://-error-.invalid/", True, False),
    ("http://-a.b.co", True, False),
    ("http://a.b-.co", True, False),
    ("http://0.0.0.0", True, False),
    ("http://10.1.1.0", True, False),
    ("http://10.1.1.255", True, False),
    ("http://224.1.1.1", True, False),
    ("http://1.1.1.1.1", True, False),
    ("http://123.123.123", True, False),
    ("http://3628126748", True, False),
    ("http://.www.foo.bar/", True, False),
    ("http://www.foo.bar./", True, False),
    ("http://.www.foo.bar./", True, False),
    ("http://10.1.1.1", True, False),
    ("", False, True),
    (None, False, True)
])
def test_url(value, fails, allow_empty):
    """Test the URL validator."""
    if not fails:
        validated = validators.url(value, allow_empty = allow_empty)
        if value:
            assert isinstance(validated, str)
        else:
            assert validated is None
    else:
        with pytest.raises((ValueError, TypeError)):
            value = validators.url(value, allow_empty = allow_empty)


@pytest.mark.parametrize('value, fails, allow_empty', [
    ('test@domain.dev', False, False),
    ('@domain.dev', True, False),
    ('domain.dev', True, False),
    ('not-an-email', True, False),
    ('', True, False),
    ('', False, True),
    (None, True, False),
    (None, False, True)
])
def test_email(value, fails, allow_empty):
    """Does validate_email_address() return a correct value?"""
    if not fails:
        validated = validators.email(value, allow_empty = allow_empty)
        if value:
            assert isinstance(validated, str)
            assert '@' in validated
        else:
            assert validated is None
    else:
        with pytest.raises((ValueError, TypeError)):
            value = validators.email(value, allow_empty = allow_empty)


@pytest.mark.parametrize('value, fails, allow_empty', [
    ('0.0.0.0', False, False),
    ('10.10.10.10', False, False),
    ('192.168.1.1', False, False),
    ('255.255.255.255', False, False),
    ('0.0.0', True, False),
    ('0', True, False),
    ('abc0.0.0.0', True, False),
    ('a.b.c.d', True, False),
    ('275.276.278.279', True, False),
    ('not-a-valid-value', True, False),
    (123, True, False),
    ("", True, False),
    (None, True, False),
    ("", False, True),
    (None, False, True),

    ('::1', False, False),
    ('abcd:ffff:0:0:0:0:41:2', False, False),
    ('abcd:abcd::1:2', False, False),
    ('0:0:0:0:0:ffff:1.2.3.4', False, False),
    ('0:0:0:0:ffff:1.2.3.4', True, False),
    ('::0.0.0.0', False, False),
    ('::10.10.10.10', False, False),
    ('::192.168.1.1', False, False),
    ('::255.255.255.255', False, False),
    ('abcd.0.0.0', True, False),
    ('abcd:123::123:1', False, False),
    ('1:2:3:4:5:6:7:8:9', True, False),
    ('abcd:1abcd', True, False),
    ('::0.0.0', True, False),
    ('abc0.0.0.0', True, False),
    ('a.b.c.d', True, False),
    ('::275.276.278.279', True, False),
    ('not-a-valid-value', True, False),
    (123, True, False),
    ("", True, False),
    (None, True, False),
    ("", False, True),
    (None, False, True)
])
def test_ip_address(value, fails, allow_empty):
    """Test the ip address validator."""
    if not fails:
        validated = validators.ip_address(value, allow_empty = allow_empty)
        if value:
            assert validated is not None
        else:
            assert validated is None
    else:
        with pytest.raises(ValueError):
            validated = validators.ip_address(value, allow_empty = allow_empty)


@pytest.mark.parametrize('value, fails, allow_empty', [
    ('0.0.0.0', False, False),
    ('10.10.10.10', False, False),
    ('192.168.1.1', False, False),
    ('255.255.255.255', False, False),
    ('0.0.0', True, False),
    ('0', True, False),
    ('abc0.0.0.0', True, False),
    ('a.b.c.d', True, False),
    ('275.276.278.279', True, False),
    ('not-a-valid-value', True, False),
    (123, True, False),
    ("", True, False),
    (None, True, False),
    ("", False, True),
    (None, False, True)
])
def test_ipv4(value, fails, allow_empty):
    """Test the ipv4 validator."""
    if not fails:
        validated = validators.ipv4(value, allow_empty = allow_empty)
        if value:
            assert validated is not None
        else:
            assert validated is None
    else:
        with pytest.raises(ValueError):
            validated = validators.ipv4(value, allow_empty = allow_empty)


@pytest.mark.parametrize('value, fails, allow_empty', [
    ('::1', False, False),
    ('abcd:ffff:0:0:0:0:41:2', False, False),
    ('abcd:abcd::1:2', False, False),
    ('0:0:0:0:0:ffff:1.2.3.4', False, False),
    ('0:0:0:0:ffff:1.2.3.4', True, False),
    ('::0.0.0.0', False, False),
    ('::10.10.10.10', False, False),
    ('::192.168.1.1', False, False),
    ('::255.255.255.255', False, False),
    ('abcd.0.0.0', True, False),
    ('abcd:123::123:1', False, False),
    ('1:2:3:4:5:6:7:8:9', True, False),
    ('abcd:1abcd', True, False),
    ('::0.0.0', True, False),
    ('abc0.0.0.0', True, False),
    ('a.b.c.d', True, False),
    ('::275.276.278.279', True, False),
    ('not-a-valid-value', True, False),
    (123, True, False),
    ("", True, False),
    (None, True, False),
    ("", False, True),
    (None, False, True)
])
def test_ipv6(value, fails, allow_empty):
    """Test the ipv6 validator."""
    if not fails:
        validated = validators.ipv6(value, allow_empty = allow_empty)
        if value:
            assert validated is not None
        else:
            assert validated is None
    else:
        with pytest.raises(ValueError):
            validated = validators.ipv6(value, allow_empty = allow_empty)


@pytest.mark.parametrize('value, fails, allow_empty', [
    ('01:23:45:67:ab:CD', False, False),
    ('C0:8E:80:0E:30:54', False, False),
    ('36:5d:44:50:36:ae', False, False),
    ('6c:ee:1b:41:d9:ea', False, False),
    ('6c:ee:1b:41:d9:ea', False, False),
    ('01-23-45-67-ab-CD', False, False),
    ('C0-8E-80-0E-30-54', False, False),
    ('36-5d-44-50-36-ae', False, False),
    ('6c-ee-1b-41-d9-ea', False, False),
    ('6c-ee-1b-41-d9-ea', False, False),
    ('0.0.0', True, False),
    ('0', True, False),
    ('abc0.0.0.0', True, False),
    ('a.b.c.d', True, False),
    ('275.276.278.279', True, False),
    ('not-a-valid-value', True, False),
    (123, True, False),
    ("", True, False),
    (None, True, False),
    ("", False, True),
    (None, False, True)
])
def test_mac_address(value, fails, allow_empty):
    """Test the ipv4 validator."""
    if not fails:
        validated = validators.mac_address(value, allow_empty = allow_empty)
        if value:
            assert validated is not None
        else:
            assert validated is None
    else:
        with pytest.raises(ValueError):
            validated = validators.mac_address(value, allow_empty = allow_empty)
