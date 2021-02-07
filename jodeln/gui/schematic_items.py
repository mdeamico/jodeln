from PySide2.QtWidgets import QGraphicsItem
from PySide2.QtCore import QRectF
from typing import Optional

from PySide2.QtGui import QPainter, QPen, QColor
from PySide2.QtWidgets import QStyleOptionGraphicsItem, QWidget


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
            pen = QPen(QColor("green"), 2)
            painter.setPen(pen)
            painter.drawLine(self.ix, self.iy, self.jx, self.jy)
        else:
            painter.drawLine(self.ix, self.iy, self.jx, self.jy)


class NodeItem(QGraphicsItem):
    """GraphicsItem for network nodes.
    
    Displayed as a circle at the node xy coordinate.
    """
    def __init__(self, x, y, parent: Optional[QGraphicsItem] = None) -> None:
        super().__init__(parent=parent)
        self.x = x
        self.y = y
    
    def boundingRect(self) -> QRectF:
        penWidth = 1
        return QRectF((self.x - 2) - penWidth / 2, (self.y - 2) - penWidth / 2,
                      (self.x + 4) + penWidth, (self.y + 4) + penWidth)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget]) -> None:
        painter.drawEllipse(self.x - 2, self.y - 2, 4, 4)