# Created By: Virgil Dupras
# Created On: 2011-06-18
# Copyright 2013 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

from functools import partial

from PyQt4.QtCore import Qt
from PyQt4.QtGui import (QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QCheckBox, QTextEdit,
    QGridLayout)
from qtlib.util import horizontalSpacer

from core.const import ElementState

class EditPane(QWidget):
    def __init__(self, model):
        QWidget.__init__(self)
        self._setupUi()
        self.model = model
        self.model.view = self
        
        self.normalButton.clicked.connect(partial(self.model.app.change_state_of_selected, ElementState.Normal))
        self.titleButton.clicked.connect(partial(self.model.app.change_state_of_selected, ElementState.Title))
        self.footnoteButton.clicked.connect(partial(self.model.app.change_state_of_selected, ElementState.Footnote))
        self.ignoreButton.clicked.connect(partial(self.model.app.change_state_of_selected, ElementState.Ignored))
        self.tofixButton.clicked.connect(partial(self.model.app.change_state_of_selected, ElementState.ToFix))
        self.hideIgnoredCheckBox.stateChanged.connect(self.hideIgnoredCheckBoxStateChanged)
        self.textEdit.textChanged.connect(self.textEditTextChanged)
        self.saveEditsButton.clicked.connect(self.model.save_edits)
        self.cancelEditsButton.clicked.connect(self.model.cancel_edits)
        
    def _setupUi(self):
        self.mainLayout = QVBoxLayout(self)
        self.buttonLayout = QGridLayout()
        self.normalButton = QPushButton("Normal")
        self.buttonLayout.addWidget(self.normalButton, 0, 0)
        self.titleButton = QPushButton("Title")
        self.buttonLayout.addWidget(self.titleButton, 1, 0)
        self.footnoteButton = QPushButton("Footnote")
        self.buttonLayout.addWidget(self.footnoteButton, 2, 0)
        self.ignoreButton = QPushButton("Ignore")
        self.buttonLayout.addWidget(self.ignoreButton, 0, 1)
        self.tofixButton = QPushButton("To Fix")
        self.buttonLayout.addWidget(self.tofixButton, 1, 1)
        self.mainLayout.addLayout(self.buttonLayout)
        
        self.rightLayout = QVBoxLayout()
        self.hideIgnoredCheckBox = QCheckBox("Hide Ignored Elements")
        self.rightLayout.addWidget(self.hideIgnoredCheckBox)
        self.textEdit = QTextEdit()
        self.textEdit.setAcceptRichText(False)
        self.rightLayout.addWidget(self.textEdit)
        self.editButtonLayout = QHBoxLayout()
        self.editButtonLayout.addItem(horizontalSpacer())
        self.saveEditsButton = QPushButton("Save")
        self.editButtonLayout.addWidget(self.saveEditsButton)
        self.cancelEditsButton = QPushButton("Cancel")
        self.editButtonLayout.addWidget(self.cancelEditsButton)
        self.rightLayout.addLayout(self.editButtonLayout)
        self.mainLayout.addLayout(self.rightLayout)
        
    #--- Signals
    def hideIgnoredCheckBoxStateChanged(self, state):
        self.model.app.hide_ignored = state == Qt.Checked
    
    def textEditTextChanged(self):
        self.model.edit_text = self.textEdit.toPlainText()
    
    #--- model -> view
    def refresh_edit_text(self):
        self.textEdit.setText(self.model.edit_text)
        self.textEdit.setEnabled(self.model.edit_enabled)
        self.saveEditsButton.setEnabled(self.model.edit_enabled)
        self.cancelEditsButton.setEnabled(self.model.edit_enabled)
    
