# -*- coding: utf-8 -*-

__license__ = 'GPL 3'
__copyright__ = '2010, Hiroshi Miura <miurahr@linux.com>'
__docformat__ = 'restructuredtext en'
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
