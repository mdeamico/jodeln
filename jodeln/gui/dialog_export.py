from PySide2.QtWidgets import QWidget, QFileDialog

from gui.ui_dialog_export import Ui_Dialog

from typing import Protocol

class Model(Protocol):
    def export_turns(self, output_folder):
        ...
    def export_node_sequence(self, output_folder):
        ...
    def export_route_list(self, output_folder):
        ...


class DialogExport(QWidget):
    """Dialog for exporting list of turns, paths, etc."""
    def __init__(self, model: Model):

        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        self.model = model

        self.ui.pbExportLinksAndTurnsByOD.clicked.connect(self.export_node_sequence)
        self.ui.pbExportRoutes.clicked.connect(self.export_routes)
        self.ui.pbExportTurns.clicked.connect(self.export_turns)

        self.ui.pbExportFolder.clicked.connect(self.on_pbExportFolder_click)

    def reject(self) -> None:
        """User clicks close."""
        self.close()

    def on_pbExportFolder_click(self) -> None:
        """Open a standard file dialog for selecting the export folder."""
        export_folder = QFileDialog.getExistingDirectory(
            self, "Select Export Folder", 
            "",
            options=QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)

        self.ui.leExportFolder.setText(export_folder)

    def export_turns(self):
        self.model.export_turns(self.ui.leExportFolder.text())

    def export_node_sequence(self):
        self.model.export_node_sequence(self.ui.leExportFolder.text())
    
    def export_routes(self):
        self.model.export_route_list(self.ui.leExportFolder.text())
        