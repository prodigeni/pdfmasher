# Created By: Virgil Dupras
# Created On: 2011-07-22
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from hscommon.geometry import Point, Line, Rect
from hscommon.util import trailiter, dedupe

from ..const import ElementState, SHORTCUTKEY2FLAG

# The view has the responsibility of determining specific colors, but when we send draw_* messages
# to our view, we still give a color category. These categories are defined here.
class PageColor:
    PageBg = 1
    PageBorder = 2
    ElemNormal = 100
    ElemTitle = 101
    ElemFootnote = 102
    ElemIgnored = 103
    ElemToFix = 104
    ElemSelected = 105
    ElemOrderArrow = 200
    MouseSelection = 300

STATE2COLOR = {
    ElementState.Title: PageColor.ElemTitle,
    ElementState.Footnote: PageColor.ElemFootnote,
    ElementState.Ignored: PageColor.ElemIgnored,
    ElementState.ToFix: PageColor.ElemToFix,
}

class PageRepresentation:
    #--- model -> view calls:
    # refresh()
    # draw_rectangle(rect, bgcolor, pencolor)
    # draw_arrow(line, width, color)
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
        self._shift_key_held = False
        # The buffer to hold reordering lines when the user holds shift while re-ordering
        self._reorder_line_buffer = []
    
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
                p1 = self._last_mouse_down
                p2 = self._last_mouse_pos
                linewidth = 5
                self.view.draw_arrow(Line(p1, p2), linewidth, PageColor.MouseSelection)
            else:
                r = Rect.from_corners(self._last_mouse_down, self._last_mouse_pos)
                self.view.draw_rectangle(r, None, PageColor.MouseSelection)
    
    def _draw_order_arrows(self):
        elems = list(self._ordered_elems())
        if not elems:
            return
        # mark the starting pos
        firstelem = elems[0]
        center = self._elem2drawrect[firstelem].center()
        r = Rect.from_center(center, 10, 10)
        self.view.draw_rectangle(r, PageColor.ElemOrderArrow, None)
        linewidth = 1
        for elem1, elem2 in trailiter(elems, skipfirst=True):
            p1 = self._elem2drawrect[elem1].center()
            p2 = self._elem2drawrect[elem2].center()
            self.view.draw_arrow(Line(p1, p2), linewidth, PageColor.ElemOrderArrow)
        linewidth = 5
        for line in self._reorder_line_buffer:
            self.view.draw_arrow(line, linewidth, PageColor.ElemOrderArrow)
    
    def _get_intersections(self, reorder_line):
        # return a list of elements that intersect with line, in order. The order depends on the
        # distance of the elem's first intersection with the line's origin
        intersections = []
        for elem in self._active_elems():
            rect = self._elem2drawrect[elem]
            for line in rect.lines():
                inter = reorder_line.intersection_point(line)
                if inter is not None:
                    dist = inter.distance_to(reorder_line.p1)
                    intersections.append((dist, elem))
        if not intersections:
            # so we cross no line, but we might be in the middle of an elem, in which case we should
            # return that elem. It's even possible that we're inside multiple rects. This case is
            # tricky (there's multiple possibilities here). We just choose the elem for which the
            # center is closest to our origin
            origin = reorder_line.p1
            for elem in self._active_elems():
                rect = self._elem2drawrect[elem]
                if rect.contains_point(origin):
                    intersections.append((origin.distance_to(rect.center()), elem))
        intersections.sort(key=lambda tup: tup[0])
        return dedupe([elem for dist, elem in intersections])
    
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
    
    def _handle_drag_completion(self):
        if self._reorder_mode:
            reorder_line = Line(self._last_mouse_down, self._last_mouse_pos)
            if self.shift_key_held:
                self._reorder_line_buffer.append(reorder_line)
            else:
                self._reorder_following_line([reorder_line])
        else:
            r = Rect.from_corners(self._last_mouse_down, self._last_mouse_pos)
            self._select_elems_in_rect(r)
    
    def _reorder_following_line(self, reorder_lines):
        # Reordering from a line is a bit more complex than it seems. We have to find intersection
        # points from all lines in all rects (when there's an interestion, of course). Then, for
        # each intersection, we compute the distance of it from the origin of the order arrow.
        # We sort our elements by that distance and we have our new order!
        neworder = []
        for reorder_line in reorder_lines:
            neworder += self._get_intersections(reorder_line)
        neworder = dedupe(neworder)
        if len(neworder) < 2:
            return # nothing to reorder
        # ok, we have our new order. That was easy huh? Now, what we have to do is to insert that
        # new order in the rest of the elements, which might not all be in our new order. So we have
        # to find our insertion point, divide it into a 'before' and an 'after' list, remove all our
        # newly ordered elems from those lists, and do a before + neworder + after concat.
        minorder = min(e.order for e in neworder)
        all_elems = list(self._ordered_elems())
        affected_elems = set(neworder)
        unaffected_elems = [e for e in all_elems if e not in affected_elems]
        before = [e for e in unaffected_elems if e.order < minorder]
        after = [e for e in unaffected_elems if e.order > minorder]
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
        page_boundaries = self._get_page_boundaries(view_width, view_height)
        # draw the page itself
        self.view.draw_rectangle(page_boundaries, PageColor.PageBg, PageColor.PageBorder)
        # now draw the elements
        self._compute_elem_drawrect(page_boundaries)
        todraw = [e for e in self.elements if e in self._elem2drawrect]
        for elem in todraw:
            elem_rect = self._elem2drawrect[elem]
            color = STATE2COLOR.get(elem.state, PageColor.ElemNormal)
            if elem in self.app.selected_elements:
                innerrect = elem_rect.scaled_rect(-2, -2)
                self.view.draw_rectangle(innerrect, None, color)
                self.view.draw_rectangle(elem_rect, None, PageColor.ElemSelected)
            else:
                self.view.draw_rectangle(elem_rect, None, color)
        if self._reorder_mode:
            self._draw_order_arrows()
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
            self._handle_drag_completion()
        self._last_mouse_down = None
        self._last_mouse_pos = None
        self.view.refresh()
    
    def press_key(self, key):
        key = key.upper()
        if key not in SHORTCUTKEY2FLAG:
            return
        state = SHORTCUTKEY2FLAG[key]
        self.app.change_state_of_selected(state)
    
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
    
    # Tracking modifiers key can be glitchy, especially when the user decides to hold more than
    # one shift key at once. The moment at which shift is pressed is unimportant, as long as we
    # know during mouse_up() whether shift is held. The moment at which shift is released, however,
    # is important because it's at this moment that we resolve the arrow buffer. So, in the GUI,
    # we don't track keyPressEvent for shift, we only check if shift is held on mouse release.
    # However, we track key release events and set shift_key_held immediately.
    @property
    def shift_key_held(self):
        return self._shift_key_held
    
    @shift_key_held.setter
    def shift_key_held(self, value):
        self._shift_key_held = value
        if not value and self._reorder_line_buffer:
            self._reorder_following_line(self._reorder_line_buffer)
            self._reorder_line_buffer = []
            self.view.refresh()
    
