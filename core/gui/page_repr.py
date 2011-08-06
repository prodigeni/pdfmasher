# Created By: Virgil Dupras
# Created On: 2011-07-22
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from hscommon.geometry import Point, Line, Rect
from hscommon.util import trailiter, dedupe
from ..pdf import ElementState

# The view has the responsibility of determining specific colors, but when we send draw_* messages
# to our view, we still give a color category. These categories are defined here.
class PageColor:
    PageBg = 1
    PageBorder = 2
    ElemNormal = 100
    ElemSelected = 101
    ElemIgnored = 102
    ElemOrderArrow = 200
    MouseSelection = 300

class PageRepresentation:
    #--- model -> view calls:
    # refresh()
    # draw_rectangle(x, y, width, height, bgcolor, pencolor)
    # draw_arrow(x1, y1, x2, y2, width, color)
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
        self._reorder_mode = False
    
    #--- Private
    def _active_elems(self):
        return (e for e in self.elements if e.state != ElementState.Ignored)
    
    def _ignored_elems(self):
        return (e for e in self.elements if e.state == ElementState.Ignored)
    
    def _ordered_elems(self):
        # ignored elements are not part of the order
        sort_key = lambda e: e.order
        return sorted(self._active_elems(), key=sort_key)
    
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
            self._elem2drawrect[elem] = Rect(adjx, adjy, adjw, adjh)
    
    def _draw_mouse_selection(self):
        if self._last_mouse_down and self._last_mouse_pos:
            if self._reorder_mode:
                x1, y1 = self._last_mouse_down
                x2, y2 = self._last_mouse_pos
                linewidth = 5
                self.view.draw_arrow(x1, y1, x2, y2, linewidth, PageColor.MouseSelection)
            else:
                rx, ry, rw, rh = Rect.from_corners(self._last_mouse_down, self._last_mouse_pos)
                self.view.draw_rectangle(rx, ry, rw, rh, None, PageColor.MouseSelection)
    
    def _draw_order_arrows(self, elems):
        for elem1, elem2 in trailiter(self._ordered_elems(), skipfirst=True):
            x1, y1 = self._elem2drawrect[elem1].center()
            x2, y2 = self._elem2drawrect[elem2].center()
            linewidth = 1
            self.view.draw_arrow(x1, y1, x2, y2, linewidth, PageColor.ElemOrderArrow)
    
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
    
    def _reorder_following_line(self, reorder_line):
        # Reordering from a line is a bit more complex than it seems. We have to find intersection
        # points from all lines in all rects (when there's an interestion, of course). Then, for
        # each intersection, we compute the distance of it from the origin of the order arrow.
        # We sort our elements by that distance and we have our new order!
        intersections = []
        for elem in self._active_elems():
            rect = self._elem2drawrect[elem]
            for line in rect.lines():
                inter = reorder_line.intersection_point(line)
                if inter is not None:
                    dist = inter.distance_to(reorder_line.p1)
                    intersections.append((dist, elem))
        if len(intersections) < 2:
            return # nothing to reorder
        intersections.sort(key=lambda tup: tup[0])
        neworder = dedupe([elem for dist, elem in intersections])
        # ok, we have our new order. That was easy huh? Now, what we have to do is to insert that
        # new order in the rest of the elements, which might not all be in our new order. So we have
        # to find our insertion point, divide it into a 'before' and an 'after' list, remove all our
        # newly ordered elems from those lists, and do a before + neworder + after concat.
        all_elems = list(self._ordered_elems())
        first = neworder[0]
        insertion_point = all_elems.index(first)
        before = all_elems[:insertion_point]
        after = all_elems[insertion_point:]
        affected_elems = set(neworder)
        before = [e for e in before if e not in affected_elems]
        after = [e for e in after if e not in affected_elems]
        # we also add ignore elems to our big concat so that their order value doesn't conflict
        ignored = list(self._ignored_elems())
        concat = before + neworder + after + ignored
        for i, elem in enumerate(concat):
            elem.order = i
    
    def _select_elems_in_rect(self, r):
        toselect = set()
        for elem, elem_rect in self._elem2drawrect.items():
            if r.intersects(elem_rect):
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
        todraw = [e for e in self.elements if e in self._elem2drawrect]
        for elem in todraw:
            adjx, adjy, adjw, adjh = self._elem2drawrect[elem]
            color = PageColor.ElemNormal
            if elem.state == ElementState.Ignored:
                color = PageColor.ElemIgnored
            if elem in self.app.selected_elements:
                color = PageColor.ElemSelected
            self.view.draw_rectangle(adjx, adjy, adjw, adjh, None, color)
        if self._reorder_mode:
            self._draw_order_arrows(todraw)
        self._draw_mouse_selection()
    
    def mouse_down(self, x, y):
        self._last_mouse_down = Point(x, y)
        self._last_mouse_pos = Point(x, y)
        self.view.refresh()
    
    def mouse_move(self, x, y):
        # only call when the mouse button is currently down
        self._last_mouse_pos = Point(x, y)
        self.view.refresh()
    
    def mouse_up(self):
        if self.page is not None:
            if self._reorder_mode:
                self._reorder_following_line(Line(self._last_mouse_down, self._last_mouse_pos))
            else:
                r = Rect.from_corners(self._last_mouse_down, self._last_mouse_pos)
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
    
    @property
    def pageno(self):
        return self._pageno
    
    @pageno.setter
    def pageno(self, value):
        if 0 <= value < len(self.app.pages):
            self._pageno = value
            self.update_page()
    
    @property
    def reorder_mode(self):
        return self._reorder_mode
    
    @reorder_mode.setter
    def reorder_mode(self, value):
        if value == self._reorder_mode:
            return
        self._reorder_mode = value
        self.view.refresh()
