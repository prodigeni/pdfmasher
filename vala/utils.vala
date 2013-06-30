using Gtk;

Label left_aligned_label(string text) {
    var result = new Label(text);
    result.set_alignment(0.0f, 0.5f);
    return result;
}