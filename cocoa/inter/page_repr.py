# Created By: Virgil Dupras
# Created On: 2011-08-01
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from hscommon.cocoa.inter import signature, PyGUIObject

from core.gui.page_repr import PageRepresentation

class PyPageRepr(PyGUIObject):
    py_class = PageRepresentation
    
    @signature('v@:ff')
    def drawWithViewWidth_height_(self, view_width, view_height):
        self.py.draw(view_width, view_height)
    
    @signature('v@:ff')
    def mouseDownAtX_y_(self, x, y):
        self.py.mouse_down(x, y)
    
    @signature('v@:ff')
    def mouseMoveAtX_y_(self, x, y):
        self.py.mouse_move(x, y)
    
    def mouseUp(self):
        self.py.mouse_up()
    
    def prevPage(self):
        self.py.prev_page()
    
    def nextPage(self):
        self.py.next_page()
    
    @signature('v@:c')
    def setShiftKeyHeld_(self, value):
        self.py.shift_key_held = value
    
    #--- model -> view calls:
    def draw_rectangle(self, x, y, width, height, bgcolor, pencolor):
        if bgcolor is None:
            bgcolor = -1
        if pencolor is None:
            pencolor = -1
        self.cocoa.drawRectAtX_y_width_height_bgColor_penColor_(
            x, y, width, height, bgcolor, pencolor)
    
    def draw_arrow(self, x1, y1, x2, y2, width, color):
        self.cocoa.drawArrowFromX_y_toX_y_width_color_(
            x1, y1, x2, y2, width, color)
    
