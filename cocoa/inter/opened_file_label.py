# Created By: Virgil Dupras
# Created On: 2011-06-19
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

from hscommon.cocoa.inter import PyGUIObject

from core.gui.opened_file_label import OpenedFileLabel

class PyOpenedFileLabel(PyGUIObject):
    py_class = OpenedFileLabel
    
    def text(self):
        return self.py.text
    
    def setText_(self, value):
        self.py.text = str(value)
    
