# Created By: Virgil Dupras
# Created On: 2011-06-12
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

import re

from .const import ElementState

RE_STARTING_NUMBER = re.compile(r'^(\d+)')

def link_footnotes(elements):
    """Adjust the text of footnotes and their linked text to add HTML anchors.
    """
    # The way we do this is that we first identify what number the footnote starts with (if it's not
    # a number, ignore it, we're not gonna link it. maybe later). Then, we look in all elemts
    # preceeding it for the first one (which is closest to the footnote) with that number in it.
    # For now, that's a bit basic because there are certainly cases where incorrect linking will
    # be made, but let's not get too complex too fast...
    # Also, footnotes get renumbered because some footnotes reset themselves suring an article.
    # Because we push all footnotes at the end, we don't want to end up with duplicate numbers.
    footnotes = [e for e in elements if e.state == ElementState.Footnote]
    for footnumber, footnote in enumerate(footnotes, start=1):
        m = RE_STARTING_NUMBER.match(footnote.text)
        if not m:
            # we can't link that, but we still want to prepend the footnote with footnumber
            footnote.modified_text = '[{}] {}'.format(footnumber, footnote.text)
            continue
        [lookfor] = m.groups()
        re_lookfor = re.compile(r'(\D){}(\D|$)'.format(lookfor))
        index = elements.index(footnote)
        # we reverse because we want the element closest to the footnote. Also, we remove footnotes
        # because we don't want to mistakenly mink footnotes to other footnotes.
        the_rest = [e for e in reversed(elements[:index]) if e.state != ElementState.Footnote]
        for e in the_rest:
            m = re_lookfor.search(e.text)
            if m is None:
                continue
            [prevchar, nextchar] = m.groups()
            link = '<a name="linkback{0}"></a><a href="#footnote{0}">[{0}]</a>'.format(footnumber)
            e.modified_text = re_lookfor.sub(prevchar+link+nextchar, e.text, count=1)
            link = '<a name="footnote{0}"></a><a href="#linkback{0}">[{0}]</a>'.format(footnumber)
            footnote.modified_text = footnote.text.replace(lookfor, link, 1)
            break
        else:
            # we don't have a link, but we still want to put the footnumber in there
            footnote.modified_text = footnote.text.replace(lookfor, '[{}]'.format(footnumber), 1)

def wrap_html(body, encoding='utf-8'):
    # The 'encoding' argument is only needed for html metadata, generate_html() returns a string,
    # not encoded bytes.
    header = "<head><meta http-equiv=\"Content-Type\" content=\"text/html; charset={}\"></head>".format(encoding)
    return "<html>{}<body>\n{}\n</body></html>".format(header, body)

def generate_markdown(elements):
    def keyfunc(e):
        footnoteorder = 0 if e.state != ElementState.Footnote else 1
        return (footnoteorder, e.page, e.order)
    
    elements = [e for e in elements if e.state != ElementState.Ignored]
    link_footnotes(elements)
    elements.sort(key=keyfunc)
    paragraphs = []
    for e in elements:
        s = e.modified_text if e.modified_text else e.text
        if e.state == ElementState.Title:
            # Titles have to be on a single line
            title_marker = '#' * e.title_level
            s = s.replace('\n', ' ').strip()
            s = '{} {}'.format(title_marker, s)
        elif e.state == ElementState.ToFix:
            s = '*FIXME* {}'.format(s)
        s = s.strip()
        paragraphs.append(s)
    s = '\n\n'.join(paragraphs)
    return s