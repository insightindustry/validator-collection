# -*- coding: utf-8 -*-

"""
validator_collection._compat
~~~~~~~~~~~~~~~
This module handles import compatibility issues between Python 2 and
Python 3.
"""
# pylint: disable=invalid-name,redefined-builtin,no-member,missing-docstring,unused-import,undefined-variable,used-before-assignment,R0204

import math
import sys
from decimal import Decimal
import datetime as datetime_
from fractions import Fraction
import time as time_

_ver = sys.version_info

#: Python 2.x?
is_py2 = (_ver[0] == 2)

#: Python 3.x?
is_py3 = (_ver[0] == 3)
is_py36 = (_ver[0] == 3 and _ver[1] >= 6)
is_py35 = (_ver[0] == 3 and _ver[1] == 5)
is_py34 = (_ver[0] == 3 and _ver[1] == 4)
is_py33 = (_ver[0] == 3 and _ver[1] == 3)
is_py32 = (_ver[0] == 3 and _ver[1] == 2)
is_py31 = (_ver[0] == 3 and _ver[1] == 1)
is_py30 = (_ver[0] == 3 and _ver[1] == 0)

try:
    import simplejson as json_
except ImportError:
    import json as json_

uses_float_infinity = (is_py2 or is_py34 or is_py33 or is_py32 or is_py31 or is_py30)

if uses_float_infinity:
    POSITIVE_INFINITY = float('+inf')
    NEGATIVE_INFINITY = float('-inf')

if is_py2:
    import regex
    re = regex
    builtin_str = str
    bytes = str
    str = unicode
    basestring = basestring
    numeric_types = (int, long, float, Decimal, Fraction)
    integer_types = (int, long)
    long = long
    xrange = xrange

    STDOFFSET = datetime_.timedelta(seconds = -time_.timezone)
    if time_.daylight:
        DSTOFFSET = datetime_.timedelta(seconds = -time_.altzone)
    else:
        DSTOFFSET = STDOFFSET

    DSTDIFF = DSTOFFSET - STDOFFSET


    class TimeZone(datetime_.tzinfo):
        """Implementation of a :class:`tzinfo <python:datetime.tzinfo>` object."""

        def __init__(self, offset = None, tzname = None, **kwargs):
            """Create an instance of a :class:`TimeZone` object.

            :param offset: The number of seconds offset against UTC.
            :type offset: numeric

            :param tzname: The name assigned to the timezone.
            :type tzname: :class:`str <python:str>` / :obj:`None <python:None>`

            """
            if offset and isinstance(offset, numeric_types):
                offset = timedelta(seconds = offset)

            if offset and not isinstance(offset, datetime_.timedelta):
                raise ValueError('offset must be a timedelta or numeric')

            if offset and offset.total_seconds() > (24 * 60 * 60):
                raise ValueError('timezone must be +/- 24h from UTC')

            if not offset:
                offset = timedelta(0)

            if not tzname:
                tzname = 'UTC'

            if not isinstance(tzname, basestring):
                raise ValueError('tzname must be None or a valid string')

            self._offset = offset
            self._name = tzname

            super(TimeZone, self).__init__(**kwargs)

        def utcoffset(self, dt):
            return self._offset

        def dst(self, dt):
            return datetime_.timedelta(0)

        def tzname(self, dt):
            return self._name

elif is_py3:
    import re
    builtin_str = str
    str = str
    bytes = bytes
    basestring = (str, bytes)
    numeric_types = (int, float, Decimal, Fraction)
    integer_types = (int,)
    long = int
    if not uses_float_infinity:
        POSITIVE_INFINITY = math.inf
        NEGATIVE_INFINITY = -math.inf
    TimeZone = datetime_.timezone
else:
    raise NotImplementedError()

datetime_types = [basestring,
                  datetime_.datetime,
                  datetime_.date]
datetime_types.extend(numeric_types)
datetime_types = tuple(datetime_types)

date_types = [basestring,
              datetime_.datetime,
              datetime_.date]
date_types.extend(numeric_types)
date_types = tuple(date_types)

timestamp_types = numeric_types

time_types = [basestring,
              datetime_.datetime,
              datetime_.time]
time_types.extend(numeric_types)
time_types = tuple(time_types)

tzinfo_types = [basestring,
                datetime_.datetime,
                datetime_.date,
                datetime_.tzinfo,
                datetime_.time,
                TimeZone]
tzinfo_types.extend(numeric_types)
tzinfo_types = tuple(tzinfo_types)

dict_ = dict
float_ = float
