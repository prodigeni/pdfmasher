# Created By: Virgil Dupras
# Created On: 2011-06-12
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

import os.path as op

from hscommon.notify import Broadcaster

from .pdf import extract_text_elements_from_pdf
from .html import generate_html

class App(Broadcaster):
    def __init__(self):
        Broadcaster.__init__(self)
        self._current_path = None
        self._selected_elements = []
        self.elements = []
    
    def build_html(self):
        assert self._current_path
        without_ext, ext = op.splitext(self._current_path)
        dest_path = without_ext + '.htm'
        with open(dest_path, 'wt', encoding='utf-8') as fp:
            fp.write(generate_html(self.elements))
        return dest_path
    
    def change_state_of_selected(self, newstate):
        for element in self._selected_elements:
            element.state = newstate
        self.notify('elements_changed')
    
    def open_file(self, path):
        self.elements = extract_text_elements_from_pdf(path)
        self._current_path = path
        self.notify('elements_changed')
    
    def select_elements(self, elements):
        self._selected_elements = elements
    
