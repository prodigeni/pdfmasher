# Created By: Virgil Dupras
# Created On: 2011-06-18
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

from .base import GUIObject

from hscommon.util import first

class EditPane(GUIObject):
    #--- model -> view calls:
    # refresh_edit_text()
    #
    
    def __init__(self, view, app):
        GUIObject.__init__(self, view, app)
        self.edit_text = ''
        self.edit_enabled = False
    
    def connect(self):
        GUIObject.connect(self)
        self.view.refresh_edit_text()
    
    #--- Public
    def save_edits(self):
        elements = self.app.selected_elements
        len(elements) == 1
        first(elements).text = self.edit_text
        # XXX Ok, this is a horrible hack, but I'll straighten this out later
        # we need to refresh the elements table
        self.app.notify('elements_changed')
    
    def cancel_edits(self):
        self.elements_selected()
    
    #--- Events
    def elements_selected(self):
        elements = self.app.selected_elements
        self.edit_enabled = False
        if not elements:
            self.edit_text = ''
        elif len(elements) == 1:
            self.edit_text = first(elements).text
            self.edit_enabled = True
        else:
            self.edit_text = "(Multiple selection)"
        self.view.refresh_edit_text()
    
