# Created By: Virgil Dupras
# Created On: 2011-06-12
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

import re

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams, LTItem, LTChar, LTTextLineHorizontal, LTTextBox
from pdfminer.converter import PDFPageAggregator

from jobprogress.job import nulljob

###### PDF Wisdom (some wisdom gathered about pdf/pdfminer during the development of this unit)
# 
#--- Coordinates
#
# So there's x0/y0 and x1/y1. x0 is left and y0 is bottom. The point (0, 0) is the bottom left point
# of the page.
#
#--- Footnotes / superscript
# 
# At first, I wanted to detect footnotes by detecting which characters were superscript, and I
# wanted to do that by looking at the height of LTChar instance. But the thing is that the height
# of all chars, including superscript chars, is the same in a text container. Maybe it's possible
# to use y-pos compared to others, but then things get real complicated real fast (there can be
# multiple lines in a text container), so for now I took a more heuristic road, that is to ask the
# user which elements are footnotes and then look for the leading numbers/symbols of that footnote
# on the rest of the page.

class ElementState:
    Normal = 'normal'
    Title = 'title'
    Footnote = 'footnote'
    ToFix = 'tofix'
    Ignored = 'ignored'

class TextElement:
    def __init__(self, x, y, fontsize, text, layout_elem):
        # The X and the Y of a text element should always be its top left corner
        self.page = None # set later
        self.order = 0 # set later
        self.x = x
        self.y = y
        self.fontsize = fontsize
        self.text = text
        self.state = ElementState.Normal
        # This is for footnotes-processed text
        self.modified_text = None
        self.layout_elem = layout_elem
    
    def __repr__(self):
        return '<TextElement {page} {x}-{y} {state} "{text}">'.format(**self.__dict__)
    

class Page:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    
def extract_text_elements_from_pdf(path, j=nulljob):
    """Opens a PDF and extract every element that is text based (LTText).
    """
    fp = open(path, 'rb')
    doc = PDFDocument(caching=True)
    parser = PDFParser(fp)
    parser.set_document(doc)
    doc.set_parser(parser)
    doc.initialize()
    rsrcmgr = PDFResourceManager()
    laparams = LAParams(all_texts=True, paragraph_indent=5)
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pages = []
    elements = []
    enumerated_pages = list(enumerate(doc.get_pages()))
    progress_msg = "Reading page %i of %i"
    for pageno, page in j.iter_with_progress(enumerated_pages, progress_msg):
        interpreter.process_page(page)
        page_layout = device.get_result()
        pages.append(Page(page_layout.width, page_layout.height))
        textboxes = extract_textboxes(page_layout)
        for boxno, textbox in enumerate(textboxes):
            elem = create_element(textbox)
            elem.page = pageno
            elem.order = boxno
            elements.append(elem)
    return pages, elements

def create_element(layout_element):
    x = layout_element.x0
    y = layout_element.y1 # top left corner in pdfminer is x0/y1
    chars = extract_chars(layout_element)
    fontsize = get_avg_text_height(chars)
    text = fix_text(get_text(layout_element))
    return TextElement(x, y, fontsize, text, layout_element)

def extract_from_elem(elem, lookfor):
    if isinstance(elem, lookfor):
        return [elem]
    else:
        try:
            return sum((extract_from_elem(subelem, lookfor) for subelem in elem), [])
        except TypeError:
            return []

def extract_chars(elem):
    """Returns a list of chars contained (possibly recursively) in `elem`.
    """
    return extract_from_elem(elem, lookfor=LTChar)

def extract_lines(elem):
    return extract_from_elem(elem, lookfor=LTTextLineHorizontal)

def extract_textboxes(elem):
    return extract_from_elem(elem, lookfor=LTTextBox)

def get_avg_text_height(chars):
    """Returns the average height of LTChar elements contained in `text_container`.
    """
    count = len(chars)
    totheight = sum(c.height for c in chars)
    return totheight / count

def get_text(layout_elements):
    if isinstance(layout_elements, LTItem):
        return layout_elements.get_text()
    else:
        return ' '.join(elem.get_text() for elem in layout_elements)

RE_MULTIPLE_SPACES = re.compile(r' {2,}')
RE_NEWLINE_AND_SPACE = re.compile(r' \n |\n | \n')
def fix_text(text):
    # This search/replace function is based on heuristic discoveries from sample pdf I've received.
    # &dquo; comes from a pdf file with quotes in it. dquo is weird because it looks like an html
    # escape but it isn't. Anyway, just replace it with quotes.
    text = text.replace('&dquo;', '"')
    
    # We also want to normalize spaces, that is: remove double spaces and remove spaces after or
    # before a newline.
    text = RE_MULTIPLE_SPACES.sub(' ', text)
    text = RE_NEWLINE_AND_SPACE.sub('\n', text)
    return text
