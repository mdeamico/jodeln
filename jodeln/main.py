import sys
from PySide2.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, 
    QAbstractItemView, QDialogButtonBox)
from PySide2.QtGui import QDoubleValidator, QPainter

from gui.ui_mainwindow import Ui_MainWindow

from gui import schematic_scene, od_tablemodel
from gui.dialog_open import DialogOpen

from model import Model


class MainWindow(QMainWindow):
    """Main window presented to the user when the program first starts."""
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Dialog Open
        self.dialog_open = DialogOpen()
        self.dialog_open.ui.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.load)

        # Connect MainWindow view/controller to model
        self.model = Model()

        # Connect push buttons to slot functions
        self.ui.pbShowDialogOpen.clicked.connect(self.show_dialog_open)
        self.ui.pbExportFolder.clicked.connect(self.on_pbExportFolder_click)
        self.ui.pbExportTurns.clicked.connect(self.export_turns)
        self.ui.pbExportRoutes.clicked.connect(self.export_routes)
        self.ui.pbExportLinksAndTurnsByOD.clicked.connect(self.export_links_and_turns_by_od)
        self.ui.pbEstimateOD.clicked.connect(self.estimate_od)

        # Set numeric validators on objective function weight line inputs.
        double_validator = QDoubleValidator(bottom=0)
        double_validator.setNotation(QDoubleValidator.StandardNotation)

        self.ui.leWeightGEH.setValidator(double_validator)
        self.ui.leWeightODSSE.setValidator(double_validator)
        self.ui.leWeightRouteRatio.setValidator(double_validator)

        # set default weights
        self.ui.leWeightGEH.setText("1")
        self.ui.leWeightODSSE.setText("0")
        self.ui.leWeightRouteRatio.setText("1")

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

            routes = self.model.get_route_list()
            self.od_table_model = od_tablemodel.ODTableModel(routes)
            self.ui.tblOD.setModel(self.od_table_model)
            self.ui.tblOD.selectionModel().selectionChanged.connect(self.on_od_table_selection)

            self.schematic_scene.load_routes(routes)

    def on_pbExportFolder_click(self) -> None:
        """Open a standard file dialog for selecting the export folder."""
        export_folder = QFileDialog.getExistingDirectory(
            self, "Select Export Folder", 
            "",
            options=QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)

        self.ui.leExportFolder.setText(export_folder)

    def export_turns(self) -> None:
        """Export turns to csv."""
        self.model.export_turns(self.ui.leExportFolder.text())

    def export_routes(self) -> None:
        """Export nodes on each route."""
        self.model.export_route_list(self.ui.leExportFolder.text())

    def export_links_and_turns_by_od(self) -> None:
        """Export links and turns along each OD pair."""
        self.model.export_node_sequence(self.ui.leExportFolder.text())

    def estimate_od(self) -> None:
        """Run OD matrix estimation."""
        
        self.model.estimate_od(
            weight_total_geh=float(self.ui.leWeightGEH.text()),
            weight_odsse=float(self.ui.leWeightODSSE.text()),
            weight_route_ratio=float(self.ui.leWeightRouteRatio.text()))
        
        self.model.export_od(self.ui.leExportFolder.text())
        self.model.export_od_by_route(self.ui.leExportFolder.text())

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
