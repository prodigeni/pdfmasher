# Copyright 2010, Kovid Goyal <kovid at kovidgoyal.net>
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license



import os, glob, re, functools
from urllib.parse import urlparse
from urllib.parse import unquote
from uuid import uuid4

from lxml import etree
from lxml.builder import ElementMaker

from ..constants import __appname__, __version__

NCX_NS = "http://www.daisy.org/z3986/2005/ncx/"
CALIBRE_NS = "http://calibre.kovidgoyal.net/2009/metadata"
NSMAP = {
            None: NCX_NS,
            'calibre':CALIBRE_NS
            }


E = ElementMaker(namespace=NCX_NS, nsmap=NSMAP)

C = ElementMaker(namespace=CALIBRE_NS, nsmap=NSMAP)


class TOC(list):

    def __init__(self, href=None, fragment=None, text=None, parent=None, play_order=0,
                 base_path=os.getcwd(), type='unknown', author=None,
                 description=None):
        self.href = href
        self.fragment = fragment
        if not self.fragment:
            self.fragment = None
        self.text = text
        self.parent = parent
        self.base_path = base_path
        self.play_order = play_order
        self.type = type
        self.author = author
        self.description = description

    def __str__(self):
        lines = ['TOC: %s#%s'%(self.href, self.fragment)]
        for child in self:
            c = str(child).splitlines()
            for l in c:
                lines.append('\t'+l)
        return '\n'.join(lines)

    def count(self, type):
        return len([i for i in self.flat() if i.type == type])

    def purge(self, types, max=0):
        remove = []
        for entry in self.flat():
            if entry.type in types:
                remove.append(entry)
        remove = remove[max:]
        for entry in remove:
            if entry.parent is None:
                continue
            entry.parent.remove(entry)
        return remove

    def remove(self, entry):
        list.remove(self, entry)
        entry.parent = None

    def add_item(self, href, fragment, text, play_order=None, type='unknown',
            author=None, description=None):
        if play_order is None:
            play_order = (self[-1].play_order if len(self) else self.play_order) + 1
        self.append(TOC(href=href, fragment=fragment, text=text, parent=self,
                        base_path=self.base_path, play_order=play_order,
                        type=type, author=author, description=description))
        return self[-1]

    def top_level_items(self):
        for item in self:
            if item.text is not None:
                yield item

    def depth(self):
        depth = 1
        for obj in self:
            c = obj.depth()
            if c > depth - 1:
                depth = c + 1
        return depth

    def flat(self):
        'Depth first iteration over the tree rooted at self'
        yield self
        for obj in self:
            for i in obj.flat():
                yield i

    @dynamic_property
    def abspath(self):
        doc='Return the file this toc entry points to as a absolute path to a file on the system.'
        def fget(self):
            if self.href is None:
                return None
            path = self.href.replace('/', os.sep)
            if not os.path.isabs(path):
                path = os.path.join(self.base_path, path)
            return path

        return property(fget=fget, doc=doc)

    def read_html_toc(self, toc):
        self.base_path = os.path.dirname(toc)
        # XXX Use xml based reader, pdf masher output is valid xhtml
        # soup = BeautifulSoup(open(toc, 'rb').read(), convertEntities=BeautifulSoup.HTML_ENTITIES)
        # for a in soup.findAll('a'):
        #     if not a.has_key('href'):
        #         continue
        #     purl = urlparse(unquote(a['href']))
        #     href, fragment = purl[2], purl[5]
        #     if not fragment:
        #         fragment = None
        #     else:
        #         fragment = fragment.strip()
        #     href = href.strip()
        # 
        #     txt = ''.join([unicode(s).strip() for s in a.findAll(text=True)])
        #     add = True
        #     for i in self.flat():
        #         if i.href == href and i.fragment == fragment:
        #             add = False
        #             break
        #     if add:
        #         self.add_item(href, fragment, txt)

    def render(self, stream, uid):
        root = E.ncx(
                E.head(
                    E.meta(name='dtb:uid', content=str(uid)),
                    E.meta(name='dtb:depth', content=str(self.depth())),
                    E.meta(name='dtb:generator', content='%s (%s)'%(__appname__,
                        __version__)),
                    E.meta(name='dtb:totalPageCount', content='0'),
                    E.meta(name='dtb:maxPageNumber', content='0'),
                ),
                E.docTitle(E.text('Table of Contents')),
        )
        navmap = E.navMap()
        root.append(navmap)
        root.set('{http://www.w3.org/XML/1998/namespace}lang', 'en')

        def navpoint(parent, np):
            text = np.text
            if not text:
                text = ''
            elem = E.navPoint(
                    E.navLabel(E.text(re.sub(r'\s+', ' ', text))),
                    E.content(src=str(np.href)+(('#' + str(np.fragment))
                        if np.fragment else '')),
                    id=str(uuid4()),
                    playOrder=str(np.play_order)
            )
            au = getattr(np, 'author', None)
            if au:
                au = re.sub(r'\s+', ' ', au)
                elem.append(C.meta(au, name='author'))
            desc = getattr(np, 'description', None)
            if desc:
                desc = re.sub(r'\s+', ' ', desc)
                elem.append(C.meta(desc, name='description'))
            parent.append(elem)
            for np2 in np:
                navpoint(elem, np2)

        for np in self:
            navpoint(navmap, np)
        raw = etree.tostring(root, encoding='utf-8', xml_declaration=True,
                pretty_print=True)
        stream.write(raw)
