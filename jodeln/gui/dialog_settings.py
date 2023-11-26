from PySide2.QtWidgets import QWidget

from gui.ui_dialog_settings import Ui_Dialog

class DialogSettings(QWidget):
    """Dialog to change settings."""
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

    def accept(self) -> None:
        """User clicks 'ok'."""
        self.close()

    def reject(self) -> None:
        """User clicks 'cancel'."""
        self.close()
