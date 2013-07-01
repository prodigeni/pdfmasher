using Gtk;

int main (string[] args) {
    Gtk.init (ref args);
    var ts = (new DateTime.now_local()).to_unix();
    Process.spawn_command_line_async ("./env/bin/python -m dbus_server");
    try {
        DEntryPoint entry_point = Bus.get_proxy_sync(BusType.SESSION, DBUS_PROGID, "/entry");
        // The server is very probably not up yet. What we do is that we repeatedly test whether
        // the server is up until it is, for a maximum of 10 seconds.
        for (int i=0; i<100; i++) {
            try {
                entry_point.test();
                print("Server is up!\n");
                break;
            } catch (Error ex) {
                print("Still waiting for the server to be up...\n");
                Posix.usleep(100000); // 1/10th of a second
            }
        }
        var window = new MainWindow(entry_point.new_app());
        window.show_all();
        Gtk.main();
        entry_point.exit();
    } catch (IOError ex) {
        print("DBus communication problems, exiting.\n");
        return 1;
    } catch (Error ex) {
        print("DBus communication problems, exiting.\n");
        return 1;
    }
    return 0;
}
