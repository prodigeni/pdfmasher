#!/usr/bin/env python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
from __future__ import with_statement

__license__   = 'GPL v3'
__copyright__ = '2009, Kovid Goyal <kovid@kovidgoyal.net>'
__docformat__ = 'restructuredtext en'

import os
from ...utils.date import isoformat, now
from ...utils import guess_type

def meta_info_to_oeb_metadata(mi, m, override_input_metadata=False):
    from ..base import OPF
    if not mi.is_null('title'):
        m.clear('title')
        m.add('title', mi.title)
    if mi.title_sort:
        if not m.title:
            m.add('title', mi.title_sort)
        m.clear('title_sort')
        m.add('title_sort', mi.title_sort)
    if not mi.is_null('authors'):
        m.filter('creator', lambda x : x.role.lower() in ['aut', ''])
        for a in mi.authors:
            attrib = {'role':'aut'}
            if mi.author_sort:
                attrib[OPF('file-as')] = mi.author_sort
            m.add('creator', a, attrib=attrib)
    if not mi.is_null('book_producer'):
        m.filter('contributor', lambda x : x.role.lower() == 'bkp')
        m.add('contributor', mi.book_producer, role='bkp')
    elif override_input_metadata:
        m.filter('contributor', lambda x : x.role.lower() == 'bkp')
    if not mi.is_null('comments'):
        m.clear('description')
        m.add('description', mi.comments)
    elif override_input_metadata:
        m.clear('description')
    if not mi.is_null('publisher'):
        m.clear('publisher')
        m.add('publisher', mi.publisher)
    elif override_input_metadata:
        m.clear('publisher')
    if not mi.is_null('series'):
        m.clear('series')
        m.add('series', mi.series)
    elif override_input_metadata:
        m.clear('series')
    identifiers = mi.get_identifiers()
    set_isbn = False
    for typ, val in identifiers.iteritems():
        has = False
        if typ.lower() == 'isbn':
            set_isbn = True
        for x in m.identifier:
            if x.scheme.lower() == typ.lower():
                x.content = val
                has = True
        if not has:
            m.add('identifier', val, scheme=typ.upper())
    if override_input_metadata and not set_isbn:
        m.filter('identifier', lambda x: x.scheme.lower() == 'isbn')
    if not mi.is_null('language'):
        m.clear('language')
        m.add('language', mi.language)
    if not mi.is_null('series_index'):
        m.clear('series_index')
        m.add('series_index', mi.format_series_index())
    elif override_input_metadata:
        m.clear('series_index')
    if not mi.is_null('rating'):
        m.clear('rating')
        m.add('rating', '%.2f'%mi.rating)
    elif override_input_metadata:
        m.clear('rating')
    if not mi.is_null('tags'):
        m.clear('subject')
        for t in mi.tags:
            m.add('subject', t)
    elif override_input_metadata:
        m.clear('subject')
    if not mi.is_null('pubdate'):
        m.clear('date')
        m.add('date', isoformat(mi.pubdate))
    if not mi.is_null('timestamp'):
        m.clear('timestamp')
        m.add('timestamp', isoformat(mi.timestamp))
    if not mi.is_null('rights'):
        m.clear('rights')
        m.add('rights', mi.rights)
    if not mi.is_null('publication_type'):
        m.clear('publication_type')
        m.add('publication_type', mi.publication_type)

    if not m.timestamp:
        m.add('timestamp', isoformat(now()))
