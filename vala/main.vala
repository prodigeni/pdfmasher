using Gtk;

int main (string[] args) {
    Gtk.init (ref args);
    // DEntryPoint entry_point;
    // entry_point = Bus.get_proxy_sync(BusType.SESSION, DBUS_PROGID, "/entry");
    // var window = new MainWindow(entry_point.new_main_window());
    var window = new MainWindow("");
    window.show_all();
    Gtk.main();
    return 0;
}
