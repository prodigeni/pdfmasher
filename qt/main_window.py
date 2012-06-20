# Created By: Virgil Dupras
# Created On: 2011-06-12
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

from PyQt4.QtCore import QCoreApplication, QRect
from PyQt4.QtGui import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QFileDialog,
    QTabWidget, QSizePolicy, QMenuBar, QMenu, QLabel)

from hscommon.trans import tr
from qtlib.util import moveToScreenCenter, createActions
from qtlib.text_field import TextField
from .element_table import ElementTable, ElementTableView
from .page_controller import PageController
from .edit_pane import EditPane
from .build_pane import BuildPane

class MainWindow(QMainWindow):
    def __init__(self, app):
        QMainWindow.__init__(self, None)
        self.app = app
        self._setupUi()
        self.elementTable = ElementTable(self.app.model.element_table, self.elementTableView)
        self.openedFileLabel = TextField(self.app.model.opened_file_label, self.openedFileLabelView)
        
        self.openButton.clicked.connect(self.actionLoadPDF.trigger)
    
    def _setupActions(self):
        ACTIONS = [
            ('actionLoadPDF', 'Ctrl+O', '', tr("Load PDF"), self.loadPDFTriggered),
        ]
        createActions(ACTIONS, self)
    
    def _setupMenu(self):
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 42, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setTitle(tr("File"))
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setTitle(tr("Help"))
        self.setMenuBar(self.menubar)
        
        self.menuFile.addAction(self.actionLoadPDF)
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
        self.resize(900, 600)
        self.mainWidget = QWidget(self)
        self.verticalLayout = QVBoxLayout(self.mainWidget)
        self.fileLayout = QHBoxLayout()
        self.openButton = QPushButton("Open File")
        # We want to leave the space to the label
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.openButton.setSizePolicy(sizePolicy)
        self.fileLayout.addWidget(self.openButton)
        self.openedFileLabelView = QLabel()
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.openedFileLabelView.setSizePolicy(sizePolicy)
        self.fileLayout.addWidget(self.openedFileLabelView)
        self.verticalLayout.addLayout(self.fileLayout)
        self.tabViewsLayout = QHBoxLayout()
        self.topTabWidget = QTabWidget()
        self.elementTableView = ElementTableView()
        self.topTabWidget.addTab(self.elementTableView, "Table")
        self.pageController = PageController(self.app.model.page_controller)
        self.topTabWidget.addTab(self.pageController, "Page")
        self.tabViewsLayout.addWidget(self.topTabWidget)
        self.bottomTabWidget = QTabWidget()
        # We want to leave the most screen estate possible to the table.
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        self.bottomTabWidget.setSizePolicy(sizePolicy)
        self.editTab = EditPane(self.app.model.edit_pane)
        self.bottomTabWidget.addTab(self.editTab, "Edit")
        self.buildTab = BuildPane(self.app.model.build_pane)
        self.bottomTabWidget.addTab(self.buildTab, "Build")
        self.tabViewsLayout.addWidget(self.bottomTabWidget)
        self.verticalLayout.addLayout(self.tabViewsLayout)
        self.setCentralWidget(self.mainWidget)
        
        self._setupActions()
        self._setupMenu()
        moveToScreenCenter(self)
    
    #--- Signals
    def loadPDFTriggered(self):
        title = "Select a PDF to open"
        files = ';;'.join(["PDF file (*.pdf)", "All Files (*.*)"])
        destination = QFileDialog.getOpenFileName(self, title, '', files)
        if destination:
            self.app.model.load_pdf(destination)
    

    
