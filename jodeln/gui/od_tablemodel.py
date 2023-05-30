# Contains Qt TableModels for showing OD and route data in tables.
import re
from enum import Enum

from PySide2 import QtCore
from PySide2.QtCore import Qt, QSortFilterProxyModel

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from PySide2.QtCore import QModelIndex

class TableCol(Enum):
    ORIGIN = 0
    DESTINATION = 1
    ROUTE_NAME = 2

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
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.re_origin = None
        self.re_destination = None


    def lessThan(self, left: 'QModelIndex', right: 'QModelIndex'):
        left_data = self.sourceModel().data(left, Qt.DisplayRole)
        right_data = self.sourceModel().data(right, Qt.DisplayRole)

        return left_data < right_data
    
    def apply_filter(self, regex_origin, regex_destination):
        self.re_origin = re.compile(regex_origin)
        self.re_destination = re.compile(regex_destination)
        if regex_origin == "" and regex_destination == "":
            self.setFilterRegExp("")
        else:
            self.setFilterRegExp("dummy")

    def filterAcceptsRow(self, source_row: int, source_parent: 'QModelIndex') -> bool:
        if self.filterRegExp() == "":
            return super().filterAcceptsRow(source_row, source_parent)
        
        index_origin = self.sourceModel().index(source_row, TableCol.ORIGIN, source_parent)
        index_destination = self.sourceModel().index(source_row, TableCol.DESTINATION, source_parent)

        origin_match = bool(
            self.re_origin.search(
                self.sourceModel().data(index_origin, Qt.DisplayRole)))

        destination_match = bool(
            self.re_destination.search(
                self.sourceModel().data(index_destination, Qt.DisplayRole)))
        
        return (origin_match and destination_match)
        


class ODTableModel(QtCore.QAbstractTableModel):
    """Model for showing a table of OD routes."""
    def __init__(self, route_data: list[RouteInfo]):
        super().__init__()
        self._data = route_data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            if index.column() == TableCol.ORIGIN:
                return self._data[index.row()].o_name
            if index.column() == TableCol.DESTINATION:
                return self._data[index.row()].d_name
            if index.column() == TableCol.ROUTE_NAME:
                return self._data[index.row()].name

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return 3

    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        """Get Table header names."""
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            if section == TableCol.ORIGIN:
                return "Origin"
            if section == TableCol.DESTINATION:
                return "Destination"
            if section == TableCol.ROUTE_NAME:
                return "Route Name"

    def get_route_at_index(self, index):
        """Return routes for the OD at the selected index."""
        route = self._data[index.row()]
        return (route.origin, route.destination, route.name)
