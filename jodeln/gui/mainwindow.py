from PySide2.QtWidgets import (
    QMainWindow, 
    QAbstractItemView)

from PySide2.QtGui import QPainter
from PySide2.QtCore import Qt

from gui.ui_mainwindow import Ui_MainWindow

from gui import schematic_scene, od_tablemodel
from gui.dialog_open import DialogOpen
from gui.dialog_export import DialogExport
from gui.dialog_od_view import DialogODView

from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from ..network.netnode import NetNode
    from ..network.netlink import NetLinkData
    from ..model import RouteInfo

class Model(Protocol):
    def get_nodes(self) -> list['NetNode']:
        ...
    def get_links(self) -> list['NetLinkData']:
        ...
    def get_routes(self) -> list['RouteInfo']:
        ...
    def has_od(self) -> bool:
        ...

class MainWindow(QMainWindow):
    """Main window presented to the user when the program first starts."""
    def __init__(self, model: Model):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect MainWindow view/controller to model
        self.model = model

        # Save persistent references to dialogs
        self.dialog_open = DialogOpen(self.model, cb_post_load=self.show_network)
        self.dialog_export = DialogExport(self.model)
        self.dialog_od_view = DialogODView(self.model)

        # Connect push buttons to slot functions
        self.ui.pbShowDialogOpen.clicked.connect(self.show_dialog_open)
        self.ui.pbShowExportDialog.clicked.connect(self.show_dialog_export)
        self.ui.pbODView.clicked.connect(self.show_dialog_od_view)

        # Disable buttons that should only be used after loading a network
        self.ui.pbShowExportDialog.setEnabled(False)
        self.ui.pbODView.setEnabled(False)

        # Setup graphics view
        self.schematic_scene = schematic_scene.SchematicScene()
        self.ui.gvSchematic.setScene(self.schematic_scene)
        self.ui.gvSchematic.setRenderHints(QPainter.Antialiasing)

        # Flip y coordinates to make y coordinates increasing from bottom to top.
        self.ui.gvSchematic.scale(1, -1)
        
        # Set table behaviors
        self.ui.tblOD.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tblOD.setSelectionMode(QAbstractItemView.SingleSelection)

        self.ui.pbFilterApply.clicked.connect(self.apply_od_table_filter)
        self.ui.pbFilterClear.clicked.connect(self.clear_od_table_filter)

        self.ui.filterToggle.clicked.connect(self.collapse_filter_section)
        self.ui.frame.setVisible(False)
        
        
    def show_dialog_open(self) -> None:
        self.dialog_open.store_data()
        self.dialog_open.show()

    def show_dialog_export(self) -> None:
        self.dialog_export.show()

    def show_dialog_od_view(self) -> None:
        self.dialog_od_view.load_od_data()
        self.dialog_od_view.show()


    def show_network(self) -> None:
        """Shows the nodes, links, etc from the loaded network."""
        self.reset()
        self.schematic_scene.load_network(self.model.get_nodes(), 
                                          self.model.get_links())

        # Set scene rectangle to something larger than the network.
        # This helps with panning & zooming near the edges of the network.
        init_rect = self.schematic_scene.sceneRect()
        self.schematic_scene.setSceneRect(
            init_rect.x() - init_rect.width(),
            init_rect.y() - init_rect.height(),
            init_rect.width() * 3,
            init_rect.height() * 3)

        self.ui.gvSchematic.fitInView(
            init_rect, 
            Qt.KeepAspectRatio)

        routes = self.model.get_routes()
        self.od_table_model = od_tablemodel.ODTableModel(routes)

        self.od_proxy_model = od_tablemodel.ODTableFilterProxyModel(self)
        self.od_proxy_model.setSourceModel(self.od_table_model)

        self.ui.tblOD.setModel(self.od_proxy_model)
        self.ui.tblOD.selectionModel().selectionChanged.connect(self.on_od_table_selection)
        self.ui.tblOD.sortByColumn(1, Qt.SortOrder.AscendingOrder)
        self.ui.tblOD.setSortingEnabled(True)

        self.schematic_scene.load_routes(routes)

        self.ui.pbShowExportDialog.setEnabled(True)
        
        self.ui.pbODView.setEnabled(self.model.has_od())


    def reset(self):
        """Reset schematic scene and OD table to an empty state."""
        self.schematic_scene = schematic_scene.SchematicScene()
        self.ui.gvSchematic.setScene(self.schematic_scene)
        self.ui.tblOD.setModel(None)
        

    def on_od_table_selection(self, selected, deselected) -> None:
        """Function called when an item in the OD Table is selected.

        Parameters
        ----------
        selected : QItemSelection
            Currently selected item from the selectionModel.
        deselected : QItemSelection
            Items from the selectionModel that were previously selected, but 
            are no longer selected.
        """
        # boolean flag to indicate if the table selection affects schematic_scene
        should_update_scene = False

        if len(deselected.indexes()) > 0:
            deselected_i = self.od_proxy_model.mapToSource(deselected.indexes()[0])
            route = self.od_table_model.get_route_at_index(deselected_i)
            self.schematic_scene.color_route(route, is_selected=False)              
            should_update_scene = True

        if len(selected.indexes()) > 0:
            # Get route for first selected OD pair
            selected_i = self.od_proxy_model.mapToSource(selected.indexes()[0])
            route = self.od_table_model.get_route_at_index(selected_i)
            self.schematic_scene.color_route(route, is_selected=True)
            should_update_scene = True
            
        if should_update_scene:
            self.schematic_scene.update()


    def apply_od_table_filter(self) -> None:
        filter_origin = self.ui.leFilter1.text()
        filter_destination = self.ui.leFilter2.text()
        self.od_proxy_model.apply_filter(filter_origin, filter_destination)
        
    def clear_od_table_filter(self) -> None:
        self.ui.leFilter1.setText("")
        self.ui.leFilter2.setText("")
        self.od_proxy_model.setFilterRegExp("")

    def collapse_filter_section(self):
        self.ui.frame.setVisible(not self.ui.frame.isVisible())
        self.ui.filterToggle.setArrowType(
            Qt.ArrowType.DownArrow if self.ui.frame.isVisible() 
            else Qt.ArrowType.RightArrow)
