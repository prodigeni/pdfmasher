# Created By: Virgil Dupras
# Created On: 2011-07-22
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

class PageRepresentation:
    def __init__(self, view):
        self.view = view
        self.page = None
    
    #--- Public
    def set_page(self, page):
        self.page = page
        self.view.refresh()
    
