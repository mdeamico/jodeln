from PySide2.QtWidgets import QWidget, QFileDialog

from gui.ui_dialog_open import Ui_Dialog
from dataclasses import dataclass

@dataclass
class FilePathCache():
    """Contains file paths stored in the line edit widgets."""
    nodes: str
    links: str
    turns: str
    routes: str
    seed_od: str


class DialogOpen(QWidget):
    """Dialog to open network files (node file, link file, etc)."""
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        self.data = FilePathCache("", "", "", "", "")

        self.ui.pbOpenNodes.clicked.connect(lambda: self.on_pbOpenClick(self.ui.leNodes, "Load Nodes"))
        self.ui.pbOpenLinks.clicked.connect(lambda: self.on_pbOpenClick(self.ui.leLinks, "Load Links"))
        self.ui.pbOpenTurns.clicked.connect(lambda: self.on_pbOpenClick(self.ui.leTurns, "Load Turns"))
        self.ui.pbOpenRoutes.clicked.connect(lambda: self.on_pbOpenClick(self.ui.leRoutes, "Load Routes"))
        self.ui.pbOpenSeedOD.clicked.connect(lambda: self.on_pbOpenClick(self.ui.leSeedOD, "Load Seed OD"))

    def store_data(self) -> None:
        """Stores current list edit text in self.data.
        
        Cached data is helpful to reset the dialog when the user clicks Cancel.
        """
        self.data = self.get_data()

    def get_data(self) -> FilePathCache:
        """Accessor function to get data from the dialog."""
        return FilePathCache(
                    self.ui.leNodes.text(),
                    self.ui.leLinks.text(),
                    self.ui.leTurns.text(),
                    self.ui.leRoutes.text(),
                    self.ui.leSeedOD.text())

    def accept(self) -> None:
        """User clicks 'ok'."""
        self.close()

    def reject(self) -> None:
        """User clicks 'cancel'."""
        self.ui.leNodes.setText(self.data.nodes)
        self.ui.leLinks.setText(self.data.links)
        self.ui.leTurns.setText(self.data.turns)
        self.ui.leRoutes.setText(self.data.routes)
        self.ui.leSeedOD.setText(self.data.seed_od)
        self.close()
    
    def on_pbOpenClick(self, line_edit, title) -> None:
        """Open a standard file dialog; put file path in line edit."""
        file_path, _ = QFileDialog.getOpenFileName(self, title)
        line_edit.setText(file_path)
