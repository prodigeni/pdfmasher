import dbus.service
import dbus

from .const import PROGID, INSTANCE_ID
from .text_field import DTextField

class DProgressWindow(dbus.service.Object):
    IFACE_NAME = PROGID + '.ProgressWindow'
    def __init__(self, model, object_path):
        session_bus = dbus.SessionBus()
        name = dbus.service.BusName(INSTANCE_ID, session_bus)
        dbus.service.Object.__init__(self, name, object_path)
        self.object_path = object_path
        self.model = model
        model.view = self
        self.jobdesc_textfield = DTextField(self.model.jobdesc_textfield, self.object_path + '/jobdesc_textfield')
        self.progressdesc_textfield = DTextField(self.model.progressdesc_textfield, self.object_path + '/progressdesc_textfield')
    
    @dbus.service.method(IFACE_NAME, out_signature='s')
    def JobdescTextfieldPath(self):
        return self.jobdesc_textfield.object_path
    
    @dbus.service.method(IFACE_NAME, out_signature='s')
    def ProgressdescTextfieldPath(self):
        return self.progressdesc_textfield.object_path
    
    @dbus.service.method(IFACE_NAME)
    def Pulse(self):
        return self.model.pulse()
    
    @dbus.service.method(IFACE_NAME)
    def Cancel(self):
        return self.model.cancel()
    
    #--- Signals
    @dbus.service.signal(IFACE_NAME, signature='i')
    def SetProgress(self, last_progress):
        pass
    
    @dbus.service.signal(IFACE_NAME)
    def Show(self):
        pass
    
    @dbus.service.signal(IFACE_NAME)
    def Close(self):
        pass
    
    #--- Callbacks
    def set_progress(self, last_progress):
        self.SetProgress(last_progress)
        
    def show(self):
        self.Show()
    
    def close(self):
        self.Close()
    
