#!/usr/bin/env  python
__license__   = 'GPL v3'
__copyright__ = '2008, Kovid Goyal kovid@kovidgoyal.net'
__docformat__ = 'restructuredtext en'

'''
Miscelleaneous utilities.
'''

import __builtin__
import sys
import os
import os.path
import re
from functools import partial

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

def prints(*args, **kwargs):
    '''
    Print unicode arguments safely by encoding them to preferred_encoding
    Has the same signature as the print function from Python 3, except for the
    additional keyword argument safe_encode, which if set to True will cause the
    function to use repr when encoding fails.
    '''
    file = kwargs.get('file', sys.stdout)
    sep  = kwargs.get('sep', ' ')
    end  = kwargs.get('end', '\n')
    enc = preferred_encoding
    safe_encode = kwargs.get('safe_encode', False)
    if 'CALIBRE_WORKER' in os.environ:
        enc = 'utf-8'
    for i, arg in enumerate(args):
        if isinstance(arg, unicode):
            try:
                arg = arg.encode(enc)
            except UnicodeEncodeError:
                try:
                    arg = arg.encode('utf-8')
                except:
                    if not safe_encode:
                        raise
                    arg = repr(arg)
        if not isinstance(arg, str):
            try:
                arg = str(arg)
            except ValueError:
                arg = unicode(arg)
            if isinstance(arg, unicode):
                try:
                    arg = arg.encode(enc)
                except UnicodeEncodeError:
                    try:
                        arg = arg.encode('utf-8')
                    except:
                        if not safe_encode:
                            raise
                        arg = repr(arg)

        try:
            file.write(arg)
        except:
            file.write(repr(arg))
        if i != len(args)-1:
            file.write(bytes(sep))
    file.write(bytes(end))

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

def walk(dir):
    ''' A nice interface to os.walk '''
    for record in os.walk(dir):
        for f in record[-1]:
            yield os.path.join(record[0], f)

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

def human_readable(size):
    """ Convert a size in bytes into a human readable form """
    divisor, suffix = 1, "B"
    for i, candidate in enumerate(('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB')):
        if size < 1024**(i+1):
            divisor, suffix = 1024**(i), candidate
            break
    size = str(float(size)/divisor)
    if size.find(".") > -1:
        size = size[:size.find(".")+2]
    if size.endswith('.0'):
        size = size[:-2]
    return size + " " + suffix

def sanitize_file_name2(name, substitute='_'):
    '''
    Sanitize filenames removing invalid chars. Keeps unicode names as unicode
    and bytestrings as bytestrings
    '''
    if isbytestring(name):
        return sanitize_file_name(name, substitute=substitute)
    return sanitize_file_name_unicode(name, substitute=substitute)
