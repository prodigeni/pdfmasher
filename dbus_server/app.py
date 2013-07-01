import dbus.service
import dbus

from core.app import App
from .const import PROGID
from .text_field import DTextField

class DApp(dbus.service.Object):
    IFACE_NAME = PROGID + '.App'
    def __init__(self, object_path):
        session_bus = dbus.SessionBus()
        name = dbus.service.BusName(PROGID, session_bus)
        dbus.service.Object.__init__(self, name, object_path)
        self.object_path = object_path
        self.model = App(view=self)
        self.opened_file_label = DTextField(self.model.opened_file_label, self.object_path + '/opened_file_label')
    
    @dbus.service.method(IFACE_NAME, out_signature='s')
    def OpenedFileLabelPath(self):
        return self.opened_file_label.object_path
    
    @dbus.service.method(IFACE_NAME)
    def LoadPdf(self):
        self.model.load_pdf()
    
