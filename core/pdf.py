# Created By: Virgil Dupras
# Created On: 2011-06-12
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams, LTContainer, LTText
from pdfminer.converter import PDFPageAggregator

class ElementState:
    Normal = 'normal'
    Ignored = 'ignored'

class TextElement:
    def __init__(self, page, layout_elem):
        self.page = page
        self.x0 = layout_elem.x0
        self.y0 = layout_elem.y0
        self.x1 = layout_elem.x1
        self.y1 = layout_elem.y1
        self.text = layout_elem.get_text()
        self.state = ElementState.Normal
    
    def __repr__(self):
        return '<TextElement {page} {x0}-{y0}-{x1}-{y1} {state} "{text}">'.format(**self.__dict__)
    

def extract_text_elements(path):
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
    result = []
    for pageno, page in enumerate(doc.get_pages()):
        interpreter.process_page(page)
        layout = device.get_result()
        layout_elems = gettext(layout)
        result += [TextElement(pageno, e) for e in layout_elems]
    return result
