Page Representation
===================

For simple texts, using the table is enough. However, some PDFs have a complex layout and it's not 
possible for a program to automatically guess the correct reading order in these layouts. This is 
why there's a "Page" tab.

This tab shows the layout of each page in the PDF, one at a time. You can navigate through pages 
with the arrow buttons at the bottom of the view. The page representation contains a rectangle -- 
placed proportionally to its actual position in the PDF -- for each text element. You can select 
elements in this page with the mouse, and selected elements can be edited like it is with the
elements table. The color of the elements change according to their state.

Editing elements is one of the uses of the Page view, but it's not its main use (the Table tab is
most of the time more efficient for this). No, the reason why the Page tab exists is to allow you to
manually re-define the reading order of the elements. You see the "Re-order mode" checkbox? Click 
it.

Cool huh? What you see is the representation of the reading order of the current page through little
arrows going from element to element. Guess what? You can change it! Cmon cmon, go ahead, click on
an element, hold the mouse button, drag to somewhere else while crossing one or more elements, and
release the mouse button. Tadaa! The reading order of the elements you touched with your arrow will
change according to it! I know, too cool to be true, but you have it right in front of you.

Now, you can easily define the reading order of complex layouts like newspaper layouts.

Ok, here's another cool trick: Sometimes, it's not possible to draw an arrow from one element to
another without mistakenly touching another element which we don't want in our new order. For
example, if you have two columns close to each other, you can't draw an arrow from the bottom of the
first column to the top of the next without touching other elements. In these cases, the **Shift**
key is your friend. If you hold the shift key while drawing your order arrows, they will be
"buffered" until you release the shift key, so you'll draw multiple arrows at once. Buffered arrows
are considered a single arrow by PdfMasher. Therefore, if you have two columns of text, drawing a
buffered arrow on the first column and then the second column will be as if you managed to draw an
arrow between the last element of the first column and the first element of the second column.

This might all seem a bit complicated, but try it, you'll understand.