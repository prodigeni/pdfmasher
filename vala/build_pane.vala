using Gtk;

public class BuildPane : Box {
    public BuildPane() {
        const int PADDING = 5;
        Object(orientation: Orientation.VERTICAL, spacing: PADDING);
        
        this.margin = 10;
        
        var step1Label = left_aligned_label("Step 1: Generate Markdown");
        this.pack_start(step1Label, false);
        var genMarkdownButton = new Button.with_label("Generate Markdown");
        this.pack_start(genMarkdownButton, false);
        var genTimeLabel = left_aligned_label("Gen Time Label");
        this.pack_start(genTimeLabel, false);
        
        var step2Label = left_aligned_label("Step 2: Post-processing");
        this.pack_start(step2Label, false);
        
        var editMarkdownButton = new Button.with_label("Edit Markdown");
        this.pack_start(editMarkdownButton, false);
        var revealMarkdownButton = new Button.with_label("Reveal Markdown");
        this.pack_start(revealMarkdownButton, false);
        var viewHTMLButton = new Button.with_label("View HTML");
        this.pack_start(viewHTMLButton, false);
         
        var step3Label = left_aligned_label("Step 3: E-book creation");
        this.pack_start(step3Label, false);
        var hbox = new Box(Orientation.HORIZONTAL, PADDING);
        var mobiRadio = new RadioButton.with_label_from_widget(null, "MOBI");
        hbox.pack_start(mobiRadio, true);
        var epubRadio = new RadioButton.with_label_from_widget(mobiRadio, "EPUB");
        hbox.pack_start(epubRadio, true);
        this.pack_start(hbox, false);
        
        var grid = new Grid();
        grid.set_row_homogeneous(true);
        grid.set_row_spacing(5);
        grid.set_column_spacing(5);
        grid.expand = false;
        var titleLabel = left_aligned_label("Title:");
        var titleEntry = new Entry();
        var authorLabel = left_aligned_label("Author:");
        var authorEntry = new Entry();
        titleEntry.expand = authorEntry.expand = true;
        grid.attach(titleLabel, 0, 0, 1, 1);
        grid.attach(titleEntry, 1, 0, 1, 1);
        grid.attach(authorLabel, 0, 1, 1, 1);
        grid.attach(authorEntry, 1, 1, 1, 1);
        this.pack_start(grid, false);
        
        var createEbookButton = new Button.with_label("Create e-book");
        this.pack_start(createEbookButton, false);
    }
}