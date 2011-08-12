# Created By: Virgil Dupras
# Created On: 2011-06-19
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

import logging

from hscommon import cocoa
from hscommon.cocoa.inter import signature, PyFairware

from core import __appname__
from core.app import App
from .app_view import AppView

class PyPdfMasher(PyFairware):
    def init(self):
        self = super(PyPdfMasher, self).init()
        logging.basicConfig(level=logging.WARNING, format='%(levelname)s %(message)s')
        cocoa.install_exception_hook()
        self.app_view = AppView()
        self.py = App(self.app_view)
        return self
    
    def buildHtml(self):
        return self.py.build_html()
    
    def changeStateOfSelected_(self, newstate):
        self.py.change_state_of_selected(newstate)
    
    def loadPDF_(self, path):
        self.py.load_pdf(path)
    
    @signature('c@:')
    def hideIgnored(self):
        return self.py.hide_ignored
    
    @signature('v@:c')
    def setHideIgnored_(self, value):
        self.py.hide_ignored = value
    
    #---Registration
    def appName(self):
        return __appname__
    
    #--- Worker. Mixin classes don't work with NSObject so we can't use them for interfaces
    def getJobProgress(self):
        try:
            return self.app_view.progress.last_progress
        except AttributeError:
            # See dupeguru ticket #106
            return -1
    
    def getJobDesc(self):
        try:
            return self.app_view.progress.last_desc
        except AttributeError:
            # see getJobProgress
            return ''
    
    def cancelJob(self):
        self.app_view.progress.job_cancelled = True
    
    def jobCompleted_(self, jobid):
        self.py._job_completed(jobid)
