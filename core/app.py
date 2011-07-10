# Created By: Virgil Dupras
# Created On: 2011-06-12
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

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
    # start_job(j, *args)
    
    def __init__(self, view):
        Broadcaster.__init__(self)
        RegistrableApplication.__init__(self, appid=6)
        self.view = view
        self.current_path = None
        self._hide_ignored = False
        self.selected_elements = []
        self.elements = []
    
    #--- Overrides
    def _setup_as_registered(self):
        self.view.setup_as_registered()
    
    #--- Protected
    def _job_completed(self, jobid):
        # Must be called by subclasses when they detect that an async job is completed.
        if jobid == JobType.LoadPDF:
            self.notify('file_opened')
            self.notify('elements_changed')
    
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
            self.elements = extract_text_elements_from_pdf(path, j)
            self.current_path = path
        
        self.view.start_job(JobType.LoadPDF, do)
    
    #--- Properties
    @property
    def hide_ignored(self):
        return self._hide_ignored
    
    @hide_ignored.setter
    def hide_ignored(self, value):
        self._hide_ignored = value
        self.notify('elements_changed')
    
