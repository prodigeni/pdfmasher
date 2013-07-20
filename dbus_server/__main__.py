from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GObject, Gdk

from .app import DApp

def main():
    # threads_init() is very important, it allows Python threading within the server. If we don't
    # call it, the GIL will always stay locked.
    GObject.threads_init()
    Gdk.threads_init()
    DBusGMainLoop(set_as_default=True)
    mainloop = GObject.MainLoop()
    app = DApp(mainloop)
    print("PdfMasher's DBus server running")
    mainloop.run()
    print("PdfMasher's DBus server stopping")

if __name__ == '__main__':
    main()
