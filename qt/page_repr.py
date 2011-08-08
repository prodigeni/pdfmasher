# Created By: Virgil Dupras
# Created On: 2011-07-22
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from math import pi, sin, cos, radians

from PyQt4.QtCore import Qt, QRectF, QLineF, QPointF
from PyQt4.QtGui import QWidget, QPainter, QPen, QPolygonF, QColor, QFont

from core.gui.page_repr import PageRepresentation as PageRepresentationModel, PageColor

COLORS = {
    PageColor.PageBg: Qt.white,
    PageColor.PageBorder: Qt.black,
    PageColor.ElemNormal: Qt.black,
    PageColor.ElemTitle: QColor('#ff6400'), # orange
    PageColor.ElemFootnote: Qt.black,
    PageColor.ElemIgnored: Qt.lightGray,
    PageColor.ElemToFix: Qt.red,
    PageColor.ElemSelected: Qt.blue,
    PageColor.ElemOrderArrow: Qt.red,
    PageColor.MouseSelection: Qt.blue,
}

class PageRepresentation(QWidget):
    def __init__(self, app):
        QWidget.__init__(self)
        self.model = PageRepresentationModel(view=self, app=app.model)
    
    def _paintPage(self, painter):
        pagewidth = self.model.page.width
        pageheight = self.model.page.height
        ratio = pageheight / pagewidth
        # somehow, if we don't put the '-1's, the (bottom/right)most pixel line gets cropped.
        width = self.width() - 1
        height = self.height() - 1
        if width * ratio > height:
            # Our constraint is height, adjust according to it
            adjusted_width = height / ratio
            adjusted_height = height
            x = (width - adjusted_width) / 2
            y = 0
        else:
            # Our constraint is width, adjust according to it
            adjusted_width = width
            adjusted_height = width * ratio
            x = 0
            y = (height - adjusted_height) / 2
        r = QRectF(x, y, adjusted_width, adjusted_height)
        painter.fillRect(r, Qt.white)
        painter.drawRect(r)
    
    #--- Qt Events
    def paintEvent(self, event):
        QWidget.paintEvent(self, event)
        self.current_painter = QPainter(self)
        self.model.draw(self.width(), self.height())
        del self.current_painter
    
    def mousePressEvent(self, event):
        self.setFocus(Qt.MouseFocusReason) # we need to do this if we want to track shift release
        self.model.mouse_down(event.x(), event.y())
    
    def mouseMoveEvent(self, event):
        self.model.mouse_move(event.x(), event.y())
    
    def mouseReleaseEvent(self, event):
        self.model.shift_key_held = bool(event.modifiers() & Qt.ShiftModifier)
        self.model.mouse_up()
    
    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Shift:
            self.model.shift_key_held = bool(event.modifiers() & Qt.ShiftModifier)
        elif len(event.text()) == 1:
            self.model.press_key(event.text())
    
    #--- model --> view
    def draw_rectangle(self, rect, bgcolor, pencolor):
        x, y, width, height = rect
        painter = self.current_painter
        painter.save()
        r = QRectF(x, y, width, height)
        if bgcolor is not None:
            painter.fillRect(r, COLORS[bgcolor])
        if pencolor is not None:
            pen = QPen(painter.pen())
            pen.setColor(COLORS[pencolor])
            painter.setPen(pen)
            painter.drawRect(r)
        painter.restore()
    
    def draw_arrow(self, line, width, color):
        (x1, y1), (x2, y2) = line
        # compute points
        line = QLineF(x1, y1, x2, y2)
        # If the line is very small, we make our arrowhead smaller
        arrowsize = min(14, line.length())
        lineangle = radians(line.angle())
        arrowpt1 = line.p2() + QPointF(sin(lineangle - (pi/3)) * arrowsize, cos(lineangle - (pi/3)) * arrowsize)
        arrowpt2 = line.p2() + QPointF(sin(lineangle - pi + (pi/3)) * arrowsize, cos(lineangle - pi + (pi/3)) * arrowsize)
        head = QPolygonF([line.p2(), arrowpt1, arrowpt2])
        # We have to draw the actual line a little short for the tip of the arrowhead not to be too wide
        adjustedLine = QLineF(line)
        adjustedLine.setLength(line.length() - arrowsize/2)
        
        # draw line
        painter = self.current_painter
        color = COLORS[color]
        painter.save()
        pen = QPen(painter.pen())
        pen.setColor(color)
        pen.setWidthF(width)
        painter.setPen(pen)
        painter.drawLine(adjustedLine)
        
        # draw arrowhead
        painter.setPen(Qt.NoPen)
        brush = painter.brush()
        brush.setColor(color)
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)
        painter.drawPolygon(head)
        painter.restore()
    
    def draw_text(self, text, rect):
        rect = QRectF(*rect)
        painter = self.current_painter
        painter.save()
        font = QFont(painter.font())
        font.setPointSize(11)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignHCenter|Qt.AlignVCenter, text)
        painter.restore()
    
    def refresh(self):
        self.update()
    
