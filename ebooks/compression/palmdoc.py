# Copyright 2008, Kovid Goyal <kovid at kovidgoyal.net>
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

from . import cPalmdoc

def decompress_doc(data):
    return cPalmdoc.decompress(data)

def compress_doc(data):
    if not data:
        return u''
    return cPalmdoc.compress(data)

