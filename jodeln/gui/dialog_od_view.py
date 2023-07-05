from PySide2.QtWidgets import QMainWindow
from PySide2.QtCore import QSize

from gui.ui_dialog_od_view import Ui_ODView


class DialogODView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ODView()
        self.ui.setupUi(self)

        self.ui.tabWidget.currentChanged.connect(self.tab_changed)
        self.ui.actionFratar.triggered.connect(self.fratar_factor)

    def load_od_data(self, od_seed, od_estimated, od_diff):
        self.ui.mv1.load_od_data(od_seed)
        self.ui.mv2.load_od_data(od_estimated)
        self.ui.mv3.load_od_data(od_diff)

        
    def tab_changed(self, index):
        """Hack to force MatrixView widgets to show/hide their scrollbars as needed.
        
        Without this hack, MatrixView widgets will show their scrollbars if the
        widgets are not on the initial tab shown by the dialog loads.
        """
        self.resize(QSize(self.size().width() + 1, self.size().height() + 1))
        self.resize(QSize(self.size().width() - 1, self.size().height() - 1))

    def fratar_factor(self):
        print(f"Placeholder for Fratar Factor Estimation.")