from PyQt4.QtCore import QCoreApplication
from PyQt4.QtGui import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton,
    QLabel, QTableView, QFileDialog)

from core.app import App
from .element_table import ElementTable

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None)
        self._setupUi()
        self.app = App()
        self.elementTable = ElementTable(self.app, self.elementTableView)
        self.elementTable.model.connect()
        
        self.openButton.clicked.connect(self.openButtonClicked)
    
    def _setupUi(self):
        self.setWindowTitle(QCoreApplication.instance().applicationName())
        self.mainWidget = QWidget(self)
        self.verticalLayout = QVBoxLayout(self.mainWidget)
        self.elementTableView = QTableView(self.mainWidget)
        self.verticalLayout.addWidget(self.elementTableView)
        self.openButton = QPushButton("Open File", self.mainWidget)
        self.verticalLayout.addWidget(self.openButton)
        self.setCentralWidget(self.mainWidget)
    
    #--- Signals
    def openButtonClicked(self):
        title = "Select a PDF to open"
        files = ';;'.join(["PDF file (*.pdf)", "All Files (*.*)"])
        destination = QFileDialog.getOpenFileName(self, title, '', files)
        if destination:
            self.app.open_file(destination)
    
