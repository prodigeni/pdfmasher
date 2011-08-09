# Created By: Virgil Dupras
# Created On: 2011-07-10
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from PyQt4.QtGui import QWidget, QVBoxLayout, QPushButton, QLabel, QSizePolicy
from qtlib.util import verticalSpacer

from core.gui.build_pane import BuildPane as BuildPaneModel

class BuildPane(QWidget):
    def __init__(self, app):
        QWidget.__init__(self)
        self.app = app
        self._setupUi()
        self.model = BuildPaneModel(view=self, app=app.model)
        self.model.connect()
        
        self.generateMarkdownButton.clicked.connect(self.model.generate_markdown)
        self.editMarkdownButton.clicked.connect(self.model.edit_markdown)
        self.revealMarkdownButton.clicked.connect(self.model.reveal_markdown)
        self.viewHtmlButton.clicked.connect(self.model.view_html)
    
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
        self.mainLayout.addItem(verticalSpacer())
    
    #--- model --> view
    def refresh(self):
        self.genDescLabel.setText(self.model.lastgen_desc)
        enabled = self.model.post_processing_enabled
        self.editMarkdownButton.setEnabled(enabled)
        self.revealMarkdownButton.setEnabled(enabled)
        self.viewHtmlButton.setEnabled(enabled)
    
