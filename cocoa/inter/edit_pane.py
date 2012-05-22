# Created By: Virgil Dupras
# Created On: 2011-06-19
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

from objp.util import dontwrap
from cocoa.inter import PyGUIObject, GUIObjectView

class EditPaneView(GUIObjectView):
    def refreshEditText(seld): pass

class PyEditPane(PyGUIObject):
    def editText(self) -> str:
        return self.model.edit_text
    
    def setEditText_(self, value: str):
        self.model.edit_text = value
    
    def editEnabled(self) -> bool:
        return self.model.edit_enabled
    
    def saveEdits(self):
        self.model.save_edits()
    
    def cancelEdits(self):
        self.model.cancel_edits()
    
    #--- model -> view calls:
    @dontwrap
    def refresh_edit_text(self):
        self.callback.refreshEditText()
    
