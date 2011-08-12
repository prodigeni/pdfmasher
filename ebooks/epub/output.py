# Copyright 2009, Kovid Goyal <kovid@kovidgoyal.net>
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license




import os, shutil, re, logging

from ..ptempfile import TemporaryDirectory
from ..utils.zipfile import zip_add_dir

from lxml import etree

_ = lambda s:s

block_level_tags = (
      'address',
      'body',
      'blockquote',
      'center',
      'dir',
      'div',
      'dl',
      'fieldset',
      'form',
      'h1',
      'h2',
      'h3',
      'h4',
      'h5',
      'h6',
      'hr',
      'isindex',
      'menu',
      'noframes',
      'noscript',
      'ol',
      'p',
      'pre',
      'table',
      'ul',
      )

def upshift_markup(oeb):
    'Upgrade markup to comply with XHTML 1.1 where possible'
    from ..oeb.base import XPath
    for x in oeb.spine:
        root = x.data
        body = XPath('//h:body')(root)
        if body:
            body = body[0]

        if not hasattr(body, 'xpath'):
            continue
        for u in XPath('//h:u')(root):
            u.tag = 'span'
            u.set('style', 'text-decoration:underline')

def convert(oeb, output_path, epub_flatten=False, dont_split_on_page_breaks=False,
        flow_size=260, no_default_epub_cover=False, no_svg_cover=False,
        preserve_cover_aspect_ratio=False, pretty_print=False):
    if epub_flatten:
        from ..oeb.transforms.filenames import FlatFilenames
        FlatFilenames()(oeb)
    else:
        from ..oeb.transforms.filenames import UniqueFilenames
        UniqueFilenames()(oeb)

    upshift_markup(oeb)
    from ..oeb.transforms.split import Split
    split = Split(not dont_split_on_page_breaks, max_flow_size=flow_size*1024)
    split(oeb)

    from ..oeb.transforms.cover import CoverManager
    cm = CoverManager(
            no_default_cover=no_default_epub_cover,
            no_svg_cover=no_svg_cover,
            preserve_aspect_ratio=preserve_cover_aspect_ratio)
    cm(oeb)

    if oeb.toc.count() == 0:
        logging.warn('This EPUB file has no Table of Contents. '
                'Creating a default TOC')
        first = next(iter(oeb.spine))
        oeb.toc.add('Start', first.href)

    from ..oeb.base import OPF
    identifiers = oeb.metadata['identifier']
    uuid = None
    for x in identifiers:
        if x.get(OPF('scheme'), None).lower() == 'uuid' or str(x).startswith('urn:uuid:'):
            uuid = str(x).split(':')[-1]
            break
    if uuid is None:
        logging.warn('No UUID identifier found')
        from uuid import uuid4
        uuid = str(uuid4())
        oeb.metadata.add('identifier', uuid, scheme='uuid', id=uuid)

    with TemporaryDirectory('_epub_output') as tdir:
        from ..oeb.output import OEBOutput
        metadata_xml = None
        extra_entries = []
        oeb_output = OEBOutput()
        oeb_output.convert(oeb, tdir, None)
        opf = [x for x in os.listdir(tdir) if x.endswith('.opf')][0]
        if pretty_print:
            condense_ncx([os.path.join(tdir, x) for x in os.listdir(tdir) if x.endswith('.ncx')][0])
        from . import initialize_container
        with initialize_container(output_path, os.path.basename(opf),
                extra_entries=extra_entries) as epub:
            zip_add_dir(epub, tdir)
            if metadata_xml is not None:
                epub.writestr('META-INF/metadata.xml', metadata_xml.encode('utf-8'))

def condense_ncx(ncx_path):
    tree = etree.parse(ncx_path)
    for tag in tree.getroot().iter(tag=etree.Element):
        if tag.text:
            tag.text = tag.text.strip()
        if tag.tail:
            tag.tail = tag.tail.strip()
    compressed = etree.tostring(tree.getroot(), encoding='utf-8')
    open(ncx_path, 'wb').write(compressed)
