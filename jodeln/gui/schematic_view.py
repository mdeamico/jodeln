from PySide2.QtWidgets import QGraphicsView
import PySide2.QtCore

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import PySide2.QtGui


class SchematicView(QGraphicsView):
    def __init__(self, parent = None):
        super().__init__()
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
    
    def wheelEvent(self, event: 'PySide2.QtGui.QWheelEvent') -> None:

        # Zoom to point under mouse cursor.
        # https://stackoverflow.com/questions/58965209/zoom-on-mouse-position-qgraphicsview
        # https://stackoverflow.com/questions/19113532/qgraphicsview-zooming-in-and-out-under-mouse-position-using-mouse-wheel

        previous_anchor = self.transformationAnchor()
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        
        zoom_factor = 1.1
        if event.angleDelta().y() <= 0:
            zoom_factor = 0.9
        
        self.scale(zoom_factor, zoom_factor)
        self.setTransformationAnchor(previous_anchor)

        # Do not call the super().wheelEvent(event) method in the return statement.
        # Doing so interferes with the zoom to cursor behavior logic implemented above.
    
        return

