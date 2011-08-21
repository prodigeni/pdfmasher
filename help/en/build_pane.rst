Build Pane
==========

Building an ebook document is done in three steps. First, we build an intermediate `Markdown`_
file, then we build a HTML file from that Markdown, and finally, we generate a MOBI or EPUB from that HTML. The Markdown intermediate step lets you make modifications to
the whole file using search and replace or other neat stuff that your favorite text editor can do.
For example, you could use regular expressions search/replace to find all lines ending with an
hyphen and then join it with the next line (the hyphen is irrelevant in an ebook and will only make
reading harder). So, here's what you do:

1. Click on Generate Markdown. This will create a ".txt" file with the same name as your pdf.
2. Edit your Markdown file. Clicking on "Edit Markdown" will open the file with the application 
   associated with text files. If you prefer, you can use the "Reveal" button and open your text 
   file with another application.
3. Click on "View HTML". This will create an html file with the same name as the source pdf (except 
   with a ".htm" extension) and open it in your default browser.
4. Make sure that your HTML looks like what you'll want to read on your ebook. If not, go back to
   the editing pane.
5. Write down the title and author of your document. This metadata is used in your ebook to manage
   your documents.
6. Select whether you want a MOBI or an EPUB, and click on "Generate e-book". You now have a ready
   to read ebook document!

A few things to know
--------------------

**Page breaks:** Titles of level 1 and 2 will generate page breaks. So if you don't want your title
to generate a page break, select a level of 3 or more.

.. _Markdown: http://daringfireball.net/projects/markdown/