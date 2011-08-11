# -*- coding: utf-8 -*-
__license__ = 'GPL 3'
__copyright__ = '2009, Kovid Goyal <kovid@kovidgoyal.net>'
__docformat__ = 'restructuredtext en'

import os, re, sys, shutil, pprint

# from ..customize.conversion import OptionRecommendation, DummyReporter
# from ..customize.ui import input_profiles, output_profiles, \
#         plugin_for_input_format, plugin_for_output_format, \
#         available_input_formats, available_output_formats, \
#         run_plugins_on_preprocess, run_plugins_on_postprocess
from .preprocess import HTMLPreProcessor
# from ..ptempfile import PersistentTemporaryDirectory
# from ..utils.date import parse_date
# from ..utils.zipfile import ZipFile
# from ..utils import extract, walk, isbytestring, filesystem_encoding, get_types_map
# from ..constants import __version__

class OptionValues(object):
    pass

def create_oebbook(path_or_stream, opts, reader=None,
        encoding='utf-8', populate=True):
    '''
    Create an OEBBook.
    '''
    from ..oeb.base import OEBBook
    html_preprocessor = HTMLPreProcessor(opts)
    if not encoding:
        encoding = None
    oeb = OEBBook(html_preprocessor, pretty_print=opts.pretty_print, input_encoding=encoding)
    if not populate:
        return oeb
    # Read OEB Book into OEBBook
    logging.info('Parsing all content...')
    if reader is None:
        from ..oeb.reader import OEBReader
        reader = OEBReader

    reader()(oeb, path_or_stream)
    return oeb
