# Created By: Virgil Dupras
# Created On: 2011-06-12
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

import re

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams, LTChar, LTTextBoxHorizontal
from pdfminer.converter import PDFPageAggregator

from hscommon.geometry import Rect, Line
from hscommon.util import extract, remove_invalid_xml
from jobprogress.job import nulljob

from .const import ElementState

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
#
#--- detect_vertical
#
# We used to set the 'detect_vertical' flag on in LAParams so that annoying vertical text, sometimes
# present next to photos in newspaper (to credit the photograph) would be automatically ignored.
# This, however, caused problems in some PDFs where the first letter of each line would mistakenly
# be detected as a vertical line. So, we don't use that flag anymore. The user of PdfMasher can
# easily weed these out by sorting by text length and removeing all text elements of 1 character.

class TextElement:
    def __init__(self, rect, fontsize, text):
        # The X and the Y of a text element should always be its top left corner
        self.page = None # set later
        self.order = 0 # set later
        self.rect = rect
        self.x = rect.x
        self.y = rect.y + rect.h # ypos in pdfminer are inverted and we want to top left corner
        self.fontsize = fontsize
        self.text = text
        self.state = ElementState.Normal
        self.title_level = 1 # 1 to 6
        # This is for footnotes-processed text
        self.modified_text = None
    
    def __repr__(self):
        return '<TextElement {page} {x}-{y} {state} "{text}">'.format(**self.__dict__)
    

class Page:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    
def extract_text_elements_from_pdf(path, demo_mode, j=nulljob):
    """Opens a PDF and extract every element that is text based (LTText).
    """
    fp = open(path, 'rb')
    doc = PDFDocument(caching=True)
    parser = PDFParser(fp)
    parser.set_document(doc)
    doc.set_parser(parser)
    doc.initialize()
    rsrcmgr = PDFResourceManager()
    laparams = LAParams(all_texts=True, paragraph_indent=5, heuristic_word_margin=True)
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pages = []
    all_elements = []
    enumerated_pages = list(enumerate(doc.get_pages()))
    if demo_mode:
        enumerated_pages = enumerated_pages[:10]
    progress_msg = "Reading page %i of %i"
    for pageno, page in j.iter_with_progress(enumerated_pages, progress_msg):
        interpreter.process_page(page)
        page_layout = device.get_result()
        pages.append(Page(page_layout.width, page_layout.height))
        textboxes = extract_textboxes(page_layout)
        elements = [create_element(box) for box in textboxes]
        merge_oneletter_elems(elements)
        for i, elem in enumerate(elements):
            elem.page = pageno
            elem.order = i
        all_elements += elements
    return pages, all_elements

def create_element(layout_element):
    rect = Rect(layout_element.x0, layout_element.y0, layout_element.width, layout_element.height)
    chars = extract_chars(layout_element)
    fontsize = get_avg_text_height(chars)
    text = fix_text(layout_element.get_text())
    return TextElement(rect, fontsize, text)

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

def extract_textboxes(elem):
    return extract_from_elem(elem, lookfor=LTTextBoxHorizontal)

def get_avg_text_height(chars):
    """Returns the average height of LTChar elements contained in `text_container`.
    """
    count = len(chars)
    totheight = sum(c.height for c in chars)
    return totheight / count

def merge_oneletter_elems(elements):
    # we go through all one-lettered boxes, we check if it intersects with any other rect. In
    # addition, we also check that the bottom-right corner of the letter is in the top-left part
    # of the paragraph.
    # HOWEVER, We must not forget that Y-positions in pdfminer layout is upside down. The bottom of
    # the page is 0 and the top is the max y-pos.
    oneletter, others = extract(lambda e: len(e.text.strip()) == 1, elements)
    for elem1 in oneletter:
        rect = elem1.rect
        for elem2 in others:
            otherrect = elem2.rect
            if rect.intersects(otherrect):
                corner = rect.corners()[1]
                line = Line(otherrect.center(), corner)
                if line.dx() < 0 and line.dy() > 0:
                    elem2.text = elem1.text.strip() + elem2.text
                    elements.remove(elem1)
                    break

RE_MULTIPLE_SPACES = re.compile(r' {2,}')
RE_NEWLINE_AND_SPACE = re.compile(r' \n |\n | \n')
def fix_text(text):
    # If we don't remove invalid XML characters, we'll get crashes on ebook creation and reloading
    # of masherproj files.
    text = remove_invalid_xml(text)
    
    # This search/replace function is based on heuristic discoveries from sample pdf I've received.
    # &dquo; comes from a pdf file with quotes in it. dquo is weird because it looks like an html
    # escape but it isn't. Anyway, just replace it with quotes.
    text = text.replace('&dquo;', '"')
    
    # We also want to normalize spaces, that is: remove double spaces and remove spaces after or
    # before a newline.
    text = RE_MULTIPLE_SPACES.sub(' ', text)
    text = RE_NEWLINE_AND_SPACE.sub('\n', text)
    return text
