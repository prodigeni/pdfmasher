# Created By: Virgil Dupras
# Created On: 2011-07-22
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

# The view has the responsibility of determining specific colors, but when we send draw_* messages
# to our view, we still give a color category. These categories are defined here.
class PageColor:
    PageBg = 1
    PageBorder = 2
    ElemNormal = 3

class PageRepresentation:
    #--- model -> view calls:
    # refresh()
    # draw_rectangle(x, y, width, height, bgcolor, pencolor)
    #
    
    def __init__(self, view):
        self.view = view
        self.page = None
        self.elements = None
    
    #--- Private
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
            adjusted_height = height
            x = (width - adjusted_width) / 2
            y = 0
        else:
            # Our constraint is width, adjust according to it
            adjusted_width = width
            adjusted_height = width * ratio
            x = 0
            y = (height - adjusted_height) / 2
        return x, y, adjusted_width, adjusted_height
    
    #--- Public
    def draw(self, view_width, view_height):
        if self.page is None:
            return
        px, py, pw, ph = self._get_page_boundaries(view_width, view_height)
        # draw the page itself
        self.view.draw_rectangle(px, py, pw, ph, PageColor.PageBg, PageColor.PageBorder)
        # now draw the elements
        xratio = pw / self.page.width
        yratio = ph / self.page.height
        for elem in self.elements:
            lelem = elem.layout_elem
            adjx = px + (lelem.x0 * xratio)
            # don't forget that ypos in pdfminer are inverted
            adjy = py + (ph - (lelem.y1 * yratio))
            adjw = lelem.width * xratio
            adjh = lelem.height * yratio
            self.view.draw_rectangle(adjx, adjy, adjw, adjh, PageColor.ElemNormal, None)
    
    def set_page(self, page, elements):
        self.page = page
        self.elements = elements
        self.view.refresh()
    
