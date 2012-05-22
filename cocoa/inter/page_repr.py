# Created By: Virgil Dupras
# Created On: 2011-08-01
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

from objp.util import dontwrap
from cocoa.inter import PyGUIObject, GUIObjectView

class PageReprView(GUIObjectView):
    def drawRectAtX_y_width_height_bgColor_penColor_(self, x: float, y: float, width: float, height: float, bgcolor: int, pencolor: int): pass
    def drawArrowFromX_y_toX_y_width_color_(self, x1: float, y1: float, x2: float, y2: float, width: float, color: int): pass
    def drawText_inRectAtX_y_width_height_(self, text: str, x: float, y: float, width: float, height: float): pass

class PyPageRepr(PyGUIObject):
    def drawWithViewWidth_height_(self, view_width: float, view_height: float):
        self.model.draw(view_width, view_height)
    
    def mouseDownAtX_y_(self, x: float, y: float):
        self.model.mouse_down(x, y)
    
    def mouseMoveAtX_y_(self, x: float, y: float):
        self.model.mouse_move(x, y)
    
    def mouseUp(self):
        self.model.mouse_up()
    
    def prevPage(self):
        self.model.prev_page()
    
    def nextPage(self):
        self.model.next_page()
    
    def setShiftKeyHeld_(self, value: bool):
        self.model.shift_key_held = value
    
    def pressKey_(self, key: str):
        self.model.press_key(key)
    
    #--- model -> view calls:
    @dontwrap
    def draw_rectangle(self, rect, bgcolor, pencolor):
        x, y, width, height = rect
        if bgcolor is None:
            bgcolor = -1
        if pencolor is None:
            pencolor = -1
        self.callback.drawRectAtX_y_width_height_bgColor_penColor_(
            x, y, width, height, bgcolor, pencolor)
    
    @dontwrap
    def draw_arrow(self, line, width, color):
        (x1, y1), (x2, y2) = line
        self.callback.drawArrowFromX_y_toX_y_width_color_(x1, y1, x2, y2, width, color)
    
    @dontwrap
    def draw_text(self, text, rect):
        x, y, width, height = rect
        self.callback.drawText_inRectAtX_y_width_height_(text, x, y, width, height)
    
