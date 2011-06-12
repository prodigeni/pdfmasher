# Created By: Virgil Dupras
# Created On: 2011-06-12
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from hscommon.notify import Broadcaster

from .pdf import extract_text_elements

class App(Broadcaster):
    def __init__(self):
        Broadcaster.__init__(self)
        self.elements = []
    
    def open_file(self, path):
        self.elements = extract_text_elements(path)
        self.notify('elements_changed')
    
