# Created By: Virgil Dupras
# Created On: 2011-07-22
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from ..pdf import ElementState

# The view has the responsibility of determining specific colors, but when we send draw_* messages
# to our view, we still give a color category. These categories are defined here.
class PageColor:
    PageBg = 1
    PageBorder = 2
    ElemNormal = 100
    ElemSelected = 101
    ElemIgnored = 102
    MouseSelection = 200

#XXX use a proper geometry library... planar (http://pygamesf.org/~casey/planar/doc/)?

def rect2pts(r):
    x, y, w, h = r
    return x, y, x+w, y+h

def rect_from_corners(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return (min(x1, x2), min(y1, y2), abs(x1-x2), abs(y1-y2))

def rects_intersect(r1, r2):
    r1x1, r1y1, r1x2, r1y2 = rect2pts(r1)
    r2x1, r2y1, r2x2, r2y2 = rect2pts(r2)
    if r1x1 < r2x1:
        xinter = r1x2 >= r2x1
    else:
        xinter = r2x2 >= r1x1
    if not xinter:
        return False
    if r1y1 < r2y1:
        yinter = r1y2 >= r2y1
    else:
        yinter = r2y2 >= r1y1
    return yinter

class PageRepresentation:
    #--- model -> view calls:
    # refresh()
    # draw_rectangle(x, y, width, height, bgcolor, pencolor)
    #
    
    def __init__(self, view, app):
        self.app = app
        self.view = view
        self._pageno = 0
        self.page = None
        self.elements = None
        self._last_mouse_down = None
        self._last_mouse_pos = None
        self._last_page_boundaries = None
        self._elem2drawrect = None
    
    #--- Private
    def _compute_elem_drawrect(self, page_boundaries):
        if self._last_page_boundaries == page_boundaries:
            return
        self._last_page_boundaries = page_boundaries
        px, py, pw, ph = page_boundaries
        self._elem2drawrect = {}
        xratio = pw / self.page.width
        yratio = ph / self.page.height
        for elem in self.elements:
            if elem.state == ElementState.Ignored and self.app.hide_ignored:
                continue # we don't draw the elem
            lelem = elem.layout_elem
            adjx = px + (lelem.x0 * xratio)
            # don't forget that ypos in pdfminer are inverted
            adjy = py + (ph - (lelem.y1 * yratio))
            adjw = lelem.width * xratio
            adjh = lelem.height * yratio
            self._elem2drawrect[elem] = (adjx, adjy, adjw, adjh)
    
    def _get_page_boundaries(self, view_width, view_height):
        pagewidth = self.page.width
        pageheight = self.page.height
        ratio = pageheight / pagewidth
        # somehow, if we don't put the '-1's, the (bottom/right)most pixel line gets cropped.
        width = view_width - 1
        height = view_height - 1
        if width * ratio > height:
            # Our constraint is height, adjust according to it
            adjusted_width = height / ratio
            adjusted_height = height - 2 # give some room for page boundaries line width
            x = (width - adjusted_width) / 2
            y = 1
        else:
            # Our constraint is width, adjust according to it
            adjusted_width = width - 2
            adjusted_height = width * ratio
            x = 1
            y = (height - adjusted_height) / 2
        return x, y, adjusted_width, adjusted_height
    
    def _select_elems_in_rect(self, r):
        toselect = set()
        for elem, elem_rect in self._elem2drawrect.items():
            if rects_intersect(r, elem_rect):
                toselect.add(elem)
        self.app.select_elements(toselect)
    
    #--- Public
    def draw(self, view_width, view_height):
        if self.page is None:
            return
        px, py, pw, ph = self._get_page_boundaries(view_width, view_height)
        # draw the page itself
        self.view.draw_rectangle(px, py, pw, ph, PageColor.PageBg, PageColor.PageBorder)
        # now draw the elements
        self._compute_elem_drawrect((px, py, pw, ph))
        todraw = (e for e in self.elements if e in self._elem2drawrect)
        for elem in todraw:
            adjx, adjy, adjw, adjh = self._elem2drawrect[elem]
            color = PageColor.ElemNormal
            if elem.state == ElementState.Ignored:
                color = PageColor.ElemIgnored
            if elem in self.app.selected_elements:
                color = PageColor.ElemSelected
            self.view.draw_rectangle(adjx, adjy, adjw, adjh, None, color)
        if self._last_mouse_down and self._last_mouse_pos:
            rx, ry, rw, rh = rect_from_corners(self._last_mouse_down, self._last_mouse_pos)
            self.view.draw_rectangle(rx, ry, rw, rh, None, PageColor.MouseSelection)
    
    def mouse_down(self, x, y):
        self._last_mouse_down = (x, y)
        self._last_mouse_pos = (x, y)
        self.view.refresh()
    
    def mouse_move(self, x, y):
        # only call when the mouse button is currently down
        self._last_mouse_pos = (x, y)
        self.view.refresh()
    
    def mouse_up(self):
        r = rect_from_corners(self._last_mouse_down, self._last_mouse_pos)
        self._select_elems_in_rect(r)
        self._last_mouse_down = None
        self._last_mouse_pos = None
        self.view.refresh()
    
    def update_page(self):
        if self.app.pages:
            self.page = self.app.pages[self.pageno]
            self.elements = [e for e in self.app.elements if e.page == self.pageno]
        else:
            self.page = None
            self.elements = None
        self._last_page_boundaries = None
        self._elem2drawrect = None
        self.view.refresh()
    
    #--- Properties
    @property
    def pageno(self):
        return self._pageno
    
    @pageno.setter
    def pageno(self, value):
        if 0 <= value < len(self.app.pages):
            self._pageno = value
            self.update_page()
    
