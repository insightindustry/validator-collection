# -*- coding: utf-8 -*-

"""
***********************************
tests.test_checkers
***********************************

Tests for :term:`checkers <checker>`.

"""

import time as time_
import uuid
from datetime import datetime, date, time, tzinfo, timedelta

import pytest

import validator_collection.checkers as checkers

from validator_collection._compat import TimeZone


## CORE

@pytest.mark.parametrize('value, expects', [
    (['test', 123], True),
    ([], True),
    (None, False),
    (None, False),
    ('not-a-list', False),
    (set([1, 2, 3]), True),
    ((1, 2, 3), True),
    (set(), True),
    (tuple(), True),
    (123, False),

    (['test', 123], True),
    ([datetime], True),
    (datetime, False),

    (str, False),
    ([str], True)

])
def test_is_iterable(value, expects):
    result = checkers.is_iterable(value)
    assert result == expects


@pytest.mark.parametrize('args, expects', [
    ([{'key': 'value'}, {'key': 'value'}], True),
    ([{'key': ['list']}, {'key': ['list']}], True),
    ([{'key': {'key': 'value'}}, {'key': {'key': 'value'}}], True),

    ([{'key': 'value'}, {'key': 'value2'}], False),
    ([{'key': ['list']}, {'key': ['else']}], False),
    ([{'key': {'key': 'value'}}, {'key': {'else': 'value'}}], False),
    ([{'key': {'key': 'value'}}, {'else': {'key': 'value'}}], False),

    ([{'key': 'value'}, 123], False)
])
def test_are_dicts_equivalent(args, expects):
    result = checkers.are_dicts_equivalent(*args)
    assert result == expects


@pytest.mark.parametrize('args, expects', [
    (['test', 'test'], True),
    ([['test','test'], ['test','test']], True),
    (['test',123], False),
    (['not-a-list',123], False),
    ([123], True),

    ([{'key': 'value'}, {'key': 'value'}], True),
    ([{'key': ['list']}, {'key': ['list']}], True),
    ([{'key': {'key': 'value'}}, {'key': {'key': 'value'}}], True),

    ([{'key': 'value'}, {'key': 'value2'}], False),
    ([{'key': ['list']}, {'key': ['else']}], False),
    ([{'key': {'key': 'value'}}, {'key': {'else': 'value'}}], False),
    ([{'key': {'key': 'value'}}, {'else': {'key': 'value'}}], False),

    ([{'key': 'value'}, 123], False)
])
def test_are_equivalent(args, expects):
    result = checkers.are_equivalent(*args)
    assert result == expects


@pytest.mark.parametrize('value, check_type, expects', [
    ('test-string', str, True),
    ('test-string', (str, int), True),
    ('test-string', int, False),
    ('test-string', 'str', True),
    ('test-string', ('str', int), True),
    (123, int, True),
    (TimeZone(timedelta(hours = 1)), [int, tzinfo], True),
    (TimeZone(timedelta(hours = 1)), tzinfo, True),
    (TimeZone(timedelta(hours = 1)), str, False)
])
def test_is_type(value, check_type, expects):
    """Test the validators.is_type() function."""
    result = checkers.is_type(value, type_ = check_type)
    assert result is expects


@pytest.mark.parametrize('value, expects', [
    ({ 'key': 'value' }, True),
    ('{"key": "json"}', True),
    (['key', 'value'], False),
    ('[{"key": "json"}]', False),
    ({}, True),
    ({}, True),
    ('not-a-dict', False),
    ('', False),
    (None, False),
])
def test_is_dict(value, expects):
    result = checkers.is_dict(value)
    assert result == expects


@pytest.mark.parametrize('value, expects, minimum_length, maximum_length, whitespace_padding', [
    ('test', True, None, None, False),
    ('', True, None, None, False),
    (None, False, None, None, False),

    ('test', True, 4, None, False),
    ('test', True, 1, None, False),
    ('test', False, 50, None, False),
    ('test', True, 50, None, True),

    ('test', True, None, 5, False),
    ('test', True, None, 4, False),
    ('test', False, None, 3, False),

])
def test_is_string(value, expects, minimum_length, maximum_length, whitespace_padding):
    result = checkers.is_string(value,
                                minimum_length = minimum_length,
                                maximum_length = maximum_length,
                                whitespace_padding = whitespace_padding)
    assert result == expects
