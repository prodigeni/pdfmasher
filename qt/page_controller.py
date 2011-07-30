# Created By: Virgil Dupras
# Created On: 2011-07-22
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from PyQt4.QtGui import QWidget, QVBoxLayout, QHBoxLayout, QPushButton

from .page_repr import PageRepresentation

class PageController(QWidget):
    def __init__(self, app):
        QWidget.__init__(self)
        self.app = app
        self._setupUi()
        
        self.previousPageButton.clicked.connect(self.pageRepr.model.prev_page)
        self.nextPageButton.clicked.connect(self.pageRepr.model.next_page)
    
    def _setupUi(self):
        self.setWindowTitle("Grouping Dialog")
        self.resize(600, 600)
        self.mainLayout = QVBoxLayout(self)
        self.pageRepr = PageRepresentation(self.app)
        self.mainLayout.addWidget(self.pageRepr)
        self.buttonLayout = QHBoxLayout()
        self.previousPageButton = QPushButton("<<")
        self.buttonLayout.addWidget(self.previousPageButton)
        self.nextPageButton = QPushButton(">>")
        self.buttonLayout.addWidget(self.nextPageButton)
        self.mainLayout.addLayout(self.buttonLayout)
    
