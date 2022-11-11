# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from .schematic_view import SchematicView

import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(926, 626)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QSize(16777215, 1024))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.pbShowDialogOpen = QPushButton(self.centralwidget)
        self.pbShowDialogOpen.setObjectName(u"pbShowDialogOpen")

        self.horizontalLayout.addWidget(self.pbShowDialogOpen)

        self.pbShowExportDialog = QPushButton(self.centralwidget)
        self.pbShowExportDialog.setObjectName(u"pbShowExportDialog")

        self.horizontalLayout.addWidget(self.pbShowExportDialog)

        self.pbShowODEstimation = QPushButton(self.centralwidget)
        self.pbShowODEstimation.setObjectName(u"pbShowODEstimation")

        self.horizontalLayout.addWidget(self.pbShowODEstimation)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setStyleSheet(u"QSplitter::handle {\n"
"	image: url(:/theme/splitter_handle.png);\n"
"}")
        self.splitter.setFrameShape(QFrame.NoFrame)
        self.splitter.setFrameShadow(QFrame.Plain)
        self.splitter.setLineWidth(1)
        self.splitter.setMidLineWidth(0)
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setOpaqueResize(True)
        self.splitter.setHandleWidth(10)
        self.tblOD = QTableView(self.splitter)
        self.tblOD.setObjectName(u"tblOD")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tblOD.sizePolicy().hasHeightForWidth())
        self.tblOD.setSizePolicy(sizePolicy1)
        self.splitter.addWidget(self.tblOD)
        self.gvSchematic = SchematicView(self.splitter)
        self.gvSchematic.setObjectName(u"gvSchematic")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.gvSchematic.sizePolicy().hasHeightForWidth())
        self.gvSchematic.setSizePolicy(sizePolicy2)
        self.splitter.addWidget(self.gvSchematic)

        self.verticalLayout.addWidget(self.splitter)

        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 5)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Jodeln", None))
        self.pbShowDialogOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.pbShowExportDialog.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.pbShowODEstimation.setText(QCoreApplication.translate("MainWindow", u"OD Estimation", None))
    # retranslateUi

