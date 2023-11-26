from PySide2.QtWidgets import QGraphicsItem
from PySide2.QtGui import QFont, QPainter, QPixmap, QFontMetrics
from PySide2.QtCore import Qt, QRectF, QPointF


class NodeLabel(QGraphicsItem):
    def __init__(self, parent, text: str) -> None:
        super().__init__(parent)

        self.text = text
        self.lod = 1.0
        self.size_multiplier = 1.0
        self.antialias_scale = 2.0

        self.font = QFont("consolas", 14 * self.antialias_scale)
        qfm = QFontMetrics(self.font)
        self.char_cap_height = qfm.capHeight()
        self.char_width = qfm.averageCharWidth()

        self.text_pixmap = self._setup_text_pixmap()

    def _setup_text_pixmap(self):
        
        width_px = len(self.text) * self.char_width
        height_px = self.char_cap_height

        canvas = QPixmap(width_px, height_px)
        canvas.fill(Qt.transparent)
        painter = QPainter(canvas)

        painter.setFont(self.font)
        painter.setPen(Qt.blue)

        painter.scale(1.0, -1.0)
        painter.drawText(0, 0, self.text)

        return canvas

    def set_size_multiplier(self, value):
        self.size_multiplier = value

    def boundingRect(self):
        return QRectF(0, 
                      0, 
                      len(self.text) * self.char_width, 
                      self.char_cap_height)

    def paint(self, painter, option, widget) -> None:
        self.lod = option.levelOfDetailFromTransform(painter.worldTransform())
                
        scale_mult = (1 / self.antialias_scale) / self.lod * self.size_multiplier
        painter.scale(scale_mult, scale_mult)
        painter.drawPixmap(QPointF(0, 0), self.text_pixmap)  
