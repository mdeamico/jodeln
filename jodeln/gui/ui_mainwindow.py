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
        MainWindow.resize(897, 494)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QSize(16777215, 800))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.leNodes = QLineEdit(self.centralwidget)
        self.leNodes.setObjectName(u"leNodes")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.leNodes)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.leLinks = QLineEdit(self.centralwidget)
        self.leLinks.setObjectName(u"leLinks")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.leLinks)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.leTurns = QLineEdit(self.centralwidget)
        self.leTurns.setObjectName(u"leTurns")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.leTurns)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_4)

        self.leRoutes = QLineEdit(self.centralwidget)
        self.leRoutes.setObjectName(u"leRoutes")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.leRoutes)

        self.leSeedOD = QLineEdit(self.centralwidget)
        self.leSeedOD.setObjectName(u"leSeedOD")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.leSeedOD)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_5)

        self.pbLoad = QPushButton(self.centralwidget)
        self.pbLoad.setObjectName(u"pbLoad")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.pbLoad)


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
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_6)

        self.leExportFolder = QLineEdit(self.centralwidget)
        self.leExportFolder.setObjectName(u"leExportFolder")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.leExportFolder)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.pbExportRoutes = QPushButton(self.centralwidget)
        self.pbExportRoutes.setObjectName(u"pbExportRoutes")

        self.gridLayout.addWidget(self.pbExportRoutes, 1, 1, 1, 1)

        self.pbEstimateOD = QPushButton(self.centralwidget)
        self.pbEstimateOD.setObjectName(u"pbEstimateOD")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pbEstimateOD.sizePolicy().hasHeightForWidth())
        self.pbEstimateOD.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.pbEstimateOD, 3, 0, 1, 1)

        self.pbExportLinksAndTurnsByOD = QPushButton(self.centralwidget)
        self.pbExportLinksAndTurnsByOD.setObjectName(u"pbExportLinksAndTurnsByOD")

        self.gridLayout.addWidget(self.pbExportLinksAndTurnsByOD, 1, 2, 1, 1)

        self.pbExportTurns = QPushButton(self.centralwidget)
        self.pbExportTurns.setObjectName(u"pbExportTurns")

        self.gridLayout.addWidget(self.pbExportTurns, 1, 0, 1, 1)

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
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.leWeightGEH.sizePolicy().hasHeightForWidth())
        self.leWeightGEH.setSizePolicy(sizePolicy2)

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.leWeightGEH)

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")

        self.formLayout_3.setWidget(2, QFormLayout.LabelRole, self.label_8)

        self.leWeightODSSE = QLineEdit(self.centralwidget)
        self.leWeightODSSE.setObjectName(u"leWeightODSSE")
        sizePolicy2.setHeightForWidth(self.leWeightODSSE.sizePolicy().hasHeightForWidth())
        self.leWeightODSSE.setSizePolicy(sizePolicy2)

        self.formLayout_3.setWidget(2, QFormLayout.FieldRole, self.leWeightODSSE)

        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")

        self.formLayout_3.setWidget(3, QFormLayout.LabelRole, self.label_9)

        self.leWeightRouteRatio = QLineEdit(self.centralwidget)
        self.leWeightRouteRatio.setObjectName(u"leWeightRouteRatio")
        sizePolicy2.setHeightForWidth(self.leWeightRouteRatio.sizePolicy().hasHeightForWidth())
        self.leWeightRouteRatio.setSizePolicy(sizePolicy2)

        self.formLayout_3.setWidget(3, QFormLayout.FieldRole, self.leWeightRouteRatio)


        self.gridLayout.addLayout(self.formLayout_3, 3, 1, 1, 2)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_2, 2, 0, 1, 3)


        self.formLayout_2.setLayout(1, QFormLayout.FieldRole, self.gridLayout)


        self.verticalLayout.addLayout(self.formLayout_2)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gvSchematic = SchematicView(self.centralwidget)
        self.gvSchematic.setObjectName(u"gvSchematic")

        self.gridLayout_2.addWidget(self.gvSchematic, 0, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Jodeln", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Nodes", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Links", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Turns", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Routes", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Seed OD", None))
        self.pbLoad.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Export Folder", None))
        self.pbExportRoutes.setText(QCoreApplication.translate("MainWindow", u"Export List of Routes", None))
        self.pbEstimateOD.setText(QCoreApplication.translate("MainWindow", u"Estimate and Export OD", None))
        self.pbExportLinksAndTurnsByOD.setText(QCoreApplication.translate("MainWindow", u"Export links and turns along each OD", None))
#if QT_CONFIG(tooltip)
        self.pbExportTurns.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.pbExportTurns.setText(QCoreApplication.translate("MainWindow", u"Export List of Turns", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"OD Estimation Objective Function Weights", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Total GEH", None))
        self.leWeightGEH.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"OD SSE", None))
        self.leWeightODSSE.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Route Ratio", None))
        self.leWeightRouteRatio.setText(QCoreApplication.translate("MainWindow", u"1", None))
    # retranslateUi

