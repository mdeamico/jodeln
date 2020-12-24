from PySide2.QtWidgets import QGraphicsScene

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import PySide2.QtWidgets


class SchematicScene(QGraphicsScene):
    def __init__(self):
        super(SchematicScene, self).__init__()

    def mousePressEvent(self, event: 'PySide2.QtWidgets.QGraphicsSceneMouseEvent') -> None:
        return super().mousePressEvent(event)
