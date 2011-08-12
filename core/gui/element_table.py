# Created By: Virgil Dupras
# Created On: 2011-06-12
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

from hscommon.gui.table import GUITable, Row

from ..const import ElementState, SHORTCUTKEY2FLAG
from .base import GUIObject

class ElementRow(Row):
    def __init__(self, table, element):
        Row.__init__(self, table)
        self.element = element
        self._order = element.order
        self._page = element.page
        self._x = element.x
        self._y = element.y
        self._fontsize = element.fontsize
        self._text_length = len(element.text)
        self.text = element.text.replace('\n', ' ')
        self._state = element.state
        
        # Format
        self.order = "{:d}".format(self._order)
        self.page = "{:d}".format(self._page)
        self.x = "{:.0f}".format(self._x)
        self.y = "{:.0f}".format(self._y)
        self.fontsize = "{:0.1f}".format(self._fontsize)
        self.text_length = "{:d}".format(self._text_length)
        statetext = self._state.capitalize()
        if self._state == ElementState.Title:
            self.state = "{} ({})".format(statetext, self.element.title_level)
        else:
            self.state = statetext
    
    def sort_key_for_column(self, column_name):
        if column_name == 'order':
            return (self._page, self._order)
        elif column_name == 'state':
            if self._state == ElementState.Title:
                return (self._state, self.element.title_level)
            else:
                return (self._state, 0)
        else:
            return Row.sort_key_for_column(self, column_name)
    

class ElementTable(GUIObject, GUITable):
    #--- model -> view calls:
    # refresh()
    #
    
    def __init__(self, view, app):
        GUIObject.__init__(self, view, app)
        GUITable.__init__(self)
    
    #--- Override
    def _fill(self):
        elements = self.app.elements
        if self.app.hide_ignored:
            elements = [e for e in elements if e.state != ElementState.Ignored]
        for element in elements:
            self.append(ElementRow(self, element))
    
    def _update_selection(self):
        # Takes the table's selection and does appropriates updates on the Document's side.
        elements = {row.element for row in self.selected_rows}
        self.app.select_elements(elements)
    
    #--- Public
    def press_key(self, key):
        key = key.upper()
        if key not in SHORTCUTKEY2FLAG:
            return
        state = SHORTCUTKEY2FLAG[key]
        self.app.change_state_of_selected(state)
    
    #--- Event Handlers
    def elements_changed(self):
        self.refresh()
    
    def elements_selected(self):
        selected_elements = self.app.selected_elements
        selected_indexes = []
        for index, row in enumerate(self):
            if row.element in selected_elements:
                selected_indexes.append(index)
        if selected_indexes != self.selected_indexes:
            self.selected_indexes = selected_indexes
            self.view.refresh()
    
