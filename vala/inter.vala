const string DBUS_PROGID = "org.hardcodedsoftware.pdfmasher";

[DBus (name = "org.hardcodedsoftware.pdfmasher.EntryPoint")]
interface DEntryPoint : Object {
    public abstract string new_app() throws IOError;
    public abstract void test() throws IOError;
    public abstract void exit() throws IOError;
}

[DBus (name = "org.hardcodedsoftware.pdfmasher.App")]
interface DApp : Object {
    public abstract string opened_file_label_path() throws IOError;
    public abstract void load_pdf() throws IOError;
}

[DBus (name = "org.hardcodedsoftware.pdfmasher.TextField")]
interface DTextField : Object {
    public abstract string text() throws IOError;
    public abstract void set_text(string s) throws IOError;
    
    public signal void refresh();
}