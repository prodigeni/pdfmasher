# Created By: Virgil Dupras
# Created On: 2011-07-22
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QCheckBox

from core.gui.page_controller import PageController as PageControllerModel
from .page_repr import PageRepresentation

class PageController(QWidget):
    def __init__(self, app):
        QWidget.__init__(self)
        self.app = app
        self._setupUi()
        self.model = PageControllerModel(view=self, app=app.model)
        self.model.set_children([self.pageRepr.model])
        self.model.connect()
        
        self.previousPageButton.clicked.connect(self.model.prev_page)
        self.nextPageButton.clicked.connect(self.model.next_page)
        self.showElementsOrderCheckBox.stateChanged.connect(self.showElementsOrderCheckBoxStateChanged)
    
    def _setupUi(self):
        self.setWindowTitle("Grouping Dialog")
        self.resize(600, 600)
        self.mainLayout = QVBoxLayout(self)
        self.pageRepr = PageRepresentation(self.app)
        self.mainLayout.addWidget(self.pageRepr)
        self.buttonLayout = QHBoxLayout()
        self.previousPageButton = QPushButton("<<")
        self.buttonLayout.addWidget(self.previousPageButton)
        self.pageLabel = QLabel()
        self.buttonLayout.addWidget(self.pageLabel)
        self.nextPageButton = QPushButton(">>")
        self.buttonLayout.addWidget(self.nextPageButton)
        self.showElementsOrderCheckBox = QCheckBox("Show Elements Order")
        self.buttonLayout.addWidget(self.showElementsOrderCheckBox)
        self.mainLayout.addLayout(self.buttonLayout)
    
    #--- Signals
    def showElementsOrderCheckBoxStateChanged(self, state):
        self.model.page_repr.show_order = state == Qt.Checked
    
    #--- model --> view
    def refresh_page_label(self):
        self.pageLabel.setText(self.model.page_label)
    
