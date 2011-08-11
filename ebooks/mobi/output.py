#!/usr/bin/env python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
from __future__ import with_statement

__license__   = 'GPL v3'
__copyright__ = '2009, Kovid Goyal <kovid@kovidgoyal.net>'
__docformat__ = 'restructuredtext en'

from cStringIO import StringIO

_ = lambda s:s

def convert(oeb, output_path, opts):
    from .mobiml import MobiMLizer
    from ..oeb.transforms.htmltoc import HTMLTOCAdder
    if not opts.no_inline_toc:
        tocadder = HTMLTOCAdder(title=opts.toc_title, position='start' if
                opts.mobi_toc_at_start else 'end')
        tocadder(oeb, opts)
    mobimlizer = MobiMLizer(ignore_tables=opts.linearize_tables)
    mobimlizer(oeb, opts)
    write_page_breaks_after_item = True
    opts.mobi_periodical = False
    from .writer import MobiWriter
    writer = MobiWriter(opts, write_page_breaks_after_item=write_page_breaks_after_item)
    writer(oeb, output_path)

