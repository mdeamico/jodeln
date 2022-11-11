import sys
from PySide2.QtWidgets import QApplication

from model import Model

from gui.mainwindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Model in Model-View-Controller framework.
    model = Model()

    # MainWindow acts as View/Controller
    window = MainWindow(model)
    window.show()

    sys.exit(app.exec_())
