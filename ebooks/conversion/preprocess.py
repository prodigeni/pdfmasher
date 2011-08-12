# Copyright 2009, Kovid Goyal <kovid@kovidgoyal.net>
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

import functools, re
import logging

from ..utils import entity_to_unicode, as_unicode

XMLDECL_RE    = re.compile(r'^\s*<[?]xml.*?[?]>')
SVG_NS       = 'http://www.w3.org/2000/svg'
XLINK_NS     = 'http://www.w3.org/1999/xlink'

convert_entities = functools.partial(entity_to_unicode,
        result_exceptions = {
            u'<' : '&lt;',
            u'>' : '&gt;',
            u"'" : '&apos;',
            u'"' : '&quot;',
            u'&' : '&amp;',
        })

LIGATURES = {
#        u'\u00c6': u'AE',
#        u'\u00e6': u'ae',
#        u'\u0152': u'OE',
#        u'\u0153': u'oe',
#        u'\u0132': u'IJ',
#        u'\u0133': u'ij',
#        u'\u1D6B': u'ue',
        u'\uFB00': u'ff',
        u'\uFB01': u'fi',
        u'\uFB02': u'fl',
        u'\uFB03': u'ffi',
        u'\uFB04': u'ffl',
        u'\uFB05': u'ft',
        u'\uFB06': u'st',
        }

_ligpat = re.compile(u'|'.join(LIGATURES))

class CSSPreProcessor(object):

    PAGE_PAT   = re.compile(r'@page[^{]*?{[^}]*?}')
    # Remove some of the broken CSS Microsoft products
    # create
    MS_PAT     = re.compile(r'''
        (?P<start>^|;|\{)\s*    # The end of the previous rule or block start
        (%s).+?                 # The invalid selectors
        (?P<end>$|;|\})         # The end of the declaration
        '''%'mso-|panose-|text-underline|tab-interval',
        re.MULTILINE|re.IGNORECASE|re.VERBOSE)

    def ms_sub(self, match):
        end = match.group('end')
        try:
            start = match.group('start')
        except:
            start = ''
        if end == ';':
            end = ''
        return start + end

    def __call__(self, data, add_namespace=False):
        from ..oeb.base import XHTML_CSS_NAMESPACE
        data = self.PAGE_PAT.sub('', data)
        data = self.MS_PAT.sub(self.ms_sub, data)
        if not add_namespace:
            return data
        ans, namespaced = [], False
        for line in data.splitlines():
            ll = line.lstrip()
            if not (namespaced or ll.startswith('@import') or
                        ll.startswith('@charset')):
                ans.append(XHTML_CSS_NAMESPACE.strip())
                namespaced = True
            ans.append(line)

        return u'\n'.join(ans)

class HTMLPreProcessor(object):

    PREPROCESS = [
                  # Convert all entities, since lxml doesn't handle them well
                  (re.compile(r'&(\S+?);'), convert_entities),
                  ]
    
    def __init__(self, extra_opts=None):
        self.extra_opts = extra_opts

    def __call__(self, html, remove_special_chars=None,
            get_preprocess_html=False):
        if remove_special_chars is not None:
            html = remove_special_chars.sub('', html)
        html = html.replace('\0', '')
        rules = []

        start_rules = []
        if not getattr(self.extra_opts, 'keep_ligatures', False):
            html = _ligpat.sub(lambda m:LIGATURES[m.group()], html)

        for search, replace in [['sr3_search', 'sr3_replace'], ['sr2_search', 'sr2_replace'], ['sr1_search', 'sr1_replace']]:
            search_pattern = getattr(self.extra_opts, search, '')
            if search_pattern:
                try:
                    search_re = re.compile(search_pattern)
                    replace_txt = getattr(self.extra_opts, replace, '')
                    if not replace_txt:
                        replace_txt = ''
                    rules.insert(0, (search_re, replace_txt))
                except Exception as e:
                    logging.error('Failed to parse %r regexp because %s', (search, as_unicode(e)))

        end_rules = []

        for rule in self.PREPROCESS + start_rules:
            html = rule[0].sub(rule[1], html)

        if get_preprocess_html:
            return html

        for rule in rules + end_rules:
            html = rule[0].sub(rule[1], html)

        html = XMLDECL_RE.sub('', html)
        return html
    
