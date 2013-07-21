import dbus.service
import dbus

from .const import PROGID, INSTANCE_ID
from .columns import DColumns

class DTable(dbus.service.Object):
    IFACE_NAME = PROGID + '.Table'
    def __init__(self, model, object_path):
        session_bus = dbus.SessionBus()
        name = dbus.service.BusName(INSTANCE_ID, session_bus)
        dbus.service.Object.__init__(self, name, object_path)
        self.object_path = object_path
        self.model = model
        model.view = self
        self.columns = DColumns(self.model.columns, self.object_path + '/columns')
    
    @dbus.service.method(IFACE_NAME, out_signature='i')
    def RowCount(self):
        return len(self.model)
    
    @dbus.service.method(IFACE_NAME, in_signature='is', out_signature='s')
    def GetCellValue(self, row_index, attrname):
        row = self.model[row_index]
        return row.get_cell_value(attrname)
    
    @dbus.service.method(IFACE_NAME, out_signature='s')
    def ColumnsPath(self):
        return self.columns.object_path
    
    #--- Signals
    @dbus.service.signal(IFACE_NAME)
    def Refresh(self):
        pass
    
    #--- Callbacks
    def refresh(self):
        self.Refresh()
    
