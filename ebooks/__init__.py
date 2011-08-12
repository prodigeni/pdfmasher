# Copyright 2008, Kovid Goyal <kovid at kovidgoyal.net>
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license
from __future__ import with_statement

'''
Code for the conversion of ebook formats and the reading of metadata
from various formats.
'''

import traceback, os, re
from cStringIO import StringIO
from .utils import CurrentDir

class ConversionError(Exception):

    def __init__(self, msg, only_msg=False):
        Exception.__init__(self, msg)
        self.only_msg = only_msg

class UnknownFormatError(Exception):
    pass

class DRMError(ValueError):
    pass

class ParserError(ValueError):
    pass

BOOK_EXTENSIONS = ['lrf', 'rar', 'zip', 'rtf', 'lit', 'txt', 'txtz', 'text', 'htm', 'xhtm',
                   'html', 'htmlz', 'xhtml', 'pdf', 'pdb', 'pdr', 'prc', 'mobi', 'azw', 'doc',
                   'epub', 'fb2', 'djvu', 'lrx', 'cbr', 'cbz', 'cbc', 'oebzip',
                   'rb', 'imp', 'odt', 'chm', 'tpz', 'azw1', 'pml', 'pmlz', 'mbp', 'tan', 'snb']

class HTMLRenderer(object):

    def __init__(self, page, loop):
        self.page, self.loop = page, loop
        self.data = ''
        self.exception = self.tb = None

    def __call__(self, ok):
        from PyQt4.Qt import QImage, QPainter, QByteArray, QBuffer
        try:
            if not ok:
                raise RuntimeError('Rendering of HTML failed.')
            de = self.page.mainFrame().documentElement()
            pe = de.findFirst('parsererror')
            if not pe.isNull():
                raise ParserError(pe.toPlainText())
            image = QImage(self.page.viewportSize(), QImage.Format_ARGB32)
            image.setDotsPerMeterX(96*(100/2.54))
            image.setDotsPerMeterY(96*(100/2.54))
            painter = QPainter(image)
            self.page.mainFrame().render(painter)
            painter.end()
            ba = QByteArray()
            buf = QBuffer(ba)
            buf.open(QBuffer.WriteOnly)
            image.save(buf, 'JPEG')
            self.data = str(ba.data())
        except Exception as e:
            self.exception = e
            self.traceback = traceback.format_exc()
        finally:
            self.loop.exit(0)


def render_html(path_to_html, width=590, height=750, as_xhtml=True):
    from PyQt4.QtWebKit import QWebPage
    from PyQt4.Qt import QEventLoop, QPalette, Qt, QUrl, QSize
    from calibre.gui2 import is_ok_to_use_qt
    if not is_ok_to_use_qt(): return None
    path_to_html = os.path.abspath(path_to_html)
    with CurrentDir(os.path.dirname(path_to_html)):
        page = QWebPage()
        pal = page.palette()
        pal.setBrush(QPalette.Background, Qt.white)
        page.setPalette(pal)
        page.setViewportSize(QSize(width, height))
        page.mainFrame().setScrollBarPolicy(Qt.Vertical, Qt.ScrollBarAlwaysOff)
        page.mainFrame().setScrollBarPolicy(Qt.Horizontal, Qt.ScrollBarAlwaysOff)
        loop = QEventLoop()
        renderer = HTMLRenderer(page, loop)
        page.loadFinished.connect(renderer, type=Qt.QueuedConnection)
        if as_xhtml:
            page.mainFrame().setContent(open(path_to_html, 'rb').read(),
                    'application/xhtml+xml', QUrl.fromLocalFile(path_to_html))
        else:
            page.mainFrame().load(QUrl.fromLocalFile(path_to_html))
        loop.exec_()
    renderer.loop = renderer.page = None
    page.loadFinished.disconnect()
    del page
    del loop
    if isinstance(renderer.exception, ParserError) and as_xhtml:
        return render_html(path_to_html, width=width, height=height,
                as_xhtml=False)
    return renderer

def check_ebook_format(stream, current_guess):
    ans = current_guess
    if current_guess.lower() in ('prc', 'mobi', 'azw', 'azw1'):
        stream.seek(0)
        if stream.read(3) == 'TPZ':
            ans = 'tpz'
        stream.seek(0)
    return ans

def normalize(x):
    if isinstance(x, unicode):
        import unicodedata
        x = unicodedata.normalize('NFKC', x)
    return x

def calibre_cover(title, author_string, series_string=None,
        output_format='jpg', title_size=46, author_size=36, logo_path=None):
    title = normalize(title)
    author_string = normalize(author_string)
    series_string = normalize(series_string)
    from calibre.utils.magick.draw import create_cover_page, TextLine
    lines = [TextLine(title, title_size), TextLine(author_string, author_size)]
    if series_string:
        lines.append(TextLine(series_string, author_size))
    if logo_path is None:
        logo_path = I('library.png')
    return create_cover_page(lines, logo_path, output_format='jpg')

UNIT_RE = re.compile(r'^(-*[0-9]*[.]?[0-9]*)\s*(%|em|ex|en|px|mm|cm|in|pt|pc)$')

def unit_convert(value, base, font, dpi):
    ' Return value in pts'
    if isinstance(value, (int, long, float)):
        return value
    try:
        return float(value) * 72.0 / dpi
    except:
        pass
    result = value
    m = UNIT_RE.match(value)
    if m is not None and m.group(1):
        value = float(m.group(1))
        unit = m.group(2)
        if unit == '%':
            result = (value / 100.0) * base
        elif unit == 'px':
            result = value * 72.0 / dpi
        elif unit == 'in':
            result = value * 72.0
        elif unit == 'pt':
            result = value
        elif unit == 'em':
            result = value * font
        elif unit in ('ex', 'en'):
            # This is a hack for ex since we have no way to know
            # the x-height of the font
            font = font
            result = value * font * 0.5
        elif unit == 'pc':
            result = value * 12.0
        elif unit == 'mm':
            result = value * 0.04
        elif unit == 'cm':
            result = value * 0.40
    return result
