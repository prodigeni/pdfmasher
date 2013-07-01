import dbus.service
import dbus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GObject

from .app import DApp
from .const import PROGID

class DEntryPoint(dbus.service.Object):
    IFACE_NAME = PROGID + '.EntryPoint'
    
    def __init__(self, mainloop):
        session_bus = dbus.SessionBus()
        name = dbus.service.BusName(PROGID, session_bus)
        dbus.service.Object.__init__(self, name, '/entry')
        self.apps = []
        self.mainloop = mainloop
    
    @dbus.service.method(IFACE_NAME, out_signature='s')
    def NewApp(self):
        index = len(self.apps)
        object_path = '/app/%d' % index
        app = DApp(object_path)
        self.apps.append(app)
        return object_path
    
    @dbus.service.method(IFACE_NAME)
    def Test(self): # this is there just to test whether the service is up
        pass
    
    @dbus.service.method(IFACE_NAME)
    def Exit(self):
        self.mainloop.quit()
    

def main():
    DBusGMainLoop(set_as_default=True)
    mainloop = GObject.MainLoop()
    entry = DEntryPoint(mainloop)
    print("PdfMasher's DBus server running")
    mainloop.run()
    print("PdfMasher's DBus server stopping")

if __name__ == '__main__':
    main()
