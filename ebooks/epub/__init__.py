from __future__ import with_statement
# Copyright 2008, Kovid Goyal kovid@kovidgoyal.net
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

'''
Conversion to EPUB.
'''
from ..utils.zipfile import ZipFile, ZIP_STORED

def rules(stylesheets):
    for s in stylesheets:
        if hasattr(s, 'cssText'):
            for r in s:
                if r.type == r.STYLE_RULE:
                    yield r

def initialize_container(path_to_container, opf_name='metadata.opf',
        extra_entries=[]):
    '''
    Create an empty EPUB document, with a default skeleton.
    '''
    rootfiles = ''
    for path, mimetype, _ in extra_entries:
        rootfiles += u'<rootfile full-path="{0}" media-type="{1}"/>'.format(
                path, mimetype)
    CONTAINER = u'''\
<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
   <rootfiles>
      <rootfile full-path="{0}" media-type="application/oebps-package+xml"/>
      {extra_entries}
   </rootfiles>
</container>
    '''.format(opf_name, extra_entries=rootfiles).encode('utf-8')
    zf = ZipFile(path_to_container, 'w')
    zf.writestr('mimetype', 'application/epub+zip', compression=ZIP_STORED)
    zf.writestr('META-INF/', '', 0700)
    zf.writestr('META-INF/container.xml', CONTAINER)
    for path, _, data in extra_entries:
        zf.writestr(path, data)
    return zf


