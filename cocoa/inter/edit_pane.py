# Created By: Virgil Dupras
# Created On: 2011-06-19
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

from hscommon.cocoa.inter import signature, PyGUIObject

class PyEditPane(PyGUIObject):
    def editText(self):
        return self.py.edit_text
    
    def setEditText_(self, value):
        self.py.edit_text = str(value)
    
    @signature('c@:')
    def editEnabled(self):
        return self.py.edit_enabled
    
    def saveEdits(self):
        self.py.save_edits()
    
    def cancelEdits(self):
        self.py.cancel_edits()
    
    #--- model -> view calls:
    def refresh_edit_text(self):
        self.cocoa.refreshEditText()
    
