# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *

from .schematic_view import SchematicView


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(917, 712)
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
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.formLayout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setLabelAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.formLayout.setVerticalSpacing(6)
        self.pbShowDialogOpen = QPushButton(self.centralwidget)
        self.pbShowDialogOpen.setObjectName(u"pbShowDialogOpen")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.pbShowDialogOpen)


        self.verticalLayout.addLayout(self.formLayout)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.formLayout_2.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setLabelAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.formLayout_2.setVerticalSpacing(6)
        self.leExportFolder = QLineEdit(self.centralwidget)
        self.leExportFolder.setObjectName(u"leExportFolder")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.leExportFolder)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.pbExportTurns = QPushButton(self.centralwidget)
        self.pbExportTurns.setObjectName(u"pbExportTurns")

        self.gridLayout.addWidget(self.pbExportTurns, 1, 0, 1, 1)

        self.pbExportLinksAndTurnsByOD = QPushButton(self.centralwidget)
        self.pbExportLinksAndTurnsByOD.setObjectName(u"pbExportLinksAndTurnsByOD")

        self.gridLayout.addWidget(self.pbExportLinksAndTurnsByOD, 1, 2, 1, 1)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_2, 2, 0, 1, 3)

        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.formLayout_3.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.label_10 = QLabel(self.centralwidget)
        self.label_10.setObjectName(u"label_10")

        self.formLayout_3.setWidget(0, QFormLayout.SpanningRole, self.label_10)

        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.label_7)

        self.leWeightGEH = QLineEdit(self.centralwidget)
        self.leWeightGEH.setObjectName(u"leWeightGEH")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.leWeightGEH.sizePolicy().hasHeightForWidth())
        self.leWeightGEH.setSizePolicy(sizePolicy1)

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.leWeightGEH)

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")

        self.formLayout_3.setWidget(3, QFormLayout.LabelRole, self.label_8)

        self.leWeightODSSE = QLineEdit(self.centralwidget)
        self.leWeightODSSE.setObjectName(u"leWeightODSSE")
        sizePolicy1.setHeightForWidth(self.leWeightODSSE.sizePolicy().hasHeightForWidth())
        self.leWeightODSSE.setSizePolicy(sizePolicy1)

        self.formLayout_3.setWidget(3, QFormLayout.FieldRole, self.leWeightODSSE)

        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")

        self.formLayout_3.setWidget(4, QFormLayout.LabelRole, self.label_9)

        self.leWeightRouteRatio = QLineEdit(self.centralwidget)
        self.leWeightRouteRatio.setObjectName(u"leWeightRouteRatio")
        sizePolicy1.setHeightForWidth(self.leWeightRouteRatio.sizePolicy().hasHeightForWidth())
        self.leWeightRouteRatio.setSizePolicy(sizePolicy1)

        self.formLayout_3.setWidget(4, QFormLayout.FieldRole, self.leWeightRouteRatio)


        self.gridLayout.addLayout(self.formLayout_3, 3, 1, 1, 2)

        self.pbExportRoutes = QPushButton(self.centralwidget)
        self.pbExportRoutes.setObjectName(u"pbExportRoutes")

        self.gridLayout.addWidget(self.pbExportRoutes, 1, 1, 1, 1)

        self.pbEstimateOD = QPushButton(self.centralwidget)
        self.pbEstimateOD.setObjectName(u"pbEstimateOD")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pbEstimateOD.sizePolicy().hasHeightForWidth())
        self.pbEstimateOD.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.pbEstimateOD, 3, 0, 1, 1)


        self.formLayout_2.setLayout(2, QFormLayout.FieldRole, self.gridLayout)

        self.pbExportFolder = QPushButton(self.centralwidget)
        self.pbExportFolder.setObjectName(u"pbExportFolder")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.pbExportFolder)


        self.verticalLayout.addLayout(self.formLayout_2)

        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setFrameShape(QFrame.NoFrame)
        self.splitter.setFrameShadow(QFrame.Plain)
        self.splitter.setLineWidth(1)
        self.splitter.setMidLineWidth(0)
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setOpaqueResize(True)
        self.splitter.setHandleWidth(10)
        self.tblOD = QTableView(self.splitter)
        self.tblOD.setObjectName(u"tblOD")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.tblOD.sizePolicy().hasHeightForWidth())
        self.tblOD.setSizePolicy(sizePolicy3)
        self.splitter.addWidget(self.tblOD)
        self.gvSchematic = SchematicView(self.splitter)
        self.gvSchematic.setObjectName(u"gvSchematic")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(1)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.gvSchematic.sizePolicy().hasHeightForWidth())
        self.gvSchematic.setSizePolicy(sizePolicy4)
        self.splitter.addWidget(self.gvSchematic)

        self.verticalLayout.addWidget(self.splitter)

        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(3, 5)
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
#if QT_CONFIG(tooltip)
        self.pbExportTurns.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.pbExportTurns.setText(QCoreApplication.translate("MainWindow", u"Export List of Turns", None))
        self.pbExportLinksAndTurnsByOD.setText(QCoreApplication.translate("MainWindow", u"Export links and turns along each OD", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"OD Estimation Objective Function Weights", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Total GEH", None))
        self.leWeightGEH.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"OD SSE", None))
        self.leWeightODSSE.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Route Ratio", None))
        self.leWeightRouteRatio.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.pbExportRoutes.setText(QCoreApplication.translate("MainWindow", u"Export List of Routes", None))
        self.pbEstimateOD.setText(QCoreApplication.translate("MainWindow", u"Estimate and Export OD", None))
        self.pbExportFolder.setText(QCoreApplication.translate("MainWindow", u"Export Folder", None))
    # retranslateUi

