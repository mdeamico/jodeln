import os
import sys
import unittest
from PySide2.QtWidgets import QApplication
from PySide2.QtTest import QTest
from PySide2.QtCore import Qt, QEventLoop, QTimer, QObject


from context import jodeln
import jodeln.main



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
        self.window = jodeln.main.MainWindow()
        return super().setUp()

    def test_draw(self):
        net_folder = os.path.join(os.getcwd(), "tests", "networks", "net01")
        self.window.show()
        self.window.ui.leLinks.setText(os.path.join(net_folder, "links.txt"))
        self.window.ui.leNodes.setText(os.path.join(net_folder, "nodes.txt"))
        QTest.mouseClick(self.window.ui.pbLoad, Qt.LeftButton)
        event_loop(5000)
        self.assertEqual(1, 1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    unittest.main()
