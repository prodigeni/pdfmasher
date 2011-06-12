# Created By: Virgil Dupras
# Created On: 2011-06-12
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from PyQt4.QtCore import Qt

from qtlib.column import Column
from qtlib.table import Table
from core.gui.element_table import ElementTable as ElementTableModel

class ElementTable(Table):
    COLUMNS = [
        Column('page', "Page", 50),
        Column('x0', "x0", 50),
        Column('y0', "y0", 50),
        Column('x1', "x1", 50),
        Column('y1', "y1", 50),
        Column('text', "Text", 300),
    ]
    
    def __init__(self, app, view):
        model = ElementTableModel(view=self, app=app)
        Table.__init__(self, model, view)
    