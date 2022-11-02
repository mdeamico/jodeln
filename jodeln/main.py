import sys
from PySide2.QtWidgets import (
    QApplication, QMainWindow, 
    QAbstractItemView, QDialogButtonBox)
from PySide2.QtGui import QPainter
from PySide2.QtCore import Qt

from gui.ui_mainwindow import Ui_MainWindow

from gui import schematic_scene, od_tablemodel
from gui.dialog_open import DialogOpen
from gui.dialog_export import DialogExport
from gui.dialog_odme import DialogODME, CallbackOdmeParameters


from model import Model


class MainWindow(QMainWindow):
    """Main window presented to the user when the program first starts."""
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect MainWindow view/controller to model
        self.model = Model()

        # Dialog Open
        self.dialog_open = DialogOpen()
        self.dialog_open.ui.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.load)

        # Dialog Export
        self.dialog_export = DialogExport(
            cb_export_links_and_turns_by_od=self.model.export_node_sequence,
            cb_export_routes=self.model.export_route_list,
            cb_export_turns=self.model.export_turns
        )

        # Dialog ODME
        self.dialog_odme = DialogODME(cb_odme=self.estimate_od)

        # Connect push buttons to slot functions
        self.ui.pbShowDialogOpen.clicked.connect(self.show_dialog_open)
        self.ui.pbShowExportDialog.clicked.connect(self.show_dialog_export)
        self.ui.pbShowODEstimation.clicked.connect(self.show_dialog_odme)

        # Disable buttons that should only be used after loading a network
        self.ui.pbShowExportDialog.setEnabled(False)
        self.ui.pbShowODEstimation.setEnabled(False)

        # Setup graphics view
        self.schematic_scene = schematic_scene.SchematicScene()
        self.ui.gvSchematic.setScene(self.schematic_scene)
        self.ui.gvSchematic.setRenderHints(QPainter.Antialiasing)
        
        # Set table behaviors
        self.ui.tblOD.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tblOD.setSelectionMode(QAbstractItemView.SingleSelection)
        
        
    def show_dialog_open(self) -> None:
        self.dialog_open.store_data()
        self.dialog_open.show()

    def show_dialog_export(self) -> None:
        self.dialog_export.show()

    def show_dialog_odme(self) -> None:
        self.dialog_odme.show()


    def load(self) -> None:
        """Load nodes, links, etc from user inputs."""
        file_paths = self.dialog_open.get_data()
        
        load_successful = self.model.load(node_file=file_paths.nodes,
                                          links_file=file_paths.links,
                                          od_seed_file=file_paths.seed_od,
                                          turns_file=file_paths.turns,
                                          od_routes_file=file_paths.routes)
        if load_successful:
            self.schematic_scene.load_network(self.model.get_node_xy(), 
                                              self.model.get_link_end_ids())

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

            # Flip y coordinates to make y coordinates increasing from bottom to top.
            self.ui.gvSchematic.scale(1, -1)

            routes = self.model.get_route_list()
            self.od_table_model = od_tablemodel.ODTableModel(routes)
            self.ui.tblOD.setModel(self.od_table_model)
            self.ui.tblOD.selectionModel().selectionChanged.connect(self.on_od_table_selection)

            self.schematic_scene.load_routes(routes)

            self.ui.pbShowExportDialog.setEnabled(True)
            self.ui.pbShowODEstimation.setEnabled(True)

    def estimate_od(self, parms: CallbackOdmeParameters) -> None:
        """Run OD matrix estimation."""
        self.model.estimate_od(
            weight_total_geh=parms.weight_GEH,
            weight_odsse=parms.weight_odsse,
            weight_route_ratio=parms.weight_route_ratio)
        
        self.model.export_od(parms.export_path)
        self.model.export_od_by_route(parms.export_path)

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
            route = self.od_table_model.get_route_at_index(deselected.indexes()[0])
            self.schematic_scene.color_route(route, is_selected=False)              
            should_update_scene = True

        if len(selected.indexes()) > 0:
            # Get route for first selected OD pair
            route = self.od_table_model.get_route_at_index(selected.indexes()[0])
            self.schematic_scene.color_route(route, is_selected=True)
            should_update_scene = True
            
        if should_update_scene:
            self.schematic_scene.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
