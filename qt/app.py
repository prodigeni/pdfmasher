# Created By: Virgil Dupras
# Created On: 2011-06-21
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

import os.path as op

from PyQt4.QtCore import SIGNAL, QUrl, QCoreApplication, QProcess
from PyQt4.QtGui import QDesktopServices, QMessageBox, QFileDialog

from hscommon.trans import tr
from hscommon.plat import ISLINUX
from jobprogress import job
from jobprogress.qt import Progress
from qtlib.about_box import AboutBox
from qtlib.app import Application as ApplicationBase
from qtlib.util import createActions, getAppData

from core.app import App, JOBID2TITLE
from .main_window import MainWindow
from .preferences import Preferences
from .plat import HELP_PATH

class PdfMasher(ApplicationBase):
    LOGO_NAME = 'logo'
    
    def __init__(self):
        ApplicationBase.__init__(self)
        self.prefs = Preferences()
        self.prefs.load()
        self.model = App(view=self)
        self._setupActions()
        self.mainWindow = MainWindow(app=self)
        self.aboutBox = AboutBox(self.mainWindow, self, withreg=False)
        self._progress = Progress(self.mainWindow)
        
        self.connect(self, SIGNAL('applicationFinishedLaunching()'), self.applicationFinishedLaunching)
        self.connect(QCoreApplication.instance(), SIGNAL('aboutToQuit()'), self.applicationWillTerminate)
        self._progress.finished.connect(self.jobFinished)
    
    #--- Public
    def askForRegCode(self):
        self.reg.ask_for_code()
    
    #--- Private
    def _setupActions(self):
        ACTIONS = [
            ('actionLoadProject', 'Ctrl+Shift+O', '', tr("Load Project"), self.model.load_project),
            ('actionSaveProject', 'Ctrl+S', '', tr("Save Project"), self.model.save_project),
            ('actionQuit', 'Ctrl+Q', '', tr("Quit"), self.quitTriggered),
            ('actionShowHelp', 'F1', '', tr("PdfMasher Help"), self.showHelpTriggered),
            ('actionAbout', '', '', tr("About PdfMasher"), self.showAboutBoxTriggered),
            ('actionRegister', '', '', tr("Register PdfMasher"), self.registerTriggered),
            ('actionCheckForUpdate', '', '', tr("Check for Update"), self.checkForUpdateTriggered),
            ('actionOpenDebugLog', '', '', tr("Open Debug Log"), self.openDebugLogTriggered),
        ]
        createActions(ACTIONS, self)
        
        if ISLINUX:
            self.actionCheckForUpdate.setVisible(False) # This only works on Windows
    
    #--- Event Handling
    def applicationFinishedLaunching(self):
        self.mainWindow.show()
    
    def applicationWillTerminate(self):
        self.prefs.save()
    
    def jobFinished(self, jobid):
        self.model._job_completed(jobid)
    
    def checkForUpdateTriggered(self):
        QProcess.execute('updater.exe', ['/checknow'])
    
    def openDebugLogTriggered(self):
        appdata = getAppData()
        debugLogPath = op.join(appdata, 'debug.log')
        url = QUrl.fromLocalFile(debugLogPath)
        QDesktopServices.openUrl(url)
    
    def quitTriggered(self):
        self.mainWindow.close()
    
    def registerTriggered(self):
        self.reg.ask_for_code()
    
    def showAboutBoxTriggered(self):
        self.aboutBox.show()
    
    def showHelpTriggered(self):
        url = QUrl.fromLocalFile(op.abspath(op.join(HELP_PATH, 'index.html')))
        QDesktopServices.openUrl(url)
    
    #--- model --> view
    @staticmethod
    def open_path(path):
        url = QUrl.fromLocalFile(path)
        QDesktopServices.openUrl(url)
    
    @staticmethod
    def reveal_path(path):
        PdfMasher.open_path(op.dirname(path))
    
    def open_url(self, url):
        url = QUrl(url)
        QDesktopServices.openUrl(url)
    
    def show_message(self, msg):
        QMessageBox.information(self.mainWindow, '', msg)
    
    def start_job(self, jobid, func, *args):
        title = JOBID2TITLE[jobid]
        try:
            j = self._progress.create_job()
            args = tuple([j] + list(args))
            self._progress.run(jobid, title, func, args=args)
        except job.JobInProgressError:
            msg = "A previous action is still hanging in there. You can't start a new one yet. Wait a few seconds, then try again."
            QMessageBox.information(self.mainWindow, "Action in progress", msg)
    
    def get_default(self, key):
        return self.prefs.get_value(key)
    
    def set_default(self, key, value):
        self.prefs.set_value(key, value)
    
    def query_load_path(self, prompt, allowed_exts):
        myfilters = ["{} file (*.{})".format(ext.upper(), ext) for ext in allowed_exts]
        files = ';;'.join(myfilters + ["All Files (*.*)"])
        return QFileDialog.getOpenFileName(self.mainWindow, prompt, '', files)
    
    def query_save_path(self, prompt, allowed_exts):
        myfilters = ["{} file (*.{})".format(ext.upper(), ext) for ext in allowed_exts]
        files = ';;'.join(myfilters + ["All Files (*.*)"])
        return QFileDialog.getSaveFileName(self.mainWindow, prompt, '', files)
    
