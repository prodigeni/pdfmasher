# Created By: Virgil Dupras
# Created On: 2011-08-01
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

from cocoa.inter import signature, PyGUIObject

class PyPageRepr(PyGUIObject):
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
    
    def pressKey_(self, key):
        self.py.press_key(key)
    
    #--- model -> view calls:
    def draw_rectangle(self, rect, bgcolor, pencolor):
        x, y, width, height = rect
        if bgcolor is None:
            bgcolor = -1
        if pencolor is None:
            pencolor = -1
        self.cocoa.drawRectAtX_y_width_height_bgColor_penColor_(
            x, y, width, height, bgcolor, pencolor)
    
    def draw_arrow(self, line, width, color):
        (x1, y1), (x2, y2) = line
        self.cocoa.drawArrowFromX_y_toX_y_width_color_(x1, y1, x2, y2, width, color)
    
    def draw_text(self, text, rect):
        x, y, width, height = rect
        self.cocoa.drawText_inRectAtX_y_width_height_(text, x, y, width, height)
    
