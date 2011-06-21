# Created By: Virgil Dupras
# Created On: 2011-06-19
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

import logging

from hscommon.cocoa import install_exception_hook
from hscommon.cocoa.inter import signature, PyFairware

from core import __appname__
from core.app import App

class PyApp(PyFairware):
    def init(self):
        self = super(PyApp, self).init()
        self.py = App()
        logging.basicConfig(level=logging.WARNING, format='%(levelname)s %(message)s')
        install_exception_hook()
        return self
    
    def buildHtml(self):
        return self.py.build_html()
    
    def changeStateOfSelected_(self, newstate):
        self.py.change_state_of_selected(newstate)
    
    def openFile_(self, path):
        self.py.open_file(path)
    
    @signature('c@:')
    def hideIgnored(self):
        return self.py.hide_ignored
    
    @signature('v@:c')
    def setHideIgnored_(self, value):
        self.py.hide_ignored = value
    
    #---Registration
    def appName(self):
        return __appname__
    
