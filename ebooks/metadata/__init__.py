# Copyright 2008, Kovid Goyal kovid@kovidgoyal.net
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license



import os, sys, re
from urllib.parse import unquote, quote
from urllib.parse import urlparse

from ..utils import relpath, remove_bracketed_text
from ..utils.mimetypes import guess_type

_author_pat = re.compile(',?\s+(and|with)\s+', re.IGNORECASE)
def string_to_authors(raw):
    raw = raw.replace('&&', '\uffff')
    raw = _author_pat.sub('&', raw)
    authors = [a.strip().replace('\uffff', '&') for a in raw.split('&')]
    return [a for a in authors if a]

def authors_to_string(authors):
    if authors is not None:
        return ' & '.join([a.replace('&', '&&') for a in authors if a])
    else:
        return ''

_title_pat = re.compile(r'^(A|The|An)\s+', re.IGNORECASE)
_ignore_starts = '\'"'+''.join(chr(x) for x in list(range(0x2018, 0x201e))+[0x2032, 0x2033])

def title_sort(title, order=None):
    if order is None:
        order = 'library_order'
    title = title.strip()
    if order == 'strictly_alphabetic':
        return title
    if title and title[0] in _ignore_starts:
        title = title[1:]
    match = _title_pat.search(title)
    if match:
        prep = match.group(1)
        title = title[len(prep):] + ', ' + prep
    return title.strip()

coding = list(zip(
[1000,900,500,400,100,90,50,40,10,9,5,4,1],
["M","CM","D","CD","C","XC","L","XL","X","IX","V","IV","I"]
))



def roman(num):
    if num <= 0 or num >= 4000 or int(num) != num:
        return str(num)
    result = []
    for d, r in coding:
        while num >= d:
            result.append(r)
            num -= d
    return ''.join(result)


def fmt_sidx(i, fmt='%.2f', use_roman=False):
    if i is None or i == '':
        i = 1
    try:
        i = float(i)
    except TypeError:
        return str(i)
    if int(i) == float(i):
        return roman(int(i)) if use_roman else '%d'%int(i)
    return fmt%i

class Resource(object):
    '''
    Represents a resource (usually a file on the filesystem or a URL pointing
    to the web. Such resources are commonly referred to in OPF files.

    They have the interface:

    :member:`path`
    :member:`mime_type`
    :method:`href`

    '''

    def __init__(self, href_or_path, basedir=os.getcwd(), is_path=True):
        self._href = None
        self._basedir = basedir
        self.path = None
        self.fragment = ''
        try:
            self.mime_type = guess_type(href_or_path)[0]
        except:
            self.mime_type = None
        if self.mime_type is None:
            self.mime_type = 'application/octet-stream'
        if is_path:
            path = href_or_path
            if not os.path.isabs(path):
                path = os.path.abspath(os.path.join(basedir, path))
            if isinstance(path, str):
                path = path.decode(sys.getfilesystemencoding())
            self.path = path
        else:
            url = urlparse(href_or_path)
            if url[0] not in ('', 'file'):
                self._href = href_or_path
            else:
                pc = url[2]
                if isinstance(pc, str):
                    pc = pc.encode('utf-8')
                pc = unquote(pc).decode('utf-8')
                self.path = os.path.abspath(os.path.join(basedir, pc.replace('/', os.sep)))
                self.fragment = unquote(url[-1])


    def href(self, basedir=None):
        '''
        Return a URL pointing to this resource. If it is a file on the filesystem
        the URL is relative to `basedir`.

        `basedir`: If None, the basedir of this resource is used (see :method:`set_basedir`).
        If this resource has no basedir, then the current working directory is used as the basedir.
        '''
        if basedir is None:
            if self._basedir:
                basedir = self._basedir
            else:
                basedir = os.getcwd()
        if self.path is None:
            return self._href
        f = self.fragment.encode('utf-8') if isinstance(self.fragment, str) else self.fragment
        frag = '#'+quote(f) if self.fragment else ''
        if self.path == basedir:
            return ''+frag
        try:
            rpath = relpath(self.path, basedir)
        except OSError: # On windows path and basedir could be on different drives
            rpath = self.path
        if isinstance(rpath, str):
            rpath = rpath.encode('utf-8')
        return quote(rpath.replace(os.sep, '/'))+frag

    def set_basedir(self, path):
        self._basedir = path

    def basedir(self):
        return self._basedir

    def __repr__(self):
        return 'Resource(%s, %s)'%(repr(self.path), repr(self.href()))


class ResourceCollection(object):

    def __init__(self):
        self._resources = []

    def __iter__(self):
        for r in self._resources:
            yield r

    def __len__(self):
        return len(self._resources)

    def __getitem__(self, index):
        return self._resources[index]

    def __bool__(self):
        return len(self._resources) > 0

    def __str__(self):
        resources = list(map(repr, self))
        return '[%s]'%', '.join(resources)

    def __repr__(self):
        return str(self)

    def append(self, resource):
        if not isinstance(resource, Resource):
            raise ValueError('Can only append objects of type Resource')
        self._resources.append(resource)

    def remove(self, resource):
        self._resources.remove(resource)

    def replace(self, start, end, items):
        'Same as list[start:end] = items'
        self._resources[start:end] = items

    @staticmethod
    def from_directory_contents(top, topdown=True):
        collection = ResourceCollection()
        for spec in os.walk(top, topdown=topdown):
            path = os.path.abspath(os.path.join(spec[0], spec[1]))
            res = Resource.from_path(path)
            res.set_basedir(top)
            collection.append(res)
        return collection

    def set_basedir(self, path):
        for res in self:
            res.set_basedir(path)



def MetaInformation(title, authors=('Unknown',)):
    ''' Convenient encapsulation of book metadata, needed for compatibility
        @param title: title or ``_('Unknown')`` or a MetaInformation object
        @param authors: List of strings or []
    '''
    from .book.base import Metadata
    mi = None
    if hasattr(title, 'title') and hasattr(title, 'authors'):
        mi = title
        title = mi.title
        authors = mi.authors
    return Metadata(title, authors, other=mi)

