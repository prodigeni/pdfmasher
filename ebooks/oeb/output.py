# Copyright 2009, Kovid Goyal <kovid@kovidgoyal.net>
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

import os, re
import logging
import uuid

from lxml import etree

from ..utils import CurrentDir
from .base import OPF_MIME, NCX_MIME, PAGE_MAP_MIME

from urllib.parse import unquote

class OEBOutput:
    def convert(self, oeb_book, output_path, input_plugin):
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        with CurrentDir(output_path):
            results = oeb_book.to_opf2(page_map=True)
            for key in (OPF_MIME, NCX_MIME, PAGE_MAP_MIME):
                href, root = results.pop(key, [None, None])
                if root is not None:
                    if key == OPF_MIME:
                        try:
                            self.workaround_nook_cover_bug(root)
                        except:
                            logging.exception('Something went wrong while trying to'
                                    ' workaround Nook cover bug, ignoring')
                        try:
                            self.workaround_pocketbook_cover_bug(root)
                        except:
                            logging.exception('Something went wrong while trying to'
                                    ' workaround Pocketbook cover bug, ignoring')
                    raw = etree.tostring(root, pretty_print=True,
                            encoding='utf-8', xml_declaration=True)
                    if key == OPF_MIME:
                        # Needed as I can't get lxml to output opf:role and
                        # not output <opf:metadata> as well
                        raw = re.sub(br'(<[/]{0,1})opf:', br'\1', raw)
                    with open(href, 'wb') as f:
                        f.write(raw)

            for item in oeb_book.manifest:
                path = os.path.abspath(unquote(item.href))
                dir = os.path.dirname(path)
                if not os.path.exists(dir):
                    os.makedirs(dir)
                with open(path, 'wt', encoding='utf-8') as f:
                    f.write(str(item))
                item.unload_data_from_memory(memory=path)

    def workaround_nook_cover_bug(self, root):
        cov = root.xpath('//*[local-name() = "meta" and @name="cover" and'
                ' @content != "cover"]')

        def manifest_items_with_id(id_):
            return root.xpath('//*[local-name() = "manifest"]/*[local-name() = "item" '
                ' and @id="%s"]'%id_)

        if len(cov) == 1:
            cov = cov[0]
            covid = cov.get('content', '')

            if covid:
                manifest_item = manifest_items_with_id(covid)
                if len(manifest_item) == 1 and manifest_item[0].get('media-type', '').startswith('image/'):
                    logging.warn('The cover image has an id != "cover". Renaming'
                            ' to work around bug in Nook Color')

                    newid = str(uuid.uuid4())

                    for item in manifest_items_with_id('cover'):
                        item.set('id', newid)

                    for x in root.xpath('//*[@idref="cover"]'):
                        x.set('idref', newid)

                    manifest_item = manifest_item[0]
                    manifest_item.set('id', 'cover')
                    cov.set('content', 'cover')
    
    def workaround_pocketbook_cover_bug(self, root):
        m = root.xpath('//*[local-name() = "manifest"]/*[local-name() = "item" '
                ' and @id="cover"]')
        if len(m) == 1:
            m = m[0]
            p = m.getparent()
            p.remove(m)
            p.insert(0, m)
