using Gtk;

public class ElementTable : TableController {
    public ElementTable(string proxy_path, TreeView tree_view) {
        base(proxy_path, tree_view);
    }
    
    protected override int[] get_default_widths() {
        return {
            50,
            50,
            50,
            50,
            70,
            70,
            75,
            150
        };
    }
}