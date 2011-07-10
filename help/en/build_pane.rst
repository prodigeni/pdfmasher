Build Pane
==========

Building the final HTML file is done in two steps. First, we build an intermediate `Markdown`_ file 
and then we build the final HTML file from that Markdown. This lets you make modifications to the
whole file using search and replace or other neat stuff that your favorite text editor can do. For
example, you could use regular expressions search/replace to find all lines ending with an hyphen
and then join it with the next line (the hyphen is irrelevant in an ebook and will only make reading
harder). So, here's what you do:

1. Click on Generate Markdown. This will create a ".txt" file with the same name as your pdf.
2. Edit your Markdown file. Clicking on "Edit Markdown" will open the file with the application 
   associated with text files. If you prefer, you can use the "Reveal" button and open your text 
   file with another application.
3. Click on "View HTML". This will create an html file with the same name as the source pdf (except 
   with a ".htm" extension) and open it in your default browser.

Once you're satisfied with the results, you can use an external tool, such as Calibre, to convert
the html to .mobi or .epub. I plan to eventually support direct mobi/epub conversion, but it ain't 
for now.

.. _Markdown: http://daringfireball.net/projects/markdown/