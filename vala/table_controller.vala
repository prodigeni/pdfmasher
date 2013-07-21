using Gtk;

public class TableController {
    private DTable model;
    private TreeView tree_view;
    private ListStore tree_model;
    private Column[] columns;
    
    public TableController(string proxy_path, TreeView tree_view) {
        this.tree_view = tree_view;
        this.tree_view.fixed_height_mode = true;
        this.model = Bus.get_proxy_sync(BusType.SESSION, get_dbus_server_name(), proxy_path);
        this.columns = get_columns(this.model.columns_path());
        Type[] column_types = {};
        foreach (Column c in this.columns) {
            column_types += typeof(string);
            int col_index = tree_view.insert_column_with_attributes(-1, c.display(),
                new CellRendererText(), "text", c.index());
            TreeViewColumn tvc = tree_view.get_column(col_index-1);
            tvc.set_sizing(TreeViewColumnSizing.FIXED);
            tvc.set_min_width(50);
        }
        this.tree_model = new ListStore.newv(column_types);
        this.tree_view.set_model(this.tree_model);
        this.model.refresh.connect(this.refresh);
    }
    
    private void refresh() {
        tree_model.clear();
        TreeIter iter;
        for (int i=0; i<model.row_count(); i++) {
            tree_model.append(out iter);
            foreach (Column c in this.columns) {
                tree_model.set_value(iter, c.index(), model.get_cell_value(i, c.attrname()));
            }
        }
    }
}
