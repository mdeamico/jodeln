# Contains Qt TableModels for showing OD and route data in tables.

from PySide2 import QtCore
from PySide2.QtCore import Qt, QSortFilterProxyModel

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from PySide2.QtCore import QModelIndex

class RouteInfo(Protocol):
    @property
    def origin(self) -> int:
        ...
    @property
    def destination(self) -> int:
        ...
    @property
    def o_name(self) -> str:
        ...
    @property
    def d_name(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def nodes(self) -> list:
        ...

class ODTableFilterProxyModel(QSortFilterProxyModel):    
    def lessThan(self, left: 'QModelIndex', right: 'QModelIndex'):
        left_data = self.sourceModel().data(left, Qt.DisplayRole)
        right_data = self.sourceModel().data(right, Qt.DisplayRole)

        return left_data < right_data

class ODTableModel(QtCore.QAbstractTableModel):
    """Model for showing a table of OD routes."""
    def __init__(self, route_data: list[RouteInfo]):
        super().__init__()
        self._data = route_data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return self._data[index.row()].o_name
            if index.column() == 1:
                return self._data[index.row()].d_name
            if index.column() == 2:
                return self._data[index.row()].name

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return 3

    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        """Get Table header names."""
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            if section == 0:
                return "Origin"
            if section == 1:
                return "Destination"
            if section == 2:
                return "Route Name"

    def get_route_at_index(self, index):
        """Return routes for the OD at the selected index."""
        route = self._data[index.row()]
        return (route.origin, route.destination, route.name)
