# Created By: Virgil Dupras
# Created On: 2011-06-12
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from functools import partial

from PyQt4.QtCore import QCoreApplication
from PyQt4.QtGui import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QFileDialog,
    QTabWidget, QSizePolicy)

from core.app import App
from core.pdf import ElementState
from .element_table import ElementTable, ElementTableView

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None)
        self.app = App()
        self._setupUi()
        self.elementTable = ElementTable(self.app, self.elementTableView)
        self.elementTable.model.connect()
        
        self.openButton.clicked.connect(self.openButtonClicked)
    
    def _setupUi(self):
        self.setWindowTitle(QCoreApplication.instance().applicationName())
        self.resize(700, 600)
        self.mainWidget = QWidget(self)
        self.verticalLayout = QVBoxLayout(self.mainWidget)
        self.openButton = QPushButton("Open File")
        self.verticalLayout.addWidget(self.openButton)
        self.elementTableView = ElementTableView()
        self.verticalLayout.addWidget(self.elementTableView)
        self.tabWidget = QTabWidget()
        # We want to leave the most screen estate possible to the table.
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.tabWidget.setSizePolicy(sizePolicy)
        self.flagTab = FlagTab(self.app)
        self.tabWidget.addTab(self.flagTab, "Flag")
        self.buildTab = BuildTab(self.app)
        self.tabWidget.addTab(self.buildTab, "Build")
        self.verticalLayout.addWidget(self.tabWidget)
        self.setCentralWidget(self.mainWidget)
    
    #--- Signals
    def openButtonClicked(self):
        title = "Select a PDF to open"
        files = ';;'.join(["PDF file (*.pdf)", "All Files (*.*)"])
        destination = QFileDialog.getOpenFileName(self, title, '', files)
        if destination:
            self.app.open_file(destination)
    

class FlagTab(QWidget):
    def __init__(self, app):
        QWidget.__init__(self)
        self.app = app
        self._setupUi()
        
        self.normalButton.clicked.connect(partial(self.app.change_state_of_selected, ElementState.Normal))
        self.titleButton.clicked.connect(partial(self.app.change_state_of_selected, ElementState.Title))
        self.footnoteButton.clicked.connect(partial(self.app.change_state_of_selected, ElementState.Footnote))
        self.ignoreButton.clicked.connect(partial(self.app.change_state_of_selected, ElementState.Ignored))
        
    def _setupUi(self):
        self.buttonLayout = QHBoxLayout(self)
        self.normalButton = QPushButton("Normal")
        self.buttonLayout.addWidget(self.normalButton)
        self.titleButton = QPushButton("Title")
        self.buttonLayout.addWidget(self.titleButton)
        self.footnoteButton = QPushButton("Footnote")
        self.buttonLayout.addWidget(self.footnoteButton)
        self.ignoreButton = QPushButton("Ignore")
        self.buttonLayout.addWidget(self.ignoreButton)
    

class BuildTab(QWidget):
    def __init__(self, app):
        QWidget.__init__(self)
        self.app = app
        self._setupUi()
        
        self.buildButton.clicked.connect(self.buildButtonClicked)
    
    def _setupUi(self):
        self.buttonLayout = QHBoxLayout(self)
        self.buildButton = QPushButton("Build")
        self.buttonLayout.addWidget(self.buildButton)
    
    #--- Signals
    def buildButtonClicked(self):
        self.app.build_html()
    
