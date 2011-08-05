# Created By: Virgil Dupras
# Created On: 2011-07-09
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

import os.path as op
from datetime import datetime

import markdown

from ..output import generate_markdown, wrap_html
from .base import GUIObject

FAIRWARE_NOTICE = """
Fairware Notice
===

This document was generated with an unregistered version of PdfMasher at a moment when development
hours invested in it were not fully funded.

Although PdfMasher is open source, it's also [fairware](http://open.hardcoded.net/about/) and
contributions are *expected* when there are development hours to compensate. I'm sorry to have to
nag you like this, but despite high usage of PdfMasher, I can't seem to get adequate funding for it.
I'm not a volunteer, I expect my development time to be paid. Without funding, PdfMasher development
and support will stop.

If you're just trying PdfMasher to see if it works for you, no problem, go ahead. However, if
PdfMasher is useful to you, please [contribute](http://open.hardcoded.net/contribute/). If you can't
afford to contribute, [let me know](mailto:hsoft@hardcoded.net), I'll send you a key.

This message doesn't show up when you have a valid contribution key or when there are no development
hours to compensate.

"""

class BuildPane(GUIObject):
    #--- model -> view calls:
    # refresh() (for generation label and post processing buttons)
    #
    
    def __init__(self, view, app):
        GUIObject.__init__(self, view, app)
        self.lastgen_desc = ''
        self.post_processing_enabled = False
    
    def connect(self):
        GUIObject.connect(self)
        self.view.refresh()
    
    #--- Private
    def _current_path(self, ext):
        assert self.app.current_path
        without_ext, _ = op.splitext(self.app.current_path)
        return without_ext + '.' + ext
    
    #--- Public
    def generate_markdown(self):
        dest_path = self._current_path('txt')
        with open(dest_path, 'wt', encoding='utf-8') as fp:
            fp.write(generate_markdown(self.app.elements))
        self.lastgen_desc = '{} generated at {}'.format(dest_path, datetime.now().strftime('%H:%M:%S'))
        self.post_processing_enabled = True
        self.view.refresh()
    
    def edit_markdown(self):
        md_path = self._current_path('txt')
        self.app.open_path(md_path)
    
    def reveal_markdown(self):
        md_path = self._current_path('txt')
        self.app.reveal_path(md_path)
    
    def view_html(self):
        md_path = self._current_path('txt')
        with open(md_path, 'rt', encoding='utf-8') as fp:
            md_contents = fp.read()
        if not self.app.registered and self.app.unpaid_hours >= 1:
            md_contents = FAIRWARE_NOTICE + md_contents
        html_body = markdown.markdown(md_contents)
        dest_path = self._current_path('htm')
        with open(dest_path, 'wt', encoding='utf-8') as fp:
            fp.write(wrap_html(html_body, 'utf-8'))
        self.app.open_path(dest_path)
    
    #--- Events
    def file_opened(self):
        self.lastgen_desc = ''
        self.post_processing_enabled = False
        self.view.refresh()
    