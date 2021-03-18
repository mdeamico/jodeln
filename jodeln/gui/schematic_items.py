from PySide2.QtWidgets import QGraphicsItem
from PySide2.QtCore import QRectF
from typing import Optional

from PySide2.QtGui import QPainter, QPen, QColor, QPainterPath, QFont
from PySide2.QtWidgets import QStyleOptionGraphicsItem, QWidget
from PySide2.QtCore import Qt


class LinkItem(QGraphicsItem):
    """GraphicsItem for network links.
    
    Displayed as a line between the starting node i and ending node j of the link.
    """
    def __init__(self, ix, iy, jx, jy, parent: Optional[QGraphicsItem] = None) -> None:
        super().__init__(parent=parent)
        self.ix = ix
        self.iy = iy
        self.jx = jx
        self.jy = jy

        self.topleft_x = min(ix, iy)
        self.topleft_y = min(iy, jy)
        self.width = abs(ix - jx)
        self.height = abs(iy - jy)

        self.is_on_selected_path = False
    
    def boundingRect(self) -> QRectF:
        return QRectF(self.topleft_x, self.topleft_y, self.width, self.height)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget]) -> None:
        if self.is_on_selected_path:
            pen = QPen(QColor("green"), 5)
            pen.setCosmetic(True)
            painter.setPen(pen)
            painter.drawLine(self.ix, self.iy, self.jx, self.jy)
        else:
            pen = QPen(Qt.gray)
            pen.setWidth(2)
            pen.setCosmetic(True)
            painter.setPen(pen)
            painter.drawLine(self.ix, self.iy, self.jx, self.jy)


class NodeItem(QGraphicsItem):
    """GraphicsItem for network nodes.
    
    Displayed as a circle at the node xy coordinate.
    """
    def __init__(self, x, y, name, parent: Optional[QGraphicsItem] = None) -> None:
        super().__init__(parent=parent)
        self.x = x
        self.y = y
        self.name = name
        self.diameter = 5
        self.pen_width = 1
    
    def boundingRect(self) -> QRectF:
        return QRectF(self.x - self.diameter / 2 - self.pen_width, 
                      self.y - self.diameter / 2 - self.pen_width,
                      self.diameter + self.pen_width * 2,
                      self.diameter + self.pen_width * 2)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget]) -> None:

        # Draw a circle for the node
        pen = QPen(Qt.gray)
        pen.setWidth(2)
        pen.setCosmetic(True)

        painter.setPen(pen)
        painter.setBrush(Qt.gray)
        painter.drawEllipse(self.x - self.diameter / 2, 
                            self.y - self.diameter / 2, 
                            self.diameter,
                            self.diameter)
        
        # Draw text for the node name
        label_path = QPainterPath()
        label_font = QFont("Calibri", 5)
        label_path.addText(self.x, self.y - self.diameter / 2, label_font, self.name)

        painter.setBrush(Qt.blue)
        painter.setPen(Qt.NoPen)
        painter.drawPath(label_path)
