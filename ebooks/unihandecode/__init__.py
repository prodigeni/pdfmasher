# Copyright 2010, Hiroshi Miura <miurahr@linux.com>
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

from __future__ import unicode_literals

__all__ = ["Unihandecoder"]

'''
Decode unicode text to an ASCII representation of the text.
Translate unicode characters to ASCII.

Inspired from John Schember's unidecode library which was created as part
of calibre.

Copyright(c) 2009, John Schember

Tranliterate the string from unicode characters to ASCII in Chinese and others.

'''
import unicodedata

class Unihandecoder(object):
    preferred_encoding = None
    decoder = None

    def __init__(self, encoding='utf-8'):
        self.preferred_encoding = encoding
        from .unidecoder import Unidecoder
        self.decoder = Unidecoder()

    def decode(self, text):
        try:
            unicode # python2
            if not isinstance(text, unicode):
                try:
                    text = unicode(text)
                except:
                    try:
                        text = text.decode(self.preferred_encoding)
                    except:
                        text = text.decode('utf-8', 'replace')
        except: # python3, str is unicode
            pass
        #at first unicode normalize it. (see Unicode standards)
        ntext = unicodedata.normalize('NFKC', text)
        return self.decoder.decode(ntext)
