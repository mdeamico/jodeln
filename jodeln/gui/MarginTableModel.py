from abc import ABC, ABCMeta, abstractmethod
from PySide2 import QtCore, QtGui
from PySide2.QtCore import Qt

# -------------------------
# Resources:
#   https://stackoverflow.com/questions/28799089/python-abc-multiple-inheritance
#   https://stackoverflow.com/questions/57349105/python-abc-inheritance-with-specified-metaclass
# -------------------------

class QABCMeta(ABCMeta, type(QtCore.QAbstractTableModel)):
    """Metaclass that combines ABC and QtCore.QAbstractTableModel"""
    pass

class MarginTableModel(ABC, metaclass=QABCMeta):
    """Abstract base class to be multi-inherited together with QtCore.QAbstractTableModel"""
    def __init__(self) -> None:
        super().__init__()
        self._data = None
        self.n_rows = 0
        self.n_cols = 0

    @abstractmethod
    def _set_n_rows_and_cols(self):
        ...

    @abstractmethod
    def orientation_stat(self):
        ...
    
    @abstractmethod
    def orientation_zone(self):
        ...
        
    @abstractmethod
    def get_stat_coord(self, index):
        ...

    @abstractmethod
    def get_zone_coord(self, index):
        ...

    def rowCount(self, index) -> int:
        return self.n_rows
    
    def columnCount(self, index) -> int:
        return self.n_cols
    
    def data(self, index, role):
        if role == Qt.TextAlignmentRole:
            return int(Qt.AlignRight | Qt.AlignVCenter)
        
        if role == Qt.DisplayRole:
            stat_coord = self.get_stat_coord(index)
            zone_coord = self.get_zone_coord(index)
            
            if stat_coord == 0:
                return self._data['diff'][zone_coord]
            if stat_coord == 1:
                return self._data['targets'][zone_coord]
            if stat_coord == 2:
                return self._data['sums'][zone_coord]
        
        if (role == Qt.ForegroundRole) and (self.get_stat_coord(index) == 1):
            return QtGui.QColor('purple')

        if (role == Qt.ForegroundRole) and (self.get_stat_coord(index) == 2):
            return QtGui.QColor('blue')
    
    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        if section == 0 and orientation == self.orientation_stat() and role == Qt.DisplayRole:
            return "Δ"
        if section == 1 and orientation == self.orientation_stat() and role == Qt.DisplayRole:
            return "T"
        if section == 2 and orientation == self.orientation_stat() and role == Qt.DisplayRole:
            return "Σ"
        
        if orientation == self.orientation_zone() and role == Qt.DisplayRole:
            return self._data['zone_names'][section]
        
        return super().headerData(section, orientation, role)

    def load_data(self, data):
        self._data = data      
        self._set_n_rows_and_cols()



class OriginMarginModel(MarginTableModel, QtCore.QAbstractTableModel):
    def __init__(self) -> None:
        super().__init__()    

    def _set_n_rows_and_cols(self):
        self.n_rows = len(self._data['sums'])
        self.n_cols = 3

    def orientation_stat(self):
        return Qt.Horizontal
    
    def orientation_zone(self):
        return Qt.Vertical
        
    def get_stat_coord(self, index):
        return index.column()

    def get_zone_coord(self, index):
        return index.row()
    

class DestinationMarginModel(MarginTableModel, QtCore.QAbstractTableModel):
    def __init__(self) -> None:
        super().__init__()    

    def _set_n_rows_and_cols(self):
        self.n_rows = 3
        self.n_cols = len(self._data['sums'])

    def orientation_stat(self):
        return Qt.Vertical
    
    def orientation_zone(self):
        return Qt.Horizontal
        
    def get_stat_coord(self, index):
        return index.row()

    def get_zone_coord(self, index):
        return index.column()