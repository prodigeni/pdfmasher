using Gtk;

public class MainWindow : Window {
    private DApp model;
    private TableController elementTable;
    private LabelController openedFileLabel;
    private ProgressWindow progress_window;
    
    public MainWindow(DApp aApp) throws IOError {
        const int PADDING = 5;
        this.model = aApp;
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
        
        var openedFileLabelView = left_aligned_label("Label");
        openedFileLabel = new LabelController(this.model.opened_file_label_path(), openedFileLabelView);
        openFileBox.pack_start(openedFileLabelView, true);
        
        vbox.pack_start(openFileBox, false);
        
        var hbox = new Box(Orientation.HORIZONTAL, PADDING);
        
        var mainNotebook = new Notebook();
        var elementTableViewWrapper = new ScrolledWindow(null, null);
        elementTableViewWrapper.shadow_type = ShadowType.OUT;
        var elementTableView = new TreeView();
        elementTableViewWrapper.add(elementTableView);
        this.elementTable = new ElementTable(this.model.element_table_path(), elementTableView);
        var tableLabel = new Label("Table");
        mainNotebook.append_page(elementTableViewWrapper, tableLabel);
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
        
        progress_window = new ProgressWindow(this.model.progress_window_path());
        
        openFileButton.clicked.connect(this.load_pdf);
        this.model.needs_load_path.connect(this.needs_load_path);
    }
    
    private void load_pdf() {
        try {
            this.model.load_pdf();
        } catch (IOError e) {}
    }
    
    private void needs_load_path(string prompt) {
        string result = "";
        var file_chooser = new FileChooserDialog (prompt, this,
            FileChooserAction.OPEN,
            Stock.CANCEL, ResponseType.CANCEL,
            Stock.OPEN, ResponseType.ACCEPT
        );
        if (file_chooser.run() == ResponseType.ACCEPT) {
            result = file_chooser.get_filename();
        }
        file_chooser.destroy();
        print(result);
        this.model.answer_to_query_load_path(result);
    }
}