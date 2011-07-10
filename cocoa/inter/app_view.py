# Created By: Virgil Dupras
# Created On: 2011-07-08
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from hscommon import cocoa
from hscommon.cocoa.objcmin import NSNotificationCenter, NSWorkspace
from jobprogress import job

from core.app import JOBID2TITLE

class AppView:
    def __init__(self):
        self.progress = cocoa.ThreadedJobPerformer()
    
    @staticmethod
    def open_path(path):
        NSWorkspace.sharedWorkspace().openFile_(path)
    
    @staticmethod
    def reveal_path(path):
        NSWorkspace.sharedWorkspace().selectFile_inFileViewerRootedAtPath_(path, '')
    
    def start_job(self, jobid, func, *args):
        try:
            j = self.progress.create_job()
            args = tuple([j] + list(args))
            self.progress.run_threaded(func, args=args)
        except job.JobInProgressError:
            NSNotificationCenter.defaultCenter().postNotificationName_object_('JobInProgress', self)
        else:
            ud = {'desc': JOBID2TITLE[jobid], 'jobid':jobid}
            NSNotificationCenter.defaultCenter().postNotificationName_object_userInfo_('JobStarted', self, ud)
    
    def setup_as_registered(self):
        pass # does nothing on Cocoa
    
