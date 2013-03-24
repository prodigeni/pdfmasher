# Created By: Virgil Dupras
# Created On: 2011-07-09
# Copyright 2013 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

import os.path as op
from datetime import datetime

import markdown
from ebooks.html.input import HTMLInput
from ebooks.mobi.output import convert as convert2mobi
from ebooks.epub.output import convert as convert2epub
from ebooks.metadata.book import Metadata

from ..output import generate_markdown, wrap_html
from .base import GUIObject

class EbookType:
    MOBI = 1
    EPUB = 2

class BuildPane(GUIObject):
    #--- model -> view calls:
    # refresh() (for generation label and post processing buttons)
    #
    
    def __init__(self, app):
        GUIObject.__init__(self, app)
        self.lastgen_desc = ''
        self.post_processing_enabled = False
        self.selected_ebook_type = EbookType.MOBI
        self.ebook_title = ''
        self.ebook_author = ''
    
    def _view_updated(self):
        self.view.refresh()
    
    #--- Private
    def _current_path(self, ext):
        assert self.app.current_path
        without_ext, _ = op.splitext(self.app.current_path)
        return without_ext + '.' + ext
    
    def _generate_html(self):
        md_path = self._current_path('txt')
        with open(md_path, 'rt', encoding='utf-8') as fp:
            md_contents = fp.read()
        html_body = markdown.markdown(md_contents)
        dest_path = self._current_path('htm')
        with open(dest_path, 'wt', encoding='utf-8') as fp:
            fp.write(wrap_html(html_body, 'utf-8'))
        return dest_path
    
    #--- Public
    def generate_markdown(self):
        dest_path = self._current_path('txt')
        with open(dest_path, 'wt', encoding='utf-8') as fp:
            fp.write(generate_markdown(self.app.elements))
        self.lastgen_desc = 'Generated at {}'.format(datetime.now().strftime('%H:%M:%S'))
        self.post_processing_enabled = True
        self.view.refresh()
    
    def edit_markdown(self):
        md_path = self._current_path('txt')
        self.app.open_path(md_path)
    
    def reveal_markdown(self):
        md_path = self._current_path('txt')
        self.app.reveal_path(md_path)
    
    def view_html(self):
        self.app.open_path(self._generate_html())
    
    def create_ebook(self):
        allowed_ext = 'mobi' if self.selected_ebook_type == EbookType.MOBI else 'epub'
        path = self.app.view.query_save_path("Select a destination for the e-book", [allowed_ext])
        if not path:
            return
        hi = HTMLInput()
        html_path = self._generate_html()
        mi = Metadata(self.ebook_title, [self.ebook_author])
        oeb = hi.create_oebbook(html_path, mi)
        if self.selected_ebook_type == EbookType.EPUB:
            convert2epub(oeb, path)
        else:
            convert2mobi(oeb, path)
    
    #--- Events
    def file_opened(self):
        self.lastgen_desc = ''
        self.post_processing_enabled = False
        self.view.refresh()
    
