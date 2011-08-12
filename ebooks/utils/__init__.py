#!/usr/bin/env  python
# Copyright 2008, Kovid Goyal kovid@kovidgoyal.net
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

'''
Miscelleaneous utilities.
'''

import __builtin__
import sys
import os
import os.path
import re
from functools import partial

from . import resources
from ..constants import preferred_encoding, filesystem_encoding

__builtin__.__dict__['dynamic_property'] = lambda(func): func(None)

class CurrentDir(object):

    def __init__(self, path):
        self.path = path
        self.cwd = None

    def __enter__(self, *args):
        self.cwd = os.getcwd()
        os.chdir(self.path)
        return self.cwd

    def __exit__(self, *args):
        try:
            os.chdir(self.cwd)
        except Exception:
            # The previous CWD no longer exists
            pass

def unicode_path(path, abs=False):
    if not isinstance(path, unicode):
        path = path.decode(sys.getfilesystemencoding())
    if abs:
        path = os.path.abspath(path)
    return path

def my_unichr(num):
    try:
        return unichr(num)
    except (ValueError, OverflowError):
        return u'?'

def entity_to_unicode(match, exceptions=[], encoding='cp1252',
        result_exceptions={}):
    '''
    :param match: A match object such that '&'+match.group(1)';' is the entity.

    :param exceptions: A list of entities to not convert (Each entry is the name of the entity, for e.g. 'apos' or '#1234'

    :param encoding: The encoding to use to decode numeric entities between 128 and 256.
    If None, the Unicode UCS encoding is used. A common encoding is cp1252.

    :param result_exceptions: A mapping of characters to entities. If the result
    is in result_exceptions, result_exception[result] is returned instead.
    Convenient way to specify exception for things like < or > that can be
    specified by various actual entities.
    '''
    def check(ch):
        return result_exceptions.get(ch, ch)

    ent = match.group(1)
    if ent in exceptions:
        return '&'+ent+';'
    if ent == 'apos':
        return check("'")
    if ent == 'hellips':
        ent = 'hellip'
    if ent.startswith('#'):
        try:
            if ent[1] in ('x', 'X'):
                num = int(ent[2:], 16)
            else:
                num = int(ent[1:])
        except:
            return '&'+ent+';'
        if encoding is None or num > 255:
            return check(my_unichr(num))
        try:
            return check(chr(num).decode(encoding))
        except UnicodeDecodeError:
            return check(my_unichr(num))
    try:
        return check(my_unichr(name2codepoint[ent]))
    except KeyError:
        return '&'+ent+';'

_ent_pat = re.compile(r'&(\S+?);')
xml_entity_to_unicode = partial(entity_to_unicode, result_exceptions = {
    '"' : '&quot;',
    "'" : '&apos;',
    '<' : '&lt;',
    '>' : '&gt;',
    '&' : '&amp;'})

def replace_entities(raw):
    return _ent_pat.sub(entity_to_unicode, raw)

def xml_replace_entities(raw):
    return _ent_pat.sub(xml_entity_to_unicode, raw)

def prepare_string_for_xml(raw, attribute=False):
    raw = _ent_pat.sub(entity_to_unicode, raw)
    raw = raw.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    if attribute:
        raw = raw.replace('"', '&quot;').replace("'", '&apos;')
    return raw

def isbytestring(obj):
    return isinstance(obj, (str, bytes))

def force_unicode(obj, enc=preferred_encoding):
    if isbytestring(obj):
        try:
            obj = obj.decode(enc)
        except:
            try:
                obj = obj.decode(filesystem_encoding if enc ==
                        preferred_encoding else preferred_encoding)
            except:
                try:
                    obj = obj.decode('utf-8')
                except:
                    obj = repr(obj)
                    if isbytestring(obj):
                        obj = obj.decode('utf-8')
    return obj

def as_unicode(obj, enc=preferred_encoding):
    if not isbytestring(obj):
        try:
            obj = unicode(obj)
        except:
            try:
                obj = str(obj)
            except:
                obj = repr(obj)
    return force_unicode(obj, enc=enc)

_mt_inited = False
def _init_mimetypes():
    global _mt_inited
    import mimetypes
    mimetypes.init([P('mime.types')])
    _mt_inited = True

def guess_type(*args, **kwargs):
    import mimetypes
    if not _mt_inited:
        _init_mimetypes()
    return mimetypes.guess_type(*args, **kwargs)

def guess_all_extensions(*args, **kwargs):
    import mimetypes
    if not _mt_inited:
        _init_mimetypes()
    return mimetypes.guess_all_extensions(*args, **kwargs)

def get_types_map():
    import mimetypes
    if not _mt_inited:
        _init_mimetypes()
    return mimetypes.types_map

_filename_sanitize = re.compile(r'[\xae\0\\|\?\*<":>\+/]')
_filename_sanitize_unicode = frozenset([u'\\', u'|', u'?', u'*', u'<',
    u'"', u':', u'>', u'+', u'/'] + list(map(unichr, xrange(32))))

def sanitize_file_name(name, substitute='_', as_unicode=False):
    '''
    Sanitize the filename `name`. All invalid characters are replaced by `substitute`.
    The set of invalid characters is the union of the invalid characters in Windows,
    OS X and Linux. Also removes leading and trailing whitespace.
    **WARNING:** This function also replaces path separators, so only pass file names
    and not full paths to it.
    *NOTE:* This function always returns byte strings, not unicode objects. The byte strings
    are encoded in the filesystem encoding of the platform, or UTF-8.
    '''
    if isinstance(name, unicode):
        name = name.encode(filesystem_encoding, 'ignore')
    one = _filename_sanitize.sub(substitute, name)
    one = re.sub(r'\s', ' ', one).strip()
    bname, ext = os.path.splitext(one)
    one = re.sub(r'^\.+$', '_', bname)
    if as_unicode:
        one = one.decode(filesystem_encoding)
    one = one.replace('..', substitute)
    one += ext
    # Windows doesn't like path components that end with a period
    if one and one[-1] in ('.', ' '):
        one = one[:-1]+'_'
    # Names starting with a period are hidden on Unix
    if one.startswith('.'):
        one = '_' + one[1:]
    return one

def extract(path, dir):
    extractor = None
    # First use the file header to identify its type
    with open(path, 'rb') as f:
        id_ = f.read(3)
    if id_ == b'Rar':
        from calibre.libunrar import extract as rarextract
        extractor = rarextract
    elif id_.startswith(b'PK'):
        from calibre.libunzip import extract as zipextract
        extractor = zipextract
    if extractor is None:
        # Fallback to file extension
        ext = os.path.splitext(path)[1][1:].lower()
        if ext in ['zip', 'cbz', 'epub', 'oebzip']:
            from calibre.libunzip import extract as zipextract
            extractor = zipextract
        elif ext in ['cbr', 'rar']:
            from calibre.libunrar import extract as rarextract
            extractor = rarextract
    if extractor is None:
        raise Exception('Unknown archive type')
    extractor(path, dir)

relpath = os.path.relpath

def remove_bracketed_text(src,
        brackets={u'(':u')', u'[':u']', u'{':u'}'}):
    from collections import Counter
    counts = Counter()
    buf = []
    src = force_unicode(src)
    rmap = dict([(v, k) for k, v in brackets.iteritems()])
    for char in src:
        if char in brackets:
            counts[char] += 1
        elif char in rmap:
            idx = rmap[char]
            if counts[idx] > 0:
                counts[idx] -= 1
        elif sum(counts.itervalues()) < 1:
            buf.append(char)
    return u''.join(buf)

def sanitize_file_name2(name, substitute='_'):
    '''
    Sanitize filenames removing invalid chars. Keeps unicode names as unicode
    and bytestrings as bytestrings
    '''
    if isbytestring(name):
        return sanitize_file_name(name, substitute=substitute)
    return sanitize_file_name_unicode(name, substitute=substitute)
