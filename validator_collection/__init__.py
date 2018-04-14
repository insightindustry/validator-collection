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

    
]
