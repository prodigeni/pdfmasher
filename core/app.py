# Created By: Virgil Dupras
# Created On: 2011-06-12
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from pdfminer.pdfparser import PDFSyntaxError

from hscommon.reg import RegistrableApplication
from hscommon.notify import Broadcaster
from hscommon.trans import tr

from .pdf import extract_text_elements_from_pdf

class JobType:
    LoadPDF = 'job_load_pdf'


JOBID2TITLE = {
    JobType.LoadPDF: tr("Reading PDF"),
}

class App(Broadcaster, RegistrableApplication):
    #--- model -> view calls:
    # open_path(path)
    # reveal_path(path)
    # setup_as_registered()
    # show_msg(msg)
    # start_job(j, *args)
    
    def __init__(self, view):
        Broadcaster.__init__(self)
        RegistrableApplication.__init__(self, appid=6)
        self.view = view
        self.current_path = None
        self._hide_ignored = False
        self.selected_elements = []
        self.elements = []
        self.last_file_was_invalid = False
    
    #--- Overrides
    def _setup_as_registered(self):
        self.view.setup_as_registered()
    
    #--- Protected
    def _job_completed(self, jobid):
        # Must be called by subclasses when they detect that an async job is completed.
        if jobid == JobType.LoadPDF:
            if not self.last_file_was_invalid:
                self.notify('file_opened')
                self.notify('elements_changed')
            else:
                self.view.show_msg("This file is not a PDF.")
    
    #--- Public (Internal)
    def select_elements(self, elements):
        self.selected_elements = elements
        self.notify('elements_selected')
    
    #--- Public (API)
    def open_path(self, path):
        self.view.open_path(path)
    
    def reveal_path(self, path):
        self.view.reveal_path(path)
    
    def change_state_of_selected(self, newstate):
        for element in self.selected_elements:
            element.state = newstate
        self.notify('elements_changed')
    
    def load_pdf(self, path):
        def do(j):
            self.last_file_was_invalid = False
            try:
                self.elements = extract_text_elements_from_pdf(path, j)
                self.current_path = path
            except PDFSyntaxError:
                self.last_file_was_invalid = True
        
        self.view.start_job(JobType.LoadPDF, do)
    
    #--- Properties
    @property
    def hide_ignored(self):
        return self._hide_ignored
    
    @hide_ignored.setter
    def hide_ignored(self, value):
        self._hide_ignored = value
        self.notify('elements_changed')
    
