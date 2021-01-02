# Contains Qt TableModels for showing OD and route data in tables.

from PySide2 import QtCore
from PySide2.QtCore import Qt


class ODTableModel(QtCore.QAbstractTableModel):
    """Model for showing a table of OD routes."""
    def __init__(self, data):
        super(ODTableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return self._data[index.row()]['o_name']
            if index.column() == 1:
                return self._data[index.row()]['d_name']
            if index.column() == 2:
                return self._data[index.row()]['route']
            if index.column() == 3:
                return str(self._data[index.row()]['nodes'])

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return 4

    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        """Get Table header names."""
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            if section == 0:
                return "Origin"
            if section == 1:
                return "Destination"
            if section == 2:
                return "Route Name"
            if section == 3:
                return "Nodes"

    def get_routes_from_OD(self, index):
        """Return routes for the OD at the selected index."""
        od = self._data[index.row()]
        return (od['origin'], od['destination'], od['route'])
