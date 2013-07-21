import dbus.service
import dbus

from .const import PROGID, INSTANCE_ID

class DColumns(dbus.service.Object):
    IFACE_NAME = PROGID + '.Columns'
    def __init__(self, model, object_path):
        session_bus = dbus.SessionBus()
        name = dbus.service.BusName(INSTANCE_ID, session_bus)
        dbus.service.Object.__init__(self, name, object_path)
        self.object_path = object_path
        self.model = model
        # model.view = self
    
    @dbus.service.method(IFACE_NAME, out_signature='i')
    def Count(self):
        return self.model.columns_count()
    
    @dbus.service.method(IFACE_NAME, in_signature='i', out_signature='s')
    def AttrnameAtIndex(self, index):
        return self.model.column_by_index(index).name
    
    @dbus.service.method(IFACE_NAME, in_signature='i', out_signature='s')
    def DisplayAtIndex(self, index):
        return self.model.column_by_index(index).display
