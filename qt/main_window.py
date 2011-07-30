# Created By: Virgil Dupras
# Created On: 2011-06-12
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from PyQt4.QtCore import QCoreApplication, QRect
from PyQt4.QtGui import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QFileDialog,
    QTabWidget, QSizePolicy, QMenuBar, QMenu)

from hscommon.trans import tr
from qtlib.util import moveToScreenCenter
from .element_table import ElementTable, ElementTableView
from .page_controller import PageController
from .opened_file_label import OpenedFileLabel
from .edit_pane import EditPane
from .build_pane import BuildPane

class MainWindow(QMainWindow):
    def __init__(self, app):
        QMainWindow.__init__(self, None)
        self.app = app
        self._setupUi()
        self.elementTable = ElementTable(self.app, self.elementTableView)
        
        self.openButton.clicked.connect(self.openButtonClicked)
    
    def _setupActions(self):
        # None for now
        pass
    
    def _setupMenu(self):
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 42, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setTitle(tr("File"))
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setTitle(tr("Help"))
        self.setMenuBar(self.menubar)
        
        self.menuFile.addAction(self.app.actionQuit)
        self.menuHelp.addAction(self.app.actionShowHelp)
        self.menuHelp.addAction(self.app.actionRegister)
        self.menuHelp.addAction(self.app.actionCheckForUpdate)
        self.menuHelp.addAction(self.app.actionOpenDebugLog)
        self.menuHelp.addAction(self.app.actionAbout)
        
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
    
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
        self.topTabWidget = QTabWidget()
        self.elementTableView = ElementTableView()
        self.topTabWidget.addTab(self.elementTableView, "Table")
        self.pageController = PageController(self.app)
        self.topTabWidget.addTab(self.pageController, "Page")
        self.verticalLayout.addWidget(self.topTabWidget)
        self.bottomTabWidget = QTabWidget()
        # We want to leave the most screen estate possible to the table.
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.bottomTabWidget.setSizePolicy(sizePolicy)
        self.editTab = EditPane(self.app)
        self.bottomTabWidget.addTab(self.editTab, "Edit")
        self.buildTab = BuildPane(self.app)
        self.bottomTabWidget.addTab(self.buildTab, "Build")
        self.verticalLayout.addWidget(self.bottomTabWidget)
        self.setCentralWidget(self.mainWidget)
        
        self._setupActions()
        self._setupMenu()
        moveToScreenCenter(self)
    
    #--- Signals
    def openButtonClicked(self):
        title = "Select a PDF to open"
        files = ';;'.join(["PDF file (*.pdf)", "All Files (*.*)"])
        destination = QFileDialog.getOpenFileName(self, title, '', files)
        if destination:
            self.app.model.load_pdf(destination)
    

    
