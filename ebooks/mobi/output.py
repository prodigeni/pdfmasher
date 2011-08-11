#!/usr/bin/env python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
from __future__ import with_statement

__license__   = 'GPL v3'
__copyright__ = '2009, Kovid Goyal <kovid@kovidgoyal.net>'
__docformat__ = 'restructuredtext en'

from .writer import MobiWriter

_ = lambda s:s

def convert(oeb, output_path, toc_title=None, mobi_toc_at_start=False):
    from .mobiml import MobiMLizer
    from ..oeb.transforms.htmltoc import HTMLTOCAdder
    tocadder = HTMLTOCAdder(title=toc_title, position='start' if mobi_toc_at_start else 'end')
    tocadder(oeb)
    mobimlizer = MobiMLizer()
    mobimlizer(oeb)
    writer = MobiWriter(dont_compress=True)
    writer(oeb, output_path)

