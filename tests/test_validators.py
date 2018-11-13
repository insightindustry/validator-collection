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

@pytest.mark.parametrize('value, fails, allow_empty', [
    (u"http://foo.com/blah_blah", False, False),
    (u"http://foo.com/blah_blah/", False, False),
    (u"http://foo.com/blah_blah_(wikipedia)", False, False),
    (u"http://foo.com/blah_blah_(wikipedia)_(again)", False, False),
    (u"http://www.example.com/wpstyle/?p=364", False, False),
    (u"https://www.example.com/foo/?bar=baz&inga=42&quux", False, False),
    (u"http://✪df.ws/123", False, False),
    (u"http://userid:password@example.com:8080", False, False),
    (u"http://userid:password@example.com:8080/", False, False),
    (u"http://userid@example.com", False, False),
    (u"http://userid@example.com/", False, False),
    (u"http://userid@example.com:8080", False, False),
    (u"http://userid@example.com:8080/", False, False),
    (u"http://userid:password@example.com", False, False),
    (u"http://userid:password@example.com/", False, False),
    (u"http://142.42.1.1/", False, False),
    (u"http://142.42.1.1:8080/", False, False),
    (u"http://➡.ws/䨹", False, False),
    (u"http://⌘.ws", False, False),
    (u"http://⌘.ws/", False, False),
    (u"http://foo.com/blah_(wikipedia)#cite-1", False, False),
    (u"http://foo.com/blah_(wikipedia)_blah#cite-1", False, False),
    (u"http://foo.com/unicode_(✪)_in_parens", False, False),
    (u"http://foo.com/(something)?after=parens", False, False),
    (u"http://☺.damowmow.com/", False, False),
    (u"http://code.google.com/events/#&product=browser", False, False),
    (u"http://j.mp", False, False),
    (u"ftp://foo.bar/baz", False, False),
    (u"http://foo.bar/?q=Test%20URL-encoded%20stuff", False, False),
    (u"http://مثال.إختبار", False, False),
    (u"http://例子.测试", False, False),
    (u"http://उदाहरण.परीक्षा", False, False),
    (u"http://-.~_!$&'()*+,;=:%40:80%2f::::::@example.com", False, False),
    (u"http://1337.net", False, False),
    (u"http://a.b-c.de", False, False),
    (u"http://a.b--c.de/", False, False),
    (u"http://223.255.255.254", False, False),
    (u"", True, False),
    (None, True, False),
    (u"http://", True, False),
    (u"http://.", True, False),
    (u"http://..", True, False),
    (u"http://../", True, False),
    (u"http://?", True, False),
    (u"http://??", True, False),
    (u"http://??/", True, False),
    (u"http://#", True, False),
    (u"http://##", True, False),
    (u"http://##/", True, False),
    (u"http://foo.bar?q=Spaces should be encoded", True, False),
    (u"//", True, False),
    (u"//a", True, False),
    (u"///a", True, False),
    (u"///", True, False),
    (u"http:///a", True, False),
    (u"foo.com", True, False),
    (u"rdar://1234", True, False),
    (u"h://test", True, False),
    (u"http:// shouldfail.com", True, False),
    (u":// should fail", True, False),
    (u"http://foo.bar/foo(bar)baz quux", True, False),
    (u"ftps://foo.bar/", True, False),
    (u"http://-error-.invalid/", True, False),
    (u"http://-a.b.co", True, False),
    (u"http://a.b-.co", True, False),
    (u"http://0.0.0.0", True, False),
    (u"http://10.1.1.0", True, False),
    (u"http://10.1.1.255", True, False),
    (u"http://224.1.1.1", True, False),
    (u"http://1.1.1.1.1", True, False),
    (u"http://123.123.123", True, False),
    (u"http://3628126748", True, False),
    (u"http://.www.foo.bar/", True, False),
    (u"http://www.foo.bar./", True, False),
    (u"http://.www.foo.bar./", True, False),
    (u"http://10.1.1.1", True, False),
    (u"", False, True),
    (None, False, True)
])
def test_url(value, fails, allow_empty):
    """Test the URL validator."""
    if not fails:
        validated = validators.url(value, allow_empty = allow_empty)
        if value:
            assert isinstance(validated, basestring)
        else:
            assert validated is None
    else:
        with pytest.raises((ValueError, TypeError)):
            value = validators.url(value, allow_empty = allow_empty)


@pytest.mark.parametrize('value, fails, allow_empty', [
    (u"foo.com", False, False),
    (u"www.example.com", False, False),
    (u"✪df.ws", False, False),
    (u"142.42.1.1", False, False),
    (u"➡.ws", False, False),
    (u"⌘.ws", False, False),
    (u"☺.damowmow.com", False, False),
    (u"j.mp", False, False),
    (u"مثال.إختبار", False, False),
    (u"例子.测试", False, False),
    (u"उदाहरण.परीक्षा", False, False),
    (u"1337.net", False, False),
    (u"a.b-c.de", False, False),
    (u"a.b--c.de", False, False),
    (u"a.b--c.de/", True, False),
    (u"223.255.255.254", False, False),
    (u" shouldfail.com", False, False),

    (u"foo.com/blah_blah", True, False),
    (u"foo.com/blah_blah/", True, False),
    (u"www.example.com/wpstyle/?p=364", True, False),
    (u"✪df.ws/123", True, False),
    (u"userid:password@example.com:8080", True, False),
    (u"userid@example.com", True, False),
    (u"userid:password@example.com", True, False),
    (u"142.42.1.1/", True, False),
    (u"142.42.1.1:8080/", True, False),
    (u"➡.ws/䨹", True, False),
    (u"⌘.ws/", True, False),
    (u"code.google.com/events/#&product=browser", True, False),
    (u"-.~_!$&'()*+,;=:%40:80%2f::::::@example.com", True, False),
    (u"", True, False),
    (None, True, False),
    (u"", True, False),
    (u".", True, False),
    (u"..", True, False),
    (u"../", True, False),
    (u"?", True, False),
    (u"??", True, False),
    (u"??/", True, False),
    (u"#", True, False),
    (u"##", True, False),
    (u"##/", True, False),
    (u"foo.bar?q=Spaces should be encoded", True, False),
    (u"//", True, False),
    (u"//a", True, False),
    (u"///a", True, False),
    (u"///", True, False),
    (u"/a", True, False),
    (u"rdar://1234", True, False),
    (u"h://test", True, False),
    (u":// should fail", True, False),
    (u"foo.bar/foo(bar)baz quux", True, False),
    (u"foo.bar/", True, False),
    (u"-error-.invalid/", True, False),
    (u"-a.b.co", True, False),
    (u"a.b-.co", True, False),
    (u"0.0.0.0", True, False),
    (u"10.1.1.0", True, False),
    (u"10.1.1.255", True, False),
    (u"224.1.1.1", True, False),
    (u"1.1.1.1.1", True, False),
    (u"123.123.123", True, False),
    (u"3628126748", True, False),
    (u".www.foo.bar/", True, False),
    (u"www.foo.bar./", True, False),
    (u".www.foo.bar./", True, False),
    (u"10.1.1.1", True, False),
])
def test_domain(value, fails, allow_empty):
    """Test the domain validator."""
    if not fails:
        validated = validators.domain(value, allow_empty = allow_empty)
        if value:
            assert isinstance(validated, basestring)
        else:
            assert validated is None
    else:
        with pytest.raises((ValueError, TypeError)):
            value = validators.domain(value, allow_empty = allow_empty)


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
