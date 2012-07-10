PdfMasher Help
==============

PdfMasher is a tool to convert PDF files containing text to MOBI or EPUB. Most ebook readers support
PDF files natively, but it's often a real pain to read those documents because we don't have font
size control over the document like we have with native ebooks. In many cases, we have to use the
zooming feature and it's just a pain. Another drawback of PDFs on ebook readers is that annotations
are not supported.

There are already tools to convert PDFs to ebooks like `Calibre`_, but what they do is that they try
to guess the role of each piece of text in the PDF. I think that in all but the simplest cases, it's
a mistake to think that anything short of an AI can do that kind of guessing.

Enter PdfMasher. PdfMasher asks the user about the role of each piece of text, and does it in
an efficient manner. Your PDF has a header on each page and you don't want them to litter your text?
Sort text elements by Y-position (thus grouping them all together), shift select the elements and
flag them as ignored. They will not appear on your final HTML. Your PDF has footnotes on many pages? 
Sort your elements by text content (thus grouping all elements with the text starting with a number 
together) and flag them as footnotes. They will be moved to the end of the document, and PdfMasher
will try to create hyperlinks to footnote references.

Early Development
-----------------

PdfMasher is in very early development. I'm releasing this preview version to get a feedback loop
started. For PdfMasher 1.0 to be any good, I need to have a lot of PDF samples. PdfMasher doesn't 
work for you? Please `let me know`_!

Contents:

.. toctree::
   :maxdepth: 2
   
   quickstart
   elements_table
   page_repr
   edit_pane
   build_pane
   save_load
   changelog


.. _Calibre: http://calibre-ebook.com/
.. _let me know: http://www.hardcoded.net/support/