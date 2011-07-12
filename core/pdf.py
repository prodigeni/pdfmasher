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
from pdfminer.layout import LAParams, LTItem, LTContainer, LTText, LTChar, LTTextLineHorizontal
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
    Ignored = 'ignored'

class TextElement:
    def __init__(self, x, y, fontsize, text):
        # The X and the Y of a text element should always be its top left corner
        self.id = None # set later
        self.page = None # set later
        self.x = x
        self.y = y
        self.fontsize = fontsize
        self.text = text
        self.state = ElementState.Normal
    
    def __repr__(self):
        return '<TextElement {page} {x}-{y} {state} "{text}">'.format(**self.__dict__)
    

def extract_text_elements_from_pdf(path, j=nulljob):
    """Opens a PDF and extract every element that is text based (LTText).
    """
    def gettext(obj):
        if isinstance(obj, LTText):
            return [obj]
        elif isinstance(obj, LTContainer):
            return sum((gettext(sub) for sub in obj), [])
        else:
            return []
    
    fp = open(path, 'rb')
    doc = PDFDocument(caching=True)
    parser = PDFParser(fp)
    parser.set_document(doc)
    doc.set_parser(parser)
    doc.initialize()
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    result = []
    enumerated_pages = list(enumerate(doc.get_pages()))
    progress_msg = "Reading page %i of %i"
    for pageno, page in j.iter_with_progress(enumerated_pages, progress_msg):
        interpreter.process_page(page)
        layout = device.get_result()
        layout_elems = gettext(layout)
        for layout_elem in layout_elems: 
            elements = extract_text_elements_from_layout(layout_elem)
            for elem in elements:
                elem.page = pageno
                result.append(elem)
    for i, elem in enumerate(result):
        elem.id = i
    return result

def create_element(layout_elements):
    # layout elem can either be an LTItem or a list of elems. We have to extract X and Y pos from it.
    # If we have a list, we use the first item of the list, which should be at the top left corner
    # of the bunch, normally
    if isinstance(layout_elements, LTItem):
        x = layout_elements.x0
        y = layout_elements.y1 # top left corner in pdfminer is x0/y1
    else:
        x = layout_elements[0].x0
        y = layout_elements[0].y1
    chars = extract_chars(layout_elements)
    fontsize = get_avg_text_height(chars)
    text = fix_text(get_text(layout_elements))
    return TextElement(x, y, fontsize, text)

def extract_text_elements_from_layout(layout_element):
    """Extract text elements from `layout_element`.
    
    Most of the time, only one text element per layout element is extracted, but it can happen
    that a layout element contains more than one paragraph and thus needs to yield more than one
    text element.
    """
    # points to the right of the min x where we consider ourselves 'indented'.
    # NOTE: When looking for indented lines, we need to be careful to check whether there's not
    # something to the left of that line. If there's enough space between the comma of the previous
    # sentence and the first letter of the next, we end up with two horizontal lines next to each
    # other.
    X_TRESHOLD = 5
    # Number of characters in the text element needed for it to be considered a 'real' paragraph(s)
    # If we're under that, it's probably a (sub)title or something along these lines, so we simply
    # create one element from it.
    CHARCOUNT_THRESHOLD = 300
    if len(layout_element.get_text()) < CHARCOUNT_THRESHOLD:
        return [create_element(layout_element)]
    lines = extract_lines(layout_element)
    # It's important to sort lines here as they're not necessarily in the right order. However, we
    # round coordinates in the sort function because in same cases, a very small (like 0.1)
    # difference in y-pos makes text which should, according to x-pos, go before another piece
    # of text go after it instead.
    keyfunc = lambda l: (-round(l.y1), l.x0)
    lines.sort(key=keyfunc)
    minx = min(line.x0 for line in lines)
    result = []
    bunch = []
    for line in lines:
        sameline = False
        if bunch and (abs(line.y1 - bunch[-1].y1) < 1):
            # we're on the same line, don't consider this indented
            sameline = True
        if bunch and (not sameline) and (line.x0 - minx > X_TRESHOLD):
            elem = create_element(bunch)
            result.append(elem)
            bunch = []
        bunch.append(line)
    elem = create_element(bunch)
    result.append(elem)
    return result

def extract_from_elem(elem, lookfor=LTChar):
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
