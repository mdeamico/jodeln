# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_settings.ui'
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
        Dialog.resize(254, 93)
        self.formLayout = QFormLayout(Dialog)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.spnNodeSize = QSpinBox(Dialog)
        self.spnNodeSize.setObjectName(u"spnNodeSize")
        self.spnNodeSize.setMaximumSize(QSize(50, 16777215))
        self.spnNodeSize.setMinimum(1)
        self.spnNodeSize.setValue(10)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.spnNodeSize)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.spnNodeLabelSize = QSpinBox(Dialog)
        self.spnNodeLabelSize.setObjectName(u"spnNodeLabelSize")
        self.spnNodeLabelSize.setMaximumSize(QSize(50, 16777215))
        self.spnNodeLabelSize.setMinimum(1)
        self.spnNodeLabelSize.setValue(14)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.spnNodeLabelSize)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.formLayout.setWidget(2, QFormLayout.SpanningRole, self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Settings", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Node Size", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Node Label Size", None))
    # retranslateUi

