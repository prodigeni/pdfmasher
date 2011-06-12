# Created By: Virgil Dupras
# Created On: 2011-06-12
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from hscommon.notify import Broadcaster

from .pdf import extract_text_elements
from .html import generate_html

class App(Broadcaster):
    def __init__(self):
        Broadcaster.__init__(self)
        self._selected_elements = []
        self.elements = []
    
    def build_html(self):
        with open('foo.html', 'wt', encoding='utf-8') as fp:
            fp.write(generate_html(self.elements))
    
    def change_state_of_selected(self, newstate):
        for element in self._selected_elements:
            element.state = newstate
        self.notify('elements_changed')
    
    def open_file(self, path):
        self.elements = extract_text_elements(path)
        self.notify('elements_changed')
    
    def select_elements(self, elements):
        self._selected_elements = elements
    
