from __future__ import with_statement
__license__   = 'GPL v3'
__copyright__ = '2008, Kovid Goyal <kovid at kovidgoyal.net>'

import os, re, collections

from ..constants import filesystem_encoding
from ..utils import isbytestring
# from ..customize.ui import get_file_type_metadata, set_file_type_metadata
from . import MetaInformation, string_to_authors

_METADATA_PRIORITIES = [
                       'html', 'htm', 'xhtml', 'xhtm',
                       'rtf', 'fb2', 'pdf', 'prc', 'odt',
                       'epub', 'lit', 'lrx', 'lrf', 'mobi',
                       'rb', 'imp', 'azw', 'snb'
                      ]

# The priorities for loading metadata from different file types
# Higher values should be used to update metadata from lower values
METADATA_PRIORITIES = collections.defaultdict(lambda:0)
for i, ext in enumerate(_METADATA_PRIORITIES):
    METADATA_PRIORITIES[ext] = i

def path_to_ext(path):
    return os.path.splitext(path)[1][1:].lower()

def metadata_from_formats(formats, force_read_metadata=False, pattern=None):
    try:
        return _metadata_from_formats(formats, force_read_metadata, pattern)
    except:
        mi = metadata_from_filename(list(iter(formats), pattern)[0])
        if not mi.authors:
            mi.authors = [_('Unknown')]
        return mi

def _metadata_from_formats(formats, force_read_metadata=False, pattern=None):
    mi = MetaInformation(None, None)
    formats.sort(cmp=lambda x,y: cmp(METADATA_PRIORITIES[path_to_ext(x)],
                                     METADATA_PRIORITIES[path_to_ext(y)]))
    extensions = list(map(path_to_ext, formats))
    if 'opf' in extensions:
        opf = formats[extensions.index('opf')]
        mi2 = opf_metadata(opf)
        if mi2 is not None and mi2.title:
            return mi2

    for path, ext in zip(formats, extensions):
        with open(path, 'rb') as stream:
            try:
                newmi = get_metadata(stream, stream_type=ext,
                                     use_libprs_metadata=True,
                                     force_read_metadata=force_read_metadata,
                                     pattern=pattern)
                mi.smart_update(newmi)
            except:
                continue
            if getattr(mi, 'application_id', None) is not None:
                return mi

    if not mi.title:
        mi.title = _('Unknown')
    if not mi.authors:
        mi.authors = [_('Unknown')]

    return mi

def get_metadata(stream, stream_type='lrf', use_libprs_metadata=False,
                 force_read_metadata=False, pattern=None):
    pos = 0
    if hasattr(stream, 'tell'):
        pos = stream.tell()
    try:
        return _get_metadata(stream, stream_type, use_libprs_metadata,
                             force_read_metadata, pattern)
    finally:
        if hasattr(stream, 'seek'):
            stream.seek(pos)


def _get_metadata(stream, stream_type, use_libprs_metadata,
                  force_read_metadata=False, pattern=None):
    if stream_type: stream_type = stream_type.lower()
    if stream_type in ('html', 'html', 'xhtml', 'xhtm', 'xml'):
        stream_type = 'html'
    if stream_type in ('mobi', 'prc', 'azw'):
        stream_type = 'mobi'
    if stream_type in ('odt', 'ods', 'odp', 'odg', 'odf'):
        stream_type = 'odt'

    opf = None
    if hasattr(stream, 'name'):
        c = os.path.splitext(stream.name)[0]+'.opf'
        if os.access(c, os.R_OK):
            opf = opf_metadata(os.path.abspath(c))

    if use_libprs_metadata and getattr(opf, 'application_id', None) is not None:
        return opf

    mi = MetaInformation(None, None)
    name = os.path.basename(getattr(stream, 'name', ''))
    base = metadata_from_filename(name, pat=pattern)
    # if force_read_metadata or prefs['read_file_metadata']:
    #     mi = get_file_type_metadata(stream, stream_type)
    if base.title == os.path.splitext(name)[0] and \
            base.is_null('authors') and base.is_null('isbn'):
        # Assume that there was no metadata in the file and the user set pattern
        # to match meta info from the file name did not match.
        # The regex is meant to match the standard format filenames are written
        # in: title_-_author_number.extension
        base.smart_update(metadata_from_filename(name, re.compile(
                    r'^(?P<title>[ \S]+?)[ _]-[ _](?P<author>[ \S]+?)_+\d+')))
        if base.title:
            base.title = base.title.replace('_', ' ')
        if base.authors:
            base.authors = [a.replace('_', ' ').strip() for a in base.authors]
    if not base.authors:
        base.authors = [_('Unknown')]
    if not base.title:
        base.title = _('Unknown')
    base.smart_update(mi)
    if opf is not None:
        base.smart_update(opf)

    return base

# def set_metadata(stream, mi, stream_type='lrf'):
#     if stream_type:
#         stream_type = stream_type.lower()
#     set_file_type_metadata(stream, mi, stream_type)


def metadata_from_filename(name, pat=None):
    if isbytestring(name):
        name = name.decode(filesystem_encoding, 'replace')
    name = name.rpartition('.')[0]
    mi = MetaInformation(None, None)
    if pat is None:
        pat = re.compile(ur'(?P<title>.+) - (?P<author>[^_]+)')
    name = name.replace('_', ' ')
    match = pat.search(name)
    if match is not None:
        try:
            mi.title = match.group('title')
        except IndexError:
            pass
        try:
            au = match.group('author')
            aus = string_to_authors(au)
            mi.authors = aus
        except (IndexError, ValueError):
            pass
        try:
            mi.series = match.group('series')
        except IndexError:
            pass
        try:
            si = match.group('series_index')
            mi.series_index = float(si)
        except (IndexError, ValueError, TypeError):
            pass
        try:
            si = match.group('isbn')
            mi.isbn = si
        except (IndexError, ValueError):
            pass
        try:
            publisher = match.group('publisher')
            mi.publisher = publisher
        except (IndexError, ValueError):
            pass
        try:
            pubdate = match.group('published')
            if pubdate:
                from calibre.utils.date import parse_date
                mi.pubdate = parse_date(pubdate)
        except:
            pass

    if mi.is_null('title'):
        mi.title = name
    return mi
