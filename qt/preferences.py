# Created By: Virgil Dupras
# Created On: 2009-11-17
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

from qtlib.preferences import Preferences as PreferencesBase

class Preferences(PreferencesBase):
    def _load_values(self, settings):
        get = self.get_value
    
    def reset(self):
        pass
    
    def _save_values(self, settings):
        set_ = self.set_value
    
