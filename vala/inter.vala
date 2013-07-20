const string DBUS_PROGID = "org.hardcodedsoftware.pdfmasher";

[DBus (name = "org.hardcodedsoftware.pdfmasher.App")]
public interface DApp : Object {
    public abstract void start() throws IOError;
    public abstract void exit() throws IOError;
    public abstract string opened_file_label_path() throws IOError;
    public abstract string progress_window_path() throws IOError;
    public abstract void load_pdf() throws IOError;
    public abstract void answer_to_query_load_path(string load_path) throws IOError;
    
    public signal void needs_load_path(string prompt);
}

[DBus (name = "org.hardcodedsoftware.pdfmasher.ProgressWindow")]
interface DProgressWindow : Object {
    public abstract string jobdesc_textfield_path() throws IOError;
    public abstract string progressdesc_textfield_path() throws IOError;
    public abstract void pulse() throws IOError;
    public abstract void cancel() throws IOError;
    
    public signal void set_progress(int progress);
    public signal void show();
    public signal void close();
}

[DBus (name = "org.hardcodedsoftware.pdfmasher.TextField")]
interface DTextField : Object {
    public abstract string text() throws IOError;
    public abstract void set_text(string s) throws IOError;
    
    public signal void refresh();
}