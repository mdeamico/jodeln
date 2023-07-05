from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt

from gui.ui_widget_matrixview import Ui_MatrixView
from gui.MarginTableModel import OriginMarginModel, DestinationMarginModel

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from od.od_matrix import ODMatrix

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self._data: 'ODMatrix' = None
        self.n_rows = 0
        self.n_cols = 0
        self.origins = None
        self.destinations = None

    def data(self, index, role):
        if role == Qt.TextAlignmentRole:
            return int(Qt.AlignRight | Qt.AlignVCenter)
        
        if role == Qt.DisplayRole:
            o = self.origins[index.row()]
            d = self.destinations[index.column()]
            return self._data.volume[(o, d)]
        
        if role == Qt.ForegroundRole:
            o = self.origins[index.row()]
            d = self.destinations[index.column()]
            if self._data.volume[(o, d)] == 0:
                return QtGui.QColor('grey')
        
        if role == Qt.BackgroundRole:
            if index.row() == index.column():
                return QtGui.QColor('lightGrey')


    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return self.names_o[section]
        
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.names_d[section]
        
        return super().headerData(section, orientation, role)

    def rowCount(self, index):
        return self.n_rows

    def columnCount(self, index):
        return self.n_cols
    
    def load_data(self, od_mat: 'ODMatrix'):
        self._data = od_mat
        
        self.origins = od_mat.origins
        self.destinations = od_mat.destinations

        self.names_o = od_mat.names_o
        self.names_d = od_mat.names_d

        self.n_rows = len(self.origins)
        self.n_cols = len(self.destinations)
    

class MatrixView(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui = Ui_MatrixView()
        self.ui.setupUi(self)

        self.od_table = TableModel()
        self.row_margins = OriginMarginModel()
        self.col_margins = DestinationMarginModel()

        # Synchronize vertical scrolling
        self.ui.tvMatrix.verticalScrollBar().valueChanged.connect(self.scroll_vertical)
        self.ui.tvMarginO.verticalScrollBar().valueChanged.connect(self.scroll_vertical)        
        self.ui.vsbar.valueChanged.connect(self.scroll_vertical)

        # Synchronize horizontal scrolling
        self.ui.tvMatrix.horizontalScrollBar().valueChanged.connect(self.scroll_horizontal)
        self.ui.tvMarginD.horizontalScrollBar().valueChanged.connect(self.scroll_horizontal)        
        self.ui.hsbar.valueChanged.connect(self.scroll_horizontal)

    def scroll_vertical(self, value):
        self.ui.tvMarginO.verticalScrollBar().setValue(value)
        self.ui.tvMatrix.verticalScrollBar().setValue(value)
        self.ui.vsbar.setValue(value)

    def scroll_horizontal(self, value):
        self.ui.tvMarginD.horizontalScrollBar().setValue(value)
        self.ui.tvMatrix.horizontalScrollBar().setValue(value)
        self.ui.hsbar.setValue(value)

    def set_header_size(self):

        def set_fixed_resize_mode(table_view):
            """Helper Function for setting the resize mode on a table view."""
            table_view.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
            table_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)

        set_fixed_resize_mode(self.ui.tvMatrix)
        set_fixed_resize_mode(self.ui.tvMarginO)
        set_fixed_resize_mode(self.ui.tvMarginD)

        for i in range(0, 3):
            self.ui.tvMarginO.setColumnWidth(i, 40)

        for i in range(0, self.od_table.n_cols):
            self.ui.tvMatrix.setColumnWidth(i, 40)
            self.ui.tvMarginD.setColumnWidth(i, 40)

        self.ui.tvMarginD.verticalHeader().setFixedWidth(self.ui.tvMatrix.verticalHeader().size().width())

    def load_od_data(self, od_mat: 'ODMatrix'):
        
        self.od_table.load_data(od_mat)
        self.ui.tvMatrix.setModel(self.od_table)

        # Temporary Targets. TODO: get real targets from user input.
        targets_o = [10 * v for _, v in od_mat.sums_o.items()]
        targets_d = [10 * v for _, v in od_mat.sums_d.items()]

        diffs_o = []
        diffs_d = []

        # Compute diff between margin sums and temporary targets. 
        # TODO: compute diff using real targets from user input.
        for i, (k, s) in enumerate(od_mat.sums_o.items()):
            diffs_o.append(s - targets_o[i])

        for i, (k, s) in enumerate(od_mat.sums_d.items()):
            diffs_d.append(s - targets_d[i])

        row_margin = {
            'zone_names': od_mat.names_o,
            'sums': [s for _, s in od_mat.sums_o.items()],
            'targets': targets_o,
            'diff': diffs_o,
        }

        self.row_margins.load_data(row_margin)
        self.ui.tvMarginO.setModel(self.row_margins)

        col_margin = {
            'zone_names': od_mat.names_d,
            'sums': [s for _, s in od_mat.sums_d.items()],
            'targets': targets_d,
            'diff': diffs_d,
        }

        self.col_margins.load_data(col_margin)
        self.ui.tvMarginD.setModel(self.col_margins)

        # Update GUI now that data is shown in the OD table. 
        self.set_header_size()

        
    def resizeEvent(self, event) -> None:
        self.ui.vsbar.setMinimum(self.ui.tvMatrix.verticalScrollBar().minimum())
        self.ui.hsbar.setMinimum(self.ui.tvMatrix.horizontalScrollBar().minimum())
        
        self.ui.vsbar.setMaximum(self.ui.tvMatrix.verticalScrollBar().maximum())
        self.ui.hsbar.setMaximum(self.ui.tvMatrix.horizontalScrollBar().maximum())

        return super().resizeEvent(event)
    