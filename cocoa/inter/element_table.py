# Created By: Virgil Dupras
# Created On: 2011-06-19
# Copyright 2013 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

from cocoa.inter import PyTable

class PyElementTable(PyTable):
    def pressKey_(self, key: str):
        self.model.press_key(key)
    
