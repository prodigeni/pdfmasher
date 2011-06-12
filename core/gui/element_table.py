# Created By: Virgil Dupras
# Created On: 2011-06-12
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from operator import attrgetter

from hscommon.gui.table import GUITable, Row

from .base import GUIObject

class ElementRow(Row):
    def __init__(self, table, element):
        Row.__init__(self, table)
        self._element = element
        # simply take all attributes of the element and set them in the row
        for attr, value in element.__dict__.items():
            setattr(self, attr, value)
    

class ElementTable(GUIObject, GUITable):
    def __init__(self, view, app):
        GUIObject.__init__(self, view, app)
        GUITable.__init__(self)
    
    #--- Override
    def _fill(self):
        for element in self.app.elements:
            self.append(ElementRow(self, element))
    
    #--- Event Handlers
    def elements_changed(self):
        self.refresh()
    
