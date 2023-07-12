from copy import deepcopy

from PySide2.QtWidgets import QMainWindow
from PySide2.QtCore import QSize

from gui.ui_dialog_od_view import Ui_ODView
from gui.dialog_odme import DialogODME
from od.od_matrix import ODMatrix

from typing import Protocol


class Model(Protocol):
    def estimate_od_fratar(self):
        ...
    @property
    def od_seed(self) -> ODMatrix:
        ...
    @property
    def od_estimated(self) -> ODMatrix:
        ...
    @property
    def od_diff(self) -> ODMatrix:
        ...


class DialogODView(QMainWindow):
    def __init__(self, model: Model):
        super().__init__()
        self.ui = Ui_ODView()
        self.ui.setupUi(self)

        self.model = model

        self.dialog_odme = DialogODME(model)

        self.ui.tabWidget.currentChanged.connect(self.tab_changed)

        self.ui.actionODME_fratar.triggered.connect(self.odme_fratar_factor)
        self.ui.actionODME_leastsq.triggered.connect(self.odme_leastsq)
        self.ui.actionODME_cmaes.triggered.connect(self.odme_cmaes)
        

    def load_od_data(self):
        self.ui.mv1.load_od_data(self.model.od_seed)
        self.ui.mv2.load_od_data(self.model.od_estimated)
        self.ui.mv3.load_od_data(self.model.od_diff)

        
    def tab_changed(self, index):
        """Hack to force MatrixView widgets to show/hide their scrollbars as needed.
        
        Without this hack, MatrixView widgets will show their scrollbars if the
        widgets are not on the initial tab shown by the dialog loads.
        """
        self.resize(QSize(self.size().width() + 1, self.size().height() + 1))
        self.resize(QSize(self.size().width() - 1, self.size().height() - 1))

    def odme_fratar_factor(self):
        self.model.estimate_od_fratar()
        self.ui.mv2.load_od_data(self.model.od_estimated)
        self.ui.mv3.load_od_data(self.model.od_diff)

    def odme_leastsq(self):
        pass

    def odme_cmaes(self):
        self.dialog_odme.show()