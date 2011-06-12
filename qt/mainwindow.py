from PyQt4.QtCore import QCoreApplication
from PyQt4.QtGui import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QFileDialog)

from core.app import App
from core.pdf import ElementState
from .element_table import ElementTable, ElementTableView

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None)
        self._setupUi()
        self.app = App()
        self.elementTable = ElementTable(self.app, self.elementTableView)
        self.elementTable.model.connect()
        
        self.openButton.clicked.connect(self.openButtonClicked)
        self.ignoreButton.clicked.connect(self.ignoreButtonClicked)
        self.normalButton.clicked.connect(self.normalButtonClicked)
        self.buildButton.clicked.connect(self.buildButtonClicked)
    
    def _setupUi(self):
        self.setWindowTitle(QCoreApplication.instance().applicationName())
        self.resize(700, 600)
        self.mainWidget = QWidget(self)
        self.verticalLayout = QVBoxLayout(self.mainWidget)
        self.openButton = QPushButton("Open File", self.mainWidget)
        self.verticalLayout.addWidget(self.openButton)
        self.elementTableView = ElementTableView(self.mainWidget)
        self.elementTableView.setupUi()
        self.verticalLayout.addWidget(self.elementTableView)
        self.buttonLayout = QHBoxLayout()
        self.ignoreButton = QPushButton("Ignore", self.mainWidget)
        self.buttonLayout.addWidget(self.ignoreButton)
        self.normalButton = QPushButton("Normal", self.mainWidget)
        self.buttonLayout.addWidget(self.normalButton)
        self.buildButton = QPushButton("Build", self.mainWidget)
        self.buttonLayout.addWidget(self.buildButton)
        self.verticalLayout.addLayout(self.buttonLayout)
        self.setCentralWidget(self.mainWidget)
    
    #--- Signals
    def openButtonClicked(self):
        title = "Select a PDF to open"
        files = ';;'.join(["PDF file (*.pdf)", "All Files (*.*)"])
        destination = QFileDialog.getOpenFileName(self, title, '', files)
        if destination:
            self.app.open_file(destination)
    
    def ignoreButtonClicked(self):
        self.app.change_state_of_selected(ElementState.Ignored)
    
    def normalButtonClicked(self):
        self.app.change_state_of_selected(ElementState.Normal)
    
    def buildButtonClicked(self):
        self.app.build_html()
    
