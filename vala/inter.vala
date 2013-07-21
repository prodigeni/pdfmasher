const string DBUS_PROGID = "org.hardcodedsoftware.pdfmasher";
int DBUS_SERVER_PID = 0;

string get_dbus_server_name() {
    return "%s.pid%d".printf(DBUS_PROGID, DBUS_SERVER_PID);
}
    
[DBus (name = "org.hardcodedsoftware.pdfmasher.App")]
public interface DApp : Object {
    public abstract void start() throws IOError;
    public abstract void exit() throws IOError;
    public abstract string opened_file_label_path() throws IOError;
    public abstract string progress_window_path() throws IOError;
    public abstract string element_table_path() throws IOError;
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

[DBus (name = "org.hardcodedsoftware.pdfmasher.Columns")]
public interface DColumns : Object {
    public abstract void initial_config(int[] default_widths) throws IOError;
    public abstract int count() throws IOError;
    public abstract string attrname_at_index(int index) throws IOError;
    public abstract string display(string attrname) throws IOError;
    public abstract int width(string attrname) throws IOError;
    
    public signal void restore_columns();
    public signal void set_column_visible();
}

[DBus (name = "org.hardcodedsoftware.pdfmasher.Table")]
public interface DTable : Object {
    public abstract int row_count() throws IOError;
    public abstract string get_cell_value(int row, string attrname) throws IOError;
    
    public abstract string columns_path() throws IOError;
    
    public signal void refresh();
}
