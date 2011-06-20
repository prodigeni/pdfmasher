Quickstart
==========

Let's say that you have a basic PDF file with a simple text. You'd convert it with a simple 
converter, but the problem is that each page has a header, which you'd like to get rid of. Also, 
your text has footnotes and you'd like them to be at the end of your text.

1. Open your PDF file with the Open File button. A list of elements will appear in the elements 
   table.
2. Sort the table by Y-Position by clicking on the "Y" column. All headers will end up grouped 
   together at the bottom of the table because they're the elements that have the highest Y values.
3. Shift-select all header elements and click on the Ignored button in the Edit pane. The state of 
   the elements will change from "normal" to "ignored".
4. Enable the "Hide ignored elements" so that stuff like page number elements don't hinder us for 
   the next operation.
5. To identify footnotes, sort the elements by "Text". This way, footnotes, because they start by a
   number, will be grouped together.
6. Select all footnotes elements and click on "Footnote" in the Edit pane.
7. Click on "View HTML" from the Build pane. Make sure the result satisfy you.
8. Convert the HTML to ebook using Calibre or another tool.
