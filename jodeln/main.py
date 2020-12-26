import sys
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import QFile
from PySide2.QtGui import QDoubleValidator
from PySide2 import QtUiTools
from gui.ui_mainwindow import Ui_MainWindow

from gui import schematic_scene
from model import Model

class MainWindow(QMainWindow):
    """Main window presented to the user when the program first starts."""
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect MainWindow view/controller to model
        self.model = Model()

        # Connect push buttons to slot functions
        self.ui.pbLoad.clicked.connect(self.load)
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

        
    def load(self):
        """Load nodes, links, etc from user inputs."""
        load_successful = self.model.load(node_file=self.ui.leNodes.text(),
                                          links_file=self.ui.leLinks.text(),
                                          od_seed_file=self.ui.leSeedOD.text(),
                                          turns_file=self.ui.leTurns.text(),
                                          od_routes_file=self.ui.leRoutes.text())
        if load_successful:
            self.draw_network()

    def export_turns(self):
        """Export turns to csv."""
        self.model.export_turns(self.ui.leExportFolder.text())

    def export_routes(self):
        """Export nodes on each route."""
        self.model.export_route_list(self.ui.leExportFolder.text())

    def export_links_and_turns_by_od(self):
        """Export links and turns along each OD pair."""
        self.model.export_node_sequence(self.ui.leExportFolder.text())

    def estimate_od(self):
        """Run OD matrix estimation."""
        
        self.model.estimate_od(
            weight_total_geh=float(self.ui.leWeightGEH.text()),
            weight_odsse=float(self.ui.leWeightODSSE.text()),
            weight_route_ratio=float(self.ui.leWeightRouteRatio.text()))
        
        self.model.export_od(self.ui.leExportFolder.text())
        self.model.export_od_by_route(self.ui.leExportFolder.text())

    def draw_network(self):
        print("drawing nodes")
        nodes = self.model.get_node_xy()
        for _, (x, y) in nodes.items():
            self.schematic_scene.addEllipse(x - 2, y - 2, 4, 4)
        
        links = self.model.get_links()
        for (i, j) in links:
            self.schematic_scene.addLine(nodes[i][0],
                                         nodes[i][1],
                                         nodes[j][0],
                                         nodes[j][1])

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
