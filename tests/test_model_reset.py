import os
import sys
import unittest
from PySide2.QtWidgets import QApplication
from PySide2.QtTest import QTest
from PySide2.QtCore import Qt, QEventLoop, QTimer
from PySide2.QtWidgets import QDialogButtonBox

from context import jodeln
import jodeln.main
from jodeln.model import Model


def event_loop(msec):
    """Event loop to show the GUI during a unit test. 
    
    https://www.qtcentre.org/threads/23541-Displaying-GUI-events-with-QtTest
    """
    loop = QEventLoop()
    timer = QTimer()
    timer.timeout.connect(loop.quit)
    timer.setSingleShot(True)
    timer.start(msec)
    loop.exec_()

class MainTest(unittest.TestCase):
    def setUp(self) -> None:
        model = Model()
        self.window = jodeln.main.MainWindow(model)
        return super().setUp()

    def test_reset(self):
        net_folder = os.path.join(os.getcwd(), "tests", "networks", "net01")
        self.window.show()
        self.window.ui.actionOpen.trigger()
        self.window.dialog_open.ui.leLinks.setText(os.path.join(net_folder, "links.csv"))
        self.window.dialog_open.ui.leNodes.setText(os.path.join(net_folder, "nodes.csv"))
        QTest.mouseClick(self.window.dialog_open.ui.buttonBox.button(QDialogButtonBox.Ok), Qt.LeftButton)
        self.window.reset()
        self.window.model.reset()
        event_loop(80000)
        self.assertEqual(1, 1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    unittest.main()
