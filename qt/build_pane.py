# Created By: Virgil Dupras
# Created On: 2011-07-10
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

from PyQt4.QtCore import Qt
from PyQt4.QtGui import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy,
    QRadioButton, QFileDialog, QFormLayout, QLineEdit)
from qtlib.util import verticalSpacer

from core.gui.build_pane import EbookType

class BuildPane(QWidget):
    def __init__(self, model):
        QWidget.__init__(self)
        self._setupUi()
        self.model = model
        self.model.view = self
        
        self.generateMarkdownButton.clicked.connect(self.model.generate_markdown)
        self.editMarkdownButton.clicked.connect(self.model.edit_markdown)
        self.revealMarkdownButton.clicked.connect(self.model.reveal_markdown)
        self.viewHtmlButton.clicked.connect(self.model.view_html)
        self.createEbookButton.clicked.connect(self.createEbookClicked)
    
    def _setupUi(self):
        self.mainLayout = QVBoxLayout(self)
        self.label1 = QLabel("Step 1: Generate Markdown")
        self.mainLayout.addWidget(self.label1)
        self.generateMarkdownButton = QPushButton("Generate Markdown")
        self.mainLayout.addWidget(self.generateMarkdownButton)
        self.genDescLabel = QLabel()
        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        self.genDescLabel.setSizePolicy(sizePolicy)
        self.mainLayout.addWidget(self.genDescLabel)
        self.label2 = QLabel("Step 2: Post-processing")
        self.mainLayout.addWidget(self.label2)
        self.editMarkdownButton = QPushButton("Edit Markdown")
        self.mainLayout.addWidget(self.editMarkdownButton)
        self.revealMarkdownButton = QPushButton("Reveal Markdown")
        self.mainLayout.addWidget(self.revealMarkdownButton)
        self.viewHtmlButton = QPushButton("View HTML")
        self.mainLayout.addWidget(self.viewHtmlButton)
        self.label2 = QLabel("Step 3: E-book creation")
        self.mainLayout.addWidget(self.label2)
        self.radioLayout = QHBoxLayout()
        self.mobiRadio = QRadioButton("MOBI")
        self.radioLayout.addWidget(self.mobiRadio)
        self.epubRadio = QRadioButton("EPUB")
        self.radioLayout.addWidget(self.epubRadio)
        self.mobiRadio.setChecked(True)
        self.mainLayout.addLayout(self.radioLayout)
        self.metadataLayout = QFormLayout()
        self.metadataLayout.setFormAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.titleEdit = QLineEdit()
        self.metadataLayout.addRow("Title:", self.titleEdit)
        self.authorEdit = QLineEdit()
        self.metadataLayout.addRow("Author:", self.authorEdit)
        self.mainLayout.addLayout(self.metadataLayout)
        self.createEbookButton = QPushButton("Create e-book")
        self.mainLayout.addWidget(self.createEbookButton)
        self.mainLayout.addItem(verticalSpacer())
    
    #--- Signals
        
    def createEbookClicked(self):
        ebook_type = EbookType.EPUB if self.epubRadio.isChecked() else EbookType.MOBI
        self.model.selected_ebook_type = ebook_type
        self.model.ebook_title = self.titleEdit.text()
        self.model.ebook_author = self.authorEdit.text()
        title = "Select a destination for the e-book"
        if self.model.selected_ebook_type == EbookType.EPUB:
            myfilter = "EPUB file (*.epub)"
        else:
            myfilter = "MOBI file (*.mobi)"
        files = ';;'.join([myfilter, "All Files (*.*)"])
        destination = QFileDialog.getSaveFileName(self, title, '', files)
        if destination:
            self.model.create_ebook(destination)
    
    #--- model --> view
    def refresh(self):
        self.genDescLabel.setText(self.model.lastgen_desc)
        enabled = self.model.post_processing_enabled
        self.editMarkdownButton.setEnabled(enabled)
        self.revealMarkdownButton.setEnabled(enabled)
        self.viewHtmlButton.setEnabled(enabled)
        self.createEbookButton.setEnabled(enabled)
    
