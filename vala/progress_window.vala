using Gtk;

public class ProgressWindow : Window {
    private DProgressWindow model;
    private LabelController jobdesc_label;
    private LabelController progressdesc_label;
    private ProgressBar progressbar;
    private uint active_timer_id;
    
    public ProgressWindow (string proxy_path) {
        this.title = "Progress";
        this.border_width = 10;
        this.window_position = WindowPosition.CENTER;
        this.model = Bus.get_proxy_sync(BusType.SESSION, DBUS_PROGID, proxy_path);
        set_default_size(350, 100);
        create_widgets();
    }
    
    private void create_widgets() {
        const int PADDING = 5;
        var vbox = new Box(Orientation.VERTICAL, PADDING);
        var jobdesc_label_view = left_aligned_label("");
        vbox.pack_start(jobdesc_label_view, false);
        progressbar = new ProgressBar();
        vbox.pack_start(progressbar, false);
        var progressdesc_label_view = left_aligned_label("");
        vbox.pack_start(progressdesc_label_view, false);
        var hbox = new Box(Orientation.HORIZONTAL, PADDING);
        var cancelButton = new Button.with_label("Cancel");
        hbox.pack_end(cancelButton, false);
        vbox.pack_start(hbox);
        this.add(vbox);
        
        jobdesc_label = new LabelController(this.model.jobdesc_textfield_path(), jobdesc_label_view);
        progressdesc_label = new LabelController(this.model.progressdesc_textfield_path(), progressdesc_label_view);
        
        cancelButton.clicked.connect(() => {
            this.model.cancel();
        });
        this.model.show.connect(this.show_window);
        this.model.close.connect(this.close_window);
        this.model.set_progress.connect((progress) => {
            if (progress > 0) {
                this.progressbar.set_fraction(progress / 100.0f);
            }
            else {
                this.progressbar.pulse();
            }
        });
    }
    
    private bool pulse() {
        this.model.pulse();
        return true;
    }
    
    private void show_window() {
        this.set_modal(true);
        this.show_all();
        active_timer_id = Timeout.add(100, this.pulse);
    }
    
    private void close_window() {
        this.set_modal(false);
        this.hide();
        GLib.Source.remove(active_timer_id);
    }
}