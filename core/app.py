# Created By: Virgil Dupras
# Created On: 2011-06-12
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

import os.path as op

from hscommon.reg import RegistrableApplication
from hscommon.notify import Broadcaster
from hscommon.trans import tr

from .pdf import extract_text_elements_from_pdf
from .html import generate_html

class JobType:
    OpenFile = 'job_open_file'


JOBID2TITLE = {
    JobType.OpenFile: tr("Reading PDF"),
}

# App view interface
# start_job(j, *args)

class App(Broadcaster, RegistrableApplication):
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
        if jobid == JobType.OpenFile:
            self.notify('file_opened')
            self.notify('elements_changed')
    
    #--- Public (Internal)
    def select_elements(self, elements):
        self.selected_elements = elements
        self.notify('elements_selected')
    
    #--- Public (API)
    def build_html(self):
        assert self.current_path
        without_ext, ext = op.splitext(self.current_path)
        dest_path = without_ext + '.htm'
        with open(dest_path, 'wt', encoding='utf-8') as fp:
            fp.write(generate_html(self.elements))
        return dest_path
    
    def change_state_of_selected(self, newstate):
        for element in self.selected_elements:
            element.state = newstate
        self.notify('elements_changed')
    
    def open_file(self, path):
        def do(j):
            self.elements = extract_text_elements_from_pdf(path, j)
            self.current_path = path
        
        self.view.start_job(JobType.OpenFile, do)
    
    #--- Properties
    @property
    def hide_ignored(self):
        return self._hide_ignored
    
    @hide_ignored.setter
    def hide_ignored(self, value):
        self._hide_ignored = value
        self.notify('elements_changed')
    
