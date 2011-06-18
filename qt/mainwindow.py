# Created By: Virgil Dupras
# Created On: 2011-06-12
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from PyQt4.QtCore import QCoreApplication, QUrl
from PyQt4.QtGui import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QFileDialog,
    QTabWidget, QSizePolicy, QDesktopServices)

from core.app import App
from .element_table import ElementTable, ElementTableView
from .opened_file_label import OpenedFileLabel
from .edit_pane import EditPane

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None)
        self.app = App()
        self._setupUi()
        self.elementTable = ElementTable(self.app, self.elementTableView)
        
        self.openButton.clicked.connect(self.openButtonClicked)
    
    def _setupUi(self):
        self.setWindowTitle(QCoreApplication.instance().applicationName())
        self.resize(700, 600)
        self.mainWidget = QWidget(self)
        self.verticalLayout = QVBoxLayout(self.mainWidget)
        self.fileLayout = QHBoxLayout()
        self.openButton = QPushButton("Open File")
        # We want to leave the space to the label
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.openButton.setSizePolicy(sizePolicy)
        self.fileLayout.addWidget(self.openButton)
        self.openedFileLabel = OpenedFileLabel(self.app)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.openedFileLabel.setSizePolicy(sizePolicy)
        self.fileLayout.addWidget(self.openedFileLabel)
        self.verticalLayout.addLayout(self.fileLayout)
        self.elementTableView = ElementTableView()
        self.verticalLayout.addWidget(self.elementTableView)
        self.tabWidget = QTabWidget()
        # We want to leave the most screen estate possible to the table.
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.tabWidget.setSizePolicy(sizePolicy)
        self.editTab = EditPane(self.app)
        self.tabWidget.addTab(self.editTab, "Edit")
        self.buildTab = BuildPane(self.app)
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
    

class BuildPane(QWidget):
    def __init__(self, app):
        QWidget.__init__(self)
        self.app = app
        self._setupUi()
        
        self.viewHtmlButton.clicked.connect(self.viewHtmlButtonClicked)
    
    def _setupUi(self):
        self.buttonLayout = QHBoxLayout(self)
        self.viewHtmlButton = QPushButton("View HTML")
        self.buttonLayout.addWidget(self.viewHtmlButton)
    
    #--- Signals
    def viewHtmlButtonClicked(self):
        html_path = self.app.build_html()
        url = QUrl.fromLocalFile(html_path)
        QDesktopServices.openUrl(url)
    
