# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_odme_leastsq.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_DialogODME_LeastSq(object):
    def setupUi(self, DialogODME_LeastSq):
        if not DialogODME_LeastSq.objectName():
            DialogODME_LeastSq.setObjectName(u"DialogODME_LeastSq")
        DialogODME_LeastSq.resize(466, 319)
        self.verticalLayout_2 = QVBoxLayout(DialogODME_LeastSq)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(DialogODME_LeastSq)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QSize(125, 16777215))

        self.horizontalLayout.addWidget(self.label)

        self.leSeedODWeight = QLineEdit(DialogODME_LeastSq)
        self.leSeedODWeight.setObjectName(u"leSeedODWeight")
        self.leSeedODWeight.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.leSeedODWeight)

        self.pbRunOdme = QPushButton(DialogODME_LeastSq)
        self.pbRunOdme.setObjectName(u"pbRunOdme")

        self.horizontalLayout.addWidget(self.pbRunOdme)

        self.pbClose = QPushButton(DialogODME_LeastSq)
        self.pbClose.setObjectName(u"pbClose")

        self.horizontalLayout.addWidget(self.pbClose)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_2 = QLabel(DialogODME_LeastSq)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.verticalLayout.addWidget(self.label_2)

        self.txtDiagnostics = QTextEdit(DialogODME_LeastSq)
        self.txtDiagnostics.setObjectName(u"txtDiagnostics")
        font = QFont()
        font.setFamily(u"Consolas")
        self.txtDiagnostics.setFont(font)
        self.txtDiagnostics.setFrameShape(QFrame.Box)
        self.txtDiagnostics.setFrameShadow(QFrame.Sunken)
        self.txtDiagnostics.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.txtDiagnostics.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.txtDiagnostics.setReadOnly(True)

        self.verticalLayout.addWidget(self.txtDiagnostics)


        self.verticalLayout_2.addLayout(self.verticalLayout)

#if QT_CONFIG(shortcut)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(DialogODME_LeastSq)

        QMetaObject.connectSlotsByName(DialogODME_LeastSq)
    # setupUi

    def retranslateUi(self, DialogODME_LeastSq):
        DialogODME_LeastSq.setWindowTitle(QCoreApplication.translate("DialogODME_LeastSq", u"Least Squares OD Matrix Estimation", None))
        self.label.setText(QCoreApplication.translate("DialogODME_LeastSq", u"Seed OD Matrix Weight", None))
        self.leSeedODWeight.setText(QCoreApplication.translate("DialogODME_LeastSq", u"0.5", None))
        self.pbRunOdme.setText(QCoreApplication.translate("DialogODME_LeastSq", u"Estimate OD", None))
        self.pbClose.setText(QCoreApplication.translate("DialogODME_LeastSq", u"Close", None))
        self.label_2.setText(QCoreApplication.translate("DialogODME_LeastSq", u"Diagnostics", None))
    # retranslateUi

