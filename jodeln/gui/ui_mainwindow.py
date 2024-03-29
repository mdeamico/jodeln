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
        MainWindow.resize(986, 675)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QSize(16777215, 16777215))
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionSettings = QAction(MainWindow)
        self.actionSettings.setObjectName(u"actionSettings")
        self.actionExport = QAction(MainWindow)
        self.actionExport.setObjectName(u"actionExport")
        self.actionEstimate_OD = QAction(MainWindow)
        self.actionEstimate_OD.setObjectName(u"actionEstimate_OD")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setStyleSheet(u"QSplitter::handle {\n"
"         image: url(:/theme/splitter_handle.png);\n"
"}")
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setHandleWidth(8)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.filterToggle = QToolButton(self.layoutWidget)
        self.filterToggle.setObjectName(u"filterToggle")
        self.filterToggle.setAutoFillBackground(False)
        self.filterToggle.setStyleSheet(u"QToolButton { border: none; }")
        self.filterToggle.setCheckable(True)
        self.filterToggle.setChecked(False)
        self.filterToggle.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.filterToggle.setAutoRaise(False)
        self.filterToggle.setArrowType(Qt.RightArrow)

        self.verticalLayout.addWidget(self.filterToggle)

        self.frame = QFrame(self.layoutWidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.formLayout = QFormLayout(self.frame)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setLayoutDirection(Qt.LeftToRight)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.leFilter1 = QLineEdit(self.frame)
        self.leFilter1.setObjectName(u"leFilter1")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.leFilter1)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.leFilter2 = QLineEdit(self.frame)
        self.leFilter2.setObjectName(u"leFilter2")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.leFilter2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pbFilterApply = QPushButton(self.frame)
        self.pbFilterApply.setObjectName(u"pbFilterApply")

        self.horizontalLayout_2.addWidget(self.pbFilterApply)

        self.pbFilterClear = QPushButton(self.frame)
        self.pbFilterClear.setObjectName(u"pbFilterClear")

        self.horizontalLayout_2.addWidget(self.pbFilterClear)


        self.formLayout.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_2)


        self.verticalLayout.addWidget(self.frame)

        self.tblOD = QTableView(self.layoutWidget)
        self.tblOD.setObjectName(u"tblOD")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tblOD.sizePolicy().hasHeightForWidth())
        self.tblOD.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.tblOD)

        self.splitter.addWidget(self.layoutWidget)
        self.gvSchematic = SchematicView(self.splitter)
        self.gvSchematic.setObjectName(u"gvSchematic")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.gvSchematic.sizePolicy().hasHeightForWidth())
        self.gvSchematic.setSizePolicy(sizePolicy2)
        self.splitter.addWidget(self.gvSchematic)

        self.verticalLayout_2.addWidget(self.splitter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionSettings)
        self.toolBar.addAction(self.actionExport)
        self.toolBar.addAction(self.actionEstimate_OD)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Jodeln", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
#if QT_CONFIG(tooltip)
        self.actionOpen.setToolTip(QCoreApplication.translate("MainWindow", u"Open Network", None))
#endif // QT_CONFIG(tooltip)
        self.actionSettings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
#if QT_CONFIG(tooltip)
        self.actionSettings.setToolTip(QCoreApplication.translate("MainWindow", u"Settings", None))
#endif // QT_CONFIG(tooltip)
        self.actionExport.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.actionEstimate_OD.setText(QCoreApplication.translate("MainWindow", u"Estimate OD", None))
#if QT_CONFIG(tooltip)
        self.actionEstimate_OD.setToolTip(QCoreApplication.translate("MainWindow", u"View and Estimate OD", None))
#endif // QT_CONFIG(tooltip)
        self.filterToggle.setText(QCoreApplication.translate("MainWindow", u"Filter", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Origin", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Destination", None))
        self.pbFilterApply.setText(QCoreApplication.translate("MainWindow", u"Apply Filter", None))
        self.pbFilterClear.setText(QCoreApplication.translate("MainWindow", u"Clear Filter", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

