using Gtk;

int main (string[] args) {
    Gtk.init (ref args);
    string[] spawn_args = {"/home/hsoft/src/pdfmasher/env/bin/python", "-m", "dbus_server"};
    string[] spawn_env = Environ.get();
    Pid child_pid;
    Process.spawn_async("/home/hsoft/src/pdfmasher",
        spawn_args,
        spawn_env,
        SpawnFlags.SEARCH_PATH | SpawnFlags.DO_NOT_REAP_CHILD,
        null,
        out child_pid
    );
    string dbus_name = "%s.pid%d".printf(DBUS_PROGID, child_pid);
    try {
        DApp app = Bus.get_proxy_sync(BusType.SESSION, dbus_name, "/");
        // The server is very probably not up yet. What we do is that we repeatedly try to start
        // the server until it works, for a maximum of 10 seconds.
        for (int i=0; i<100; i++) {
            try {
                app.start();
                print("Server is up!\n");
                break;
            } catch (Error ex) {
                print("Still waiting for the server to be up...\n");
                Posix.usleep(100000); // 1/10th of a second
            }
        }
        var window = new MainWindow(app);
        window.show_all();
        Gtk.main();
        app.exit();
    } catch (IOError ex) {
        print("DBus communication problems, exiting.\n");
        return 1;
    } catch (Error ex) {
        print("DBus communication problems, exiting.\n");
        return 1;
    }
    return 0;
}
