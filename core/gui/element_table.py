# Created By: Virgil Dupras
# Created On: 2011-06-12
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from hscommon.gui.table import GUITable, Row

from .base import GUIObject

class ElementRow(Row):
    def __init__(self, table, element):
        Row.__init__(self, table)
        self.element = element
        self._id = element.id
        self._page = element.page
        self._x = element.x0
        self._y = element.y0
        self._font_height = element.avgheight
        self.text = element.text
        self.state = element.state
        
        # Format
        self.id = "{:d}".format(self._id)
        self.page = "{:d}".format(self._page)
        self.x = "{:.0f}".format(self._x)
        self.y = "{:.0f}".format(self._y)
        self.font_height = "{:0.1f}".format(self._font_height)
        
    

class ElementTable(GUIObject, GUITable):
    def __init__(self, view, app):
        GUIObject.__init__(self, view, app)
        GUITable.__init__(self)
    
    #--- Override
    def _fill(self):
        for element in self.app.elements:
            self.append(ElementRow(self, element))
    
    def _update_selection(self):
        # Takes the table's selection and does appropriates updates on the Document's side.
        elements = [row.element for row in self.selected_rows]
        self.app.select_elements(elements)
    
    #--- Event Handlers
    def elements_changed(self):
        self.refresh()
    
