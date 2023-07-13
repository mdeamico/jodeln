from PySide2.QtWidgets import QWidget, QFileDialog
from PySide2.QtGui import QDoubleValidator

from gui.ui_dialog_odme_leastsq import Ui_DialogODME_LeastSq

from typing import Protocol

class Model(Protocol):
    def estimate_od_leastsq(self, seed_od_weight: float):
        ...



class DialogODME_LeastSq(QWidget):
    """Dialog for doing OD Estimation."""
    def __init__(self, model: Model, cb_post_odme):

        super().__init__()
        self.ui = Ui_DialogODME_LeastSq()
        self.ui.setupUi(self)

        self.model = model
        self.post_odme_fn = cb_post_odme

        double_validator = QDoubleValidator(bottom=0)
        double_validator.setNotation(QDoubleValidator.StandardNotation)
        self.ui.leSeedODWeight.setValidator(double_validator)

        self.ui.pbRunOdme.clicked.connect(self.estimate_od)
        self.ui.pbClose.clicked.connect(self.close)

    def estimate_od(self) -> None:
        """Run OD matrix estimation."""
        self.ui.txtDiagnostics.setText("")
        diagnostics = self.model.estimate_od_leastsq(float(self.ui.leSeedODWeight.text()))
        self.ui.txtDiagnostics.setText(diagnostics.__repr__())
        self.post_odme_fn()

    def close(self) -> bool:
        return super().close()        
