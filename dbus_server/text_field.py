import dbus.service
import dbus

from core.app import App
from .const import PROGID

class DTextField(dbus.service.Object):
    IFACE_NAME = PROGID + '.TextField'
    def __init__(self, model, object_path):
        session_bus = dbus.SessionBus()
        name = dbus.service.BusName(PROGID, session_bus)
        dbus.service.Object.__init__(self, name, object_path)
        self.object_path = object_path
        self.model = model
        model.view = self
    
    @dbus.service.method(IFACE_NAME, out_signature='s')
    def Text(self):
        return self.model.text
    
    @dbus.service.method(IFACE_NAME, in_signature='s')
    def SetText(self, text):
        self.model.text = text
    
    #--- Signals
    @dbus.service.signal(IFACE_NAME)
    def Refresh(self):
        pass
    
    #--- Callbacks
    def refresh(self):
        self.Refresh()
    
