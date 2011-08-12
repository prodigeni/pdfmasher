# Created By: Virgil Dupras
# Created On: 2011-06-12
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QTableView, QSizePolicy, QShortcut, QKeySequence

from qtlib.column import Column
from qtlib.table import Table
from core.gui.element_table import ElementTable as ElementTableModel, SHORTCUTKEY2FLAG

class ElementTable(Table):
    COLUMNS = [
        Column('page', "Page", 50),
        Column('order', "Order", 50),
        Column('x', "X", 50),
        Column('y', "Y", 50),
        Column('fontsize', "Font Size", 70),
        Column('text_length', "Text Length", 70),
        Column('state', "State", 75),
        Column('text', "Text", 150),
    ]
    
    def __init__(self, app, view):
        model = ElementTableModel(view=self, app=app.model)
        Table.__init__(self, model, view)
        self.setColumnsWidth(None) # set default widths
        self._setupKeyBindings()
        self.model.connect()
    
    def _setupKeyBindings(self):
        # we have to keep a reference to the shortcuts for them not to be freed right away
        self.shortcuts = []
        for c in SHORTCUTKEY2FLAG:
            seq = QKeySequence(c)
            shortcut = QShortcut(seq, self.view, None, None, Qt.WidgetShortcut)
            shortcut.activated.connect(self.keyActivated)
            self.shortcuts.append(shortcut)
    
    #--- Event Handlers
    def keyActivated(self):
        shortcut = self.sender()
        key = shortcut.key().toString()
        self.model.press_key(key)
    

class ElementTableView(QTableView):
    def __init__(self):
        QTableView.__init__(self)
        self._setupUi()
    
    def _setupUi(self):
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.setSizePolicy(sizePolicy)
        self.setSelectionMode(QTableView.ExtendedSelection)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setSortingEnabled(True)
        h = self.verticalHeader()
        h.setVisible(False)
        h.setDefaultSectionSize(18)
        h = self.horizontalHeader()
        h.setHighlightSections(False)
        h.setStretchLastSection(False)
        h.setDefaultAlignment(Qt.AlignLeft)
    