# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_odme.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(459, 196)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_11 = QLabel(Dialog)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout.addWidget(self.label_11, 0, 0, 1, 3)

        self.label_12 = QLabel(Dialog)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout.addWidget(self.label_12, 1, 0, 1, 1)

        self.leWeightGEH = QLineEdit(Dialog)
        self.leWeightGEH.setObjectName(u"leWeightGEH")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leWeightGEH.sizePolicy().hasHeightForWidth())
        self.leWeightGEH.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.leWeightGEH, 1, 1, 1, 2)

        self.label_13 = QLabel(Dialog)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout.addWidget(self.label_13, 2, 0, 1, 1)

        self.leWeightODSSE = QLineEdit(Dialog)
        self.leWeightODSSE.setObjectName(u"leWeightODSSE")
        sizePolicy.setHeightForWidth(self.leWeightODSSE.sizePolicy().hasHeightForWidth())
        self.leWeightODSSE.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.leWeightODSSE, 2, 1, 1, 2)

        self.label_14 = QLabel(Dialog)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout.addWidget(self.label_14, 3, 0, 1, 1)

        self.leWeightRouteRatio = QLineEdit(Dialog)
        self.leWeightRouteRatio.setObjectName(u"leWeightRouteRatio")
        sizePolicy.setHeightForWidth(self.leWeightRouteRatio.sizePolicy().hasHeightForWidth())
        self.leWeightRouteRatio.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.leWeightRouteRatio, 3, 1, 1, 2)

        self.pbExportFolder = QPushButton(Dialog)
        self.pbExportFolder.setObjectName(u"pbExportFolder")

        self.gridLayout.addWidget(self.pbExportFolder, 4, 0, 1, 2)

        self.leExportFolder = QLineEdit(Dialog)
        self.leExportFolder.setObjectName(u"leExportFolder")

        self.gridLayout.addWidget(self.leExportFolder, 4, 2, 1, 1)

        self.pbEstimateOD = QPushButton(Dialog)
        self.pbEstimateOD.setObjectName(u"pbEstimateOD")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pbEstimateOD.sizePolicy().hasHeightForWidth())
        self.pbEstimateOD.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.pbEstimateOD, 5, 0, 1, 3)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Close)

        self.gridLayout.addWidget(self.buttonBox, 6, 0, 1, 3)


        self.retranslateUi(Dialog)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Estimate OD", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"OD Estimation Objective Function Weights", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"Total GEH", None))
        self.leWeightGEH.setText(QCoreApplication.translate("Dialog", u"1", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"OD SSE", None))
        self.leWeightODSSE.setText(QCoreApplication.translate("Dialog", u"1", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"Route Ratio", None))
        self.leWeightRouteRatio.setText(QCoreApplication.translate("Dialog", u"1", None))
        self.pbExportFolder.setText(QCoreApplication.translate("Dialog", u"Export Folder", None))
        self.pbEstimateOD.setText(QCoreApplication.translate("Dialog", u"Estimate and Export OD", None))
    # retranslateUi

