from PySide2.QtWidgets import QGraphicsItem
from PySide2.QtCore import QRectF, QPointF
from typing import Optional

from PySide2.QtGui import QPainter, QPen, QColor, QPainterPath, QFont, QPolygonF
from PySide2.QtWidgets import QStyleOptionGraphicsItem, QWidget
from PySide2.QtCore import Qt


class LinkItem(QGraphicsItem):
    """GraphicsItem for network links.
    
    Displayed as a line between the starting node i and ending node j of the link.
    """
    def __init__(self, pts, parent: Optional[QGraphicsItem] = None) -> None:
        super().__init__(parent=parent)
        self.pts = pts
        self.polyline = QPolygonF([QPointF(x, y) for x, y in pts])

        self.topleft_x = min([x for x, _ in pts])
        self.topleft_y = min([y for _, y in pts])
        self.width = abs(max([x for x, _ in pts]) - self.topleft_x)
        self.height = abs(max([y for _, y in pts]) - self.topleft_y)

        self.is_on_selected_path = False
    
    def boundingRect(self) -> QRectF:
        return QRectF(self.topleft_x, self.topleft_y, self.width, self.height)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget]) -> None:
        if self.is_on_selected_path:
            pen = QPen(QColor("green"), 5)
        else:
            pen = QPen(Qt.gray, 2)

        pen.setCosmetic(True)
        painter.setPen(pen)
        # painter.drawLine(self.ix, self.iy, self.jx, self.jy)
        painter.drawPolyline(self.polyline)
        


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

        # Combine ideas from these code samples to draw items at a fixed size:
        # https://stackoverflow.com/questions/1222914/qgraphicsview-and-qgraphicsitem-don%C2%B4t-scale-item-when-scaling-the-view-rect
        # https://www.qtcentre.org/threads/28691-Scale-independent-QGraphicsItem

        object_rect = self.boundingRect()
        mapped_rect = painter.transform().mapRect(object_rect)
        
        width_ratio = object_rect.width() / mapped_rect.width()

        scale_factor = max(1, width_ratio)

        painter.setPen(pen)
        painter.setBrush(Qt.gray)

        scaled_diameter = self.diameter * scale_factor

        painter.drawEllipse((self.x - scaled_diameter / 2), 
                            (self.y - scaled_diameter / 2), 
                            scaled_diameter,
                            scaled_diameter)

        # Draw text for the node name
        label_path = QPainterPath()
        label_font = QFont("Calibri", 10 * scale_factor)
        label_path.addText(self.x, -self.y - self.diameter / 2, label_font, self.name)
        painter.scale(1.0, -1.0)
        
        painter.setBrush(Qt.blue)
        painter.setPen(Qt.NoPen)
        painter.drawPath(label_path)
        
