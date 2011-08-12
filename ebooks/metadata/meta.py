# Copyright 2008, Kovid Goyal <kovid at kovidgoyal.net>
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license




import os, re, collections

from ..constants import filesystem_encoding
from ..utils import isbytestring
from . import MetaInformation, string_to_authors

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


def metadata_from_filename(name, pat=None):
    if isbytestring(name):
        name = name.decode(filesystem_encoding, 'replace')
    name = name.rpartition('.')[0]
    mi = MetaInformation(None, None)
    if pat is None:
        pat = re.compile(r'(?P<title>.+) - (?P<author>[^_]+)')
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
    
    if mi.is_null('title'):
        mi.title = name
    return mi
