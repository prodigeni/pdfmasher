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
    
    # This method *has* to be called because it sets default widths, and only then it connects the
    # view.
    @dbus.service.method(IFACE_NAME, in_signature='ai')
    def InitialConfig(self, default_widths):
        for i, width in enumerate(default_widths):
            attrname = self.model.column_by_index(i).name
            self.model.set_default_width(attrname, width)
        self.model.view = self
    
    @dbus.service.method(IFACE_NAME, out_signature='i')
    def Count(self):
        return self.model.columns_count()
    
    @dbus.service.method(IFACE_NAME, in_signature='i', out_signature='s')
    def AttrnameAtIndex(self, index):
        return self.model.column_by_index(index).name
    
    @dbus.service.method(IFACE_NAME, in_signature='s', out_signature='s')
    def Display(self, attrname):
        return self.model.column_display(attrname)
    
    @dbus.service.method(IFACE_NAME, in_signature='s', out_signature='i')
    def Width(self, attrname):
        result = self.model.column_width(attrname)
        if not result:
            result = self.model.column_by_name(attrname).default_width
        return result
    
    #--- Signals
    @dbus.service.signal(IFACE_NAME)
    def RestoreColumns(self):
        pass
    
    @dbus.service.signal(IFACE_NAME, signature='sb')
    def SetColumnVisible(self, colname, visible):
        pass
    
    #--- Callbacks
    def restore_columns(self):
        print('restore')
        self.RestoreColumns()
    
    def set_column_visible(self, colname, visible):
        self.SetColumnVisible(colname, visible)
    
