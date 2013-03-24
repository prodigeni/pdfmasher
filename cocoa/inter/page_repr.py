# Created By: Virgil Dupras
# Created On: 2011-08-01
# Copyright 2013 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

from objp.util import dontwrap, nspoint, nsrect
from cocoa.inter import PyGUIObject, GUIObjectView

class PageReprView(GUIObjectView):
    def drawRect_bgColor_penColor_(self, rect: nsrect, bgcolor: int, pencolor: int): pass
    def drawArrowFrom_to_width_color_(self, src: nspoint, dst: nspoint, width: float, color: int): pass
    def drawText_inRect_(self, text: str, rect: nsrect): pass

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
        if bgcolor is None:
            bgcolor = -1
        if pencolor is None:
            pencolor = -1
        self.callback.drawRect_bgColor_penColor_(rect, bgcolor, pencolor)
    
    @dontwrap
    def draw_arrow(self, line, width, color):
        src, dst = line
        self.callback.drawArrowFrom_to_width_color_(src, dst, width, color)
    
    @dontwrap
    def draw_text(self, text, rect):
        self.callback.drawText_inRect_(text, rect)
    
