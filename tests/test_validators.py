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
import random
import sys
import uuid
from datetime import datetime, date, time, tzinfo, timedelta

import pytest

import validator_collection.validators as validators
from validator_collection._compat import numeric_types, basestring
from tests.conftest import GetItemIterable, IterIterable, IterableIterable, FalseIterable


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
        with pytest.raises((ValueError, TypeError)):
            value = validators.dict(value, allow_empty = allow_empty)


@pytest.mark.parametrize('value, schema, fails, allow_empty, return_type', [
    ({ 'key': 'value' }, None, False, False, dict),
    ('{"key": "json"}', None, False, False, dict),
    (['key', 'value'], None, False, False, list),
    ('[{"key": "json"}]', None, False, False, list),
    ({}, None, False, True, type(None)),
    ({}, None, True, False, None),
    ('not-a-dict', None, True, False, None),
    ('', None, True, False, None),
    ('', None, False, True, type(None)),
    (None, None, True, False, None),
    (None, None, False, True, type(None)),

    ({ 'key': 'value' },
     {
         '$schema': "http://json-schema.org/draft-04/schema#",
         'type': "object",
         'properties': {
             'key': {
                 'type': 'string',
                 'title': 'Key',
                 'description': 'A key property.',
                 'example': 'Some example goes here.',
                 'readOnly': True
             }
         },
         'required': [
             'key'
         ]
     }, False, False, dict),
    ({ 'key': 'value' },
     {
         '$schema': "http://json-schema.org/draft-04/schema#",
         'type': "object",
         'properties': {
             'key': {
                 'type': 'boolean',
                 'title': 'Key',
                 'description': 'A key property.',
                 'example': 'Some example goes here.',
                 'readOnly': True
             }
         },
         'required': [
             'key'
         ]
     }, True, False, dict),
    ('{"key": "json"}',
     {
         '$schema': "http://json-schema.org/draft-04/schema#",
         'type': "object",
         'properties': {
             'key': {
                 'type': 'string',
                 'title': 'Key',
                 'description': 'A key property.',
                 'example': 'Some example goes here.',
                 'readOnly': True
             }
         },
         'required': [
             'key'
         ]
     }, False, False, dict),
    ('{"key": "json"}',
     {
         '$schema': "http://json-schema.org/draft-04/schema#",
         'type': "object",
         'properties': {
             'key': {
                 'type': 'integer',
                 'title': 'Key',
                 'description': 'A key property.',
                 'example': 'Some example goes here.',
                 'readOnly': True
             }
         },
         'required': [
             'key'
         ]
     }, True, False, dict),
    (['key', 'value'], {"minItems": 0, "maxItems": 2}, False, False, list),
    (['key', 'value'], {"minItems": 3, "maxItems": 3}, True, False, list),
    ('[{"key": "json"}]', {"minItems": 0, "maxItems": 2}, False, False, list),
    ('[{"key": "json"}]', {"minItems": 3, "maxItems": 3}, True, False, list),

])
def test_json(value, schema, fails, allow_empty, return_type):
    """Does json() return a correct value?"""
    if not fails:
        validated = validators.json(value, schema, allow_empty = allow_empty)
        if value:
            assert isinstance(validated, return_type)
        else:
            assert validated is None
    else:
        with pytest.raises((ValueError, TypeError)):
            value = validators.json(value, schema, allow_empty = allow_empty)


@pytest.mark.parametrize('value, fails, allow_empty, coerce_value, minimum_length, maximum_length, whitespace_padding, expected_length', [
    ('test', False, False, False, None, None, False, 4),
    ('', False, True, False, None, None, False, 0),
    ('', True, False, False, None, None, False, 0),
    (None, False, True, False, None, None, False, 0),
    (None, True, False, False, None, None, False, 0),

    ('test', False, False, False, 4, None, False, 4),
    ('test', False, False, False, 1, None, False, 4),
    ('test', True, False, False, 50, None, False, 4),
    ('test', False, False, False, 50, None, True, 50),

    ('test', False, False, False, None, 5, False, 4),
    ('test', False, False, False, None, 4, False, 4),
    ('test', True, False, False, None, 3, False, 4),

    (123, True, False, False, None, None, False, None),
    (123, False, False, True, None, None, False, 3),

])
def test_string(value,
                fails,
                allow_empty,
                coerce_value,
                minimum_length,
                maximum_length,
                whitespace_padding,
                expected_length):
    """Test the string validator."""
    if not fails:
        validated = validators.string(value,
                                      allow_empty = allow_empty,
                                      coerce_value = coerce_value,
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
                                          coerce_value = coerce_value,
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

    (GetItemIterable(), False, False, None, None),
    (IterIterable(), False, False, None, None),
    (IterableIterable(), False, False, None, None),

    (FalseIterable(), True, False, None, None),

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
            iter(validated)
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


@pytest.mark.parametrize('value, fails, allow_empty', [
    (['test', 123], True, False),
    ([], False, True),
    ([], True, False),
    (None, False, False),
    ('', False, True),
    ('', True, False),
])
def test_none(value, fails, allow_empty):
    """Test the null validator."""
    if not fails:
        validated = validators.none(value,
                                    allow_empty = allow_empty)
        assert validated is None
    else:
        with pytest.raises((ValueError, TypeError)):
            validated = validators.none(value,
                                        allow_empty = allow_empty)


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
    (None, True, False),
    ('raise Exception("Foo")\nxyz', True, False),
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
        with pytest.raises((ValueError, TypeError)):
            validated = validators.variable_name(value,
                                                 allow_empty = allow_empty)



## DATE / TIME

@pytest.mark.parametrize('value, fails, allow_empty, minimum, maximum, coerce_value', [
    ('2018-01-01', False, False, None, None, True),
    ('2018/01/01', False, False, None, None, True),
    ('01/01/2018', True, False, None, None, True),
    (date(2018,1,1), False, False, None, None, True),
    (datetime.utcnow(), False, False, None, None, True),
    ('1/1/2018', True, False, None, None, True),
    ('1/1/18', True, False, None, None, True),
    (None, True, False, None, None, True),
    (None, False, True, None, None, True),
    ('', True, False, None, None, True),
    ('', False, True, None, None, True),
    ('1/46/2018', True, False, None, None, True),
    ('not-a-date', True, False, None, None, True),
    ('2018-01-01 00:00:00.00000', False, False, None, None, True),
    ('01/01/2018 00:00:00.00000', True, False, None, None, True),
    ('2018-01-46', True, False, None, None, True),
    ('1/46/2018', True, False, None, None, True),
    ('not-a-date', True, False, None, None, True),

    ('2018-01-01', False, False, '2017-12-01', None, True),
    ('2018/01/01', False, False, '2018-01-01', None, True),
    ('2018-01-01', True, False, '2018-02-01', None, True),

    ('2018/01/01', False, False, None, '2018-01-31', True),
    ('2018/01/01', False, False, None, '2018-01-01', True),
    ('2018/01/01', True, False, None, '2017-12-31', True),

    (time_.time(), False, False, None, None, True),
    (datetime.utcnow().time(), True, False, None, None, True),


    ('2018-01-01', False, False, None, None, False),
    ('2018/01/01', False, False, None, None, False),
    ('01/01/2018', True, False, None, None, False),
    (date(2018,1,1), False, False, None, None, False),
    (datetime.utcnow(), True, False, None, None, False),
    ('1/1/2018', True, False, None, None, False),
    ('1/1/18', True, False, None, None, False),
    (None, True, False, None, None, False),
    (None, False, True, None, None, False),
    ('', True, False, None, None, False),
    ('', False, True, None, None, False),
    ('1/46/2018', True, False, None, None, False),
    ('not-a-date', True, False, None, None, False),
    ('2018-01-01 00:00:00.00000', True, False, None, None, False),
    ('01/01/2018 00:00:00.00000', True, False, None, None, False),
    ('2018-01-46', True, False, None, None, False),
    ('1/46/2018', True, False, None, None, False),
    ('not-a-date', True, False, None, None, False),

    ('2018-01-01', False, False, '2017-12-01', None, False),
    ('2018/01/01', False, False, '2018-01-01', None, False),
    ('2018-01-01', True, False, '2018-02-01', None, False),

    ('2018/01/01', False, False, None, '2018-01-31', False),
    ('2018/01/01', False, False, None, '2018-01-01', False),
    ('2018/01/01', True, False, None, '2017-12-31', False),

    (time_.time(), True, False, None, None, False),
    (datetime.utcnow().time(), True, False, None, None, False),

])
def test_date(value, fails, allow_empty, minimum, maximum, coerce_value):
    """Test the date validator."""
    if not fails:
        validated = validators.date(value,
                                    allow_empty = allow_empty,
                                    minimum = minimum,
                                    maximum = maximum,
                                    coerce_value = coerce_value)
        if value:
            assert isinstance(validated, date)
        else:
            assert validated is None
    else:
        with pytest.raises((ValueError, TypeError)):
            validated = validators.date(value,
                                        allow_empty = allow_empty,
                                        minimum = minimum,
                                        maximum = maximum,
                                        coerce_value = coerce_value)


@pytest.mark.parametrize('value, fails, allow_empty, minimum, maximum, coerce_value', [
    ('2018-01-01', False, False, None, None, True),
    ('2018/01/01', False, False, None, None, True),
    ('01/01/2018', True, False, None, None, True),
    (date(2018,1,1), False, False, None, None, True),
    (datetime.utcnow(), False, False, None, None, True),
    ('1/1/2018', True, False, None, None, True),
    ('1/1/18', True, False, None, None, True),
    (None, True, False, None, None, True),
    (None, False, True, None, None, True),
    ('', True, False, None, None, True),
    ('', False, True, None, None, True),
    ('1/46/2018', True, False, None, None, True),
    ('not-a-date', True, False, None, None, True),
    ('2018-01-01T00:00:00.00000', False, False, None, None, True),
    ('2018-01-01 00:00:00.00000', False, False, None, None, True),
    ('01/01/2018 00:00:00.00000', True, False, None, None, True),
    ('2018-01-46', True, False, None, None, True),
    ('1/46/2018', True, False, None, None, True),
    ('not-a-date', True, False, None, None, True),
    ('2018-01-01T00:00:00', False, False, None, None, True),

    ('2018-01-01', False, False, '2010-01-01', None, True),
    ('2018/01/01', False, False, '2018-01-01', None, True),
    ('2018/01/01', True, False, '2018-02-01', None, True),

    ('2018-01-01', False, False, None, '2018-02-01', True),
    ('2018/01/01', False, False, None, '2018-01-01', True),
    ('2018/01/01', True, False, None, '2010-01-01', True),

    ('2018-01-01T00:00:00.000000', False, False, None, None, True),
    ('2018-01-01T00:00:00.000000Z', False, False, None, None, True),
    ('2018-01-01T00:00:00.000000+01:00', False, False, None, None, True),
    ('2018-01-01T00:00:00.000000Z-05:00', False, False, None, None, True),

    ('2018-01-01T00:00:00.000000Z-05:00', True, False, None, None, False),

    (time_.time(), False, False, None, None, True),
    (datetime.utcnow().time(), True, False, None, None, True),


    ('2018-01-01', True, False, None, None, False),
    ('2018/01/01', True, False, None, None, False),
    ('01/01/2018', True, False, None, None, False),
    (date(2018,1,1), True, False, None, None, False),
    (datetime.utcnow(), False, False, None, None, False),
    ('1/1/2018', True, False, None, None, False),
    ('1/1/18', True, False, None, None, False),
    (None, True, False, None, None, False),
    (None, False, True, None, None, False),
    ('', True, False, None, None, False),
    ('', False, True, None, None, False),
    ('1/46/2018', True, False, None, None, False),
    ('not-a-date', True, False, None, None, False),
    ('2018-01-01T00:00:00.00000', False, False, None, None, False),
    ('2018-01-01 00:00:00.00000', False, False, None, None, False),
    ('01/01/2018 00:00:00.00000', True, False, None, None, False),
    ('2018-01-46', True, False, None, None, False),
    ('1/46/2018', True, False, None, None, False),
    ('not-a-date', True, False, None, None, False),
    ('2018-01-01T00:00:00', False, False, None, None, False),

    ('2018-01-01', True, False, '2010-01-01', None, False),
    ('2018/01/01', True, False, '2018-01-01', None, False),
    ('2018/01/01', True, False, '2018-02-01', None, False),

    ('2018-01-01', True, False, None, '2018-02-01', False),
    ('2018/01/01', True, False, None, '2018-01-01', False),
    ('2018/01/01', True, False, None, '2010-01-01', False),

    (time_.time(), True, False, None, None, False),
    (datetime.utcnow().time(), True, False, None, None, False),

])
def test_datetime(value, fails, allow_empty, minimum, maximum, coerce_value):
    """Test the datetime validator."""
    if not fails:
        validated = validators.datetime(value,
                                        allow_empty = allow_empty,
                                        minimum = minimum,
                                        maximum = maximum,
                                        coerce_value = coerce_value)
        if value:
            assert isinstance(validated, datetime)
        else:
            assert validated is None
    else:
        with pytest.raises((ValueError, TypeError)):
            validated = validators.datetime(value,
                                            allow_empty = allow_empty,
                                            minimum = minimum,
                                            maximum = maximum,
                                            coerce_value = coerce_value)


@pytest.mark.parametrize('value, fails, allow_empty, minimum, maximum, coerce_value', [
    ('2018-01-01', True, False, None, None, True),
    ('2018/01/01', True, False, None, None, True),
    ('01/01/2018', True, False, None, None, True),
    (date(2018,1,1), True, False, None, None, True),
    (datetime.utcnow(), False, False, None, None, True),
    ('1/1/2018', True, False, None, None, True),
    ('1/1/18', True, False, None, None, True),
    (None, True, False, None, None, True),
    (None, False, True, None, None, True),
    ('', True, False, None, None, True),
    ('', False, True, None, None, True),
    ('1/46/2018', True, False, None, None, True),
    ('not-a-date', True, False, None, None, True),
    ('2018-01-01T00:00:00.00000', False, False, None, None, True),
    ('2018-01-01 00:00:00.00000', False, False, None, None, True),
    ('01/01/2018 00:00:00.00000', True, False, None, None, True),
    ('2018-01-46', True, False, None, None, True),
    ('1/46/2018', True, False, None, None, True),
    ('not-a-date', True, False, None, None, True),
    ('2018-01-01T00:00:00', False, False, None, None, True),

    ('2018-01-01', True, False, datetime(year = 2017,
                                         month = 1,
                                         day = 1).time(), None, True),
    ('2018/01/01', True, False, datetime(year = 2018,
                                         month = 1,
                                         day = 1).time(), None, True),
    ('2018-01-01T00:00:00', False, False, datetime(year = 2017,
                                                   month = 1,
                                                   day = 1).time(), None, True),
    ('2018/01/01T00:00:00', False, False, datetime(year = 2018,
                                                   month = 1,
                                                   day = 1).time(), None, True),
    ('2018/01/01', True, False, datetime(year = 2018,
                                         month = 2,
                                         day = 1,
                                         hour = 3).time(), None, True),

    ('2018-01-01', True, False, None, datetime(year = 2019,
                                               month = 1,
                                               day = 1).time(), True),
    ('2018/01/01', True, False, None, datetime(year = 2018,
                                               month = 1,
                                               day = 1).time(), True),
    ('2018-01-01T00:00:00', False, False, None, datetime(year = 2019,
                                                         month = 1,
                                                         day = 1).time(), True),
    ('2018/01/01T00:00:00', False, False, None, datetime(year = 2018,
                                                         month = 1,
                                                         day = 1).time(), True),
    ('2018/01/01T03:00:00', True, False, None, datetime(year = 2017,
                                                        month = 1,
                                                        day = 1,
                                                        hour = 0).time(), True),

    (time_.time(), False, False, None, None, True),
    (datetime.utcnow().time(), False, False, None, None, True),


    ('2018-01-01', True, False, None, None, False),
    ('2018/01/01', True, False, None, None, False),
    ('01/01/2018', True, False, None, None, False),
    (date(2018,1,1), True, False, None, None, False),
    (datetime.utcnow(), True, False, None, None, False),
    ('1/1/2018', True, False, None, None, False),
    ('1/1/18', True, False, None, None, False),
    (None, True, False, None, None, False),
    (None, False, True, None, None, False),
    ('', True, False, None, None, False),
    ('', False, True, None, None, False),
    ('1/46/2018', True, False, None, None, False),
    ('not-a-date', True, False, None, None, False),
    ('2018-01-01T00:00:00.00000', True, False, None, None, False),
    ('2018-01-01 00:00:00.00000', True, False, None, None, False),
    ('01/01/2018 00:00:00.00000', True, False, None, None, False),
    ('2018-01-46', True, False, None, None, False),
    ('1/46/2018', True, False, None, None, False),
    ('not-a-date', True, False, None, None, False),
    ('2018-01-01T00:00:00', True, False, None, None, False),

    ('2018-01-01', True, False, datetime(year = 2017,
                                         month = 1,
                                         day = 1).time(), None, False),
    ('2018/01/01', True, False, datetime(year = 2018,
                                         month = 1,
                                         day = 1).time(), None, False),
    ('2018-01-01T00:00:00', True, False, datetime(year = 2017,
                                                  month = 1,
                                                  day = 1).time(), None, False),
    ('2018/01/01T00:00:00', True, False, datetime(year = 2018,
                                                  month = 1,
                                                  day = 1).time(), None, False),
    ('2018/01/01', True, False, datetime(year = 2018,
                                         month = 2,
                                         day = 1,
                                         hour = 3).time(), None, False),

    ('2018-01-01', True, False, None, datetime(year = 2019,
                                               month = 1,
                                               day = 1).time(), False),
    ('2018/01/01', True, False, None, datetime(year = 2018,
                                               month = 1,
                                               day = 1).time(), False),
    ('2018-01-01T00:00:00', True, False, None, datetime(year = 2019,
                                                        month = 1,
                                                        day = 1).time(), False),
    ('2018/01/01T00:00:00', True, False, None, datetime(year = 2018,
                                                        month = 1,
                                                        day = 1).time(), False),
    ('2018/01/01T03:00:00', True, False, None, datetime(year = 2017,
                                                        month = 1,
                                                        day = 1,
                                                        hour = 0).time(), False),

    (time_.time(), True, False, None, None, False),
    (datetime.utcnow().time(), False, False, None, None, False),


])
def test_time(value, fails, allow_empty, minimum,  maximum, coerce_value):
    """Test the datetime validator."""
    if not fails:
        validated = validators.time(value,
                                    allow_empty = allow_empty,
                                    minimum = minimum,
                                    maximum = maximum,
                                    coerce_value = coerce_value)
        if value:
            assert isinstance(validated, time)
            if minimum is not None:
                assert validated >= minimum
            if maximum is not None:
                assert validated <= maximum
        else:
            assert validated is None
    else:
        with pytest.raises((ValueError, TypeError)):
            validated = validators.time(value,
                                        allow_empty = allow_empty,
                                        minimum = minimum,
                                        maximum = maximum,
                                        coerce_value = coerce_value)


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
        with pytest.raises((ValueError, TypeError)):
            value = validators.timezone(value,
                                        allow_empty = allow_empty)


@pytest.mark.parametrize('value, fails, allow_empty, resolution, expected_value', [
    (timedelta(seconds = 123), False, False, 'seconds', timedelta(seconds = 123)),
    (123, False, False, 'seconds', timedelta(seconds = 123)),
    (123.5, False, False, 'seconds', timedelta(seconds = 123.5)),
    (123, False, False, 'days', timedelta(days = 123)),
    (1, False, False, 'years', timedelta(days = 365)),
    (23.5, False, False, 'weeks', timedelta(days = (23.5 * 7))),
    (123, False, False, None, timedelta(seconds = 123)),

    ('00:35:00', False, False, 'seconds', timedelta(minutes = 35)),
    ('5 day, 12:36:35.333333', False, False, 'seconds', timedelta(days = 5, hours = 12, minutes = 36, seconds = 35, microseconds = 333333)),
    ('5 days, 12:36:35.333333', False, False, 'seconds', timedelta(days = 5, hours = 12, minutes = 36, seconds = 35, microseconds = 333333)),
    ('5 day, 36:36:35.333333', False, False, 'seconds', timedelta(days = 6, hours = 12, minutes = 36, seconds = 35, microseconds = 333333)),

    (None, True, False, 'seconds', None),
    ('', True, False, 'seconds', None),

    ('not a valid timedelta', True, False, 'seconds', None),
    (123, True, False, 'not-a-valid-resolution', None),

])
def test_timedelta(value, fails, allow_empty, resolution, expected_value):
    """Test the timedelta validator."""
    print('value: %s' % value)
    if not fails:
        validated = validators.timedelta(value,
                                         allow_empty = allow_empty,
                                         resolution = resolution)

        if value:
            assert isinstance(validated, timedelta)
            assert validated == expected_value
        else:
            assert validated is None

    else:
        with pytest.raises((ValueError, TypeError)):
            value = validators.timedelta(value,
                                         allow_empty = allow_empty,
                                         resolution = resolution)


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

    ('not-a-number', True, False, None, None),

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
    (123, False, False),
    (1.5, True, False),
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


@pytest.mark.parametrize('value, fails, allow_empty', [
    ('/var/data/xx1.txt', False, False),
    (None, False, True),

    ('/var/data/xx1.txt', True, False),
    (None, True, False),
])
def test_readable(fs, value, fails, allow_empty):
    """Test validators.readable()"""
    if value:
        fs.create_file(value)

    if not fails:
        validated = validators.readable(value,
                                        allow_empty = allow_empty)

        if value:
            assert validated is not None
        else:
            assert value is None
    elif fails and sys.platform in ['linux', 'linux2', 'darwin']:
        if value:
            real_uid = os.getuid()
            real_gid = os.getgid()
            fake_uid = real_uid
            fake_gid = real_gid
            while fake_uid == real_uid:
                fake_uid = int(random.random() * 100)

            while fake_gid == real_gid:
                fake_gid = int(random.random() * 100)

            os.chown(value, fake_uid, fake_gid)
            os.chmod(value, 0o027)

        with pytest.raises((IOError, ValueError)):
            validated = validators.readable(value,
                                            allow_empty = allow_empty)

    elif fails and sys.platform in ['win32', 'cygwin']:
        if not value:
            with pytest.raises((IOError, ValueError)):
                validated = validators.readable(value,
                                                allow_empty = allow_empty)
    else:
        raise NotImplementedError('platform is not supported')


@pytest.mark.parametrize('value, fails, allow_empty', [
    ('/var/data/xx1.txt', False, False),
    (None, False, True),

    ('/var/data/xx1.txt', True, False),
    (None, True, False),
])
def test_writeable(fs, value, fails, allow_empty):
    """Test validators.readable()"""
    if sys.platform in ['win32', 'cygwin'] and value:
        fails = True

    if value:
        fs.create_file(value)

    if not fails:
        validated = validators.writeable(value,
                                         allow_empty = allow_empty)

        if value:
            assert validated is not None
        else:
            assert value is None
    elif fails and sys.platform in ['linux', 'linux2', 'darwin']:
        if value:
            real_uid = os.getuid()
            real_gid = os.getgid()
            fake_uid = real_uid
            fake_gid = real_gid
            while fake_uid == real_uid:
                fake_uid = int(random.random() * 100)

            while fake_gid == real_gid:
                fake_gid = int(random.random() * 100)

            dirname = os.path.dirname(value)
            os.chown(value, fake_uid, fake_gid)
            os.chown(dirname, fake_uid, fake_gid)
            os.chmod(dirname, 0o0444)
            os.chmod(value, 0o0444)

        with pytest.raises((IOError, ValueError)):
            validated = validators.writeable(value,
                                             allow_empty = allow_empty)

    elif fails and sys.platform in ['win32', 'cygwin']:
        with pytest.raises((IOError, ValueError, NotImplementedError)):
            validated = validators.writeable(value,
                                             allow_empty = allow_empty)
    else:
        raise NotImplementedError('platform is not supported')

@pytest.mark.parametrize('value, fails, allow_empty', [
    ('/var/data/xx1.txt', False, False),
    (None, False, True),

    ('/var/data/xx1.txt', True, False),
    (None, True, False),
])
def test_executable(fs, value, fails, allow_empty):
    """Test validators.executable()"""
    if sys.platform in ['win32', 'cygwin'] and value:
        fails = True

    if value:
        fs.create_file(value)

    if not fails and sys.platform in ['linux', 'linux2', 'darwin']:
        if value:
            os.chmod(value, 0o0777)

        validated = validators.executable(value,
                                          allow_empty = allow_empty)

        if value:
            assert validated is not None
        else:
            assert value is None
    elif fails and sys.platform in ['linux', 'linux2', 'darwin']:
        if value:
            real_uid = os.getuid()
            real_gid = os.getgid()
            fake_uid = real_uid
            fake_gid = real_gid
            while fake_uid == real_uid:
                fake_uid = int(random.random() * 100)

            while fake_gid == real_gid:
                fake_gid = int(random.random() * 100)

            dirname = os.path.dirname(value)
            os.chown(value, fake_uid, fake_gid)
            os.chown(dirname, fake_uid, fake_gid)
            os.chmod(dirname, 0o0444)
            os.chmod(value, 0o0444)

        with pytest.raises((IOError, ValueError)):
            validated = validators.executable(value,
                                              allow_empty = allow_empty)

    elif fails and sys.platform in ['win32', 'cygwin']:
        with pytest.raises((IOError, ValueError, NotImplementedError)):
            validated = validators.executable(value,
                                              allow_empty = allow_empty)
    elif not fails:
        validated = validators.executable(value,
                                          allow_empty = allow_empty)
    else:
        raise NotImplementedError('platform is not supported')


## INTERNET-RELATED

@pytest.mark.parametrize('value, fails, allow_empty, allow_special_ips', [
    (u"http://foo.com/blah_blah", False, False, False),
    (u"http://foo.com/blah_blah/", False, False, False),
    (u"http://foo.com/blah_blah_(wikipedia)", False, False, False),
    (u"http://foo.com/blah_blah_(wikipedia)_(again)", False, False, False),
    (u"http://www.example.com/wpstyle/?p=364", False, False, False),
    (u"https://www.example.com/foo/?bar=baz&inga=42&quux", False, False, False),
    (u"http://✪df.ws/123", False, False, False),
    (u"http://userid:password@example.com:8080", False, False, False),
    (u"http://userid:password@example.com:8080/", False, False, False),
    (u"http://userid@example.com", False, False, False),
    (u"http://userid@example.com/", False, False, False),
    (u"http://userid@example.com:8080", False, False, False),
    (u"http://userid@example.com:8080/", False, False, False),
    (u"http://userid:password@example.com", False, False, False),
    (u"http://userid:password@example.com/", False, False, False),
    (u"http://142.42.1.1/", False, False, False),
    (u"http://142.42.1.1:8080/", False, False, False),
    (u"http://➡.ws/䨹", False, False, False),
    (u"http://⌘.ws", False, False, False),
    (u"http://⌘.ws/", False, False, False),
    (u"http://foo.com/blah_(wikipedia)#cite-1", False, False, False),
    (u"http://foo.com/blah_(wikipedia)_blah#cite-1", False, False, False),
    (u"http://foo.com/unicode_(✪)_in_parens", False, False, False),
    (u"http://foo.com/(something)?after=parens", False, False, False),
    (u"http://☺.damowmow.com/", False, False, False),
    (u"http://jurnalsda_pusair.pu.go.id", False, False, False),
    (u"http://code.google.com/events/#&product=browser", False, False, False),
    (u"http://j.mp", False, False, False),
    (u"ftp://foo.bar/baz", False, False, False),
    (u"http://foo.bar/?q=Test%20URL-encoded%20stuff", False, False, False),
    (u"http://مثال.إختبار", False, False, False),
    (u"http://例子.测试", False, False, False),
    (u"http://उदाहरण.परीक्षा", False, False, False),
    (u"http://-.~_!$&'()*+,;=:%40:80%2f::::::@example.com", False, False, False),
    (u"http://1337.net", False, False, False),
    (u"http://a.b-c.de", False, False, False),
    (u"http://a.b--c.de/", False, False, False),
    (u"http://223.255.255.254", False, False, False),
    (u"", True, False, False),
    (None, True, False, False),
    (u"http://", True, False, False),
    (u"http://.", True, False, False),
    (u"http://..", True, False, False),
    (u"http://../", True, False, False),
    (u"http://?", True, False, False),
    (u"http://??", True, False, False),
    (u"http://??/", True, False, False),
    (u"http://#", True, False, False),
    (u"http://##", True, False, False),
    (u"http://##/", True, False, False),
    (u"http://foo.bar?q=Spaces should be encoded", True, False, False),
    (u"//", True, False, False),
    (u"//a", True, False, False),
    (u"///a", True, False, False),
    (u"///", True, False, False),
    (u"http:///a", True, False, False),
    (u"foo.com", True, False, False),
    (u"rdar://1234", True, False, False),
    (u"h://test", True, False, False),
    (u"http:// shouldfail.com", True, False, False),
    (u":// should fail", True, False, False),
    (u"http://foo.bar/foo(bar)baz quux", True, False, False),
    (u"ftps://foo.bar/", True, False, False),
    (u"http://-error-.invalid/", True, False, False),
    (u"http://-a.b.co", True, False, False),
    (u"http://a.b-.co", True, False, False),
    (u"http://0.0.0.0", True, False, False),
    (u"http://10.1.1.0", True, False, False),
    (u"http://10.1.1.255", True, False, False),
    (u"http://224.1.1.1", True, False, False),
    (u"http://1.1.1.1.1", True, False, False),
    (u"http://123.123.123", True, False, False),
    (u"http://3628126748", True, False, False),
    (u"http://.www.foo.bar/", True, False, False),
    (u"http://www.foo.bar./", True, False, False),
    (u"http://.www.foo.bar./", True, False, False),
    (u"http://10.1.1.1", True, False, False),
    (u"", False, True, False),
    (None, False, True, False),

    (u"localhost", True, False, False),
    (u"abc.localhost.com", True, False, False),
    (u"invalid", True, False, False),
    (u"abc.invalid.com", True, False, False),

    (u"http://localhost", False, False, False),
    (u"http://localhost:8080", False, False, False),
    (u"http://localhost/some_path", False, False, False),
    (u"http://localhost:8080/some_path", False, False, False),
    (u"http://someuserid:somepass@localhost/some_path/some_path", False, False, False),
    (u"http://someuserid:somepass@localhost:8080/some_path/some_path", False, False, False),
    (u"http://abc.localhost.com", False, False, False),
    (u"http://invalid", False, False, False),
    (u"http://abc.invalid.com", False, False, False),

    (u"http://foo.com/blah_blah", False, False, True),
    (u"http://foo.com/blah_blah/", False, False, True),
    (u"http://foo.com/blah_blah_(wikipedia)", False, False, True),
    (u"http://foo.com/blah_blah_(wikipedia)_(again)", False, False, True),
    (u"http://www.example.com/wpstyle/?p=364", False, False, True),
    (u"https://www.example.com/foo/?bar=baz&inga=42&quux", False, False, True),
    (u"http://✪df.ws/123", False, False, True),
    (u"http://userid:password@example.com:8080", False, False, True),
    (u"http://userid:password@example.com:8080/", False, False, True),
    (u"http://userid@example.com", False, False, True),
    (u"http://userid@example.com/", False, False, True),
    (u"http://userid@example.com:8080", False, False, True),
    (u"http://userid@example.com:8080/", False, False, True),
    (u"http://userid:password@example.com", False, False, True),
    (u"http://userid:password@example.com/", False, False, True),
    (u"http://142.42.1.1/", False, False, True),
    (u"http://142.42.1.1:8080/", False, False, True),
    (u"http://➡.ws/䨹", False, False, True),
    (u"http://⌘.ws", False, False, True),
    (u"http://⌘.ws/", False, False, True),
    (u"http://foo.com/blah_(wikipedia)#cite-1", False, False, True),
    (u"http://foo.com/blah_(wikipedia)_blah#cite-1", False, False, True),
    (u"http://foo.com/unicode_(✪)_in_parens", False, False, True),
    (u"http://foo.com/(something)?after=parens", False, False, True),
    (u"http://☺.damowmow.com/", False, False, True),
    (u"http://jurnalsda_pusair.pu.go.id", False, False, True),
    (u"http://code.google.com/events/#&product=browser", False, False, True),
    (u"http://j.mp", False, False, True),
    (u"ftp://foo.bar/baz", False, False, True),
    (u"http://foo.bar/?q=Test%20URL-encoded%20stuff", False, False, True),
    (u"http://مثال.إختبار", False, False, True),
    (u"http://例子.测试", False, False, True),
    (u"http://उदाहरण.परीक्षा", False, False, True),
    (u"http://-.~_!$&'()*+,;=:%40:80%2f::::::@example.com", False, False, True),
    (u"http://1337.net", False, False, True),
    (u"http://a.b-c.de", False, False, True),
    (u"http://a.b--c.de/", False, False, True),
    (u"http://223.255.255.254", False, False, True),
    (u"", True, False, True),
    (None, True, False, True),
    (u"http://", True, False, True),
    (u"http://.", True, False, True),
    (u"http://..", True, False, True),
    (u"http://../", True, False, True),
    (u"http://?", True, False, True),
    (u"http://??", True, False, True),
    (u"http://??/", True, False, True),
    (u"http://#", True, False, True),
    (u"http://##", True, False, True),
    (u"http://##/", True, False, True),
    (u"http://foo.bar?q=Spaces should be encoded", True, False, True),
    (u"//", True, False, True),
    (u"//a", True, False, True),
    (u"///a", True, False, True),
    (u"///", True, False, True),
    (u"http:///a", True, False, True),
    (u"foo.com", True, False, True),
    (u"rdar://1234", True, False, True),
    (u"h://test", True, False, True),
    (u"http:// shouldfail.com", True, False, True),
    (u":// should fail", True, False, True),
    (u"http://foo.bar/foo(bar)baz quux", True, False, True),
    (u"ftps://foo.bar/", True, False, True),
    (u"http://-error-.invalid/", True, False, True),
    (u"http://-a.b.co", True, False, True),
    (u"http://a.b-.co", True, False, True),
    (u"http://0.0.0.0", False, False, True),
    (u"http://10.1.1.0", False, False, True),
    (u"http://10.1.1.255", False, False, True),
    (u"http://224.1.1.1", False, False, True),
    (u"http://1.1.1.1.1", True, False, True),
    (u"http://123.123.123", True, False, True),
    (u"http://3628126748", True, False, True),
    (u"http://.www.foo.bar/", True, False, True),
    (u"http://www.foo.bar./", True, False, True),
    (u"http://.www.foo.bar./", True, False, True),
    (u"http://10.1.1.1", False, False, True),
    (u"", False, True, True),
    (None, False, True, True),

    (u"localhost", True, False, True),
    (u"abc.localhost.com", True, False, True),
    (u"invalid", True, False, True),
    (u"abc.invalid.com", True, False, True),

    (u"http://localhost", False, False, True),
    (u"http://abc.localhost.com", False, False, True),
    (u"http://invalid", False, False, True),
    (u"http://abc.invalid.com", False, False, True),

    (u"http://10.1.1.1:8080", False, False, True),
    (u"http://10.1.1.1:8080/some_path/some_path", False, False, True),
    (u"http://someuserid:somepassword@10.1.1.1:8080", False, False, True),
    (u"http://someuserid:somepassword@10.1.1.1:8080/some_path", False, False, True),
    (u"http://someuserid:somepass@10.1.1.1:8080/some_path/some_path", False, False, True),

    (u"https://www.myDOMAIN.co.uk/THIS_IS_IN_UPPER", False, False, True),
    (u"https://LOCALHOST", False, False, True),
    (u"http://localHOST", False, False, True),
    (u"http://LOCALHOST/test_is_lowercase", False, False, True),
    (u"http://LocalHost/test_is_MIXED", False, False, True),

    (u"invalid-url", True, False, True),

    # Issue #59
    (u"http://www.foo.bar]", True, False, False),
    (u"http://www.foo.bar]]]]", True, False, False),
    (u"http://www.test.com]", True, False, True),
    (u"http://www.test.com]]]]]", True, False, True),
    (u"https://www.foo.bar[]]", True, False, False),
    (u"https://www.test.com]", True, False, False),
    (u"https://www.test.com]", True, False, True),

    # Issue #64
    (u"HTTP://www.foo.com", False, False, False),
    (u"http://www.foo.com", False, False, False),
    (u"HTTPS://www.foo.com", False, False, False),
    (u"httPS://www.foo.com", False, False, False),
    (u"FTP://www.foo.com", False, False, False),
    (u"FtP://www.foo.com", False, False, False),


])
def test_url(value, fails, allow_empty, allow_special_ips):
    """Test the URL validator."""
    if not fails:
        validated = validators.url(value,
                                   allow_empty = allow_empty,
                                   allow_special_ips = allow_special_ips)
        if value:
            assert isinstance(validated, basestring)
        else:
            assert validated is None
    else:
        with pytest.raises((ValueError, TypeError)):
            value = validators.url(value, allow_empty = allow_empty)


@pytest.mark.parametrize('value, fails, allow_empty, allow_ips', [
    (u"foo.com", False, False, False),
    (u"www.example.com", False, False, False),
    (u"✪df.ws", False, False, False),
    (u"142.42.1.1", False, False, False),
    (u"➡.ws", False, False, False),
    (u"⌘.ws", False, False, False),
    (u"☺.damowmow.com", False, False, False),
    (u"j.mp", False, False, False),
    (u"مثال.إختبار", False, False, False),
    (u"例子.测试", False, False, False),
    (u"उदाहरण.परीक्षा", False, False, False),
    (u"1337.net", False, False, False),
    (u"a.b-c.de", False, False, False),
    (u"a.b--c.de", False, False, False),
    (u"a.b--c.de/", True, False, False),
    (u"223.255.255.254", False, False, False),
    (u" shouldfail.com", False, False, False),
    (u"jurnalsda_pusair.pu.go.id", False, False, False),

    (u"-example.com", True, False, False),
    (u"127.0.0.1", True, False, False),
    (u"foo.com/blah_blah", True, False, False),
    (u"foo.com/blah_blah/", True, False, False),
    (u"www.example.com/wpstyle/?p=364", True, False, False),
    (u"✪df.ws/123", True, False, False),
    (u"userid:password@example.com:8080", True, False, False),
    (u"userid@example.com", True, False, False),
    (u"userid:password@example.com", True, False, False),
    (u"142.42.1.1/", True, False, False),
    (u"142.42.1.1:8080/", True, False, False),
    (u"➡.ws/䨹", True, False, False),
    (u"⌘.ws/", True, False, False),
    (u"code.google.com/events/#&product=browser", True, False, False),
    (u"-.~_!$&'()*+,;=:%40:80%2f::::::@example.com", True, False, False),
    (u"", True, False, False),
    (None, True, False, False),
    (u"", True, False, False),
    (u".", True, False, False),
    (u"..", True, False, False),
    (u"../", True, False, False),
    (u"?", True, False, False),
    (u"??", True, False, False),
    (u"??/", True, False, False),
    (u"#", True, False, False),
    (u"##", True, False, False),
    (u"##/", True, False, False),
    (u"foo.bar?q=Spaces should be encoded", True, False, False),
    (u"//", True, False, False),
    (u"//a", True, False, False),
    (u"///a", True, False, False),
    (u"///", True, False, False),
    (u"/a", True, False, False),
    (u"rdar://1234", True, False, False),
    (u"h://test", True, False, False),
    (u":// should fail", True, False, False),
    (u"foo.bar/foo(bar)baz quux", True, False, False),
    (u"foo.bar/", True, False, False),
    (u"-error-.invalid/", True, False, False),
    (u"-a.b.co", True, False, False),
    (u"a.b-.co", True, False, False),
    (u"0.0.0.0", True, False, False),
    (u"10.1.1.0", True, False, False),
    (u"10.1.1.255", True, False, False),
    (u"224.1.1.1", True, False, False),
    (u"1.1.1.1.1", True, False, False),
    (u"123.123.123", True, False, False),
    (u"3628126748", True, False, False),
    (u".www.foo.bar/", True, False, False),
    (u"www.foo.bar./", True, False, False),
    (u".www.foo.bar./", True, False, False),
    (u"10.1.1.1", True, False, False),

    (u"10.1.1.0", False, False, True),
    (u"10.1.1.255", False, False, True),
    (u"224.1.1.1", False, False, True),
    (u"1.1.1.1.1", True, False, True),
    (u"123.123.123", True, False, True),
    (u"10.1.1.1", False, False, True),

    (u"localhost", False, False, False),
    (u"abc.localhost.com", False, False, False),
    (u"invalid", False, False, False),
    (u"abc.invalid.com", False, False, False),

    # Issue 59
    (u"www.foo.bar]", True, False, False),
    (u"www.foo.bar]]]]", True, False, False),
    (u"www.foo.bar[]]", True, False, False),
    (u"www.test.com]", True, False, False),
    (u"www.test.com]", True, False, True),
])
def test_domain(value, fails, allow_empty, allow_ips):
    """Test the domain validator."""
    if not fails:
        validated = validators.domain(value,
                                      allow_empty = allow_empty,
                                      allow_ips = allow_ips)
        if value:
            assert isinstance(validated, basestring)
        else:
            assert validated is None
    else:
        with pytest.raises((ValueError, TypeError)):
            value = validators.domain(value,
                                      allow_empty = allow_empty,
                                      allow_ips = allow_ips)


@pytest.mark.parametrize('value, fails, allow_empty', [
    ('test@domain.dev', False, False),
    ('@domain.dev', True, False),
    ('domain.dev', True, False),
    ('not-an-email', True, False),
    ('', True, False),
    ('', False, True),
    (None, True, False),
    (None, False, True),

    ('email@example.com', False, False),
    ('firstname.lastname@example.com', False, False),
    ('email@subdomain.example.com', False, False),
    ('firstname+lastname@example.com', False, False),
    ('email@123.123.123.123', False, False),
    ('email@[123.123.123.123]', False, False),
    ('"email"@example.com', False, False),
    ('1234567890@example.com', False, False),
    ('email@example-one.com', False, False),
    ('_______@example.com', False, False),
    ('email@example.name', False, False),
    ('email@example.museum', False, False),
    ('email@example.co.jp', False, False),
    ('firstname-lastname@example.com', False, False),
    ('email@example.web', False, False),
    ('email+tag@example.com', False, False),
    ('test(comment)@test.com', False, False),

    ('much."more\\ unusual"@example.com', False, False),
    ('very.unusual."@".unusual.com@example.com', False, False),
    ('very."(),:;<>[]".VERY."very@\\ "very".unusual@strange.example.com', False, False),
    ('Joe.Smith."<".email.">".test@example.com', False, False),

    ('plainaddress', True, False),
    ('#@%^%#$@#$@#.com', True, False),
    ('@example.com', True, False),
    ('Joe Smith <email@example.com>', True, False),
    ('Joe Smith <email@example.com', True, False),
    ('Joe Smith email@example.com>', True, False),
    ('email.example.com', True, False),
    ('email@example@example.com', True, False),
    ('.email@example.com', True, False),
    ('email.@example.com', True, False),
    ('email..email@example.com', True, False),
    ('あいうえお@example.com', True, False),
    ('email@example.com (Joe Smith)', True, False),
    ('email@example', True, False),
    ('email@-example.com', True, False),
    ('email@111.222.333.44444', True, False),
    ('email@example..com', True, False),
    ('Abc..123@example.com', True, False),
    ('test(bad-comment@test.com', True, False),
    ('testbad-comment)goeshere@test.com', True, False),

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
    ('10.1.1.1', False, False),
    (u"127.0.0.1", False, False),
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
        with pytest.raises((ValueError, TypeError)):
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
        with pytest.raises((ValueError, TypeError)):
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
        with pytest.raises((ValueError, TypeError)):
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
        with pytest.raises((ValueError, TypeError)):
            validated = validators.mac_address(value, allow_empty = allow_empty)


@pytest.mark.parametrize('value, fails, allow_empty', [
    ('application/vnd.hzn-3d-crossword', False, False),
    ('video/3gpp', False, False),
    ('video/3gpp2', False, False),
    ('application/vnd.mseq', False, False),
    ('application/vnd.3m.post-it-notes', False, False),
    ('application/vnd.3gpp.pic-bw-large', False, False),
    ('application/vnd.3gpp.pic-bw-small', False, False),
    ('application/vnd.3gpp.pic-bw-var', False, False),
    ('application/vnd.3gpp2.tcap', False, False),
    ('application/x-7z-compressed', False, False),
    ('application/x-abiword', False, False),
    ('application/x-ace-compressed', False, False),
    ('application/vnd.americandynamics.acc', False, False),
    ('application/vnd.acucobol', False, False),
    ('application/vnd.acucorp', False, False),
    ('audio/adpcm', False, False),
    ('application/x-authorware-bin', False, False),
    ('application/x-authorware-map', False, False),
    ('application/x-authorware-seg', False, False),
    ('application/x-shockwave-flash', False, False),
    ('application/vnd.adobe.fxp', False, False),
    ('application/pdf', False, False),
    ('application/vnd.cups-ppd', False, False),
    ('application/x-director', False, False),
    ('application/vnd.adobe.xfdf', False, False),
    ('audio/x-aac', False, False),
    ('application/vnd.ahead.space', False, False),
    ('application/vnd.airzip.filesecure.azf', False, False),
    ('application/vnd.airzip.filesecure.azs', False, False),
    ('application/vnd.amazon.ebook', False, False),
    ('application/vnd.amiga.ami', False, False),
    ('application/andrew-inset', False, False),
    ('application/vnd.android.package-archive', False, False),
    ('application/vnd.anser-web-certificate-issue-initiation', False, False),
    ('application/vnd.anser-web-funds-transfer-initiation', False, False),
    ('application/vnd.antix.game-component', False, False),
    ('application/x-apple-diskimage', False, False),
    ('application/vnd.apple.installer+xml', False, False),
    ('application/applixware', False, False),
    ('application/vnd.hhe.lesson-player', False, False),
    ('application/vnd.aristanetworks.swi', False, False),
    ('text/x-asm', False, False),
    ('application/atomcat+xml', False, False),
    ('application/atomsvc+xml', False, False),
    ('application/atom+xml', False, False),
    ('application/pkix-attr-cert', False, False),
    ('audio/x-aiff', False, False),
    ('video/x-msvideo', False, False),
    ('application/vnd.audiograph', False, False),
    ('image/vnd.dxf', False, False),
    ('model/vnd.dwf', False, False),
    ('text/plain-bas', False, False),
    ('application/x-bcpio', False, False),
    ('application/octet-stream', False, False),
    ('image/bmp', False, False),
    ('application/x-bittorrent', False, False),
    ('application/vnd.rim.cod', False, False),
    ('application/vnd.blueice.multipass', False, False),
    ('application/vnd.bmi', False, False),
    ('application/x-sh', False, False),
    ('image/prs.btif', False, False),
    ('application/vnd.businessobjects', False, False),
    ('application/x-bzip', False, False),
    ('application/x-bzip2', False, False),
    ('application/x-csh', False, False),
    ('text/x-c', False, False),
    ('application/vnd.chemdraw+xml', False, False),
    ('text/css', False, False),
    ('chemical/x-cdx', False, False),
    ('chemical/x-cml', False, False),
    ('chemical/x-csml', False, False),
    ('application/vnd.contact.cmsg', False, False),
    ('application/vnd.claymore', False, False),
    ('application/vnd.clonk.c4group', False, False),
    ('image/vnd.dvb.subtitle', False, False),
    ('application/cdmi-capability', False, False),
    ('application/cdmi-container', False, False),
    ('application/cdmi-domain', False, False),
    ('application/cdmi-object', False, False),
    ('application/cdmi-queue', False, False),
    ('application/vnd.cluetrust.cartomobile-config', False, False),
    ('application/vnd.cluetrust.cartomobile-config-pkg', False, False),
    ('image/x-cmu-raster', False, False),
    ('model/vnd.collada+xml', False, False),
    ('text/csv', False, False),
    ('application/mac-compactpro', False, False),
    ('application/vnd.wap.wmlc', False, False),
    ('image/cgm', False, False),
    ('x-conference/x-cooltalk', False, False),
    ('image/x-cmx', False, False),
    ('application/vnd.xara', False, False),
    ('application/vnd.cosmocaller', False, False),
    ('application/x-cpio', False, False),
    ('application/vnd.crick.clicker', False, False),
    ('application/vnd.crick.clicker.keyboard', False, False),
    ('application/vnd.crick.clicker.palette', False, False),
    ('application/vnd.crick.clicker.template', False, False),
    ('application/vnd.crick.clicker.wordbank', False, False),
    ('application/vnd.criticaltools.wbs+xml', False, False),
    ('application/vnd.rig.cryptonote', False, False),
    ('chemical/x-cif', False, False),
    ('chemical/x-cmdf', False, False),
    ('application/cu-seeme', False, False),
    ('application/prs.cww', False, False),
    ('text/vnd.curl', False, False),
    ('text/vnd.curl.dcurl', False, False),
    ('text/vnd.curl.mcurl', False, False),
    ('text/vnd.curl.scurl', False, False),
    ('application/vnd.curl.car', False, False),
    ('application/vnd.curl.pcurl', False, False),
    ('application/vnd.yellowriver-custom-menu', False, False),
    ('application/dssc+der', False, False),
    ('application/dssc+xml', False, False),
    ('application/x-debian-package', False, False),
    ('audio/vnd.dece.audio', False, False),
    ('image/vnd.dece.graphic', False, False),
    ('video/vnd.dece.hd', False, False),
    ('video/vnd.dece.mobile', False, False),
    ('video/vnd.uvvu.mp4', False, False),
    ('video/vnd.dece.pd', False, False),
    ('video/vnd.dece.sd', False, False),
    ('video/vnd.dece.video', False, False),
    ('application/x-dvi', False, False),
    ('application/vnd.fdsn.seed', False, False),
    ('application/x-dtbook+xml', False, False),
    ('application/x-dtbresource+xml', False, False),
    ('application/vnd.dvb.ait', False, False),
    ('application/vnd.dvb.service', False, False),
    ('audio/vnd.digital-winds', False, False),
    ('image/vnd.djvu', False, False),
    ('application/xml-dtd', False, False),
    ('application/vnd.dolby.mlp', False, False),
    ('application/x-doom', False, False),
    ('application/vnd.dpgraph', False, False),
    ('audio/vnd.dra', False, False),
    ('application/vnd.dreamfactory', False, False),
    ('audio/vnd.dts', False, False),
    ('audio/vnd.dts.hd', False, False),
    ('image/vnd.dwg', False, False),
    ('application/vnd.dynageo', False, False),
    ('application/ecmascript', False, False),
    ('application/vnd.ecowin.chart', False, False),
    ('image/vnd.fujixerox.edmics-mmr', False, False),
    ('image/vnd.fujixerox.edmics-rlc', False, False),
    ('application/exi', False, False),
    ('application/vnd.proteus.magazine', False, False),
    ('application/epub+zip', False, False),
    ('message/rfc822', False, False),
    ('application/vnd.enliven', False, False),
    ('application/vnd.is-xpr', False, False),
    ('image/vnd.xiff', False, False),
    ('application/vnd.xfdl', False, False),
    ('application/emma+xml', False, False),
    ('application/vnd.ezpix-album', False, False),
    ('application/vnd.ezpix-package', False, False),
    ('image/vnd.fst', False, False),
    ('video/vnd.fvt', False, False),
    ('image/vnd.fastbidsheet', False, False),
    ('application/vnd.denovo.fcselayout-link', False, False),
    ('video/x-f4v', False, False),
    ('video/x-flv', False, False),
    ('image/vnd.fpx', False, False),
    ('image/vnd.net-fpx', False, False),
    ('text/vnd.fmi.flexstor', False, False),
    ('video/x-fli', False, False),
    ('application/vnd.fluxtime.clip', False, False),
    ('application/vnd.fdf', False, False),
    ('text/x-fortran', False, False),
    ('application/vnd.mif', False, False),
    ('application/vnd.framemaker', False, False),
    ('image/x-freehand', False, False),
    ('application/vnd.fsc.weblaunch', False, False),
    ('application/vnd.frogans.fnc', False, False),
    ('application/vnd.frogans.ltf', False, False),
    ('application/vnd.fujixerox.ddd', False, False),
    ('application/vnd.fujixerox.docuworks', False, False),
    ('application/vnd.fujixerox.docuworks.binder', False, False),
    ('application/vnd.fujitsu.oasys', False, False),
    ('application/vnd.fujitsu.oasys2', False, False),
    ('application/vnd.fujitsu.oasys3', False, False),
    ('application/vnd.fujitsu.oasysgp', False, False),
    ('application/vnd.fujitsu.oasysprs', False, False),
    ('application/x-futuresplash', False, False),
    ('application/vnd.fuzzysheet', False, False),
    ('image/g3fax', False, False),
    ('application/vnd.gmx', False, False),
    ('model/vnd.gtw', False, False),
    ('application/vnd.genomatix.tuxedo', False, False),
    ('application/vnd.geogebra.file', False, False),
    ('application/vnd.geogebra.tool', False, False),
    ('model/vnd.gdl', False, False),
    ('application/vnd.geometry-explorer', False, False),
    ('application/vnd.geonext', False, False),
    ('application/vnd.geoplan', False, False),
    ('application/vnd.geospace', False, False),
    ('application/x-font-ghostscript', False, False),
    ('application/x-font-bdf', False, False),
    ('application/x-gtar', False, False),
    ('application/x-texinfo', False, False),
    ('application/x-gnumeric', False, False),
    ('application/vnd.google-earth.kml+xml', False, False),
    ('application/vnd.google-earth.kmz', False, False),
    ('application/vnd.grafeq', False, False),
    ('image/gif', False, False),
    ('text/vnd.graphviz', False, False),
    ('application/vnd.groove-account', False, False),
    ('application/vnd.groove-help', False, False),
    ('application/vnd.groove-identity-message', False, False),
    ('application/vnd.groove-injector', False, False),
    ('application/vnd.groove-tool-message', False, False),
    ('application/vnd.groove-tool-template', False, False),
    ('application/vnd.groove-vcard', False, False),
    ('video/h261', False, False),
    ('video/h263', False, False),
    ('video/h264', False, False),
    ('application/vnd.hp-hpid', False, False),
    ('application/vnd.hp-hps', False, False),
    ('application/x-hdf', False, False),
    ('audio/vnd.rip', False, False),
    ('application/vnd.hbci', False, False),
    ('application/vnd.hp-jlyt', False, False),
    ('application/vnd.hp-pcl', False, False),
    ('application/vnd.hp-hpgl', False, False),
    ('application/vnd.yamaha.hv-script', False, False),
    ('application/vnd.yamaha.hv-dic', False, False),
    ('application/vnd.yamaha.hv-voice', False, False),
    ('application/vnd.hydrostatix.sof-data', False, False),
    ('application/hyperstudio', False, False),
    ('application/vnd.hal+xml', False, False),
    ('text/html', False, False),
    ('application/vnd.ibm.rights-management', False, False),
    ('application/vnd.ibm.secure-container', False, False),
    ('text/calendar', False, False),
    ('application/vnd.iccprofile', False, False),
    ('image/x-icon', False, False),
    ('application/vnd.igloader', False, False),
    ('image/ief', False, False),
    ('application/vnd.immervision-ivp', False, False),
    ('application/vnd.immervision-ivu', False, False),
    ('application/reginfo+xml', False, False),
    ('text/vnd.in3d.3dml', False, False),
    ('text/vnd.in3d.spot', False, False),
    ('model/iges', False, False),
    ('application/vnd.intergeo', False, False),
    ('application/vnd.cinderella', False, False),
    ('application/vnd.intercon.formnet', False, False),
    ('application/vnd.isac.fcs', False, False),
    ('application/ipfix', False, False),
    ('application/pkix-cert', False, False),
    ('application/pkixcmp', False, False),
    ('application/pkix-crl', False, False),
    ('application/pkix-pkipath', False, False),
    ('application/vnd.insors.igm', False, False),
    ('application/vnd.ipunplugged.rcprofile', False, False),
    ('application/vnd.irepository.package+xml', False, False),
    ('text/vnd.sun.j2me.app-descriptor', False, False),
    ('application/java-archive', False, False),
    ('application/java-vm', False, False),
    ('application/x-java-jnlp-file', False, False),
    ('application/java-serialized-object', False, False),
    ('text/x-java-source,java', True, False),
    ('application/javascript', False, False),
    ('application/json', False, False),
    ('application/vnd.joost.joda-archive', False, False),
    ('video/jpm', False, False),
    ('image/jpeg', False, False),
    ('image/x-citrix-jpeg', False, False),
    ('image/pjpeg', False, False),
    ('video/jpeg', False, False),
    ('application/vnd.kahootz', False, False),
    ('application/vnd.chipnuts.karaoke-mmd', False, False),
    ('application/vnd.kde.karbon', False, False),
    ('application/vnd.kde.kchart', False, False),
    ('application/vnd.kde.kformula', False, False),
    ('application/vnd.kde.kivio', False, False),
    ('application/vnd.kde.kontour', False, False),
    ('application/vnd.kde.kpresenter', False, False),
    ('application/vnd.kde.kspread', False, False),
    ('application/vnd.kde.kword', False, False),
    ('application/vnd.kenameaapp', False, False),
    ('application/vnd.kidspiration', False, False),
    ('application/vnd.kinar', False, False),
    ('application/vnd.kodak-descriptor', False, False),
    ('application/vnd.las.las+xml', False, False),
    ('application/x-latex', False, False),
    ('application/vnd.llamagraphics.life-balance.desktop', False, False),
    ('application/vnd.llamagraphics.life-balance.exchange+xml', False, False),
    ('application/vnd.jam', False, False),
    ('application/vnd.lotus-1-2-3', False, False),
    ('application/vnd.lotus-approach', False, False),
    ('application/vnd.lotus-freelance', False, False),
    ('application/vnd.lotus-notes', False, False),
    ('application/vnd.lotus-organizer', False, False),
    ('application/vnd.lotus-screencam', False, False),
    ('application/vnd.lotus-wordpro', False, False),
    ('audio/vnd.lucent.voice', False, False),
    ('audio/x-mpegurl', False, False),
    ('video/x-m4v', False, False),
    ('application/mac-binhex40', False, False),
    ('application/vnd.macports.portpkg', False, False),
    ('application/vnd.osgeo.mapguide.package', False, False),
    ('application/marc', False, False),
    ('application/marcxml+xml', False, False),
    ('application/mxf', False, False),
    ('application/vnd.wolfram.player', False, False),
    ('application/mathematica', False, False),
    ('application/mathml+xml', False, False),
    ('application/mbox', False, False),
    ('application/vnd.medcalcdata', False, False),
    ('application/mediaservercontrol+xml', False, False),
    ('application/vnd.mediastation.cdkey', False, False),
    ('application/vnd.mfer', False, False),
    ('application/vnd.mfmp', False, False),
    ('model/mesh', False, False),
    ('application/mads+xml', False, False),
    ('application/mets+xml', False, False),
    ('application/mods+xml', False, False),
    ('application/metalink4+xml', False, False),
    ('application/vnd.mcd', False, False),
    ('application/vnd.micrografx.flo', False, False),
    ('application/vnd.micrografx.igx', False, False),
    ('application/vnd.eszigno3+xml', False, False),
    ('application/x-msaccess', False, False),
    ('video/x-ms-asf', False, False),
    ('application/x-msdownload', False, False),
    ('application/vnd.ms-artgalry', False, False),
    ('application/vnd.ms-cab-compressed', False, False),
    ('application/vnd.ms-ims', False, False),
    ('application/x-ms-application', False, False),
    ('application/x-msclip', False, False),
    ('image/vnd.ms-modi', False, False),
    ('application/vnd.ms-fontobject', False, False),
    ('application/vnd.ms-excel', False, False),
    ('application/vnd.ms-excel.addin.macroenabled.12', False, False),
    ('application/vnd.ms-excel.sheet.binary.macroenabled.12', False, False),
    ('application/vnd.ms-excel.template.macroenabled.12', False, False),
    ('application/vnd.ms-excel.sheet.macroenabled.12', False, False),
    ('application/vnd.ms-htmlhelp', False, False),
    ('application/x-mscardfile', False, False),
    ('application/vnd.ms-lrm', False, False),
    ('application/x-msmediaview', False, False),
    ('application/x-msmoney', False, False),
    ('application/vnd.openxmlformats-officedocument.presentationml.presentation', False, False),
    ('application/vnd.openxmlformats-officedocument.presentationml.slide', False, False),
    ('application/vnd.openxmlformats-officedocument.presentationml.slideshow', False, False),
    ('application/vnd.openxmlformats-officedocument.presentationml.template', False, False),
    ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', False, False),
    ('application/vnd.openxmlformats-officedocument.spreadsheetml.template', False, False),
    ('application/vnd.openxmlformats-officedocument.wordprocessingml.document', False, False),
    ('application/vnd.openxmlformats-officedocument.wordprocessingml.template', False, False),
    ('application/x-msbinder', False, False),
    ('application/vnd.ms-officetheme', False, False),
    ('application/onenote', False, False),
    ('audio/vnd.ms-playready.media.pya', False, False),
    ('video/vnd.ms-playready.media.pyv', False, False),
    ('application/vnd.ms-powerpoint', False, False),
    ('application/vnd.ms-powerpoint.addin.macroenabled.12', False, False),
    ('application/vnd.ms-powerpoint.slide.macroenabled.12', False, False),
    ('application/vnd.ms-powerpoint.presentation.macroenabled.12', False, False),
    ('application/vnd.ms-powerpoint.slideshow.macroenabled.12', False, False),
    ('application/vnd.ms-powerpoint.template.macroenabled.12', False, False),
    ('application/vnd.ms-project', False, False),
    ('application/x-mspublisher', False, False),
    ('application/x-msschedule', False, False),
    ('application/x-silverlight-app', False, False),
    ('application/vnd.ms-pki.stl', False, False),
    ('application/vnd.ms-pki.seccat', False, False),
    ('application/vnd.visio', False, False),
    ('application/vnd.visio2013', False, False),
    ('video/x-ms-wm', False, False),
    ('audio/x-ms-wma', False, False),
    ('audio/x-ms-wax', False, False),
    ('video/x-ms-wmx', False, False),
    ('application/x-ms-wmd', False, False),
    ('application/vnd.ms-wpl', False, False),
    ('application/x-ms-wmz', False, False),
    ('video/x-ms-wmv', False, False),
    ('video/x-ms-wvx', False, False),
    ('application/x-msmetafile', False, False),
    ('application/x-msterminal', False, False),
    ('application/msword', False, False),
    ('application/vnd.ms-word.document.macroenabled.12', False, False),
    ('application/vnd.ms-word.template.macroenabled.12', False, False),
    ('application/x-mswrite', False, False),
    ('application/vnd.ms-works', False, False),
    ('application/x-ms-xbap', False, False),
    ('application/vnd.ms-xpsdocument', False, False),
    ('audio/midi', False, False),
    ('application/vnd.ibm.minipay', False, False),
    ('application/vnd.ibm.modcap', False, False),
    ('application/vnd.jcp.javame.midlet-rms', False, False),
    ('application/vnd.tmobile-livetv', False, False),
    ('application/x-mobipocket-ebook', False, False),
    ('application/vnd.mobius.mbk', False, False),
    ('application/vnd.mobius.dis', False, False),
    ('application/vnd.mobius.plc', False, False),
    ('application/vnd.mobius.mqy', False, False),
    ('application/vnd.mobius.msl', False, False),
    ('application/vnd.mobius.txf', False, False),
    ('application/vnd.mobius.daf', False, False),
    ('text/vnd.fly', False, False),
    ('application/vnd.mophun.certificate', False, False),
    ('application/vnd.mophun.application', False, False),
    ('video/mj2', False, False),
    ('audio/mpeg', False, False),
    ('video/vnd.mpegurl', False, False),
    ('video/mpeg', False, False),
    ('application/mp21', False, False),
    ('audio/mp4', False, False),
    ('video/mp4', False, False),
    ('application/mp4', False, False),
    ('application/vnd.apple.mpegurl', False, False),
    ('application/vnd.musician', False, False),
    ('application/vnd.muvee.style', False, False),
    ('application/xv+xml', False, False),
    ('application/vnd.nokia.n-gage.data', False, False),
    ('application/vnd.nokia.n-gage.symbian.install', False, False),
    ('application/x-dtbncx+xml', False, False),
    ('application/x-netcdf', False, False),
    ('application/vnd.neurolanguage.nlu', False, False),
    ('application/vnd.dna', False, False),
    ('application/vnd.noblenet-directory', False, False),
    ('application/vnd.noblenet-sealer', False, False),
    ('application/vnd.noblenet-web', False, False),
    ('application/vnd.nokia.radio-preset', False, False),
    ('application/vnd.nokia.radio-presets', False, False),
    ('text/n3', False, False),
    ('application/vnd.novadigm.edm', False, False),
    ('application/vnd.novadigm.edx', False, False),
    ('application/vnd.novadigm.ext', False, False),
    ('application/vnd.flographit', False, False),
    ('audio/vnd.nuera.ecelp4800', False, False),
    ('audio/vnd.nuera.ecelp7470', False, False),
    ('audio/vnd.nuera.ecelp9600', False, False),
    ('application/oda', False, False),
    ('application/ogg', False, False),
    ('audio/ogg', False, False),
    ('video/ogg', False, False),
    ('application/vnd.oma.dd2+xml', False, False),
    ('application/vnd.oasis.opendocument.text-web', False, False),
    ('application/oebps-package+xml', False, False),
    ('application/vnd.intu.qbo', False, False),
    ('application/vnd.openofficeorg.extension', False, False),
    ('application/vnd.yamaha.openscoreformat', False, False),
    ('audio/webm', False, False),
    ('video/webm', False, False),
    ('application/vnd.oasis.opendocument.chart', False, False),
    ('application/vnd.oasis.opendocument.chart-template', False, False),
    ('application/vnd.oasis.opendocument.database', False, False),
    ('application/vnd.oasis.opendocument.formula', False, False),
    ('application/vnd.oasis.opendocument.formula-template', False, False),
    ('application/vnd.oasis.opendocument.graphics', False, False),
    ('application/vnd.oasis.opendocument.graphics-template', False, False),
    ('application/vnd.oasis.opendocument.image', False, False),
    ('application/vnd.oasis.opendocument.image-template', False, False),
    ('application/vnd.oasis.opendocument.presentation', False, False),
    ('application/vnd.oasis.opendocument.presentation-template', False, False),
    ('application/vnd.oasis.opendocument.spreadsheet', False, False),
    ('application/vnd.oasis.opendocument.spreadsheet-template', False, False),
    ('application/vnd.oasis.opendocument.text', False, False),
    ('application/vnd.oasis.opendocument.text-master', False, False),
    ('application/vnd.oasis.opendocument.text-template', False, False),
    ('image/ktx', False, False),
    ('application/vnd.sun.xml.calc', False, False),
    ('application/vnd.sun.xml.calc.template', False, False),
    ('application/vnd.sun.xml.draw', False, False),
    ('application/vnd.sun.xml.draw.template', False, False),
    ('application/vnd.sun.xml.impress', False, False),
    ('application/vnd.sun.xml.impress.template', False, False),
    ('application/vnd.sun.xml.math', False, False),
    ('application/vnd.sun.xml.writer', False, False),
    ('application/vnd.sun.xml.writer.global', False, False),
    ('application/vnd.sun.xml.writer.template', False, False),
    ('application/x-font-otf', False, False),
    ('application/vnd.yamaha.openscoreformat.osfpvg+xml', False, False),
    ('application/vnd.osgi.dp', False, False),
    ('application/vnd.palm', False, False),
    ('text/x-pascal', False, False),
    ('application/vnd.pawaafile', False, False),
    ('application/vnd.hp-pclxl', False, False),
    ('application/vnd.picsel', False, False),
    ('image/x-pcx', False, False),
    ('image/vnd.adobe.photoshop', False, False),
    ('application/pics-rules', False, False),
    ('image/x-pict', False, False),
    ('application/x-chat', False, False),
    ('application/pkcs10', False, False),
    ('application/x-pkcs12', False, False),
    ('application/pkcs7-mime', False, False),
    ('application/pkcs7-signature', False, False),
    ('application/x-pkcs7-certreqresp', False, False),
    ('application/x-pkcs7-certificates', False, False),
    ('application/pkcs8', False, False),
    ('application/vnd.pocketlearn', False, False),
    ('image/x-portable-anymap', False, False),
    ('image/x-portable-bitmap', False, False),
    ('application/x-font-pcf', False, False),
    ('application/font-tdpfr', False, False),
    ('application/x-chess-pgn', False, False),
    ('image/x-portable-graymap', False, False),
    ('image/png', False, False),
    ('image/x-citrix-png', False, False),
    ('image/x-png', False, False),
    ('image/x-portable-pixmap', False, False),
    ('application/pskc+xml', False, False),
    ('application/vnd.ctc-posml', False, False),
    ('application/postscript', False, False),
    ('application/x-font-type1', False, False),
    ('application/vnd.powerbuilder6', False, False),
    ('application/pgp-encrypted', False, False),
    ('application/pgp-signature', False, False),
    ('application/vnd.previewsystems.box', False, False),
    ('application/vnd.pvi.ptid1', False, False),
    ('application/pls+xml', False, False),
    ('application/vnd.pg.format', False, False),
    ('application/vnd.pg.osasli', False, False),
    ('text/prs.lines.tag', False, False),
    ('application/x-font-linux-psf', False, False),
    ('application/vnd.publishare-delta-tree', False, False),
    ('application/vnd.pmi.widget', False, False),
    ('application/vnd.quark.quarkxpress', False, False),
    ('application/vnd.epson.esf', False, False),
    ('application/vnd.epson.msf', False, False),
    ('application/vnd.epson.ssf', False, False),
    ('application/vnd.epson.quickanime', False, False),
    ('application/vnd.intu.qfx', False, False),
    ('video/quicktime', False, False),
    ('application/x-rar-compressed', False, False),
    ('audio/x-pn-realaudio', False, False),
    ('audio/x-pn-realaudio-plugin', False, False),
    ('application/rsd+xml', False, False),
    ('application/vnd.rn-realmedia', False, False),
    ('application/vnd.realvnc.bed', False, False),
    ('application/vnd.recordare.musicxml', False, False),
    ('application/vnd.recordare.musicxml+xml', False, False),
    ('application/relax-ng-compact-syntax', False, False),
    ('application/vnd.data-vision.rdz', False, False),
    ('application/rdf+xml', False, False),
    ('application/vnd.cloanto.rp9', False, False),
    ('application/vnd.jisp', False, False),
    ('application/rtf', False, False),
    ('text/richtext', False, False),
    ('application/vnd.route66.link66+xml', False, False),
    ('application/rss+xml', False, False),
    ('application/shf+xml', False, False),
    ('application/vnd.sailingtracker.track', False, False),
    ('image/svg+xml', False, False),
    ('application/vnd.sus-calendar', False, False),
    ('application/sru+xml', False, False),
    ('application/set-payment-initiation', False, False),
    ('application/set-registration-initiation', False, False),
    ('application/vnd.sema', False, False),
    ('application/vnd.semd', False, False),
    ('application/vnd.semf', False, False),
    ('application/vnd.seemail', False, False),
    ('application/x-font-snf', False, False),
    ('application/scvp-vp-request', False, False),
    ('application/scvp-vp-response', False, False),
    ('application/scvp-cv-request', False, False),
    ('application/scvp-cv-response', False, False),
    ('application/sdp', False, False),
    ('text/x-setext', False, False),
    ('video/x-sgi-movie', False, False),
    ('application/vnd.shana.informed.formdata', False, False),
    ('application/vnd.shana.informed.formtemplate', False, False),
    ('application/vnd.shana.informed.interchange', False, False),
    ('application/vnd.shana.informed.package', False, False),
    ('application/thraud+xml', False, False),
    ('application/x-shar', False, False),
    ('image/x-rgb', False, False),
    ('application/vnd.epson.salt', False, False),
    ('application/vnd.accpac.simply.aso', False, False),
    ('application/vnd.accpac.simply.imp', False, False),
    ('application/vnd.simtech-mindmapper', False, False),
    ('application/vnd.commonspace', False, False),
    ('application/vnd.yamaha.smaf-audio', False, False),
    ('application/vnd.smaf', False, False),
    ('application/vnd.yamaha.smaf-phrase', False, False),
    ('application/vnd.smart.teacher', False, False),
    ('application/vnd.svd', False, False),
    ('application/sparql-query', False, False),
    ('application/sparql-results+xml', False, False),
    ('application/srgs', False, False),
    ('application/srgs+xml', False, False),
    ('application/ssml+xml', False, False),
    ('application/vnd.koan', False, False),
    ('text/sgml', False, False),
    ('application/vnd.stardivision.calc', False, False),
    ('application/vnd.stardivision.draw', False, False),
    ('application/vnd.stardivision.impress', False, False),
    ('application/vnd.stardivision.math', False, False),
    ('application/vnd.stardivision.writer', False, False),
    ('application/vnd.stardivision.writer-global', False, False),
    ('application/vnd.stepmania.stepchart', False, False),
    ('application/x-stuffit', False, False),
    ('application/x-stuffitx', False, False),
    ('application/vnd.solent.sdkm+xml', False, False),
    ('application/vnd.olpc-sugar', False, False),
    ('audio/basic', False, False),
    ('application/vnd.wqd', False, False),
    ('application/vnd.symbian.install', False, False),
    ('application/smil+xml', False, False),
    ('application/vnd.syncml+xml', False, False),
    ('application/vnd.syncml.dm+wbxml', False, False),
    ('application/vnd.syncml.dm+xml', False, False),
    ('application/x-sv4cpio', False, False),
    ('application/x-sv4crc', False, False),
    ('application/sbml+xml', False, False),
    ('text/tab-separated-values', False, False),
    ('image/tiff', False, False),
    ('application/vnd.tao.intent-module-archive', False, False),
    ('application/x-tar', False, False),
    ('application/x-tcl', False, False),
    ('application/x-tex', False, False),
    ('application/x-tex-tfm', False, False),
    ('application/tei+xml', False, False),
    ('text/plain', False, False),
    ('application/vnd.spotfire.dxp', False, False),
    ('application/vnd.spotfire.sfs', False, False),
    ('application/timestamped-data', False, False),
    ('application/vnd.trid.tpt', False, False),
    ('application/vnd.triscape.mxs', False, False),
    ('text/troff', False, False),
    ('application/vnd.trueapp', False, False),
    ('application/x-font-ttf', False, False),
    ('text/turtle', False, False),
    ('application/vnd.umajin', False, False),
    ('application/vnd.uoml+xml', False, False),
    ('application/vnd.unity', False, False),
    ('application/vnd.ufdl', False, False),
    ('text/uri-list', False, False),
    ('application/vnd.uiq.theme', False, False),
    ('application/x-ustar', False, False),
    ('text/x-uuencode', False, False),
    ('text/x-vcalendar', False, False),
    ('text/x-vcard', False, False),
    ('application/x-cdlink', False, False),
    ('application/vnd.vsf', False, False),
    ('model/vrml', False, False),
    ('application/vnd.vcx', False, False),
    ('model/vnd.mts', False, False),
    ('model/vnd.vtu', False, False),
    ('application/vnd.visionary', False, False),
    ('video/vnd.vivo', False, False),
    ('application/ccxml+xml', False, False),
    ('application/voicexml+xml', False, False),
    ('application/x-wais-source', False, False),
    ('application/vnd.wap.wbxml', False, False),
    ('image/vnd.wap.wbmp', False, False),
    ('audio/x-wav', False, False),
    ('application/davmount+xml', False, False),
    ('application/x-font-woff', False, False),
    ('application/wspolicy+xml', False, False),
    ('image/webp', False, False),
    ('application/vnd.webturbo', False, False),
    ('application/widget', False, False),
    ('application/winhlp', False, False),
    ('text/vnd.wap.wml', False, False),
    ('text/vnd.wap.wmlscript', False, False),
    ('application/vnd.wap.wmlscriptc', False, False),
    ('application/vnd.wordperfect', False, False),
    ('application/vnd.wt.stf', False, False),
    ('application/wsdl+xml', False, False),
    ('image/x-xbitmap', False, False),
    ('image/x-xpixmap', False, False),
    ('image/x-xwindowdump', False, False),
    ('application/x-x509-ca-cert', False, False),
    ('application/x-xfig', False, False),
    ('application/xhtml+xml', False, False),
    ('application/xml', False, False),
    ('application/xcap-diff+xml', False, False),
    ('application/xenc+xml', False, False),
    ('application/patch-ops-error+xml', False, False),
    ('application/resource-lists+xml', False, False),
    ('application/rls-services+xml', False, False),
    ('application/resource-lists-diff+xml', False, False),
    ('application/xslt+xml', False, False),
    ('application/xop+xml', False, False),
    ('application/x-xpinstall', False, False),
    ('application/xspf+xml', False, False),
    ('application/vnd.mozilla.xul+xml', False, False),
    ('chemical/x-xyz', False, False),
    ('text/yaml', False, False),
    ('application/yang', False, False),
    ('application/yin+xml', False, False),
    ('application/vnd.zul', False, False),
    ('application/zip', False, False),
    ('application/vnd.handheld-entertainment+xml', False, False),
    ('application/vnd.zzazz.deck+xml', False, False),
    ('application/vnd.adobe.air-application-installer-package+zip', False, False),
    ('application/vnd.adobe.xdp+xml', False, False),
    ('multipart', False, False),
    ('application/x-www-form-urlencoded', False, False),

    ('invalid expression', True, False),
])
def test_mimetype(value, fails, allow_empty):
    if not fails:
        validated = validators.mimetype(value, allow_empty = allow_empty)
        if value:
            assert validated is not None
        else:
            assert validated is None
    else:
        with pytest.raises(ValueError):
            value = validators.mimetype(value, allow_empty = allow_empty)


@pytest.mark.parametrize('value, fails, allow_empty', [
    ("US-ASCII", False, False),
    ("ISO-8859-1", False, False),
    ("ISO-8859-2", False, False),
    ("ISO-8859-3", False, False),
    ("ISO-8859-4", False, False),
    ("ISO-8859-5", False, False),
    ("ISO-8859-6", False, False),
    ("ISO-8859-7", False, False),
    ("ISO-8859-8", False, False),
    ("ISO-8859-9", False, False),
    ("ISO-8859-10", False, False),
    ("ISO_6937-2-add", False, False),
    ("JIS_X0201", False, False),
    ("JIS_Encoding", False, False),
    ("Shift_JIS", False, False),
    ("EUC-JP", False, False),
    ("Extended_UNIX_Code_Fixed_Width_for_Japanese", False, False),
    ("BS_4730", False, False),
    ("SEN_850200_C", False, False),
    ("IT", False, False),
    ("ES", False, False),
    ("DIN_66003", False, False),
    ("NS_4551-1", False, False),
    ("NF_Z_62-010", False, False),
    ("ISO-10646-UTF-1", False, False),
    ("ISO_646.basic:1983", False, False),
    ("INVARIANT", False, False),
    ("ISO_646.irv:1983", False, False),
    ("NATS-SEFI", False, False),
    ("NATS-SEFI-ADD", False, False),
    ("NATS-DANO", False, False),
    ("NATS-DANO-ADD", False, False),
    ("SEN_850200_B", False, False),
    ("KS_C_5601-1987", False, False),
    ("ISO-2022-KR", False, False),
    ("EUC-KR", False, False),
    ("ISO-2022-JP", False, False),
    ("ISO-2022-JP-2", False, False),
    ("JIS_C6220-1969-jp", False, False),
    ("JIS_C6220-1969-ro", False, False),
    ("PT", False, False),
    ("greek7-old", False, False),
    ("latin-greek", False, False),
    ("NF_Z_62-010_(1973)", False, False),
    ("Latin-greek-1", False, False),
    ("ISO_5427", False, False),
    ("JIS_C6226-1978", False, False),
    ("BS_viewdata", False, False),
    ("INIS", False, False),
    ("INIS-8", False, False),
    ("INIS-cyrillic", False, False),
    ("ISO_5427:1981", False, False),
    ("ISO_5428:1980", False, False),
    ("GB_1988-80", False, False),
    ("GB_2312-80", False, False),
    ("NS_4551-2", False, False),
    ("videotex-suppl", False, False),
    ("PT2", False, False),
    ("ES2", False, False),
    ("MSZ_7795.3", False, False),
    ("JIS_C6226-1983", False, False),
    ("greek7", False, False),
    ("ASMO_449", False, False),
    ("iso-ir-90", False, False),
    ("JIS_C6229-1984-a", False, False),
    ("JIS_C6229-1984-b", False, False),
    ("JIS_C6229-1984-b-add", False, False),
    ("JIS_C6229-1984-hand", False, False),
    ("JIS_C6229-1984-hand-add", False, False),
    ("JIS_C6229-1984-kana", False, False),
    ("ISO_2033-1983", False, False),
    ("ANSI_X3.110-1983", False, False),
    ("T.61-7bit", False, False),
    ("T.61-8bit", False, False),
    ("ECMA-cyrillic", False, False),
    ("CSA_Z243.4-1985-1", False, False),
    ("CSA_Z243.4-1985-2", False, False),
    ("CSA_Z243.4-1985-gr", False, False),
    ("ISO-8859-6-E", False, False),
    ("ISO-8859-6-I", False, False),
    ("T.101-G2", False, False),
    ("ISO-8859-8-E", False, False),
    ("ISO-8859-8-I", False, False),
    ("CSN_369103", False, False),
    ("JUS_I.B1.002", False, False),
    ("IEC_P27-1", False, False),
    ("JUS_I.B1.003-serb", False, False),
    ("JUS_I.B1.003-mac", False, False),
    ("greek-ccitt", False, False),
    ("NC_NC00-10:81", False, False),
    ("ISO_6937-2-25", False, False),
    ("GOST_19768-74", False, False),
    ("ISO_8859-supp", False, False),
    ("ISO_10367-box", False, False),
    ("latin-lap", False, False),
    ("JIS_X0212-1990", False, False),
    ("DS_2089", False, False),
    ("us-dk", False, False),
    ("dk-us", False, False),
    ("KSC5636", False, False),
    ("UNICODE-1-1-UTF-7", False, False),
    ("ISO-2022-CN", False, False),
    ("ISO-2022-CN-EXT", False, False),
    ("UTF-8", False, False),
    ("ISO-8859-13", False, False),
    ("ISO-8859-14", False, False),
    ("ISO-8859-15", False, False),
    ("ISO-8859-16", False, False),
    ("GBK", False, False),
    ("GB18030", False, False),
    ("OSD_EBCDIC_DF04_15", False, False),
    ("OSD_EBCDIC_DF03_IRV", False, False),
    ("OSD_EBCDIC_DF04_1", False, False),
    ("ISO-11548-1", False, False),
    ("KZ-1048", False, False),
    ("ISO-10646-UCS-2", False, False),
    ("ISO-10646-UCS-4", False, False),
    ("ISO-10646-UCS-Basic", False, False),
    ("ISO-10646-Unicode-Latin1", False, False),
    ("ISO-10646-J-1", False, False),
    ("ISO-Unicode-IBM-1261", False, False),
    ("ISO-Unicode-IBM-1268", False, False),
    ("ISO-Unicode-IBM-1276", False, False),
    ("ISO-Unicode-IBM-1264", False, False),
    ("ISO-Unicode-IBM-1265", False, False),
    ("UNICODE-1-1", False, False),
    ("SCSU", False, False),
    ("UTF-7", False, False),
    ("UTF-16BE", False, False),
    ("UTF-16LE", False, False),
    ("UTF-16", False, False),
    ("CESU-8", False, False),
    ("UTF-32", False, False),
    ("UTF-32BE", False, False),
    ("UTF-32LE", False, False),
    ("BOCU-1", False, False),
    ("UTF-7-IMAP", False, False),
    ("ISO-8859-1-Windows-3.0-Latin-1", False, False),
    ("ISO-8859-1-Windows-3.1-Latin-1", False, False),
    ("ISO-8859-2-Windows-Latin-2", False, False),
    ("ISO-8859-9-Windows-Latin-5", False, False),
    ("hp-roman8", False, False),
    ("Adobe-Standard-Encoding", False, False),
    ("Ventura-US", False, False),
    ("Ventura-International", False, False),
    ("DEC-MCS", False, False),
    ("IBM850", False, False),
    ("PC8-Danish-Norwegian", False, False),
    ("IBM862", False, False),
    ("PC8-Turkish", False, False),
    ("IBM-Symbols", False, False),
    ("IBM-Thai", False, False),
    ("HP-Legal", False, False),
    ("HP-Pi-font", False, False),
    ("HP-Math8", False, False),
    ("Adobe-Symbol-Encoding", False, False),
    ("HP-DeskTop", False, False),
    ("Ventura-Math", False, False),
    ("Microsoft-Publishing", False, False),
    ("Windows-31J", False, False),
    ("GB2312", False, False),
    ("Big5", False, False),
    ("macintosh", False, False),
    ("IBM037", False, False),
    ("IBM038", False, False),
    ("IBM273", False, False),
    ("IBM274", False, False),
    ("IBM275", False, False),
    ("IBM277", False, False),
    ("IBM278", False, False),
    ("IBM280", False, False),
    ("IBM281", False, False),
    ("IBM284", False, False),
    ("IBM285", False, False),
    ("IBM290", False, False),
    ("IBM297", False, False),
    ("IBM420", False, False),
    ("IBM423", False, False),
    ("IBM424", False, False),
    ("IBM437", False, False),
    ("IBM500", False, False),
    ("IBM851", False, False),
    ("IBM852", False, False),
    ("IBM855", False, False),
    ("IBM857", False, False),
    ("IBM860", False, False),
    ("IBM861", False, False),
    ("IBM863", False, False),
    ("IBM864", False, False),
    ("IBM865", False, False),
    ("IBM868", False, False),
    ("IBM869", False, False),
    ("IBM870", False, False),
    ("IBM871", False, False),
    ("IBM880", False, False),
    ("IBM891", False, False),
    ("IBM903", False, False),
    ("IBM904", False, False),
    ("IBM905", False, False),
    ("IBM918", False, False),
    ("IBM1026", False, False),
    ("EBCDIC-AT-DE", False, False),
    ("EBCDIC-AT-DE-A", False, False),
    ("EBCDIC-CA-FR", False, False),
    ("EBCDIC-DK-NO", False, False),
    ("EBCDIC-DK-NO-A", False, False),
    ("EBCDIC-FI-SE", False, False),
    ("EBCDIC-FI-SE-A", False, False),
    ("EBCDIC-FR", False, False),
    ("EBCDIC-IT", False, False),
    ("EBCDIC-PT", False, False),
    ("EBCDIC-ES", False, False),
    ("EBCDIC-ES-A", False, False),
    ("EBCDIC-ES-S", False, False),
    ("EBCDIC-UK", False, False),
    ("EBCDIC-US", False, False),
    ("UNKNOWN-8BIT", False, False),
    ("MNEMONIC", False, False),
    ("MNEM", False, False),
    ("VISCII", False, False),
    ("VIQR", False, False),
    ("KOI8-R", False, False),
    ("HZ-GB-2312", False, False),
    ("IBM866", False, False),
    ("IBM775", False, False),
    ("KOI8-U", False, False),
    ("IBM00858", False, False),
    ("IBM00924", False, False),
    ("IBM01140", False, False),
    ("IBM01141", False, False),
    ("IBM01142", False, False),
    ("IBM01143", False, False),
    ("IBM01144", False, False),
    ("IBM01145", False, False),
    ("IBM01146", False, False),
    ("IBM01147", False, False),
    ("IBM01148", False, False),
    ("IBM01149", False, False),
    ("Big5-HKSCS", False, False),
    ("IBM1047", False, False),
    ("PTCP154", False, False),
    ("Amiga-1251", False, False),
    ("KOI7-switched", False, False),
    ("BRF", False, False),
    ("TSCII", False, False),
    ("CP51932", False, False),
    ("windows-874", False, False),
    ("windows-1250", False, False),
    ("windows-1251", False, False),
    ("windows-1252", False, False),
    ("windows-1253", False, False),
    ("windows-1254", False, False),
    ("windows-1255", False, False),
    ("windows-1256", False, False),
    ("windows-1257", False, False),
    ("windows-1258", False, False),
    ("TIS-620", False, False),
    ("CP50220", False, False),

    ("UTF8", False, False),
    ("utf8", False, False),
    ("csISO646basic1983", False, False),

    (None, True, False),
    (None, False, True),

    ('invalid-value', True, False),

])
def test_charset(value, fails, allow_empty):
    if not fails:
        validated = validators.charset(value, allow_empty = allow_empty)
        if value:
            assert validated is not None
        else:
            assert validated is None
    else:
        with pytest.raises(ValueError):
            value = validators.charset(value, allow_empty = allow_empty)
