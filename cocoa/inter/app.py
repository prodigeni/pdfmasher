# Created By: Virgil Dupras
# Created On: 2011-06-19
# Copyright 2013 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

import logging

from objp.util import pyref, dontwrap
import cocoa
from cocoa import proxy
from cocoa.inter import PyBaseApp, BaseAppView
from jobprogress import job

from core.app import JOBID2TITLE

from core.app import App

class PdfMasherView(BaseAppView):
    def queryLoadPathWithPrompt_(self, prompt: str) -> str: pass
    def querySavePathWithPrompt_allowedExts_(self, prompt: str, allowedExts: list) -> str: pass

class PyPdfMasher(PyBaseApp):
    FOLLOW_PROTOCOLS = ['Worker']
    
    def __init__(self):
        logging.basicConfig(level=logging.WARNING, format='%(levelname)s %(message)s')
        cocoa.install_exception_hook()
        cocoa.install_cocoa_logger()
        self.progress = cocoa.ThreadedJobPerformer()
        model = App(self)
        PyBaseApp.__init__(self, model)
    
    def elementTable(self) -> pyref:
        return self.model.element_table
    
    def openedFileLabel(self) -> pyref:
        return self.model.opened_file_label
    
    def pageController(self) -> pyref:
        return self.model.page_controller
    
    def buildPane(self) -> pyref:
        return self.model.build_pane
    
    def editPane(self) -> pyref:
        return self.model.edit_pane
    
    def buildHtml(self):
        return self.model.build_html()
    
    def changeStateOfSelected_(self, newstate: str):
        self.model.change_state_of_selected(newstate)
    
    def loadPDF(self):
        self.model.load_pdf()
    
    def loadProject(self):
        self.model.load_project()
    
    def saveProject(self):
        self.model.save_project()
    
    def hideIgnored(self) -> bool:
        return self.model.hide_ignored
    
    def setHideIgnored_(self, value: bool):
        self.model.hide_ignored = value
    
    #--- Worker. Mixin classes don't work with NSObject so we can't use them for interfaces
    def getJobProgress(self) -> object:
        try:
            return self.progress.last_progress
        except AttributeError:
            # See dupeguru ticket #106
            return -1
    
    def getJobDesc(self) -> str:
        try:
            return self.progress.last_desc
        except AttributeError:
            # see getJobProgress
            return ''
    
    def cancelJob(self):
        self.progress.job_cancelled = True
    
    def jobCompleted_(self, jobid: str):
        self.progress.reraise_if_error()
        self.model._job_completed(jobid)
    
    #--- Python --> cocoa
    @dontwrap
    def open_path(self, path):
        proxy.openPath_(path)
    
    @dontwrap
    def reveal_path(self, path):
        proxy.revealPath_(path)
    
    @dontwrap
    def start_job(self, jobid, func, args=()):
        try:
            j = self.progress.create_job()
            args = tuple([j] + list(args))
            self.progress.run_threaded(func, args=args)
        except job.JobInProgressError:
            proxy.postNotification_userInfo_('JobInProgress', None)
        else:
            ud = {'desc': JOBID2TITLE[jobid], 'jobid':jobid}
            proxy.postNotification_userInfo_('JobStarted', ud)
    
    @dontwrap
    def query_load_path(self, prompt, allowed_exts):
        # allowed_exts is, for now, ignored on Cocoa
        return self.callback.queryLoadPathWithPrompt_(prompt)
    
    @dontwrap
    def query_save_path(self, prompt, allowed_exts):
        return self.callback.querySavePathWithPrompt_allowedExts_(prompt, allowed_exts)
    
