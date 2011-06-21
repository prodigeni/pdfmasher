# Created By: Virgil Dupras
# Created On: 2009-11-17
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from qtlib.preferences import Preferences as PreferencesBase

class Preferences(PreferencesBase):
    def _load_values(self, settings):
        get = self.get_value
        self.registration_code = get('RegistrationCode', self.registration_code)
        self.registration_email = get('RegistrationEmail', self.registration_email)
    
    def reset(self):
        self.registration_code = ''
        self.registration_email = ''
    
    def _save_values(self, settings):
        set_ = self.set_value
        set_('RegistrationCode', self.registration_code)
        set_('RegistrationEmail', self.registration_email)
    
