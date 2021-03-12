# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_open.ui'
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


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(663, 174)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.leTurns = QLineEdit(Dialog)
        self.leTurns.setObjectName(u"leTurns")

        self.gridLayout.addWidget(self.leTurns, 2, 2, 1, 1)

        self.leSeedOD = QLineEdit(Dialog)
        self.leSeedOD.setObjectName(u"leSeedOD")

        self.gridLayout.addWidget(self.leSeedOD, 4, 2, 1, 1)

        self.leRoutes = QLineEdit(Dialog)
        self.leRoutes.setObjectName(u"leRoutes")

        self.gridLayout.addWidget(self.leRoutes, 3, 2, 1, 1)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 3)

        self.leNodes = QLineEdit(Dialog)
        self.leNodes.setObjectName(u"leNodes")

        self.gridLayout.addWidget(self.leNodes, 0, 2, 1, 1)

        self.leLinks = QLineEdit(Dialog)
        self.leLinks.setObjectName(u"leLinks")

        self.gridLayout.addWidget(self.leLinks, 1, 2, 1, 1)

        self.pbOpenNodes = QPushButton(Dialog)
        self.pbOpenNodes.setObjectName(u"pbOpenNodes")

        self.gridLayout.addWidget(self.pbOpenNodes, 0, 1, 1, 1)

        self.pbOpenLinks = QPushButton(Dialog)
        self.pbOpenLinks.setObjectName(u"pbOpenLinks")

        self.gridLayout.addWidget(self.pbOpenLinks, 1, 1, 1, 1)

        self.pbOpenTurns = QPushButton(Dialog)
        self.pbOpenTurns.setObjectName(u"pbOpenTurns")

        self.gridLayout.addWidget(self.pbOpenTurns, 2, 1, 1, 1)

        self.pbOpenRoutes = QPushButton(Dialog)
        self.pbOpenRoutes.setObjectName(u"pbOpenRoutes")

        self.gridLayout.addWidget(self.pbOpenRoutes, 3, 1, 1, 1)

        self.pbOpenSeedOD = QPushButton(Dialog)
        self.pbOpenSeedOD.setObjectName(u"pbOpenSeedOD")

        self.gridLayout.addWidget(self.pbOpenSeedOD, 4, 1, 1, 1)

        QWidget.setTabOrder(self.leNodes, self.leLinks)
        QWidget.setTabOrder(self.leLinks, self.leTurns)
        QWidget.setTabOrder(self.leTurns, self.leRoutes)
        QWidget.setTabOrder(self.leRoutes, self.leSeedOD)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Open Network", None))
        self.pbOpenNodes.setText(QCoreApplication.translate("Dialog", u"Nodes", None))
        self.pbOpenLinks.setText(QCoreApplication.translate("Dialog", u"Links", None))
        self.pbOpenTurns.setText(QCoreApplication.translate("Dialog", u"Turns", None))
        self.pbOpenRoutes.setText(QCoreApplication.translate("Dialog", u"Routes", None))
        self.pbOpenSeedOD.setText(QCoreApplication.translate("Dialog", u"Seed OD", None))
    # retranslateUi

