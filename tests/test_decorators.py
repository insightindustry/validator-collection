"""
***********************************
tests.test_decorator.py
***********************************

Tests for decorators.

"""

import os

from validator_collection._decorators import disable_on_env, disable_checker_on_env

import pytest


@pytest.mark.parametrize('env_value, input_value, force_run, expects', [
    (None, 'test', False, 123),
    ('decorated_function', 'test', False, 'test'),
    ('decorated_function, other_function', 'test', False, 'test'),
    ('other_function1, other_function2', 'test', False, 123),

    ('decorated_function', 'test', True, 123),
    ('decorated_function, other_function', 'test', True, 123),
    ('other_function1, other_function2', 'test', True, 123),

])
def test_disable_on_env(env_value, input_value, force_run, expects):
    """
    The test function for the test.

    Args:
        env_value: (todo): write your description
        input_value: (todo): write your description
        force_run: (bool): write your description
        expects: (todo): write your description
    """
    if os.getenv('VALIDATORS_DISABLED', None):
        del os.environ['VALIDATORS_DISABLED']

    if env_value:
        os.environ['VALIDATORS_DISABLED'] = env_value

    @disable_on_env
    def decorated_function(value, other_value = None):                          # pylint: disable=W0613
        """
        Decorator to convert a function.

        Args:
            value: (todo): write your description
            other_value: (todo): write your description
        """
        return 123

    result = decorated_function(input_value,                                    # pylint: disable=E1123
                                force_run = force_run)
    assert result == expects

    if env_value:
        del os.environ['VALIDATORS_DISABLED']


@pytest.mark.parametrize('env_value, input_value, force_run, expects', [
    (None, 'test', False, 123),
    ('decorated_function', 'test', False, True),
    ('decorated_function, other_function', 'test', False, True),
    ('other_function1, other_function2', 'test', False, 123),

    ('decorated_function', 'test', True, 123),
    ('decorated_function, other_function', 'test', True, 123),
    ('other_function1, other_function2', 'test', True, 123),

])
def test_disable_checker_on_env(env_value, input_value, force_run, expects):
    """
    Decorator to runer.

    Args:
        env_value: (todo): write your description
        input_value: (todo): write your description
        force_run: (bool): write your description
        expects: (todo): write your description
    """
    if os.getenv('CHECKERS_DISABLED', None):
        del os.environ['CHECKERS_DISABLED']

    if env_value:
        os.environ['CHECKERS_DISABLED'] = env_value

    @disable_checker_on_env
    def decorated_function(value, other_value = None, **kwargs):                          # pylint: disable=W0613
        """
        Decorator for decorator.

        Args:
            value: (todo): write your description
            other_value: (todo): write your description
        """
        return 123

    result = decorated_function(input_value,                                    # pylint: disable=E1123
                                force_run = force_run)
    assert result == expects

    if env_value:
        del os.environ['CHECKERS_DISABLED']
