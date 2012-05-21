# Created By: Virgil Dupras
# Created On: 2011-06-19
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

import logging

from hscommon import cocoa
from hscommon.cocoa.inter import signature, subproxy, PyFairware
from hscommon.cocoa.objcmin import NSNotificationCenter, NSWorkspace
from jobprogress import job

from core.app import JOBID2TITLE

from core import __appname__
from core.app import App

from .element_table import PyElementTable
from .opened_file_label import PyOpenedFileLabel
from .page_controller import PyPageController
from .build_pane import PyBuildPane
from .edit_pane import PyEditPane

class PyPdfMasher(PyFairware):
    def init(self):
        self = super(PyPdfMasher, self).init()
        logging.basicConfig(level=logging.WARNING, format='%(levelname)s %(message)s')
        cocoa.install_exception_hook()
        self.progress = cocoa.ThreadedJobPerformer()
        self.py = App(self)
        return self
    
    def bindCocoa_(self, cocoa):
        self.cocoa = cocoa
    
    elementTable = subproxy('elementTable', 'element_table', PyElementTable)
    openedFileLabel = subproxy('openedFileLabel', 'opened_file_label', PyOpenedFileLabel)
    pageController = subproxy('pageController', 'page_controller', PyPageController)
    buildPane = subproxy('buildPane', 'build_pane', PyBuildPane)
    editPane = subproxy('editPane', 'edit_pane', PyEditPane)
    
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
            return self.progress.last_progress
        except AttributeError:
            # See dupeguru ticket #106
            return -1
    
    def getJobDesc(self):
        try:
            return self.progress.last_desc
        except AttributeError:
            # see getJobProgress
            return ''
    
    def cancelJob(self):
        self.progress.job_cancelled = True
    
    def jobCompleted_(self, jobid):
        self.py._job_completed(jobid)
    
    #--- Python --> cocoa
    @staticmethod
    def open_path(path):
        NSWorkspace.sharedWorkspace().openFile_(path)
    
    @staticmethod
    def reveal_path(path):
        NSWorkspace.sharedWorkspace().selectFile_inFileViewerRootedAtPath_(path, '')
    
    def start_job(self, jobid, func):
        try:
            j = self.progress.create_job()
            args = (j, )
            self.progress.run_threaded(func, args=args)
        except job.JobInProgressError:
            NSNotificationCenter.defaultCenter().postNotificationName_object_('JobInProgress', self)
        else:
            ud = {'desc': JOBID2TITLE[jobid], 'jobid':jobid}
            NSNotificationCenter.defaultCenter().postNotificationName_object_userInfo_('JobStarted', self, ud)
    
