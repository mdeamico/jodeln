# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_od_view.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from gui.widget_matrixview import MatrixView


class Ui_ODView(object):
    def setupUi(self, ODView):
        if not ODView.objectName():
            ODView.setObjectName(u"ODView")
        ODView.resize(819, 528)
        self.actionODME_fratar = QAction(ODView)
        self.actionODME_fratar.setObjectName(u"actionODME_fratar")
        self.actionODME_cmaes = QAction(ODView)
        self.actionODME_cmaes.setObjectName(u"actionODME_cmaes")
        self.actionODME_leastsq = QAction(ODView)
        self.actionODME_leastsq.setObjectName(u"actionODME_leastsq")
        self.centralwidget = QWidget(ODView)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabPosition(QTabWidget.North)
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tabSeed = QWidget()
        self.tabSeed.setObjectName(u"tabSeed")
        self.gridLayout = QGridLayout(self.tabSeed)
        self.gridLayout.setObjectName(u"gridLayout")
        self.mv1 = MatrixView(self.tabSeed)
        self.mv1.setObjectName(u"mv1")

        self.gridLayout.addWidget(self.mv1, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tabSeed, "")
        self.tabEst = QWidget()
        self.tabEst.setObjectName(u"tabEst")
        self.gridLayout_2 = QGridLayout(self.tabEst)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.mv2 = MatrixView(self.tabEst)
        self.mv2.setObjectName(u"mv2")

        self.gridLayout_2.addWidget(self.mv2, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tabEst, "")
        self.tabDiff = QWidget()
        self.tabDiff.setObjectName(u"tabDiff")
        self.gridLayout_4 = QGridLayout(self.tabDiff)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.mv3 = MatrixView(self.tabDiff)
        self.mv3.setObjectName(u"mv3")

        self.gridLayout_4.addWidget(self.mv3, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tabDiff, "")

        self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 1, 1)

        ODView.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(ODView)
        self.statusbar.setObjectName(u"statusbar")
        ODView.setStatusBar(self.statusbar)
        self.menuBar = QMenuBar(ODView)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 819, 21))
        self.menuODME = QMenu(self.menuBar)
        self.menuODME.setObjectName(u"menuODME")
        ODView.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuODME.menuAction())
        self.menuODME.addAction(self.actionODME_fratar)
        self.menuODME.addAction(self.actionODME_leastsq)
        self.menuODME.addAction(self.actionODME_cmaes)

        self.retranslateUi(ODView)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(ODView)
    # setupUi

    def retranslateUi(self, ODView):
        ODView.setWindowTitle(QCoreApplication.translate("ODView", u"OD Matrix", None))
        self.actionODME_fratar.setText(QCoreApplication.translate("ODView", u"Bi-proportional matrix factoring (Fratar Method)", None))
        self.actionODME_cmaes.setText(QCoreApplication.translate("ODView", u"CMA-ES Method", None))
        self.actionODME_leastsq.setText(QCoreApplication.translate("ODView", u"Least Squares Method", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSeed), QCoreApplication.translate("ODView", u"Seed Matrix", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabEst), QCoreApplication.translate("ODView", u"Estimated Matrix", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabDiff), QCoreApplication.translate("ODView", u"Diff Matrix", None))
        self.menuODME.setTitle(QCoreApplication.translate("ODView", u"Estimate OD", None))
    # retranslateUi

