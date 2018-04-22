# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

"""
****************************************
validator_collection._decorators.py
****************************************

Defines the decorator used to prevent validator execution based on an available
environment variable.

"""

import os
from functools import wraps

from validator_collection.errors import ValidatorUsageError

def disable_on_env(func):
    """Disable the ``func`` called if its name is present in ``VALIDATORS_DISABLED``.

    :param func: The function/validator to be disabled.
    :type func: callable

    :returns: If disabled, the ``value`` (first positional argument) passed to
      ``func``. If enabled, the result of ``func``.

    """
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        # pylint: disable=C0111, C0103
        function_name = func.__name__
        VALIDATORS_DISABLED = os.getenv('VALIDATORS_DISABLED', '')
        disabled_functions = [x.strip() for x in VALIDATORS_DISABLED.split(',')]

        force_run = kwargs.get('force_run', False)

        try:
            value = args[0]
        except IndexError:
            raise ValidatorUsageError('no value was supplied')

        if function_name in disabled_functions and not force_run:
            return value
        else:
            updated_kwargs = {key : kwargs[key]
                              for key in kwargs
                              if key != 'force_run'}
            return func(*args, **updated_kwargs)

    return func_wrapper


def disable_checker_on_env(func):
    """Disable the ``func`` called if its name is present in ``CHECKERS_DISABLED``.

    :param func: The function/validator to be disabled.
    :type func: callable

    :returns: If disabled, ``True``. If enabled, the result of ``func``.

    """
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        # pylint: disable=C0111, C0103
        function_name = func.__name__
        CHECKERS_DISABLED = os.getenv('CHECKERS_DISABLED', '')
        disabled_functions = [x.strip() for x in CHECKERS_DISABLED.split(',')]

        force_run = kwargs.get('force_run', False)

        if function_name in disabled_functions and not force_run:
            return True
        else:
            return func(*args, **kwargs)

    return func_wrapper
