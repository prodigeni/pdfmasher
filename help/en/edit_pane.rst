Edit Pane
=========

The "Edit" pane at the bottom of the main window lets you alter the currently selected elements. The
4 buttons at the left change the state of the selected elements. This is their meaning:

* Normal (N): The text will be displayed normally in the result HTML.
* Title (T): The text will be a title (H1) in the result HTML.
* Footnote (F): The text will be moved at the bottom of the document, and an attempt will be made to 
  create an hyperlink to it in the text.
* To Fix (X): Sometimes, there's no way around it, you're gonna have to manually fix the Markdown file.
  In these cases, you can flag elements with this flag and "FIXME" will be inserted next to the
  element in the Markdown. This way, you can easily locate those elements.
* Ignored (I): The text will not appear in the result HTML.

The first thing you usually want to do is to flag your "Ignored" elements, and then go on with 
footnotes and titles. Often, ignored elements can get in your way. This is why there's a "Hide 
ignored elements". When it's enabled, ignored elements will disappear from the table.

Titles have multiple levels (1 to 6). 1 is the biggest title and 6 is the smallest. To select a
title level, simply click on the "Title" button repeatedly. It will cycle the element's title level
from 1 to 6. The current title will be shown in the "State" column. For example, "Title (3)" means a
title of level 3.

Because clicking buttons is slow, there's also keyboard shortcuts for each flag. When the element
table has the focus, clicking on a letter associated (in parenthesis above) with a flag will set 
selected elements to that flag. For example, pressing "T" will set all selected elements to Title.

You can also manually tweak the text of elements. For this, you'll need to select only one element.
Then, change the text and press "Save".
