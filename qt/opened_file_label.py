# Created By: Virgil Dupras
# Created On: 2011-06-18
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

from PyQt4.QtGui import QLabel

class OpenedFileLabel(QLabel):
    def __init__(self, model):
        QLabel.__init__(self)
        self.model = model
        self.model.view = self
    
    #--- model -> view
    def refresh(self):
        self.setText(self.model.text)
    
