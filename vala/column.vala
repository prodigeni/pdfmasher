public class Column {
    private DColumns _columns;
    private int _index;
    private string _attrname;
    private string _display;
    
    public Column(DColumns columns, int index) {
        this._columns = columns;
        this._index = index;
        this._attrname = columns.attrname_at_index(index);
        this._display = columns.display_at_index(index);
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
}

Column[] get_columns(string proxy_path) {
    DColumns model = Bus.get_proxy_sync(BusType.SESSION, get_dbus_server_name(), proxy_path);
    Column[] result = {};
    for (int i=0; i<model.count(); i++) {
        result += new Column(model, i);
    }
    return result;
}