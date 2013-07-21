using Gtk;

public class Column {
    private DColumns _columns;
    private int _index;
    private string _attrname;
    private string _display;
    private int _width;
    
    public Column(DColumns columns, int index) {
        this._columns = columns;
        this._index = index;
        this._attrname = _columns.attrname_at_index(_index);
        update();
    }
    
    public int index() {
        return this._index;
    }
    
    public string attrname() {
        return this._attrname;
    }
    
    public string display() {
        return this._display;
    }
    
    public int width() {
        return this._width;
    }
    
    public void update() {
        this._display = _columns.display(_attrname);
        this._width = _columns.width(_attrname);
    }
}

public class Columns {
    private DColumns model;
    private TreeView tree_view;
    public Column[] columns;
    
    public Columns(string proxy_path, TreeView tree_view) {
        this.model = Bus.get_proxy_sync(BusType.SESSION, get_dbus_server_name(), proxy_path);
        this.tree_view = tree_view;
        Column[] new_columns = {};
        for (int i=0; i<model.count(); i++) {
            Column c = new Column(model, i);
            int col_index = tree_view.insert_column_with_attributes(-1, c.display(),
                new CellRendererText(), "text", c.index());
            TreeViewColumn tvc = tree_view.get_column(col_index-1);
            tvc.sizing = TreeViewColumnSizing.FIXED;
            tvc.resizable = true;
            new_columns += c;
        }
        this.columns = new_columns;
        model.restore_columns.connect(restore_columns);
    }
    
    private void restore_columns() {
        foreach (Column c in columns) {
            c.update();
            TreeViewColumn tvc = tree_view.get_column(c.index());
            tvc.fixed_width = c.width();
        }
    }
    
    public void initial_config(int[] default_widths) {
        model.initial_config(default_widths);
    }
}
