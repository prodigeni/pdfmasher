# Created By: Virgil Dupras
# Created On: 2011-08-04
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

from hscommon.cocoa.inter import PyGUIObject, signature, subproxy

from .page_repr import PyPageRepr

class PyPageController(PyGUIObject):
    pageRepr = subproxy('pageRepr', 'page_repr', PyPageRepr)
    
    def prevPage(self):
        self.py.prev_page()
    
    def nextPage(self):
        self.py.next_page()
    
    def pageLabel(self):
        return self.py.page_label
    
    @signature('v@:c')
    def setReorderMode_(self, flag):
        self.py.page_repr.reorder_mode = flag
    
    #--- model -> view calls:
    def refresh_page_label(self):
        self.cocoa.refreshPageLabel()
    
