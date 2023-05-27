from PySide2.QtWidgets import QWidget, QFileDialog
from PySide2.QtGui import QDoubleValidator

from gui.ui_dialog_odme import Ui_Dialog

from typing import Callable
from dataclasses import dataclass

@dataclass(slots=True)
class CallbackOdmeParameters():
    """Group parameters needed for the ODME Callback Function."""
    weight_GEH: float
    weight_odsse: float
    weight_route_ratio: float
    export_path: str

class DialogODME(QWidget):
    """Dialog for doing OD Estimation."""
    def __init__(self, cb_odme: Callable[[CallbackOdmeParameters], None]):

        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.cb_odme = cb_odme

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

        self.cb_odme(
            CallbackOdmeParameters(
                weight_GEH=float(self.ui.leWeightGEH.text()),
                weight_odsse=float(self.ui.leWeightODSSE.text()),
                weight_route_ratio=float(self.ui.leWeightRouteRatio.text()),
                export_path=self.ui.leExportFolder.text())
            )

    def on_pbExportFolder_click(self) -> None:
        """Open a standard file dialog for selecting the export folder."""
        export_folder = QFileDialog.getExistingDirectory(
            self, "Select Export Folder", 
            "",
            options=QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)

        self.ui.leExportFolder.setText(export_folder)
