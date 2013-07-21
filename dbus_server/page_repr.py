import dbus.service
import dbus

from .const import PROGID, INSTANCE_ID

class DPageRepr(dbus.service.Object):
    IFACE_NAME = PROGID + '.PageRepr'
    def __init__(self, model, object_path):
        session_bus = dbus.SessionBus()
        name = dbus.service.BusName(INSTANCE_ID, session_bus)
        dbus.service.Object.__init__(self, name, object_path)
        self.object_path = object_path
        self.model = model
        model.view = self
    
    #--- Signals
    @dbus.service.signal(IFACE_NAME)
    def Refresh(self):
        pass
    
    #--- Callbacks
    def refresh(self):
        self.Refresh()
    
    def refresh_page_label(self):
        pass
        
    def refresh_edit_text(self):
        pass
