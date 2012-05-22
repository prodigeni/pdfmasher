# Created By: Virgil Dupras
# Created On: 2011-06-12
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

from hscommon.gui.base import GUIObject as GUIObjectBase
from hscommon.notify import Listener

class GUIObject(Listener, GUIObjectBase):
    def __init__(self, app):
        Listener.__init__(self, app)
        GUIObjectBase.__init__(self)
        self.app = app
        self.connect()
    
    def elements_changed(self):
        # The list of loaded elements have changed.
        pass
    
    def file_opened(self):
        pass
    
