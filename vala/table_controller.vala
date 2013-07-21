using Gtk;

public class TableController {
    protected DTable model;
    protected TreeView tree_view;
    protected ListStore tree_model;
    protected Columns columns;
    
    public TableController(string proxy_path, TreeView tree_view) {
        this.tree_view = tree_view;
        this.tree_view.fixed_height_mode = true;
        this.tree_view.headers_clickable = true;
        this.model = Bus.get_proxy_sync(BusType.SESSION, get_dbus_server_name(), proxy_path);
        this.columns = new Columns(this.model.columns_path(), tree_view);
        this.columns.initial_config(get_default_widths());
        Type[] column_types = {};
        foreach (Column c in this.columns.columns) {
            column_types += typeof(string);
        }
        this.tree_model = new ListStore.newv(column_types);
        this.tree_view.set_model(this.tree_model);
        this.model.refresh.connect(this.refresh);
    }
    
    protected virtual int[] get_default_widths() {
        return {};
    }
    
    protected void refresh() {
        tree_model.clear();
        TreeIter iter;
        for (int i=0; i<model.row_count(); i++) {
            tree_model.append(out iter);
            foreach (Column c in this.columns.columns) {
                tree_model.set_value(iter, c.index(), model.get_cell_value(i, c.attrname()));
            }
        }
    }
}
