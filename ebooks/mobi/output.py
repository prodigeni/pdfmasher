# Copyright 2009, Kovid Goyal <kovid@kovidgoyal.net>
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

from __future__ import unicode_literals

from .writer import MobiWriter

def convert(oeb, output_path, toc_title=None, mobi_toc_at_start=False):
    from .mobiml import MobiMLizer
    from ..oeb.transforms.htmltoc import HTMLTOCAdder
    tocadder = HTMLTOCAdder(title=toc_title, position='start' if mobi_toc_at_start else 'end')
    tocadder(oeb)
    mobimlizer = MobiMLizer()
    mobimlizer(oeb)
    writer = MobiWriter()
    writer(oeb, output_path)

