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
        self.page = element.page
        self.x0 = int(element.x0)
        self.y0 = int(element.y0)
        self.x1 = int(element.x1)
        self.y1 = int(element.y1)
        self.text = element.text
    

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
    
