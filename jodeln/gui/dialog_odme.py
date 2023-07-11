from PySide2.QtWidgets import QWidget, QFileDialog
from PySide2.QtGui import QDoubleValidator

from gui.ui_dialog_odme import Ui_Dialog

from typing import Protocol

class Model(Protocol):
    def estimate_od_cmaes(self, weight_total_geh=None, weight_odsse=None, weight_route_ratio=None):
        ...
    def export_od(self, output_folder=None) -> None:
        ...
    def export_od_by_route(self, output_folder=None) -> None:
        ...


class DialogODME(QWidget):
    """Dialog for doing OD Estimation."""
    def __init__(self, model: Model):

        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.model = model

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

        self.ui.pbExportFolder.clicked.connect(self.on_pbExportFolder_click)

    def reject(self) -> None:
        """User clicks 'Close'."""
        self.close()

    def estimate_od(self) -> None:
        """Run OD matrix estimation."""
        self.model.estimate_od_cmaes(
                weight_total_geh=float(self.ui.leWeightGEH.text()),
                weight_odsse=float(self.ui.leWeightODSSE.text()),
                weight_route_ratio=float(self.ui.leWeightRouteRatio.text())
            )
        
        self.model.export_od(self.ui.leExportFolder.text())
        self.model.export_od_by_route(self.ui.leExportFolder.text())

    def on_pbExportFolder_click(self) -> None:
        """Open a standard file dialog for selecting the export folder."""
        export_folder = QFileDialog.getExistingDirectory(
            self, "Select Export Folder", 
            "",
            options=QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)

        self.ui.leExportFolder.setText(export_folder)
