# -*- coding: utf-8 -*-
"""Collection of commonly-used Validator Functions

While this entry point to the library exposes all :term:`validator` and
:term:`checker` functions for convenience, those functions themselves are actually
implemented and documented in child modules: ``validator_collection/validators.py``
and ``validator_collection/checkers.py`` respectively.

"""

import os

# Get the version number from the _version.py file
version_dict = {}
with open(os.path.join(os.path.dirname(__file__), '_version.py')) as version_file:
    exec(version_file.read(), version_dict)                                     # pylint: disable=W0122

__version__ = version_dict.get('__version__')


from validator_collection.validators import bytesIO, date, dict, decimal, \
    directory_exists, datetime, email, float, fraction, file_exists, ip_address, \
    ipv4, ipv6, integer, iterable, mac_address, none, numeric, not_empty, path, \
    path_exists, string, stringIO, time, timezone, url, uuid, variable_name, domain

from validator_collection.checkers import is_between, has_length, is_uuid, is_email,\
    is_url, is_string, is_iterable, is_datetime, is_date, is_time, is_timezone, \
    is_not_empty, is_none, is_numeric, is_decimal, is_float, is_integer, is_fraction,\
    is_variable_name, is_ipv4, is_ipv6, is_ip_address, is_mac_address, is_dict, \
    is_stringIO, is_bytesIO, is_pathlike, is_on_filesystem, is_file, is_directory, \
    is_type, are_dicts_equivalent, are_equivalent, is_domain

__all__ = [
    'bytesIO',
    'date',
    'dict',
    'decimal',
    'directory_exists',
    'datetime',
    'email',
    'float',
    'fraction',
    'file_exists',
    'ip_address',
    'ipv4',
    'ipv6',
    'integer',
    'iterable',
    'domain',
    'mac_address',
    'none',
    'not_empty',
    'path',
    'path_exists',
    'string',
    'stringIO',
    'time',
    'timezone',
    'url',
    'uuid',
    'variable_name',

    'is_between',
    'has_length',
    'is_uuid',
    'is_email',
    'is_url',
    'is_string',
    'is_iterable',
    'is_datetime',
    'is_date',
    'is_time',
    'is_timezone',
    'is_not_empty',
    'is_none',
    'is_numeric',
    'is_decimal',
    'is_float',
    'is_integer',
    'is_fraction',
    'is_variable_name',
    'is_ipv4',
    'is_ipv6',
    'is_ip_address',
    'is_mac_address',
    'is_domain',
    'is_dict',
    'is_stringIO',
    'is_bytesIO',
    'is_pathlike',
    'is_on_filesystem',
    'is_file',
    'is_directory',
    'is_type',
    'are_dicts_equivalent',
    'are_equivalent'
]
