# Created By: Virgil Dupras
# Created On: 2011-07-22
# Copyright 2013 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

from .base import GUIObject
from .page_repr import PageRepresentation

class PageController(GUIObject):
    #--- model -> view calls:
    # refresh_page_label()
    #
    
    def __init__(self, app):
        GUIObject.__init__(self, app)
        self.page_repr = PageRepresentation(app)
    
    #--- Public
    def prev_page(self):
        self.page_repr.pageno -= 1
        self.view.refresh_page_label()
    
    def next_page(self):
        self.page_repr.pageno += 1
        self.view.refresh_page_label()
    
    @property
    def page_label(self):
        return "Page: {}".format(self.page_repr.pageno)
    
    #--- Events
    def file_opened(self):
        self.page_repr.pageno = 0
        self.view.refresh_page_label()
    
    def elements_changed(self):
        self.page_repr.update_page()
    

    
    