# Created By: Virgil Dupras
# Created On: 2011-06-12
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams, LTContainer, LTText, LTChar
from pdfminer.converter import PDFPageAggregator

class ElementState:
    Normal = 'normal'
    Title = 'title'
    Ignored = 'ignored'

class TextElement:
    def __init__(self, id, page, layout_elem):
        self.id = id
        self.page = page
        self.x0 = layout_elem.x0
        self.y0 = layout_elem.y0
        self.x1 = layout_elem.x1
        self.y1 = layout_elem.y1
        self.avgheight = get_avg_text_height(layout_elem)
        self.text = layout_elem.get_text()
        self.state = ElementState.Normal
        self.layout_elem = layout_elem
    
    def __repr__(self):
        return '<TextElement {page} {x0}-{y0}-{x1}-{y1} {state} "{text}">'.format(**self.__dict__)
    

def extract_text_elements(path):
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
    if not doc.is_extractable:
        raise Exception('not extractable')
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    current_id = 0
    result = []
    for pageno, page in enumerate(doc.get_pages()):
        interpreter.process_page(page)
        layout = device.get_result()
        layout_elems = gettext(layout)
        for layout_elem in layout_elems: 
            elem = TextElement(current_id, pageno, layout_elem)
            current_id += 1
            result.append(elem)
    return result

def get_avg_text_height(text_container):
    """Returns the average height of LTChar elements contained in `text_container`.
    """
    def return_chars(elem):
        # To extract char of a container (which can contain sub containers), we simply iterate
        # through elements recursively until it's not possible anymore, then we'll have chars.
        try:
            return sum((return_chars(subelem) for subelem in elem), [])
        except TypeError: # we have A LTChar or a LTAnon
            if isinstance(elem, LTChar):
                return [elem]
            else:
                return []
    
    chars = return_chars(text_container)
    count = len(chars)
    totheight = sum(c.height for c in chars)
    return totheight / count
