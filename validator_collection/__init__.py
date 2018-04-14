# -*- coding: utf-8 -*-
"""Collection of commonly-used Validator Functions

While this entry point to the library exposes all :term:`validator` and
:term:`checker` functions for convenience, those functions themselves are actually
implemented and documented in child modules: ``validator_collection/validators.py``
and ``validator_collection/checkers.py`` respectively.

"""

import os

with open(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                       'VERSION')) as version_file:
    __version__ = version_file.read().strip()

from validator_collection.validators import bytesIO, date, dict, decimal, \
    directory_exists, datetime, email, float, fraction, file_exists, ipv4, \
    ipv6, integer, iterable, mac_address, none, numeric, not_empty, path, \
    path_exists, string, stringIO, time, timezone, url, uuid, valid_variable_name

from validator_collection.checkers import is_uuid, is_email, is_url, is_string, \
    is_iterable, is_datetime, is_date, is_time, is_timezone, is_not_empty, is_none, \
    is_numeric, is_decimal, is_float, is_integer, is_fraction, is_valid_variable_name, \
    is_ipv4, is_ipv6, is_ip, is_mac_address, is_dict, is_stringIO, is_bytesIO, \
    is_pathlike, is_on_filesystem, is_file, is_directory, is_type, are_dicts_equivalent,\
    are_equivalent

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
    'ipv4',
    'ipv6',
    'integer',
    'iterable',
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
    'valid_variable_name',
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
    'is_valid_variable_name',
    'is_ipv4',
    'is_ipv6',
    'is_ip',
    'is_mac_address',
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
