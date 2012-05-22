# Created By: Virgil Dupras
# Created On: 2011-07-22
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QCheckBox

from qtlib.util import horizontalSpacer

from .page_repr import PageRepresentation

class PageController(QWidget):
    def __init__(self, model):
        QWidget.__init__(self)
        self.model = model
        self.model.view = self
        self._setupUi()
        
        self.previousPageButton.clicked.connect(self.model.prev_page)
        self.nextPageButton.clicked.connect(self.model.next_page)
        self.reorderModeCheckBox.stateChanged.connect(self.reorderModeCheckBoxStateChanged)
    
    def _setupUi(self):
        self.setWindowTitle("Grouping Dialog")
        self.resize(600, 600)
        self.mainLayout = QVBoxLayout(self)
        self.pageRepr = PageRepresentation(self.model.page_repr)
        self.mainLayout.addWidget(self.pageRepr)
        self.buttonLayout = QHBoxLayout()
        self.previousPageButton = QPushButton("<<")
        self.buttonLayout.addWidget(self.previousPageButton)
        self.pageLabel = QLabel()
        self.buttonLayout.addWidget(self.pageLabel)
        self.nextPageButton = QPushButton(">>")
        self.buttonLayout.addWidget(self.nextPageButton)
        self.reorderModeCheckBox = QCheckBox("Re-order mode")
        self.buttonLayout.addWidget(self.reorderModeCheckBox)
        self.buttonLayout.addItem(horizontalSpacer())
        self.mainLayout.addLayout(self.buttonLayout)
    
    #--- Signals
    def reorderModeCheckBoxStateChanged(self, state):
        self.model.page_repr.reorder_mode = state == Qt.Checked
    
    #--- model --> view
    def refresh_page_label(self):
        self.pageLabel.setText(self.model.page_label)
    
