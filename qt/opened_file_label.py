# Created By: Virgil Dupras
# Created On: 2011-06-18
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from PyQt4.QtGui import QLabel

from core.gui.opened_file_label import OpenedFileLabel as OpenedFileLabelModel

class OpenedFileLabel(QLabel):
    def __init__(self, app):
        QLabel.__init__(self)
        self.model = OpenedFileLabelModel(view=self, app=app)
        self.model.connect()
    
    #--- model -> view
    def refresh(self):
        self.setText(self.model.text)
    
