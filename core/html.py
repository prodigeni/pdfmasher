# Created By: Virgil Dupras
# Created On: 2011-06-12
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from .pdf import ElementState

def generate_html(elements):
    elements = [e for e in elements if e.state != ElementState.Ignored]
    paragraphs = []
    for e in elements:
        s = "<p>{}</p>".format(e.text)
        paragraphs.append(s)
    s = '\n'.join(paragraphs)
    return "<html>\n{}\n</html>".format(s)