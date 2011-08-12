# Copyright 2008, Kovid Goyal <kovid at kovidgoyal.net>
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license


'''
Try to read metadata from an HTML file.
'''

import re

from . import MetaInformation
from ..utils import entity_to_unicode

def get_metadata(stream):
    src = stream.read()
    return get_metadata_(src, 'utf-8')

def get_meta_regexp_(name):
    return re.compile('<meta name=[\'"]' + name + '[\'"] content=[\'"](.+?)[\'"]\s*/?>', re.IGNORECASE)

def get_metadata_(src, encoding):
    if not isinstance(src, str):
        assert encoding
        src = src.decode(encoding, 'replace')

    # Meta data definitions as in
    # http://www.mobileread.com/forums/showpost.php?p=712544&postcount=9

    # Title
    title = None
    pat = re.compile(r'<!--.*?TITLE=(?P<q>[\'"])(.+?)(?P=q).*?-->', re.DOTALL)
    match = pat.search(src)
    if match:
        title = match.group(2)
    else:
        for x in ('DC.title','DCTERMS.title','Title'):
            pat = get_meta_regexp_(x)
            match = pat.search(src)
            if match:
                title = match.group(1)
                break
    if not title:
        pat = re.compile('<title>([^<>]+?)</title>', re.IGNORECASE)
        match = pat.search(src)
        if match:
            title = match.group(1)

    # Author
    author = None
    pat = re.compile(r'<!--.*?AUTHOR=(?P<q>[\'"])(.+?)(?P=q).*?-->', re.DOTALL)
    match = pat.search(src)
    if match:
        author = match.group(2).replace(',', ';')
    else:
        for x in ('Author','DC.creator.aut','DCTERMS.creator.aut', 'DC.creator'):
            pat = get_meta_regexp_(x)
            match = pat.search(src)
            if match:
                author = match.group(1)
                break

    # Create MetaInformation with Title and Author
    ent_pat = re.compile(r'&(\S+)?;')
    if title:
        title = ent_pat.sub(entity_to_unicode, title)
    if author:
        author = ent_pat.sub(entity_to_unicode, author)
    return MetaInformation(title, [author] if author else None)
