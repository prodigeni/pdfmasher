# Created By: Virgil Dupras
# Created On: 2011-07-22
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

class GroupDialog:
    def __init__(self, app):
        self.app = app
        self.current_pageno = 0
    
    def set_children(self, children):
        [self.page_repr] = children
        self._update_page()
    
    #--- Private
    def _update_page(self):
        page = self.app.pages[self.current_pageno]
        elems = [e for e in self.app.elements if e.page == self.current_pageno]
        self.page_repr.set_page(page, elems)
    
    #--- Public
    def prev_page(self):
        if self.current_pageno > 0:
            self.current_pageno -= 1
            self._update_page()
    
    def next_page(self):
        if self.current_pageno < len(self.app.pages)-1:
            self.current_pageno += 1
            self._update_page()
    

    
    