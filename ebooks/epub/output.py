#!/usr/bin/env python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
from __future__ import with_statement

__license__   = 'GPL v3'
__copyright__ = '2009, Kovid Goyal <kovid@kovidgoyal.net>'
__docformat__ = 'restructuredtext en'

import os, shutil, re

from ..ptempfile import TemporaryDirectory

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


def workaround_webkit_quirks(oeb):
    from ..oeb.base import XPath
    for x in oeb.spine:
        root = x.data
        body = XPath('//h:body')(root)
        if body:
            body = body[0]

        if not hasattr(body, 'xpath'):
            continue

        for pre in XPath('//h:pre')(body):
            if not pre.text and len(pre) == 0:
                pre.tag = 'div'

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

def convert(oeb, output_path, opts):
    if opts.epub_flatten:
        from ..oeb.transforms.filenames import FlatFilenames
        FlatFilenames()(oeb, opts)
    else:
        from ..oeb.transforms.filenames import UniqueFilenames
        UniqueFilenames()(oeb, opts)

    workaround_ade_quirks(oeb)
    workaround_webkit_quirks(oeb)
    upshift_markup(oeb)
    # from calibre.ebooks.oeb.transforms.rescale import RescaleImages
    # RescaleImages()(oeb, opts)

    from ..oeb.transforms.split import Split
    split = Split(not opts.dont_split_on_page_breaks,
            max_flow_size=opts.flow_size*1024
            )
    split(oeb, opts)

    from ..oeb.transforms.cover import CoverManager
    cm = CoverManager(
            no_default_cover=opts.no_default_epub_cover,
            no_svg_cover=opts.no_svg_cover,
            preserve_aspect_ratio=opts.preserve_cover_aspect_ratio)
    cm(oeb, opts)

    workaround_sony_quirks(oeb)

    if oeb.toc.count() == 0:
        logging.warn('This EPUB file has no Table of Contents. '
                'Creating a default TOC')
        first = iter(oeb.spine).next()
        oeb.toc.add('Start', first.href)

    from ..oeb.base import OPF
    identifiers = oeb.metadata['identifier']
    uuid = None
    for x in identifiers:
        if x.get(OPF('scheme'), None).lower() == 'uuid' or unicode(x).startswith('urn:uuid:'):
            uuid = unicode(x).split(':')[-1]
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
        # if self.is_periodical:
        #     if self.opts.output_profile.epub_periodical_format == 'sony':
        #         from calibre.ebooks.epub.periodical import sony_metadata
        #         metadata_xml, atom_xml = sony_metadata(oeb)
        #         extra_entries = [('atom.xml', 'application/atom+xml', atom_xml)]
        oeb_output = OEBOutput()
        oeb_output.convert(oeb, tdir, None, opts)
        opf = [x for x in os.listdir(tdir) if x.endswith('.opf')][0]
        if opts.pretty_print:
            condense_ncx([os.path.join(tdir, x) for x in os.listdir(tdir) if x.endswith('.ncx')][0])
        from . import initialize_container
        with initialize_container(output_path, os.path.basename(opf),
                extra_entries=extra_entries) as epub:
            epub.add_dir(tdir)
            if metadata_xml is not None:
                epub.writestr('META-INF/metadata.xml',
                        metadata_xml.encode('utf-8'))

def condense_ncx(ncx_path):
    tree = etree.parse(ncx_path)
    for tag in tree.getroot().iter(tag=etree.Element):
        if tag.text:
            tag.text = tag.text.strip()
        if tag.tail:
            tag.tail = tag.tail.strip()
    compressed = etree.tostring(tree.getroot(), encoding='utf-8')
    open(ncx_path, 'wb').write(compressed)

def workaround_ade_quirks(oeb):
    '''
    Perform various markup transforms to get the output to render correctly
    in the quirky ADE.
    '''
    from ..oeb.base import XPath, XHTML, OEB_STYLES, barename, urlunquote

    stylesheet = None
    for item in oeb.manifest:
        if item.media_type.lower() in OEB_STYLES:
            stylesheet = item
            break

    # ADE cries big wet tears when it encounters an invalid fragment
    # identifier in the NCX toc.
    frag_pat = re.compile(r'[-A-Za-z0-9_:.]+$')
    for node in oeb.toc.iter():
        href = getattr(node, 'href', None)
        if hasattr(href, 'partition'):
            base, _, frag = href.partition('#')
            frag = urlunquote(frag)
            if frag and frag_pat.match(frag) is None:
                logging.warn('Removing invalid fragment identifier %r from TOC'%frag)
                node.href = base

    for x in oeb.spine:
        root = x.data
        body = XPath('//h:body')(root)
        if body:
            body = body[0]

        if hasattr(body, 'xpath'):
            # remove <img> tags with empty src elements
            bad = []
            for x in XPath('//h:img')(body):
                src = x.get('src', '').strip()
                if src in ('', '#') or src.startswith('http:'):
                    bad.append(x)
            for img in bad:
                img.getparent().remove(img)

            # Add id attribute to <a> tags that have name
            for x in XPath('//h:a[@name]')(body):
                if not x.get('id', False):
                    x.set('id', x.get('name'))

            # Replace <br> that are children of <body> as ADE doesn't handle them
            for br in XPath('./h:br')(body):
                if br.getparent() is None:
                    continue
                try:
                    prior = br.itersiblings(preceding=True).next()
                    priortag = barename(prior.tag)
                    priortext = prior.tail
                except:
                    priortag = 'body'
                    priortext = body.text
                if priortext:
                    priortext = priortext.strip()
                br.tag = XHTML('p')
                br.text = u'\u00a0'
                style = br.get('style', '').split(';')
                style = filter(None, map(lambda x: x.strip(), style))
                style.append('margin:0pt; border:0pt')
                # If the prior tag is a block (including a <br> we replaced)
                # then this <br> replacement should have a 1-line height.
                # Otherwise it should have no height.
                if not priortext and priortag in block_level_tags:
                    style.append('height:1em')
                else:
                    style.append('height:0pt')
                br.set('style', '; '.join(style))

        for tag in XPath('//h:embed')(root):
            tag.getparent().remove(tag)
        for tag in XPath('//h:object')(root):
            if tag.get('type', '').lower().strip() in ('image/svg+xml',):
                continue
            tag.getparent().remove(tag)

        for tag in XPath('//h:title|//h:style')(root):
            if not tag.text:
                tag.getparent().remove(tag)
        for tag in XPath('//h:script')(root):
            if not tag.text and not tag.get('src', False):
                tag.getparent().remove(tag)
        for tag in XPath('//h:body/descendant::h:script')(root):
            tag.getparent().remove(tag)

        for tag in XPath('//h:form')(root):
            tag.getparent().remove(tag)

        for tag in XPath('//h:center')(root):
            tag.tag = XHTML('div')
            tag.set('style', 'text-align:center')
        # ADE can't handle &amp; in an img url
        for tag in XPath('//h:img[@src]')(root):
            tag.set('src', tag.get('src', '').replace('&', ''))

        # ADE whimpers in fright when it encounters a <td> outside a
        # <table>
        in_table = XPath('ancestor::h:table')
        for tag in XPath('//h:td|//h:tr|//h:th')(root):
            if not in_table(tag):
                tag.tag = XHTML('div')

        special_chars = re.compile(u'[\u200b\u00ad]')
        for elem in root.iterdescendants():
            if getattr(elem, 'text', False):
                elem.text = special_chars.sub('', elem.text)
                elem.text = elem.text.replace(u'\u2011', '-')
            if getattr(elem, 'tail', False):
                elem.tail = special_chars.sub('', elem.tail)
                elem.tail = elem.tail.replace(u'\u2011', '-')

        if stylesheet is not None:
            # ADE doesn't render lists correctly if they have left margins
            from cssutils.css import CSSRule
            for lb in XPath('//h:ul[@class]|//h:ol[@class]')(root):
                sel = '.'+lb.get('class')
                for rule in stylesheet.data.cssRules.rulesOfType(CSSRule.STYLE_RULE):
                    if sel == rule.selectorList.selectorText:
                        rule.style.removeProperty('margin-left')
                        # padding-left breaks rendering in webkit and gecko
                        rule.style.removeProperty('padding-left')
            # Change whitespace:pre to pre-wrap to accommodate readers that
            # cannot scroll horizontally
            for rule in stylesheet.data.cssRules.rulesOfType(CSSRule.STYLE_RULE):
                style = rule.style
                ws = style.getPropertyValue('white-space')
                if ws == 'pre':
                    style.setProperty('white-space', 'pre-wrap')

def workaround_sony_quirks(oeb):
    '''
    Perform toc link transforms to alleviate slow loading.
    '''
    from ..oeb.base import urldefrag, XPath

    def frag_is_at_top(root, frag):
        body = XPath('//h:body')(root)
        if body:
            body = body[0]
        else:
            return False
        tree = body.getroottree()
        elem = XPath('//*[@id="%s" or @name="%s"]'%(frag, frag))(root)
        if elem:
            elem = elem[0]
        else:
            return False
        path = tree.getpath(elem)
        for el in body.iterdescendants():
            epath = tree.getpath(el)
            if epath == path:
                break
            if el.text and el.text.strip():
                return False
            if not path.startswith(epath):
                # Only check tail of non-parent elements
                if el.tail and el.tail.strip():
                    return False
        return True

    def simplify_toc_entry(toc):
        if toc.href:
            href, frag = urldefrag(toc.href)
            if frag:
                for x in oeb.spine:
                    if x.href == href:
                        if frag_is_at_top(x.data, frag):
                            logging.debug('Removing anchor from TOC href:',
                                    href+'#'+frag)
                            toc.href = href
                        break
        for x in toc:
            simplify_toc_entry(x)

    if oeb.toc:
        simplify_toc_entry(oeb.toc)

