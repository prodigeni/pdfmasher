# Created By: Virgil Dupras
# Created On: 2011-08-04
# Copyright 2013 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

from objp.util import pyref, dontwrap
from cocoa.inter import PyGUIObject, GUIObjectView

class PageControllerView(GUIObjectView):
    def refreshPageLabel(self): pass

class PyPageController(PyGUIObject):
    def pageRepr(self) -> pyref:
        return self.model.page_repr
    
    def prevPage(self):
        self.model.prev_page()
    
    def nextPage(self):
        self.model.next_page()
    
    def pageLabel(self) -> str:
        return self.model.page_label
    
    def setReorderMode_(self, flag: bool):
        self.model.page_repr.reorder_mode = flag
    
    #--- model -> view calls:
    @dontwrap
    def refresh_page_label(self):
        self.callback.refreshPageLabel()
    
