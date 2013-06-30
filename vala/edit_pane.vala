using Gtk;

public class EditPane : Box {
    public EditPane() {
        const int PADDING = 5;
        Object(orientation: Orientation.VERTICAL, spacing: PADDING);
        
        this.margin = 10;
        
        var grid = new Grid();
        grid.set_row_homogeneous(true);
        grid.set_column_homogeneous(true);
        grid.set_row_spacing(5);
        grid.set_column_spacing(5);
        var normalButton = new Button.with_label("Normal");
        grid.attach(normalButton, 0, 0, 1, 1);
        var titleButton = new Button.with_label("Title");
        grid.attach(titleButton, 0, 1, 1, 1);
        var footnoteButton = new Button.with_label("Footnote");
        grid.attach(footnoteButton, 0, 2, 1, 1);
        var ignoreButton = new Button.with_label("Ignore");
        grid.attach(ignoreButton, 1, 0, 1, 1);
        var tofixButton = new Button.with_label("To Fix");
        grid.attach(tofixButton, 1, 1, 1, 1);
        
        this.pack_start(grid, false);
        
        var hideIgnoredCheckbox = new CheckButton.with_label("Hide Ignored Elements");
        this.pack_start(hideIgnoredCheckbox, false);
        
        var editTextViewWrapper = new ScrolledWindow(null, null);
        editTextViewWrapper.shadow_type = ShadowType.OUT;
        var editTextview = new TextView();
        editTextViewWrapper.add(editTextview);
        this.pack_start(editTextViewWrapper, true);
        
        var hbox = new Box(Orientation.HORIZONTAL, PADDING);
        var saveButton = new Button.with_label("Save");
        var cancelButton = new Button.with_label("Cancel");
        saveButton.width_request = cancelButton.width_request = 75;
        hbox.pack_end(cancelButton, false);
        hbox.pack_end(saveButton, false);
        this.pack_start(hbox, false);
    }
}