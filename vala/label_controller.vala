using Gtk;

public class LabelController {
    
    private Label labelView;
    private DTextField model;
    
    public LabelController(string proxy_path, Label labelView) throws IOError {
        this.labelView = labelView;
        this.model = Bus.get_proxy_sync(BusType.SESSION, get_dbus_server_name(), proxy_path);
        this.model.refresh.connect(() => {
            try {
                this.labelView.set_text(this.model.text());
            } catch (IOError e) {}
        });
    }
}
