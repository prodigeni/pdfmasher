# Created By: Virgil Dupras
# Created On: 2011-06-12
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QTableView

from qtlib.column import Column
from qtlib.table import Table
from core.gui.element_table import ElementTable as ElementTableModel

class ElementTable(Table):
    COLUMNS = [
        Column('id', "ID", 50),
        Column('page', "Page", 50),
        Column('x', "X", 50),
        Column('y', "Y", 50),
        Column('fontsize', "Font Size", 75),
        Column('state', "State", 75),
        Column('text', "Text", 250),
    ]
    
    def __init__(self, app, view):
        model = ElementTableModel(view=self, app=app)
        Table.__init__(self, model, view)
        self.setColumnsWidth(None) # set default widths
    
class ElementTableView(QTableView):
    def setupUi(self):
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
    