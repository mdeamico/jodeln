from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt

from gui.ui_widget_matrixview import Ui_MatrixView
from gui.MarginTableModel import OriginMarginModel, DestinationMarginModel

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self._data = None
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
            return self._data[(o, d)]
        
        if role == Qt.ForegroundRole:
            o = self.origins[index.row()]
            d = self.destinations[index.column()]
            if self._data[(o, d)] == 0:
                return QtGui.QColor('grey')
        
        if role == Qt.BackgroundRole:
            if index.row() == index.column():
                return QtGui.QColor('lightGrey')


    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return self.o_names[section]
        
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.d_names[section]
        
        return super().headerData(section, orientation, role)

    def rowCount(self, index):
        return self.n_rows

    def columnCount(self, index):
        return self.n_cols
    
    def load_data(self, od_mat, origins, destinations, o_names, d_names):
        self._data = od_mat
        
        self.origins = origins
        self.destinations = destinations

        self.o_names = o_names
        self.d_names = d_names

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

    def load_od_data(self, od_mat, origins, destinations, o_names, d_names):
        
        self.od_table.load_data(od_mat, origins, destinations, o_names, d_names)
        self.ui.tvMatrix.setModel(self.od_table)

        o_sums, d_sums = margin_sums(od_mat, origins, destinations)
        o_sums = [v for _, v in o_sums.items()]
        d_sums = [v for _, v in d_sums.items()]

        o_targets = [10 * v for v in o_sums]
        d_targets = [10 * v for v in d_sums]

        o_diffs = [s - t for s, t in zip(o_sums, o_targets)]
        d_diffs = [s - t for s, t in zip(d_sums, d_targets)]

        row_margin = {
            'zone_names': o_names,
            'sums': o_sums,
            'targets': o_targets,
            'diff': o_diffs,
        }

        self.row_margins.load_data(row_margin)
        self.ui.tvMarginO.setModel(self.row_margins)

        col_margin = {
            'zone_names': d_names,
            'sums': d_sums,
            'targets': d_targets,
            'diff': d_diffs,
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

def margin_sums(od_mat, origins, destinations):
    pass
    origin_sums = dict.fromkeys(origins, 0)
    destination_sums = dict.fromkeys(destinations, 0)

    for (o, d), v in od_mat.items():
        origin_sums[o] += v
        destination_sums[d] += v

    return (origin_sums, destination_sums)
    