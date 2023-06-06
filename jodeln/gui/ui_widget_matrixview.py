# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_matrixview.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MatrixView(object):
    def setupUi(self, MatrixView):
        if not MatrixView.objectName():
            MatrixView.setObjectName(u"MatrixView")
        MatrixView.resize(632, 472)
        self.gridLayout = QGridLayout(MatrixView)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tvMarginD = QTableView(MatrixView)
        self.tvMarginD.setObjectName(u"tvMarginD")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tvMarginD.sizePolicy().hasHeightForWidth())
        self.tvMarginD.setSizePolicy(sizePolicy)
        self.tvMarginD.setMaximumSize(QSize(16777215, 120))
        self.tvMarginD.setFrameShape(QFrame.StyledPanel)
        self.tvMarginD.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tvMarginD.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.gridLayout.addWidget(self.tvMarginD, 0, 1, 1, 1)

        self.tvMarginO = QTableView(MatrixView)
        self.tvMarginO.setObjectName(u"tvMarginO")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tvMarginO.sizePolicy().hasHeightForWidth())
        self.tvMarginO.setSizePolicy(sizePolicy1)
        self.tvMarginO.setMaximumSize(QSize(160, 16777215))
        self.tvMarginO.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tvMarginO.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.gridLayout.addWidget(self.tvMarginO, 1, 0, 1, 1)

        self.tvMatrix = QTableView(MatrixView)
        self.tvMatrix.setObjectName(u"tvMatrix")
        self.tvMatrix.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tvMatrix.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.gridLayout.addWidget(self.tvMatrix, 1, 1, 1, 1)

        self.vsbar = QScrollBar(MatrixView)
        self.vsbar.setObjectName(u"vsbar")
        self.vsbar.setOrientation(Qt.Vertical)

        self.gridLayout.addWidget(self.vsbar, 1, 2, 1, 1)

        self.hsbar = QScrollBar(MatrixView)
        self.hsbar.setObjectName(u"hsbar")
        self.hsbar.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.hsbar, 2, 1, 1, 1)


        self.retranslateUi(MatrixView)

        QMetaObject.connectSlotsByName(MatrixView)
    # setupUi

    def retranslateUi(self, MatrixView):
        MatrixView.setWindowTitle(QCoreApplication.translate("MatrixView", u"MatrixView", None))
    # retranslateUi

