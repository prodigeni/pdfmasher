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

from core.app import App

class PdfMasherView(BaseAppView):
    def queryLoadPathWithPrompt_(self, prompt: str) -> str: pass
    def querySavePathWithPrompt_allowedExts_(self, prompt: str, allowedExts: list) -> str: pass

class PyPdfMasher(PyBaseApp):
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
    
    def progressWindow(self) -> pyref:
        return self.model.progress_window
    
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
    
    #--- Python --> cocoa
    @dontwrap
    def open_path(self, path):
        proxy.openPath_(path)
    
    @dontwrap
    def reveal_path(self, path):
        proxy.revealPath_(path)
    
    @dontwrap
    def query_load_path(self, prompt, allowed_exts):
        # allowed_exts is, for now, ignored on Cocoa
        return self.callback.queryLoadPathWithPrompt_(prompt)
    
    @dontwrap
    def query_save_path(self, prompt, allowed_exts):
        return self.callback.querySavePathWithPrompt_allowedExts_(prompt, allowed_exts)
    
