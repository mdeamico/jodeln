from PySide2.QtWidgets import QWidget, QFileDialog

from gui.ui_dialog_export import Ui_Dialog



class DialogExport(QWidget):
    """Dialog for exporting list of turns, paths, etc."""
    def __init__(self, 
                 cb_export_links_and_turns_by_od, 
                 cb_export_routes,
                 cb_export_turns):

        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        self.ui.pbExportLinksAndTurnsByOD.clicked.connect(lambda: cb_export_links_and_turns_by_od(self.ui.leExportFolder.text()))
        self.ui.pbExportRoutes.clicked.connect(lambda: cb_export_routes(self.ui.leExportFolder.text()))
        self.ui.pbExportTurns.clicked.connect(lambda: cb_export_turns(self.ui.leExportFolder.text()))

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