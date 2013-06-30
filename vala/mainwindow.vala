using Gtk;

public class MainWindow : Window {
    public MainWindow(string proxy_path) {
        const int PADDING = 5;
        this.title = "PdfMasher";
        this.window_position = WindowPosition.CENTER;
        this.border_width = 8;
        this.set_default_size(900, 600);
        this.destroy.connect(Gtk.main_quit);
        
        var vbox = new Box(Orientation.VERTICAL, PADDING);
        this.add(vbox);
        
        var openFileBox = new Box(Orientation.HORIZONTAL, PADDING);
        
        var openFileButton = new Button.with_label("Open File");
        openFileBox.pack_start(openFileButton, false);
        
        var openedFileLabel = left_aligned_label("Label");
        openFileBox.pack_start(openedFileLabel, true);
        
        vbox.pack_start(openFileBox, false);
        
        var hbox = new Box(Orientation.HORIZONTAL, PADDING);
        
        var mainNotebook = new Notebook();
        var tableBox = new Box(Orientation.VERTICAL, PADDING);
        var tableLabel = new Label("Table");
        mainNotebook.append_page(tableBox, tableLabel);
        var pageBox = new Box(Orientation.VERTICAL, PADDING);
        var pageLabel = new Label("Page");
        mainNotebook.append_page(pageBox, pageLabel);
        hbox.pack_start(mainNotebook, true);
        
        var toolsNotebook = new Notebook();
        toolsNotebook.width_request = 300;
        var editPane = new EditPane();
        toolsNotebook.append_page(editPane, new Label("Edit"));
        var buildPane = new BuildPane();
        toolsNotebook.append_page(buildPane, new Label("Build"));
        hbox.pack_start(toolsNotebook, false);
        
        vbox.pack_start(hbox, true);
    }
}