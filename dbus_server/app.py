import time
from threading import Thread

import dbus.service
import dbus

from .const import PROGID, INSTANCE_ID
from .text_field import DTextField
from .table import DTable
from .page_repr import DPageRepr
from .progress_window import DProgressWindow

class DApp(dbus.service.Object):
    IFACE_NAME = PROGID + '.App'
    def __init__(self, mainloop):
        session_bus = dbus.SessionBus()
        name = dbus.service.BusName(INSTANCE_ID, session_bus)
        self.object_path = '/'
        dbus.service.Object.__init__(self, name, self.object_path)
        self.mainloop = mainloop
        self.model = None
    
    @dbus.service.method(IFACE_NAME)
    def Start(self):
        # We initialize our model app in Start instead of __init__ so that the UI can connect with
        # the server as early as possible. Importing the model is time-consuming, so we do it here
        #too.
        if self.model is not None:
            return
        from core.app import App
        self.model = App(view=self)
        self.opened_file_label = DTextField(self.model.opened_file_label, self.object_path + 'opened_file_label')
        self.progress_window = DProgressWindow(self.model.progress_window, self.object_path + 'progress_window')
        self.element_table = DTable(self.model.element_table, self.object_path + 'element_table')
        # All the code below is dirty placeholder code to avoid callback exception upon loading.
        # Nothing of this is working or correct.
        self.page_controller = DPageRepr(self.model.page_controller, self.object_path + 'page_controller')
        self.page_repr = DPageRepr(self.model.page_controller.page_repr, self.object_path + 'page_repr')
        self.build_pane = DPageRepr(self.model.build_pane, self.object_path + 'build_pane')
        self.edit_pane = DPageRepr(self.model.edit_pane, self.object_path + 'edit_pane')
    
    @dbus.service.method(IFACE_NAME)
    def Exit(self):
        self.mainloop.quit()
    
    @dbus.service.method(IFACE_NAME, out_signature='s')
    def OpenedFileLabelPath(self):
        return self.opened_file_label.object_path
    
    @dbus.service.method(IFACE_NAME, out_signature='s')
    def ProgressWindowPath(self):
        return self.progress_window.object_path
    
    @dbus.service.method(IFACE_NAME, out_signature='s')
    def ElementTablePath(self):
        return self.element_table.object_path
    
    @dbus.service.method(IFACE_NAME)
    def LoadPdf(self):
        # Call has to be threaded because it results in a user-input-asking signal
        Thread(target=self.model.load_pdf).start()
    
    @dbus.service.method(IFACE_NAME, in_signature='s')
    def AnswerToQueryLoadPath(self, load_path):
        self.answer_to_query_load_path = load_path
    
    #--- Signals
    @dbus.service.signal(IFACE_NAME, signature='s')
    def NeedsLoadPath(self, prompt):
        pass
    
    #--- Callbacks
    def query_load_path(self, prompt, filetypes):
        # The lack of return values for DBus signal makes this kind of callback very awkward to
        # implement, but since return values are rather rare, I guess we can tolerate this
        # awkwardness.
        self.answer_to_query_load_path = None
        self.NeedsLoadPath(prompt)
        while self.answer_to_query_load_path is None:
            time.sleep(0.1)
        return self.answer_to_query_load_path
        return None
    
