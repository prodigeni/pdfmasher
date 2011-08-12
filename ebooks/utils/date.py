# Copyright 2010, Kovid Goyal <kovid@kovidgoyal.net>
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license
from __future__ import with_statement
from __future__ import unicode_literals

import re
from datetime import datetime
from functools import partial

from dateutil.parser import parse
from dateutil.tz import tzlocal, tzutc

class SafeLocalTimeZone(tzlocal):
    '''
    Assume DST was not in effect for historical dates, if DST
    data for the local timezone is not present in the operating system.
    '''

    def _isdst(self, dt):
        try:
            return tzlocal._isdst(self, dt)
        except ValueError:
            pass
        return False

def compute_locale_info_for_parse_date():
    try:
        dt = datetime.strptime('1/5/2000', "%x")
    except:
        try:
            dt = datetime.strptime('1/5/01', '%x')
        except:
            return False
    if dt.month == 5:
        return True
    return False

parse_date_day_first = compute_locale_info_for_parse_date()
utc_tz = _utc_tz = tzutc()
local_tz = _local_tz = SafeLocalTimeZone()

UNDEFINED_DATE = datetime(101,1,1, tzinfo=utc_tz)
DEFAULT_DATE = datetime(2000,1,1, tzinfo=utc_tz)

def strftime(fmt, t=None):
    ''' A version of strftime that returns unicode strings and tries to handle dates
    before 1900 '''
    if not fmt:
        return u''
    if t is None:
        t = time.localtime()
    if hasattr(t, 'timetuple'):
        t = t.timetuple()
    early_year = t[0] < 1900
    if early_year:
        replacement = 1900 if t[0]%4 == 0 else 1901
        fmt = fmt.replace('%Y', '_early year hack##')
        t = list(t)
        orig_year = t[0]
        t[0] = replacement
    ans = None
    if iswindows:
        if isinstance(fmt, unicode):
            fmt = fmt.encode('mbcs')
        ans = plugins['winutil'][0].strftime(fmt, t)
    else:
        ans = time.strftime(fmt, t).decode(preferred_encoding, 'replace')
    if early_year:
        ans = ans.replace('_early year hack##', str(orig_year))
    return ans

def parse_date(date_string, assume_utc=False, as_utc=True, default=None):
    '''
    Parse a date/time string into a timezone aware datetime object. The timezone
    is always either UTC or the local timezone.

    :param assume_utc: If True and date_string does not specify a timezone,
    assume UTC, otherwise assume local timezone.

    :param as_utc: If True, return a UTC datetime

    :param default: Missing fields are filled in from default. If None, the
    current date is used.
    '''
    if not date_string:
        return UNDEFINED_DATE
    if default is None:
        func = datetime.utcnow if assume_utc else datetime.now
        default = func().replace(hour=0, minute=0, second=0, microsecond=0,
                tzinfo=_utc_tz if assume_utc else _local_tz)
    dt = parse(date_string, default=default, dayfirst=parse_date_day_first)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=_utc_tz if assume_utc else _local_tz)
    return dt.astimezone(_utc_tz if as_utc else _local_tz)

def isoformat(date_time, assume_utc=False, as_utc=True, sep='T'):
    if not hasattr(date_time, 'tzinfo'):
        return unicode(date_time.isoformat())
    if date_time.tzinfo is None:
        date_time = date_time.replace(tzinfo=_utc_tz if assume_utc else
                _local_tz)
    date_time = date_time.astimezone(_utc_tz if as_utc else _local_tz)
    # str(sep) because isoformat barfs with unicode sep on python 2.x
    return unicode(date_time.isoformat(str(sep)))

def as_utc(date_time, assume_utc=True):
    if not hasattr(date_time, 'tzinfo'):
        return date_time
    if date_time.tzinfo is None:
        date_time = date_time.replace(tzinfo=_utc_tz if assume_utc else
                _local_tz)
    return date_time.astimezone(_utc_tz)

def now():
    return datetime.now().replace(tzinfo=_local_tz)

def utcnow():
    return datetime.utcnow().replace(tzinfo=_utc_tz)

def format_date(dt, format, assume_utc=False, as_utc=False):
    ''' Return a date formatted as a string using a subset of Qt's formatting codes '''
    if not format:
        format = 'dd MMM yyyy'

    if hasattr(dt, 'tzinfo'):
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=_utc_tz if assume_utc else
                    _local_tz)
        dt = dt.astimezone(_utc_tz if as_utc else _local_tz)

    if format == 'iso':
        return isoformat(dt, assume_utc=assume_utc, as_utc=as_utc)

    strf = partial(strftime, t=dt.timetuple())

    def format_day(mo):
        l = len(mo.group(0))
        if l == 1: return '%d'%dt.day
        if l == 2: return '%02d'%dt.day
        if l == 3: return strf('%a')
        return strf('%A')

    def format_month(mo):
        l = len(mo.group(0))
        if l == 1: return '%d'%dt.month
        if l == 2: return '%02d'%dt.month
        if l == 3: return strf('%b')
        return strf('%B')

    def format_year(mo):
        if len(mo.group(0)) == 2: return '%02d'%(dt.year % 100)
        return '%04d'%dt.year

    if dt == UNDEFINED_DATE:
        return ''

    format = re.sub('d{1,4}', format_day, format)
    format = re.sub('M{1,4}', format_month, format)
    return re.sub('yyyy|yy', format_year, format)
