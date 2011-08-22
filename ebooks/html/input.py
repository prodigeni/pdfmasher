# Copyright 2009, Kovid Goyal <kovid@kovidgoyal.net>
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

import os, re, sys, uuid, tempfile
from urllib.parse import urlparse, urlunparse
from urllib.parse import unquote
from functools import partial
import cssutils
import logging

from ..oeb.base import (OEBBook, DirContainer, rewrite_links, urlnormalize, urldefrag, BINARY_MIME,
    OEB_STYLES, xpath)
from ..conversion.preprocess import HTMLPreProcessor
from ..constants import islinux, isbsd, iswindows
from ..utils import unicode_path, as_unicode
from ..utils.mimetypes import guess_type
from ..oeb.transforms.metadata import meta_info_to_oeb_metadata

class Link:
    '''
    Represents a link in a HTML file.
    '''

    @classmethod
    def url_to_local_path(cls, url, base):
        path = url.path
        isabs = False
        if iswindows and path.startswith('/'):
            path = path[1:]
            isabs = True
        path = urlunparse(('', '', path, url.params, url.query, ''))
        path = unquote(path)
        if isabs or os.path.isabs(path):
            return path
        return os.path.abspath(os.path.join(base, path))

    def __init__(self, url, base):
        '''
        :param url:  The url this link points to. Must be an unquoted unicode string.
        :param base: The base directory that relative URLs are with respect to.
                     Must be a unicode string.
        '''
        assert isinstance(url, str) and isinstance(base, str)
        self.url         = url
        self.parsed_url  = urlparse(self.url)
        self.is_local    = self.parsed_url.scheme in ('', 'file')
        self.is_internal = self.is_local and not bool(self.parsed_url.path)
        self.path        = None
        self.fragment    = unquote(self.parsed_url.fragment)
        if self.is_local and not self.is_internal:
            self.path = self.url_to_local_path(self.parsed_url, base)

    def __hash__(self):
        if self.path is None:
            return hash(self.url)
        return hash(self.path)

    def __eq__(self, other):
        return self.path == getattr(other, 'path', other)

    def __str__(self):
        return 'Link: %s --> %s'%(self.url, self.path)


class IgnoreFile(Exception):
    def __init__(self, msg, errno):
        Exception.__init__(self, msg)
        self.doesnt_exist = errno == 2
        self.errno = errno

class HTMLFile:
    '''
    Contains basic information about an HTML file. This
    includes a list of links to other files as well as
    the encoding of each file. Also tries to detect if the file is not a HTML
    file in which case :member:`is_binary` is set to True.

    The encoding of the file is available as :member:`encoding`.
    '''

    HTML_PAT  = re.compile(r'<\s*html', re.IGNORECASE)
    TITLE_PAT = re.compile('<title>([^<>]+)</title>', re.IGNORECASE)
    LINK_PAT  = re.compile(
    r'<\s*a\s+.*?href\s*=\s*(?:(?:"(?P<url1>[^"]+)")|(?:\'(?P<url2>[^\']+)\')|(?P<url3>[^\s>]+))',
    re.DOTALL|re.IGNORECASE)

    def __init__(self, path_to_html_file, level, encoding, verbose, referrer=None):
        '''
        :param level: The level of this file. Should be 0 for the root file.
        :param encoding: Use `encoding` to decode HTML.
        :param referrer: The :class:`HTMLFile` that first refers to this file.
        '''
        self.path     = unicode_path(path_to_html_file, abs=True)
        self.title    = os.path.splitext(os.path.basename(self.path))[0]
        self.base     = os.path.dirname(self.path)
        self.level    = level
        self.referrer = referrer
        self.links    = []

        try:
            with open(self.path, 'rb') as f:
                src = f.read()
        except IOError as err:
            msg = 'Could not read from file: %s with error: %s'%(self.path, as_unicode(err))
            if level == 0:
                raise IOError(msg)
            raise IgnoreFile(msg, err.errno)

        self.is_binary = level > 0 and not bool(self.HTML_PAT.search(src[:4096]))
        if not self.is_binary:
            assert encoding
            self.encoding = encoding

            src = src.decode(encoding, 'replace')
            match = self.TITLE_PAT.search(src)
            self.title = match.group(1) if match is not None else self.title
            self.find_links(src)

    def __eq__(self, other):
        return self.path == getattr(other, 'path', other)
    
    def __hash__(self):
        return object.__hash__(self)
    
    def __str__(self):
        return 'HTMLFile:%d:%s:%s'%(self.level, 'b' if self.is_binary else 'a', self.path)

    def __repr__(self):
        return str(self)


    def find_links(self, src):
        for match in self.LINK_PAT.finditer(src):
            url = None
            for i in ('url1', 'url2', 'url3'):
                url = match.group(i)
                if url:
                    break
            link = self.resolve(url)
            if link not in self.links:
                self.links.append(link)

    def resolve(self, url):
        return Link(url, self.base)


def depth_first(root, flat, visited=set()):
    yield root
    visited.add(root)
    for link in root.links:
        if link.path is not None and link not in visited:
            try:
                index = flat.index(link)
            except ValueError: # Can happen if max_levels is used
                continue
            hf = flat[index]
            if hf not in visited:
                yield hf
                visited.add(hf)
                for hf in depth_first(hf, flat, visited):
                    if hf not in visited:
                        yield hf
                        visited.add(hf)


def traverse(path_to_html_file, max_levels=sys.maxsize, verbose=0, encoding=None):
    '''
    Recursively traverse all links in the HTML file.

    :param max_levels: Maximum levels of recursion. Must be non-negative. 0
                       implies that no links in the root HTML file are followed.
    :param encoding:   Specify character encoding of HTML files. If `None` it is
                       auto-detected.
    :return:           A pair of lists (breadth_first, depth_first). Each list contains
                       :class:`HTMLFile` objects.
    '''
    assert max_levels >= 0
    level = 0
    flat =  [HTMLFile(path_to_html_file, level, encoding, verbose)]
    next_level = list(flat)
    while level < max_levels and len(next_level) > 0:
        level += 1
        nl = []
        for hf in next_level:
            rejects = []
            for link in hf.links:
                if link.path is None or link.path in flat:
                    continue
                try:
                    nf = HTMLFile(link.path, level, encoding, verbose, referrer=hf)
                    if nf.is_binary:
                        raise IgnoreFile('%s is a binary file'%nf.path, -1)
                    nl.append(nf)
                    flat.append(nf)
                except IgnoreFile as err:
                    rejects.append(link)
                    if not err.doesnt_exist or verbose > 1:
                        print(repr(err))
            for link in rejects:
                hf.links.remove(link)

        next_level = list(nl)
    orec = sys.getrecursionlimit()
    sys.setrecursionlimit(500000)
    try:
        return flat, list(depth_first(flat[0], flat))
    finally:
        sys.setrecursionlimit(orec)


def get_filelist(htmlfile, dir, encoding='utf-8', max_levels=999, breadth_first=False, verbose=0):
    '''
    Build list of files referenced by html file or try to detect and use an
    OPF file instead.
    '''
    logging.info('Building file list...')
    filelist = traverse(htmlfile, max_levels=int(max_levels),
                        verbose=verbose,
                        encoding=encoding)[0 if breadth_first else 1]
    if verbose:
        logging.debug('\tFound files...')
        for f in filelist:
            logging.debug('\t\t%s', f)
    return filelist

def find_headers(html, header_tags=('h1', 'h2')):
    result = []
    predicate = ' or '.join('name()=\'{}\''.format(tag) for tag in header_tags)
    expr = '/h:html/h:body//h:*[{}]'.format(predicate)
    result = xpath(html, expr)
    return result

class HTMLInput:
    def is_case_sensitive(self, path):
        if getattr(self, '_is_case_sensitive', None) is not None:
            return self._is_case_sensitive
        if not path or not os.path.exists(path):
            return islinux or isbsd
        self._is_case_sensitive = not (os.path.exists(path.lower()) \
                and os.path.exists(path.upper()))
        return self._is_case_sensitive

    def create_oebbook(self, htmlpath, mi, encoding='utf-8', pretty_print=False):
        cssutils.log.setLevel(logging.WARN)
        self.OEB_STYLES = OEB_STYLES
        basedir = os.path.dirname(htmlpath)
        html_preprocessor = HTMLPreProcessor()
        assert encoding
        oeb = OEBBook(html_preprocessor, pretty_print=pretty_print, input_encoding=encoding)
        self.oeb = oeb

        metadata = oeb.metadata
        meta_info_to_oeb_metadata(mi, metadata)
        if not metadata.language:
            logging.warn('Language not specified')
            metadata.add('language', 'en')
        if not metadata.creator:
            logging.warn('Creator not specified')
            metadata.add('creator', 'Unknown')
        if not metadata.title:
            logging.warn('Title not specified')
            metadata.add('title', 'Unknown')
        bookid = str(uuid.uuid4())
        metadata.add('identifier', bookid, id='uuid_id', scheme='uuid')
        for ident in metadata.identifier:
            if 'id' in ident.attrib:
                self.oeb.uid = metadata.identifier[0]
                break

        filelist = get_filelist(htmlpath, basedir)
        filelist = [f for f in filelist if not f.is_binary]
        htmlfile_map = {}
        for f in filelist:
            path = f.path
            oeb.container = DirContainer(os.path.dirname(path), ignore_opf=True)
            bname = os.path.basename(path)
            id, href = oeb.manifest.generate(id='html', href=bname)
            htmlfile_map[path] = href
            item = oeb.manifest.add(id, href, 'text/html')
            item.html_input_href = bname
            oeb.spine.add(item, True)

        self.added_resources = {}
        for path, href in list(htmlfile_map.items()):
            if not self.is_case_sensitive(path):
                path = path.lower()
            self.added_resources[path] = href
        self.urlnormalize, self.DirContainer = urlnormalize, DirContainer
        self.urldefrag = urldefrag
        self.guess_type, self.BINARY_MIME = guess_type, BINARY_MIME

        for f in filelist:
            path = f.path
            dpath = os.path.dirname(path)
            oeb.container = DirContainer(dpath, ignore_opf=True)
            item = oeb.manifest.hrefs[htmlfile_map[path]]
            rewrite_links(item.data, partial(self.resource_adder, base=dpath))

        for item in list(oeb.manifest.values()):
            if item.media_type in self.OEB_STYLES:
                dpath = None
                for path, href in list(self.added_resources.items()):
                    if href == item.href:
                        dpath = os.path.dirname(path)
                        break
                cssutils.replaceUrls(item.data, partial(self.resource_adder, base=dpath))

        toc = self.oeb.toc
        headers = []
        for item in self.oeb.spine:
            if not item.linear:
                continue
            html = item.data
            for header in find_headers(html):
                headers.append((item, header))
        for i, (item, header) in enumerate(headers):
            if not item.linear:
                continue
            tocid = 'tocid{}'.format(i)
            header.attrib['id'] = tocid
            link = '{}#{}'.format(item.href, tocid)
            toc.add(header.text, link)
        oeb.container = DirContainer(os.getcwd(), ignore_opf=True)
        return oeb

    def link_to_local_path(self, link_, base=None):
        if not isinstance(link_, str):
            try:
                link_ = link_.decode('utf-8', 'error')
            except Exception:
                logging.warn('Failed to decode link %r. Ignoring', link_)
                return None, None
        try:
            l = Link(link_, base if base else os.getcwd())
        except Exception:
            logging.exception('Failed to process link: %r', link_)
            return None, None
        if l.path is None:
            # Not a local resource
            return None, None
        link = l.path.replace('/', os.sep).strip()
        frag = l.fragment
        if not link:
            return None, None
        return link, frag

    def resource_adder(self, link_, base=None):
        link, frag = self.link_to_local_path(link_, base=base)
        if link is None:
            return link_
        try:
            if base and not os.path.isabs(link):
                link = os.path.join(base, link)
            link = os.path.abspath(link)
        except:
            return link_
        if not os.access(link, os.R_OK):
            return link_
        if os.path.isdir(link):
            logging.warn('%r is a link to a directory. Ignoring.', link_)
            return link_
        if not self.is_case_sensitive(tempfile.gettempdir()):
            link = link.lower()
        if link not in self.added_resources:
            bhref = os.path.basename(link)
            id, href = self.oeb.manifest.generate(id='added',
                    href=bhref)
            guessed = self.guess_type(href)[0]
            media_type = guessed or self.BINARY_MIME
            if media_type == 'text/plain':
                logging.warn('Ignoring link to text file %r', link_)
                return None

            self.oeb.log.debug('Added', link)
            self.oeb.container = self.DirContainer(os.path.dirname(link),
                    self.oeb.log, ignore_opf=True)
            # Load into memory
            item = self.oeb.manifest.add(id, href, media_type)
            item.html_input_href = bhref
            if guessed in self.OEB_STYLES:
                item.override_css_fetch = partial(
                        self.css_import_handler, os.path.dirname(link))
            item.data
            self.added_resources[link] = href

        nlink = self.added_resources[link]
        if frag:
            nlink = '#'.join((nlink, frag))
        return nlink

    def css_import_handler(self, base, href):
        link, frag = self.link_to_local_path(href, base=base)
        if link is None or not os.access(link, os.R_OK) or os.path.isdir(link):
            return (None, None)
        try:
            raw = open(link, 'rb').read().decode('utf-8', 'replace')
            raw = self.oeb.css_preprocessor(raw, add_namespace=True)
        except:
            logging.exception('Failed to read CSS file: %r', link)
            return (None, None)
        return (None, raw)
